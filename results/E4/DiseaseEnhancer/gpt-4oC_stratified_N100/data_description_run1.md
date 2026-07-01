**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer - single value
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer - single value
3. biosample_name: categorical - Name of the biosample - single value
4. crm_ID: text - ID for cis-regulatory module - unique values
5. crossref: categorical - Cross-reference information - single value
6. current_assembly: categorical - Current genome assembly version - single value
7. current_chr: text - Current chromosome - unique values
8. disease: text - Disease associated - unique values
9. disease_method: categorical - Method used for identifying disease association - single value
10. enh2gene_PMID: text - PubMed ID for enhancer to gene - unique values
11. enh2gene_method: categorical - Method used for identifying enhancer to gene - single value
12. enh_method: categorical - Method used for identifying enhancer - single value
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - single value
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique values
15. minimum_ratio: categorical - Minimum ratio - single value
16. mutation_PMID: text - PubMed ID for mutation - unique values
17. mutation_method: categorical - Method used for identifying mutation - single value
18. orig_assembly: categorical - Original genome assembly version - single value
19. orig_chr: text - Original chromosome - unique values
20. original_ID: text - Original ID - unique values
21. refseq_ID: text - RefSeq ID - unique values
22. score: categorical - Score - single value
23. source: categorical - Source of the data - single value
24. type: categorical - Type of the data - single value
25. current_end: Numerical - Current end position in the genome - range from 635800.0 to 188069612.0
26. current_start: Numerical - Current start position in the genome - range from 613202.0 to 188069414.0
27. disease_PMID: Numerical - PubMed ID for disease - range from 19306335.0 to 29093029.0
28. enh_PMID: Numerical - PubMed ID for enhancer - range from 19306335.0 to 29093029.0
29. orig_end: Numerical - Original end position in the genome - range from 685800.0 to 187787400.0
30. orig_start: Numerical - Original start position in the genome - range from 663202.0 to 187787202.0

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
2. associatedWithDisease: GeneticElement - Disease
3. identifiedByMethod: GeneticElement - Method
4. hasPublication: GeneticElement - Publication
5. hasBiosample: GeneticElement - Biosample
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. crm_ID: CisRegulatoryModule - xsd:string
2. current_assembly: GenomicCoordinate - xsd:string
3. current_chr: GenomicCoordinate - xsd:string
4. current_end: GenomicCoordinate - xsd:decimal
5. current_start: GenomicCoordinate - xsd:decimal
6. disease: Disease - xsd:string
7. disease_PMID: Disease - xsd:decimal
8. enh2gene_PMID: Publication - xsd:string
9. enh_PMID: Publication - xsd:decimal
10. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
11. hgnc_symbol_target_genes: Gene - xsd:string
12. minimum_ratio: GeneticElement - xsd:decimal
13. mutation_PMID: Publication - xsd:string
14. orig_assembly: GenomicCoordinate - xsd:string
15. orig_chr: GenomicCoordinate - xsd:string
16. orig_end: GenomicCoordinate - xsd:decimal
17. orig_start: GenomicCoordinate - xsd:decimal
18. original_ID: GeneticElement - xsd:string
19. refseq_ID: Gene - xsd:string
20. score: GeneticElement - xsd:decimal
21. source: GeneticElement - xsd:string
22. type: GeneticElement - xsd:string