**Foundational Prefix:**
https://base_ontology.com#

**Data Description:**

1. TFs2enh_PMID
   - type: categorical
   - short description: PubMed IDs associated with transcription factors to enhancers interactions
   - possible range: string

2. TFs2enh_method
   - type: categorical
   - short description: Methods used for identifying transcription factors to enhancers interactions
   - possible range: string

3. biosample
   - type: categorical
   - short description: Cell lines or biosamples associated with the data
   - possible range: string

4. crm_ID
   - type: text
   - short description: IDs of chromatin modification regions
   - possible range: string

5. crossref
   - type: categorical
   - short description: Cross-references to external databases or resources
   - possible range: string

6. current_assembly
   - type: categorical
   - short description: Current genome assembly versions associated with the data
   - possible range: string

7. current_chr
   - type: categorical
   - short description: Chromosome IDs of the current genome assembly
   - possible range: string

8. disease
   - type: categorical
   - short description: Diseases or conditions associated with the data
   - possible range: string

9. disease_PMID
   - type: categorical
   - short description: PubMed IDs associated with disease-related information
   - possible range: string

10. disease_method
    - type: categorical
    - short description: Methods used for identifying disease associations
    - possible range: string

11. enh2gene_PMID
    - type: categorical
    - short description: PubMed IDs associated with enhancer to gene interactions
    - possible range: string

12. enh2gene_method
    - type: categorical
    - short description: Methods used for identifying enhancer to gene interactions
    - possible range: string

13. enh_PMID
    - type: categorical
    - short description: PubMed IDs associated with enhancers
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
    - short description: Minimum ratios associated with the data
    - possible range: number

18. mutation_PMID
    - type: categorical
    - short description: PubMed IDs associated with mutations
    - possible range: string

19. mutation_method
    - type: categorical
    - short description: Methods used for identifying mutations
    - possible range: string

20. orig_assembly
    - type: categorical
    - short description: Original genome assembly versions associated with the data
    - possible range: string

21. orig_chr
    - type: categorical
    - short description: Chromosome IDs of the original genome assembly
    - possible range: string

22. original_ID
    - type: categorical
    - short description: IDs of original chromatin modification regions
    - possible range: string

23. refsnp_ID
    - type: categorical
    - short description: RefSNP IDs associated with the data
    - possible range: string

24. score
    - type: categorical
    - short description: Scores associated with the data
    - possible range: number

25. source
    - type: categorical
    - short description: Sources of the data
    - possible range: string

26. type
    - type: categorical
    - short description: Types of genetic regulatory elements
    - possible range: string

27. current_end
    - type: Numerical
    - short description: End coordinates of the current genome assembly
    - possible range: integer

28. current_start
    - type: Numerical
    - short description: Start coordinates of the current genome assembly
    - possible range: integer

29. orig_end
    - type: Numerical
    - short description: End coordinates of the original genome assembly
    - possible range: integer

30. orig_start
    - type: Numerical
    - short description: Start coordinates of the original genome assembly
    - possible range: integer

**classes:**

1. class_entity

**subclasses:**

1. entity_name: subclass of -> class_entity

2. enhancer: subclass of -> class_entity

3. super_enhancer: subclass of -> class_entity

4. chromatin_modification_region: subclass of -> class_entity

5. gene: subclass of -> class_entity

6. transcription_factor: subclass of -> class_entity

7. disease_association: subclass of -> class_entity

8. mutation: subclass of -> class_entity

9. genomic_coordinate: subclass of -> class_entity

10. biosample: subclass of -> class_entity

**Object Properties:**

1. has_PMID: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (PubMed ID)

2. has_method: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (method name)

3. is_target_of: domain - range
   - gene -> transcription_factor

4. is_associated_with: domain - range
   - disease_association -> disease

5. has_score: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> number (score)

6. has_source: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (source name)

7. has_type: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (type of genetic regulatory element)

8. has_coordinates: domain - range
   - genomic_coordinate -> integer (start and end coordinates)

9. is_part_of: domain - range
   - chromatin_modification_region -> enhancer

10. has_refSNP_ID: domain - range
    - chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate -> string (RefSNP ID)

**Data Type Properties:**

1. has_PMID: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (PubMed ID)

2. has_method: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (method name)

3. is_target_of: domain - range
   - gene -> transcription_factor

4. is_associated_with: domain - range
   - disease_association -> disease

5. has_score: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> number (score)

6. has_source: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (source name)

7. has_type: domain - range
   - enhancer, super_enhancer, chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate, biosample -> string (type of genetic regulatory element)

8. has_coordinates: domain - range
   - genomic_coordinate -> integer (start and end coordinates)

9. is_part_of: domain - range
   - chromatin_modification_region -> enhancer

10. has_refSNP_ID: domain - range
    - chromatin_modification_region, gene, transcription_factor, disease_association, mutation, genomic_coordinate -> string (RefSNP ID)