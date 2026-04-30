"""
config.py - Configuración central del proyecto TFM
"Evaluación de LLMs para la Generación de Ontologías en Bases de Datos Genéticas"
"""

import os
from pathlib import Path

# ─── Rutas del proyecto ───────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
# Ruta del host del usuario (para datos originales - no necesaria para experimentos con muestras)
DATA_ROOT    = Path(os.environ.get("TFM_DATA_ROOT", "/Users/franciscosaez/Documents/data-2"))

PATHS = {
    # Bases de datos procesadas
    "processed_db": DATA_ROOT / "CRM" / "processed_db",
    # Esquemas de referencia (Turtle)
    "schemas":      DATA_ROOT / "CRM" / "schema",
    # RDF de referencia
    "rdf":          DATA_ROOT / "CRM" / "rdf",
    # Salidas del proyecto
    "samples":      PROJECT_ROOT / "data" / "samples",
    "results":      PROJECT_ROOT / "results",
    "prompts":      PROJECT_ROOT / "data" / "prompts",
    "ontologies":   PROJECT_ROOT / "data" / "ontologies_generated",
}

# Crear carpetas de salida si no existen
for p in ["samples", "results", "prompts", "ontologies"]:
    PATHS[p].mkdir(parents=True, exist_ok=True)

# ─── Bases de datos disponibles ───────────────────────────────────────────────
DATABASES = {
    "dbSUPER": {
        "file": "dbSUPER.tsv",
        "description": "Super-enhancers con coordenadas, líneas celulares y genes diana",
        "has_header": True,
        "separator": "\t",
        "url": "https://asntech.org/dbsuper/",
    },
    "FANTOM5": {
        "file": "FANTOM5.tsv",
        "description": "Enhancers activos identificados por CAGE-seq",
        "has_header": True,
        "separator": "\t",
        "url": "https://fantom.gsc.riken.jp/5/",
    },
    "ENdb": {
        "file": "ENdb.tsv",
        "description": "Enhancers validados experimentalmente con evidencias ChIP-seq",
        "has_header": True,
        "separator": "\t",
        "url": "http://www.licpathway.net/ENdb/",
    },
    "HACER": {
        "file": "HACER.tsv",
        "description": "Human Active Cis-regulatory Elements database",
        "has_header": True,
        "separator": "\t",
        "url": "http://bioinfo.vanderbilt.edu/AE/HACER/",
    },
    "DiseaseEnhancer": {
        "file": "DiseaseEnhancer.tsv",
        "description": "Enhancers asociados a enfermedades",
        "has_header": True,
        "separator": "\t",
        "url": "http://biocc.hrbmu.edu.cn/DiseaseEnhancer/",
    },
    "SEA": {
        "file": "SEA.tsv",
        "description": "Super-Enhancer Archive",
        "has_header": True,
        "separator": "\t",
        "url": "http://sea.edbc.org/",
    },
    "SCREEN": {
        "file": "SCREEN.tsv",
        "description": "Search Candidate Regulatory Elements by ENCODE (cCREs)",
        "has_header": True,
        "separator": "\t",
        "url": "https://screen.encodeproject.org/",
    },
    "EnDisease": {
        "file": "EnDisease.tsv",
        "description": "Enhancers asociados a enfermedades con evidencias publicadas",
        "has_header": True,
        "separator": "\t",
        "url": "-",
    },
    "RefSeq": {
        "file": "RefSeq.tsv",
        "description": "Secuencias de referencia NCBI RefSeq",
        "has_header": True,
        "separator": "\t",
        "url": "https://www.ncbi.nlm.nih.gov/refseq/",
    },
    "Ensembl": {
        "file": "Ensembl.tsv",
        "description": "Datos de ensamblaje genómico Ensembl",
        "has_header": True,
        "separator": "\t",
        "url": "https://www.ensembl.org/",
    },
}

