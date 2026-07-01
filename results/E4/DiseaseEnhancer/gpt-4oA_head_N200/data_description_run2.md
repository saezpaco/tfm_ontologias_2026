**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PMID for transcription factors to enhancer associations - unique_count: 1
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer associations - unique_count: 1
3. biosample_name: categorical - Name of the biosample - unique_count: 1
4. crm_ID: text - ID for cis-regulatory module - unique_count: 41
5. crossref: categorical - Cross-reference information - unique_count: 1
6. current_assembly: categorical - Current genome assembly version - unique_count: 1
7. current_chr: categorical - Current chromosome - unique_count: 5
8. disease: text - Disease associated with the data - unique_count: 49
9. disease_method: categorical - Method used for disease association - unique_count: 1
10. enh2gene_PMID: text - PMID for enhancer to gene associations - unique_count: 40
11. enh2gene_method: categorical - Method used for enhancer to gene associations - unique_count: 1
12. enh_method: categorical - Method used for enhancer identification - unique_count: 1
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique_count: 1
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique_count: 29
15. minimum_ratio: categorical - Minimum ratio value - unique_count: 1, count: 200, max: 0.95, mean: 0.95, min: 0.95, std: 0.0
16. mutation_PMID: text - PMID for mutation information - unique_count: 31
17. mutation_method: categorical - Method used for mutation information - unique_count: 1
18. orig_assembly: categorical - Original genome assembly version - unique_count: 1
19. orig_chr: categorical - Original chromosome - unique_count: 5
20. original_ID: text - Original ID for the data - unique_count: 46
21. refseq_ID: text - RefSeq ID for the data - unique_count: 35
22. score: categorical - Score value - unique_count: 1, count: 200, max: 1.0, mean: 1.0, min: 1.0, std: 0.0
23. source: categorical - Source of the data - unique_count: 1
24. type: categorical - Type of the data - unique_count: 1
25. current_end: Numerical - Current end position in the genome - count: 200, max: 243478698.0, mean: 90268822.485, min: 107935.0, std: 65091893.88859966
26. current_start: Numerical - Current start position in the genome - count: 200, max: 243469900.0, mean: 90260653.615, min: 105934.0, std: 65093484.200071655
27. disease_PMID: Numerical - PMID for disease information - count: 200, max: 28854172.0, mean: 24680664.115, min: 16269442.0, std: 3028518.180970768
28. enh_PMID: Numerical - PMID for enhancer information - count: 200, max: 28854172.0, mean: 24680664.115, min: 16269442.0, std: 3028518.180970768
29. orig_end: Numerical - Original end position in the genome - count: 200, max: 243642000.0, mean: 90934790.945, min: 107935.0, std: 65269026.93902713
30. orig_start: Numerical - Original start position in the genome - count: 200, max: 243633202.0, mean: 90926622.075, min: 105934.0, std: 65270605.62114296

**classes:**
1. GeneticRegulatoryElement
2. GenomicCoordinate
3. Biosample
4. Gene
5. TranscriptionFactor
6. Disease

**subclasses:**
1. Enhancer: subclass of -> GeneticRegulatoryElement
2. SuperEnhancer: subclass of -> GeneticRegulatoryElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticRegulatoryElement - GenomicCoordinate
2. associatedWithBiosample: GeneticRegulatoryElement - Biosample
3. targetsGene: GeneticRegulatoryElement - Gene
4. regulatedByTF: GeneticRegulatoryElement - TranscriptionFactor
5. associatedWithDisease: GeneticRegulatoryElement - Disease

**Data Type Properties:**
1. TFs2enh_PMID: GeneticRegulatoryElement - xsd:string
2. TFs2enh_method: GeneticRegulatoryElement - xsd:string
3. biosample_name: Biosample - xsd:string
4. crm_ID: GeneticRegulatoryElement - xsd:string
5. crossref: GeneticRegulatoryElement - xsd:string
6. current_assembly: GenomicCoordinate - xsd:string
7. current_chr: GenomicCoordinate - xsd:string
8. disease: Disease - xsd:string
9. disease_method: Disease - xsd:string
10. enh2gene_PMID: GeneticRegulatoryElement - xsd:string
11. enh2gene_method: GeneticRegulatoryElement - xsd:string
12. enh_method: GeneticRegulatoryElement - xsd:string
13. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
14. hgnc_symbol_target_genes: Gene - xsd:string
15. minimum_ratio: GeneticRegulatoryElement - xsd:float
16. mutation_PMID: GeneticRegulatoryElement - xsd:string
17. mutation_method: GeneticRegulatoryElement - xsd:string
18. orig_assembly: GenomicCoordinate - xsd:string
19. orig_chr: GenomicCoordinate - xsd:string
20. original_ID: GeneticRegulatoryElement - xsd:string
21. refseq_ID: GeneticRegulatoryElement - xsd:string
22. score: GeneticRegulatoryElement - xsd:float
23. source: GeneticRegulatoryElement - xsd:string
24. type: GeneticRegulatoryElement - xsd:string
25. current_end: GenomicCoordinate - xsd:integer
26. current_start: GenomicCoordinate - xsd:integer
27. disease_PMID: Disease - xsd:integer
28. enh_PMID: GeneticRegulatoryElement - xsd:integer
29. orig_end: GenomicCoordinate - xsd:integer
30. orig_start: GenomicCoordinate - xsd:integer