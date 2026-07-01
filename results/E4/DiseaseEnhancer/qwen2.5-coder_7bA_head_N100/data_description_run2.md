**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - integer
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - Cell Regulatory Module identifier - string
5. crossref: type - reference for the data - string
6. current_assembly: type - genomic assembly version - string
7. current_chr: type - chromosome number in the current assembly - integer
8. disease: type - disease associated with the genetic regulatory element - string
9. disease_method: type - method used to identify disease association - string
10. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - integer
11. enh2gene_method: type - method used in enhancer to gene interaction study - string
12. enh_method: type - method used to identify the enhancer - string
13. hgnc_symbol_TFs: type - HGNC symbol of transcription factors - string
14. hgnc_symbol_target_genes: type - HGNC symbol of target genes - string
15. minimum_ratio: type - minimum ratio of interaction - float
16. mutation_PMID: type - PubMed ID for mutation study - integer
17. mutation_method: type - method used in mutation study - string
18. orig_assembly: type - original genomic assembly version - string
19. orig_chr: type - chromosome number in the original assembly - integer
20. original_ID: type - original identifier for the genetic regulatory element - string
21. refseq_ID: type - RefSeq ID of the gene or enhancer - string
22. score: type - score associated with the interaction - float
23. source: type - source of the data - string
24. type: type - type of genetic regulatory element (enhancer, super-enhancer) - string
25. current_end: type - end position in the current assembly - integer
26. current_start: type - start position in the current assembly - integer
27. disease_PMID: type - PubMed ID for disease study - integer
28. enh_PMID: type - PubMed ID for enhancer study - integer
29. orig_end: type - end position in the original assembly - integer
30. orig_start: type - start position in the original assembly - integer

**Classes:**
1. GeneticRegulatoryElement
2. TranscriptionFactor
3. Enhancer
4. SuperEnhancer
5. TargetGene
6. Disease
7. CellLineOrBiosample
8. Mutation
9. PubMedArticle

**Subclasses:**
1. TranscriptionFactorToEnhancerInteraction (subclass of GeneticRegulatoryElement)
2. EnhancerToGeneInteraction (subclass of GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactorToEnhancerInteraction, range - TranscriptionFactor)
2. hasEnhancer (domain - TranscriptionFactorToEnhancerInteraction, range - Enhancer)
3. hasTargetGene (domain - EnhancerToGeneInteraction, range - TargetGene)
4. associatedWithDisease (domain - GeneticRegulatoryElement, range - Disease)
5. occursInCellLineOrBiosample (domain - GeneticRegulatoryElement, range - CellLineOrBiosample)
6. involvesMutation (domain - GeneticRegulatoryElement, range - Mutation)
7. hasPubMedArticle (domain - GeneticRegulatoryElement, range - PubMedArticle)

**Data Type Properties:**
1. pmid (domain - PubMedArticle, range - xsd:int)
2. method (domain - GeneticRegulatoryElement, range - xsd:string)
3. assemblyVersion (domain - GeneticRegulatoryElement, range - xsd:string)
4. chromosomeNumber (domain - GeneticRegulatoryElement, range - xsd:int)
5. score (domain - GeneticRegulatoryElement, range - xsd:float)
6. ratio (domain - TranscriptionFactorToEnhancerInteraction, EnhancerToGeneInteraction, range - xsd:float)
7. startPosition (domain - GeneticRegulatoryElement, range - xsd:int)
8. endPosition (domain - GeneticRegulatoryElement, range - xsd:int)