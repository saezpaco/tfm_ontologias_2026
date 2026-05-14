# Preguntas de competencia (CQ) — resumen

_Corpus de 15 preguntas SPARQL canónicas del dominio cis-regulatorio. Cada ontología generada se evalúa a nivel de TBox: una CQ se considera satisfecha si la ontología declara, como mínimo, el 50 % de las clases y predicados requeridos para responder la pregunta. Implementación en scripts/competency_questions.py._

| Experimento | Modelo / variante | n ontologías | Cobertura media (de 15) | Cobertura min | Cobertura max |
|---|---|---|---|---|---|
| E1 | gpt-4o_A_head | 2 | 1.5 / 15 (10%) | 1 | 2 |
| E1 | gpt-4o_B_random | 2 | 1.0 / 15 (7%) | 1 | 1 |
| E1 | gpt-4o_C_stratified | 2 | 1.5 / 15 (10%) | 1 | 2 |
| E1 | gpt-4o_D_diversity | 2 | 2.0 / 15 (13%) | 2 | 2 |
| E1 | llama3.1_8b_A_head | 2 | 2.5 / 15 (17%) | 2 | 3 |
| E1 | llama3.1_8b_B_random | 2 | 4.0 / 15 (27%) | 3 | 5 |
| E1 | llama3.1_8b_C_stratified | 2 | 3.0 / 15 (20%) | 2 | 4 |
| E1 | llama3.1_8b_D_diversity | 2 | 3.5 / 15 (23%) | 3 | 4 |
| E3 | gpt-4o_N100_ragapi | 6 | 1.7 / 15 (11%) | 0 | 3 |
| E3 | gpt-4o_N200_ragapi | 6 | 1.3 / 15 (9%) | 0 | 3 |
| E3 | gpt-4o_N25_ragapi | 6 | 1.2 / 15 (8%) | 0 | 3 |
| E3 | gpt-4o_N50_ragapi | 6 | 1.3 / 15 (9%) | 0 | 3 |
| E3 | gpt-4o_legacy | 12 | 3.3 / 15 (22%) | 3 | 4 |
| E3 | gpt-4o_ragapi | 12 | 5.0 / 15 (33%) | 3 | 7 |
| E3 | llama3.1_8b_N100_ragapi | 6 | 0.5 / 15 (3%) | 0 | 2 |
| E3 | llama3.1_8b_N200_ragapi | 6 | 1.2 / 15 (8%) | 0 | 3 |
| E3 | llama3.1_8b_N25_ragapi | 6 | 2.2 / 15 (14%) | 1 | 3 |
| E3 | llama3.1_8b_N50_ragapi | 6 | 1.7 / 15 (11%) | 1 | 3 |
| E3 | llama3.1_8b_legacy | 12 | 5.9 / 15 (39%) | 5 | 7 |
| E3 | llama3.1_8b_ragapi | 12 | 1.2 / 15 (8%) | 0 | 4 |
| E3 | llama3.1_8b_ragapi_C1 | 12 | 2.4 / 15 (16%) | 0 | 4 |
| E3 | llama3.1_8b_ragapi_C2 | 12 | 3.2 / 15 (22%) | 2 | 5 |
| E3 | llama3.1_8b_ragapi_C3 | 12 | 3.0 / 15 (20%) | 0 | 8 |
| E4 | gpt-4o_A_head | 4 | 1.0 / 15 (7%) | 0 | 2 |
| E4 | gpt-4o_B_random | 4 | 1.0 / 15 (7%) | 0 | 2 |
| E4 | gpt-4o_C_stratified | 4 | 1.0 / 15 (7%) | 0 | 2 |
| E4 | gpt-4o_D_diversity | 4 | 1.0 / 15 (7%) | 0 | 2 |
| E4 | llama3.1_8b | 24 | 2.1 / 15 (14%) | 0 | 6 |

## Corpus de las 15 preguntas

**CQ01.** ¿Qué módulo cis-regulador (CRM) está localizado en una región genómica dada (cromosoma, start, end)?

