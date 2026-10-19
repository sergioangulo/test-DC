# 04.06 · Análisis **entre** requests — cómo se relacionan los datos

- **Alcance:** relaciones **entre** las 7 respuestas del PDF (`SRC-02-07`, `SRC-02-08`/`SRC-03-01`, `SRC-03-02`, `SRC-03-03`, `SRC-03-04`, `SRC-04-01…03`).
- Todo lo calculado aquí usa **solo** datos del PDF más **zonas horarias verificadas** con tzdata para el **2026-09-15** (Santiago UTC-3 · Lima UTC-5 · Ciudad de México UTC-6).
- Lo marcado **[HIPÓTESIS]** es un resultado **a validar por ti**; no es un requisito del PDF.
- Orden: §1 llaves · §2 línea de tiempo · §3 caso base paso a paso · §4 variables de política · §5 presupuesto de tiempo · §6 convenciones · §7 PII · §8 reglas de calidad · §9 casos borde · §10 observaciones transversales.

## 1. Llaves de unión entre respuestas
| Llave | Nace en | Se usa en | Observación |
|---|---|---|---|
| `booking_id` | argumento de `get_trip_context` | (solo ahí) | **No aparece** en eventos, opciones, política ni en las tools de escritura. |
| `segment_id` (`S1`, `S2`) | `trip_context.segments[]` | argumento y respuesta de `get_operational_events` | Única unión fuerte reserva↔eventos. |
| `passenger_id` (`P1`, `P2`) | `trip_context.passengers[]` | (solo ahí) | Ninguna otra tool lo recibe → **no se puede rebookear/notificar por pasajero**. |
| `option_id` (`O1…O3`) | `get_eligible_options` | argumento `option` de `create_rebooking_request` | Local a la respuesta; no estable. |
| `policy_ref` ↔ `version` | `get_policy_rules.version` | `options[].policy_ref`, `notify_passenger.message.policy_ref` | Debe **coincidir** con una versión recuperada y no superseded. |
| `scenario` (`DELAY`) | argumento de `get_policy_rules` | prefijo de `version` y de `policy_ref` (`POL-DELAY-…`, `POL-REFUND-…`) | Se **infiere** que `POL-REFUND-…` ⇒ `get_policy_rules("REFUND")`. |
| `request_id`, `case_id`, `notification_id` | respuestas de escritura | — | Solo salidas. Nada los ata a `booking_id` en el contrato. |
| `event_id` | `get_operational_events` | (solo ahí) | No es clave de orden. |

**`DAT-73` (ALTA):** ni `create_rebooking_request` ni `notify_passenger` reciben `booking_id`/destinatario, y no existe un **identificador de correlación** de punta a punta. Para la trazabilidad exigida (`SRC-01-11`) hará falta un **`decision_id`/`correlation_id` propio** que ate: reserva → eventos usados → versión de política → opción → acción → mensaje (`REQ-F-28`).

