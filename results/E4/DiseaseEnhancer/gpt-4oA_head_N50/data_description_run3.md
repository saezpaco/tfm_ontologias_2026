**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer - unique values: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer - unique values: 1
3. biosample_name: categorical - Name of the biosample - unique values: 1
4. crm_ID: text - ID for cis-regulatory module - unique values: 19
5. crossref: categorical - Cross-reference information - unique values: 1
6. current_assembly: categorical - Current genome assembly - unique values: 1
7. current_chr: categorical - Current chromosome - unique values: 5
8. disease: text - Disease associated - unique values: 33
9. disease_method: categorical - Method used for disease association - unique values: 1
10. enh2gene_PMID: text - PubMed ID for enhancer to gene - unique values: 18
11. enh2gene_method: categorical - Method used for enhancer to gene - unique values: 1
12. enh_method: categorical - Method used for enhancer identification - unique values: 1
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique values: 1
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values: 16
15. minimum_ratio: categorical - Minimum ratio - unique values: 1, max: 0.95, mean: 0.95, min: 0.95, std: 6.72896768e-16
16. mutation_PMID: text - PubMed ID for mutation - unique values: 12
17. mutation_method: categorical - Method used for mutation identification - unique values: 1
18. orig_assembly: categorical - Original genome assembly - unique values: 1
19. orig_chr: categorical - Original chromosome - unique values: 5
20. original_ID: text - Original ID - unique values: 21
21. refseq_ID: text - RefSeq ID - unique values: 12
22. score: categorical - Score - unique values: 1, max: 1.0, mean: 1.0, min: 1.0, std: 0.0
23. source: categorical - Source of data - unique values: 1
24. type: categorical - Type of data - unique values: 1
25. current_end: Numerical - Current end position - max: 243478698.0, mean: 147448970.78, min: 107935.0, std: 68928764.23575936
26. current_start: Numerical - Current start position - max: 243469900.0, mean: 147443577.1, min: 105934.0, std: 68928148.40871745
27. disease_PMID: Numerical - PubMed ID for disease - max: 28717659.0, mean: 24755009.88, min: 16269442.0, std: 3206087.430186772
28. enh_PMID: Numerical - PubMed ID for enhancer - max: 28717659.0, mean: 24755009.88, min: 16269442.0, std: 3206087.430186772
29. orig_end: Numerical - Original end position - max: 243642000.0, mean: 147504993.26, min: 107935.0, std: 68937583.87712999
30. orig_start: Numerical - Original start position - max: 243633202.0, mean: 147499599.58, min: 105934.0, std: 68936951.6672135

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
2. crossref: GeneticElement - xsd:string
3. current_assembly: GenomicCoordinate - xsd:string
4. current_chr: Chromosome - xsd:string
5. disease: Disease - xsd:string
6. enh2gene_PMID: Publication - xsd:string
7. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
8. hgnc_symbol_target_genes: Gene - xsd:string
9. minimum_ratio: GeneticElement - xsd:float
10. mutation_PMID: Publication - xsd:string
11. orig_assembly: GenomicCoordinate - xsd:string
12. orig_chr: Chromosome - xsd:string
13. original_ID: GeneticElement - xsd:string
14. refseq_ID: Gene - xsd:string
15. score: GeneticElement - xsd:float
16. source: GeneticElement - xsd:string
17. type: GeneticElement - xsd:string
18. current_end: GenomicCoordinate - xsd:integer
19. current_start: GenomicCoordinate - xsd:integer
20. disease_PMID: Publication - xsd:integer
21. enh_PMID: Publication - xsd:integer
22. orig_end: GenomicCoordinate - xsd:integer
23. orig_start: GenomicCoordinate - xsd:integer