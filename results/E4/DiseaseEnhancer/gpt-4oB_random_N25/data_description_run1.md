**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - unique
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer associations - unique
3. biosample_name: categorical - Name of the biosample or cell line - unique
4. crm_ID: text - Unique identifier for cis-regulatory modules - unique
5. crossref: categorical - Cross-reference identifier - unique
6. current_assembly: categorical - Current genome assembly version - unique
7. current_chr: text - Current chromosome identifier - unique
8. disease: text - Disease associated with the genetic element - unique
9. disease_method: categorical - Method used for identifying disease associations - unique
10. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - unique
11. enh_method: categorical - Method used for identifying enhancers - unique
12. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique
13. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique
14. minimum_ratio: categorical - Minimum ratio value - 0.95
15. mutation_PMID: categorical - PubMed ID for mutation associations - unique
16. mutation_method: categorical - Method used for identifying mutation associations - unique
17. orig_assembly: categorical - Original genome assembly version - unique
18. orig_chr: text - Original chromosome identifier - unique
19. original_ID: text - Original identifier for the genetic element - unique
20. refseq_ID: text - RefSeq identifier - unique
21. score: categorical - Score value - 1.0
22. source: categorical - Source of the data - unique
23. type: categorical - Type of genetic element - unique
24. current_end: Numerical - Current end position in the genome - range: 2137970.0 to 188083612.0
25. current_start: Numerical - Current start position in the genome - range: 2136972.0 to 188081014.0
26. disease_PMID: Numerical - PubMed ID for disease associations - range: 19543368.0 to 29093029.0
27. enh2gene_PMID: Numerical - PubMed ID for enhancer to gene associations - range: 19543368.0 to 29093029.0
28. enh_PMID: Numerical - PubMed ID for enhancer associations - range: 19543368.0 to 29093029.0
29. orig_end: Numerical - Original end position in the genome - range: 2159200.0 to 187801400.0
30. orig_start: Numerical - Original start position in the genome - range: 2158202.0 to 187798802.0

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
1. crmID: GeneticElement - xsd:string
2. crossrefID: GeneticElement - xsd:string
3. currentAssembly: GeneticElement - xsd:string
4. currentChr: GeneticElement - xsd:string
5. diseaseName: Disease - xsd:string
6. hgncSymbol: GeneticElement - xsd:string
7. minimumRatio: GeneticElement - xsd:float
8. originalID: GeneticElement - xsd:string
9. refseqID: GeneticElement - xsd:string
10. score: GeneticElement - xsd:float
11. source: GeneticElement - xsd:string
12. type: GeneticElement - xsd:string
13. currentEnd: GeneticElement - xsd:integer
14. currentStart: GeneticElement - xsd:integer
15. diseasePMID: Disease - xsd:integer
16. enh2genePMID: Publication - xsd:integer
17. enhPMID: Publication - xsd:integer
18. origEnd: GeneticElement - xsd:integer
19. origStart: GeneticElement - xsd:integer