**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer interaction - range: xsd:string
2. TFs2enh_method: type - method used in transcription factor to enhancer interaction study - range: xsd:string
3. biosample_name: type - name of the cell line or biosample - range: xsd:string
4. crm_ID: type - ID of the chromatin regulatory module - range: xsd:string
5. crossref: type - reference for the data - range: xsd:string
6. current_assembly: type - current genome assembly version - range: xsd:string
7. current_chr: type - chromosome number in the current assembly - range: xsd:string
8. disease: type - disease associated with the genetic regulatory element - range: xsd:string
9. disease_PMID: type - PubMed ID for disease study - range: xsd:string
10. disease_method: type - method used in disease study - range: xsd:string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene interaction - range: xsd:string
12. enh2gene_method: type - method used in enhancer to gene interaction study - range: xsd:string
13. enh_PMID: type - PubMed ID for enhancer study - range: xsd:string
14. enh_method: type - method used in enhancer study - range: xsd:string
15. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - range: xsd:string
16. hgnc_symbol_target_genes: type - HGNC symbols of the target genes - range: xsd:string
17. minimum_ratio: type - minimum ratio value - range: xsd:float
18. mutation_PMID: type - PubMed ID for mutation study - range: xsd:string
19. mutation_method: type - method used in mutation study - range: xsd:string
20. orig_assembly: type - original genome assembly version - range: xsd:string
21. orig_chr: type - chromosome number in the original assembly - range: xsd:string
22. original_ID: type - ID of the original data - range: xsd:string
23. refsnp_ID: type - RSID for the genetic variant - range: xsd:string
24. score: type - score associated with the interaction or study - range: xsd:float
25. source: type - source of the data - range: xsd:string
26. type: type - type of the genetic regulatory element (enhancer, super-enhancer) - range: xsd:string
27. current_end: type - end position in the current assembly - range: xsd:int
28. current_start: type - start position in the current assembly - range: xsd:int
29. orig_end: type - end position in the original assembly - range: xsd:int
30. orig_start: type - start position in the original assembly - range: xsd:int

**Classes:**
1. GeneticRegulatoryElement (subClassOf: Entity)
2. TranscriptionFactor (subClassOf: GeneticRegulatoryElement)
3. Enhancer (subClassOf: GeneticRegulatoryElement)
4. SuperEnhancer (subClassOf: Enhancer)
5. TargetGene (subClassOf: GeneticRegulatoryElement)
6. CellLineOrBiosample (subClassOf: Entity)

**Object Properties:**
1. hasTranscriptionFactor (domain: TranscriptionFactor, range: GeneticRegulatoryElement)
2. interactsWithEnhancer (domain: Enhancer, range: GeneticRegulatoryElement)
3. associatedWithDisease (domain: GeneticRegulatoryElement, range: Disease)
4. locatedInCellLineOrBiosample (domain: GeneticRegulatoryElement, range: CellLineOrBiosample)
5. hasTargetGene (domain: GeneticRegulatoryElement, range: TargetGene)

**Data Type Properties:**
1. pmid (domain: PubMedID, range: xsd:string)
2. method (domain: Method, range: xsd:string)
3. chromosomeNumber (domain: ChromosomeNumber, range: xsd:int)
4. scoreValue (domain: Score, range: xsd:float)