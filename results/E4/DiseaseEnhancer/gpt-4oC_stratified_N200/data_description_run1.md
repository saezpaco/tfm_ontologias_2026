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
4. crm_ID: text - Identifier for cis-regulatory modules - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: text - Current chromosome identifier - text
8. disease: text - Disease associated with the genetic element - text
9. disease_method: categorical - Method used for identifying disease associations - categorical
10. enh2gene_PMID: text - PubMed ID for enhancer to gene associations - text
11. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - categorical
12. enh_method: categorical - Method used for identifying enhancers - categorical
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
15. minimum_ratio: categorical - Minimum ratio value - categorical
16. mutation_PMID: text - PubMed ID for mutation information - text
17. mutation_method: categorical - Method used for identifying mutations - categorical
18. orig_assembly: categorical - Original genome assembly version - categorical
19. orig_chr: text - Original chromosome identifier - text
20. original_ID: text - Original identifier for the genetic element - text
21. refseq_ID: text - RefSeq identifier - text
22. score: categorical - Score value - categorical
23. source: categorical - Source of the data - categorical
24. type: categorical - Type of genetic element - categorical
25. current_end: Numerical - Current end position in the genome - Numerical
26. current_start: Numerical - Current start position in the genome - Numerical
27. disease_PMID: Numerical - PubMed ID for disease information - Numerical
28. enh_PMID: Numerical - PubMed ID for enhancer information - Numerical
29. orig_end: Numerical - Original end position in the genome - Numerical
30. orig_start: Numerical - Original start position in the genome - Numerical

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
5. Mutation: subclass of -> GeneticElement

**Object Properties:**
1. hasBiosample: GeneticElement - Biosample
2. associatedWithDisease: GeneticElement - Disease
3. identifiedByMethod: GeneticElement - Method
4. referencedInPublication: GeneticElement - Publication
5. regulates: TranscriptionFactor - TargetGene
6. locatedOnChromosome: GeneticElement - xsd:string

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. crossref: GeneticElement - xsd:string
3. current_assembly: GeneticElement - xsd:string
4. current_chr: GeneticElement - xsd:string
5. disease: Disease - xsd:string
6. enh2gene_PMID: Publication - xsd:string
7. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
8. hgnc_symbol_target_genes: TargetGene - xsd:string
9. minimum_ratio: GeneticElement - xsd:float
10. mutation_PMID: Publication - xsd:string
11. orig_assembly: GeneticElement - xsd:string
12. orig_chr: GeneticElement - xsd:string
13. original_ID: GeneticElement - xsd:string
14. refseq_ID: GeneticElement - xsd:string
15. score: GeneticElement - xsd:float
16. source: GeneticElement - xsd:string
17. type: GeneticElement - xsd:string
18. current_end: GeneticElement - xsd:integer
19. current_start: GeneticElement - xsd:integer
20. disease_PMID: Publication - xsd:integer
21. enh_PMID: Publication - xsd:integer
22. orig_end: GeneticElement - xsd:integer
23. orig_start: GeneticElement - xsd:integer