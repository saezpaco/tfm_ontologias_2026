**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. cell_name: type - text - short description of the cell line or biosample - possible range: any textual identifier for a cell line or biosample
2. chrom: type - text - chromosome number - possible range: any textual identifier for a chromosome (e.g., "chr1", "chr2")
3. gene_symbol: type - text - target gene symbol - possible range: any valid gene symbol from the genome
4. se_id: type - text - super-enhancer identifier - possible range: any unique identifier for a super-enhancer
5. rank: type - Numerical - rank of the enhancer or super-enhancer - possible range: any numerical value indicating the rank
6. start: type - Numerical - genomic start position - possible range: any numerical value representing a genomic coordinate
7. stop: type - Numerical - genomic stop position - possible range: any numerical value representing a genomic coordinate

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. CellLine
5. TargetGene
6. TranscriptionFactor
7. DiseaseAssociation

**Subclasses:**
1. Enhancer: subclass of -> GeneticElement
2. SuperEnhancer: subclass of -> Enhancer
3. CellLine: subclass of -> GeneticElement
4. TargetGene: subclass of -> GeneticElement
5. TranscriptionFactor: subclass of -> GeneticElement
6. DiseaseAssociation: subclass of -> GeneticElement

**Object Properties:**
1. hasCellLine: domain - GeneticElement; range - CellLine
2. targetsGene: domain - Enhancer/SuperEnhancer; range - TargetGene
3. regulatedByTranscriptionFactor: domain - Enhancer/SuperEnhancer; range - TranscriptionFactor
4. associatedWithDisease: domain - GeneticElement; range - DiseaseAssociation

**Data Type Properties:**
1. cellName: domain - GeneticElement; range - xsd:string
2. chromosome: domain - GeneticElement; range - xsd:string
3. geneSymbol: domain - TargetGene; range - xsd:string
4. superEnhancerID: domain - SuperEnhancer; range - xsd:string
5. rankValue: domain - Enhancer/SuperEnhancer; range - xsd:integer
6. startPosition: domain - GeneticElement; range - xsd:integer
7. stopPosition: domain - GeneticElement; range - xsd:integer