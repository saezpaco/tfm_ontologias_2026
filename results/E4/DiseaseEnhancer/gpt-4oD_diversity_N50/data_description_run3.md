**Foundational Prefix:**
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:skos="http://www.w3.org/2004/02/skos/core#"
         xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:base="https://base_ontology.com#">

<owl:Ontology rdf:about="https://base_ontology.com#"/>

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - categorical
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer associations - categorical
3. biosample_name: categorical - Name of the biosample or cell line - categorical
4. crm_ID: text - Unique identifier for cis-regulatory modules - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: text - Current chromosome - text
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
19. orig_chr: text - Original chromosome - text
20. original_ID: text - Original identifier - text
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

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. current_assembly: GeneticElement - xsd:string
3. current_chr: GeneticElement - xsd:string
4. current_end: GeneticElement - xsd:decimal
5. current_start: GeneticElement - xsd:decimal
6. disease: Disease - xsd:string
7. disease_method: Method - xsd:string
8. enh2gene_PMID: Publication - xsd:string
9. enh2gene_method: Method - xsd:string
10. enh_method: Method - xsd:string
11. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
12. hgnc_symbol_target_genes: TargetGene - xsd:string
13. minimum_ratio: GeneticElement - xsd:decimal
14. mutation_PMID: Publication - xsd:string
15. mutation_method: Method - xsd:string
16. orig_assembly: GeneticElement - xsd:string
17. orig_chr: GeneticElement - xsd:string
18. original_ID: GeneticElement - xsd:string
19. refseq_ID: GeneticElement - xsd:string
20. score: GeneticElement - xsd:decimal
21. source: GeneticElement - xsd:string
22. type: GeneticElement - xsd:string
23. disease_PMID: Publication - xsd:decimal
24. enh_PMID: Publication - xsd:decimal
25. orig_end: GeneticElement - xsd:decimal
26. orig_start: GeneticElement - xsd:decimal