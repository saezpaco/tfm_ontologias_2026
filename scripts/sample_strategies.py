#!/usr/bin/env python3
"""
sample_strategies.py
────────────────────
Genera muestras de las bases de datos siguiendo cuatro estrategias
distintas, para realizar un análisis de sensibilidad al muestreo en los
experimentos E1 y E4.

Estrategias
-----------
A. **head**          — Cabecera: las primeras N filas tras el header.
                       Reproducible y determinista. Es la que usa el TFM
                       por defecto.
B. **random**        — Aleatorio uniforme con seed fijo. Estimador
                       insesgado de la distribución de la base.
C. **stratified**    — Estratificado por la columna categórica más
                       informativa (cell line / biosample / tissue).
                       Garantiza representación de cada categoría con
                       cuota proporcional.
D. **diversity**     — Máxima diversidad léxica: para cada columna
                       categórica se eligen filas que cubran el mayor
                       número de valores únicos posibles.

Uso
---
    # Genera las 4 estrategias x N BBDD a partir de los TSV originales
    python scripts/sample_strategies.py \
           --input-dir data/raw \
           --output-dir data/samples_strategies \
           --databases FANTOM5 dbSUPER \
           --n-rows 25

    # Si solo tienes los samples actuales (25 filas), el script se adapta
    # haciendo sub-muestreo dentro de ellos
    python scripts/sample_strategies.py \
           --input-dir data/samples \
           --suffix _sample.tsv \
           --output-dir data/samples_strategies \
           --databases FANTOM5 dbSUPER \
           --n-rows 15

Salida
------
    data/samples_strategies/
        A_head/
            FANTOM5.csv
            FANTOM5_sample_prompt.txt
            dbSUPER.csv
            dbSUPER_sample_prompt.txt
        B_random/      (idem)
        C_stratified/  (idem)
        D_diversity/   (idem)

El nombre de archivo `*_sample_prompt.txt` es el que ya consume
``run_gpt_experiments.py``; el ``*.csv`` es el que consume
``run_ontogenix_experiments.py``. Así, cualquier estrategia puede
inyectarse cambiando solo la variable de entorno ``SAMPLES_DIR`` o el
flag ``--samples-dir``.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT  = PROJECT_ROOT / "data" / "raw"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "samples_strategies"

STRATEGIES = ["A_head", "B_random", "C_stratified", "D_diversity"]

# Columnas candidatas a estratificación, en orden de preferencia.
# Se elige la primera que exista en el DataFrame con cardinalidad
# razonable (entre 2 y MAX_STRATIFY_CARDINALITY valores únicos).
STRATIFY_CANDIDATES = [
    "cell_name",          # dbSUPER raw (líneas celulares)
    "biosample_name",     # dbSUPER enriquecido
    "biosample",          # FANTOM5 enriquecido
    "cell_line",          # genérico
    "tissue",
    "cell_type",
    "gene_symbol",        # dbSUPER raw (gen diana)
    "hgnc_symbol_target_genes",
    "type",               # categórico amplio
    "source",
    "enh_method",
    "current_chr",        # fallback geográfico
    "orig_chr",
    "chrom",              # último fallback (cromosoma)
]
MAX_STRATIFY_CARDINALITY = 500   # evita columnas con valores casi-únicos


# Nombres estándar BED12 (UCSC) — usados para FANTOM5 que no trae header
BED12_COLS = [
    "chrom", "chromStart", "chromEnd", "name", "score", "strand",
    "thickStart", "thickEnd", "itemRgb", "blockCount",
    "blockSizes", "blockStarts",
]


def load_table(path: Path, separator: str = "\t",
               has_header: bool | None = None) -> pd.DataFrame:
    """Carga un TSV/BED ignorando filas mal formadas y limpiando headers.

    has_header=None → autodetecta: si la primera fila empieza con 'chr' es
    BED y se asignan nombres BED12 estándar.
    """
    if has_header is None:
        # Heurística: si la primera fila parece datos (chr1/chrX/chr22…) y
        # la columna 2 es un entero (start position BED), no hay header.
        # Si la primera columna es exactamente "chrom" o no empieza por "chr"
        # seguido de número, asumimos que sí hay header.
        import re
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            first_row = f.readline().rstrip("\n").split(separator)
        first_cell = first_row[0].strip().lower()
        looks_like_chr_value = bool(re.match(r"^chr[\dxymtXYMT]+$", first_cell))
        col2_is_int = (len(first_row) >= 2 and
                       first_row[1].strip().isdigit())
        has_header = not (looks_like_chr_value and col2_is_int)

    if has_header:
        df = pd.read_csv(path, sep=separator, dtype=str,
                         keep_default_na=False, on_bad_lines="skip")
        # Strip whitespace en headers y valores
        df.columns = [c.strip() for c in df.columns]
        for c in df.columns:
            df[c] = df[c].astype(str).str.strip()
    else:
        df = pd.read_csv(path, sep=separator, dtype=str, header=None,
                         keep_default_na=False, on_bad_lines="skip")
        # Asignar nombres BED12 (truncar/pad si las columnas no coinciden)
        n = len(df.columns)
        if n <= len(BED12_COLS):
            df.columns = BED12_COLS[:n]
        else:
            df.columns = BED12_COLS + [f"col{i}" for i in range(len(BED12_COLS), n)]
        for c in df.columns:
            df[c] = df[c].astype(str).str.strip()
    return df


def pick_stratify_col(df: pd.DataFrame) -> str | None:
    """Elige la columna categórica más informativa para estratificar.
    Prioriza columnas semánticamente ricas (cell_name, biosample, etc.) y
    descarta columnas con cardinalidad excesiva (>500) que serían casi-id."""
    for c in STRATIFY_CANDIDATES:
        if c in df.columns:
            unique = df[c].nunique()
            if 2 <= unique <= MAX_STRATIFY_CARDINALITY:
                return c
    # Fallback: primera columna con cardinalidad razonable
    for c in df.columns:
        u = df[c].nunique()
        if 2 <= u <= MAX_STRATIFY_CARDINALITY:
            return c
    return None


# ─── Estrategias ─────────────────────────────────────────────────────
def strategy_head(df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    return df.head(n).reset_index(drop=True)


def strategy_random(df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    if len(df) <= n:
        return df.copy().reset_index(drop=True)
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


def strategy_stratified(df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    col = pick_stratify_col(df)
    if col is None or len(df) <= n:
        return strategy_random(df, n, seed)
    counts = df[col].value_counts()
    # Si hay más categorías que cuota, no podemos garantizar 1 por categoría
    # → seleccionamos las n_cat categorías más frecuentes hasta agotar n.
    if len(counts) > n:
        # Top-n categorías por frecuencia, 1 fila por categoría
        top_cats = counts.head(n).index
        parts = [df[df[col] == c].sample(n=1, random_state=seed)
                 for c in top_cats]
    else:
        # Cuota proporcional, mínimo 1; ajuste hasta sumar exactamente n
        quotas = (counts / counts.sum() * n).round().astype(int).clip(lower=1)
        while quotas.sum() > n and (quotas > 1).any():
            quotas.loc[quotas.idxmax()] -= 1
        while quotas.sum() < n:
            quotas.loc[quotas.idxmin()] += 1
        parts = [df[df[col] == c].sample(n=min(k, len(df[df[col] == c])),
                                         random_state=seed)
                 for c, k in quotas.items()]
    return pd.concat(parts).sample(frac=1, random_state=seed).reset_index(drop=True)


def strategy_diversity(df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    """Selecciona iterativamente filas que maximizan la cobertura conjunta
    de valores únicos a través de las columnas categóricas."""
    if len(df) <= n:
        return df.copy().reset_index(drop=True)
    cat_cols = [c for c in df.columns
                if 2 <= df[c].nunique() <= len(df)]
    if not cat_cols:
        return strategy_random(df, n, seed)
    rng = random.Random(seed)
    selected: list[int] = []
    seen: dict[str, set[str]] = {c: set() for c in cat_cols}
    indices = list(df.index)
    rng.shuffle(indices)
    # Greedy: en cada paso, elegir la fila que añada más valores nuevos
    while len(selected) < n and indices:
        best_idx = None
        best_gain = -1
        for idx in indices:
            row = df.loc[idx]
            gain = sum(1 for c in cat_cols
                       if str(row[c]) not in seen[c])
            if gain > best_gain:
                best_gain = gain
                best_idx = idx
                if gain == len(cat_cols):
                    break
        if best_idx is None:
            break
        selected.append(best_idx)
        for c in cat_cols:
            seen[c].add(str(df.loc[best_idx, c]))
        indices.remove(best_idx)
    return df.loc[selected].reset_index(drop=True)


STRATEGY_FN = {
    "A_head":       strategy_head,
    "B_random":     strategy_random,
    "C_stratified": strategy_stratified,
    "D_diversity":  strategy_diversity,
}


# ─── Utilidades de salida ────────────────────────────────────────────
def df_to_prompt_txt(df: pd.DataFrame, max_chars: int = 12000) -> str:
    """Convierte el DataFrame a un bloque TSV legible para el prompt.
    Trunca por longitud para no rebasar la ventana del modelo."""
    lines = ["\t".join(df.columns)]
    for _, row in df.iterrows():
        lines.append("\t".join(str(v).strip() for v in row.values))
    text = "\n".join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n# [muestra truncada por longitud]"
    return text


def diversity_report(df: pd.DataFrame, sample: pd.DataFrame,
                      max_cardinality: int = MAX_STRATIFY_CARDINALITY) -> dict:
    """Métricas de cobertura del muestreo respecto al universo. Solo
    reporta columnas con cardinalidad ≤ max_cardinality (categóricas)."""
    cat_cols = [c for c in df.columns
                if 2 <= df[c].nunique() <= max_cardinality]
    cov = {}
    for c in cat_cols:
        u_full = df[c].nunique()
        u_sample = sample[c].nunique()
        cov[c] = {
            "unique_in_universe": int(u_full),
            "unique_in_sample":   int(u_sample),
            "coverage_ratio":     round(u_sample / u_full, 3) if u_full else 0,
        }
    return cov


def export_strategy(df: pd.DataFrame,
                    db: str,
                    strategy: str,
                    out_dir: Path,
                    n_rows: int,
                    seed: int) -> dict:
    fn = STRATEGY_FN[strategy]
    sample = fn(df, n_rows, seed)
    s_dir = out_dir / strategy
    s_dir.mkdir(parents=True, exist_ok=True)
    csv_path = s_dir / f"{db}.csv"
    txt_path = s_dir / f"{db}_sample_prompt.txt"
    sample.to_csv(csv_path, index=False)
    txt_path.write_text(df_to_prompt_txt(sample), encoding="utf-8")
    def rel_or_abs(p: Path) -> str:
        try:    return str(p.resolve().relative_to(PROJECT_ROOT))
        except ValueError: return str(p.resolve())
    rep = {
        "strategy":         strategy,
        "db":               db,
        "n_universe":       len(df),
        "n_sample":         len(sample),
        "stratify_column":  pick_stratify_col(df),
        "coverage":         diversity_report(df, sample),
        "csv_path":         rel_or_abs(csv_path),
        "txt_path":         rel_or_abs(txt_path),
    }
    return rep


# ─── Orquestación ────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir",  type=Path, default=DEFAULT_INPUT,
                    help="Carpeta con los TSV originales o samples")
    ap.add_argument("--suffix",     default=".tsv",
                    help="Sufijo de archivo (default '.tsv'). "
                         "Para muestras pre-reducidas usa '_sample.tsv'")
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--databases",  nargs="+",
                    default=["FANTOM5", "dbSUPER"],
                    help="BBDD a procesar (default: %(default)s)")
    ap.add_argument("--n-rows",     type=int, default=25,
                    help="Filas de muestra por estrategia (default 25)")
    ap.add_argument("--seed",       type=int, default=42)
    ap.add_argument("--separator",  default="\t",
                    help="Separador del archivo de entrada (default \\t)")
    args = ap.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []
    for db in args.databases:
        in_path = args.input_dir / f"{db}{args.suffix}"
        if not in_path.exists():
            print(f"[skip] No existe {in_path}", file=sys.stderr)
            continue
        df = load_table(in_path, separator=args.separator)
        print(f"\n=== {db} ({len(df)} filas, {len(df.columns)} columnas) ===")
        for strategy in STRATEGIES:
            rep = export_strategy(df, db, strategy, args.output_dir,
                                  args.n_rows, args.seed)
            report.append(rep)
            cov_summary = ", ".join(
                f"{c}:{m['coverage_ratio']*100:.0f}%"
                for c, m in list(rep["coverage"].items())[:4]
            )
            print(f"  [{strategy}]  n={rep['n_sample']}  "
                  f"strat_col={rep['stratify_column']}  "
                  f"cov={cov_summary}")

    rep_path = args.output_dir / "_sampling_report.json"
    rep_path.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"\n[OK] Reporte → {rep_path}")
    print(f"[OK] Muestras → {args.output_dir}/{{A,B,C,D}}_*/<DB>{{.csv,_sample_prompt.txt}}")


if __name__ == "__main__":
    main()
