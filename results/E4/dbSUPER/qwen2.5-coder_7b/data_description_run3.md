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
24. score: type - Score value - range: xsd:float
25. source: type - Source of the data - range: xsd:string
26. type: type - Type of genetic regulatory element (enhancer, super-enhancer) - range: xsd:string
27. current_end: type - End position in the current assembly - range: xsd:int
28. current_start: type - Start position in the current assembly - range: xsd:int
29. orig_end: type - End position in the original assembly - range: xsd:int
30. orig_start: type - Start position in the original assembly - range: xsd:int

**Classes:**
1. GeneticRegulatoryElement (class_entity)
   1. Enhancer (subclass of -> GeneticRegulatoryElement)
   2. SuperEnhancer (subclass of -> GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - GeneticRegulatoryElement, range - TranscriptionFactor)
2. hasTargetGene (domain - GeneticRegulatoryElement, range - Gene)
3. associatedWithDisease (domain - GeneticRegulatoryElement, range - Disease)
4. hasPubMedID (domain - GeneticRegulatoryElement, range - xsd:string)
5. usesMethod (domain - GeneticRegulatoryElement, range - Method)

**Data Type Properties:**
1. assemblyVersion (domain - GeneticRegulatoryElement, range - xsd:string)
2. chromosomeNumber (domain - GeneticRegulatoryElement, range - xsd:int)
3. scoreValue (domain - GeneticRegulatoryElement, range - xsd:float)
4. startPosition (domain - GeneticRegulatoryElement, range - xsd:int)
5. endPosition (domain - GeneticRegulatoryElement, range - xsd:int)