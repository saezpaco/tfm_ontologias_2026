#!/usr/bin/env python3
"""
03_test_llm_connection.py
Prueba de conectividad con los modelos LLM disponibles.

Verifica:
  - Ollama (local): conectividad, modelos instalados, generación básica
  - OpenAI API: clave de API, acceso a GPT-4o, generación básica

Uso:
    python 03_test_llm_connection.py
    python 03_test_llm_connection.py --provider ollama
    python 03_test_llm_connection.py --provider openai
    python 03_test_llm_connection.py --model llama3.1:8b --full-test
"""

import sys
import os
import json
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from config import LLM_MODELS, GENERATION_PARAMS

# Test prompt especializado en el dominio del TFM
TEST_PROMPT_SIMPLE = """You are an expert ontologist. Define in one sentence what a 'cis-regulatory module' is."""

TEST_PROMPT_TURTLE = """You are an expert ontologist specializing in biological knowledge graphs.
Generate a minimal valid OWL ontology in Turtle format for a 'cis-regulatory module' (CRM) concept.
Include only:
- The namespace declarations
- One class definition (CRM)
- Two properties (hasChromosome, hasStartPosition)
- SKOS annotations

Output ONLY valid Turtle code, no explanations."""


def check_ollama_installed() -> bool:
    """Verifica si Ollama está instalado."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_ollama_models() -> list:
    """Obtiene la lista de modelos instalados en Ollama."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            models = []
            for line in lines[1:]:  # Skip header
                parts = line.split()
                if parts:
                    models.append(parts[0])
            return models
        return []
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


def test_ollama_generation(model_name: str, prompt: str,
                            params: dict = None) -> dict:
    """Prueba la generación con un modelo Ollama."""
    try:
        import requests
    except ImportError:
        return {"success": False, "error": "requests no instalado. Ejecuta: pip install requests"}

    params = params or GENERATION_PARAMS
    base_url = LLM_MODELS.get(model_name, {}).get("base_url", "http://localhost:11434")

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "options": {
            "temperature": params.get("temperature", 0.1),
            "top_p": params.get("top_p", 0.9),
            "num_predict": params.get("max_tokens", 512),
            "seed": params.get("seed", 42),
        },
        "stream": False,
    }

    start = time.time()
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json=payload,
            timeout=120
        )
        elapsed = time.time() - start

        if response.status_code == 200:
            data = response.json()
            content = data.get("message", {}).get("content", "")
            return {
                "success": True,
                "model": model_name,
                "response_length": len(content),
                "elapsed_seconds": round(elapsed, 2),
                "response_preview": content[:300] + "..." if len(content) > 300 else content,
                "full_response": content,
            }
        else:
            return {
                "success": False,
                "model": model_name,
                "error": f"HTTP {response.status_code}: {response.text[:200]}",
                "elapsed_seconds": round(elapsed, 2),
            }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "model": model_name,
            "error": "Ollama no está en ejecución. Inicia con: ollama serve",
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "model": model_name,
            "error": "Timeout (>120s). El modelo puede estar cargándose.",
        }


