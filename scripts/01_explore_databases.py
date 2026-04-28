#!/usr/bin/env python3
"""
01_explore_databases.py
Exploración y análisis estadístico de todas las bases de datos CRM disponibles.

Genera un informe detallado con:
- Dimensiones (filas × columnas)
- Valores únicos por columna
- Completitud de datos (% de valores no nulos)
- Distribución de tipos de CRM y métodos de evidencia
- Muestras representativas de cada base de datos

Uso:
    python 01_explore_databases.py
    python 01_explore_databases.py --db dbSUPER
    python 01_explore_databases.py --output results/exploration_report.json
"""

import pandas as pd
import numpy as np
import json
import argparse
from pathlib import Path
import sys
import warnings
warnings.filterwarnings('ignore')

# Añadir directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))
from config import DATABASES, PATHS


def load_database(db_name: str, nrows: int = None) -> pd.DataFrame:
    """Carga una base de datos desde el fichero TSV."""
    db_config = DATABASES[db_name]
    filepath = PATHS["processed_db"] / db_config["file"]

    if not filepath.exists():
        print(f"  ⚠️  Fichero no encontrado: {filepath}")
        return None

    df = pd.read_csv(
        filepath,
        sep=db_config["separator"],
        header=0 if db_config["has_header"] else None,
        nrows=nrows,
        low_memory=False,
        on_bad_lines='skip'
    )
    return df


def analyze_column(series: pd.Series) -> dict:
    """Análisis estadístico de una columna."""
    total = len(series)
    null_mask = series.isna() | (series.astype(str) == '-') | (series.astype(str) == '')
    n_missing = null_mask.sum()
    n_valid = total - n_missing

    result = {
        "total": total,
        "missing": int(n_missing),
        "missing_pct": round(n_missing / total * 100, 1) if total > 0 else 0,
        "valid": int(n_valid),
        "completeness_pct": round(n_valid / total * 100, 1) if total > 0 else 0,
    }

    if n_valid > 0:
        valid_series = series[~null_mask]
        result["n_unique"] = int(valid_series.nunique())

        # Top 5 valores más frecuentes
        top_values = valid_series.value_counts().head(5)
        result["top_values"] = {str(k): int(v) for k, v in top_values.items()}

        # Tipo inferido
        try:
            pd.to_numeric(valid_series)
            result["inferred_type"] = "numeric"
            result["min"] = str(valid_series.min())
            result["max"] = str(valid_series.max())
        except (ValueError, TypeError):
            result["inferred_type"] = "string"
            result["avg_length"] = round(valid_series.astype(str).str.len().mean(), 1)

    return result


def analyze_database(db_name: str) -> dict:
    """Análisis completo de una base de datos."""
    print(f"\n{'='*60}")
    print(f"  Analizando: {db_name}")
    print(f"{'='*60}")

    db_config = DATABASES[db_name]
    filepath = PATHS["processed_db"] / db_config["file"]

    if not filepath.exists():
        return {"error": f"Fichero no encontrado: {filepath}"}

    # Tamaño del fichero
    file_size_mb = filepath.stat().st_size / (1024 * 1024)

    # Carga completa (cabecera + primera muestra para análisis rápido)
    print(f"  Cargando datos... ({file_size_mb:.1f} MB)")

    # Contar líneas sin cargar todo en memoria
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        total_lines = sum(1 for _ in f)
    n_rows = total_lines - (1 if db_config["has_header"] else 0)

    # Cargar muestra representativa para análisis
    sample_size = min(10000, n_rows)
    df_full = load_database(db_name, nrows=sample_size + 1)

    if df_full is None:
        return {"error": "No se pudo cargar la base de datos"}

    n_cols = len(df_full.columns)
    print(f"  Dimensiones: {n_rows:,} filas × {n_cols} columnas")
    print(f"  Tamaño fichero: {file_size_mb:.2f} MB")

    # Análisis por columna
    print(f"  Analizando {n_cols} columnas...")
    columns_analysis = {}
    for col in df_full.columns:
        columns_analysis[col] = analyze_column(df_full[col])

    # Estadísticas de completitud global
    completeness_values = [v["completeness_pct"] for v in columns_analysis.values()]

    # Análisis de tipos de CRM y métodos
    type_dist = {}
    method_dist = {}
    biosample_dist = {}

    if "type" in df_full.columns:
        type_dist = df_full["type"].value_counts().head(10).to_dict()
    if "enh_method" in df_full.columns:
        method_dist = df_full["enh_method"].value_counts().head(10).to_dict()
    if "biosample_name" in df_full.columns:
        biosample_dist = df_full["biosample_name"].value_counts().head(10).to_dict()
    elif "biosample" in df_full.columns:
        biosample_dist = df_full["biosample"].value_counts().head(10).to_dict()

    # Cobertura de genes diana
    gene_coverage = 0
    if "hgnc_symbol_target_genes" in df_full.columns:
        gene_mask = ~(df_full["hgnc_symbol_target_genes"].isna() |
                      (df_full["hgnc_symbol_target_genes"] == '-'))
        gene_coverage = round(gene_mask.sum() / len(df_full) * 100, 1)

    # Cobertura de enfermedades
    disease_coverage = 0
    if "disease" in df_full.columns:
        disease_mask = ~(df_full["disease"].isna() |
                         (df_full["disease"] == '-'))
        disease_coverage = round(disease_mask.sum() / len(df_full) * 100, 1)

    # Cobertura de TFs
    tf_coverage = 0
    for tf_col in ["hgnc_symbol_TFs", "uniprot_TFs"]:
        if tf_col in df_full.columns:
            tf_mask = ~(df_full[tf_col].isna() | (df_full[tf_col] == '-'))
            tf_coverage = round(tf_mask.sum() / len(df_full) * 100, 1)
            break

    result = {
        "db_name": db_name,
        "description": db_config["description"],
        "url": db_config["url"],
        "file_size_mb": round(file_size_mb, 2),
        "n_rows": n_rows,
        "n_cols": n_cols,
        "columns": list(df_full.columns),
        "analysis_sample_size": sample_size,
        "completeness": {
            "avg_completeness_pct": round(np.mean(completeness_values), 1),
            "min_completeness_pct": round(min(completeness_values), 1),
            "max_completeness_pct": round(max(completeness_values), 1),
            "gene_coverage_pct": gene_coverage,
            "disease_coverage_pct": disease_coverage,
            "tf_coverage_pct": tf_coverage,
        },
        "distributions": {
            "crm_types": type_dist,
            "evidence_methods": method_dist,
            "top_biosamples": biosample_dist,
        },
        "columns_analysis": columns_analysis,
    }

    # Imprimir resumen
    print(f"\n  📊 RESUMEN:")
    print(f"     Filas totales:        {n_rows:>12,}")
    print(f"     Columnas:             {n_cols:>12}")
    print(f"     Completitud media:    {result['completeness']['avg_completeness_pct']:>11.1f}%")
    print(f"     Cobertura genes:      {gene_coverage:>11.1f}%")
    print(f"     Cobertura enfermed.:  {disease_coverage:>11.1f}%")
    print(f"     Cobertura TFs:        {tf_coverage:>11.1f}%")

    if type_dist:
        print(f"\n  📋 Tipos de CRM:")
        for t, count in list(type_dist.items())[:5]:
            print(f"     {str(t):<30} {count:>8,}")

    if method_dist:
        print(f"\n  🔬 Métodos de evidencia:")
        for m, count in list(method_dist.items())[:5]:
            print(f"     {str(m):<30} {count:>8,}")

    return result


