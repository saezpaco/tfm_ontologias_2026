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
3. biosample: categorical - Biosample or cell line used in the study - unique values: 1
4. crm_ID: text - Cis-regulatory module identifier - unique values: 24
5. crossref: categorical - Cross-reference identifier - unique values: 1
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: categorical - Current chromosome - unique values: 4
8. disease: categorical - Disease associated with the data - unique values: 1
9. disease_PMID: categorical - PubMed ID for disease association - unique values: 1
10. disease_method: categorical - Method used for disease association - unique values: 1
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - unique values: 2
12. enh2gene_method: categorical - Method used for enhancer to gene associations - unique values: 2
13. enh_PMID: categorical - PubMed ID for enhancer data - unique values: 1
14. enh_method: categorical - Method used for enhancer data - unique values: 1
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 21
17. minimum_ratio: categorical - Minimum ratio value - unique values: 1
18. mutation_PMID: categorical - PubMed ID for mutation data - unique values: 1
19. mutation_method: categorical - Method used for mutation data - unique values: 1
20. orig_assembly: categorical - Original genome assembly version - unique values: 1
21. orig_chr: categorical - Original chromosome - unique values: 4
22. original_ID: categorical - Original identifier - unique values: 1
23. refsnp_ID: categorical - Reference SNP ID - unique values: 1
24. score: categorical - Score value - unique values: 1
25. source: categorical - Source of the data - unique values: 1
26. type: categorical - Type of data - unique values: 1
27. current_end: Numerical - Current end position in the genome - range: 16040344.0 to 212088783.0
28. current_start: Numerical - Current start position in the genome - range: 16039967.0 to 212088562.0
29. orig_end: Numerical - Original end position in the genome - range: 16366839.0 to 212262125.0
30. orig_start: Numerical - Original start position in the genome - range: 16366462.0 to 212261904.0

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
12. disease_PMID: Disease - xsd:string
13. enh2gene_PMID: Publication - xsd:string
14. enh2gene_method: Method - xsd:string
15. enh_PMID: Publication - xsd:string
16. enh_method: Method - xsd:string
17. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
18. hgnc_symbol_target_genes: Gene - xsd:string
19. minimum_ratio: GeneticElement - xsd:float
20. mutation_PMID: Publication - xsd:string
21. mutation_method: Method - xsd:string
22. original_ID: GeneticElement - xsd:string
23. refsnp_ID: GeneticElement - xsd:string
24. score: GeneticElement - xsd:float
25. source: GeneticElement - xsd:string
26. type: GeneticElement - xsd:string