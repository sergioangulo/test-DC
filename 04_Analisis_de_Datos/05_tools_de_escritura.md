# 04.05 · Tools de escritura — `create_rebooking_request`, `create_human_case`, `notify_passenger`

- **Fuente en el PDF:** `SRC-03-04` (p. 3) + `SRC-04-01`, `SRC-04-02`, `SRC-04-03` (p. 4) · **Contratos:** `SRC-02-03`, `SRC-02-04`, `SRC-02-05`.
- Son las únicas tools que **cambian el mundo**. "Cambiar una reserva o emitir una compensación son acciones de alto impacto" (`SRC-04-06`).
- Severidades: ver `01_get_trip_context.md`.

## 1. Ejemplo tal cual (literal del PDF)
```text
Tools de escritura

create_rebooking_request(option, idempotency_key)
  → 201 { "request_id": "RBK-88231", "status": "PENDING_CONFIRMATION",
          "expires_at": "2026-09-15T11:12:00Z" }
  → 409 { "error": "DUPLICATE_REQUEST", "request_id": "RBK-88231" }
  → 503 { "error": "UPSTREAM_TIMEOUT" }   // el resultado real es indeterminado

create_human_case(reason, evidence)
  → 201 { "case_id": "HC-4471", "queue": "DISRUPTION_L2", "sla_minutes": 45 }

notify_passenger(message)
  → 202 { "notification_id": "NT-9912", "channel": "PUSH", "status": "QUEUED" }
  → 422 { "error": "UNVALIDATED_CONTENT", "detail": "falta policy_ref" }
```
> Nota de formato: el comentario `// el resultado real es indeterminado` **no es JSON válido**; es una anotación del documento. No se debe parsear, pero **contiene semántica** (`DAT-67`).

## 2. Diccionario de campos y respuestas

### 2.1 `create_rebooking_request(option, idempotency_key)`
| Elemento | Tipo | Valor | Qué se sabe | Qué **no** se sabe | Cuidado |
|---|---|---|---|---|---|
| **Entrada** `option` | objeto o id | — | Una opción de `get_eligible_options`. | Si se pasa el **objeto completo** o solo `option_id`; **qué pasajeros** cubre; a qué **reserva** se aplica (la opción no trae `booking_id`). | `DAT-62` |
| **Entrada** `idempotency_key` | string | — | Debe evitar duplicados. | Formato, longitud, TTL de la llave, si es por llamada o por operación. | `DAT-63` |
| `201 request_id` | string `RBK-<n>` | `RBK-88231` | Solicitud creada. | Si `RBK-` es estable para consultas posteriores (**no hay tool de consulta**). | `DAT-61` |
| `201 status` | enum | `PENDING_CONFIRMATION` | La solicitud **no está confirmada**. | Estados posteriores y **quién confirma**. | `DAT-61`, `DAT-69` |
| `201 expires_at` | ISO UTC | `2026-09-15T11:12:00Z` | Caduca. | Qué ocurre al caducar. | `DAT-61`, `DAT-68` |
| `409 error` | string | `DUPLICATE_REQUEST` | Ya existe una solicitud con esa llave. | Si la existente está pendiente, caducada o confirmada. | `DAT-60` |
| `409 request_id` | string | `RBK-88231` | **El mismo** id del `201` (repetición idempotente). | — | `DAT-60` |
| `503 error` | string | `UPSTREAM_TIMEOUT` | Falló un sistema aguas arriba. | **El resultado real**: "indeterminado". | `DAT-59` |

### 2.2 `create_human_case(reason, evidence)`
| Elemento | Tipo | Valor | Qué se sabe | Qué **no** se sabe | Cuidado |
|---|---|---|---|---|---|
| **Entrada** `reason` | string/enum | — | Motivo del escalamiento. | Catálogo de motivos. | `DAT-64` |
| **Entrada** `evidence` | ? | — | Evidencia que acompaña. | **Esquema**, tamaño, si admite adjuntos; **sin llave idempotente**. | `DAT-64` |
| `201 case_id` | `HC-<n>` | `HC-4471` | Caso creado. | — | |
| `201 queue` | string | `DISRUPTION_L2` | Cola de nivel 2. | Si existe L1; reglas de ruteo. | `DAT-72` |
| `201 sla_minutes` | entero | `45` | Tiempo objetivo de atención. | Si es de respuesta o de resolución. | `DAT-64`, `GAP-25` |

