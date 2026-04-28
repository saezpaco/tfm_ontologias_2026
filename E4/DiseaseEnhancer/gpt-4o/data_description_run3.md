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
4. crm_ID: text - ID of the cis-regulatory module - 23 unique values
5. crossref: categorical - Cross-reference information - unique value
6. current_assembly: categorical - Current genome assembly version - unique value
7. current_chr: text - Current chromosome - 12 unique values
8. disease: text - Disease associated with the data - 18 unique values
9. disease_method: categorical - Method used for disease association - unique value
10. enh2gene_PMID: text - PubMed ID for enhancer to gene mapping - 16 unique values
11. enh2gene_method: categorical - Method used for enhancer to gene mapping - unique value
12. enh_method: categorical - Method used for enhancer identification - unique value
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique value
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - 19 unique values
15. minimum_ratio: categorical - Minimum ratio value - 0.95
16. mutation_PMID: text - PubMed ID for mutation information - 11 unique values
17. mutation_method: categorical - Method used for mutation identification - unique value
18. orig_assembly: categorical - Original genome assembly version - unique value
19. orig_chr: text - Original chromosome - 12 unique values
20. original_ID: text - Original ID of the data entry - 23 unique values
21. refseq_ID: text - RefSeq ID - 11 unique values
22. score: categorical - Score value - 1.0
23. source: categorical - Source of the data - unique value
24. type: categorical - Type of the data entry - unique value
25. current_end: Numerical - End coordinate in the current assembly - range: 6062837.0 to 201340077.0
26. current_start: Numerical - Start coordinate in the current assembly - range: 6032039.0 to 201339879.0
27. disease_PMID: Numerical - PubMed ID for disease information - range: 19543368.0 to 28234966.0
28. enh_PMID: Numerical - PubMed ID for enhancer information - range: 19543368.0 to 28234966.0
29. orig_end: Numerical - End coordinate in the original assembly - range: 6104800.0 to 202204800.0
30. orig_start: Numerical - Start coordinate in the original assembly - range: 6074002.0 to 202204602.0

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
2. associatedWithBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. crm_ID: CisRegulatoryModule - xsd:string
2. current_assembly: GenomicCoordinate - xsd:string
3. current_chr: GenomicCoordinate - xsd:string
4. current_end: GenomicCoordinate - xsd:decimal
5. current_start: GenomicCoordinate - xsd:decimal
6. disease: Disease - xsd:string
7. enh2gene_PMID: Publication - xsd:string
8. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
9. hgnc_symbol_target_genes: Gene - xsd:string
10. minimum_ratio: GeneticElement - xsd:decimal
11. mutation_PMID: Publication - xsd:string
12. orig_assembly: GenomicCoordinate - xsd:string
13. orig_chr: GenomicCoordinate - xsd:string
14. orig_end: GenomicCoordinate - xsd:decimal
15. orig_start: GenomicCoordinate - xsd:decimal
16. original_ID: GeneticElement - xsd:string
17. refseq_ID: Gene - xsd:string
18. score: GeneticElement - xsd:decimal
19. source: GeneticElement - xsd:string
20. type: GeneticElement - xsd:string