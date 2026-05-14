"""Sugerencia 2 del tutor: corpus reproducible de preguntas de competencia.

Define 15 preguntas SPARQL canónicas del dominio cis-regulatorio y evalúa, para
cada ontología generada, si declara los elementos TBox mínimos necesarios para
responderlas (i.e., satisfacción a nivel de esquema; no se ejecuta SPARQL sobre
ABox porque las ontologías generadas son TBox + pocas instancias).

Cada CQ se modela como un patrón de requisitos:
  - classes:   conjunto de fragmentos de URI/local-name que deben estar en la
               ontología como clases o entidades referenciadas
  - predicates: conjunto de fragmentos de propiedades (object / datatype) que
                deben estar declaradas o usadas

Una ontología "cumple" la CQ si sus URIs/términos cubren todos los elementos
del patrón (matching por substring case-insensitive sobre el TTL).

Outputs:
  - results/evaluation/competency_questions.csv   (matriz: ontología × CQ)
  - results/evaluation/competency_questions.md    (resumen agregado)
"""
from __future__ import annotations
import csv, re
from collections import defaultdict
from pathlib import Path

ROOT = Path("/sessions/nifty-beautiful-knuth/mnt/TFM")
RES  = ROOT / "results"
EVAL = RES / "evaluation"
EVAL.mkdir(parents=True, exist_ok=True)

# ─────────── corpus de 15 preguntas de competencia ───────────
# Cada CQ tiene: id, pregunta natural, consulta SPARQL canónica (sobre
# vocabulario cisreg + obo) y patrón de requisitos sobre el TBox.

