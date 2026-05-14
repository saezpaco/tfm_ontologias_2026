"""Sugerencia 1 del tutor: análisis del core semántico común entre BBDD.

Las cuatro BBDD comparten esquema columnar (preprocesado a 30 columnas
canónicas). La pregunta es: ¿el LLM modela las mismas clases / propiedades
para las cuatro BBDD dentro de un mismo experimento × modelo?

Métrica: Jaccard pareado entre los conjuntos de URIs de las ontologías
generadas para las cuatro BBDD, agregado por (experimento, modelo, run).

Salida: results/evaluation/semantic_core.csv y semantic_core_summary.md
"""
from __future__ import annotations
import csv
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path("/sessions/nifty-beautiful-knuth/mnt/TFM")
RES = ROOT / "results"
EVAL = RES / "evaluation"
EVAL.mkdir(parents=True, exist_ok=True)

# Reusamos las funciones del módulo de fidelidad
import sys; sys.path.insert(0, str(ROOT / "scripts"))
from cisreg_fidelity import expand_uris, classify_namespace

# Estructura común columnar de las 4 BBDD
COMMON_COLUMNS = {
    "crm_ID", "orig_chr", "orig_start", "orig_end", "orig_assembly",
    "current_chr", "current_start", "current_end", "current_assembly",
    "minimum_ratio", "score", "original_ID", "crossref", "enh_PMID",
    "biosample_name", "enh_method", "type", "source",
    "hgnc_symbol_target_genes", "enh2gene_PMID", "enh2gene_method",
    "hgnc_symbol_TFs", "TFs2enh_PMID", "TFs2enh_method",
    "disease", "disease_PMID", "disease_method",
    "refsnp_ID", "mutation_PMID", "mutation_method",
}

def parse_path(p: Path):
    parts = p.relative_to(RES).parts
    out = {"experiment": parts[0] if len(parts) >= 1 else "",
           "db":         parts[1] if len(parts) >= 2 else "",
           "model":      parts[2] if len(parts) >= 3 else "",
           "variant":    "postprocessed" if "postprocessed" in parts else "raw"}
    m = re.search(r"run(\d+)", p.name); out["run"] = m.group(1) if m else ""
    return out

def collect_uris(p: Path) -> set[str]:
    text = p.read_text(encoding="utf-8", errors="replace")
    uris = expand_uris(text)
    # Filtrar a "contenido semántico" — descartar w3.org/XML, standard, vacíos
    return {u for u in uris
            if classify_namespace(u) not in ("standard",)}

def jaccard(a: set, b: set) -> float:
    if not a and not b: return 1.0
    inter = len(a & b); union = len(a | b)
    return inter / union if union else 0.0

def main():
    # Indexar por (experimento, modelo, run, variant) → {db → set_uris}
    bucket = defaultdict(dict)
    for p in sorted(RES.rglob("*.ttl")):
        if ".owlcache" in str(p): continue
        meta = parse_path(p)
        if not meta["experiment"]: continue
        # Preferimos postprocessed; si no existe, raw
        key = (meta["experiment"], meta["model"], meta["run"], meta["variant"])
        bucket[key][meta["db"]] = collect_uris(p)

    # Para cada (experimento, modelo, run), si hay postprocessed para todas las BBDD,
    # usar postprocessed; si no, raw.
    grouped = defaultdict(dict)  # (exp,mod,run) -> {db -> set}
    for (exp, mod, run, variant), dbs in bucket.items():
        key = (exp, mod, run)
        # solo añadir si no hay aún o variant=postprocessed sobreescribe raw
        for db, s in dbs.items():
            if (db not in grouped[key]) or (variant == "postprocessed"):
                grouped[key][db] = s

    out_rows = []
    for (exp, mod, run), dbs in grouped.items():
        if len(dbs) < 2: continue
        # pares
        pairs = list(combinations(sorted(dbs.keys()), 2))
        for db_a, db_b in pairs:
            j = jaccard(dbs[db_a], dbs[db_b])
            out_rows.append({
                "experiment": exp, "model": mod, "run": run,
                "db_a": db_a, "db_b": db_b,
                "n_uris_a": len(dbs[db_a]), "n_uris_b": len(dbs[db_b]),
                "intersection": len(dbs[db_a] & dbs[db_b]),
                "union":       len(dbs[db_a] | dbs[db_b]),
                "jaccard":     round(j, 4),
            })

    out_csv = EVAL / "semantic_core.csv"
    fieldnames = ["experiment","model","run","db_a","db_b",
                  "n_uris_a","n_uris_b","intersection","union","jaccard"]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for r in out_rows: w.writerow(r)
    print(f"[OK] {out_csv}  ({len(out_rows)} pares)")

    # Resumen agregado por (experimento, modelo)
    agg = defaultdict(list)
    for r in out_rows:
        agg[(r["experiment"], r["model"])].append(r["jaccard"])

    summary = ["# Core semántico común entre BBDD — análisis intra-modelo",
               "",
               "_Las cuatro BBDD comparten esquema columnar tras "
               "pre-procesado: 30 columnas canónicas (CRM_ID, "
               "coordenadas, score, biosample, target genes, TFs, disease, "
               "mutation). La pregunta de la sugerencia 1 es si el LLM "
               "modela las mismas clases / propiedades para las cuatro BBDD "
               "dentro de un mismo (experimento × modelo). Métrica: Jaccard "
               "pareado de los conjuntos de URIs (excluidos rdf/rdfs/owl/xsd)."
               "_", ""]
    summary += ["| Experimento | Modelo | n pares | Jaccard medio | "
                "Jaccard min | Jaccard max | Interpretación |",
                "|---|---|---|---|---|---|---|"]
    def interp(j):
        if j >= 0.75: return "muy consistente"
        if j >= 0.50: return "consistente"
        if j >= 0.30: return "parcial"
        return "divergente"
    for (exp, mod), js in sorted(agg.items()):
        if not js: continue
        j_mean = sum(js)/len(js)
        j_min  = min(js); j_max = max(js)
        summary.append(f"| {exp} | {mod} | {len(js)} | {j_mean:.3f} | "
                       f"{j_min:.3f} | {j_max:.3f} | {interp(j_mean)} |")

    out_md = EVAL / "semantic_core_summary.md"
    out_md.write_text("\n".join(summary))
    print(f"[OK] {out_md}")

if __name__ == "__main__":
    main()
