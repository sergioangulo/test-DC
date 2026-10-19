# 04.03 · `get_eligible_options(trip_context)` — opciones candidatas

- **Fuente en el PDF:** `SRC-03-02` (p. 3) · **Contrato:** `SRC-02-01` — *Lectura · "Entrega opciones candidatas, no una decisión final."*
- Severidades: ver `01_get_trip_context.md`.

## 1. Ejemplo tal cual (literal del PDF)
```json
get_eligible_options(trip_context)
{
  "options": [
    { "option_id": "O1", "type": "REBOOK", "flight_number": "LA2412",
      "origin": "LIM", "destination": "MEX", "date": "2026-09-16",
      "departure": "08:15", "fare_difference": 0, "seats_available": 4,
      "policy_ref": "POL-DELAY-2026-03", "confidence": "HIGH" },
    { "option_id": "O2", "type": "REBOOK", "flight_number": "LA2450",
      "origin": "LIM", "destination": "MEX", "date": "2026-09-15",
      "departure": "23:40", "fare_difference": 180000, "currency": "CLP",
      "seats_available": 1,
      "policy_ref": "POL-DELAY-2026-03", "confidence": "MEDIUM" },
    { "option_id": "O3", "type": "REFUND",
      "policy_ref": "POL-REFUND-2026-01", "confidence": "LOW" }
  ],
  "_meta": { "retrieved_at": "2026-09-15T11:02:35Z", "ttl_seconds": 120 }
}
```

## 2. Diccionario de campos
| Campo | Tipo / formato | O1 | O2 | O3 | Qué se sabe | Qué **no** se sabe | Cuidado |
|---|---|---|---|---|---|---|---|
| `option_id` | string `O<n>` | `O1` | `O2` | `O3` | Id **dentro de esta respuesta**. | Si es estable entre llamadas. | `DAT-44` |
| `type` | enum | `REBOOK` | `REBOOK` | `REFUND` | Tipo de solución. | Otros tipos (¿`HOTEL`, `MEAL`, `COMPENSATION`, `HUMAN`?). | `DAT-37` |
| `flight_number` | string | `LA2412` | `LA2450` | — | Vuelo de reemplazo. | Operador real, si es código compartido. | Solo en `REBOOK` (**esquema heterogéneo por tipo**) |
| `origin` → `destination` | IATA | `LIM→MEX` | `LIM→MEX` | — | Reemplazan **S2** (el tramo que se pierde). | **A qué segmento original** reemplazan (se infiere). | `DAT-43` |
| `date` | ISO fecha | `2026-09-16` | `2026-09-15` | — | Fecha de salida. | Fecha de llegada. | O1 implica **pernocte en Lima** (`DAT-39`) |
| `departure` | `HH:MM` sin zona | `08:15` | `23:40` | — | Hora de salida (local de LIM, se asume). | **Hora de llegada** a MEX. | No se puede calcular el retraso total de llegada |
| `fare_difference` | entero | `0` | `180000` | — | Diferencia tarifaria (se asume por el cambio). | Por pasajero o total; signo; qué cubre. | `DAT-32` |
| `currency` | string ISO | — (ausente) | `CLP` | — | Solo cuando hay monto. | Moneda cuando `fare_difference == 0`. | `DAT-40` |
| `seats_available` | entero | `4` | `1` | — | Cupos del vuelo para esa opción. | Si es por cabina; cuánto dura. | `DAT-31` |
| `policy_ref` | string `POL-<ESCENARIO>-<AAAA>-<NN>` | `POL-DELAY-2026-03` | `POL-DELAY-2026-03` | `POL-REFUND-2026-01` | Política que respalda. | Si `POL-REFUND-…` existe/está vigente. | `DAT-34` |
| `confidence` | enum | `HIGH` | `MEDIUM` | `LOW` | Una gradación. | **De qué** (elegibilidad, disponibilidad, encaje con la política). | `DAT-36` |
| `_meta.retrieved_at` | ISO UTC | `11:02:35Z` | | | Momento de recuperación. | — | |
| `_meta.ttl_seconds` | entero | `120` | | | Vigencia de **toda** la respuesta. | Si algún asiento se retiene durante el TTL. | `DAT-35` |