def generate_comparison_table(all_results: dict) -> None:
    """Genera tabla comparativa de todas las bases de datos."""
    print(f"\n\n{'='*80}")
    print("  TABLA COMPARATIVA DE BASES DE DATOS")
    print(f"{'='*80}")
    print(f"{'Base de datos':<18} {'Filas':>10} {'MB':>6} {'Completi.':>9} {'Genes%':>7} {'Enf.%':>6} {'TF%':>5}")
    print(f"{'-'*18} {'-'*10} {'-'*6} {'-'*9} {'-'*7} {'-'*6} {'-'*5}")

    for db_name, result in all_results.items():
        if "error" in result:
            print(f"{db_name:<18} ERROR: {result['error']}")
            continue

        c = result["completeness"]
        print(
            f"{db_name:<18} "
            f"{result['n_rows']:>10,} "
            f"{result['file_size_mb']:>6.1f} "
            f"{c['avg_completeness_pct']:>8.1f}% "
            f"{c['gene_coverage_pct']:>6.1f}% "
            f"{c['disease_coverage_pct']:>5.1f}% "
            f"{c['tf_coverage_pct']:>4.1f}%"
        )


def main():
    parser = argparse.ArgumentParser(
        description='Exploración y análisis de bases de datos CRM'
    )
    parser.add_argument(
        '--db',
        choices=list(DATABASES.keys()) + ['all'],
        default='all',
        help='Base de datos a analizar (default: all)'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Fichero de salida JSON (default: results/01_exploration_report.json)'
    )
    args = parser.parse_args()

    output_path = args.output or str(PATHS["results"] / "01_exploration_report.json")

    print("\n" + "="*60)
    print("  EXPLORACIÓN DE BASES DE DATOS CRM")
    print("  TFM: Generación de Ontologías con LLMs")
    print("="*60)
    print(f"\n  Data root: {PATHS['processed_db']}")

    # Verificar que existen los ficheros
    missing = []
    for db_name, config in DATABASES.items():
        fp = PATHS["processed_db"] / config["file"]
        if not fp.exists():
            missing.append(db_name)

    if missing:
        print(f"\n  ⚠️  Bases de datos no encontradas: {missing}")
        print(f"     Verifica que la ruta es correcta: {PATHS['processed_db']}")

    # Selección de bases de datos a analizar
    if args.db == 'all':
        dbs_to_analyze = [db for db in DATABASES.keys()
                          if (PATHS["processed_db"] / DATABASES[db]["file"]).exists()]
    else:
        dbs_to_analyze = [args.db]

    print(f"\n  Analizando {len(dbs_to_analyze)} base(s) de datos: {dbs_to_analyze}\n")

    # Análisis
    all_results = {}
    for db_name in dbs_to_analyze:
        all_results[db_name] = analyze_database(db_name)

    # Tabla comparativa
    generate_comparison_table(all_results)

    # Guardar resultados
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n\n✅ Informe guardado en: {output_path}")
    print(f"\n   Próximo paso: ejecuta '02_sample_databases.py' para generar")
    print(f"   las muestras que se usarán en los experimentos con LLMs.\n")

    return all_results


if __name__ == "__main__":
    main()