### 2.3 `notify_passenger(message)`
| Elemento | Tipo | Valor | Qué se sabe | Qué **no** se sabe | Cuidado |
|---|---|---|---|---|---|
| **Entrada** `message` | ? | — | Contenido; **debe llevar `policy_ref`**. | **A quién** (sin pasajero ni reserva en la firma), idioma, formato, longitud, adjuntos. | `DAT-65` |
| `202 notification_id` | `NT-<n>` | `NT-9912` | Notificación aceptada. | — | |
| `202 channel` | enum | `PUSH` | Canal usado. | Otros canales (email/SMS); cómo se elige. | `DAT-71` |
| `202 status` | enum | `QUEUED` | **Encolada**, no entregada. | `SENT`, `DELIVERED`, `FAILED`. | `DAT-65`, `DAT-69` |
| `422 error` | string | `UNVALIDATED_CONTENT` | Contenido no validado. | Qué más valida (solo se ve `policy_ref`). | `DAT-65` |
| `422 detail` | string | `falta policy_ref` | Motivo legible. | Códigos estructurados del motivo. | |

## 3. Relaciones dentro de las respuestas
| # | Relación | Resultado |
|---|---|---|
| I-1 | `409.request_id == 201.request_id` | ✔ — la repetición con la **misma llave** devuelve el **mismo** id |
| I-2 | `expires_at > ahora` ⇒ solicitud vigente | `11:12:00Z` = **9 min 25 s** después de las opciones (`11:02:35Z`) |
| I-3 | `sla_minutes (45) > expires_at − ahora (≈9 min)` | **Conflicto de tiempos** entre humano y solicitud (`DAT-61`, `GAP-25`) |
| I-4 | `notify_passenger` exige `policy_ref` ⇒ coherente con `option.policy_ref` | Un mensaje **sin** política recuperada **no** debe enviarse (`DAT-34`) |
| I-5 | Códigos HTTP por respuesta: `201` (creación), `202` (aceptación asíncrona), `409`, `422`, `503` | Coherentes con su semántica; faltan `400/401/403/404/429/5xx` |

## 4. Lo que llama la atención

### DAT-59 · `503`: el resultado real es **indeterminado** — `CRÍTICA`
El rebooking **puede o no** haberse creado. No hay tool de consulta (`GAP-12`). Reintentar con **otra** llave podría **duplicar** una acción de alto impacto; no reintentar podría dejar al pasajero sin solución.
**Cuidado:** persistir la llave **antes** de llamar; reintentar con la **misma llave** (idempotente) un número acotado de veces; si sigue indeterminado ⇒ `create_human_case`. **No** informar al pasajero ni éxito ni fracaso: "estamos confirmando" (`DEC-18`).

### DAT-60 · `409` es "ya existe", no "falló" — `ALTA`
Debe tratarse como **éxito idempotente** (la solicitud ya existe) y a la vez no se sabe su estado (puede estar caducada). Sin tool de consulta, hay que **suponer pendiente** hasta que expire, y **no entrar en bucle**.
**Cuidado:** mapear `409` a "existente" y registrar el `request_id` devuelto.

### DAT-61 · `PENDING_CONFIRMATION` sin forma de confirmar, consultar ni cancelar — `ALTA`
El enunciado no incluye una tool de **confirmación** ni de **estado**. ¿Confirma el pasajero? ¿Operaciones? ¿Expira sola a las `11:12:00Z`? Si la aprobación humana tarda hasta 45 min, la solicitud **caduca antes**. El ciclo de vida es una **brecha** (`GAP-12`, `GAP-25`).
**Cuidado:** documentar el supuesto (por ejemplo "confirmación fuera de alcance de v1") y no prometer "tu vuelo está cambiado" (`DEC-18`, `DEC-19`).

### DAT-62 · El rebooking no dice **a quién** ni **en qué reserva** — `ALTA`
La llamada recibe `option` e `idempotency_key`; **no** `booking_id`, **no** pasajeros. La opción tampoco trae `booking_id`. El riesgo: rebookear solo a un pasajero (**separar al menor**) o a la reserva equivocada (`GAP-20`, `DAT-43`).
**Cuidado:** en el mock, incluir `booking_id` y `passenger_ids` como **extensión documentada** del contrato (a decidir; `DEC-18`).

