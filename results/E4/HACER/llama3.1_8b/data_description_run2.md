**Foundational Prefix:**
https://base_ontology.com#

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
   - type: text
   - short description: Biosample Name
   - possible range: [String]

4. crm_ID
   - type: text
   - short description: CRM ID
   - possible range: [String]

5. crossref
   - type: categorical
   - short description: Cross Reference
   - possible range: [Cross Reference]

6. current_assembly
   - type: categorical
   - short description: Current Assembly
   - possible range: [Assembly]

7. current_chr
   - type: categorical
   - short description: Current Chromosome
   - possible range: [Chromosome]

8. disease
   - type: categorical
   - short description: Disease
   - possible range: [Disease]

9. disease_PMID
   - type: categorical
   - short description: Disease PMID
   - possible range: [PMID]

10. disease_method
    - type: categorical
    - short description: Disease Method
    - possible range: [Method]

11. enh2gene_PMID
    - type: categorical
    - short description: Enhancer to Gene PMID
    - possible range: [PMID]

12. enh2gene_method
    - type: categorical
    - short description: Enhancer to Gene Method
    - possible range: [Method]

13. enh_PMID
    - type: categorical
    - short description: Enhancer PMID
    - possible range: [PMID]

14. enh_method
    - type: categorical
    - short description: Enhancer Method
    - possible range: [Method]

15. hgnc_symbol_TFs
    - type: categorical
    - short description: HGNC Symbol Transcription Factors
    - possible range: [HGNC Symbol]

16. hgnc_symbol_target_genes
    - type: text
    - short description: HGNC Symbol Target Genes
    - possible range: [String]

17. minimum_ratio
    - type: categorical
    - short description: Minimum Ratio
    - possible range: [Ratio]

18. mutation_PMID
    - type: categorical
    - short description: Mutation PMID
    - possible range: [PMID]

19. mutation_method
    - type: categorical
    - short description: Mutation Method
    - possible range: [Method]

20. orig_assembly
    - type: categorical
    - short description: Original Assembly
    - possible range: [Assembly]

21. orig_chr
    - type: categorical
    - short description: Original Chromosome
    - possible range: [Chromosome]

22. original_ID
    - type: categorical
    - short description: Original ID
    - possible range: [ID]

23. refsnp_ID
    - type: categorical
    - short description: RefSNP ID
    - possible range: [RefSNP ID]

24. score
    - type: categorical
    - short description: Score
    - possible range: [Score]

25. source
    - type: categorical
    - short description: Source
    - possible range: [Source]

26. type
    - type: categorical
    - short description: Type
    - possible range: [Type]

27. current_end
    - type: Numerical
    - short description: Current End Coordinate
    - possible range: [Integer]

28. current_start
    - type: Numerical
    - short description: Current Start Coordinate
    - possible range: [Integer]

29. orig_end
    - type: Numerical
    - short description: Original End Coordinate
    - possible range: [Integer]

30. orig_start
    - type: Numerical
    - short description: Original Start Coordinate
    - possible range: [Integer]

**classes:**

1. class_entity

**subclasses:**

1. entity_name: subclass of -> class_entity

2. enhancer: subclass of -> class_entity

3. super_enhancer: subclass of -> enhancer

4. target_gene: subclass of -> class_entity

5. transcription_factor: subclass of -> class_entity

6. disease_association: subclass of -> class_entity

7. biosample: subclass of -> class_entity

8. cell_line: subclass of -> biosample

9. genomic_coordinate: subclass of -> class_entity

10. chromosome: subclass of -> genomic_coordinate

11. assembly: subclass of -> genomic_coordinate

**Object Properties:**

1. has_PMID: domain - enhancer, super_enhancer, target_gene, transcription_factor, disease_association
   range - PMID

2. has_method: domain - enhancer, super_enhancer, target_gene, transcription_factor, disease_association
   range - Method

3. has_biosample: domain - biosample
   range - Biosample

4. has_cell_line: domain - cell_line
   range - Cell Line

5. has_genomic_coordinate: domain - genomic_coordinate
   range - Genomic Coordinate

6. has_chromosome: domain - chromosome
   range - Chromosome

7. has_assembly: domain - assembly
   range - Assembly

8. has_original_ID: domain - original_ID
   range - Original ID

9. has_refSNP_ID: domain - refsnp_ID
   range - RefSNP ID

10. has_score: domain - score
    range - Score

11. has_source: domain - source
    range - Source

12. has_type: domain - type
    range - Type

13. has_current_end: domain - current_end
    range - Current End Coordinate

14. has_current_start: domain - current_start
    range - Current Start Coordinate

15. has_orig_end: domain - orig_end
    range - Original End Coordinate

16. has_orig_start: domain - orig_start
    range - Original Start Coordinate

17. is_target_of: domain - target_gene
   range - Transcription Factor

18. regulates: domain - enhancer, super_enhancer
   range - Target Gene

19. associated_with: domain - disease_association
   range - Disease

20. has_hgnc_symbol: domain - hgnc_symbol_TFs
    range - HGNC Symbol

21. has_minimum_ratio: domain - minimum_ratio
    range - Ratio

22. has_mutation_PMID: domain - mutation_PMID
    range - PMID

23. has_mutation_method: domain - mutation_method
    range - Method

**Data Type Properties:**

1. has_PMID_value: domain - enhancer, super_enhancer, target_gene, transcription_factor, disease_association
   range - String

2. has_method_value: domain - enhancer, super_enhancer, target_gene, transcription_factor, disease_association
   range - String

3. has_biosample_name: domain - biosample
   range - String

4. has_cell_line_name: domain - cell_line
   range - String

5. has_genomic_coordinate_value: domain - genomic_coordinate
   range - Integer

6. has_chromosome_value: domain - chromosome
   range - Chromosome

7. has_assembly_value: domain - assembly
   range - Assembly

8. has_original_ID_value: domain - original_ID
   range - ID

9. has_refSNP_ID_value: domain - refsnp_ID
    range - RefSNP ID

10. has_score_value: domain - score
    range - Score

11. has_source_value: domain - source
    range - Source

12. has_type_value: domain - type
    range - Type

13. has_current_end_value: domain - current_end
    range - Integer

14. has_current_start_value: domain - current_start
    range - Integer

15. has_orig_end_value: domain - orig_end
    range - Integer

16. has_orig_start_value: domain - orig_start
    range - Integer