"""Métrica de fidelidad léxico-semántica al dominio cisreg.

Evalúa cuánto reuso de URIs canónicas del dominio (cisreg + ontologías
biomédicas estándar) hace cada ontología LLM-generada, frente a URIs
inventadas en namespaces example.org.

Métricas por archivo:
  - n_canonical: URIs cuyo namespace pertenece al gold (cisreg + obo + etc.)
  - n_invented:  URIs en example.org/* (claramente inventadas)
  - canonical_ratio = n_canonical / (n_canonical + n_invented)
  - overlap_count:  |gold_uris ∩ generated_uris|
  - jaccard:        |∩| / |∪|
  - precision_vs_gold: |∩| / |generated_canonical|
  - recall_vs_gold:    |∩| / |gold_uris|

No usa rdflib: parsea @prefix y términos prefix:local con regex,
suficiente para la métrica.

Outputs:
  - results/evaluation/cisreg_fidelity.csv      (una fila por TTL)
  - results/evaluation/cisreg_fidelity_summary.md
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path("/sessions/nifty-beautiful-knuth/mnt/TFM")
RES  = ROOT / "results"
EVAL = RES / "evaluation"
REFS = Path("/sessions/nifty-beautiful-knuth/mnt/RAGannotationAPI/embeddings/ontologies")

# ───────────── namespaces "canónicos" del dominio ─────────────
# (estos son namespaces reales y autoritativos; cualquier IRI en uno de
# estos cuenta como reuso de vocabulario establecido)
CANONICAL_NS_PREFIXES = (
    "http://rdf.biogateway.eu/",
    "http://purl.obolibrary.org/obo/",
    "http://www.ebi.ac.uk/",
    "https://www.ebi.ac.uk/",
    "http://purl.org/dc/terms/",
    "http://purl.org/linked-data/",
    "http://semanticscience.org/resource/",
    "https://w3id.org/biolink/",
    "http://identifiers.org/",
    "https://identifiers.org/",
    "http://www.ncbi.nlm.nih.gov/",
    "https://www.ncbi.nlm.nih.gov/",
    "http://schema.org/",
    "https://schema.org/",
    "http://www.geneontology.org/",
    "http://purl.uniprot.org/",
    "http://www.bioassayontology.org/",
)
# namespaces que NO cuentan (son sintaxis universal, no dominio)
STANDARD_NS_PREFIXES = (
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/2001/XMLSchema#",
    "http://www.w3.org/2004/02/skos/core#",
    "https://w3id.org/linkml/",
)

INVENTED_NS_PREFIXES = (
    "http://example.org/",
    "https://example.org/",
    "http://example.com/",
)

# ───────────── parser ligero TTL ─────────────
PREFIX_RE = re.compile(
    r"@prefix\s+([A-Za-z_][\w-]*)?\s*:\s*<([^>]+)>\s*\.", re.MULTILINE)
PREFIX_RE_SPARQL = re.compile(
    r"^\s*PREFIX\s+([A-Za-z_][\w-]*)?\s*:\s*<([^>]+)>\s*$",
    re.MULTILINE | re.IGNORECASE)
PNAME_RE = re.compile(r"(?<![\w/#:])([A-Za-z_][\w-]*)?:([A-Za-z_][\w._-]*)")
ABSOLUTE_RE = re.compile(r"<(https?://[^>]+)>")


def parse_prefixes(text: str) -> dict[str, str]:
    out = {}
    for m in PREFIX_RE.finditer(text):
        out[m.group(1) or ""] = m.group(2)
    for m in PREFIX_RE_SPARQL.finditer(text):
        out[m.group(1) or ""] = m.group(2)
    return out


def expand_uris(text: str) -> set[str]:
    """Conjunto de URIs absolutas referenciadas en el texto TTL."""
    prefixes = parse_prefixes(text)
    uris: set[str] = set()
    # absolutas
    for m in ABSOLUTE_RE.finditer(text):
        uris.add(m.group(1))
    # nombres pname (prefix:local)
    for m in PNAME_RE.finditer(text):
        prefix = m.group(1) or ""
        local  = m.group(2)
        if prefix in prefixes:
            uris.add(prefixes[prefix] + local)
    return uris


def classify_namespace(uri: str) -> str:
    for ns in STANDARD_NS_PREFIXES:
        if uri.startswith(ns):
            return "standard"
    for ns in CANONICAL_NS_PREFIXES:
        if uri.startswith(ns):
            return "canonical"
    for ns in INVENTED_NS_PREFIXES:
        if uri.startswith(ns):
            return "invented"
    # otros namespaces (purl.org, w3.org otros, etc.): canonical conservador
    if uri.startswith("http://purl.org/") or uri.startswith("https://purl.org/"):
        return "canonical"
    if uri.startswith("http://www.w3.org/") or uri.startswith("https://www.w3.org/"):
        return "standard"
    # default: cuenta como "otros"
    return "other"


# ───────────── gold set: cisreg references ─────────────
def build_gold_uris() -> tuple[set[str], dict[str, set[str]]]:
    """Extrae URIs canónicas de las 8 ontologías cisreg de referencia.

    Devuelve (gold_set, per_file_dict).
    """
    cisreg_files = [
        "crm.ttl", "crm_example.ttl",
        "crm2gene.ttl", "crm2gene_example.ttl",
        "crm2phen.ttl", "crm2phen_example.ttl",
        "crm2tfac.ttl", "crm2tfac_example.ttl",
    ]
    gold = set()
    per_file = {}
    for f in cisreg_files:
        path = REFS / f
        if not path.exists():
            print(f"[warn] missing {f}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        uris = expand_uris(text)
        # Solo añadimos al gold las URIs canónicas (no las standard como rdf/owl)
        uris_canonical = {u for u in uris
                          if classify_namespace(u) in ("canonical", "other")}
        per_file[f] = uris_canonical
        gold |= uris_canonical
    return gold, per_file


# ───────────── procesar un TTL generado ─────────────
def fidelity_for_file(path: Path, gold: set[str]) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    uris = expand_uris(text)
    n_canonical = 0
    n_invented = 0
    n_standard = 0
    n_other = 0
    generated_canonical = set()
    for u in uris:
        kind = classify_namespace(u)
        if kind == "canonical":
            n_canonical += 1
            generated_canonical.add(u)
        elif kind == "invented":
            n_invented += 1
        elif kind == "standard":
            n_standard += 1
        else:
            n_other += 1
            # tratamos "other" como semicanónico si parece dominio
            if any(k in u.lower() for k in ("ontology", "biology", "gene",
                                            "enhancer", "fantom", "hacer",
                                            "biolink", "obo")):
                generated_canonical.add(u)
    overlap = generated_canonical & gold
    union = generated_canonical | gold
    jaccard = len(overlap) / len(union) if union else 0.0
    canonical_ratio = (n_canonical /
                       max(1, n_canonical + n_invented))
    precision = len(overlap) / len(generated_canonical) \
                if generated_canonical else 0.0
    recall = len(overlap) / len(gold) if gold else 0.0
    return {
        "n_uris_total":  len(uris),
        "n_canonical":   n_canonical,
        "n_invented":    n_invented,
        "n_standard":    n_standard,
        "n_other":       n_other,
        "canonical_ratio":  round(canonical_ratio, 4),
        "overlap_with_gold": len(overlap),
        "jaccard":           round(jaccard, 4),
        "precision_vs_gold": round(precision, 4),
        "recall_vs_gold":    round(recall, 4),
    }


# ───────────── recorrido del corpus ─────────────
def parse_path_meta(path: Path) -> dict:
    """Extrae experimento / BBDD / modelo / variant / run del path."""
    parts = path.relative_to(RES).parts
    meta = {"experiment": "", "db": "", "model_variant": "",
            "variant": "raw", "run": ""}
    if len(parts) >= 2:
        meta["experiment"] = parts[0]
        meta["db"] = parts[1]
    if len(parts) >= 3:
        meta["model_variant"] = parts[2]
    if "postprocessed" in parts:
        meta["variant"] = "postprocessed"
    m = re.search(r"run(\d+)", path.name)
    if m: meta["run"] = m.group(1)
    return meta


def main():
    EVAL.mkdir(parents=True, exist_ok=True)
    gold, per_file = build_gold_uris()
    print(f"[info] gold cisreg URIs: {len(gold)} únicas, "
          f"distribuidas en {len(per_file)} archivos")
    for f, s in per_file.items():
        print(f"    {f:30s} → {len(s)} URIs canónicas")

    out_csv = EVAL / "cisreg_fidelity.csv"
    fieldnames = ["file", "experiment", "db", "model_variant", "variant", "run",
                  "n_uris_total", "n_canonical", "n_invented", "n_standard",
                  "n_other", "canonical_ratio", "overlap_with_gold",
                  "jaccard", "precision_vs_gold", "recall_vs_gold"]
    rows = []
    n = 0
    for p in sorted(RES.rglob("*.ttl")):
        if ".owlcache" in str(p): continue
        meta = parse_path_meta(p)
        if not meta["experiment"]: continue
        try:
            metrics = fidelity_for_file(p, gold)
        except Exception as e:
            print(f"[warn] error en {p}: {e}")
            continue
        row = {"file": str(p.relative_to(RES)), **meta, **metrics}
        rows.append(row); n += 1
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
    print(f"[OK] {n} ontologías procesadas")
    print(f"[OK] {out_csv}")

    # ── agregación por (experimento × modelo_variant) ──
    bucket = defaultdict(list)
    for r in rows:
        # Excluir cache; usar variant raw para E1/E2 (no hay postprocessed real)
        # y postprocessed para E3 cuando exista
        key = (r["experiment"], r["model_variant"])
        bucket[key].append(r)

    summary_lines = ["# Fidelidad cisreg — resumen agregado", ""]
    summary_lines += [f"_Gold set: {len(gold)} URIs canónicas únicas extraídas "
                      f"de las 8 ontologías cisreg de referencia "
                      f"(crm, crm2gene, crm2phen, crm2tfac y sus variantes "
                      f"_example)._", ""]
    summary_lines += [
        "| Experimento | Modelo / variante | n TTL | n_canonical (mean) | "
        "n_invented (mean) | canonical_ratio | overlap | Jaccard | "
        "Recall vs gold |",
        "|---|---|---|---|---|---|---|---|---|"
    ]
    def mean(xs): return round(sum(xs) / len(xs), 3) if xs else 0.0
    for (exp, mod), rs in sorted(bucket.items()):
        # solo postprocessed donde haya (consistente con OQuaRE)
        rs_pp = [r for r in rs if r["variant"] == "postprocessed"]
        rs_use = rs_pp if rs_pp else rs
        if not rs_use: continue
        nc  = mean([r["n_canonical"] for r in rs_use])
        ninv = mean([r["n_invented"] for r in rs_use])
        ratio = mean([r["canonical_ratio"] for r in rs_use])
        ovl = mean([r["overlap_with_gold"] for r in rs_use])
        jac = mean([r["jaccard"] for r in rs_use])
        rec = mean([r["recall_vs_gold"] for r in rs_use])
        summary_lines.append(
            f"| {exp} | {mod} | {len(rs_use)} | {nc} | {ninv} | "
            f"{ratio:.3f} | {ovl} | {jac:.3f} | {rec:.3f} |")

    out_md = EVAL / "cisreg_fidelity_summary.md"
    out_md.write_text("\n".join(summary_lines))
    print(f"[OK] {out_md}")
    return rows


if __name__ == "__main__":
    main()