### DAT-63 · Diseño de la `idempotency_key` — `ALTA`
Aleatoria por intento ⇒ **no es idempotente**. Debe derivarse de la **operación**: p. ej. hash de `booking_id + option(vuelo+fecha) + policy_version + decisión`. Guardarla **antes** de llamar.
**Cuidado:** misma operación ⇒ misma llave; operación distinta (otra opción) ⇒ otra llave; llave nueva tras cambio de política (`DAT-44`, `DEC-18`).

### DAT-64 · `create_human_case`: sin llave, sin esquema, SLA largo — `ALTA`
Reintentos pueden crear **casos duplicados**. `reason` y `evidence` no están definidos y la `evidence` puede arrastrar **PII**. El SLA de **45 min** es mucho mayor que el TTL de opciones (2 min) y que la expiración del rebooking (≈9 min).
**Cuidado:** deduplicar del lado cliente (llave de negocio); `evidence` = **referencias + hechos mínimos** (ids, versión de política, ids de eventos), no copias de la reserva (`DEC-15`, `DEC-22`, `DEC-23`).

### DAT-65 · `notify_passenger`: sin destinatario, `QUEUED` ≠ entregado, validación mínima — `ALTA`
- La firma no incluye **a quién** (ni reserva ni pasajero) (`GAP-13`).
- `202 QUEUED` significa **aceptado**, no **recibido**; reintentar duplica (no hay llave idempotente).
- El `422` solo demuestra que **falta** `policy_ref`; **no** valida que el contenido sea **verdadero**. El requisito del producto ("no debe enviar información no validada") es **más estricto**: hace falta un validador **nuestro** (`SRC-02-05`).
**Cuidado:** validador previo con lista blanca de hechos (cada afirmación ↔ evidencia), `policy_ref` presente y vigente, sin PII innecesaria; **un** envío por decisión (`DEC-20`).

### DAT-66 · Modelo de errores incompleto — `MEDIA`
Solo `201/202/409/422/503`. Faltan `400`, `401/403`, `404`, `429`, `500`. Política por defecto: error no listado ⇒ **no reintentar a ciegas**, registrar y escalar.

### DAT-67 · El comentario "indeterminado" no es dato — `MEDIA`
Está en el PDF como `// …`. Se conserva como **regla de negocio** (503 ⇒ indeterminado) pero no se debe esperar en el payload.

### DAT-68 · `expires_at` sin `created_at` — `MEDIA`
No se puede calcular la ventana total ni el desfase de relojes. Usar un margen de seguridad antes de `expires_at`.

### DAT-69 · Estados sin enumerar — `MEDIA`
`PENDING_CONFIRMATION` y `QUEUED` son los únicos vistos. No se sabe si existen `CONFIRMED`, `EXPIRED`, `CANCELLED`, `FAILED`, `DELIVERED`. El código debe tolerar estados nuevos.

### DAT-70 · Identificadores opacos — `BAJA`
`RBK-88231`, `HC-4471`, `NT-9912`: tratarlos como **strings opacos**, sin interpretar el número.

### DAT-71 · `channel: PUSH` depende de datos que no están — `MEDIA`
El push requiere una cuenta/app asociada. `trip_context` **no** trae token ni preferencia; el menor no tiene contacto. Si no hay push posible, no hay canal alternativo definido (`GAP-13`, `DEC-20`).

### DAT-72 · `DISRUPTION_L2` — `BAJA`
"L2" sugiere un nivel 1 previo. ¿Debe el sistema escalar primero a L1? No se dice.

## 5. Cuidados (resumen operativo)
1. **Persistir la llave idempotente antes** de escribir; misma operación ⇒ misma llave (`DAT-63`).
2. `503` ⇒ no reintentar con llave nueva; tras N intentos ⇒ humano; **no** decir al pasajero ni sí ni no (`DAT-59`).
3. `409` ⇒ existente (éxito idempotente), sin bucles (`DAT-60`).
4. Revalidar opciones y política **inmediatamente antes** de `create_rebooking_request` (`DAT-35`, `DAT-58`).
5. `notify_passenger`: validador propio; un envío por decisión; `QUEUED` ≠ entregado (`DAT-65`).
6. `create_human_case`: evidencia mínima, sin PII, deduplicada (`DAT-64`).
