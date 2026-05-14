# Evaluación de LLMs para la Generación de Ontologías en Bases de Datos Genéticas

**Trabajo de Fin de Máster** · Máster Universitario en Inteligencia Artificial · Facultad de Informática · Universidad de Murcia · Mayo 2026

**Autor**: Francisco Sáez

---

## Resumen

Este repositorio contiene el código, los datos, los resultados y la memoria del Trabajo Fin de Máster *«Evaluación de LLMs para la Generación de Ontologías en Bases de Datos Genéticas»*.

La construcción manual de una ontología biomédica requiere semanas de trabajo de personal cualificado en semántica formal y dominio biomédico. La pregunta operativa que aborda este trabajo es: dado un CSV de una base de datos genética, ¿hasta dónde puede llegar un modelo de lenguaje grande (LLM) por sí solo, y dónde merece la pena ayudarle?

Para responderla se construye un banco experimental con cuatro estrategias de generación (zero-shot, vocabulario controlado, RAG y pipeline multi-agente OntoGenix), tres modelos (gpt-4o, Llama 3.1 8B, Qwen 2.5 Coder 7B) y cuatro bases de datos del dominio cis-regulatorio humano (FANTOM5, dbSUPER, HACER, DiseaseEnhancer). Se generan aproximadamente **240 ontologías** y se evalúan con tres métricas complementarias: OQuaRE estructural (Duque-Ramos et al., 2014) con razonador HermiT, fidelidad léxico-semántica al dominio cisreg, y cobertura de un corpus reproducible de **15 preguntas de competencia SPARQL**. Adicionalmente, se sustituye el RAG por keywords del experimento original por uno semántico real basado en sentence-transformers e índice vectorial Neo4j (proyecto annotationRAG del grupo Tecnomod, Universidad de Murcia).

## Contribuciones principales

El trabajo aporta tres contribuciones replicables:

1. **Guía empírica de calibración del RAG por tamaño de modelo**. Se demuestra cuantitativamente que el número óptimo de fragmentos recuperados depende de la capacidad de absorción de contexto del LLM: para modelos compactos (Llama 3.1 8B), reducir top_k de 5 a 2 cierra el **84 % del gap respecto al modelo cerrado de referencia** sin tocar el modelo.

2. **Módulo de post-procesado mecánico determinista** que separa el problema sintáctico del semántico y rescata el **100 %** de los outputs sintácticamente recuperables en E3 (McNemar p < 0.001) sin invocaciones adicionales al modelo.

3. **Métrica complementaria de fidelidad léxico-semántica al dominio**, calculable sin validación experta a partir de las ontologías de referencia del propio dominio, que matiza los resultados de OQuaRE y discrimina cuantitativamente entre estrategias de reuso de vocabulario y estrategias de generación libre.

El trabajo añade además un marco de reproducibilidad alineado con la crisis de la replicación en investigación con LLMs, con manifest SHA-256 de inputs y dependencias.

## Estructura del repositorio

```
.
├── README.md                       ← este archivo
├── docs/
│   ├── TFM_FranciscoSaez_Memoria.docx     Memoria final (67 páginas)
│   ├── TFM_FranciscoSaez_Memoria.pdf      Versión PDF
│   ├── Defensa_TFM_FranciscoSaez.pptx     Slides de defensa (19 slides)
│   ├── Defensa_TFM_FranciscoSaez.pdf      Defensa en PDF
│   └── REPRODUCIBILITY.md                 Guía operativa de reproducción
├── scripts/                        ← Código del banco experimental
├── data/
│   ├── samples/                    Muestras canónicas de 25 filas
│   ├── samples_strategies/         4 estrategias × 2 BBDD (sensibilidad muestreo)
│   ├── samples_sizes/              Barrido N ∈ {25, 50, 100, 200}
│   ├── csv_for_ontogenix/          Inputs para E4
│   ├── prompts/                    Prompts E1–E4 versionados
│   └── raw/                        TSVs originales (FANTOM5, dbSUPER)
└── results/
    ├── comparison_E1-E4.csv        Métricas absolutas por TTL
    ├── postprocess_report.csv      Efecto del post-procesado mecánico
    ├── E1/  E3/  E4/               Ontologías Turtle generadas (~240 .ttl)
    ├── evaluation/                 Tablas agregadas (OQuaRE, fidelidad, CQ, tests)
    └── figures/                    14 figuras (PNG + PDF)
```

## Diseño experimental

| Dimensión | Valores |
|---|---|
| Estrategias | E1 zero-shot · E2 vocabulario controlado · E3 RAG · E4 OntoGenix |
| Modelos | gpt-4o (2024-05-13) · Llama 3.1 8B Instruct · Qwen 2.5 Coder 7B |
| Bases de datos | FANTOM5 · dbSUPER · HACER · DiseaseEnhancer |
| Semillas | 42 · 43 · 44 |
| n principal | 4 estrategias × 3 modelos × 4 BBDD × 3 corridas = 144 ontologías |
| n sub-experimentos | + 144 corridas (sensibilidad muestreo, calibración RAG, barrido N) |

