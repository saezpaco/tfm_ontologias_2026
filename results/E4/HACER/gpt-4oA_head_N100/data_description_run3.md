**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer mapping - unique values: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer mapping - unique values: 1
3. biosample_name: text - Name of the biosample or cell line - unique values: 29
4. crm_ID: categorical - ID for cis-regulatory module - unique values: 7
5. crossref: categorical - Cross-reference information - unique values: 1
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: categorical - Current chromosome - unique values: 4
8. current_end: categorical - End position in the current genome assembly - unique values: 7
9. current_start: categorical - Start position in the current genome assembly - unique values: 7
10. disease: categorical - Disease associated with the data - unique values: 1
11. disease_PMID: categorical - PubMed ID for disease association - unique values: 1
12. disease_method: categorical - Method used for disease association - unique values: 1
13. enh2gene_PMID: categorical - PubMed ID for enhancer to gene mapping - unique values: 2
14. enh2gene_method: categorical - Method used for enhancer to gene mapping - unique values: 4
15. enh_PMID: categorical - PubMed ID for enhancer information - unique values: 1
16. enh_method: categorical - Method used for enhancer identification - unique values: 1
17. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
18. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 14
19. minimum_ratio: categorical - Minimum ratio value - unique values: 1
20. mutation_PMID: categorical - PubMed ID for mutation information - unique values: 1
21. mutation_method: categorical - Method used for mutation identification - unique values: 1
22. orig_assembly: categorical - Original genome assembly version - unique values: 1
23. orig_chr: categorical - Original chromosome - unique values: 4
24. orig_end: categorical - End position in the original genome assembly - unique values: 7
25. orig_start: categorical - Start position in the original genome assembly - unique values: 7
26. original_ID: categorical - Original ID for the data - unique values: 1
27. refsnp_ID: categorical - Reference SNP ID - unique values: 1
28. score: categorical - Score value - unique values: 1
29. source: categorical - Source of the data - unique values: 1
30. type: categorical - Type of the data - unique values: 1

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Gene
5. TranscriptionFactor
6. Disease

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. targetsGene: GeneticElement - Gene
4. regulatedBy: GeneticElement - TranscriptionFactor
5. associatedWithDisease: GeneticElement - Disease

**Data Type Properties:**
1. TFs2enh_PMID: GeneticElement - xsd:string
2. TFs2enh_method: GeneticElement - xsd:string
3. biosample_name: Biosample - xsd:string
4. crm_ID: CisRegulatoryModule - xsd:string
5. crossref: GeneticElement - xsd:string
6. current_assembly: GenomicCoordinate - xsd:string
7. current_chr: GenomicCoordinate - xsd:string
8. current_end: GenomicCoordinate - xsd:integer
9. current_start: GenomicCoordinate - xsd:integer
10. disease: Disease - xsd:string
11. disease_PMID: Disease - xsd:string
12. disease_method: Disease - xsd:string
13. enh2gene_PMID: GeneticElement - xsd:string
14. enh2gene_method: GeneticElement - xsd:string
15. enh_PMID: Enhancer - xsd:string
16. enh_method: Enhancer - xsd:string
17. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
18. hgnc_symbol_target_genes: Gene - xsd:string
19. minimum_ratio: GeneticElement - xsd:float
20. mutation_PMID: GeneticElement - xsd:string
21. mutation_method: GeneticElement - xsd:string
22. orig_assembly: GenomicCoordinate - xsd:string
23. orig_chr: GenomicCoordinate - xsd:string
24. orig_end: GenomicCoordinate - xsd:integer
25. orig_start: GenomicCoordinate - xsd:integer
26. original_ID: GeneticElement - xsd:string
27. refsnp_ID: GeneticElement - xsd:string
28. score: GeneticElement - xsd:float
29. source: GeneticElement - xsd:string
30. type: GeneticElement - xsd:string