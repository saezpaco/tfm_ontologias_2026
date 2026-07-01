**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. blockCount: categorical - count of blocks - [2.0]
2. chromEnd: Numerical - end position on chromosome - [840250.0, 1803303.0]
3. chromStart: Numerical - start position on chromosome - [839741.0, 1803114.0]
4. score: Numerical - score value - [2.0, 443.0]
5. thickEnd: Numerical - thick end position on chromosome - [839788.0, 1803274.0]
6. thickStart: Numerical - thick start position on chromosome - [839787.0, 1803273.0]
7. blockSizes: text - sizes of blocks - [various]
8. blockStarts: text - start positions of blocks - [various]
9. chrom: categorical - chromosome identifier - [various]
10. itemRgb: categorical - RGB color value - [various]
11. name: text - name identifier - [various]
12. strand: categorical - DNA strand - [various]

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. CellLine
4. Biosample
5. TargetGene
6. TranscriptionFactor
7. Disease

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. associatedWithCellLine: GeneticElement - CellLine
3. associatedWithBiosample: GeneticElement - Biosample
4. targetsGene: GeneticElement - TargetGene
5. boundByTranscriptionFactor: GeneticElement - TranscriptionFactor
6. associatedWithDisease: GeneticElement - Disease

**Data Type Properties:**
1. blockCount: GeneticElement - xsd:float
2. chromEnd: GenomicCoordinate - xsd:float
3. chromStart: GenomicCoordinate - xsd:float
4. score: GeneticElement - xsd:float
5. thickEnd: GenomicCoordinate - xsd:float
6. thickStart: GenomicCoordinate - xsd:float
7. blockSizes: GeneticElement - xsd:string
8. blockStarts: GeneticElement - xsd:string
9. chrom: GenomicCoordinate - xsd:string
10. itemRgb: GeneticElement - xsd:string
11. name: GeneticElement - xsd:string
12. strand: GenomicCoordinate - xsd:string