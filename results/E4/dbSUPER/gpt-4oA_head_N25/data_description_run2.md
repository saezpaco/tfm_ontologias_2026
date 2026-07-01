**Foundational Prefix:**
@prefix base: <https://base_ontology.com#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

**Data Description:**
1. cell_name: categorical - name of the cell line or biosample - single value
2. chrom: text - chromosome identifier - multiple values
3. gene_symbol: text - symbol of the gene - multiple values
4. se_id: text - identifier for super-enhancer - single value
5. rank: Numerical - rank of the super-enhancer - range: 1 to 25
6. start: Numerical - start position of the genomic coordinate - range: 12327760 to 218548183
7. stop: Numerical - stop position of the genomic coordinate - range: 12522419 to 218895526

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
2. isLocatedIn: GenomicCoordinate - Chromosome
3. isExpressedIn: Gene - CellLine
4. targetsGene: SuperEnhancer - Gene

**Data Type Properties:**
1. cellName: CellLine - xsd:string
2. chrom: Chromosome - xsd:string
3. geneSymbol: Gene - xsd:string
4. seId: SuperEnhancer - xsd:string
5. rank: SuperEnhancer - xsd:integer
6. start: GenomicCoordinate - xsd:integer
7. stop: GenomicCoordinate - xsd:integer