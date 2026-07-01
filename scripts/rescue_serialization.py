#!/usr/bin/env python3
"""
rescue_serialization.py
───────────────────────
Rescate de serialización para ontologías generadas por LLM que son
*semánticamente* parseables pero están guardadas con la **sintaxis
equivocada**: cuerpo RDF/XML (`<owl:Class rdf:ID=…>`) bajo cabeceras
Turtle (`@prefix … .`) y extensión `.ttl`.

Es un experimento metodológico complementario: la evaluación principal
respeta el formato tal cual lo emite el modelo (un `.ttl` debe ser Turtle
válido). Este script mide cuántas ontologías adicionales serían válidas
si se corrige *solo el formato*, sin tocar el contenido.

Estrategia por fichero:
  1. Intentar parsear como Turtle. Si carga → ya válido (no se rescata).
  2. Si falla y el texto parece RDF/XML (tiene rdf:about / rdf:ID y
     elementos <owl:…>), reconstruir un documento RDF/XML bien formado
     (quitar @prefix, envolver en <rdf:RDF> con xml:base, convertir el
     <owl:Ontology> contenedor en elemento autocontenido) y parsear como
     XML. Si carga → rescatado por corrección de formato.
  3. En cualquier otro caso (Turtle con errores sintácticos genuinos) →
     no rescatable por corrección de formato.

Uso:
    python scripts/rescue_serialization.py "results/E4/*/llama3.1_8b/ontology_run*.ttl"
    python scripts/rescue_serialization.py <glob> --write-dir results/_rescued
"""
from __future__ import annotations
import argparse, glob, re, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")

try:
    import rdflib
except ImportError:
    sys.exit("Falta rdflib: pip install rdflib")


def looks_like_rdfxml(text: str) -> bool:
    return ('rdf:about=' in text or 'rdf:ID=' in text) and '<owl:' in text


def rdfxml_rescue_doc(text: str) -> str:
    ns = {}
    for m in re.finditer(r'@prefix\s+([\w\-]*):\s*<([^>]+)>\s*\.', text):
        ns[m.group(1) or ''] = m.group(2)
    ns.setdefault('owl', 'http://www.w3.org/2002/07/owl#')
    ns.setdefault('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    ns.setdefault('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    ns.setdefault('xsd', 'http://www.w3.org/2001/XMLSchema#')
    base = ns.get('base_ontology', 'https://base_ontology.com#').rstrip('#')
    body = re.sub(r'@prefix[^\n]*\n', '', text)
    m = re.search(r'<owl:Ontology\s+rdf:about="([^"]+)"', body)
    onto_iri = m.group(1) if m else base + '/ontology'
    body = re.sub(r'<owl:Ontology\b[^>]*>', '', body, count=1)
    body = re.sub(r'</owl:Ontology>\s*$', '', body).strip()
    xmlns = ' '.join(f'xmlns:{p}="{u}"' for p, u in ns.items() if p)
    return (f'<?xml version="1.0"?>\n<rdf:RDF {xmlns} xml:base="{base}">\n'
            f'  <owl:Ontology rdf:about="{onto_iri}"/>\n{body}\n</rdf:RDF>\n')


def try_load(path: Path):
    """Devuelve (status, graph). status ∈ {valid, rescued, broken}."""
    text = path.read_text(encoding='utf-8', errors='ignore')
    g = rdflib.Graph()
    try:
        g.parse(data=text, format='turtle')
        return 'valid', g
    except Exception:
        pass
    if looks_like_rdfxml(text):
        try:
            g = rdflib.Graph()
            g.parse(data=rdfxml_rescue_doc(text), format='xml')
            return 'rescued', g
        except Exception:
            return 'broken', None
    return 'broken', None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('patterns', nargs='+', help='globs de ficheros .ttl')
    ap.add_argument('--write-dir', type=Path, default=None,
                    help='si se indica, guarda las rescatadas como Turtle válido aquí')
    args = ap.parse_args()

    files = []
    for p in args.patterns:
        files += glob.glob(p, recursive=True)
    files = sorted(set(files))

    counts = {'valid': 0, 'rescued': 0, 'broken': 0}
    for f in files:
        path = Path(f)
        status, g = try_load(path)
        counts[status] += 1
        n = len(g) if g is not None else 0
        print(f"  [{status:7}] {f.split('results/')[-1]:55} triples={n}")
        if status == 'rescued' and args.write_dir:
            args.write_dir.mkdir(parents=True, exist_ok=True)
            out = args.write_dir / (path.parent.name + '__' + path.name)
            g.serialize(destination=str(out), format='turtle')

    tot = len(files)
    print(f"\nTotal={tot}  válidas={counts['valid']}  "
          f"rescatadas(formato)={counts['rescued']}  "
          f"no-rescatables={counts['broken']}")
    print(f"Validez original = {counts['valid']}/{tot}; "
          f"validez tras corrección de formato = "
          f"{counts['valid']+counts['rescued']}/{tot}")


if __name__ == '__main__':
    main()
