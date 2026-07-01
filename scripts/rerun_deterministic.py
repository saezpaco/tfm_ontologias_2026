#!/usr/bin/env python3
"""
Re-ejecuta el banco experimental del TFM con la configuración determinista
recomendada por el tutor (Tabla 2 de la memoria v2):

    temperature       = 0
    top_p             = 1.0   (valor neutro en OpenAI cuando T=0)
    top_k             = 1     (si la API lo admite)
    seed              = 42    (semilla única para las tres réplicas)
    frequency_penalty = 0
    presence_penalty  = 0

Las 3 réplicas con la misma semilla determinista permiten medir el nivel
real de no-determinismo del proveedor (las APIs comerciales no garantizan
determinismo bit-a-bit pese a la configuración; Henderson et al. 2018).

Cubre los cuatro bancos:
  * principal           — 4 técnicas × 3 modelos × 4 BD × 3 réplicas = 144
  * sensibilidad        — E1 y E4 × 4 tipos × 2 BD × 2 modelos × 3 réplicas
  * calibración del RAG — E3 × 3 configs (C1/C2/C3) × 4 BD × 3 réplicas (Llama)
  * barrido N           — E3 × 4 tamaños × 2 BD × 2 modelos × 3 réplicas

Uso típico (desde la raíz del repositorio TFM):

    cd ~/Documents/Claude/Projects/TFM
    export OPENAI_API_KEY=sk-...                # para gpt-4o
    ollama serve &                              # para Llama 3.1 8B y Qwen 2.5 Coder
    python scripts/rerun_deterministic.py --patch-only       # sólo parchea config.py
    python scripts/rerun_deterministic.py --all              # ejecuta los cuatro bancos
    python scripts/rerun_deterministic.py --banco principal  # sólo el principal
    python scripts/rerun_deterministic.py --evaluate         # sólo re-evaluar los TTL
"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ─── Configuración determinista (Tabla 2 de la memoria v2) ─────────────────
DETERMINISTIC_PARAMS = {
    "temperature":       0.0,
    "top_p":             1.0,
    "top_k":             1,
    "seed":              42,
    "frequency_penalty": 0.0,
    "presence_penalty":  0.0,
    "max_tokens":        8192,
}

# Modelos canónicos del banco
MODELS_MAIN = {
    "gpt-4o":           "gpt-4o-2024-05-13",  # snapshot fijo
    "llama3.1:8b":      "llama3.1:8b",
    "qwen2.5-coder:7b": "qwen2.5-coder:7b",
}

DBS_ALL = ["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"]
EXPS_ALL = ["E1", "E2", "E3", "E4"]


# ───────────────────────────────────────────────────────────────────────────
# 1.  Parchear config.py con la configuración determinista
# ───────────────────────────────────────────────────────────────────────────
def patch_config():
    """Sobrescribe GENERATION_PARAMS en scripts/config.py."""
    cfg = ROOT / "scripts" / "config.py"
    text = cfg.read_text(encoding="utf-8")
    new_block = (
        "# ─── Parámetros de generación (DETERMINISTAS - Tabla 2 memoria v2) ──────────\n"
        "GENERATION_PARAMS = {\n"
        '    "temperature":       0.0,\n'
        '    "top_p":             1.0,\n'
        '    "top_k":             1,\n'
        '    "seed":              42,\n'
        '    "frequency_penalty": 0.0,\n'
        '    "presence_penalty":  0.0,\n'
        '    "max_tokens":        8192,\n'
        "}"
    )
    pattern = re.compile(
        r"# ─── Parámetros de generación.*?\n"
        r"GENERATION_PARAMS\s*=\s*\{[^}]*\}",
        re.DOTALL,
    )
    if pattern.search(text):
        backup = cfg.with_suffix(".py.bak")
        backup.write_text(text, encoding="utf-8")
        text = pattern.sub(new_block, text)
        cfg.write_text(text, encoding="utf-8")
        print(f"  ✓ Patched {cfg} (backup en {backup.name})")
    else:
        print(f"  ⚠ No se localizó el bloque GENERATION_PARAMS en {cfg}.")
        print(f"  Por favor edítalo manualmente con los valores de la Tabla 2.")


# ───────────────────────────────────────────────────────────────────────────
# 2.  Banco principal — E1/E2/E3/E4 × 3 modelos × 4 BD × 3 réplicas
# ───────────────────────────────────────────────────────────────────────────
def run_banco_principal():
    print("\n=== BANCO PRINCIPAL ===")
    print("4 técnicas × 3 modelos × 4 BD × 3 réplicas = 144 réplicas planificadas\n")

    # E1, E2, E3 → run_gpt_experiments.py
    for exp in ["E1", "E2", "E3"]:
        for model_short, model_full in MODELS_MAIN.items():
            for db in DBS_ALL:
                cmd = [
                    sys.executable, "scripts/run_gpt_experiments.py",
                    "--model", model_short,
                    "--experiment", exp,
                    "--db", db,
                    "--n-runs", "3",
                ]
                _run(cmd)

    # E4 → run_ontogenix_experiments.py
    for model_short, model_full in MODELS_MAIN.items():
        cmd = [
            sys.executable, "scripts/run_ontogenix_experiments.py",
            "--model", model_full if model_short == "gpt-4o" else model_short,
            "--databases", *DBS_ALL,
            "--runs", "3",
            "--seed", "42",
        ]
        _run(cmd)


# ───────────────────────────────────────────────────────────────────────────
# 3.  Sensibilidad al tipo de muestreo
# ───────────────────────────────────────────────────────────────────────────
def run_sensibilidad_muestreo():
    print("\n=== SENSIBILIDAD AL TIPO DE MUESTREO ===")
    print("E1 y E4 × 4 tipos × 2 BD × 2 modelos × 3 réplicas = 96 réplicas\n")

    samplings = ["A_head", "B_random", "C_stratified", "D_diversity"]
    models = ["gpt-4o", "llama3.1:8b"]
    dbs = ["FANTOM5", "dbSUPER"]

    for sampling in samplings:
        samples_dir = ROOT / "data" / "samples_strategies" / sampling
        if not samples_dir.exists():
            print(f"  ⚠ {samples_dir} no existe, salto {sampling}")
            continue
        for model in models:
            for db in dbs:
                # E1 zero-shot
                cmd = [
                    sys.executable, "scripts/run_gpt_experiments.py",
                    "--model", model,
                    "--experiment", "E1",
                    "--db", db,
                    "--n-runs", "3",
                    "--samples-dir", str(samples_dir),
                    "--results-suffix", f"_{sampling}",
                ]
                _run(cmd)
        # E4 OntoGenix por muestreo (sólo gpt-4o por restricción de la pipeline)
        csv_dir = ROOT / "data" / "samples_strategies" / sampling
        cmd = [
            sys.executable, "scripts/run_ontogenix_experiments.py",
            "--model", "gpt-4o-2024-05-13",
            "--databases", *dbs,
            "--runs", "3",
            "--seed", "42",
            "--csv-dir", str(csv_dir),
            "--results-suffix", f"_{sampling}",
        ]
        _run(cmd)


# ───────────────────────────────────────────────────────────────────────────
# 4.  Calibración del RAG semántico sobre Llama 3.1 8B
# ───────────────────────────────────────────────────────────────────────────
def run_calibracion_rag():
    print("\n=== CALIBRACIÓN DEL RAG (Llama 3.1 8B en E3) ===")
    print("3 configs × 4 BD × 3 réplicas = 36 réplicas\n")
    configs = {
        # C1, C2, C3 según §4.5.2 de la memoria
        "C1": {"top_k": 2, "score_thr": 0.4, "max_chars": 5000},
        "C2": {"top_k": 5, "score_thr": 0.6, "max_chars": 5000},
        "C3": {"top_k": 2, "score_thr": 0.6, "max_chars": 2000},
    }
    for label, p in configs.items():
        for db in DBS_ALL:
            cmd = [
                sys.executable, "scripts/run_gpt_experiments.py",
                "--model", "llama3.1:8b",
                "--experiment", "E3",
                "--db", db,
                "--n-runs", "3",
                "--rag-backend", "api",
                "--rag-top-k", str(p["top_k"]),
                "--rag-score-thr", str(p["score_thr"]),
                "--rag-max-chars", str(p["max_chars"]),
                "--results-suffix", f"_{label}",
            ]
            _run(cmd)


# ───────────────────────────────────────────────────────────────────────────
# 5.  Barrido del tamaño de muestra
# ───────────────────────────────────────────────────────────────────────────
def run_barrido_n():
    print("\n=== BARRIDO DEL TAMAÑO MUESTRAL ===")
    print("4 tamaños × 2 BD × 2 modelos × 3 réplicas = 48 réplicas\n")
    sizes = [25, 50, 100, 200]
    models = ["gpt-4o", "llama3.1:8b"]
    dbs = ["FANTOM5", "dbSUPER"]
    for N in sizes:
        samples_dir = ROOT / "data" / "samples_sizes" / f"N={N}"
        if not samples_dir.exists():
            print(f"  ⚠ {samples_dir} no existe, salto N={N}")
            continue
        for model in models:
            for db in dbs:
                cmd = [
                    sys.executable, "scripts/run_gpt_experiments.py",
                    "--model", model,
                    "--experiment", "E3",
                    "--db", db,
                    "--n-runs", "3",
                    "--samples-dir", str(samples_dir),
                    "--rag-backend", "api",
                    "--results-suffix", f"_N{N}",
                ]
                _run(cmd)


# ───────────────────────────────────────────────────────────────────────────
# 6.  Evaluación completa
# ───────────────────────────────────────────────────────────────────────────
def evaluate_all():
    print("\n=== EVALUACIÓN COMPLETA ===\n")
    steps = [
        ["scripts/postprocess_ttl.py", "--batch"],
        ["scripts/05_evaluate_results.py"],
        ["scripts/oquare_eval.py", "--batch"],
        ["scripts/cisreg_fidelity.py"],
        ["scripts/competency_questions.py"],
        ["scripts/statistical_tests.py"],
    ]
    for cmd in steps:
        _run([sys.executable] + cmd)


# ───────────────────────────────────────────────────────────────────────────
# Util
# ───────────────────────────────────────────────────────────────────────────
def _run(cmd):
    """Run a subprocess command with logging; non-fatal errors."""
    print(f"  → {' '.join(str(c) for c in cmd[1:])}")
    try:
        subprocess.run(cmd, cwd=ROOT, check=False)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        sys.exit(130)


# ───────────────────────────────────────────────────────────────────────────
# Entry point
# ───────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--patch-only", action="store_true",
                        help="Sólo parchear scripts/config.py con la nueva configuración.")
    parser.add_argument("--no-patch", action="store_true",
                        help="No parchear config.py (asumir que ya está ajustado).")
    parser.add_argument("--all", action="store_true",
                        help="Re-ejecutar los cuatro bancos + evaluación.")
    parser.add_argument("--banco",
                        choices=["principal", "sensibilidad", "calibracion", "barrido"],
                        help="Re-ejecutar un banco concreto.")
    parser.add_argument("--evaluate", action="store_true",
                        help="Sólo re-evaluar los TTL ya generados.")
    args = parser.parse_args()

    if not args.no_patch:
        print("Aplicando configuración determinista a scripts/config.py...")
        patch_config()
        if args.patch_only:
            return

    t0 = time.time()
    if args.evaluate:
        evaluate_all()
    elif args.all:
        run_banco_principal()
        run_sensibilidad_muestreo()
        run_calibracion_rag()
        run_barrido_n()
        evaluate_all()
    elif args.banco == "principal":
        run_banco_principal()
    elif args.banco == "sensibilidad":
        run_sensibilidad_muestreo()
    elif args.banco == "calibracion":
        run_calibracion_rag()
    elif args.banco == "barrido":
        run_barrido_n()
    else:
        parser.print_help()
        return

    print(f"\n=== TIEMPO TOTAL: {(time.time()-t0)/60:.1f} min ===")


if __name__ == "__main__":
    main()
