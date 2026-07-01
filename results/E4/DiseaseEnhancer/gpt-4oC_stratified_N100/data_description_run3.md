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
4. crm_ID: text - Identifier for cis-regulatory modules - 82 unique values
5. crossref: categorical - Cross-reference information - unique
6. current_assembly: categorical - Current genome assembly version - unique
7. current_chr: text - Current chromosome - 23 unique values
8. disease: text - Disease associated with the data - 43 unique values
9. disease_method: categorical - Method used for identifying disease associations - unique
10. enh2gene_PMID: text - PubMed ID for enhancer to gene associations - 35 unique values
11. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - unique
12. enh_method: categorical - Method used for identifying enhancers - unique
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - 83 unique values
15. minimum_ratio: categorical - Minimum ratio value - 0.95
16. mutation_PMID: text - PubMed ID for mutation information - 29 unique values
17. mutation_method: categorical - Method used for identifying mutations - unique
18. orig_assembly: categorical - Original genome assembly version - unique
19. orig_chr: text - Original chromosome - 23 unique values
20. original_ID: text - Original identifier - 87 unique values
21. refseq_ID: text - RefSeq identifier - 47 unique values
22. score: categorical - Score value - 1.0
23. source: categorical - Source of the data - unique
24. type: categorical - Type of data - unique
25. current_end: Numerical - End position in the current genome assembly - 635800 to 188069612
26. current_start: Numerical - Start position in the current genome assembly - 613202 to 188069414
27. disease_PMID: Numerical - PubMed ID for disease information - 19306335 to 29093029
28. enh_PMID: Numerical - PubMed ID for enhancer information - 19306335 to 29093029
29. orig_end: Numerical - End position in the original genome assembly - 685800 to 187787400
30. orig_start: Numerical - Start position in the original genome assembly - 663202 to 187787202

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Gene
5. TranscriptionFactor
6. Disease

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. Mutation: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. targetsGene: GeneticElement - Gene
4. regulatedByTF: GeneticElement - TranscriptionFactor
5. associatedWithDisease: GeneticElement - Disease

**Data Type Properties:**
1. TFs2enh_PMID: GeneticElement - xsd:string
2. TFs2enh_method: GeneticElement - xsd:string
3. biosample_name: Biosample - xsd:string
4. crm_ID: GeneticElement - xsd:string
5. crossref: GeneticElement - xsd:string
6. current_assembly: GenomicCoordinate - xsd:string
7. current_chr: GenomicCoordinate - xsd:string
8. disease: Disease - xsd:string
9. disease_method: Disease - xsd:string
10. enh2gene_PMID: GeneticElement - xsd:string
11. enh2gene_method: GeneticElement - xsd:string
12. enh_method: GeneticElement - xsd:string
13. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
14. hgnc_symbol_target_genes: Gene - xsd:string
15. minimum_ratio: GeneticElement - xsd:float
16. mutation_PMID: Mutation - xsd:string
17. mutation_method: Mutation - xsd:string
18. orig_assembly: GenomicCoordinate - xsd:string
19. orig_chr: GenomicCoordinate - xsd:string
20. original_ID: GeneticElement - xsd:string
21. refseq_ID: Gene - xsd:string
22. score: GeneticElement - xsd:float
23. source: GeneticElement - xsd:string
24. type: GeneticElement - xsd:string
25. current_end: GenomicCoordinate - xsd:integer
26. current_start: GenomicCoordinate - xsd:integer
27. disease_PMID: Disease - xsd:integer
28. enh_PMID: GeneticElement - xsd:integer
29. orig_end: GenomicCoordinate - xsd:integer
30. orig_start: GenomicCoordinate - xsd:integer