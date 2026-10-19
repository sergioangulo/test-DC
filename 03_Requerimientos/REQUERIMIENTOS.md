# 03 · Documento de requerimientos — Caso A "Disruption Companion"

> **Fuente única:** `Disruption Companion.pdf` (7 págs.). Todo se traza a `SRC-pp-nn` (ver `01_Fuente_y_Trazabilidad/01_Indice_de_fuente_SRC.md`).
> **Método:** análisis ESF (ver `02_Analisis_ESF/ANALISIS_ESF.md`). Aquí está el **resultado documental**: requisitos, contratos, ambigüedades y brechas.
> **Regla de oro:** si un requisito **no** cita un `SRC`, es **DERIVADO** (con su cadena de derivación) o **SUPUESTO** (a decidir por ti). Nada se presenta como "dicho por el PDF" si no lo dice.

## 0. Cómo leer este documento

| Marca | Significa |
|---|---|
| **E** (explícito) | Lo dice el PDF; se cita el `SRC`. |
| **D** (derivado) | Se **deduce** de uno o más enunciados explícitos; se muestra la cadena. |
| **S** (supuesto) | Mi lectura/propuesta; **requiere tu confirmación** (aparece en §10 y en `06_Decisiones`). |
| `REQ-P/D/F/N/C/E-nn` | Proceso · Entregables · Funcional · No funcional/restricción · Contrato de tool · Evaluación |
| `AMB-nn` | Ambigüedad **declarada** por el PDF (§4 del PDF) |
| `GAP-nn` | Brecha **detectada por mí** (algo que falta y que podría necesitarse) |
| `DAT-nn` | Observación de datos (`04_Analisis_de_Datos`) |
| `POL-xx-nn` | Política externa (`05_Politicas_Externas`) — **requiere revisión estricta tuya** |
| `DEC-nn` | Decisión pendiente (`06_Decisiones`) |

## 1. Dos capas en un solo documento
El PDF mezcla **dos niveles** que conviene no confundir:
1. **El ejercicio** (proceso, entregables, evaluación): qué debes **entregar y defender** (`REQ-P`, `REQ-D`, `REQ-E`).
2. **El producto** "Disruption Companion" (funcionalidad, restricciones, contratos): qué debe **hacer el sistema** (`REQ-F`, `REQ-N`, `REQ-C`).

El producto es el **objeto** del ejercicio, y el ejercicio mide cómo razonas sobre él.

**Resumen del producto (E):** una funcionalidad construida por un equipo compacto (PM, Product Designer, Engineering Team Lead, Software Engineer) para **ayudar a pasajeros cuyo vuelo sufrió una modificación** (`SRC-01-09`) a **entender qué ocurrió y cuál es su siguiente paso**, **sin entregar información no verificada** y **sin ejecutar acciones de alto impacto sin controles** (`SRC-01-10`). Resultado de negocio: **reducir la incertidumbre del pasajero y los contactos evitables al call center**, manteniendo **exactitud, seguridad y trazabilidad** (`SRC-01-11`).

## 2. Requisitos de proceso (`REQ-P`)
| ID | Requisito | T | Fuente | Verificación | Relacionado |
|---|---|---|---|---|---|
| **REQ-P-01** | El trabajo efectivo tiene un **máximo de 3 horas** e incluye análisis, implementación, validaciones y documentación. | E | `SRC-01-02`, `SRC-06-01` | Bitácora de tiempo | `DEC-04`, `DEC-24` |
| **REQ-P-02** | La propuesta se entrega **dentro de 48 horas** desde la recepción del documento (plazo disponible, no trabajo continuo). | E | `SRC-01-03`, `SRC-05-06`, `SRC-05-07` | Fecha/hora de entrega | — |
| **REQ-P-03** | Las 3 horas pueden **distribuirse en varias sesiones**. | E | `SRC-05-07` | — | — |
| **REQ-P-04** | El tiempo es un **límite, no una meta**: no se evalúa cuánto se produce. | E | `SRC-06-01`, `SRC-01-07` | — | `REQ-E-09` |
| **REQ-P-05** | Habrá una **sesión con un comité de 2 evaluadores** de 40–45 min, dentro de las **48 h hábiles** siguientes a la entrega. | E | `SRC-01-04`, `SRC-06-03` | Agenda | — |
| **REQ-P-06** | La sesión **comienza con 10 min** de presentación con el soporte que prefieras; **no se exige** presentación formal ni diapositivas; **no se espera** aplicación terminada ni despliegue. | E | `SRC-01-06`, `SRC-06-03`, `SRC-05-06` | — | `REQ-D-11` |
| **REQ-P-07** | La presentación explica: **entendimiento** del problema, **estructura** de la solución, **decisiones y supuestos**, **criterios** de decisión y **trade-offs** relevantes (sin recorrer cada detalle). | E | `SRC-06-03` | Guion de 10 min | `REQ-D-11` |
| **REQ-P-08** | Preparar la **defensa**: el comité puede cuestionar decisiones y supuestos, explorar **alternativas descartadas**, plantear **escenarios o cambiar restricciones** y preguntar por **riesgos y evolución**; no requiere desarrollo nuevo. | E | `SRC-06-04` | Lista de preguntas previsibles | `REQ-E-08` |
| **REQ-P-09** | **Formato y herramientas libres** (repositorio, Markdown, PDF, documento, diagrama, demo); la estética no se evalúa; el **contenido** de los 3 entregables es obligatorio. | E | `SRC-06-02`, `SRC-01-05` | — | `DEC-03` |
| **REQ-P-10** | Se puede usar IA **libremente**; se pide **transparencia** en el Entregable 3 y se conversará sobre decisiones concretas del proceso. | E | `SRC-06-05`, `SRC-01-07` | `REQ-D-08` | `DEC-37` |
| **REQ-P-11** | Si el enunciado es insuficiente, **documentar el supuesto y por qué**. | E | `SRC-07-10`, `SRC-04-11` | Sección de supuestos | `AMB-01…05` |
| **REQ-P-12** | Tratar el documento como **confidencial**: cada página está marcada "Uso interno". | D (de `SRC-00-01`) | `SRC-00-01` | — | `REQ-N-10`, `DEC-37` |

