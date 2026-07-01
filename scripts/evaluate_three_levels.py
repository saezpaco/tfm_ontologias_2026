#!/usr/bin/env python3
"""
evaluate_three_levels.py
────────────────────────
Driver ÚNICO de evaluación de tres niveles (revisión del tutor: «utiliza siempre
el mismo sistema de evaluación con tres niveles, ya que cada nivel evalúa
cualidades diferentes»).

Recorre un subárbol de ``results/`` y, para CADA ontología generada, calcula los
tres niveles y los vuelca en una sola tabla, además de un resumen agregado por
celda con el número de ejecuciones válidas (n_runs OK):

  Nivel 1 · Sintáctico  : parse_ok (rdflib)
  Nivel 2 · Estructural : OQuaRE (Global + 5 subcaracterísticas) + HermiT
                          (vía scripts/oquare_eval.py)
  Nivel 3 · Funcional   : fidelidad léxica (canonical_ratio, recall vs 88 URIs
                          gold) + cobertura de 15 preguntas de competencia
                          (vía scripts/cisreg_fidelity.py y competency_questions.py)

Salida
------
    results/evaluation/threelevel_per_ontology.csv   (una fila por ontología)
    results/evaluation/threelevel_summary.csv        (media por celda + n_runs OK)

Las columnas de coordenadas (modelo, estrategia, BD, tipo de muestreo, tamaño N,
configuración RAG, réplica) se deducen del nombre de carpeta ``model_variant``,
de modo que el mismo driver sirve para las tres fases del protocolo.

Regla de agregación (documentada en el resumen): las medias de los niveles 2 y 3
se calculan SOLO sobre las réplicas válidas (parse_ok = 1); n_runs_OK indica
cuántas son, sobre n_total ejecuciones de la celda.

Uso
---
    python scripts/evaluate_three_levels.py                 # todo results/
    python scripts/evaluate_three_levels.py --root results/E3
    python scripts/evaluate_three_levels.py --no-reasoner   # sin HermiT (más rápido)
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ── Nivel 3 (funcional): puro texto, sin dependencias pesadas ──
from cisreg_fidelity import build_gold_uris, fidelity_for_file   # noqa: E402
from competency_questions import CQS, evaluate_cq                 # noqa: E402

# ── Nivel 1 (sintáctico): rdflib si está disponible ──
try:
    import rdflib
    _HAVE_RDFLIB = True
except Exception:
    _HAVE_RDFLIB = False

# ── Nivel 2 (estructural): oquare_eval si está disponible (rdflib + owlready2) ──
# owlready2 se importa dentro de evaluate_one(), así que lo comprobamos aquí
# para que la detección sea honesta y el nivel 2 degrade limpio si falta.
try:
    import oquare_eval
    import owlready2  # noqa: F401  (lo exige evaluate_one en tiempo de llamada)
    _HAVE_OQUARE = True
except Exception:
    _HAVE_OQUARE = False

KNOWN_MODELS = ["gpt-4o-mini", "gpt-4o", "llama3.1_8b", "llama3.1_70b",
                "llama3.2_3b", "qwen2.5-coder_7b", "mistral_7b"]
SAMPLINGS = ["A_head", "B_random", "C_stratified", "D_diversity"]
RAG_CONFIGS = ["ragapi_C1", "ragapi_C2", "ragapi_C3", "ragapi",
               "legacy", "baseline", "C1", "C2", "C3"]

OQUARE_FIELDS = ["oquare_global", "score_structural", "score_modularity",
                 "score_reusability", "score_operability", "score_reliability",
                 "n_classes", "n_obj_props", "n_data_props", "consistent"]


def parse_variant(variant: str) -> dict:
    """Extrae (modelo, tipo de muestreo, N, config RAG) del nombre de carpeta."""
    model = next((m for m in KNOWN_MODELS if variant.startswith(m)), "")
    sampling = next((s for s in SAMPLINGS if s in variant), "")
    mN = re.search(r"N(\d+)", variant)
    N = mN.group(1) if mN else ""
    rag = next((r for r in RAG_CONFIGS if r in variant), "")
    return {"model": model or variant, "sampling": sampling, "N": N, "rag_config": rag}


def path_meta(p: Path, results_root: Path) -> dict:
    # Las coordenadas (exp/db/variant) se leen SIEMPRE respecto a results/,
    # aunque el escaneo esté acotado a un subárbol más profundo.
    try:
        parts = p.resolve().relative_to(results_root).parts
    except ValueError:
        parts = p.parts
    exp = parts[0] if len(parts) >= 1 else ""
    db = parts[1] if len(parts) >= 2 else ""
    variant = parts[2] if len(parts) >= 3 else ""
    is_pp = "postprocessed" in parts
    run = ""
    m = re.search(r"run(\d+)", p.name)
    if m:
        run = m.group(1)
    meta = {"experiment": exp, "db": db, "model_variant": variant,
            "variant": "postprocessed" if is_pp else "raw", "run": run}
    meta.update(parse_variant(variant))
    return meta


def parse_ok_rdflib(text: str) -> int:
    if not _HAVE_RDFLIB:
        return -1  # desconocido
    try:
        g = rdflib.Graph()
        g.parse(data=text, format="turtle")
        return 1
    except Exception:
        return 0


def discover_ttls(root: Path):
    """Prefiere postprocessed cuando existe; ignora caché del razonador."""
    for p in sorted(root.rglob("*.ttl")):
        if ".owlcache" in str(p) or p.name.endswith(".sanitized.ttl"):
            continue
        if "postprocessed" not in p.parts:
            pp = p.parent / "postprocessed" / p.name
            if pp.exists():
                continue  # se evaluará la versión postprocesada
        yield p


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=PROJECT_ROOT / "results")
    ap.add_argument("--out-dir", type=Path, default=PROJECT_ROOT / "results" / "evaluation")
    ap.add_argument("--no-reasoner", action="store_true",
                    help="No ejecutar HermiT (nivel 2 estructural sin razonador)")
    args = ap.parse_args()
    root = args.root.resolve()
    RESULTS_ROOT = (PROJECT_ROOT / "results").resolve()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    def proj_rel(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(PROJECT_ROOT))
        except ValueError:
            return str(p.resolve())

    if not _HAVE_RDFLIB:
        print("[warn] rdflib no disponible: parse_ok quedará como -1 (desconocido).", file=sys.stderr)
    if not _HAVE_OQUARE:
        print("[warn] oquare_eval/owlready2 no disponible: nivel 2 (OQuaRE) se omite "
              "en este entorno. Ejecútalo en tu máquina con el venv del TFM.", file=sys.stderr)

    gold, _ = build_gold_uris()
    print(f"[i ] Gold set de fidelidad léxica: {len(gold)} URIs canónicas")

    rows = []
    for p in discover_ttls(root):
        meta = path_meta(p, RESULTS_ROOT)
        if not meta["experiment"]:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rec = {"file": proj_rel(p), **meta}

        # Nivel 1 · sintáctico
        rec["parse_ok"] = parse_ok_rdflib(text)

        # Nivel 2 · estructural (OQuaRE + HermiT)
        if _HAVE_OQUARE:
            try:
                o = oquare_eval.evaluate_one(p, with_reasoner=not args.no_reasoner)
                for k in OQUARE_FIELDS:
                    if k in o:
                        rec[k] = o[k]
                if "load_ok" in o and rec["parse_ok"] == -1:
                    rec["parse_ok"] = 1 if o["load_ok"] else 0
            except Exception as e:
                rec["oquare_error"] = str(e)[:120]

        # Nivel 3 · funcional (fidelidad léxica + CQ)
        fid = fidelity_for_file(p, gold)
        rec["canonical_ratio"] = fid["canonical_ratio"]
        rec["recall_vs_gold"] = fid["recall_vs_gold"]
        rec["n_canonical"] = fid["n_canonical"]
        rec["n_invented"] = fid["n_invented"]
        n_sat = sum(evaluate_cq(text, cq)["satisfies"] for cq in CQS)
        rec["cq_n_satisfied"] = n_sat
        rec["cq_coverage"] = round(n_sat / len(CQS), 3)
        rows.append(rec)

    if not rows:
        print("[!] No se encontraron ontologías en", args.root); return

    # ── CSV por ontología ──
    per_fields = ["file", "experiment", "db", "model_variant", "model",
                  "sampling", "N", "rag_config", "variant", "run", "parse_ok",
                  *OQUARE_FIELDS, "canonical_ratio", "recall_vs_gold",
                  "n_canonical", "n_invented", "cq_n_satisfied", "cq_coverage",
                  "oquare_error"]
    per_csv = args.out_dir / "threelevel_per_ontology.csv"
    with open(per_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=per_fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ── Resumen agregado por celda ──
    # Clave de celda = (experiment, model, db, sampling, N, rag_config, variant)
    key_fields = ["experiment", "model", "db", "sampling", "N", "rag_config", "variant"]
    groups = defaultdict(list)
    for r in rows:
        groups[tuple(r.get(k, "") for k in key_fields)].append(r)

    def m(vals):
        vals = [v for v in vals if isinstance(v, (int, float))]
        return round(mean(vals), 3) if vals else ""

    sum_rows = []
    for key, items in sorted(groups.items()):
        ok = [r for r in items if r.get("parse_ok") == 1]
        base = dict(zip(key_fields, key))
        base["n_total"] = len(items)
        base["n_runs_OK"] = len(ok)
        src = ok if ok else []
        base["oquare_global"] = m([r.get("oquare_global") for r in src])
        for k in ["score_structural", "score_modularity", "score_reusability",
                  "score_operability", "score_reliability"]:
            base[k] = m([r.get(k) for r in src])
        base["canonical_ratio"] = m([r.get("canonical_ratio") for r in src])
        base["recall_vs_gold"] = m([r.get("recall_vs_gold") for r in src])
        base["cq_coverage"] = m([r.get("cq_coverage") for r in src])
        base["cq_n_satisfied"] = m([r.get("cq_n_satisfied") for r in src])
        base["agregacion"] = "media sobre réplicas válidas (parse_ok=1)"
        sum_rows.append(base)

    sum_fields = key_fields + ["n_total", "n_runs_OK", "oquare_global",
                               "score_structural", "score_modularity",
                               "score_reusability", "score_operability",
                               "score_reliability", "canonical_ratio",
                               "recall_vs_gold", "cq_coverage", "cq_n_satisfied",
                               "agregacion"]
    sum_csv = args.out_dir / "threelevel_summary.csv"
    with open(sum_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sum_fields, extrasaction="ignore")
        w.writeheader()
        for r in sum_rows:
            w.writerow(r)

    print(f"[OK] {len(rows)} ontologías evaluadas · {len(sum_rows)} celdas")
    print(f"[OK] Por ontologia -> {proj_rel(per_csv)}")
    print(f"[OK] Resumen       -> {proj_rel(sum_csv)}")
    lvl = "1+3" if not _HAVE_OQUARE else "1+2+3"
    print(f"[i ] Niveles calculados en este entorno: {lvl}"
          + ("  (instala owlready2 para el nivel 2)" if not _HAVE_OQUARE else ""))


if __name__ == "__main__":
    main()