## 2. Línea de tiempo (UTC, con las zonas verificadas)
| Instante (UTC) | Hora local relevante | Qué pasa | Fuente |
|---|---|---|---|
| 09:30:00Z (15-sep) | 06:30 SCL | `E-1012` LEGACY_MIRROR dice `ON_TIME` | `SRC-03-01` |
| 10:48:00Z | 07:48 SCL | `E-1001` DELAY 160 min (OPS_CORE) · `E-2003` S2 `SCHEDULED` | `SRC-02-08`, `SRC-03-01` |
| 10:55:00Z | 07:55 SCL | `E-1007` cambio de puerta 24 | `SRC-02-08` |
| **11:02:31Z** | — | `get_trip_context` recuperado | `SRC-02-07` |
| **11:02:33Z** | — | `get_operational_events` recuperado | `SRC-03-01` |
| **11:02:35Z** | — | `get_eligible_options` recuperado (**TTL 120 s**) | `SRC-03-02` |
| **11:02:36Z** | — | `get_policy_rules` recuperado | `SRC-03-03` |
| 11:04:35Z | — | **Vencen las opciones** | derivado de `ttl_seconds` |
| 11:12:00Z | — | `expires_at` de la solicitud de rebooking del ejemplo | `SRC-03-04` |
| ≈ 11:47Z | — | Fin del SLA de 45 min de un caso humano creado a las ~11:02:36Z **(ilustrativo)** | `SRC-04-02` |
| 17:30Z | 14:30 SCL | Salida original de S1 | `SRC-02-07` |
| 20:10Z | 17:10 SCL | **Nueva** salida de S1 | `SRC-02-08` |
| 22:55Z | 17:55 LIM | Llegada original de S1 a LIM (con zonas reales) | `SRC-02-07` |
| 00:05Z (16-sep) | 19:05 LIM | Salida programada de S2 | `SRC-02-07` |
| 01:35Z (16-sep) | 20:35 LIM | **Nueva** llegada de S1 (si el retraso se propaga íntegro) | **[HIPÓTESIS]** derivada |
| 04:40Z (16-sep) | 23:40 LIM | Salida de O2 | `SRC-03-02` |
| 05:40Z (16-sep) | 23:40 MEX | Llegada programada de S2 a MEX | `SRC-02-07` |
| 13:15Z (16-sep) | 08:15 LIM | Salida de O1 | `SRC-03-02` |

- Distancias derivadas: de la recuperación (11:02:31Z) a la salida **original** de S1 hay **6 h 27 min**; a la **nueva** salida, **9 h 07 min**; a la salida de S2, **13 h 02 min**.
- **`DAT-74` (MEDIA):** las cuatro lecturas ocurren en una ventana de **5 s** (11:02:31–11:02:36): coherentes entre sí. El riesgo no es esa ventana, sino el tiempo **entre** la lectura y la acción/mensaje.
- **Atención `DAT-05`:** con zonas reales, S1 duraría 5 h 25 min (sospechoso). La línea de tiempo anterior usa zonas reales **solo para ordenar**; el análisis de la conexión (§3) **no depende de ellas** porque compara dos horas **de Lima**.

## 3. El caso base, paso a paso **[HIPÓTESIS — a validar]**
> Es el resultado que se obtiene al **combinar reserva + eventos + política** (`SRC-04-18`, `SRC-04-21`). Está aquí para que revises la **lógica**; las decisiones que lo modifican están en `06_Decisiones`.

**Paso 0 · Entradas.** 2 pasajeros (1 adulto, 1 niño de 7 años); 2 segmentos SCL→LIM→MEX el 15-sep-2026; política `POL-DELAY-2026-03`.

**Paso 1 · Resolver eventos por segmento.**
| Segmento | Candidatos | Resolución | Razón |
|---|---|---|---|
| S1 | `E-1001` DELAY · `E-1007` GATE_CHANGE · `E-1012` ON_TIME | `E-1012` **descartado** | más antiguo (−78 min) **y** fuente degradada (`DAT-15`) |
| S1 estado efectivo | — | **retrasado 160 min**, nueva salida 17:10, puerta 24 | `E-1001` + `E-1007` |
| S2 | `E-2003` SCHEDULED | "sin información posterior al retraso de S1" | `DAT-24` |

**Paso 2 · Consistencia.** `14:30 + 160 min = 17:10` ✔ (`E-1001`).

**Paso 3 · Derivar la nueva llegada de S1 a Lima.** Supuesto **A1** (el retraso se propaga íntegro): `17:55 + 160 min = 20:35`.

**Paso 4 · Evaluar la conexión (mismo aeropuerto, misma zona).**
- Escala planificada: `19:05 − 17:55 = 70 min`.
- Nueva diferencia: `19:05 − 20:35 = −90 min` → la llegada es **90 min después** de la salida de S2.
- **`missed_connection = true` (derivado)**, con supuestos **A1** (propagación íntegra), **A2** (no hay MCT en los datos) y **A3** (S2 no se retiene: no hay evento que lo diga).
- **Sensibilidad:** para salvarla habría que **recuperar** en vuelo `90 + MCT` min: 90 (MCT 0), 135 (MCT 45), 150 (MCT 60). Con 160 min de retraso inicial es **improbable**, pero el dato **no lo prueba**.

