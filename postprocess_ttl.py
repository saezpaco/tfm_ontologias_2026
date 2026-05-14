#!/usr/bin/env python3
"""
postprocess_ttl.py
──────────────────
Post-procesa los .ttl generados por los experimentos E1/E2/E3 aplicando dos
fixes mecánicos:

  1. **auto-prefix injection** — inyecta declaraciones ``@prefix`` para los
     prefijos que el TTL usa pero no declara (ej.: usa ``dc:hasVersion`` y
     olvida ``@prefix dc:``).
  2. **local-name escaping** — reescribe los tokens ``prefix:local`` en los
     que ``local`` contiene caracteres no permitidos por la spec Turtle
     (``!``, ``#``, ``@``, ``(``, ``)``, ``,``, ``;``, ``=`` …) como IRI
     absoluta entre ``<>`` para que el parser no se rompa.

El objetivo es cuantificar cuánto del fallo de parseo es *puramente
sintáctico* (recuperable sin llamar a la API) frente a *errores
semánticos* del modelo.

Prefijos canónicos
------------------
Cubre los más usados en el dominio cisreg + bioinformática estándar.
Si el TTL declara su propia URI para un prefijo, NO se sobrescribe.

Uso
---
    # Procesar un único archivo
    python scripts/postprocess_ttl.py --input results/E3/FANTOM5/gpt-4o/ontology_run1.ttl \\
                                       --output /tmp/run1_fixed.ttl

    # Procesar todos los E1/E2/E3 (gpt-4o) en bloque
    python scripts/postprocess_ttl.py --batch
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT_ROOT / "results"

# Prefijos canónicos (los URIs los hemos extraído de las ontologías cisreg
# y de los vocabularios estándar bioinformáticos).
CANONICAL_PREFIXES: dict[str, str] = {
    "rdf":         "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs":        "http://www.w3.org/2000/01/rdf-schema#",
    "owl":         "http://www.w3.org/2002/07/owl#",
    "xsd":         "http://www.w3.org/2001/XMLSchema#",
    "skos":        "http://www.w3.org/2004/02/skos/core#",
    "dc":          "http://purl.org/dc/terms/",
    "dcterms":     "http://purl.org/dc/terms/",
    "dce":         "http://purl.org/dc/elements/1.1/",
    "obo":         "http://purl.obolibrary.org/obo/",
    "biolink":     "https://w3id.org/biolink/vocab/",
    "schema":      "http://schema.org/",
    "sio":         "http://semanticscience.org/resource/",
    "ncbigene":    "http://identifiers.org/ncbigene/",
    "id_ncbigene": "http://identifiers.org/ncbigene/",
    "pubmed":      "http://www.ncbi.nlm.nih.gov/pubmed/",
    "id_pubmed":   "http://identifiers.org/pubmed/",
    "nuccore":     "https://www.ncbi.nlm.nih.gov/nuccore/",
    "assembly":    "https://www.ncbi.nlm.nih.gov/assembly/",
    "hgnc":        "http://identifiers.org/hgnc/",
    "ensembl":     "http://identifiers.org/ensembl/",
    "uniprot":     "http://purl.uniprot.org/uniprot/",
    "go":          "http://purl.obolibrary.org/obo/GO_",
    "so":          "http://purl.obolibrary.org/obo/SO_",
    "doid":        "http://purl.obolibrary.org/obo/DOID_",
    "mondo":       "http://purl.obolibrary.org/obo/MONDO_",
    "chebi":       "http://purl.obolibrary.org/obo/CHEBI_",
    "hp":          "http://purl.obolibrary.org/obo/HP_",
    "ncbitaxon":   "http://purl.obolibrary.org/obo/NCBITaxon_",
    "foaf":        "http://xmlns.com/foaf/0.1/",
    "prov":        "http://www.w3.org/ns/prov#",
    "void":        "http://rdfs.org/ns/void#",
    # Vocabularios que aparecen en outputs de modelos open-source
    "linkml":      "https://w3id.org/linkml/",
    "linkml_meta": "https://w3id.org/linkml/meta/",
    "pav":         "http://purl.org/pav/",
    "ro":          "http://www.obolibrary.org/obo/ro.owl#",
    "iao":         "http://purl.obolibrary.org/obo/iao.owl#",
    "uberon":      "http://purl.obolibrary.org/obo/UBERON_",
    "cl":          "http://purl.obolibrary.org/obo/CL_",
    "edam":        "http://edamontology.org/",
    "efo":         "http://www.ebi.ac.uk/efo/",
    "doi":         "https://doi.org/",
    "orcid":       "https://orcid.org/",
    # Prefijos del dominio cisreg/biogateway propios de los esquemas E3
    "hcrm":        "http://rdf.biogateway.eu/crm/9606/",
    "crm":         "http://rdf.biogateway.eu/crm/",
    "crm2pgene":   "http://rdf.biogateway.eu/crm2pgene/",
    "crm2gene":    "http://rdf.biogateway.eu/crm2gene/",
    "crm2phen":    "http://rdf.biogateway.eu/crm2phen/",
    "crm2tfac":    "http://rdf.biogateway.eu/crm2tfac/",
    "hgene":       "http://rdf.biogateway.eu/gene/9606/",
    "dbsuper":     "https://asntech.org/dbsuper/",
    "fantom":      "https://fantom.gsc.riken.jp/5/",
    "hacer":       "http://bioinfo.vanderbilt.edu/AE/HACER/",
    # Prefijo vacío por defecto (E1/E2 lo usan a menudo sin declarar)
    "":            "http://example.org/ontology/",
}

# Patrones para detectar prefijos
RE_DECLARED = re.compile(
    r"^\s*@prefix\s+([A-Za-z_][\w\-]*)?\s*:\s*<([^>]+)>\s*\.\s*$",
    re.MULTILINE,
)
RE_USED = re.compile(r"(?<![A-Za-z_:])([A-Za-z_][\w\-]*)?:[A-Za-z_][\w\-]*")


def declared_prefixes(ttl: str) -> set[str]:
    """Devuelve el conjunto de prefijos declarados (incluye '' para el default)."""
    return {m.group(1) or "" for m in RE_DECLARED.finditer(ttl)}


def used_prefixes(ttl: str) -> set[str]:
    """Conjunto de prefijos usados como ``foo:bar``.

    Excluye URIs absolutas (``<http://...>``) y comentarios (``# ...``)."""
    used: set[str] = set()
    for line in ttl.splitlines():
        # Quita comentarios fuera de literales (heurística: '#' no entre comillas)
        if "#" in line:
            in_str = False
            cut = len(line)
            for i, ch in enumerate(line):
                if ch in ('"', "'"):
                    in_str = not in_str
                if ch == "#" and not in_str:
                    cut = i
                    break
            line = line[:cut]
        # Elimina URIs absolutas para no capturar 'http:' como prefijo
        line = re.sub(r"<[^>]*>", "", line)
        # Elimina literales con escape de comillas (heurística)
        line = re.sub(r'"[^"]*"', '""', line)
        for m in RE_USED.finditer(line):
            pref = m.group(1) or ""
            # Saltar palabras reservadas Turtle que llevan ':' pero NO son prefijos
            # (no aplica realmente aquí, pero por seguridad: 'a' no se captura)
            used.add(pref)
    return used


def inject_prefixes(ttl: str) -> tuple[str, list[str], list[str]]:
    """Inserta @prefix declarations para los prefijos usados pero no declarados.

    Devuelve (texto_corregido, prefijos_añadidos, prefijos_no_resueltos).
    """
    declared = declared_prefixes(ttl)
    used = used_prefixes(ttl)
    missing = used - declared
    added: list[str] = []
    unresolved: list[str] = []
    new_decls: list[str] = []

    for pref in sorted(missing):
        if pref in CANONICAL_PREFIXES:
            new_decls.append(f"@prefix {pref}: <{CANONICAL_PREFIXES[pref]}> .")
            added.append(pref)
        else:
            unresolved.append(pref)

    if not new_decls:
        return ttl, [], unresolved

    # Insertar al inicio del bloque de prefijos existente, o al inicio absoluto.
    lines = ttl.splitlines(keepends=False)
    insert_at = 0
    for i, ln in enumerate(lines):
        if ln.strip().startswith("@prefix") or ln.strip().startswith("@base"):
            insert_at = i + 1
        elif ln.strip() == "" and insert_at > 0:
            continue
        elif insert_at > 0:
            break
    fixed = "\n".join(lines[:insert_at] + new_decls + lines[insert_at:])
    if not fixed.endswith("\n"):
        fixed += "\n"
    return fixed, added, unresolved


# Caracteres que NO son válidos en un PN_LOCAL Turtle sin escape (\\X) y
# que, si aparecen, hacen que rdflib lance "Bad syntax (EOF found in middle
# of path syntax)". Lista basada en la gramática W3C de Turtle 1.1.
# IMPORTANTE: '(' y ')' NO se incluyen aquí aunque la spec los permita con
# escape, porque en Turtle son delimitadores de listas de colección
# (rdf:List). Si capturáramos un local name terminado en ')' romperíamos
# expresiones legítimas como `owl:unionOf ( obo:A obo:B )`.
INVALID_PN_LOCAL_CHARS = set("!#@*+,;=?$&'~")

# Mapa de prefijos declarados en un TTL → URI base (extraído del propio TTL).
def get_prefix_map(ttl: str) -> dict[str, str]:
    return {(m.group(1) or ""): m.group(2)
            for m in RE_DECLARED.finditer(ttl)}


# Token sospechoso: prefix:localname con al menos un carácter problemático en
# el local. Excluye URIs absolutas (entre <>), literales y comentarios. NO
# admitimos ',', ';', '(' ni ')' dentro del local porque son separadores
# Turtle (separadores de objetos/predicados, listas de colección).
RE_SUSPECT_TOKEN = re.compile(
    r"(?<![<\"\w/])"
    r"([A-Za-z_][\w\-]*)?"           # prefix (puede ser vacío)
    r":"
    r"([A-Za-z0-9_][\w\-./%@!#*+=?$&'~]*)"
    r"(?=[\s\.,;\]\)]|$)",
)


def escape_local_names(ttl: str) -> tuple[str, int]:
    """Reescribe ``prefix:local`` con caracteres especiales como IRI absoluta.

    Devuelve (texto_corregido, n_reemplazos).
    """
    prefix_map = get_prefix_map(ttl)
    n = 0

    def fix_token(match: "re.Match[str]") -> str:
        nonlocal n
        pref = match.group(1) or ""
        local = match.group(2)
        # Solo intervenimos si hay caracteres realmente problemáticos
        if not any(c in INVALID_PN_LOCAL_CHARS for c in local):
            return match.group(0)
        # Necesitamos la URI del prefijo (declarado o canónico)
        base = prefix_map.get(pref) or CANONICAL_PREFIXES.get(pref)
        if not base:
            return match.group(0)
        n += 1
        return f"<{base}{local}>"

    # Procesar línea a línea, ignorando lo que esté dentro de literales o
    # de IRIs absolutas.
    out_lines: list[str] = []
    for line in ttl.splitlines(keepends=False):
        # Saltamos líneas que sean declaración @prefix o @base
        stripped = line.lstrip()
        if stripped.startswith("@prefix") or stripped.startswith("@base"):
            out_lines.append(line)
            continue
        # Heurística simple: protegemos URIs absolutas <...> reemplazándolas
        # por placeholders y restaurándolas al final.
        protected: list[str] = []
        def _hide_iri(m: "re.Match[str]") -> str:
            protected.append(m.group(0))
            return f"\x00IRI{len(protected)-1}\x00"
        prot_line = re.sub(r"<[^>]*>", _hide_iri, line)
        # Misma protección para literales con comillas
        def _hide_lit(m: "re.Match[str]") -> str:
            protected.append(m.group(0))
            return f"\x00LIT{len(protected)-1}\x00"
        prot_line = re.sub(r'"(?:[^"\\]|\\.)*"', _hide_lit, prot_line)
        # Aplicamos el fix de tokens
        prot_line = RE_SUSPECT_TOKEN.sub(fix_token, prot_line)
        # Restauramos
        for i, p in enumerate(protected):
            prot_line = prot_line.replace(f"\x00IRI{i}\x00", p)
            prot_line = prot_line.replace(f"\x00LIT{i}\x00", p)
        out_lines.append(prot_line)
    return "\n".join(out_lines) + ("\n" if ttl.endswith("\n") else ""), n


def process_file(src: Path, dst: Path) -> dict:
    """Procesa un .ttl. Devuelve métricas del fix."""
    txt = src.read_text(encoding="utf-8", errors="ignore")
    fixed, added, unresolved = inject_prefixes(txt)
    fixed, n_escaped = escape_local_names(fixed)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(fixed, encoding="utf-8")
    return {
        "src":          str(src.relative_to(PROJECT_ROOT)),
        "dst":          str(dst.relative_to(PROJECT_ROOT)),
        "size_before":  src.stat().st_size,
        "size_after":   dst.stat().st_size,
        "added":        added,
        "unresolved":   unresolved,
        "n_escaped":    n_escaped,
    }


try:
    from rdflib import Graph as _RDFG  # noqa: F401
    HAS_RDFLIB = True
    # Silenciar los warnings ruidosos de rdflib sobre literales mal tipados
    # (p. ej. "start_position"^^xsd:integer). Son alucinaciones del LLM, no
    # errores del script — los registramos vía parse_ok=0 y seguimos.
    import logging as _logging
    import warnings as _warnings
    _logging.getLogger("rdflib").setLevel(_logging.ERROR)
    _logging.getLogger("rdflib.term").setLevel(_logging.CRITICAL)
    _warnings.filterwarnings("ignore", module=r"rdflib(\..*)?")
except ImportError:
    HAS_RDFLIB = False


def parse_ok(path: Path) -> int:
    """Comprueba si rdflib parsea el TTL. -1 si rdflib no está disponible.
    Captura todas las excepciones (incluidos warnings → tracebacks emitidos
    por rdflib durante la conversión de literales)."""
    if not HAS_RDFLIB:
        return -1
    try:
        from rdflib import Graph
        g = Graph()
        # rdflib emite tracebacks por stderr para literales mal tipados,
        # pero no lanza excepción. Solo nos interesa el resultado del parse.
        g.parse(str(path), format="turtle")
        return 1
    except Exception:
        return 0


def batch_process(experiments: list[str], model: str = "gpt-4o") -> list[dict]:
    """Procesa todos los .ttl de los experimentos indicados."""
    rows: list[dict] = []
    for exp in experiments:
        exp_dir = RESULTS / exp
        if not exp_dir.is_dir():
            print(f"[skip] {exp_dir} no existe", file=sys.stderr)
            continue
        for ttl in sorted(exp_dir.glob(f"*/{model}/ontology_run*.ttl")):
            rel = ttl.relative_to(RESULTS / exp)
            dst = RESULTS / exp / rel.parent / "postprocessed" / ttl.name
            try:
                r = process_file(ttl, dst)
            except Exception as e:                                   # noqa
                # Aislar fallos por archivo para no detener el batch
                print(f"  [WARN] process_file falló en {ttl.name}: "
                      f"{type(e).__name__}: {str(e)[:200]}",
                      file=sys.stderr)
                r = {"src": str(ttl.relative_to(PROJECT_ROOT)),
                     "dst": "", "size_before": ttl.stat().st_size,
                     "size_after": 0, "added": [], "unresolved": [],
                     "n_escaped": 0,
                     "process_error": f"{type(e).__name__}: {e}"}
            r["experiment"]   = exp
            r["db"]           = ttl.parent.parent.name
            r["run"]          = ttl.stem.replace("ontology_run", "")
            r["parse_before"] = parse_ok(ttl)
            r["parse_after"]  = parse_ok(dst) if dst.exists() else -1
            rows.append(r)
            tag = (f"parse {r['parse_before']}→{r['parse_after']}"
                   if HAS_RDFLIB else "parse=N/A (rdflib no instalado)")
            print(f"[{exp}/{r['db']}/run{r['run']}] {tag}  "
                  f"+prefixes: {r['added']}"
                  + (f"  unresolved: {r['unresolved']}"
                     if r['unresolved'] else ""))
    return rows


def write_report(rows: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    import csv
    fields = ["experiment", "db", "run", "parse_before", "parse_after",
              "added", "unresolved", "n_escaped",
              "size_before", "size_after", "src", "dst"]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r2 = dict(r)
            r2["added"] = ",".join(r["added"])
            r2["unresolved"] = ",".join(r["unresolved"])
            w.writerow(r2)
    print(f"[OK] {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input",  type=Path, help="TTL único a procesar")
    ap.add_argument("--output", type=Path, help="Salida (modo single)")
    ap.add_argument("--batch", action="store_true",
                    help="Procesar E1/E2/E3 en bloque")
    ap.add_argument("--experiments", nargs="+", default=["E1", "E2", "E3"],
                    help="Experimentos a procesar en --batch")
    ap.add_argument("--model", default="gpt-4o",
                    help="(Deprecado, use --models) Subdirectorio de modelo")
    ap.add_argument("--models", nargs="+", default=None,
                    help="Subdirectorios de modelo a procesar "
                         "(ej.: gpt-4o llama3.1_8b)")
    args = ap.parse_args()

    if args.batch:
        models = args.models or [args.model]
        rows: list[dict] = []
        for m in models:
            print(f"\n=== Modelo: {m} ===")
            rows.extend(batch_process(args.experiments, m))
        write_report(rows, RESULTS / "postprocess_report.csv")
        # Resumen
        print()
        print("=== Resumen del post-procesado ===")
        if not HAS_RDFLIB:
            print("⚠️  rdflib no está instalado en este entorno.")
            print("   Los TTL post-procesados se han generado en")
            print("   results/{Ex}/{DB}/gpt-4o/postprocessed/ — para medir")
            print("   parse_ok ejecuta `evaluate_E4_vs_E1-E3.py` (o este")
            print("   mismo script) en una máquina con rdflib instalado.")
            return
        rescued = sum(1 for r in rows
                      if r["parse_before"] == 0 and r["parse_after"] == 1)
        broke   = sum(1 for r in rows
                      if r["parse_before"] == 1 and r["parse_after"] == 0)
        ok_all  = sum(max(r["parse_after"], 0) for r in rows)
        print(f"Total runs procesadas: {len(rows)}")
        print(f"Rescatadas por post-fix: {rescued}")
        print(f"Rotas por post-fix:      {broke}")
        print(f"Parse_ok después:         {ok_all}/{len(rows)}")
        if rows:
            for exp in sorted({r["experiment"] for r in rows}):
                rs = [r for r in rows if r["experiment"] == exp]
                ok_b = sum(max(r["parse_before"], 0) for r in rs)
                ok_a = sum(max(r["parse_after"], 0) for r in rs)
                print(f"  {exp}: {ok_b} → {ok_a} (de {len(rs)})")
        return

    if not args.input or not args.output:
        ap.error("Usa --input + --output, o --batch")
    r = process_file(args.input, args.output)
    print(r)
    print(f"parse_before={int(parse_ok(args.input))} "
          f"parse_after={int(parse_ok(args.output))}")


if __name__ == "__main__":
    main()
