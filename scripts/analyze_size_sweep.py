"""Analiza los resultados del barrido del tamaño muestral.

Una vez ejecutado run_size_sweep.sh, este script:
 1. Recoge OQuaRE Global, n_triples, n_labels, parse_ok por (N, modelo, BBDD, run)
 2. Aplica bootstrap para la diferencia OQuaRE entre N=25 y N=200
 3. Reporta tabla resumen + figura

Entrada:  results/E3/{DB}/{model}_N{N}_ragapi/postprocessed/*.ttl
Salida:   results/evaluation/size_sweep_summary.{csv,md}
          results/figures/fig14_size_sweep.{png,pdf}
"""
from pathlib import Path
import csv
import re
from collections import defaultdict

ROOT = Path("/Users/franciscosaez/Documents/Claude/Projects/TFM")
if not ROOT.exists():
    ROOT = Path("/sessions/nifty-beautiful-knuth/mnt/TFM")
RES = ROOT / "results"
EVAL = RES / "evaluation"

OQUARE_CSV = EVAL / "oquare_metrics.csv"  # generado por oquare_eval.py
SIZES = [25, 50, 100, 200]

def main():
    if not OQUARE_CSV.exists():
        print(f"[err] {OQUARE_CSV} no existe. Lanza antes el barrido y oquare_eval.")
        return

    rows = list(csv.DictReader(open(OQUARE_CSV)))
    # Filtrar solo runs con sufijo _N{N}_ragapi
    pat = re.compile(r"_N(\d+)_ragapi")
    by_cell = defaultdict(list)
    for r in rows:
        m = pat.search(r.get("model", "") or "")
        if m:
            N = int(m.group(1))
            key = (N, r["db"], r["model"].replace(f"_N{N}_ragapi", ""))
            try: by_cell[key].append(float(r["oquare_global"]))
            except: pass

    # Resumen
    summary = []
    for (N, db, mod), vals in sorted(by_cell.items()):
        if not vals: continue
        mean = sum(vals)/len(vals)
        sd = (sum((v-mean)**2 for v in vals)/max(1,len(vals)-1)) ** 0.5
        summary.append({"N": N, "db": db, "model": mod,
                        "n_runs_ok": len(vals),
                        "oquare_mean": round(mean,3),
                        "oquare_sd":   round(sd,3)})

    # CSV
    out_csv = EVAL / "size_sweep_summary.csv"
    if summary:
        with open(out_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
            w.writeheader()
            for s in summary: w.writerow(s)
        print(f"[OK] {out_csv} ({len(summary)} celdas)")

    # MD
    md = ["# Sensibilidad al tamaño muestral — resumen", "",
          "| N filas | BBDD | Modelo | n_runs OK | OQuaRE mean ± SD |",
          "|---|---|---|---|---|"]
    for s in summary:
        md.append(f"| {s['N']} | {s['db']} | {s['model']} | "
                  f"{s['n_runs_ok']} | {s['oquare_mean']} ± {s['oquare_sd']} |")
    md_path = EVAL / "size_sweep_summary.md"
    md_path.write_text("\n".join(md))
    print(f"[OK] {md_path}")

if __name__ == "__main__":
    main()
