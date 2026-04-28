#!/usr/bin/env python3
"""
evaluate_E4_vs_E1-E3.py
───────────────────────
Valida las ontologías generadas por OntoGenix (E4) y las compara con los
resultados previos de E1/E2/E3 sobre las mismas bases de datos.

Métricas por ontología (.ttl):
  · parse_ok         → 1/0 si rdflib puede parsear el TTL
  · n_triples        → número de triples parseados
  · n_classes        → #owl:Class
  · n_object_props   → #owl:ObjectProperty
  · n_datatype_props → #owl:DatatypeProperty
  · n_subclass_axioms→ #rdfs:subClassOf
  · n_restrictions   → #owl:Restriction
  · n_labels         → #rdfs:label
  · n_comments       → #rdfs:comment | skos:definition
  · size_bytes       → tamaño del archivo

Salida: results/comparison_E1-E4.csv  +  results/comparison_E1-E4.md
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS      = PROJECT_ROOT / "results"
EXPERIMENTS  = ["E1", "E2", "E3", "E4"]
MODEL_SUBDIR = {"E1": "gpt-4o", "E2": "gpt-4o", "E3": "gpt-4o",
                "E4": "gpt-4o"}
DATABASES    = ["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"]

try:
    from rdflib import Graph
    from rdflib.namespace import OWL, RDFS, SKOS
    HAS_RDFLIB = True
except ImportError:
    HAS_RDFLIB = False
    print("[WARN] rdflib no está instalado: `pip install rdflib`. "
          "Haré solo el conteo por bytes.")


def count_pattern(path: Path, needles: list[str]) -> int:
    txt = path.read_text(encoding="utf-8", errors="ignore")
    return sum(txt.count(n) for n in needles)


def evaluate_ttl(path: Path) -> dict:
    """Parsea la ontología y devuelve métricas."""
    m = {
        "file":             path.name,
        "size_bytes":       path.stat().st_size,
        "parse_ok":         0,
        "n_triples":        None,
        "n_classes":        None,
        "n_object_props":   None,
        "n_datatype_props": None,
        "n_subclass_axioms":None,
        "n_restrictions":   None,
        "n_labels":         None,
        "n_comments":       None,
    }
    if not HAS_RDFLIB:
        # Heurística por texto: contamos apariciones como fallback.
        # Consideramos parse_ok=1 si el archivo tiene contenido y al menos una
        # clase o propiedad OWL (señal mínima de ontología válida).
        m["n_classes"]         = count_pattern(path, ["owl:Class", "<owl:Class"])
        m["n_object_props"]    = count_pattern(path, ["owl:ObjectProperty"])
        m["n_datatype_props"]  = count_pattern(path, ["owl:DatatypeProperty"])
        m["n_subclass_axioms"] = count_pattern(path, ["rdfs:subClassOf"])
        m["n_restrictions"]    = count_pattern(path, ["owl:Restriction"])
        m["n_labels"]          = count_pattern(path, ["rdfs:label"])
        m["n_comments"]        = count_pattern(path, ["rdfs:comment",
                                                      "skos:definition"])
        # parse_ok heurístico
        if (m["n_classes"] + m["n_object_props"] + m["n_datatype_props"]) > 0:
            m["parse_ok"] = 1
        return m

    g = Graph()
    try:
        g.parse(str(path), format="turtle")
        m["parse_ok"]  = 1
        m["n_triples"] = len(g)
    except Exception as e:                                          # noqa: BLE001
        m["parse_error"] = f"{type(e).__name__}: {e}"
        return m

    q = lambda typ: sum(1 for _ in g.subjects(predicate=None, object=typ))  # noqa: E731
    # Conteo por tipo
    from rdflib import RDF
    m["n_classes"]         = sum(1 for _ in g.subjects(RDF.type, OWL.Class))
    m["n_object_props"]    = sum(1 for _ in g.subjects(RDF.type, OWL.ObjectProperty))
    m["n_datatype_props"]  = sum(1 for _ in g.subjects(RDF.type, OWL.DatatypeProperty))
    m["n_subclass_axioms"] = sum(1 for _ in g.triples((None, RDFS.subClassOf, None)))
    m["n_restrictions"]    = sum(1 for _ in g.subjects(RDF.type, OWL.Restriction))
    m["n_labels"]          = sum(1 for _ in g.triples((None, RDFS.label, None)))
    m["n_comments"]        = (
        sum(1 for _ in g.triples((None, RDFS.comment, None))) +
        sum(1 for _ in g.triples((None, SKOS.definition, None)))
    )
    return m


def collect_rows(include_postprocessed: bool = True) -> list[dict]:
    rows = []
    for exp in EXPERIMENTS:
        model = MODEL_SUBDIR[exp]
        for db in DATABASES:
            exp_dir = RESULTS / exp / db / model
            if not exp_dir.is_dir():
                rows.append({"experiment": exp, "db": db, "file": None,
                             "parse_ok": 0, "note": "missing",
                             "variant": "raw"})
                continue
            # Variante "raw" (output original del LLM)
            ttls = sorted(exp_dir.glob("ontology_run*.ttl"))
            if not ttls:
                rows.append({"experiment": exp, "db": db, "file": None,
                             "parse_ok": 0, "note": "no_ttl",
                             "variant": "raw"})
                continue
            for p in ttls:
                r = evaluate_ttl(p)
                r["experiment"] = exp
                r["db"]         = db
                r["run"]        = p.stem.replace("ontology_run", "")
                r["variant"]    = "raw"
                rows.append(r)
            # Variante "postprocessed" (con auto-prefix injection)
            if include_postprocessed and exp != "E4":
                pp_dir = exp_dir / "postprocessed"
                if pp_dir.is_dir():
                    for p in sorted(pp_dir.glob("ontology_run*.ttl")):
                        r = evaluate_ttl(p)
                        r["experiment"] = exp
                        r["db"]         = db
                        r["run"]        = p.stem.replace("ontology_run", "")
                        r["variant"]    = "postprocessed"
                        rows.append(r)
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    fields = ["experiment", "variant", "db", "run", "file", "parse_ok",
              "size_bytes", "n_triples", "n_classes", "n_object_props",
              "n_datatype_props", "n_subclass_axioms", "n_restrictions",
              "n_labels", "n_comments", "parse_error", "note"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] {path}")


def aggregate_table(rows: list[dict], variant: str = "raw") -> str:
    """Genera un resumen markdown agregado por (experiment, db) y variante."""
    from collections import defaultdict
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        if r.get("variant", "raw") != variant:
            continue
        if r.get("parse_ok"):
            buckets[(r["experiment"], r["db"])].append(r)

    lines = ["| Exp | DB | runs_ok | n_triples | n_classes | n_obj_props | n_data_props | n_subClassOf | n_labels |",
             "|-----|----|---------|-----------|-----------|-------------|--------------|--------------|----------|"]
    mean = lambda xs: (sum(xs) / len(xs)) if xs else 0  # noqa: E731
    for exp in EXPERIMENTS:
        if variant == "postprocessed" and exp == "E4":
            continue
        for db in DATABASES:
            rs = buckets.get((exp, db), [])
            if not rs:
                lines.append(f"| {exp} | {db} | 0 | - | - | - | - | - | - |")
                continue
            def avg(k: str) -> str:
                vs = [r[k] for r in rs if isinstance(r.get(k), (int, float))]
                return f"{mean(vs):.1f}"
            lines.append(
                f"| {exp} | {db} | {len(rs)} | {avg('n_triples')} | "
                f"{avg('n_classes')} | {avg('n_object_props')} | "
                f"{avg('n_datatype_props')} | {avg('n_subclass_axioms')} | "
                f"{avg('n_labels')} |"
            )
    return "\n".join(lines)


def aggregate_diff_table(rows: list[dict]) -> str:
    """Tabla comparativa raw vs postprocessed: parse_ok antes/después."""
    from collections import defaultdict
    by_exp_db = defaultdict(lambda: {"raw": [], "postprocessed": []})
    for r in rows:
        v = r.get("variant", "raw")
        by_exp_db[(r["experiment"], r["db"])][v].append(r)

    lines = ["| Exp | DB | runs_ok (raw) | runs_ok (post-fix) | rescued |",
             "|-----|----|---------------|--------------------|---------|"]
    for exp in [e for e in EXPERIMENTS if e != "E4"]:
        for db in DATABASES:
            raws  = by_exp_db[(exp, db)]["raw"]
            posts = by_exp_db[(exp, db)]["postprocessed"]
            ok_raw  = sum(1 for r in raws  if r.get("parse_ok"))
            ok_post = sum(1 for r in posts if r.get("parse_ok"))
            rescued = max(0, ok_post - ok_raw)
            lines.append(f"| {exp} | {db} | {ok_raw}/{len(raws)} "
                         f"| {ok_post}/{len(posts)} | +{rescued} |")
    return "\n".join(lines)


def main():
    if not RESULTS.exists():
        sys.exit(f"[ERROR] {RESULTS} no existe.")
    rows = collect_rows()
    csv_path = RESULTS / "comparison_E1-E4.csv"
    md_path  = RESULTS / "comparison_E1-E4.md"
    write_csv(rows, csv_path)
    md_path.write_text(
        "# Comparativa E1–E4: ontologías generadas\n\n"
        "Métricas por corrida (ver `comparison_E1-E4.csv`).\n\n"
        "## Resumen — output crudo del LLM (raw)\n\n"
        + aggregate_table(rows, variant="raw") + "\n\n"
        "## Resumen — tras post-procesado (auto-prefix injection)\n\n"
        + aggregate_table(rows, variant="postprocessed") + "\n\n"
        "## Diferencial: ¿cuántas ontologías se rescatan con el fix?\n\n"
        + aggregate_diff_table(rows) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] {md_path}")

if __name__ == "__main__":
    main()
