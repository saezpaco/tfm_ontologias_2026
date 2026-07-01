**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer mapping - unique value
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer mapping - unique value
3. biosample_name: categorical - Name of the biosample - unique value
4. crm_ID: text - ID of the cis-regulatory module - 19 unique values
5. crossref: categorical - Cross-reference information - unique value
6. current_assembly: categorical - Current genome assembly version - unique value
7. current_chr: categorical - Current chromosome - 5 unique values
8. disease: text - Disease associated with the data - 33 unique values
9. disease_method: categorical - Method used for disease association - unique value
10. enh2gene_PMID: text - PubMed ID for enhancer to gene mapping - 18 unique values
11. enh2gene_method: categorical - Method used for enhancer to gene mapping - unique value
12. enh_method: categorical - Method used for enhancer identification - unique value
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique value
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - 16 unique values
15. minimum_ratio: categorical - Minimum ratio value - 0.95
16. mutation_PMID: text - PubMed ID for mutation information - 12 unique values
17. mutation_method: categorical - Method used for mutation identification - unique value
18. orig_assembly: categorical - Original genome assembly version - unique value
19. orig_chr: categorical - Original chromosome - 5 unique values
20. original_ID: text - Original ID of the data - 21 unique values
21. refseq_ID: text - RefSeq ID - 12 unique values
22. score: categorical - Score value - 1.0
23. source: categorical - Source of the data - unique value
24. type: categorical - Type of the data - unique value
25. current_end: Numerical - Current end coordinate - 107935 to 243478698
26. current_start: Numerical - Current start coordinate - 105934 to 243469900
27. disease_PMID: Numerical - PubMed ID for disease information - 16269442 to 28717659
28. enh_PMID: Numerical - PubMed ID for enhancer information - 16269442 to 28717659
29. orig_end: Numerical - Original end coordinate - 107935 to 243642000
30. orig_start: Numerical - Original start coordinate - 105934 to 243633202

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. Gene
8. TranscriptionFactor

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. crm_ID: CisRegulatoryModule - xsd:string
2. current_assembly: GenomicCoordinate - xsd:string
3. current_chr: GenomicCoordinate - xsd:string
4. current_end: GenomicCoordinate - xsd:integer
5. current_start: GenomicCoordinate - xsd:integer
6. orig_assembly: GenomicCoordinate - xsd:string
7. orig_chr: GenomicCoordinate - xsd:string
8. orig_end: GenomicCoordinate - xsd:integer
9. orig_start: GenomicCoordinate - xsd:integer
10. biosample_name: Biosample - xsd:string
11. disease: Disease - xsd:string
12. disease_PMID: Disease - xsd:integer
13. enh2gene_PMID: Publication - xsd:string
14. enh_PMID: Publication - xsd:integer
15. mutation_PMID: Publication - xsd:string
16. original_ID: GeneticElement - xsd:string
17. refseq_ID: Gene - xsd:string
18. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
19. hgnc_symbol_target_genes: Gene - xsd:string
20. minimum_ratio: GeneticElement - xsd:float
21. score: GeneticElement - xsd:float
22. source: GeneticElement - xsd:string
23. type: GeneticElement - xsd:string