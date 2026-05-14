# Fidelidad cisreg — resumen agregado

_Gold set: 88 URIs canónicas únicas extraídas de las 8 ontologías cisreg de referencia (crm, crm2gene, crm2phen, crm2tfac y sus variantes _example)._

| Experimento | Modelo / variante | n TTL | n_canonical (mean) | n_invented (mean) | canonical_ratio | overlap | Jaccard | Recall vs gold |
|---|---|---|---|---|---|---|---|---|
| E1 | gpt-4o_A_head | 2 | 3.0 | 12.5 | 0.199 | 1.0 | 0.011 | 0.011 |
| E1 | gpt-4o_B_random | 2 | 6.5 | 4.5 | 0.625 | 1.0 | 0.011 | 0.011 |
| E1 | gpt-4o_C_stratified | 2 | 3.0 | 11.5 | 0.213 | 1.0 | 0.011 | 0.011 |
| E1 | gpt-4o_D_diversity | 2 | 2.5 | 10.0 | 0.199 | 1.0 | 0.011 | 0.011 |
| E1 | llama3.1_8b_A_head | 2 | 4.5 | 5.0 | 0.575 | 1.0 | 0.011 | 0.011 |
| E1 | llama3.1_8b_B_random | 2 | 2.0 | 2.0 | 0.500 | 1.0 | 0.011 | 0.011 |
| E1 | llama3.1_8b_C_stratified | 2 | 8.0 | 16.0 | 0.333 | 1.0 | 0.011 | 0.011 |
| E1 | llama3.1_8b_D_diversity | 2 | 26.0 | 15.0 | 0.729 | 1.0 | 0.009 | 0.011 |
| E3 | gpt-4o_N100_ragapi | 6 | 16.5 | 13.833 | 0.546 | 7.333 | 0.073 | 0.083 |
| E3 | gpt-4o_N200_ragapi | 6 | 12.5 | 14.333 | 0.532 | 6.5 | 0.068 | 0.074 |
| E3 | gpt-4o_N25_ragapi | 6 | 12.667 | 11.833 | 0.542 | 6.5 | 0.067 | 0.074 |
| E3 | gpt-4o_N50_ragapi | 6 | 15.333 | 10.833 | 0.581 | 7.0 | 0.070 | 0.080 |
| E3 | gpt-4o_legacy | 12 | 37.917 | 0.0 | 1.000 | 27.583 | 0.279 | 0.313 |
| E3 | gpt-4o_ragapi | 12 | 14.0 | 21.083 | 0.460 | 6.833 | 0.069 | 0.078 |
| E3 | llama3.1_8b_N100_ragapi | 6 | 19.167 | 2.333 | 0.905 | 7.333 | 0.074 | 0.083 |
| E3 | llama3.1_8b_N200_ragapi | 6 | 18.167 | 2.0 | 0.876 | 8.5 | 0.087 | 0.097 |
| E3 | llama3.1_8b_N25_ragapi | 6 | 19.167 | 0.0 | 1.000 | 7.5 | 0.075 | 0.085 |
| E3 | llama3.1_8b_N50_ragapi | 6 | 20.167 | 0.0 | 1.000 | 7.333 | 0.072 | 0.083 |
| E3 | llama3.1_8b_legacy | 12 | 52.833 | 0.0 | 1.000 | 49.583 | 0.543 | 0.563 |
| E3 | llama3.1_8b_ragapi | 12 | 30.333 | 0.917 | 0.974 | 5.583 | 0.050 | 0.063 |
| E3 | llama3.1_8b_ragapi_C1 | 12 | 27.167 | 2.333 | 0.912 | 5.667 | 0.052 | 0.064 |
| E3 | llama3.1_8b_ragapi_C2 | 12 | 29.167 | 0.0 | 1.000 | 6.417 | 0.057 | 0.073 |
| E3 | llama3.1_8b_ragapi_C3 | 12 | 21.583 | 2.083 | 0.925 | 5.0 | 0.047 | 0.057 |
| E4 | gpt-4o_A_head | 2 | 0.0 | 0.0 | 0.000 | 0.0 | 0.000 | 0.000 |
| E4 | gpt-4o_B_random | 2 | 0.0 | 0.0 | 0.000 | 0.0 | 0.000 | 0.000 |
| E4 | gpt-4o_C_stratified | 2 | 0.0 | 0.0 | 0.000 | 0.0 | 0.000 | 0.000 |
| E4 | gpt-4o_D_diversity | 2 | 0.0 | 0.0 | 0.000 | 0.0 | 0.000 | 0.000 |
| E4 | llama3.1_8b | 24 | 0.0 | 14.625 | 0.000 | 0.0 | 0.000 | 0.000 |