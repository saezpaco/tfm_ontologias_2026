#!/usr/bin/env python3
"""
ragannotation_server.py
───────────────────────
Servidor **compatible** con el cliente `scripts/rag_backend.py` del TFM.

Reimplementa la API `RAGannotationAPI` (FastAPI + búsqueda vectorial) que el
experimento E3 (RAG semántico) espera escuchando en http://localhost:8000.
El corpus indexado son las ontologías cisreg de referencia del propio repo
(`data/samples/schemas/*.txt`), embebidas con sentence-transformers
`all-MiniLM-L6-v2` (384 dim) — el mismo modelo descrito en la memoria.

⚠️  Reproducibilidad: este servidor es una **re-implementación** del servicio
    original de Tecnomod (que no está disponible). Reproduce el *contrato* HTTP
    y la *arquitectura* (embeddings + índice vectorial), no sus pesos exactos.
    El RAG semántico ya está clasificado como nivel R3 (metodológico) en
    docs/REPRODUCIBILITY.md, así que esto es coherente con esa garantía.
    Documenta su uso en la memoria.

Dos modos de almacenamiento (variable de entorno RAG_STORE):
    memory  (default) → índice vectorial en proceso (numpy). Cero dependencias
                        externas. Recomendado para reproducir E3 sin fricción.
    neo4j             → índice vectorial Neo4j ('ontology-embeddings').
                        Requiere NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD.
                        Reproduce la arquitectura exacta de la memoria.

Endpoints (contrato consumido por rag_backend.py):
    GET /                                  → health
    GET /ontology/similar-ontologies       → {"results": [{ontologyId,filename,score}]}
    GET /ontology/similar-entities         → {"ontologies": [{ontologyId, mapping}]}
    GET /ontology/similar-relations        → {"ontologies": [{ontologyId, mapping}]}

Arranque:
    pip install fastapi uvicorn sentence-transformers numpy
    python scripts/ragannotation_server.py            # :8000, modo memory
    # o con uvicorn directamente:
    uvicorn scripts.ragannotation_server:app --host 0.0.0.0 --port 8000

Diagnóstico (en otra terminal):
    python scripts/rag_backend.py --health
    python scripts/rag_backend.py --db FANTOM5 --top-k 3
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np

try:
    from fastapi import FastAPI, Query
except ImportError:
    sys.exit("Falta FastAPI. Instala: pip install fastapi uvicorn sentence-transformers numpy")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = Path(os.environ.get(
    "CISREG_REFS", PROJECT_ROOT / "data" / "samples" / "schemas"))
EMBED_MODEL = os.environ.get("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
RAG_STORE = os.environ.get("RAG_STORE", "memory").lower()
# Backend de embeddings: 'auto' usa sentence-transformers si está disponible
# y cae a 'hash' (léxico, sin torch) si no. 'st' fuerza sentence-transformers,
# 'hash' fuerza el fallback léxico determinista.
RAG_EMBED_BACKEND = os.environ.get("RAG_EMBED_BACKEND", "auto").lower()
HASH_DIM = int(os.environ.get("RAG_HASH_DIM", "384"))

# Las 8 ontologías cisreg de referencia (gold set del TFM)
CORPUS_FILES = [
    "crm", "crm_example",
    "crm2gene", "crm2gene_example",
    "crm2phen", "crm2phen_example",
    "crm2tfac", "crm2tfac_example",
]

# Prefijos estándar que NO son entidades de dominio (se ignoran como clases)
_STD_PRED = {
    "rdf:type", "rdfs:subClassOf", "rdf:subject", "rdf:predicate",
    "rdf:object", "skos:prefLabel", "skos:definition", "skos:closeMatch",
    "rdfs:label", "rdfs:isDefinedBy", "a",
}


# ───────────────────────────────────────────────────────────────────
# Parser ligero de los esquemas Turtle-like (con placeholders, no
# parsean con rdflib estricto, por eso un parser por líneas).
# ───────────────────────────────────────────────────────────────────
def _parse_prefixes(text: str) -> dict[str, str]:
    prefixes: dict[str, str] = {}
    for m in re.finditer(r'@prefix\s+([\w\-]*):\s*<([^>]+)>', text):
        prefixes[m.group(1)] = m.group(2)
    return prefixes


def _expand(curie: str, prefixes: dict[str, str]) -> str:
    if curie.startswith("<") and curie.endswith(">"):
        return curie[1:-1]
    if ":" in curie:
        pfx, local = curie.split(":", 1)
        if pfx in prefixes:
            return prefixes[pfx] + local
    return curie


def _strip_comment(line: str) -> tuple[str, str]:
    """Separa el comentario inline '# ...' (label humano) del contenido."""
    # No confundir '#' dentro de <...> o de CURIEs con fragmento.
    in_angle = False
    for i, ch in enumerate(line):
        if ch == "<":
            in_angle = True
        elif ch == ">":
            in_angle = False
        elif ch == "#" and not in_angle:
            # Heurística: un '#' precedido de espacio es comentario.
            if i > 0 and line[i - 1] in " \t":
                return line[:i].rstrip(), line[i + 1:].strip()
    return line, ""


def parse_schema(path: Path) -> dict[str, Any]:
    """Extrae de un esquema cisreg: descripción global, clases y propiedades."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    prefixes = _parse_prefixes(text)

    classes: list[dict[str, Any]] = []
    props: dict[str, dict[str, Any]] = {}
    descriptions: list[str] = []

    current_subject: str | None = None
    current_is_class = False
    block_label = ""
    block_def = ""

    def flush_block():
        nonlocal current_subject, current_is_class, block_label, block_def
        if current_subject and current_is_class:
            iri = _expand(current_subject, prefixes)
            label = block_label or current_subject.split(":")[-1]
            classes.append({
                "iri": iri,
                "label": label,
                "definition": block_def,
                "text": f"{label}. {block_def}".strip(),
            })
            if block_def:
                descriptions.append(block_def)
        current_subject = None
        current_is_class = False
        block_label = ""
        block_def = ""

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("@prefix"):
            continue
        content, comment = _strip_comment(line)
        stripped = content.strip()
        if not stripped:
            continue

        # ¿Nueva línea de sujeto? (no empieza por separador de predicado)
        starts_new_subject = bool(re.match(r'^\S', raw)) and not raw[0].isspace()

        tokens = stripped.split()
        # Detectar inicio de bloque sujeto: 'subject predicate object ...'
        if starts_new_subject and len(tokens) >= 1 and ":" in tokens[0] or (
                starts_new_subject and tokens and tokens[0].startswith("<")):
            flush_block()
            current_subject = tokens[0]
            # ¿es declaración de clase?
            if "owl:Class" in stripped and ("rdf:type" in stripped or " a " in f" {stripped} "):
                current_is_class = True

        # Capturar prefLabel / definition del bloque
        m_lbl = re.search(r'skos:prefLabel\s+"([^"]+)"', stripped)
        if m_lbl:
            block_label = m_lbl.group(1)
        m_def = re.search(r'skos:definition\s+"([^"]+)"', stripped)
        if m_def:
            block_def = m_def.group(1)
            descriptions.append(m_def.group(1))

        # Extraer predicados (propiedades de dominio)
        # Triple en la misma línea: sujeto/; predicado objeto ;
        for tok_i, tok in enumerate(tokens):
            if re.match(r'^(obo|sio|biolink|schema|dc|rdfs):\S+', tok) \
                    and tok not in _STD_PRED \
                    and tok_i > 0:  # no es el sujeto
                # ¿está en posición de predicado? (token siguiente existe)
                if tok_i + 1 < len(tokens):
                    iri = _expand(tok, prefixes)
                    label = comment.split("#")[0].strip() if comment else tok.split(":")[-1]
                    # Limpia labels tipo '"human"' del comentario
                    label = label.strip().strip('"') or tok.split(":")[-1]
                    if iri not in props:
                        props[iri] = {
                            "iri": iri,
                            "label": label,
                            "text": f"{label} ({tok})",
                        }
    flush_block()

    onto_id = path.stem
    global_desc = f"cis-regulatory module ontology {onto_id}. " + " ".join(descriptions[:8])
    return {
        "ontologyId": onto_id,
        "filename": path.name,
        "description": global_desc.strip(),
        "classes": classes,
        "properties": list(props.values()),
    }


