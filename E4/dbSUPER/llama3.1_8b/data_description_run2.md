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
   - type: text
   - short description: Cross-reference IDs for external databases
   - possible range: string

6. current_assembly
   - type: categorical
   - short description: Current genome assembly versions
   - possible range: string

7. current_chr
   - type: categorical
   - short description: Current chromosome numbers
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
    - short description: Transcription factor symbols from HGNC database
    - possible range: string

16. hgnc_symbol_target_genes
    - type: text
    - short description: Target gene symbols from HGNC database
    - possible range: string

17. minimum_ratio
    - type: categorical
    - short description: Minimum ratio values for enhancer to gene associations
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
    - short description: Original chromosome numbers
    - possible range: string

22. original_ID
    - type: text
    - short description: IDs of original data sources
    - possible range: string

23. refsnp_ID
    - type: categorical
    - short description: RefSNP IDs for genetic variations
    - possible range: string

24. score
    - type: categorical
    - short description: Scores for enhancer to gene associations
    - possible range: float

25. source
    - type: categorical
    - short description: Sources of data
    - possible range: string

26. type
    - type: categorical
    - short description: Types of genetic elements
    - possible range: string

27. current_end
    - type: Numerical
    - short description: Current end coordinates of genomic regions
    - possible range: integer

28. current_start
    - type: Numerical
    - short description: Current start coordinates of genomic regions
    - possible range: integer

29. orig_end
    - type: Numerical
    - short description: Original end coordinates of genomic regions
    - possible range: integer

30. orig_start
    - type: Numerical
    - short description: Original start coordinates of genomic regions
    - possible range: integer

**classes:**

1. class_entity

**subclasses:**

1. entity_name: subclass of -> class_entity

2. enhancer: subclass of -> class_entity

3. super_enhancer: subclass of -> class_entity

4. target_gene: subclass of -> class_entity

5. transcription_factor: subclass of -> class_entity

6. disease_association: subclass of -> class_entity

7. mutation: subclass of -> class_entity

8. genomic_region: subclass of -> class_entity

**Object Properties:**

1. associated_with: domain - enhancer, super_enhancer; range - target_gene, transcription_factor

2. regulates: domain - transcription_factor; range - target_gene

3. associated_disease: domain - disease_association; range - disease

4. mutation_in: domain - mutation; range - genomic_region

5. located_in: domain - genomic_region; range - chromosome

6. has_coordinate: domain - genomic_region; range - integer

7. has_score: domain - enhancer, super_enhancer; range - float

8. has_source: domain - entity_name; range - string

9. has_type: domain - entity_name; range - string

**Data Type Properties:**

1. PubMed_ID: domain - TFs2enh_PMID, disease_PMID, enh_PMID, mutation_PMID; range - string

2. method: domain - TFs2enh_method, disease_method, enh_method, mutation_method; range - string

3. chromosome: domain - current_chr, orig_chr; range - string

4. assembly_version: domain - current_assembly, orig_assembly; range - string

5. ID: domain - crm_ID, original_ID, refsnp_ID; range - string

6. name: domain - biosample_name; range - string

7. symbol: domain - hgnc_symbol_TFs, hgnc_symbol_target_genes; range - string