## 3. Relaciones dentro de la respuesta (invariantes verificables)
| # | Invariante | Resultado |
|---|---|---|
| I-1 | Toda `REBOOK` tiene `flight_number`, `origin`, `destination`, `date`, `departure` | ✔ O1, O2 · O3 es `REFUND` (otro esquema) |
| I-2 | `fare_difference == 0` ⇒ coherente con `REBOOK_NO_FEE` | O1 ✔ · **O2 ✘** (180000 CLP) |
| I-3 | `fare_difference > 0` ⇒ existe `currency` | ✔ (O2 = CLP) · para `0` no hay `currency` |
| I-4 | `seats_available ≥ n.º de pasajeros` (aquí **2**) | O1 ✔ (4) · **O2 ✘ (1)** |
| I-5 | `policy_ref` coincide con la **versión recuperada** y **no** está en `superseded_versions` | O1/O2 ✔ (`POL-DELAY-2026-03`) · **O3 sin verificar** (`POL-REFUND-2026-01` no se recuperó) |
| I-6 | La opción es **posterior** a la nueva llegada de S1 (conexión factible) | O1 ✔ (día siguiente) · O2 ✔ en teoría: S1 llegaría ~20:35 y O2 sale 23:40 (**margen 3 h 05**, sin MCT disponible) |
| I-7 | `ttl_seconds` ⇒ validez hasta `11:02:35Z + 120 s = 11:04:35Z` | Ventana de **2 minutos** |
| I-8 | `confidence` ordena `HIGH > MEDIUM > LOW` y las opciones vienen ordenadas así | ✔ (¿es un orden de **preferencia**? **No se declara**) |

## 4. Lo que llama la atención

### DAT-31 · O2 tiene **1 cupo para 2 pasajeros** — `CRÍTICA`
La reserva tiene un adulto y un niño de 7 años. Ofrecer u ejecutar O2 implicaría **separar** al menor de su acompañante, o no poder rebookear a ambos. Las políticas de la aerolínea prevén que los **menores de 14** viajen en asientos contiguos a un adulto de su reserva (`POL-CL-13`) y varias normas protegen menores (`POL-PE-09`, `POL-CO-06`).
**Cuidado:** una opción solo es viable si `seats_available ≥ pasajeros a rebookear`; **no ofrecer** opciones parciales sin intervención humana (`GAP-20`, `DEC-16`, `DEC-17`).

### DAT-32 · O2 cuesta 180.000 CLP pero el derecho es "sin costo" — `ALTA`
`R3` (conexión perdida) da `REBOOK_NO_FEE`. Una opción con diferencia tarifaria **contradice** ese derecho: o es una opción **no cubierta** por la política (p. ej. otra cabina/tarifa), o es un dato erróneo. No se sabe si el monto es por pasajero o total.
**Cuidado:** **nunca** presentar O2 como "sin costo"; no incluir montos sin moneda y sin aclarar la base (`DEC-17`).

### DAT-33 · O3 (reembolso) es un cascarón — `ALTA`
Sin monto, plazo ni medio de pago; `confidence: LOW`; y la tarifa dice `refundable: false`. Aun así, el derecho a devolución por disrupción **existe** en las políticas de la aerolínea (`POL-CL-07`, `POL-UY-03`; y "**siempre** devolución de tasas": `POL-CL-16`) y en la Decisión 619 (**art. 11**, plazo de **5 días hábiles**: `POL-PE-10`). Pero el PDF **no tiene regla de reembolso** (`GAP-04`).
**Cuidado:** no prometer monto ni plazo; mencionar que existe la vía y **escalar** (`DEC-28`).

### DAT-34 · `policy_ref` es un puntero que hay que **verificar** — `ALTA`
- O1/O2 apuntan a `POL-DELAY-2026-03`, la **misma versión** que devolvió `get_policy_rules("DELAY")` y que **no** está superseded ✔.
- O3 apunta a `POL-REFUND-2026-01`, que **no se recuperó** en ningún ejemplo.
- `notify_passenger` **rechaza** mensajes sin `policy_ref` (`SRC-04-03`).
**Cuidado:** un `policy_ref` solo "respalda" si coincide con una política **recuperada y vigente** en el momento de decidir; si no, **no usarlo** para sostener un mensaje.

