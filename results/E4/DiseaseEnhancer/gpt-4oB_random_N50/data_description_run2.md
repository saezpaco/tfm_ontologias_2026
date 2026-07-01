**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer mapping - unique
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer mapping - unique
3. biosample_name: categorical - Name of the biosample or cell line - unique
4. crm_ID: text - Identifier for cis-regulatory module - unique
5. crossref: categorical - Cross-reference information - unique
6. current_assembly: categorical - Current genome assembly version - unique
7. current_chr: text - Current chromosome - unique
8. disease: text - Disease associated with the data - unique
9. disease_method: categorical - Method used for disease association - unique
10. enh2gene_method: categorical - Method used for enhancer to gene mapping - unique
11. enh_method: categorical - Method used for enhancer identification - unique
12. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - unique
13. hgnc_symbol_target_genes: text - HGNC symbol for target genes - unique
14. minimum_ratio: categorical - Minimum ratio value - 0.95
15. mutation_PMID: text - PubMed ID for mutation information - unique
16. mutation_method: categorical - Method used for mutation identification - unique
17. orig_assembly: categorical - Original genome assembly version - unique
18. orig_chr: text - Original chromosome - unique
19. original_ID: text - Original identifier - unique
20. refseq_ID: text - RefSeq identifier - unique
21. score: categorical - Score value - 1.0
22. source: categorical - Source of the data - unique
23. type: categorical - Type of data - unique
24. current_end: Numerical - Current end position in the genome - range: 2137970.0 to 188083612.0
25. current_start: Numerical - Current start position in the genome - range: 2136972.0 to 188081014.0
26. disease_PMID: Numerical - PubMed ID for disease information - range: 19543368.0 to 29093029.0
27. enh2gene_PMID: Numerical - PubMed ID for enhancer to gene mapping - range: 19543368.0 to 29093029.0
28. enh_PMID: Numerical - PubMed ID for enhancer information - range: 19543368.0 to 29093029.0
29. orig_end: Numerical - Original end position in the genome - range: 2159200.0 to 187801400.0
30. orig_start: Numerical - Original start position in the genome - range: 2158202.0 to 187798802.0

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
3. CisRegulatoryModule: subclass of -> GeneticElement

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
4. crm_ID: CisRegulatoryModule - xsd:string
5. crossref: GeneticElement - xsd:string
6. current_assembly: GenomicCoordinate - xsd:string
7. current_chr: GenomicCoordinate - xsd:string
8. disease: Disease - xsd:string
9. disease_method: Disease - xsd:string
10. enh2gene_method: GeneticElement - xsd:string
11. enh_method: GeneticElement - xsd:string
12. hgnc_symbol_TFs: TranscriptionFactor - xsd:string
13. hgnc_symbol_target_genes: Gene - xsd:string
14. minimum_ratio: GeneticElement - xsd:float
15. mutation_PMID: GeneticElement - xsd:string
16. mutation_method: GeneticElement - xsd:string
17. orig_assembly: GenomicCoordinate - xsd:string
18. orig_chr: GenomicCoordinate - xsd:string
19. original_ID: GeneticElement - xsd:string
20. refseq_ID: Gene - xsd:string
21. score: GeneticElement - xsd:float
22. source: GeneticElement - xsd:string
23. type: GeneticElement - xsd:string
24. current_end: GenomicCoordinate - xsd:float
25. current_start: GenomicCoordinate - xsd:float
26. disease_PMID: Disease - xsd:float
27. enh2gene_PMID: GeneticElement - xsd:float
28. enh_PMID: GeneticElement - xsd:float
29. orig_end: GenomicCoordinate - xsd:float
30. orig_start: GenomicCoordinate - xsd:float