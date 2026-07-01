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
5. rank: Numerical - rank of the super-enhancer - 45.0 to 1247.0
6. start: Numerical - start coordinate of the genomic region - 49148.0 to 187454355.0
7. stop: Numerical - stop coordinate of the genomic region - 60599.0 to 187468841.0

**classes:**
1. GeneticElement
2. GenomicCoordinate
3. CellLine
4. Gene
5. SuperEnhancer

**subclasses:**
1. Enhancer: subclass of -> GeneticElement

**Object Properties:**
1. hasGenomicCoordinate: GeneticElement - GenomicCoordinate
2. isLocatedIn: GenomicCoordinate - CellLine
3. targetsGene: GeneticElement - Gene
4. hasRank: SuperEnhancer - xsd:integer

**Data Type Properties:**
1. cellName: CellLine - xsd:string
2. chromosome: GenomicCoordinate - xsd:string
3. geneSymbol: Gene - xsd:string
4. seId: SuperEnhancer - xsd:string
5. rankValue: SuperEnhancer - xsd:integer
6. startCoordinate: GenomicCoordinate - xsd:integer
7. stopCoordinate: GenomicCoordinate - xsd:integer