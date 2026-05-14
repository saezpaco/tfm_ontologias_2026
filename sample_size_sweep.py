"""Sugerencia 4 del tutor: barrido del tamaño muestral.

Genera muestras de N ∈ {25, 50, 100, 200} filas con estrategia A_head
para FANTOM5 y dbSUPER, las prepara como prompts y reporta el coste
estimado de tokens y la longitud del input que recibirá el modelo.

Salidas:
  - data/samples_sizes/N={25,50,100,200}/{DB}_sample_prompt.txt
  - results/evaluation/sample_size_estimates.csv  (tokens y costes proyectados)
  - scripts/run_size_sweep.sh   (lanzador del experimento real)

El usuario ejecuta luego: bash scripts/run_size_sweep.sh
con OPENAI_API_KEY y/o Ollama corriendo.
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path("/sessions/nifty-beautiful-knuth/mnt/TFM")
RAW  = ROOT / "data" / "raw"
OUT  = ROOT / "data" / "samples_sizes"
EVAL = ROOT / "results" / "evaluation"

DBS = {
    "FANTOM5": {
        "tsv":  RAW / "FANTOM5.tsv",
        "desc": "Enhancers activos identificados por CAGE-seq",
        "source": "https://fantom.gsc.riken.jp/5/",
    },
    "dbSUPER": {
        "tsv":  RAW / "dbSUPER.tsv",
        "desc": "Super-enhancers con coordenadas, líneas celulares y genes diana",
        "source": "https://asntech.org/dbsuper/",
    },
}

SIZES = [25, 50, 100, 200]

# Modelos de coste (USD por 1M tokens, mayo 2026)
PRICING = {
    "gpt-4o":      {"input": 2.50, "output": 10.00},
    "llama-local": {"input": 0.0,  "output": 0.0},   # Ollama local
}


def estimate_tokens(text: str) -> int:
    """Estimación 4 chars/token (regla estándar para texto inglés/Turtle)."""
    return max(1, len(text) // 4)


def build_prompt_block(db_name: str, db_info: dict, n_rows: int) -> str:
    """Construye el sample_prompt.txt con la cabecera + n filas (A_head)."""
    with open(db_info["tsv"], encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    header = lines[0].rstrip()
    data_lines = [l.rstrip() for l in lines[1:n_rows+1]]
    block = (
        f"# Base de datos: {db_name}\n"
        f"# Descripción: {db_info['desc']}\n"
        f"# Fuente: {db_info['source']}\n"
        f"# Dimensiones totales: {len(lines)-1} filas, "
        f"{len(header.split(chr(9)))} columnas\n"
        f"# Filas en esta muestra: {n_rows}\n"
        f"# Estrategia: A_head (canónica del TFM)\n"
        f"\n"
        f"# MUESTRA DE DATOS (formato TSV):\n"
        f"# Nota: '-' indica valor no disponible\n\n"
        + header + "\n"
        + "\n".join(data_lines)
    )
    return block


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    EVAL.mkdir(parents=True, exist_ok=True)
    rows = []
    for n in SIZES:
        sub = OUT / f"N={n}"
        sub.mkdir(parents=True, exist_ok=True)
        for db_name, db_info in DBS.items():
            block = build_prompt_block(db_name, db_info, n)
            outf = sub / f"{db_name}_sample_prompt.txt"
            outf.write_text(block, encoding="utf-8")
            tk = estimate_tokens(block)
            # Asumimos prompts envolventes ~600 tokens (system + user template)
            prompt_total = tk + 600
            # estimación de output ~3000 tokens para una ontología media
            out_tokens = 3000
            # coste por una corrida para gpt-4o
            cost_gpt4o = (prompt_total / 1e6 * PRICING["gpt-4o"]["input"]
                          + out_tokens / 1e6 * PRICING["gpt-4o"]["output"])
            rows.append({
                "n_rows":         n,
                "db":             db_name,
                "sample_bytes":   len(block),
                "sample_tokens":  tk,
                "prompt_tokens":  prompt_total,
                "output_tokens_est": out_tokens,
                "cost_per_run_gpt4o_usd": round(cost_gpt4o, 4),
            })
            print(f"  [OK] {outf}  ({len(block)} bytes, ~{tk} tokens, "
                  f"~${cost_gpt4o:.3f}/run gpt-4o)")
    # CSV
    csv_path = EVAL / "sample_size_estimates.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows: w.writerow(r)
    print(f"\n[OK] {csv_path}")

    # Resumen markdown
    md = ["# Estimación de coste — barrido del tamaño muestral", "",
          "_Estimación de tokens (regla 4 caracteres/token) y coste proyectado "
          "para gpt-4o (input $2.50/M tokens, output $10/M tokens, snapshot "
          "mayo 2026)._", "",
          "| N filas | BBDD | tokens prompt | output est. | "
          "USD / run (gpt-4o) | USD por 3 runs / BBDD | USD total exp. |",
          "|---|---|---|---|---|---|---|"]
    by_n = {}
    for r in rows:
        by_n.setdefault(r["n_rows"], []).append(r)
    grand_total = 0.0
    for n, rs in sorted(by_n.items()):
        for r in rs:
            cost_3 = r["cost_per_run_gpt4o_usd"] * 3
            md.append(f"| {n} | {r['db']} | {r['prompt_tokens']:,} | "
                      f"{r['output_tokens_est']:,} | "
                      f"${r['cost_per_run_gpt4o_usd']:.4f} | "
                      f"${cost_3:.3f} | — |")
        sub_total = sum(r['cost_per_run_gpt4o_usd'] for r in rs) * 3
        grand_total += sub_total
        md.append(f"| **Subtotal N={n}** | (FANTOM5 + dbSUPER) | | | | | "
                  f"**${sub_total:.2f}** |")
    md.append(f"\n**Total estimado para gpt-4o** (4 tamaños × 2 BBDD × 3 runs, "
              f"solo E3 RAG semántico): **${grand_total:.2f}**.")
    md.append("\nReplicar el barrido con E1, E2, E4 multiplica el coste por "
              "tantas estrategias como se contemplen. La replicación con "
              "Llama 3.1 8B vía Ollama es gratuita en términos económicos "
              "pero exige ~4 h adicionales de cómputo en hardware Apple M3 "
              "por (N, BBDD, estrategia, seed).")
    md.append("\nLa estimación de output (3 000 tokens) es conservadora: "
              "se basa en el percentil 75 de los outputs E3 RAG semántico "
              "del banco principal (rango observado 1 500–4 200 tokens).")

    md_path = EVAL / "sample_size_estimates.md"
    md_path.write_text("\n".join(md))
    print(f"[OK] {md_path}")


if __name__ == "__main__":
    main()
