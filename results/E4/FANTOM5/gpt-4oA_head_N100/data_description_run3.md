**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - categorical
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer associations - categorical
3. biosample: categorical - Type of biosample or cell line used - categorical
4. crm_ID: text - Identifier for cis-regulatory module - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: categorical - Current chromosome - categorical
8. disease: categorical - Disease associated with the genetic element - categorical
9. disease_PMID: categorical - PubMed ID for disease association - categorical
10. disease_method: categorical - Method used for identifying disease association - categorical
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - categorical
12. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - categorical
13. enh_PMID: categorical - PubMed ID for enhancer information - categorical
14. enh_method: categorical - Method used for identifying enhancer - categorical
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
17. minimum_ratio: categorical - Minimum ratio value - categorical
18. mutation_PMID: categorical - PubMed ID for mutation information - categorical
19. mutation_method: categorical - Method used for identifying mutation - categorical
20. orig_assembly: categorical - Original genome assembly version - categorical
21. orig_chr: categorical - Original chromosome - categorical
22. original_ID: categorical - Original identifier - categorical
23. refsnp_ID: categorical - Reference SNP ID - categorical
24. score: categorical - Score value - categorical
25. source: categorical - Source of the data - categorical
26. type: categorical - Type of genetic element - categorical
27. current_end: Numerical - Current end position in the genome - Numerical
28. current_start: Numerical - Current start position in the genome - Numerical
29. orig_end: Numerical - Original end position in the genome - Numerical
30. orig_start: Numerical - Original start position in the genome - Numerical

**classes:**
1. GeneticElement
2. Biosample
3. Disease
4. Method
5. Publication

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. TranscriptionFactor: subclass of -> GeneticElement
4. TargetGene: subclass of -> GeneticElement
5. Mutation: subclass of -> GeneticElement

**Object Properties:**
1. hasBiosample: GeneticElement - Biosample
2. associatedWithDisease: GeneticElement - Disease
3. identifiedByMethod: GeneticElement - Method
4. referencedInPublication: GeneticElement - Publication
5. regulates: TranscriptionFactor - TargetGene
6. locatedOnChromosome: GeneticElement - xsd:string

**Data Type Properties:**
1. crmID: GeneticElement - xsd:string
2. currentAssembly: GeneticElement - xsd:string
3. currentChr: GeneticElement - xsd:string
4. currentEnd: GeneticElement - xsd:integer
5. currentStart: GeneticElement - xsd:integer
6. origAssembly: GeneticElement - xsd:string
7. origChr: GeneticElement - xsd:string
8. origEnd: GeneticElement - xsd:integer
9. origStart: GeneticElement - xsd:integer
10. originalID: GeneticElement - xsd:string
11. refsnpID: GeneticElement - xsd:string
12. score: GeneticElement - xsd:float
13. source: GeneticElement - xsd:string
14. type: GeneticElement - xsd:string
15. minimumRatio: GeneticElement - xsd:float
16. hgncSymbolTFs: TranscriptionFactor - xsd:string
17. hgncSymbolTargetGenes: TargetGene - xsd:string
18. TFs2enhPMID: TranscriptionFactor - xsd:string
19. TFs2enhMethod: TranscriptionFactor - xsd:string
20. enh2genePMID: Enhancer - xsd:string
21. enh2geneMethod: Enhancer - xsd:string
22. enhPMID: Enhancer - xsd:string
23. enhMethod: Enhancer - xsd:string
24. diseasePMID: Disease - xsd:string
25. diseaseMethod: Disease - xsd:string
26. mutationPMID: Mutation - xsd:string
27. mutationMethod: Mutation - xsd:string