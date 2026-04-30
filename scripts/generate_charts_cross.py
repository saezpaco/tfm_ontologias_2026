#!/usr/bin/env python3
"""
generate_charts_cross.py
────────────────────────
Gráficas cross-model + OQuaRE a partir de
``results/evaluation/oquare_metrics.csv``.

Figuras:
  · fig05_oquare_global.png       — barras agrupadas oquare_global por
                                     (experimento, modelo).
  · fig06_oquare_radar_models.png — radar de las 5 sub-características
                                     OQuaRE por modelo (promedio E1-E3).
  · fig07_load_success.png        — % de ontologías que cargan OK
                                     (load_ok) por (Exp, modelo) tras
                                     post-procesado y saneo.
  · fig08_hallucinations.png      — alucinaciones tipadas
                                     (n_literals_sanitized) por
                                     (Exp, modelo).
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

EXPERIMENTS = ["E1", "E2", "E3", "E4"]
MODELS_ORDER = ["gpt-4o", "llama3.1_8b", "qwen2.5-coder_7b"]
COLOR_MODEL = {
    "gpt-4o":            "#1F77B4",   # azul Tableau
    "llama3.1_8b":       "#FF7F0E",   # naranja Tableau
    "qwen2.5-coder_7b":  "#2CA02C",   # verde Tableau
}
COLOR_EXP = {
    "E1": "#2CA02C", "E2": "#9467BD", "E3": "#E377C2", "E4": "#D62728",
}


def load_rows() -> list[dict]:
    rows: list[dict] = []
    with (RESULTS / "evaluation" / "oquare_metrics.csv").open(
            encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in ("oquare_global", "score_structural", "score_modularity",
                      "score_reusability", "score_operability",
                      "score_reliability", "n_literals_sanitized",
                      "n_classes", "n_obj_props", "n_data_props",
                      "n_annotations", "load_ok"):
                v = r.get(k, "")
                try:
                    r[k] = float(v) if v not in ("", None) else None
                except ValueError:
                    r[k] = None
            rows.append(r)
    return rows


def save(fig, name: str) -> None:
    for ext in ("png", "pdf"):
        out = FIG_DIR / f"{name}.{ext}"
        fig.savefig(str(out), bbox_inches="tight", dpi=200)
        print(f"  [OK] {out}")
    plt.close(fig)


def fig_oquare_global(rows: list[dict]) -> None:
    bucket: dict[tuple, list[float]] = defaultdict(list)
    for r in rows:
        if r.get("load_ok") and r.get("oquare_global") is not None:
            bucket[(r["experiment"], r["model"])].append(r["oquare_global"])
    means = {k: sum(v)/len(v) for k, v in bucket.items() if v}

    x = np.arange(len(EXPERIMENTS)); w = 0.27
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    for i, m in enumerate(MODELS_ORDER):
        ys = [means.get((e, m), 0) for e in EXPERIMENTS]
        bars = ax.bar(x + (i - (len(MODELS_ORDER)-1)/2) * w, ys, w, label=m,
                      color=COLOR_MODEL[m], edgecolor="white")
        for j, (b, y) in enumerate(zip(bars, ys)):
            if y > 0:
                ax.text(b.get_x() + b.get_width()/2, y + 0.05,
                        f"{y:.2f}", ha="center", fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(EXPERIMENTS)
    ax.set_ylim(0, 5.5)
    ax.set_ylabel("OQuaRE Global (escala 1-5)")
    ax.set_title("OQuaRE Global por experimento y modelo",
                 fontsize=13, pad=12)
    ax.axhline(3.0, color="gray", linestyle=":", alpha=0.5)
    ax.text(len(EXPERIMENTS)-0.5, 3.05, "umbral 'aceptable' (3.0)",
            fontsize=8, color="gray", ha="right", va="bottom")
    ax.legend(title="Modelo", loc="upper right", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.4); ax.set_axisbelow(True)
    save(fig, "fig05_oquare_global")


def fig_oquare_radar(rows: list[dict]) -> None:
    metrics = ["score_structural", "score_modularity", "score_reusability",
               "score_operability", "score_reliability"]
    labels  = ["Structural", "Modularity", "Reusability",
               "Operability", "Reliability"]
    by_model: dict[str, dict[str, list[float]]] = {
        m: {k: [] for k in metrics} for m in MODELS_ORDER}
    for r in rows:
        if not r.get("load_ok"):
            continue
        m = r.get("model")
        if m not in by_model:
            continue
        for k in metrics:
            v = r.get(k)
            if v is not None:
                by_model[m][k].append(v)

    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7.5, 7.5),
                           subplot_kw=dict(projection="polar"))
    for m in MODELS_ORDER:
        vals = [(sum(by_model[m][k])/len(by_model[m][k])
                 if by_model[m][k] else 0) / 5.0
                for k in metrics]
        vals += vals[:1]
        ax.plot(angles, vals, color=COLOR_MODEL[m], linewidth=2.2,
                label=m, marker='o')
        ax.fill(angles, vals, color=COLOR_MODEL[m], alpha=0.15)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels, fontsize=11)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_title("Sub-características OQuaRE — promedio por modelo "
                 "(E1-E3 + E4 si aplica)", fontsize=12, pad=22)
    ax.legend(loc="upper right", bbox_to_anchor=(1.30, 1.05))
    save(fig, "fig06_oquare_radar_models")


def fig_load_success(rows: list[dict]) -> None:
    by_em_total = defaultdict(int); by_em_ok = defaultdict(int)
    for r in rows:
        key = (r["experiment"], r["model"])
        by_em_total[key] += 1
        if r.get("load_ok"):
            by_em_ok[key] += 1

    x = np.arange(len(EXPERIMENTS)); w = 0.27
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    for i, m in enumerate(MODELS_ORDER):
        ratios, labels = [], []
        for e in EXPERIMENTS:
            t = by_em_total[(e, m)]; ok = by_em_ok[(e, m)]
            ratios.append((ok / t * 100) if t else 0)
            labels.append(f"{ok}/{t}" if t else "—")
        bars = ax.bar(x + (i - (len(MODELS_ORDER)-1)/2) * w, ratios, w,
                      label=m,
                      color=COLOR_MODEL[m], edgecolor="white")
        for b, lab in zip(bars, labels):
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5,
                    lab, ha="center", fontsize=9,
                    fontweight="bold" if lab.endswith("/12") else "normal")
    ax.set_xticks(x); ax.set_xticklabels(EXPERIMENTS)
    ax.set_ylim(0, 115)
    ax.set_ylabel("% de ontologías que cargan en owlready2 (load_ok)")
    ax.set_title("Validez en owlready2 (post-procesado + saneo de literales)",
                 fontsize=13, pad=12)
    ax.legend(title="Modelo", loc="lower right", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.4); ax.set_axisbelow(True)
    save(fig, "fig07_load_success")


def fig_hallucinations(rows: list[dict]) -> None:
    bucket = defaultdict(int)
    for r in rows:
        n = r.get("n_literals_sanitized") or 0
        bucket[(r["experiment"], r["model"])] += int(n)

    x = np.arange(len(EXPERIMENTS)); w = 0.27
    fig, ax = plt.subplots(figsize=(9.0, 4.5))
    for i, m in enumerate(MODELS_ORDER):
        ys = [bucket.get((e, m), 0) for e in EXPERIMENTS]
        bars = ax.bar(x + (i - (len(MODELS_ORDER)-1)/2) * w, ys, w, label=m,
                      color=COLOR_MODEL[m], edgecolor="white")
        for b, y in zip(bars, ys):
            if y > 0:
                ax.text(b.get_x() + b.get_width()/2, y + 0.4,
                        str(y), ha="center", fontsize=10,
                        fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(EXPERIMENTS)
    ax.set_ylabel("Literales con tipo numérico espurio "
                  "(saneados a xsd:string)")
    ax.set_title("Alucinaciones tipadas por modelo y experimento",
                 fontsize=13, pad=12)
    ax.legend(title="Modelo", loc="upper left", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.4); ax.set_axisbelow(True)
    save(fig, "fig08_hallucinations")


def main() -> None:
    rows = load_rows()
    print(f"[OK] {len(rows)} filas leídas")
    fig_oquare_global(rows)
    fig_oquare_radar(rows)
    fig_load_success(rows)
    fig_hallucinations(rows)
    print("\n[DONE] 4 figuras nuevas en results/figures/")


if __name__ == "__main__":
    main()
