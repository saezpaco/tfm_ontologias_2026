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
4. crm_ID: text - Unique identifier for cis-regulatory module - unique values
5. crossref: categorical - Cross-reference information - single value
6. current_assembly: categorical - Current genome assembly version - single value
7. current_chr: text - Current chromosome identifier - unique values
8. disease: text - Disease associated with the data - unique values
9. disease_method: categorical - Method used for disease association - single value
10. enh2gene_PMID: text - PubMed ID for enhancer to gene mapping - unique values
11. enh2gene_method: categorical - Method used for enhancer to gene mapping - single value
12. enh_method: categorical - Method used for enhancer identification - single value
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - single value
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values
15. minimum_ratio: categorical - Minimum ratio value - single value
16. mutation_PMID: text - PubMed ID for mutation information - unique values
17. mutation_method: categorical - Method used for mutation identification - single value
18. orig_assembly: categorical - Original genome assembly version - single value
19. orig_chr: text - Original chromosome identifier - unique values
20. original_ID: text - Original identifier - unique values
21. refseq_ID: text - RefSeq identifier - unique values
22. score: categorical - Score value - two unique values
23. source: categorical - Source of the data - single value
24. type: categorical - Type of the data - single value
25. current_end: Numerical - End position in the current genome assembly - range: 6062837.0 to 185799612.0
26. current_start: Numerical - Start position in the current genome assembly - range: 6032039.0 to 185781414.0
27. disease_PMID: Numerical - PubMed ID for disease information - range: 19561607.0 to 29093029.0
28. enh_PMID: Numerical - PubMed ID for enhancer information - range: 19561607.0 to 29093029.0
29. orig_end: Numerical - End position in the original genome assembly - range: 6104800.0 to 185517400.0
30. orig_start: Numerical - Start position in the original genome assembly - range: 6074002.0 to 185499202.0

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
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. crm_ID: CisRegulatoryModule - xsd:string
2. current_chr: GenomicCoordinate - xsd:string
3. current_end: GenomicCoordinate - xsd:decimal
4. current_start: GenomicCoordinate - xsd:decimal
5. orig_chr: GenomicCoordinate - xsd:string
6. orig_end: GenomicCoordinate - xsd:decimal
7. orig_start: GenomicCoordinate - xsd:decimal
8. biosample_name: Biosample - xsd:string
9. disease: Disease - xsd:string
10. hgnc_symbol_target_genes: Gene - xsd:string
11. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
12. TFs2enh_PMID: Publication - xsd:string
13. enh2gene_PMID: Publication - xsd:string
14. mutation_PMID: Publication - xsd:string
15. disease_PMID: Publication - xsd:decimal
16. enh_PMID: Publication - xsd:decimal
17. score: GeneticElement - xsd:decimal
18. minimum_ratio: GeneticElement - xsd:decimal
19. source: GeneticElement - xsd:string
20. type: GeneticElement - xsd:string
21. current_assembly: GenomicCoordinate - xsd:string
22. orig_assembly: GenomicCoordinate - xsd:string
23. crossref: GeneticElement - xsd:string
24. original_ID: GeneticElement - xsd:string
25. refseq_ID: Gene - xsd:string