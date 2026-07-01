#!/usr/bin/env python3
"""
run_phases.py
─────────────
Orquestador de las tres fases del protocolo experimental (revisión del tutor).
Recorre la rejilla, enruta cada (modelo, experimento) al runner correcto con los
flags de trazabilidad, post-procesa y aplica el driver de evaluación de TRES
NIVELES uniforme. Incluye un subcomando `select` que aplica la regla de
selección lexicográfica para fijar parámetros entre fases.

Por defecto NO ejecuta nada: imprime el plan de comandos (--dry-run). Añade
``--execute`` para lanzarlo de verdad. Así puedes revisar el plan antes de
gastar cómputo.

Fases
-----
  phase1 : sensibilidad conjunta muestreo×tamaño (rejilla de data/grid).
           Fija la pareja (tipo*, N*).  → luego: `select --for phase1`
  phase2 : calibración del RAG (baseline/C1/C2/C3) con (tipo*, N*) fijos.
           Fija la configuración RAG*.   → luego: `select --for phase2`
  phase3 : banco principal completo con (tipo*, N*, RAG*) congelados.
  select : aplica la regla lexicográfica sobre results/evaluation/
           threelevel_summary.csv y propone el mejor nivel.

Política de enrutado (default)
------------------------------
  · E1, E2, E3 · cualquier modelo → run_gpt_experiments.py
        run_gpt_experiments.py gestiona AMBOS proveedores: lee provider de
        config.LLM_MODELS y, si es Ollama, enruta solo a localhost:11434/v1.
        Es donde vive el RAG semántico (annotationRAG) y los top_k/score_thr de
        la calibración, así que mantiene E1–E3 coherentes para los tres modelos.
  · E4 · cualquier modelo         → run_ontogenix_experiments.py
  · Alternativa: --ollama-e12-runner 04 manda E1/E2 de modelos abiertos por
    04_run_experiments.py (no usa annotationRAG).
Cada generación E1–E3 se post-procesa (postprocess_ttl.py) y todo se evalúa con
evaluate_three_levels.py.

Ejemplos
--------
    # Ver el plan de la Fase 1 (no ejecuta):
    python scripts/run_phases.py phase1 --grid-dir data/grid

    # Ejecutar la Fase 1 de verdad:
    python scripts/run_phases.py phase1 --grid-dir data/grid --execute

    # Elegir la mejor (tipo, N) tras la Fase 1:
    python scripts/run_phases.py select --for phase1

    # Fase 2 con la pareja elegida:
    python scripts/run_phases.py phase2 --sampling A_head --size 25 --execute
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PROJECT_ROOT / "scripts"
PY = sys.executable

GPT_MODELS = {"gpt-4o", "gpt-4o-mini", "gpt-4o-2024-05-13"}
DEFAULT_MODELS = ["gpt-4o", "llama3.1:8b", "qwen2.5-coder:7b"]
DEFAULT_DBS = ["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"]
DEFAULT_SAMPLINGS = ["A_head", "B_random", "C_stratified", "D_diversity"]
DEFAULT_SIZES = [25, 50, 100, 200]
RAG_CONFIGS = {
    "baseline": {},
    "C1": {"--rag-top-k": "2"},
    "C2": {"--rag-score-thr": "0.6"},
    "C3": {"--rag-top-k": "2", "--rag-score-thr": "0.6"},
}
# Coste aproximado gpt-4o por run (de sample_size_estimates), para estimar.
GPT_COST_PER_RUN = 0.05


def folder(model: str, suffix: str) -> str:
    # Los runners (run_gpt_experiments / run_ontogenix) concatenan el sufijo al
    # nombre del modelo SIN separador (p. ej. gpt-4oA_head_N25). Reproducimos esa
    # convención para que already_done() y postprocess_ttl --models coincidan con
    # las carpetas reales. El análisis usa las columnas parseadas (model, sampling,
    # N), no el nombre crudo de la carpeta.
    base = model.replace(":", "_")
    return f"{base}{suffix}" if suffix else base


def gen_cmd(model, exp, db, samples_dir, suffix, n_runs, rag_over=None,
            ollama_runner="gpt"):
    """Comando de generación para una celda, según la política de enrutado.

    Por defecto TODO E1–E3 (gpt-4o y modelos abiertos) se enruta por
    run_gpt_experiments.py, que gestiona ambos proveedores (Ollama →
    localhost:11434/v1) y el RAG semántico (annotationRAG). E4 → OntoGenix.
    Con ollama_runner="04", E1/E2 de modelos abiertos usan 04_run_experiments.py.
    """
    rag_over = rag_over or {}
    if exp == "E4":
        return [PY, str(SCRIPTS / "run_ontogenix_experiments.py"),
                "--databases", db, "--runs", str(n_runs),
                "--model", "gpt-4o-2024-05-13" if model == "gpt-4o" else model,
                "--csv-dir", str(samples_dir), "--results-suffix", suffix]
    use_gpt_runner = (model in GPT_MODELS) or (exp == "E3") or (ollama_runner == "gpt")
    if use_gpt_runner:
        cmd = [PY, str(SCRIPTS / "run_gpt_experiments.py"),
               "--model", model, "--experiment", exp, "--db", db,
               "--n-runs", str(n_runs),
               "--samples-dir", str(samples_dir), "--results-suffix", suffix]
        for k, v in rag_over.items():
            cmd += [k, v]
        return cmd
    # E1/E2 de modelo Ollama por el runner alternativo (04)
    return [PY, str(SCRIPTS / "04_run_experiments.py"),
            "--experiment", exp, "--model", model, "--db", db,
            "--n-runs", str(n_runs),
            "--samples-dir", str(samples_dir), "--results-suffix", suffix]


def already_done(exp, db, fold, n_runs) -> bool:
    base = PROJECT_ROOT / "results" / exp / db / fold
    if not base.exists():
        return False
    ttls = list(base.glob("ontology_run*.ttl")) + list((base / "postprocessed").glob("ontology_run*.ttl"))
    return len({t.name for t in ttls}) >= n_runs


def run(cmd, execute):
    print("    $ " + " ".join(cmd))
    if execute:
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print(f"    [!] returncode={r.returncode}", file=sys.stderr)


def collect_jobs(models, exps, dbs, samplings, sizes, grid_dir, n_runs,
                 fixed_sampling=None, fixed_size=None, rag_configs=None,
                 exclude=None):
    """Devuelve lista de (model, exp, db, samples_dir, suffix, rag_over, fold)."""
    exclude = exclude or set()
    jobs = []
    samp_levels = [fixed_sampling] if fixed_sampling else samplings
    size_levels = [fixed_size] if fixed_size else sizes
    for model in models:
        for exp in exps:
            if (model, exp) in exclude:
                continue
            for db in dbs:
                for samp in samp_levels:
                    for N in size_levels:
                        samples_dir = grid_dir / samp / f"N={N}"
                        cfgs = rag_configs if (rag_configs and exp == "E3") else {None: {}}
                        for cfg_name, rag_over in cfgs.items():
                            parts = [samp, f"N{N}"]
                            if cfg_name:
                                parts.append(cfg_name)
                            suffix = "_".join(parts)
                            jobs.append((model, exp, db, samples_dir, suffix,
                                         rag_over, folder(model, suffix)))
    return jobs


def execute_phase(jobs, n_runs, execute, postproc=True, evaluate=True, skip_done=True,
                  ollama_runner="gpt"):
    n_total = len(jobs)
    n_runs_total = n_total * n_runs
    n_gpt = sum(1 for j in jobs if j[0] in GPT_MODELS)
    print(f"\n[plan] {n_total} celdas × {n_runs} réplicas = {n_runs_total} ejecuciones")
    print(f"[plan] coste gpt-4o estimado ≈ ${n_gpt * n_runs * GPT_COST_PER_RUN:.2f} "
          f"({n_gpt} celdas gpt); los modelos Ollama no tienen coste $ (sí horas).")
    variants_e123 = []
    skipped = 0
    for (model, exp, db, samples_dir, suffix, rag_over, fold) in jobs:
        done = skip_done and already_done(exp, db, fold, n_runs)
        if done:
            skipped += 1
        elif not samples_dir.exists():
            print(f"    [skip] no existe {samples_dir} (genera la rejilla primero)", file=sys.stderr)
        else:
            print(f"  · {exp} {db} {model} → results/{exp}/{db}/{fold}/")
            run(gen_cmd(model, exp, db, samples_dir, suffix, n_runs, rag_over,
                        ollama_runner=ollama_runner), execute)
        # Registrar para post-procesado toda celda E1–E3 cuya carpeta exista
        # (recién generada O ya hecha), para que el re-post-procesado las cubra.
        if exp in ("E1", "E2", "E3") and (PROJECT_ROOT / "results" / exp / db / fold).exists():
            variants_e123.append((exp, fold))
    if skipped:
        print(f"[i ] {skipped} celdas ya hechas (omitidas; usa --no-skip para rehacer)")

    if postproc and variants_e123:
        print("\n[post] post-procesado mecánico de E1–E3")
        exps = sorted({e for e, _ in variants_e123})
        folds = sorted({f for _, f in variants_e123})
        run([PY, str(SCRIPTS / "postprocess_ttl.py"), "--batch",
             "--experiments", *exps, "--models", *folds], execute)

    if evaluate:
        print("\n[eval] evaluación de tres niveles sobre results/")
        run([PY, str(SCRIPTS / "evaluate_three_levels.py")], execute)


# ───────────────────────── selección lexicográfica ─────────────────────────
def cmd_select(args):
    import csv
    from collections import defaultdict
    from statistics import mean
    path = PROJECT_ROOT / "results" / "evaluation" / "threelevel_summary.csv"
    if not path.exists():
        sys.exit(f"No existe {path}. Ejecuta antes la evaluación de tres niveles.")
    rows = list(csv.DictReader(open(path)))

    def fnum(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    # Filtro opcional por modelo (p. ej. seleccionar sobre el modelo estable).
    model_filter = getattr(args, "model", None)
    if model_filter:
        rows = [r for r in rows if r.get("model") == model_filter]

    if args.__dict__["for"] == "phase1":
        keyf = lambda r: (r["sampling"], r["N"])
        title = "(tipo de muestreo, N)"
        # Solo celdas REALES de la rejilla: deben tener tipo Y tamaño.
        # Esto excluye carpetas legacy (muestreo antiguo sin N, barrido sin tipo).
        before = len(rows)
        rows = [r for r in rows if r.get("sampling") and r.get("N")]
        excluded = before - len(rows)
    else:
        keyf = lambda r: (r["rag_config"],)
        title = "(configuración RAG)"
        before = len(rows)
        # Solo E3 con una configuración RAG explícita (excluye legacy sin config).
        rows = [r for r in rows if r["experiment"] == "E3" and r.get("rag_config")]
        excluded = before - len(rows)

    if excluded:
        print(f"[i ] Excluidas {excluded} filas legacy (sin coordenadas completas de la fase).")

    groups = defaultdict(list)
    for r in rows:
        if not r.get("model"):
            continue
        groups[keyf(r)].append(r)

    ranked = []
    for key, items in groups.items():
        n_ok = sum(int(i["n_runs_OK"] or 0) for i in items)
        n_tot = sum(int(i["n_total"] or 0) for i in items)
        valid_rate = n_ok / n_tot if n_tot else 0
        oqg = [fnum(i["oquare_global"]) for i in items if fnum(i["oquare_global"]) is not None]
        can = [fnum(i["canonical_ratio"]) for i in items if fnum(i["canonical_ratio"]) is not None]
        cq = [fnum(i["cq_coverage"]) for i in items if fnum(i["cq_coverage"]) is not None]
        ranked.append({
            "key": key,
            "n_ok": n_ok, "n_total": n_tot,
            "valid_rate": round(valid_rate, 3),
            "oquare_global": round(mean(oqg), 3) if oqg else 0,
            "canonical_ratio": round(mean(can), 3) if can else 0,
            "cq_coverage": round(mean(cq), 3) if cq else 0,
        })
    # Regla lexicográfica: validez → OQuaRE → fidelidad → CQ
    ranked.sort(key=lambda d: (d["valid_rate"], d["oquare_global"],
                               d["canonical_ratio"], d["cq_coverage"]),
                reverse=True)
    print(f"\nRanking lexicográfico {title}  "
          f"[validez → OQuaRE → fidelidad → CQ]\n")
    print(f"  {'opción':<26} {'val/tot':>9} {'validez':>8} {'OQuaRE':>8} {'canon':>7} {'CQ':>6}")
    for d in ranked:
        k = " · ".join(d["key"])
        nn = f"{d['n_ok']}/{d['n_total']}"
        print(f"  {k:<26} {nn:>9} {d['valid_rate']:>8} {d['oquare_global']:>8} "
              f"{d['canonical_ratio']:>7} {d['cq_coverage']:>6}")
    if ranked:
        best = ranked[0]["key"]
        print(f"\n→ Mejor {title}: {' · '.join(best)}")


# ───────────────────────── CLI ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="phase", required=True)

    def common(p):
        p.add_argument("--grid-dir", type=Path, default=PROJECT_ROOT / "data" / "grid")
        p.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
        p.add_argument("--dbs", nargs="+", default=DEFAULT_DBS)
        p.add_argument("--n-runs", type=int, default=3)
        p.add_argument("--execute", action="store_true",
                       help="Ejecuta de verdad (por defecto solo imprime el plan)")
        p.add_argument("--no-skip", action="store_true",
                       help="No omitir celdas ya generadas")
        p.add_argument("--no-postproc", action="store_true")
        p.add_argument("--no-eval", action="store_true")
        p.add_argument("--ollama-e12-runner", choices=["gpt", "04"], default="gpt",
                       help="Runner para E1/E2 de modelos abiertos. 'gpt' (default): "
                            "run_gpt_experiments.py (coherente con E3, gestiona Ollama). "
                            "'04': 04_run_experiments.py.")

    p1 = sub.add_parser("phase1", help="Sensibilidad conjunta muestreo×tamaño")
    common(p1)
    p1.add_argument("--exps", nargs="+", default=["E1", "E2", "E3", "E4"])
    p1.add_argument("--samplings", nargs="+", default=DEFAULT_SAMPLINGS)
    p1.add_argument("--sizes", nargs="+", type=int, default=DEFAULT_SIZES)
    p1.add_argument("--keep-llama-e4", action="store_true",
                    help="No excluir Llama×E4 (por defecto se excluye: 0/12 válidas)")

    p2 = sub.add_parser("phase2", help="Calibración del RAG")
    common(p2)
    p2.add_argument("--sampling", required=True, help="Tipo de muestreo fijado en la Fase 1")
    p2.add_argument("--size", required=True, type=int, help="Tamaño N fijado en la Fase 1")

    p3 = sub.add_parser("phase3", help="Banco principal con parámetros congelados")
    common(p3)
    p3.add_argument("--sampling", required=True)
    p3.add_argument("--size", required=True, type=int)
    p3.add_argument("--rag-config", default="baseline", choices=list(RAG_CONFIGS))
    p3.add_argument("--exps", nargs="+", default=["E1", "E2", "E3", "E4"])

    ps = sub.add_parser("select", help="Selección lexicográfica desde la evaluación")
    ps.add_argument("--for", choices=["phase1", "phase2"], required=True)
    ps.add_argument("--model", default=None,
                    help="Filtrar por un modelo (p. ej. gpt-4o) para decidir sobre el "
                         "modelo estable en vez de agregar los tres.")

    args = ap.parse_args()

    if args.phase == "select":
        return cmd_select(args)

    exclude = set()
    if args.phase == "phase1" and not getattr(args, "keep_llama_e4", False):
        exclude = {("llama3.1:8b", "E4")}

    if args.phase == "phase1":
        jobs = collect_jobs(args.models, args.exps, args.dbs, args.samplings,
                            args.sizes, args.grid_dir, args.n_runs, exclude=exclude)
    elif args.phase == "phase2":
        jobs = collect_jobs(args.models, ["E3"], args.dbs, None, None,
                            args.grid_dir, args.n_runs,
                            fixed_sampling=args.sampling, fixed_size=args.size,
                            rag_configs=RAG_CONFIGS)
    else:  # phase3
        rag = {args.rag_config: RAG_CONFIGS[args.rag_config]}
        jobs = collect_jobs(args.models, args.exps, args.dbs, None, None,
                            args.grid_dir, args.n_runs,
                            fixed_sampling=args.sampling, fixed_size=args.size,
                            rag_configs=rag, exclude={("llama3.1:8b", "E4")})

    if not args.execute:
        print("[DRY-RUN] No se ejecuta nada. Añade --execute para lanzar.\n")
    execute_phase(jobs, args.n_runs, args.execute,
                  postproc=not args.no_postproc, evaluate=not args.no_eval,
                  skip_done=not args.no_skip,
                  ollama_runner=args.ollama_e12_runner)


if __name__ == "__main__":
    main()
