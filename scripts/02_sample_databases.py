#!/usr/bin/env python3
"""
02_sample_databases.py
Genera muestras representativas de cada base de datos para los experimentos con LLMs.

Estrategia de muestreo:
  1. Incluye las primeras N filas (estructura/cabecera)
  2. Muestreo aleatorio estratificado adicional
  3. Garantiza representación de todas las columnas con datos no nulos
  4. Limita el tamaño en tokens para caber en la ventana de contexto del LLM

Salida:
  - data/samples/{db_name}_sample.tsv     (muestra TSV)
  - data/samples/{db_name}_sample.txt     (formato texto para prompt)
  - data/samples/schemas/crm*.txt         (copia de esquemas de referencia)

Uso:
    python 02_sample_databases.py
    python 02_sample_databases.py --db dbSUPER --n-rows 25
"""

import pandas as pd
import numpy as np
import argparse
import shutil
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).parent))
from config import DATABASES, SCHEMAS, SCHEMA_EXAMPLES, PATHS, SAMPLING_PARAMS


def count_tokens_approx(text: str) -> int:
    """Estimación aproximada de tokens (1 token ≈ 4 caracteres)."""
    return len(text) // 4


def load_database_sample(db_name: str, n_header: int = 5,
                          n_sample: int = 20, seed: int = 42) -> pd.DataFrame:
    """
    Carga una muestra representativa de la base de datos.

    Args:
        db_name: Nombre de la base de datos
        n_header: Número de filas de cabecera (primeras filas)
        n_sample: Número de filas adicionales a muestrear
        seed: Semilla aleatoria

    Returns:
        DataFrame con la muestra
    """
    db_config = DATABASES[db_name]
    filepath = PATHS["processed_db"] / db_config["file"]

    if not filepath.exists():
        print(f"  ⚠️  Fichero no encontrado: {filepath}")
        return None

    # Cargar muestra grande para el muestreo estratificado
    print(f"  Cargando datos de {db_name}...")
    df = pd.read_csv(
        filepath,
        sep=db_config["separator"],
        header=0 if db_config["has_header"] else None,
        nrows=10000,  # Cargamos 10k para estratificar
        low_memory=False,
        on_bad_lines='skip'
    )

    print(f"  {len(df):,} filas disponibles para muestreo.")

    # Paso 1: Primeras N filas (siempre incluidas)
    header_sample = df.head(n_header)

    # Paso 2: Muestreo estratificado adicional
    # Intentamos cubrir diferentes valores en columnas clave
    remaining = df.iloc[n_header:]

    if len(remaining) == 0:
        return header_sample

    # Estratificar por tipo de CRM si existe, si no muestreo aleatorio
    np.random.seed(seed)

    stratify_cols = ["type", "enh_method", "source"]
    available_strat = [c for c in stratify_cols if c in df.columns]

    if available_strat and len(remaining) > n_sample:
        strat_col = available_strat[0]
        groups = remaining.groupby(strat_col, dropna=False)

        # Calcular cuántas filas por grupo
        n_groups = groups.ngroups
        per_group = max(1, n_sample // n_groups)

        sampled_groups = []
        for _, group_df in groups:
            n_take = min(per_group, len(group_df))
            sampled_groups.append(group_df.sample(n=n_take, random_state=seed))

        additional_sample = pd.concat(sampled_groups)

        # Si hay filas sobrantes, completar con muestra aleatoria
        if len(additional_sample) < n_sample:
            already_idx = additional_sample.index
            remaining_after = remaining[~remaining.index.isin(already_idx)]
            n_extra = n_sample - len(additional_sample)
            if len(remaining_after) > 0:
                extra = remaining_after.sample(
                    n=min(n_extra, len(remaining_after)),
                    random_state=seed
                )
                additional_sample = pd.concat([additional_sample, extra])
    else:
        additional_sample = remaining.sample(
            n=min(n_sample, len(remaining)),
            random_state=seed
        )

    sample = pd.concat([header_sample, additional_sample]).drop_duplicates()
    return sample


def format_sample_for_prompt(db_name: str, df: pd.DataFrame,
                              max_tokens: int = 3000) -> str:
    """
    Formatea una muestra de datos para incluirla en un prompt de LLM.

    Returns:
        Texto formateado con información del contexto y la muestra
    """
    db_config = DATABASES[db_name]
    lines = []

    lines.append(f"# Base de datos: {db_name}")
    lines.append(f"# Descripción: {db_config['description']}")
    lines.append(f"# Fuente: {db_config['url']}")
    lines.append(f"# Dimensiones totales: [ver informe de exploración]")
    lines.append(f"# Número de columnas: {len(df.columns)}")
    lines.append(f"# Filas en esta muestra: {len(df)}")
    lines.append("")
    lines.append("# MUESTRA DE DATOS (formato TSV):")
    lines.append("# Nota: '-' indica valor no disponible")
    lines.append("")

    # Convertir a texto TSV
    tsv_text = df.to_csv(sep='\t', index=False)

    # Verificar límite de tokens
    header_text = '\n'.join(lines)
    total_text = header_text + '\n' + tsv_text

    if count_tokens_approx(total_text) > max_tokens:
        # Reducir número de filas para cumplir el límite
        lines_tsv = tsv_text.split('\n')
        header_line = lines_tsv[0]
        data_lines = lines_tsv[1:]

        kept_lines = [header_line]
        current_tokens = count_tokens_approx(header_text + '\n' + header_line)

        for line in data_lines:
            line_tokens = count_tokens_approx(line)
            if current_tokens + line_tokens > max_tokens:
                break
            kept_lines.append(line)
            current_tokens += line_tokens

        tsv_text = '\n'.join(kept_lines)
        lines.append(f"# [Muestra reducida a {len(kept_lines)-1} filas por límite de tokens]")
        lines.append("")

    return '\n'.join(lines) + '\n' + tsv_text


def copy_schemas(dest_dir: Path) -> None:
    """Copia los esquemas de referencia al directorio de samples."""
    schema_dir = dest_dir / "schemas"
    schema_dir.mkdir(exist_ok=True)

    for schema_name, schema_file in SCHEMAS.items():
        src = PATHS["schemas"] / schema_file
        if src.exists():
            shutil.copy2(src, schema_dir / schema_file)
            print(f"  ✅ Schema copiado: {schema_file}")
        else:
            print(f"  ⚠️  Schema no encontrado: {src}")

    for schema_name, example_file in SCHEMA_EXAMPLES.items():
        src = PATHS["schemas"] / example_file
        if src.exists():
            shutil.copy2(src, schema_dir / example_file)
            print(f"  ✅ Ejemplo copiado: {example_file}")
        else:
            print(f"  ⚠️  Ejemplo no encontrado: {src}")


def generate_sample(db_name: str,
                    n_header: int = None,
                    n_sample: int = None,
                    max_tokens: int = None,
                    output_dir: Path = None) -> dict:
    """
    Genera y guarda la muestra de una base de datos.

    Returns:
        Diccionario con información de la muestra generada
    """
    n_header = n_header or SAMPLING_PARAMS["n_header_rows"]
    n_sample = n_sample or SAMPLING_PARAMS["n_sample_rows"]
    max_tokens = max_tokens or SAMPLING_PARAMS["max_tokens_data"]
    output_dir = output_dir or PATHS["samples"]
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'─'*50}")
    print(f"  Generando muestra: {db_name}")
    print(f"{'─'*50}")

    # Cargar muestra
    df_sample = load_database_sample(
        db_name,
        n_header=n_header,
        n_sample=n_sample,
        seed=SAMPLING_PARAMS["random_seed"]
    )

    if df_sample is None:
        return {"db_name": db_name, "error": "No se pudo cargar"}

    print(f"  Muestra generada: {len(df_sample)} filas × {len(df_sample.columns)} columnas")

    # Guardar muestra TSV
    tsv_path = output_dir / f"{db_name}_sample.tsv"
    df_sample.to_csv(tsv_path, sep='\t', index=False)
    print(f"  💾 TSV guardado: {tsv_path.name}")

    # Formatear para prompt
    prompt_text = format_sample_for_prompt(db_name, df_sample, max_tokens)
    txt_path = output_dir / f"{db_name}_sample_prompt.txt"
    txt_path.write_text(prompt_text, encoding='utf-8')
    print(f"  💾 Texto prompt guardado: {txt_path.name}")

    token_estimate = count_tokens_approx(prompt_text)
    print(f"  📊 Tokens estimados: ~{token_estimate:,}")

    # Análisis de completitud de la muestra
    null_mask = df_sample.isna() | (df_sample.astype(str) == '-') | (df_sample.astype(str) == '')
    completeness = (1 - null_mask.mean()).mean() * 100

    # Columnas con datos útiles
    useful_cols = []
    for col in df_sample.columns:
        valid_ratio = 1 - null_mask[col].mean()
        if valid_ratio > 0.1:  # Al menos 10% de datos válidos
            useful_cols.append(col)

    print(f"  📋 Completitud de la muestra: {completeness:.1f}%")
    print(f"  📋 Columnas con datos útiles (>10%): {len(useful_cols)}/{len(df_sample.columns)}")
    print(f"     {useful_cols[:10]}{'...' if len(useful_cols) > 10 else ''}")

    return {
        "db_name": db_name,
        "n_rows_sample": len(df_sample),
        "n_cols": len(df_sample.columns),
        "completeness_pct": round(completeness, 1),
        "token_estimate": token_estimate,
        "useful_columns": useful_cols,
        "tsv_path": str(tsv_path),
        "prompt_path": str(txt_path),
    }