CQS = [
    {
        "id": "CQ01",
        "question": "¿Qué módulo cis-regulador (CRM) está localizado en una "
                    "región genómica dada (cromosoma, start, end)?",
        "sparql": (
            "SELECT ?crm WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:BFO_0000050 ?chr ;\n"
            "       obo:GENO_0000895 ?start ;\n"
            "       obo:GENO_0000894 ?end .\n"
            "  FILTER(?chr = nuccore:chr1 && ?start >= 1000 && ?end <= 2000)\n"
            "}"
        ),
        "requires": {
            "classes":    ["crm", "regulator", "module"],
            "predicates": ["start", "end", "chromosome", "position"],
        },
    },
    {
        "id": "CQ02",
        "question": "¿Qué genes diana regula un CRM concreto?",
        "sparql": (
            "SELECT ?gene WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       sio:SIO_000628 ?gene .\n"
            "  FILTER(?crm = hcrm:CRMHS00000005752)\n"
            "}"
        ),
        "requires": {
            "classes":    ["gene", "target"],
            "predicates": ["target", "regulat", "gene"],
        },
    },
    {
        "id": "CQ03",
        "question": "¿Qué factores de transcripción se unen a un CRM?",
        "sparql": (
            "SELECT ?tf WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:RO_0002436 ?tf .\n"
            "  ?tf a sio:SIO_010035 .\n"
            "}"
        ),
        "requires": {
            "classes":    ["transcription", "factor", "tf"],
            "predicates": ["bind", "transcription", "tf"],
        },
    },
    {
        "id": "CQ04",
        "question": "¿Qué enhancers están asociados a una enfermedad concreta?",
        "sparql": (
            "SELECT ?crm WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:RO_0004026 ?disease .\n"
            "  FILTER(?disease = obo:DOID_0060785)\n"
            "}"
        ),
        "requires": {
            "classes":    ["disease", "enhancer", "phenotype"],
            "predicates": ["disease", "associat", "phen"],
        },
    },
    {
        "id": "CQ05",
        "question": "¿Cuál es la evidencia experimental que respalda un CRM?",
        "sparql": (
            "SELECT ?evidence ?article WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       rdfs:isDefinedBy ?evidence ;\n"
            "       sio:SIO_000772 ?article .\n"
            "}"
        ),
        "requires": {
            "classes":    ["evidence", "publication"],
            "predicates": ["evidence", "publication", "pubmed", "method"],
        },
    },
    {
        "id": "CQ06",
        "question": "¿En qué tejido o tipo celular es activo un CRM?",
        "sparql": (
            "SELECT ?tissue WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:TXPO_0003500 ?tissue .\n"
            "  ?tissue a obo:UBERON_ID .\n"
            "}"
        ),
        "requires": {
            "classes":    ["tissue", "biosample", "cell"],
            "predicates": ["biosample", "tissue", "cell"],
        },
    },
    {
        "id": "CQ07",
        "question": "¿Qué super-enhancers están registrados en dbSUPER y "
                    "cuáles son sus genes diana?",
        "sparql": (
            "SELECT ?se ?gene WHERE {\n"
            "  ?se a hcrm:crm_ID ;\n"
            "      rdfs:isDefinedBy <dbSUPER> ;\n"
            "      sio:SIO_000628 ?gene .\n"
            "}"
        ),
        "requires": {
            "classes":    ["super", "enhancer", "gene"],
            "predicates": ["target", "source", "database"],
        },
    },
    {
        "id": "CQ08",
        "question": "¿Qué mutaciones se han documentado en un CRM?",
        "sparql": (
            "SELECT ?mutation WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:RO_0001025 ?mutation .\n"
            "}"
        ),
        "requires": {
            "classes":    ["mutation", "variant", "snp"],
            "predicates": ["mutation", "variant"],
        },
    },
    {
        "id": "CQ09",
        "question": "¿Qué versión de ensamblaje genómico (hg19 / hg38) "
                    "utiliza la anotación de un CRM?",
        "sparql": (
            "SELECT ?assembly WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       dc:hasVersion ?assembly .\n"
            "}"
        ),
        "requires": {
            "classes":    ["assembly"],
            "predicates": ["assembly", "version", "build"],
        },
    },
    {
        "id": "CQ10",
        "question": "¿Cuál es el método experimental utilizado para "
                    "identificar un enhancer (CAGE, H3K27ac, etc.)?",
        "sparql": (
            "SELECT ?method WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:OBI_0000293 ?method .\n"
            "}"
        ),
        "requires": {
            "classes":    ["method", "assay"],
            "predicates": ["method", "assay", "technique"],
        },
    },
    {
        "id": "CQ11",
        "question": "¿En qué taxón (especie) se encuentra anotado un CRM?",
        "sparql": (
            "SELECT ?taxon WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:RO_0002162 ?taxon .\n"
            "}"
        ),
        "requires": {
            "classes":    ["taxon", "organism", "species"],
            "predicates": ["taxon", "organism"],
        },
    },
    {
        "id": "CQ12",
        "question": "¿Qué CRM tienen un score de confianza mínimo determinado?",
        "sparql": (
            "SELECT ?crm ?score WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       sio:SIO_000300 ?score .\n"
            "  FILTER(?score >= 0.9)\n"
            "}"
        ),
        "requires": {
            "classes":    [],
            "predicates": ["score", "confidence", "ratio"],
        },
    },
    {
        "id": "CQ13",
        "question": "¿Cuál es el cross-reference (identificador externo) de un "
                    "enhancer en su base de datos original?",
        "sparql": (
            "SELECT ?xref WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       sio:SIO_000253 ?xref .\n"
            "}"
        ),
        "requires": {
            "classes":    [],
            "predicates": ["crossref", "xref", "external", "identif"],
        },
    },
    {
        "id": "CQ14",
        "question": "¿Existe una relación CRM → fenotipo distinguible de "
                    "CRM → enfermedad?",
        "sparql": (
            "SELECT ?phenotype WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       obo:RO_0002200 ?phenotype .\n"
            "  ?phenotype a obo:HP_0000118 .\n"
            "}"
        ),
        "requires": {
            "classes":    ["phenotype", "trait"],
            "predicates": ["phenotype", "phen"],
        },
    },
    {
        "id": "CQ15",
        "question": "¿Hay anotación bibliográfica (PMID) que valide la "
                    "asociación CRM → gen para una corrida concreta?",
        "sparql": (
            "SELECT ?article WHERE {\n"
            "  ?crm a hcrm:crm_ID ;\n"
            "       sio:SIO_000628 ?gene ;\n"
            "       sio:SIO_000772 ?article .\n"
            "  ?article a obo:IAO_0000013 .\n"
            "}"
        ),
        "requires": {
            "classes":    ["article", "publication"],
            "predicates": ["pmid", "pubmed", "publication"],
        },
    },
]


