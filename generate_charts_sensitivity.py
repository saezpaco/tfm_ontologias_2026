#!/usr/bin/env python3
"""
generate_charts_sensitivity.py
──────────────────────────────
Genera la figura del análisis de sensibilidad al muestreo a partir de
los OQuaRE scores de las corridas con sufijo de estrategia
(_A_head, _B_random, _C_stratified, _D_diversity).

Salida:
    results/figures/fig09_sensitivity.png
    results/figures/fig09_sensitivity.pdf
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT_ROOT / "results"
FIG_DIR = RESULTS / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

STRATEGIES = ["A_head", "B_random", "C_stratified", "D_diversity"]
STRATEGY_LABEL = {
    "A_head":       "A · head",
    "B_random":     "B · random",
    "C_stratified": "C · stratified",
    "D_diversity":  "D · diversity",
}
COLOR_STRATEGY = {
    "A_head":       "#9DB7C9",   # gris-azul (la del TFM)
    "B_random":     "#1F77B4",   # azul
    "C_stratified": "#2CA02C",   # verde
    "D_diversity":  "#FF7F0E",   # naranja
}


def parse_model_strategy(model_str: str) -> tuple[str, str | None]:
    """De 'gpt-4o_A_head' devuelve ('gpt-4o', 'A_head')."""
    for s in STRATEGIES:
        suffix = "_" + s
        if model_str.endswith(suffix):
            return model_str[: -len(suffix)], s
    return model_str, None


def load_summary(csv_path: Path) -> dict:
    """Lee oquare_metrics.csv y agrupa por (model_base, exp, strategy)."""
    bucket: dict[tuple, list[float]] = defaultdict(list)
    with csv_path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("load_ok") != "1":
                continue
            model_base, strat = parse_model_strategy(r.get("model", ""))
            if strat is None:
                continue   # no es del análisis de sensibilidad
            try:
                score = float(r.get("oquare_global") or 0)
            except (TypeError, ValueError):
                continue
            bucket[(model_base, r.get("experiment"), strat)].append(score)
    return bucket


def fig_sensitivity(bucket: dict) -> None:
    # Filas: (modelo, experimento). Columnas: estrategia.
    keys = sorted({(m, e) for (m, e, _) in bucket.keys()})
    if not keys:
        print("[WARN] No hay datos de sensibilidad. ¿Has corrido el análisis?")
        return

    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    n_groups = len(keys)
    n_strats = len(STRATEGIES)
    w = 0.20
    x = np.arange(n_groups)

    for i, strat in enumerate(STRATEGIES):
        ys, labels = [], []
        for k in keys:
            scores = bucket.get((k[0], k[1], strat), [])
            if scores:
                mean = sum(scores) / len(scores)
                ys.append(mean)
                labels.append(f"{mean:.2f}")
            else:
                ys.append(0)
                labels.append("—")
        bars = ax.bar(x + (i - (n_strats - 1) / 2) * w, ys, w,
                      label=STRATEGY_LABEL[strat],
                      color=COLOR_STRATEGY[strat], edgecolor="white")
        for b, lab, val in zip(bars, labels, ys):
            if val > 0:
                ax.text(b.get_x() + b.get_width() / 2, val + 0.05,
                        lab, ha="center", fontsize=8)

    xt = [f"{m}\n{e}" for (m, e) in keys]
    ax.set_xticks(x); ax.set_xticklabels(xt, fontsize=9)
    ax.set_ylim(0, 5.4)
    ax.set_ylabel("OQuaRE Global (escala 1-5)")
    ax.set_title("Análisis de sensibilidad al muestreo — OQuaRE Global "
                 "por estrategia",
                 fontsize=13, pad=12)
    ax.axhline(3.0, color="gray", linestyle=":", alpha=0.5)
    ax.text(n_groups - 0.5, 3.05, "umbral 'aceptable' (3.0)",
            fontsize=8, color="gray", ha="right", va="bottom")
    ax.legend(title="Estrategia de muestreo", loc="upper right",
              framealpha=0.95, ncol=2)
    ax.grid(axis="y", linestyle="--", alpha=0.4); ax.set_axisbelow(True)

    for ext in ("png", "pdf"):
        out = FIG_DIR / f"fig09_sensitivity.{ext}"
        fig.savefig(str(out), bbox_inches="tight", dpi=200)
        print(f"  [OK] {out}")
    plt.close(fig)


def main() -> None:
    csv_path = RESULTS / "evaluation" / "oquare_metrics.csv"
    if not csv_path.exists():
        raise SystemExit(f"[ERROR] {csv_path} no existe.")
    bucket = load_summary(csv_path)
    print(f"[OK] {len(bucket)} celdas (modelo, experimento, estrategia)")
    fig_sensitivity(bucket)


if __name__ == "__main__":
    main()
