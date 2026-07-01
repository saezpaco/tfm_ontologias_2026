**Foundational Prefix:**
https://genetic_regulatory_elements.com#

**Data Description:**
1. cell_name: type - text - short description of the cell line or biosample - possible range: any string representing a cell line or biosample name
2. chrom: type - text - chromosome number - possible range: any string representing a chromosome number (e.g., "chr1", "chr2")
3. gene_symbol: type - text - target gene symbol - possible range: any string representing a gene symbol (e.g., "BRCA1", "EGFR")
4. se_id: type - text - identifier for the super-enhancer - possible range: any string representing a unique identifier
5. rank: type - Numerical - rank of the enhancer or super-enhancer - possible range: any integer between 20 and 1079
6. start: type - Numerical - genomic start position of the element - possible range: any integer between 1,088,778 and 235,489,531
7. stop: type - Numerical - genomic stop position of the element - possible range: any integer between 1,110,655 and 235,500,911

**Classes:**
1. GeneticElement
2. Enhancer
3. SuperEnhancer
4. CellLine
5. TargetGene
6. TranscriptionFactor
7. DiseaseAssociation

**Subclasses:**
1. SpecificEnhancer: subclass of -> Enhancer
2. SpecificSuperEnhancer: subclass of -> SuperEnhancer
3. SpecificCellLine: subclass of -> CellLine
4. SpecificTargetGene: subclass of -> TargetGene
5. SpecificTranscriptionFactor: subclass of -> TranscriptionFactor
6. SpecificDiseaseAssociation: subclass of -> DiseaseAssociation

**Object Properties:**
1. hasGenomicCoordinates: domain - GeneticElement; range - GenomicCoordinates
2. associatedWithCellLine: domain - GeneticElement; range - CellLine
3. targetsGene: domain - Enhancer/SuperEnhancer; range - TargetGene
4. regulatedByTranscriptionFactor: domain - Enhancer/SuperEnhancer; range - TranscriptionFactor
5. associatedWithDisease: domain - GeneticElement; range - DiseaseAssociation

**Data Type Properties:**
1. rankValue: domain - Enhancer/SuperEnhancer; range - xsd:int
2. startPosition: domain - GenomicCoordinates; range - xsd:int
3. stopPosition: domain - GenomicCoordinates; range - xsd:int