**Paso 5 · Evaluar reglas (`POL-DELAY-2026-03`).**
| Regla | Valor | Resultado |
|---|---|---|
| R1 `delay_minutes >= 180` | 160 | **Falso** |
| R2 `delay_minutes >= 240 AND international` | 160 | **Falso** |
| **R3** `missed_connection == true` | derivado | **Verdadero** |
| R4 `compensation_requested == true` | nadie lo pidió | **No aplica / desconocido** |
| **R5** `group_includes_minor == true` | `P2` CHILD, 7 años | **Verdadero** |

**Paso 6 · Derechos.** `REBOOK_NO_FEE` (R3, sin aprobación) + `PRIORITY_HANDLING` (R5, **con aprobación humana**). Cómo se combinan: **no está definido** (`DAT-47`, `DEC-13`).

**Paso 7 · Filtrar opciones (2 pasajeros).**
| Opción | Cupos vs 2 pax | Costo | Coherencia con `REBOOK_NO_FEE` | Política verificable | Viable |
|---|---|---|---|---|---|
| **O1** | 4 ✔ | 0 | ✔ | ✔ `POL-DELAY-2026-03` | **Sí** |
| O2 | **1 ✘** | 180.000 CLP | **✘** | ✔ | **No** (`DAT-31`, `DAT-32`) |
| O3 REFUND | n/a | sin dato | sin dato | **✘** no recuperada | **No verificable** (`DAT-33`) |

**Paso 8 · Resultado esperado [HIPÓTESIS].**
1. Informar a la pasajera: su vuelo SCL→LIM **se retrasó 160 min**, nueva salida 17:10, puerta 24 (con hora de la información).
2. Informar: **con este retraso no alcanzaría la conexión** a Ciudad de México (explicando que es una **estimación**).
3. Proponer **O1** (LA2412, 16-sep 08:15, **sin costo**), citando `POL-DELAY-2026-03`.
4. Indicar que existe la **vía de reembolso** (sin prometer monto ni plazo) **o** derivar la consulta.
5. **Crear un caso humano** (hay un menor: R5; hay pernocte: alojamiento no cubierto por las reglas del PDF).
6. **No ejecutar** `create_rebooking_request` hasta que se resuelva la aprobación (según `DEC-13`/`DEC-16`) y tras **revalidar** opciones.

**Paso 9 · Lo que el sistema **no** puede decir (por falta de dato):** hora de llegada a México; si la aerolínea retendrá el S2; hotel/comidas/traslados (no hay regla); monto de reembolso o compensación; que el cambio "ya está hecho"; la **causa** del retraso.

**`DAT-75` (ALTA):** el resultado del caso base descansa en **una derivación crítica** (`missed_connection`) y **tres supuestos** (A1 propagación íntegra, A2 sin MCT, A3 S2 no se retiene). Si cualquiera cambia, el resultado puede cambiar. Por eso el resultado debe presentarse con sus supuestos visibles y con revisión humana antes de actuar (`DEC-07`, `DEC-13`).

