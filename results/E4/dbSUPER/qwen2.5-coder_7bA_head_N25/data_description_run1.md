**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. cell_name: type - categorical - short description of the cell line or biosample - possible range: [cell_line_1, cell_line_2, ..., cell_line_n]
2. chrom: type - text - short description of the chromosome number - possible range: [chr1, chr2, ..., chrX, chrY, chrM]
3. gene_symbol: type - text - short description of the target gene symbol - possible range: [gene1, gene2, ..., geneN]
4. se_id: type - text - short description of the super-enhancer identifier - possible range: [se1, se2, ..., seN]
5. rank: type - Numerical - short description of the rank or significance of the enhancer - possible range: [1, 2, ..., n]
6. start: type - Numerical - short description of the genomic start position of the enhancer - possible range: [0, 1, ..., max_genomic_position]
7. stop: type - Numerical - short description of the genomic stop position of the enhancer - possible range: [0, 1, ..., max_genomic_position]

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. CellLine
5. TargetGene

**Subclasses:**
1. EnhancerType (subclass of -> GeneticElement)
2. SuperEnhancerType (subclass of -> GeneticElement)

**Object Properties:**
1. hasCellLine: domain - Enhancer/SuperEnhancer; range - CellLine
2. targetsGene: domain - Enhancer/SuperEnhancer; range - TargetGene

**Data Type Properties:**
1. chromosomeNumber: domain - GeneticElement; range - xsd:string
2. genomicStart: domain - GeneticElement; range - xsd:integer
3. genomicStop: domain - GeneticElement; range - xsd:integer
4. rankScore: domain - Enhancer/SuperEnhancer; range - xsd:float