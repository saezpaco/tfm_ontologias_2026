# Tests estadísticos — TFM

_Generado por `scripts/statistical_tests.py`. N_BOOT = 10000, α = 0.05._

## 1. Densidad estructural — E4 vs E1/E2/E3 (n_triples)

| Comparación | n pares | Diff media [IC95%] | Cohen's d | Wilcoxon p | Ratio E4/Base |
|---|---|---|---|---|---|
| E4_vs_E1_n_triples | 12 | +174.7 [+164.6, +186.7] | 8.48 (grande) | p = 0.002 | 4.51× (3.08–6.03) |
| E4_vs_E2_n_triples | 12 | +159.9 [+129.4, +183.8] | 3.23 (grande) | p = 0.002 | 3.91× (1.11–7.03) |
| E4_vs_E3_n_triples | 12 | +184.3 [+169.5, +201.8] | 6.15 (grande) | p = 0.002 | 6.31× (2.76–12.77) |

## 2. Riqueza documental — E4 vs E1/E2/E3 (n_labels)

| Comparación | n pares | Diff media [IC95%] | Cohen's d |
|---|---|---|---|
| E4_vs_E1_n_labels | 12 | +43.1 [+41.8, +44.1] | 20.43 |
| E4_vs_E2_n_labels | 12 | +42.4 [+41.3, +43.3] | 23.15 |
| E4_vs_E3_n_labels | 12 | +43.1 [+41.8, +44.1] | 20.43 |

## 3. Validez sintáctica antes/después del post-procesado (McNemar)

| Experimento | n | parse_ok raw | parse_ok pp | Rescatadas | Regresadas | McNemar p |
|---|---|---|---|---|---|---|
| parse_ok_E1 | 12 | 83% | 100% | 2 | 0 | p = 0.500 |
| parse_ok_E2 | 12 | 67% | 100% | 4 | 0 | p = 0.125 |
| parse_ok_E3 | 12 | 0% | 100% | 12 | 0 | p < 0.001 |

## 4. Calibración del RAG en Llama 3.1 8B (vs ragapi baseline)

| Variante | n pares | Δ OQuaRE [IC95%] | Cohen's d |
|---|---|---|---|
| llama3.1_8b_legacy_vs_ragapi | 6 | -0.233 [-0.457, +0.013] | -0.68 (mediano) |
| llama3.1_8b_ragapi_C1_vs_ragapi | 2 | +0.800 [+0.800, +0.800] | — |
| llama3.1_8b_ragapi_C2_vs_ragapi | 2 | +0.425 [+0.350, +0.500] | +4.01 (grande) |
| llama3.1_8b_ragapi_C3_vs_ragapi | 3 | +0.487 [+0.100, +0.800] | +1.37 (grande) |

## 5. Gap respecto a gpt-4o (referencia 4.20 OQuaRE)

| Variante | n_runs OK | Mean OQuaRE ± SD | Gap a gpt-4o | % gap cerrado vs legacy |
|---|---|---|---|---|
| llama3.1_8b_legacy | 12 | 3.45 ± 0.05 | +0.75 | 0.0% |
| llama3.1_8b_ragapi | 6 | 3.69 ± 0.31 | +0.51 | 31.3% |
| llama3.1_8b_ragapi_C1 | 6 | 4.08 ± 0.13 | +0.12 | 83.9% |
| llama3.1_8b_ragapi_C2 | 5 | 3.74 ± 0.80 | +0.46 | 38.4% |
| llama3.1_8b_ragapi_C3 | 7 | 3.49 ± 1.13 | +0.71 | 5.1% |

## 6. Análisis de potencia (OQuaRE Global)

_SD muestral observada: 0.602._

| n por celda | Δ OQuaRE detectable (potencia 80 %) | Cohen's d | Interpretación |
|---|---|---|---|
| n=3 | 0.974 | 1.618 | grande |
| n=6 | 0.689 | 1.144 | grande |
| n=12 | 0.487 | 0.809 | grande |
| n=24 | 0.344 | 0.572 | mediano |

## 7. Corrección Bonferroni-Holm de p-valores principales

| Test | p crudo | p ajustado (Holm) | Sig. (α=0.05) |
|---|---|---|---|
| density E4_vs_E1_n_triples | p = 0.002 | p = 0.009 | ✓ |
| density E4_vs_E2_n_triples | p = 0.002 | p = 0.009 | ✓ |
| density E4_vs_E3_n_triples | p = 0.002 | p = 0.009 | ✓ |
| calibration llama3.1_8b_legacy_vs_ragapi | p = 0.070 | p = 0.070 | — |
| calibration llama3.1_8b_ragapi_C1_vs_ragapi | p < 0.001 | p < 0.001 | ✓ |
| calibration llama3.1_8b_ragapi_C2_vs_ragapi | p < 0.001 | p < 0.001 | ✓ |
| calibration llama3.1_8b_ragapi_C3_vs_ragapi | p < 0.001 | p < 0.001 | ✓ |
