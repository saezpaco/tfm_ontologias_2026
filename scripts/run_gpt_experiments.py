#!/usr/bin/env python3
"""
run_gpt_experiments.py
Script dedicado para lanzar experimentos de generación de ontologías con GPT (OpenAI API).

Diseñado para ser el punto de entrada principal para las pruebas contra GPT-4o y GPT-4o-mini.

CONFIGURACIÓN DE API KEY (elegir una opción):
  - Variable de entorno:  export OPENAI_API_KEY="sk-..."
  - Argumento CLI:        python run_gpt_experiments.py --api-key "sk-..."
  - Archivo .env en TFM/ (ver instrucciones en --help)

EXPERIMENTOS DISPONIBLES:
  E1 - Zero-shot:              Generación directa desde muestra de datos
  E2 - Vocabulario controlado: Con vocabulario cisreg como contexto
  E3 - RAG (ontología cisreg): Con fragmentos de ontología de referencia

USO RÁPIDO:
  # Prueba rápida (1 BD, 1 run, muestra el prompt sin llamar a la API):
  python run_gpt_experiments.py --dry-run

  # Prueba real con gpt-4o-mini (barato) en dbSUPER, experimento E1:
  python run_gpt_experiments.py --model gpt-4o-mini --experiment E1 --db dbSUPER

  # Todos los experimentos en todas las BDs con gpt-4o:
  python run_gpt_experiments.py --model gpt-4o --experiment all --db all --n-runs 3
"""

import sys
import os
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# ─── Añadir scripts/ al path ─────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from config import (DATABASES, SCHEMAS, SCHEMA_EXAMPLES, LLM_MODELS,
                    GENERATION_PARAMS, EXPERIMENTS, PATHS, N_REPETITIONS)

# ─── Modelos GPT disponibles ──────────────────────────────────────────────────
GPT_MODELS = {k: v for k, v in LLM_MODELS.items() if v.get("provider") == "openai"}

# ─── Templates de prompts ─────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert ontologist specializing in biological knowledge graphs and semantic web technologies.
Your expertise includes OWL 2, RDF, SPARQL, and biological domain ontologies (SO, GO, BioLink Model, SKOS).
Your task is to analyze biological database samples and generate formal OWL ontology schemas in Turtle serialization.

Domain context: The databases contain information about cis-regulatory modules (CRM), specifically enhancer sequences
that modulate the transcription rate of their target genes in the human genome.
These sequences are characterized by their genomic coordinates, experimental evidence, cell line activity,
target genes, associated diseases, and interacting transcription factors."""

USER_PROMPT_E1 = """Analyze the following biological database sample and generate a formal OWL ontology schema in Turtle format.

DATABASE: {db_name}
DESCRIPTION: {db_description}

DATABASE SAMPLE (TSV format, '-' means missing value):
{db_sample}

Think step by step:
1. Identify the main concepts/classes present in the data
2. Identify the relationships (object properties) and attributes (datatype properties)
3. Map concepts to standard biological ontologies where possible (SO, GO, BioLink)
4. Generate the formal Turtle schema

