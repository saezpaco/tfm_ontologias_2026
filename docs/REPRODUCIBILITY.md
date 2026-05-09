# Reproducibilidad del TFM

> *"Evaluación de LLMs para la Generación de Ontologías en Bases de Datos Genéticas"*  ·  Francisco Sáez

Este documento es la guía operativa para **reproducir cualquier experimento** descrito en la memoria. Está alineado con las recomendaciones de Pineau et al. (2021) sobre reproducibilidad en investigación de aprendizaje automático y reconoce explícitamente las amenazas que la "crisis de la replicación" plantea para experimentos basados en LLMs (Hutson, 2018; Gundersen & Kjensmo, 2018).

---

## 1. Tres niveles de reproducibilidad

Los experimentos se garantizan a tres niveles distintos, no equivalentes:

| Nivel | Garantía | Cómo se asegura | Qué experimentos cubre |
|---|---|---|---|
| **R1 — Reproducibilidad estricta** (bit-a-bit) | El mismo input produce el mismo output byte por byte | Seeds fijas + algoritmo determinista + versiones pinneadas | Post-procesado de TTL, evaluador OQuaRE estructural (sin razonador), generación de muestras |
| **R2 — Reproducibilidad estadística** | Mismo input produce outputs con la misma distribución (medias y varianzas indistinguibles) | Seeds + temperature=0 + modelo snapshot fijo | E1, E2, E3 (legacy y RAG semántico), E4 OntoGenix con gpt-4o |
| **R3 — Reproducibilidad metodológica** | El procedimiento es replicable; los outputs concretos pueden variar pero las conclusiones cualitativas se mantienen | Documentación completa del setup, prompts versionados, datos congelados | Razonador HermiT (HermiT no es determinista), API de RAGannotationAPI, modelos open-source vía Ollama |

> **Importante**: ningún experimento con `gpt-4o` está al nivel R1. OpenAI no garantiza determinismo bit-a-bit incluso con `temperature=0` y `seed`. Documentamos esta limitación explícitamente.

---

## 2. Setup mínimo para reproducir

```bash
# 2.1 Clonar el repositorio del TFM
git clone <repo-url> TFM
cd TFM

# 2.2 Python 3.12 con venv aislado (requerido)
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel

# 2.3 Dependencias del pipeline E1-E4 + evaluador
pip install -r scripts/requirements_e4.txt
pip install owlready2 matplotlib python-docx

# 2.4 Clonar OntoGenix (E4)
git clone https://github.com/tecnomod-um/OntoGenix.git OntoGenix

# 2.5 Setup Ollama (para experimentos open-source)
brew install ollama  # macOS; o curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b

# 2.6 Setup Neo4j + RAGannotationAPI (para E3 con RAG semántico)
# Ver docs/SETUP_RAG.md para instrucciones detalladas

# 2.7 Verificar reproducibilidad inicial
python scripts/check_reproducibility.py --out results/manifest_baseline.json
```

---

## 3. Cómo reproducir cada experimento

### E1 — Zero-shot

```bash
export OPENAI_API_KEY="sk-..."
for DB in FANTOM5 dbSUPER HACER DiseaseEnhancer; do
  python scripts/run_gpt_experiments.py \
         --model gpt-4o --experiment E1 --db "$DB" --n-runs 3
done
```

**Determinismo esperado**: ~95% — gpt-4o con seed=42 converge a outputs muy similares pero no idénticos byte-a-byte. Comparar con `results/E1/{DB}/gpt-4o/` previo.

### E2 — Vocabulario controlado

Ídem cambiando `--experiment E2`. Mismas garantías que E1.

### E3 — RAG (legacy + semántico)

```bash
# Legacy (keyword-match estático)
for DB in FANTOM5 dbSUPER HACER DiseaseEnhancer; do
  python scripts/run_gpt_experiments.py \
         --model gpt-4o --experiment E3 --db "$DB" --n-runs 3 \
         --rag-backend legacy --results-suffix _legacy
done

# RAG semántico (requiere RAGannotationAPI corriendo)
for DB in FANTOM5 dbSUPER HACER DiseaseEnhancer; do
  python scripts/run_gpt_experiments.py \
         --model gpt-4o --experiment E3 --db "$DB" --n-runs 3 \
         --rag-backend api --results-suffix _ragapi
done
```

### E4 — OntoGenix

```bash
python scripts/run_ontogenix_experiments.py \
       --model gpt-4o-2024-05-13 \
       --databases FANTOM5 dbSUPER HACER DiseaseEnhancer \
       --runs 3
```

### Cross-model con Llama / Qwen

Igual que arriba pero `--model llama3.1:8b` o `--model qwen2.5-coder:7b`. Para Llama es necesario `--num-ctx 16384` o superior.

### Análisis de sensibilidad al muestreo

```bash
python scripts/sample_strategies.py \
       --input-dir data/raw --suffix .tsv \
       --databases FANTOM5 dbSUPER --n-rows 25
# Luego cada estrategia:
for STRAT in A_head B_random C_stratified D_diversity; do
  python scripts/run_gpt_experiments.py \
         --model gpt-4o --experiment E1 --db FANTOM5 --n-runs 1 \
         --samples-dir "data/samples_strategies/$STRAT" \
         --results-suffix "_$STRAT"
done
```

### Calibración del RAG para modelos compactos

