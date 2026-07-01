#!/usr/bin/env python3
"""
build_sampling_grid.py
──────────────────────
Generador unificado de la rejilla de muestreo de la Fase 1 (revisión del tutor):
cruza TIPO DE MUESTREO × TAMAÑO DE MUESTRA en una sola pasada, para todas las
bases de datos, de modo que la mejor pareja (tipo, N) pueda elegirse sin asumir
un orden (resuelve el problema del «huevo o la gallina»).

Reutiliza la lógica de muestreo ya validada en ``sample_strategies.py``
(estrategias A_head / B_random / C_stratified / D_diversity) y la generaliza
añadiendo el eje del tamaño N.

Salida (estructura consumible por los runners existentes)
--------------------------------------------------------
    data/grid/
        A_head/
            N=25/   FANTOM5.csv  FANTOM5_sample_prompt.txt  dbSUPER.csv ...
            N=50/   ...
            N=100/  ...
            N=200/  ...
        B_random/   (idem)
        C_stratified/ (idem)
        D_diversity/  (idem)
        _grid_manifest.csv   _grid_manifest.json

  · ``{DB}.csv``              → lo consume run_ontogenix_experiments.py (--csv-dir)
  · ``{DB}_sample_prompt.txt``→ lo consume run_gpt_experiments.py / 04_run_experiments.py
    (--samples-dir apuntando a data/grid/<tipo>/N=<n>/)

Uso
---
    # Rejilla completa (4 tipos × 4 tamaños × 4 BD) desde el dato canónico.
    # En tu máquina, --input-dir debe apuntar al dato completo de las 4 BD
    # (p. ej. $TFM_DATA_ROOT/CRM/processed_db). FANTOM5 y dbSUPER también
    # están en data/raw dentro del repo.
    python scripts/build_sampling_grid.py \
        --input-dir "$TFM_DATA_ROOT/CRM/processed_db" \
        --databases FANTOM5 dbSUPER HACER DiseaseEnhancer \
        --sizes 25 50 100 200

    # Subconjunto de prueba (solo lo que hay en el repo):
    python scripts/build_sampling_grid.py --input-dir data/raw \
        --databases FANTOM5 dbSUPER --sizes 25 50

Notas
-----
· La muestra es única por celda (tipo, N) con semilla fija; las 3 réplicas del
  banco varían la semilla de generación del MODELO, no la muestra.
· El coste estimado de tokens/€ por celda (gpt-4o) se incluye en el manifest
  para planificar la ejecución.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# Reutilizamos la librería de muestreo ya validada del propio repo.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sample_strategies import (  # noqa: E402
    STRATEGIES, STRATEGY_FN, load_table, df_to_prompt_txt,
    pick_stratify_col, diversity_report,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _default_input_dir() -> Path:
    """Carpeta de datos por defecto: la `processed_db` de config.py (la misma
    que valida el preflight). Si no existe, cae a data/raw del repo. Así no
    depende de la variable de entorno TFM_DATA_ROOT."""
    try:
        import io
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            import config  # noqa: E402  (ya tenemos scripts/ en sys.path)
        p = Path(config.PATHS["processed_db"])
        if p.exists():
            return p
    except Exception:
        pass
    return PROJECT_ROOT / "data" / "raw"


# Metadatos por BD (descripción y fuente) para el encabezado del prompt.
DB_META = {
    "FANTOM5":        ("Enhancers activos identificados por CAGE-seq", "https://fantom.gsc.riken.jp/5/"),
    "dbSUPER":        ("Super-enhancers con coordenadas, líneas celulares y genes diana", "https://asntech.org/dbsuper/"),
    "HACER":          ("Human Active Cis-regulatory Elements database", "http://bioinfo.vanderbilt.edu/AE/HACER/"),
    "DiseaseEnhancer":("Enhancers asociados a enfermedades", "http://biocc.hrbmu.edu.cn/DiseaseEnhancer/"),
}
STRAT_LABEL = {
    "A_head": "A_head (cabecera determinista)",
    "B_random": "B_random (aleatorio, semilla fija)",
    "C_stratified": "C_stratified (estratificado por columna categórica)",
    "D_diversity": "D_diversity (máxima diversidad léxica)",
}
# Coste API gpt-4o por 1k tokens (entrada+salida aprox., snapshot 2024-05-13).
USD_PER_1K_IN = 0.005
USD_PER_1K_OUT = 0.015
OUTPUT_TOKENS_EST = 3000          # estimación de salida TTL por run (de sample_size_estimates)


def build_prompt(df, db: str, strategy: str, n_universe: int) -> str:
    desc, url = DB_META.get(db, ("", ""))
    head = [
        f"# Base de datos: {db}",
        f"# Descripción: {desc}",
        f"# Fuente: {url}",
        f"# Dimensiones totales: {n_universe} filas, {len(df.columns)} columnas",
        f"# Filas en esta muestra: {len(df)}",
        f"# Estrategia: {STRAT_LABEL.get(strategy, strategy)}",
        "",
        "# MUESTRA DE DATOS (formato TSV):",
        "",
    ]
    return "\n".join(head) + "\n" + df_to_prompt_txt(df)


def rel(p: Path) -> str:
    """Ruta relativa al proyecto si es posible; si no, absoluta."""
    try:
        return str(p.resolve().relative_to(PROJECT_ROOT))
    except ValueError:
        return str(p.resolve())


def est_tokens(prompt_text: str) -> int:
    # ~4 caracteres por token (heurística estándar para texto en inglés/código).
    return max(1, round(len(prompt_text) / 4))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir", type=Path, default=_default_input_dir(),
                    help="Carpeta con los datos completos por BD. Por defecto usa la "
                         "processed_db de config.py (la del preflight); si no, data/raw.")
    ap.add_argument("--suffix", default=".tsv", help="Sufijo de los ficheros de entrada (default .tsv)")
    ap.add_argument("--separator", default="\t", help="Separador del fichero de entrada")
    ap.add_argument("--databases", nargs="+",
                    default=["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"])
    ap.add_argument("--strategies", nargs="+", default=STRATEGIES)
    ap.add_argument("--sizes", nargs="+", type=int, default=[25, 50, 100, 200])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "data" / "grid")
    ap.add_argument("--diversity-pool", type=int, default=3000,
                    help="Para D_diversity, sub-muestrea antes un pool aleatorio de este "
                         "tamaño si el universo es mayor (acota el coste del greedy sin "
                         "perder diversidad; default 3000). 0 = sin límite.")
    args = ap.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    for db in args.databases:
        in_path = args.input_dir / f"{db}{args.suffix}"
        if not in_path.exists():
            print(f"[skip] No existe {in_path} — omito {db}", file=sys.stderr)
            continue
        df = load_table(in_path, separator=args.separator)
        n_universe = len(df)
        print(f"\n=== {db}  ({n_universe} filas, {len(df.columns)} columnas) ===")
        for strategy in args.strategies:
            if strategy not in STRATEGY_FN:
                print(f"  [warn] estrategia desconocida: {strategy}", file=sys.stderr); continue
            # D_diversity es un greedy O(universo·N): sobre universos grandes
            # se acota con un pool aleatorio previo (la diversidad dentro de un
            # pool aleatorio amplio es equivalente a la del universo completo).
            src_df = df
            if (strategy == "D_diversity" and args.diversity_pool
                    and len(df) > args.diversity_pool):
                src_df = df.sample(n=args.diversity_pool,
                                   random_state=args.seed).reset_index(drop=True)
            for n in args.sizes:
                sample = STRATEGY_FN[strategy](src_df, n, args.seed)
                cell = args.output_dir / strategy / f"N={n}"
                cell.mkdir(parents=True, exist_ok=True)
                csv_path = cell / f"{db}.csv"
                txt_path = cell / f"{db}_sample_prompt.txt"
                sample.to_csv(csv_path, index=False)
                prompt = build_prompt(sample, db, strategy, n_universe)
                txt_path.write_text(prompt, encoding="utf-8")

                tin = est_tokens(prompt)
                cost = (tin / 1000 * USD_PER_1K_IN
                        + OUTPUT_TOKENS_EST / 1000 * USD_PER_1K_OUT)
                manifest.append({
                    "db": db, "strategy": strategy, "N": n,
                    "n_universe": n_universe, "n_sample": len(sample),
                    "stratify_column": pick_stratify_col(df) if strategy == "C_stratified" else "",
                    "prompt_tokens_est": tin,
                    "cost_per_run_gpt4o_usd": round(cost, 4),
                    "csv_path": rel(csv_path),
                    "txt_path": rel(txt_path),
                })
                print(f"  [{strategy:<13} N={n:<3}] n={len(sample):<3} "
                      f"~{tin} tok  ~${cost:.4f}/run")

    # Manifest
    mj = args.output_dir / "_grid_manifest.json"
    mc = args.output_dir / "_grid_manifest.csv"
    mj.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    if manifest:
        with open(mc, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
            w.writeheader(); w.writerows(manifest)
    # Resumen de coste
    n_cells = len(manifest)
    total_gpt = sum(m["cost_per_run_gpt4o_usd"] for m in manifest)
    print(f"\n[OK] {n_cells} celdas (tipo×N×BD) → {args.output_dir}")
    print(f"[OK] Manifest → {rel(mc)}  ·  {rel(mj)}")
    print(f"[i ] Coste gpt-4o por réplica (suma de celdas): ~${total_gpt:.2f}  "
          f"(×3 réplicas ≈ ${total_gpt*3:.2f}; los modelos Ollama no tienen coste $)")


if __name__ == "__main__":
    main()