## 4. Variables de política: de dónde sale cada una
**`DAT-76` (ALTA):** cada variable derivada es una decisión con supuestos.
| Variable | Usada en | Origen / derivación | Supuestos | Riesgo |
|---|---|---|---|---|
| `delay_minutes` | R1, R2 | `E-1001.delay_minutes` del segmento afectado, **tras resolver** conflictos | Retraso de **salida**; por segmento | Medir salida vs llegada cambia el derecho (`DAT-19`, `DAT-54`) |
| `international` | R2 | País de origen ≠ país de destino, desde una **tabla aeropuerto→país** externa | Por segmento (S1: CL→PE, S2: PE→MX = ambos internacionales) | Tabla no incluida en los datos |
| `missed_connection` | R3 | §3 paso 4: `nueva_llegada(S1) > salida(S2) − MCT` | A1, A2, A3 | **CRÍTICO**: gatilla un derecho económico |
| `compensation_requested` | R4 | **Intención explícita** del pasajero | Por defecto `false` | No inducir al usuario ni inferirlo |
| `group_includes_minor` | R5 | `any(passenger.type == "CHILD")` (o `age < X`) | "Menor" = `CHILD` | Definición legal distinta por norma (`GAP-08`) |
| `new_arrival` | (nuestra) | llegada original + retraso | A1 | No viene en eventos |
| `overnight_required` | (nuestra) | opción del día siguiente | — | Dispara derechos de alojamiento (`GAP-03`) |
| `seats_needed` | (nuestra) | número de pasajeros a rebookear | Todos, juntos | Menor no debe separarse |
| `event_age`, `source_health` | (nuestra) | `now − recorded_at`; `source ∈ sources_degraded` | Reloj confiable | Frescura |

## 5. Presupuesto de tiempo (conflictos entre vigencias)
| Ventana | Valor | Fuente |
|---|---|---|
| Vigencia de las opciones | **120 s** | `SRC-03-02` |
| Vigencia de una solicitud de rebooking (ejemplo) | **≈ 9 min 25 s** desde las opciones | `SRC-03-04` |
| SLA de atención de un caso humano | **45 min** | `SRC-04-02` |
| Antelación mínima legal para avisar cambios | 4 h (Decisión 619 art. 4 g); 24 h (Colombia); 4 h/12 h (Bolivia) | `POL-PE-03`, `POL-CO-02`, `POL-BO-01` |
| Tiempo hasta la nueva salida de S1 | 9 h 07 min | cálculo §2 |

**`DAT-77` (ALTA):** `TTL (2 min) < expiración (≈9 min) < SLA humano (45 min)`. Una aprobación humana **siempre** llegará con opciones **vencidas** y con la solicitud **caducada** → el flujo "humano aprueba → se ejecuta" requiere **recuperar y revalidar** de nuevo (`GAP-25`, `DEC-19`).

## 6. Convenciones y heterogeneidad (para no confundirse)
| Tema | Observación |
|---|---|
| Horas | **Locales sin zona** (`HH:MM`) en segmentos, eventos (`new_departure`) y opciones; **UTC con `Z`** en `recorded_at`, `retrieved_at`, `expires_at`. |
| "Salida" | Tres nombres: `scheduled_departure` (segmento), `new_departure` (evento), `departure` (opción). Semánticas distintas. |
| Fechas | `date` aparece en segmentos y opciones; **no** en eventos. |
| Ids | `S<n>`, `P<n>`, `O<n>`, `R<n>`, `E-<n>`, `RBK-<n>`, `HC-<n>`, `NT-<n>`, `POL-…` — todos **opacos**. |
| Enumeraciones | `UPPER_SNAKE`; listas **abiertas** (hay que tolerar valores nuevos). |
| Numéricos | Enteros (CLP sin decimales; minutos). |
| `_meta` | Presente en las 4 lecturas, con `retrieved_at`. No en las de escritura. |
| Errores | `{ "error": "<CODIGO>", "detail"?: "<texto>" }` + HTTP 4xx/5xx. |
| Comentarios | `// …` dentro del bloque de `503`: no es JSON. |

**`DAT-78` (MEDIA):** tres nombres de "salida" y dos convenciones horarias en un mismo flujo son una fuente natural de errores de unión.

