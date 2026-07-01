**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - categorical
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer associations - categorical
3. biosample_name: categorical - Name of the biosample or cell line - categorical
4. crm_ID: text - Unique identifier for cis-regulatory modules - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: text - Current chromosome identifier - text
8. disease: text - Disease associated with the genetic element - text
9. disease_method: categorical - Method used for identifying disease associations - categorical
10. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - categorical
11. enh_method: categorical - Method used for identifying enhancers - categorical
12. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
13. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
14. minimum_ratio: categorical - Minimum ratio value - categorical
15. mutation_PMID: categorical - PubMed ID for mutation information - categorical
16. mutation_method: categorical - Method used for identifying mutations - categorical
17. orig_assembly: categorical - Original genome assembly version - categorical
18. orig_chr: text - Original chromosome identifier - text
19. original_ID: text - Original identifier for the genetic element - text
20. refseq_ID: text - RefSeq identifier - text
21. score: categorical - Score value - categorical
22. source: categorical - Source of the data - categorical
23. type: categorical - Type of genetic element - categorical
24. current_end: Numerical - Current end position on the chromosome - Numerical
25. current_start: Numerical - Current start position on the chromosome - Numerical
26. disease_PMID: Numerical - PubMed ID for disease information - Numerical
27. enh2gene_PMID: Numerical - PubMed ID for enhancer to gene associations - Numerical
28. enh_PMID: Numerical - PubMed ID for enhancer information - Numerical
29. orig_end: Numerical - Original end position on the chromosome - Numerical
30. orig_start: Numerical - Original start position on the chromosome - Numerical

**classes:**
1. GeneticElement
2. Biosample
3. Disease
4. Method
5. Publication

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. TranscriptionFactor: subclass of -> GeneticElement
4. TargetGene: subclass of -> GeneticElement

**Object Properties:**
1. hasBiosample: GeneticElement - Biosample
2. associatedWithDisease: GeneticElement - Disease
3. identifiedByMethod: GeneticElement - Method
4. referencedInPublication: GeneticElement - Publication

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. current_assembly: GeneticElement - xsd:string
3. current_chr: GeneticElement - xsd:string
4. current_end: GeneticElement - xsd:integer
5. current_start: GeneticElement - xsd:integer
6. disease: Disease - xsd:string
7. disease_method: Method - xsd:string
8. enh2gene_method: Method - xsd:string
9. enh_method: Method - xsd:string
10. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
11. hgnc_symbol_target_genes: TargetGene - xsd:string
12. minimum_ratio: GeneticElement - xsd:float
13. mutation_PMID: Publication - xsd:string
14. mutation_method: Method - xsd:string
15. orig_assembly: GeneticElement - xsd:string
16. orig_chr: GeneticElement - xsd:string
17. original_ID: GeneticElement - xsd:string
18. refseq_ID: GeneticElement - xsd:string
19. score: GeneticElement - xsd:float
20. source: GeneticElement - xsd:string
21. type: GeneticElement - xsd:string
22. disease_PMID: Publication - xsd:integer
23. enh2gene_PMID: Publication - xsd:integer
24. enh_PMID: Publication - xsd:integer
25. orig_end: GeneticElement - xsd:integer
26. orig_start: GeneticElement - xsd:integer