## 3. Entregables (`REQ-D`)
| ID | Requisito | T | Fuente | Verificación | Relacionado |
|---|---|---|---|---|---|
| **REQ-D-01** | **Entregable 1 — Evidencia técnica:** el vertical slice del track elegido **más** diseño/contrato/pseudocódigo de la capa complementaria. Debe permitir **verificar al menos una decisión relevante del caso**. | E | `SRC-05-02`, `SRC-01-05`, `SRC-04-17` | Existe y se puede ejecutar/revisar | `DEC-01`, `DEC-04` |
| **REQ-D-02** | El Entregable 1 indica el **track elegido** (Backend/Integración o Frontend/Experience) **y por qué**. | E | `SRC-05-02` | — | `DEC-01` |
| **REQ-D-03** | El Entregable 1 incluye **instrucciones para revisarlo o ejecutarlo**. | E | `SRC-05-02` | Un tercero puede ejecutarlo | — |
| **REQ-D-04** | El Entregable 1 declara el **alcance efectivamente implementado**. | E | `SRC-05-02` | — | `DEC-04` |
| **REQ-D-05** | El Entregable 1 lista **tests o validaciones** disponibles (y el slice incluye **≥ 1** validación o test). | E | `SRC-05-02`, `SRC-04-18`, `SRC-04-19` | Test pasa | `DEC-24`, `TC-01…20` |
| **REQ-D-06** | El Entregable 1 declara **limitaciones conocidas**. | E | `SRC-05-02` | — | — |
| **REQ-D-07** | **Entregable 2 — README de ingeniería (máx. 2 págs.):** (a) problema entendido y outcome esperado; (b) supuestos y alcance; (c) decisiones principales y **alternativas descartadas**; (d) qué quedó **determinístico / AI-assisted / agentic / human-controlled**; (e) riesgos y próximos pasos; (f) **cómo validaste**. | E | `SRC-05-03`, `SRC-01-05` | Revisión de contenido y largo | `REQ-D-09` |
| **REQ-D-08** | **Entregable 3 — AI Usage & Decision Note (máx. 1 pág.):** (a) herramientas de IA usadas y para qué; (b) outputs **aceptados, rechazados o modificados** y cómo se validaron; (c) decisiones tomadas **personalmente**; (d) qué información **nunca** se entregaría a un modelo. | E | `SRC-05-04`, `SRC-06-05` | — | `DEC-22`, `DEC-37` |
| **REQ-D-09** | La **clasificación de pasos** (determinístico / AI-assisted / agentic / human) debe aparecer (en el README o en la presentación) con **razón, riesgo y control/fallback**. La tabla es **opcional** como formato. | E | `SRC-05-05`, `SRC-05-03` | Tabla presente | `REQ-F-06` |
| **REQ-D-10** | Los **tres entregables** son obligatorios en su contenido. | E | `SRC-06-02` | — | — |
| **REQ-D-11** | Soporte de presentación (libre) que cubra `REQ-P-07`. | D | `SRC-06-03`, `SRC-01-06` | — | `DEC-03` |

## 4. Requisitos funcionales (`REQ-F`)

