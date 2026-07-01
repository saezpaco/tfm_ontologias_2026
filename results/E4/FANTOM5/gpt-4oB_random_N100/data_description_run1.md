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
4. crm_ID: text - Cis-regulatory module ID - unique value
5. crossref: categorical - Cross-reference information - single value
6. current_assembly: categorical - Current genome assembly version - single value
7. current_chr: text - Current chromosome - 23 unique values
8. disease: categorical - Disease associated - single value
9. disease_PMID: categorical - PubMed ID for disease - single value
10. disease_method: categorical - Method used for disease association - single value
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene - two unique values
12. enh2gene_method: categorical - Method used for enhancer to gene - two unique values
13. enh_PMID: categorical - PubMed ID for enhancer - single value
14. enh_method: categorical - Method used for enhancer - single value
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - single value
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - 66 unique values
17. minimum_ratio: categorical - Minimum ratio - single value
18. mutation_PMID: categorical - PubMed ID for mutation - single value
19. mutation_method: categorical - Method used for mutation - single value
20. orig_assembly: categorical - Original genome assembly version - single value
21. orig_chr: text - Original chromosome - 23 unique values
22. original_ID: categorical - Original ID - single value
23. refsnp_ID: categorical - Reference SNP ID - single value
24. score: categorical - Score - single value
25. source: categorical - Source of data - single value
26. type: categorical - Type of data - single value
27. current_end: Numerical - Current end position in genome - range from 790270 to 241905502
28. current_start: Numerical - Current start position in genome - range from 790053 to 241905360
29. orig_end: Numerical - Original end position in genome - range from 693510 to 242068804
30. orig_start: Numerical - Original start position in genome - range from 693293 to 242068662

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. Gene
8. TranscriptionFactor
9. SNP

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. Chromosome: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor
8. hasSNP: GeneticElement - SNP

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. crossref: GeneticElement - xsd:string
3. current_assembly: GenomicCoordinate - xsd:string
4. current_chr: GenomicCoordinate - xsd:string
5. current_end: GenomicCoordinate - xsd:integer
6. current_start: GenomicCoordinate - xsd:integer
7. orig_assembly: GenomicCoordinate - xsd:string
8. orig_chr: GenomicCoordinate - xsd:string
9. orig_end: GenomicCoordinate - xsd:integer
10. orig_start: GenomicCoordinate - xsd:integer
11. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
12. hgnc_symbol_target_genes: Gene - xsd:string
13. minimum_ratio: GeneticElement - xsd:float
14. original_ID: GeneticElement - xsd:string
15. refsnp_ID: SNP - xsd:string
16. score: GeneticElement - xsd:float
17. source: GeneticElement - xsd:string
18. type: GeneticElement - xsd:string