Requirements for the output schema:
- Use these standard prefixes: rdf:, rdfs:, owl:, skos:, xsd:, obo: (http://purl.obolibrary.org/obo/)
- Add skos:prefLabel and skos:definition to all classes and properties
- Include at least: class for CRM/enhancer, genomic coordinate properties, evidence properties
- Use owl:Class for all main concepts
- Use owl:ObjectProperty for relationships and owl:DatatypeProperty for literals
- Include skos:exactMatch or skos:closeMatch mappings to standard biological ontologies where appropriate

Output ONLY valid Turtle code. No explanations, no markdown code blocks."""

USER_PROMPT_E2 = """Analyze the following biological database sample and generate a formal OWL ontology schema in Turtle format.
Use the provided controlled vocabulary to name and align your ontology terms.

DATABASE: {db_name}
DESCRIPTION: {db_description}

DATABASE SAMPLE (TSV format, '-' means missing value):
{db_sample}

CONTROLLED VOCABULARY (cisreg terms):
{vocab_terms}

Think step by step:
1. Identify the main concepts/classes in the data
2. Map them to the controlled vocabulary terms above
3. Identify relationships and attributes, reusing vocabulary terms
4. Generate the formal Turtle schema

Requirements:
- Prefer vocabulary terms for class and property names where applicable
- Use standard prefixes: rdf:, rdfs:, owl:, skos:, xsd:, obo:
- Include skos:prefLabel, skos:definition, and skos:exactMatch/closeMatch mappings
- Include both owl:Class and owl:ObjectProperty/owl:DatatypeProperty declarations

Output ONLY valid Turtle code. No explanations, no markdown code blocks."""

USER_PROMPT_E3 = """Analyze the following biological database sample and generate a formal OWL ontology schema in Turtle format.
Align your schema as closely as possible with the cisreg reference ontology fragments provided below.

DATABASE: {db_name}
DESCRIPTION: {db_description}

DATABASE SAMPLE (TSV format, '-' means missing value):
{db_sample}

CISREG REFERENCE ONTOLOGY (most relevant fragments in Turtle):
{ontology_fragments}

Think step by step:
1. Identify the main concepts/classes in the data
2. Find the corresponding classes and properties in the cisreg reference ontology
3. Reuse cisreg URIs where semantically appropriate
4. Add new terms only where cisreg does not cover the concept

Requirements:
- Reuse cisreg classes and properties where semantically appropriate
- Add explicit skos:exactMatch or skos:closeMatch to cisreg URIs for aligned terms
- New classes/properties only where cisreg doesn't cover the concept

CRITICAL — PREFIX DECLARATIONS (MANDATORY):
The output MUST start with the following @prefix declarations BEFORE any
other statement. If your schema uses ANY prefix below, it MUST be declared
at the top of the file. Do NOT use a prefix that you have not declared.

@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix dc:      <http://purl.org/dc/terms/> .
@prefix obo:     <http://purl.obolibrary.org/obo/> .
@prefix biolink: <https://w3id.org/biolink/vocab/> .
@prefix schema:  <http://schema.org/> .
@prefix sio:     <http://semanticscience.org/resource/> .

Plus any additional prefixes used by the cisreg reference ontology fragments
above (hcrm, crm2pgene, hgene, assembly, nuccore, pubmed, id_pubmed,
id_ncbigene, dbsuper, etc.) MUST also be declared with their full URIs at the
top of the document.

VERIFICATION: before producing the final output, scan your code and confirm
that EVERY ``prefix:localname`` you write has a matching ``@prefix prefix:``
declaration at the top. The Turtle file must parse with rdflib without
``Prefix not bound`` errors.

Output ONLY valid Turtle code. No explanations, no markdown code blocks."""


# ─── Funciones de carga ───────────────────────────────────────────────────────

def load_sample(db_name: str) -> str | None:
    """Carga la muestra de datos para el prompt."""
    sample_path = PATHS["samples"] / f"{db_name}_sample_prompt.txt"
    if sample_path.exists():
        return sample_path.read_text(encoding='utf-8')
    print(f"  ⚠️  Muestra no encontrada: {sample_path}")
    return None


def load_schema(schema_name: str) -> str | None:
    """Carga un esquema de referencia cisreg."""
    for base in [PATHS["samples"] / "schemas", PATHS.get("schemas", Path("/nonexistent"))]:
        path = base / (SCHEMAS.get(schema_name, "") or "")
        if path.exists():
            return path.read_text(encoding='utf-8')
    return None


def load_vocabulary() -> str:
    """Construye un vocabulario compacto desde los esquemas cisreg."""
    lines = []
    for schema_name in SCHEMAS.keys():
        text = load_schema(schema_name)
        if not text:
            continue
        for line in text.split('\n'):
            if 'skos:prefLabel' in line or 'skos:definition' in line:
                lines.append(line.strip())

    if not lines:
        return "# [Vocabulario no disponible - ver esquemas CRM]"

    # Deduplicar y limitar
    seen = set()
    unique = []
    for l in lines:
        if l not in seen:
            seen.add(l)
            unique.append(l)

    result = '\n'.join(unique[:80])
    return result


def get_rag_fragments(db_name: str) -> str:
    """Selecciona fragmentos relevantes de la ontología cisreg para el RAG."""
    selected = []
    priority = ["crm"]  # Base siempre

    # Heurística sobre el contenido de la muestra
    sample_text = (load_sample(db_name) or "").lower()
    if any(kw in sample_text for kw in ["gene", "hgnc", "target"]):
        priority.append("crm2gene")
    if any(kw in sample_text for kw in ["disease", "phen", "doid", "omim"]):
        priority.append("crm2phen")
    if any(kw in sample_text for kw in ["tf", "transcription factor", "uniprot"]):
        priority.append("crm2tfac")

    for schema_name in priority:
        text = load_schema(schema_name)
        if text:
            selected.append(f"# === {schema_name.upper()} SCHEMA ===\n{text}")

    result = "\n\n".join(selected) if selected else "# [Esquemas de referencia no disponibles]"
    # Limitar a ~5000 chars
    if len(result) > 5000:
        result = result[:5000] + "\n# [truncado por límite de contexto]"
    return result


# ─── Llamada a la API de OpenAI ───────────────────────────────────────────────

def call_gpt(model_name: str, system_prompt: str, user_prompt: str,
             params: dict, api_key: str) -> dict:
    """Llama a la API de OpenAI y devuelve el resultado."""
    try:
        import openai
    except ImportError:
        return {
            "success": False,
            "error": "Paquete 'openai' no instalado. Ejecuta: pip install openai"
        }

    client = openai.OpenAI(api_key=api_key)
    start = time.time()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=params.get("temperature", 0.1),
            top_p=params.get("top_p", 0.9),
            max_tokens=params.get("max_tokens", 4096),
            seed=params.get("seed", 42),
        )
        elapsed = round(time.time() - start, 2)
        content = response.choices[0].message.content or ""
        usage = response.usage

        return {
            "success": True,
            "content": content,
            "elapsed": elapsed,
            "model": model_name,
            "usage": {
                "prompt_tokens":     usage.prompt_tokens if usage else None,
                "completion_tokens": usage.completion_tokens if usage else None,
                "total_tokens":      usage.total_tokens if usage else None,
            },
            "finish_reason": response.choices[0].finish_reason,
        }

    except openai.AuthenticationError:
        return {"success": False, "error": "API Key inválida o sin permisos"}
    except openai.RateLimitError:
        return {"success": False, "error": "Rate limit alcanzado. Espera y reintenta."}
    except openai.APIError as e:
        return {"success": False, "error": f"Error API: {str(e)[:200]}"}
    except Exception as e:
        return {"success": False, "error": str(e)[:300]}


# ─── Extracción y validación de Turtle ───────────────────────────────────────

def extract_turtle(text: str) -> str:
    """Extrae el bloque Turtle válido de la respuesta del LLM."""
    stripped = text.strip()

    # Caso 1: respuesta directamente en Turtle
    if stripped.startswith('@prefix') or stripped.startswith('<'):
        return stripped

    # Caso 2: bloque de código markdown
    for marker in ['```turtle\n', '```ttl\n', '```rdf\n', '```\n']:
        if marker in text:
            parts = text.split(marker)
            if len(parts) > 1:
                candidate = parts[1].split('```')[0].strip()
                if candidate:
                    return candidate

    # Caso 3: buscar primer @prefix o <http en el texto
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('@prefix') or line.strip().startswith('<http'):
            turtle_lines = lines[i:]
            # Cortar en la última tripleta
            for j in range(len(turtle_lines) - 1, -1, -1):
                if turtle_lines[j].strip().endswith(' .') or turtle_lines[j].strip() == '.':
                    return '\n'.join(turtle_lines[:j+1]).strip()
            return '\n'.join(turtle_lines).strip()

    return text  # fallback: devolver todo


def validate_turtle(turtle_text: str) -> dict:
    """Valida la sintaxis Turtle con rdflib."""
    try:
        import rdflib
        g = rdflib.Graph()
        g.parse(data=turtle_text, format="turtle")
        classes = [str(s) for s, p, o in g if str(p) == str(rdflib.RDF.type)
                   and str(o) == str(rdflib.OWL.Class)]
        props = [str(s) for s, p, o in g if str(p) == str(rdflib.RDF.type)
                 and str(o) in [str(rdflib.OWL.ObjectProperty),
                                str(rdflib.OWL.DatatypeProperty)]]
        return {
            "valid": True,
            "n_triples": len(g),
            "n_classes": len(classes),
            "n_properties": len(props),
        }
    except ImportError:
        return {"valid": None, "note": "rdflib no instalado (pip install rdflib)"}
    except Exception as e:
        return {"valid": False, "error": str(e)[:300]}


# ─── Construcción de prompts ──────────────────────────────────────────────────

def build_prompt(experiment: str, db_name: str) -> tuple[str, str]:
    """Construye system + user prompt para el experimento dado."""
    db_config = DATABASES[db_name]
    sample = load_sample(db_name) or f"[Muestra de {db_name} no disponible]"

    if experiment == "E1":
        user = USER_PROMPT_E1.format(
            db_name=db_name,
            db_description=db_config["description"],
            db_sample=sample,
        )
    elif experiment == "E2":
        vocab = load_vocabulary()
        user = USER_PROMPT_E2.format(
            db_name=db_name,
            db_description=db_config["description"],
            db_sample=sample,
            vocab_terms=vocab,
        )
    elif experiment == "E3":
        rag = get_rag_fragments(db_name)
        user = USER_PROMPT_E3.format(
            db_name=db_name,
            db_description=db_config["description"],
            db_sample=sample,
            ontology_fragments=rag,
        )
    else:
        raise ValueError(f"Experimento desconocido: {experiment}")

    return SYSTEM_PROMPT, user


# ─── Ejecución de un experimento individual ───────────────────────────────────

def run_single(experiment: str, db_name: str, model_name: str,
               run_number: int, api_key: str, dry_run: bool = False) -> dict:
    """Ejecuta un único experimento y guarda los resultados."""
    exp_config = EXPERIMENTS[experiment]
    safe_model = model_name.replace(':', '_').replace('/', '_')
    output_dir = PATHS["results"] / experiment / db_name / safe_model
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  [{experiment}] {db_name} | {model_name} | run {run_number}")

    system_prompt, user_prompt = build_prompt(experiment, db_name)
    token_est = (len(system_prompt) + len(user_prompt)) // 4
    print(f"  Tokens estimados en prompt: ~{token_est:,}")

    # ── DRY RUN ──────────────────────────────────────────────────────────────
    if dry_run:
        print(f"  [DRY RUN] System ({len(system_prompt)} chars) | User ({len(user_prompt)} chars)")
        print(f"\n  System prompt (primeros 300 chars):\n  {system_prompt[:300]}")
        print(f"\n  User prompt (primeros 500 chars):\n  {user_prompt[:500]}")
        prompt_path = output_dir / f"prompt_dry_run{run_number}.txt"
        prompt_path.write_text(
            f"=== SYSTEM PROMPT ===\n{system_prompt}\n\n=== USER PROMPT ===\n{user_prompt}",
            encoding='utf-8'
        )
        print(f"\n  Prompt guardado: {prompt_path.name}")
        return {"dry_run": True, "token_estimate": token_est, "db": db_name,
                "experiment": experiment, "model": model_name}

    # ── LLAMADA REAL ──────────────────────────────────────────────────────────
    run_params = {**GENERATION_PARAMS, "seed": GENERATION_PARAMS["seed"] + run_number - 1}

    print(f"  🔄 Llamando a {model_name}...", end='', flush=True)
    result = call_gpt(model_name, system_prompt, user_prompt, run_params, api_key)

    if not result["success"]:
        print(f"\n  ❌ Error: {result['error']}")
        return {
            "experiment": experiment, "db_name": db_name, "model": model_name,
            "run": run_number, "success": False, "error": result["error"],
            "timestamp": datetime.now().isoformat(),
        }

    usage = result.get("usage", {})
    print(f" ✅ {result['elapsed']}s | "
          f"{usage.get('total_tokens', '?')} tokens | "
          f"{len(result['content'])} chars")

    # Extraer y validar Turtle
    turtle = extract_turtle(result["content"])
    validation = validate_turtle(turtle)

    if validation.get("valid") is True:
        print(f"  ✅ Turtle válido: {validation['n_triples']} tripletas, "
              f"{validation['n_classes']} clases, {validation['n_properties']} propiedades")
    elif validation.get("valid") is False:
        print(f"  ⚠️  Turtle inválido: {validation.get('error', '')[:100]}")
    else:
        print(f"  ℹ️  Validación pendiente (instala rdflib)")

    # Guardar ficheros de salida
    ttl_path  = output_dir / f"ontology_run{run_number}.ttl"
    raw_path  = output_dir / f"response_raw_run{run_number}.txt"
    meta_path = output_dir / f"metadata_run{run_number}.json"

    ttl_path.write_text(turtle, encoding='utf-8')
    raw_path.write_text(result["content"], encoding='utf-8')

    metadata = {
        "experiment": experiment,
        "experiment_name": exp_config["name"],
        "db_name": db_name,
        "model": model_name,
        "run": run_number,
        "timestamp": datetime.now().isoformat(),
        "success": True,
        "elapsed_seconds": result["elapsed"],
        "finish_reason": result.get("finish_reason"),
        "usage": usage,
        "prompt_tokens_estimate": token_est,
        "response_chars": len(result["content"]),
        "turtle_chars": len(turtle),
        "validation": validation,
        "output_files": {
            "turtle": str(ttl_path),
            "raw": str(raw_path),
        },
    }

    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

    print(f"  💾 {ttl_path.name} | {raw_path.name} | {meta_path.name}")
    return metadata


# ─── Ejecución de lote ────────────────────────────────────────────────────────

def run_batch(experiment: str, db_names: list[str], model_name: str,
              n_runs: int, api_key: str, dry_run: bool = False) -> list[dict]:
    """Ejecuta un experimento para múltiples BDs y repeticiones."""
    all_results = []

    print(f"\n{'='*65}")
    print(f"  EXPERIMENTO {experiment}: {EXPERIMENTS[experiment]['name']}")
    print(f"  Modelo: {model_name}")
    print(f"  BDs ({len(db_names)}): {', '.join(db_names)}")
    print(f"  Repeticiones: {n_runs}")
    print(f"{'='*65}")

    for db_name in db_names:
        db_results = []
        for run in range(1, n_runs + 1):
            res = run_single(experiment, db_name, model_name, run, api_key, dry_run)
            db_results.append(res)
            if not dry_run:
                time.sleep(1)  # pausa cortés entre llamadas

        if not dry_run:
            # Resumen por BD
            safe_model = model_name.replace(':', '_').replace('/', '_')
            out_dir = PATHS["results"] / experiment / db_name / safe_model
            summary = {
                "experiment": experiment,
                "db_name": db_name,
                "model": model_name,
                "n_runs": n_runs,
                "n_success": sum(1 for r in db_results if r.get("success")),
                "n_valid_turtle": sum(
                    1 for r in db_results
                    if r.get("validation", {}).get("valid") is True
                ),
                "avg_elapsed": (
                    sum(r.get("elapsed_seconds", 0) for r in db_results) / n_runs
                    if n_runs else 0
                ),
                "total_tokens": sum(
                    (r.get("usage", {}).get("total_tokens") or 0) for r in db_results
                ),
                "runs": db_results,
            }
            with open(out_dir / "summary.json", 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

        all_results.extend(db_results)

    return all_results


# ─── Main ─────────────────────────────────────────────────────────────────────

def resolve_api_key(args_key: str | None) -> str | None:
    """Resuelve la API key desde argumento > variable de entorno > .env."""
    if args_key:
        return args_key

    # Variable de entorno
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key

    # Archivo .env en la raíz del proyecto
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Experimentos de ontologías CRM con GPT (OpenAI API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Ver prompts sin consumir API (gratis):
  python run_gpt_experiments.py --dry-run

  # Prueba rápida: E1 en dbSUPER con gpt-4o-mini
  python run_gpt_experiments.py --model gpt-4o-mini --experiment E1 --db dbSUPER

  # Todos los experimentos en todas las BDs:
  python run_gpt_experiments.py --model gpt-4o --experiment all --db all --n-runs 3

  # Con API key explícita:
  python run_gpt_experiments.py --api-key "sk-..." --model gpt-4o-mini --experiment E1

  # O con variable de entorno:
  export OPENAI_API_KEY="sk-..."
  python run_gpt_experiments.py --model gpt-4o-mini --experiment E1

Configurar API key con archivo .env (en carpeta TFM/):
  echo 'OPENAI_API_KEY=sk-...' > TFM/.env
        """
    )
    parser.add_argument('--api-key',   type=str,  default=None,
                        help='OpenAI API key (alternativa a OPENAI_API_KEY env)')
    parser.add_argument('--model',     type=str,  default='gpt-4o-mini',
                        choices=list(GPT_MODELS.keys()),
                        help='Modelo GPT (default: gpt-4o-mini)')
    parser.add_argument('--experiment',type=str,  default='E1',
                        choices=list(EXPERIMENTS.keys()) + ['all'],
                        help='Experimento(s) a ejecutar (default: E1)')
    parser.add_argument('--db',        type=str,  default='dbSUPER',
                        choices=list(DATABASES.keys()) + ['all'],
                        help='Base(s) de datos (default: dbSUPER)')
    parser.add_argument('--n-runs',    type=int,  default=1,
                        help='Repeticiones por experimento/BD (default: 1)')
    parser.add_argument('--dry-run',   action='store_true',
                        help='Construir prompts sin llamar a la API')
    args = parser.parse_args()

    print("\n" + "="*65)
    print("  TFM - EXPERIMENTOS GPT: GENERACIÓN DE ONTOLOGÍAS CRM")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*65)

    # ── Selección de BDs ──────────────────────────────────────────────────────
    if args.db == 'all':
        db_names = [db for db in DATABASES.keys()
                    if (PATHS["samples"] / f"{db}_sample_prompt.txt").exists()]
    else:
        db_names = [args.db]

    if not db_names:
        print("  ❌ No se encontraron muestras. Ejecuta primero: python 02_sample_databases.py")
        sys.exit(1)

    # ── Selección de experimentos ─────────────────────────────────────────────
    experiments = list(EXPERIMENTS.keys()) if args.experiment == 'all' else [args.experiment]

    # ── API Key ───────────────────────────────────────────────────────────────
    api_key = None
    if not args.dry_run:
        api_key = resolve_api_key(args.api_key)
        if not api_key:
            print("  ❌ API Key no encontrada.")
            print("     Opciones:")
            print("     1. export OPENAI_API_KEY='sk-...'")
            print("     2. python run_gpt_experiments.py --api-key 'sk-...'")
            print("     3. Crear TFM/.env con: OPENAI_API_KEY=sk-...")
            sys.exit(1)
        print(f"  ✅ API Key configurada (sk-...{api_key[-4:]})")
    else:
        print("  ⚠️  MODO DRY-RUN: no se consume API")

    print(f"  Modelo:          {args.model}")
    print(f"  Experimentos:    {experiments}")
    print(f"  Bases de datos:  {db_names}")
    print(f"  Repeticiones:    {args.n_runs}")
    print(f"  Resultados en:   {PATHS['results']}")

    # ── Ejecutar ──────────────────────────────────────────────────────────────
    all_results = []
    for exp in experiments:
        results = run_batch(
            experiment=exp,
            db_names=db_names,
            model_name=args.model,
            n_runs=args.n_runs,
            api_key=api_key,
            dry_run=args.dry_run,
        )
        all_results.extend(results)

    # ── Resumen global ────────────────────────────────────────────────────────
    if not args.dry_run:
        n_success = sum(1 for r in all_results if r.get("success"))
        n_valid   = sum(1 for r in all_results
                        if r.get("validation", {}).get("valid") is True)
        total_tok = sum((r.get("usage", {}).get("total_tokens") or 0)
                        for r in all_results)

        print(f"\n{'='*65}")
        print("  RESUMEN FINAL")
        print(f"{'='*65}")
        print(f"  Experimentos lanzados: {len(all_results)}")
        print(f"  Llamadas exitosas:     {n_success}/{len(all_results)}")
        print(f"  Ontologías Turtle válidas: {n_valid}/{len(all_results)}")
        print(f"  Tokens totales usados: {total_tok:,}")
        print(f"\n  📂 Resultados en: {PATHS['results']}")
        print(f"  👉 Siguiente paso: python 05_evaluate_results.py")
    else:
        print(f"\n  [DRY RUN completado] {len(all_results)} prompts generados.")
        print(f"  Prompts guardados en: {PATHS['results']}")
        print(f"\n  Para ejecutar de verdad, añade tu API key y quita --dry-run:")
        print(f"  python run_gpt_experiments.py --model gpt-4o-mini --experiment E1 --db dbSUPER")


if __name__ == "__main__":
    main()
