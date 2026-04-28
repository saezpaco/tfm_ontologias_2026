#!/usr/bin/env python3
"""
setup_check.py
Verifica que el entorno está correctamente configurado para los experimentos GPT.

Comprueba:
  1. Versión de Python (>= 3.10)
  2. Paquetes necesarios (openai, rdflib)
  3. API Key de OpenAI (configurable o en entorno)
  4. Muestras de datos disponibles
  5. Conectividad con la API de OpenAI (llamada mínima de prueba)

Uso:
  python setup_check.py
  python setup_check.py --api-key "sk-..."
  python setup_check.py --skip-api-test  # Solo verifica paquetes y datos
"""

import sys
import os
import argparse
from pathlib import Path

def check(label: str, ok: bool, detail: str = ""):
    icon = "✅" if ok else "❌"
    line = f"  {icon}  {label}"
    if detail:
        line += f"  →  {detail}"
    print(line)
    return ok


def main():
    parser = argparse.ArgumentParser(description="Verificación del entorno TFM")
    parser.add_argument('--api-key',       type=str, default=None)
    parser.add_argument('--skip-api-test', action='store_true',
                        help='No llamar a la API (solo verificar paquetes y datos)')
    args = parser.parse_args()

    print("\n" + "="*55)
    print("  VERIFICACIÓN DEL ENTORNO - TFM Ontologías CRM")
    print("="*55 + "\n")

    all_ok = True

    # ── 1. Python ─────────────────────────────────────────────────────────────
    ver = sys.version_info
    py_ok = ver >= (3, 10)
    all_ok &= check(
        f"Python {ver.major}.{ver.minor}.{ver.micro}",
        py_ok,
        "OK" if py_ok else "Se requiere Python >= 3.10"
    )

    # ── 2. Paquetes ───────────────────────────────────────────────────────────
    print()

    try:
        import openai
        check("openai", True, openai.__version__)
    except ImportError:
        check("openai", False, "No instalado → pip install openai")
        all_ok = False

    try:
        import rdflib
        check("rdflib", True, rdflib.__version__)
    except ImportError:
        check("rdflib", False, "No instalado (opcional) → pip install rdflib")
        # rdflib es opcional, no bloqueante

    # ── 3. Config y rutas ────────────────────────────────────────────────────
    print()
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from config import PATHS, DATABASES
        check("config.py", True, "Importado correctamente")
    except Exception as e:
        check("config.py", False, str(e))
        all_ok = False
        print("\n  ❌ Sin config.py no se puede continuar.")
        sys.exit(1)

    samples_dir = PATHS["samples"]
    check(
        f"Directorio de muestras",
        samples_dir.exists(),
        str(samples_dir)
    )

    # ── 4. Muestras de datos ──────────────────────────────────────────────────
    print()
    print("  Muestras disponibles:")
    n_samples = 0
    for db_name in DATABASES.keys():
        sample_path = samples_dir / f"{db_name}_sample_prompt.txt"
        exists = sample_path.exists()
        size = f"{sample_path.stat().st_size // 1024} KB" if exists else ""
        check(f"  {db_name}", exists, size)
        if exists:
            n_samples += 1

    check(
        f"Total muestras",
        n_samples > 0,
        f"{n_samples}/{len(DATABASES)} bases de datos"
    )
    all_ok &= n_samples > 0

    # ── 5. API Key ────────────────────────────────────────────────────────────
    print()
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")

    # Buscar en .env
    if not api_key:
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    if api_key:
        masked = f"sk-...{api_key[-4:]}"
        check("OPENAI_API_KEY", True, masked)
    else:
        check("OPENAI_API_KEY", False,
              "No encontrada → export OPENAI_API_KEY='sk-...' o usar --api-key")
        all_ok = False

    # ── 6. Test de conexión a la API ──────────────────────────────────────────
    if api_key and not args.skip_api_test:
        print()
        print("  Test de conexión a OpenAI API...")
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            # Llamada mínima: 1 token para verificar credenciales
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say: OK"}],
                max_tokens=5,
            )
            reply = response.choices[0].message.content.strip()
            check("Conexión API OpenAI", True, f"Respuesta: '{reply}'")
            check("Modelo gpt-4o-mini", True, "Accesible")
        except openai.AuthenticationError:
            check("Conexión API OpenAI", False, "API Key inválida o sin permisos")
            all_ok = False
        except Exception as e:
            check("Conexión API OpenAI", False, str(e)[:80])
            all_ok = False
    elif args.skip_api_test:
        print()
        print("  ⏭️  Test de API omitido (--skip-api-test)")

    # ── Resultado final ───────────────────────────────────────────────────────
    print()
    print("="*55)
    if all_ok:
        print("  ✅ Entorno configurado correctamente.")
        print()
        print("  Siguiente paso — prueba de validación (dry-run):")
        print("  python run_gpt_experiments.py --dry-run")
        print()
        print("  Primera prueba real (barata, ~$0.001):")
        print("  python run_gpt_experiments.py --model gpt-4o-mini --experiment E1 --db dbSUPER")
    else:
        print("  ⚠️  Hay problemas que resolver antes de lanzar experimentos.")
        print()
        if not api_key:
            print("  → Configura la API key:")
            print("    export OPENAI_API_KEY='sk-...'")
            print("    # o añade al archivo TFM/.env:")
            print("    echo 'OPENAI_API_KEY=sk-...' > TFM/.env")
        print()
        print("  Para instalar paquetes faltantes:")
        print("  pip install openai rdflib")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()
