#!/usr/bin/env python3
"""
05_evaluate_results.py
Evaluación de las ontologías generadas por los LLMs.

Métricas calculadas:
  - Validez sintáctica Turtle (VS): ¿es parseable por rdflib?
  - Nº de tripletas generadas
  - Precisión de clases (P_c): clases generadas que coinciden con referencia
  - Recall de clases (R_c): clases referencia presentes en generada
  - F1 de clases (F1_c)
  - Precisión de propiedades (P_p), Recall (R_p), F1 (F1_p)
  - Tasa de mappings correctos (M): skos:exactMatch/closeMatch vs referencia
  - Cobertura de anotaciones (CA): % clases con skos:prefLabel y definition

Salida:
  results/evaluation/
    ├── metrics_all.csv          # Métricas por experimento/BD/modelo/run
    ├── metrics_summary.csv      # Medias por experimento/BD/modelo
    └── evaluation_report.json   # Informe completo

Uso:
    python 05_evaluate_results.py
    python 05_evaluate_results.py --experiment E1 --model llama3.1:8b
"""

import sys
import json
import csv
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from config import DATABASES, SCHEMAS, LLM_MODELS, EXPERIMENTS, PATHS


# ─── Carga de ontologías ──────────────────────────────────────────────────────

def parse_turtle_safe(turtle_text: str) -> Optional[object]:
    """Parsea Turtle con rdflib, devuelve None si falla."""
    try:
        import rdflib
        g = rdflib.Graph()
        g.parse(data=turtle_text, format="turtle")
        return g
    except Exception:
        return None


def load_reference_ontology(schema_names: list = None) -> Optional[object]:
    """Carga la ontología de referencia cisreg."""
    try:
        import rdflib
        g = rdflib.Graph()
        schema_names = schema_names or list(SCHEMAS.keys())

        for schema_name in schema_names:
            schema_path = PATHS["schemas"] / SCHEMAS[schema_name]
            if schema_path.exists():
                try:
                    g.parse(source=str(schema_path), format="turtle")
                except Exception as e:
                    print(f"  ⚠️  Error cargando schema {schema_name}: {e}")
        return g if len(g) > 0 else None
    except ImportError:
        return None


# ─── Extracción de términos ontológicos ───────────────────────────────────────

def extract_classes(graph) -> set:
    """Extrae las clases OWL de un grafo."""
    try:
        import rdflib
        OWL = rdflib.OWL
        RDF = rdflib.RDF
        RDFS = rdflib.RDFS

        classes = set()

        # owl:Class declarations
        for s in graph.subjects(RDF.type, OWL.Class):
            classes.add(str(s))

        # rdfs:Class declarations
        for s in graph.subjects(RDF.type, RDFS.Class):
            classes.add(str(s))

        # Subjects of rdfs:subClassOf
        for s, o in graph.subject_objects(RDFS.subClassOf):
            classes.add(str(s))

        return classes
    except Exception:
        return set()


def extract_properties(graph) -> set:
    """Extrae las propiedades OWL de un grafo."""
    try:
        import rdflib
        OWL = rdflib.OWL
        RDF = rdflib.RDF

        properties = set()
        for prop_type in [OWL.ObjectProperty, OWL.DatatypeProperty,
                          OWL.AnnotationProperty, rdflib.RDF.Property]:
            for s in graph.subjects(RDF.type, prop_type):
                properties.add(str(s))
        return properties
    except Exception:
        return set()


def extract_mappings(graph) -> set:
    """Extrae los mappings skos:exactMatch y skos:closeMatch."""
    try:
        import rdflib
        SKOS = rdflib.namespace.SKOS

        mappings = set()
        for pred in [SKOS.exactMatch, SKOS.closeMatch]:
            for s, o in graph.subject_objects(pred):
                mappings.add((str(s), str(pred), str(o)))
        return mappings
    except Exception:
        return set()


def extract_labels(graph) -> dict:
    """Extrae las etiquetas skos:prefLabel de un grafo."""
    try:
        import rdflib
        SKOS = rdflib.namespace.SKOS

        labels = {}
        for s, o in graph.subject_objects(SKOS.prefLabel):
            labels[str(s)] = str(o)
        return labels
    except Exception:
        return {}


def normalize_uri(uri: str) -> str:
    """Normaliza una URI para comparación (elimina fragmentos y versiones)."""
    # Extraer la parte local de la URI
    if '#' in uri:
        return uri.split('#')[-1].lower()
    if '/' in uri:
        return uri.split('/')[-1].lower()
    return uri.lower()


