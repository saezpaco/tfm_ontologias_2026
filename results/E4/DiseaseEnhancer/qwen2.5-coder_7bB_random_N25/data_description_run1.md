**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for Transcription Factor to Enhancer relationship - range: xsd:string
2. TFs2enh_method: type - Method used in Transcription Factor to Enhancer relationship - range: xsd:string
3. biosample_name: type - Name of the cell line/biosample - range: xsd:string
4. crm_ID: type - Cell Regulatory Module ID - range: xsd:string
5. crossref: type - Cross-reference information - range: xsd:string
6. current_assembly: type - Current genome assembly version - range: xsd:string
7. current_chr: type - Chromosome number of the enhancer - range: xsd:string
8. disease: type - Disease associated with the enhancer - range: xsd:string
9. disease_method: type - Method used in disease association - range: xsd:string
10. enh2gene_method: type - Method used in Enhancer to Gene relationship - range: xsd:string
11. enh_method: type - Method used in Enhancer identification - range: xsd:string
12. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - range: xsd:string
13. hgnc_symbol_target_genes: type - HGNC symbols of target genes - range: xsd:string
14. minimum_ratio: type - Minimum ratio value - range: xsd:float
15. mutation_PMID: type - PubMed ID for Mutation information - range: xsd:string
16. mutation_method: type - Method used in mutation analysis - range: xsd:string
17. orig_assembly: type - Original genome assembly version - range: xsd:string
18. orig_chr: type - Chromosome number of the enhancer (original) - range: xsd:string
19. original_ID: type - Original ID of the enhancer - range: xsd:string
20. refseq_ID: type - RefSeq ID of the enhancer - range: xsd:string
21. score: type - Score associated with the enhancer - range: xsd:float
22. source: type - Source of the data - range: xsd:string
23. type: type - Type of genetic regulatory element (enhancer, super-enhancer) - range: xsd:string
24. current_end: type - End position of the enhancer in the current assembly - range: xsd:int
25. current_start: type - Start position of the enhancer in the current assembly - range: xsd:int
26. disease_PMID: type - PubMed ID for Disease information - range: xsd:string
27. enh2gene_PMID: type - PubMed ID for Enhancer to Gene relationship - range: xsd:string
28. enh_PMID: type - PubMed ID for Enhancer information - range: xsd:string
29. orig_end: type - End position of the enhancer in the original assembly - range: xsd:int
30. orig_start: type - Start position of the enhancer in the original assembly - range: xsd:int

**Classes:**
1. GeneticRegulatoryElement
2. Enhancer
3. SuperEnhancer
4. TranscriptionFactor
5. TargetGene
6. Disease
7. CellLineBiosample
8. Mutation
9. PubMedArticle

**Subclasses:**
1. TranscriptionFactorToEnhancerRelationship (subclass of GeneticRegulatoryElement)
2. EnhancerToGeneRelationship (subclass of GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain: TranscriptionFactor, range: TranscriptionFactorToEnhancerRelationship)
2. hasTargetGene (domain: EnhancerToGeneRelationship, range: TargetGene)
3. associatedWithDisease (domain: GeneticRegulatoryElement, range: Disease)
4. occursInCellLineBiosample (domain: GeneticRegulatoryElement, range: CellLineBiosample)
5. involvesMutation (domain: GeneticRegulatoryElement, range: Mutation)

**Data Type Properties:**
1. pmid (domain: PubMedArticle, range: xsd:string)
2. method (domain: GeneticRegulatoryElement, range: xsd:string)
3. assemblyVersion (domain: GeneticRegulatoryElement, range: xsd:string)
4. chromosomeNumber (domain: GeneticRegulatoryElement, range: xsd:string)
5. ratioValue (domain: GeneticRegulatoryElement, range: xsd:float)
6. scoreValue (domain: GeneticRegulatoryElement, range: xsd:float)
7. sourceName (domain: GeneticRegulatoryElement, range: xsd:string)
8. typeOfElement (domain: GeneticRegulatoryElement, range: xsd:string)
9. startPosition (domain: GeneticRegulatoryElement, range: xsd:int)
10. endPosition (domain: GeneticRegulatoryElement, range: xsd:int)