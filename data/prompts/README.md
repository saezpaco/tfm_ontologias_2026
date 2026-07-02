# Prompts del banco E1–E3 · variantes evaluadas y plantilla fijada

Este directorio recoge de forma trazable el proceso de ingeniería de prompts
documentado en §3.5.1 de la memoria («Selección del prompt óptimo»), evitando
que los detalles queden únicamente en el historial git de
`scripts/run_gpt_experiments.py`.

## Contexto

Antes de fijar la plantilla del banco principal se compararon cuatro variantes
del prompt de la categoría I (E1 zero-shot y E2 vocabulario controlado) con
`gpt-4o-mini` sobre `dbSUPER`, variando cuatro ejes:

1. **Orden**: lista de pasos ANTES vs DESPUÉS de la muestra CSV.
2. **Cadena de razonamiento**: presencia u omisión de la directiva
   «Think step by step».
3. **Prefijos canónicos**: lista de `@prefix` a exigir en la salida.
4. **Formato de salida**: Turtle plano vs Turtle + explicación.

La combinación ganadora —lista antes del CSV, chain-of-thought presente,
prefijos rdf/rdfs/owl/skos/xsd/obo, sólo Turtle— elevó la tasa de parse-OK
nativo de gpt-4o-mini del 0 % al 83 % en dbSUPER, y se fijó como plantilla
del banco principal.

## Ficheros

| Fichero                              | Rol                                                        |
| ------------------------------------ | ---------------------------------------------------------- |
| `system_prompt.txt`                  | System prompt común a E1–E3, versión fijada.              |
| `E1_final.prompt`                    | Plantilla ganadora E1 (zero-shot). En uso en el banco.     |
| `E1_variant_A_lista_despues.prompt`  | Variante rechazada: lista de pasos DESPUÉS del CSV.        |
| `E1_variant_B_sin_cot.prompt`        | Variante rechazada: sin directiva «Think step by step».    |
| `E1_variant_C_con_explicacion.prompt`| Variante rechazada: pide explicación + Turtle.             |

Las variantes se guardan por completitud del razonamiento del §3.5.1, no
por uso en producción. La única plantilla realmente empleada en el banco
principal es `E1_final.prompt` (y su derivada E2 en el propio script).

## Trazabilidad

- Fuente autoritativa en producción: constantes `SYSTEM_PROMPT`,
  `USER_PROMPT_E1`, `USER_PROMPT_E2` y `USER_PROMPT_E3` en
  `scripts/run_gpt_experiments.py`.
- Historial git del script: `git log -p scripts/run_gpt_experiments.py` en
  el repositorio del TFM.
- Este directorio es la instantánea consolidada, legible sin ejecutar
  código ni consultar el historial.
