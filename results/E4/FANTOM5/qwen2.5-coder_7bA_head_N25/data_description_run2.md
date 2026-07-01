**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. blockCount: type - Number of blocks - Integer
2. chromEnd: type - End position of chromosome - Integer
3. chromStart: type - Start position of chromosome - Integer
4. score: type - Score of the element - Float
5. thickEnd: type - End position of thick region - Integer
6. thickStart: type - Start position of thick region - Integer
7. blockSizes: type - Sizes of blocks - Text
8. blockStarts: type - Starts of blocks - Text
9. chrom: type - Chromosome name - Categorical
10. itemRgb: type - RGB color code - Categorical
11. name: type - Name of the element - Text
12. strand: type - Strand orientation (forward/reverse) - Categorical

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
9. hasChrom: domain - GeneticElement, range - Categorical
10. hasItemRgb: domain - GeneticElement, range - Categorical
11. hasName: domain - GeneticElement, range - Text
12. hasStrand: domain - GeneticElement, range - Categorical

**Data Type Properties:**
1. blockCountValue: domain - GeneticElement, range - xsd:integer
2. chromEndValue: domain - GeneticElement, range - xsd:integer
3. chromStartValue: domain - GeneticElement, range - xsd:integer
4. scoreValue: domain - GeneticElement, range - xsd:float
5. thickEndValue: domain - GeneticElement, range - xsd:integer
6. thickStartValue: domain - GeneticElement, range - xsd:integer
7. blockSizesValue: domain - GeneticElement, range - xsd:string
8. blockStartsValue: domain - GeneticElement, range - xsd:string
9. chromValue: domain - GeneticElement, range - xsd:string
10. itemRgbValue: domain - GeneticElement, range - xsd:string
11. nameValue: domain - GeneticElement, range - xsd:string
12. strandValue: domain - GeneticElement, range - xsd:string