## 7. Inventario de datos personales y mínimo privilegio
| Dato | Dónde | Categoría | ¿Necesario para decidir? | ¿A un LLM? **(recomendación provisional)** | En logs |
|---|---|---|---|---|---|
| `document_id` (RUT) | `trip_context` | Identificador gubernamental | **No** | **Nunca** | **Nunca** |
| `email`, `phone` | `trip_context` | Contacto | No (el canal lo resuelve `notify`) | **Nunca** | Enmascarado |
| `name` | `trip_context` | PII | Solo saludo | Solo **nombre de pila** si hace falta | Enmascarado |
| `age` (menor) | `trip_context` | PII de menor | Solo como `has_minor` | **Solo booleano** | Booleano |
| `loyalty_tier` | `trip_context` | Comercial | **No** (las reglas del PDF no lo usan) | No | Opcional |
| `booking_id` | todo | Referencia | Sí (auditoría) | Seudonimizado | Hash |
| `passenger_id` | `trip_context` | Interno | Sí | Sí (no es identificable) | Sí |
| Vuelos, horas, puertas | varios | Operacional | Sí | Sí | Sí |
| `fare_difference`, `fare_conditions` | varios | Comercial | Parcial | Solo lo imprescindible | Sí |

**`DAT-79` (ALTA):** cinco campos PII viajan en **una** lectura y el contrato fuerza que viajen a `get_eligible_options` (`SRC-02-01`). "Mantén estos contratos" (`SRC-01-16`) vs "mínimo privilegio" (`SRC-04-07`) es una tensión a decidir (`DEC-22`).

## 8. Reglas de calidad de datos propuestas (`DQ-nn`)
| ID | Regla | Si falla |
|---|---|---|
| DQ-01 | Toda lectura trae `_meta.retrieved_at` en ISO UTC | Rechazar/degradar |
| DQ-02 | La reserva tiene ≥ 1 segmento y ≥ 1 pasajero | Humano |
| DQ-03 | Cadena continua: `seg[i].destination == seg[i+1].origin` | Marcar |
| DQ-04 | Horas en `HH:MM`; fechas ISO | Rechazar |
| DQ-05 | `completeness` coherente con `missing_fields` | Marcar |
| DQ-06 | `CHILD` ⇒ `age`; menor ⇒ al menos un adulto en la reserva | Humano |
| DQ-07 | `segment_id` de eventos ⊆ segmentos pedidos | Descartar el evento |
| DQ-08 | `type` de evento conocido y con sus campos | Degradar a humano |
| DQ-09 | `DELAY`: `scheduled_departure + delay_minutes == new_departure` | Degradar |
| DQ-10 | `recorded_at ≤ retrieved_at` (± tolerancia de reloj) | Marcar |
| DQ-11 | Orden por `recorded_at`; desempate por fuente; **nunca** por `event_id` | — |
| DQ-12 | Fuente en `sources_degraded` ⇒ no es evidencia primaria | Excluir |
| DQ-13 | Conflicto sin resolver (todas degradadas / misma jerarquía) | Humano |
| DQ-14 | Edad del evento ≤ umbral por tipo de acción | Refrescar o degradar |
| DQ-15 | `retrieved_at + ttl_seconds` > ahora al **usar** las opciones | Refrescar |
| DQ-16 | `seats_available ≥ pasajeros a rebookear` | Opción no viable |
| DQ-17 | `fare_difference > 0` y derecho "sin costo" ⇒ incoherencia | No presentar como gratuita |
| DQ-18 | `fare_difference > 0` ⇒ `currency` presente | Rechazar la opción |
| DQ-19 | `policy_ref` == versión recuperada y ∉ `superseded_versions` | Opción sin respaldo |
| DQ-20 | `condition` de regla reconocida | Humano |
| DQ-21 | Versión de política y `rule_id` **fijadas** en la auditoría | — |
| DQ-22 | Llave idempotente **persistida antes** de escribir | Bloquear la escritura |
| DQ-23 | `409` ⇒ existente; **sin bucle** | — |
| DQ-24 | `503` ⇒ misma llave, intentos acotados, luego humano | — |
| DQ-25 | `notify`: `policy_ref` + destinatario + hechos ⊆ lista blanca validada | Bloquear |
| DQ-26 | PII fuera de LLM y logs | Bloquear |
| DQ-27 | Enumeración nueva/desconocida ⇒ degradar | Humano |
| DQ-28 | Sin `change_penalty_amount` ⇒ no cotizar cambios voluntarios | No afirmar costo |
| DQ-29 | Sin causa del evento ⇒ no afirmar derechos que dependan de ella | Cauto |
| DQ-30 | Cruce de medianoche con fecha completa | Corregir fecha |

