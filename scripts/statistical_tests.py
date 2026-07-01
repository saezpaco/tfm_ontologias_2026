"""Tests estadísticos formales para el TFM.

Implementa sin dependencias externas (numpy + pandas únicamente):
 1. Bootstrap pareado de la diferencia de medias con IC al 95 %.
 2. Wilcoxon signed-rank (aprox. normal) para pares (n>=6).
 3. McNemar para proporciones pareadas (parse_ok).
 4. Cohen's d (efecto pareado) y análisis de potencia minimal.
 5. Corrección Bonferroni-Holm para p-valores múltiples.

Uso:
    python scripts/statistical_tests.py
    → results/evaluation/statistical_tests.json
    → results/evaluation/statistical_tests.md
"""
from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/franciscosaez/Documents/Claude/Projects/TFM")
if not ROOT.exists():  # ejecución dentro del sandbox
    ROOT = Path("/sessions/nifty-beautiful-knuth/mnt/TFM")
RES = ROOT / "results"
EVAL = RES / "evaluation"
EVAL.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(42)
N_BOOT = 10_000
ALPHA = 0.05

# ---------- inferencia básica ----------
def paired_bootstrap_ci(diffs: np.ndarray, n_boot: int = N_BOOT,
                        alpha: float = ALPHA) -> dict:
    """Bootstrap percentile sobre la media de las diferencias pareadas."""
    diffs = np.asarray(diffs, dtype=float)
    n = len(diffs)
    if n == 0:
        return {"n": 0, "mean_diff": np.nan,
                "ci_low": np.nan, "ci_high": np.nan, "p_two_sided": np.nan}
    rng = np.random.default_rng(42)
    boot_means = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boot_means[i] = diffs[idx].mean()
    lo, hi = np.percentile(boot_means, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    # p-valor bilateral por inversión del intervalo
    n_neg = (boot_means <= 0).sum()
    n_pos = (boot_means >= 0).sum()
    p_two = 2 * min(n_neg, n_pos) / n_boot
    p_two = max(p_two, 1.0 / n_boot)  # piso numérico
    return {"n": int(n),
            "mean_diff": float(diffs.mean()),
            "sd_diff":   float(diffs.std(ddof=1)) if n > 1 else float("nan"),
            "ci_low":    float(lo),
            "ci_high":   float(hi),
            "p_two_sided": float(p_two)}


def wilcoxon_signed_rank(x: np.ndarray, y: np.ndarray) -> dict:
    """Wilcoxon signed-rank (aprox. normal) — pares con diferencias no nulas."""
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    d = x - y
    d = d[d != 0]
    n = len(d)
    if n < 6:
        return {"n_nonzero": int(n), "W": np.nan, "z": np.nan, "p": np.nan,
                "note": "n<6: muestra demasiado pequeña para aprox. normal"}
    abs_d = np.abs(d)
    ranks = pd.Series(abs_d).rank(method="average").values
    W_pos = float(ranks[d > 0].sum())
    W_neg = float(ranks[d < 0].sum())
    W = min(W_pos, W_neg)
    mu = n * (n + 1) / 4.0
    sigma = (n * (n + 1) * (2 * n + 1) / 24.0) ** 0.5
    if sigma == 0:
        return {"n_nonzero": int(n), "W": W, "z": np.nan, "p": np.nan,
                "note": "sigma=0"}
    z = (W - mu) / sigma
    # bilateral via normal aproximation
    from math import erf, sqrt
    cdf = 0.5 * (1 + erf(abs(z) / sqrt(2)))
    p = 2 * (1 - cdf)
    return {"n_nonzero": int(n), "W": float(W), "z": float(z),
            "p_two_sided": float(p), "W_pos": W_pos, "W_neg": W_neg}


def mcnemar_test(b: int, c: int) -> dict:
    """McNemar para discordantes (b, c)."""
    n_disc = b + c
    if n_disc == 0:
        return {"b": b, "c": c, "p": np.nan,
                "note": "no hay pares discordantes"}
    if n_disc < 25:
        # versión exacta binomial
        from math import comb
        k = min(b, c)
        p = sum(comb(n_disc, i) for i in range(k + 1)) * 2 ** (-n_disc) * 2
        p = min(1.0, p)
    else:
        # chi² con corrección de continuidad
        chi2 = (abs(b - c) - 1) ** 2 / (b + c)
        from math import erf, sqrt
        # 1 grado de libertad → χ² ≈ Z²
        p = 1 - (0.5 * (1 + erf((chi2 ** 0.5) / sqrt(2))) -
                 0.5 * (1 - erf((chi2 ** 0.5) / sqrt(2))))
        # mejor: integramos por 1-CDF chi2 con df=1
        # aproximación rápida
        from math import exp
        p = exp(-chi2 / 2)  # cola superior chi2(1) aprox
    return {"b": int(b), "c": int(c), "p_two_sided": float(p)}


def cohens_d_paired(diffs: np.ndarray) -> dict:
    diffs = np.asarray(diffs, dtype=float)
    if len(diffs) < 2:
        return {"d": np.nan}
    sd = diffs.std(ddof=1)
    return {"d": float(diffs.mean() / sd) if sd > 0 else np.nan,
            "interpretation": _interp_d(diffs.mean() / sd if sd > 0 else 0)}


def _interp_d(d: float) -> str:
    a = abs(d)
    if a < 0.2:    return "trivial"
    if a < 0.5:    return "pequeño"
    if a < 0.8:    return "mediano"
    return "grande"


def bonferroni_holm(p_values: list[float]) -> list[float]:
    """Corrección Bonferroni-Holm — devuelve p-valores ajustados."""
    p = np.asarray(p_values, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running_max = 0.0
    for rank, idx in enumerate(order):
        adj_p = p[idx] * (m - rank)
        adj_p = min(adj_p, 1.0)
        running_max = max(running_max, adj_p)
        adj[idx] = running_max
    return adj.tolist()


def detectable_effect(sd: float, n: int, power: float = 0.80,
                      alpha: float = 0.05) -> float:
    """Mínimo efecto Cohen's d detectable a potencia dada (aprox. normal)."""
    # z values for 1-sided
    from math import erf, sqrt
    def z(p):
        # aprox inversa de la normal estándar
        # Beasley-Springer-Moro
        a0 = -3.969683028665376e+01
        a1 =  2.209460984245205e+02
        a2 = -2.759285104469687e+02
        a3 =  1.383577518672690e+02
        a4 = -3.066479806614716e+01
        a5 =  2.506628277459239e+00
        b1 = -5.447609879822406e+01
        b2 =  1.615858368580409e+02
        b3 = -1.556989798598866e+02
        b4 =  6.680131188771972e+01
        b5 = -1.328068155288572e+01
        c1 = -7.784894002430293e-03
        c2 = -3.223964580411365e-01
        c3 = -2.400758277161838e+00
        c4 = -2.549732539343734e+00
        c5 =  4.374664141464968e+00
        c6 =  2.938163982698783e+00
        d1 =  7.784695709041462e-03
        d2 =  3.224671290700398e-01
        d3 =  2.445134137142996e+00
        d4 =  3.754408661907416e+00
        plow = 0.02425
        phigh = 1 - plow
        if p < plow:
            q = (-2 * np.log(p)) ** 0.5
            return ((((c1*q+c2)*q+c3)*q+c4)*q+c5)*q+c6 \
                   / ((((d1*q+d2)*q+d3)*q+d4)*q+1)
        elif p <= phigh:
            q = p - 0.5
            r = q*q
            return (((((a1*r+a2)*r+a3)*r+a4)*r+a5)*r+a6 if False else
                    (((((a1*r+a2)*r+a3)*r+a4)*r+a5)*r+a5)*q
                    if False else
                    ((((a1*r+a2)*r+a3)*r+a4)*r+a5)*q
                    / (((((b1*r+b2)*r+b3)*r+b4)*r+b5)*r+1))
        else:
            q = (-2 * np.log(1-p)) ** 0.5
            return -((((c1*q+c2)*q+c3)*q+c4)*q+c5)*q+c6 \
                   / ((((d1*q+d2)*q+d3)*q+d4)*q+1)
    # aproximación clásica simétrica:
    z_alpha = 1.96
    z_beta  = 0.8416 if power >= 0.80 else 0.5
    if power >= 0.90: z_beta = 1.2816
    return (z_alpha + z_beta) / (n ** 0.5)


# ---------- carga de datos ----------
def load_comparison():
    return pd.read_csv(RES / "comparison_E1-E4.csv")


def load_oquare():
    return pd.read_csv(EVAL / "oquare_metrics.csv")


# ---------- tests sobre comparison_E1-E4 (gpt-4o) ----------
def test_density_E4_vs_others(df: pd.DataFrame) -> dict:
    """Bootstrap pareado de n_triples: E4 vs E1/E2/E3 (postprocessed)."""
    out = {}
    df_pp = df[df["variant"] == "postprocessed"].copy()
    df_e4 = df[(df["experiment"] == "E4") & (df["variant"] == "raw")].copy()
    df_pp = pd.concat([df_pp, df_e4], ignore_index=True)
    df_pp = df_pp.dropna(subset=["n_triples"])
    df_pp["n_triples"] = pd.to_numeric(df_pp["n_triples"])
    for base in ("E1", "E2", "E3"):
        diffs = []
        keys = []
        for (db, run), g in df_pp.groupby(["db", "run"]):
            x = g[g["experiment"] == "E4"]["n_triples"].values
            y = g[g["experiment"] == base]["n_triples"].values
            if len(x) and len(y):
                diffs.append(x[0] - y[0])
                keys.append((db, run, x[0], y[0]))
        diffs = np.array(diffs)
        boot = paired_bootstrap_ci(diffs)
        wil  = wilcoxon_signed_rank(np.array([k[2] for k in keys]),
                                    np.array([k[3] for k in keys]))
        d    = cohens_d_paired(diffs)
        # ratio: para «E4 es X× más denso»
        ratios = [k[2] / k[3] if k[3] > 0 else np.nan for k in keys]
        ratios = np.array([r for r in ratios if not np.isnan(r)])
        out[f"E4_vs_{base}_n_triples"] = {
            "metric": "n_triples (postprocessed para E1-E3, raw para E4)",
            "n_pairs": len(diffs),
            "bootstrap": boot,
            "wilcoxon": wil,
            "cohens_d": d,
            "ratio_mean": float(ratios.mean()) if len(ratios) else float("nan"),
            "ratio_min":  float(ratios.min())  if len(ratios) else float("nan"),
            "ratio_max":  float(ratios.max())  if len(ratios) else float("nan"),
        }
    return out


def test_labels_E4(df: pd.DataFrame) -> dict:
    """Bootstrap pareado de n_labels: E4 vs E1/E2/E3."""
    out = {}
    df = df.copy()
    df["n_labels"] = pd.to_numeric(df["n_labels"], errors="coerce")
    df = df[df["n_labels"].notna()]
    for base in ("E1", "E2", "E3"):
        diffs = []
        for (db, run), g in df.groupby(["db", "run"]):
            x = g[(g["experiment"] == "E4") & (g["variant"] == "raw")]["n_labels"].values
            y = g[(g["experiment"] == base) & (g["variant"] == "postprocessed")]["n_labels"].values
            if len(x) and len(y):
                diffs.append(x[0] - y[0])
        diffs = np.array(diffs)
        out[f"E4_vs_{base}_n_labels"] = {
            "metric": "n_labels",
            "n_pairs": len(diffs),
            "bootstrap": paired_bootstrap_ci(diffs),
            "cohens_d": cohens_d_paired(diffs),
        }
    return out


def test_parse_ok_postproc(df: pd.DataFrame) -> dict:
    """McNemar pareado para parse_ok antes/después del post-procesado en E1-E3."""
    out = {}
    df = df.copy()
    df["parse_ok"] = pd.to_numeric(df["parse_ok"], errors="coerce")
    for exp in ("E1", "E2", "E3"):
        g_raw  = df[(df["experiment"] == exp) & (df["variant"] == "raw")]
        g_pp   = df[(df["experiment"] == exp) & (df["variant"] == "postprocessed")]
        merged = g_raw.merge(g_pp, on=["db", "run"], suffixes=("_raw", "_pp"))
        b = int(((merged["parse_ok_raw"] == 0) & (merged["parse_ok_pp"] == 1)).sum())
        c = int(((merged["parse_ok_raw"] == 1) & (merged["parse_ok_pp"] == 0)).sum())
        n_total = len(merged)
        recovered = int(((merged["parse_ok_raw"] == 0) & (merged["parse_ok_pp"] == 1)).sum())
        out[f"parse_ok_{exp}"] = {
            "n": n_total,
            "rate_raw":  float(merged["parse_ok_raw"].mean()),
            "rate_pp":   float(merged["parse_ok_pp"].mean()),
            "recovered_count": recovered,
            "regressed_count": c,
            "mcnemar":  mcnemar_test(b, c),
        }
    return out


# ---------- tests sobre oquare_metrics (Llama variantes) ----------
def test_calibration_llama(df: pd.DataFrame) -> dict:
    """Bootstrap pareado: cada variante vs ragapi (baseline) en OQuaRE Global."""
    out = {}
    df = df[df["load_ok"] == 1].copy()
    df["oquare_global"] = pd.to_numeric(df["oquare_global"])
    base = df[df["model"] == "llama3.1_8b_ragapi"]
    targets = ["llama3.1_8b_legacy", "llama3.1_8b_ragapi_C1",
               "llama3.1_8b_ragapi_C2", "llama3.1_8b_ragapi_C3"]
    for tgt in targets:
        df_t = df[df["model"] == tgt]
        diffs = []
        for (db, run), g_b in base.groupby(["db", "run"]):
            g_t = df_t[(df_t["db"] == db) & (df_t["run"] == run)]
            if len(g_t) and len(g_b):
                diffs.append(g_t["oquare_global"].values[0]
                             - g_b["oquare_global"].values[0])
        diffs = np.array(diffs)
        out[f"{tgt}_vs_ragapi"] = {
            "metric": "OQuaRE Global",
            "n_pairs": len(diffs),
            "bootstrap": paired_bootstrap_ci(diffs),
            "cohens_d": cohens_d_paired(diffs),
        }
    return out


def gpt_gap_close_llama(df: pd.DataFrame) -> dict:
    """Cierre del gap respecto a gpt-4o (4.20). Ejecución informativa, sin test.

    Si existe la variante ``llama3.1_8b_legacy`` en los datos, se usa como baseline
    para calcular qué porcentaje del gap cierra cada otra variante. Si no existe
    (caso del re-banco determinista en el que sólo se ejecutó annotationRAG), se
    cae al baseline ``llama3.1_8b_ragapi`` o, si tampoco está, se omite el
    cálculo del porcentaje.
    """
    df = df[df["load_ok"] == 1].copy()
    df["oquare_global"] = pd.to_numeric(df["oquare_global"])
    GPT_BASELINE = 4.20  # citado en el TFM
    means = (df.groupby("model")["oquare_global"]
               .agg(["mean", "std", "count"]).round(3))
    means["gap_to_gpt"] = (GPT_BASELINE - means["mean"]).round(3)

    # Detectar baseline disponible
    baseline_key = None
    pct_col = ""
    for candidate in ("llama3.1_8b_legacy",
                      "llama3.1_8b_ragapi",
                      "llama3.1_8b"):
        if candidate in means.index:
            baseline_key = candidate
            pct_col = f"pct_closed_vs_{candidate.replace('llama3.1_8b_', '')}"
            break

    means[pct_col or "pct_closed"] = ""
    if baseline_key is not None and pct_col:
        base_gap = GPT_BASELINE - means.loc[baseline_key, "mean"]
        if base_gap > 0:
            for m in means.index:
                gap = means.loc[m, "gap_to_gpt"]
                pct = 100 * (1 - gap / base_gap)
                means.loc[m, pct_col] = f"{pct:.1f}%"

    return {
        "summary_vs_gpt_4_20": means.reset_index().to_dict("records"),
        "baseline_used": baseline_key,
    }


# ---------- power analysis ----------
def power_summary(df: pd.DataFrame) -> dict:
    """SD observada y efecto detectable mínimo a potencia 80% (n=12)."""
    df = df[df["load_ok"] == 1].copy()
    df["oquare_global"] = pd.to_numeric(df["oquare_global"])
    sd = df["oquare_global"].std(ddof=1)
    out = {}
    for n in (3, 6, 12, 24):
        d_min = detectable_effect(sd, n, power=0.80)
        delta_min = d_min * sd
        out[f"n={n}"] = {
            "cohens_d_min": float(d_min),
            "delta_min_oquare": float(delta_min),
            "interpretation": _interp_d(d_min),
        }
    return {"sd_observed_oquare_global": float(sd),
            "power_table": out}


# ---------- markdown report ----------
def fmt_ci(b: dict, decimals: int = 3) -> str:
    if np.isnan(b.get("mean_diff", float("nan"))):
        return "—"
    return (f"{b['mean_diff']:+.{decimals}f} "
            f"[{b['ci_low']:+.{decimals}f}, {b['ci_high']:+.{decimals}f}]")


def fmt_p(p: float) -> str:
    if np.isnan(p): return "—"
    if p < 1e-3: return "p < 0.001"
    return f"p = {p:.3f}"


def render_markdown(results: dict) -> str:
    md = ["# Tests estadísticos — TFM", ""]
    md += [f"_Generado por `scripts/statistical_tests.py`. "
           f"N_BOOT = {N_BOOT}, α = {ALPHA}._", ""]

    # 1. n_triples E4 vs E1/E2/E3
    md += ["## 1. Densidad estructural — E4 vs E1/E2/E3 (n_triples)", ""]
    md += ["| Comparación | n pares | Diff media [IC95%] | Cohen's d | "
           "Wilcoxon p | Ratio E4/Base |",
           "|---|---|---|---|---|---|"]
    for k, v in results["density"].items():
        diff_ci = fmt_ci(v["bootstrap"], 1)
        d = v["cohens_d"]["d"]
        d_str = f"{d:.2f} ({v['cohens_d']['interpretation']})" if not np.isnan(d) else "—"
        wp = v["wilcoxon"].get("p_two_sided", float("nan"))
        ratio = (f"{v['ratio_mean']:.2f}× "
                 f"({v['ratio_min']:.2f}–{v['ratio_max']:.2f})"
                 if not np.isnan(v["ratio_mean"]) else "—")
        md.append(f"| {k} | {v['n_pairs']} | {diff_ci} | {d_str} | "
                  f"{fmt_p(wp)} | {ratio} |")
    md.append("")

    # 2. n_labels
    md += ["## 2. Riqueza documental — E4 vs E1/E2/E3 (n_labels)", ""]
    md += ["| Comparación | n pares | Diff media [IC95%] | Cohen's d |",
           "|---|---|---|---|"]
    for k, v in results["labels"].items():
        diff_ci = fmt_ci(v["bootstrap"], 1)
        d = v["cohens_d"]["d"]
        d_str = f"{d:.2f}" if not np.isnan(d) else "—"
        md.append(f"| {k} | {v['n_pairs']} | {diff_ci} | {d_str} |")
    md.append("")

    # 3. Post-procesado parse_ok
    md += ["## 3. Validez sintáctica antes/después del post-procesado (McNemar)", ""]
    md += ["| Experimento | n | parse_ok raw | parse_ok pp | "
           "Rescatadas | Regresadas | McNemar p |",
           "|---|---|---|---|---|---|---|"]
    for k, v in results["parse_ok"].items():
        md.append(f"| {k} | {v['n']} | {v['rate_raw']:.0%} | "
                  f"{v['rate_pp']:.0%} | {v['recovered_count']} | "
                  f"{v['regressed_count']} | "
                  f"{fmt_p(v['mcnemar'].get('p_two_sided', float('nan')))} |")
    md.append("")

    # 4. Calibración Llama
    md += ["## 4. Calibración del RAG en Llama 3.1 8B (vs ragapi baseline)", ""]
    md += ["| Variante | n pares | Δ OQuaRE [IC95%] | Cohen's d |",
           "|---|---|---|---|"]
    for k, v in results["calibration"].items():
        diff_ci = fmt_ci(v["bootstrap"], 3)
        d = v["cohens_d"]["d"]
        d_str = f"{d:+.2f} ({v['cohens_d']['interpretation']})" if not np.isnan(d) else "—"
        md.append(f"| {k} | {v['n_pairs']} | {diff_ci} | {d_str} |")
    md.append("")

    # 5. Gap to gpt-4o
    md += ["## 5. Gap respecto a gpt-4o (referencia 4.20 OQuaRE)", ""]
    md += ["| Variante | n_runs OK | Mean OQuaRE ± SD | "
           "Gap a gpt-4o | % gap cerrado vs legacy |",
           "|---|---|---|---|---|"]
    for r in results["gpt_gap"]["summary_vs_gpt_4_20"]:
        m = r["mean"]; s = r["std"]; g = r["gap_to_gpt"]
        md.append(f"| {r['model']} | {int(r['count'])} | "
                  f"{m:.2f} ± {s:.2f} | {g:+.2f} | "
                  f"{r.get('pct_closed_vs_legacy','')} |")
    md.append("")

    # 6. Power
    md += ["## 6. Análisis de potencia (OQuaRE Global)", ""]
    p = results["power"]
    md += [f"_SD muestral observada: {p['sd_observed_oquare_global']:.3f}._", ""]
    md += ["| n por celda | Δ OQuaRE detectable (potencia 80 %) | Cohen's d | "
           "Interpretación |",
           "|---|---|---|---|"]
    for n_key, vals in p["power_table"].items():
        md.append(f"| {n_key} | {vals['delta_min_oquare']:.3f} | "
                  f"{vals['cohens_d_min']:.3f} | {vals['interpretation']} |")
    md.append("")

    # 7. Bonferroni-Holm sobre los principales p
    md += ["## 7. Corrección Bonferroni-Holm de p-valores principales", ""]
    p_names = []
    p_vals = []
    for k, v in results["density"].items():
        p_names.append(f"density {k}")
        p_vals.append(v["wilcoxon"].get("p_two_sided", 1.0))
    for k, v in results["calibration"].items():
        p_names.append(f"calibration {k}")
        p_vals.append(v["bootstrap"].get("p_two_sided", 1.0))
    p_adj = bonferroni_holm(p_vals)
    md += ["| Test | p crudo | p ajustado (Holm) | Sig. (α=0.05) |",
           "|---|---|---|---|"]
    for name, pv, pa in zip(p_names, p_vals, p_adj):
        sig = "✓" if pa < 0.05 else "—"
        md.append(f"| {name} | {fmt_p(pv)} | {fmt_p(pa)} | {sig} |")
    md.append("")
    return "\n".join(md)


# ---------- main ----------
def main():
    df_cmp  = load_comparison()
    df_oqua = load_oquare()
    results = {}
    print("─── Tests sobre comparison_E1-E4.csv (gpt-4o) ───")
    results["density"]   = test_density_E4_vs_others(df_cmp)
    results["labels"]    = test_labels_E4(df_cmp)
    results["parse_ok"]  = test_parse_ok_postproc(df_cmp)
    print("─── Tests sobre oquare_metrics.csv (Llama variantes) ───")
    results["calibration"] = test_calibration_llama(df_oqua)
    results["gpt_gap"]     = gpt_gap_close_llama(df_oqua)
    results["power"]       = power_summary(df_oqua)

    # JSON
    out_json = EVAL / "statistical_tests.json"
    out_json.write_text(json.dumps(results, indent=2, default=str))
    # Markdown
    out_md = EVAL / "statistical_tests.md"
    out_md.write_text(render_markdown(results))

    print(f"[OK] {out_json}")
    print(f"[OK] {out_md}")
    return results


if __name__ == "__main__":
    res = main()
