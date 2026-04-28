# Experimento E4 – Pipeline OntoGenix

Generación de ontologías sobre bases de datos genéticas usando la herramienta
[tecnomod-um/OntoGenix](https://github.com/tecnomod-um/OntoGenix) en modo
programático (sin GUI PyQt5).

## Pipeline replicado

| Paso | Agente          | Entrada                                   | Salida                         |
|------|-----------------|-------------------------------------------|--------------------------------|
| 1    | `csv_data_preprocessing` | CSV limpio                      | stats DataFrame                |
| 2    | `dataframe2prettyjson`   | stats DataFrame                 | JSON con descripción columnar  |
| 3    | `LlmPlanner`    | JSON + task                               | `data_description_run{N}.md`   |
| 4    | `LlmOntology`   | JSON + descripción                        | `ontology_run{N}.ttl`          |
| 5    | `LlmOntoMapper` | descripción + ontología + nombre CSV      | `mapping_run{N}.ttl`           |

> El paso de **interoperabilidad con SERP API** (`LlmPlanner.update()`) se omite
> por requerir una `SERP_API_KEY`. La ontología se genera directamente desde la
> descripción producida por `LlmPlanner.interaction()`.

## Bases de datos incluidas

Subconjunto representativo definido tras la revisión con el tutor/a:

- `FANTOM5` – enhancers activos (CAGE-seq)
- `dbSUPER` – super-enhancers
- `HACER` – cis-regulatory elements activos
- `DiseaseEnhancer` – enhancers asociados a enfermedad

Los CSV de entrada viven en `data/csv_for_ontogenix/{DB}.csv` (convertidos
desde `data/samples/{DB}_sample.tsv`).

## Cómo ejecutarlo

```bash
# 1. Exportar la API key
export OPENAI_API_KEY="sk-..."

# 2. Lanzar los experimentos (4 BBDD × 3 runs = 12 corridas)
cd "$(pwd)"
python scripts/run_ontogenix_experiments.py \
       --databases FANTOM5 dbSUPER HACER DiseaseEnhancer \
       --runs 3 \
       --model gpt-4o-2024-05-13 \
       --mapping-extension ttl

# 3. Evaluar + comparar con E1/E2/E3
python scripts/evaluate_E4_vs_E1-E3.py
```

### Dependencias (en tu máquina local, no en el sandbox de Cowork)

```bash
pip install -r OntoGenix/requirements.txt
# o, si solo quieres lo imprescindible para este script:
pip install openai pandas chardet python-dotenv rdflib serpapi
```

> PyQt5 **no** hace falta porque el script no importa la GUI; llama
> directamente a los agentes `LlmPlanner`, `LlmOntology` y `LlmOntoMapper`.

## Semillas y reproducibilidad

- Semilla base: `42`; cada run incrementa la seed (`42`, `43`, `44`…).
- Temperatura = 0 dentro de `LlmBase.get_async_api_response`.
- Modelo recomendado: `gpt-4o-2024-05-13` (el declarado por OntoGenix).

## Estructura de salida por (DB, run)

```
results/E4/{DB}/gpt-4o/
├── data_description_run{N}.md       ← output de LlmPlanner
├── ontology_run{N}.ttl              ← output de LlmOntology
├── mapping_run{N}.ttl               ← output de LlmOntoMapper
├── response_raw_run{N}.txt          ← concatenación de los 3 pasos
├── metadata_run{N}.json             ← tiempos, tamaños, errores
└── summary.json                     ← agregado de las N runs
```

## Comparativa con E1/E2/E3

El script `evaluate_E4_vs_E1-E3.py` produce:

- `results/comparison_E1-E4.csv` – métricas por corrida (triples, clases,
  object/datatype properties, subClassOf, labels, parse_ok…).
- `results/comparison_E1-E4.md` – tabla resumen en Markdown (media por
  experimento y BBDD).

Las métricas se calculan con `rdflib` cuando está disponible, o por heurística
textual en su defecto.
