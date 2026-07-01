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
3. biosample: categorical - Biosample or cell line used - single value
4. crm_ID: text - Cis-regulatory module ID - multiple values
5. crossref: categorical - Cross-reference information - single value
6. current_assembly: categorical - Current genome assembly version - single value
7. current_chr: categorical - Current chromosome - multiple values
8. disease: categorical - Associated disease - single value
9. disease_PMID: categorical - PubMed ID for disease association - single value
10. disease_method: categorical - Method used for identifying disease association - single value
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene association - multiple values
12. enh2gene_method: categorical - Method used for identifying enhancer to gene association - multiple values
13. enh_PMID: categorical - PubMed ID for enhancer - single value
14. enh_method: categorical - Method used for identifying enhancer - single value
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - single value
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - multiple values
17. minimum_ratio: categorical - Minimum ratio - single value
18. mutation_PMID: categorical - PubMed ID for mutation - single value
19. mutation_method: categorical - Method used for identifying mutation - single value
20. orig_assembly: categorical - Original genome assembly version - single value
21. orig_chr: categorical - Original chromosome - multiple values
22. original_ID: categorical - Original ID - single value
23. refsnp_ID: categorical - Reference SNP ID - single value
24. score: categorical - Score - single value
25. source: categorical - Source of data - single value
26. type: categorical - Type of data - single value
27. current_end: Numerical - Current end position in the genome - range from 1069606.0 to 159102934.0
28. current_start: Numerical - Current start position in the genome - range from 1069266.0 to 159102636.0
29. orig_end: Numerical - Original end position in the genome - range from 1004986.0 to 159523966.0
30. orig_start: Numerical - Original start position in the genome - range from 1004646.0 to 159523668.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Method
6. Publication
7. TranscriptionFactor
8. TargetGene

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. identifiedByMethod: GeneticElement - Method
5. referencedInPublication: GeneticElement - Publication
6. regulatesTranscriptionFactor: GeneticElement - TranscriptionFactor
7. targetsGene: GeneticElement - TargetGene

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
10. biosample: Biosample - xsd:string
11. disease: Disease - xsd:string
12. disease_PMID: Disease - xsd:string
13. disease_method: Method - xsd:string
14. enh2gene_PMID: Publication - xsd:string
15. enh2gene_method: Method - xsd:string
16. enh_PMID: Publication - xsd:string
17. enh_method: Method - xsd:string
18. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
19. hgnc_symbol_target_genes: TargetGene - xsd:string
20. minimum_ratio: GeneticElement - xsd:decimal
21. mutation_PMID: Publication - xsd:string
22. mutation_method: Method - xsd:string
23. original_ID: GeneticElement - xsd:string
24. refsnp_ID: GeneticElement - xsd:string
25. score: GeneticElement - xsd:decimal
26. source: GeneticElement - xsd:string
27. type: GeneticElement - xsd:string