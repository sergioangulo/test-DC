# 04 · Análisis de datos de las respuestas de ejemplo

> **Objetivo (tu pedido):** para cada ejemplo de respuesta del PDF: el **ejemplo tal cual**, luego la **explicación** de sus campos, cómo se relacionan **dentro** del request y **entre** requests, lo que **llama la atención** y los **cuidados** a tener.
> **Fuente:** `SRC-02-07` … `SRC-04-03` (págs. 2–4 del PDF). Los JSON están copiados **literalmente**.
> **Método:** lectura campo a campo + comprobaciones aritméticas/temporales reproducibles + zonas horarias verificadas con tzdata (2026-09-15: Santiago UTC-3, Lima UTC-5, Ciudad de México UTC-6).

## Archivos
| Archivo | Contenido |
|---|---|
| `01_get_trip_context.md` | Reserva: pasajeros, segmentos, tarifa, `_meta` |
| `02_get_operational_events.md` | Eventos: retraso, puerta, estados, fuentes y degradación |
| `03_get_eligible_options.md` | Opciones: `O1`, `O2`, `O3`, TTL |
| `04_get_policy_rules.md` | Política `DELAY`: reglas `R1…R5`, versión |
| `05_tools_de_escritura.md` | `create_rebooking_request`, `create_human_case`, `notify_passenger` |
| `06_Analisis_cruzado.md` | Llaves de unión · línea de tiempo · **caso base paso a paso** · variables de política · presupuesto de tiempo · PII · reglas de calidad (`DQ`) · casos borde (`TC`) |

## Convenciones
- `DAT-nn` = observación de datos (se cita desde requerimientos y decisiones).
- **Severidad:** `CRÍTICA` puede producir un mensaje/acción **incorrectos** · `ALTA` puede distorsionar una decisión · `MEDIA` exige un criterio explícito · `BAJA` a tener presente.
- `DQ-nn` = regla de calidad propuesta · `TC-nn` = caso de prueba propuesto (**propuestas**, no requisitos del PDF).
- **[HIPÓTESIS]** = resultado derivado a validar por ti.

## Las cinco observaciones críticas (léelas primero)
1. **`DAT-15`** · `E-1012` (`ON_TIME`, fuente degradada, más antiguo) **contradice** `E-1001` (retraso 160 min). Mostrar `ON_TIME` sería información falsa.
2. **`DAT-31`** · `O2` ofrece **1 cupo** para **2 pasajeros** (adulto + niño de 7): no es viable y separaría al menor.
3. **`DAT-45`** · **4 de las 5 variables** de las reglas no existen en los datos: hay que derivarlas.
4. **`DAT-46`** · En el caso base **`R1` no se cumple (160 < 180) pero `R3` sí** (la conexión se pierde). Y `R5` (menor) exige aprobación humana.
5. **`DAT-59`** · `503` en el rebooking es **indeterminado**: no se puede reintentar a ciegas ni informar éxito/fracaso.

## Catálogo completo de observaciones
Total: **82** observaciones · CRÍTICA: **5** · ALTA: **32** · MEDIA: **34** · BAJA: **11**

