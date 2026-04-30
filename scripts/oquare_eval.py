#!/usr/bin/env python3
"""
oquare_eval.py
──────────────
Evaluador de calidad de ontologías basado en OQuaRE
(Duque-Ramos, Fernández-Breis, Stevens & Aussenac-Gilles, 2011, 2014).

OQuaRE adapta el modelo SQuaRE (ISO/IEC 25000) para ontologías. Define un
conjunto jerárquico de **métricas → sub-características → características**
con una puntuación normalizada de 1 (bajo) a 5 (alto) por sub-característica.

Esta implementación cubre:

  · Métricas **estructurales** (sin razonador): WMCOnto, NOMOnto, INROnto,
    DITM, NACOnto, TMOnto, RROnto, AROnto, CBOnto, LCOMOnto, ANOnto.
  · Métricas **con razonador** (owlready2 + HermiT): consistency,
    coherence (clases insatisfacibles), tiempo de clasificación,
    n_inferred_axioms.
  · Score por sub-característica en escala 1-5 según rúbricas publicadas.
  · Reporte CSV + Markdown agregado por (modelo, experimento, BBDD).

Dependencias
------------
    pip install owlready2 rdflib

owlready2 incluye HermiT (Java). Asegúrate de tener `java` en el PATH.

Uso
---
    # Evaluar todos los TTL post-procesados de E1-E4
    python scripts/oquare_eval.py --batch

    # Un único archivo
    python scripts/oquare_eval.py --input results/E4/FANTOM5/gpt-4o/ontology_run1.ttl
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT_ROOT / "results"
EXPERIMENTS = ["E1", "E2", "E3", "E4"]
DATABASES = ["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"]

# ─── Rúbricas OQuaRE (Duque-Ramos et al., 2014, Tabla 4) ─────────────
# Cada métrica se mapea a 1-5 según rangos. Los rangos provienen de la
# publicación original; en algunos casos se han ajustado a la escala de
# las ontologías ligeras de este TFM (50-300 triples) — se documenta
# en la columna "rationale" del reporte.
OQUARE_RUBRIC: dict[str, list[tuple[float, int]]] = {
    # Cuanto MENOR, mejor (complejidad)
    "WMCOnto":   [(20, 5), (30, 4), (40, 3), (50, 2), (float("inf"), 1)],
    "NOMOnto":   [(10, 5), (20, 4), (30, 3), (40, 2), (float("inf"), 1)],
    "DITM":      [(4,  5), (6,  4), (8,  3), (10, 2), (float("inf"), 1)],
    "NACOnto":   [(2,  5), (3,  4), (4,  3), (5,  2), (float("inf"), 1)],
    "CBOnto":    [(1,  5), (3,  4), (5,  3), (7,  2), (float("inf"), 1)],
    "TMOnto":    [(0.05, 5), (0.10, 4), (0.20, 3), (0.40, 2),
                  (float("inf"), 1)],
    "LCOMOnto":  [(1,  5), (2,  4), (4,  3), (8,  2), (float("inf"), 1)],
    # Cuanto MAYOR, mejor (riqueza)
    "ANOnto":    [(0.1, 1), (0.5, 2), (1.0, 3), (1.5, 4),
                  (float("inf"), 5)],
    "INROnto":   [(0.1, 1), (0.5, 2), (1.0, 3), (1.5, 4),
                  (float("inf"), 5)],
    "RROnto":    [(0.1, 1), (0.3, 2), (0.5, 3), (0.8, 4),
                  (float("inf"), 5)],
    "AROnto":    [(0.1, 1), (0.2, 2), (0.4, 3), (0.6, 4),
                  (float("inf"), 5)],
}


def score_metric(name: str, value: float | None) -> int:
    if value is None:
        return 0
    rubric = OQUARE_RUBRIC.get(name)
    if not rubric:
        return 0
    for limit, sc in rubric:
        if value <= limit:
            return sc
    return 1


# ─── Sub-características (composición OQuaRE) ────────────────────────
SUBCHARACTERISTICS = {
    # Maintainability (ISO 25010)
    "structural":   ["WMCOnto", "DITM", "NOMOnto", "NACOnto"],
    "modularity":   ["CBOnto", "LCOMOnto"],
    "reusability":  ["ANOnto", "INROnto", "TMOnto"],
    "operability":  ["RROnto", "AROnto"],
    # Reliability — depende del razonador
    "reliability":  [],   # se inyecta tras razonar
}


# ─── Cálculo de métricas ─────────────────────────────────────────────
def compute_structural(ontology) -> dict[str, float | int | None]:
    """Métricas OQuaRE estructurales calculadas con owlready2.

    Sigue la convención de Duque-Ramos et al. (2014):
        - C: número de clases
        - subC[c]: subclases directas de c
        - props(c): propiedades de objeto/datos cuyo dominio es c
        - parents(c): superclases directas
    """
    classes = list(ontology.classes())
    n_classes = len(classes)

    # Object & datatype properties
    obj_props = list(ontology.object_properties())
    data_props = list(ontology.data_properties())
    annot_props = list(ontology.annotation_properties())
    n_props = len(obj_props) + len(data_props)

    # Anotaciones por clase
    n_annotations = 0
    for c in classes:
        for prop in annot_props + [
            ontology.world.search_one(iri="*rdfs#label"),
            ontology.world.search_one(iri="*rdfs#comment"),
            ontology.world.search_one(iri="*skos*#prefLabel"),
            ontology.world.search_one(iri="*skos*#definition"),
        ]:
            if prop is None:
                continue
            try:
                vals = list(getattr(c, prop.python_name, None) or [])
                n_annotations += len(vals)
            except Exception:                                       # noqa
                pass

    # Profundidad y ancestros
    def depth(c, seen=None) -> int:
        if seen is None:
            seen = set()
        if c in seen:
            return 0
        seen = seen | {c}
        parents = [p for p in c.is_a if hasattr(p, "iri") and p in classes]
        if not parents:
            return 1
        return 1 + max(depth(p, seen) for p in parents)

    depths = [depth(c) for c in classes] if classes else [0]

    # Subclases directas
    n_subclasses = sum(
        1 for c in classes
        for p in c.is_a if hasattr(p, "iri") and p in classes
    )

    # Tangledness — clases con > 1 superclase de la propia ontología
    n_tangled = sum(
        1 for c in classes
        if sum(1 for p in c.is_a
               if hasattr(p, "iri") and p in classes) > 1
    )

    # Acoplamiento (clases referenciadas en restricciones / dominios)
    referenced = set()
    for p in obj_props:
        for d in (p.domain or []):
            if d in classes:
                referenced.add(d)
        for r in (p.range or []):
            if r in classes:
                referenced.add(r)
    n_coupled = len(referenced)

    # Métricas finales
    if n_classes == 0:
        return {
            "n_classes": 0, "n_obj_props": len(obj_props),
            "n_data_props": len(data_props),
            "n_annotations": n_annotations,
            "WMCOnto": None, "NOMOnto": None, "DITM": None,
            "NACOnto": None, "CBOnto": None, "TMOnto": None,
            "LCOMOnto": None, "ANOnto": None, "INROnto": None,
            "RROnto": None, "AROnto": None,
        }

    return {
        "n_classes":      n_classes,
        "n_obj_props":    len(obj_props),
        "n_data_props":   len(data_props),
        "n_annotations":  n_annotations,
        "WMCOnto":        n_props / n_classes,
        "NOMOnto":        n_props / n_classes,  # interpretación ligera
        "DITM":           max(depths),
        "NACOnto":        sum(depths) / n_classes,
        "CBOnto":         n_coupled / n_classes,
        "TMOnto":         n_tangled / n_classes,
        "LCOMOnto":       max(0, n_classes - n_subclasses),
        "ANOnto":         n_annotations / n_classes,
        "INROnto":        n_subclasses / n_classes,
        "RROnto":         len(obj_props) / n_classes,
        "AROnto":         len(obj_props) / max(1, n_props),
    }


def reason_with_hermit(onto, timeout_s: int = 60) -> dict[str, Any]:
    """Aplica HermiT vía owlready2.sync_reasoner_hermit."""
    from owlready2 import sync_reasoner_hermit, OwlReadyInconsistentOntologyError

    out: dict[str, Any] = {
        "consistent":         None,
        "n_unsatisfiable":    None,
        "n_inferred_classes": None,
        "reasoner_seconds":   None,
        "reasoner_error":     None,
    }
    t0 = time.time()
    try:
        # Pasamos el World aislado al razonador para no contaminar el global
        sync_reasoner_hermit(onto.world,
                             infer_property_values=True,
                             debug=0)
        unsat = list(onto.world.inconsistent_classes())
        out["consistent"] = True
        out["n_unsatisfiable"] = len(unsat)
        out["n_inferred_classes"] = len(list(onto.classes()))
        out["reasoner_seconds"] = round(time.time() - t0, 2)
    except OwlReadyInconsistentOntologyError:
        out["consistent"] = False
        out["reasoner_seconds"] = round(time.time() - t0, 2)
    except Exception as e:                                          # noqa
        out["reasoner_error"] = f"{type(e).__name__}: {e}"
        out["reasoner_seconds"] = round(time.time() - t0, 2)
    return out


# ─── Conversión TTL → RDF/XML ────────────────────────────────────────
# owlready2 no parsea Turtle nativamente: solo entiende RDF/XML y NTriples.
# Convertimos al vuelo con rdflib y guardamos el .owl en un cache para no
# repetir la conversión.

# Datatypes XSD que owlready2 valida estrictamente. Si un literal está
# tipado como uno de estos pero su lexical no se puede convertir, lo
# saneamos a xsd:string para no perder el resto del esquema.
_NUMERIC_XSD = {
    "http://www.w3.org/2001/XMLSchema#integer":            int,
    "http://www.w3.org/2001/XMLSchema#int":                int,
    "http://www.w3.org/2001/XMLSchema#long":               int,
    "http://www.w3.org/2001/XMLSchema#short":              int,
    "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": int,
    "http://www.w3.org/2001/XMLSchema#positiveInteger":    int,
    "http://www.w3.org/2001/XMLSchema#decimal":            float,
    "http://www.w3.org/2001/XMLSchema#double":             float,
    "http://www.w3.org/2001/XMLSchema#float":              float,
    "http://www.w3.org/2001/XMLSchema#boolean":
        lambda v: v.lower() in ("true", "false", "0", "1"),
    "http://www.w3.org/2001/XMLSchema#date":               None,  # heurística
    "http://www.w3.org/2001/XMLSchema#dateTime":           None,
}


# Patrón: literal entre comillas seguido de ^^<datatype> o ^^prefix:type
# que sea uno de los tipos numéricos XSD. Capturamos lexical y datatype.
RE_TYPED_LITERAL = re.compile(
    r'"((?:[^"\\]|\\.)*)"'                       # 1: lexical
    r'\s*\^\^\s*'
    r'(?:'
        r'<(http://www\.w3\.org/2001/XMLSchema#'  # 2a: full URI datatype
        r'(?:integer|int|long|short|nonNegativeInteger|positiveInteger|'
        r'decimal|double|float|boolean))>'
        r'|'
        r'(xsd):'                                 # 3: prefix
        r'(integer|int|long|short|nonNegativeInteger|positiveInteger|'
        r'decimal|double|float|boolean)'         # 4: localname
    r')',
    re.MULTILINE,
)


def _is_valid_lexical(lex: str, dt_name: str) -> bool:
    """Comprueba si el lexical es convertible al tipo XSD declarado."""
    try:
        if dt_name in ("integer", "int", "long", "short",
                       "nonNegativeInteger", "positiveInteger"):
            int(lex)
        elif dt_name in ("decimal", "double", "float"):
            float(lex)
        elif dt_name == "boolean":
            return lex.lower() in ("true", "false", "0", "1")
        return True
    except (ValueError, TypeError):
        return False


def _sanitize_ttl_text(text: str) -> tuple[str, int]:
    """Recorre el TTL como texto y reemplaza literales tipados como
    xsd:integer/decimal/etc. cuyo lexical NO es convertible, sustituyendo
    el datatype por xsd:string. Esto evita los crashes de owlready2.

    Devuelve (texto_corregido, n_literales_saneados).
    """
    n_fixed = 0
    def repl(m: "re.Match[str]") -> str:
        nonlocal n_fixed
        lex = m.group(1)
        dt_name = m.group(2).split("#")[-1] if m.group(2) else m.group(4)
        if _is_valid_lexical(lex, dt_name):
            return m.group(0)
        n_fixed += 1
        return f'"{lex}"^^xsd:string'
    fixed = RE_TYPED_LITERAL.sub(repl, text)
    return fixed, n_fixed


def _sanitize_graph(g) -> int:
    """Fallback: si quedan literales mal tipados tras el saneo textual,
    los limpiamos también a nivel de grafo."""
    from rdflib import Literal, XSD
    n_fixed = 0
    bad: list = []
    new: list = []
    for s, p, o in g:
        if not isinstance(o, Literal):
            continue
        dt = o.datatype
        if dt is None or str(dt) not in _NUMERIC_XSD:
            continue
        conv = _NUMERIC_XSD[str(dt)]
        lex = str(o)
        if conv is None:
            continue
        try:
            if callable(conv):
                conv(lex)
        except (ValueError, TypeError):
            bad.append((s, p, o))
            new.append((s, p, Literal(lex, datatype=XSD.string)))
            n_fixed += 1
    for t in bad: g.remove(t)
    for t in new: g.add(t)
    return n_fixed


def ttl_to_owl(ttl_path: Path) -> tuple[Path | None, int]:
    """Convierte un .ttl a .owl (RDF/XML) con rdflib aplicando dos pasadas
    de saneo:

      1. Saneo **textual** sobre el TTL fuente: regex que detecta literales
         tipados como xsd:integer/decimal/etc. con lexicales no convertibles
         y los reescribe como xsd:string. Esto es necesario porque rdflib
         emite warnings pero el serializador RDF/XML revalida los tipos.
      2. Saneo **a nivel de grafo** como red de seguridad por si quedaran
         literales mal tipados que el regex no haya capturado.

    Devuelve (ruta_convertida, n_literales_saneados)."""
    try:
        from rdflib import Graph
    except ImportError:
        return None, 0
    cache_dir = ttl_path.parent / ".owlcache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = cache_dir / (ttl_path.stem + ".owl")
    sidecar = cache_dir / (ttl_path.stem + ".sanitized.json")
    if (out.exists() and out.stat().st_mtime >= ttl_path.stat().st_mtime
            and sidecar.exists()):
        try:
            n = json.loads(sidecar.read_text())["n_sanitized"]
            return out, n
        except Exception:                                           # noqa
            pass

    # Pasada 1: saneo textual del TTL antes de pasarlo a rdflib
    try:
        raw_text = ttl_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:                                          # noqa
        print(f"  [WARN] no se puede leer {ttl_path}: {e}", file=sys.stderr)
        return None, 0
    sanitized_text, n_text_fixed = _sanitize_ttl_text(raw_text)

    # Si hubo saneo textual, guardamos el TTL parcheado en el cache
    sane_ttl_path = (cache_dir / (ttl_path.stem + ".sanitized.ttl")
                     if n_text_fixed else ttl_path)
    if n_text_fixed:
        sane_ttl_path.write_text(sanitized_text, encoding="utf-8")

    # Pasada 2: cargar con rdflib + saneo de grafo + serializar a XML
    try:
        g = Graph()
        g.parse(str(sane_ttl_path), format="turtle")
        n_graph_fixed = _sanitize_graph(g)
        g.serialize(destination=str(out), format="xml")
        n_total = n_text_fixed + n_graph_fixed
        sidecar.write_text(json.dumps({
            "n_sanitized": n_total,
            "n_text_fixed": n_text_fixed,
            "n_graph_fixed": n_graph_fixed,
        }))
        return out, n_total
    except Exception as e:                                          # noqa
        print(f"  [WARN] conversión TTL→OWL falla en {ttl_path.name}: "
              f"{type(e).__name__}: {str(e)[:120]}", file=sys.stderr)
        return None, n_text_fixed


# ─── Evaluación de un único archivo ──────────────────────────────────
def evaluate_one(path: Path, with_reasoner: bool = True) -> dict[str, Any]:
    """Cada llamada usa su propio ``owlready2.World`` para aislar el grafo
    y evitar que clases/propiedades de runs anteriores se mezclen."""
    from owlready2 import World

    rec: dict[str, Any] = {
        "file":     path.name,
        "src":      str(path),
        "size_bytes": path.stat().st_size,
        "load_ok":  0,
        "load_error": None,
        "n_literals_sanitized": 0,
    }
    # Convertir Turtle a RDF/XML antes de pasarlo a owlready2
    if path.suffix == ".ttl":
        owl_path, n_sanitized = ttl_to_owl(path)
        rec["n_literals_sanitized"] = n_sanitized
    else:
        owl_path = path
    if owl_path is None:
        rec["load_error"] = "rdflib_parse_failed: el TTL no es válido"
        return rec
    world = World()
    try:
        onto = world.get_ontology(f"file://{owl_path.resolve()}").load()
        rec["load_ok"] = 1
    except Exception as e:                                          # noqa
        rec["load_error"] = f"{type(e).__name__}: {e}"
        try: world.close()                                          # noqa
        except Exception: pass                                       # noqa
        return rec

    # Estructurales
    try:
        rec.update(compute_structural(onto))
    except Exception as e:                                          # noqa
        rec["structural_error"] = f"{type(e).__name__}: {e}"

    # Razonador
    if with_reasoner:
        rec.update(reason_with_hermit(onto))

    # Scores OQuaRE 1-5 por sub-característica
    sub_scores: dict[str, float] = {}
    for sub, metrics in SUBCHARACTERISTICS.items():
        if not metrics:
            continue
        scs = [score_metric(m, rec.get(m)) for m in metrics
               if rec.get(m) is not None]
        sub_scores[f"score_{sub}"] = (
            round(sum(scs) / len(scs), 2) if scs else 0
        )
    # Reliability se calcula a partir del razonador
    if with_reasoner and rec.get("consistent") is not None:
        if not rec["consistent"]:
            sub_scores["score_reliability"] = 1
        elif rec.get("n_unsatisfiable", 0) > 0:
            sub_scores["score_reliability"] = 2
        else:
            sub_scores["score_reliability"] = 5
    else:
        sub_scores["score_reliability"] = 0

    rec.update(sub_scores)
    if sub_scores:
        rec["oquare_global"] = round(
            sum(sub_scores.values()) / len(sub_scores), 2
        )

    # Limpieza del World aislado
    try: world.close()                                              # noqa
    except Exception: pass                                           # noqa
    return rec


# ─── Batch ───────────────────────────────────────────────────────────
def batch(experiments: list[str], model: str = "gpt-4o",
          with_reasoner: bool = True,
          variant: str = "postprocessed") -> list[dict]:
    rows: list[dict] = []
    for exp in experiments:
        for db in DATABASES:
            base = RESULTS / exp / db / model
            if exp == "E4":
                # E4 no tiene postprocessed; se evalúa el raw
                target = base
            else:
                target = base / "postprocessed" if variant == "postprocessed" else base
            if not target.is_dir():
                print(f"[skip] {target} no existe", file=sys.stderr)
                continue
            for ttl in sorted(target.glob("ontology_run*.ttl")):
                t0 = time.time()
                rec = evaluate_one(ttl, with_reasoner=with_reasoner)
                rec["experiment"] = exp
                rec["db"]         = db
                rec["model"]      = model
                rec["variant"]    = "raw" if exp == "E4" else variant
                rec["run"]        = ttl.stem.replace("ontology_run", "")
                rec["eval_seconds"] = round(time.time() - t0, 2)
                ok = "OK" if rec.get("load_ok") else "FAIL"
                consist = rec.get("consistent")
                print(f"[{exp}/{db}/run{rec['run']}/{model}] "
                      f"load={ok} cons={consist} "
                      f"score={rec.get('oquare_global', '—')} "
                      f"({rec['eval_seconds']}s)")
                rows.append(rec)
    return rows


def write_outputs(rows: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "oquare_metrics.csv"
    md_path  = out_dir / "oquare_summary.md"
    # Unión de keys
    fields: list[str] = []
    seen: set[str] = set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k); fields.append(k)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] {csv_path}")

    # Resumen MD: media de scores por (experimento, modelo)
    from collections import defaultdict
    bucket: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        if r.get("load_ok"):
            bucket[(r["experiment"], r["model"])].append(r)

    metric_keys = ["score_structural", "score_modularity", "score_reusability",
                   "score_operability", "score_reliability", "oquare_global"]
    lines = ["# OQuaRE: resumen agregado",
             "",
             "Media por (Experimento, Modelo) sobre las corridas con load_ok=1.",
             "",
             "| Exp | Modelo | n_runs | Structural | Modularity | "
             "Reusability | Operability | Reliability | **Global** |",
             "|-----|--------|--------|------------|------------|"
             "-------------|-------------|-------------|------------|"]
    for (exp, model), rs in sorted(bucket.items()):
        def avg(k: str) -> str:
            vs = [r[k] for r in rs if isinstance(r.get(k), (int, float))]
            return f"{sum(vs)/len(vs):.2f}" if vs else "—"
        lines.append(
            f"| {exp} | {model} | {len(rs)} | {avg(metric_keys[0])} | "
            f"{avg(metric_keys[1])} | {avg(metric_keys[2])} | "
            f"{avg(metric_keys[3])} | {avg(metric_keys[4])} | "
            f"**{avg(metric_keys[5])}** |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] {md_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, help="TTL único")
    ap.add_argument("--batch", action="store_true",
                    help="Evaluar E1-E4 sobre todas las BBDD")
    ap.add_argument("--experiments", nargs="+", default=EXPERIMENTS)
    ap.add_argument("--models", nargs="+", default=["gpt-4o"],
                    help="Subdirectorios de modelo (gpt-4o, llama3.1_8b, …)")
    ap.add_argument("--no-reasoner", action="store_true",
                    help="Saltar HermiT (más rápido, sin reliability)")
    args = ap.parse_args()

    if args.input:
        rec = evaluate_one(args.input, with_reasoner=not args.no_reasoner)
        print(json.dumps(rec, indent=2, default=str))
        return

    if args.batch:
        all_rows: list[dict] = []
        for model in args.models:
            print(f"\n=== Modelo: {model} ===")
            rs = batch(args.experiments, model=model,
                       with_reasoner=not args.no_reasoner)
            all_rows.extend(rs)
        write_outputs(all_rows, RESULTS / "evaluation")
        return

    ap.error("Usa --input <ttl> o --batch")


if __name__ == "__main__":
    main()
