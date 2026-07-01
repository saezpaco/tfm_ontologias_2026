**Foundational Prefix:**
https://genetic_regulatory_elements.com#, http://www.w3.org/1999/02/22-rdf-syntax-ns#, http://www.w3.org/2000/01/rdf-schema#, http://www.w3.org/2004/02/skos/core#, http://www.w3.org/2001/XMLSchema# and http://www.w3.org/2002/07/owl#

**Data Description:**
1. blockCount: type - Number of blocks in the genomic region - Integer
2. chromEnd: type - End position of the chromosome - Integer
3. chromStart: type - Start position of the chromosome - Integer
4. score: type - Score or significance of the element - Float
5. thickEnd: type - End position of the thick part of the element - Integer
6. thickStart: type - Start position of the thick part of the element - Integer
7. blockSizes: type - Sizes of each block in the genomic region - Text
8. blockStarts: type - Starting positions of each block in the genomic region - Text
9. chrom: type - Chromosome identifier - Text
10. itemRgb: type - RGB color code for visualization - Categorical
11. name: type - Name or identifier of the element - Text
12. strand: type - Orientation of the element (positive/negative) - Categorical

**Classes:**
1. GeneticElement

**Subclasses:**
1. Enhancer subclass of -> GeneticElement
2. SuperEnhancer subclass of -> Enhancer

**Object Properties:**
1. hasBlockCount: domain - GeneticElement, range - Integer
2. hasChromEnd: domain - GeneticElement, range - Integer
3. hasChromStart: domain - GeneticElement, range - Integer
4. hasScore: domain - GeneticElement, range - Float
5. hasThickEnd: domain - GeneticElement, range - Integer
6. hasThickStart: domain - GeneticElement, range - Integer
7. hasBlockSizes: domain - GeneticElement, range - Text
8. hasBlockStarts: domain - GeneticElement, range - Text
9. hasChrom: domain - GeneticElement, range - Text
10. hasItemRgb: domain - GeneticElement, range - Categorical
11. hasName: domain - GeneticElement, range - Text
12. hasStrand: domain - GeneticElement, range - Categorical

**Data Type Properties:**
1. count: domain - GeneticElement, range - Integer
2. max: domain - GeneticElement, range - Float or Integer
3. mean: domain - GeneticElement, range - Float
4. min: domain - GeneticElement, range - Float or Integer
5. non_null_count: domain - GeneticElement, range - Integer
6. std: domain - GeneticElement, range - Float
7. type: domain - GeneticElement, range - Categorical (categorical, numerical, text)
8. unique_count: domain - GeneticElement, range - Integer