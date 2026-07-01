**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. cell_name: type - text - short description of the cell line or biosample - possible range: any textual identifier for a cell line or biosample
2. chrom: type - text - chromosome number - possible range: any textual identifier for a chromosome (e.g., "chr1", "chr2")
3. gene_symbol: type - text - target gene symbol - possible range: any valid gene symbol from the genome
4. se_id: type - text - unique identifier for an enhancer or super-enhancer - possible range: any textual identifier for an enhancer or super-enhancer
5. rank: type - Numerical - rank of the enhancer or super-enhancer - possible range: any numerical value indicating the rank
6. start: type - Numerical - genomic start position of the enhancer or super-enhancer - possible range: any numerical value representing a genomic position
7. stop: type - Numerical - genomic stop position of the enhancer or super-enhancer - possible range: any numerical value representing a genomic position

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. CellLineOrBiosample
5. TargetGene
6. TranscriptionFactor
7. DiseaseAssociation

**Subclasses:**
1. SpecificEnhancer: subclass of -> Enhancer
2. SpecificSuperEnhancer: subclass of -> SuperEnhancer

**Object Properties:**
1. hasCellLineOrBiosample: domain - GeneticElement, range - CellLineOrBiosample
2. targetsGene: domain - GeneticElement, range - TargetGene
3. regulatedByTranscriptionFactor: domain - GeneticElement, range - TranscriptionFactor
4. associatedWithDisease: domain - GeneticElement, range - DiseaseAssociation

**Data Type Properties:**
1. cellName: domain - GeneticElement, range - xsd:string
2. chromosome: domain - GeneticElement, range - xsd:string
3. geneSymbol: domain - TargetGene, range - xsd:string
4. enhancerId: domain - Enhancer, range - xsd:string
5. superEnhancerId: domain - SuperEnhancer, range - xsd:string
6. rankValue: domain - GeneticElement, range - xsd:integer
7. startPosition: domain - GeneticElement, range - xsd:integer
8. stopPosition: domain - GeneticElement, range - xsd:integer