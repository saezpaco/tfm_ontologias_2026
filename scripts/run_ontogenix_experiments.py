#!/usr/bin/env python3
"""
run_ontogenix_experiments.py
────────────────────────────
Experimento E4 del TFM "Evaluación de LLMs para la Generación de Ontologías
en Bases de Datos Genéticas".

Este script ejecuta la pipeline multi-agente de OntoGenix
(github.com/tecnomod-um/OntoGenix) sobre un subconjunto representativo de las
bases de datos de enhancers/super-enhancers del proyecto, y guarda las
ontologías (.ttl) y mappings (.ttl) generados junto con sus metadatos.

Pipeline OntoGenix utilizado (sin GUI PyQt5):
    1. csv_data_preprocessing  → estadísticas y DataFrame del CSV
    2. dataframe2prettyjson    → representación JSON del CSV
    3. LlmPlanner.interaction  → descripción de datos + estructura ontológica
    4. LlmOntology.interact    → ontología OWL/TTL completa
    5. LlmOntoMapper.interact  → mapping RML en formato TTL

Uso:
    export OPENAI_API_KEY="sk-..."
    python scripts/run_ontogenix_experiments.py [--databases FANTOM5 dbSUPER ...]
                                                 [--runs 3]
                                                 [--model gpt-4o-2024-05-13]

Salidas: results/E4/{DB}/{model}/
    - ontology_run{N}.ttl
    - mapping_run{N}.ttl
    - data_description_run{N}.md
    - response_raw_run{N}.txt   (concatenación de los 3 pasos LLM)
    - metadata_run{N}.json      (tiempos, tokens, modelo, errores)
    - summary.json              (agregado de N runs)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

# ────────────────────────────── PATHS ────────────────────────────────────────
PROJECT_ROOT    = Path(__file__).resolve().parent.parent
ONTOGENIX_ROOT  = PROJECT_ROOT / "OntoGenix"
CSV_INPUT_DIR   = PROJECT_ROOT / "data" / "csv_for_ontogenix"
RESULTS_ROOT    = PROJECT_ROOT / "results" / "E4"

if not ONTOGENIX_ROOT.exists():
    sys.exit(f"[ERROR] No se encuentra OntoGenix en {ONTOGENIX_ROOT}. "
             f"Clónalo con: git clone https://github.com/tecnomod-um/OntoGenix.git")

# Añade OntoGenix al path para poder hacer `from GUI...`
sys.path.insert(0, str(ONTOGENIX_ROOT))
# OntoGenix usa rutas relativas './GUI/...' para cargar prompts → cwd = OntoGenix
os.chdir(ONTOGENIX_ROOT)

# ──────────────────────── .env con la OPENAI_API_KEY ─────────────────────────
ENV_PATH = ONTOGENIX_ROOT / "GUI" / ".env"

def ensure_env_file() -> None:
    """Crea OntoGenix/GUI/.env a partir de OPENAI_API_KEY si no existe."""
    if ENV_PATH.exists() and "OPENAI_API_KEY" in ENV_PATH.read_text():
        return
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("[ERROR] OPENAI_API_KEY no está exportada y OntoGenix/GUI/.env no contiene la clave.")
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Añadimos SERP_API_KEY=dummy para que Searcher.__init__ no reviente
    ENV_PATH.write_text(
        f'OPENAI_API_KEY="{api_key}"\n'
        f'SERP_API_KEY="dummy"\n',
        encoding="utf-8",
    )
    print(f"[INFO] .env creado en {ENV_PATH}")

ensure_env_file()

# ───────────── Imports de OntoGenix (después de configurar paths) ────────────
# Silenciamos los logs ruidosos
import logging
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

from GUI.PlanSage.LLM_planner  import LlmPlanner       # noqa: E402
from GUI.OntoBuilder.LLM_ontology import LlmOntology   # noqa: E402
from GUI.OntoMapper.LLM_ontomapper import LlmOntoMapper  # noqa: E402
from GUI.tools.tools import csv_data_preprocessing, dataframe2prettyjson  # noqa: E402

# ────────────────────────── METADATOS DE AGENTES ─────────────────────────────
def build_metadata(api_model: str,
                   seed: int,
                   ontology_extension: str = "ttl",
                   mapping_extension: str = "ttl") -> tuple[dict, dict, dict]:
    """Construye los diccionarios de metadatos para los 3 agentes LLM,
    replicando el contenido de GUI/GuiManager/metadata.json pero con valores
    ya resueltos (sin la interpolación `${...}` que hace MetadataManager)."""
    base = str(ONTOGENIX_ROOT / "GUI")
    common = {
        "api_key_path": str(ENV_PATH),
        "client":      "openai",
        "ssl_cert":    None,
        "model":       api_model,
        "seed":        seed,
    }
    planner_metadata = {
        **common,
        "role": ("You are a powerful ontology engineer that generates the reasoning steps "
                 "needed to generate\nthe context needed to create an ontology from a json data table."),
        "instructions":               f"{base}/PlanSage/instructions.prompt",
        "data_description":           f"{base}/PlanSage/data_description.prompt",
        "interoperability_management":f"{base}/PlanSage/interoperability_management.prompt",
        "dataset": None,
    }
    onto_metadata = {
        **common,
        "role": f"You are a powerful ontology engineer that generates OWL ontologies in {ontology_extension} format.",
        "ontology_instructions":       f"{base}/OntoBuilder/ontology_instructions.prompt",
        "ontology_instructions_error": f"{base}/OntoBuilder/ontology_instructions_error.prompt",
        "entity_improvement":          f"{base}/OntoBuilder/entity_improvement.prompt",
        "dataset": None,
    }
    mapper_metadata = {
        **common,
        "role": f"You are a powerful ontology engineer that generates mappings in {mapping_extension} format.",
        "instructions":       f"{base}/OntoMapper/instructions.prompt",
        "error_instructions": f"{base}/OntoMapper/error_instructions.prompt",
        "example_extension":  f"{base}/OntoMapper/examples/example_{mapping_extension}.prompt",
        "dataset": None,
    }
    return planner_metadata, onto_metadata, mapper_metadata

# ──────────────────────── Ejecutor async de la pipeline ──────────────────────
async def _collect(gen) -> str:
    out = []
    async for chunk in gen:
        if chunk:
            out.append(chunk)
    return "".join(out)

async def run_single_experiment(csv_path: Path,
                                out_dir:  Path,
                                run_idx:  int,
                                api_model: str,
                                seed: int,
                                skip_mapping: bool = False,
                                mapping_extension: str = "ttl") -> dict:
    """Ejecuta una sola corrida del pipeline OntoGenix sobre `csv_path`."""
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        "run":             run_idx,
        "dataset_csv":     str(csv_path),
        "api_model":       api_model,
        "seed":            seed,
        "mapping_extension": mapping_extension,
        "started_at":      datetime.now(timezone.utc).isoformat(),
        "steps":           {},
        "errors":          [],
    }
    planner_meta, onto_meta, mapper_meta = build_metadata(
        api_model=api_model, seed=seed, mapping_extension=mapping_extension
    )

    try:
        # ── 1-2. Pre-procesado + serialización del CSV ──────────────────────
        t0 = time.time()
        df = csv_data_preprocessing(str(csv_path))
        json_data = dataframe2prettyjson(df)
        meta["steps"]["csv_preprocessing_s"] = round(time.time() - t0, 3)

        # ── 3. Descripción de datos + estructura (LlmPlanner) ───────────────
        t0 = time.time()
        planner = LlmPlanner(planner_meta)
        input_task = ("Generate a high-level ontology design description for the given dataset. "
                      "Focus on the classes, subclasses, object properties and datatype properties "
                      "required to model genetic regulatory elements (enhancers, super-enhancers), "
                      "their genomic coordinates, cell lines/biosamples, target genes, transcription "
                      "factors and disease associations.")
        data_description = await _collect(
            planner.interaction(input_task=input_task, json_data=json_data)
        )
        (out_dir / f"data_description_run{run_idx}.md").write_text(
            data_description, encoding="utf-8"
        )
        meta["steps"]["plan_s"]                  = round(time.time() - t0, 3)
        meta["steps"]["plan_chars"]              = len(data_description)
        meta["steps"]["plan_prompt_chars"]       = len(planner.current_prompt or "")

        # ── 4. Generación de la ontología (LlmOntology) ─────────────────────
        t0 = time.time()
        onto_builder = LlmOntology(onto_meta)
        ontology_text = await _collect(onto_builder.interact(
            json_data=json_data,
            data_description=data_description,
            state="ONTOLOGY",
        ))
        (out_dir / f"ontology_run{run_idx}.ttl").write_text(
            ontology_text, encoding="utf-8"
        )
        meta["steps"]["onto_s"]            = round(time.time() - t0, 3)
        meta["steps"]["onto_chars"]        = len(ontology_text)
        meta["steps"]["onto_prompt_chars"] = len(onto_builder.current_prompt or "")

        # ── 5. Mapping (LlmOntoMapper) ──────────────────────────────────────
        if not skip_mapping:
            t0 = time.time()
            mapper = LlmOntoMapper(mapper_meta)
            mapper.dataset_path = csv_path.name  # el prompt usa el *nombre* del CSV
            # example_extension = contenido del example_{mapping}.prompt
            example = mapper.example_extension or ""
            mapping_text = await _collect(mapper.interact(
                rationale=data_description,
                ontology=ontology_text,
                mapping_extension=mapping_extension.upper(),
                example_extension=example,
                ontology_extension="TTL",
            ))
            (out_dir / f"mapping_run{run_idx}.ttl").write_text(
                mapping_text, encoding="utf-8"
            )
            meta["steps"]["map_s"]            = round(time.time() - t0, 3)
            meta["steps"]["map_chars"]        = len(mapping_text)
            meta["steps"]["map_prompt_chars"] = len(mapper.current_prompt or "")
        else:
            mapping_text = ""

        # ── Respuesta cruda concatenada (para auditoría estilo E1/E2/E3) ────
        raw = (
            "################ DATA DESCRIPTION (PlanSage) ################\n"
            f"{data_description}\n\n"
            "################ ONTOLOGY (OntoBuilder) #####################\n"
            f"{ontology_text}\n\n"
            "################ MAPPING (OntoMapper) #######################\n"
            f"{mapping_text}\n"
        )
        (out_dir / f"response_raw_run{run_idx}.txt").write_text(raw, encoding="utf-8")

        meta["status"]     = "ok"
    except Exception as e:                                                # noqa: BLE001
        meta["status"]     = "error"
        meta["errors"].append({"type": type(e).__name__, "msg": str(e),
                               "trace": traceback.format_exc()})
        print(f"[ERROR] run {run_idx}: {e}")

    meta["finished_at"]    = datetime.now(timezone.utc).isoformat()
    meta["total_s"]        = round(sum(v for k, v in meta["steps"].items()
                                       if k.endswith("_s")), 3)
    # Guardar metadatos de esta corrida
    (out_dir / f"metadata_run{run_idx}.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return meta

# ─────────────────────────────── MAIN ────────────────────────────────────────
DEFAULT_DATABASES = ["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"]

async def run_all(databases: list[str],
                  runs: int,
                  api_model: str,
                  base_seed: int,
                  skip_mapping: bool,
                  mapping_extension: str) -> None:
    model_tag = api_model.replace("-2024-05-13", "")  # carpeta "gpt-4o"
    for db in databases:
        csv_path = CSV_INPUT_DIR / f"{db}.csv"
        if not csv_path.exists():
            print(f"[WARN] No existe CSV {csv_path}, salto {db}")
            continue
        db_out = RESULTS_ROOT / db / model_tag
        db_out.mkdir(parents=True, exist_ok=True)
        print(f"\n╔═══ {db}  →  {db_out}")
        all_meta = []
        for i in range(1, runs + 1):
            print(f"╠═  run {i}/{runs}…", flush=True)
            meta = await run_single_experiment(
                csv_path=csv_path,
                out_dir=db_out,
                run_idx=i,
                api_model=api_model,
                seed=base_seed + i - 1,  # seeds 42, 43, 44
                skip_mapping=skip_mapping,
                mapping_extension=mapping_extension,
            )
            all_meta.append(meta)
            status = meta["status"]
            tot    = meta.get("total_s", "-")
            print(f"╠═  run {i}: {status} ({tot}s)")
        # Summary agregado
        summary = {
            "db":          db,
            "api_model":   api_model,
            "runs":        runs,
            "ok":          sum(1 for m in all_meta if m["status"] == "ok"),
            "errors":      sum(1 for m in all_meta if m["status"] == "error"),
            "avg_total_s": round(
                sum(m.get("total_s", 0) for m in all_meta) / max(len(all_meta), 1),
                3),
            "runs_meta":   all_meta,
        }
        (db_out / "summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"╚═  summary → {db_out/'summary.json'}")

def parse_args():
    p = argparse.ArgumentParser(description="E4 – Pipeline OntoGenix sobre bases genéticas")
    p.add_argument("--databases", nargs="+", default=DEFAULT_DATABASES,
                   help="Bases de datos a ejecutar (default: %(default)s)")
    p.add_argument("--runs",      type=int, default=3,
                   help="Repeticiones por BBDD (default: 3)")
    p.add_argument("--model",     default="gpt-4o-2024-05-13",
                   help="Modelo OpenAI (default: gpt-4o-2024-05-13)")
    p.add_argument("--seed",      type=int, default=42,
                   help="Semilla base (se incrementa en cada run)")
    p.add_argument("--skip-mapping", action="store_true",
                   help="Saltar el paso 5 (OntoMapper) y generar solo la ontología")
    p.add_argument("--mapping-extension", default="ttl",
                   choices=["ttl", "yarrrml"],
                   help="Formato del mapping (default: ttl)")
    return p.parse_args()

def main():
    args = parse_args()
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    print("╔═════════════════════════════════════════════════════════════")
    print("║ EXPERIMENTO E4  –  OntoGenix pipeline")
    print(f"║ Bases de datos : {args.databases}")
    print(f"║ Modelo         : {args.model}")
    print(f"║ Repeticiones   : {args.runs}  (seeds {args.seed}…{args.seed+args.runs-1})")
    print(f"║ Mapping        : {'skip' if args.skip_mapping else args.mapping_extension}")
    print(f"║ Resultados     : {RESULTS_ROOT}")
    print("╚═════════════════════════════════════════════════════════════")
    asyncio.run(run_all(
        databases=args.databases,
        runs=args.runs,
        api_model=args.model,
        base_seed=args.seed,
        skip_mapping=args.skip_mapping,
        mapping_extension=args.mapping_extension,
    ))

if __name__ == "__main__":
    main()
