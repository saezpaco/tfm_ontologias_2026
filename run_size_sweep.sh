#!/usr/bin/env bash
# run_size_sweep.sh — barrido del tamaño muestral (sugerencia 4 del tutor).
#
# Ejecuta el experimento E3 (RAG semántico) sobre FANTOM5 y dbSUPER con
# tamaños muestrales N ∈ {25, 50, 100, 200} y 3 corridas por celda.
# Total: 4 tamaños × 2 BBDD × 3 runs = 24 corridas. Coste estimado para
# gpt-4o: ≈ $0.85 USD. Coste para Llama 3.1 8B vía Ollama: $0 (cómputo
# local, ~4 h por modelo en Apple M3).
#
# Requisitos:
#   - OPENAI_API_KEY exportada en el entorno (si se ejecuta gpt-4o)
#   - Ollama corriendo en localhost:11434 con el modelo descargado
#     (si se ejecuta Llama)
#   - annotationRAG corriendo en localhost:8000 (para RAG semántico)
#
# Uso:
#   cd ~/Documents/Claude/Projects/TFM
#   bash scripts/run_size_sweep.sh
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MODELS="${MODELS:-gpt-4o llama3.1:8b}"
DBS="FANTOM5 dbSUPER"
SIZES="25 50 100 200"
N_RUNS=3

for N in $SIZES; do
  SAMPLES_DIR="$ROOT/data/samples_sizes/N=$N"
  if [ ! -d "$SAMPLES_DIR" ]; then
    echo "[skip] $SAMPLES_DIR no existe — ejecuta antes scripts/sample_size_sweep.py"
    continue
  fi
  for MODEL in $MODELS; do
    for DB in $DBS; do
      echo "==> N=$N, model=$MODEL, db=$DB"
      python3 "$ROOT/scripts/run_gpt_experiments.py" \
        --model "$MODEL" \
        --experiment E3 \
        --db "$DB" \
        --n-runs $N_RUNS \
        --rag-backend api \
        --samples-dir "$SAMPLES_DIR" \
        --results-suffix "_N${N}_ragapi"
    done
  done
done

echo ""
echo "==> Evaluación con OQuaRE"
python3 "$ROOT/scripts/oquare_eval.py" --batch \
  --experiments E3 \
  --models gpt-4o llama3.1_8b

echo ""
echo "==> Análisis de sensibilidad al tamaño"
python3 "$ROOT/scripts/analyze_size_sweep.py"
