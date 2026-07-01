**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - integer
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - cluster region module identifier - string
5. crossref: type - reference for the data - string
6. current_assembly: type - current genome assembly version - string
7. current_chr: type - chromosome number in current assembly - integer
8. disease: type - disease associated with the genetic regulatory element - string
9. disease_method: type - method used to identify disease association - string
10. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - integer
11. enh2gene_method: type - method used in enhancer to gene interaction study - string
12. enh_method: type - method used to identify the enhancer - string
13. hgnc_symbol_TFs: type - HGNC symbol of transcription factors - string
14. hgnc_symbol_target_genes: type - HGNC symbols of target genes - string
15. minimum_ratio: type - minimum ratio of interaction - float
16. mutation_PMID: type - PubMed ID for mutation study - integer
17. mutation_method: type - method used in mutation study - string
18. orig_assembly: type - original genome assembly version - string
19. orig_chr: type - chromosome number in original assembly - integer
20. original_ID: type - original identifier of the genetic regulatory element - string
21. refseq_ID: type - RefSeq ID of the genetic regulatory element - string
22. score: type - score of the interaction - float
23. source: type - source of the data - string
24. type: type - type of the genetic regulatory element (enhancer, super-enhancer) - string
25. current_end: type - end position in current assembly - integer
26. current_start: type - start position in current assembly - integer
27. disease_PMID: type - PubMed ID for disease study - integer
28. enh_PMID: type - PubMed ID for enhancer study - integer
29. orig_end: type - end position in original assembly - integer
30. orig_start: type - start position in original assembly - integer

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
1. TFs2enhInteraction (subclass of -> GeneticRegulatoryElement)
2. enh2geneInteraction (subclass of -> GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactor, range - TFs2enhInteraction)
2. hasEnhancer (domain - Enhancer, range - TFs2enhInteraction)
3. hasTargetGene (domain - TargetGene, range - enh2geneInteraction)
4. associatedWithDisease (domain - Disease, range - GeneticRegulatoryElement)
5. occursInCellLineOrBiosample (domain - CellLineOrBiosample, range - GeneticRegulatoryElement)
6. involvesMutation (domain - Mutation, range - GeneticRegulatoryElement)

**Data Type Properties:**
1. hasPubMedID (domain - PubMedArticle, range - integer)
2. hasMethod (domain - GeneticRegulatoryElement, range - string)
3. hasChromosomeNumber (domain - GeneticRegulatoryElement, range - integer)
4. hasScore (domain - GeneticRegulatoryElement, range - float)
5. hasAssemblyVersion (domain - GeneticRegulatoryElement, range - string)
6. hasStartPosition (domain - GeneticRegulatoryElement, range - integer)
7. hasEndPosition (domain - GeneticRegulatoryElement, range - integer)