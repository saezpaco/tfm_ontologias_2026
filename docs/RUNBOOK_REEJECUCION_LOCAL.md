# Runbook — re-ejecución local de los experimentos pendientes

> Objetivo: generar en tu máquina lo que el sandbox no puede (necesita Ollama,
> clave de OpenAI y el RAGannotationAPI con Neo4j) y dejar los resultados en
> `results/` para que luego se integren en la memoria.
>
> **Pendiente real:**
> 1. **Cross-model** Llama 3.1 8B y Qwen 2.5 Coder en E1–E4 (Tablas 15–17). Los TTL crudos actuales están casi todos rotos (3/45 Llama, 3/36 Qwen) → hay que **regenerarlos**.
> 2. (Opcional) **Calibración** C1–C3 y **barrido N** sobre Llama: los TTL existen pero ~50 % no parsean; regenerarlos da números más limpios. Si no, se pueden evaluar tal cual (eso lo hago yo en el sandbox).
>
> Todos los comandos asumen que estás en la raíz del repo: `cd ~/Documents/Claude/Projects/TFM`

---

## 0. Aviso sobre el bug de evaluación

`scripts/rerun_deterministic.py --evaluate` (y su `evaluate_all`) llama a
`oquare_eval.py --batch` **sin `--models`**, por lo que solo evalúa `gpt-4o`.
Esa es la razón de que el cross-model, la calibración y el barrido nunca
entraran en `results/evaluation/oquare_metrics.csv`. Por eso, en el paso 4 de
abajo se ejecuta la evaluación **a mano con `--models` explícito**. No uses
`--evaluate` para esto.

---

## 1. Prerequisitos (una sola vez)

```bash
cd ~/Documents/Claude/Projects/TFM

# 1.1 Entorno Python 3.12 aislado
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r scripts/requirements_e4.txt
pip install owlready2 rdflib pandas matplotlib python-docx
java -version          # HermiT necesita Java en el PATH (cualquier JDK 11+)

# 1.2 Ollama con los dos modelos open-source
#     (instala Ollama si no lo tienes: https://ollama.com/download)
ollama serve &                       # deja el servidor corriendo
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
ollama list                          # confirma que aparecen los dos

# 1.3 OntoGenix (necesario para E4 cross-model)
git clone https://github.com/tecnomod-um/OntoGenix.git OntoGenix

# 1.4 Clave de OpenAI (solo si vas a regenerar también gpt-4o; para
#     el cross-model puro NO hace falta)
export OPENAI_API_KEY="sk-..."
```

### 1.5 RAGannotationAPI + Neo4j — **el bloqueante clave para E3**

E3 (RAG semántico) y la calibración/barrido necesitan el servicio
`RAGannotationAPI` (FastAPI + índice vectorial Neo4j del grupo Tecnomod)
escuchando en su puerto. `config.py` apunta el backend Ollama a
`http://localhost:11434`; el RAG se selecciona con `--rag-backend api`.

- Si **tienes** el servicio: arráncalo antes de E3 y verifica que responde.
- Si **no lo tienes a mano**: usa la **reimplementación compatible** incluida
  ahora en el repo (`scripts/ragannotation_server.py`). Guía completa en
  **`docs/SETUP_RAG.md`**. Arranque rápido (modo memoria):

  ```bash
  source .venv/bin/activate
  pip install fastapi uvicorn sentence-transformers numpy requests
  python scripts/ragannotation_server.py        # deja la terminal abierta
  # en otra terminal:
  python scripts/rag_backend.py --health         # → ✅ disponible
  ```

- Alternativa sin el servicio: generar E3 con `--rag-backend legacy`
  (keyword-match estático), pero **deja de ser el mismo experimento**;
  márcalo como tal. Para E1/E2/E4 el RAG no interviene.

---

## 2. Generación — cross-model Llama / Qwen (Tablas 15–17) · **lo que falta**

E1 y E2 no usan RAG; E3 sí; E4 usa OntoGenix. Bucle por modelo y BD:

```bash
source .venv/bin/activate
ollama serve &        # si no está ya corriendo

for MODEL in llama3.1:8b qwen2.5-coder:7b; do
  # --- E1 zero-shot y E2 vocabulario (sin RAG) ---
  for EXP in E1 E2; do
    for DB in FANTOM5 dbSUPER HACER DiseaseEnhancer; do
      python scripts/run_gpt_experiments.py \
             --model "$MODEL" --experiment "$EXP" --db "$DB" --n-runs 3
    done
  done

  # --- E3 RAG semántico (requiere RAGannotationAPI; si no, usa legacy) ---
  for DB in FANTOM5 dbSUPER HACER DiseaseEnhancer; do
    python scripts/run_gpt_experiments.py \
           --model "$MODEL" --experiment E3 --db "$DB" --n-runs 3 \
           --rag-backend api
  done
done

# --- E4 OntoGenix cross-model ---
for MODEL in llama3.1:8b qwen2.5-coder:7b; do
  python scripts/run_ontogenix_experiments.py \
         --model "$MODEL" \
         --databases FANTOM5 dbSUPER HACER DiseaseEnhancer \
         --runs 3 --seed 42
done
```

