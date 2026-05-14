# Estimación de coste — barrido del tamaño muestral

_Estimación de tokens (regla 4 caracteres/token) y coste proyectado para gpt-4o (input $2.50/M tokens, output $10/M tokens, snapshot mayo 2026)._

| N filas | BBDD | tokens prompt | output est. | USD / run (gpt-4o) | USD por 3 runs / BBDD | USD total exp. |
|---|---|---|---|---|---|---|
| 25 | FANTOM5 | 1,191 | 3,000 | $0.0330 | $0.099 | — |
| 25 | dbSUPER | 1,055 | 3,000 | $0.0326 | $0.098 | — |
| **Subtotal N=25** | (FANTOM5 + dbSUPER) | | | | | **$0.20** |
| 50 | FANTOM5 | 1,704 | 3,000 | $0.0343 | $0.103 | — |
| 50 | dbSUPER | 1,411 | 3,000 | $0.0335 | $0.101 | — |
| **Subtotal N=50** | (FANTOM5 + dbSUPER) | | | | | **$0.20** |
| 100 | FANTOM5 | 2,735 | 3,000 | $0.0368 | $0.110 | — |
| 100 | dbSUPER | 2,132 | 3,000 | $0.0353 | $0.106 | — |
| **Subtotal N=100** | (FANTOM5 + dbSUPER) | | | | | **$0.22** |
| 200 | FANTOM5 | 4,774 | 3,000 | $0.0419 | $0.126 | — |
| 200 | dbSUPER | 3,594 | 3,000 | $0.0390 | $0.117 | — |
| **Subtotal N=200** | (FANTOM5 + dbSUPER) | | | | | **$0.24** |

**Total estimado para gpt-4o** (4 tamaños × 2 BBDD × 3 runs, solo E3 RAG semántico): **$0.86**.

Replicar el barrido con E1, E2, E4 multiplica el coste por tantas estrategias como se contemplen. La replicación con Llama 3.1 8B vía Ollama es gratuita en términos económicos pero exige ~4 h adicionales de cómputo en hardware Apple M3 por (N, BBDD, estrategia, seed).

La estimación de output (3 000 tokens) es conservadora: se basa en el percentil 75 de los outputs E3 RAG semántico del banco principal (rango observado 1 500–4 200 tokens).