def test_openai_generation(model_name: str, prompt: str,
                            params: dict = None) -> dict:
    """Prueba la generación con un modelo OpenAI."""
    try:
        import openai
    except ImportError:
        return {
            "success": False,
            "error": "openai no instalado. Ejecuta: pip install openai"
        }

    model_config = LLM_MODELS.get(model_name, {})
    api_key_env = model_config.get("api_key_env", "OPENAI_API_KEY")
    api_key = os.environ.get(api_key_env)

    if not api_key:
        return {
            "success": False,
            "model": model_name,
            "error": f"Variable de entorno {api_key_env} no definida. "
                     f"Ejecuta: export {api_key_env}=tu_clave_aqui",
        }

    params = params or GENERATION_PARAMS

    try:
        client = openai.OpenAI(api_key=api_key)
        start = time.time()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=params.get("temperature", 0.1),
            top_p=params.get("top_p", 0.9),
            max_tokens=params.get("max_tokens", 512),
            seed=params.get("seed", 42),
        )
        elapsed = time.time() - start

        content = response.choices[0].message.content
        return {
            "success": True,
            "model": model_name,
            "response_length": len(content),
            "elapsed_seconds": round(elapsed, 2),
            "tokens_used": response.usage.total_tokens if response.usage else "N/A",
            "response_preview": content[:300] + "..." if len(content) > 300 else content,
            "full_response": content,
        }
    except openai.AuthenticationError:
        return {
            "success": False,
            "model": model_name,
            "error": "Clave de API incorrecta o inválida.",
        }
    except openai.RateLimitError:
        return {
            "success": False,
            "model": model_name,
            "error": "Rate limit alcanzado. Espera unos segundos y reintenta.",
        }
    except Exception as e:
        return {
            "success": False,
            "model": model_name,
            "error": str(e),
        }


def validate_turtle_output(text: str) -> dict:
    """Valida si la salida es Turtle válido."""
    try:
        import rdflib
        g = rdflib.Graph()
        g.parse(data=text, format="turtle")
        return {
            "valid": True,
            "n_triples": len(g),
        }
    except ImportError:
        return {"valid": None, "error": "rdflib no instalado"}
    except Exception as e:
        return {"valid": False, "error": str(e)[:200]}


def test_provider_ollama(models_to_test: list, full_test: bool = False) -> dict:
    """Realiza todas las pruebas para Ollama."""
    print("\n" + "="*60)
    print("  PRUEBA DE CONECTIVIDAD: OLLAMA")
    print("="*60)

    results = {"provider": "ollama", "tests": {}}

    # Verificar instalación
    installed = check_ollama_installed()
    results["installed"] = installed
    if not installed:
        print("  ❌ Ollama no está instalado.")
        print("     Instala desde: https://ollama.ai/download")
        return results
    print("  ✅ Ollama instalado correctamente.")

    # Modelos disponibles
    available_models = get_ollama_models()
    results["available_models"] = available_models
    print(f"\n  📋 Modelos instalados ({len(available_models)}):")
    if available_models:
        for m in available_models:
            in_config = "✅" if m in LLM_MODELS else "ℹ️ "
            print(f"     {in_config} {m}")
    else:
        print("     (ninguno instalado o Ollama no en ejecución)")
        print("\n  Para instalar Llama 3:")
        print("     ollama pull llama3.1:8b      # Versión 8B (recomendada para inicio)")
        print("     ollama pull llama3.1:70b     # Versión 70B (requiere >40GB RAM)")
        print("     ollama pull mistral:7b        # Mistral 7B alternativo")

    # Prueba de generación por modelo
    for model_name in models_to_test:
        model_config = LLM_MODELS.get(model_name, {})
        if model_config.get("provider") != "ollama":
            continue

        in_ollama = any(model_name in m for m in available_models)
        if not in_ollama:
            print(f"\n  ⚠️  {model_name}: NO instalado en Ollama")
            print(f"     Instala con: ollama pull {model_name}")
            results["tests"][model_name] = {
                "success": False,
                "error": "Modelo no instalado"
            }
            continue

        print(f"\n  🔄 Probando {model_name}...")

        # Test simple
        result_simple = test_ollama_generation(model_name, TEST_PROMPT_SIMPLE,
                                               params={"temperature": 0.1,
                                                       "top_p": 0.9,
                                                       "max_tokens": 100,
                                                       "seed": 42})
        if result_simple["success"]:
            print(f"     ✅ Test simple: OK ({result_simple['elapsed_seconds']}s)")
            print(f"     📝 Respuesta: {result_simple['response_preview'][:150]}...")
        else:
            print(f"     ❌ Test simple: FALLO - {result_simple.get('error')}")
            results["tests"][model_name] = result_simple
            continue

        if full_test:
            # Test Turtle
            print(f"     🔄 Test Turtle (ontología)...")
            result_turtle = test_ollama_generation(
                model_name, TEST_PROMPT_TURTLE,
                params={"temperature": 0.1, "top_p": 0.9,
                        "max_tokens": 1024, "seed": 42}
            )
            if result_turtle["success"]:
                validation = validate_turtle_output(result_turtle["full_response"])
                print(f"     ✅ Test Turtle: OK ({result_turtle['elapsed_seconds']}s)")
                if validation.get("valid"):
                    print(f"     ✅ Validación Turtle: válido ({validation['n_triples']} tripletas)")
                elif validation.get("valid") is False:
                    print(f"     ⚠️  Validación Turtle: inválido - {validation.get('error')[:100]}")
                    # Intentar extraer el bloque turtle de la respuesta
                    turtle_text = result_turtle["full_response"]
                    if "```turtle" in turtle_text:
                        turtle_block = turtle_text.split("```turtle")[1].split("```")[0]
                        val2 = validate_turtle_output(turtle_block)
                        if val2.get("valid"):
                            print(f"     ✅ Bloque extraído: válido ({val2['n_triples']} tripletas)")
                result_simple["turtle_test"] = {
                    "success": result_turtle["success"],
                    "turtle_valid": validation.get("valid"),
                    "n_triples": validation.get("n_triples"),
                    "elapsed_seconds": result_turtle.get("elapsed_seconds"),
                }
            else:
                print(f"     ❌ Test Turtle: FALLO - {result_turtle.get('error')}")

        results["tests"][model_name] = result_simple

    return results


