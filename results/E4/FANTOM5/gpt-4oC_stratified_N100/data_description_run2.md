**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer - single value
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer - single value
3. biosample: categorical - Biosample or cell line - single value
4. crm_ID: text - Cis-regulatory module ID - unique values
5. crossref: categorical - Cross-reference information - single value
6. current_assembly: categorical - Current genome assembly version - single value
7. current_chr: text - Current chromosome - multiple values
8. disease: categorical - Disease associated - single value
9. disease_PMID: categorical - PubMed ID for disease - single value
10. disease_method: categorical - Method used for disease association - single value
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene - two values
12. enh2gene_method: categorical - Method used for enhancer to gene - two values
13. enh_PMID: categorical - PubMed ID for enhancer - single value
14. enh_method: categorical - Method used for enhancer identification - single value
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - single value
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - multiple values
17. minimum_ratio: categorical - Minimum ratio - single value
18. mutation_PMID: categorical - PubMed ID for mutation - single value
19. mutation_method: categorical - Method used for mutation - single value
20. orig_assembly: categorical - Original genome assembly version - single value
21. orig_chr: text - Original chromosome - multiple values
22. original_ID: categorical - Original ID - single value
23. refsnp_ID: categorical - Reference SNP ID - single value
24. score: categorical - Score - single value
25. source: categorical - Source of data - single value
26. type: categorical - Type of data - single value
27. current_end: Numerical - Current end position in genome - range from 1085427 to 247360458
28. current_start: Numerical - Current start position in genome - range from 1085285 to 247360162
29. orig_end: Numerical - Original end position in genome - range from 1085426 to 247523760
30. orig_start: Numerical - Original start position in genome - range from 1085284 to 247523464

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Publication
6. Method
7. Gene
8. TranscriptionFactor
9. Mutation

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. Chromosome: subclass of -> GeneticElement

**Object Properties:**
1. hasBiosample: GeneticElement - Biosample
2. associatedWithDisease: GeneticElement - Disease
3. hasPublication: GeneticElement - Publication
4. identifiedByMethod: GeneticElement - Method
5. targetsGene: GeneticElement - Gene
6. regulatedByTF: GeneticElement - TranscriptionFactor
7. hasMutation: GeneticElement - Mutation
8. hasGenomicCoordinate: GeneticElement - GenomicCoordinate

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. crossref: GeneticElement - xsd:string
3. current_assembly: GenomicCoordinate - xsd:string
4. current_chr: GenomicCoordinate - xsd:string
5. current_end: GenomicCoordinate - xsd:integer
6. current_start: GenomicCoordinate - xsd:integer
7. disease: Disease - xsd:string
8. disease_PMID: Disease - xsd:string
9. disease_method: Disease - xsd:string
10. enh2gene_PMID: Publication - xsd:string
11. enh2gene_method: Method - xsd:string
12. enh_PMID: Publication - xsd:string
13. enh_method: Method - xsd:string
14. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
15. hgnc_symbol_target_genes: Gene - xsd:string
16. minimum_ratio: GeneticElement - xsd:float
17. mutation_PMID: Mutation - xsd:string
18. mutation_method: Method - xsd:string
19. orig_assembly: GenomicCoordinate - xsd:string
20. orig_chr: GenomicCoordinate - xsd:string
21. orig_end: GenomicCoordinate - xsd:integer
22. orig_start: GenomicCoordinate - xsd:integer
23. original_ID: GeneticElement - xsd:string
24. refsnp_ID: GeneticElement - xsd:string
25. score: GeneticElement - xsd:float
26. source: GeneticElement - xsd:string
27. type: GeneticElement - xsd:string