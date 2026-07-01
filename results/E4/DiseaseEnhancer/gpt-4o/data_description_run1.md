**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer mapping - categorical
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer mapping - categorical
3. biosample_name: categorical - Name of the biosample or cell line - categorical
4. crm_ID: text - Cis-regulatory module ID - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: text - Current chromosome - text
8. disease: text - Disease associated with the genetic element - text
9. disease_method: categorical - Method used for disease association - categorical
10. enh2gene_PMID: text - PubMed ID for enhancer to gene mapping - text
11. enh2gene_method: categorical - Method used for enhancer to gene mapping - categorical
12. enh_method: categorical - Method used for enhancer identification - categorical
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
15. minimum_ratio: categorical - Minimum ratio value - categorical
16. mutation_PMID: text - PubMed ID for mutation information - text
17. mutation_method: categorical - Method used for mutation identification - categorical
18. orig_assembly: categorical - Original genome assembly version - categorical
19. orig_chr: text - Original chromosome - text
20. original_ID: text - Original ID of the genetic element - text
21. refseq_ID: text - RefSeq ID - text
22. score: categorical - Score value - categorical
23. source: categorical - Source of the data - categorical
24. type: categorical - Type of genetic element - categorical
25. current_end: Numerical - End coordinate in the current assembly - Numerical
26. current_start: Numerical - Start coordinate in the current assembly - Numerical
27. disease_PMID: Numerical - PubMed ID for disease information - Numerical
28. enh_PMID: Numerical - PubMed ID for enhancer information - Numerical
29. orig_end: Numerical - End coordinate in the original assembly - Numerical
30. orig_start: Numerical - Start coordinate in the original assembly - Numerical

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
5. mappedToGene: Enhancer - TargetGene
6. regulatedByTF: Enhancer - TranscriptionFactor

**Data Type Properties:**
1. crmID: GeneticElement - xsd:string
2. crossref: GeneticElement - xsd:string
3. currentAssembly: GeneticElement - xsd:string
4. currentChr: GeneticElement - xsd:string
5. diseaseName: Disease - xsd:string
6. enh2genePMID: Enhancer - xsd:string
7. enh2geneMethod: Enhancer - xsd:string
8. enhMethod: Enhancer - xsd:string
9. hgncSymbolTFs: TranscriptionFactor - xsd:string
10. hgncSymbolTargetGenes: TargetGene - xsd:string
11. minimumRatio: GeneticElement - xsd:float
12. mutationPMID: Mutation - xsd:string
13. mutationMethod: Mutation - xsd:string
14. origAssembly: GeneticElement - xsd:string
15. origChr: GeneticElement - xsd:string
16. originalID: GeneticElement - xsd:string
17. refseqID: GeneticElement - xsd:string
18. score: GeneticElement - xsd:float
19. source: GeneticElement - xsd:string
20. type: GeneticElement - xsd:string
21. currentEnd: GeneticElement - xsd:integer
22. currentStart: GeneticElement - xsd:integer
23. diseasePMID: Disease - xsd:integer
24. enhPMID: Enhancer - xsd:integer
25. origEnd: GeneticElement - xsd:integer
26. origStart: GeneticElement - xsd:integer