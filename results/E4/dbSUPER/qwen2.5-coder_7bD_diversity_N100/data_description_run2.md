**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - string
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - ID of the chromatin regulatory module - string
5. crossref: type - reference for the data - string
6. current_assembly: type - current genome assembly version - string
7. current_chr: type - chromosome number in the current assembly - string
8. disease: type - disease associated with the genetic element - string
9. disease_PMID: type - PubMed ID for disease study - string
10. disease_method: type - method used in disease study - string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - string
12. enh2gene_method: type - method used in enhancer to gene interaction study - string
13. enh_PMID: type - PubMed ID for enhancer study - string
14. enh_method: type - method used in enhancer study - string
15. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - string
16. hgnc_symbol_target_genes: type - HGNC symbol of the target genes - string
17. minimum_ratio: type - minimum ratio associated with the genetic element - float
18. mutation_PMID: type - PubMed ID for mutation study - string
19. mutation_method: type - method used in mutation study - string
20. orig_assembly: type - original genome assembly version - string
21. orig_chr: type - chromosome number in the original assembly - string
22. original_ID: type - original ID of the genetic element - string
23. refsnp_ID: type - reference SNP ID associated with the genetic element - string
24. source: type - source of the data - string
25. type: type - type of the genetic regulatory element (enhancer, super-enhancer) - string
26. current_end: type - end position of the genetic element in the current assembly - integer
27. current_start: type - start position of the genetic element in the current assembly - integer
28. orig_end: type - end position of the genetic element in the original assembly - integer
29. orig_start: type - start position of the genetic element in the original assembly - integer
30. score: type - score associated with the genetic element - float

**Classes:**
1. GeneticElement
2. TranscriptionFactor
3. Enhancer
4. SuperEnhancer
5. TargetGene
6. Disease
7. CellLineOrBiosample
8. Mutation
9. ChromatinRegulatoryModule

**Subclasses:**
1. TranscriptionFactorToEnhancerInteraction (subclass of -> GeneticElement)
2. EnhancerToGeneInteraction (subclass of -> GeneticElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactorToEnhancerInteraction, range - TranscriptionFactor)
2. hasEnhancer (domain - TranscriptionFactorToEnhancerInteraction, range - Enhancer)
3. hasTargetGene (domain - EnhancerToGeneInteraction, range - TargetGene)
4. associatedWithDisease (domain - GeneticElement, range - Disease)
5. occursInCellLineOrBiosample (domain - GeneticElement, range - CellLineOrBiosample)
6. involvesMutation (domain - GeneticElement, range - Mutation)
7. partOfChromatinRegulatoryModule (domain - GeneticElement, range - ChromatinRegulatoryModule)

**Data Type Properties:**
1. hasPubMedID (domain - GeneticElement, range - xsd:string)
2. hasMethod (domain - GeneticElement, range - xsd:string)
3. hasHGNCsymbol (domain - TranscriptionFactor, domain - TargetGene, range - xsd:string)
4. hasChromosomeNumber (domain - GeneticElement, range - xsd:string)
5. hasScore (domain - GeneticElement, range - xsd:float)
6. hasStartPosition (domain - GeneticElement, range - xsd:int)
7. hasEndPosition (domain - GeneticElement, range - xsd:int)