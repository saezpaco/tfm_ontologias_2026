#!/usr/bin/env python3
"""
rag_backend.py
──────────────
Cliente para el backend RAG `RAGannotationAPI`
(github.com/<repo>) — API local FastAPI con embeddings indexados en
Neo4j que sustituye al RAG por keywords del experimento E3 original.

Arquitectura del backend:
    sentence-transformers/all-MiniLM-L6-v2 (384 dim)
    Neo4j vector index 'ontology-embeddings'  ← corpus de ontologías
    FastAPI uvicorn @ :8000  ← endpoints HTTP

Endpoints consumidos:
    GET /ontology/similar-ontologies      → top-K ontologías
    GET /ontology/similar-entities        → mapeo de columnas → clases
    GET /ontology/similar-relations       → mapeo de relaciones → properties

Función pública principal:
    retrieve_context(sample_text, db_name=None, k=5)
        Devuelve un STRING listo para inyectar en el placeholder
        ``{ontology_fragments}`` del USER_PROMPT_E3, manteniendo la
        misma firma que la función legacy `get_rag_fragments`.

Configuración:
    RAG_API_URL      base URL del servicio (default http://localhost:8000)
    RAG_API_TIMEOUT  timeout HTTP en segundos (default 60)
    RAG_TOP_K        nº de ontologías a recuperar (default 5)
    RAG_SCORE_THR    umbral de similitud para mantener matches (default 0.4)
    RAG_FAIL_FAST    si '1', lanza excepción cuando la API falla;
                     si '0' (default), devuelve string vacío y deja que
                     run_gpt_experiments.py haga fallback al legacy.

Uso programático:
    from rag_backend import RAGAnnotationClient, retrieve_context
    client = RAGAnnotationClient()
    if client.is_available():
        context = client.retrieve_context(sample_text, db_name="FANTOM5")

Diagnóstico desde CLI:
    python scripts/rag_backend.py --health
    python scripts/rag_backend.py --query "enhancer cell line gene"
    python scripts/rag_backend.py --db FANTOM5 --top-k 3
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None   # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── Configuración por entorno ──────────────────────────────────────
DEFAULT_API_URL = os.environ.get("RAG_API_URL", "http://localhost:8000")
DEFAULT_TIMEOUT = float(os.environ.get("RAG_API_TIMEOUT", "60"))
DEFAULT_TOP_K = int(os.environ.get("RAG_TOP_K", "5"))
DEFAULT_SCORE_THR = float(os.environ.get("RAG_SCORE_THR", "0.4"))
FAIL_FAST = os.environ.get("RAG_FAIL_FAST", "0") == "1"
DEFAULT_MAX_CHARS = int(os.environ.get("RAG_MAX_CHARS", "5000"))


@dataclass
class RAGResult:
    """Resultado normalizado del pipeline RAG (para serialización JSON
    o conversión a string-context para el prompt)."""
    api_url: str
    available: bool
    ontologies: list[dict[str, Any]] = field(default_factory=list)
    mappings: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    relations: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None

    def to_prompt_context(self, max_chars: int = DEFAULT_MAX_CHARS) -> str:
        """Renderiza el resultado como bloque de texto Turtle-like que
        pueda inyectarse en el placeholder ``{ontology_fragments}`` del
        prompt de E3.

        El formato emula la estructura que el modelo ya está acostumbrado
        a recibir en el RAG legacy: secciones ``# === <SCHEMA> ===`` con
        triples Turtle. El nuevo backend nos da metadata (label, IRI,
        score) que serializamos en pseudo-Turtle para que el modelo la
        procese sin cambiar el resto del prompt.
        """
        if not self.available:
            return f"# [RAG backend no disponible: {self.error or 'desconocido'}]"

        parts: list[str] = []

        # ─── Bloque 1: ontologías recomendadas ───────────────────────
        if self.ontologies:
            parts.append("# === RECOMMENDED ONTOLOGIES (semantic search) ===")
            for o in self.ontologies[:DEFAULT_TOP_K]:
                onto_id = o.get("ontologyId") or o.get("id") or "?"
                fname = o.get("filename", "")
                score = o.get("score")
                score_str = f"{score:.3f}" if isinstance(score, (int, float)) else "?"
                parts.append(
                    f"#   • ontology={onto_id}  file={fname}  score={score_str}"
                )

        # ─── Bloque 2: mapeo entidades (columnas) → clases ───────────
        if self.mappings:
            parts.append("")
            parts.append("# === COLUMN → ONTOLOGY CLASS MAPPINGS ===")
            for entity, matches in self.mappings.items():
                if not matches:
                    continue
                parts.append(f"# Column '{entity}':")
                for m in matches:
                    cls = m.get("class", {})
                    iri = cls.get("iri", "?")
                    labels = cls.get("label") or []
                    label = (labels[0] if labels else "")
                    score = m.get("score")
                    score_str = f"{score:.3f}" if isinstance(score, (int, float)) else "?"
                    parts.append(
                        f"#   - <{iri}> rdfs:label \"{label}\" ; "
                        f"# score={score_str}"
                    )

        # ─── Bloque 3: relaciones (object/data properties) ───────────
        if self.relations:
            parts.append("")
            parts.append("# === RELATION → ONTOLOGY PROPERTY MAPPINGS ===")
            for rel in self.relations[:20]:
                raw = rel.get("raw_relation", "")
                matches = rel.get("matches") or []
                if not matches:
                    continue
                parts.append(f"# Relation '{raw}':")
                for m in matches:
                    prop = m.get("property", {})
                    iri = prop.get("iri", "?")
                    label = prop.get("label", "")
                    score = m.get("score")
                    score_str = f"{score:.3f}" if isinstance(score, (int, float)) else "?"
                    parts.append(
                        f"#   - <{iri}> rdfs:label \"{label}\" ; "
                        f"# score={score_str}"
                    )

        text = "\n".join(parts)
        if not text.strip():
            return "# [RAG backend devolvió 0 matches sobre el corpus indexado]"

        if len(text) > max_chars:
            text = text[:max_chars] + "\n# [truncado por límite de contexto]"
        return text


class RAGBackendError(Exception):
    """Cualquier error de comunicación con la API RAG."""


class RAGAnnotationClient:
    """Wrapper HTTP del API RAGannotationAPI.

    Métodos:
      · is_available()         → bool, comprueba el endpoint /docs
      · similar_ontologies(...)
      · similar_entities(...)
      · similar_relations(...)
      · retrieve_context(...)  → string para inyectar en el prompt
    """

    def __init__(self,
                 api_url: str | None = None,
                 timeout: float | None = None,
                 top_k: int | None = None,
                 score_threshold: float | None = None) -> None:
        self.api_url = (api_url or DEFAULT_API_URL).rstrip("/")
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.top_k = top_k or DEFAULT_TOP_K
        self.score_threshold = score_threshold or DEFAULT_SCORE_THR

    # ─── Health check ───────────────────────────────────────────────
    def is_available(self) -> bool:
        """Comprueba que la API responde. Tolera el redirect a /docs."""
        if requests is None:
            return False
        try:
            # FastAPI por defecto sirve docs_url="/" en main.py de RAGannot.
            resp = requests.get(self.api_url + "/", timeout=min(self.timeout, 5))
            return resp.status_code in (200, 307, 308)
        except Exception:                                           # noqa: BLE001
            return False

    # ─── Endpoint: similar-ontologies ───────────────────────────────
    def similar_ontologies(self,
                            description_text: str,
                            top_k: int | None = None,
                            blacklist: list[str] | None = None
                            ) -> list[dict[str, Any]]:
        params = {
            "description_text": description_text,
            "top_k": top_k or self.top_k,
        }
        if blacklist:
            params["blacklist"] = ",".join(blacklist)
        data = self._get("/ontology/similar-ontologies", params=params)
        return data.get("results", [])

    # ─── Endpoint: similar-entities ─────────────────────────────────
    def similar_entities(self,
                          description_text: str,
                          ontology_ids: list[str],
                          top_class_per_entity: int = 1,
                          score_threshold: float | None = None,
                          context: bool = False
                          ) -> dict[str, Any]:
        params = {
            "description_text":      description_text,
            "ontology_ids":          ",".join(ontology_ids),
            "top_class_per_entity":  top_class_per_entity,
            "score_threshold":       score_threshold or self.score_threshold,
            "context":               str(context).lower(),
        }
        return self._get("/ontology/similar-entities", params=params)

    # ─── Endpoint: similar-relations ────────────────────────────────
    def similar_relations(self,
                           description_text: str,
                           ontology_ids: list[str],
                           top_property_per_relation: int = 1,
                           score_threshold: float | None = None
                           ) -> dict[str, Any]:
        params = {
            "description_text":          description_text,
            "ontology_ids":              ",".join(ontology_ids),
            "top_property_per_relation": top_property_per_relation,
            "score_threshold":           score_threshold or self.score_threshold,
        }
        return self._get("/ontology/similar-relations", params=params)

    # ─── Pipeline orquestado: contexto para el prompt E3 ────────────
    def retrieve_context(self,
                          sample_text: str,
                          db_name: str | None = None,
                          top_k: int | None = None,
                          score_threshold: float | None = None
                          ) -> RAGResult:
        """Ejecuta el pipeline completo: recomendar ontologías → mapear
        entidades → mapear relaciones, y devuelve un RAGResult.

        sample_text es el contenido del CSV/sample (cabecera + filas).
        db_name es opcional, solo se usa para enriquecer el contexto.
        """
        result = RAGResult(api_url=self.api_url, available=False)

        if not self.is_available():
            result.error = f"API no disponible en {self.api_url}"
            return result

        try:
            # Paso 1: recomendar las ontologías más cercanas al sample
            ontos = self.similar_ontologies(
                description_text=sample_text,
                top_k=top_k or self.top_k,
            )
            result.ontologies = ontos
            if not ontos:
                result.available = True
                result.error = "Sin ontologías indexadas que coincidan"
                return result

            # Paso 2: mapear las entidades (cabeceras de columna) a clases
            ontology_ids = [o["ontologyId"] for o in ontos
                             if o.get("ontologyId")]
            if ontology_ids:
                entities_text = self._extract_columns_as_entities(sample_text)
                if entities_text:
                    ent_resp = self.similar_entities(
                        description_text=entities_text,
                        ontology_ids=ontology_ids,
                        top_class_per_entity=2,
                        score_threshold=score_threshold or self.score_threshold,
                        context=True,
                    )
                    # Mergear los mappings de todas las ontologías
                    merged: dict[str, list] = {}
                    for o in ent_resp.get("ontologies", []):
                        for ent, matches in (o.get("mapping") or {}).items():
                            merged.setdefault(ent, []).extend(matches)
                    result.mappings = merged

            # Paso 3 (opcional): relaciones — saltado por defecto porque
            # los samples CSV no contienen relaciones explícitas (sí que
            # tienen columnas pero la inferencia de relaciones es ruidosa)
            result.relations = []

            result.available = True
            return result

        except RAGBackendError as e:
            result.error = str(e)
            if FAIL_FAST:
                raise
            return result
        except Exception as e:                                      # noqa: BLE001
            result.error = f"{type(e).__name__}: {e}"
            if FAIL_FAST:
                raise RAGBackendError(result.error) from e
            return result

    # ─── Helpers privados ───────────────────────────────────────────
    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        """GET con manejo uniforme de errores."""
        if requests is None:
            raise RAGBackendError("paquete 'requests' no instalado")
        url = self.api_url + path
        try:
            resp = requests.get(url, params=params, timeout=self.timeout)
        except requests.exceptions.ConnectionError as e:
            raise RAGBackendError(f"No se pudo conectar a {url}") from e
        except requests.exceptions.Timeout as e:
            raise RAGBackendError(
                f"Timeout ({self.timeout}s) en {url}") from e
        if resp.status_code >= 400:
            raise RAGBackendError(
                f"HTTP {resp.status_code} en {url}: "
                f"{resp.text[:200]}")
        try:
            return resp.json()
        except ValueError as e:
            raise RAGBackendError(
                f"Respuesta no-JSON de {url}: {resp.text[:200]}") from e

    @staticmethod
    def _extract_columns_as_entities(sample_text: str) -> str:
        """De un sample TSV/CSV extrae sólo la cabecera (primera línea
        no vacía) y la formatea como 'col1, col2, col3' para alimentar
        /similar-entities."""
        for line in sample_text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            # Detectar TSV / CSV
            sep = "\t" if "\t" in stripped else ","
            cols = [c.strip() for c in stripped.split(sep)
                     if c.strip() and c.strip() != "-"]
            return ", ".join(cols)
        return ""


# ─── API funcional simple (compatible con la firma del legacy) ─────
def retrieve_context(sample_text: str,
                      db_name: str | None = None,
                      top_k: int | None = None,
                      score_threshold: float | None = None,
                      max_chars: int = DEFAULT_MAX_CHARS,
                      api_url: str | None = None) -> str:
    """Función orquestadora con la misma firma que `get_rag_fragments`
    del legacy. Devuelve un string listo para inyectar en el prompt o
    cadena vacía si la API falla y FAIL_FAST=0.

    Los tres parámetros principales (top_k, score_threshold, max_chars)
    se exponen para permitir el experimento de calibración del §10.7.7
    sin tocar el código de run_gpt_experiments.py."""
    client = RAGAnnotationClient(
        api_url=api_url,
        top_k=top_k,
        score_threshold=score_threshold,
    )
    rag_result = client.retrieve_context(
        sample_text, db_name=db_name,
        top_k=top_k,
        score_threshold=score_threshold,
    )
    return rag_result.to_prompt_context(max_chars=max_chars)


# ─── CLI para diagnóstico rápido ────────────────────────────────────
def _main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--api-url",  default=DEFAULT_API_URL,
                    help=f"URL del servicio (default: {DEFAULT_API_URL})")
    ap.add_argument("--health",   action="store_true",
                    help="Solo comprobar disponibilidad de la API")
    ap.add_argument("--query",    type=str, default=None,
                    help="Texto libre a usar como sample")
    ap.add_argument("--db",       type=str, default=None,
                    help="Nombre de BBDD (FANTOM5, dbSUPER…) para "
                         "leer su sample del proyecto")
    ap.add_argument("--top-k",    type=int, default=DEFAULT_TOP_K)
    ap.add_argument("--score-thr", type=float, default=DEFAULT_SCORE_THR)
    ap.add_argument("--json",     action="store_true",
                    help="Mostrar el resultado JSON crudo en lugar del "
                         "contexto Turtle-like")
    args = ap.parse_args()

    client = RAGAnnotationClient(
        api_url=args.api_url,
        top_k=args.top_k,
        score_threshold=args.score_thr,
    )

    if args.health:
        ok = client.is_available()
        print(f"API @ {client.api_url}: "
              f"{'✅ disponible' if ok else '❌ no responde'}")
        return 0 if ok else 1

    # Determinar el texto de entrada
    if args.query:
        sample_text = args.query
    elif args.db:
        sample_path = (PROJECT_ROOT / "data" / "samples"
                       / f"{args.db}_sample_prompt.txt")
        if not sample_path.exists():
            print(f"❌ No existe sample en {sample_path}", file=sys.stderr)
            return 1
        sample_text = sample_path.read_text(encoding="utf-8")
    else:
        ap.error("Indica --health, --query <texto> o --db <BBDD>")

    rag_result = client.retrieve_context(sample_text, db_name=args.db)

    if args.json:
        print(json.dumps({
            "api_url":      rag_result.api_url,
            "available":    rag_result.available,
            "error":        rag_result.error,
            "ontologies":   rag_result.ontologies,
            "mappings":     rag_result.mappings,
            "relations":    rag_result.relations,
        }, indent=2, ensure_ascii=False))
    else:
        print(rag_result.to_prompt_context())
    return 0 if rag_result.available else 1


if __name__ == "__main__":
    raise SystemExit(_main())
