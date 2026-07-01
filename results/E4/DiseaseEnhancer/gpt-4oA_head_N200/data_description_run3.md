**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer mapping - categorical
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer mapping - categorical
3. biosample_name: categorical - Name of the biosample - categorical
4. crm_ID: text - ID for cis-regulatory module - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: categorical - Current chromosome - categorical
8. disease: text - Disease associated with the data - text
9. disease_method: categorical - Method used for disease association - categorical
10. enh2gene_PMID: text - PubMed ID for enhancer to gene mapping - text
11. enh2gene_method: categorical - Method used for enhancer to gene mapping - categorical
12. enh_method: categorical - Method used for enhancer identification - categorical
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
15. minimum_ratio: categorical - Minimum ratio value - categorical
16. mutation_PMID: text - PubMed ID for mutation information - text
17. mutation_method: categorical - Method used for mutation identification - categorical
18. orig_assembly: categorical - Original genome assembly version - categorical
19. orig_chr: categorical - Original chromosome - categorical
20. original_ID: text - Original ID for the data - text
21. refseq_ID: text - RefSeq ID for the data - text
22. score: categorical - Score value - categorical
23. source: categorical - Source of the data - categorical
24. type: categorical - Type of the data - categorical
25. current_end: Numerical - Current end position in the genome - Numerical
26. current_start: Numerical - Current start position in the genome - Numerical
27. disease_PMID: Numerical - PubMed ID for disease information - Numerical
28. enh_PMID: Numerical - PubMed ID for enhancer information - Numerical
29. orig_end: Numerical - Original end position in the genome - Numerical
30. orig_start: Numerical - Original start position in the genome - Numerical

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. TranscriptionFactor
8. TargetGene
9. Mutation

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. regulatesTranscriptionFactor: GeneticElement - TranscriptionFactor
7. targetsGene: GeneticElement - TargetGene
8. hasMutation: GeneticElement - Mutation

**Data Type Properties:**
1. TFs2enh_PMID: Publication - xsd:string
2. TFs2enh_method: Method - xsd:string
3. biosample_name: Biosample - xsd:string
4. crm_ID: CisRegulatoryModule - xsd:string
5. crossref: GeneticElement - xsd:string
6. current_assembly: GenomicCoordinate - xsd:string
7. current_chr: GenomicCoordinate - xsd:string
8. disease: Disease - xsd:string
9. disease_method: Method - xsd:string
10. enh2gene_PMID: Publication - xsd:string
11. enh2gene_method: Method - xsd:string
12. enh_method: Method - xsd:string
13. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
14. hgnc_symbol_target_genes: TargetGene - xsd:string
15. minimum_ratio: GeneticElement - xsd:float
16. mutation_PMID: Publication - xsd:string
17. mutation_method: Method - xsd:string
18. orig_assembly: GenomicCoordinate - xsd:string
19. orig_chr: GenomicCoordinate - xsd:string
20. original_ID: GeneticElement - xsd:string
21. refseq_ID: GeneticElement - xsd:string
22. score: GeneticElement - xsd:float
23. source: GeneticElement - xsd:string
24. type: GeneticElement - xsd:string
25. current_end: GenomicCoordinate - xsd:long
26. current_start: GenomicCoordinate - xsd:long
27. disease_PMID: Publication - xsd:long
28. enh_PMID: Publication - xsd:long
29. orig_end: GenomicCoordinate - xsd:long
30. orig_start: GenomicCoordinate - xsd:long