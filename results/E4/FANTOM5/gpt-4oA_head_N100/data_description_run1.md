**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - categorical
2. TFs2enh_method: categorical - Method used for identifying transcription factors to enhancer associations - categorical
3. biosample: categorical - Biological sample or cell line - categorical
4. crm_ID: text - Cis-regulatory module ID - text
5. crossref: categorical - Cross-reference information - categorical
6. current_assembly: categorical - Current genome assembly version - categorical
7. current_chr: categorical - Current chromosome - categorical
8. disease: categorical - Associated disease - categorical
9. disease_PMID: categorical - PubMed ID for disease association - categorical
10. disease_method: categorical - Method used for identifying disease association - categorical
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - categorical
12. enh2gene_method: categorical - Method used for identifying enhancer to gene associations - categorical
13. enh_PMID: categorical - PubMed ID for enhancer information - categorical
14. enh_method: categorical - Method used for identifying enhancers - categorical
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - categorical
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - text
17. minimum_ratio: categorical - Minimum ratio for some measurement - categorical
18. mutation_PMID: categorical - PubMed ID for mutation information - categorical
19. mutation_method: categorical - Method used for identifying mutations - categorical
20. orig_assembly: categorical - Original genome assembly version - categorical
21. orig_chr: categorical - Original chromosome - categorical
22. original_ID: categorical - Original ID - categorical
23. refsnp_ID: categorical - Reference SNP ID - categorical
24. score: categorical - Score for some measurement - categorical
25. source: categorical - Source of the data - categorical
26. type: categorical - Type of data - categorical
27. current_end: Numerical - End position in the current genome assembly - Numerical
28. current_start: Numerical - Start position in the current genome assembly - Numerical
29. orig_end: Numerical - End position in the original genome assembly - Numerical
30. orig_start: Numerical - Start position in the original genome assembly - Numerical

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. BiologicalSample
4. Disease
5. Publication
6. Method
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
5. foundInSample: GeneticElement - BiologicalSample
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. crm_ID: CisRegulatoryModule - xsd:string
2. current_assembly: GenomicCoordinate - xsd:string
3. current_chr: GenomicCoordinate - xsd:string
4. current_end: GenomicCoordinate - xsd:integer
5. current_start: GenomicCoordinate - xsd:integer
6. orig_assembly: GenomicCoordinate - xsd:string
7. orig_chr: GenomicCoordinate - xsd:string
8. orig_end: GenomicCoordinate - xsd:integer
9. orig_start: GenomicCoordinate - xsd:integer
10. biosample: BiologicalSample - xsd:string
11. disease: Disease - xsd:string
12. disease_PMID: Disease - xsd:string
13. enh2gene_PMID: Publication - xsd:string
14. enh2gene_method: Method - xsd:string
15. enh_PMID: Publication - xsd:string
16. enh_method: Method - xsd:string
17. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
18. hgnc_symbol_target_genes: Gene - xsd:string
19. minimum_ratio: GeneticElement - xsd:float
20. mutation_PMID: Publication - xsd:string
21. mutation_method: Method - xsd:string
22. original_ID: GeneticElement - xsd:string
23. refsnp_ID: GeneticElement - xsd:string
24. score: GeneticElement - xsd:float
25. source: GeneticElement - xsd:string
26. type: GeneticElement - xsd:string