### 4.1 Del objetivo de negocio y las tareas
| ID | Requisito | T | Fuente | Verificación | Relacionado |
|---|---|---|---|---|---|
| **REQ-F-00** | **Alcance v1:** ayudar a **pasajeros cuyo vuelo sufrió una modificación**. | E | `SRC-01-09` | — | `GAP-07`, `DEC-04`, `DEC-31` |
| **REQ-F-01** | El pasajero puede **consultar el contexto de su viaje**. | E | `SRC-01-12`, `SRC-01-17` | `get_trip_context` → vista | `AMB-02`, `GAP-21`, `DAT-01…14`, `DEC-21` |
| **REQ-F-02** | El pasajero puede **entender si hubo una modificación relevante y qué implica**. | E | `SRC-01-13`, `SRC-01-18` | Caso base: "S1 retrasó 160 min; conexión en riesgo" | `AMB-01`, `DAT-15…30`, `DEC-05` |
| **REQ-F-03** | El pasajero recibe una **explicación o recomendación accionable** (qué ocurrió y cuál es su siguiente paso). | E | `SRC-01-14`, `SRC-01-10` | Mensaje con siguiente paso | `DEC-14`, `DEC-17`, `DEC-20` |
| **REQ-F-04** | El pasajero puede ser **derivado a una persona**, o **iniciar una acción controlada**, cuando corresponda. | E | `SRC-01-15`, `SRC-02-03`, `SRC-02-04` | `create_human_case` / `create_rebooking_request` | `AMB-03`, `AMB-04`, `DEC-15` |
| **REQ-F-05** | **Resolver el caso base:** a partir de la información disponible (reserva + eventos + políticas), determinar **qué ocurrió** y **qué corresponde ofrecer o comunicar**. | E | `SRC-04-21`, `SRC-04-18` | Resultado de `REQ-F-30` | `DAT-46`, `06_Analisis_cruzado §3` |
| **REQ-F-06** | **Diseñar** el manejo de una **consulta ambigua o compleja** que combine reserva, eventos y políticas: cómo se descompone el trabajo, **qué contexto se recupera**, **qué queda determinístico**, **qué se resuelve con IA o agente**, y **dónde se detiene para pedir intervención humana**. | E | `SRC-04-22`, `SRC-07-07` | Diagrama/tabla en README | `REQ-D-09`, `GAP-22`, `DEC-02` |
| **REQ-F-07** | **[Opción A — Backend/Integración]** Implementar la lógica del caso base como **servicio o función invocable**, con **manejo de errores** y **≥ 1 validación o test**. | E | `SRC-04-18`, `SRC-04-17` | Test automatizado | `DEC-01` |
| **REQ-F-08** | **[Opción B — Frontend/Experience]** Implementar la **pantalla o flujo** del pasajero que **consume datos equivalentes** a los de las tools y muestra **estado del viaje, alerta y recomendación**, con **≥ 1 validación**. | E | `SRC-04-19`, `SRC-04-17` | Demo/captura + validación | `DEC-01` |
| **REQ-F-09** | **Especificar** (sin implementar) la **capa complementaria**: si el track fue Backend → cómo se vería/comunicaría al pasajero (pantalla, wireframe o especificación del mensaje); si fue Frontend → qué contrato/lógica de backend asume. Profundidad en **un** track; capacidad de diseñar la integración. | E | `SRC-04-23`, `SRC-04-20`, `SRC-07-09` | Documento de diseño | `DEC-01`, `DEC-20` |
| **REQ-F-10** | **Decidir y justificar el uso de IA en runtime**; si no se incorpora, explicar **qué beneficio se esperaba** y **por qué** el riesgo, costo o complejidad no lo justifican. | E | `SRC-05-01`, `SRC-07-09` | Párrafo en README | `DEC-02` |

### 4.2 Ambigüedades declaradas → requisitos de decisión
El PDF dice: *"El enunciado no las define a propósito. Puedes decidirlas, documentarlas o explicitar qué preguntarías y a quién."* (`SRC-04-11`). Cada una es un **requisito de resolución** (ver también §6).
| ID | Requisito | T | Fuente | Relacionado |
|---|---|---|---|---|
| **REQ-F-11** | Definir **qué se considera una modificación relevante** (**AMB-01**). | E | `SRC-04-12` | `DEC-05`, `DEC-26`, `DEC-31`, `GAP-02`, `GAP-07` |
| **REQ-F-12** | Definir **qué información puede mostrarse al pasajero y cuál no** (**AMB-02**). | E | `SRC-04-13` | `DEC-21`, `DEC-22`, `GAP-21`, `DAT-01`, `DAT-02` |
| **REQ-F-13** | Definir **en qué casos una recomendación puede entregarse de forma automática** (**AMB-03**). | E | `SRC-04-14` | `DEC-14`, `DEC-17` |
| **REQ-F-14** | Definir **en qué casos debe intervenir una persona antes de actuar o comunicar** (**AMB-04**). | E | `SRC-04-15` | `DEC-15`, `DEC-16`, `DEC-13` |
| **REQ-F-15** | Definir **qué hacer cuando las fuentes entregan información contradictoria** (**AMB-05**). | E | `SRC-04-16` | `DEC-09`, `DAT-15`, `DAT-16` |

