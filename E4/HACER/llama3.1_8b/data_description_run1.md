**Foundational Prefix:**
https://base_ontology.com#

**Data Description:**

1. TFs2enh_PMID
   - type: categorical
   - short description: PubMed IDs of transcription factors to enhancers associations
   - possible range: string

2. TFs2enh_method
   - type: categorical
   - short description: Methods used for identifying transcription factors to enhancers associations
   - possible range: string

3. biosample_name
   - type: text
   - short description: Names of cell lines or biosamples
   - possible range: string

4. crm_ID
   - type: text
   - short description: IDs of chromatin modification regions
   - possible range: string

5. crossref
   - type: categorical
   - short description: Cross-references to external databases
   - possible range: string

6. current_assembly
   - type: categorical
   - short description: Current genome assembly versions
   - possible range: string

7. current_chr
   - type: categorical
   - short description: Current chromosome IDs
   - possible range: string

8. disease
   - type: categorical
   - short description: Disease names associated with enhancers
   - possible range: string

9. disease_PMID
   - type: categorical
   - short description: PubMed IDs of disease associations
   - possible range: string

10. disease_method
    - type: categorical
    - short description: Methods used for identifying disease associations
    - possible range: string

11. enh2gene_PMID
    - type: categorical
    - short description: PubMed IDs of enhancer to gene associations
    - possible range: string

12. enh2gene_method
    - type: categorical
    - short description: Methods used for identifying enhancer to gene associations
    - possible range: string

13. enh_PMID
    - type: categorical
    - short description: PubMed IDs of enhancers
    - possible range: string

14. enh_method
    - type: categorical
    - short description: Methods used for identifying enhancers
    - possible range: string

15. hgnc_symbol_TFs
    - type: categorical
    - short description: HGNC symbols of transcription factors
    - possible range: string

16. hgnc_symbol_target_genes
    - type: text
    - short description: HGNC symbols of target genes
    - possible range: string

17. minimum_ratio
    - type: categorical
    - short description: Minimum ratios of enhancer activity
    - possible range: float

18. mutation_PMID
    - type: categorical
    - short description: PubMed IDs of mutations associated with enhancers
    - possible range: string

19. mutation_method
    - type: categorical
    - short description: Methods used for identifying mutations associated with enhancers
    - possible range: string

20. orig_assembly
    - type: categorical
    - short description: Original genome assembly versions
    - possible range: string

21. orig_chr
    - type: categorical
    - short description: Original chromosome IDs
    - possible range: string

22. original_ID
    - type: categorical
    - short description: Original IDs of chromatin modification regions
    - possible range: string

23. refsnp_ID
    - type: categorical
    - short description: RefSNP IDs of enhancers
    - possible range: string

24. score
    - type: categorical
    - short description: Scores of enhancer activity
    - possible range: float

25. source
    - type: categorical
    - short description: Sources of data
    - possible range: string

26. type
    - type: categorical
    - short description: Types of data
    - possible range: string

27. current_end
    - type: Numerical
    - short description: Current end coordinates of enhancers
    - possible range: integer

28. current_start
    - type: Numerical
    - short description: Current start coordinates of enhancers
    - possible range: integer

29. orig_end
    - type: Numerical
    - short description: Original end coordinates of enhancers
    - possible range: integer

30. orig_start
    - type: Numerical
    - short description: Original start coordinates of enhancers
    - possible range: integer

**classes:**

1. class_entity

**subclasses:**

1. entity_name: subclass of -> class_entity

2. enhancer: subclass of -> class_entity

3. super_enhancer: subclass of -> enhancer

4. chromatin_modification_region: subclass of -> class_entity

5. cell_line: subclass of -> class_entity

6. biosample: subclass of -> class_entity

7. target_gene: subclass of -> class_entity

8. transcription_factor: subclass of -> class_entity

9. disease_association: subclass of -> class_entity

10. mutation: subclass of -> class_entity

**Object Properties:**

1. has_PMID: enhancer - PubMed ID
2. is_associated_with: enhancer - target_gene
3. has_method: enhancer - method
4. has_chromatin_modification_region: chromatin_modification_region - enhancer
5. has_cell_line: cell_line - biosample
6. has_transcription_factor: transcription_factor - enhancer
7. is_disease_associated_with: disease_association - enhancer

**Data Type Properties:**

1. has_PMID_value: enhancer - PubMed ID value
2. has_method_name: enhancer - method name
3. has_chromatin_modification_region_ID: chromatin_modification_region - ID
4. has_cell_line_name: cell_line - name
5. has_transcription_factor_HGNC_symbol: transcription_factor - HGNC symbol
6. is_disease_associated_with_name: disease_association - disease name