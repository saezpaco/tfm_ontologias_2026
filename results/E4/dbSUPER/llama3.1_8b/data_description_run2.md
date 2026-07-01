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
   - type: text
   - short description: Biosample Name
   - possible range: [String]

4. crm_ID
   - type: text
   - short description: CRM ID
   - possible range: [String]

5. crossref
   - type: text
   - short description: Cross Reference
   - possible range: [String]

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
    - type: text
    - short description: Original ID
    - possible range: [String]

23. refsnp_ID
    - type: categorical
    - short description: RefSNP ID
    - possible range: [ID]

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

4. transcription_factor: subclass of -> class_entity

5. target_gene: subclass of -> class_entity

6. disease_association: subclass of -> class_entity

7. biosample: subclass of -> class_entity

8. cell_line: subclass of -> biosample

9. gene: subclass of -> class_entity

10. chromosome: subclass of -> class_entity

**Object Properties:**

1. has_PMID: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [PMID]

2. has_method: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Method]

3. has_assembly: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Assembly]

4. has_chromosome: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Chromosome]

5. has_ID: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [ID]

6. has_score: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Score]

7. has_source: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Source]

8. has_type: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Type]

9. has_end_coordinate: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Integer]

10. has_start_coordinate: domain - range
    - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Integer]

**Data Type Properties:**

1. has_PMID_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [PMID]

2. has_method_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Method]

3. has_assembly_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Assembly]

4. has_chromosome_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Chromosome]

5. has_ID_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [ID]

6. has_score_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Score]

7. has_source_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Source]

8. has_type_value: domain - range
   - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Type]

9. has_end_coordinate_value: domain - range
    - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Integer]

10. has_start_coordinate_value: domain - range
     - enhancer, super_enhancer, transcription_factor, target_gene, disease_association, biosample, cell_line, gene, chromosome - [Integer]