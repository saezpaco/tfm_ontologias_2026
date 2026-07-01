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
3. biosample_name: categorical - Name of the biosample or cell line - categorical
4. crm_ID: text - Identifier for cis-regulatory modules - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: categorical - Current chromosome - categorical
8. disease: text - Disease associated with the genetic element - text
9. disease_method: categorical - Method used for identifying disease associations - categorical
10. enh2gene_PMID: text - PubMed ID for enhancer to gene associations - text
11. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - categorical
12. enh_method: categorical - Method used for identifying enhancers - categorical
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
15. minimum_ratio: categorical - Minimum ratio value - categorical
16. mutation_PMID: text - PubMed ID for mutation associations - text
17. mutation_method: categorical - Method used for identifying mutation associations - categorical
18. orig_assembly: categorical - Original genome assembly version - categorical
19. orig_chr: categorical - Original chromosome - categorical
20. original_ID: text - Original identifier for the genetic element - text
21. refseq_ID: text - RefSeq identifier - text
22. score: categorical - Score value - categorical
23. source: categorical - Source of the data - categorical
24. type: categorical - Type of genetic element - categorical
25. current_end: Numerical - Current end position in the genome - Numerical
26. current_start: Numerical - Current start position in the genome - Numerical
27. disease_PMID: Numerical - PubMed ID for disease associations - Numerical
28. enh_PMID: Numerical - PubMed ID for enhancer associations - Numerical
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
5. hasTranscriptionFactor: Enhancer - TranscriptionFactor
6. targetsGene: Enhancer - TargetGene
7. hasMutation: GeneticElement - Mutation

**Data Type Properties:**
1. crmID: GeneticElement - xsd:string
2. crossref: GeneticElement - xsd:string
3. currentAssembly: GeneticElement - xsd:string
4. currentChr: GeneticElement - xsd:string
5. diseaseName: Disease - xsd:string
6. enh2genePMID: Enhancer - xsd:string
7. hgncSymbolTFs: TranscriptionFactor - xsd:string
8. hgncSymbolTargetGenes: TargetGene - xsd:string
9. minimumRatio: GeneticElement - xsd:float
10. mutationPMID: Mutation - xsd:string
11. origAssembly: GeneticElement - xsd:string
12. origChr: GeneticElement - xsd:string
13. originalID: GeneticElement - xsd:string
14. refseqID: GeneticElement - xsd:string
15. score: GeneticElement - xsd:float
16. source: GeneticElement - xsd:string
17. type: GeneticElement - xsd:string
18. currentEnd: GeneticElement - xsd:integer
19. currentStart: GeneticElement - xsd:integer
20. diseasePMID: Disease - xsd:integer
21. enhPMID: Enhancer - xsd:integer
22. origEnd: GeneticElement - xsd:integer
23. origStart: GeneticElement - xsd:integer