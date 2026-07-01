**Foundational Prefix:**
https://genetic_regulatory_elements.com#, http://www.w3.org/1999/02/22-rdf-syntax-ns#, http://www.w3.org/2000/01/rdf-schema#, http://www.w3.org/2004/02/skos/core#, http://www.w3.org/2001/XMLSchema# and http://www.w3.org/2002/07/owl#

**Data Description:**
1. blockCount: type - Number of blocks in the genomic region - Integer
2. chromEnd: type - End position of the chromosome - Integer
3. chromStart: type - Start position of the chromosome - Integer
4. score: type - Score associated with the genomic element - Float
5. thickEnd: type - End position of the thick part of the genomic element - Integer
6. thickStart: type - Start position of the thick part of the genomic element - Integer
7. blockSizes: type - Sizes of each block in the genomic region - Text
8. blockStarts: type - Starting positions of each block in the genomic region - Text
9. chrom: type - Chromosome identifier - Text
10. itemRgb: type - RGB color code for visualization - Categorical
11. name: type - Name or identifier of the genomic element - Text
12. strand: type - Orientation of the genomic element (forward/reverse) - Categorical

**Classes:**
1. GenomicElement

**Subclasses:**
1. Enhancer subclass of -> GenomicElement
2. SuperEnhancer subclass of -> Enhancer

**Object Properties:**
1. hasBlockCount: domain - GenomicElement, range - Integer
2. hasChromEnd: domain - GenomicElement, range - Integer
3. hasChromStart: domain - GenomicElement, range - Integer
4. hasScore: domain - GenomicElement, range - Float
5. hasThickEnd: domain - GenomicElement, range - Integer
6. hasThickStart: domain - GenomicElement, range - Integer
7. hasBlockSizes: domain - GenomicElement, range - Text
8. hasBlockStarts: domain - GenomicElement, range - Text
9. hasChrom: domain - GenomicElement, range - Text
10. hasItemRgb: domain - GenomicElement, range - Categorical
11. hasName: domain - GenomicElement, range - Text
12. hasStrand: domain - GenomicElement, range - Categorical

**Data Type Properties:**
1. blockCountValue: domain - GenomicElement, range - xsd:integer
2. chromEndValue: domain - GenomicElement, range - xsd:integer
3. chromStartValue: domain - GenomicElement, range - xsd:integer
4. scoreValue: domain - GenomicElement, range - xsd:float
5. thickEndValue: domain - GenomicElement, range - xsd:integer
6. thickStartValue: domain - GenomicElement, range - xsd:integer
7. blockSizesValue: domain - GenomicElement, range - xsd:string
8. blockStartsValue: domain - GenomicElement, range - xsd:string
9. chromValue: domain - GenomicElement, range - xsd:string
10. itemRgbValue: domain - GenomicElement, range - xsd:string
11. nameValue: domain - GenomicElement, range - xsd:string
12. strandValue: domain - GenomicElement, range - xsd:string