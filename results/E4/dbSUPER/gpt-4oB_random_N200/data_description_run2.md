**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. TFs2enh_PMID: categorical - PubMed ID for transcription factors to enhancer associations - [single value]
2. TFs2enh_method: categorical - Method used for transcription factors to enhancer associations - [single value]
3. biosample_name: text - Name of the biosample or cell line - [82 unique values]
4. crm_ID: text - Cis-regulatory module ID - [200 unique values]
5. crossref: text - Cross-reference ID - [200 unique values]
6. current_assembly: categorical - Current genome assembly version - [single value]
7. current_chr: text - Current chromosome - [23 unique values]
8. disease: categorical - Disease associated with the data - [single value]
9. disease_PMID: categorical - PubMed ID for disease associations - [single value]
10. disease_method: categorical - Method used for disease associations - [single value]
11. enh2gene_PMID: categorical - PubMed ID for enhancer to gene associations - [8 unique values]
12. enh2gene_method: categorical - Method used for enhancer to gene associations - [2 unique values]
13. enh_PMID: categorical - PubMed ID for enhancer data - [7 unique values]
14. enh_method: categorical - Method used for enhancer data - [3 unique values]
15. hgnc_symbol_TFs: categorical - HGNC symbol for transcription factors - [single value]
16. hgnc_symbol_target_genes: text - HGNC symbol for target genes - [191 unique values]
17. minimum_ratio: categorical - Minimum ratio value - [single value]
18. mutation_PMID: categorical - PubMed ID for mutation data - [single value]
19. mutation_method: categorical - Method used for mutation data - [single value]
20. orig_assembly: categorical - Original genome assembly version - [single value]
21. orig_chr: text - Original chromosome - [23 unique values]
22. original_ID: text - Original ID - [200 unique values]
23. refsnp_ID: categorical - Reference SNP ID - [single value]
24. score: categorical - Score value - [5 unique values]
25. source: categorical - Source of the data - [single value]
26. type: categorical - Type of data - [single value]
27. current_end: Numerical - Current end position in the genome - [range: 283173.0 to 248646628.0]
28. current_start: Numerical - Current start position in the genome - [range: 237486.0 to 248640408.0]
29. orig_end: Numerical - Original end position in the genome - [range: 283173.0 to 248809929.0]
30. orig_start: Numerical - Original start position in the genome - [range: 237486.0 to 248803709.0]

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. Biosample
4. Disease
5. Publication
6. Method
7. Gene
8. TranscriptionFactor

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement
3. CisRegulatoryModule: subclass of -> GeneticElement
4. SNP: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithBiosample: GeneticElement - Biosample
3. associatedWithDisease: GeneticElement - Disease
4. hasPublication: GeneticElement - Publication
5. usesMethod: GeneticElement - Method
6. targetsGene: GeneticElement - Gene
7. regulatedByTF: GeneticElement - TranscriptionFactor

**Data Type Properties:**
1. biosampleName: Biosample - xsd:string
2. crmID: CisRegulatoryModule - xsd:string
3. crossrefID: GeneticElement - xsd:string
4. currentAssembly: GenomicCoordinate - xsd:string
5. currentChr: GenomicCoordinate - xsd:string
6. diseaseName: Disease - xsd:string
7. diseasePMID: Disease - xsd:string
8. diseaseMethod: Disease - xsd:string
9. enh2genePMID: Publication - xsd:string
10. enh2geneMethod: Method - xsd:string
11. enhPMID: Publication - xsd:string
12. enhMethod: Method - xsd:string
13. hgncSymbolTFs: TranscriptionFactor - xsd:string
14. hgncSymbolTargetGenes: Gene - xsd:string
15. minimumRatio: GeneticElement - xsd:float
16. mutationPMID: Publication - xsd:string
17. mutationMethod: Method - xsd:string
18. origAssembly: GenomicCoordinate - xsd:string
19. origChr: GenomicCoordinate - xsd:string
20. originalID: GeneticElement - xsd:string
21. refsnpID: SNP - xsd:string
22. score: GeneticElement - xsd:float
23. source: GeneticElement - xsd:string
24. type: GeneticElement - xsd:string
25. currentEnd: GenomicCoordinate - xsd:integer
26. currentStart: GenomicCoordinate - xsd:integer
27. origEnd: GenomicCoordinate - xsd:integer
28. origStart: GenomicCoordinate - xsd:integer