# ───────────────────────────────────────────────────────────────────
# Índice vectorial
# ───────────────────────────────────────────────────────────────────
def _cosine(q: np.ndarray, M: np.ndarray) -> np.ndarray:
    qn = q / (np.linalg.norm(q) + 1e-9)
    Mn = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    return Mn @ qn


# ───────────────────────────────────────────────────────────────────
# Backend de embeddings (sentence-transformers o fallback léxico)
# ───────────────────────────────────────────────────────────────────
class _HashEmbedder:
    """Embedder léxico determinista sin dependencias pesadas (sin torch).

    Vectoriza por hashing de tokens + n-gramas de caracteres a un espacio
    de dimensión fija. NO es semántico como all-MiniLM-L6-v2: captura
    solape léxico, suficiente para validar el servicio y como modo
    'sin-dependencias'. Para resultados fieles usa el backend 'st'.
    """

    def __init__(self, dim: int = HASH_DIM):
        self.dim = dim

    @staticmethod
    def _tokens(text: str) -> list[str]:
        text = text.lower()
        words = re.findall(r"[a-z0-9_]+", text)
        grams = [text[i:i + 3] for i in range(max(0, len(text) - 2))]
        return words + grams

    def encode(self, texts, normalize_embeddings: bool = False):
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for r, t in enumerate(texts):
            for tok in self._tokens(t or ""):
                h = hash(tok) % self.dim
                out[r, h] += 1.0
        return out


