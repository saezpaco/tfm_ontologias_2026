# Scripts TFM - Generación de Ontologías con LLMs

## Estructura

```
scripts/
├── config.py                  # Configuración central (rutas, modelos, experimentos)
├── 01_explore_databases.py    # Exploración y análisis estadístico de las BDs
├── 02_sample_databases.py     # Generación de muestras para los prompts
├── 03_test_llm_connection.py  # Test de conectividad con LLMs (Ollama / OpenAI)
├── 04_run_experiments.py      # Ejecución de los experimentos E1, E2, E3
├── 05_evaluate_results.py     # Evaluación de las ontologías generadas
└── README.md                  # Este fichero
```

## Flujo de trabajo

```
01_explore  →  02_sample  →  03_test_llm  →  04_run_experiments  →  05_evaluate
(análisis)     (muestras)    (conectividad)   (generación)           (métricas)
```

## Requisitos

### Python
```bash
pip install pandas numpy rdflib requests openai
```

### Ollama (para modelos open-source)
```bash
# Instalar Ollama: https://ollama.ai/download
ollama pull llama3.1:8b     # Modelo principal (requiere ~5GB)
ollama pull llama3.1:70b    # Modelo grande (requiere ~40GB RAM)
ollama pull mistral:7b       # Referencia adicional
```

### OpenAI API (opcional, para baseline GPT-4o)
```bash
export OPENAI_API_KEY='sk-...'
```

## Uso paso a paso

### 1. Explorar bases de datos
```bash
python 01_explore_databases.py          # Todas las BDs
python 01_explore_databases.py --db dbSUPER  # Solo dbSUPER
```

### 2. Generar muestras
```bash
python 02_sample_databases.py           # Todas las BDs
python 02_sample_databases.py --db ENdb --n-rows 30
```

### 3. Verificar conectividad LLM
```bash
python 03_test_llm_connection.py            # Ollama + OpenAI
python 03_test_llm_connection.py --provider ollama
python 03_test_llm_connection.py --full-test  # Incluye test de generación Turtle
```

### 4. Ejecutar experimentos
```bash
# Experimento E1 (base, sin contexto adicional)
python 04_run_experiments.py --experiment E1 --model llama3.1:8b --db dbSUPER

# Experimento E1 con todas las BDs
python 04_run_experiments.py --experiment E1 --model llama3.1:8b

# Experimento E2 (con vocabulario controlado)
python 04_run_experiments.py --experiment E2 --model llama3.1:8b

# Experimento E3 (con RAG - ontología cisreg)
python 04_run_experiments.py --experiment E3 --model llama3.1:8b

# Todos los experimentos
python 04_run_experiments.py --experiment all --model llama3.1:8b --n-runs 3

# Ver los prompts sin llamar al LLM (dry-run)
python 04_run_experiments.py --experiment E1 --model llama3.1:8b --dry-run
```

### 5. Evaluar resultados
```bash
python 05_evaluate_results.py            # Todos los resultados
python 05_evaluate_results.py --experiment E1
python 05_evaluate_results.py --experiment E1 --model llama3.1:8b
```

## Bases de datos disponibles

| Base de datos | Filas | Descripción |
|---|---|---|
| dbSUPER | 69,022 | Super-enhancers con coordenadas, genes diana |
| FANTOM5 | 96,932 | Enhancers por CAGE-seq |
| ENdb | 14,206 | Enhancers validados experimentalmente |
| HACER | 7,476,524 | Human Active Cis-regulatory Elements |
| DiseaseEnhancer | 4,059 | Enhancers asociados a enfermedades |
| SEA | 2,282,026 | Super-Enhancer Archive |
| SCREEN | 1,922,454 | ENCODE cCREs |
| EnDisease | 777 | Enhancers - enfermedades con publicaciones |
| RefSeq | ~varios | Secuencias de referencia NCBI |
| Ensembl | ~varios | Datos Ensembl |

## Experimentos

| ID | Nombre | Input al LLM | Objetivo |
|---|---|---|---|
| E1 | Base | Muestra de BD | Capacidad nativa de inferencia |
| E2 | Vocabulario | Muestra + vocab. controlado cisreg | Impacto del vocabulario |
| E3 | RAG | Muestra + fragmentos ontología cisreg | Impacto del contexto ontológico |

## Modelos

| Modelo | Proveedor | Parámetros | Notas |
|---|---|---|---|
| llama3.1:8b | Ollama | 8B | Recomendado para inicio (modelo principal) |
| llama3.1:70b | Ollama | 70B | Máxima calidad open-source (requiere GPU) |
| llama3.2:3b | Ollama | 3B | Muy eficiente, calidad reducida |
| mistral:7b | Ollama | 7B | Referencia adicional open-source |
| gpt-4o | OpenAI API | - | Baseline comercial (requiere API key) |
| gpt-4o-mini | OpenAI API | - | Baseline comercial compacto |

## Métricas de evaluación

- **VS** (Validez Sintáctica): ¿es el Turtle parseable?
- **F1_c** (F1 clases): coincidencia de clases con la ontología cisreg
- **F1_p** (F1 propiedades): coincidencia de propiedades
- **M** (Mappings): corrección de mappings skos:exactMatch/closeMatch
- **CA** (Cobertura Anotaciones): % clases con skos:prefLabel

## Estructura de resultados

```
results/
├── 01_exploration_report.json      # Análisis estadístico de las BDs
├── 03_llm_connectivity_test.json   # Resultados test LLM
├── E1/                             # Resultados Experimento 1
│   ├── dbSUPER/
│   │   └── llama3.1_8b/
│   │       ├── ontology_run1.ttl   # Ontología generada
│   │       ├── metadata_run1.json  # Metadatos de la generación
│   │       └── summary.json        # Resumen de todas las runs
│   └── ...
├── E2/                             # Resultados Experimento 2
├── E3/                             # Resultados Experimento 3
└── evaluation/
    ├── metrics_all.csv             # Métricas detalladas por run
    ├── metrics_summary.csv         # Medias por experimento/BD/modelo
    └── evaluation_report.json      # Informe completo de evaluación
```
