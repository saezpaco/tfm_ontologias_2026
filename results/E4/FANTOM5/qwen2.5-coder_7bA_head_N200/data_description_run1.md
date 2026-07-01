**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - string
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample: type - cell line or tissue sample - string
4. crm_ID: type - cluster region module identifier - string
5. crossref: type - reference ID for cross-referencing - string
6. current_assembly: type - current genome assembly version - string
7. current_chr: type - chromosome number in the current assembly - integer
8. disease: type - disease associated with genetic regulatory element - string
9. disease_PMID: type - PubMed ID for disease study - string
10. disease_method: type - method used in disease study - string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - string
12. enh2gene_method: type - method used in enhancer to gene interaction study - string
13. enh_PMID: type - PubMed ID for enhancer study - integer
14. enh_method: type - method used in enhancer study - string
15. hgnc_symbol_TFs: type - HGNC symbol of transcription factors - string
16. hgnc_symbol_target_genes: type - HGNC symbol of target genes - string
17. minimum_ratio: type - minimum ratio value - float
18. mutation_PMID: type - PubMed ID for mutation study - string
19. mutation_method: type - method used in mutation study - string
20. orig_assembly: type - original genome assembly version - string
21. orig_chr: type - chromosome number in the original assembly - integer
22. original_ID: type - original identifier - string
23. refsnp_ID: type - reference SNP ID - string
24. score: type - score value - float
25. source: type - data source - string
26. type: type - type of genetic regulatory element - string
27. current_end: type - end position in the current assembly - integer
28. current_start: type - start position in the current assembly - integer
29. orig_end: type - end position in the original assembly - integer
30. orig_start: type - start position in the original assembly - integer

**Classes:**
1. GeneticRegulatoryElement
2. TranscriptionFactor
3. Enhancer
4. SuperEnhancer
5. TargetGene
6. Disease
7. CellLine
8. Mutation
9. PubMedArticle
10. AssemblyVersion
11. Chromosome
12. ClusterRegionModule

**Subclasses:**
1. TranscriptionFactorToEnhancerInteraction (subclass of -> GeneticRegulatoryElement)
2. EnhancerToGeneInteraction (subclass of -> GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactorToEnhancerInteraction, range - TranscriptionFactor)
2. hasEnhancer (domain - TranscriptionFactorToEnhancerInteraction, range - Enhancer)
3. hasTargetGene (domain - EnhancerToGeneInteraction, range - TargetGene)
4. associatedWithDisease (domain - GeneticRegulatoryElement, range - Disease)
5. occursInCellLine (domain - GeneticRegulatoryElement, range - CellLine)
6. involvesMutation (domain - GeneticRegulatoryElement, range - Mutation)
7. publishedInArticle (domain - GeneticRegulatoryElement, range - PubMedArticle)
8. hasAssemblyVersion (domain - GeneticRegulatoryElement, range - AssemblyVersion)
9. locatedOnChromosome (domain - GeneticRegulatoryElement, range - Chromosome)

**Data Type Properties:**
1. pmidValue (domain - PubMedArticle, range - xsd:string)
2. methodType (domain - GeneticRegulatoryElement, range - xsd:string)
3. hgncSymbol (domain - TranscriptionFactor, TargetGene, Disease, CellLine, Mutation, Chromosome, ClusterRegionModule, AssemblyVersion, PubMedArticle, GeneticRegulatoryElement, EnhancerToGeneInteraction, TranscriptionFactorToEnhancerInteraction), range - xsd:string)
4. scoreValue (domain - GeneticRegulatoryElement, range - xsd:float)
5. ratioValue (domain - GeneticRegulatoryElement, range - xsd:float)
6. chromosomeNumber (domain - Chromosome, range - xsd:int)
7. startPosition (domain - GeneticRegulatoryElement, range - xsd:int)
8. endPosition (domain - GeneticRegulatoryElement, range - xsd:int)