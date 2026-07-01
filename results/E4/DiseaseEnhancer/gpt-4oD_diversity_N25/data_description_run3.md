**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for TFs to enhancer associations - single value
2. TFs2enh_method: categorical - Method used for TFs to enhancer associations - single value
3. biosample_name: categorical - Name of the biosample - single value
4. crm_ID: text - ID for cis-regulatory module - unique values
5. crossref: categorical - Cross-reference information - single value
6. current_assembly: categorical - Current genome assembly version - single value
7. current_chr: text - Current chromosome - unique values
8. disease: text - Disease associated with the data - unique values
9. disease_method: categorical - Method used for disease association - single value
10. enh2gene_PMID: text - PubMed ID for enhancer to gene associations - unique values
11. enh2gene_method: categorical - Method used for enhancer to gene associations - single value
12. enh_method: categorical - Method used for enhancer identification - single value
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - single value
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values
15. minimum_ratio: categorical - Minimum ratio value - single value
16. mutation_PMID: text - PubMed ID for mutation information - unique values
17. mutation_method: categorical - Method used for mutation information - single value
18. orig_assembly: categorical - Original genome assembly version - single value
19. orig_chr: text - Original chromosome - unique values
20. original_ID: text - Original ID for the data - unique values
21. refseq_ID: text - RefSeq ID - unique values
22. score: categorical - Score value - two unique values
23. source: categorical - Source of the data - single value
24. type: categorical - Type of the data - single value
25. current_end: Numerical - Current end position in the genome - range from 6062837.0 to 185799612.0
26. current_start: Numerical - Current start position in the genome - range from 6032039.0 to 185781414.0
27. disease_PMID: Numerical - PubMed ID for disease information - range from 19561607.0 to 29093029.0
28. enh_PMID: Numerical - PubMed ID for enhancer information - range from 19561607.0 to 29093029.0
29. orig_end: Numerical - Original end position in the genome - range from 6104800.0 to 185517400.0
30. orig_start: Numerical - Original start position in the genome - range from 6074002.0 to 185499202.0

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
2. current_assembly: GenomicCoordinate - xsd:string
3. current_chr: GenomicCoordinate - xsd:string
4. current_end: GenomicCoordinate - xsd:decimal
5. current_start: GenomicCoordinate - xsd:decimal
6. orig_assembly: GenomicCoordinate - xsd:string
7. orig_chr: GenomicCoordinate - xsd:string
8. orig_end: GenomicCoordinate - xsd:decimal
9. orig_start: GenomicCoordinate - xsd:decimal
10. biosample_name: Biosample - xsd:string
11. disease: Disease - xsd:string
12. disease_PMID: Disease - xsd:decimal
13. enh2gene_PMID: Publication - xsd:string
14. enh_PMID: Publication - xsd:decimal
15. mutation_PMID: Publication - xsd:string
16. TFs2enh_PMID: Publication - xsd:string
17. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
18. hgnc_symbol_target_genes: Gene - xsd:string
19. minimum_ratio: GeneticElement - xsd:decimal
20. score: GeneticElement - xsd:decimal
21. source: GeneticElement - xsd:string
22. type: GeneticElement - xsd:string