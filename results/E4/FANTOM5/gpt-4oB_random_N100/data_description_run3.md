**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - unique
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer associations - unique
3. biosample: categorical - Type of biosample or cell line used - unique
4. crm_ID: text - Unique identifier for cis-regulatory module - unique
5. crossref: categorical - Cross-reference information - unique
6. current_assembly: categorical - Current genome assembly version - unique
7. current_chr: text - Current chromosome identifier - 23 unique values
8. disease: categorical - Disease associated with the data - unique
9. disease_PMID: categorical - PubMed ID for disease association - unique
10. disease_method: categorical - Method used for identifying disease association - unique
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - 2 unique values
12. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - 2 unique values
13. enh_PMID: categorical - PubMed ID for enhancer information - 1 unique value
14. enh_method: categorical - Method used for identifying enhancer - unique
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - 66 unique values
17. minimum_ratio: categorical - Minimum ratio value - 0.95
18. mutation_PMID: categorical - PubMed ID for mutation information - unique
19. mutation_method: categorical - Method used for identifying mutation - unique
20. orig_assembly: categorical - Original genome assembly version - unique
21. orig_chr: text - Original chromosome identifier - 23 unique values
22. original_ID: categorical - Original identifier - unique
23. refsnp_ID: categorical - Reference SNP ID - unique
24. score: categorical - Score value - 1.0
25. source: categorical - Source of the data - unique
26. type: categorical - Type of data - unique
27. current_end: Numerical - Current end position in the genome - range: 790270.0 to 241905502.0
28. current_start: Numerical - Current start position in the genome - range: 790053.0 to 241905360.0
29. orig_end: Numerical - Original end position in the genome - range: 693510.0 to 242068804.0
30. orig_start: Numerical - Original start position in the genome - range: 693293.0 to 242068662.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Publication
6. Method
7. Gene
8. TranscriptionFactor
9. SNP

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. hasPublication: GeneticElement - Publication
5. identifiedByMethod: GeneticElement - Method
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: Gene - TranscriptionFactor
8. hasSNP: GeneticElement - SNP

**Data Type Properties:**
1. crm_ID: CisRegulatoryModule - xsd:string
2. current_chr: GenomicCoordinate - xsd:string
3. current_end: GenomicCoordinate - xsd:integer
4. current_start: GenomicCoordinate - xsd:integer
5. orig_chr: GenomicCoordinate - xsd:string
6. orig_end: GenomicCoordinate - xsd:integer
7. orig_start: GenomicCoordinate - xsd:integer
8. biosample: Biosample - xsd:string
9. disease: Disease - xsd:string
10. enh2gene_PMID: Publication - xsd:string
11. enh2gene_method: Method - xsd:string
12. enh_PMID: Publication - xsd:string
13. enh_method: Method - xsd:string
14. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
15. hgnc_symbol_target_genes: Gene - xsd:string
16. minimum_ratio: GeneticElement - xsd:float
17. mutation_PMID: Publication - xsd:string
18. mutation_method: Method - xsd:string
19. original_ID: GeneticElement - xsd:string
20. refsnp_ID: SNP - xsd:string
21. score: GeneticElement - xsd:float
22. source: GeneticElement - xsd:string
23. type: GeneticElement - xsd:string