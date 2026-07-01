**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - string
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - ID of the chromatin regulatory module - string
5. crossref: type - reference type (e.g., PMID, DOI) - string
6. current_assembly: type - current genome assembly version - string
7. current_chr: type - chromosome number in the current assembly - string
8. disease: type - disease associated with the genetic regulatory element - string
9. disease_PMID: type - PubMed ID for disease study - string
10. disease_method: type - method used in disease study - string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction study - string
12. enh2gene_method: type - method used in enhancer to gene interaction study - string
13. enh_PMID: type - PubMed ID for enhancer study - string
14. enh_method: type - method used in enhancer study - string
15. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - string
16. hgnc_symbol_target_genes: type - HGNC symbols of target genes - string
17. minimum_ratio: type - minimum ratio value - float
18. mutation_PMID: type - PubMed ID for mutation study - string
19. mutation_method: type - method used in mutation study - string
20. orig_assembly: type - original genome assembly version - string
21. orig_chr: type - chromosome number in the original assembly - string
22. original_ID: type - original ID of the genetic regulatory element - string
23. refsnp_ID: type - reference SNP ID - string
24. score: type - score value - float
25. source: type - source of the data - string
26. type: type - type of the genetic regulatory element (e.g., enhancer, super-enhancer) - string
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
6. CellLineOrBiosample
7. Disease
8. Mutation
9. ChromatinRegulatoryModule

**Subclasses:**
1. TranscriptionFactorToEnhancerInteraction (subclass of GeneticRegulatoryElement)
2. EnhancerToGeneInteraction (subclass of GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactorToEnhancerInteraction, range - TranscriptionFactor)
2. hasEnhancer (domain - TranscriptionFactorToEnhancerInteraction, range - Enhancer)
3. hasTargetGene (domain - EnhancerToGeneInteraction, range - TargetGene)
4. associatedWithCellLineOrBiosample (domain - GeneticRegulatoryElement, range - CellLineOrBiosample)
5. associatedWithDisease (domain - GeneticRegulatoryElement, range - Disease)
6. associatedWithMutation (domain - GeneticRegulatoryElement, range - Mutation)
7. hasChromatinRegulatoryModule (domain - GeneticRegulatoryElement, range - ChromatinRegulatoryModule)

**Data Type Properties:**
1. pmid (domain - PubMed ID, range - xsd:string)
2. method (domain - Method, range - xsd:string)
3. chromosomeNumber (domain - Chromosome Number, range - xsd:string)
4. scoreValue (domain - Score Value, range - xsd:float)
5. startPosition (domain - Start Position, range - xsd:int)
6. endPosition (domain - End Position, range - xsd:int)