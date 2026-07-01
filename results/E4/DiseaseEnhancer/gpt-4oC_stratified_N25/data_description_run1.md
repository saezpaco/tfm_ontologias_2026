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
3. biosample_name: categorical - Name of the biosample - unique values: 1
4. crm_ID: text - ID for cis-regulatory module - unique values: 25
5. crossref: categorical - Cross-reference information - unique values: 1
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: text - Current chromosome - unique values: 23
8. disease: text - Disease associated with the data - unique values: 18
9. disease_method: categorical - Method used for disease association - unique values: 1
10. enh2gene_method: categorical - Method used for enhancer to gene mapping - unique values: 1
11. enh_method: categorical - Method used for enhancer identification - unique values: 1
12. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
13. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 25
14. minimum_ratio: categorical - Minimum ratio value - unique values: 1, range: 0.95
15. mutation_PMID: categorical - PubMed ID for mutation information - unique values: 8
16. mutation_method: categorical - Method used for mutation identification - unique values: 1
17. orig_assembly: categorical - Original genome assembly version - unique values: 1
18. orig_chr: text - Original chromosome - unique values: 23
19. original_ID: text - Original ID for the data entry - unique values: 25
20. refseq_ID: text - RefSeq ID - unique values: 12
21. score: categorical - Score value - unique values: 1, range: 1.0
22. source: categorical - Source of the data - unique values: 1
23. type: categorical - Type of data - unique values: 1
24. current_end: Numerical - End position in the current genome assembly - range: 2831570.0 to 166981712.0
25. current_start: Numerical - Start position in the current genome assembly - range: 2823972.0 to 166981514.0
26. disease_PMID: Numerical - PubMed ID for disease information - range: 19543368.0 to 29093029.0
27. enh2gene_PMID: Numerical - PubMed ID for enhancer to gene mapping - range: 19543368.0 to 29093029.0
28. enh_PMID: Numerical - PubMed ID for enhancer information - range: 19543368.0 to 29093029.0
29. orig_end: Numerical - End position in the original genome assembly - range: 2852800.0 to 167395200.0
30. orig_start: Numerical - Start position in the original genome assembly - range: 2845202.0 to 167395002.0

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
4. crm_ID: GeneticElement - xsd:string
5. crossref: GeneticElement - xsd:string
6. current_assembly: GenomicCoordinate - xsd:string
7. current_chr: GenomicCoordinate - xsd:string
8. disease: Disease - xsd:string
9. disease_method: Disease - xsd:string
10. enh2gene_method: GeneticElement - xsd:string
11. enh_method: GeneticElement - xsd:string
12. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
13. hgnc_symbol_target_genes: Gene - xsd:string
14. minimum_ratio: GeneticElement - xsd:float
15. mutation_PMID: GeneticElement - xsd:string
16. mutation_method: GeneticElement - xsd:string
17. orig_assembly: GenomicCoordinate - xsd:string
18. orig_chr: GenomicCoordinate - xsd:string
19. original_ID: GeneticElement - xsd:string
20. refseq_ID: Gene - xsd:string
21. score: GeneticElement - xsd:float
22. source: GeneticElement - xsd:string
23. type: GeneticElement - xsd:string
24. current_end: GenomicCoordinate - xsd:integer
25. current_start: GenomicCoordinate - xsd:integer
26. disease_PMID: Disease - xsd:integer
27. enh2gene_PMID: GeneticElement - xsd:integer
28. enh_PMID: GeneticElement - xsd:integer
29. orig_end: GenomicCoordinate - xsd:integer
30. orig_start: GenomicCoordinate - xsd:integer