def make_embedder():
    """Devuelve (embedder, nombre) según RAG_EMBED_BACKEND."""
    want = RAG_EMBED_BACKEND
    if want in ("auto", "st"):
        try:
            from sentence_transformers import SentenceTransformer
            print(f"[rag] embeddings: sentence-transformers {EMBED_MODEL}")
            return SentenceTransformer(EMBED_MODEL), f"st:{EMBED_MODEL}"
        except Exception as e:  # noqa: BLE001
            if want == "st":
                sys.exit(f"[rag] RAG_EMBED_BACKEND=st pero falta sentence-transformers: {e}")
            print(f"[rag] sentence-transformers no disponible ({type(e).__name__}); "
                  f"usando fallback léxico 'hash'. Instala torch+sentence-transformers "
                  f"para embeddings semánticos.")
    print(f"[rag] embeddings: fallback léxico hash (dim={HASH_DIM})")
    return _HashEmbedder(), f"hash:{HASH_DIM}"


class VectorIndex:
    """Carga el corpus, calcula embeddings y resuelve búsquedas top-k.
    Mantiene matrices separadas para ontologías, clases y propiedades."""

    def __init__(self):
        self.model, self.embed_name = make_embedder()
        self.ontologies: list[dict] = []
        self._load_corpus()
        self._build_embeddings()
        self._maybe_neo4j()

    def _load_corpus(self):
        for name in CORPUS_FILES:
            for ext in (".ttl", ".txt"):
                p = SCHEMAS_DIR / f"{name}{ext}"
                if p.exists():
                    self.ontologies.append(parse_schema(p))
                    break
        if not self.ontologies:
            sys.exit(f"[rag] no se encontró corpus en {SCHEMAS_DIR}")
        n_cls = sum(len(o["classes"]) for o in self.ontologies)
        n_prop = sum(len(o["properties"]) for o in self.ontologies)
        print(f"[rag] corpus: {len(self.ontologies)} ontologías, "
              f"{n_cls} clases, {n_prop} propiedades")

    def _embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 384), dtype=np.float32)
        return np.asarray(self.model.encode(texts, normalize_embeddings=False),
                          dtype=np.float32)

    def _build_embeddings(self):
        self.onto_vecs = self._embed([o["description"] for o in self.ontologies])
        for o in self.ontologies:
            o["_cls_vecs"] = self._embed([c["text"] for c in o["classes"]])
            o["_prop_vecs"] = self._embed([p["text"] for p in o["properties"]])

    def _maybe_neo4j(self):
        if RAG_STORE != "neo4j":
            self.neo4j = None
            return
        try:
            from neo4j import GraphDatabase
        except ImportError:
            sys.exit("[rag] RAG_STORE=neo4j pero falta 'neo4j'. pip install neo4j")
        uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        pwd = os.environ.get("NEO4J_PASSWORD", "neo4jpassword")
        print(f"[rag] conectando a Neo4j {uri} e indexando embeddings…")
        self.neo4j = GraphDatabase.driver(uri, auth=(user, pwd))
        self._index_neo4j()

    def _index_neo4j(self):
        """Crea el índice vectorial 'ontology-embeddings' y carga las clases.
        (La búsqueda sigue resolviéndose en memoria; Neo4j queda como store
        persistente para reproducir la arquitectura descrita en la memoria.)"""
        with self.neo4j.session() as s:
            s.run("CREATE VECTOR INDEX `ontology-embeddings` IF NOT EXISTS "
                  "FOR (c:OntoClass) ON (c.embedding) "
                  "OPTIONS {indexConfig: {`vector.dimensions`: 384, "
                  "`vector.similarity_function`: 'cosine'}}")
            for o in self.ontologies:
                for c, v in zip(o["classes"], o["_cls_vecs"]):
                    s.run("MERGE (c:OntoClass {iri:$iri}) "
                          "SET c.label=$label, c.ontologyId=$oid, "
                          "c.embedding=$emb",
                          iri=c["iri"], label=c["label"],
                          oid=o["ontologyId"], emb=v.tolist())
        print("[rag] Neo4j: índice 'ontology-embeddings' poblado")

    # ─── búsquedas ───────────────────────────────────────────────
    def similar_ontologies(self, text: str, top_k: int,
                           blacklist: set[str]) -> list[dict]:
        q = self._embed([text])[0]
        sims = _cosine(q, self.onto_vecs)
        order = np.argsort(-sims)
        out = []
        for i in order:
            o = self.ontologies[i]
            if o["ontologyId"] in blacklist:
                continue
            out.append({
                "ontologyId": o["ontologyId"],
                "filename": o["filename"],
                "score": round(float(sims[i]), 4),
            })
            if len(out) >= top_k:
                break
        return out

    def _onto_by_id(self, oid: str) -> dict | None:
        for o in self.ontologies:
            if o["ontologyId"] == oid:
                return o
        return None

    def similar_entities(self, entities: list[str], ontology_ids: list[str],
                         top_class_per_entity: int, score_threshold: float
                         ) -> list[dict]:
        results = []
        for oid in ontology_ids:
            o = self._onto_by_id(oid)
            if not o or len(o["classes"]) == 0:
                continue
            mapping: dict[str, list] = {}
            for ent in entities:
                qv = self._embed([ent])[0]
                sims = _cosine(qv, o["_cls_vecs"])
                order = np.argsort(-sims)[:top_class_per_entity]
                matches = []
                for j in order:
                    sc = float(sims[j])
                    if sc < score_threshold:
                        continue
                    cls = o["classes"][j]
                    matches.append({
                        "class": {"iri": cls["iri"], "label": [cls["label"]]},
                        "score": round(sc, 4),
                    })
                if matches:
                    mapping[ent] = matches
            if mapping:
                results.append({"ontologyId": oid, "mapping": mapping})
        return results

    def similar_relations(self, relations: list[str], ontology_ids: list[str],
                          top_property_per_relation: int, score_threshold: float
                          ) -> list[dict]:
        results = []
        for oid in ontology_ids:
            o = self._onto_by_id(oid)
            if not o or len(o["properties"]) == 0:
                continue
            mapping: dict[str, list] = {}
            for rel in relations:
                qv = self._embed([rel])[0]
                sims = _cosine(qv, o["_prop_vecs"])
                order = np.argsort(-sims)[:top_property_per_relation]
                matches = []
                for j in order:
                    sc = float(sims[j])
                    if sc < score_threshold:
                        continue
                    pr = o["properties"][j]
                    matches.append({
                        "property": {"iri": pr["iri"], "label": [pr["label"]]},
                        "score": round(sc, 4),
                    })
                if matches:
                    mapping[rel] = matches
            if mapping:
                results.append({"ontologyId": oid, "mapping": mapping})
        return results


