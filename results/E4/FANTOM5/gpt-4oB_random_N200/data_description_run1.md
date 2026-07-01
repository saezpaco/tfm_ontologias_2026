**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - categorical
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer associations - categorical
3. biosample: categorical - Biosample or cell line used in the study - categorical
4. crm_ID: text - Unique identifier for cis-regulatory module - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: text - Current chromosome - text
8. disease: categorical - Disease associated with the genetic element - categorical
9. disease_PMID: categorical - PubMed ID for disease association - categorical
10. disease_method: categorical - Method used for disease association - categorical
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - categorical
12. enh2gene_method: categorical - Method used for enhancer to gene associations - categorical
13. enh_PMID: categorical - PubMed ID for enhancer information - categorical
14. enh_method: categorical - Method used for enhancer information - categorical
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
17. minimum_ratio: categorical - Minimum ratio value - categorical
18. mutation_PMID: categorical - PubMed ID for mutation information - categorical
19. mutation_method: categorical - Method used for mutation information - categorical
20. orig_assembly: categorical - Original genome assembly version - categorical
21. orig_chr: text - Original chromosome - text
22. original_ID: categorical - Original identifier - categorical
23. refsnp_ID: categorical - Reference SNP ID - categorical
24. score: categorical - Score value - categorical
25. source: categorical - Source of the data - categorical
26. type: categorical - Type of genetic element - categorical
27. current_end: Numerical - Current end position in the genome - Numerical
28. current_start: Numerical - Current start position in the genome - Numerical
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

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. regulatesTranscriptionFactor: GeneticElement - TranscriptionFactor
7. targetsGene: GeneticElement - TargetGene

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. crossref: GeneticElement - xsd:string
3. current_assembly: GenomicCoordinate - xsd:string
4. current_chr: GenomicCoordinate - xsd:string
5. current_end: GenomicCoordinate - xsd:decimal
6. current_start: GenomicCoordinate - xsd:decimal
7. disease: Disease - xsd:string
8. disease_PMID: Disease - xsd:string
9. disease_method: Method - xsd:string
10. enh2gene_PMID: Publication - xsd:string
11. enh2gene_method: Method - xsd:string
12. enh_PMID: Publication - xsd:string
13. enh_method: Method - xsd:string
14. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
15. hgnc_symbol_target_genes: TargetGene - xsd:string
16. minimum_ratio: GeneticElement - xsd:decimal
17. mutation_PMID: Publication - xsd:string
18. mutation_method: Method - xsd:string
19. orig_assembly: GenomicCoordinate - xsd:string
20. orig_chr: GenomicCoordinate - xsd:string
21. orig_end: GenomicCoordinate - xsd:decimal
22. orig_start: GenomicCoordinate - xsd:decimal
23. original_ID: GeneticElement - xsd:string
24. refsnp_ID: GeneticElement - xsd:string
25. score: GeneticElement - xsd:decimal
26. source: GeneticElement - xsd:string
27. type: GeneticElement - xsd:string