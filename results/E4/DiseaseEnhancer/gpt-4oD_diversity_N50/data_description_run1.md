**Foundational Prefix:**
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:skos="http://www.w3.org/2004/02/skos/core#"
         xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:base="https://base_ontology.com#">

<owl:Ontology rdf:about="https://base_ontology.com#"/>

**Data Description:**
1. TFs2enh_PMID: categorical - PMID for transcription factors to enhancer - unique
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer - unique
3. biosample_name: categorical - Name of the biosample - unique
4. crm_ID: text - ID for cis-regulatory module - unique
5. crossref: categorical - Cross-reference information - unique
6. current_assembly: categorical - Current genome assembly - unique
7. current_chr: text - Current chromosome - unique
8. disease: text - Disease associated - unique
9. disease_method: categorical - Method used for disease association - unique
10. enh2gene_PMID: text - PMID for enhancer to gene - unique
11. enh2gene_method: categorical - Method used for enhancer to gene - unique
12. enh_method: categorical - Method used for enhancer identification - unique
13. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique
14. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique
15. minimum_ratio: categorical - Minimum ratio - 0.95
16. mutation_PMID: text - PMID for mutation - unique
17. mutation_method: categorical - Method used for mutation - unique
18. orig_assembly: categorical - Original genome assembly - unique
19. orig_chr: text - Original chromosome - unique
20. original_ID: text - Original ID - unique
21. refseq_ID: text - RefSeq ID - unique
22. score: categorical - Score - range: 0.9687451164 to 1.0
23. source: categorical - Source of data - unique
24. type: categorical - Type of data - unique
25. current_end: Numerical - Current end position - range: 1287401.0 to 185799612.0
26. current_start: Numerical - Current start position - range: 1285401.0 to 185781414.0
27. disease_PMID: Numerical - PMID for disease - range: 18194515.0 to 29093029.0
28. enh_PMID: Numerical - PMID for enhancer - range: 18194515.0 to 29093029.0
29. orig_end: Numerical - Original end position - range: 1287516.0 to 185517400.0
30. orig_start: Numerical - Original start position - range: 1285516.0 to 185499202.0

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

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. hasBiosample: GeneticElement - Biosample
3. targetsGene: GeneticElement - Gene
4. regulatedBy: GeneticElement - TranscriptionFactor
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
16. mutation_PMID: GeneticElement - xsd:string
17. mutation_method: GeneticElement - xsd:string
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