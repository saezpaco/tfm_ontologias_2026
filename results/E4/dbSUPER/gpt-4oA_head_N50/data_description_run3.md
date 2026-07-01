**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. cell_name: categorical - name of the cell line or biosample - categorical
2. chrom: text - chromosome identifier - text
3. gene_symbol: text - symbol of the target gene - text
4. se_id: text - identifier for the super-enhancer - text
5. rank: Numerical - rank of the super-enhancer - 1 to 50
6. start: Numerical - start coordinate of the genomic region - 1631156 to 218548183
7. stop: Numerical - stop coordinate of the genomic region - 1749787 to 218895526

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
2. isLocatedIn: GenomicCoordinate - CellLine
3. targetsGene: GeneticElement - Gene
4. hasIdentifier: GeneticElement - SuperEnhancer

**Data Type Properties:**
1. cellName: CellLine - xsd:string
2. chromosome: GenomicCoordinate - xsd:string
3. geneSymbol: Gene - xsd:string
4. seIdentifier: SuperEnhancer - xsd:string
5. rank: SuperEnhancer - xsd:integer
6. start: GenomicCoordinate - xsd:integer
7. stop: GenomicCoordinate - xsd:integer