# ───────────────────────────────────────────────────────────────────
# FastAPI app
# ───────────────────────────────────────────────────────────────────
app = FastAPI(title="RAGannotationAPI (compatible)", version="1.0-tfm")
INDEX: VectorIndex | None = None


@app.on_event("startup")
def _startup():
    global INDEX
    INDEX = VectorIndex()
    print(f"[rag] listo. store={RAG_STORE}  embeddings={INDEX.embed_name}")


@app.get("/")
def root():
    n = len(INDEX.ontologies) if INDEX else 0
    return {"status": "ok", "service": "RAGannotationAPI-compatible",
            "store": RAG_STORE, "ontologies_indexed": n}


def _split(csv: str | None) -> list[str]:
    if not csv:
        return []
    return [x.strip() for x in csv.split(",") if x.strip()]


@app.get("/ontology/similar-ontologies")
def similar_ontologies(description_text: str = Query(...),
                       top_k: int = Query(5),
                       blacklist: str | None = Query(None)):
    res = INDEX.similar_ontologies(description_text, top_k, set(_split(blacklist)))
    return {"results": res}


@app.get("/ontology/similar-entities")
def similar_entities(description_text: str = Query(...),
                     ontology_ids: str = Query(...),
                     top_class_per_entity: int = Query(1),
                     score_threshold: float = Query(0.4),
                     context: str = Query("false")):
    entities = _split(description_text)
    oids = _split(ontology_ids)
    res = INDEX.similar_entities(entities, oids, top_class_per_entity, score_threshold)
    return {"ontologies": res}


@app.get("/ontology/similar-relations")
def similar_relations(description_text: str = Query(...),
                      ontology_ids: str = Query(...),
                      top_property_per_relation: int = Query(1),
                      score_threshold: float = Query(0.4)):
    relations = _split(description_text)
    oids = _split(ontology_ids)
    res = INDEX.similar_relations(relations, oids, top_property_per_relation, score_threshold)
    return {"ontologies": res}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("RAG_API_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