# ─── Esquemas ontológicos de referencia ───────────────────────────────────────
SCHEMAS = {
    "crm":          "crm.txt",
    "crm2gene":     "crm2gene.txt",
    "crm2phen":     "crm2phen.txt",
    "crm2tfac":     "crm2tfac.txt",
}
SCHEMA_EXAMPLES = {
    "crm":          "crm_example.txt",
    "crm2gene":     "crm2gene_example.txt",
    "crm2phen":     "crm2phen_example.txt",
    "crm2tfac":     "crm2tfac_example.txt",
}

# ─── Modelos LLM ─────────────────────────────────────────────────────────────
LLM_MODELS = {
    # Modelos open-source via Ollama (modelo principal del TFM)
    "llama3.1:70b": {
        "provider": "ollama",
        "base_url": "http://localhost:11434",
        "context_window": 131072,
        "description": "Llama 3.1 70B - modelo principal open-source",
    },
    "llama3.1:8b": {
        "provider": "ollama",
        "base_url": "http://localhost:11434",
        "context_window": 131072,
        "description": "Llama 3.1 8B - modelo compacto open-source",
    },
    "llama3.2:3b": {
        "provider": "ollama",
        "base_url": "http://localhost:11434",
        "context_window": 131072,
        "description": "Llama 3.2 3B - modelo muy compacto",
    },
    "mistral:7b": {
        "provider": "ollama",
        "base_url": "http://localhost:11434",
        "context_window": 32768,
        "description": "Mistral 7B - referencia open-source adicional",
    },
    "qwen2.5-coder:7b": {
        "provider": "ollama",
        "base_url": "http://localhost:11434",
        "context_window": 32768,
        "description": "Qwen 2.5 Coder 7B - open-source especializado en "
                       "código (Alibaba). Comparativo con Llama 3.1 8B "
                       "para medir el efecto de la especialización en "
                       "código sobre la generación de Turtle.",
    },
    # Modelos comerciales via API (baseline de comparación)
    "gpt-4o": {
        "provider": "openai",
        "base_url": "https://api.openai.com/v1",
        "context_window": 128000,
        "description": "GPT-4o - baseline comercial",
        "api_key_env": "OPENAI_API_KEY",
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "base_url": "https://api.openai.com/v1",
        "context_window": 128000,
        "description": "GPT-4o-mini - baseline comercial compacto",
        "api_key_env": "OPENAI_API_KEY",
    },
}

# Modelo por defecto para experimentos rápidos
DEFAULT_MODEL = "llama3.1:8b"

# ─── Parámetros de generación ─────────────────────────────────────────────────
GENERATION_PARAMS = {
    "temperature": 0.1,    # Baja aleatoriedad para código formal
    "top_p": 0.9,
    "max_tokens": 4096,
    "seed": 42,            # Reproducibilidad
}

# ─── Parámetros de muestreo de datos ─────────────────────────────────────────
SAMPLING_PARAMS = {
    "n_header_rows": 5,        # Filas de cabecera siempre incluidas
    "n_sample_rows": 20,       # Filas adicionales de muestra
    "max_tokens_data": 3000,   # Límite de tokens para datos en el prompt
    "random_seed": 42,
}

# ─── Tipos de experimento ─────────────────────────────────────────────────────
EXPERIMENTS = {
    "E1": {
        "name": "Base (zero-shot)",
        "description": "Generación de esquema directamente desde datos en bruto",
        "use_vocabulary": False,
        "use_rag": False,
    },
    "E2": {
        "name": "Con vocabulario controlado",
        "description": "Generación con vocabulario controlado de cisreg como contexto",
        "use_vocabulary": True,
        "use_rag": False,
    },
    "E3": {
        "name": "Con RAG (ontología cisreg)",
        "description": "Generación aumentada con fragmentos de la ontología cisreg",
        "use_vocabulary": False,
        "use_rag": True,
    },
}

# ─── Número de repeticiones por experimento ────────────────────────────────────
N_REPETITIONS = 3  # Para estimar variabilidad del modelo

print("✅ Configuración cargada correctamente.")
print(f"   • Bases de datos disponibles: {list(DATABASES.keys())}")
print(f"   • Modelos disponibles: {list(LLM_MODELS.keys())}")
print(f"   • Experimentos: {list(EXPERIMENTS.keys())}")
