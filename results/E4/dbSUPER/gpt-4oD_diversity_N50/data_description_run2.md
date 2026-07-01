**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer association - unique
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer association - unique
3. biosample_name: text - Name of the biosample - unique
4. crm_ID: text - Cis-regulatory module ID - unique
5. crossref: text - Cross-reference ID - unique
6. current_assembly: categorical - Current genome assembly version - unique
7. current_chr: text - Current chromosome - unique
8. disease: categorical - Disease associated - unique
9. disease_PMID: categorical - PubMed ID for disease association - unique
10. disease_method: categorical - Method used for disease association - unique
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene association - multiple
12. enh2gene_method: categorical - Method used for enhancer to gene association - multiple
13. enh_PMID: categorical - PubMed ID for enhancer - multiple
14. enh_method: categorical - Method used for enhancer identification - multiple
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique
17. minimum_ratio: categorical - Minimum ratio - unique
18. mutation_PMID: categorical - PubMed ID for mutation - unique
19. mutation_method: categorical - Method used for mutation identification - unique
20. orig_assembly: categorical - Original genome assembly version - unique
21. orig_chr: text - Original chromosome - unique
22. original_ID: text - Original ID - unique
23. refsnp_ID: categorical - Reference SNP ID - unique
24. source: categorical - Source of the data - unique
25. type: categorical - Type of the data - unique
26. current_end: Numerical - Current end position in the genome - range
27. current_start: Numerical - Current start position in the genome - range
28. orig_end: Numerical - Original end position in the genome - range
29. orig_start: Numerical - Original start position in the genome - range
30. score: Numerical - Score value - range

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
7. identifiedByMethod: GeneticElement - Method

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
22. source: GeneticElement - xsd:string
23. type: GeneticElement - xsd:string
24. currentEnd: GenomicCoordinate - xsd:integer
25. currentStart: GenomicCoordinate - xsd:integer
26. origEnd: GenomicCoordinate - xsd:integer
27. origStart: GenomicCoordinate - xsd:integer
28. score: GeneticElement - xsd:float