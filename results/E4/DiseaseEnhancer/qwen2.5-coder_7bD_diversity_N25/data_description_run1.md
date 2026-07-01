**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - integer
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - unique identifier for chromatin regulatory module - string
5. crossref: type - reference ID - integer
6. current_assembly: type - genomic assembly version - string
7. current_chr: type - chromosome number - string
8. disease: type - disease associated with the genetic element - string
9. disease_method: type - method used in disease study - string
10. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - integer
11. enh2gene_method: type - method used in enhancer to gene interaction study - string
12. enh_method: type - method used in enhancer study - string
13. hgnc_symbol_TFs: type - HGNC symbol of transcription factors - string
14. hgnc_symbol_target_genes: type - HGNC symbol of target genes - string
15. minimum_ratio: type - minimum ratio value - float
16. mutation_PMID: type - PubMed ID for mutation study - integer
17. mutation_method: type - method used in mutation study - string
18. orig_assembly: type - original genomic assembly version - string
19. orig_chr: type - original chromosome number - string
20. original_ID: type - unique identifier for the genetic element - string
21. refseq_ID: type - RefSeq ID of the genetic element - string
22. score: type - score value - float
23. source: type - source of the data - string
24. type: type - type of the genetic regulatory element - string
25. current_end: type - end position of the genetic element in the current assembly - integer
26. current_start: type - start position of the genetic element in the current assembly - integer
27. disease_PMID: type - PubMed ID for disease study - integer
28. enh_PMID: type - PubMed ID for enhancer study - integer
29. orig_end: type - end position of the genetic element in the original assembly - integer
30. orig_start: type - start position of the genetic element in the original assembly - integer

**Classes:**
1. GeneticElement
2. TranscriptionFactor
3. Enhancer
4. SuperEnhancer
5. TargetGene
6. Disease
7. CellLineOrBiosample

**Subclasses:**
1. TranscriptionFactorToEnhancerInteraction (subclass of -> GeneticElement)
2. EnhancerToGeneInteraction (subclass of -> GeneticElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactorToEnhancerInteraction, range - TranscriptionFactor)
2. hasEnhancer (domain - TranscriptionFactorToEnhancerInteraction, range - Enhancer)
3. hasTargetGene (domain - EnhancerToGeneInteraction, range - TargetGene)
4. associatedWithDisease (domain - GeneticElement, range - Disease)
5. occursInCellLineOrBiosample (domain - GeneticElement, range - CellLineOrBiosample)

**Data Type Properties:**
1. pmid (domain - PubMed ID, range - xsd:int)
2. method (domain - Method, range - xsd:string)
3. chromosomeNumber (domain - Chromosome Number, range - xsd:string)
4. assemblyVersion (domain - Assembly Version, range - xsd:string)
5. ratioValue (domain - Ratio Value, range - xsd:float)
6. scoreValue (domain - Score Value, range - xsd:float)