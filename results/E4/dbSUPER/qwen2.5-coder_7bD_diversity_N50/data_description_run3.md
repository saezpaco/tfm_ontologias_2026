**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - range: xsd:string
2. TFs2enh_method: type - Method used in transcription factor to enhancer interaction study - range: xsd:string
3. biosample_name: type - Name of the cell line or biosample - range: xsd:string
4. crm_ID: type - ID of the chromatin regulatory module - range: xsd:string
5. crossref: type - Cross-reference identifier for the data - range: xsd:string
6. current_assembly: type - Current genome assembly version - range: xsd:string
7. current_chr: type - Chromosome number in the current assembly - range: xsd:string
8. disease: type - Disease associated with the genetic regulatory element - range: xsd:string
9. disease_PMID: type - PubMed ID for disease study - range: xsd:string
10. disease_method: type - Method used in disease study - range: xsd:string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - range: xsd:string
12. enh2gene_method: type - Method used in enhancer to gene interaction study - range: xsd:string
13. enh_PMID: type - PubMed ID for enhancer study - range: xsd:string
14. enh_method: type - Method used in enhancer study - range: xsd:string
15. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - range: xsd:string
16. hgnc_symbol_target_genes: type - HGNC symbols of target genes - range: xsd:string
17. minimum_ratio: type - Minimum ratio value - range: xsd:float
18. mutation_PMID: type - PubMed ID for mutation study - range: xsd:string
19. mutation_method: type - Method used in mutation study - range: xsd:string
20. orig_assembly: type - Original genome assembly version - range: xsd:string
21. orig_chr: type - Chromosome number in the original assembly - range: xsd:string
22. original_ID: type - Original ID of the genetic regulatory element - range: xsd:string
23. refsnp_ID: type - Reference SNP identifier - range: xsd:string
24. source: type - Source of the data - range: xsd:string
25. type: type - Type of the genetic regulatory element (e.g., enhancer, super-enhancer) - range: xsd:string
26. current_end: type - End position in the current assembly - range: xsd:integer
27. current_start: type - Start position in the current assembly - range: xsd:integer
28. orig_end: type - End position in the original assembly - range: xsd:integer
29. orig_start: type - Start position in the original assembly - range: xsd:integer
30. score: type - Score associated with the genetic regulatory element - range: xsd:float

**Classes:**
1. GeneticRegulatoryElement
2. TranscriptionFactor
3. Enhancer
4. SuperEnhancer
5. TargetGene
6. Disease
7. CellLineOrBiosample
8. Mutation
9. ChromatinRegulatoryModule

**Subclasses:**
1. TranscriptionFactorToEnhancerInteraction (subclass of GeneticRegulatoryElement)
2. EnhancerToGeneInteraction (subclass of GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain: TranscriptionFactorToEnhancerInteraction, range: TranscriptionFactor)
2. hasEnhancer (domain: TranscriptionFactorToEnhancerInteraction, range: Enhancer)
3. hasTargetGene (domain: EnhancerToGeneInteraction, range: TargetGene)
4. associatedWithDisease (domain: GeneticRegulatoryElement, range: Disease)
5. occursInCellLineOrBiosample (domain: GeneticRegulatoryElement, range: CellLineOrBiosample)
6. involvesMutation (domain: GeneticRegulatoryElement, range: Mutation)
7. partOfChromatinRegulatoryModule (domain: Enhancer, range: ChromatinRegulatoryModule)

**Data Type Properties:**
1. pmid (domain: PubMed ID, range: xsd:string)
2. method (domain: Method, range: xsd:string)
3. chromosomeNumber (domain: Chromosome Number, range: xsd:string)
4. hgncSymbol (domain: HGNC Symbol, range: xsd:string)
5. scoreValue (domain: Score Value, range: xsd:float)