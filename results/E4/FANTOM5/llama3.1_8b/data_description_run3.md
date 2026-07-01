**Foundational Prefix:**
https://base_ontology.com#

**Data Description:**

1. TFs2enh_PMID
   - type: categorical
   - short description: PubMed IDs of transcription factors to enhancers associations
   - possible range: string

2. TFs2enh_method
   - type: categorical
   - short description: Methods used for transcription factors to enhancers associations
   - possible range: string

3. biosample
   - type: categorical
   - short description: Cell lines or biosamples associated with the regulatory elements
   - possible range: string

4. crm_ID
   - type: text
   - short description: IDs of chromatin modification regions
   - possible range: string

5. crossref
   - type: categorical
   - short description: Cross-reference information for the regulatory elements
   - possible range: string

6. current_assembly
   - type: categorical
   - short description: Current genome assembly versions associated with the regulatory elements
   - possible range: string

7. current_chr
   - type: categorical
   - short description: Chromosome IDs of the current genome assembly
   - possible range: string

8. disease
   - type: categorical
   - short description: Diseases associated with the regulatory elements
   - possible range: string

9. disease_PMID
   - type: categorical
   - short description: PubMed IDs of disease associations
   - possible range: string

10. disease_method
    - type: categorical
    - short description: Methods used for disease associations
    - possible range: string

11. enh2gene_PMID
    - type: categorical
    - short description: PubMed IDs of enhancer to gene associations
    - possible range: string

12. enh2gene_method
    - type: categorical
    - short description: Methods used for enhancer to gene associations
    - possible range: string

13. enh_PMID
    - type: categorical
    - short description: PubMed IDs of regulatory elements (enhancers, super-enhancers)
    - possible range: string

14. enh_method
    - type: categorical
    - short description: Methods used for regulatory element identification
    - possible range: string

15. hgnc_symbol_TFs
    - type: categorical
    - short description: Transcription factor symbols (HGNC IDs)
    - possible range: string

16. hgnc_symbol_target_genes
    - type: text
    - short description: Target gene symbols (HGNC IDs) associated with the regulatory elements
    - possible range: string

17. minimum_ratio
    - type: categorical
    - short description: Minimum ratio values for regulatory element identification
    - possible range: number

18. mutation_PMID
    - type: categorical
    - short description: PubMed IDs of mutations associated with the regulatory elements
    - possible range: string

19. mutation_method
    - type: categorical
    - short description: Methods used for mutation associations
    - possible range: string

20. orig_assembly
    - type: categorical
    - short description: Original genome assembly versions associated with the regulatory elements
    - possible range: string

21. orig_chr
    - type: categorical
    - short description: Chromosome IDs of the original genome assembly
    - possible range: string

22. original_ID
    - type: categorical
    - short description: Original IDs of chromatin modification regions
    - possible range: string

23. refsnp_ID
    - type: categorical
    - short description: RefSNP IDs associated with the regulatory elements
    - possible range: string

24. score
    - type: categorical
    - short description: Scores for regulatory element identification
    - possible range: number

25. source
    - type: categorical
    - short description: Sources of the regulatory element data
    - possible range: string

26. type
    - type: categorical
    - short description: Types of regulatory elements (enhancers, super-enhancers)
    - possible range: string

27. current_end
    - type: Numerical
    - short description: Current end coordinates of the regulatory elements
    - possible range: integer

28. current_start
    - type: Numerical
    - short description: Current start coordinates of the regulatory elements
    - possible range: integer

29. orig_end
    - type: Numerical
    - short description: Original end coordinates of the regulatory elements
    - possible range: integer

30. orig_start
    - type: Numerical
    - short description: Original start coordinates of the regulatory elements
    - possible range: integer

**classes:**

1. class_entity

**subclasses:**

1. entity_name: subclass of -> class_entity

**Object Properties:**

For each class and subclass enumerate its corresponding object properties:

1. associated_with: domain - class_entity, range - biosample
2. has_PMID: domain - class_entity, range - TFs2enh_PMID
3. has_method: domain - class_entity, range - TFs2enh_method
4. has_disease_PMID: domain - class_entity, range - disease_PMID
5. has_disease_method: domain - class_entity, range - disease_method
6. has_enhancer_PMID: domain - class_entity, range - enh_PMID
7. has_enhancer_method: domain - class_entity, range - enh_method
8. targets_gene: domain - class_entity, range - hgnc_symbol_target_genes
9. associated_with_transcription_factor: domain - class_entity, range - hgnc_symbol_TFs

**Data Type Properties:**

For each class and subclass enumerate its corresponding data type properties:

1. has_PMID_value: domain - TFs2enh_PMID, range - string
2. has_method_value: domain - TFs2enh_method, range - string
3. has_disease_PMID_value: domain - disease_PMID, range - string
4. has_disease_method_value: domain - disease_method, range - string
5. has_enhancer_PMID_value: domain - enh_PMID, range - string
6. has_enhancer_method_value: domain - enh_method, range - string
7. targets_gene_value: domain - hgnc_symbol_target_genes, range - string
8. associated_with_transcription_factor_value: domain - hgnc_symbol_TFs, range - string