def test_provider_openai(models_to_test: list, full_test: bool = False) -> dict:
    """Realiza todas las pruebas para OpenAI."""
    print("\n" + "="*60)
    print("  PRUEBA DE CONECTIVIDAD: OpenAI API")
    print("="*60)

    results = {"provider": "openai", "tests": {}}

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("  ⚠️  OPENAI_API_KEY no está definida.")
        print("     Para configurar:")
        print("     export OPENAI_API_KEY='sk-...'")
        print("     (o añade al fichero .env del proyecto)")
        results["api_key_configured"] = False
        return results

    print(f"  ✅ API key configurada: sk-...{api_key[-4:]}")
    results["api_key_configured"] = True

    for model_name in models_to_test:
        model_config = LLM_MODELS.get(model_name, {})
        if model_config.get("provider") != "openai":
            continue

        print(f"\n  🔄 Probando {model_name}...")

        result_simple = test_openai_generation(
            model_name, TEST_PROMPT_SIMPLE,
            params={"temperature": 0.1, "top_p": 0.9,
                    "max_tokens": 100, "seed": 42}
        )

        if result_simple["success"]:
            tokens = result_simple.get("tokens_used", "N/A")
            print(f"     ✅ Test simple: OK ({result_simple['elapsed_seconds']}s, {tokens} tokens)")
            print(f"     📝 Respuesta: {result_simple['response_preview'][:150]}...")
        else:
            print(f"     ❌ Test simple: FALLO - {result_simple.get('error')}")
            results["tests"][model_name] = result_simple
            continue

        if full_test:
            print(f"     🔄 Test Turtle (ontología)...")
            result_turtle = test_openai_generation(
                model_name, TEST_PROMPT_TURTLE,
                params={"temperature": 0.1, "top_p": 0.9,
                        "max_tokens": 1024, "seed": 42}
            )
            if result_turtle["success"]:
                validation = validate_turtle_output(result_turtle["full_response"])
                print(f"     ✅ Test Turtle: OK ({result_turtle['elapsed_seconds']}s)")
                if validation.get("valid"):
                    print(f"     ✅ Validación: {validation['n_triples']} tripletas generadas")
                elif validation.get("valid") is False:
                    # Try to extract turtle block
                    turtle_text = result_turtle["full_response"]
                    if "```" in turtle_text:
                        for marker in ["```turtle\n", "```ttl\n", "```\n"]:
                            if marker in turtle_text:
                                block = turtle_text.split(marker)[1].split("```")[0]
                                val2 = validate_turtle_output(block)
                                if val2.get("valid"):
                                    print(f"     ✅ Bloque extraído: válido ({val2['n_triples']} tripletas)")
                                    break
                result_simple["turtle_test"] = {
                    "success": result_turtle["success"],
                    "turtle_valid": validation.get("valid"),
                }

        results["tests"][model_name] = result_simple

    return results


