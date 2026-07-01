**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. blockCount: categorical - Number of blocks in the genomic feature - [2]
2. chromEnd: Numerical - End position of the genomic feature on the chromosome - [840250.0, 1114310.0]
3. chromStart: Numerical - Start position of the genomic feature on the chromosome - [839741.0, 1114183.0]
4. score: Numerical - Score associated with the genomic feature - [2.0, 143.0]
5. thickEnd: Numerical - End position of the thick part of the feature - [839788.0, 1114246.0]
6. thickStart: Numerical - Start position of the thick part of the feature - [839787.0, 1114245.0]
7. blockSizes: text - Sizes of the blocks - [various]
8. blockStarts: text - Start positions of the blocks - [various]
9. chrom: categorical - Chromosome on which the feature is located - [various]
10. itemRgb: categorical - RGB value for the item - [various]
11. name: text - Name of the genomic feature - [various]
12. strand: categorical - Strand of the genomic feature - [various]

**classes:**
1. GenomicFeature

**subclasses:**
1. Enhancer: subclass of -> GenomicFeature
2. SuperEnhancer: subclass of -> GenomicFeature

**Object Properties:**
1. hasChromosome: GenomicFeature - Chromosome
2. hasBlock: GenomicFeature - Block
3. hasStrand: GenomicFeature - Strand

**Data Type Properties:**
1. blockCount: GenomicFeature - xsd:integer
2. chromEnd: GenomicFeature - xsd:integer
3. chromStart: GenomicFeature - xsd:integer
4. score: GenomicFeature - xsd:integer
5. thickEnd: GenomicFeature - xsd:integer
6. thickStart: GenomicFeature - xsd:integer
7. blockSizes: GenomicFeature - xsd:string
8. blockStarts: GenomicFeature - xsd:string
9. chrom: GenomicFeature - xsd:string
10. itemRgb: GenomicFeature - xsd:string
11. name: GenomicFeature - xsd:string
12. strand: GenomicFeature - xsd:string