**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer mapping - single value
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer mapping - single value
3. biosample_name: categorical - Name of the biosample or cell line - single value
4. crm_ID: text - Identifier for cis-regulatory module - multiple values
5. crossref: categorical - Cross-reference information - single value
6. current_assembly: categorical - Current genome assembly version - single value
7. current_chr: text - Current chromosome - multiple values
8. disease: text - Disease associated with the data - multiple values
9. disease_method: categorical - Method used for disease association - single value
10. enh2gene_PMID: text - PubMed ID for enhancer to gene mapping - multiple values
11. enh2gene_method: categorical - Method used for enhancer to gene mapping - single value
12. enh_method: categorical - Method used for enhancer identification - single value
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - single value
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - multiple values
15. minimum_ratio: categorical - Minimum ratio value - single value
16. mutation_PMID: text - PubMed ID for mutation information - multiple values
17. mutation_method: categorical - Method used for mutation identification - single value
18. orig_assembly: categorical - Original genome assembly version - single value
19. orig_chr: text - Original chromosome - multiple values
20. original_ID: text - Original identifier - multiple values
21. refseq_ID: text - RefSeq identifier - multiple values
22. score: categorical - Score value - single value
23. source: categorical - Source of the data - single value
24. type: categorical - Type of data - single value
25. current_end: Numerical - Current end position in the genome - range: 635800.0 to 232295090.0
26. current_start: Numerical - Current start position in the genome - range: 613202.0 to 232289692.0
27. disease_PMID: Numerical - PubMed ID for disease information - range: 16269442.0 to 29093029.0
28. enh_PMID: Numerical - PubMed ID for enhancer information - range: 16269442.0 to 29093029.0
29. orig_end: Numerical - Original end position in the genome - range: 685800.0 to 233159800.0
30. orig_start: Numerical - Original start position in the genome - range: 663202.0 to 233154402.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. Gene
8. TranscriptionFactor
9. Mutation

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. Chromosome: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor
8. hasMutation: GeneticElement - Mutation

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. crossref: GeneticElement - xsd:string
3. current_assembly: GeneticElement - xsd:string
4. current_chr: Chromosome - xsd:string
5. disease: Disease - xsd:string
6. enh2gene_PMID: Publication - xsd:string
7. enh2gene_method: Method - xsd:string
8. enh_method: Method - xsd:string
9. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
10. hgnc_symbol_target_genes: Gene - xsd:string
11. minimum_ratio: GeneticElement - xsd:float
12. mutation_PMID: Publication - xsd:string
13. mutation_method: Method - xsd:string
14. orig_assembly: GeneticElement - xsd:string
15. orig_chr: Chromosome - xsd:string
16. original_ID: GeneticElement - xsd:string
17. refseq_ID: Gene - xsd:string
18. score: GeneticElement - xsd:float
19. source: GeneticElement - xsd:string
20. type: GeneticElement - xsd:string
21. current_end: GenomicCoordinate - xsd:integer
22. current_start: GenomicCoordinate - xsd:integer
23. disease_PMID: Publication - xsd:integer
24. enh_PMID: Publication - xsd:integer
25. orig_end: GenomicCoordinate - xsd:integer
26. orig_start: GenomicCoordinate - xsd:integer