#!/usr/bin/env python3
"""
preflight_check.py
──────────────────
Verifica que TODO el entorno local necesario para lanzar las fases del banco
está levantado y operativo, ANTES de ejecutar experimentos. Comprueba:

  1. Python y paquetes (rdflib, owlready2, pandas, openai, requests, numpy …)
  2. Java (necesario para el razonador HermiT de OQuaRE)
  3. OPENAI_API_KEY  (+ ping real con --online)
  4. Ollama en :11434 y modelos requeridos (llama3.1:8b, qwen2.5-coder:7b)
  5. Servidor RAG (annotationRAG) en :8000   — necesario para E3
  6. Dato canónico de las 4 BD con filas suficientes para N hasta 200
  7. Pipeline OntoGenix / dependencias de E4

Uso
---
    python scripts/preflight_check.py                 # comprobaciones locales
    python scripts/preflight_check.py --online        # + pings reales (OpenAI, Ollama, RAG)
    python scripts/preflight_check.py --sizes 25 50 100 200   # exige filas para esos N

Devuelve código de salida 0 si no hay ningún FAIL; 1 si algo crítico falla.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import socket
import subprocess
import sys
import urllib.request
from contextlib import redirect_stdout
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_OLLAMA = ["llama3.1:8b", "qwen2.5-coder:7b"]
REQUIRED_DBS = ["FANTOM5", "dbSUPER", "HACER", "DiseaseEnhancer"]

OK, WARN, FAIL = "OK", "WARN", "FAIL"
ICON = {OK: "✓", WARN: "‼", FAIL: "✗"}
results: list[tuple[str, str, str]] = []


def add(name, status, detail=""):
    results.append((name, status, detail))
    print(f"  [{ICON[status]} {status:<4}] {name}" + (f"  — {detail}" if detail else ""))


def http_get(url, timeout=4):
    req = urllib.request.Request(url, headers={"User-Agent": "preflight"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def port_open(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


# ── 1. Python + paquetes ────────────────────────────────────────────────────
def check_python():
    v = sys.version_info
    add("Python ≥ 3.10", OK if v >= (3, 10) else FAIL, f"{v.major}.{v.minor}.{v.micro}")
    needed = {"rdflib": True, "owlready2": True, "pandas": True,
              "openai": True, "requests": True, "numpy": True}
    optional = {"sentence_transformers": False, "neo4j": False}
    import importlib
    for mod, crit in {**needed, **optional}.items():
        try:
            m = importlib.import_module(mod)
            ver = getattr(m, "__version__", "?")
            add(f"paquete {mod}", OK, ver)
        except Exception as e:
            add(f"paquete {mod}", FAIL if needed.get(mod) else WARN,
                f"no instalado ({type(e).__name__})")


# ── 2. Java / HermiT ────────────────────────────────────────────────────────
def check_java():
    exe = shutil.which("java")
    if not exe:
        add("Java (HermiT)", FAIL, "no encontrado en PATH; OQuaRE no podrá razonar")
        return
    try:
        out = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=10)
        line = (out.stderr or out.stdout).splitlines()[0] if (out.stderr or out.stdout) else "?"
        add("Java (HermiT)", OK, line.strip())
    except Exception as e:
        add("Java (HermiT)", WARN, str(e)[:60])


# ── 3. OpenAI ───────────────────────────────────────────────────────────────
def check_openai(online):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        env = PROJECT_ROOT / ".env"
        if env.exists() and "OPENAI_API_KEY" in env.read_text():
            add("OPENAI_API_KEY", OK, "definida en TFM/.env")
        else:
            add("OPENAI_API_KEY", FAIL, "no definida (export OPENAI_API_KEY=sk-… o TFM/.env)")
            return
    else:
        add("OPENAI_API_KEY", OK, f"…{key[-4:]}")
    if online:
        try:
            import openai
            cli = openai.OpenAI()
            models = cli.models.list()
            has = any("gpt-4o" in m.id for m in models.data)
            add("OpenAI alcanzable", OK if has else WARN,
                "gpt-4o disponible" if has else "responde, pero no veo gpt-4o")
        except Exception as e:
            add("OpenAI alcanzable", FAIL, str(e)[:80])


# ── 4. Ollama ───────────────────────────────────────────────────────────────
def check_ollama(online):
    if not port_open("localhost", 11434):
        add("Ollama :11434", FAIL, "no responde (arranca: `ollama serve`)")
        return
    try:
        st, body = http_get("http://localhost:11434/api/tags")
        tags = json.loads(body)
        installed = [m["name"] for m in tags.get("models", [])]
        add("Ollama :11434", OK, f"{len(installed)} modelos instalados")
        for req in REQUIRED_OLLAMA:
            present = any(req == n or n.startswith(req) or req.split(":")[0] in n for n in installed)
            add(f"modelo {req}", OK if present else FAIL,
                "instalado" if present else "falta (`ollama pull " + req + "`)")
        if online and installed:
            import time
            t0 = time.time()
            payload = json.dumps({"model": REQUIRED_OLLAMA[0], "prompt": "ping",
                                  "stream": False, "options": {"num_predict": 1}}).encode()
            req = urllib.request.Request("http://localhost:11434/api/generate", data=payload,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                r.read()
            add("Ollama generación", OK, f"respuesta en {time.time()-t0:.1f}s")
    except Exception as e:
        add("Ollama :11434", FAIL, str(e)[:80])


# ── 5. Servidor RAG ─────────────────────────────────────────────────────────
def check_rag(online):
    if not port_open("localhost", 8000):
        add("RAG annotationRAG :8000", FAIL,
            "no responde (arranca: `python scripts/ragannotation_server.py`)")
        return
    add("RAG annotationRAG :8000", OK, "puerto abierto")
    if online:
        for path in ("/docs", "/", "/openapi.json"):
            try:
                st, _ = http_get("http://localhost:8000" + path)
                add("RAG responde HTTP", OK, f"GET {path} → {st}")
                break
            except Exception:
                continue
        else:
            add("RAG responde HTTP", WARN, "puerto abierto pero sin respuesta HTTP esperada")


# ── 6. Dato canónico de las 4 BD ────────────────────────────────────────────
def check_data(sizes):
    need = max(sizes)
    # localizar processed_db vía config (silenciando sus prints), con fallback a data/raw
    proc = None
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        with redirect_stdout(io.StringIO()):
            import config  # noqa
        proc = Path(config.PATHS["processed_db"])
    except Exception:
        proc = PROJECT_ROOT / "data" / "raw"
    add("processed_db", OK if proc.exists() else WARN,
        str(proc) + ("" if proc.exists() else "  (no existe; ¿TFM_DATA_ROOT?)"))
    for db in REQUIRED_DBS:
        found = None
        for cand in (proc / f"{db}.tsv", PROJECT_ROOT / "data" / "raw" / f"{db}.tsv"):
            if cand.exists():
                found = cand
                break
        if not found:
            add(f"datos {db}", FAIL, f"no encuentro {db}.tsv (necesario para muestrear)")
            continue
        try:
            with open(found, "r", encoding="utf-8", errors="ignore") as f:
                n = sum(1 for _ in f) - 1
            status = OK if n >= need else WARN
            add(f"datos {db}", status,
                f"{n} filas" + ("" if n >= need else f"  (<{need}: N>{n} muestreará de menos)"))
        except Exception as e:
            add(f"datos {db}", WARN, str(e)[:60])


# ── 7. OntoGenix / E4 ───────────────────────────────────────────────────────
def check_ontogenix():
    runner = PROJECT_ROOT / "scripts" / "run_ontogenix_experiments.py"
    add("runner E4", OK if runner.exists() else FAIL,
        "run_ontogenix_experiments.py" if runner.exists() else "no encontrado")
    root = PROJECT_ROOT / "OntoGenix"
    if not root.exists():
        add("carpeta OntoGenix/", FAIL,
            f"no existe {root} (clónala: la necesita E4)")
        return
    add("carpeta OntoGenix/", OK if (root / "GUI").exists() else WARN,
        "GUI/ presente" if (root / "GUI").exists() else "falta GUI/ dentro de OntoGenix")

    # Importación REAL del runner: añade OntoGenix al path, hace chdir y carga
    # los tres agentes. Se hace en un subproceso para aislar chdir/efectos.
    code = (
        "import sys, os;"
        f"sys.path.insert(0, r'{root}');"
        f"os.chdir(r'{root}');"
        "from GUI.PlanSage.LLM_planner import LlmPlanner;"
        "from GUI.OntoBuilder.LLM_ontology import LlmOntology;"
        "from GUI.OntoMapper.LLM_ontomapper import LlmOntoMapper;"
        "from GUI.tools.tools import csv_data_preprocessing;"
        "print('ok')"
    )
    try:
        r = subprocess.run([sys.executable, "-c", code],
                           capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and "ok" in r.stdout:
            add("import agentes OntoGenix", OK,
                "LlmPlanner/LlmOntology/LlmOntoMapper cargan")
        else:
            err = (r.stderr.strip().splitlines() or ["?"])[-1][:90]
            add("import agentes OntoGenix", FAIL,
                f"{err}  → pip install -r OntoGenix/requirements.txt")
    except Exception as e:
        add("import agentes OntoGenix", FAIL, str(e)[:80])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--online", action="store_true",
                    help="Hace pings reales (OpenAI, generación Ollama, HTTP del RAG)")
    ap.add_argument("--sizes", nargs="+", type=int, default=[25, 50, 100, 200],
                    help="Tamaños N que vas a usar (exige filas suficientes en las BD)")
    args = ap.parse_args()

    print("\n" + "=" * 64)
    print("  PREFLIGHT · verificación del entorno local del banco TFM")
    print("=" * 64)
    print("\n— 1. Python y paquetes —")
    check_python()
    print("\n— 2. Java / razonador HermiT —")
    check_java()
    print("\n— 3. OpenAI (gpt-4o) —")
    check_openai(args.online)
    print("\n— 4. Ollama (modelos abiertos) —")
    check_ollama(args.online)
    print("\n— 5. Servidor RAG semántico (E3) —")
    check_rag(args.online)
    print("\n— 6. Datos de las 4 bases —")
    check_data(args.sizes)
    print("\n— 7. OntoGenix / E4 —")
    check_ontogenix()

    n_fail = sum(1 for _, s, _ in results if s == FAIL)
    n_warn = sum(1 for _, s, _ in results if s == WARN)
    print("\n" + "=" * 64)
    print(f"  RESUMEN: {len(results)} comprobaciones · "
          f"{n_fail} FAIL · {n_warn} WARN · {len(results)-n_fail-n_warn} OK")
    if n_fail:
        print("  ✗ Hay fallos críticos. Resuélvelos antes de lanzar las fases.")
    elif n_warn:
        print("  ‼ Sin fallos críticos, pero revisa los avisos (p. ej. filas por BD).")
    else:
        print("  ✓ Entorno listo. Puedes lanzar las fases.")
    print("=" * 64)
    if not args.online:
        print("  (sugerencia: repite con --online para validar OpenAI/Ollama/RAG de verdad)")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
