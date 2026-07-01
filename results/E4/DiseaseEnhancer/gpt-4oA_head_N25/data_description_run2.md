**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer mapping - unique values: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer mapping - unique values: 1
3. biosample_name: categorical - Name of the biosample - unique values: 1
4. crm_ID: text - Cis-regulatory module ID - unique values: 13
5. crossref: categorical - Cross-reference information - unique values: 1
6. current_assembly: categorical - Current genome assembly version - unique values: 1
7. current_chr: categorical - Current chromosome - unique values: 5
8. disease: text - Disease associated with the data - unique values: 21
9. disease_method: categorical - Method used for disease association - unique values: 1
10. enh2gene_PMID: text - PubMed ID for enhancer to gene mapping - unique values: 11
11. enh2gene_method: categorical - Method used for enhancer to gene mapping - unique values: 1
12. enh_method: categorical - Method used for enhancer identification - unique values: 1
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 11
15. minimum_ratio: categorical - Minimum ratio value - unique values: 1, range: 0.95
16. mutation_PMID: categorical - PubMed ID for mutation information - unique values: 6
17. mutation_method: categorical - Method used for mutation identification - unique values: 1
18. orig_assembly: categorical - Original genome assembly version - unique values: 1
19. orig_chr: categorical - Original chromosome - unique values: 5
20. original_ID: text - Original ID - unique values: 13
21. refseq_ID: categorical - RefSeq ID - unique values: 6
22. score: categorical - Score value - unique values: 1, range: 1.0
23. source: categorical - Source of the data - unique values: 1
24. type: categorical - Type of data - unique values: 1
25. current_end: Numerical - Current end position in the genome - range: 107935.0 to 162052179.0
26. current_start: Numerical - Current start position in the genome - range: 105934.0 to 162050179.0
27. disease_PMID: Numerical - PubMed ID for disease information - range: 16269442.0 to 28717659.0
28. enh_PMID: Numerical - PubMed ID for enhancer information - range: 16269442.0 to 28717659.0
29. orig_end: Numerical - Original end position in the genome - range: 107935.0 to 162021969.0
30. orig_start: Numerical - Original start position in the genome - range: 105934.0 to 162019969.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. Gene
8. TranscriptionFactor

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. Chromosome: subclass of -> GenomicCoordinate

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. crm_ID: GeneticElement - xsd:string
2. original_ID: GeneticElement - xsd:string
3. type: GeneticElement - xsd:string
4. current_start: GenomicCoordinate - xsd:integer
5. current_end: GenomicCoordinate - xsd:integer
6. orig_start: GenomicCoordinate - xsd:integer
7. orig_end: GenomicCoordinate - xsd:integer
8. current_chr: Chromosome - xsd:string
9. orig_chr: Chromosome - xsd:string
10. current_assembly: GenomicCoordinate - xsd:string
11. orig_assembly: GenomicCoordinate - xsd:string
12. biosample_name: Biosample - xsd:string
13. disease: Disease - xsd:string
14. disease_PMID: Disease - xsd:integer
15. enh2gene_PMID: Publication - xsd:string
16. enh_PMID: Publication - xsd:integer
17. TFs2enh_PMID: Publication - xsd:string
18. mutation_PMID: Publication - xsd:string
19. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
20. hgnc_symbol_target_genes: Gene - xsd:string
21. minimum_ratio: GeneticElement - xsd:float
22. score: GeneticElement - xsd:float
23. source: GeneticElement - xsd:string