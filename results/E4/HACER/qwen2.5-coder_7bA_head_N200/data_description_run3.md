**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer relationship - string
2. TFs2enh_method: type - method used in transcription factor to enhancer relationship - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - ID of the chromatin regulatory module - string
5. crossref: type - reference for the data - string
6. current_assembly: type - assembly version of the genome - string
7. current_chr: type - chromosome number - integer
8. current_end: type - end position of the genomic region - integer
9. current_start: type - start position of the genomic region - integer
10. disease: type - name of the disease - string
11. disease_PMID: type - PubMed ID for disease information - string
12. disease_method: type - method used in disease information - string
13. enh2gene_PMID: type - PubMed ID for enhancer to gene relationship - string
14. enh2gene_method: type - method used in enhancer to gene relationship - string
15. enh_PMID: type - PubMed ID for enhancer information - string
16. enh_method: type - method used in enhancer information - string
17. hgnc_symbol_TFs: type - HGNC symbol of the transcription factor - string
18. hgnc_symbol_target_genes: type - HGNC symbols of target genes - string
19. minimum_ratio: type - minimum ratio value - float
20. mutation_PMID: type - PubMed ID for mutation information - string
21. mutation_method: type - method used in mutation information - string
22. orig_assembly: type - original assembly version of the genome - string
23. orig_chr: type - original chromosome number - integer
24. orig_end: type - original end position of the genomic region - integer
25. orig_start: type - original start position of the genomic region - integer
26. original_ID: type - original ID of the data - string
27. refsnp_ID: type - RSID for genetic variation - string
28. score: type - score value - float
29. source: type - source of the data - string
30. type: type - type of the data - string

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
1. TranscriptionFactorToEnhancerRelationship (subclass of -> GeneticElement)
2. EnhancerToGeneRelationship (subclass of -> GeneticElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactor, range - TranscriptionFactorToEnhancerRelationship)
2. hasEnhancer (domain - Enhancer, range - TranscriptionFactorToEnhancerRelationship)
3. hasTargetGene (domain - TargetGene, range - EnhancerToGeneRelationship)
4. associatedWithDisease (domain - Disease, range - GeneticElement)
5. occursInCellLineOrBiosample (domain - CellLineOrBiosample, range - GeneticElement)
6. involvesMutation (domain - Mutation, range - GeneticElement)

**Data Type Properties:**
1. hasPubMedID (domain - GeneticElement, range - xsd:string)
2. hasMethod (domain - GeneticElement, range - xsd:string)
3. hasChromosomeNumber (domain - GeneticElement, range - xsd:int)
4. hasGenomicRegionStart (domain - GeneticElement, range - xsd:int)
5. hasGenomicRegionEnd (domain - GeneticElement, range - xsd:int)
6. hasScore (domain - GeneticElement, range - xsd:float)