def fuzzy_match(set1: set, set2: set, threshold: float = 0.7) -> tuple:
    """
    Calcula coincidencias aproximadas entre dos conjuntos de URIs.
    Usa coincidencia exacta primero, luego por etiqueta normalizada.
    """
    # Exactas
    exact = set1 & set2

    # Normalizadas
    norm1 = {normalize_uri(u): u for u in set1}
    norm2 = {normalize_uri(u): u for u in set2}
    fuzzy = set(norm1.keys()) & set(norm2.keys())

    matched = len(exact) + len(fuzzy - {normalize_uri(u) for u in exact})
    return matched, exact, fuzzy


# ─── Cálculo de métricas ──────────────────────────────────────────────────────

def calculate_metrics(generated_graph, reference_graph) -> dict:
    """
    Calcula todas las métricas de evaluación entre una ontología
    generada y la ontología de referencia.
    """
    if generated_graph is None:
        return {
            "valid_turtle": False,
            "n_triples": 0,
            "error": "No se pudo parsear el Turtle generado",
        }

    metrics = {
        "valid_turtle": True,
        "n_triples": len(generated_graph),
    }

    # Extraer términos de ambas ontologías
    gen_classes = extract_classes(generated_graph)
    gen_props   = extract_properties(generated_graph)
    gen_mappings = extract_mappings(generated_graph)
    gen_labels  = extract_labels(generated_graph)

    metrics["n_classes_generated"] = len(gen_classes)
    metrics["n_properties_generated"] = len(gen_props)
    metrics["n_mappings_generated"] = len(gen_mappings)

    if reference_graph is None:
        # Sin referencia, solo estadísticas básicas
        metrics["n_classes_ref"] = 0
        metrics["coverage_annotations"] = (
            len(gen_labels) / len(gen_classes) * 100
            if gen_classes else 0
        )
        return metrics

    ref_classes  = extract_classes(reference_graph)
    ref_props    = extract_properties(reference_graph)
    ref_mappings = extract_mappings(reference_graph)

    metrics["n_classes_ref"] = len(ref_classes)
    metrics["n_properties_ref"] = len(ref_props)
    metrics["n_mappings_ref"] = len(ref_mappings)

    # ── Métricas de clases ──
    matched_classes, _, _ = fuzzy_match(gen_classes, ref_classes)
    metrics["classes_matched"] = matched_classes
    metrics["precision_classes"] = (
        matched_classes / len(gen_classes) if gen_classes else 0
    )
    metrics["recall_classes"] = (
        matched_classes / len(ref_classes) if ref_classes else 0
    )
    p, r = metrics["precision_classes"], metrics["recall_classes"]
    metrics["f1_classes"] = (
        2 * p * r / (p + r) if (p + r) > 0 else 0
    )

    # ── Métricas de propiedades ──
    matched_props, _, _ = fuzzy_match(gen_props, ref_props)
    metrics["properties_matched"] = matched_props
    metrics["precision_properties"] = (
        matched_props / len(gen_props) if gen_props else 0
    )
    metrics["recall_properties"] = (
        matched_props / len(ref_props) if ref_props else 0
    )
    p, r = metrics["precision_properties"], metrics["recall_properties"]
    metrics["f1_properties"] = (
        2 * p * r / (p + r) if (p + r) > 0 else 0
    )

    # ── Métricas de mappings ──
    if ref_mappings:
        # Normalizar mappings para comparación
        ref_mapping_pairs = {(normalize_uri(s), normalize_uri(o))
                             for s, pred, o in ref_mappings}
        gen_mapping_pairs = {(normalize_uri(s), normalize_uri(o))
                             for s, pred, o in gen_mappings}
        matched_mappings = len(ref_mapping_pairs & gen_mapping_pairs)
        metrics["mappings_matched"] = matched_mappings
        metrics["mapping_precision"] = (
            matched_mappings / len(gen_mapping_pairs) if gen_mapping_pairs else 0
        )
        metrics["mapping_recall"] = (
            matched_mappings / len(ref_mapping_pairs) if ref_mapping_pairs else 0
        )
    else:
        metrics["mappings_matched"] = 0
        metrics["mapping_precision"] = 0
        metrics["mapping_recall"] = 0

    # ── Cobertura de anotaciones ──
    metrics["n_with_label"] = len(gen_labels)
    metrics["coverage_annotations"] = (
        len(gen_labels) / len(gen_classes) * 100
        if gen_classes else 0
    )

    # ── Puntuación global (media armónica de F1_c, F1_p, mapping_recall) ──
    scores = [
        metrics["f1_classes"],
        metrics["f1_properties"],
        metrics["mapping_recall"],
    ]
    valid_scores = [s for s in scores if s > 0]
    metrics["global_score"] = (
        len(valid_scores) / sum(1/s for s in valid_scores)
        if valid_scores else 0
    )

    # Redondear a 4 decimales
    for key in ["precision_classes", "recall_classes", "f1_classes",
                "precision_properties", "recall_properties", "f1_properties",
                "mapping_precision", "mapping_recall", "coverage_annotations",
                "global_score"]:
        if key in metrics:
            metrics[key] = round(metrics[key], 4)

    return metrics


