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
10. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - categorical
11. enh_method: categorical - Method used for identifying enhancers - categorical
12. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
13. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
14. minimum_ratio: categorical - Minimum ratio value - categorical
15. mutation_PMID: text - PubMed ID for mutation information - text
16. mutation_method: categorical - Method used for identifying mutations - categorical
17. orig_assembly: categorical - Original genome assembly version - categorical
18. orig_chr: text - Original chromosome identifier - text
19. original_ID: text - Original identifier for the genetic element - text
20. refseq_ID: text - RefSeq identifier for the genetic element - text
21. score: categorical - Score value - categorical
22. source: categorical - Source of the data - categorical
23. type: categorical - Type of genetic element - categorical
24. current_end: Numerical - Current end position in the genome - Numerical
25. current_start: Numerical - Current start position in the genome - Numerical
26. disease_PMID: Numerical - PubMed ID for disease information - Numerical
27. enh2gene_PMID: Numerical - PubMed ID for enhancer to gene associations - Numerical
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

**Data Type Properties:**
1. crmID: GeneticElement - xsd:string
2. currentAssembly: GeneticElement - xsd:string
3. currentChr: GeneticElement - xsd:string
4. diseaseName: Disease - xsd:string
5. hgncSymbol: GeneticElement - xsd:string
6. minimumRatio: GeneticElement - xsd:float
7. originalID: GeneticElement - xsd:string
8. refseqID: GeneticElement - xsd:string
9. score: GeneticElement - xsd:float
10. source: GeneticElement - xsd:string
11. type: GeneticElement - xsd:string
12. currentEnd: GeneticElement - xsd:integer
13. currentStart: GeneticElement - xsd:integer
14. diseasePMID: Disease - xsd:integer
15. enh2genePMID: Publication - xsd:integer
16. enhPMID: Publication - xsd:integer
17. origEnd: GeneticElement - xsd:integer
18. origStart: GeneticElement - xsd:integer