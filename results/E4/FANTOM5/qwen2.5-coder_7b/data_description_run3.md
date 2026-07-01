**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer relationship - string
2. TFs2enh_method: type - method used in transcription factor to enhancer relationship - string
3. biosample: type - cell line or biosample - string
4. crm_ID: type - cluster region module identifier - string
5. crossref: type - cross-reference information - string
6. current_assembly: type - current genome assembly - string
7. current_chr: type - current chromosome number - integer
8. disease: type - disease associated with the genetic regulatory element - string
9. disease_PMID: type - PubMed ID for disease association - string
10. disease_method: type - method used in disease association - string
11. enh2gene_PMID: type - PubMed ID for enhancer to gene relationship - string
12. enh2gene_method: type - method used in enhancer to gene relationship - string
13. enh_PMID: type - PubMed ID for the genetic regulatory element - integer
14. enh_method: type - method used in the genetic regulatory element - string
15. hgnc_symbol_TFs: type - HGNC symbol of transcription factors - string
16. hgnc_symbol_target_genes: type - HGNC symbol of target genes - string
17. minimum_ratio: type - minimum ratio associated with the genetic regulatory element - float
18. mutation_PMID: type - PubMed ID for mutation information - string
19. mutation_method: type - method used in mutation analysis - string
20. orig_assembly: type - original genome assembly - string
21. orig_chr: type - original chromosome number - integer
22. original_ID: type - original identifier - string
23. refsnp_ID: type - reference SNP ID - string
24. score: type - score associated with the genetic regulatory element - float
25. source: type - source of the data - string
26. type: type - type of the genetic regulatory element (enhancer, super-enhancer) - string
27. current_end: type - current end position of the genetic regulatory element - integer
28. current_start: type - current start position of the genetic regulatory element - integer
29. orig_end: type - original end position of the genetic regulatory element - integer
30. orig_start: type - original start position of the genetic regulatory element - integer

**Classes:**
1. GeneticRegulatoryElement
2. TranscriptionFactor
3. Enhancer
4. SuperEnhancer
5. TargetGene
6. Disease
7. CellLineOrBiosample
8. Mutation
9. PubMedID
10. Method
11. Assembly
12. Chromosome

**Subclasses:**
1. TranscriptionFactorToEnhancerRelationship (subclass of GeneticRegulatoryElement)
2. EnhancerToGeneRelationship (subclass of GeneticRegulatoryElement)

**Object Properties:**
1. hasTranscriptionFactor (domain - TranscriptionFactor, range - TranscriptionFactorToEnhancerRelationship)
2. hasEnhancer (domain - Enhancer, range - TranscriptionFactorToEnhancerRelationship)
3. hasTargetGene (domain - TargetGene, range - EnhancerToGeneRelationship)
4. associatedWithDisease (domain - Disease, range - GeneticRegulatoryElement)
5. occursInCellLineOrBiosample (domain - CellLineOrBiosample, range - GeneticRegulatoryElement)
6. involvesMutation (domain - Mutation, range - GeneticRegulatoryElement)

**Data Type Properties:**
1. hasPubMedID (domain - PubMedID, range - xsd:string)
2. hasMethod (domain - Method, range - xsd:string)
3. hasAssembly (domain - Assembly, range - xsd:string)
4. hasChromosome (domain - Chromosome, range - xsd:int)
5. hasScore (domain - GeneticRegulatoryElement, range - xsd:float)
6. hasRatio (domain - GeneticRegulatoryElement, range - xsd:float)
7. hasStartPosition (domain - GeneticRegulatoryElement, range - xsd:int)
8. hasEndPosition (domain - GeneticRegulatoryElement, range - xsd:int)