```bash
# Configuración C3 (combinada agresiva, recomendada como punto de partida)
for DB in FANTOM5 dbSUPER HACER DiseaseEnhancer; do
  python scripts/run_gpt_experiments.py \
         --model llama3.1:8b --experiment E3 --db "$DB" --n-runs 3 \
         --rag-backend api \
         --rag-top-k 2 --rag-score-thr 0.6 --rag-max-chars 2000 \
         --results-suffix _ragapi_C3
done
```

---

## 4. Evaluación

```bash
# Post-procesado mecánico (auto-prefix + escape de local names)
python scripts/postprocess_ttl.py --batch \
       --experiments E1 E2 E3 E4 \
       --models gpt-4o llama3.1_8b qwen2.5-coder_7b

# Evaluación OQuaRE con razonador HermiT
find results -type d -name '.owlcache' -exec rm -rf {} + 2>/dev/null
python scripts/oquare_eval.py --batch \
       --models gpt-4o llama3.1_8b qwen2.5-coder_7b \
       --experiments E1 E2 E3 E4

# Tablas y figuras
python scripts/evaluate_E4_vs_E1-E3.py
python scripts/generate_charts_cross.py
python scripts/generate_charts_sensitivity.py
```

---

## 5. Manifest de reproducibilidad

Cada vez que se ejecuta una tanda completa de experimentos, regenera el manifest:

```bash
python scripts/check_reproducibility.py \
       --out results/manifest_$(date +%Y%m%d).json
```

Esto produce un JSON con:
- Versión de Python e intérprete
- Versiones exactas de las 12 dependencias críticas
- Modelos LLM con su snapshot recomendado
- Parámetros de generación (`temperature`, `top_p`, `seed`, `max_tokens`)
- Hashes SHA-256 de **todos los inputs deterministas** (samples, esquemas RAG, CSV, scripts)
- Recuento de outputs por (experimento, BBDD, modelo)
- Commit git si está disponible

Para detectar drift entre dos manifests:

```bash
python scripts/check_reproducibility.py \
       --diff results/manifest_baseline.json
```

---

## 6. Garantías de reproducibilidad — tabla matricial

| Componente | Reproducible | Cómo se asegura | Limitaciones documentadas |
|---|---|---|---|
| Muestreo de datos | R1 | Seeds 42 (sample), 42-44 (run) | Las 4 estrategias del §4.3 cubren la sensibilidad |
| Prompts E1-E4 | R1 | Strings constantes en `run_gpt_experiments.py` y plantillas .prompt de OntoGenix | Versionados en git |
| Cliente OpenAI | R2 | `gpt-4o-2024-05-13` snapshot fijo | OpenAI no garantiza determinismo bit-a-bit |
| Cliente Ollama | R2-R3 | Modelo + digest del Modelfile | Las quantizaciones varían entre actualizaciones |
| RAG legacy | R1 | Esquemas Turtle congelados en `data/samples/schemas/` | — |
| RAG semántico | R3 | Modelo `all-MiniLM-L6-v2` + Neo4j vector index | sentence-transformers actualiza pesos sin avisar |
| Post-procesado | R1 | Regex deterministas + saneo lexical determinista | — |
| Evaluador OQuaRE estructural | R1 | rdflib + métricas calculadas algorítmicamente | — |
| Razonador HermiT | R3 | HermiT vía owlready2 | HermiT no es determinista en orden de inferencia |
| Figuras matplotlib | R1 | Datos del CSV + script congelado | — |

---

## 7. Limitaciones reconocidas

1. **gpt-4o no es 100% determinista**. Aun fijando `seed=42` y `temperature=0`, la API de OpenAI puede devolver outputs ligeramente distintos en ejecuciones separadas. Las medias inter-runs (3 corridas) atenúan esta variación pero no la eliminan.

2. **Drift de modelos cerrados**. `gpt-4o` (alias móvil) puede apuntar a una versión distinta dentro de unos meses. Por eso fijamos el **snapshot** `gpt-4o-2024-05-13` en `MODEL_SNAPSHOTS` del script de auditoría. Quienes intenten reproducir en 2027 deberán usar ese snapshot explícito.

3. **Drift de embeddings**. `sentence-transformers/all-MiniLM-L6-v2` puede recibir actualizaciones que cambien sus vectores. La hash del modelo no se versiona automáticamente.

4. **HermiT no determinista**. El razonador OWL DL puede producir clasificaciones equivalentes pero en orden distinto. Esto solo afecta a `n_inferred_classes`, no a `consistent` ni `n_unsatisfiable`.

5. **Modelos open-source vía Ollama**. La quantización Q4_K_M usada por defecto puede regenerarse al re-descargar el modelo. Para reproducción estricta, fijar el digest exacto: `ollama show llama3.1:8b --modelfile`.

6. **El razonador y la API RAG requieren servicios externos** (Java/HermiT, Neo4j, FastAPI). Las dependencias entre servicios pueden generar fallos transitorios no determinísticos.

---

## 8. Referencias clave

- Hutson, M. (2018). *Artificial intelligence faces reproducibility crisis*. Science, 359(6377), 725–726.
- Gundersen, O. E., & Kjensmo, S. (2018). *State of the art: Reproducibility in artificial intelligence*. AAAI 2018.
- Pineau, J., Vincent-Lamarre, P., Sinha, K., Larivière, V., Beygelzimer, A., d'Alché-Buc, F., Fox, E., & Larochelle, H. (2021). *Improving reproducibility in machine learning research (a report from the NeurIPS 2019 reproducibility program)*. JMLR 22.
- Henderson, P., Islam, R., Bachman, P., Pineau, J., Precup, D., & Meger, D. (2018). *Deep reinforcement learning that matters*. AAAI 2018.

Ver bibliografía completa en §13 del documento de metodología.