## Requisitos

- Python 3.12 (entorno virtual aislado recomendado)
- Java Runtime (para HermiT vía owlready2)
- LibreOffice (opcional, para conversión .docx → PDF)
- Ollama (para modelos open-source) con `llama3.1:8b` y `qwen2.5-coder:7b` descargados
- Neo4j 5.26 (para RAG semántico, ver `docs/REPRODUCIBILITY.md`)
- OpenAI API key (para gpt-4o)

### Instalación

```bash
# 1. Clonar el repositorio
git clone <repo-url> TFM
cd TFM

# 2. Entorno Python aislado
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r scripts/requirements_e4.txt
pip install owlready2 matplotlib python-docx pandas

# 3. Clonar OntoGenix (E4) — no incluido por ser código de terceros
git clone https://github.com/tecnomod-um/OntoGenix.git OntoGenix
# Aplicar parche LlmBase para soporte Ollama (si se proporciona)
# patch -p1 < third_party_patches/ontogenix_LlmBase.patch

# 4. Verificar instalación
python scripts/setup_check.py
python scripts/check_reproducibility.py --out results/manifest_baseline.json
```

## Reproducción rápida

```bash
# Variables de entorno
export OPENAI_API_KEY="sk-..."
# Ollama corriendo en localhost:11434 (modelos descargados)
# annotationRAG corriendo en localhost:8000 (RAG semántico)

# 1. Banco principal — E1, E2, E3 con los tres modelos
for DB in FANTOM5 dbSUPER HACER DiseaseEnhancer; do
  for EXP in E1 E2 E3; do
    for MODEL in gpt-4o llama3.1:8b qwen2.5-coder:7b; do
      python scripts/run_gpt_experiments.py \
        --model "$MODEL" --experiment "$EXP" --db "$DB" --n-runs 3
    done
  done
done

# 2. E4 — OntoGenix solo con gpt-4o
python scripts/run_ontogenix_experiments.py \
  --model gpt-4o-2024-05-13 \
  --databases FANTOM5 dbSUPER HACER DiseaseEnhancer --runs 3

# 3. Post-procesado mecánico
python scripts/postprocess_ttl.py --batch \
  --experiments E1 E2 E3 \
  --models gpt-4o llama3.1_8b qwen2.5-coder_7b

# 4. Evaluación OQuaRE con HermiT
python scripts/oquare_eval.py --batch \
  --experiments E1 E2 E3 E4 \
  --models gpt-4o llama3.1_8b qwen2.5-coder_7b

# 5. Métricas complementarias
python scripts/cisreg_fidelity.py        # fidelidad léxica al dominio
python scripts/competency_questions.py   # cobertura SPARQL (15 CQs)
python scripts/semantic_core_analysis.py # consistencia inter-BBDD

# 6. Tests estadísticos formales
python scripts/statistical_tests.py      # bootstrap + Wilcoxon + McNemar

# 7. Figuras
python scripts/generate_charts.py
python scripts/generate_charts_cross.py
python scripts/generate_charts_sensitivity.py

# 8. Manifest reproducible
python scripts/check_reproducibility.py --out results/manifest_$(date +%Y%m%d).json
```

Guía operativa completa por experimento: `docs/REPRODUCIBILITY.md`.

## Resultados destacados

### OQuaRE Global por celda (escala 1–5)

| Estrategia | gpt-4o | Llama 3.1 8B | Qwen 2.5 Coder 7B |
|---|---|---|---|
| E1 zero-shot | 3.45 | 3.36 | — (0/12 válidas) |
| E2 vocabulario | 3.98 | **4.40** | 4.00 |
| E3 RAG keywords | 2.91 | 3.45 | 3.27 |
| **E3 RAG semántico** | **4.20** (+44 %) | 3.69 → 4.08 (C1) | — |
| E4 OntoGenix | 4.12 | 3.21 | — |

### Densidad estructural — E4 vs baselines (n_triples, gpt-4o)

| Comparación | Δ media [IC 95 %] | Cohen's d | p ajustado |
|---|---|---|---|
| E4 vs E1 | +174.7 [+164.6, +186.7] | 8.48 (grande) | 0.009 |
| E4 vs E2 | +159.9 [+129.4, +183.8] | 3.23 (grande) | 0.009 |
| E4 vs E3 | +184.3 [+169.5, +201.8] | 6.15 (grande) | 0.009 |

OntoGenix produce ontologías **entre 3.91× y 6.31× más densas** que las baselines (ratio observado, IC bootstrap).

