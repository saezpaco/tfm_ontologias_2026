**Foundational Prefix:**
https://base_ontology.com#
http://www.w3.org/1999/02/22-rdf-syntax-ns#
http://www.w3.org/2000/01/rdf-schema#
http://www.w3.org/2004/02/skos/core#
http://www.w3.org/2001/XMLSchema#
http://www.w3.org/2002/07/owl#

**Data Description:**
1. cell_name: text - name of the cell line or biosample - unique values
2. chrom: text - chromosome identifier - unique values
3. gene_symbol: text - symbol of the target gene - unique values
4. se_id: text - identifier for the super-enhancer - unique values
5. rank: Numerical - rank of the super-enhancer - 20.0 to 1079.0
6. start: Numerical - start coordinate of the genomic region - 1088778.0 to 235489531.0
7. stop: Numerical - stop coordinate of the genomic region - 1110655.0 to 235500911.0

**classes:**
1. CellLine
2. Chromosome
3. Gene
4. SuperEnhancer
5. GenomicRegion

**subclasses:**
1. Enhancer: subclass of -> GenomicRegion

**Object Properties:**
1. hasChromosome: SuperEnhancer - Chromosome
2. targetsGene: SuperEnhancer - Gene
3. foundInCellLine: SuperEnhancer - CellLine
4. hasGenomicRegion: SuperEnhancer - GenomicRegion

**Data Type Properties:**
1. cellName: CellLine - xsd:string
2. chromName: Chromosome - xsd:string
3. geneSymbol: Gene - xsd:string
4. seId: SuperEnhancer - xsd:string
5. rankValue: SuperEnhancer - xsd:float
6. startCoordinate: GenomicRegion - xsd:long
7. stopCoordinate: GenomicRegion - xsd:long