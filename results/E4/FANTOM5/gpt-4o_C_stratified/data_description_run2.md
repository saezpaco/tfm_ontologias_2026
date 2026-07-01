**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. blockCount: categorical - Number of blocks in the genomic feature - [2.0]
2. chromEnd: Numerical - End position of the genomic feature on the chromosome - [1910781.0, 173378884.0]
3. chromStart: Numerical - Start position of the genomic feature on the chromosome - [1910638.0, 173378612.0]
4. score: Numerical - Score associated with the genomic feature - [2.0, 1215.0]
5. thickEnd: Numerical - End position of the thick part of the feature - [1910698.0, 173378727.0]
6. thickStart: Numerical - Start position of the thick part of the feature - [1910697.0, 173378726.0]
7. blockSizes: text - Sizes of the blocks - [various]
8. blockStarts: text - Start positions of the blocks - [various]
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
4. Biosample: subclass of -> GenomicFeature
5. TargetGene: subclass of -> GenomicFeature
6. TranscriptionFactor: subclass of -> GenomicFeature
7. DiseaseAssociation: subclass of -> GenomicFeature

**Object Properties:**
1. hasGenomicCoordinate: GenomicFeature - GenomicCoordinate
2. hasCellLine: GenomicFeature - CellLine
3. hasBiosample: GenomicFeature - Biosample
4. targetsGene: GenomicFeature - TargetGene
5. boundBy: GenomicFeature - TranscriptionFactor
6. associatedWith: GenomicFeature - DiseaseAssociation

**Data Type Properties:**
1. blockCount: GenomicFeature - xsd:float
2. chromEnd: GenomicFeature - xsd:float
3. chromStart: GenomicFeature - xsd:float
4. score: GenomicFeature - xsd:float
5. thickEnd: GenomicFeature - xsd:float
6. thickStart: GenomicFeature - xsd:float
7. blockSizes: GenomicFeature - xsd:string
8. blockStarts: GenomicFeature - xsd:string
9. chrom: GenomicFeature - xsd:string
10. itemRgb: GenomicFeature - xsd:string
11. name: GenomicFeature - xsd:string
12. strand: GenomicFeature - xsd:string