# ─── Evaluación de ficheros ───────────────────────────────────────────────────

def evaluate_ontology_file(ttl_path: Path, reference_graph) -> dict:
    """Evalúa un fichero de ontología generada."""
    if not ttl_path.exists():
        return {"error": f"Fichero no encontrado: {ttl_path}"}

    turtle_text = ttl_path.read_text(encoding='utf-8', errors='replace')
    generated_graph = parse_turtle_safe(turtle_text)

    metrics = calculate_metrics(generated_graph, reference_graph)
    metrics["file"] = str(ttl_path)

    return metrics


def find_result_files(base_dir: Path, experiment: str = None,
                       model: str = None) -> list:
    """Encuentra todos los ficheros de ontología generada."""
    pattern = "ontology_run*.ttl"
    results = []

    if experiment:
        exp_dirs = [base_dir / experiment]
    else:
        exp_dirs = [d for d in base_dir.iterdir() if d.is_dir()
                    and d.name in EXPERIMENTS]

    for exp_dir in exp_dirs:
        if not exp_dir.exists():
            continue
        for db_dir in exp_dir.iterdir():
            if not db_dir.is_dir():
                continue
            for model_dir in db_dir.iterdir():
                if not model_dir.is_dir():
                    continue
                # Saltar carpetas de backup/respaldo (no son corridas activas)
                low = model_dir.name.lower()
                if any(s in low for s in ("failed", "backup", "_v1", "_old",
                                          "archive")):
                    continue
                if model and model.replace(':', '_') not in model_dir.name:
                    continue
                for ttl_file in model_dir.glob(pattern):
                    results.append({
                        "experiment": exp_dir.name,
                        "db_name": db_dir.name,
                        "model": model_dir.name.replace('_', ':'),
                        "run": int(ttl_file.stem.replace('ontology_run', '')),
                        "ttl_path": ttl_file,
                    })

    return sorted(results, key=lambda x: (x["experiment"], x["db_name"],
                                           x["model"], x["run"]))