## 9. Casos borde sugeridos (derivados del propio ejemplo) **[propuestas]**
| ID | Perturbación | Resultado esperable | Qué demuestra | Datos/DQ |
|---|---|---|---|---|
| TC-01 | Caso base tal cual | §3 paso 8 | Combinación reserva+eventos+política | `DAT-46` |
| TC-02 | Solo `E-1012` (sin `E-1001`) | **No** concluir "a tiempo": fuente degradada ⇒ cauto/humano | Fuente degradada | `DAT-15`, DQ-12 |
| TC-03 | `E-1012` **más reciente** que `E-1001` | Conflicto no trivial ⇒ regla de desempate / humano | Precedencia | DQ-13 |
| TC-04 | `delay_minutes` = 179 y 180 (sin pérdida de conexión) | R1 falso / verdadero | Borde inclusivo | `DAT-54` |
| TC-05 | `delay_minutes` = 239 y 240, internacional | R2 falso / verdadero | Borde R2 | `DAT-54` |
| TC-06 | Retraso de 60 min (menor que la escala de 70) | `missed_connection = false` | Derivación | DQ-09 |
| TC-07 | Quitar a `P2` | R5 falso; R3 verdadero ⇒ rebooking sin menor | Efecto del menor | `DAT-47` |
| TC-08 | Opciones con `ttl` vencido al usarlas | Refrescar antes de escribir | Vigencia | DQ-15 |
| TC-09 | Solo O2 disponible, 2 pasajeros | Ninguna opción viable ⇒ humano | Cupos | DQ-16 |
| TC-10 | `policy_ref` superseded (`POL-DELAY-2025-11`) | Opción sin respaldo | Versionado | DQ-19 |
| TC-11 | O3 con `POL-REFUND-…` no recuperada | Sin respaldo para afirmar | Verificabilidad | `DAT-34` |
| TC-12 | Falta `change_penalty_amount` y ninguna regla aplica | No cotizar costo | Datos parciales | DQ-28 |
| TC-13 | Evento `CANCELLATION` (tipo nuevo) | Degradar a humano | Tipos desconocidos | DQ-08 |
| TC-14 | `503` en el rebooking | Misma llave, reintentos acotados, luego caso humano; mensaje cauto | Indeterminado | `DAT-59` |
| TC-15 | `409` al repetir | Tratar como existente | Idempotencia | `DAT-60` |
| TC-16 | `notify` sin `policy_ref` (→ `422`) y con `policy_ref` pero afirmación no validada | Bloqueo por **validador propio** | Contenido validado | `DAT-65` |
| TC-17 | `compensation_requested = true` | R4 ⇒ humano; sin montos | Compensación | `GAP-05` |
| TC-18 | Retraso que cruza medianoche | Fecha correcta de llegada | Fechas | `DAT-06` |
| TC-19 | `sources_degraded` incluye `OPS_CORE` | Sin fuente sana ⇒ humano | Degradación total | DQ-13 |
| TC-20 | Solicitud de PII ("dime el documento de la reserva") | Rechazo | Mínimo privilegio | `DAT-01`, DQ-26 |

## 10. Observaciones transversales
- **`DAT-80` (MEDIA):** no hay identificador de correlación extremo a extremo (ver `DAT-73`).
- **`DAT-81` (MEDIA):** el ejemplo parece **sintético**: duración implícita de S1 inconsistente con zonas reales (`DAT-05`), O2 con costo en un caso "sin costo" (`DAT-32`), `LEGACY_MIRROR` fabricando el contraste. Sirve para **probar criterio**, no para modelar la realidad.
- **`DAT-82` (MEDIA):** el ejemplo es **un solo caso**: no cubre cancelación, adelanto, múltiples pasajeros en segmentos distintos, 3+ tramos, reservas sin conexión, ni opciones de hotel. No confundir **ejemplo** con **esquema** (`SRC-02-06`: "representativos"; "úsalos como base de trabajo").
