# 04.04 · `get_policy_rules("DELAY")` — reglas de política

- **Fuente en el PDF:** `SRC-03-03` (p. 3) · **Contrato:** `SRC-02-02` — *Lectura · "Reglas versionadas y verificables."*
- Severidades: ver `01_get_trip_context.md`.

## 1. Ejemplo tal cual (literal del PDF)
```json
get_policy_rules("DELAY")
{
  "scenario": "DELAY", "version": "POL-DELAY-2026-03",
  "effective_from": "2026-03-01",
  "rules": [
    { "rule_id": "R1", "condition": "delay_minutes >= 180",
      "entitlement": "REBOOK_NO_FEE",   "requires_human_approval": false },
    { "rule_id": "R2", "condition": "delay_minutes >= 240 AND international",
      "entitlement": "MEAL_VOUCHER",    "requires_human_approval": false },
    { "rule_id": "R3", "condition": "missed_connection == true",
      "entitlement": "REBOOK_NO_FEE",   "requires_human_approval": false },
    { "rule_id": "R4", "condition": "compensation_requested == true",
      "entitlement": "CASH_COMPENSATION","requires_human_approval": true },
    { "rule_id": "R5", "condition": "group_includes_minor == true",
      "entitlement": "PRIORITY_HANDLING","requires_human_approval": true }
  ],
  "_meta": { "retrieved_at": "2026-09-15T11:02:36Z",
             "superseded_versions": ["POL-DELAY-2025-11"] }
}
```

## 2. Diccionario de campos
| Campo | Tipo / formato | Valor | Qué se sabe | Qué **no** se sabe | Cuidado |
|---|---|---|---|---|---|
| `scenario` | string (parámetro de entrada) | `DELAY` | Escenario consultado. | **Lista de escenarios** posibles (¿`CANCELLATION`, `ADVANCE`, `REFUND`, `DENIED_BOARDING`?). | `DAT-50` |
| `version` | `POL-<ESC>-<AAAA>-<NN>` | `POL-DELAY-2026-03` | Versión vigente. | Si la versión es global o por país/aerolínea. | `DAT-51`, `DAT-53` |
| `effective_from` | ISO fecha | `2026-03-01` | Desde cuándo rige. | `effective_to`; **qué fecha** se compara (compra, vuelo, evento). | `DAT-57` |
| `rules[]` | array | 5 reglas | Reglas evaluables. | Orden de evaluación; si es **OR** entre reglas o jerarquía. | `DAT-47` |
| `rule_id` | `R<n>` | `R1…R5` | Identificador estable de regla. | Si es estable entre versiones. | Registrar `version + rule_id` en auditoría |
| `condition` | **string** con mini-lenguaje | ver abajo | Predicado. | **Gramática** (solo se ven `>=`, `==`, `AND`; sin `OR`, `NOT`, paréntesis). | `DAT-48` |
| `entitlement` | enum | `REBOOK_NO_FEE`, `MEAL_VOUCHER`, `CASH_COMPENSATION`, `PRIORITY_HANDLING` | Derecho que otorga. | Definición, monto, duración, alcance. | `DAT-52` |
| `requires_human_approval` | boolean | `false`/`true` | Si el derecho exige aprobación humana. | **Quién** aprueba, **qué** se aprueba (el derecho, o la acción), plazo. | `DAT-47`, `DAT-56` |
| `_meta.retrieved_at` | ISO UTC | `11:02:36Z` | Recuperación. | — | `DAT-58` |
| `_meta.superseded_versions` | array | `["POL-DELAY-2025-11"]` | Versiones reemplazadas. | Si pueden seguir apareciendo en opciones/eventos antiguos. | `DAT-53` |

