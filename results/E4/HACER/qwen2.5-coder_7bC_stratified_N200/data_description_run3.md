**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - string
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - Cell Regulatory Module identifier - string
5. crossref: type - Cross-reference ID for additional information - string
6. current_assembly: type - Current genome assembly version - string
7. current_chr: type - Chromosome number in the current assembly - string
8. disease: type - Disease associated with the genetic regulatory element - string
9. disease_PMID: type - PubMed ID for disease study - string
10. disease_method: type - Method used in disease study - string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - string
12. enh2gene_method: type - Method used in enhancer to gene interaction study - string
13. enh_PMID: type - PubMed ID for enhancer study - integer
14. enh_method: type - Method used in enhancer study - string
15. hgnc_symbol_TFs: type - HGNC symbol of the transcription factor - string
16. hgnc_symbol_target_genes: type - HGNC symbol of the target gene - string
17. minimum_ratio: type - Minimum ratio value - float
18. mutation_PMID: type - PubMed ID for mutation study - string
19. mutation_method: type - Method used in mutation study - string
20. orig_assembly: type - Original genome assembly version - string
21. orig_chr: type - Chromosome number in the original assembly - string
22. original_ID: type - Original identifier for the genetic regulatory element - string
23. refsnp_ID: type - Reference SNP ID - string
24. score: type - Score value - float
25. source: type - Source of the data - string
26. type: type - Type of the genetic regulatory element (e.g., enhancer, super-enhancer) - string
27. current_end: type - End position in the current assembly - integer
28. current_start: type - Start position in the current assembly - integer
29. orig_end: type - End position in the original assembly - integer
30. orig_start: type - Start position in the original assembly - integer

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
1. pmid (domain - PubMedArticle, range - xsd:string)
2. method (domain - GeneticRegulatoryElement, range - xsd:string)
3. assemblyVersion (domain - GeneticRegulatoryElement, range - xsd:string)
4. chromosomeNumber (domain - GeneticRegulatoryElement, range - xsd:string)
5. hgncSymbol (domain - TranscriptionFactor, TargetGene, Enhancer, SuperEnhancer, Disease, CellLineOrBiosample, Mutation, PubMedArticle, range - xsd:string)
6. scoreValue (domain - GeneticRegulatoryElement, range - xsd:float)
7. startPosition (domain - GeneticRegulatoryElement, range - xsd:int)
8. endPosition (domain - GeneticRegulatoryElement, range - xsd:int)