def main():
    parser = argparse.ArgumentParser(
        description='Evaluación de ontologías generadas por LLMs'
    )
    parser.add_argument('--experiment', choices=list(EXPERIMENTS.keys()),
                        default=None, help='Filtrar por experimento')
    parser.add_argument('--model', choices=list(LLM_MODELS.keys()),
                        default=None, help='Filtrar por modelo')
    parser.add_argument('--results-dir', type=str, default=None,
                        help='Directorio de resultados')
    args = parser.parse_args()

    results_dir = Path(args.results_dir) if args.results_dir else PATHS["results"]
    eval_dir = results_dir / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("  EVALUACIÓN DE ONTOLOGÍAS GENERADAS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Cargar ontología de referencia
    print("\n  Cargando ontología de referencia cisreg...")
    reference_graph = load_reference_ontology()
    if reference_graph:
        ref_classes = extract_classes(reference_graph)
        ref_props = extract_properties(reference_graph)
        print(f"  ✅ Referencia cargada: {len(reference_graph)} tripletas, "
              f"{len(ref_classes)} clases, {len(ref_props)} propiedades")
    else:
        print("  ⚠️  No se pudo cargar la ontología de referencia")
        print("     (verifica que rdflib está instalado: pip install rdflib)")
        print("     Se calcularán solo métricas básicas.")

    # Encontrar ficheros de resultados
    result_files = find_result_files(results_dir, args.experiment, args.model)
    if not result_files:
        print(f"\n  ⚠️  No se encontraron ontologías en: {results_dir}")
        print("     Ejecuta primero: python 04_run_experiments.py")
        return

    print(f"\n  Evaluando {len(result_files)} ontología(s)...\n")

    # Evaluación
    all_metrics = []
    for file_info in result_files:
        print(f"  {file_info['experiment']} | {file_info['db_name']} | "
              f"{file_info['model']} | Run {file_info['run']}... ", end='', flush=True)

        metrics = evaluate_ontology_file(file_info["ttl_path"], reference_graph)

        record = {**file_info, **metrics}
        record.pop("ttl_path", None)
        all_metrics.append(record)

        if metrics.get("valid_turtle"):
            score = metrics.get("global_score", 0)
            f1c = metrics.get("f1_classes", 0)
            f1p = metrics.get("f1_properties", 0)
            print(f"✅ F1c={f1c:.3f} F1p={f1p:.3f} Score={score:.3f}")
        else:
            print(f"❌ Turtle inválido")

    # Guardar CSV con todas las métricas
    if all_metrics:
        csv_path = eval_dir / "metrics_all.csv"
        # Unión de todas las claves: registros con error tienen claves extra
        # ('error') que no aparecen en los registros válidos.
        fieldnames: list[str] = []
        seen: set[str] = set()
        for record in all_metrics:
            for k in record.keys():
                if k not in seen:
                    seen.add(k)
                    fieldnames.append(k)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames,
                                     extrasaction='ignore')
            writer.writeheader()
            writer.writerows(all_metrics)
        print(f"\n  💾 CSV guardado: {csv_path}")

        # Calcular medias por experimento/BD/modelo
        summary = {}
        numeric_keys = ["n_triples", "f1_classes", "f1_properties",
                        "mapping_recall", "global_score", "coverage_annotations"]

        for record in all_metrics:
            key = (record["experiment"], record["db_name"], record["model"])
            if key not in summary:
                summary[key] = {"count": 0, **{k: [] for k in numeric_keys},
                                 "n_valid": 0}
            summary[key]["count"] += 1
            if record.get("valid_turtle"):
                summary[key]["n_valid"] += 1
            for k in numeric_keys:
                if k in record and record[k] is not None:
                    summary[key][k].append(float(record[k]))

        summary_rows = []
        for (exp, db, model), data in summary.items():
            row = {"experiment": exp, "db_name": db, "model": model,
                   "n_runs": data["count"], "n_valid": data["n_valid"]}
            for k in numeric_keys:
                vals = data[k]
                row[f"avg_{k}"] = round(sum(vals) / len(vals), 4) if vals else None
                row[f"std_{k}"] = round(
                    (sum((v - row[f"avg_{k}"]) ** 2 for v in vals) / len(vals)) ** 0.5, 4
                ) if len(vals) > 1 else 0
            summary_rows.append(row)

        summary_csv = eval_dir / "metrics_summary.csv"
        if summary_rows:
            with open(summary_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
                writer.writeheader()
                writer.writerows(summary_rows)
            print(f"  💾 Resumen guardado: {summary_csv}")

        # JSON completo
        json_path = eval_dir / "evaluation_report.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "n_ontologies_evaluated": len(all_metrics),
                "n_valid_turtle": sum(1 for m in all_metrics if m.get("valid_turtle")),
                "metrics_detail": all_metrics,
                "summary": summary_rows,
            }, f, indent=2, ensure_ascii=False, default=str)
        print(f"  💾 Informe JSON: {json_path}")

    # Tabla resumen en consola
    print(f"\n{'='*80}")
    print("  RESUMEN DE EVALUACIÓN")
    print(f"{'='*80}")
    if summary_rows:
        print(f"{'Exp':<4} {'BD':<18} {'Modelo':<16} "
              f"{'Valid':>5} {'F1-c':>6} {'F1-p':>6} {'MapR':>6} {'Score':>6}")
        print(f"{'-'*4} {'-'*18} {'-'*16} {'-'*5} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")
        for row in summary_rows:
            model_short = row["model"].split(':')[0][-12:]
            print(
                f"{row['experiment']:<4} "
                f"{row['db_name']:<18} "
                f"{model_short:<16} "
                f"{row['n_valid']}/{row['n_runs']:>2} "
                f"{row.get('avg_f1_classes', 0) or 0:>6.3f} "
                f"{row.get('avg_f1_properties', 0) or 0:>6.3f} "
                f"{row.get('avg_mapping_recall', 0) or 0:>6.3f} "
                f"{row.get('avg_global_score', 0) or 0:>6.3f}"
            )

    print(f"\n  Resultados completos en: {eval_dir}\n")


if __name__ == "__main__":
    main()
