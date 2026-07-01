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
13. enh_PMID: type - PubMed ID for enhancer study - integer
14. enh_method: type - method used in enhancer study - string
15. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - string
16. hgnc_symbol_target_genes: type - HGNC symbol of the target genes - string
17. minimum_ratio: type - minimum ratio value - float
18. mutation_PMID: type - PubMed ID for mutation study - string
19. mutation_method: type - method used in mutation study - string
20. orig_assembly: type - original genome assembly version - string
21. orig_chr: type - chromosome number in the original assembly - string
22. original_ID: type - original ID of the genetic element - string
23. refsnp_ID: type - reference SNP ID - string
24. score: type - score associated with the genetic element - float
25. source: type - source of the data - string
26. type: type - type of the genetic regulatory element (enhancer, super-enhancer) - string
27. current_end: type - end position in the current assembly - integer
28. current_start: type - start position in the current assembly - integer
29. orig_end: type - end position in the original assembly - integer
30. orig_start: type - start position in the original assembly - integer

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. TranscriptionFactor
5. TargetGene
6. Disease
7. Mutation
8. CellLineOrBiosample

**Subclasses:**
1. Enhancer subclass of -> GeneticElement
2. SuperEnhancer subclass of -> Enhancer
3. TranscriptionFactor subclass of -> GeneticElement
4. TargetGene subclass of -> GeneticElement
5. Disease subclass of -> GeneticElement
6. Mutation subclass of -> GeneticElement
7. CellLineOrBiosample subclass of -> GeneticElement

**Object Properties:**
1. hasTranscriptionFactor: domain - TranscriptionFactor, range - Enhancer or SuperEnhancer
2. hasTargetGene: domain - TargetGene, range - Enhancer or SuperEnhancer
3. associatedWithDisease: domain - Disease, range - GeneticElement
4. associatedWithMutation: domain - Mutation, range - GeneticElement
5. occursInCellLineOrBiosample: domain - CellLineOrBiosample, range - GeneticElement

**Data Type Properties:**
1. hasPubMedID: domain - GeneticElement, range - xsd:string
2. hasMethod: domain - GeneticElement, range - xsd:string
3. hasChromosomeNumber: domain - GeneticElement, range - xsd:string
4. hasScore: domain - GeneticElement, range - xsd:float
5. hasAssemblyVersion: domain - GeneticElement, range - xsd:string
6. hasStartPosition: domain - GeneticElement, range - xsd:int
7. hasEndPosition: domain - GeneticElement, range - xsd:int