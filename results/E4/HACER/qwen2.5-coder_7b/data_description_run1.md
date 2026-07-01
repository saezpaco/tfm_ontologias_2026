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
13. enh_PMID: type - PubMed ID for enhancer study - integer
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
25. source: type - data source - string
26. type: type - type of genetic regulatory element (e.g., enhancer, super-enhancer) - string
27. current_end: type - end position in the current assembly - integer
28. current_start: type - start position in the current assembly - integer
29. orig_end: type - end position in the original assembly - integer
30. orig_start: type - start position in the original assembly - integer

**Classes:**
1. GeneticRegulatoryElement
2. Enhancer
3. SuperEnhancer
4. TranscriptionFactor
5. TargetGene
6. Disease
7. CellLineOrBiosample
8. Mutation
9. ChromatinRegulatoryModule

**Subclasses:**
1. Enhancer subclass of -> GeneticRegulatoryElement
2. SuperEnhancer subclass of -> Enhancer
3. TranscriptionFactor subclass of -> GeneticRegulatoryElement
4. TargetGene subclass of -> GeneticRegulatoryElement
5. Disease subclass of -> GeneticRegulatoryElement
6. CellLineOrBiosample subclass of -> GeneticRegulatoryElement
7. Mutation subclass of -> GeneticRegulatoryElement
8. ChromatinRegulatoryModule subclass of -> GeneticRegulatoryElement

**Object Properties:**
1. hasTranscriptionFactor: domain - Enhancer, SuperEnhancer; range - TranscriptionFactor
2. hasTargetGene: domain - Enhancer, SuperEnhancer; range - TargetGene
3. associatedWithDisease: domain - GeneticRegulatoryElement; range - Disease
4. occursInCellLineOrBiosample: domain - GeneticRegulatoryElement; range - CellLineOrBiosample
5. involvesMutation: domain - GeneticRegulatoryElement; range - Mutation
6. partOfChromatinRegulatoryModule: domain - Enhancer, SuperEnhancer; range - ChromatinRegulatoryModule

**Data Type Properties:**
1. hasPMID: domain - GeneticRegulatoryElement; range - xsd:string
2. usesMethod: domain - GeneticRegulatoryElement; range - xsd:string
3. hasAssemblyVersion: domain - GeneticRegulatoryElement; range - xsd:string
4. hasChromosomeNumber: domain - GeneticRegulatoryElement; range - xsd:string
5. hasScore: domain - GeneticRegulatoryElement; range - xsd:float
6. hasSource: domain - GeneticRegulatoryElement; range - xsd:string
7. hasType: domain - GeneticRegulatoryElement; range - xsd:string
8. hasStartPosition: domain - GeneticRegulatoryElement; range - xsd:int
9. hasEndPosition: domain - GeneticRegulatoryElement; range - xsd:int