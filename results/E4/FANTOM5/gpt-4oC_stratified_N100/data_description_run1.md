**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer - unique value
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer - unique value
3. biosample: categorical - Biosample or cell line used - unique value
4. crm_ID: text - Cis-regulatory module ID - unique values
5. crossref: categorical - Cross-reference information - unique value
6. current_assembly: categorical - Current genome assembly version - unique value
7. current_chr: text - Current chromosome - 24 unique values
8. disease: categorical - Disease associated - unique value
9. disease_PMID: categorical - PubMed ID for disease association - unique value
10. disease_method: categorical - Method used for identifying disease association - unique value
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene association - 2 unique values
12. enh2gene_method: categorical - Method used for identifying enhancer to gene association - 2 unique values
13. enh_PMID: categorical - PubMed ID for enhancer - single value
14. enh_method: categorical - Method used for identifying enhancer - unique value
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique value
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - 54 unique values
17. minimum_ratio: categorical - Minimum ratio - single value
18. mutation_PMID: categorical - PubMed ID for mutation - unique value
19. mutation_method: categorical - Method used for identifying mutation - unique value
20. orig_assembly: categorical - Original genome assembly version - unique value
21. orig_chr: text - Original chromosome - 24 unique values
22. original_ID: categorical - Original ID - unique value
23. refsnp_ID: categorical - Reference SNP ID - unique value
24. score: categorical - Score - single value
25. source: categorical - Source of data - unique value
26. type: categorical - Type of data - unique value
27. current_end: Numerical - Current end position in genome - range: 1085427.0 to 247360458.0
28. current_start: Numerical - Current start position in genome - range: 1085285.0 to 247360162.0
29. orig_end: Numerical - Original end position in genome - range: 1085426.0 to 247523760.0
30. orig_start: Numerical - Original start position in genome - range: 1085284.0 to 247523464.0

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
5. identifiedByMethod: GeneticElement - Method
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
10. biosample: Biosample - xsd:string
11. disease: Disease - xsd:string
12. enh2gene_PMID: Publication - xsd:string
13. enh2gene_method: Method - xsd:string
14. enh_PMID: Publication - xsd:string
15. enh_method: Method - xsd:string
16. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
17. hgnc_symbol_target_genes: Gene - xsd:string
18. minimum_ratio: GeneticElement - xsd:float
19. mutation_PMID: Publication - xsd:string
20. mutation_method: Method - xsd:string
21. original_ID: GeneticElement - xsd:string
22. refsnp_ID: GeneticElement - xsd:string
23. score: GeneticElement - xsd:float
24. source: GeneticElement - xsd:string
25. type: GeneticElement - xsd:string