### 4.3 Comportamientos exigidos por el enunciado y los contratos
| ID | Requisito | T | Fuente | Verificación | Relacionado |
|---|---|---|---|---|---|
| **REQ-F-16** | **No entregar información no verificada** al pasajero; `notify_passenger` no debe enviar información no validada. | E | `SRC-01-10`, `SRC-02-05`, `SRC-04-03` | Todo hecho del mensaje ↔ evidencia | `REQ-F-29`, `DAT-65` |
| **REQ-F-17** | **No ejecutar acciones de alto impacto sin los controles correspondientes** (cambiar una reserva; emitir una compensación). | E | `SRC-01-10`, `SRC-04-06`, `SRC-02-03` | Escritura bloqueada sin control | `DEC-13`, `DEC-15`, `DEC-16` |
| **REQ-F-18** | Las recomendaciones deben ser **exactas**: una incorrecta genera costo, reclamo o incumplimiento de política. | E | `SRC-04-05` | Casos de prueba `TC` | `REQ-N-02` |
| **REQ-F-19** | Usar **reglas versionadas y verificables**; el mensaje debe llevar **`policy_ref`** (el servicio rechaza con `422 UNVALIDATED_CONTENT` si falta). | E | `SRC-02-02`, `SRC-03-03`, `SRC-04-03` | `policy_ref` == versión recuperada y vigente | `DAT-34`, `DAT-53` |
| **REQ-F-20** | Las **opciones son candidatas, no una decisión final**: el sistema selecciona y valida. | E | `SRC-02-01`, `SRC-03-02` | Filtro/validación explícitos | `DAT-31…37`, `DEC-17` |
| **REQ-F-21** | **Controlar timestamp, fuente y frescura** de los eventos operacionales. | E | `SRC-01-18`, `SRC-04-04` | Casos `TC-02/03/19` | `DAT-15…30`, `DEC-09`, `DEC-10`, `GAP-16` |
| **REQ-F-22** | **Tolerar información parcial** del contexto (`completeness: PARTIAL`) y **declararla**. | E | `SRC-01-17`, `SRC-02-07` | Caso `TC-12` | `DAT-09`, `DEC-11`, `GAP-17` |
| **REQ-F-23** | **Idempotencia** en `create_rebooking_request` con `idempotency_key`. | E | `SRC-02-03`, `SRC-03-04` | Misma operación ⇒ misma llave | `DAT-63`, `DEC-18` |
| **REQ-F-24** | Manejar **`409 DUPLICATE_REQUEST`** (existente) y **`503 UPSTREAM_TIMEOUT`** (**resultado indeterminado**). | E | `SRC-03-04`, `SRC-04-01` | `TC-14`, `TC-15` | `DAT-59`, `DAT-60`, `GAP-12`, `DEC-18` |
| **REQ-F-25** | Respetar la **vigencia (TTL = 120 s)** de las opciones; no actuar con opciones vencidas. | D (de `SRC-03-02`) | `SRC-03-02` | `TC-08` | `DAT-35`, `DAT-77`, `DEC-19`, `GAP-25` |
| **REQ-F-26** | **Escalar a operación humana** con **razón y evidencia** mediante `create_human_case` (cola `DISRUPTION_L2`, SLA 45 min en el ejemplo). | E | `SRC-02-04`, `SRC-04-02` | Caso humano creado con evidencia mínima | `DAT-64`, `GAP-26`, `DEC-15` |
| **REQ-F-27** | Si se usan **mocks propios, mantener los contratos** de las tools. | E | `SRC-01-16` | Mocks ↔ contratos de §6 | `DEC-22`, `DAT-38` |
| **REQ-F-28** | **Trazabilidad:** cada decisión/acción debe poder reconstruirse (datos usados con su `retrieved_at`, versión de política y `rule_id`, evento(s) elegido(s) y descartado(s), opción, acción, mensaje). | E (objetivo) / D | `SRC-01-11`, `SRC-07-05` | Registro de decisión completo | `DAT-73`, `DAT-80`, `DEC-23` |
| **REQ-F-29** | **Validar mensajes antes de notificar:** además del `policy_ref` exigido por el servicio, un validador **propio** que verifique que cada afirmación tiene evidencia vigente. | D (de `SRC-02-05` + `SRC-04-03`) | `SRC-02-05`, `SRC-04-03` | `TC-16` | `DAT-65`, `DEC-20` |

### 4.4 Resultado esperado del caso base `REQ-F-30` **[S/D — hipótesis a validar]**
Derivado de combinar `SRC-04-21` con los datos de `SRC-02-07`, `SRC-02-08`, `SRC-03-01`, `SRC-03-02`, `SRC-03-03`. **No lo dice el PDF**: lo deduzco. Cálculo paso a paso en `04_Analisis_de_Datos/06_Analisis_cruzado.md §3`.
| ID | Requisito | T | Fuente | Verificación | Relacionado |
|---|---|---|---|---|---|
| **REQ-F-30** | **Resultado esperado del caso base** `ABC123` (hipótesis; sub-resultados F-30a…h). | D/S | `SRC-04-21`, `SRC-04-18`, `SRC-02-07`, `SRC-02-08`, `SRC-03-01`, `SRC-03-02`, `SRC-03-03` | `TC-01` | `DEC-06`, `DEC-07`, `DEC-13`, `DEC-16`, `DEC-17`, `DAT-46`, `DAT-75` |

| Sub-req | Resultado esperado (hipótesis) | Supuesto clave | Datos |
|---|---|---|---|
| F-30a | S1 está **retrasado 160 min** (nueva salida 17:10, puerta 24); se **descarta** `E-1012`. | Resolución por recencia **y** salud de fuente | `DAT-15`, `DAT-16` |
| F-30b | S2: **sin información posterior** (no "a tiempo"). | — | `DAT-24` |
| F-30c | **`missed_connection = true`** (derivado: llegada a Lima 20:35 > salida de S2 19:05). | A1 propagación íntegra · A2 sin MCT · A3 S2 no se retiene | `DAT-75` |
| F-30d | **R1 falso (160<180), R2 falso, R3 verdadero, R5 verdadero**, R4 no aplica. | Definición de "menor" = `CHILD` | `DAT-46` |
| F-30e | **O1 viable**; **O2 no viable** (1 cupo < 2 pax; 180.000 CLP ≠ sin costo); **O3 no verificable**. | `seats ≥ pasajeros` | `DAT-31…33` |
| F-30f | Recomendar **O1** (sin costo, 16-sep 08:15) citando `POL-DELAY-2026-03`; mencionar la **vía de reembolso** sin monto. | — | `DEC-17`, `DEC-28` |
| F-30g | **Crear caso humano** (menor + pernocte + alojamiento no cubierto). **No** ejecutar el rebooking hasta resolver la aprobación y revalidar. | `DEC-13`/`DEC-16` | `DAT-47`, `DAT-77` |
| F-30h | **No afirmar**: hora de llegada a MEX, retención de S2, hotel/comidas, montos, causa, "ya está cambiado". | Falta de dato | `DAT-22`, `GAP-03` |

