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
3. biosample_name: text - Name of the biosample - unique values: 20
4. crm_ID: text - ID of the cis-regulatory module - unique values: 25
5. crossref: text - Cross-reference ID - unique values: 25
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: categorical - Current chromosome - unique values: 4
8. disease: categorical - Associated disease - unique values: 1
9. disease_PMID: categorical - PubMed ID for disease association - unique values: 1
10. disease_method: categorical - Method used for disease association - unique values: 1
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene association - unique values: 3
12. enh2gene_method: categorical - Method used for enhancer to gene association - unique values: 2
13. enh_PMID: categorical - PubMed ID for enhancer - unique values: 2
14. enh_method: categorical - Method used for enhancer identification - unique values: 2
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 23
17. minimum_ratio: categorical - Minimum ratio - unique values: 1
18. mutation_PMID: categorical - PubMed ID for mutation - unique values: 1
19. mutation_method: categorical - Method used for mutation identification - unique values: 1
20. orig_assembly: categorical - Original genome assembly version - unique values: 1
21. orig_chr: categorical - Original chromosome - unique values: 4
22. original_ID: text - Original ID - unique values: 25
23. refsnp_ID: categorical - Reference SNP ID - unique values: 1
24. score: categorical - Score - unique values: 2
25. source: categorical - Source of the data - unique values: 1
26. type: categorical - Type of the data - unique values: 1
27. current_end: Numerical - Current end position in the genome - range: 1892695.0 to 228229323.0
28. current_start: Numerical - Current start position in the genome - range: 1761447.0 to 228162417.0
29. orig_end: Numerical - Original end position in the genome - range: 1824134.0 to 228417024.0
30. orig_start: Numerical - Original start position in the genome - range: 1692886.0 to 228350118.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Publication
6. Method
7. Gene
8. TranscriptionFactor

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement
4. SNP: subclass of -> GeneticElement

**Object Properties:**
1. hasBiosample: GeneticElement - Biosample
2. associatedWithDisease: GeneticElement - Disease
3. hasPublication: GeneticElement - Publication
4. identifiedByMethod: GeneticElement - Method
5. targetsGene: GeneticElement - Gene
6. regulatedByTF: GeneticElement - TranscriptionFactor
7. hasGenomicCoordinate: GeneticElement - GenomicCoordinate

**Data Type Properties:**
1. biosampleName: Biosample - xsd:string
2. diseaseName: Disease - xsd:string
3. publicationID: Publication - xsd:string
4. methodName: Method - xsd:string
5. geneSymbol: Gene - xsd:string
6. tfSymbol: TranscriptionFactor - xsd:string
7. crmID: CisRegulatoryModule - xsd:string
8. crossrefID: GeneticElement - xsd:string
9. currentAssembly: GenomicCoordinate - xsd:string
10. currentChr: GenomicCoordinate - xsd:string
11. origAssembly: GenomicCoordinate - xsd:string
12. origChr: GenomicCoordinate - xsd:string
13. originalID: GeneticElement - xsd:string
14. refSnpID: SNP - xsd:string
15. scoreValue: GeneticElement - xsd:float
16. sourceName: GeneticElement - xsd:string
17. typeName: GeneticElement - xsd:string
18. currentEnd: GenomicCoordinate - xsd:integer
19. currentStart: GenomicCoordinate - xsd:integer
20. origEnd: GenomicCoordinate - xsd:integer
21. origStart: GenomicCoordinate - xsd:integer