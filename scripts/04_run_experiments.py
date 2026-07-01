#!/usr/bin/env python3
"""
04_run_experiments.py
Script principal de experimentación: genera ontologías con LLMs para cada BD y experimento.

Experimentos:
  E1 - Base: generación directa desde datos en bruto (zero-shot)
  E2 - Vocabulario: generación con vocabulario controlado cisreg
  E3 - RAG: generación aumentada con fragmentos de la ontología cisreg

Salida:
  results/{experiment}/{db_name}/{model_name}/
    ├── ontology_run{N}.ttl    # Ontología generada (Turtle)
    ├── metadata_run{N}.json   # Metadatos de la generación
    └── summary.json           # Resumen de todas las repeticiones

Uso:
    python 04_run_experiments.py --experiment E1 --model llama3.1:8b --db dbSUPER
    python 04_run_experiments.py --experiment E1 --model llama3.1:8b  # Todas las BDs
    python 04_run_experiments.py --experiment all --model llama3.1:8b  # Todos los experimentos
    python 04_run_experiments.py --dry-run  # Solo muestra los prompts, no llama al LLM
"""

import sys
import os
import json
import time
import argparse
import re
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from config import (DATABASES, SCHEMAS, SCHEMA_EXAMPLES, LLM_MODELS,
                    GENERATION_PARAMS, EXPERIMENTS, PATHS, N_REPETITIONS)


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
3. Map concepts to standard biological ontologies where possible
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

CONTROLLED VOCABULARY (classes):
{vocab_classes}

CONTROLLED VOCABULARY (properties):
{vocab_properties}

Think step by step:
1. Identify the main concepts/classes in the data
2. Map them to the controlled vocabulary terms above
3. Identify relationships and attributes
4. Generate the formal Turtle schema using vocabulary terms

Requirements:
- Use the controlled vocabulary terms for class and property names where applicable
- Use standard prefixes: rdf:, rdfs:, owl:, skos:, xsd:, obo:
- Include skos:prefLabel, skos:definition, and skos:exactMatch/closeMatch mappings
- Include both owl:Class and owl:ObjectProperty/owl:DatatypeProperty declarations

Output ONLY valid Turtle code. No explanations, no markdown code blocks."""

USER_PROMPT_E3 = """Analyze the following biological database sample and generate a formal OWL ontology schema in Turtle format.
Align your schema with the cisreg reference ontology fragments provided below.

DATABASE: {db_name}
DESCRIPTION: {db_description}

DATABASE SAMPLE (TSV format, '-' means missing value):
{db_sample}

CISREG REFERENCE ONTOLOGY FRAGMENTS (most relevant to this database):
{ontology_fragments}

Think step by step:
1. Identify the main concepts/classes in the data
2. Find corresponding classes in the cisreg reference ontology
3. Identify relationships and map to cisreg properties where possible
4. Generate the Turtle schema aligned with cisreg

Requirements:
- Reuse cisreg classes and properties where semantically appropriate
- Add explicit skos:exactMatch/closeMatch to cisreg URIs for aligned terms
- Use all standard prefixes from the cisreg ontology (hcrm:, obo:, biolink:, etc.)
- Include new classes/properties only where cisreg doesn't cover the concept

