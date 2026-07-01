**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for Transcription Factor to Enhancer relationship - range: xsd:string
2. TFs2enh_method: type - Method used in Transcription Factor to Enhancer relationship - range: xsd:string
3. biosample_name: type - Name of the cell line/biosample - range: xsd:string
4. crm_ID: type - Cell Regulatory Module ID - range: xsd:string
5. crossref: type - Cross-reference information - range: xsd:string
6. current_assembly: type - Current genome assembly version - range: xsd:string
7. current_chr: type - Chromosome number in the current assembly - range: xsd:string
8. disease: type - Disease associated with the genetic regulatory element - range: xsd:string
9. disease_method: type - Method used to identify disease association - range: xsd:string
10. enh2gene_method: type - Method used in Enhancer to Gene relationship - range: xsd:string
11. enh_method: type - Method used in Enhancer identification - range: xsd:string
12. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - range: xsd:string
13. hgnc_symbol_target_genes: type - HGNC symbols of target genes - range: xsd:string
14. minimum_ratio: type - Minimum ratio value - range: xsd:float
15. mutation_PMID: type - PubMed ID for Mutation information - range: xsd:string
16. mutation_method: type - Method used in Mutation identification - range: xsd:string
17. orig_assembly: type - Original genome assembly version - range: xsd:string
18. orig_chr: type - Chromosome number in the original assembly - range: xsd:string
19. original_ID: type - Original ID of the genetic regulatory element - range: xsd:string
20. refseq_ID: type - RefSeq ID of the gene - range: xsd:string
21. score: type - Score associated with the relationship - range: xsd:float
22. source: type - Source of the data - range: xsd:string
23. type: type - Type of genetic regulatory element (e.g., enhancer, super-enhancer) - range: xsd:string
24. current_end: type - End position in the current assembly - range: xsd:int
25. current_start: type - Start position in the current assembly - range: xsd:int
26. disease_PMID: type - PubMed ID for Disease information - range: xsd:int
27. enh2gene_PMID: type - PubMed ID for Enhancer to Gene relationship - range: xsd:int
28. enh_PMID: type - PubMed ID for Enhancer information - range: xsd:int
29. orig_end: type - End position in the original assembly - range: xsd:int
30. orig_start: type - Start position in the original assembly - range: xsd:int

**Classes:**
1. GeneticRegulatoryElement (class_entity)
   - Subclasses:
     1. Enhancer (subclass of -> GeneticRegulatoryElement)
     2. SuperEnhancer (subclass of -> GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain: Enhancer, range: TranscriptionFactor)
2. hasTargetGene (domain: Enhancer, range: Gene)
3. associatedWithDisease (domain: GeneticRegulatoryElement, range: Disease)
4. hasPubMedID (domain: GeneticRegulatoryElement, range: xsd:string)
5. hasMethod (domain: GeneticRegulatoryElement, range: xsd:string)
6. hasChromosome (domain: GeneticRegulatoryElement, range: xsd:string)
7. hasAssemblyVersion (domain: GeneticRegulatoryElement, range: xsd:string)

**Data Type Properties:**
1. hasScore (domain: GeneticRegulatoryElement, range: xsd:float)
2. hasRatio (domain: GeneticRegulatoryElement, range: xsd:float)
3. hasStartPosition (domain: GeneticRegulatoryElement, range: xsd:int)
4. hasEndPosition (domain: GeneticRegulatoryElement, range: xsd:int)