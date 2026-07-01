**Foundational Prefix:**
https://geneticregulatoryelements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - string
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - ID of the chromatin region module - string
5. crossref: type - reference for the data - string
6. current_assembly: type - current genome assembly version - string
7. current_chr: type - chromosome number in the current assembly - integer
8. current_end: type - end position of the genomic feature in the current assembly - integer
9. current_start: type - start position of the genomic feature in the current assembly - integer
10. disease: type - name of the disease associated with the data - string
11. disease_PMID: type - PubMed ID for disease study - string
12. disease_method: type - method used in disease study - string
13. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - string
14. enh2gene_method: type - method used in enhancer to gene interaction study - string
15. enh_PMID: type - PubMed ID for enhancer study - string
16. enh_method: type - method used in enhancer study - string
17. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - string
18. hgnc_symbol_target_genes: type - HGNC symbol of the target genes - string
19. minimum_ratio: type - minimum ratio value - float
20. mutation_PMID: type - PubMed ID for mutation study - string
21. mutation_method: type - method used in mutation study - string
22. orig_assembly: type - original genome assembly version - string
23. orig_chr: type - chromosome number in the original assembly - integer
24. orig_end: type - end position of the genomic feature in the original assembly - integer
25. orig_start: type - start position of the genomic feature in the original assembly - integer
26. original_ID: type - ID of the original data - string
27. refsnp_ID: type - RSID for the genetic variation - string
28. score: type - score value - float
29. source: type - source of the data - string
30. type: type - type of the data - string

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. TranscriptionFactor
5. TargetGene
6. Disease
7. CellLineOrBiosample
8. Mutation
9. ChromatinRegionModule

**Subclasses:**
1. TFs2enh_Interaction (subclass of -> GeneticElement)
2. enh2gene_Interaction (subclass of -> GeneticElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - Enhancer, SuperEnhancer; range - TranscriptionFactor)
2. hasTargetGene (domain - Enhancer, SuperEnhancer; range - TargetGene)
3. associatedWithDisease (domain - GeneticElement; range - Disease)
4. occursInCellLineOrBiosample (domain - GeneticElement; range - CellLineOrBiosample)
5. involvesMutation (domain - GeneticElement; range - Mutation)
6. partOfChromatinRegionModule (domain - Enhancer, SuperEnhancer; range - ChromatinRegionModule)

**Data Type Properties:**
1. hasPubMedID (domain - GeneticElement; range - xsd:string)
2. usesMethod (domain - GeneticElement; range - xsd:string)
3. hasHGNCsymbol (domain - TranscriptionFactor, TargetGene; range - xsd:string)
4. hasChromosomeNumber (domain - Enhancer, SuperEnhancer, ChromatinRegionModule; range - xsd:integer)
5. hasGenomicStart (domain - Enhancer, SuperEnhancer, ChromatinRegionModule; range - xsd:integer)
6. hasGenomicEnd (domain - Enhancer, SuperEnhancer, ChromatinRegionModule; range - xsd:integer)
7. hasScore (domain - GeneticElement; range - xsd:float)