Output ONLY valid Turtle code. No explanations, no markdown code blocks."""


# ─── Funciones de carga de datos ─────────────────────────────────────────────

# ── Overrides para la rejilla muestreo×tamaño (Fase 1 del protocolo) ──────────
# Permiten que este runner (Ollama: Llama/Qwen) consuma una celda concreta de
# la rejilla y escriba los resultados en una carpeta trazable {modelo}_{sufijo}.
# Sin los flags --samples-dir/--results-suffix el comportamiento es el original.
SAMPLES_DIR_OVERRIDE: Optional[Path] = None
RESULTS_SUFFIX: str = ""


def _samples_dir() -> Path:
    return SAMPLES_DIR_OVERRIDE if SAMPLES_DIR_OVERRIDE else PATHS["samples"]


def _model_folder(model_name: str) -> str:
    # Sin separador, igual que run_gpt_experiments / run_ontogenix (p. ej.
    # llama3.1_8bA_head_N25), para que el post-procesado y already_done coincidan.
    base = model_name.replace(':', '_')
    return f"{base}{RESULTS_SUFFIX}" if RESULTS_SUFFIX else base


def load_sample_text(db_name: str) -> Optional[str]:
    """Carga el texto de la muestra de datos para el prompt."""
    sample_path = _samples_dir() / f"{db_name}_sample_prompt.txt"
    if not sample_path.exists():
        # Generar muestra on-the-fly si no existe
        print(f"  ⚠️  Muestra no encontrada: {sample_path}")
        print(f"     Ejecuta primero: python 02_sample_databases.py --db {db_name}")
        return None
    return sample_path.read_text(encoding='utf-8')


def load_schema(schema_name: str) -> Optional[str]:
    """Carga un esquema de referencia cisreg."""
    schema_path = PATHS["samples"] / "schemas" / SCHEMAS.get(schema_name, "")
    if schema_path.exists():
        return schema_path.read_text(encoding='utf-8')
    # Intentar directamente desde la fuente
    schema_path2 = PATHS["schemas"] / SCHEMAS.get(schema_name, "")
    if schema_path2.exists():
        return schema_path2.read_text(encoding='utf-8')
    return None


def load_vocabulary() -> tuple:
    """Carga el vocabulario controlado de cisreg (desde esquemas)."""
    # Extraer términos de los esquemas como vocabulario simplificado
    vocab_classes = []
    vocab_properties = []

    for schema_name in SCHEMAS.keys():
        schema_text = load_schema(schema_name)
        if not schema_text:
            continue

        lines = schema_text.split('\n')
        for line in lines:
            if 'owl:Class' in line and 'rdf:type' not in line:
                continue
            if 'skos:prefLabel' in line:
                label = line.strip()
                if 'ObjectProperty\|DatatypeProperty' in schema_text:
                    vocab_properties.append(label)
                else:
                    vocab_classes.append(label)

    # Si no encontramos vocabulario, usar un resumen básico del esquema crm
    crm_schema = load_schema("crm")
    if crm_schema:
        # Extraer las líneas con prefLabels
        pref_labels = [l.strip() for l in crm_schema.split('\n')
                       if 'skos:prefLabel' in l]
        vocab_classes = pref_labels[:20]

    return (
        '\n'.join(vocab_classes) if vocab_classes else "# [Ver esquema crm.txt]",
        '\n'.join(vocab_properties) if vocab_properties else "# [Ver esquemas crm2*.txt]"
    )


def get_rag_fragments(db_name: str, n_fragments: int = 5) -> str:
    """
    Recupera fragmentos relevantes de la ontología cisreg para el RAG.
    Versión simplificada: devuelve fragmentos del esquema crm base.
    Para RAG completo, usar chromadb con embeddings.
    """
    # Cargar todos los esquemas disponibles
    all_schemas = []
    for schema_name in ["crm", "crm2gene", "crm2phen", "crm2tfac"]:
        schema_text = load_schema(schema_name)
        if schema_text:
            all_schemas.append(f"# Schema: {schema_name}\n{schema_text}")

    if not all_schemas:
        return "# [Esquemas de referencia no disponibles]"

    # Heurística simple: para cada BD, cargar el esquema más relevante
    # Según el contenido de la BD
    db_config = DATABASES.get(db_name, {})
    db_desc = db_config.get("description", "").lower()

    priority_schemas = ["crm"]  # Siempre incluir el schema base

    # Añadir schemas según el contenido de la BD
    sample_path = _samples_dir() / f"{db_name}_sample_prompt.txt"
    sample_text = ""
    if sample_path.exists():
        sample_text = sample_path.read_text(encoding='utf-8').lower()

    if any(kw in sample_text for kw in ["gene", "hgnc", "target"]):
        priority_schemas.append("crm2gene")
    if any(kw in sample_text for kw in ["disease", "phen", "doid", "omim", "mesh"]):
        priority_schemas.append("crm2phen")
    if any(kw in sample_text for kw in ["tf", "tfac", "transcription factor", "uniprot"]):
        priority_schemas.append("crm2tfac")

    # Combinar los esquemas prioritarios
    selected_schemas = []
    for schema_name in priority_schemas:
        schema_text = load_schema(schema_name)
        if schema_text:
            selected_schemas.append(f"# === Schema: {schema_name} ===\n{schema_text}")

    result = "\n\n".join(selected_schemas)

    # Limitar tamaño
    max_chars = 4000
    if len(result) > max_chars:
        result = result[:max_chars] + "\n# [fragmento truncado por límite de contexto]"

    return result


# ─── Interfaz LLM ─────────────────────────────────────────────────────────────

def call_llm(model_name: str, system_prompt: str, user_prompt: str,
             params: dict = None) -> dict:
    """
    Llama al LLM especificado y devuelve la respuesta.
    Soporta Ollama y OpenAI API.
    """
    params = params or GENERATION_PARAMS
    model_config = LLM_MODELS.get(model_name, {})
    provider = model_config.get("provider", "ollama")

    start = time.time()

    if provider == "ollama":
        return _call_ollama(model_name, system_prompt, user_prompt, params,
                            model_config.get("base_url", "http://localhost:11434"),
                            start)
    elif provider == "openai":
        return _call_openai(model_name, system_prompt, user_prompt, params, start)
    else:
        return {"success": False, "error": f"Proveedor desconocido: {provider}"}


def _call_ollama(model_name, system_prompt, user_prompt, params, base_url, start):
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "options": {
            "temperature": params.get("temperature", 0.1),
            "top_p": params.get("top_p", 0.9),
            "num_predict": params.get("max_tokens", 4096),
            "seed": params.get("seed", 42),
        },
        "stream": False,
    }
    try:
        response = requests.post(f"{base_url}/api/chat", json=payload, timeout=300)
        elapsed = time.time() - start
        if response.status_code == 200:
            data = response.json()
            content = data.get("message", {}).get("content", "")
            return {"success": True, "content": content, "elapsed": round(elapsed, 2),
                    "model": model_name}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}",
                    "elapsed": round(time.time() - start, 2)}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Ollama no disponible (¿está en ejecución?)"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout (>300s)"}


def _call_openai(model_name, system_prompt, user_prompt, params, start):
    try:
        import openai
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {"success": False, "error": "OPENAI_API_KEY no configurada"}
        client = openai.OpenAI(api_key=api_key)
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
        elapsed = time.time() - start
        content = response.choices[0].message.content
        return {
            "success": True, "content": content,
            "elapsed": round(elapsed, 2),
            "tokens_used": response.usage.total_tokens if response.usage else None,
            "model": model_name,
        }
    except ImportError:
        return {"success": False, "error": "openai package no instalado"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─── Post-procesamiento de ontologías ─────────────────────────────────────────

def extract_turtle(text: str) -> str:
    """
    Extrae el código Turtle de la respuesta del LLM.
    Maneja casos donde el LLM añade texto o bloques markdown.
    """
    # Caso 1: Solo Turtle (empieza con @prefix o < )
    stripped = text.strip()
    if stripped.startswith('@prefix') or stripped.startswith('<'):
        return stripped

    # Caso 2: Bloque de código markdown
    for marker in ['```turtle\n', '```ttl\n', '```rdf\n', '```\n']:
        if marker in text:
            parts = text.split(marker)
            if len(parts) > 1:
                candidate = parts[1].split('```')[0].strip()
                if candidate:
                    return candidate

    # Caso 3: Buscar desde la primera línea con @prefix
    lines = text.split('\n')
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('@prefix') or line.strip().startswith('<http'):
            start_idx = i
            break

    if start_idx is not None:
        turtle_lines = lines[start_idx:]
        # Cortar al final del Turtle (última línea con ' .')
        end_idx = len(turtle_lines)
        for i in range(len(turtle_lines) - 1, -1, -1):
            if turtle_lines[i].strip().endswith(' .') or turtle_lines[i].strip() == '.':
                end_idx = i + 1
                break
        return '\n'.join(turtle_lines[:end_idx]).strip()

    # No se encontró Turtle: devolver el texto completo
    return text


def validate_turtle(turtle_text: str) -> dict:
    """Valida la sintaxis Turtle con rdflib."""
    try:
        import rdflib
        g = rdflib.Graph()
        g.parse(data=turtle_text, format="turtle")
        return {
            "valid": True,
            "n_triples": len(g),
            "classes": [],
            "properties": [],
        }
    except ImportError:
        return {"valid": None, "error": "rdflib no instalado"}
    except Exception as e:
        return {"valid": False, "error": str(e)[:300]}


# ─── Ejecución de experimentos ────────────────────────────────────────────────

def build_prompt(experiment: str, db_name: str) -> tuple:
    """Construye el prompt del sistema y usuario para un experimento."""
    db_config = DATABASES[db_name]
    sample_text = load_sample_text(db_name) or f"[Muestra de {db_name} no disponible]"

    if experiment == "E1":
        user_prompt = USER_PROMPT_E1.format(
            db_name=db_name,
            db_description=db_config["description"],
            db_sample=sample_text,
        )
    elif experiment == "E2":
        vocab_classes, vocab_properties = load_vocabulary()
        user_prompt = USER_PROMPT_E2.format(
            db_name=db_name,
            db_description=db_config["description"],
            db_sample=sample_text,
            vocab_classes=vocab_classes,
            vocab_properties=vocab_properties,
        )
    elif experiment == "E3":
        rag_fragments = get_rag_fragments(db_name)
        user_prompt = USER_PROMPT_E3.format(
            db_name=db_name,
            db_description=db_config["description"],
            db_sample=sample_text,
            ontology_fragments=rag_fragments,
        )
    else:
        raise ValueError(f"Experimento desconocido: {experiment}")

    return SYSTEM_PROMPT, user_prompt


def run_single_experiment(experiment: str, db_name: str, model_name: str,
                           run_number: int = 1, dry_run: bool = False,
                           output_dir: Path = None) -> dict:
    """
    Ejecuta un experimento individual y guarda los resultados.

    Returns:
        Diccionario con metadatos de la ejecución
    """
    exp_config = EXPERIMENTS[experiment]
    output_dir = output_dir or (
        PATHS["results"] / experiment / db_name / _model_folder(model_name)
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  Experimento: {experiment} | DB: {db_name} | "
          f"Modelo: {model_name} | Run: {run_number}")

    # Construir prompt
    system_prompt, user_prompt = build_prompt(experiment, db_name)

    token_estimate = len(system_prompt + user_prompt) // 4
    print(f"  Tokens estimados en prompt: ~{token_estimate:,}")

    if dry_run:
        print(f"\n  [DRY RUN - No se llama al LLM]")
        print(f"  System prompt ({len(system_prompt)} chars):")
        print(f"    {system_prompt[:200]}...")
        print(f"\n  User prompt ({len(user_prompt)} chars):")
        print(f"    {user_prompt[:400]}...")

        # Guardar prompts para revisión
        prompt_path = output_dir / f"prompt_run{run_number}.txt"
        prompt_path.write_text(
            f"=== SYSTEM PROMPT ===\n{system_prompt}\n\n"
            f"=== USER PROMPT ===\n{user_prompt}",
            encoding='utf-8'
        )
        print(f"\n  Prompt guardado en: {prompt_path}")
        return {"dry_run": True, "prompt_tokens": token_estimate}

    # Parámetros con seed ajustada por run
    run_params = {**GENERATION_PARAMS, "seed": GENERATION_PARAMS["seed"] + run_number - 1}

    # Llamada al LLM
    print(f"  🔄 Llamando a {model_name}...", end='', flush=True)
    llm_result = call_llm(model_name, system_prompt, user_prompt, run_params)

    if not llm_result["success"]:
        print(f"\n  ❌ Error: {llm_result.get('error')}")
        return {
            "experiment": experiment,
            "db_name": db_name,
            "model": model_name,
            "run": run_number,
            "success": False,
            "error": llm_result.get("error"),
            "timestamp": datetime.now().isoformat(),
        }

    print(f" ✅ ({llm_result['elapsed']}s, {len(llm_result['content'])} chars)")

    # Extraer y validar Turtle
    turtle_text = extract_turtle(llm_result["content"])
    validation = validate_turtle(turtle_text)

    if validation.get("valid"):
        print(f"  ✅ Turtle válido: {validation['n_triples']} tripletas")
    elif validation.get("valid") is False:
        print(f"  ⚠️  Turtle inválido: {validation.get('error', '')[:100]}")
    else:
        print(f"  ℹ️  Validación no disponible (rdflib no instalado)")

    # Guardar ontología generada
    ttl_path = output_dir / f"ontology_run{run_number}.ttl"
    ttl_path.write_text(turtle_text, encoding='utf-8')

    # Guardar respuesta raw
    raw_path = output_dir / f"response_raw_run{run_number}.txt"
    raw_path.write_text(llm_result["content"], encoding='utf-8')

    # Metadatos
    metadata = {
        "experiment": experiment,
        "experiment_name": exp_config["name"],
        "db_name": db_name,
        "model": model_name,
        "run": run_number,
        "timestamp": datetime.now().isoformat(),
        "success": True,
        "elapsed_seconds": llm_result["elapsed"],
        "prompt_tokens_estimate": token_estimate,
        "response_chars": len(llm_result["content"]),
        "turtle_extracted_chars": len(turtle_text),
        "validation": validation,
        "tokens_used": llm_result.get("tokens_used"),
        "output_files": {
            "turtle": str(ttl_path),
            "raw_response": str(raw_path),
        }
    }

    meta_path = output_dir / f"metadata_run{run_number}.json"
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

    print(f"  💾 Guardado: {ttl_path.name}")
    return metadata


def run_experiment_batch(experiment: str, db_names: list, model_name: str,
                          n_repetitions: int = 1, dry_run: bool = False) -> list:
    """Ejecuta un experimento para múltiples bases de datos."""
    all_results = []

    print(f"\n{'='*60}")
    print(f"  EXPERIMENTO {experiment}: {EXPERIMENTS[experiment]['name']}")
    print(f"  Modelo: {model_name}")
    print(f"  BDs: {db_names}")
    print(f"  Repeticiones: {n_repetitions}")
    print(f"{'='*60}")

    for db_name in db_names:
        db_results = []
        for run in range(1, n_repetitions + 1):
            result = run_single_experiment(
                experiment, db_name, model_name,
                run_number=run, dry_run=dry_run
            )
            db_results.append(result)

        # Resumen por BD
        if not dry_run:
            output_dir = (PATHS["results"] / experiment / db_name /
                          _model_folder(model_name))
            summary = {
                "experiment": experiment,
                "db_name": db_name,
                "model": model_name,
                "n_runs": n_repetitions,
                "n_success": sum(1 for r in db_results if r.get("success")),
                "n_valid_turtle": sum(
                    1 for r in db_results
                    if r.get("validation", {}).get("valid") is True
                ),
                "avg_elapsed": (
                    sum(r.get("elapsed_seconds", 0) for r in db_results) / n_repetitions
                ),
                "runs": db_results,
            }
            summary_path = output_dir / "summary.json"
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

        all_results.extend(db_results)

    return all_results


def main():
    parser = argparse.ArgumentParser(
        description='Ejecutar experimentos de generación de ontologías con LLMs'
    )
    parser.add_argument(
        '--experiment',
        choices=list(EXPERIMENTS.keys()) + ['all'],
        default='E1',
        help='Experimento a ejecutar (default: E1)'
    )
    parser.add_argument(
        '--model',
        choices=list(LLM_MODELS.keys()),
        default='llama3.1:8b',
        help='Modelo LLM a usar (default: llama3.1:8b)'
    )
    parser.add_argument(
        '--db',
        choices=list(DATABASES.keys()) + ['all'],
        default='all',
        help='Base de datos (default: all)'
    )
    parser.add_argument(
        '--n-runs',
        type=int,
        default=N_REPETITIONS,
        help=f'Número de repeticiones (default: {N_REPETITIONS})'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostrar prompts sin llamar al LLM'
    )
    parser.add_argument(
        '--samples-dir',
        type=Path, default=None,
        help='Carpeta con las muestras {DB}_sample_prompt.txt (p. ej. una celda '
             'de data/grid/<tipo>/N=<n>/). Por defecto usa data/samples.'
    )
    parser.add_argument(
        '--results-suffix',
        default='',
        help='Sufijo para la carpeta de modelo, p. ej. A_head_N50 → '
             'results/{exp}/{db}/{modelo}_A_head_N50/. Da trazabilidad a la rejilla.'
    )
    args = parser.parse_args()

    global SAMPLES_DIR_OVERRIDE, RESULTS_SUFFIX
    SAMPLES_DIR_OVERRIDE = args.samples_dir
    RESULTS_SUFFIX = args.results_suffix or ""

    print("\n" + "="*60)
    print("  EXPERIMENTOS LLM - TFM ONTOLOGÍAS CRM")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print(f"\n  Modelo: {args.model}")
    print(f"  Experimento(s): {args.experiment}")
    if args.dry_run:
        print("  ⚠️  MODO DRY-RUN: no se llama al LLM")

    # Selección de BDs
    if args.db == 'all':
        dbs = [db for db in DATABASES.keys()
               if (PATHS["processed_db"] / DATABASES[db]["file"]).exists()]
    else:
        dbs = [args.db]

    # Selección de experimentos
    experiments = list(EXPERIMENTS.keys()) if args.experiment == 'all' else [args.experiment]

    # Verificar muestras disponibles
    missing_samples = [db for db in dbs
                       if not (_samples_dir() / f"{db}_sample_prompt.txt").exists()]
    if missing_samples:
        print(f"\n  ⚠️  Muestras no encontradas para: {missing_samples}")
        print(f"     Ejecuta primero: python 02_sample_databases.py")
        if not args.dry_run:
            print(f"     O usa --dry-run para ver los prompts sin datos.")

    # Ejecutar experimentos
    all_results = []
    for experiment in experiments:
        results = run_experiment_batch(
            experiment, dbs, args.model,
            n_repetitions=args.n_runs,
            dry_run=args.dry_run
        )
        all_results.extend(results)

    # Resumen global
    if not args.dry_run:
        n_success = sum(1 for r in all_results if r.get("success"))
        n_valid = sum(
            1 for r in all_results
            if r.get("validation", {}).get("valid") is True
        )
        print(f"\n{'='*60}")
        print(f"  RESUMEN GLOBAL")
        print(f"{'='*60}")
        print(f"  Experimentos ejecutados: {len(all_results)}")
        print(f"  Llamadas exitosas:       {n_success}/{len(all_results)}")
        print(f"  Ontologías válidas:      {n_valid}/{len(all_results)}")
        print(f"\n  Resultados en: {PATHS['results']}")
        print(f"  Siguiente paso: python 05_evaluate_results.py")


if __name__ == "__main__":
    main()