### DAT-35 · TTL de 120 s: las opciones envejecen más rápido que cualquier flujo humano — `ALTA`
Vigencia hasta `11:04:35Z`. La solicitud de rebooking (si se creara justo ahí) vence a las `11:12:00Z` (`SRC-03-04`) y el caso humano tiene un SLA de **45 min** (`SRC-04-02`). Una aprobación humana tardará **más** que el TTL → habrá que **recuperar de nuevo** y revalidar cupos antes de escribir (`GAP-25`, `DEC-19`).
**Cuidado:** el mensaje al pasajero debe reflejar "opciones sujetas a disponibilidad"; la acción de escritura siempre sobre opciones **recién recuperadas**.

### DAT-36 · `confidence` no tiene definición — `MEDIA`
¿Probabilidad de que la política aplique? ¿De que haya cupo? ¿De que el pasajero la acepte? Como no está definida, **no** debe usarse como probabilidad ni para decidir automáticamente (`SRC-02-01`: "no una decisión final").
**Cuidado:** tratarla como **señal de ordenamiento** hasta que se defina (`GAP-17`, `DEC-17`).

### DAT-37 · "Elegible" se calculó con datos **parciales** — `MEDIA`
`get_eligible_options` recibe el `trip_context` que es `PARTIAL` (falta `change_penalty_amount`). Una opción "elegible" podría serlo **solo bajo supuestos** que el servicio no declara.
**Cuidado:** la elección final es **nuestra** y debe revalidarse contra reglas y contra los datos faltantes.

### DAT-38 · Entrada con PII completa — `MEDIA`
La firma exige pasar el `trip_context` entero (con email, teléfono, documento). Si se simula con un mock, se podría pasar una versión **reducida**, pero "mantén estos contratos" (`SRC-01-16`) lo desaconseja (`DAT-02`, `DEC-22`).

### DAT-39 · O1 obliga a **pernoctar** en Lima — `MEDIA`
O1 sale `08:15` del **día siguiente**. Si la nueva llegada a Lima es ~20:35, la pasajera y su hijo de 7 años pasarían la noche. Las normas dan derecho a **alojamiento y traslados** en ese caso (Chile: `POL-CL-04`; Decisión 619 art. 8 c: `POL-PE-07`), pero **las reglas del PDF no tienen regla de alojamiento** (`GAP-03`). Además la opción **no trae hora de llegada** a MEX.
**Cuidado:** el mensaje debe reconocer el pernocte y **escalar** el alojamiento a humano (`DEC-27`).

### DAT-40 · Moneda y formato del monto — `MEDIA`
`180000` es entero CLP (sin decimales); `currency` aparece **solo** cuando hay monto. Formatear con separador y moneda; no usar `float`.

### DAT-41 · No hay cabina ni clase — `MEDIA`
Las políticas comerciales exigen "**misma cabina**"; la opción no la declara (`DAT-08`, `GAP-20`).

### DAT-42 · Coincidencia 23:40 — `BAJA`
`O2.departure = 23:40` coincide con `S2.scheduled_arrival = 23:40`. **No hay relación** entre ambos; es una coincidencia del ejemplo. No unir por hora.

### DAT-43 · Las opciones son de la reserva, no por pasajero ni por segmento — `MEDIA`
No indican qué pasajeros cubren ni qué segmento reemplazan (se deduce que **S2**, por origen/destino). Si el sistema necesita rebookear solo a algunos, la tool **no lo modela** (`DAT-62`).

### DAT-44 · `option_id` local — `BAJA`
`O1` de hoy puede no ser `O1` mañana. La llave idempotente del rebooking debe incluir vuelo/fecha/versión de política y no depender solo de `option_id` (`DAT-63`).

## 5. Cuidados (resumen operativo)
1. Viabilidad = `seats_available ≥ pasajeros` **y** consistencia con la política (`DAT-31`, `DAT-32`).
2. No presentar montos sin moneda/base; no llamar "gratis" lo que tiene diferencia tarifaria (`DAT-32`, `DAT-40`).
3. `policy_ref` solo sostiene un mensaje si es una política **recuperada y vigente** (`DAT-34`).
4. Revalidar siempre las opciones **justo antes** de escribir (`DAT-35`).
5. `confidence` no es probabilidad (`DAT-36`).
6. Las opciones **no** son la decisión (`SRC-02-01`).
