#!/usr/bin/env bash
# ───────────────────────────────────────────────────────────────────────────
# run_pending.sh — repite TODOS los experimentos pendientes del TFM y reevalúa.
#
# Pendiente (según docs/CAMBIOS_PENDIENTES_REGENERAR.md):
#   • Cross-model Llama / Qwen en E1–E4        (Tablas 15–17)
#   • Calibración del RAG en Llama (C1/C2/C3)  (Tablas 21–24)
#   • Barrido de tamaño muestral N             (Tabla 28)
#
# Requisitos en ESTA máquina:
#   • source .venv/bin/activate
#   • ollama serve  + modelos llama3.1:8b y qwen2.5-coder:7b descargados
#   • Servidor RAG escuchando en :8000   (python scripts/ragannotation_server.py)
#   • export OPENAI_API_KEY=sk-...        (para gpt-4o del barrido)
#   • OntoGenix clonado en ./OntoGenix    (para E4)
#
# Uso:
#   bash scripts/run_pending.sh            # todo: cross + calib + size + eval
#   bash scripts/run_pending.sh --cross    # solo cross-model
#   bash scripts/run_pending.sh --calib    # solo calibración
#   bash scripts/run_pending.sh --size     # solo barrido N
#   bash scripts/run_pending.sh --eval     # solo reevaluar (sin generar)
#   bash scripts/run_pending.sh --no-eval  # generar todo pero no evaluar
# ───────────────────────────────────────────────────────────────────────────
set -uo pipefail
cd "$(dirname "$0")/.."          # raíz del repo
ROOT="$(pwd)"
PY="${PYTHON:-python}"
LOG="logs/run_pending_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs
exec > >(tee -a "$LOG") 2>&1
echo "=== run_pending.sh  $(date)  root=$ROOT  log=$LOG ==="

DO_CROSS=1; DO_CALIB=1; DO_SIZE=1; DO_EVAL=1
case "${1:-}" in
  --cross) DO_CALIB=0; DO_SIZE=0; DO_EVAL=0 ;;
  --calib) DO_CROSS=0; DO_SIZE=0; DO_EVAL=0 ;;
  --size)  DO_CROSS=0; DO_CALIB=0; DO_EVAL=0 ;;
  --eval)  DO_CROSS=0; DO_CALIB=0; DO_SIZE=0 ;;
  --no-eval) DO_EVAL=0 ;;
  ""|--all) ;;
  *) echo "Opción desconocida: $1"; exit 2 ;;
esac

DBS=(FANTOM5 dbSUPER HACER DiseaseEnhancer)
run(){ echo "  → $*"; "$@"; }

# ── Preflight ──────────────────────────────────────────────────────────────
preflight(){
  echo "--- preflight ---"
  command -v ollama >/dev/null && ollama list | sed 's/^/    ollama: /' || echo "    ⚠ ollama no encontrado"
  curl -s -m 3 http://localhost:8000/ >/dev/null && echo "    RAG :8000 ✅" || echo "    ⚠ RAG :8000 no responde (E3 caerá a legacy)"
  [ -n "${OPENAI_API_KEY:-}" ] && echo "    OPENAI_API_KEY ✅" || echo "    ⚠ OPENAI_API_KEY no exportada (gpt-4o del barrido fallará)"
  [ -d OntoGenix ] && echo "    OntoGenix ✅" || echo "    ⚠ OntoGenix no clonado (E4 fallará)"
}

# ── 1. Cross-model Llama / Qwen (Tablas 15–17) ──────────────────────────────
gen_cross(){
  echo "=== CROSS-MODEL (Llama 3.1 8B + Qwen 2.5 Coder) ==="
  for MODEL in llama3.1:8b qwen2.5-coder:7b; do
    for EXP in E1 E2; do
      for DB in "${DBS[@]}"; do
        run "$PY" scripts/run_gpt_experiments.py --model "$MODEL" --experiment "$EXP" --db "$DB" --n-runs 3
      done
    done
    for DB in "${DBS[@]}"; do
      run "$PY" scripts/run_gpt_experiments.py --model "$MODEL" --experiment E3 --db "$DB" --n-runs 3 --rag-backend api
    done
  done
  # E4 OntoGenix cross-model (Llama necesita ventana de contexto amplia)
  run "$PY" scripts/run_ontogenix_experiments.py --model llama3.1:8b      --databases "${DBS[@]}" --runs 3 --seed 42 --num-ctx 16384
  run "$PY" scripts/run_ontogenix_experiments.py --model qwen2.5-coder:7b --databases "${DBS[@]}" --runs 3 --seed 42
}

# ── 2. Calibración del RAG (Tablas 21–24) ───────────────────────────────────
gen_calib(){
  echo "=== CALIBRACIÓN RAG (Llama 3.1 8B, E3) ==="
  run "$PY" scripts/rerun_deterministic.py --banco calibracion --no-patch
}

# ── 3. Barrido de tamaño muestral (Tabla 28) ────────────────────────────────
gen_size(){
  echo "=== BARRIDO DE TAMAÑO MUESTRAL (E3) ==="
  run "$PY" scripts/rerun_deterministic.py --banco barrido --no-patch
}

# ── 4. Evaluación corregida (UNA sola llamada a oquare_eval) ─────────────────
evaluate(){
  echo "=== EVALUACIÓN CORREGIDA ==="
  # Descubre dinámicamente todos los subdirectorios de modelo/variante reales
  MODELS=$(find results/E1 results/E2 results/E3 results/E4 -mindepth 2 -maxdepth 2 -type d 2>/dev/null \
             | awk -F/ '{print $NF}' | sort -u | tr '\n' ' ')
  echo "Modelos/variantes detectados: $MODELS"

  echo "--- 4.1 post-procesado mecánico ---"
  run "$PY" scripts/postprocess_ttl.py --batch --experiments E1 E2 E3 E4 --models $MODELS

  echo "--- 4.2 OQuaRE + HermiT (todo en una llamada → un único CSV) ---"
  find results -type d -name '.owlcache' -exec rm -rf {} + 2>/dev/null
  run "$PY" scripts/oquare_eval.py --batch --experiments E1 E2 E3 E4 --models $MODELS

  echo "--- 4.3 métricas funcionales y tests ---"
  run "$PY" scripts/cisreg_fidelity.py
  run "$PY" scripts/competency_questions.py
  run "$PY" scripts/statistical_tests.py

  echo "--- 4.4 manifest de reproducibilidad ---"
  run "$PY" scripts/check_reproducibility.py --out "results/manifest_$(date +%Y%m%d).json"
}

# ── Orquestación ────────────────────────────────────────────────────────────
preflight
[ "$DO_CROSS" = 1 ] && gen_cross
[ "$DO_CALIB" = 1 ] && gen_calib
[ "$DO_SIZE"  = 1 ] && gen_size
[ "$DO_EVAL"  = 1 ] && evaluate

echo "=== FIN  $(date) ==="
echo "Resultados en results/evaluation/. Avísame y los integro en la memoria."
