**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. blockCount: categorical - Number of blocks in the genomic feature - [2.0]
2. chromEnd: Numerical - End position of the genomic feature on the chromosome - [794815.0, 157131690.0]
3. chromStart: Numerical - Start position of the genomic feature on the chromosome - [794631.0, 157131379.0]
4. score: Numerical - Score associated with the genomic feature - [2.0, 205.0]
5. thickEnd: Numerical - End position of the thick part of the feature - [794739.0, 157131421.0]
6. thickStart: Numerical - Start position of the thick part of the feature - [794738.0, 157131420.0]
7. blockSizes: text - Sizes of the blocks in the genomic feature - [various]
8. blockStarts: text - Start positions of the blocks in the genomic feature - [various]
9. chrom: text - Chromosome on which the feature is located - [various]
10. itemRgb: categorical - RGB value for the item - [various]
11. name: text - Name of the genomic feature - [various]
12. strand: categorical - Strand of the genomic feature - [various]

**classes:**
1. GenomicFeature
2. Chromosome
3. Block
4. Strand
5. Score

**subclasses:**
1. Enhancer: subclass of -> GenomicFeature
2. SuperEnhancer: subclass of -> GenomicFeature

**Object Properties:**
1. hasChromosome: GenomicFeature - Chromosome
2. hasBlock: GenomicFeature - Block
3. hasStrand: GenomicFeature - Strand
4. hasScore: GenomicFeature - Score

**Data Type Properties:**
1. blockCount: Block - xsd:integer
2. chromEnd: GenomicFeature - xsd:integer
3. chromStart: GenomicFeature - xsd:integer
4. scoreValue: Score - xsd:integer
5. thickEnd: GenomicFeature - xsd:integer
6. thickStart: GenomicFeature - xsd:integer
7. blockSizes: Block - xsd:string
8. blockStarts: Block - xsd:string
9. chrom: Chromosome - xsd:string
10. itemRgb: GenomicFeature - xsd:string
11. name: GenomicFeature - xsd:string
12. strand: Strand - xsd:string