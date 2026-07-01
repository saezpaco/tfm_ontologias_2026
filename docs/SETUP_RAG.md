# Setup del RAGannotationAPI (servicio para E3 — RAG semántico)

El experimento **E3** inyecta en el prompt fragmentos recuperados por un
servicio HTTP (`RAGannotationAPI`) que el cliente `scripts/rag_backend.py`
consume en `http://localhost:8000`. El servidor original del grupo Tecnomod no
está incluido en el repo, así que se proporciona una **reimplementación
compatible**: `scripts/ragannotation_server.py`.

> **Reproducibilidad:** este servidor replica el *contrato* HTTP y la
> *arquitectura* (embeddings `all-MiniLM-L6-v2` + índice vectorial sobre el
> corpus cisreg de `data/samples/schemas/`), no los pesos exactos del servicio
> original. El RAG semántico ya es nivel **R3 (metodológico)** en
> `REPRODUCIBILITY.md`; usar este servidor es coherente con esa garantía,
> pero **decláralo en la memoria** como reimplementación.

---

## Opción A — Modo memoria (recomendado, sin dependencias externas)

Índice vectorial en proceso (numpy). No necesita Docker ni Neo4j.

```bash
source .venv/bin/activate
# Embeddings semánticos reales (necesita torch + sentence-transformers):
pip install fastapi uvicorn sentence-transformers numpy requests

# Arrancar el servicio (deja esta terminal abierta)
python scripts/ragannotation_server.py        # escucha en :8000
```

En otra terminal, comprobar que responde:

```bash
python scripts/rag_backend.py --health         # → ✅ disponible
python scripts/rag_backend.py --db FANTOM5 --top-k 3
```

Si responde, ya puedes lanzar E3 (`--rag-backend api`) como en el runbook.

### Fallback sin torch (modo `hash`)

Si no puedes instalar torch/sentence-transformers, el servidor cae a un
embedder **léxico determinista** (sin dependencias pesadas). Es suficiente
para que el servicio funcione, pero **no es semántico** (solo solape léxico);
úsalo solo como último recurso y baja el umbral:

```bash
RAG_EMBED_BACKEND=hash RAG_SCORE_THR=0.1 python scripts/ragannotation_server.py
```

---

## Opción B — Modo Neo4j (reproduce la arquitectura de la memoria)

Levanta Neo4j con Docker, el servidor crea el índice vectorial
`ontology-embeddings` y lo puebla con las clases del corpus.

```bash
# 1. Neo4j 5 con Docker
docker compose -f docker-compose.neo4j.yml up -d
# espera ~20 s a que arranque; UI en http://localhost:7474 (neo4j/neo4jpassword)

# 2. Servidor en modo neo4j
source .venv/bin/activate
pip install fastapi uvicorn sentence-transformers numpy requests neo4j
export RAG_STORE=neo4j
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=neo4jpassword
python scripts/ragannotation_server.py
```

---

## Variables de entorno

| Variable | Default | Para qué |
|---|---|---|
| `RAG_API_PORT` | `8000` | Puerto del servidor |
| `RAG_STORE` | `memory` | `memory` o `neo4j` |
| `RAG_EMBED_BACKEND` | `auto` | `auto` (st si está; si no hash), `st`, `hash` |
| `RAG_EMBED_MODEL` | `all-MiniLM-L6-v2` | Modelo sentence-transformers |
| `CISREG_REFS` | `data/samples/schemas` | Carpeta del corpus a indexar |
| `NEO4J_URI/USER/PASSWORD` | bolt://localhost:7687 / neo4j / neo4jpassword | Conexión Neo4j |
| (cliente) `RAG_API_URL` | `http://localhost:8000` | URL que usa `rag_backend.py` |
| (cliente) `RAG_TOP_K` `RAG_SCORE_THR` `RAG_MAX_CHARS` | 5 / 0.4 / 5000 | Parámetros RAG / calibración |

---

## Endpoints implementados (contrato de `rag_backend.py`)

- `GET /` → health `{status, ontologies_indexed}`
- `GET /ontology/similar-ontologies?description_text=&top_k=&blacklist=` → `{results:[{ontologyId,filename,score}]}`
- `GET /ontology/similar-entities?description_text=&ontology_ids=&top_class_per_entity=&score_threshold=&context=` → `{ontologies:[{ontologyId,mapping:{col:[{class:{iri,label[]},score}]}}]}`
- `GET /ontology/similar-relations?description_text=&ontology_ids=&top_property_per_relation=&score_threshold=` → `{ontologies:[{ontologyId,mapping:{rel:[{property:{iri,label[]},score}]}}]}`

---

## Solución de problemas

- **`❌ no responde`**: el servidor no está arriba o usas otro puerto. Revisa la
  terminal del servidor y `RAG_API_URL`.
- **Mappings de entidades vacíos**: el `score_threshold` (0.4) filtra matches
  débiles. Con el backend `hash` es normal; baja `RAG_SCORE_THR`.
- **`run_gpt_experiments.py` cae a legacy**: con `--rag-backend api` y
  `RAG_FAIL_FAST=1` verás el error real en vez del fallback silencioso.
- **Primer arranque lento**: sentence-transformers descarga el modelo
  (~90 MB) la primera vez; luego queda cacheado.
