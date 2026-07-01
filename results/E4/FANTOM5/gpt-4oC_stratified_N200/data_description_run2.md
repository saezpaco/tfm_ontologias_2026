**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - [single value]
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer associations - [single value]
3. biosample: categorical - Type of biosample or cell line - [single value]
4. crm_ID: text - Unique identifier for cis-regulatory module - [unique values]
5. crossref: categorical - Cross-reference information - [single value]
6. current_assembly: categorical - Current genome assembly version - [single value]
7. current_chr: text - Current chromosome identifier - [24 unique values]
8. disease: categorical - Disease associated with the data - [single value]
9. disease_PMID: categorical - PubMed ID for disease association - [single value]
10. disease_method: categorical - Method used for disease association - [single value]
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - [two unique values]
12. enh2gene_method: categorical - Method used for enhancer to gene associations - [two unique values]
13. enh_PMID: categorical - PubMed ID for enhancer information - [single value]
14. enh_method: categorical - Method used for enhancer information - [single value]
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - [single value]
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - [120 unique values]
17. minimum_ratio: categorical - Minimum ratio value - [single value]
18. mutation_PMID: categorical - PubMed ID for mutation information - [single value]
19. mutation_method: categorical - Method used for mutation information - [single value]
20. orig_assembly: categorical - Original genome assembly version - [single value]
21. orig_chr: text - Original chromosome identifier - [24 unique values]
22. original_ID: categorical - Original identifier - [single value]
23. refsnp_ID: categorical - Reference SNP ID - [single value]
24. score: categorical - Score value - [single value]
25. source: categorical - Source of the data - [single value]
26. type: categorical - Type of data - [single value]
27. current_end: Numerical - Current end position in the genome - [373512.0 to 247360458.0]
28. current_start: Numerical - Current start position in the genome - [373277.0 to 247360162.0]
29. orig_end: Numerical - Original end position in the genome - [373627.0 to 247523760.0]
30. orig_start: Numerical - Original start position in the genome - [373392.0 to 247523464.0]

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

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. hasPublication: GeneticElement - Publication
5. usesMethod: GeneticElement - Method
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. crm_ID: CisRegulatoryModule - xsd:string
2. current_chr: GenomicCoordinate - xsd:string
3. orig_chr: GenomicCoordinate - xsd:string
4. hgnc_symbol_target_genes: Gene - xsd:string
5. current_end: GenomicCoordinate - xsd:integer
6. current_start: GenomicCoordinate - xsd:integer
7. orig_end: GenomicCoordinate - xsd:integer
8. orig_start: GenomicCoordinate - xsd:integer
9. TFs2enh_PMID: Publication - xsd:string
10. TFs2enh_method: Method - xsd:string
11. biosample: Biosample - xsd:string
12. crossref: GeneticElement - xsd:string
13. current_assembly: GenomicCoordinate - xsd:string
14. disease: Disease - xsd:string
15. disease_PMID: Publication - xsd:string
16. disease_method: Method - xsd:string
17. enh2gene_PMID: Publication - xsd:string
18. enh2gene_method: Method - xsd:string
19. enh_PMID: Publication - xsd:string
20. enh_method: Method - xsd:string
21. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
22. minimum_ratio: GeneticElement - xsd:float
23. mutation_PMID: Publication - xsd:string
24. mutation_method: Method - xsd:string
25. orig_assembly: GenomicCoordinate - xsd:string
26. original_ID: GeneticElement - xsd:string
27. refsnp_ID: GeneticElement - xsd:string
28. score: GeneticElement - xsd:float
29. source: GeneticElement - xsd:string
30. type: GeneticElement - xsd:string