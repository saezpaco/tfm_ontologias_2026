**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - unique_count: 1
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer associations - unique_count: 1
3. biosample_name: text - Name of the biosample or cell line - unique_count: 11
4. crm_ID: categorical - ID for cis-regulatory module - unique_count: 2
5. crossref: categorical - Cross-reference information - unique_count: 1
6. current_assembly: categorical - Current genome assembly version - unique_count: 1
7. current_chr: categorical - Current chromosome - unique_count: 2
8. current_end: categorical - End position in the current genome assembly - unique_count: 2
9. current_start: categorical - Start position in the current genome assembly - unique_count: 2
10. disease: categorical - Disease associated with the genetic element - unique_count: 1
11. disease_PMID: categorical - PubMed ID for disease association - unique_count: 1
12. disease_method: categorical - Method used for identifying disease association - unique_count: 1
13. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - unique_count: 2
14. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - unique_count: 4
15. enh_PMID: categorical - PubMed ID for enhancer information - unique_count: 1
16. enh_method: categorical - Method used for identifying enhancers - unique_count: 1
17. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique_count: 1
18. hgnc_symbol_target_genes: categorical - HGNC symbol for target genes - unique_count: 5
19. minimum_ratio: categorical - Minimum ratio value - unique_count: 1
20. mutation_PMID: categorical - PubMed ID for mutation information - unique_count: 1
21. mutation_method: categorical - Method used for identifying mutations - unique_count: 1
22. orig_assembly: categorical - Original genome assembly version - unique_count: 1
23. orig_chr: categorical - Original chromosome - unique_count: 2
24. orig_end: categorical - End position in the original genome assembly - unique_count: 2
25. orig_start: categorical - Start position in the original genome assembly - unique_count: 2
26. original_ID: categorical - Original ID for the genetic element - unique_count: 1
27. refsnp_ID: categorical - Reference SNP ID - unique_count: 1
28. score: categorical - Score value - unique_count: 1
29. source: categorical - Source of the data - unique_count: 1
30. type: categorical - Type of genetic element - unique_count: 1

**classes:**
1. GeneticElement
2. Biosample
3. Disease
4. Method
5. Publication

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. TranscriptionFactor: subclass of -> GeneticElement
4. TargetGene: subclass of -> GeneticElement
5. Mutation: subclass of -> GeneticElement

**Object Properties:**
1. hasBiosample: GeneticElement - Biosample
2. associatedWithDisease: GeneticElement - Disease
3. identifiedByMethod: GeneticElement - Method
4. referencedInPublication: GeneticElement - Publication
5. regulates: TranscriptionFactor - TargetGene
6. locatedOnChromosome: GeneticElement - xsd:string

**Data Type Properties:**
1. biosampleName: Biosample - xsd:string
2. crmID: GeneticElement - xsd:string
3. crossref: GeneticElement - xsd:string
4. currentAssembly: GeneticElement - xsd:string
5. currentChr: GeneticElement - xsd:string
6. currentEnd: GeneticElement - xsd:integer
7. currentStart: GeneticElement - xsd:integer
8. diseaseName: Disease - xsd:string
9. diseasePMID: Disease - xsd:string
10. enh2genePMID: Publication - xsd:string
11. enh2geneMethod: Method - xsd:string
12. enhPMID: Publication - xsd:string
13. enhMethod: Method - xsd:string
14. hgncSymbolTFs: TranscriptionFactor - xsd:string
15. hgncSymbolTargetGenes: TargetGene - xsd:string
16. minimumRatio: GeneticElement - xsd:float
17. mutationPMID: Publication - xsd:string
18. mutationMethod: Method - xsd:string
19. origAssembly: GeneticElement - xsd:string
20. origChr: GeneticElement - xsd:string
21. origEnd: GeneticElement - xsd:integer
22. origStart: GeneticElement - xsd:integer
23. originalID: GeneticElement - xsd:string
24. refsnpID: GeneticElement - xsd:string
25. score: GeneticElement - xsd:float
26. source: GeneticElement - xsd:string
27. type: GeneticElement - xsd:string