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
5. rank: Numerical - rank of the super-enhancer - 8.0 to 864.0
6. start: Numerical - start coordinate of the genomic region - 2022617.0 to 204375797.0
7. stop: Numerical - stop coordinate of the genomic region - 2055462.0 to 204381837.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. CellLine
4. Gene
5. SuperEnhancer

**subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> Enhancer

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. isLocatedIn: GenomicCoordinate - GeneticElement
3. isExpressedIn: Gene - CellLine
4. targetsGene: SuperEnhancer - Gene

**Data Type Properties:**
1. cellName: CellLine - xsd:string
2. chrom: GenomicCoordinate - xsd:string
3. geneSymbol: Gene - xsd:string
4. seId: SuperEnhancer - xsd:string
5. rank: SuperEnhancer - xsd:float
6. start: GenomicCoordinate - xsd:float
7. stop: GenomicCoordinate - xsd:float