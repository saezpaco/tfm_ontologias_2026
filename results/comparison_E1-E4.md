# Comparativa E1–E4: ontologías generadas

Métricas por corrida (ver `comparison_E1-E4.csv`).

## Resumen — output crudo del LLM (raw)

| Exp | DB | runs_ok | n_triples | n_classes | n_obj_props | n_data_props | n_subClassOf | n_labels |
|-----|----|---------|-----------|-----------|-------------|--------------|--------------|----------|
| E1 | FANTOM5 | 2 | 46.0 | 2.5 | 1.0 | 5.5 | 0.0 | 0.0 |
| E1 | dbSUPER | 3 | 55.3 | 5.0 | 3.0 | 4.0 | 0.3 | 0.0 |
| E1 | HACER | 2 | 61.5 | 5.0 | 3.5 | 5.0 | 0.0 | 0.0 |
| E1 | DiseaseEnhancer | 3 | 41.3 | 4.3 | 2.0 | 3.0 | 0.0 | 0.0 |
| E2 | FANTOM5 | 2 | 60.5 | 4.0 | 3.0 | 7.0 | 0.0 | 1.0 |
| E2 | dbSUPER | 3 | 50.0 | 4.0 | 2.7 | 5.0 | 0.0 | 0.7 |
| E2 | HACER | 2 | 51.0 | 4.5 | 3.0 | 3.5 | 0.0 | 0.5 |
| E2 | DiseaseEnhancer | 1 | 62.0 | 5.0 | 4.0 | 8.0 | 0.0 | 0.0 |
| E3 | FANTOM5 | 0 | - | - | - | - | - | - |
| E3 | dbSUPER | 0 | - | - | - | - | - | - |
| E3 | HACER | 0 | - | - | - | - | - | - |
| E3 | DiseaseEnhancer | 0 | - | - | - | - | - | - |
| E4 | FANTOM5 | 3 | 233.0 | 11.3 | 7.3 | 26.0 | 10.3 | 44.7 |
| E4 | dbSUPER | 3 | 236.7 | 9.7 | 5.7 | 27.0 | 11.7 | 42.3 |
| E4 | HACER | 3 | 225.0 | 9.0 | 5.0 | 30.0 | 3.0 | 44.0 |
| E4 | DiseaseEnhancer | 3 | 213.7 | 9.0 | 5.7 | 26.7 | 4.0 | 41.3 |

## Resumen — tras post-procesado (auto-prefix injection)

| Exp | DB | runs_ok | n_triples | n_classes | n_obj_props | n_data_props | n_subClassOf | n_labels |
|-----|----|---------|-----------|-----------|-------------|--------------|--------------|----------|
| E1 | FANTOM5 | 3 | 51.7 | 2.7 | 1.3 | 6.3 | 0.0 | 0.0 |
| E1 | dbSUPER | 3 | 55.3 | 5.0 | 3.0 | 4.0 | 0.3 | 0.0 |
| E1 | HACER | 3 | 61.3 | 4.3 | 3.0 | 6.0 | 0.0 | 0.0 |
| E1 | DiseaseEnhancer | 3 | 41.3 | 4.3 | 2.0 | 3.0 | 0.0 | 0.0 |
| E2 | FANTOM5 | 3 | 66.0 | 4.0 | 3.0 | 7.3 | 0.0 | 1.0 |
| E2 | dbSUPER | 3 | 50.0 | 4.0 | 2.7 | 5.0 | 0.0 | 0.7 |
| E2 | HACER | 3 | 53.7 | 4.7 | 3.3 | 3.7 | 0.0 | 0.7 |
| E2 | DiseaseEnhancer | 3 | 99.0 | 4.3 | 3.3 | 4.7 | 0.0 | 0.3 |
| E3 | FANTOM5 | 3 | 37.0 | 1.3 | 0.0 | 0.0 | 1.3 | 0.0 |
| E3 | dbSUPER | 3 | 25.7 | 1.3 | 0.0 | 0.0 | 1.3 | 0.0 |
| E3 | HACER | 3 | 55.0 | 2.3 | 0.0 | 0.0 | 2.3 | 0.0 |
| E3 | DiseaseEnhancer | 3 | 53.3 | 2.0 | 0.0 | 0.0 | 2.0 | 0.0 |

## Diferencial: ¿cuántas ontologías se rescatan con el fix?

| Exp | DB | runs_ok (raw) | runs_ok (post-fix) | rescued |
|-----|----|---------------|--------------------|---------|
| E1 | FANTOM5 | 2/3 | 3/3 | +1 |
| E1 | dbSUPER | 3/3 | 3/3 | +0 |
| E1 | HACER | 2/3 | 3/3 | +1 |
| E1 | DiseaseEnhancer | 3/3 | 3/3 | +0 |
| E2 | FANTOM5 | 2/3 | 3/3 | +1 |
| E2 | dbSUPER | 3/3 | 3/3 | +0 |
| E2 | HACER | 2/3 | 3/3 | +1 |
| E2 | DiseaseEnhancer | 1/3 | 3/3 | +2 |
| E3 | FANTOM5 | 0/3 | 3/3 | +3 |
| E3 | dbSUPER | 0/3 | 3/3 | +3 |
| E3 | HACER | 0/3 | 3/3 | +3 |
| E3 | DiseaseEnhancer | 0/3 | 3/3 | +3 |
