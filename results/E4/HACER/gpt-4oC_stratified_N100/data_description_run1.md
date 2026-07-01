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
3. biosample_name: text - Name of the biosample - unique_count: 100
4. crm_ID: text - ID of the cis-regulatory module - unique_count: 100
5. crossref: categorical - Cross-reference ID - unique_count: 6
6. current_assembly: categorical - Current genome assembly version - unique_count: 1
7. current_chr: text - Current chromosome - unique_count: 22
8. disease: categorical - Disease associated - unique_count: 1
9. disease_PMID: categorical - PubMed ID for disease association - unique_count: 1
10. disease_method: categorical - Method used for disease association - unique_count: 1
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene association - unique_count: 2
12. enh2gene_method: categorical - Method used for enhancer to gene association - unique_count: 4
13. enh_PMID: categorical - PubMed ID for enhancer - unique_count: 1
14. enh_method: categorical - Method used for enhancer identification - unique_count: 2
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique_count: 1
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique_count: 70
17. minimum_ratio: categorical - Minimum ratio - unique_count: 1
18. mutation_PMID: categorical - PubMed ID for mutation - unique_count: 2
19. mutation_method: categorical - Method used for mutation identification - unique_count: 2
20. orig_assembly: categorical - Original genome assembly version - unique_count: 1
21. orig_chr: text - Original chromosome - unique_count: 22
22. original_ID: categorical - Original ID - unique_count: 6
23. refsnp_ID: categorical - Reference SNP ID - unique_count: 6
24. score: categorical - Score - unique_count: 1
25. source: categorical - Source of the data - unique_count: 1
26. type: categorical - Type of the data - unique_count: 1
27. current_end: Numerical - Current end position in the genome - range: 3025796.0 to 241763444.0
28. current_start: Numerical - Current start position in the genome - range: 3025518.0 to 241763028.0
29. orig_end: Numerical - Original end position in the genome - range: 3065430.0 to 242702859.0
30. orig_start: Numerical - Original start position in the genome - range: 3065152.0 to 242702443.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Gene
5. TranscriptionFactor
6. Disease
7. Method
8. Publication

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement
4. SNP: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. targetsGene: Enhancer - Gene
4. regulatedByTF: Enhancer - TranscriptionFactor
5. associatedWithDisease: GeneticElement - Disease
6. identifiedByMethod: GeneticElement - Method
7. referencedInPublication: GeneticElement - Publication

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
16. mutationPMID: SNP - xsd:string
17. mutationMethod: SNP - xsd:string
18. origAssembly: GenomicCoordinate - xsd:string
19. origChr: GenomicCoordinate - xsd:string
20. originalID: GeneticElement - xsd:string
21. refsnpID: SNP - xsd:string
22. score: GeneticElement - xsd:float
23. source: GeneticElement - xsd:string
24. type: GeneticElement - xsd:string
25. currentEnd: GenomicCoordinate - xsd:integer
26. currentStart: GenomicCoordinate - xsd:integer
27. origEnd: GenomicCoordinate - xsd:integer
28. origStart: GenomicCoordinate - xsd:integer