## 5. Restricciones y requisitos no funcionales (`REQ-N`)
| ID | Requisito | T | Fuente | Verificación | Relacionado |
|---|---|---|---|---|---|
| **REQ-N-01** | Los **datos operacionales** pueden estar **desactualizados o ser contradictorios** entre fuentes. | E | `SRC-04-04` | `TC-02`, `TC-03` | `REQ-F-15`, `REQ-F-21` |
| **REQ-N-02** | Una recomendación incorrecta puede generar **costo, reclamo o incumplimiento de política**. | E | `SRC-04-05` | — | `REQ-F-18` |
| **REQ-N-03** | **Cambiar una reserva** o **emitir una compensación** son acciones de **alto impacto**. | E | `SRC-04-06` | — | `REQ-F-17` |
| **REQ-N-04** | **Proteger datos personales** y aplicar **mínimo privilegio**. | E | `SRC-04-07` | Inventario PII; `DQ-26`; `TC-20` | `GAP-21`, `GAP-27`, `DAT-79`, `DEC-22` |
| **REQ-N-05** | La primera versión debe poder ser **operada por un equipo pequeño**. | E | `SRC-04-08` | Runbook mínimo | `GAP-24`, `DEC-24` |
| **REQ-N-06** | Considerar **latencia, costo por interacción y dependencia de modelos**. | E | `SRC-04-09` | Presupuestos declarados | `GAP-24`, `DEC-02`, `DEC-24` |
| **REQ-N-07** | **No existe una única solución correcta.** | E | `SRC-04-10`, `SRC-06-07` | — | `REQ-E-09` |
| **REQ-N-08** | Mantener **exactitud, seguridad y trazabilidad**. | E | `SRC-01-11` | — | `REQ-F-18`, `REQ-F-28`, `REQ-N-04` |
| **REQ-N-09** | **Resultado de negocio:** reducir la **incertidumbre del pasajero** y los **contactos evitables al call center**. (No hay métrica definida.) | E | `SRC-01-11` | Métrica propuesta (`GAP-23`) | `REQ-E-01`, `DEC-24` |
| **REQ-N-10** | **Confidencialidad** del documento ("Uso interno") y de los datos del caso. | D | `SRC-00-01` | — | `REQ-P-12`, `DEC-37` |

## 6. Contratos de las tools (`REQ-C`) — "mantén estos contratos" (`SRC-01-16`)
| ID | Tool | Firma | Tipo | Consideración (literal del PDF) | Respuestas del ejemplo | Fuente | Datos |
|---|---|---|---|---|---|---|---|
| **REQ-C-01** | `get_trip_context` | `(booking_id)` | Lectura | "Puede devolver información parcial." | `booking_id`, `passengers[]`, `segments[]`, `fare_conditions`, `_meta{retrieved_at, completeness, missing_fields}` | `SRC-01-17`, `SRC-02-07` | `01_get_trip_context.md` |
| **REQ-C-02** | `get_operational_events` | `(segment_ids)` | Lectura | "Requiere controlar timestamp, fuente y frescura." | `events[]{event_id, segment_id, type, …, source, recorded_at}`, `_meta{retrieved_at, sources_available, sources_degraded}` | `SRC-01-18`, `SRC-02-08`, `SRC-03-01` | `02_get_operational_events.md` |
| **REQ-C-03** | `get_eligible_options` | `(trip_context)` | Lectura | "Entrega opciones candidatas, no una decisión final." | `options[]{option_id, type, …, policy_ref, confidence}`, `_meta{retrieved_at, ttl_seconds:120}` | `SRC-02-01`, `SRC-03-02` | `03_get_eligible_options.md` |
| **REQ-C-04** | `get_policy_rules` | `(scenario)` | Lectura | "Reglas versionadas y verificables." | `{scenario, version, effective_from, rules[R1…R5], _meta{superseded_versions}}` | `SRC-02-02`, `SRC-03-03` | `04_get_policy_rules.md` |
| **REQ-C-05** | `create_rebooking_request` | `(option, idempotency_key)` | **Escritura** | "Acción de alto impacto." | `201 {request_id, status:PENDING_CONFIRMATION, expires_at}` · `409 DUPLICATE_REQUEST` · `503 UPSTREAM_TIMEOUT` (**indeterminado**) | `SRC-02-03`, `SRC-03-04`, `SRC-04-01` | `05_tools_de_escritura.md` |
| **REQ-C-06** | `create_human_case` | `(reason, evidence)` | **Escritura** | "Escalamiento a operación humana." | `201 {case_id, queue:DISRUPTION_L2, sla_minutes:45}` | `SRC-02-04`, `SRC-04-02` | `05_tools_de_escritura.md` |
| **REQ-C-07** | `notify_passenger` | `(message)` | **Escritura** | "No debe enviar información no validada." | `202 {notification_id, channel:PUSH, status:QUEUED}` · `422 UNVALIDATED_CONTENT ("falta policy_ref")` | `SRC-02-05`, `SRC-04-03` | `05_tools_de_escritura.md` |
| **REQ-C-08** | (ejemplos) | — | — | "Estos ejemplos son representativos… Úsalos como base de trabajo." | Los 7 bloques de ejemplo | `SRC-02-06` | `DAT-82` |

