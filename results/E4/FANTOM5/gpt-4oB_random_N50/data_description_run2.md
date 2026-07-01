**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. blockCount: categorical - Number of blocks in the genomic feature - [2]
2. chromEnd: Numerical - End position of the genomic feature on the chromosome - [1391783.0, 236335565.0]
3. chromStart: Numerical - Start position of the genomic feature on the chromosome - [1391218.0, 236335410.0]
4. score: Numerical - Score associated with the genomic feature - [2.0, 265.0]
5. thickEnd: Numerical - End position of the thick part of the feature - [1391434.0, 236335488.0]
6. thickStart: Numerical - Start position of the thick part of the feature - [1391433.0, 236335487.0]
7. blockSizes: text - Sizes of the blocks in the genomic feature - [various]
8. blockStarts: text - Start positions of the blocks in the genomic feature - [various]
9. chrom: text - Chromosome on which the feature is located - [various]
10. itemRgb: categorical - RGB value for the item - [various]
11. name: text - Name of the genomic feature - [various]
12. strand: categorical - Strand of the genomic feature - [various]

**classes:**
1. GenomicFeature

**subclasses:**
1. Enhancer: subclass of -> GenomicFeature
2. SuperEnhancer: subclass of -> GenomicFeature
3. CellLine: subclass of -> GenomicFeature
4. BioSample: subclass of -> GenomicFeature
5. TargetGene: subclass of -> GenomicFeature
6. TranscriptionFactor: subclass of -> GenomicFeature
7. DiseaseAssociation: subclass of -> GenomicFeature

**Object Properties:**
1. hasChromosome: GenomicFeature - Chromosome
2. hasBlockCount: GenomicFeature - BlockCount
3. hasBlockSizes: GenomicFeature - BlockSizes
4. hasBlockStarts: GenomicFeature - BlockStarts
5. hasItemRgb: GenomicFeature - ItemRgb
6. hasStrand: GenomicFeature - Strand

**Data Type Properties:**
1. chromEnd: GenomicFeature - xsd:float
2. chromStart: GenomicFeature - xsd:float
3. score: GenomicFeature - xsd:float
4. thickEnd: GenomicFeature - xsd:float
5. thickStart: GenomicFeature - xsd:float
6. name: GenomicFeature - xsd:string