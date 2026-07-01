**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - integer
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - unique identifier for chromatin regulatory module - string
5. crossref: type - reference ID for external data sources - string
6. current_assembly: type - genomic assembly version - string
7. current_chr: type - chromosome number of the enhancer - integer
8. disease: type - name of the disease associated with the enhancer - string
9. disease_method: type - method used in disease association study - string
10. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - integer
11. enh2gene_method: type - method used in enhancer to gene interaction study - string
12. enh_method: type - method used in enhancer study - string
13. hgnc_symbol_TFs: type - HGNC symbol of the transcription factor - string
14. hgnc_symbol_target_genes: type - HGNC symbols of target genes - string
15. minimum_ratio: type - minimum ratio value - float
16. mutation_PMID: type - PubMed ID for mutation study - integer
17. mutation_method: type - method used in mutation study - string
18. orig_assembly: type - original genomic assembly version - string
19. orig_chr: type - chromosome number of the enhancer in original assembly - integer
20. original_ID: type - unique identifier for the enhancer in original assembly - string
21. refseq_ID: type - RefSeq ID of the enhancer - string
22. score: type - score value - float
23. source: type - data source - string
24. type: type - type of genetic regulatory element - string
25. current_end: type - end position of the enhancer in current assembly - integer
26. current_start: type - start position of the enhancer in current assembly - integer
27. disease_PMID: type - PubMed ID for disease study - integer
28. enh_PMID: type - PubMed ID for enhancer study - integer
29. orig_end: type - end position of the enhancer in original assembly - integer
30. orig_start: type - start position of the enhancer in original assembly - integer

**Classes:**
1. GeneticRegulatoryElement
2. Enhancer
3. SuperEnhancer
4. TranscriptionFactor
5. TargetGene
6. Disease
7. CellLineOrBiosample

**Subclasses:**
1. Enhancer subclass of -> GeneticRegulatoryElement
2. SuperEnhancer subclass of -> Enhancer
3. TranscriptionFactor subclass of -> GeneticRegulatoryElement
4. TargetGene subclass of -> GeneticRegulatoryElement
5. Disease subclass of -> GeneticRegulatoryElement
6. CellLineOrBiosample subclass of -> GeneticRegulatoryElement

**Object Properties:**
1. hasTranscriptionFactor: domain - Enhancer or SuperEnhancer - range - TranscriptionFactor
2. hasTargetGene: domain - Enhancer, SuperEnhancer, or Disease - range - TargetGene
3. associatedWithDisease: domain - Enhancer, SuperEnhancer, or CellLineOrBiosample - range - Disease
4. occursInCellLineOrBiosample: domain - Enhancer, SuperEnhancer, TranscriptionFactor, or TargetGene - range - CellLineOrBiosample

**Data Type Properties:**
1. hasPubMedID: domain - GeneticRegulatoryElement - range - integer
2. hasMethod: domain - GeneticRegulatoryElement - range - string
3. hasChromosomeNumber: domain - Enhancer, SuperEnhancer, or CellLineOrBiosample - range - integer
4. hasScore: domain - GeneticRegulatoryElement - range - float
5. hasAssemblyVersion: domain - GeneticRegulatoryElement - range - string
6. hasRefSeqID: domain - Enhancer, SuperEnhancer, or TranscriptionFactor - range - string
7. hasHGNCSymbol: domain - TranscriptionFactor or TargetGene - range - string