**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. TFs2enh_PMID: type - PubMed ID for transcription factor to enhancer relationship - string
2. TFs2enh_method: type - method used in transcription factor to enhancer relationship - string
3. biosample_name: type - name of the cell line or biosample - string
4. crm_ID: type - ID of the CRISPR/Cas9 target region - string
5. crossref: type - reference for the data - string
6. current_assembly: type - assembly version of the genome - string
7. current_chr: type - chromosome number - integer
8. current_end: type - end position of the genomic feature - integer
9. current_start: type - start position of the genomic feature - integer
10. disease: type - name of the disease associated with the data - string
11. disease_PMID: type - PubMed ID for disease information - string
12. disease_method: type - method used in disease association - string
13. enh2gene_PMID: type - PubMed ID for enhancer to gene relationship - string
14. enh2gene_method: type - method used in enhancer to gene relationship - string
15. enh_PMID: type - PubMed ID for enhancer information - string
16. enh_method: type - method used in enhancer analysis - string
17. hgnc_symbol_TFs: type - HGNC symbol of the transcription factors - string
18. hgnc_symbol_target_genes: type - HGNC symbols of target genes - string
19. minimum_ratio: type - minimum ratio value - float
20. mutation_PMID: type - PubMed ID for mutation information - string
21. mutation_method: type - method used in mutation analysis - string
22. orig_assembly: type - original assembly version of the genome - string
23. orig_chr: type - chromosome number from the original assembly - integer
24. orig_end: type - end position of the genomic feature from the original assembly - integer
25. orig_start: type - start position of the genomic feature from the original assembly - integer
26. original_ID: type - ID of the original data - string
27. refsnp_ID: type - RSID for the genetic variation - string
28. score: type - score value - float
29. source: type - source of the data - string
30. type: type - type of the genomic feature - string

**Classes:**
1. class_entity

**Subclasses:**
1. entity_name: subclass of -> class_entity

**Object Properties:**
1. has_transcription_factor_to_enhancer_relationship: domain - TFs2enh_PMID, range - transcription_factor
2. has_method_for_transcription_factor_to_enhancer_relationship: domain - TFs2enh_method, range - method
3. has_biosample: domain - biosample_name, range - biosample
4. has_CRISPR_Cas9_target_region_ID: domain - crm_ID, range - CRISPR_Cas9_target_region
5. has_cross_reference: domain - crossref, range - reference
6. has_assembly_version: domain - current_assembly, range - assembly_version
7. has_chromosome_number: domain - current_chr, range - chromosome_number
8. has_end_position: domain - current_end, range - end_position
9. has_start_position: domain - current_start, range - start_position
10. has_disease_association: domain - disease, range - disease
11. has_disease_PMID: domain - disease_PMID, range - disease_PMID
12. has_method_for_disease_association: domain - disease_method, range - method
13. has_enhancer_to_gene_relationship: domain - enh2gene_PMID, range - gene
14. has_method_for_enhancer_to_gene_relationship: domain - enh2gene_method, range - method
15. has_enhancer_information: domain - enh_PMID, range - enhancer
16. has_method_for_enhancer_analysis: domain - enh_method, range - method
17. has_transcription_factor_symbol: domain - hgnc_symbol_TFs, range - transcription_factor_symbol
18. has_target_gene_symbols: domain - hgnc_symbol_target_genes, range - gene_symbol
19. has_minimum_ratio: domain - minimum_ratio, range - ratio
20. has_mutation_information: domain - mutation_PMID, range - mutation
21. has_method_for_mutation_analysis: domain - mutation_method, range - method
22. has_original_assembly_version: domain - orig_assembly, range - assembly_version
23. has_original_chromosome_number: domain - orig_chr, range - chromosome_number
24. has_original_end_position: domain - orig_end, range - end_position
25. has_original_start_position: domain - orig_start, range - start_position
26. has_original_ID: domain - original_ID, range - ID
27. has_RSID: domain - refsnp_ID, range - RSID
28. has_score: domain - score, range - score_value
29. has_source: domain - source, range - source_of_data
30. has_type_of_genomic_feature: domain - type, range - genomic_feature_type

**Data Type Properties:**
1. PubMed_ID: domain - TFs2enh_PMID, disease_PMID, enh2gene_PMID, enh_PMID, mutation_PMID, refsnp_ID, original_ID, crm_ID, crossref, source, type, score
2. Method: domain - TFs2enh_method, disease_method, enh2gene_method, enh_method, mutation_method, source, type
3. String: domain - biosample_name, hgnc_symbol_TFs, hgnc_symbol_target_genes, disease, crm_ID, crossref, original_ID, refsnp_ID, source, type
4. Integer: domain - current_chr, orig_chr, current_end, current_start, orig_end, orig_start
5. Float: domain - minimum_ratio, score