```sparql
SELECT ?crm WHERE {
  ?crm a hcrm:crm_ID ;
       obo:BFO_0000050 ?chr ;
       obo:GENO_0000895 ?start ;
       obo:GENO_0000894 ?end .
  FILTER(?chr = nuccore:chr1 && ?start >= 1000 && ?end <= 2000)
}
```

**CQ02.** ¿Qué genes diana regula un CRM concreto?

```sparql
SELECT ?gene WHERE {
  ?crm a hcrm:crm_ID ;
       sio:SIO_000628 ?gene .
  FILTER(?crm = hcrm:CRMHS00000005752)
}
```

**CQ03.** ¿Qué factores de transcripción se unen a un CRM?

```sparql
SELECT ?tf WHERE {
  ?crm a hcrm:crm_ID ;
       obo:RO_0002436 ?tf .
  ?tf a sio:SIO_010035 .
}
```

**CQ04.** ¿Qué enhancers están asociados a una enfermedad concreta?

```sparql
SELECT ?crm WHERE {
  ?crm a hcrm:crm_ID ;
       obo:RO_0004026 ?disease .
  FILTER(?disease = obo:DOID_0060785)
}
```

**CQ05.** ¿Cuál es la evidencia experimental que respalda un CRM?

```sparql
SELECT ?evidence ?article WHERE {
  ?crm a hcrm:crm_ID ;
       rdfs:isDefinedBy ?evidence ;
       sio:SIO_000772 ?article .
}
```

**CQ06.** ¿En qué tejido o tipo celular es activo un CRM?

```sparql
SELECT ?tissue WHERE {
  ?crm a hcrm:crm_ID ;
       obo:TXPO_0003500 ?tissue .
  ?tissue a obo:UBERON_ID .
}
```

**CQ07.** ¿Qué super-enhancers están registrados en dbSUPER y cuáles son sus genes diana?

```sparql
SELECT ?se ?gene WHERE {
  ?se a hcrm:crm_ID ;
      rdfs:isDefinedBy <dbSUPER> ;
      sio:SIO_000628 ?gene .
}
```

**CQ08.** ¿Qué mutaciones se han documentado en un CRM?

```sparql
SELECT ?mutation WHERE {
  ?crm a hcrm:crm_ID ;
       obo:RO_0001025 ?mutation .
}
```

**CQ09.** ¿Qué versión de ensamblaje genómico (hg19 / hg38) utiliza la anotación de un CRM?

```sparql
SELECT ?assembly WHERE {
  ?crm a hcrm:crm_ID ;
       dc:hasVersion ?assembly .
}
```

**CQ10.** ¿Cuál es el método experimental utilizado para identificar un enhancer (CAGE, H3K27ac, etc.)?

```sparql
SELECT ?method WHERE {
  ?crm a hcrm:crm_ID ;
       obo:OBI_0000293 ?method .
}
```

**CQ11.** ¿En qué taxón (especie) se encuentra anotado un CRM?

```sparql
SELECT ?taxon WHERE {
  ?crm a hcrm:crm_ID ;
       obo:RO_0002162 ?taxon .
}
```

**CQ12.** ¿Qué CRM tienen un score de confianza mínimo determinado?

```sparql
SELECT ?crm ?score WHERE {
  ?crm a hcrm:crm_ID ;
       sio:SIO_000300 ?score .
  FILTER(?score >= 0.9)
}
```

**CQ13.** ¿Cuál es el cross-reference (identificador externo) de un enhancer en su base de datos original?

```sparql
SELECT ?xref WHERE {
  ?crm a hcrm:crm_ID ;
       sio:SIO_000253 ?xref .
}
```

**CQ14.** ¿Existe una relación CRM → fenotipo distinguible de CRM → enfermedad?

```sparql
SELECT ?phenotype WHERE {
  ?crm a hcrm:crm_ID ;
       obo:RO_0002200 ?phenotype .
  ?phenotype a obo:HP_0000118 .
}
```

**CQ15.** ¿Hay anotación bibliográfica (PMID) que valide la asociación CRM → gen para una corrida concreta?

```sparql
SELECT ?article WHERE {
  ?crm a hcrm:crm_ID ;
       sio:SIO_000628 ?gene ;
       sio:SIO_000772 ?article .
  ?article a obo:IAO_0000013 .
}
```
