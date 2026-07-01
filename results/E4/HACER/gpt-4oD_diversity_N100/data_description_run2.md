**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - unique values: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer associations - unique values: 1
3. biosample_name: text - Name of the biosample - unique values: 49
4. crm_ID: text - Cis-regulatory module ID - unique values: 100
5. crossref: text - Cross-reference ID - unique values: 99
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: text - Current chromosome - unique values: 23
8. disease: categorical - Disease associated with the data - unique values: 1
9. disease_PMID: categorical - PubMed ID for disease associations - unique values: 1
10. disease_method: categorical - Method used for disease associations - unique values: 1
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - unique values: 2
12. enh2gene_method: categorical - Method used for enhancer to gene associations - unique values: 3
13. enh_PMID: categorical - PubMed ID for enhancer data - unique values: 1
14. enh_method: categorical - Method used for enhancer data - unique values: 2
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 86
17. minimum_ratio: categorical - Minimum ratio value - unique values: 1
18. mutation_PMID: categorical - PubMed ID for mutation data - unique values: 2
19. mutation_method: categorical - Method used for mutation data - unique values: 2
20. orig_assembly: categorical - Original genome assembly version - unique values: 1
21. orig_chr: text - Original chromosome - unique values: 23
22. original_ID: text - Original ID - unique values: 99
23. refsnp_ID: text - Reference SNP ID - unique values: 99
24. score: categorical - Score value - unique values: 6
25. source: categorical - Source of the data - unique values: 1
26. type: categorical - Type of data - unique values: 1
27. current_end: Numerical - Current end position in the genome - range: 331297.0 to 230114260.0
28. current_start: Numerical - Current start position in the genome - range: 325610.0 to 230113600.0
29. orig_end: Numerical - Original end position in the genome - range: 325086.0 to 230250007.0
30. orig_start: Numerical - Original start position in the genome - range: 319399.0 to 230249347.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Gene
5. TranscriptionFactor
6. Disease
7. Publication
8. Method

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement
4. Mutation: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. targetsGene: Enhancer - Gene
4. regulatedByTF: Enhancer - TranscriptionFactor
5. associatedWithDisease: GeneticElement - Disease
6. hasPublication: GeneticElement - Publication
7. usesMethod: GeneticElement - Method

**Data Type Properties:**
1. biosampleName: Biosample - xsd:string
2. crmID: CisRegulatoryModule - xsd:string
3. crossrefID: GeneticElement - xsd:string
4. currentAssembly: GenomicCoordinate - xsd:string
5. currentChr: GenomicCoordinate - xsd:string
6. diseaseName: Disease - xsd:string
7. diseasePMID: Disease - xsd:string
8. diseaseMethod: Disease - xsd:string
9. enh2genePMID: Enhancer - xsd:string
10. enh2geneMethod: Enhancer - xsd:string
11. enhPMID: Enhancer - xsd:string
12. enhMethod: Enhancer - xsd:string
13. hgncSymbolTFs: TranscriptionFactor - xsd:string
14. hgncSymbolTargetGenes: Gene - xsd:string
15. minimumRatio: GeneticElement - xsd:float
16. mutationPMID: Mutation - xsd:string
17. mutationMethod: Mutation - xsd:string
18. origAssembly: GenomicCoordinate - xsd:string
19. origChr: GenomicCoordinate - xsd:string
20. originalID: GeneticElement - xsd:string
21. refsnpID: GeneticElement - xsd:string
22. score: GeneticElement - xsd:float
23. source: GeneticElement - xsd:string
24. type: GeneticElement - xsd:string
25. currentEnd: GenomicCoordinate - xsd:integer
26. currentStart: GenomicCoordinate - xsd:integer
27. origEnd: GenomicCoordinate - xsd:integer
28. origStart: GenomicCoordinate - xsd:integer