### Fidelidad léxico-semántica al dominio cisreg (recall vs 88 URIs gold)

| Configuración | Recall vs gold |
|---|---|
| E3 RAG legacy · Llama 3.1 8B | **0.563** |
| E3 RAG legacy · gpt-4o | 0.313 |
| E3 RAG semántico · gpt-4o | 0.078 |
| E3 RAG semántico · Llama 3.1 8B | 0.063 |
| E4 OntoGenix (ambos modelos) | **0.000** |

### Cobertura de preguntas de competencia (de 15)

| Configuración | Cobertura |
|---|---|
| E3 RAG legacy · Llama 3.1 8B | **5.9 / 15 (39 %)** |
| E3 RAG semántico · gpt-4o | 5.0 / 15 (33 %) |
| E4 OntoGenix · gpt-4o | 1.0 / 15 (7 %) |

Ninguna configuración del banco supera el **40 %** de cobertura: techo empírico para la generación automática end-to-end en este dominio.

### Sensibilidad al tamaño muestral (N ∈ {25, 50, 100, 200})

Para gpt-4o las métricas permanecen estables. Para Llama 3.1 8B se observa **degradación monotónica con N** en cobertura de CQ (FANTOM5: 2.00 → 0.00) y en canonical_ratio (1.000 → 0.777), consistente con saturación del contexto del modelo compacto. Conclusión operativa: **N = 25 es la elección correcta**; N ≥ 100 es contraproducente para modelos compactos.

## Métricas implementadas

- **Validez sintáctica**: `parse_ok` con rdflib
- **OQuaRE Global** y sub-características (Structural, Modularity, Reusability, Operability, Reliability) con razonador HermiT vía owlready2
- **Métricas estructurales**: 11 indicadores (WMCOnto, NOMOnto, DITM, NACOnto, CBOnto, TMOnto, LCOMOnto, ANOnto, INROnto, RROnto, AROnto)
- **Fidelidad léxica al dominio**: canonical_ratio, overlap_with_gold, Jaccard, precision_vs_gold, recall_vs_gold (gold = 88 URIs canónicas extraídas de las 8 ontologías cisreg de referencia)
- **Cobertura de preguntas de competencia**: 15 CQs SPARQL canónicas del dominio (Anexo D de la memoria)
- **Consistencia inter-BBDD**: Jaccard pareado sobre los conjuntos de URIs de las 4 BBDD por (experimento, modelo, corrida)
- **Tests estadísticos**: bootstrap pareado (10 000 réplicas), Wilcoxon de rangos con signo, McNemar para proporciones pareadas, corrección Bonferroni-Holm

## Dependencias de terceros

Este TFM se apoya en dos proyectos externos no incluidos en el repositorio:

- **OntoGenix** (Val Calvo, M.; Egaña Aranguren, M.; Fernández Breis, J. T., 2024). *OntoGenix: Leveraging large language models for enhanced ontology engineering from datasets*. Information Processing and Management, 62(3), 104042. https://github.com/tecnomod-um/OntoGenix · MIT License.
- **annotationRAG** (grupo Tecnomod, Universidad de Murcia). Microservicio FastAPI + Neo4j + sentence-transformers para RAG semántico sobre ontologías biomédicas.

Las adaptaciones técnicas aplicadas a OntoGenix (bypass del Searcher, bypass del paso SERP, soporte para Ollama vía parche en `LlmBase.py`) están documentadas en `docs/TFM_FranciscoSaez_Memoria.docx` §3.4.5.

## Citación

Si utilizas el código o los datos de este repositorio, cítalo como:

```bibtex
@mastersthesis{saez2026llm,
  author       = {Sáez, Francisco},
  title        = {Evaluación de LLMs para la generación de ontologías
                  en bases de datos genéticas},
  school       = {Universidad de Murcia, Facultad de Informática},
  type         = {Trabajo de Fin de Máster},
  year         = {2026},
  month        = {Mayo},
  note         = {Máster Universitario en Inteligencia Artificial}
}
```

## Licencia

Código fuente bajo licencia MIT (ver `LICENSE`). La memoria del TFM, las figuras y los resultados se publican bajo CC BY 4.0. Las ontologías cisreg de referencia y el proyecto OntoGenix mantienen sus respectivas licencias originales.

## Agradecimientos

A los autores de OntoGenix (Val Calvo, Egaña Aranguren y Fernández Breis) por publicar su trabajo como código abierto reproducible. Al grupo Tecnomod de la Universidad de Murcia por annotationRAG. A Duque-Ramos et al. por el marco OQuaRE. A los mantenedores de owlready2, rdflib, HermiT, sentence-transformers, Neo4j y Ollama por el ecosistema técnico que ha hecho posible este trabajo.
