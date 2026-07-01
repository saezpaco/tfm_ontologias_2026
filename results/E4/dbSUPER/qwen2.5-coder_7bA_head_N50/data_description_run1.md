**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. cell_name: type - categorical - short description of the cell line or biosample - possible range: [cell_line_1, cell_line_2, ..., cell_line_n]
2. chrom: type - text - short description of the chromosome number - possible range: [chr1, chr2, ..., chrX]
3. gene_symbol: type - text - short description of the target gene symbol - possible range: [gene1, gene2, ..., geneN]
4. se_id: type - text - short description of the super-enhancer identifier - possible range: [se1, se2, ..., seN]
5. rank: type - Numerical - short description of the rank or significance score - possible range: [1, 2, ..., n]
6. start: type - Numerical - short description of the genomic start position - possible range: [0, 1, ..., max_genomic_position]
7. stop: type - Numerical - short description of the genomic stop position - possible range: [0, 1, ..., max_genomic_position]

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. CellLine
5. TargetGene

**Subclasses:**
1. GeneticElement
   - subclass of -> Entity
2. Enhancer
   - subclass of -> GeneticElement
3. SuperEnhancer
   - subclass of -> Enhancer
4. CellLine
   - subclass of -> Entity
5. TargetGene
   - subclass of -> Entity

**Object Properties:**
1. hasCellLine: domain - GeneticElement, range - CellLine
2. containsTargetGene: domain - SuperEnhancer, range - TargetGene
3. locatedOnChromosome: domain - GeneticElement, range - Chromosome
4. hasRank: domain - GeneticElement, range - xsd:integer

**Data Type Properties:**
1. cellName: domain - GeneticElement, range - xsd:string
2. chromosome: domain - GeneticElement, range - xsd:string
3. geneSymbol: domain - TargetGene, range - xsd:string
4. seId: domain - SuperEnhancer, range - xsd:string
5. start: domain - GeneticElement, range - xsd:integer
6. stop: domain - GeneticElement, range - xsd:integer