**Observaciones de contrato (todas con `DAT`):** la firma de `notify_passenger` no incluye destinatario (`DAT-65`); `create_rebooking_request` no incluye reserva ni pasajeros (`DAT-62`); `create_human_case` no tiene llave idempotente ni esquema de `evidence` (`DAT-64`); no hay tool para **consultar/confirmar/cancelar** el rebooking (`GAP-12`).

## 7. Ambigüedades **declaradas** por el PDF (`AMB`)
| AMB | Qué pregunta el PDF | Por qué importa (según los datos) | Qué haría falta | Relacionado |
|---|---|---|---|---|
| **AMB-01** `SRC-04-12` | ¿Qué es una **modificación relevante**? | El ejemplo mezcla un retraso (160 min), un cambio de puerta y un estado. Umbral de política: R1=180 min; umbral comercial de la aerolínea: **31 min** (retraso), **16 min** (adelanto). | Criterio explícito (por umbral, por impacto en itinerario, o por tipo). | `GAP-02`, `GAP-07`, `DAT-23`, `POL-CL-03`, `POL-UY-01/02`, `DEC-05`, `DEC-26`, `DEC-31` |
| **AMB-02** `SRC-04-13` | ¿Qué **información** se muestra al pasajero y cuál no? | `trip_context` trae PII; el menor tiene datos; las reglas son internas. | Lista blanca de campos y de hechos; verificación de identidad. | `GAP-21`, `DAT-01`, `DAT-02`, `DAT-03`, `DEC-21`, `DEC-22` |
| **AMB-03** `SRC-04-14` | ¿Cuándo una recomendación va **automática**? | `R1/R3` no exigen aprobación, `R4/R5` sí; pero rebookear es "alto impacto". | Matriz acción × condiciones. | `DAT-47`, `DEC-14`, `DEC-17` |
| **AMB-04** `SRC-04-15` | ¿Cuándo interviene una **persona** antes de actuar/comunicar? | Menor (R5), compensación (R4), datos parciales, fuentes en conflicto, 503. | Disparadores explícitos. | `DAT-47`, `DEC-15`, `DEC-16` |
| **AMB-05** `SRC-04-16` | ¿Qué hacer con **fuentes contradictorias**? | `E-1012` vs `E-1001`; `event_id` no ordena; fuente degradada. | Precedencia + frescura + degradación. | `DAT-15`, `DAT-16`, `DAT-26`, `DEC-09` |

## 8. Brechas detectadas por mí (`GAP`)
> Cosas que **el PDF no dice** y que **podrían hacer falta**. **P** = relacionada con política externa (ver archivo); **N** = no relacionada. Prioridad: `C`ritica / `A`lta / `M`edia para el caso base.

