**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer association - unique values: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer association - unique values: 1
3. biosample_name: text - Name of the biosample - unique values: 50
4. crm_ID: text - Cis-regulatory module ID - unique values: 50
5. crossref: text - Cross-reference ID - unique values: 50
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: text - Current chromosome - unique values: 23
8. disease: categorical - Disease associated - unique values: 1
9. disease_PMID: categorical - PubMed ID for disease association - unique values: 1
10. disease_method: categorical - Method used for disease association - unique values: 1
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene association - unique values: 8
12. enh2gene_method: categorical - Method used for enhancer to gene association - unique values: 2
13. enh_PMID: categorical - PubMed ID for enhancer - unique values: 7
14. enh_method: categorical - Method used for enhancer identification - unique values: 3
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 50
17. minimum_ratio: categorical - Minimum ratio - unique values: 1
18. mutation_PMID: categorical - PubMed ID for mutation - unique values: 1
19. mutation_method: categorical - Method used for mutation identification - unique values: 1
20. orig_assembly: categorical - Original genome assembly version - unique values: 1
21. orig_chr: text - Original chromosome - unique values: 23
22. original_ID: text - Original ID - unique values: 50
23. refsnp_ID: categorical - Reference SNP ID - unique values: 1
24. source: categorical - Source of the data - unique values: 1
25. type: categorical - Type of the data - unique values: 1
26. current_end: Numerical - Current end position in the genome - range: 121087.0 to 206591648.0
27. current_start: Numerical - Current start position in the genome - range: 104619.0 to 206550559.0
28. orig_end: Numerical - Original end position in the genome - range: 171086.0 to 206764980.0
29. orig_start: Numerical - Original start position in the genome - range: 154617.0 to 206723887.0
30. score: Numerical - Score value - range: 0.9861407 to 1.005692

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Publication
6. Method
7. TranscriptionFactor
8. Gene
9. Mutation

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. Chromosome: subclass of -> GenomicCoordinate

**Object Properties:**
1. hasBiosample: GeneticElement - Biosample
2. associatedWithDisease: GeneticElement - Disease
3. hasPublication: GeneticElement - Publication
4. identifiedByMethod: GeneticElement - Method
5. regulatesGene: GeneticElement - Gene
6. boundByTF: GeneticElement - TranscriptionFactor
7. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
8. hasMutation: GeneticElement - Mutation

**Data Type Properties:**
1. biosampleName: Biosample - xsd:string
2. crmID: GeneticElement - xsd:string
3. crossrefID: GeneticElement - xsd:string
4. currentAssembly: GenomicCoordinate - xsd:string
5. currentChr: Chromosome - xsd:string
6. diseaseName: Disease - xsd:string
7. diseasePMID: Disease - xsd:string
8. diseaseMethod: Disease - xsd:string
9. enh2genePMID: Publication - xsd:string
10. enh2geneMethod: Method - xsd:string
11. enhPMID: Publication - xsd:string
12. enhMethod: Method - xsd:string
13. hgncSymbolTFs: TranscriptionFactor - xsd:string
14. hgncSymbolTargetGenes: Gene - xsd:string
15. minimumRatio: GeneticElement - xsd:float
16. mutationPMID: Mutation - xsd:string
17. mutationMethod: Mutation - xsd:string
18. origAssembly: GenomicCoordinate - xsd:string
19. origChr: Chromosome - xsd:string
20. originalID: GeneticElement - xsd:string
21. refsnpID: Mutation - xsd:string
22. source: GeneticElement - xsd:string
23. type: GeneticElement - xsd:string
24. currentEnd: GenomicCoordinate - xsd:integer
25. currentStart: GenomicCoordinate - xsd:integer
26. origEnd: GenomicCoordinate - xsd:integer
27. origStart: GenomicCoordinate - xsd:integer
28. score: GeneticElement - xsd:float