## 3. (Opcional) Regenerar calibración C1–C3 y barrido N sobre Llama

Solo si quieres TTL limpios en lugar de evaluar los actuales (~50 % inválidos).
Necesita el RAG API corriendo.

```bash
# Calibración (C1: top_k=2/thr=0.4/5000 · C2: 5/0.6/5000 · C3: 2/0.6/2000)
python scripts/rerun_deterministic.py --banco calibracion --no-patch

# Barrido de tamaño muestral (N=25,50,100,200)
python scripts/rerun_deterministic.py --banco barrido --no-patch
```

> Alternativa de un solo comando para regenerar TODO el banco determinista
> (incluye gpt-4o, consume API y tiempo, pero deja el banco 100 % consistente):
> `python scripts/rerun_deterministic.py --all`

---

## 4. Evaluación — **con `--models` explícito** (corrige el bug del paso 0)

```bash
source .venv/bin/activate

# 4.1 Post-procesado mecánico (determinista, sin LLM) para los nuevos modelos
python scripts/postprocess_ttl.py --batch \
       --experiments E1 E2 E3 E4 \
       --models gpt-4o llama3.1_8b qwen2.5-coder_7b

# 4.2 OQuaRE + HermiT del banco principal (los 3 modelos)
find results -type d -name '.owlcache' -exec rm -rf {} + 2>/dev/null
python scripts/oquare_eval.py --batch \
       --experiments E1 E2 E3 E4 \
       --models gpt-4o llama3.1_8b qwen2.5-coder_7b

# 4.3 OQuaRE de las variantes de calibración y barrido (son subdirs = "modelos")
python scripts/oquare_eval.py --batch --experiments E3 \
       --models llama3.1_8b_ragapi llama3.1_8b_ragapi_C1 \
                llama3.1_8b_ragapi_C2 llama3.1_8b_ragapi_C3
python scripts/oquare_eval.py --batch --experiments E3 \
       --models gpt-4o_N25_ragapi gpt-4o_N50_ragapi gpt-4o_N100_ragapi gpt-4o_N200_ragapi \
                llama3.1_8b_N25 llama3.1_8b_N50 llama3.1_8b_N100 llama3.1_8b_N200
```

> ⚠️ `oquare_eval.py` **sobrescribe** `results/evaluation/oquare_metrics.csv` en
> cada ejecución con solo las filas de esa corrida. Para no perder filas, haz
> **una sola** llamada con TODOS los `--models` que quieras en el CSV final, o
> haz copia entre llamadas. Lo más simple: una única invocación del 4.2 con
> todos los modelos+variantes juntos en `--models`.

```bash
# 4.4 Métricas funcionales y tests (leen los TTL/CSV, regeneran los resúmenes)
python scripts/cisreg_fidelity.py
python scripts/competency_questions.py
python scripts/statistical_tests.py
```

Esto regenera en `results/evaluation/`:
`oquare_metrics.csv`, `oquare_summary.md`, `cisreg_fidelity*.{csv,md}`,
`competency_questions.{csv,md}`, `statistical_tests.{json,md}`.

---

## 5. Hand-off (que yo integre los resultados)

Cuando termine la tanda:

```bash
python scripts/check_reproducibility.py --out results/manifest_$(date +%Y%m%d).json
ls -la results/evaluation/        # confirma fechas de hoy en los CSV
```

Dímelo y yo:
1. Leo los CSV nuevos en `results/evaluation/`.
2. Recalculo y actualizo las Tablas 15–17, 21–24, 28 (y reviso 29) en
   `docs/TFM_FranciscoSaez_Memoria_v2.docx`.
3. Regenero las figuras cross-model/sensibilidad si hace falta.

---

## Checklist rápido

- [ ] `.venv` activo + deps instaladas + `java -version` OK
- [ ] `ollama serve` corriendo + `llama3.1:8b` y `qwen2.5-coder:7b` descargados
- [ ] OntoGenix clonado (para E4)
- [ ] RAGannotationAPI + Neo4j arriba (para E3) — o decisión consciente de usar `legacy`
- [ ] Paso 2 (cross-model) ejecutado
- [ ] Paso 3 (calibración/barrido) ejecutado *(opcional)*
- [ ] Paso 4 (evaluación con `--models` explícito) ejecutado
- [ ] Paso 5 (manifest + avisarme)
