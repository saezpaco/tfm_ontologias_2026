#!/usr/bin/env python3
"""
generate_charts.py
──────────────────
Genera las gráficas comparativas E1–E4 a partir de
``results/comparison_E1-E4.csv``. Produce PNG + PDF en ``results/figures/``.

Figuras producidas:

  1. fig01_parse_ok.png        — barras agrupadas raw vs post-procesado por
                                  experimento (validez sintáctica).
  2. fig02_triples.png         — n_triples por (experimento, BBDD), variante
                                  post-procesado.
  3. fig03_labels.png          — n_labels por experimento (riqueza
                                  documental — donde E4 destaca).
  4. fig04_radar_richness.png  — radar multimétrica (clases, props, labels,
                                  triples, restrictions) normalizada por el
                                  máximo observado.

Uso
---

    python scripts/generate_charts.py
    python scripts/generate_charts.py --variant raw
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT_ROOT / "results"
FIG_DIR = RESULTS / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

EXPERIMENTS = ["E1", "E2", "E3", "E4"]
DATABASES = ["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"]

# Paleta de colores consistente (Tableau-like para impresión)
COLOR_EXP = {
    "E1": "#1F77B4",  # azul
    "E2": "#2CA02C",  # verde
    "E3": "#FF7F0E",  # naranja
    "E4": "#D62728",  # rojo
}
COLOR_RAW  = "#9DB7C9"
COLOR_POST = "#1F77B4"


def load_rows(csv_path: Path) -> list[dict]:
    rows: list[dict] = []
    with csv_path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in ("parse_ok", "n_triples", "n_classes", "n_object_props",
                      "n_datatype_props", "n_subclass_axioms",
                      "n_restrictions", "n_labels", "n_comments",
                      "size_bytes"):
                v = r.get(k, "")
                r[k] = float(v) if v not in ("", None) else None
            rows.append(r)
    return rows


def save(fig, name: str) -> None:
    for ext in ("png", "pdf"):
        out = FIG_DIR / f"{name}.{ext}"
        fig.savefig(str(out), bbox_inches="tight", dpi=200)
        print(f"  [OK] {out}")
    plt.close(fig)


# ─── Figura 1: parse_ok antes/después ──────────────────────────────────
def fig_parse_ok(rows: list[dict]) -> None:
    by_exp = defaultdict(lambda: {"raw": [], "postprocessed": []})
    for r in rows:
        v = r.get("variant", "raw")
        if v in ("raw", "postprocessed"):
            by_exp[r["experiment"]][v].append(r)

    # Para E4 NO hay variante "postprocessed" (no se procesó). Reutilizamos el
    # raw como su versión post (E4 es 12/12 nativamente).
    raw_ok  = []
    post_ok = []
    n_total = []
    for exp in EXPERIMENTS:
        ok_r  = sum(1 for r in by_exp[exp]["raw"] if r["parse_ok"])
        if exp == "E4":
            ok_p = ok_r
            n    = len(by_exp[exp]["raw"])
        else:
            ok_p = sum(1 for r in by_exp[exp]["postprocessed"] if r["parse_ok"])
            n    = len(by_exp[exp]["raw"])
        raw_ok.append(ok_r)
        post_ok.append(ok_p)
        n_total.append(n)

    x = np.arange(len(EXPERIMENTS))
    w = 0.36
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(x - w/2, raw_ok,  w, label="Output crudo (raw)",
           color=COLOR_RAW, edgecolor="white")
    ax.bar(x + w/2, post_ok, w, label="Tras post-procesado",
           color=COLOR_POST, edgecolor="white")
    for i, (r, p, t) in enumerate(zip(raw_ok, post_ok, n_total)):
        ax.text(i - w/2, r + 0.2, f"{r}/{t}", ha="center", fontsize=10)
        ax.text(i + w/2, p + 0.2, f"{p}/{t}", ha="center", fontsize=10,
                fontweight="bold" if p > r else "normal")

    ax.set_xticks(x)
    ax.set_xticklabels(EXPERIMENTS, fontsize=11)
    ax.set_ylim(0, max(n_total) + 2)
    ax.set_ylabel("Corridas con parse_ok = 1")
    ax.set_title("Validez sintáctica (rdflib): efecto del post-procesado",
                 fontsize=13, pad=12)
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    save(fig, "fig01_parse_ok")


# ─── Figura 2: n_triples por (Exp, DB) ────────────────────────────────
def fig_triples(rows: list[dict]) -> None:
    """Una barra por (Exp, DB). Para E1/E2/E3 usamos variante post-procesada;
    E4 usa raw (es su única variante)."""
    means: dict[tuple, float] = {}
    for exp in EXPERIMENTS:
        target = "raw" if exp == "E4" else "postprocessed"
        for db in DATABASES:
            vs = [r["n_triples"] for r in rows
                  if r["experiment"] == exp and r["db"] == db
                  and r.get("variant") == target
                  and r["parse_ok"] == 1
                  and r["n_triples"] is not None]
            means[(exp, db)] = sum(vs) / len(vs) if vs else 0.0

    x = np.arange(len(DATABASES))
    w = 0.20
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    for i, exp in enumerate(EXPERIMENTS):
        ys = [means[(exp, db)] for db in DATABASES]
        ax.bar(x + (i - 1.5) * w, ys, w, label=exp,
               color=COLOR_EXP[exp], edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(DATABASES, fontsize=10)
    ax.set_ylabel("Media de triples por ontología")
    ax.set_title("Riqueza estructural (n_triples) por experimento y base de datos",
                 fontsize=13, pad=12)
    ax.legend(title="Experimento", loc="upper right", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    save(fig, "fig02_triples")


# ─── Figura 3: n_labels por experimento ───────────────────────────────
def fig_labels(rows: list[dict]) -> None:
    by_exp: dict[str, list[float]] = defaultdict(list)
    for exp in EXPERIMENTS:
        target = "raw" if exp == "E4" else "postprocessed"
        for r in rows:
            if (r["experiment"] == exp and r.get("variant") == target
                    and r["parse_ok"] == 1 and r["n_labels"] is not None):
                by_exp[exp].append(r["n_labels"])

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bp = ax.boxplot([by_exp[e] for e in EXPERIMENTS],
                    labels=EXPERIMENTS, patch_artist=True, widths=0.55,
                    medianprops=dict(color="black", linewidth=1.2))
    for patch, exp in zip(bp["boxes"], EXPERIMENTS):
        patch.set_facecolor(COLOR_EXP[exp]); patch.set_alpha(0.85)
    means = [np.mean(by_exp[e]) if by_exp[e] else 0 for e in EXPERIMENTS]
    for i, m in enumerate(means, 1):
        ax.text(i, m + 1, f"x̄={m:.1f}", ha="center", fontsize=9)
    ax.set_ylabel("rdfs:label declarados")
    ax.set_title("Riqueza documental: distribución de rdfs:label",
                 fontsize=13, pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    save(fig, "fig03_labels")


# ─── Figura 4: radar multimétrica ─────────────────────────────────────
def fig_radar(rows: list[dict]) -> None:
    metrics = ["n_classes", "n_object_props", "n_datatype_props",
               "n_subclass_axioms", "n_labels"]
    metric_labels = ["Clases", "ObjectProps", "DatatypeProps",
                     "subClassOf", "Labels"]
    means: dict[str, dict[str, float]] = {}
    for exp in EXPERIMENTS:
        target = "raw" if exp == "E4" else "postprocessed"
        means[exp] = {}
        for k in metrics:
            vs = [r[k] for r in rows
                  if r["experiment"] == exp and r.get("variant") == target
                  and r["parse_ok"] == 1 and r[k] is not None]
            means[exp][k] = sum(vs) / len(vs) if vs else 0.0
    # Normalización por máximo de cada métrica
    maxes = {k: max(means[e][k] for e in EXPERIMENTS) or 1 for k in metrics}

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7.5, 7.5),
                           subplot_kw=dict(projection="polar"))
    for exp in EXPERIMENTS:
        vals = [means[exp][k] / maxes[k] for k in metrics]
        vals += vals[:1]
        ax.plot(angles, vals, color=COLOR_EXP[exp], linewidth=2, label=exp)
        ax.fill(angles, vals, color=COLOR_EXP[exp], alpha=0.12)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metric_labels, fontsize=11)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25 %", "50 %", "75 %", "100 %"], fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_title("Riqueza multimétrica relativa al máximo observado",
                 fontsize=12, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.05))
    save(fig, "fig04_radar_richness")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path,
                    default=RESULTS / "comparison_E1-E4.csv",
                    help="CSV de entrada (default: comparison_E1-E4.csv)")
    args = ap.parse_args()
    if not args.csv.exists():
        raise SystemExit(f"[ERROR] {args.csv} no existe. Ejecuta primero "
                         "evaluate_E4_vs_E1-E3.py")
    rows = load_rows(args.csv)
    print(f"[OK] {len(rows)} filas leídas de {args.csv}")
    print(f"[OK] figuras → {FIG_DIR}\n")
    fig_parse_ok(rows)
    fig_triples(rows)
    fig_labels(rows)
    fig_radar(rows)
    print("\n[DONE] 4 figuras generadas (PNG + PDF)")


if __name__ == "__main__":
    main()
