# Core semántico común entre BBDD — análisis intra-modelo

_Las cuatro BBDD comparten esquema columnar tras pre-procesado: 30 columnas canónicas (CRM_ID, coordenadas, score, biosample, target genes, TFs, disease, mutation). La pregunta de la sugerencia 1 es si el LLM modela las mismas clases / propiedades para las cuatro BBDD dentro de un mismo (experimento × modelo). Métrica: Jaccard pareado de los conjuntos de URIs (excluidos rdf/rdfs/owl/xsd)._

| Experimento | Modelo | n pares | Jaccard medio | Jaccard min | Jaccard max | Interpretación |
|---|---|---|---|---|---|---|
| E1 | gpt-4o_A_head | 1 | 0.148 | 0.148 | 0.148 | divergente |
| E1 | gpt-4o_B_random | 1 | 0.100 | 0.100 | 0.100 | divergente |
| E1 | gpt-4o_C_stratified | 1 | 0.115 | 0.115 | 0.115 | divergente |
| E1 | gpt-4o_D_diversity | 1 | 0.087 | 0.087 | 0.087 | divergente |
| E1 | llama3.1_8b_A_head | 1 | 0.056 | 0.056 | 0.056 | divergente |
| E1 | llama3.1_8b_B_random | 1 | 0.143 | 0.143 | 0.143 | divergente |
| E1 | llama3.1_8b_C_stratified | 1 | 0.067 | 0.067 | 0.067 | divergente |
| E1 | llama3.1_8b_D_diversity | 1 | 0.171 | 0.171 | 0.171 | divergente |
| E3 | gpt-4o_legacy | 18 | 0.518 | 0.429 | 0.614 | consistente |
| E3 | gpt-4o_ragapi | 18 | 0.209 | 0.119 | 0.433 | divergente |
| E3 | llama3.1_8b_legacy | 18 | 0.845 | 0.569 | 1.000 | muy consistente |
| E3 | llama3.1_8b_ragapi | 18 | 0.186 | 0.078 | 0.350 | divergente |
| E3 | llama3.1_8b_ragapi_C1 | 18 | 0.268 | 0.184 | 0.371 | divergente |
| E3 | llama3.1_8b_ragapi_C2 | 18 | 0.106 | 0.065 | 0.217 | divergente |
| E3 | llama3.1_8b_ragapi_C3 | 18 | 0.235 | 0.088 | 0.394 | divergente |
| E4 | gpt-4o_A_head | 1 | 0.114 | 0.114 | 0.114 | divergente |
| E4 | gpt-4o_B_random | 1 | 0.105 | 0.105 | 0.105 | divergente |
| E4 | gpt-4o_C_stratified | 1 | 0.108 | 0.108 | 0.108 | divergente |
| E4 | gpt-4o_D_diversity | 1 | 0.114 | 0.114 | 0.114 | divergente |
| E4 | llama3.1_8b | 18 | 0.333 | 0.000 | 1.000 | parcial |