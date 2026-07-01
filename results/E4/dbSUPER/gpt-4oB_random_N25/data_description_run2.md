**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. cell_name: text - name of the cell line or biosample - string
2. chrom: text - chromosome identifier - string
3. gene_symbol: text - symbol of the target gene - string
4. se_id: text - identifier for the super-enhancer - string
5. rank: Numerical - rank of the super-enhancer - float
6. start: Numerical - start coordinate of the genomic region - float
7. stop: Numerical - stop coordinate of the genomic region - float

**classes:**
1. CellLine
2. Chromosome
3. Gene
4. SuperEnhancer
5. GenomicRegion

**subclasses:**
1. CellLine: subclass of -> base:Entity
2. Chromosome: subclass of -> base:Entity
3. Gene: subclass of -> base:Entity
4. SuperEnhancer: subclass of -> base:RegulatoryElement
5. GenomicRegion: subclass of -> base:Entity

**Object Properties:**
1. hasChromosome: base:GenomicRegion - base:Chromosome
2. targetsGene: base:SuperEnhancer - base:Gene
3. foundInCellLine: base:SuperEnhancer - base:CellLine

**Data Type Properties:**
1. cellName: base:CellLine - xsd:string
2. chromName: base:Chromosome - xsd:string
3. geneSymbol: base:Gene - xsd:string
4. seID: base:SuperEnhancer - xsd:string
5. rankValue: base:SuperEnhancer - xsd:float
6. startCoordinate: base:GenomicRegion - xsd:float
7. stopCoordinate: base:GenomicRegion - xsd:float