def main():
    parser = argparse.ArgumentParser(
        description='Generación de muestras de bases de datos CRM para experimentos LLM'
    )
    parser.add_argument(
        '--db',
        choices=list(DATABASES.keys()) + ['all'],
        default='all',
        help='Base de datos a muestrear (default: all)'
    )
    parser.add_argument(
        '--n-rows',
        type=int,
        default=None,
        help=f'Número de filas de muestra (default: {SAMPLING_PARAMS["n_sample_rows"]})'
    )
    parser.add_argument(
        '--max-tokens',
        type=int,
        default=None,
        help=f'Límite de tokens para el prompt (default: {SAMPLING_PARAMS["max_tokens_data"]})'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Directorio de salida (default: data/samples/)'
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else PATHS["samples"]

    print("\n" + "="*60)
    print("  GENERACIÓN DE MUESTRAS - TFM ONTOLOGÍAS CON LLMs")
    print("="*60)
    print(f"\n  Directorio de salida: {output_dir}")

    # Selección de bases de datos
    if args.db == 'all':
        dbs_to_sample = [db for db in DATABASES.keys()
                         if (PATHS["processed_db"] / DATABASES[db]["file"]).exists()]
    else:
        dbs_to_sample = [args.db]

    print(f"  Bases de datos: {dbs_to_sample}")

    # Copiar esquemas de referencia
    print(f"\n{'─'*50}")
    print("  Copiando esquemas de referencia...")
    print(f"{'─'*50}")
    copy_schemas(output_dir)

    # Generar muestras
    all_results = {}
    for db_name in dbs_to_sample:
        result = generate_sample(
            db_name,
            n_sample=args.n_rows,
            max_tokens=args.max_tokens,
            output_dir=output_dir
        )
        all_results[db_name] = result

    # Guardar metadatos
    metadata_path = output_dir / "sampling_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    # Resumen final
    print(f"\n\n{'='*60}")
    print("  RESUMEN DE MUESTRAS GENERADAS")
    print(f"{'='*60}")
    print(f"{'Base de datos':<18} {'Filas':>6} {'Tokens':>7} {'Completi.':>9} {'Cols útiles':>11}")
    print(f"{'-'*18} {'-'*6} {'-'*7} {'-'*9} {'-'*11}")

    for db_name, result in all_results.items():
        if "error" in result:
            print(f"{db_name:<18} ERROR")
            continue
        print(
            f"{db_name:<18} "
            f"{result['n_rows_sample']:>6} "
            f"{result['token_estimate']:>7,} "
            f"{result['completeness_pct']:>8.1f}% "
            f"{len(result['useful_columns']):>11}"
        )

    print(f"\n✅ Muestras guardadas en: {output_dir}")
    print(f"✅ Metadatos guardados en: {metadata_path}")
    print(f"\n   Próximo paso: ejecuta '03_test_llm_connection.py' para")
    print(f"   verificar la conectividad con los modelos LLM.\n")


if __name__ == "__main__":
    main()
