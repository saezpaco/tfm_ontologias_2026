**Foundational Prefix:**
https://base_ontology.com#, http://www.w3.org/1999/02/22-rdf-syntax-ns#, http://www.w3.org/2000/01/rdf-schema#, http://www.w3.org/2004/02/skos/core#, http://www.w3.org/2001/XMLSchema# and http://www.w3.org/2002/07/owl#

**Data Description:**

1. TFs2enh_PMID
   - type: categorical
   - short description: Transcription Factors to Enhancers PMID
   - possible range: [PMID]

2. TFs2enh_method
   - type: categorical
   - short description: Transcription Factors to Enhancers Method
   - possible range: [Method]

3. biosample_name
   - type: categorical
   - short description: Biosample Name
   - possible range: [Name]

4. crm_ID
   - type: text
   - short description: CRM ID
   - possible range: [ID]

5. crossref
   - type: categorical
   - short description: Cross Reference
   - possible range: [Reference]

6. current_assembly
   - type: categorical
   - short description: Current Assembly
   - possible range: [Assembly]

7. current_chr
   - type: text
   - short description: Current Chromosome
   - possible range: [Chromosome]

8. disease
   - type: text
   - short description: Disease Name
   - possible range: [Name]

9. disease_method
   - type: categorical
   - short description: Disease Method
   - possible range: [Method]

10. enh2gene_PMID
    - type: text
    - short description: Enhancer to Gene PMID
    - possible range: [PMID]

11. enh2gene_method
    - type: categorical
    - short description: Enhancer to Gene Method
    - possible range: [Method]

12. enh_method
    - type: categorical
    - short description: Enhancer Method
    - possible range: [Method]

13. hgnc_symbol_TFs
    - type: categorical
    - short description: HGNC Symbol Transcription Factors
    - possible range: [Symbol]

14. hgnc_symbol_target_genes
    - type: text
    - short description: HGNC Symbol Target Genes
    - possible range: [Symbol]

15. minimum_ratio
    - type: categorical
    - short description: Minimum Ratio
    - possible range: [Ratio]

16. mutation_PMID
    - type: text
    - short description: Mutation PMID
    - possible range: [PMID]

17. mutation_method
    - type: categorical
    - short description: Mutation Method
    - possible range: [Method]

18. orig_assembly
    - type: categorical
    - short description: Original Assembly
    - possible range: [Assembly]

19. orig_chr
    - type: text
    - short description: Original Chromosome
    - possible range: [Chromosome]

20. original_ID
    - type: text
    - short description: Original ID
    - possible range: [ID]

21. refseq_ID
    - type: text
    - short description: RefSeq ID
    - possible range: [ID]

22. score
    - type: categorical
    - short description: Score
    - possible range: [Score]

23. source
    - type: categorical
    - short description: Source
    - possible range: [Source]

24. type
    - type: categorical
    - short description: Type
    - possible range: [Type]

25. current_end
    - type: Numerical
    - short description: Current End Coordinate
    - possible range: [Coordinate]

26. current_start
    - type: Numerical
    - short description: Current Start Coordinate
    - possible range: [Coordinate]

27. disease_PMID
    - type: Numerical
    - short description: Disease PMID
    - possible range: [PMID]

28. enh_PMID
    - type: Numerical
    - short description: Enhancer PMID
    - possible range: [PMID]

29. orig_end
    - type: Numerical
    - short description: Original End Coordinate
    - possible range: [Coordinate]

30. orig_start
    - type: Numerical
    - short description: Original Start Coordinate
    - possible range: [Coordinate]

**classes:**

1. class_entity

**subclasses:**

1. entity_name: subclass of -> class_entity

**Object Properties:**

For each class and subclass enumerate its corresponding object properties:

1. has_PMID: domain - class_entity, range - [PMID]
2. has_method: domain - class_entity, range - [Method]
3. has_biosample: domain - class_entity, range - [Biosample]
4. has_crm_ID: domain - class_entity, range - [ID]
5. has_crossref: domain - class_entity, range - [Reference]
6. has_current_assembly: domain - class_entity, range - [Assembly]
7. has_current_chr: domain - class_entity, range - [Chromosome]
8. has_disease: domain - class_entity, range - [Disease]
9. has_disease_method: domain - class_entity, range - [Method]
10. has_enh2gene_PMID: domain - class_entity, range - [PMID]
11. has_enh2gene_method: domain - class_entity, range - [Method]
12. has_enh_method: domain - class_entity, range - [Method]
13. has_hgnc_symbol_TFs: domain - class_entity, range - [Symbol]
14. has_hgnc_symbol_target_genes: domain - class_entity, range - [Symbol]
15. has_minimum_ratio: domain - class_entity, range - [Ratio]
16. has_mutation_PMID: domain - class_entity, range - [PMID]
17. has_mutation_method: domain - class_entity, range - [Method]
18. has_orig_assembly: domain - class_entity, range - [Assembly]
19. has_orig_chr: domain - class_entity, range - [Chromosome]
20. has_original_ID: domain - class_entity, range - [ID]
21. has_refseq_ID: domain - class_entity, range - [ID]
22. has_score: domain - class_entity, range - [Score]
23. has_source: domain - class_entity, range - [Source]
24. has_type: domain - class_entity, range - [Type]

**Data Type Properties:**

For each class and subclass enumerate its corresponding data type properties:

1. has_PMID_value: domain - class_entity, range - [PMID]
2. has_method_value: domain - class_entity, range - [Method]
3. has_biosample_value: domain - class_entity, range - [Biosample]
4. has_crm_ID_value: domain - class_entity, range - [ID]
5. has_crossref_value: domain - class_entity, range - [Reference]
6. has_current_assembly_value: domain - class_entity, range - [Assembly]
7. has_current_chr_value: domain - class_entity, range - [Chromosome]
8. has_disease_value: domain - class_entity, range - [Disease]
9. has_disease_method_value: domain - class_entity, range - [Method]
10. has_enh2gene_PMID_value: domain - class_entity, range - [PMID]
11. has_enh2gene_method_value: domain - class_entity, range - [Method]
12. has_enh_method_value: domain - class_entity, range - [Method]
13. has_hgnc_symbol_TFs_value: domain - class_entity, range - [Symbol]
14. has_hgnc_symbol_target_genes_value: domain - class_entity, range - [Symbol]
15. has_minimum_ratio_value: domain - class_entity, range - [Ratio]
16. has_mutation_PMID_value: domain - class_entity, range - [PMID]
17. has_mutation_method_value: domain - class_entity, range - [Method]
18. has_orig_assembly_value: domain - class_entity, range - [Assembly]
19. has_orig_chr_value: domain - class_entity, range - [Chromosome]
20. has_original_ID_value: domain - class_entity, range - [ID]
21. has_refseq_ID_value: domain - class_entity, range - [ID]
22. has_score_value: domain - class_entity, range - [Score]
23. has_source_value: domain - class_entity, range - [Source]
24. has_type_value: domain - class_entity, range - [Type]