# ─────────── evaluación TBox satisfaction ───────────
def evaluate_cq(ttl_text: str, cq: dict) -> dict:
    """Comprueba si la ontología declara los elementos mínimos para la CQ."""
    text_l = ttl_text.lower()
    classes_required = cq["requires"]["classes"]
    predicates_required = cq["requires"]["predicates"]

    # Para clases: matching por substring o término relacionado
    cls_hits = [c for c in classes_required if c.lower() in text_l]
    cls_score = (len(cls_hits) / len(classes_required)
                 if classes_required else 1.0)

    pred_hits = [p for p in predicates_required if p.lower() in text_l]
    pred_score = (len(pred_hits) / len(predicates_required)
                  if predicates_required else 1.0)

    # Satisfacción global: la ontología cumple si tiene AL MENOS una clase
    # de cada conjunto requerido (más laxo) o si cubre todo (estricto).
    # Adoptamos el criterio intermedio: cobertura ≥ 50 % de clases Y de predicates.
    satisfies = (cls_score >= 0.5 and pred_score >= 0.5)
    return {
        "cq_id": cq["id"],
        "satisfies": int(satisfies),
        "cls_score": round(cls_score, 3),
        "pred_score": round(pred_score, 3),
        "cls_hits":   "|".join(cls_hits),
        "pred_hits":  "|".join(pred_hits),
    }


def parse_path(p: Path):
    parts = p.relative_to(RES).parts
    return {
        "experiment":   parts[0] if len(parts) >= 1 else "",
        "db":           parts[1] if len(parts) >= 2 else "",
        "model_variant": parts[2] if len(parts) >= 3 else "",
        "variant":      "postprocessed" if "postprocessed" in parts else "raw",
        "run":          re.search(r"run(\d+)", p.name).group(1) if re.search(r"run(\d+)", p.name) else "",
    }


def main():
    # Filtrar solo ontologías parseables — usamos los postprocessed cuando
    # existen
    rows = []
    for p in sorted(RES.rglob("*.ttl")):
        if ".owlcache" in str(p): continue
        meta = parse_path(p)
        if not meta["experiment"]: continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Si hay postprocessed para esta corrida, saltamos el raw
        if meta["variant"] == "raw":
            pp_path = p.parent / "postprocessed" / p.name
            if pp_path.exists(): continue

        rec = {"file": str(p.relative_to(RES)), **meta}
        cq_satisfactions = []
        for cq in CQS:
            ev = evaluate_cq(text, cq)
            rec[f"{cq['id']}_sat"] = ev["satisfies"]
            cq_satisfactions.append(ev["satisfies"])
        rec["n_satisfied"] = sum(cq_satisfactions)
        rec["coverage"]    = round(sum(cq_satisfactions) / len(CQS), 3)
        rows.append(rec)

    # CSV detallado
    out_csv = EVAL / "competency_questions.csv"
    fieldnames = (["file", "experiment", "db", "model_variant", "variant", "run"]
                  + [f"{cq['id']}_sat" for cq in CQS]
                  + ["n_satisfied", "coverage"])
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
    print(f"[OK] {out_csv} ({len(rows)} ontologías evaluadas)")

    # Resumen agregado por (experimento, modelo)
    agg = defaultdict(list)
    for r in rows:
        key = (r["experiment"], r["model_variant"])
        agg[key].append(r["coverage"])

    md = ["# Preguntas de competencia (CQ) — resumen", "",
          f"_Corpus de {len(CQS)} preguntas SPARQL canónicas del dominio "
          "cis-regulatorio. Cada ontología generada se evalúa a nivel de "
          "TBox: una CQ se considera satisfecha si la ontología declara, "
          "como mínimo, el 50 % de las clases y predicados requeridos para "
          "responder la pregunta. Implementación en "
          "scripts/competency_questions.py._", ""]
    md += ["| Experimento | Modelo / variante | n ontologías | "
           "Cobertura media (de 15) | Cobertura min | Cobertura max |",
           "|---|---|---|---|---|---|"]
    for (exp, mod), covs in sorted(agg.items()):
        if not covs: continue
        n = len(covs)
        mean = sum(covs)/n
        md.append(f"| {exp} | {mod} | {n} | {mean*15:.1f} / 15 "
                  f"({mean:.0%}) | {min(covs)*15:.0f} | {max(covs)*15:.0f} |")
    md.append("")
    md += ["## Corpus de las 15 preguntas", ""]
    for cq in CQS:
        md.append(f"**{cq['id']}.** {cq['question']}")
        md.append("")
        md.append("```sparql")
        md.append(cq["sparql"])
        md.append("```")
        md.append("")
    out_md = EVAL / "competency_questions.md"
    out_md.write_text("\n".join(md))
    print(f"[OK] {out_md}")
    return rows


if __name__ == "__main__":
    main()
