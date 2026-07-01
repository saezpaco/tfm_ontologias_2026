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
8. disease: type - disease associated with the genetic element - string
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
20. original_ID: type - unique identifier for the genetic element - string
21. refseq_ID: type - RefSeq ID of the gene - string
22. score: type - score indicating confidence or significance - float
23. source: type - data source - string
24. type: type - type of genetic regulatory element (enhancer, super-enhancer) - string
25. current_end: type - end position of the enhancer in current assembly - integer
26. current_start: type - start position of the enhancer in current assembly - integer
27. disease_PMID: type - PubMed ID for disease study - integer
28. enh_PMID: type - PubMed ID for enhancer study - integer
29. orig_end: type - end position of the enhancer in original assembly - integer
30. orig_start: type - start position of the enhancer in original assembly - integer

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
1. TranscriptionFactor (subclass of -> GeneticElement)
2. Enhancer (subclass of -> GeneticElement)
3. SuperEnhancer (subclass of -> Enhancer)
4. TargetGene (subclass of -> GeneticElement)
5. Disease (subclass of -> GeneticElement)
6. CellLineOrBiosample (subclass of -> GeneticElement)
7. Mutation (subclass of -> GeneticElement)
8. ChromatinRegulatoryModule (subclass of -> GeneticElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactor, range - Enhancer)
2. hasTargetGene (domain - Enhancer, range - TargetGene)
3. associatedWithDisease (domain - GeneticElement, range - Disease)
4. occursInCellLineOrBiosample (domain - GeneticElement, range - CellLineOrBiosample)
5. involvesMutation (domain - GeneticElement, range - Mutation)
6. partOfChromatinRegulatoryModule (domain - Enhancer, range - ChromatinRegulatoryModule)

**Data Type Properties:**
1. pmid (domain - PubMed ID, range - xsd:int)
2. method (domain - Method, range - xsd:string)
3. chromosomeNumber (domain - Chromosome Number, range - xsd:int)
4. score (domain - Score, range - xsd:float)