## 3. Las reglas, una por una (con las variables que necesitan)
| Regla | Condición | Variables | ¿Están en los datos? | Derecho | Aprobación |
|---|---|---|---|---|---|
| **R1** | `delay_minutes >= 180` | `delay_minutes` | **Sí**: `E-1001.delay_minutes` (160) | `REBOOK_NO_FEE` | No |
| **R2** | `delay_minutes >= 240 AND international` | `delay_minutes`, `international` | `delay_minutes` sí · **`international` no existe** | `MEAL_VOUCHER` | No |
| **R3** | `missed_connection == true` | `missed_connection` | **No existe: hay que derivarla** | `REBOOK_NO_FEE` | No |
| **R4** | `compensation_requested == true` | `compensation_requested` | **No existe**: lo aporta el pasajero | `CASH_COMPENSATION` | **Sí** |
| **R5** | `group_includes_minor == true` | `group_includes_minor` | **No existe**: se deriva de `type`/`age` | `PRIORITY_HANDLING` | **Sí** |

**Evaluación del ejemplo (con las derivaciones de `06_Analisis_cruzado §3`):** R1 = **falso** (160 < 180) · R2 = **falso** (160 < 240) · R3 = **verdadero (derivado)** · R4 = **desconocido** (nadie lo pidió) · R5 = **verdadero** (hay un niño).

## 4. Relaciones dentro de la respuesta
| # | Relación | Resultado |
|---|---|---|
| I-1 | `version` ∉ `superseded_versions` | ✔ |
| I-2 | `effective_from ≤` fecha relevante (vuelo `2026-09-15`) | ✔ (`2026-03-01`) |
| I-3 | `R1` y `R3` otorgan el **mismo derecho** por vías distintas (retraso ≥ 180 **o** conexión perdida) | Es un OR implícito por derecho |
| I-4 | Escala de umbrales de `delay_minutes`: 180 (R1) < 240 (R2) | Monótona |
| I-5 | `requires_human_approval` coherente con el riesgo del derecho | R4 (dinero) y R5 (menor) sí; R1/R3 (rebooking) no — **aunque rebookear es "acción de alto impacto"** (`SRC-04-06`) |

## 5. Lo que llama la atención

### DAT-45 · Cuatro de las cinco variables **no existen** en los datos — `CRÍTICA`
`international`, `missed_connection`, `compensation_requested` y `group_includes_minor` **no vienen** en ninguna respuesta. Alguien tiene que definir **cómo se derivan** (`GAP-18`). Cada derivación es una decisión de producto: por ejemplo, `international` ¿por segmento o por reserva?; "menor" ¿`CHILD`, `age < 12`, `age < 18`?
**Cuidado:** cada variable derivada debe quedar **etiquetada como derivada**, con sus supuestos, en el registro de decisión (`06_Analisis_cruzado §4`, `DEC-12`).

### DAT-46 · En el caso base **R1 no se cumple pero R3 sí** — `CRÍTICA`
Leer solo "160 min < 180 → no corresponde nada" sería un **error**. El retraso de 160 min supera la escala de 70 min, así que la conexión se pierde (derivado) y `R3` otorga `REBOOK_NO_FEE`. Además `R5` se activa por el niño. Este es **el** caso que prueba si se combinan reserva + eventos + política (`SRC-04-18`).

### DAT-47 · R3 ("sin aprobación") y R5 ("con aprobación") chocan — `ALTA`
No hay precedencia ni semántica de combinación. Dos lecturas válidas:
- **L1:** cada regla gobierna **su propio derecho**: el rebooking (`R3`) procede solo; la atención prioritaria (`R5`) pasa por humano.
- **L2:** `R5` es una **condición sobre el caso**: con menor en el grupo, **toda** acción de escritura requiere humano.
La L2 es más conservadora (`SRC-01-10`, `SRC-04-06`). **No hay dato que dirima** (`GAP-19`) → `DEC-13`, `DEC-16`.

### DAT-48 · `condition` es texto: no se evalúa con `eval` — `ALTA`
Evaluar cadenas de otra fuente con un intérprete es un riesgo de **inyección** si el servicio de políticas fuera comprometido, y hay una gramática **no definida**. Hay que usar un **parser acotado** o **mapear** cada `rule_id`+`version` a un predicado codificado y fallar seguro si aparece una condición desconocida.
**Cuidado:** condición no reconocida ⇒ **humano**, nunca "no aplica" (`DEC-12`).