| GAP | Qué falta | Dónde se nota | P/N | Política externa a revisar (**tu decisión**) | DEC | Pri. |
|---|---|---|---|---|---|---|
| **GAP-01** | **Jurisdicción** aplicable por segmento. Las reglas no traen país; S1 sale de **Chile**, S2 de **Perú** (Decisión 619 aplica a quien "inicia" el viaje en un país andino: ambiguo). | `SRC-03-03`; `DAT-51` | P | `03_Chile` (POL-CL-00, 07) · `04_Peru` (POL-PE-01) · `00_LEEME §3` | `DEC-25` | A |
| **GAP-02** | **Umbral de cambio sin costo por retraso**: R1=**180 min** vs política la aerolínea **31 min**. | `SRC-03-03`; `DAT-46`, `DAT-55` | P | `01_la aerolínea_UY` (POL-UY-01) · `03_Chile` (POL-CL-02/03) | `DEC-26` | A |
| **GAP-03** | **Asistencia** durante la espera (comunicación, comida, alojamiento, traslado): el PDF solo tiene `MEAL_VOUCHER` a ≥240 min internacional. | `SRC-03-03`; `DAT-39`, `DAT-55` | P | `03_Chile` (POL-CL-01/04) · `04_Peru` (POL-PE-07) · `05_Colombia` · `11_Paraguay` · `07_Argentina` | `DEC-27` | A |
| **GAP-04** | **Reembolso**: no hay regla (O3 usa `POL-REFUND-2026-01`, no recuperada); `refundable:false`. | `SRC-03-02`; `DAT-33`, `DAT-11` | P | `03_Chile` (POL-CL-07, 16) · `04_Peru` (POL-PE-10) · `01_la aerolínea_UY` (POL-UY-03) | `DEC-28` | A |
| **GAP-05** | **Compensación económica**: `R4` es solo una bandera; sin montos ni base. | `SRC-03-03`; `DAT-50` | P | `04_Peru` (POL-PE-07 e) · `05_Colombia` · `02_UE` · `13_UK` · `03_Chile` (solo sobreventa) | `DEC-29` | M |
| **GAP-06** | **Causa** del evento (clima, fuerza mayor, técnica, ATC): no existe y las normas la usan como exención. | `SRC-02-08`; `DAT-22`, `DAT-49` | P | `03_Chile` (POL-CL-01) · `04_Peru` (POL-PE-06) · `02_UE` (POL-UE-03) | `DEC-30` | A |
| **GAP-07** | **Otros eventos/escenarios**: cancelación, adelanto, desvío, sobreventa no tienen política ni ejemplo; `scenario` sin enumerar. | `SRC-03-03`; `DAT-18`, `DAT-50` | P | `01_la aerolínea_UY` (POL-UY-02/03) · `05_Colombia` (POL-CO-07) · `02_UE` (adelanto > 1 h = cancelación) | `DEC-31`, `DEC-04` | M |
| **GAP-08** | **Definición de "menor"** (edad) y derechos asociados. | `SRC-03-03`; `DAT-03` | P | `03_Chile` (POL-CL-13: < 14) · `04_Peru` (art. 3/10: < 5) · `06_Uruguay` (< 5; 18 migratorio) | `DEC-32` | A |
| **GAP-09** | **Plazo y contenido de la notificación** al pasajero (aviso ≥ 4 h, información escrita de derechos). | `SRC-02-05`; `DAT-65` | P | `04_Peru` (POL-PE-03) · `05_Colombia` (POL-CO-02) · `09_Bolivia` (POL-BO-01) | `DEC-33` | M |
| **GAP-10** | **Plazos** de reembolso/cambio (12 meses; 5 días hábiles; 10 días hábiles; 7/15/30 días). | — | P | `01_la aerolínea_UY` (12 meses) · `04_Peru` (POL-PE-10) · `03_Chile` (POL-CL-06) · `10_Ecuador` · `08_Brasil` | `DEC-28` | M |
| **GAP-11** | **Tiempo mínimo de conexión (MCT)** y terminales. | `SRC-02-07`; `DAT-07` | N | — | `DEC-07` | C |
| **GAP-12** | **Ciclo de vida del rebooking** (`PENDING_CONFIRMATION` sin confirmar/consultar/cancelar; `503` sin reconciliación). | `SRC-03-04`; `DAT-59`, `DAT-61` | N | — | `DEC-18` | C |
| **GAP-13** | **`notify_passenger`**: destinatario, canal, esquema del mensaje, idioma. | `SRC-04-03`; `DAT-65`, `DAT-71` | N | — | `DEC-20` | A |
| **GAP-14** | **México** (destino final) **no figura** en la lista de países de la página de la aerolínea. | `00_LEEME §3` | P | (ninguna: no hay fuente) | `DEC-34` | M |
| **GAP-15** | **Zonas horarias y fechas**: horas locales sin offset; `new_departure` sin fecha; sin llegada nueva. | `SRC-02-07`; `DAT-05`, `DAT-06`, `DAT-20` | N | — | `DEC-08` | A |
| **GAP-16** | **Precedencia de fuentes** y **umbrales de frescura**. | `SRC-03-01`; `DAT-15`, `DAT-17` | N | — | `DEC-09`, `DEC-10` | C |
| **GAP-17** | **Semántica de `confidence` y `completeness`**; qué dato faltante bloquea qué decisión. | `SRC-03-02`; `DAT-09`, `DAT-36` | N | — | `DEC-11`, `DEC-17` | A |
| **GAP-18** | **Variables de política** que no existen en los datos y **gramática** de `condition`. | `SRC-03-03`; `DAT-45`, `DAT-48` | N | — | `DEC-12` | C |
| **GAP-19** | **Semántica de los derechos** (`PRIORITY_HANDLING`, `CASH_COMPENSATION`, `MEAL_VOUCHER`) y **precedencia** entre reglas (R3 vs R5). | `SRC-03-03`; `DAT-47`, `DAT-52` | N | — | `DEC-13` | A |
| **GAP-20** | **Grupo familiar y cabina**: opciones sin mapa por pasajero ni cabina; "mantener al menor con un adulto". | `SRC-03-02`; `DAT-31`, `DAT-41`, `DAT-43` | N | `03_Chile` (POL-CL-13) | `DEC-16`, `DEC-17` | A |
| **GAP-21** | **Autenticación** del pasajero y control de acceso. | `SRC-01-12`; `DAT-01` | N | — | `DEC-21` | C |
| **GAP-22** | **Canal y forma de la "consulta"** (chat, app, web; libre o estructurada) e idioma. | `SRC-04-22` | N | — | `DEC-02`, `DEC-20` | M |
| **GAP-23** | **Métricas de éxito** (reducción de contactos, exactitud) y línea base. | `SRC-01-11`, `SRC-07-01` | N | — | `DEC-24` | M |
| **GAP-24** | **Presupuestos** de latencia/costo/disponibilidad y modelo de operación. | `SRC-04-08`, `SRC-04-09` | N | — | `DEC-24` | M |
| **GAP-25** | **Vigencias incompatibles**: TTL 2 min < expiración ≈ 9 min < SLA humano 45 min. | `SRC-03-02`, `SRC-03-04`, `SRC-04-02`; `DAT-77` | N | — | `DEC-19` | A |
| **GAP-26** | **Caso humano**: esquema de `reason`/`evidence`, deduplicación y **quién aprueba**. | `SRC-02-04`; `DAT-64` | N | — | `DEC-15` | A |
| **GAP-27** | **Marco de protección de datos** aplicable y **retención** de registros/logs. | `SRC-04-07`; `DAT-79` | N | — (no hay fuente en esta carpeta) | `DEC-22`, `DEC-23` | M |

