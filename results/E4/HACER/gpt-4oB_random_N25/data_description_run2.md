**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - unique values: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer associations - unique values: 1
3. biosample_name: text - Name of the biosample - unique values: 24
4. crm_ID: text - ID of the cis-regulatory module - unique values: 25
5. crossref: categorical - Cross-reference information - unique values: 4
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: text - Current chromosome - unique values: 12
8. disease: categorical - Disease associated with the data - unique values: 1
9. disease_PMID: categorical - PubMed ID for disease associations - unique values: 1
10. disease_method: categorical - Method used for disease associations - unique values: 1
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - unique values: 2
12. enh2gene_method: categorical - Method used for enhancer to gene associations - unique values: 4
13. enh_PMID: categorical - PubMed ID for enhancer information - unique values: 1
14. enh_method: categorical - Method used for enhancer information - unique values: 2
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 20
17. minimum_ratio: categorical - Minimum ratio value - unique values: 1
18. mutation_PMID: categorical - PubMed ID for mutation information - unique values: 2
19. mutation_method: categorical - Method used for mutation information - unique values: 2
20. orig_assembly: categorical - Original genome assembly version - unique values: 1
21. orig_chr: text - Original chromosome - unique values: 12
22. original_ID: categorical - Original ID - unique values: 4
23. refsnp_ID: categorical - Reference SNP ID - unique values: 4
24. score: categorical - Score value - unique values: 2
25. source: categorical - Source of the data - unique values: 1
26. type: categorical - Type of data - unique values: 1
27. current_end: Numerical - Current end position in the genome - range: 1021432.0 to 224410716.0
28. current_start: Numerical - Current start position in the genome - range: 1021183.0 to 224410422.0
29. orig_end: Numerical - Original end position in the genome - range: 956812.0 to 224598418.0
30. orig_start: Numerical - Original start position in the genome - range: 956563.0 to 224598124.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. TranscriptionFactor
8. TargetGene
9. Mutation
10. SNP

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. regulatesTranscriptionFactor: GeneticElement - TranscriptionFactor
7. targetsGene: GeneticElement - TargetGene
8. associatedWithMutation: GeneticElement - Mutation
9. associatedWithSNP: GeneticElement - SNP

**Data Type Properties:**
1. biosampleName: Biosample - xsd:string
2. crmID: CisRegulatoryModule - xsd:string
3. crossref: GeneticElement - xsd:string
4. currentAssembly: GenomicCoordinate - xsd:string
5. currentChr: GenomicCoordinate - xsd:string
6. diseaseName: Disease - xsd:string
7. diseasePMID: Disease - xsd:string
8. diseaseMethod: Disease - xsd:string
9. enh2genePMID: Publication - xsd:string
10. enh2geneMethod: Method - xsd:string
11. enhPMID: Publication - xsd:string
12. enhMethod: Method - xsd:string
13. hgncSymbolTFs: TranscriptionFactor - xsd:string
14. hgncSymbolTargetGenes: TargetGene - xsd:string
15. minimumRatio: GeneticElement - xsd:float
16. mutationPMID: Publication - xsd:string
17. mutationMethod: Method - xsd:string
18. origAssembly: GenomicCoordinate - xsd:string
19. origChr: GenomicCoordinate - xsd:string
20. originalID: GeneticElement - xsd:string
21. refsnpID: SNP - xsd:string
22. score: GeneticElement - xsd:float
23. source: GeneticElement - xsd:string
24. type: GeneticElement - xsd:string
25. currentEnd: GenomicCoordinate - xsd:integer
26. currentStart: GenomicCoordinate - xsd:integer
27. origEnd: GenomicCoordinate - xsd:integer
28. origStart: GenomicCoordinate - xsd:integer