def print_summary(ollama_results: dict, openai_results: dict) -> None:
    """Imprime resumen de resultados."""
    print("\n" + "="*60)
    print("  RESUMEN DE CONECTIVIDAD")
    print("="*60)

    print("\n  OLLAMA:")
    if not ollama_results.get("installed"):
        print("    ❌ No instalado")
    else:
        print(f"    ✅ Instalado")
        available = ollama_results.get("available_models", [])
        for model_name, test_result in ollama_results.get("tests", {}).items():
            status = "✅ OK" if test_result.get("success") else "❌ FALLO"
            print(f"    {status} - {model_name}")

    print("\n  OPENAI API:")
    if not openai_results.get("api_key_configured"):
        print("    ⚠️  API key no configurada")
    else:
        for model_name, test_result in openai_results.get("tests", {}).items():
            status = "✅ OK" if test_result.get("success") else "❌ FALLO"
            print(f"    {status} - {model_name}")

    # Recomendaciones
    print("\n  💡 RECOMENDACIONES PARA EL TFM:")
    any_ollama_ok = any(
        r.get("success") for r in ollama_results.get("tests", {}).values()
    )
    any_openai_ok = any(
        r.get("success") for r in openai_results.get("tests", {}).values()
    )

    if any_ollama_ok:
        print("    ✅ Puedes comenzar los experimentos con Ollama (Llama 3)")
    else:
        print("    📥 Instala un modelo Ollama: ollama pull llama3.1:8b")

    if any_openai_ok:
        print("    ✅ OpenAI API disponible para experimentos de comparación")
    else:
        print("    ℹ️  Configura OPENAI_API_KEY para el baseline con GPT-4o")

    if any_ollama_ok or any_openai_ok:
        print("\n    🚀 Siguiente paso: python 04_run_experiments.py --experiment E1")


def main():
    parser = argparse.ArgumentParser(
        description='Test de conectividad con modelos LLM para el TFM'
    )
    parser.add_argument(
        '--provider',
        choices=['ollama', 'openai', 'all'],
        default='all',
        help='Proveedor a probar (default: all)'
    )
    parser.add_argument(
        '--model',
        choices=list(LLM_MODELS.keys()),
        default=None,
        help='Modelo específico a probar'
    )
    parser.add_argument(
        '--full-test',
        action='store_true',
        help='Realizar test completo incluyendo generación de Turtle'
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("  TEST DE CONECTIVIDAD LLM - TFM ONTOLOGÍAS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Determinar modelos a probar
    if args.model:
        models_to_test = [args.model]
    else:
        models_to_test = list(LLM_MODELS.keys())

    ollama_results = {}
    openai_results = {}

    if args.provider in ['ollama', 'all']:
        ollama_results = test_provider_ollama(models_to_test, args.full_test)

    if args.provider in ['openai', 'all']:
        openai_results = test_provider_openai(models_to_test, args.full_test)

    print_summary(ollama_results, openai_results)

    # Guardar resultados
    results_path = Path("results") / "03_llm_connectivity_test.json"
    results_path.parent.mkdir(exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "ollama": ollama_results,
            "openai": openai_results,
        }, f, indent=2, default=str)
    print(f"\n  📊 Resultados guardados en: {results_path}\n")


if __name__ == "__main__":
    main()