| ID | Severidad | Observación | Archivo |
|---|---|---|---|
| `DAT-01` | ALTA | `booking_id` abre PII y no es una credencial | `01_get_trip_context.md` |
| `DAT-02` | ALTA | Concentración de PII y propagación | `01_get_trip_context.md` |
| `DAT-03` | ALTA | El menor (`P2`) cambia el tratamiento y casi no tiene datos | `01_get_trip_context.md` |
| `DAT-04` | MEDIA | Campos opcionales según pasajero y ausencia de mapa pasajero↔segmento | `01_get_trip_context.md` |
| `DAT-05` | ALTA | Horas locales **sin zona horaria** | `01_get_trip_context.md` |
| `DAT-06` | MEDIA | No hay fecha de llegada | `01_get_trip_context.md` |
| `DAT-07` | ALTA | La conexión es **implícita** | `01_get_trip_context.md` |
| `DAT-08` | MEDIA | No hay cabina ni estado del ticket | `01_get_trip_context.md` |
| `DAT-09` | ALTA | `PARTIAL`: qué bloquea cada dato faltante | `01_get_trip_context.md` |
| `DAT-10` | BAJA | `retrieved_at` es de recuperación, no de validez | `01_get_trip_context.md` |
| `DAT-11` | MEDIA | `refundable:false` / `changeable:true` describen **cambios voluntarios** | `01_get_trip_context.md` |
| `DAT-12` | BAJA | Codificación y nombres | `01_get_trip_context.md` |
| `DAT-13` | BAJA | `flight_number` | `01_get_trip_context.md` |
| `DAT-14` | MEDIA | `date` repetida y atada a la hora | `01_get_trip_context.md` |
| `DAT-15` | CRÍTICA | Contradicción en S1: `ON_TIME` vs `DELAY` | `02_get_operational_events.md` |
| `DAT-16` | ALTA | `event_id` no ordena en el tiempo | `02_get_operational_events.md` |
| `DAT-17` | ALTA | Frescura: no hay umbral y hay una espera oculta | `02_get_operational_events.md` |
| `DAT-18` | ALTA | Payload polimórfico y tipos desconocidos | `02_get_operational_events.md` |
| `DAT-19` | ALTA | `delay_minutes` mide la **salida**; no hay llegada | `02_get_operational_events.md` |
| `DAT-20` | MEDIA | `new_departure` sin fecha ni zona | `02_get_operational_events.md` |
| `DAT-21` | MEDIA | Redundancia `new_departure` / `delay_minutes` | `02_get_operational_events.md` |
| `DAT-22` | ALTA | No hay **causa** del retraso | `02_get_operational_events.md` |
| `DAT-23` | MEDIA | `GATE_CHANGE` es útil pero perecedero | `02_get_operational_events.md` |
| `DAT-24` | ALTA | `STATUS: SCHEDULED` del S2 no prueba que la conexión se sostenga | `02_get_operational_events.md` |
| `DAT-25` | MEDIA | Marcas de tiempo idénticas | `02_get_operational_events.md` |
| `DAT-26` | MEDIA | `sources_degraded` es a nivel de consulta | `02_get_operational_events.md` |
| `DAT-27` | MEDIA | Una fuente caída no deja rastro de evento | `02_get_operational_events.md` |
| `DAT-28` | BAJA | Segmentos sin eventos | `02_get_operational_events.md` |
| `DAT-29` | MEDIA | Dependencia del `trip_context` | `02_get_operational_events.md` |
| `DAT-30` | BAJA | Los timestamps UTC son la parte **inequívoca** | `02_get_operational_events.md` |
| `DAT-31` | CRÍTICA | O2 tiene **1 cupo para 2 pasajeros** | `03_get_eligible_options.md` |
| `DAT-32` | ALTA | O2 cuesta 180.000 CLP pero el derecho es "sin costo" | `03_get_eligible_options.md` |
| `DAT-33` | ALTA | O3 (reembolso) es un cascarón | `03_get_eligible_options.md` |
| `DAT-34` | ALTA | `policy_ref` es un puntero que hay que **verificar** | `03_get_eligible_options.md` |
| `DAT-35` | ALTA | TTL de 120 s: las opciones envejecen más rápido que cualquier flujo humano | `03_get_eligible_options.md` |
| `DAT-36` | MEDIA | `confidence` no tiene definición | `03_get_eligible_options.md` |
| `DAT-37` | MEDIA | "Elegible" se calculó con datos **parciales** | `03_get_eligible_options.md` |
| `DAT-38` | MEDIA | Entrada con PII completa | `03_get_eligible_options.md` |
| `DAT-39` | MEDIA | O1 obliga a **pernoctar** en Lima | `03_get_eligible_options.md` |
| `DAT-40` | MEDIA | Moneda y formato del monto | `03_get_eligible_options.md` |
| `DAT-41` | MEDIA | No hay cabina ni clase | `03_get_eligible_options.md` |
| `DAT-42` | BAJA | Coincidencia 23:40 | `03_get_eligible_options.md` |
| `DAT-43` | MEDIA | Las opciones son de la reserva, no por pasajero ni por segmento | `03_get_eligible_options.md` |
| `DAT-44` | BAJA | `option_id` local | `03_get_eligible_options.md` |
| `DAT-45` | CRÍTICA | Cuatro de las cinco variables **no existen** en los datos | `04_get_policy_rules.md` |
| `DAT-46` | CRÍTICA | En el caso base **R1 no se cumple pero R3 sí** | `04_get_policy_rules.md` |
| `DAT-47` | ALTA | R3 ("sin aprobación") y R5 ("con aprobación") chocan | `04_get_policy_rules.md` |
| `DAT-48` | ALTA | `condition` es texto: no se evalúa con `eval` | `04_get_policy_rules.md` |
| `DAT-49` | ALTA | Las reglas no tienen **causa** | `04_get_policy_rules.md` |
| `DAT-50` | ALTA | No hay reglas de reembolso, alojamiento, comunicación ni cuantía; solo `DELAY` | `04_get_policy_rules.md` |
| `DAT-51` | ALTA | No hay jurisdicción | `04_get_policy_rules.md` |
| `DAT-52` | MEDIA | Los "derechos" son etiquetas sin significado | `04_get_policy_rules.md` |
| `DAT-53` | MEDIA | Versionado: fijar la versión usada | `04_get_policy_rules.md` |
| `DAT-54` | MEDIA | `delay_minutes`: ¿de qué segmento, medido dónde y con qué borde? | `04_get_policy_rules.md` |
| `DAT-55` | MEDIA | R2 es **más exigente** que varias normas externas | `04_get_policy_rules.md` |
| `DAT-56` | BAJA | `requires_human_approval` sin quién ni cuándo | `04_get_policy_rules.md` |
| `DAT-57` | BAJA | Sin `effective_to` ni país | `04_get_policy_rules.md` |
| `DAT-58` | MEDIA | La política puede cambiar entre lectura y acción | `04_get_policy_rules.md` |
| `DAT-59` | CRÍTICA | `503`: el resultado real es **indeterminado** | `05_tools_de_escritura.md` |
| `DAT-60` | ALTA | `409` es "ya existe", no "falló" | `05_tools_de_escritura.md` |
| `DAT-61` | ALTA | `PENDING_CONFIRMATION` sin forma de confirmar, consultar ni cancelar | `05_tools_de_escritura.md` |
| `DAT-62` | ALTA | El rebooking no dice **a quién** ni **en qué reserva** | `05_tools_de_escritura.md` |
| `DAT-63` | ALTA | Diseño de la `idempotency_key` | `05_tools_de_escritura.md` |
| `DAT-64` | ALTA | `create_human_case`: sin llave, sin esquema, SLA largo | `05_tools_de_escritura.md` |
| `DAT-65` | ALTA | `notify_passenger`: sin destinatario, `QUEUED` ≠ entregado, validación mínima | `05_tools_de_escritura.md` |
| `DAT-66` | MEDIA | Modelo de errores incompleto | `05_tools_de_escritura.md` |
| `DAT-67` | MEDIA | El comentario "indeterminado" no es dato | `05_tools_de_escritura.md` |
| `DAT-68` | MEDIA | `expires_at` sin `created_at` | `05_tools_de_escritura.md` |
| `DAT-69` | MEDIA | Estados sin enumerar | `05_tools_de_escritura.md` |
| `DAT-70` | BAJA | Identificadores opacos | `05_tools_de_escritura.md` |
| `DAT-71` | MEDIA | `channel: PUSH` depende de datos que no están | `05_tools_de_escritura.md` |
| `DAT-72` | BAJA | `DISRUPTION_L2` | `05_tools_de_escritura.md` |
| `DAT-73` | ALTA | Sin llaves de unión completas ni id de correlación (rebooking y notify no reciben booking/destinatario) | `06_Analisis_cruzado.md` |
| `DAT-74` | MEDIA | Las 4 lecturas caen en una ventana de 5 s; el riesgo es el tiempo entre lectura y acción | `06_Analisis_cruzado.md` |
| `DAT-75` | ALTA | El caso base descansa en 1 derivación crítica y 3 supuestos | `06_Analisis_cruzado.md` |
| `DAT-76` | ALTA | Cada variable derivada de política es una decisión con supuestos | `06_Analisis_cruzado.md` |
| `DAT-77` | ALTA | TTL de opciones (2 min) < expiración (≈9 min) < SLA humano (45 min) | `06_Analisis_cruzado.md` |
| `DAT-78` | MEDIA | Tres nombres de 'salida' y dos convenciones horarias | `06_Analisis_cruzado.md` |
| `DAT-79` | ALTA | Cinco campos PII en una lectura y el contrato fuerza su propagación | `06_Analisis_cruzado.md` |
| `DAT-80` | MEDIA | No hay identificador de correlación extremo a extremo | `06_Analisis_cruzado.md` |
| `DAT-81` | MEDIA | El ejemplo parece sintético (inconsistencias deliberadas o accidentales) | `06_Analisis_cruzado.md` |
| `DAT-82` | MEDIA | El ejemplo es un solo caso: no confundir ejemplo con esquema | `06_Analisis_cruzado.md` |
