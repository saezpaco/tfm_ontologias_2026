**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - string
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - unique identifier for a cellular region of interest (CRM) - string
5. crossref: type - reference ID for external resources - string
6. current_assembly: type - genomic assembly version - string
7. current_chr: type - chromosome number in the current assembly - string
8. disease: type - name of the disease associated with the genetic element - string
9. disease_PMID: type - PubMed ID for disease study - string
10. disease_method: type - method used in disease study - string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction study - string
12. enh2gene_method: type - method used in enhancer to gene interaction study - string
13. enh_PMID: type - PubMed ID for enhancer study - string
14. enh_method: type - method used in enhancer study - string
15. hgnc_symbol_TFs: type - HGNC symbol of the transcription factor - string
16. hgnc_symbol_target_genes: type - HGNC symbol of the target gene - string
17. minimum_ratio: type - minimum ratio value - float
18. mutation_PMID: type - PubMed ID for mutation study - string
19. mutation_method: type - method used in mutation study - string
20. orig_assembly: type - original genomic assembly version - string
21. orig_chr: type - chromosome number in the original assembly - string
22. original_ID: type - unique identifier for the genetic element - string
23. refsnp_ID: type - reference SNP ID - string
24. source: type - source of the data - string
25. type: type - type of the genetic regulatory element (enhancer, super-enhancer) - string
26. current_end: type - end position in the current assembly - integer
27. current_start: type - start position in the current assembly - integer
28. orig_end: type - end position in the original assembly - integer
29. orig_start: type - start position in the original assembly - integer
30. score: type - score of the genetic regulatory element - float

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. TranscriptionFactor
5. TargetGene
6. Disease
7. CellLineOrBiosample

**Subclasses:**
1. Enhancer subclass of -> GeneticElement
2. SuperEnhancer subclass of -> Enhancer
3. TranscriptionFactor subclass of -> GeneticElement
4. TargetGene subclass of -> GeneticElement
5. Disease subclass of -> GeneticElement
6. CellLineOrBiosample subclass of -> GeneticElement

**Object Properties:**
1. hasTranscriptionFactor: domain - TranscriptionFactor, range - Enhancer or SuperEnhancer
2. hasTargetGene: domain - TargetGene, range - Enhancer or SuperEnhancer
3. associatedWithDisease: domain - Disease, range - Enhancer or SuperEnhancer
4. occursInCellLineOrBiosample: domain - CellLineOrBiosample, range - Enhancer or SuperEnhancer

**Data Type Properties:**
1. hasPubMedID: domain - GeneticElement, range - xsd:string
2. hasMethod: domain - GeneticElement, range - xsd:string
3. hasHGNCsymbol: domain - TranscriptionFactor or TargetGene, range - xsd:string
4. hasChromosomeNumber: domain - Enhancer or SuperEnhancer, range - xsd:string
5. hasScore: domain - Enhancer or SuperEnhancer, range - xsd:float
6. hasStartPosition: domain - Enhancer or SuperEnhancer, range - xsd:int
7. hasEndPosition: domain - Enhancer or SuperEnhancer, range - xsd:int