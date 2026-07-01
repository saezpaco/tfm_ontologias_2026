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
3. biosample_name: text - Name of the biosample or cell line - unique values: 95
4. crm_ID: text - ID for cis-regulatory module - unique values: 100
5. crossref: text - Cross-reference ID - unique values: 100
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: text - Current chromosome - unique values: 23
8. disease: categorical - Disease associated with the data - unique values: 1
9. disease_PMID: categorical - PubMed ID for disease associations - unique values: 1
10. disease_method: categorical - Method used for disease associations - unique values: 1
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - unique values: 8
12. enh2gene_method: categorical - Method used for enhancer to gene associations - unique values: 2
13. enh_PMID: categorical - PubMed ID for enhancer data - unique values: 7
14. enh_method: categorical - Method used for enhancer data - unique values: 3
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 100
17. minimum_ratio: categorical - Minimum ratio value - unique values: 1
18. mutation_PMID: categorical - PubMed ID for mutation data - unique values: 1
19. mutation_method: categorical - Method used for mutation data - unique values: 1
20. orig_assembly: categorical - Original genome assembly version - unique values: 1
21. orig_chr: text - Original chromosome - unique values: 23
22. original_ID: text - Original ID - unique values: 100
23. refsnp_ID: categorical - Reference SNP ID - unique values: 1
24. source: categorical - Source of the data - unique values: 1
25. type: categorical - Type of data - unique values: 1
26. current_end: Numerical - Current end position in the genome - range: 121087.0 to 206591648.0
27. current_start: Numerical - Current start position in the genome - range: 104619.0 to 206550559.0
28. orig_end: Numerical - Original end position in the genome - range: 171086.0 to 206764980.0
29. orig_start: Numerical - Original start position in the genome - range: 154617.0 to 206723887.0
30. score: Numerical - Score value - range: 0.9861407 to 1.005692

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
9. disease_PMID: Disease - xsd:string
10. disease_method: Disease - xsd:string
11. enh2gene_PMID: GeneticElement - xsd:string
12. enh2gene_method: GeneticElement - xsd:string
13. enh_PMID: GeneticElement - xsd:string
14. enh_method: GeneticElement - xsd:string
15. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
16. hgnc_symbol_target_genes: Gene - xsd:string
17. minimum_ratio: GeneticElement - xsd:float
18. mutation_PMID: GeneticElement - xsd:string
19. mutation_method: GeneticElement - xsd:string
20. orig_assembly: GenomicCoordinate - xsd:string
21. orig_chr: GenomicCoordinate - xsd:string
22. original_ID: GeneticElement - xsd:string
23. refsnp_ID: GeneticElement - xsd:string
24. source: GeneticElement - xsd:string
25. type: GeneticElement - xsd:string
26. current_end: GenomicCoordinate - xsd:integer
27. current_start: GenomicCoordinate - xsd:integer
28. orig_end: GenomicCoordinate - xsd:integer
29. orig_start: GenomicCoordinate - xsd:integer
30. score: GeneticElement - xsd:float