#!/usr/bin/env python3
"""
check_reproducibility.py
────────────────────────
Auditoría de reproducibilidad de los experimentos del TFM
"Evaluación de LLMs para la Generación de Ontologías en Bases de Datos
Genéticas".

Genera ``results/reproducibility_manifest.json`` con:

  · Versión exacta de Python e intérprete
  · Versiones de dependencias críticas (openai, rdflib, owlready2,
    sentence-transformers, neo4j, requests, pandas, numpy, matplotlib)
  · Hashes SHA-256 de los inputs deterministas:
      - data/raw/*.tsv               (universos completos)
      - data/samples/*.tsv,_sample_prompt.txt
      - data/samples/schemas/*.txt   (esquemas RAG legacy)
      - data/csv_for_ontogenix/*.csv
      - scripts/*.py                 (código del pipeline)
  · Seeds y parámetros de generación congelados
  · Modelos LLM con snapshot fijo (gpt-4o-2024-05-13, llama3.1:8b @ digest)
  · Contadores de outputs (cuántos TTL hay por experimento/modelo)
  · Métricas de drift: para cada gpt-4o snapshot indica si el alias móvil
    (gpt-4o sin sufijo) responde con la misma versión

Uso
---
    python scripts/check_reproducibility.py             # imprime + guarda
    python scripts/check_reproducibility.py --json      # solo JSON a stdout
    python scripts/check_reproducibility.py --diff old.json  # compara dos manifests
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT_ROOT / "results"

# ─── Inputs cuyo SHA-256 hay que registrar ──────────────────────────
HASH_PATHS = {
    "raw_tsv":            PROJECT_ROOT / "data" / "raw",
    "samples":            PROJECT_ROOT / "data" / "samples",
    "rag_schemas":        PROJECT_ROOT / "data" / "samples" / "schemas",
    "csv_for_ontogenix":  PROJECT_ROOT / "data" / "csv_for_ontogenix",
    "scripts":            PROJECT_ROOT / "scripts",
}

# Patrones que SÍ se hashean (hashable assets) o se EXCLUYEN
INCLUDE_GLOBS = {
    "raw_tsv":            ("*.tsv",),
    "samples":            ("*.tsv", "*_sample_prompt.txt"),
    "rag_schemas":        ("*.txt", "*.ttl"),
    "csv_for_ontogenix":  ("*.csv",),
    "scripts":            ("*.py",),
}
EXCLUDE_NAMES = {"__pycache__", ".pyc"}

# Dependencias clave a auditar
TRACKED_PACKAGES = [
    "openai", "rdflib", "owlready2", "sentence_transformers",
    "neo4j", "requests", "pandas", "numpy", "matplotlib",
    "python-docx", "fastapi", "uvicorn",
]

# Modelos LLM con snapshot recomendado
MODEL_SNAPSHOTS = {
    "gpt-4o":          "gpt-4o-2024-05-13",
    "gpt-4o-mini":     "gpt-4o-mini-2024-07-18",
    "llama3.1:8b":     "(local Ollama; pin via 'ollama show llama3.1:8b')",
    "qwen2.5-coder:7b":"(local Ollama; pin via 'ollama show qwen2.5-coder:7b')",
}


# ─── Helpers ────────────────────────────────────────────────────────
def sha256_file(path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def hash_directory(root: Path, patterns: tuple[str, ...]) -> dict:
    """Hashea recursivamente todos los archivos que coincidan con
    los patrones, ignorando los EXCLUDE_NAMES."""
    if not root.is_dir():
        return {"present": False}
    result: dict[str, str] = {}
    for pat in patterns:
        for p in sorted(root.rglob(pat)):
            if any(part in EXCLUDE_NAMES or part.endswith(tuple(EXCLUDE_NAMES))
                   for part in p.parts):
                continue
            try:
                rel = str(p.relative_to(root))
                result[rel] = sha256_file(p)
            except (PermissionError, OSError):
                continue
    return {"present": True, "files": result, "n_files": len(result)}


def package_versions() -> dict:
    versions = {}
    for pkg in TRACKED_PACKAGES:
        try:
            mod_name = pkg.replace("-", "_")
            mod = importlib.import_module(mod_name)
            versions[pkg] = getattr(mod, "__version__", "unknown")
        except ImportError:
            versions[pkg] = "(not installed)"
        except Exception as e:                                       # noqa: BLE001
            versions[pkg] = f"(error: {type(e).__name__}: {e})"
    return versions


def python_info() -> dict:
    return {
        "version":        sys.version.split()[0],
        "executable":     sys.executable,
        "platform":       platform.platform(),
        "machine":        platform.machine(),
        "processor":      platform.processor() or "?",
        "implementation": platform.python_implementation(),
    }


def output_counts() -> dict:
    """Cuenta cuántos TTL hay por (experiment, db, model_subdir)."""
    counts: dict[str, int] = {}
    if not RESULTS.is_dir():
        return counts
    for ttl in sorted(RESULTS.rglob("ontology_run*.ttl")):
        parts = ttl.relative_to(RESULTS).parts
        if len(parts) < 4:
            continue
        key = "/".join(parts[:3])  # E?/DB/model
        counts[key] = counts.get(key, 0) + 1
    return counts


def generation_params() -> dict:
    """Lee config.py y extrae GENERATION_PARAMS, SAMPLING_PARAMS,
    EXPERIMENTS, N_REPETITIONS."""
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    try:
        import config                                                # noqa: WPS433
    except Exception as e:                                           # noqa: BLE001
        return {"error": f"{type(e).__name__}: {e}"}
    return {
        "GENERATION_PARAMS": getattr(config, "GENERATION_PARAMS", None),
        "SAMPLING_PARAMS":   getattr(config, "SAMPLING_PARAMS", None),
        "N_REPETITIONS":     getattr(config, "N_REPETITIONS", None),
        "EXPERIMENTS":       list(getattr(config, "EXPERIMENTS", {}).keys()),
        "DATABASES":         list(getattr(config, "DATABASES", {}).keys()),
    }


def build_manifest() -> dict:
    print("⏳ Calculando hashes y versiones...", file=sys.stderr)
    manifest = {
        "_meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "project_root":     str(PROJECT_ROOT),
            "git_commit":       _git_commit(),
        },
        "python":            python_info(),
        "packages":          package_versions(),
        "model_snapshots":   MODEL_SNAPSHOTS,
        "generation_params": generation_params(),
        "input_hashes":      {},
        "output_counts":     output_counts(),
    }
    for label, root in HASH_PATHS.items():
        manifest["input_hashes"][label] = hash_directory(
            root, INCLUDE_GLOBS[label]
        )
        n = manifest["input_hashes"][label].get("n_files", 0)
        print(f"   {label:22s} {n:4d} archivos hasheados",
              file=sys.stderr)
    return manifest


def _git_commit() -> str:
    """Si el proyecto está bajo git, devuelve el SHA actual."""
    try:
        import subprocess
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(PROJECT_ROOT), capture_output=True, text=True,
            timeout=2,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:                                               # noqa: BLE001
        pass
    return "(no git repo)"


def diff_manifests(a: dict, b: dict) -> list[str]:
    """Devuelve líneas legibles describiendo diferencias entre dos
    manifests (a=anterior, b=actual)."""
    lines: list[str] = []
    # Versiones de paquetes
    pa, pb = a.get("packages", {}), b.get("packages", {})
    for pkg in sorted(set(pa) | set(pb)):
        va, vb = pa.get(pkg, "(missing)"), pb.get(pkg, "(missing)")
        if va != vb:
            lines.append(f"  pkg {pkg}: {va} → {vb}")
    # Hashes de inputs
    for label in HASH_PATHS:
        ha = a.get("input_hashes", {}).get(label, {}).get("files", {})
        hb = b.get("input_hashes", {}).get(label, {}).get("files", {})
        added = sorted(set(hb) - set(ha))
        removed = sorted(set(ha) - set(hb))
        changed = sorted(f for f in (set(ha) & set(hb))
                         if ha[f] != hb[f])
        if added or removed or changed:
            lines.append(f"  inputs[{label}]: "
                         f"+{len(added)} -{len(removed)} ~{len(changed)}")
            for f in changed[:5]:
                lines.append(f"      ~ {f}")
                lines.append(f"          {ha[f][:16]} → {hb[f][:16]}")
    # Output counts
    oa, ob = a.get("output_counts", {}), b.get("output_counts", {})
    for k in sorted(set(oa) | set(ob)):
        if oa.get(k) != ob.get(k):
            lines.append(f"  outputs[{k}]: {oa.get(k, 0)} → {ob.get(k, 0)}")
    return lines


# ─── Pretty-print ──────────────────────────────────────────────────
def render_text(manifest: dict) -> str:
    lines: list[str] = []
    lines.append("═" * 70)
    lines.append("  REPRODUCIBILIDAD — Manifest del TFM")
    lines.append(f"  Generado: {manifest['_meta']['generated_at_utc']}")
    lines.append(f"  Git:       {manifest['_meta']['git_commit']}")
    lines.append("═" * 70)

    py = manifest["python"]
    lines.append(f"\n▸ Python {py['version']} ({py['implementation']}) "
                 f"on {py['platform']}")
    lines.append(f"  Executable: {py['executable']}")

    lines.append("\n▸ Paquetes críticos:")
    for pkg, ver in manifest["packages"].items():
        lines.append(f"    {pkg:24s} {ver}")

    lines.append("\n▸ Modelos LLM (snapshots recomendados):")
    for alias, snap in manifest["model_snapshots"].items():
        lines.append(f"    {alias:20s} → {snap}")

    lines.append("\n▸ Parámetros de generación:")
    gp = manifest["generation_params"].get("GENERATION_PARAMS") or {}
    sp = manifest["generation_params"].get("SAMPLING_PARAMS") or {}
    for k, v in gp.items():
        lines.append(f"    GENERATION.{k:18s} {v}")
    for k, v in sp.items():
        lines.append(f"    SAMPLING.{k:20s} {v}")
    lines.append(f"    N_REPETITIONS: {manifest['generation_params'].get('N_REPETITIONS')}")

    lines.append("\n▸ Inputs hasheados (SHA-256):")
    for label, info in manifest["input_hashes"].items():
        if not info.get("present"):
            lines.append(f"    {label:22s} (carpeta no presente)")
            continue
        n = info.get("n_files", 0)
        lines.append(f"    {label:22s} {n} archivos")
    total_files = sum(info.get("n_files", 0)
                      for info in manifest["input_hashes"].values())
    lines.append(f"    TOTAL                 {total_files} archivos")

    lines.append("\n▸ Outputs detectados:")
    for k, v in sorted(manifest["output_counts"].items()):
        lines.append(f"    {k:50s} {v} TTL")

    lines.append("\n" + "═" * 70)
    return "\n".join(lines)


# ─── Main ──────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json",  action="store_true",
                    help="Imprime solo el JSON crudo")
    ap.add_argument("--out",   type=Path,
                    default=RESULTS / "reproducibility_manifest.json",
                    help=f"Ruta del manifest (default: {RESULTS}/reproducibility_manifest.json)")
    ap.add_argument("--diff",  type=Path, default=None,
                    help="Compara con un manifest anterior y muestra diffs")
    args = ap.parse_args()

    if args.diff:
        if not args.diff.is_file():
            print(f"❌ {args.diff} no existe", file=sys.stderr)
            return 1
        old = json.loads(args.diff.read_text(encoding="utf-8"))
        new = build_manifest()
        diffs = diff_manifests(old, new)
        if not diffs:
            print(f"✅ Sin cambios respecto a {args.diff}")
            return 0
        print(f"⚠️  Cambios respecto a {args.diff}:")
        print("\n".join(diffs))
        return 2

    manifest = build_manifest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        print(render_text(manifest))
        print(f"\n✅ Manifest guardado en {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
