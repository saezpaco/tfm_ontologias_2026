**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer association - unique_count: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer association - unique_count: 1
3. biosample_name: text - Name of the biosample - unique_count: 11
4. crm_ID: categorical - ID for cis-regulatory module - unique_count: 2
5. crossref: categorical - Cross-reference information - unique_count: 1
6. current_assembly: categorical - Current genome assembly version - unique_count: 1
7. current_chr: categorical - Current chromosome - unique_count: 2
8. current_end: categorical - End position in the current assembly - unique_count: 2
9. current_start: categorical - Start position in the current assembly - unique_count: 2
10. disease: categorical - Associated disease - unique_count: 1
11. disease_PMID: categorical - PubMed ID for disease association - unique_count: 1
12. disease_method: categorical - Method used for disease association - unique_count: 1
13. enh2gene_PMID: categorical - PubMed ID for enhancer to gene association - unique_count: 2
14. enh2gene_method: categorical - Method used for enhancer to gene association - unique_count: 4
15. enh_PMID: categorical - PubMed ID for enhancer - unique_count: 1
16. enh_method: categorical - Method used for enhancer identification - unique_count: 1
17. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique_count: 1
18. hgnc_symbol_target_genes: categorical - HGNC symbol for target genes - unique_count: 5
19. minimum_ratio: categorical - Minimum ratio value - unique_count: 1
20. mutation_PMID: categorical - PubMed ID for mutation - unique_count: 1
21. mutation_method: categorical - Method used for mutation identification - unique_count: 1
22. orig_assembly: categorical - Original genome assembly version - unique_count: 1
23. orig_chr: categorical - Original chromosome - unique_count: 2
24. orig_end: categorical - End position in the original assembly - unique_count: 2
25. orig_start: categorical - Start position in the original assembly - unique_count: 2
26. original_ID: categorical - Original ID - unique_count: 1
27. refsnp_ID: categorical - Reference SNP ID - unique_count: 1
28. score: categorical - Score value - unique_count: 1
29. source: categorical - Source information - unique_count: 1
30. type: categorical - Type information - unique_count: 1

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. TranscriptionFactor
8. TargetGene

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement
4. Mutation: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithDisease: GeneticElement - Disease
3. identifiedByMethod: GeneticElement - Method
4. referencedInPublication: GeneticElement - Publication
5. hasBiosample: GeneticElement - Biosample
6. regulatesGene: TranscriptionFactor - TargetGene
7. associatedWithTF: Enhancer - TranscriptionFactor

**Data Type Properties:**
1. biosampleName: Biosample - xsd:string
2. crmID: CisRegulatoryModule - xsd:string
3. crossref: GeneticElement - xsd:string
4. currentAssembly: GenomicCoordinate - xsd:string
5. currentChr: GenomicCoordinate - xsd:string
6. currentEnd: GenomicCoordinate - xsd:integer
7. currentStart: GenomicCoordinate - xsd:integer
8. diseaseName: Disease - xsd:string
9. diseasePMID: Disease - xsd:string
10. diseaseMethod: Disease - xsd:string
11. enh2genePMID: Enhancer - xsd:string
12. enh2geneMethod: Enhancer - xsd:string
13. enhPMID: Enhancer - xsd:string
14. enhMethod: Enhancer - xsd:string
15. hgncSymbolTFs: TranscriptionFactor - xsd:string
16. hgncSymbolTargetGenes: TargetGene - xsd:string
17. minimumRatio: GeneticElement - xsd:float
18. mutationPMID: Mutation - xsd:string
19. mutationMethod: Mutation - xsd:string
20. origAssembly: GenomicCoordinate - xsd:string
21. origChr: GenomicCoordinate - xsd:string
22. origEnd: GenomicCoordinate - xsd:integer
23. origStart: GenomicCoordinate - xsd:integer
24. originalID: GeneticElement - xsd:string
25. refsnpID: GeneticElement - xsd:string
26. score: GeneticElement - xsd:float
27. source: GeneticElement - xsd:string
28. type: GeneticElement - xsd:string