## 9. Criterios de evaluación → qué evidencia los cubre (`REQ-E`)
| ID | Dimensión (literal) | Fuente | Evidencia que debes poder mostrar | Requisitos relacionados |
|---|---|---|---|---|
| **REQ-E-01** | Pensamiento de producto: cómo entiendes y acotas, qué supuestos explicitas, qué priorizas **y cómo lo medirías**. | `SRC-07-01` | README (a, b); **métrica propuesta** | `REQ-D-07`, `REQ-N-09`, `GAP-23` |
| **REQ-E-02** | Fundamentos de ingeniería: contratos, estados, errores, límites, integración. | `SRC-07-02` | Contratos `REQ-C`, manejo `409/503`, idempotencia, TTL | `REQ-F-22…25`, `REQ-C-01…07` |
| **REQ-E-03** | Desarrollo asistido por IA: controles, qué verificas, qué aceptas/corriges/rechazas. | `SRC-07-03` | Entregable 3 | `REQ-D-08`, `REQ-P-10` |
| **REQ-E-04** | Calidad, seguridad y confiabilidad: comprobaciones, fallos, permisos, datos sensibles, operación. | `SRC-07-04` | `DQ`/`TC`, inventario PII, runbook | `REQ-N-04`, `REQ-N-05`, `REQ-F-16/17/29` |
| **REQ-E-05** | Priorización y evidencia: tiempo en lo importante, evidencia **localizable**, pendientes **explícitos**. | `SRC-07-05` | Índice de IDs, sección de pendientes | `REQ-D-03…06`, `REQ-F-28` |
| **REQ-E-06** | Juicio técnico y trade-offs: alternativas, consecuencias, costos, riesgos, reversibilidad. | `SRC-07-06` | Decisiones con alternativas descartadas | `REQ-D-07 (c)`, `06_Decisiones` |
| **REQ-E-07** | Razonamiento agentic y control: dónde IA/agente vs. determinístico vs. humano; contexto, herramientas, permisos; dónde se detiene; cómo detectas un output incorrecto. | `SRC-07-07` | Tabla de clasificación de pasos | `REQ-F-06`, `REQ-D-09`, `DEC-02` |
| **REQ-E-08** | Responsabilidad y adaptación: asumes el resultado, reconoces límites, revisas decisiones ante información nueva. | `SRC-07-08` | Defensa; sección de limitaciones | `REQ-P-08`, `REQ-D-06` |
| **REQ-E-09** | **Principio:** se evalúa el **criterio** sobre el volumen; no hay una única solución correcta; **no se penaliza**: no terminar la capa complementaria, no usar IA en runtime, no usar MCP/framework, pseudocódigo no esencial, UI poco pulida, solución distinta, velocidad, conocimiento del dominio aéreo, estética, uso/no uso de IA por sí mismo. | `SRC-01-08`, `SRC-06-06`, `SRC-06-07`, `SRC-07-09` | — | `REQ-N-07`, `REQ-P-04` |

## 10. Suposiciones de trabajo mías (`S-nn`) — **confírmalas o corrígelas**
| ID | Suposición | Efecto si es falsa | DEC |
|---|---|---|---|
| S-01 | El análisis cubre la **primera versión** (v1) y el **caso base** `ABC123` (`SRC-04-21`). | Faltaría cubrir más eventos | `DEC-04` |
| S-02 | "Menor" = pasajero `type == CHILD` (en el ejemplo, 7 años). | `R5` se activaría distinto | `DEC-32` |
| S-03 | Las horas sin zona son **locales del aeropuerto** correspondiente. | La conexión y la edad cambian | `DEC-08` |
| S-04 | El retraso de S1 se **propaga íntegro** al arribo (A1), sin MCT (A2) y S2 no se retiene (A3). | `missed_connection` podría ser falso | `DEC-07` |
| S-05 | "Acción de alto impacto" incluye `create_rebooking_request` y `CASH_COMPENSATION`; el **mensaje** al pasajero es de riesgo medio-alto. | Cambia los controles | `DEC-14`, `DEC-20` |
| S-06 | `409` = existente (éxito idempotente). | Doble ejecución | `DEC-18` |
| S-07 | Las políticas externas **no** son requisito: son **insumos para tu decisión**. | — | `DEC-35` |
| S-08 | El PDF es la **única** fuente de requisitos; la web de la aerolínea es contexto. | — | `DEC-35` |

## 11. Matriz de trazabilidad inversa (SRC → REQ)
Ver el archivo generado `01_Fuente_y_Trazabilidad/02_Matriz_SRC_a_REQ.md`. Verificado por script: **77 de las 78 entradas `SRC` están citadas por al menos un requisito**; la única sin requisito propio es `SRC-01-01` (el título del documento).
