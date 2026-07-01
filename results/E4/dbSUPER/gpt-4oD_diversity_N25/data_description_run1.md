**Foundational Prefix:**
https://base_ontology.com#
http://www.w3.org/1999/02/22-rdf-syntax-ns#
http://www.w3.org/2000/01/rdf-schema#
http://www.w3.org/2004/02/skos/core#
http://www.w3.org/2001/XMLSchema#
http://www.w3.org/2002/07/owl#

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
1. CellLine: subclass of -> Biosample
2. SuperEnhancer: subclass of -> Enhancer

**Object Properties:**
1. hasChromosome: SuperEnhancer - Chromosome
2. targetsGene: SuperEnhancer - Gene
3. locatedIn: SuperEnhancer - GenomicRegion
4. derivedFrom: SuperEnhancer - CellLine

**Data Type Properties:**
1. cellName: CellLine - string
2. chromName: Chromosome - string
3. geneSymbol: Gene - string
4. seId: SuperEnhancer - string
5. rankValue: SuperEnhancer - float
6. startCoordinate: GenomicRegion - float
7. stopCoordinate: GenomicRegion - float