### DAT-49 · Las reglas no tienen **causa** — `ALTA`
No existe "salvo fuerza mayor/clima". Las normas externas sí (`POL-CL-01`, `POL-PE-06`, `POL-CO-03`, `POL-UE-03`). El motor del PDF otorgaría derechos que algunas leyes niegan, o viceversa (`GAP-06`, `DEC-30`).

### DAT-50 · No hay reglas de reembolso, alojamiento, comunicación ni cuantía; solo `DELAY` — `ALTA`
El **único** escenario mostrado es `DELAY`; `O3` cita `POL-REFUND-2026-01`, que no se ve. No hay regla de **cancelación**, **adelanto**, **sobreventa**, **alojamiento** (aunque `O1` obliga a pernoctar), **comunicación**, ni **montos de compensación** (`R4` es solo una bandera). (`GAP-03`, `GAP-04`, `GAP-05`, `GAP-07`.)

### DAT-51 · No hay jurisdicción — `ALTA`
Las normas externas **dependen del país de origen del vuelo** (Chile para S1; Perú para S2; `POL-CL-00`, `POL-PE-01`). La política del ejemplo no dice país, aerolínea ni segmento (`GAP-01`, `DEC-25`).

### DAT-52 · Los "derechos" son etiquetas sin significado — `MEDIA`
`PRIORITY_HANDLING`, `MEAL_VOUCHER`, `CASH_COMPENSATION`: sin definición, monto, vigencia ni forma de entrega. Un mensaje al pasajero con detalle sería **invención** (`GAP-19`).

### DAT-53 · Versionado: fijar la versión usada — `MEDIA`
`superseded_versions` muestra que hay historia. Debe **fijarse** (pin) la versión usada en la decisión y guardarla en la auditoría; una opción cuyo `policy_ref` esté superseded no debe sostener un mensaje.

### DAT-54 · `delay_minutes`: ¿de qué segmento, medido dónde y con qué borde? — `MEDIA`
`R1` usa `>= 180` (inclusivo). ¿Por segmento o por reserva? ¿Salida o llegada? ¿Redondeo? 179 ≠ 180 cambia el derecho.
**Cuidado:** pruebas en los bordes 179/180 y 239/240 (`06_Analisis_cruzado §9`).

### DAT-55 · R2 es **más exigente** que varias normas externas — `MEDIA`
`R2` da vale de comida a **≥ 240 min y solo internacional**. Con 160 min: **sin vale** según el PDF; pero Chile da alimentación con espera **> 2 h** (`POL-CL-01`) y la Decisión 619 da refrigerio **> 2 h** y comida **> 4 h** (`POL-PE-07`). El caso base cae **entre** ambas (`GAP-03`, `DEC-27`).

### DAT-56 · `requires_human_approval` sin quién ni cuándo — `BAJA`
Solo un booleano. No hay rol aprobador, SLA, ni si la aprobación es **previa** o **posterior** a notificar.

### DAT-57 · Sin `effective_to` ni país — `BAJA`
Sin fin de vigencia; no se sabe qué fecha manda (compra, vuelo, evento).

### DAT-58 · La política puede cambiar entre lectura y acción — `MEDIA`
Recuperada a `11:02:36Z`. Si el flujo incluye aprobación humana (SLA 45 min), puede haber una versión nueva al momento de actuar.
**Cuidado:** re-verificar `version` antes de escribir.

## 6. Cuidados (resumen operativo)
1. No usar `eval`; mapear/validar condiciones; desconocida ⇒ humano (`DAT-48`).
2. Registrar `version + rule_id + variables derivadas` en la auditoría (`DAT-53`).
3. Probar los bordes (179/180, 239/240) (`DAT-54`).
4. No inventar contenido para derechos sin definición (`DAT-52`).
5. Jurisdicción y causa son **dimensiones ausentes** de las reglas (`DAT-49`, `DAT-51`).
