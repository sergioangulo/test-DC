# RFC: Disruption Companion

**Status**: DRAFT
**Date**: 2026-10-19
**Author**: sdd-workflow-mcp (BUILDER, paso A2)

---

## How to Use This RFC

This RFC is the **formal communication interface** between the SDD workflow and your team. Business stakeholders review the functional sections (1-4), technical stakeholders review the technical sections (5-8), and everyone reviews the results (9).

> **Important**: The functional specs (`sdd/specs/functional/*.md`) are the source of truth. This RFC is a consolidated view generated from those specs. If you have feedback, edit this RFC — the agent will reconcile your changes back into the individual specs.

Estado de este borrador (paso A2): consolida los **104 specs funcionales** (12 flujos del backend F-01 a F-12 con sus subflujos, 4 flujos del front FE-01 a FE-04 con sus subflujos, y 2 specs de apoyo X-01 y X-02). La cobertura de requisitos está en `sdd/reports/FR_COVERAGE.md` y las preguntas abiertas en `sdd/reports/A2_OPEN_QUESTIONS.md`. Las secciones técnicas (5 a 9) enlazan a `ARCHITECTURE.md` y `EXTERNAL_CONTRACTS.md`, que siguen siendo su fuente.

---

## 1. Context and Objective

**Propósito.** Disruption Companion es un acompañante para pasajeros ante disrupciones de vuelo, en particular retrasos que pueden hacer perder una conexión. Dada una reserva, combina el contexto del viaje, los eventos operacionales y las reglas de política para mostrar al pasajero qué cambió, qué implica y, solo cuando una política se rompe, qué opciones viables tiene y qué acciones puede autorizar con un clic: aceptar una opción de cambio o hablar con una persona. Un retraso que no rompe ninguna política solo se informa. La misma evaluación puede pedirla otro sistema, que recibe un resultado sin información personal y dispara avisos con plantilla fija.

**Problema que resuelve.** Ante un retraso, el pasajero no sabe si perderá su conexión, qué derechos tiene ni qué alternativas existen, y las decisiones sobre datos operacionales dudosos o contradictorios no deben automatizarse a ciegas.

**Objetivos.**

- Mostrar el contexto, la causa del cambio y la estimación de la conexión sin afirmar más de lo que la evidencia respalda (FR-080 a FR-084).
- Decidir de forma determinística y auditable, sin inteligencia artificial en ejecución (NFR-001), con reglas de política evaluadas por un analizador acotado (FR-030 a FR-039).
- Proponer solo opciones viables y respaldadas, y ejecutar una acción externa únicamente tras un clic explícito del pasajero (FR-050), con la notificación del sistema como única excepción (FR-122).
- Degradar a una persona ante anomalías, conflictos, datos desconocidos o errores, nunca a «sin novedad» (FR-007, FR-013, FR-038, FR-105).
- Proteger la privacidad por diseño: solo el nombre de pila es visible y ningún dato personal se persiste ni se envía a otras herramientas (FR-091, FR-112, NFR-002).
- Mantener todos los parámetros de negocio configurables y validados al arrancar (NFR-012).

**Alcance de la versión 1.** Servicio de decisión (evidencia principal) y front de prueba, con las siete herramientas externas simuladas; los elementos de Fase 2 (disparo automático por evento, confirmación de la solicitud, adaptador real, políticas externas, memoria intermedia) quedan fuera (`REQUERIMIENTOS_V1.md` §7).

**Riesgo de proporcionalidad.** Los 104 specs y unos 400 escenarios son desproporcionados frente al plazo de 3 horas del reto (REQ-P-01). **Slice de implementación prioritario:** el caso base (TC-01), TC-01 a TC-20 y el modo sistema (TC-42 a TC-44, TC-50 a TC-52 y TC-55); el resto se implementa solo si alcanza el tiempo (X-01, OQ-A2-21).

**Cobertura.** 96 FR, 13 NFR y 13 DOC cubiertos por al menos un spec; los 60 casos de prueba TC-01 a TC-60 están asignados a specs (`FR_COVERAGE.md`, verificado por `sdd/scripts/check_specs.py`).

---

## 2. Business Flows

### 2.1 F-01 Evaluar viaje como pasajero

**Spec fuente**: [F-01 Evaluar viaje como pasajero](01-f-01-evaluar-viaje-como-pasajero.md)  
**Requisitos**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-031, FR-032, FR-033, FR-034, FR-035, FR-036, FR-037, FR-038, FR-039, FR-040, FR-041, FR-042, FR-043, FR-044, FR-045, FR-046, FR-047, FR-048, FR-049, FR-057, FR-058, FR-060, FR-063, FR-064, FR-066, FR-067, FR-068, FR-070, FR-071, FR-080, FR-081, FR-082, FR-083, FR-084, FR-085, FR-086, FR-090, FR-091, FR-105, FR-110, FR-112, FR-120, NFR-001, NFR-004, NFR-012, NFR-013  
**Pruebas (TC)**: TC-01, TC-02, TC-03, TC-04, TC-05, TC-06, TC-07, TC-09, TC-10, TC-11, TC-12, TC-13, TC-18, TC-19, TC-23, TC-24, TC-25, TC-26, TC-27, TC-28, TC-29, TC-35, TC-36, TC-37, TC-39, TC-45, TC-46, TC-47, TC-51, TC-52, TC-53, TC-54, TC-58, TC-60

Construye la vista completa de una reserva para el pasajero: contexto, eventos, anomalías, variables derivadas, reglas evaluadas, opciones viables, acciones ofrecidas, plazos y mensajes, y registra la decisión. Cada entrada reconsulta los datos.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una reserva de dos pasajeros (un adulto y un niño) con un retraso validado de 160 minutos, política de retrasos recuperada y una opción viable | el pasajero entra a la vista | ve el contexto, el retraso, la conexión estimada, las reglas que se cumplen y las que no, la opción propuesta con la vía de reembolso no afirmativa, la hora límite y las acciones ofrecidas; la decisión exige aprobación humana por el menor y no se escribe nada externo |
| 2 | una reserva cuyos eventos son solo de estado informado o no existen | el pasajero entra a la vista | ve solo el contexto del viaje, sin alertas, reglas, opciones ni botones de soporte, y la decisión es nula |
| 3 | una conexión perdida desconocida por tiempo mínimo de conexión no provisto, con política rota y opciones en el proveedor | el pasajero entra a la vista | ninguna opción es viable, la decisión es BLOQUEADA y se ofrece «Hablar con una persona»; no se afirma ni niega la conexión |
| 4 | el pasajero ya vio la vista hace un minuto | vuelve a entrar | el sistema consulta de nuevo el contexto y los eventos y genera un registro de decisión nuevo |
| 5 | el caso base de la reserva ABC123 con Ana (adulta) y un niño, LA500 SCL-LIM 14:30 y LA2410 LIM-MEX 19:05, el retraso E-1001 de 160 min, el estado E-1012 de una fuente degradada, la política POL-DELAY-2026-03 y el contexto parcial: falta el monto de penalidad de cambio | Ana abre la vista a las 11:02:47Z | ve el retraso de 160 min con nueva salida 17:10, que R3 y R5 se cumplen y R1, R2 y R4 no, la opción propuesta O1 LA2412 con 4 asientos, la decisión PENDIENTE_APROBACION por el menor y ninguna escritura externa; O2 y O3 no se muestran y, sin monto de penalidad, no se cotiza ningún cambio voluntario |

**Acceptance Criteria**:

- [ ] La vista del caso base responde en menos de 1,5 s (percentil 95) con proveedores simulados de 100 ms, en 50 solicitudes secuenciales.
- [ ] Con las mismas lecturas y el mismo reloj, el 100 % de las evaluaciones produce la misma huella de decisión y los mismos mensajes.
- [ ] El 0 % de los mensajes mostrados afirma un hecho sin evidencia vigente (los bloqueados no llegan al pasajero).
- [ ] El 100 % de los escenarios con anomalía termina en decisión BLOQUEADA y no consulta política ni opciones; el 100 % de los retrasos sin política rota termina en decisión INFORMATIVA y no consulta opciones.
- [ ] Cada evaluación deja exactamente un registro de decisión sin ningún campo de la lista prohibida.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Contexto del viaje | booking_id, passenger_count, passengers, segments, fare_conditions, retrieved_at, completeness, missing_fields | Reserva del pasajero con sus tramos; se reduce de inmediato a lo mínimo necesario (sin correo, teléfono, documento, nombre completo ni edad). |
| Evento operacional | event_id, segment_id, type, delay_minutes, new_departure, gate, status, source, recorded_at | Hecho operacional informado por una fuente (retraso, cambio de puerta, estado) con su instante de registro. |
| Estado resuelto del segmento | segment_id, state, affected, delay_minutes, gate, gate_recorded_at, information_as_of, discarded_events | Resultado de validar los eventos de un segmento: qué se afirma de su salida y de su puerta. |
| Variable derivada | name, segment_id, value, known, origin, estimated, assumptions | Valor calculado a partir de los datos, con su origen y sus supuestos. |
| Política y regla | scenario, status, version, effective_from, superseded_versions, entitlements, requires_human_approval, rules | Versión recuperada de la política de retrasos y el resultado de evaluar cada una de sus reglas. |
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, date, departure, fare_difference, currency, seats_available, policy_ref, confidence, viable, discard_reasons, fingerprint, is_proposed, overnight, expires_at | Alternativa candidata entregada por el proveedor; solo las viables se muestran. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, load_status, data_as_of, segments, alerts, derived_variables, policy, options, proposed_option_id, refund_notice, offer_deadline, actions, messages, operations, human_cases | Respuesta completa para el pasajero; solo contiene campos de la lista blanca. |
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Validar sesión → Leer contexto y eventos → Verificar integridad → Validar eventos → Detectar anomalía → Leer política → Derivar variables → Evaluar reglas → Filtrar opciones → Definir acciones y motivos → Construir mensajes → Registrar decisión → Entregar la vista
```

Subprocess detail (if applicable):

```
SF-01.1: Validación de cuerpo y autorización de sesión
SF-01.2: Lectura de contexto y eventos
SF-01.3: Integridad de lecturas
SF-01.4: Validación de eventos
SF-01.5: Detección de anomalía y bloqueo previo
SF-01.6: Lectura de política
SF-01.7: Derivación de variables
SF-01.8: Evaluación de reglas y estado de la decisión
SF-01.9: Lectura y filtrado de opciones
SF-01.10: Motivos, soporte y acciones ofrecidas
SF-01.11: Construcción y validación de mensajes
SF-01.12: Barrido perezoso del ciclo de vida
SF-01.13: Huella por opción y registro de decisión
SF-01.14: Ensamblado de la respuesta
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.2 SF-01.1 Validación de cuerpo y autorización de sesión

**Spec fuente**: [SF-01.1 Validación de cuerpo y autorización de sesión](02-sf-01-1-validacion-de-cuerpo-y-autorizacion-de-sesion.md)  
**Requisitos**: FR-001, FR-120, NFR-003, NFR-013  
**Pruebas (TC)**: TC-21, TC-58

Comprueba quién pide la evaluación y si puede pedirla: el valor del modo de llamada, la sesión del pasajero y la pertenencia de la reserva.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el modo de llamada indica pasajero y la sesión coincide con la reserva de la ruta | se pide la evaluación | el flujo continúa con la sesión autorizada |
| 2 | una sesión de la reserva A pide la reserva B (ajena) y luego la reserva Z (inexistente) | se comparan ambas respuestas | ambas son la misma respuesta de «no encontrado», con el mismo contenido y sin repetir la entrada |
| 3 | la misma reserva y credencial ya hicieron `EVALUATE_RATE_LIMIT_PER_MINUTE` solicitudes en el último minuto | llega una más | se rechaza por límite de tasa antes de comprobar la pertenencia y sin consultar herramientas externas |
| 4 | la petición no trae sesión o la sesión simulada está apagada | se pide la evaluación | el sistema rechaza por falta de autenticación y no consulta ninguna herramienta externa |
| 5 | la sesión de ABC123 y las reservas XYZ789 (ajena) y ZZZ999 (inexistente) | se piden ambas evaluaciones | las dos respuestas son idénticas de «no encontrado», sin repetir el identificador pedido |

**Acceptance Criteria**:

- [ ] El 100 % de las respuestas a una reserva ajena y a una inexistente son idénticas en estado y contenido.
- [ ] El 100 % de las peticiones sin sesión válida se rechaza antes de consultar cualquier herramienta externa.
- [ ] Ningún mensaje de error contiene trazas ni repite la entrada recibida.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | Identidad con la que se pide una evaluación: sesión del pasajero o credencial de servicio. |

**Business Process (BPM)**:

```
Recibir petición → Validar modo de llamada → Comprobar sesión → Aplicar límite de tasa → Comprobar pertenencia → Autorizar
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.3 SF-01.2 Lectura de contexto y eventos

**Spec fuente**: [SF-01.2 Lectura de contexto y eventos](03-sf-01-2-lectura-de-contexto-y-eventos.md)  
**Requisitos**: FR-002, FR-105, FR-009, NFR-004  
**Pruebas (TC)**: TC-33

Consulta, en secuencia, el contexto del viaje y los eventos operacionales de los segmentos de la reserva, con una re-consulta ante fallo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el contexto y los eventos responden correctamente | el pasajero abre la reserva | se consulta primero el contexto del viaje y después los eventos con los segmentos obtenidos, sin llamadas en paralelo |
| 2 | la consulta del contexto falla por tiempo agotado y la re-consulta también | el pasajero abre la reserva | no se construye la vista: se responde «no pudimos cargar tu viaje» con la posibilidad de reintentar y sin soporte |
| 3 | el contexto responde y los eventos fallan tras la re-consulta | el pasajero abre la reserva | se muestra el contexto sin estado ni alerta, con un aviso, sin decisión y sin soporte |
| 4 | el contexto de ABC123 responde a las 11:02:31Z y los eventos de S1 (LA500) y S2 (LA2410) fallan dos veces seguidas | se arma la lectura | se muestra el contexto con ambos segmentos sin estado, un aviso y ninguna decisión; hubo exactamente 2 consultas de eventos |

**Acceptance Criteria**:

- [ ] El 100 % de las entradas del pasajero provoca una nueva consulta de contexto y de eventos.
- [ ] Ante una falla de lectura se realiza exactamente una re-consulta y nunca más.
- [ ] En el peor caso con los valores por defecto la cadena de lecturas del flujo completo no excede 16 s.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Contexto del viaje | booking_id, passenger_count, passengers, segments, fare_conditions, retrieved_at, completeness, missing_fields | Reserva del pasajero con sus tramos; se reduce de inmediato a lo mínimo necesario (sin correo, teléfono, documento, nombre completo ni edad). |
| Evento operacional | event_id, segment_id, type, delay_minutes, new_departure, gate, status, source, recorded_at | Hecho operacional informado por una fuente (retraso, cambio de puerta, estado) con su instante de registro. |

**Business Process (BPM)**:

```
Consultar contexto del viaje → Consultar eventos operacionales → Re-consultar si falló → Entregar lecturas o fallo acotado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.4 SF-01.3 Integridad de lecturas

**Spec fuente**: [SF-01.3 Integridad de lecturas](04-sf-01-3-integridad-de-lecturas.md)  
**Requisitos**: FR-066, FR-038, FR-086  
**Pruebas (TC)**: TC-39

Verifica que lo leído sea utilizable: instante de lectura, segmentos y pasajeros presentes, formatos válidos, cadena de segmentos y composición del grupo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la lectura del contexto no trae instante de lectura o trae cero segmentos | se verifica la integridad | es una lectura fallida: sin decisión, con aviso y reintento y sin soporte |
| 2 | el destino de un segmento no coincide con el origen del siguiente, o hay un niño sin adulto en la reserva | se verifica la integridad | la conexión queda desconocida y la decisión BLOQUEADA con el motivo de datos parciales bloqueantes |
| 3 | los segmentos llegan fuera de orden pero encadenan | se verifica la integridad | se reordenan por fecha y salida programada y no hay bloqueo |
| 4 | el destino de LA500 es LIM pero el origen del segundo segmento es MEX | se verifica la integridad | la conexión queda desconocida y la decisión es BLOQUEADA con datos parciales bloqueantes |

**Acceptance Criteria**:

- [ ] El 100 % de las lecturas inválidas termina sin decisión y sin soporte.
- [ ] El 100 % de las cadenas rotas y de los menores sin adulto termina BLOQUEADO con conexión desconocida.
- [ ] Los segmentos desordenados se reordenan en el 100 % de los casos sin generar bloqueo.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Contexto del viaje | booking_id, passenger_count, passengers, segments, fare_conditions, retrieved_at, completeness, missing_fields | Reserva del pasajero con sus tramos; se reduce de inmediato a lo mínimo necesario (sin correo, teléfono, documento, nombre completo ni edad). |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |

**Business Process (BPM)**:

```
Revisar instante y formatos → Revisar segmentos y pasajeros → Revisar cadena y menor → Clasificar el resultado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.5 SF-01.4 Validación de eventos

**Spec fuente**: [SF-01.4 Validación de eventos](05-sf-01-4-validacion-de-eventos.md)  
**Requisitos**: FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-007, FR-006  
**Pruebas (TC)**: TC-02, TC-03, TC-13, TC-19, TC-24, TC-25, TC-26, TC-36, TC-54

Decide qué eventos son evidencia y qué estado resulta para cada segmento: excluye degradados e inválidos, aplica la precedencia por instante, detecta conflicto y conserva la puerta vigente.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | un segmento tiene un retraso sano y un estado «a tiempo» de una fuente degradada posterior | se validan los eventos | el degradado se excluye con la razón fuente degradada y el retraso se mantiene |
| 2 | un segmento tiene un retraso y un estado «horario programado» sano de instante posterior | se validan los eventos | el segmento queda «programado» y no hay retraso ni alerta |
| 3 | dos eventos sanos del mismo segmento tienen el mismo instante de registro y afirman «retrasado» y «a tiempo» | se validan los eventos | no se afirma ningún estado: aviso neutro y caso humano por conflicto de fuentes |
| 4 | un segmento solo tiene eventos degradados, y otro no tiene eventos o solo cambios de puerta | se validan los eventos | el primero muestra «sin información verificada» y el segundo su horario programado, sin alertar |
| 5 | E-1001 (DELAY de 160 min, OPS_CORE, 10:48:00Z) y E-1012 (ON_TIME, LEGACY_MIRROR degradada, 11:00:00Z) | se validan los eventos de S1 | E-1012 se excluye con la razón fuente degradada y el estado sigue siendo retrasado 160 min |
| 6 | E-1001 de 160 min a las 10:48:00Z y un estado sano «horario programado» a las 11:00:00Z en S1 | se validan los eventos | S1 queda programado y no hay alerta de retraso |
| 7 | un retraso de 100 min a las 10:30:00Z y otro de 160 min a las 10:48:00Z, más un evento del segmento S9 que no se pidió y otro con instante 11:20:00Z posterior a la lectura de 11:02:33Z | se validan los eventos | gana el de 160 min sin conflicto y los otros dos se descartan con las razones segmento desconocido y marca futura |
| 8 | dos eventos sanos de S1 con el mismo instante 10:48:00Z que dicen «retrasado 160 min» y «a tiempo», y S2 sin eventos | se validan los eventos | S1 queda en conflicto sin afirmar estado y S2 muestra su horario programado 19:05 sin alertar |
| 9 | S1 solo tiene E-1012 (ON_TIME de LEGACY_MIRROR, fuente degradada) | se validan los eventos de S1 | E-1012 se excluye con la razón fuente degradada; S1 se muestra «sin información verificada», nunca «a tiempo», sin alerta ni botón |

**Acceptance Criteria**:

- [ ] El 100 % de los eventos de fuentes degradadas queda excluido y registrado con su razón.
- [ ] Ningún orden depende del identificador del evento: reordenar los identificadores no cambia el resultado.
- [ ] El 100 % de los empates conflictivos termina en aviso neutro, sin afirmar estado.
- [ ] Un segmento sin evidencia nunca se muestra como «a tiempo».

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Evento operacional | event_id, segment_id, type, delay_minutes, new_departure, gate, status, source, recorded_at | Hecho operacional informado por una fuente (retraso, cambio de puerta, estado) con su instante de registro. |
| Estado resuelto del segmento | segment_id, state, affected, delay_minutes, gate, gate_recorded_at, information_as_of, discarded_events | Resultado de validar los eventos de un segmento: qué se afirma de su salida y de su puerta. |

**Business Process (BPM)**:

```
Excluir degradados e inválidos → Buscar conflicto → Resolver por instante más reciente → Conservar puerta vigente → Asignar estado por segmento
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.6 SF-01.5 Detección de anomalía y bloqueo previo

**Spec fuente**: [SF-01.5 Detección de anomalía y bloqueo previo](06-sf-01-5-deteccion-de-anomalia-y-bloqueo-previo.md)  
**Requisitos**: FR-004, FR-005, FR-006, FR-019, FR-038, FR-068  
**Pruebas (TC)**: TC-13, TC-23, TC-51, TC-52, TC-54

Decide si hay un evento relevante validado o evidencia anómala y, según eso, si el viaje solo se muestra, si es informativo, si se bloquea antes de consultar política o si sigue la cadena.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | solo hay eventos de estado informado o ninguno | se detecta la anomalía | no hay anomalía: se muestra solo el contexto, sin botones |
| 2 | el único evento validado es un cambio de puerta | se detecta la anomalía | la decisión es INFORMATIVA con la puerta destacada y no se consulta la política |
| 3 | dos segmentos tienen retraso relevante | se detecta la anomalía | no se decide: se informa y se ofrece el caso humano por varios segmentos afectados; la decisión es BLOQUEADA y la política queda sin solicitar |
| 4 | tres reservas ABC123: una con solo E-1007 (puerta 24), otra con un evento CANCELLATION y otra con retrasos de 160 min en S1 y S2 | se detecta la anomalía | la primera es INFORMATIVA sin consultar política, la segunda y la tercera son BLOQUEADAS sin consultar política ni opciones y con el caso humano correspondiente |

**Acceptance Criteria**:

- [ ] El 100 % de los viajes sin evento relevante se muestra sin alertas ni botones.
- [ ] El 100 % de los viajes solo con cambio de puerta termina INFORMATIVO sin consultar política.
- [ ] El 100 % de las anomalías previas termina BLOQUEADO sin consultar política ni opciones.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Estado resuelto del segmento | segment_id, state, affected, delay_minutes, gate, gate_recorded_at, information_as_of, discarded_events | Resultado de validar los eventos de un segmento: qué se afirma de su salida y de su puerta. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |

**Business Process (BPM)**:

```
Revisar eventos validados → Clasificar relevancia → Aplicar bloqueo previo → Elegir camino
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.7 SF-01.6 Lectura de política

**Spec fuente**: [SF-01.6 Lectura de política](07-sf-01-6-lectura-de-politica.md)  
**Requisitos**: FR-008, FR-009, FR-068, FR-086, FR-105, NFR-004  
**Pruebas (TC)**: TC-33, TC-35, TC-52, TC-53

Consulta la política de retrasos solo cuando hay un retraso relevante validado y ningún bloqueo previo; el cambio de puerta nunca la consulta.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | hay un retraso relevante validado y ningún bloqueo previo | se llega a la lectura de política | se consulta la política de retrasos y se evalúan todas sus reglas |
| 2 | la configuración incluyera otros escenarios y el único evento es un cambio de puerta | se evalúa el viaje | no se consulta ninguna política |
| 3 | la consulta falla por tiempo agotado y la re-consulta también | se evalúa el viaje | la decisión es BLOQUEADA con anomalía que exige validación manual: no se consultan opciones y el soporte se ofrece con el motivo de datos parciales bloqueantes |
| 4 | un retraso de 160 min validado en ABC123 | la política de retrasos llega con 0 reglas, o falla dos veces | ambos casos terminan BLOQUEADOS; con la política vacía el soporte se ofrece, con el fallo se registra la revisión manual; con solo E-1007 la política no se consulta aunque la configuración la incluya |

**Acceptance Criteria**:

- [ ] La política se consulta en el 100 % de los retrasos relevantes validados sin bloqueo previo y en el 0 % de los demás casos.
- [ ] Ninguna lectura de política ocurre en paralelo con otra: la cadena es secuencial.
- [ ] El 100 % de los fallos de lectura de política termina BLOQUEADO con soporte ofrecido.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Política y regla | scenario, status, version, effective_from, superseded_versions, entitlements, requires_human_approval, rules | Versión recuperada de la política de retrasos y el resultado de evaluar cada una de sus reglas. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |

**Business Process (BPM)**:

```
Confirmar condición de consulta → Consultar política de retrasos → Re-consultar si falló → Entregar política o bloqueo
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.8 SF-01.7 Derivación de variables

**Spec fuente**: [SF-01.7 Derivación de variables](08-sf-01-7-derivacion-de-variables.md)  
**Requisitos**: FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-029, FR-086, DOC-009  
**Pruebas (TC)**: TC-06, TC-18, TC-23, TC-28, TC-47

Calcula las variables que alimentan las reglas: retraso, nueva llegada, conexión perdida, carácter internacional, grupo con menor y compensación solicitada, cada una con su origen y supuestos.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | retraso de 60 minutos, margen de 10 minutos y tiempo mínimo de conexión no provisto | se derivan las variables | la conexión perdida queda desconocida, se rotula «estimada» y se ofrece el caso humano |
| 2 | retraso de 10 minutos, margen de 60 minutos y tiempo mínimo no provisto | se derivan las variables | la conexión perdida es falsa, rotulada «estimada, sujeta al tiempo mínimo de conexión»; nunca se dice «tu conexión está segura» |
| 3 | una llegada programada a las 23:40 con 160 minutos de retraso | se calcula la nueva llegada | resulta en la fecha siguiente, con fecha completa y etiquetada como derivada y estimada |
| 4 | un pasajero no trae tipo | se deriva el grupo con menor | el valor es desconocido y se trata como posible menor |
| 5 | LA500 llega a las 17:55 y LA2410 sale a las 19:05 (margen 70 min sin retraso) | se deriva con retrasos de 60 min y de 10 min | con 60 min el margen es 10 min y la conexión es desconocida; con 10 min el margen es 60 min y es falsa «estimada, sujeta al tiempo mínimo de conexión» |
| 6 | S1 llega a las 23:30 con 120 min de retraso y un pasajero P2 sin campo de tipo | se deriva la nueva llegada y el grupo | la nueva llegada es 01:30 del día siguiente (derivada, estimada) y el grupo con menor es desconocido, tratado como posible menor |
| 7 | un retraso de 200 min solo en S2 (LA2410), último segmento de ABC123 | se deriva la conexión | no hay segmento siguiente: la conexión perdida es falsa (FR-022) y R1 (desde 180 min) queda como único derecho de cambio |
| 8 | el caso base ABC123: LA500 llega a las 17:55, LA2410 sale a las 19:05 y el retraso es de 160 min, con tiempo mínimo de conexión 0 no provisto | se derivan las variables | la nueva llegada es 17:55 + 160 min = 20:35 (estimada); el margen es 19:05 − 20:35 = −90 min, menor que 0, por lo que la conexión perdida es verdadera aun con tiempo mínimo 0 (fuera del rango incierto de 0 a 45 min); R3 se cumple, el grupo incluye un menor y R5 se cumple, la política está rota y la decisión es PENDIENTE_APROBACION |

**Acceptance Criteria**:

- [ ] El 100 % de las variables derivadas se registra con valor, origen y supuestos.
- [ ] Con tiempo mínimo no provisto, el 0 % de los resultados «falso» en el rango incierto se afirma como cierto.
- [ ] El 100 % de los retrasos que cruzan medianoche produce la fecha de llegada correcta.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Variable derivada | name, segment_id, value, known, origin, estimated, assumptions | Valor calculado a partir de los datos, con su origen y sus supuestos. |
| Contexto del viaje | booking_id, passenger_count, passengers, segments, fare_conditions, retrieved_at, completeness, missing_fields | Reserva del pasajero con sus tramos; se reduce de inmediato a lo mínimo necesario (sin correo, teléfono, documento, nombre completo ni edad). |
| Estado resuelto del segmento | segment_id, state, affected, delay_minutes, gate, gate_recorded_at, information_as_of, discarded_events | Resultado de validar los eventos de un segmento: qué se afirma de su salida y de su puerta. |

**Business Process (BPM)**:

```
Obtener retraso del segmento afectado → Calcular nueva llegada → Estimar conexión perdida → Derivar grupo y compensación → Registrar origen y supuestos
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.9 SF-01.8 Evaluación de reglas y estado de la decisión

**Spec fuente**: [SF-01.8 Evaluación de reglas y estado de la decisión](09-sf-01-8-evaluacion-de-reglas-y-estado-de-la-decision.md)  
**Requisitos**: FR-030, FR-031, FR-032, FR-033, FR-034, FR-035, FR-036, FR-037, FR-038, FR-039, FR-008, FR-024, NFR-003, NFR-012  
**Pruebas (TC)**: TC-04, TC-05, TC-07, TC-23, TC-35, TC-41, TC-45, TC-47, TC-49, TC-53

Evalúa todas las reglas de la política con un analizador acotado y lógica de tres valores, determina si la política está rota y fija el estado de la decisión.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el caso base con el niño: se cumplen la regla de conexión y la de menores | se evalúan las reglas | hay política rota, y como una regla cumplida exige aprobación la decisión es PENDIENTE_APROBACION |
| 2 | un retraso que solo activa una regla de trato prioritario | se evalúan las reglas | la decisión es INFORMATIVA: se informa y se muestran las reglas, sin opciones ni soporte |
| 3 | un pasajero sin tipo y una política que rompe, sin regla de menores | se evalúan las reglas | la decisión es BLOQUEADA para validación manual aunque la política no traiga esa regla |
| 4 | una condición usa un identificador fuera de la lista blanca | se evalúan las reglas | toda la evaluación queda indeterminada: decisión BLOQUEADA y caso humano por datos parciales bloqueantes |
| 5 | retrasos de 179, 180, 239 y 240 min en un vuelo internacional | se evalúan R1 y R2 | R1 se cumple desde 180 min y R2 desde 240 min; con 179 y 239 min no se cumplen |
| 6 | dos pasajeros adultos con 160 min (R5 falsa), una política con EQ/NE y una condición de 201 caracteres, y un retraso de 5 min | se evalúa la política | con dos adultos la decisión es AUTOMATICA; la condición de 201 caracteres es error de regla; con 5 min solo se cumple R5 (trato prioritario) y la decisión es INFORMATIVA |

**Acceptance Criteria**:

- [ ] El 100 % de las condiciones del enunciado (incluidos los bordes de 179/180 y 239/240 minutos) se evalúa con el resultado esperado.
- [ ] Ninguna condición ejecuta código dinámico: las entradas fuera de la lista blanca terminan en error de regla en el 100 % de los casos.
- [ ] El 100 % de las decisiones registra la versión de política y los identificadores de regla evaluados.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Política y regla | scenario, status, version, effective_from, superseded_versions, entitlements, requires_human_approval, rules | Versión recuperada de la política de retrasos y el resultado de evaluar cada una de sus reglas. |
| Variable derivada | name, segment_id, value, known, origin, estimated, assumptions | Valor calculado a partir de los datos, con su origen y sus supuestos. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |

**Business Process (BPM)**:

```
Analizar condición → Evaluar con tres valores → Resumir resultado por regla → Determinar política rota → Fijar estado de la decisión
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.10 SF-01.9 Lectura y filtrado de opciones

**Spec fuente**: [SF-01.9 Lectura y filtrado de opciones](10-sf-01-9-lectura-y-filtrado-de-opciones.md)  
**Requisitos**: FR-009, FR-017, FR-029, FR-039, FR-040, FR-041, FR-042, FR-043, FR-044, FR-045, FR-046, FR-047, FR-048, FR-049, FR-071, FR-102, NFR-002  
**Pruebas (TC)**: TC-01, TC-06, TC-09, TC-10, TC-11, TC-12, TC-27, TC-28, TC-29, TC-37, TC-45, TC-60

Solo con política rota consulta las opciones elegibles con un contexto reducido sin información personal, filtra las viables, registra las descartadas con todas sus razones y elige la propuesta.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una opción de cambio sin costo con asientos para el grupo, referencia de política vigente y salida posterior a la nueva llegada | se filtran las opciones | queda como viable y propuesta, con hora límite según su vigencia |
| 2 | una opción con un solo asiento para dos pasajeros y diferencia de tarifa, y una opción de reembolso sin respaldo recuperado | se filtran las opciones | ninguna se muestra; la de un asiento se registra con asientos insuficientes y conflicto de costo, y la de reembolso con su razón |
| 3 | ninguna opción cubre al grupo | se filtran las opciones | se muestra un mensaje claro y se ofrece el caso humano por ninguna opción cubre al grupo |
| 4 | la conexión perdida es desconocida y el proveedor entrega opciones con cupos y política vigente | se filtran las opciones | ninguna opción es viable, todas se registran como itinerario incoherente, la decisión es BLOQUEADA y se ofrece soporte |
| 5 | la salida de la opción propuesta cae en la fecha siguiente a la nueva llegada | se arma la propuesta | se activa el aviso «podrías tener derecho a asistencia; un agente lo confirmará», sin cifras |
| 6 | O1 LA2412 con 4 asientos, O2 LA2450 con 1 asiento y 180.000 CLP, O3 reembolso con POL-REFUND-2026-01, y 2 pasajeros | se filtran las opciones con la política POL-DELAY-2026-03 | solo O1 es viable y se propone; O2 se descarta por asientos insuficientes y conflicto de costo, y O3 por referencia de política no verificada; con dos adultos y solo O2 no hay opción viable |
| 7 | opciones leídas a las 11:02:35Z: una con diferencia de 180.000 CLP sin moneda, otra con destino distinto, el contexto sin monto de penalidad de cambio y O1 que sale el 16 sep a las 08:15 | se evalúan las opciones | la opción sin moneda y la de destino distinto no son viables; no se cotizan cambios voluntarios; O1 activa el aviso de pernocte |
| 8 | las opciones de ABC123 traen la referencia POL-DELAY-2025-11, que figura entre las versiones superadas de POL-DELAY-2026-03 | se filtran las opciones | ninguna opción queda respaldada: todas se descartan por referencia de política superada y la decisión ofrece soporte |
| 9 | O1 LA2412 leída a las 11:02:35Z, primero sin `ttl_seconds` y luego con vigencia de 120 s | se evalúa sin vigencia, a 119 s y a 120 s de la lectura | sin vigencia el conjunto está vencido; a 119 s está vigente y a 120 s vencida |
| 10 | un retraso de 200 min solo en S2 (LA2410, el último segmento) donde R1 (desde 180 min) concede REBOOK_NO_FEE | se evalúa y se filtran las opciones | no hay conexión siguiente y la política está rota por R1; las opciones reemplazan al segmento afectado: mismo origen LIM y destino MEX que LA2410 y salida posterior a la lectura de 11:02:35Z (rama «sin conexión perdida» de FR-041 f) |

**Acceptance Criteria**:

- [ ] El 100 % de las opciones no viables se omite de la pantalla y se registra con todas sus razones de descarte.
- [ ] La consulta de opciones no contiene ningún campo de la lista prohibida en el 100 % de los casos.
- [ ] En decisión INFORMATIVA se realizan 0 consultas de opciones.
- [ ] La propuesta principal es siempre la viable de mayor confianza, con desempate por salida y luego por identificador.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, date, departure, fare_difference, currency, seats_available, policy_ref, confidence, viable, discard_reasons, fingerprint, is_proposed, overnight, expires_at | Alternativa candidata entregada por el proveedor; solo las viables se muestran. |
| Contexto del viaje | booking_id, passenger_count, passengers, segments, fare_conditions, retrieved_at, completeness, missing_fields | Reserva del pasajero con sus tramos; se reduce de inmediato a lo mínimo necesario (sin correo, teléfono, documento, nombre completo ni edad). |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |

**Business Process (BPM)**:

```
Consultar opciones con contexto reducido → Evaluar viabilidad → Registrar descartadas → Elegir propuesta → Calcular hora límite y pernocte
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.11 SF-01.10 Motivos, soporte y acciones ofrecidas

**Spec fuente**: [SF-01.10 Motivos, soporte y acciones ofrecidas](11-sf-01-10-motivos-soporte-y-acciones-ofrecidas.md)  
**Requisitos**: FR-004, FR-014, FR-047, FR-050, FR-057, FR-058, FR-060, FR-062, FR-063, FR-067  
**Pruebas (TC)**: TC-01, TC-09, TC-17, TC-19, TC-45, TC-46

Reúne los motivos de caso humano aplicables, los prioriza, decide si el soporte se ofrece y calcula la elegibilidad de compensación para el menú.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la decisión es PENDIENTE_APROBACION por el menor | se definen las acciones | se ofrecen aceptar la opción (que abrirá un caso humano) y «Hablar con una persona» con los motivos de otra ayuda y datos personales |
| 2 | la decisión es INFORMATIVA, o la lectura de contexto o eventos falló, o solo hay evidencia degradada | se definen las acciones | no se ofrece soporte ni acciones |
| 3 | una regla de compensación se cumple al fijar la solicitud como verdadera y la decisión no es INFORMATIVA | se arma el menú de motivos | se incluye el motivo «Tengo una consulta sobre compensaciones»; si no, el menú no lo ofrece |
| 4 | ya existe una operación de cambio en curso para la reserva | se definen las acciones | la acción de aceptar se muestra deshabilitada con su explicación |
| 5 | el caso base con R4 que concede CASH_COMPENSATION, y otra reserva con OPS_CORE degradada en S1 | se arma el menú de soporte | el caso base ofrece los 3 motivos incluida la compensación y la reserva con OPS_CORE degradada no ofrece soporte |

**Acceptance Criteria**:

- [ ] El soporte se ofrece en el 0 % de las vistas sin acción posible y en el 100 % de las BLOQUEADAS por anomalía que exige validación manual.
- [ ] El motivo de compensación aparece en el 0 % de los menús sin compensación elegible.
- [ ] El motivo principal del caso es el de mayor prioridad en el 100 % de las combinaciones.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, load_status, data_as_of, segments, alerts, derived_variables, policy, options, proposed_option_id, refund_notice, offer_deadline, actions, messages, operations, human_cases | Respuesta completa para el pasajero; solo contiene campos de la lista blanca. |

**Business Process (BPM)**:

```
Reunir motivos → Ordenar por prioridad → Decidir si hay acción posible → Calcular elegibilidad de compensación → Definir acciones y su efecto
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.12 SF-01.11 Construcción y validación de mensajes

**Spec fuente**: [SF-01.11 Construcción y validación de mensajes](12-sf-01-11-construccion-y-validacion-de-mensajes.md)  
**Requisitos**: FR-039, FR-046, FR-058, FR-071, FR-080, FR-081, FR-082, FR-083, FR-084, NFR-001  
**Pruebas (TC)**: TC-01, TC-11, TC-16, TC-45

Arma los mensajes con plantillas determinísticas y evidencia por afirmación, y los somete al validador antes de devolverlos.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | un mensaje que afirma la opción propuesta con su referencia de política y su evidencia | pasa por el validador | se devuelve al pasajero |
| 2 | un mensaje afirma «tu conexión está segura» o menciona hotel, comidas o montos | pasa por el validador | se bloquea, se reemplaza por un texto neutro y se cuenta como mensaje bloqueado |
| 3 | la decisión es INFORMATIVA | se arman los mensajes | el texto dice que con la información actual no hay acciones disponibles y que vuelva a consultar más tarde |
| 4 | el mensaje de la opción O1 con POL-DELAY-2026-03 y otro que dice «tu conexión está segura» | pasan por el validador | el primero se libera y el segundo se bloquea y se cuenta como mensaje bloqueado |

**Acceptance Criteria**:

- [ ] El 100 % de los mensajes mostrados pasa por el validador y cumple las prohibiciones de contenido.
- [ ] El número de afirmaciones sin evidencia emitidas es 0 por construcción.
- [ ] Los mensajes bloqueados quedan contados para la métrica de éxito.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, load_status, data_as_of, segments, alerts, derived_variables, policy, options, proposed_option_id, refund_notice, offer_deadline, actions, messages, operations, human_cases | Respuesta completa para el pasajero; solo contiene campos de la lista blanca. |

**Business Process (BPM)**:

```
Elegir plantilla → Adjuntar evidencia → Validar mensaje → Bloquear o liberar → Contar bloqueados
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.13 SF-01.12 Barrido perezoso del ciclo de vida

**Spec fuente**: [SF-01.12 Barrido perezoso del ciclo de vida](13-sf-01-12-barrido-perezoso-del-ciclo-de-vida.md)  
**Requisitos**: FR-064  
**Pruebas (TC)**: TC-38, TC-57

Antes de mostrar operaciones y casos, actualiza los estados que cambiaron con el paso del tiempo para que la vista muestre lo vigente.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una operación está en curso y superó `OPERATION_STALE_SECONDS` (120) sin respuesta | se arma la vista | se muestra como indeterminada |
| 2 | una operación indeterminada superó `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900) sin resolverse | se arma la vista | se muestra como expirada y deja de bloquear una operación nueva |
| 3 | una solicitud creada llegó a su vencimiento | se arma la vista | se muestra como expirada y permite una nueva operación con la generación siguiente |
| 4 | una operación de ABC123 en curso hace 121 s, otra creada con vencimiento 11:12:00Z y una indeterminada de 900 s | se lee el registro a las 11:12:01Z | pasan a indeterminada, expirada y expirada respectivamente |

**Acceptance Criteria**:

- [ ] El 100 % de las operaciones en curso sin respuesta pasa a indeterminada al superar el tiempo configurado.
- [ ] El 100 % de las solicitudes creadas pasa a expirada en su vencimiento y el 100 % de las indeterminadas, tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS`.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Detectar estados vencidos → Aplicar transición → Entregar estados al día
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.14 SF-01.13 Huella por opción y registro de decisión

**Spec fuente**: [SF-01.13 Huella por opción y registro de decisión](14-sf-01-13-huella-por-opcion-y-registro-de-decision.md)  
**Requisitos**: FR-070, FR-090, FR-091, FR-093, NFR-001, NFR-002, NFR-013  
**Pruebas (TC)**: TC-31, TC-34, TC-58, TC-59

Calcula la huella de decisión y la huella de cada opción viable, y registra la evaluación completa sin información personal.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | dos evaluaciones con las mismas lecturas y distinto reloj de lectura | se calcula la huella | ambas huellas son iguales porque marcas de tiempo, identificadores de opción y confianza no cuentan |
| 2 | se agotan los asientos de la opción elegida o se sustituye su itinerario | se calcula la huella | la huella cambia |
| 3 | una evaluación completada | se registra la decisión | el registro contiene solo identificadores seudónimos, enumeraciones, números, marcas de tiempo y huellas; nunca nombre, contacto, documento ni edad |
| 4 | O1 LA2412 con 4 asientos y un segundo cálculo con 0 asientos, y otro con la política POL-DELAY-2026-04 | se calculan las huellas | con otro reloj la huella no cambia; con 0 asientos o la política nueva la huella cambia |

**Acceptance Criteria**:

- [ ] Con las mismas lecturas la huella es idéntica en el 100 % de las repeticiones.
- [ ] Cualquier cambio en estado, reglas, derechos, grupo, itinerario, asientos, tarifa o referencia de política cambia la huella.
- [ ] Un recorrido de los registros no encuentra ningún dato de la lista prohibida.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, date, departure, fare_difference, currency, seats_available, policy_ref, confidence, viable, discard_reasons, fingerprint, is_proposed, overnight, expires_at | Alternativa candidata entregada por el proveedor; solo las viables se muestran. |

**Business Process (BPM)**:

```
Normalizar datos de la decisión → Calcular huella de decisión → Calcular huella por opción → Registrar sin información personal
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.15 SF-01.14 Ensamblado de la respuesta

**Spec fuente**: [SF-01.14 Ensamblado de la respuesta](15-sf-01-14-ensamblado-de-la-respuesta.md)  
**Requisitos**: FR-003, FR-110, FR-112, NFR-002  
**Pruebas (TC)**: TC-01, TC-51

Compone la vista del viaje con la lista blanca de campos: contexto, puerta con su hora, saludo con nombre de pila, código de reserva, aviso de menor sin edad, operaciones activas y casos existentes.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la reserva tiene un primer pasajero adulto | se arma la vista | se muestra solo su nombre de pila, el código de reserva y el número de pasajeros |
| 2 | la reserva no tiene un pasajero adulto | se arma la vista | se omite el saludo |
| 3 | la reserva tiene una solicitud creada para una opción que ya no se muestra | se arma la vista | la solicitud sigue apareciendo entre las operaciones activas, independiente de las opciones mostradas |
| 4 | el caso base ABC123 con Ana (adulta) y un niño, y el cambio de puerta 24 informado a las 10:55 UTC | se arma la vista | muestra «Hola, Ana», la reserva ABC123, 2 pasajeros y la puerta 24 con su hora, sin edad del menor |

**Acceptance Criteria**:

- [ ] La vista contiene el 100 % de los campos de la lista blanca aplicables y el 0 % de los campos de la lista prohibida.
- [ ] Las operaciones activas de la reserva aparecen en el 100 % de las vistas, aunque su opción ya no se muestre.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, load_status, data_as_of, segments, alerts, derived_variables, policy, options, proposed_option_id, refund_notice, offer_deadline, actions, messages, operations, human_cases | Respuesta completa para el pasajero; solo contiene campos de la lista blanca. |
| Contexto del viaje | booking_id, passenger_count, passengers, segments, fare_conditions, retrieved_at, completeness, missing_fields | Reserva del pasajero con sus tramos; se reduce de inmediato a lo mínimo necesario (sin correo, teléfono, documento, nombre completo ni edad). |

**Business Process (BPM)**:

```
Seleccionar campos de la lista blanca → Incorporar puerta y su hora → Adjuntar operaciones y casos → Entregar la vista
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.16 F-02 Aceptar opción

**Spec fuente**: [F-02 Aceptar opción](16-f-02-aceptar-opcion.md)  
**Requisitos**: FR-001, FR-017, FR-038, FR-050, FR-051, FR-052, FR-053, FR-054, FR-055, FR-056, FR-059, FR-062, FR-063, FR-064, FR-065, FR-070, FR-072, FR-081, FR-090, FR-105, NFR-004, DOC-012, DOC-013  
**Pruebas (TC)**: TC-01, TC-07, TC-08, TC-14, TC-15, TC-22, TC-27, TC-30, TC-31, TC-33, TC-34, TC-38, TC-40, TC-57

Un clic del pasajero autoriza exactamente una acción: crear la solicitud de cambio si la decisión es automática, o abrir un caso humano con la opción elegida si exige aprobación o está bloqueada.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la decisión es AUTOMATICA, la huella de la opción coincide y la opción está vigente | el pasajero acepta la opción | se crea una única solicitud de cambio con la llave de idempotencia y la vista dice «solicitud registrada, pendiente de confirmación, sujeta a disponibilidad» con su vencimiento, sin afirmar que el vuelo ya cambió |
| 2 | la decisión es PENDIENTE_APROBACION o BLOQUEADA | el pasajero acepta la opción | no se crea la solicitud de cambio: se abre un caso humano con la opción elegida como evidencia, sin revalidar |
| 3 | entre lo que vio el pasajero y el clic se agotaron los asientos de la opción | el pasajero acepta la opción | no se escribe nada y se muestra la vista nueva con el aviso de que la situación cambió |
| 4 | el pasajero pulsa dos veces o desde dos pestañas | se procesan ambas aceptaciones | se escribe una sola solicitud y la segunda recibe el estado de la primera |
| 5 | dos pasajeros adultos, decisión AUTOMATICA, O1 LA2412 con 4 asientos, huella igual y opción vigente | se acepta O1 a las 11:03:00Z | se crea una solicitud (RBK-88231, vence 11:12:00Z) y el mensaje dice «pendiente de confirmación, sujeta a disponibilidad» |

**Acceptance Criteria**:

- [ ] En 100 solicitudes simultáneas sobre la misma opción se escribe exactamente una.
- [ ] El 100 % de los clics que producen una escritura externa lo declaró antes en el texto del botón.
- [ ] Una huella distinta o una opción vencida no resuelta produce 0 escrituras.
- [ ] El peor caso de aceptar con los valores por defecto no excede 40,6 s y el botón permanece deshabilitado todo ese tiempo.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, date, departure, fare_difference, currency, seats_available, policy_ref, confidence, viable, discard_reasons, fingerprint, is_proposed, overnight, expires_at | Alternativa candidata entregada por el proveedor; solo las viables se muestran. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |

**Business Process (BPM)**:

```
Autorizar y validar → Elegir camino por estado → Revalidar → Verificar vigencia → Reservar llave → Crear solicitud → Responder con mensaje validado
```

Subprocess detail (if applicable):

```
SF-02.1: Autorización y validación
SF-02.2: Bifurcación por estado de la decisión
SF-02.3: Revalidación
SF-02.4: Vigencia de la opción
SF-02.5: Llave idempotente y registro de operaciones
SF-02.6: Llamada a la solicitud de cambio
SF-02.7: Reintentos del resultado indeterminado
SF-02.8: Derivación tras falla persistente
SF-02.9: Caso humano con la opción elegida
SF-02.10: Mensaje de resultado y registro
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.17 SF-02.1 Autorización y validación

**Spec fuente**: [SF-02.1 Autorización y validación](17-sf-02-1-autorizacion-y-validacion.md)  
**Requisitos**: FR-001, FR-065, NFR-003, NFR-013  
**Pruebas (TC)**: TC-21, TC-40, TC-58

Comprueba que la sesión pertenece a la reserva, que la decisión es de esa sesión, que la opción fue ofrecida y que la huella e itinerario enviados corresponden a la instantánea guardada.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la sesión coincide, la decisión es suya y la opción, la clave de itinerario y la huella corresponden | se valida la aceptación | se continúa con el flujo |
| 2 | la decisión pertenece a otra reserva | se valida la aceptación | la respuesta es la misma de «no encontrado» que para una decisión inexistente |
| 3 | la opción indicada no figura en la decisión o su huella no coincide con la guardada | se valida la aceptación | se rechaza por opción no ofrecida o por validación, sin escribir nada |
| 4 | la sesión de ABC123 y una decisión de XYZ789 | se acepta O1 con esa decisión, o con una huella distinta a la guardada | la primera responde «no encontrado» idéntico y la segunda se rechaza sin escribir; el servidor ignora cualquier contenido de la opción |
| 5 | ABC123 con `EVALUATE_RATE_LIMIT_PER_MINUTE` de 30 y 30 aceptaciones de O1 en el último minuto desde el mismo origen | llega la 31.ª aceptación | se rechaza por límite de tasa sin escribir nada |

**Acceptance Criteria**:

- [ ] El 100 % de las peticiones con decisión ajena recibe la misma respuesta que con decisión inexistente.
- [ ] El 100 % de las peticiones con contenido de opción distinto del guardado se rechaza sin escritura.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | Identidad con la que se pide una evaluación: sesión del pasajero o credencial de servicio. |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |

**Business Process (BPM)**:

```
Comprobar sesión → Comprobar decisión de la sesión → Comprobar opción, clave y huella
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.18 SF-02.2 Bifurcación por estado de la decisión

**Spec fuente**: [SF-02.2 Bifurcación por estado de la decisión](18-sf-02-2-bifurcacion-por-estado-de-la-decision.md)  
**Requisitos**: FR-038, FR-052, DOC-012  
**Pruebas (TC)**: TC-01, TC-07

Decide, según el estado guardado de la decisión, si el clic crea una solicitud de cambio o abre un caso humano con la opción.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | decisión AUTOMATICA | el pasajero acepta | sigue la revalidación para crear la solicitud de cambio |
| 2 | decisión PENDIENTE_APROBACION o BLOQUEADA | el pasajero acepta | se abre un caso humano con la opción sin revalidar y sin llamar a la solicitud de cambio |
| 3 | el caso base PENDIENTE_APROBACION con O1 y el escenario sin menor AUTOMATICA | se acepta O1 en cada uno | el primero abre un caso humano con O1 sin llamar a la solicitud de cambio; el segundo sigue a la revalidación |

**Acceptance Criteria**:

- [ ] El 100 % de las decisiones PENDIENTE_APROBACION o BLOQUEADA termina sin solicitud de cambio.
- [ ] El 100 % de las decisiones AUTOMATICA llega a la revalidación.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |

**Business Process (BPM)**:

```
Leer estado de la decisión → Elegir camino
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.19 SF-02.3 Revalidación

**Spec fuente**: [SF-02.3 Revalidación](19-sf-02-3-revalidacion.md)  
**Requisitos**: FR-070, FR-072, NFR-001  
**Pruebas (TC)**: TC-08, TC-31

Antes de crear el cambio reconsulta contexto, eventos, política y opciones, recalcula la decisión y compara la huella de la opción elegida con la mostrada.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | solo cambiaron marcas de tiempo e identificadores de opción | se revalida | la huella coincide y el flujo continúa |
| 2 | se agotaron los cupos de la opción o se sustituyó su itinerario | se revalida | no se escribe nada y se devuelve la vista nueva con el aviso de que la situación cambió |
| 3 | el clic abre un caso humano | se procesa | no se revalida: el caso lleva la instantánea que el pasajero vio |
| 4 | O1 LA2412 tenía 4 asientos al mostrarse y la relectura trae 0 | se revalida | la huella cambia, no se escribe y se muestra la vista nueva con «la situación cambió» |

**Acceptance Criteria**:

- [ ] El 100 % de las huellas distintas termina sin escritura.
- [ ] Cambiar solo marcas de tiempo, identificadores de opción o confianza no provoca ningún aviso de cambio.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, date, departure, fare_difference, currency, seats_available, policy_ref, confidence, viable, discard_reasons, fingerprint, is_proposed, overnight, expires_at | Alternativa candidata entregada por el proveedor; solo las viables se muestran. |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |

**Business Process (BPM)**:

```
Reconsultar contexto, eventos, política y opciones → Recalcular decisión y huella de la opción → Comparar con la mostrada
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.20 SF-02.4 Vigencia de la opción

**Spec fuente**: [SF-02.4 Vigencia de la opción](20-sf-02-4-vigencia-de-la-opcion.md)  
**Requisitos**: FR-017, FR-041, FR-072  
**Pruebas (TC)**: TC-08, TC-27

Comprueba que la opción re-consultada está vigente en el instante de escribir y, si venció, la refresca una sola vez recalculando viabilidad y huella.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la opción tiene 119 segundos de edad | se verifica la vigencia | está vigente y se escribe |
| 2 | la opción tiene 120 segundos de edad (instante exacto) y la re-consulta devuelve una opción viable | se verifica la vigencia | se refresca una sola vez, se recalculan viabilidad y huella sobre la nueva respuesta y, si coinciden, se escribe |
| 3 | tras el refresco la opción sigue vencida o ya no es viable | se verifica la vigencia | no se escribe y se muestra el estado nuevo |
| 4 | opciones leídas a las 11:02:35Z con vigencia de 120 s | se acepta a las 11:04:34Z y a las 11:04:35Z | a las 11:04:34Z está vigente; a las 11:04:35Z se refresca una sola vez y, si sigue vencida, estado cambiado |

**Acceptance Criteria**:

- [ ] La opción de 119 s se usa en el 100 % de los casos y la de 120 s siempre se refresca.
- [ ] Se realiza como máximo un refresco por acción.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, date, departure, fare_difference, currency, seats_available, policy_ref, confidence, viable, discard_reasons, fingerprint, is_proposed, overnight, expires_at | Alternativa candidata entregada por el proveedor; solo las viables se muestran. |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |

**Business Process (BPM)**:

```
Calcular vigencia → Refrescar una vez si venció → Recalcular viabilidad y huella → Confirmar o declarar estado cambiado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.21 SF-02.5 Llave idempotente y registro de operaciones

**Spec fuente**: [SF-02.5 Llave idempotente y registro de operaciones](21-sf-02-5-llave-idempotente-y-registro-de-operaciones.md)  
**Requisitos**: FR-053, FR-062, FR-064  
**Pruebas (TC)**: TC-22, TC-34, TC-38, TC-57

Calcula la llave de idempotencia de la operación, la reserva de forma atómica antes de llamar y la reutiliza mientras la operación no haya fracasado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | no existe operación activa para la reserva e itinerario | se acepta la opción | se registra la operación en curso con su llave antes de llamar al proveedor |
| 2 | dos aceptaciones llegan a la vez | ambas intentan reservar la llave | solo una escribe; la otra recibe el estado de la primera |
| 3 | la operación anterior está expirada (incluida una indeterminada vencida) o fallida | se acepta de nuevo | se usa la llave de la generación siguiente |
| 4 | la llave no puede guardarse | se acepta la opción | no se escribe nada |
| 5 | O1 LA2412 de ABC123 con política POL-DELAY-2026-03 y otra versión POL-DELAY-2026-04 en la reevaluación | dos clics llegan a la vez | se registra una sola operación con una sola llave, reutilizada pese al cambio de versión de política |

**Acceptance Criteria**:

- [ ] En 100 intentos simultáneos sobre el mismo itinerario se registra exactamente una operación.
- [ ] La llave no incluye el identificador de decisión ni marcas de tiempo y no es adivinable sin el secreto del servicio.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |

**Business Process (BPM)**:

```
Calcular llave → Reservar operación en curso → Reutilizar o crear generación siguiente
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.22 SF-02.6 Llamada a la solicitud de cambio

**Spec fuente**: [SF-02.6 Llamada a la solicitud de cambio](22-sf-02-6-llamada-a-la-solicitud-de-cambio.md)  
**Requisitos**: FR-054, FR-055, FR-056, FR-105, DOC-013  
**Pruebas (TC)**: TC-14, TC-15, TC-30, TC-40

Una llamada al proveedor de cambios con la opción resuelta por el servidor, la llave, la reserva y todos los pasajeros del grupo, y traducción del resultado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el proveedor responde con una solicitud pendiente de confirmación y vencimiento | se llama | la operación queda creada y el mensaje dice «pendiente de confirmación, sujeta a disponibilidad» |
| 2 | el proveedor indica que ya existe una solicitud | se llama | se trata como solicitud existente: «ya existe una solicitud en curso para esta opción», sin bucles |
| 3 | el proveedor rechaza por un error no definido | se llama | la operación queda fallida, no se reintenta, se muestra un fallo genérico y se ofrece el caso humano |
| 4 | la llamada incluye ABC123 y los pasajeros P1 y P2 | el proveedor responde creada (RBK-88231, vence 11:12:00Z), duplicado, o rechazo por pasajeros no cubiertos | queda creada con su vencimiento, solicitud existente, o fallida sin reintento |

**Acceptance Criteria**:

- [ ] El 100 % de las solicitudes enviadas incluye la reserva y todos los pasajeros.
- [ ] Ninguna respuesta afirma que el vuelo ya cambió.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |

**Business Process (BPM)**:

```
Armar solicitud con todo el grupo → Llamar una vez → Traducir resultado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.23 SF-02.7 Reintentos del resultado indeterminado

**Spec fuente**: [SF-02.7 Reintentos del resultado indeterminado](23-sf-02-7-reintentos-del-resultado-indeterminado.md)  
**Requisitos**: FR-054, NFR-012  
**Pruebas (TC)**: TC-14, TC-33, TC-49

Reintenta hasta `REBOOK_MAX_RETRIES` (2) veces con la misma llave y espera creciente; nunca informa éxito ni fracaso mientras sea indeterminado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el proveedor falla temporalmente una vez y luego responde creada | se reintenta con la misma llave | la operación queda creada y los reintentos realizados es 1 |
| 2 | el proveedor falla en la llamada inicial y en los dos reintentos | se agotan los reintentos | la operación queda indeterminada y se pasa a la derivación a caso humano |
| 3 | el proveedor falla con indisponibilidad en la 1.ª llamada y en los 2 reintentos de 200 ms y 400 ms | se agotan los reintentos | la operación queda indeterminada tras 3 llamadas con la misma llave |

**Acceptance Criteria**:

- [ ] Los reintentos usan la misma llave en el 100 % de los casos.
- [ ] El número de reintentos nunca supera `REBOOK_MAX_RETRIES`.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |

**Business Process (BPM)**:

```
Esperar y reintentar → Mantener la misma llave → Evaluar resultado final
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.24 SF-02.8 Derivación tras falla persistente

**Spec fuente**: [SF-02.8 Derivación tras falla persistente](24-sf-02-8-derivacion-tras-falla-persistente.md)  
**Requisitos**: FR-050, FR-054, FR-063  
**Pruebas (TC)**: TC-14

Si el resultado sigue indeterminado, abre un caso humano con el motivo de falla indeterminada del proveedor, cubierto por el clic del pasajero.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | los reintentos se agotaron | se deriva | se crea un caso humano con motivo de falla indeterminada del proveedor y la operación queda indeterminada |
| 2 | el botón declaró que, si no podía confirmarse, el caso se derivaría a una persona | se deriva | no se pide un segundo clic para esta derivación |
| 3 | la operación de O1 quedó indeterminada tras 3 llamadas | se deriva | se crea un caso humano con el motivo falla indeterminada (HC-4471, 45 minutos) y la operación sigue indeterminada |

**Acceptance Criteria**:

- [ ] El 100 % de las fallas persistentes produce un caso humano o un aviso explícito de que no pudo registrarse.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |

**Business Process (BPM)**:

```
Detectar falla persistente → Reservar intento de caso → Crear caso humano → Responder
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.25 SF-02.9 Caso humano con la opción elegida

**Spec fuente**: [SF-02.9 Caso humano con la opción elegida](25-sf-02-9-caso-humano-con-la-opcion-elegida.md)  
**Requisitos**: FR-052, FR-059, FR-063, FR-105  
**Pruebas (TC)**: TC-01, TC-33

Crea el caso humano con la opción como evidencia, todos los motivos aplicables, reserva atómica y deduplicación local, usando la instantánea guardada.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | no hay caso previo para la misma clave | se acepta la opción | se crea el caso con la opción, todos los motivos y sin información personal |
| 2 | ya hay un caso creado con la misma clave o un intento en curso | se acepta de nuevo | se devuelve el caso existente sin enviar nada |
| 3 | el intento previo quedó indeterminado | se acepta sin confirmar el posible duplicado | se pide un segundo clic explícito, conservando la misma opción |
| 4 | el caso base con decisión PENDIENTE_APROBACION y los motivos aprobación de política y pernocte | se acepta O1 dos veces y el proveedor de casos responde HC-4471 | se crea un solo caso HC-4471 con O1 como evidencia y los dos motivos; el segundo clic devuelve el caso existente |

**Acceptance Criteria**:

- [ ] El 100 % de los casos creados por aceptar una opción lleva esa opción como evidencia.
- [ ] Cero casos duplicados por clics concurrentes.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |

**Business Process (BPM)**:

```
Reunir motivos → Deduplicar → Reservar intento → Crear caso con la opción → Responder
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.26 SF-02.10 Mensaje de resultado y registro

**Spec fuente**: [SF-02.10 Mensaje de resultado y registro](26-sf-02-10-mensaje-de-resultado-y-registro.md)  
**Requisitos**: FR-056, FR-081, FR-090, FR-105  
**Pruebas (TC)**: TC-16, TC-30

Construye el mensaje validado del resultado, actualiza los registros de operaciones y casos y responde con el resultado de aceptación.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la operación quedó creada | se arma el mensaje | dice «solicitud registrada, pendiente de confirmación, sujeta a disponibilidad» |
| 2 | la operación quedó fallida | se arma el mensaje | dice que no pudimos procesar la solicitud, sin detalle técnico, y ofrece el caso humano |
| 3 | la operación creada RBK-88231 con vencimiento 11:12:00Z | se arma el mensaje | dice «Solicitud registrada, pendiente de confirmación, sujeta a disponibilidad. Vence a las 11:12 UTC.» y no «ya está cambiado» |

**Acceptance Criteria**:

- [ ] Los siete resultados posibles usan una redacción aprobada por el validador en el 100 % de los casos.
- [ ] Ninguno afirma «ya está cambiado».

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |

**Business Process (BPM)**:

```
Elegir plantilla por resultado → Validar mensaje → Actualizar registros → Responder
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.27 F-03 Caso humano manual («Hablar con una persona»)

**Spec fuente**: [F-03 Caso humano manual («Hablar con una persona»)](27-f-03-caso-humano-manual-hablar-con-una-persona.md)  
**Requisitos**: FR-001, FR-025, FR-050, FR-057, FR-059, FR-060, FR-061, FR-063, FR-067, FR-081, FR-091, FR-105, NFR-002  
**Pruebas (TC)**: TC-17, TC-20, TC-33, TC-46

El pasajero pide hablar con una persona eligiendo un motivo de enumeración cerrada, sin texto libre, solo cuando existe una acción posible; el sistema reúne los motivos, aplica la prioridad, evita duplicados y registra cada intento.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | existe una acción posible y el pasajero elige «Necesito ayuda con mi vuelo» | envía la solicitud con la decisión que vio | se crea un caso con el motivo de mayor prioridad entre todos los aplicables y el mensaje informa el plazo de atención devuelto por el proveedor |
| 2 | ya existe un caso creado con la misma clave de deduplicación | el pasajero pide hablar con una persona otra vez | se devuelve el caso existente y no se envía nada nuevo |
| 3 | el proveedor de casos no responde | el pasajero pide hablar con una persona | se muestra «no pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté», no se reenvía solo y un segundo intento exige un segundo clic tras la advertencia del posible duplicado |
| 4 | la decisión es INFORMATIVA o no hay anomalía | el pasajero intenta pedir soporte | el sistema responde que no hay una acción de soporte disponible |
| 5 | el caso base con motivos aprobación de política y pernocte, y el pasajero elige «Necesito ayuda con mis datos o documentos» | envía la solicitud con la decisión que vio | se crea el caso HC-4471 (cola DISRUPTION_L2, 45 minutos) con el motivo de mayor prioridad y sin ningún dato personal |

**Acceptance Criteria**:

- [ ] El 100 % de los clics repetidos sobre el mismo caso creado devuelve el existente sin envío adicional.
- [ ] Cero respuestas de caso humano contienen un campo de la lista prohibida, incluso con el motivo de datos personales.
- [ ] Un timeout nunca provoca un reenvío automático.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de caso humano | outcome, message, human_case, decision_id | Respuesta a un clic de «Hablar con una persona». |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |

**Business Process (BPM)**:

```
Autorizar y validar motivo → Determinar evidencia → Resolver motivos → Deduplicar → Reservar intento → Crear caso → Mostrar resultado
```

Subprocess detail (if applicable):

```
SF-03.1: Autorización y validación del motivo
SF-03.2: Origen de la evidencia y disponibilidad
SF-03.3: Resolución de motivos
SF-03.4: Deduplicación
SF-03.5: Reserva atómica del intento
SF-03.6: Llamada al caso humano
SF-03.7: Reintento tras indeterminado
SF-03.8: Mensaje y registro
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.28 SF-03.1 Autorización y validación del motivo

**Spec fuente**: [SF-03.1 Autorización y validación del motivo](28-sf-03-1-autorizacion-y-validacion-del-motivo.md)  
**Requisitos**: FR-001, FR-060, NFR-013  
**Pruebas (TC)**: TC-17, TC-21, TC-58

Comprueba la sesión y que el motivo pertenezca a la enumeración cerrada, sin campos extra ni texto libre.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la sesión coincide con la reserva y el motivo es uno de los tres permitidos | se valida | la solicitud continúa |
| 2 | el cuerpo trae un motivo fuera de la lista o un campo de texto libre | se valida | se rechaza por validación sin repetir la entrada |
| 3 | el sistema ya conoce el motivo (conflicto, sin opción) | el pasajero pulsa el botón de un clic | se envía «otra ayuda» con la decisión y el sistema fija el motivo principal por prioridad |
| 4 | ABC123 con conflicto de fuentes | se envía el motivo «COMPENSATION_REQUESTED» sin compensación elegible, y luego «OTHER_HELP» con la decisión | el primero se rechaza y el segundo crea el caso con el motivo conflicto de fuentes |
| 5 | ABC123 con 30 solicitudes de caso humano en el último minuto desde el mismo origen | llega la 31.ª | se rechaza por límite de tasa sin enviar nada al proveedor de casos |

**Acceptance Criteria**:

- [ ] El 100 % de las peticiones con texto libre o motivo fuera de la lista se rechaza.
- [ ] La enumeración cerrada tiene exactamente tres motivos manuales.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de caso humano | outcome, message, human_case, decision_id | Respuesta a un clic de «Hablar con una persona». |
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | Identidad con la que se pide una evaluación: sesión del pasajero o credencial de servicio. |

**Business Process (BPM)**:

```
Comprobar sesión → Validar motivo y campos → Aceptar solicitud
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.29 SF-03.2 Origen de la evidencia y disponibilidad

**Spec fuente**: [SF-03.2 Origen de la evidencia y disponibilidad](29-sf-03-2-origen-de-la-evidencia-y-disponibilidad.md)  
**Requisitos**: FR-025, FR-059, FR-060, FR-067, FR-090  
**Pruebas (TC)**: TC-17, TC-45, TC-46

Decide de dónde sale la evidencia (decisión guardada o evaluación fresca) y si hay soporte disponible para ese motivo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la petición trae la decisión de la sesión | se arma la evidencia | se toma de la decisión guardada y de su proyección mínima, sin releer ni revalidar |
| 2 | la petición no trae decisión | se arma la evidencia | se ejecuta una evaluación fresca y se registra una decisión nueva |
| 3 | la decisión es INFORMATIVA, no hay anomalía, hay solo evidencia degradada o falló la lectura de contexto o eventos | se pide soporte | se responde que no hay soporte disponible |
| 4 | falló la lectura de la política o de las opciones | se pide soporte | el soporte sí se ofrece porque la decisión es BLOQUEADA con anomalía que exige validación manual |
| 5 | el caso base (R4 concede CASH_COMPENSATION) y una variante sin esa regla | se pide compensación con la decisión que vio | en el caso base se acepta y fija la compensación; en la variante se rechaza por motivo no disponible |

**Acceptance Criteria**:

- [ ] Con decisión indicada se realizan 0 lecturas nuevas.
- [ ] El 0 % de los motivos de compensación se acepta sin compensación elegible.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Elegir origen de evidencia → Verificar acción posible → Verificar elegibilidad del motivo
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.30 SF-03.3 Resolución de motivos

**Spec fuente**: [SF-03.3 Resolución de motivos](30-sf-03-3-resolucion-de-motivos.md)  
**Requisitos**: FR-057, FR-063, FR-102, NFR-012  
**Pruebas (TC)**: TC-01, TC-49

Une el motivo elegido con los motivos del sistema, los ordena por prioridad y fija el motivo principal y la lista completa.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el sistema detecta aprobación por menor y pernocte, y el pasajero elige otra ayuda | se resuelven | el motivo principal es el de mayor prioridad y la evidencia conserva los tres |
| 2 | se cambia `REASON_PRIORITY` | se resuelven | cambia el motivo principal |
| 3 | los motivos del caso base ABC123: aprobación de política, pernocte y otra ayuda | se resuelven | el motivo principal es aprobación de política y la evidencia conserva los 3 |

**Acceptance Criteria**:

- [ ] El motivo principal coincide con el de mayor prioridad en el 100 % de las combinaciones probadas.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Reunir motivos → Ordenar por prioridad → Fijar motivo principal
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.31 SF-03.4 Deduplicación

**Spec fuente**: [SF-03.4 Deduplicación](31-sf-03-4-deduplicacion.md)  
**Requisitos**: FR-059  
**Pruebas (TC)**: TC-33

Calcula la clave de deduplicación (reserva, motivos ordenados y huella de decisión) y devuelve el caso existente si ya hay uno creado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | ya hay un caso creado con la misma clave | se pide otro | se devuelve el existente |
| 2 | el intento anterior fue fallido o indeterminado | el pasajero reintenta de forma explícita | la deduplicación no lo bloquea y se registra un intento nuevo |
| 3 | un caso HC-4471 creado para ABC123 y luego un intento fallido | se repite el clic | con el caso creado se devuelve HC-4471 sin enviar; tras el intento fallido se permite un intento nuevo |

**Acceptance Criteria**:

- [ ] Cero casos creados para la misma clave mientras exista uno creado.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Calcular clave → Buscar caso creado → Permitir reintento explícito
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.32 SF-03.5 Reserva atómica del intento

**Spec fuente**: [SF-03.5 Reserva atómica del intento](32-sf-03-5-reserva-atomica-del-intento.md)  
**Requisitos**: FR-059, FR-064, FR-105  
**Pruebas (TC)**: TC-22, TC-33, TC-38

Registra el intento en curso antes de llamar, con exclusión concurrente, y recupera los intentos colgados.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | hay un intento en curso vigente | llega otra solicitud igual | no envía y devuelve el caso con estado en curso |
| 2 | un intento está en curso hace más de `OPERATION_STALE_SECONDS` (120) | se lee el registro | pasa a indeterminado y exige confirmar el posible duplicado |
| 3 | un intento en curso hace 121 s y otro simultáneo | llegan 2 solicitudes | la simultánea no envía y el colgado pasa a indeterminado |

**Acceptance Criteria**:

- [ ] Con 100 solicitudes simultáneas se envía exactamente una.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Reservar intento en curso → Detectar intento vigente → Recuperar colgados
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.33 SF-03.6 Llamada al caso humano

**Spec fuente**: [SF-03.6 Llamada al caso humano](33-sf-03-6-llamada-al-caso-humano.md)  
**Requisitos**: FR-059, FR-061, FR-105  
**Pruebas (TC)**: TC-20, TC-33

Una llamada al proveedor de casos con evidencia sin información personal, y traducción del resultado: creado, fallido o indeterminado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el proveedor devuelve caso, cola y plazo | se llama | el intento queda creado y el mensaje cita el plazo devuelto |
| 2 | el proveedor responde con error | se llama | el intento queda fallido y el mensaje dice «puedes reintentar» |
| 3 | el proveedor no responde | se llama | el intento queda indeterminado y no se reenvía |
| 4 | el proveedor de casos responde HC-4471, o un error, o no responde en 5 s | se llama | creado con 45 minutos, fallido «puedes reintentar» e indeterminado sin reenvío |

**Acceptance Criteria**:

- [ ] El 0 % de las evidencias enviadas contiene información personal.
- [ ] El 0 % de los timeouts se reenvía sin segundo clic.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Resultado de caso humano | outcome, message, human_case, decision_id | Respuesta a un clic de «Hablar con una persona». |

**Business Process (BPM)**:

```
Armar evidencia → Llamar al proveedor de casos → Traducir resultado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.34 SF-03.7 Reintento tras indeterminado

**Spec fuente**: [SF-03.7 Reintento tras indeterminado](34-sf-03-7-reintento-tras-indeterminado.md)  
**Requisitos**: FR-050, FR-105  
**Pruebas (TC)**: TC-33

Tras un intento indeterminado exige un segundo clic explícito, con advertencia del posible duplicado, para crear un intento nuevo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el intento previo fue indeterminado | el pasajero reenvía sin confirmar el posible duplicado | no se envía y se muestra la advertencia |
| 2 | el pasajero confirma el posible duplicado | reenvía | se crea un intento nuevo con la misma opción como evidencia |
| 3 | el intento anterior de ABC123 quedó indeterminado | se reenvía sin y con confirmación del posible duplicado | sin confirmar no se envía; con confirmar se crea el intento 2 con la misma opción O1 |

**Acceptance Criteria**:

- [ ] El 100 % de los reintentos tras indeterminado exige la confirmación explícita.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Resultado de caso humano | outcome, message, human_case, decision_id | Respuesta a un clic de «Hablar con una persona». |

**Business Process (BPM)**:

```
Detectar intento indeterminado → Advertir posible duplicado → Aceptar segundo clic → Crear intento nuevo
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.35 SF-03.8 Mensaje y registro

**Spec fuente**: [SF-03.8 Mensaje y registro](35-sf-03-8-mensaje-y-registro.md)  
**Requisitos**: FR-081, FR-091  
**Pruebas (TC)**: TC-16, TC-20

Construye el mensaje validado con el plazo de atención devuelto, persiste el resultado del intento y responde con el resultado de caso humano.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el caso quedó creado con plazo de atención | se arma el mensaje | cita únicamente el plazo devuelto |
| 2 | cualquier resultado | se registra | queda el intento con su estado, sin texto libre ni información personal |
| 3 | el caso HC-4471 con 45 minutos, pedido con el motivo «Necesito ayuda con mis datos o documentos» | se arma el mensaje | cita 45 minutos, nunca otro plazo, y no incluye ningún dato personal |

**Acceptance Criteria**:

- [ ] El 100 % de los mensajes de resultado pasa por el validador y no cita plazos distintos del devuelto.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de caso humano | outcome, message, human_case, decision_id | Respuesta a un clic de «Hablar con una persona». |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |

**Business Process (BPM)**:

```
Armar mensaje → Validar → Registrar resultado → Responder
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.36 F-04 Consulta de decisión

**Spec fuente**: [F-04 Consulta de decisión](36-f-04-consulta-de-decision.md)  
**Requisitos**: FR-001, FR-042, FR-090, FR-091, FR-093, NFR-002  
**Pruebas (TC)**: TC-21, TC-59

Devuelve el registro de auditoría de una decisión, solo si pertenece a la reserva de la sesión, con los campos de la lista cerrada, las opciones no viables con todas sus razones de descarte y, en evaluaciones del sistema, el llamante; la sesión del pasajero no recibe la revisión manual ni el detalle de las notificaciones (campos internos).

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una decisión de la reserva de la sesión | se consulta por su identificador | se devuelve el registro con la lista cerrada de campos y todas las opciones, también las no viables, con sus razones de descarte |
| 2 | la decisión es de otra reserva o no existe | se consulta | la respuesta es idéntica de «no encontrado» |
| 3 | la decisión se originó en una evaluación del sistema | se consulta | incluye el llamante, pero no la revisión manual ni el detalle de las notificaciones, que son campos internos |
| 4 | una decisión de ABC123 evaluada por el sistema y otra de XYZ789 | la sesión de ABC123 lee ambas | la propia devuelve el registro con O3 descartada y sin revisión manual ni notificaciones; la ajena responde «no encontrado» idéntico |

**Acceptance Criteria**:

- [ ] El 100 % de las consultas ajenas e inexistentes recibe una respuesta idéntica.
- [ ] El registro devuelto contiene el 0 % de campos de la lista prohibida.
- [ ] La consulta responde en menos de 200 ms (percentil 95) en una lectura local.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Autorizar pertenencia → Leer registro → Proyectar a lista cerrada
```

Subprocess detail (if applicable):

```
SF-04.1: Autorización de pertenencia
SF-04.2: Lectura del registro
SF-04.3: Proyección a la lista cerrada de campos
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.37 SF-04.1 Autorización de pertenencia

**Spec fuente**: [SF-04.1 Autorización de pertenencia](37-sf-04-1-autorizacion-de-pertenencia.md)  
**Requisitos**: FR-001, FR-093, NFR-013  
**Pruebas (TC)**: TC-21, TC-58

Comprueba que la sesión es la dueña de la reserva a la que pertenece la decisión pedida.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la decisión pertenece a la reserva de la sesión | se consulta | se permite la lectura |
| 2 | la decisión pertenece a otra reserva | se consulta | se responde exactamente igual que a una inexistente |
| 3 | la sesión de ABC123 y una decisión de XYZ789 | se consulta | se responde igual que a una inexistente |
| 4 | la sesión de ABC123 con 30 consultas de decisión en el último minuto desde el mismo origen | llega la 31.ª | se rechaza por límite de tasa |

**Acceptance Criteria**:

- [ ] El 100 % de las lecturas ajenas se responde igual que las inexistentes.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | Identidad con la que se pide una evaluación: sesión del pasajero o credencial de servicio. |

**Business Process (BPM)**:

```
Comprobar sesión → Comprobar pertenencia
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.38 SF-04.2 Lectura del registro

**Spec fuente**: [SF-04.2 Lectura del registro](38-sf-04-2-lectura-del-registro.md)  
**Requisitos**: FR-042, FR-090, FR-093  
**Pruebas (TC)**: TC-01

Recupera el registro guardado de la decisión, con sus lecturas, eventos, reglas, variables, opciones, acciones y resultados.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una decisión con una opción de reembolso sin respaldo | se lee el registro | la opción aparece como no viable con todas sus razones de descarte |
| 2 | se creó una solicitud o un caso | se lee el registro | aparecen sus estados y referencias |
| 3 | la decisión del caso base con O3 sin respaldo recuperado | se lee el registro | O3 figura como no viable con sus razones y O1 como propuesta |

**Acceptance Criteria**:

- [ ] El registro del caso base incluye las tres opciones con sus razones de descarte cuando corresponde.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, date, departure, fare_difference, currency, seats_available, policy_ref, confidence, viable, discard_reasons, fingerprint, is_proposed, overnight, expires_at | Alternativa candidata entregada por el proveedor; solo las viables se muestran. |

**Business Process (BPM)**:

```
Buscar decisión → Reunir lecturas, eventos y reglas → Reunir opciones y resultados
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.39 SF-04.3 Proyección a la lista cerrada de campos

**Spec fuente**: [SF-04.3 Proyección a la lista cerrada de campos](39-sf-04-3-proyeccion-a-la-lista-cerrada-de-campos.md)  
**Requisitos**: FR-091, FR-093, NFR-002  
**Pruebas (TC)**: TC-21, TC-59

Entrega solo los campos de la lista cerrada de FR-091, sin información personal.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | las lecturas originales contenían nombre y contacto ficticios | se consulta el registro | ninguno aparece |
| 2 | cualquier decisión | se consulta | solo hechos operacionales, identificadores seudónimos, enumeraciones, números, marcas de tiempo y huellas |
| 3 | una evaluación del sistema con revisión manual y 2 notificaciones | la sesión de ABC123 lee la decisión | no aparecen la revisión manual ni las notificaciones y no hay ningún dato de Ana |

**Acceptance Criteria**:

- [ ] Una búsqueda de los datos ficticios en la respuesta no encuentra ninguno.
- [ ] La respuesta a la sesión del pasajero no contiene la revisión manual ni el detalle de las notificaciones en el 100 % de los casos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Filtrar por lista cerrada → Quitar campos internos → Entregar registro
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.40 F-05 Ping

**Spec fuente**: [F-05 Ping](40-f-05-ping.md)  
**Requisitos**: FR-110, NFR-005  
**Pruebas (TC)**: TC-01

Verificación de vida del servicio: responde «pong» en texto plano y no requiere sesión.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el servicio está en marcha | se hace la verificación de vida | responde «pong» en texto plano sin pedir sesión |
| 2 | cualquier llamada | se hace la verificación de vida | la respuesta no revela información de reservas ni de configuración |
| 3 | el servicio en marcha sin sesión | se hace la verificación de vida | responde «pong» en menos de 50 ms |

**Acceptance Criteria**:

- [ ] La verificación responde en menos de 50 ms (percentil 99).
- [ ] La respuesta es exactamente «pong» en el 100 % de los casos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |

**Business Process (BPM)**:

```
Recibir verificación → Responder pong
```

Subprocess detail (if applicable):

```
SF-05.1: Respuesta fija
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.41 SF-05.1 Respuesta fija

**Spec fuente**: [SF-05.1 Respuesta fija](41-sf-05-1-respuesta-fija.md)  
**Requisitos**: FR-110  
**Pruebas (TC)**: TC-01

Devuelve el texto fijo «pong» sin depender de la sesión ni de los proveedores externos.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | todos los proveedores están caídos | se hace la verificación | responde «pong» |
| 2 | los 7 proveedores simulados caídos | se hace la verificación de vida | responde «pong» igualmente |

**Acceptance Criteria**:

- [ ] La respuesta es idéntica en cada llamada.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |

**Business Process (BPM)**:

```
Responder texto fijo
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.42 F-06 Escenarios y reloj de desarrollo

**Spec fuente**: [F-06 Escenarios y reloj de desarrollo](42-f-06-escenarios-y-reloj-de-desarrollo.md)  
**Requisitos**: FR-001, FR-017, FR-071, FR-100, FR-101, FR-102, FR-103, FR-111, NFR-001, NFR-006  
**Pruebas (TC)**: TC-01, TC-08, TC-27, TC-32, TC-49, TC-57, TC-58, TC-59, TC-60

Solo en desarrollo: lista los escenarios (los siete ejemplos del enunciado con datos personales ficticios y las variantes de prueba), activa uno en las simulaciones de las siete herramientas y gobierna el reloj de escenario, que solo avanza a pedido.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | los funciones de desarrollo están habilitados | se pide el catálogo | se devuelven los escenarios, el activo y el reloj; `ui` indica los visibles en el selector |
| 2 | existe el escenario pedido | se activa | las simulaciones sirven sus datos y el reloj vuelve al instante base del escenario |
| 3 | modo de reloj de escenario | se avanzan 120 segundos | las opciones del escenario quedan vencidas en el instante exacto y la demostración del vencimiento es posible |
| 4 | los funciones de desarrollo están apagados (valor por defecto) | se piden | responden «desactivado» y rige el reloj del sistema |
| 5 | las funciones de desarrollo habilitadas y el catálogo con INDETERMINADA_VENCE_TC57, LIMITE_TASA_TEXTO_PLANO_TC58, DECISION_SESION_SIN_INTERNOS_TC59 y AVISO_TITULAR_ADULTO_TC60 | se activa cada una sobre ABC123 | cada variante se activa y el reloj vuelve a 11:02:35Z con desplazamiento 0 |

**Acceptance Criteria**:

- [ ] El 100 % de los TC-01 a TC-60 tiene un escenario o variante activable (incluidos los de TC-57 a TC-60).
- [ ] Con las funciones de desarrollo apagadas el 100 % de las llamadas de desarrollo responde como desactivado.
- [ ] Los escenarios no contienen datos personales reales.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |
| Reloj de escenario | mode, now, offset_seconds, advance_seconds | Reloj controlado de desarrollo: instante base del escenario más un desplazamiento que solo avanza a pedido. |

**Business Process (BPM)**:

```
Verificar habilitación → Listar catálogo → Activar escenario y reiniciar reloj → Avanzar reloj
```

Subprocess detail (if applicable):

```
SF-06.1: Verificación de los flags de desarrollo
SF-06.2: Listado del catálogo
SF-06.3: Activación del escenario y reinicio del reloj
SF-06.4: Avance del reloj de escenario
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.43 SF-06.1 Verificación de los flags de desarrollo

**Spec fuente**: [SF-06.1 Verificación de los flags de desarrollo](43-sf-06-1-verificacion-de-los-flags-de-desarrollo.md)  
**Requisitos**: FR-001, NFR-003  
**Pruebas (TC)**: TC-21, TC-49

Comprueba que los funciones de desarrollo y la sesión simulada estén habilitados antes de atender.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | `DEV_ENDPOINTS_ENABLED` es falso | se llama | responde «desactivado» |
| 2 | `DEV_SESSION_HEADER_ENABLED` es falso | se usa la sesión simulada | toda consulta de negocio se rechaza por falta de autenticación |
| 3 | `DEV_ENDPOINTS_ENABLED` y `DEV_SESSION_HEADER_ENABLED` sin definir | se piden el catálogo y la sesión simulada de ABC123 | ambas responden como desactivadas |

**Acceptance Criteria**:

- [ ] En el perfil por defecto el 100 % de las llamadas de desarrollo y de sesión simulada se rechaza.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Leer banderas → Permitir o rechazar
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.44 SF-06.2 Listado del catálogo

**Spec fuente**: [SF-06.2 Listado del catálogo](44-sf-06-2-listado-del-catalogo.md)  
**Requisitos**: FR-100, FR-101, FR-102, FR-103, FR-111  
**Pruebas (TC)**: TC-01, TC-02, TC-03, TC-57, TC-58, TC-59, TC-60

Devuelve el escenario activo, el reloj vigente y el catálogo con título, descripción, visibilidad en el selector y pruebas relacionadas.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | los funciones de desarrollo están habilitados | se lista | aparecen los escenarios con `ui` verdadero y las variantes de prueba con `ui` falso |
| 2 | cualquier escenario | se inspecciona | los datos personales son claramente ficticios |
| 3 | el catálogo con BASE_TC01, SOLO_DEGRADADO_TC02 (solo E-1012) y CONFLICTO_TC03 | se lista | BASE_TC01 y SOLO_DEGRADADO_TC02 son visibles y todos traen datos ficticios de Ana Prueba |

**Acceptance Criteria**:

- [ ] Los siete ejemplos del enunciado figuran en el catálogo.
- [ ] Una búsqueda de datos personales del enunciado original no encuentra ninguno.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |

**Business Process (BPM)**:

```
Leer catálogo → Entregar escenario activo y reloj
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.45 SF-06.3 Activación del escenario y reinicio del reloj

**Spec fuente**: [SF-06.3 Activación del escenario y reinicio del reloj](45-sf-06-3-activacion-del-escenario-y-reinicio-del-reloj.md)  
**Requisitos**: FR-100, FR-101, FR-103  
**Pruebas (TC)**: TC-27

Cambia el conjunto de datos de las simulaciones y reinicia el reloj de escenario al instante de lectura del contexto del escenario.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | un escenario válido | se activa | el reloj queda en el instante de lectura del escenario con desplazamiento cero |
| 2 | un identificador fuera del catálogo | se activa | respuesta de escenario no encontrado |
| 3 | BASE_TC01 activo con el reloj avanzado 120 s | se activa SIN_MENOR_TC07 | el reloj vuelve a 11:02:35Z con desplazamiento 0 |

**Acceptance Criteria**:

- [ ] Tras activar, el desplazamiento del reloj es 0 en el 100 % de los casos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |
| Reloj de escenario | mode, now, offset_seconds, advance_seconds | Reloj controlado de desarrollo: instante base del escenario más un desplazamiento que solo avanza a pedido. |

**Business Process (BPM)**:

```
Validar escenario → Cambiar datos simulados → Reiniciar reloj
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.46 SF-06.4 Avance del reloj de escenario

**Spec fuente**: [SF-06.4 Avance del reloj de escenario](46-sf-06-4-avance-del-reloj-de-escenario.md)  
**Requisitos**: FR-017, FR-071, NFR-001  
**Pruebas (TC)**: TC-08, TC-27

Suma segundos al desplazamiento del reloj de escenario para demostrar vigencias y vencimientos sin esperar.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el escenario activo y modo de reloj de escenario | se avanzan 120 segundos | devuelve el nuevo instante y el desplazamiento |
| 2 | el valor es negativo o mayor que 86400 | se avanza | rechazo por validación |
| 3 | el escenario base con reloj 11:02:35Z | se avanzan 120 s | el reloj marca 11:04:35Z y las opciones quedan vencidas |

**Acceptance Criteria**:

- [ ] El desplazamiento solo cambia con la orden explícita de avance.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Reloj de escenario | mode, now, offset_seconds, advance_seconds | Reloj controlado de desarrollo: instante base del escenario más un desplazamiento que solo avanza a pedido. |

**Business Process (BPM)**:

```
Validar avance → Sumar desplazamiento → Informar instante vigente
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.47 F-07 Purga de retención

**Spec fuente**: [F-07 Purga de retención](47-f-07-purga-de-retencion.md)  
**Requisitos**: FR-092, FR-064, NFR-005, NFR-012  
**Pruebas (TC)**: TC-32, TC-56, TC-57

Elimina, por comando y una vez al arrancar, los registros de decisión, operaciones, casos y notificaciones más antiguos que `AUDIT_RETENTION_DAYS` (30, provisional), conservando el registro mínimo de las operaciones no finalizadas.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | registros más antiguos que la retención | se ejecuta la purga | se eliminan en cascada y se informa cuántas filas se borraron |
| 2 | una operación CREADA de 31 días de antigüedad cuyo vencimiento todavía no llega (a +10 min) | se ejecuta la purga | se conserva minimizada (solo identidad, estado y vigencia) y su bloqueo sigue impidiendo una operación nueva |
| 3 | FixedClock 2026-10-19T00:00:00Z y retención de 30 días (corte 2026-09-19T00:00:00Z), registros de 29 y 31 días, 3 operaciones jóvenes (EN_CURSO de 10 s, INDETERMINADA de 300 s, CREADA con vencimiento a +10 min) y 3 vencidas (EN_CURSO de 40 días, INDETERMINADA de 40 días, CREADA vencida hace 40 días) | se ejecuta la purga | primero se aplican los vencimientos (las 3 vencidas pasan a EXPIRADA) y luego se borra por antigüedad: se eliminan las 3 vencidas y los registros de 31 días; se conservan las 3 operaciones jóvenes y el registro de 29 días |

**Acceptance Criteria**:

- [ ] El 100 % de los registros más antiguos que la retención se elimina, salvo las operaciones no finalizadas, que quedan minimizadas.
- [ ] Una purga no borra ningún registro más reciente que el umbral.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de retención | cutoff, deleted_decisions, deleted_operations, deleted_cases, deleted_notifications, expired_by_sweep, minimized_operations | Resultado de una purga del registro: cuántas filas se eliminaron y cuáles se conservaron minimizadas. |
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Calcular umbral → Borrar en cascada → Minimizar operaciones vigentes → Informar
```

Subprocess detail (if applicable):

```
SF-07.1: Cálculo del umbral con el reloj inyectado
SF-07.2: Borrado en cascada
SF-07.3: Informe de filas eliminadas
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.48 SF-07.1 Cálculo del umbral con el reloj inyectado

**Spec fuente**: [SF-07.1 Cálculo del umbral con el reloj inyectado](48-sf-07-1-calculo-del-umbral-con-el-reloj-inyectado.md)  
**Requisitos**: FR-092, NFR-001, NFR-012  
**Pruebas (TC)**: TC-32

Calcula la fecha de corte restando la retención al instante vigente del reloj inyectado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | reloj fijo y retención de 30 días | se calcula | el corte es treinta días antes del instante fijo |
| 2 | reloj fijo 2026-10-19T00:00:00Z y retención de 30 días | se calcula | el corte es 2026-09-19T00:00:00Z |

**Acceptance Criteria**:

- [ ] El corte es idéntico en repeticiones con el mismo reloj.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de retención | cutoff, deleted_decisions, deleted_operations, deleted_cases, deleted_notifications, expired_by_sweep, minimized_operations | Resultado de una purga del registro: cuántas filas se eliminaron y cuáles se conservaron minimizadas. |
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Leer retención → Leer reloj → Calcular corte
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.49 SF-07.2 Borrado en cascada

**Spec fuente**: [SF-07.2 Borrado en cascada](49-sf-07-2-borrado-en-cascada.md)  
**Requisitos**: FR-064, FR-092  
**Pruebas (TC)**: TC-32, TC-56

Elimina los registros de decisión y sus dependientes y los de operaciones, casos y notificaciones más antiguos que el corte, conservando minimizadas las operaciones no finalizadas.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una decisión antigua con opciones y reglas | se borra | desaparecen todas sus dependientes |
| 2 | una operación INDETERMINADA de 300 s, una CREADA con vencimiento a +10 min y una INDETERMINADA de 40 días | se borra por antigüedad tras aplicar los vencimientos | la de 40 días ya venció a EXPIRADA y se elimina; las 2 vigentes se conservan y, si superaran la retención, quedarían minimizadas |
| 3 | operaciones en curso de 10 s, indeterminada de 300 s y creada con vencimiento a +10 min, más una EN_CURSO de 40 días, una fallida y una expirada | se borra | las 3 vigentes se conservan y las 3 vencidas o finales se eliminan |

**Acceptance Criteria**:

- [ ] Ninguna operación no finalizada se pierde por antigüedad.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de retención | cutoff, deleted_decisions, deleted_operations, deleted_cases, deleted_notifications, expired_by_sweep, minimized_operations | Resultado de una purga del registro: cuántas filas se eliminaron y cuáles se conservaron minimizadas. |
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |

**Business Process (BPM)**:

```
Seleccionar antiguos → Borrar dependientes → Minimizar vigentes
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.50 SF-07.3 Informe de filas eliminadas

**Spec fuente**: [SF-07.3 Informe de filas eliminadas](50-sf-07-3-informe-de-filas-eliminadas.md)  
**Requisitos**: FR-092, FR-091, NFR-005  
**Pruebas (TC)**: TC-32, TC-56

Informa cuántas filas se eliminaron y cuántas operaciones se conservaron minimizadas, sin datos personales.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una purga ejecutada | termina | muestra el número de filas eliminadas por tipo y de operaciones minimizadas |
| 2 | una purga con retención de 30 días que aplicó 3 vencimientos, eliminó 5 filas y minimizó 1 operación aún vigente | se informa | dice 3 vencimientos aplicados, 5 filas eliminadas y 1 minimizada, sin datos personales |

**Acceptance Criteria**:

- [ ] El informe coincide en el 100 % con las filas efectivamente afectadas.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de retención | cutoff, deleted_decisions, deleted_operations, deleted_cases, deleted_notifications, expired_by_sweep, minimized_operations | Resultado de una purga del registro: cuántas filas se eliminaron y cuáles se conservaron minimizadas. |

**Business Process (BPM)**:

```
Contar filas → Redactar informe
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.51 F-08 Notificación al pasajero

**Spec fuente**: [F-08 Notificación al pasajero](51-f-08-notificacion-al-pasajero.md)  
**Requisitos**: FR-050, FR-081, FR-085, FR-103, FR-122, FR-123, DOC-013  
**Pruebas (TC)**: TC-42, TC-44, TC-48, TC-50, TC-55, TC-60

Solo invocado por la evaluación del sistema: envía el aviso con plantilla fija «Hubo un cambio en tu vuelo asociado a {motivo}. Revisa tu reserva en la web o en la aplicación.», una notificación por motivo (retraso con política rota; cambio de puerta validado), dirigida al titular adulto y nunca al menor, sin dirección web, enlace ni contacto, y de forma idempotente (la huella del retraso es la versión de política más las reglas disparadas).

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el sistema evalúa un retraso con política rota y la notificación está activa | se notifica | se envía el aviso de tipo política con el motivo «un retraso» y la referencia de política evaluada |
| 2 | hay un cambio de puerta validado | se notifica | se envía el aviso informativo con el motivo «un cambio de puerta» y sin referencia de política, sin inventar una |
| 3 | la misma notificación se pidió hace menos del enfriamiento | se pide de nuevo | no se reenvía y se informa que fue deduplicada con el estado del envío previo |
| 4 | una reserva donde el niño figura antes que el adulto | se notifica | el aviso se dirige al titular adulto, nunca al menor |
| 5 | ya se avisó un retraso con la política rota y luego el retraso pasa de 160 a 170 minutos con las mismas reglas disparadas | se evalúa de nuevo como sistema | no se repite el aviso porque la huella del motivo (versión de política y reglas disparadas) no cambió |
| 6 | la puerta cambia de 24 a 25 | se evalúa de nuevo como sistema | se envía un aviso nuevo porque la huella del motivo incluye la puerta validada |
| 7 | un texto contiene un enlace, dominio, teléfono o correo | pasa por el validador | se bloquea y nunca se envía |
| 8 | una reserva ABC123 con un solo pasajero, el niño P2, sin titular adulto, con un retraso E-1001 de 180 min (R1 concede REBOOK_NO_FEE) que rompe la política POL-DELAY-2026-03 y la notificación activa | se notifica en modo sistema | no se envía ningún aviso: el estado es NOT_SENT con la razón NO_ADULT_RECIPIENT («sin destinatario adulto») y la revisión manual queda verdadera |
| 9 | ABC123 con política rota POL-DELAY-2026-03 y la puerta 24, la notificación activa | se notifica en modo sistema | se envían 2 avisos con la plantilla fija, en cola con identificadores distintos (NT-9912 y NT-9913), sin enlaces; con la puerta 25 se envía un aviso nuevo y con la 24 repetida no |

**Acceptance Criteria**:

- [ ] El 0 % de los mensajes enviados contiene dirección web, enlace, teléfono o correo.
- [ ] La misma notificación (reserva, motivo, huella del motivo y plantilla) se envía una sola vez dentro del enfriamiento.
- [ ] El 100 % de las notificaciones aceptadas se informa como «en cola», nunca como entregada.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |

**Business Process (BPM)**:

```
Validar mensaje → Reservar llave → Llamar con reintentos → Mapear resultado
```

Subprocess detail (if applicable):

```
SF-08.1: Validación del mensaje
SF-08.2: Llave idempotente y reserva atómica
SF-08.3: Llamada con reintentos
SF-08.4: Mapeo de resultados y registro
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.52 SF-08.1 Validación del mensaje

**Spec fuente**: [SF-08.1 Validación del mensaje](52-sf-08-1-validacion-del-mensaje.md)  
**Requisitos**: FR-081, FR-122  
**Pruebas (TC)**: TC-16, TC-48, TC-60

Construye el texto de la plantilla con el motivo cerrado y lo valida: texto idéntico a la plantilla, referencia de política según el tipo, destinatario y ausencia de datos de contacto.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | plantilla fija con «un retraso» y referencia de política | se valida | pasa |
| 2 | tipo informativo y sin referencia de política | se valida | pasa; con referencia sería bloqueado |
| 3 | el texto trae un enlace, dominio, correo o teléfono | se valida | se bloquea y no se envía |
| 4 | una reserva ABC123 con un solo pasajero, el niño P2, sin titular adulto, con un retraso E-1001 de 180 min (R1 concede REBOOK_NO_FEE) que rompe la política POL-DELAY-2026-03 y la notificación activa | se arma el mensaje | no se envía ningún aviso: el estado es NOT_SENT con la razón NO_ADULT_RECIPIENT («sin destinatario adulto») y la revisión manual queda verdadera |
| 5 | un texto con «www.ejemplo.test» y otro sin referencia de política con tipo política | pasan por el validador | ambos se bloquean antes de llamar |

**Acceptance Criteria**:

- [ ] El 100 % de los textos con datos de contacto se bloquea antes de llamar.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |

**Business Process (BPM)**:

```
Armar texto de plantilla → Verificar plantilla y motivo → Verificar referencia de política → Detectar datos de contacto
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.53 SF-08.2 Llave idempotente y reserva atómica

**Spec fuente**: [SF-08.2 Llave idempotente y reserva atómica](53-sf-08-2-llave-idempotente-y-reserva-atomica.md)  
**Requisitos**: FR-064, FR-123, NFR-012  
**Pruebas (TC)**: TC-44, TC-55, TC-60

Calcula la llave por reserva, motivo, huella del motivo y plantilla y reserva el intento en curso antes de llamar, gestionando las transiciones por enfriamiento.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | ya hay un aviso vigente dentro del enfriamiento | se pide de nuevo | no se reenvía, con indicación de deduplicado |
| 2 | el retraso pasa de 160 a 170 minutos con la misma versión de política y las mismas reglas cumplidas | se pide de nuevo | la llave no cambia y el aviso no se repite |
| 3 | la puerta pasa de 24 a 25 | se pide | la llave cambia y se envía un aviso nuevo |
| 4 | el intento anterior fue fallido o vencido | se pide | se permite una reserva nueva de inmediato |
| 5 | un aviso en cola hace 1 h con `NOTIFY_COOLDOWN_SECONDS` de 86400 | se pide de nuevo con la misma puerta y luego con la puerta 25 | la primera se deduplica y la segunda envía un aviso nuevo |

**Acceptance Criteria**:

- [ ] Cero avisos duplicados por la misma (reserva, motivo, huella, plantilla) dentro del enfriamiento.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |

**Business Process (BPM)**:

```
Calcular llave → Normalizar estados vencidos → Reservar intento en curso
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.54 SF-08.3 Llamada con reintentos

**Spec fuente**: [SF-08.3 Llamada con reintentos](54-sf-08-3-llamada-con-reintentos.md)  
**Requisitos**: FR-123, NFR-012  
**Pruebas (TC)**: TC-44

Llama al proveedor de notificaciones con el tiempo de escritura configurado y reintenta con la misma llave ante falla temporal.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el proveedor falla una vez y luego acepta | se llama | queda en cola con la misma llave |
| 2 | falla en la llamada y en los reintentos | se llama | queda indeterminada |
| 3 | el proveedor no responde en 5 s | se llama con `NOTIFY_MAX_RETRIES` de 2 | hay 3 llamadas con la misma llave y la notificación queda indeterminada |

**Acceptance Criteria**:

- [ ] El número de llamadas nunca supera 1 más `NOTIFY_MAX_RETRIES`.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |

**Business Process (BPM)**:

```
Llamar → Esperar y reintentar → Entregar resultado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.55 SF-08.4 Mapeo de resultados y registro

**Spec fuente**: [SF-08.4 Mapeo de resultados y registro](55-sf-08-4-mapeo-de-resultados-y-registro.md)  
**Requisitos**: FR-123  
**Pruebas (TC)**: TC-44

Traduce la respuesta a estados (en cola, fallida, indeterminada) y registra con actualización condicional por intento y estado esperado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el proveedor acepta | se registra | estado «en cola»; no se afirma entrega |
| 2 | llega la respuesta de un intento viejo cuando ya hay uno nuevo | se registra | no cambia el nuevo ni sobrescribe un estado final |
| 3 | el intento 1 pasó a vencida y existe el intento 2 en curso | llega la respuesta 202 del intento 1 | no modifica el intento 2 |

**Acceptance Criteria**:

- [ ] Una respuesta fuera de orden modifica 0 registros.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |

**Business Process (BPM)**:

```
Interpretar respuesta → Actualizar con condición → Registrar estado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.56 F-09 Ciclo de vida de operaciones, intentos de caso y notificaciones (barrido perezoso)

**Spec fuente**: [F-09 Ciclo de vida de operaciones, intentos de caso y notificaciones (barrido perezoso)](56-f-09-ciclo-de-vida-de-operaciones-intentos-de-caso-y.md)  
**Requisitos**: FR-053, FR-059, FR-062, FR-064, FR-123, NFR-012  
**Pruebas (TC)**: TC-22, TC-38, TC-44, TC-57

Al leer los registros aplica las transiciones por el paso del tiempo: operación o intento en curso sin respuesta pasa a indeterminado, solicitud creada pasa a expirada, operación indeterminada pasa a expirada tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900), operación indeterminada pasa a expirada tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900), notificación en cola o indeterminada con enfriamiento terminado pasa a vencida, y una expirada o fallida admite la generación siguiente.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una operación en curso sobrepasó `OPERATION_STALE_SECONDS` (120) | se lee el registro | pasa a indeterminada |
| 2 | una solicitud creada llegó a su vencimiento | se lee el registro | pasa a expirada y permite una operación nueva con la generación siguiente |
| 3 | una operación indeterminada superó `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900) | se lee el registro | pasa a expirada y permite una operación nueva con la generación siguiente |
| 4 | una notificación en cola o indeterminada superó el enfriamiento | se lee | pasa a vencida y permite una nueva reserva |
| 5 | operación en curso hace 121 s, solicitud creada con vencimiento 11:12:00Z e indeterminada de 900 s | se lee el registro a las 11:12:01Z | pasan a indeterminada, expirada y expirada |

**Acceptance Criteria**:

- [ ] El 100 % de los registros vencidos se muestra con su estado actual en la siguiente lectura.
- [ ] No hay ningún proceso periódico: toda transición ocurre al leer.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |

**Business Process (BPM)**:

```
Detectar colgados → Vencer solicitudes, indeterminadas y notificaciones → Habilitar generación siguiente
```

Subprocess detail (if applicable):

```
SF-09.1: Detección de operaciones, casos y notificaciones colgados
SF-09.2: Vencimiento de solicitudes creadas e indeterminadas
SF-09.3: Generación siguiente de la llave
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.57 SF-09.1 Detección de operaciones, casos y notificaciones colgados

**Spec fuente**: [SF-09.1 Detección de operaciones, casos y notificaciones colgados](57-sf-09-1-deteccion-de-operaciones-casos-y-notificaciones.md)  
**Requisitos**: FR-059, FR-064, FR-123  
**Pruebas (TC)**: TC-38

Detecta los registros en curso sin respuesta tras `OPERATION_STALE_SECONDS` y los pasa a indeterminado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | operación en curso hace 121 segundos | se barre | indeterminada |
| 2 | operación en curso hace 119 segundos | se barre | sigue en curso |
| 3 | operaciones en curso hace 121 s y 119 s con `OPERATION_STALE_SECONDS` de 120 | se barre | la de 121 s pasa a indeterminada y la de 119 s sigue en curso |

**Acceptance Criteria**:

- [ ] El umbral de 120 s es exacto en el 100 % de los casos probados.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |

**Business Process (BPM)**:

```
Buscar en curso → Comparar con el umbral → Pasar a indeterminado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.58 SF-09.2 Vencimiento de solicitudes creadas e indeterminadas

**Spec fuente**: [SF-09.2 Vencimiento de solicitudes creadas e indeterminadas](58-sf-09-2-vencimiento-de-solicitudes-creadas-e-indetermina.md)  
**Requisitos**: FR-064, NFR-012  
**Pruebas (TC)**: TC-38, TC-57

Pasa a expirada una solicitud creada cuando llega su vencimiento y una operación indeterminada cuando supera `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900).

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | solicitud creada con vencimiento | el reloj lo alcanza | pasa a expirada y no bloquea la siguiente |
| 2 | una operación indeterminada con 899 segundos de antigüedad y otra con 900 | se lee el registro | la primera sigue bloqueando y la segunda pasa a expirada y permite la generación siguiente |
| 3 | dos operaciones indeterminadas de 899 s y 900 s y una purga previa que dejó `minimized` verdadero (solo identidad, estado y vigencia) | se lee el registro | la de 900 s pasa a expirada y la de 899 s sigue bloqueando; el estado se conserva aunque la operación esté minimizada |

**Acceptance Criteria**:

- [ ] El 100 % de las solicitudes creadas pasa a expirada en su vencimiento.
- [ ] El 100 % de las indeterminadas pasa a expirada al alcanzar `OPERATION_INDETERMINATE_EXPIRY_SECONDS`.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |

**Business Process (BPM)**:

```
Leer vencimiento → Comparar con el reloj → Pasar a expirada
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.59 SF-09.3 Generación siguiente de la llave

**Spec fuente**: [SF-09.3 Generación siguiente de la llave](59-sf-09-3-generacion-siguiente-de-la-llave.md)  
**Requisitos**: FR-053, FR-062, FR-064  
**Pruebas (TC)**: TC-22, TC-34, TC-38

Permite una operación nueva con la llave de la generación siguiente cuando la anterior está expirada o fallida.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la operación previa está expirada (incluida una indeterminada vencida) o fallida | se acepta de nuevo | se usa la llave con la generación siguiente |
| 2 | la operación previa está creada, en curso o indeterminada | se acepta de nuevo | se bloquea y se muestra su estado |
| 3 | una operación expirada de generación 1 para LA2412 | se acepta de nuevo | se usa la llave de la generación 2 y una creada de generación 1 sigue bloqueando |

**Acceptance Criteria**:

- [ ] Cero operaciones duplicadas en generaciones sucesivas.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, expires_at, passenger_ids, minimized | Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. |

**Business Process (BPM)**:

```
Revisar estado previo → Calcular generación → Permitir o bloquear
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.60 F-10 Reporte de métricas de éxito

**Spec fuente**: [F-10 Reporte de métricas de éxito](60-f-10-reporte-de-metricas-de-exito.md)  
**Requisitos**: NFR-008, FR-090, FR-091  
**Pruebas (TC)**: TC-01, TC-16

Por comando y de solo lectura, calcula desde el registro (sin información personal) las tres métricas: resolución sin contacto humano, tasa de casos humanos por motivo y afirmaciones sin evidencia.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | un registro con situaciones, opciones, operaciones y casos | se ejecuta el reporte | informa las tres métricas con sus definiciones y la unidad de análisis |
| 2 | hay evaluaciones informativas y del sistema | se ejecuta | no cuentan como situaciones accionables y se reportan aparte |
| 3 | 10 situaciones accionables, 4 con opción viable y operación creada sin caso humano, y 2 informativas | se ejecuta el reporte | M1 es 4 de 10, las informativas se reportan aparte y M3 informa 0 afirmaciones sin evidencia |

**Acceptance Criteria**:

- [ ] Las tres métricas se calculan solo desde el registro, sin una función de consulta nueva.
- [ ] La métrica de afirmaciones sin evidencia reporta 0.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Reporte de métricas | situations_actionable, m1_resolution_without_human, m1_viable_option_shown, m2_human_cases_by_reason, m3_messages_blocked, m3_unsupported_claims, informative_count | Cálculo de las tres métricas de éxito desde el registro, sin información personal. |
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Seleccionar situaciones → Calcular métricas → Emitir informe
```

Subprocess detail (if applicable):

```
SF-10.1: Selección de decisiones con anomalía y deduplicación por huella
SF-10.2: Cálculo de las tres métricas
SF-10.3: Informe
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.61 SF-10.1 Selección de decisiones con anomalía y deduplicación por huella

**Spec fuente**: [SF-10.1 Selección de decisiones con anomalía y deduplicación por huella](61-sf-10-1-seleccion-de-decisiones-con-anomalia-y-deduplica.md)  
**Requisitos**: NFR-008, FR-090  
**Pruebas (TC)**: TC-01

Selecciona las decisiones del pasajero con anomalía y las deduplica por reserva y huella, contando la primera.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | tres decisiones con la misma huella | se seleccionan | cuentan como una situación |
| 2 | decisiones del modo sistema | se seleccionan | no cuentan |
| 3 | 3 decisiones de ABC123 con la misma huella | se seleccionan | cuentan como 1 situación |

**Acceptance Criteria**:

- [ ] Las recargas nunca aumentan el denominador.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Reporte de métricas | situations_actionable, m1_resolution_without_human, m1_viable_option_shown, m2_human_cases_by_reason, m3_messages_blocked, m3_unsupported_claims, informative_count | Cálculo de las tres métricas de éxito desde el registro, sin información personal. |

**Business Process (BPM)**:

```
Filtrar por anomalía y llamante → Deduplicar por huella
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.62 SF-10.2 Cálculo de las tres métricas

**Spec fuente**: [SF-10.2 Cálculo de las tres métricas](62-sf-10-2-calculo-de-las-tres-metricas.md)  
**Requisitos**: NFR-008, FR-091  
**Pruebas (TC)**: TC-16

Calcula la resolución sin contacto humano, la tasa de casos por motivo y las afirmaciones sin evidencia.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | situaciones accionables con opción viable y operación creada o expirada sin caso | se calcula | es el cociente sobre las situaciones accionables |
| 2 | mensajes bloqueados por el validador | se calcula | se suman y las afirmaciones sin evidencia son 0 por construcción |
| 3 | 3 casos humanos CREADO, 2 por aprobación de política y 1 por conflicto de fuentes, sobre 10 situaciones | se calcula M2 | aprobación de política 2 de 10 y conflicto 1 de 10 |

**Acceptance Criteria**:

- [ ] Los resultados coinciden con los esperados en un registro de prueba.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Reporte de métricas | situations_actionable, m1_resolution_without_human, m1_viable_option_shown, m2_human_cases_by_reason, m3_messages_blocked, m3_unsupported_claims, informative_count | Cálculo de las tres métricas de éxito desde el registro, sin información personal. |

**Business Process (BPM)**:

```
Contar situaciones accionables → Calcular tres métricas
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.63 SF-10.3 Informe

**Spec fuente**: [SF-10.3 Informe](63-sf-10-3-informe.md)  
**Requisitos**: NFR-008, FR-091  
**Pruebas (TC)**: TC-01

Emite el informe de métricas con unidades y límites declarados.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el informe terminado | se lee | declara que la sesión se aproxima y que la ventana es la retención |
| 2 | un informe con 0 mensajes bloqueados | se lee | declara que la ventana máxima es de 30 días y que la sesión se aproxima por situación |

**Acceptance Criteria**:

- [ ] El informe no contiene ningún campo prohibido.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Reporte de métricas | situations_actionable, m1_resolution_without_human, m1_viable_option_shown, m2_human_cases_by_reason, m3_messages_blocked, m3_unsupported_claims, informative_count | Cálculo de las tres métricas de éxito desde el registro, sin información personal. |

**Business Process (BPM)**:

```
Redactar informe → Declarar límites
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.64 F-11 Evaluar viaje como sistema

**Spec fuente**: [F-11 Evaluar viaje como sistema](64-f-11-evaluar-viaje-como-sistema.md)  
**Requisitos**: FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-039, FR-050, FR-068, FR-085, FR-120, FR-121, FR-122, FR-123, FR-124, DOC-013, NFR-003, NFR-004, NFR-013  
**Pruebas (TC)**: TC-42, TC-43, TC-44, TC-45, TC-50, TC-51, TC-52, TC-55, TC-58, TC-59, TC-60

Otro sistema pide la misma evaluación con una credencial de servicio y recibe un resultado mínimo sin información personal; el servicio notifica por motivo (política rota por retraso, y cambio de puerta validado) y nunca ejecuta cambios ni casos humanos.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la credencial es válida y la notificación está activa | otro sistema pide la evaluación | se envía una notificación de política y la respuesta trae solo identificador de decisión, estado, motivo, estado de la notificación y revisión manual |
| 2 | hay un cambio de puerta validado | se evalúa como sistema | se envía un aviso informativo sin consultar política |
| 3 | hay retraso con política rota y cambio de puerta | se evalúa como sistema | se envían dos notificaciones, una por motivo, una tras otra |
| 4 | retraso sin política rota, o anomalía que impide evaluar la política | se evalúa como sistema | no se notifica y la decisión queda marcada para revisión manual cuando corresponde |
| 5 | decisión BLOQUEADA por menor desconocido con política rota | se evalúa como sistema | sí se notifica y además queda en revisión manual |
| 6 | una reserva ABC123 con un solo pasajero, el niño P2, sin titular adulto, con un retraso E-1001 de 180 min (R1 concede REBOOK_NO_FEE) que rompe la política POL-DELAY-2026-03 y la notificación activa | otro sistema pide la evaluación | no se envía ningún aviso: el estado es NOT_SENT con la razón NO_ADULT_RECIPIENT («sin destinatario adulto») y la revisión manual queda verdadera |
| 7 | ABC123 con retraso de 160 min y puerta 24 en S1, la credencial de servicio válida y un simulador que asigna identificadores distintos a cada aviso aceptado | otro sistema pide la evaluación | recibe decision_id, estado PENDIENTE_APROBACION, motivo DELAY, 2 notificaciones en cola con identificadores distintos (NT-9912 para el retraso y NT-9913 para la puerta) y revisión manual falsa, sin datos de Ana |

**Acceptance Criteria**:

- [ ] El 100 % de las respuestas del modo sistema carece de información personal y de vista completa.
- [ ] Cero llamadas a la solicitud de cambio o al caso humano en modo sistema.
- [ ] En el peor caso con dos notificaciones la evaluación completa no excede 47,2 s con los valores por defecto.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de evaluación del sistema | decision_id, decision_state, reason, notifications, needs_manual_review | Respuesta mínima y sin información personal para otro sistema. |
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | Identidad con la que se pide una evaluación: sesión del pasajero o credencial de servicio. |

**Business Process (BPM)**:

```
Validar cuerpo y credencial → Evaluar → Decidir notificaciones por motivo → Invocar notificación → Registrar auditoría → Responder sin información personal
```

Subprocess detail (if applicable):

```
SF-11.1: Validación del cuerpo y credencial de servicio
SF-11.2: Evaluación
SF-11.3: Decisión de notificar por motivo
SF-11.4: Invocación de la notificación
SF-11.5: Registro de auditoría
SF-11.6: Respuesta sin información personal
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.65 SF-11.1 Validación del cuerpo y credencial de servicio

**Spec fuente**: [SF-11.1 Validación del cuerpo y credencial de servicio](65-sf-11-1-validacion-del-cuerpo-y-credencial-de-servicio.md)  
**Requisitos**: FR-120, NFR-003, NFR-013  
**Pruebas (TC)**: TC-50, TC-58

Exige el modo `system` explícito y la credencial de servicio, comparada en tiempo constante.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | `SERVICE_API_KEY` configurada y enviada correctamente | se pide | se autoriza |
| 2 | `SERVICE_API_KEY` sin configurar | se pide | siempre se rechaza |
| 3 | `SERVICE_API_KEY` configurada y una petición con una clave distinta de la configurada | se pide la evaluación de ABC123 | se rechaza por falta de autenticación sin consultar ninguna herramienta ni revelar si la clave existe |
| 4 | un origen con 30 intentos fallidos de clave de servicio sobre ABC123 en un minuto | llega el 31.º intento, ya con la clave correcta | se rechaza por límite de tasa hasta que pase el minuto |

**Acceptance Criteria**:

- [ ] El 100 % de las peticiones sin credencial correcta se rechaza.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | Identidad con la que se pide una evaluación: sesión del pasajero o credencial de servicio. |

**Business Process (BPM)**:

```
Validar modo → Verificar credencial → Aplicar límite de tasa
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.66 SF-11.2 Evaluación

**Spec fuente**: [SF-11.2 Evaluación](66-sf-11-2-evaluacion.md)  
**Requisitos**: FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-039, FR-068, FR-121  
**Pruebas (TC)**: TC-45, TC-50, TC-51

Ejecuta la misma cadena de lecturas, validación, variables, reglas y opciones que el pasajero, pero sin armar la vista ni ofrecer acciones.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | las mismas lecturas | se evalúa como pasajero y como sistema | el estado de la decisión y su huella coinciden |
| 2 | modo sistema | se evalúa | no se ejecuta solicitud de cambio ni caso humano |
| 3 | retraso de 5 min en ABC123 | se evalúa como pasajero y como sistema | ambos dan INFORMATIVA con la misma huella y no se consultan opciones |

**Acceptance Criteria**:

- [ ] El estado de decisión y la huella son idénticos en ambos modos con las mismas lecturas.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, compensation_eligible, needs_manual_review | Resultado de evaluar la reserva: su estado y las razones que lo explican. |
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Leer en secuencia → Validar y decidir → Registrar sin armar la vista
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.67 SF-11.3 Decisión de notificar por motivo

**Spec fuente**: [SF-11.3 Decisión de notificar por motivo](67-sf-11-3-decision-de-notificar-por-motivo.md)  
**Requisitos**: FR-039, FR-068, FR-122, FR-123  
**Pruebas (TC)**: TC-43, TC-51, TC-52, TC-60

Decide, por motivo, si corresponde notificar: retraso con política rota (incluso BLOQUEADA o PENDIENTE_APROBACION) o cambio de puerta validado; sin ellos, no.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | decisión BLOQUEADA con política rota | se decide | se notifica el retraso y se marca revisión manual |
| 2 | retraso sin política rota | se decide | no se notifica («sin política rota») |
| 3 | `NOTIFY_ENABLED` falso | se decide | no se notifica («notificación desactivada») |
| 4 | una reserva ABC123 con un solo pasajero, el niño P2, sin titular adulto, con un retraso E-1001 de 180 min (R1 concede REBOOK_NO_FEE) que rompe la política POL-DELAY-2026-03 y la notificación activa | se decide por motivo | no se envía ningún aviso: el estado es NOT_SENT con la razón NO_ADULT_RECIPIENT («sin destinatario adulto») y la revisión manual queda verdadera |
| 5 | un pasajero sin tipo con retraso de 160 min (R3 cumplida, R5 no evaluable) | se decide | se notifica el retraso aunque la decisión sea BLOQUEADA y se marca revisión manual |

**Acceptance Criteria**:

- [ ] Cero notificaciones sin política rota ni cambio de puerta validado.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |
| Resultado de evaluación del sistema | decision_id, decision_state, reason, notifications, needs_manual_review | Respuesta mínima y sin información personal para otro sistema. |

**Business Process (BPM)**:

```
Evaluar motivo retraso → Evaluar motivo puerta → Aplicar bandera de notificación
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.68 SF-11.4 Invocación de la notificación

**Spec fuente**: [SF-11.4 Invocación de la notificación](68-sf-11-4-invocacion-de-la-notificacion.md)  
**Requisitos**: FR-122, FR-123  
**Pruebas (TC)**: TC-42, TC-52, TC-55, TC-60

Invoca el flujo de notificación una vez por motivo, en secuencia: política con su referencia, e informativa sin referencia.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | retraso con política rota y cambio de puerta | se invoca | se envían dos avisos distintos, uno tras otro, cada uno con su resultado |
| 2 | una reserva ABC123 con un solo pasajero, el niño P2, sin titular adulto, con un retraso E-1001 de 180 min (R1 concede REBOOK_NO_FEE) que rompe la política POL-DELAY-2026-03 y la notificación activa | se invoca la notificación | no se envía ningún aviso: el estado es NOT_SENT con la razón NO_ADULT_RECIPIENT («sin destinatario adulto») y la revisión manual queda verdadera |
| 3 | retraso de 160 min con política rota y la puerta 24 de E-1007 | se invoca | se envía primero el aviso de retraso con POL-DELAY-2026-03 y luego el de puerta sin referencia de política |

**Acceptance Criteria**:

- [ ] Máximo dos notificaciones por evaluación, cada una con resultado propio.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, idempotency_key, attempt, status, notification_id, not_sent_reason, deduplicated, attempts | Aviso al pasajero enviado solo por el sistema, con plantilla fija, una por motivo. |

**Business Process (BPM)**:

```
Notificar retraso → Notificar puerta
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.69 SF-11.5 Registro de auditoría

**Spec fuente**: [SF-11.5 Registro de auditoría](69-sf-11-5-registro-de-auditoria.md)  
**Requisitos**: FR-090, FR-091, FR-093, FR-123  
**Pruebas (TC)**: TC-43, TC-44, TC-59

Persiste el llamante, la revisión manual y el estado de cada notificación sin información personal ni texto del mensaje.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una evaluación del sistema | se registra | queda el llamante, la revisión manual y el estado por motivo, sin texto del mensaje |
| 2 | una evaluación del sistema de ABC123 con la notificación NT-9912 en cola y otra fallida | se registra | quedan el llamante, la revisión manual y los 2 estados, sin texto del mensaje |

**Acceptance Criteria**:

- [ ] El 100 % de las evaluaciones del sistema registra su llamante.
- [ ] La lectura del registro por la sesión del pasajero nunca devuelve la revisión manual ni el detalle de las notificaciones.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Reunir estados → Persistir
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.70 SF-11.6 Respuesta sin información personal

**Spec fuente**: [SF-11.6 Respuesta sin información personal](70-sf-11-6-respuesta-sin-informacion-personal.md)  
**Requisitos**: FR-120, FR-124, NFR-002  
**Pruebas (TC)**: TC-50

Devuelve el resultado mínimo: identificador de decisión, estado, motivo, notificaciones y revisión manual; sin vista ni datos del pasajero, y sin guardarla para el front.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | evaluación del sistema | se responde | sin vista, sin opciones y sin datos personales |
| 2 | el pasajero entra después | consulta | el modo pasajero vuelve a evaluar de cero |
| 3 | ABC123 evaluada con la clave de servicio válida | se responde | contiene 5 campos y ningún dato de Ana ni del niño |

**Acceptance Criteria**:

- [ ] Cero datos personales en el 100 % de las respuestas.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de evaluación del sistema | decision_id, decision_state, reason, notifications, needs_manual_review | Respuesta mínima y sin información personal para otro sistema. |

**Business Process (BPM)**:

```
Armar resultado mínimo → Responder
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.71 F-12 Carga y validación de la configuración

**Spec fuente**: [F-12 Carga y validación de la configuración](71-f-12-carga-y-validacion-de-la-configuracion.md)  
**Requisitos**: NFR-012, NFR-005, NFR-003, NFR-007, FR-005, FR-016, FR-017, FR-022, FR-030, FR-039, FR-054, FR-064, FR-067, FR-068, FR-085, FR-092, FR-120, FR-123, NFR-013  
**Pruebas (TC)**: TC-49, TC-57, TC-58

Al arrancar construye la configuración desde los valores por defecto documentados, la sobrescribe con variables de entorno (los secretos solo por entorno), valida cada parámetro y la entrega por inyección; un valor inválido o un secreto obligatorio ausente impide el arranque.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | no hay variable de entorno | se arranca | rigen los valores por defecto documentados |
| 2 | `RELEVANT_DELAY_MIN_MINUTES` = 20 por entorno | se evalúa un retraso de 10 minutos | no hay alerta |
| 3 | un parámetro tiene un valor fuera de rango | se arranca | el servicio no arranca y el error nombra el parámetro, nunca el valor de un secreto |
| 4 | falta `IDEMPOTENCY_SECRET` | se arranca | el servicio no arranca |
| 5 | falta `SERVICE_API_KEY` | se arranca | arranca con el modo sistema apagado |
| 6 | `OPERATION_INDETERMINATE_EXPIRY_SECONDS` y `EVALUATE_RATE_LIMIT_PER_MINUTE` con sus valores por defecto (900 y 30) | se cambia cada uno | cambian el vencimiento de una operación indeterminada y el límite de tasa de la evaluación |
| 7 | los parámetros operativos de `EXTERNAL_CONTRACTS.md` §2.4 (tiempos de espera, reintentos de lectura, modo de reloj, origen permitido, ubicación del registro, banderas de desarrollo) | se cambian | cada uno tiene valor por defecto, sobrescritura por entorno y validación al arrancar, igual que los de los supuestos S-09 a S-19 |
| 8 | `RELEVANT_DELAY_MIN_MINUTES` en 20 por entorno | se evalúa un retraso de 10 min | no hay alerta; con el valor por defecto 1 sí |
| 9 | `DEV_SESSION_HEADER_ENABLED` y `DEV_ENDPOINTS_ENABLED` en falso por defecto, `CLOCK_MODE` en system, `CORS_ALLOWED_ORIGINS` con el origen del front de prueba y `DB_PATH` con un archivo escribible | se cambia cada uno por entorno | las funciones de desarrollo se habilitan, el reloj pasa a modo escenario, un origen distinto queda rechazado y el registro se escribe en la ruta nueva; un `CLOCK_MODE` inválido o un `DB_PATH` no escribible impide arrancar |
| 10 | `UPSTREAM_READ_TIMEOUT_MS` de 2000, `UPSTREAM_WRITE_TIMEOUT_MS` de 5000, `READ_MAX_REQUERIES` de 1 y `WRITE_RETRY_BACKOFF_MS` de 200 | se cambian por entorno | cambian el tiempo de espera de cada lectura y escritura, las re-consultas de una lectura fallida y la pausa de 200 ms entre reintentos (400 ms el segundo); un valor por debajo de 100 ms impide arrancar |
| 11 | `ASSERTION_COMPATIBILITY` con «retrasado», «a tiempo» y «horario programado» incompatibles entre sí | se quita «a tiempo» de la tabla | un empate entre E-1001 (160 min) y un estado «a tiempo» deja de ser conflicto; una entrada con una afirmación fuera del conjunto cerrado impide arrancar |

**Acceptance Criteria**:

- [ ] El 100 % de los parámetros de la tabla de configuración (incluidos los operativos y los dos nuevos) tiene una prueba que cambia su valor y verifica el efecto.
- [ ] El 100 % de los valores inválidos impide el arranque nombrando el parámetro.
- [ ] Ningún parámetro de los supuestos S-09 a S-19 aparece fijado en la lógica de negocio.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Leer valores por defecto → Sobrescribir por entorno → Validar → Fallar o entregar configuración
```

Subprocess detail (if applicable):

```
SF-12.1: Lectura de los valores por defecto
SF-12.2: Sobrescritura por entorno
SF-12.3: Validación
SF-12.4: Fallo de arranque
SF-12.5: Inyección
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.72 SF-12.1 Lectura de los valores por defecto

**Spec fuente**: [SF-12.1 Lectura de los valores por defecto](72-sf-12-1-lectura-de-los-valores-por-defecto.md)  
**Requisitos**: FR-005, FR-016, FR-017, NFR-012  
**Pruebas (TC)**: TC-49

Carga el archivo de valores por defecto con el valor documentado de cada parámetro.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | sin variables de entorno | se leen | cada parámetro tiene su valor documentado (por ejemplo `RELEVANT_DELAY_MIN_MINUTES` = 1) |
| 2 | sin variables de entorno | se arranca | `RELEVANT_DELAY_MIN_MINUTES` es 1, `MCT_UNCERTAINTY_MINUTES` es 45 y `AUDIT_RETENTION_DAYS` es 30 |
| 3 | sin variables de entorno | se leen los valores por defecto operativos | `UPSTREAM_READ_TIMEOUT_MS` es 2000, `UPSTREAM_WRITE_TIMEOUT_MS` es 5000, `READ_MAX_REQUERIES` es 1, `WRITE_RETRY_BACKOFF_MS` es 200, `DEV_SESSION_HEADER_ENABLED` y `DEV_ENDPOINTS_ENABLED` son falso, `CLOCK_MODE` es system, `CORS_ALLOWED_ORIGINS` es el origen del front de prueba y `DB_PATH` apunta al registro local |

**Acceptance Criteria**:

- [ ] Todo parámetro del contrato de configuración tiene valor por defecto documentado.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Abrir archivo → Interpretar valores
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.73 SF-12.2 Sobrescritura por entorno

**Spec fuente**: [SF-12.2 Sobrescritura por entorno](73-sf-12-2-sobrescritura-por-entorno.md)  
**Requisitos**: FR-085, FR-120, NFR-012, NFR-003  
**Pruebas (TC)**: TC-49

Aplica las variables de entorno con prioridad; los secretos solo se leen del entorno.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una variable de entorno con el nombre del parámetro | se arranca | su valor reemplaza al del archivo |
| 2 | el secreto está en el archivo y no en el entorno | se arranca | no se usa: los secretos solo se leen del entorno |
| 3 | el archivo con `OPERATION_STALE_SECONDS` de 120 y el entorno con 300, y un secreto escrito en el archivo | se arranca | rige 300 y el secreto del archivo no se usa |
| 4 | `DEV_ENDPOINTS_ENABLED` en verdadero y `DB_PATH` con otra ruta en el entorno y los valores por defecto en el archivo | se arranca | rigen los valores del entorno y `CORS_ALLOWED_ORIGINS` conserva su valor por defecto |

**Acceptance Criteria**:

- [ ] Todo parámetro es sobrescribible por entorno excepto los secretos, que solo existen por entorno.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Leer entorno → Aplicar prioridad
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.74 SF-12.3 Validación

**Spec fuente**: [SF-12.3 Validación](74-sf-12-3-validacion.md)  
**Requisitos**: FR-030, FR-039, FR-067, NFR-012  
**Pruebas (TC)**: TC-49

Valida tipo, rango, lista no vacía y longitud mínima de cada parámetro.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | `REBOOK_MAX_RETRIES` = 9 | se valida | se rechaza (rango entre 0 y 5) |
| 2 | `REMEDY_RIGHTS` vacía | se valida | se rechaza |
| 3 | `REBOOK_MAX_RETRIES` en 9 (rango de 0 a 5) y `OPERATION_INDETERMINATE_EXPIRY_SECONDS` en 100 con `OPERATION_STALE_SECONDS` de 120 | se valida | ambos se rechazan nombrando el parámetro |
| 4 | `UPSTREAM_WRITE_TIMEOUT_MS` en 50 (mínimo 100), `READ_MAX_REQUERIES` en 5 (rango de 0 a 3) y `CLOCK_MODE` en wall | se valida | los 3 se rechazan nombrando el parámetro |

**Acceptance Criteria**:

- [ ] El 100 % de los valores inválidos probados es rechazado.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Validar tipo → Validar rango y listas → Validar longitud de secretos
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.75 SF-12.4 Fallo de arranque

**Spec fuente**: [SF-12.4 Fallo de arranque](75-sf-12-4-fallo-de-arranque.md)  
**Requisitos**: NFR-012, FR-120  
**Pruebas (TC)**: TC-49

Un valor inválido o la ausencia del secreto de idempotencia impide el arranque con un error que nombra el parámetro; sin credencial de servicio el modo sistema queda apagado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | un valor fuera de rango | se arranca | el error nombra el parámetro |
| 2 | falta la credencial de servicio | se arranca | arranca y el modo sistema responde rechazo |
| 3 | `IDEMPOTENCY_SECRET` de 8 caracteres cuando el mínimo es 16, o ausente | se arranca | el servicio no arranca y el error nombra el parámetro sin mostrar valores |
| 4 | `ASSERTION_COMPATIBILITY` mal formada y `DEV_SESSION_HEADER_ENABLED` con un valor no booleano | se arranca | el servicio no arranca y el error nombra el parámetro defectuoso |

**Acceptance Criteria**:

- [ ] Todo error de arranque nombra el parámetro y ninguno revela un secreto.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Detectar error → Nombrar parámetro → Detener arranque
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.76 SF-12.5 Inyección

**Spec fuente**: [SF-12.5 Inyección](76-sf-12-5-inyeccion.md)  
**Requisitos**: FR-022, FR-054, FR-064, FR-092, NFR-012, NFR-007  
**Pruebas (TC)**: TC-49

Entrega los valores a los casos de uso y al dominio por inyección; el dominio no lee el entorno.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | una configuración con un valor cambiado | se construye el dominio | su comportamiento cambia sin tocar el código |
| 2 | el dominio construido con `MCT_UNCERTAINTY_MINUTES` en 45 y otro en 0 | se evalúa un margen de 10 min | con 45 es desconocido y con 0 es falso |

**Acceptance Criteria**:

- [ ] Ningún literal de los parámetros aparece en la lógica de negocio.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |

**Business Process (BPM)**:

```
Construir configuración → Entregar al dominio
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.77 FE-01 Selector de escenario y reloj (solo desarrollo)

**Spec fuente**: [FE-01 Selector de escenario y reloj (solo desarrollo)](77-fe-01-selector-de-escenario-y-reloj-solo-desarrollo.md)  
**Requisitos**: FR-001, FR-101, FR-111, NFR-011, NFR-012, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01, TC-08, TC-27

En el front de prueba y solo en desarrollo: lista los escenarios visibles, activa el elegido, fija la sesión simulada, recarga la vista y ofrece «Avanzar reloj» para demostrar la vigencia. No aparece en la versión de producción.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el selector muestra los escenarios visibles | el evaluador elige uno | se activa, se fija la sesión simulada de su reserva y la vista se recarga |
| 2 | hay un escenario activo | el evaluador pulsa «Avanzar reloj» | el reloj avanza y la cuenta regresiva de la hora límite llega a cero |
| 3 | versión de producción | se abre la aplicación | el selector no existe |
| 4 | el selector con los escenarios visibles | el evaluador elige BASE_TC01 y pulsa «Avanzar reloj» una vez de 120 s | ve la vista del caso base con «Quedan 01:48 (hasta 11:04 UTC)» y luego la hora límite vencida |

**Acceptance Criteria**:

- [ ] El evaluador activa cualquier escenario visible en 2 clics o menos.
- [ ] El 100 % de los escenarios visibles recarga la vista con el escenario elegido.
- [ ] El selector no existe en la versión de producción.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |
| Reloj de escenario | mode, now, offset_seconds, advance_seconds | Reloj controlado de desarrollo: instante base del escenario más un desplazamiento que solo avanza a pedido. |
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Cargar catálogo → Activar escenario → Fijar sesión simulada → Recargar vista → Avanzar reloj
```

Subprocess detail (if applicable):

```
FE-01.1: Carga del catálogo
FE-01.2: Activación del escenario
FE-01.3: Fijación de la sesión simulada
FE-01.4: Avance del reloj de escenario
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.78 FE-01.1 Carga del catálogo

**Spec fuente**: [FE-01.1 Carga del catálogo](78-fe-01-1-carga-del-catalogo.md)  
**Requisitos**: FR-101, FR-111, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01

Al abrir la aplicación pide la lista de escenarios y muestra solo los visibles.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el catálogo responde | se abre la aplicación | aparecen solo los escenarios visibles con su título |
| 2 | el catálogo llega con 0 escenarios, o no responde | se abre la aplicación | con 0 escenarios se lee «No hay escenarios disponibles.»; si no responde, «No pudimos cargar los escenarios.» sin bloquear la vista; mientras carga, «Cargando escenarios…» |
| 3 | el catálogo con BASE_TC01, SIN_ANOMALIA y variantes de prueba | se abre la aplicación | aparecen solo los 2 visibles con su título |

**Acceptance Criteria**:

- [ ] La lista contiene solo escenarios visibles en el 100 % de los casos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Pedir catálogo → Mostrar visibles
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.79 FE-01.2 Activación del escenario

**Spec fuente**: [FE-01.2 Activación del escenario](79-fe-01-2-activacion-del-escenario.md)  
**Requisitos**: FR-101, FR-111, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01

Al elegir un escenario lo activa en el servicio de desarrollo y espera su confirmación.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el evaluador elige otro escenario | se confirma la activación | se continúa con la sesión simulada |
| 2 | BASE_TC01 activo y un escenario que ya no existe en el catálogo | se elige ese escenario | se lee «El escenario ya no existe. Elige otro.» y se conserva BASE_TC01; mientras activa se lee «Activando escenario…» con la lista deshabilitada |
| 3 | BASE_TC01 activo | se elige SIN_MENOR_TC07 | se activa y la vista muestra dos pasajeros adultos |

**Acceptance Criteria**:

- [ ] El 100 % de las activaciones fallidas conserva el escenario anterior.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. |

**Business Process (BPM)**:

```
Enviar elección → Confirmar activación
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.80 FE-01.3 Fijación de la sesión simulada

**Spec fuente**: [FE-01.3 Fijación de la sesión simulada](80-fe-01-3-fijacion-de-la-sesion-simulada.md)  
**Requisitos**: FR-001, FR-111, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-21

Fija la sesión simulada con la reserva del escenario elegido para las siguientes llamadas.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | un escenario activado | se fija la sesión | las llamadas siguientes usan su reserva |
| 2 | `DEV_SESSION_HEADER_ENABLED` apagado en el servicio | se fija la sesión de ABC123 | se lee «No se pudo iniciar la sesión de prueba.» con «Reintentar» y rol de alerta |
| 3 | el escenario OTRA_RESERVA_TC21 con reserva XYZ789 | se elige | las llamadas siguientes usan XYZ789 y no ABC123 |

**Acceptance Criteria**:

- [ ] Cada escenario usa exclusivamente su propia reserva.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | Identidad con la que se pide una evaluación: sesión del pasajero o credencial de servicio. |

**Business Process (BPM)**:

```
Tomar reserva del escenario → Fijar sesión
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.81 FE-01.4 Avance del reloj de escenario

**Spec fuente**: [FE-01.4 Avance del reloj de escenario](81-fe-01-4-avance-del-reloj-de-escenario.md)  
**Requisitos**: FR-071, FR-111, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-08, TC-27

Ofrece «Avanzar reloj» para sumar tiempo al reloj de escenario y recargar la vista.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | hay cuenta regresiva | se pulsa «Avanzar reloj» | el reloj avanza y la vista se recarga con la hora límite vencida |
| 2 | el reloj no está en modo escenario | se pulsa «Avanzar reloj» | el botón queda con `aria-disabled` y fuera de él se lee «Avanzar reloj no está disponible en este modo.» |
| 3 | el reloj en 11:02:35Z | se pulsa «Avanzar reloj» | el reloj marca 11:04:35Z y la hora límite se ve vencida |

**Acceptance Criteria**:

- [ ] Tras avanzar 120 segundos la cuenta regresiva del escenario base muestra la hora límite vencida.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Reloj de escenario | mode, now, offset_seconds, advance_seconds | Reloj controlado de desarrollo: instante base del escenario más un desplazamiento que solo avanza a pedido. |

**Business Process (BPM)**:

```
Pedir avance → Recargar vista
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.82 FE-02 Vista de viaje

**Spec fuente**: [FE-02 Vista de viaje](82-fe-02-vista-de-viaje.md)  
**Requisitos**: FR-003, FR-004, FR-007, FR-008, FR-014, FR-023, FR-039, FR-043, FR-046, FR-047, FR-056, FR-058, FR-066, FR-071, FR-041, FR-111, FR-112, FR-113, NFR-011, NFR-004, NFR-013, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01, TC-02, TC-03, TC-09, TC-12, TC-30, TC-45, TC-51, TC-54, TC-58, TC-60

Pantalla principal para el pasajero: pide la evaluación con el modo pasajero y pinta, según el estado, la carga, la vista sin anomalía, la informativa, el retraso con opción propuesta, el conflicto de fuentes, la ausencia de opción viable, la solicitud registrada, la lectura fallida y el error de carga, con el cambio de puerta siempre destacado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la evaluación trae retraso, reglas, una opción propuesta y acciones | se pinta la vista | se ve el resumen del viaje, las alertas, las reglas plegadas con «Se cumplen X de Y reglas», la opción propuesta, la vía «Si prefieres no viajar», la hora límite con cuenta regresiva y una sola acción primaria |
| 2 | la evaluación no trae anomalía | se pinta | solo el contexto del viaje con «Estado del vuelo» de cada segmento, sin alertas, reglas, opciones ni botones de acción, y el botón secundario «Actualizar» |
| 3 | retraso sin política rota | se pinta | alerta informativa del retraso con «Con la información actual, este retraso no da lugar a acciones disponibles para ti. Vuelve a consultar tu viaje más tarde.», la estimación rotulada, las reglas plegadas con «Se cumplen 1 de 5 reglas», la aclaración «Cumplir una regla no siempre da lugar a una acción.», «Actualizar» y sin opciones ni soporte |
| 4 | el único evento es un cambio de puerta | se pinta | cada segmento muestra «Estado del vuelo: Horario programado» sin ícono de estado, la puerta 24 aparte («Puerta 24 (informada a las 10:55 UTC)»), la alerta destacada de puerta, el texto «Con la información actual no hay acciones disponibles para ti. Vuelve a consultar tu viaje más tarde.» y «Actualizar» |
| 5 | el contexto no pudo cargarse | se pinta | «No pudimos cargar tu viaje», «Ocurrió un problema al consultar tu reserva. Inténtalo de nuevo en unos segundos.» y «Reintentar», sin soporte |
| 6 | SIN_OPCION_TC09: dos pasajeros adultos (R5 falsa), reglas «Se cumplen 1 de 5 reglas» y solo O2 LA2450 con 1 asiento | se pinta | se ven las reglas plegadas, el aviso «No encontramos una opción que cubra a todo tu grupo» con «Las opciones disponibles no tienen asientos para los 2 pasajeros juntos, y no ofrecemos separar al grupo. Una persona puede ayudarte con otras alternativas.», «Una persona revisará tu caso. Esto no cambia tu reserva.» y «Hablar con una persona» de un clic; no se muestra ninguna opción no viable |
| 7 | BASE_TC01 con O1 LA2412 el 16 sep a las 08:15, un día después de la nueva llegada | se pinta | además de la tarjeta de la opción aparece la alerta de pernocte, última de las alertas: «Posible asistencia por pernocte» y «Tu nueva salida es al día siguiente: podrías tener derecho a asistencia; un agente lo confirmará.», sin cifras |
| 8 | BASE_TC01 con una alerta crítica de conflicto en otro viaje, retraso de 160 min, puerta 24, conexión en riesgo y pernocte, y GATE_SOLO_TC51 sin retraso | se pintan | el orden es críticas, retraso, puerta (justo tras el retraso), conexión y pernocte; sin retraso la puerta va primero |
| 9 | BASE_TC01 con un niño en el grupo y la vía de reembolso (O3 sin respaldo recuperado) | se pinta | el aviso «Tu grupo incluye a un menor: esta decisión necesita la aprobación de una persona.» queda pegado al botón de acción y la vía de reembolso es un bloque con título «Si prefieres no viajar» y «Si prefieres no viajar, una persona puede revisar contigo las alternativas.» sin monto ni plazo |
| 10 | BASE_TC01 con retraso de 160 min en LA500, puerta 24 informada a las 10:55 UTC y la opción O1 LA2412 | se pinta la vista | se ven, en orden, el retraso, la puerta 24, la conexión «Estimación», las reglas plegadas «Se cumplen 2 de 5 reglas», O1 «Propuesta» y la acción primaria única |

**Acceptance Criteria**:

- [ ] El pasajero identifica el estado de su viaje y la acción principal en menos de 10 segundos en las pantallas de prueba.
- [ ] El 100 % del texto visible sale del catálogo.
- [ ] El 100 % de los pares de color de texto y fondo cumple contraste 4,5:1.
- [ ] Ninguna pantalla muestra campos de la lista prohibida.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, load_status, data_as_of, segments, alerts, derived_variables, policy, options, proposed_option_id, refund_notice, offer_deadline, actions, messages, operations, human_cases | Respuesta completa para el pasajero; solo contiene campos de la lista blanca. |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, blocked | Texto de plantilla con su evidencia, aprobado por el validador antes de mostrarse o enviarse. |

**Business Process (BPM)**:

```
Cargar vista → Pintar por estado → Mostrar hora límite → Permitir reintento y actualización
```

Subprocess detail (if applicable):

```
FE-02.1: Carga y mensaje de lentitud
FE-02.2: Pintado por estado
FE-02.3: Hora límite en UTC y cuenta regresiva
FE-02.4: Error de carga con reintento
FE-02.5: Catálogo de textos y lista blanca de campos
FE-02.6: Botón «Actualizar»
FE-02.7: Destino del foco
FE-02.8: Cambio de puerta destacado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.83 FE-02.1 Carga y mensaje de lentitud

**Spec fuente**: [FE-02.1 Carga y mensaje de lentitud](83-fe-02-1-carga-y-mensaje-de-lentitud.md)  
**Requisitos**: FR-111, FR-113, NFR-011, NFR-004, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01

Pide la evaluación al abrir la pantalla; muestra un esqueleto y, pasado 1,5 s, un aviso de lentitud.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la respuesta llega en menos de 1,5 s | se abre la pantalla | se ve el esqueleto y luego la vista, sin aviso |
| 2 | la respuesta tarda más de 1,5 s | se abre la pantalla | aparece el aviso «Esto está tardando más de lo habitual. Seguimos consultando tu viaje.» |
| 3 | BASE_TC01: la evaluación del caso base tarda 2 s | se abre la pantalla | a 1,5 s aparece el aviso de lentitud y a 2 s la vista del caso base |

**Acceptance Criteria**:

- [ ] El aviso de lentitud aparece a partir de 1,5 s y no antes.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Pedir evaluación → Mostrar esqueleto → Mostrar aviso de lentitud
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.84 FE-02.2 Pintado por estado

**Spec fuente**: [FE-02.2 Pintado por estado](84-fe-02-2-pintado-por-estado.md)  
**Requisitos**: FR-003, FR-004, FR-007, FR-008, FR-014, FR-023, FR-039, FR-041, FR-043, FR-046, FR-047, FR-056, FR-058, FR-066, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-02, TC-03, TC-06, TC-09, TC-12, TC-30, TC-45, TC-54, TC-60

Elige qué componentes pintar según el estado de la vista: sin anomalía, informativa, retraso con opción, conflicto, sin opción viable, solicitud registrada y lectura fallida.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | un segmento sin eventos | se pinta | muestra «Horario programado» sin ícono de estado; «Sin información verificada» solo aparece con evidencia degradada |
| 2 | conflicto de fuentes | se pinta | aviso crítico, sin reglas y con botón de caso humano de un clic |
| 3 | conexión estimada | se pinta | aviso «Tu conexión podría perderse (Estimación)» con «Es una estimación del sistema, sujeta al tiempo mínimo de conexión, que no tenemos. No es un hecho confirmado.», rotulado «Estimación» y nunca en color de éxito |
| 4 | la conexión perdida es desconocida con política rota | se pinta | sin opciones, con el estado de decisión bloqueada explicado con lenguaje neutro y el botón «Hablar con una persona» de un clic |
| 5 | CONEXION_FALSA_TC06B con retraso de 10 min y margen de 60 min | se pinta | aviso informativo «Estimación de tu conexión»: «No detectamos que pierdas la conexión. Es una estimación, sujeta al tiempo mínimo de conexión; no es una garantía.» y nunca «tu conexión está segura» |
| 6 | BASE_TC01 con O3 sin respaldo recuperado | se pinta | el bloque tiene un título de sección «Si prefieres no viajar» y el texto «Si prefieres no viajar, una persona puede revisar contigo las alternativas.», sin monto ni plazo ni afirmación de derecho |
| 7 | SIN_OPCION_TC09 con 2 pasajeros adultos y solo O2 con 1 asiento | se pinta | mensaje de grupo no cubierto, sin opciones no viables y con el botón «Hablar con una persona» de un clic |
| 8 | S2 LA2410 sin eventos y S1 LA500 en conflicto de fuentes | se pinta | S2 muestra «Horario programado» sin ícono y S1 «En revisión» con aviso crítico y caso humano de un clic |
| 9 | el caso base ABC123: LA500 llega a las 17:55, LA2410 sale a las 19:05 y el retraso es de 160 min | se pinta | la fila de LA500 muestra «Retrasado 160 min», «Nueva salida 17:10» y «Nueva llegada (Estimación): 20:35»; la alerta de conexión dice «Estimamos que no alcanzarías tu vuelo LA2410 (LIM → MEX)» (margen 19:05 − 20:35 = −90 min); se cumplen 2 de 5 reglas (R3 y R5) y la acción es «Aceptar y enviar a una persona» por PENDIENTE_APROBACION |

**Acceptance Criteria**:

- [ ] Cada uno de los diez estados del DESIGN_CONTRACT produce los componentes indicados en su tabla.
- [ ] Cero apariciones de «tu conexión está segura» o «llegarás a tiempo».

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, load_status, data_as_of, segments, alerts, derived_variables, policy, options, proposed_option_id, refund_notice, offer_deadline, actions, messages, operations, human_cases | Respuesta completa para el pasajero; solo contiene campos de la lista blanca. |

**Business Process (BPM)**:

```
Leer estado de la vista → Elegir componentes → Pintar textos del catálogo
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.85 FE-02.3 Hora límite en UTC y cuenta regresiva

**Spec fuente**: [FE-02.3 Hora límite en UTC y cuenta regresiva](85-fe-02-3-hora-limite-en-utc-y-cuenta-regresiva.md)  
**Requisitos**: FR-071, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-08, TC-27

Dentro de la barra de acciones muestra «Quedan mm:ss (hasta HH:MM UTC)» calculada contra la hora de generación; al llegar a cero reemplaza el texto y el botón sigue activo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la oferta vence a las 11:04:35Z (11:02:35Z más 120 s) y la vista se generó a las 11:02:47Z | se pinta | junto al botón primario se lee «Quedan 01:48 (hasta 11:04 UTC)» (hora truncada al minuto hacia abajo) y debajo «Pasada esa hora, la opción queda sujeta a disponibilidad.» |
| 2 | el contador llega a cero | se pinta | el contador se reemplaza por completo por «La hora límite pasó: la opción está sujeta a disponibilidad.» (sin «Quedan 00:00») y el botón sigue activo |
| 3 | oferta hasta 11:04:35Z (11:02:35Z más una vigencia de 120 s) y generación a las 11:02:47Z; la vigencia vence a los 120 s | se pinta | muestra «Quedan 01:48 (hasta 11:04 UTC)» con la hora truncada al minuto |

**Acceptance Criteria**:

- [ ] La cuenta regresiva coincide con la hora límite menos la hora de generación en el 100 % de los casos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Leer hora límite → Calcular restante → Reemplazar texto al llegar a cero
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.86 FE-02.4 Error de carga con reintento

**Spec fuente**: [FE-02.4 Error de carga con reintento](86-fe-02-4-error-de-carga-con-reintento.md)  
**Requisitos**: FR-066, FR-086, FR-105, FR-111, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-33, TC-39

Si no se puede cargar el viaje, muestra «No pudimos cargar tu viaje» con «Reintentar» y sin soporte.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el servicio responde contexto no disponible | se pinta | «No pudimos cargar tu viaje» con «Ocurrió un problema al consultar tu reserva. Inténtalo de nuevo en unos segundos.» y «Reintentar», sin soporte y sin «Actualizar» |
| 2 | la lectura es inválida | se pinta | «Reserva ABC123», «No hay tramos para mostrar.», «No pudimos validar los datos de tu reserva.» «Inténtalo de nuevo en unos segundos.» y «Reintentar», sin saludo, sin pasajeros y sin soporte |
| 3 | el contexto de ABC123 falla dos veces | se pinta | muestra el error con «Reintentar» y sin soporte |

**Acceptance Criteria**:

- [ ] En el 100 % de los errores de carga existe «Reintentar» y ninguno ofrece soporte.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Detectar error → Mostrar aviso → Reintentar
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.87 FE-02.5 Catálogo de textos y lista blanca de campos

**Spec fuente**: [FE-02.5 Catálogo de textos y lista blanca de campos](87-fe-02-5-catalogo-de-textos-y-lista-blanca-de-campos.md)  
**Requisitos**: FR-112, FR-113, NFR-002, NFR-013, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01, TC-58

Todo texto visible sale del catálogo en español neutro, y solo se pintan los campos de la lista blanca.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | todos los componentes | se recorren | no hay ninguna cadena visible fuera del catálogo |
| 2 | se renderiza el escenario base | se busca | no aparecen correo, teléfono, documento, edad, apellido ni nombre completo |
| 3 | una condición de regla, un derecho o una puerta con marcado HTML | se pinta | el marcado se ve literal y no se interpreta |
| 4 | BASE_TC01 con el nombre de pila Ana | se recorren los 10 componentes | no hay cadenas fuera del catálogo y ningún dato de la lista prohibida |

**Acceptance Criteria**:

- [ ] Cero cadenas visibles fuera del catálogo.
- [ ] Cero datos de la lista prohibida en pantalla.
- [ ] Ningún texto del proveedor se interpreta como marcado HTML.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Recorrer componentes → Verificar catálogo → Verificar lista blanca
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.88 FE-02.6 Botón «Actualizar»

**Spec fuente**: [FE-02.6 Botón «Actualizar»](88-fe-02-6-boton-actualizar.md)  
**Requisitos**: FR-002, FR-050, FR-111, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-45, TC-51

En las vistas sin acción primaria ofrece «Actualizar», con «Información de las HH:MM UTC», que relee la vista y no es una acción externa.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | INFORMATIVA_TC45 con retraso de 5 min a las 11:02 UTC, una de las tres pantallas de la lista cerrada (sin anomalía, informativa o solo puerta) | el pasajero pulsa «Actualizar» | se muestra el botón secundario «Actualizar» con «Información de las 11:02 UTC» y sin botones de acción; al pulsarlo se vuelve a pedir la evaluación y se actualiza la hora de la información, sin consentimiento ni escritura externa |
| 2 | las pantallas de solicitud registrada, de error de carga y de lectura inválida PARCIAL_BLOQUEANTE_TC12 | se pintan | no hay botón «Actualizar»: la pantalla de solicitud registrada solo tiene sus acciones y las otras dos tienen «Reintentar» |

**Acceptance Criteria**:

- [ ] Pulsar «Actualizar» nunca provoca una escritura externa.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Pulsar actualizar → Releer vista → Mostrar hora de la información
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.89 FE-02.7 Destino del foco

**Spec fuente**: [FE-02.7 Destino del foco](89-fe-02-7-destino-del-foco.md)  
**Requisitos**: NFR-011, FR-111, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01

Tras «Reintentar», «Actualizar» y un cambio de estado, el foco va a un destino definido y se anuncia la actualización.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el pasajero reintenta | se recarga | el foco pasa al título «Tu viaje» y una región anuncia «Información actualizada a las HH:MM UTC» |
| 2 | la situación cambió al aceptar | se recarga | el foco pasa a un aviso informativo al inicio |
| 3 | la vista del caso base con el selector de escenario en el encabezado índigo | se navega con el teclado desde el inicio | el primer foco es el enlace «Saltar al contenido» y el anillo de foco dentro del encabezado es blanco, en el resto es índigo de 3 px |
| 4 | BASE_TC01 con el panel de reglas plegado con «Ver reglas» y «Se cumplen 2 de 5 reglas» | se activa con Intro o Espacio | el botón expone `aria-expanded` verdadero, cambia a «Ocultar reglas» y el panel se despliega |
| 5 | el contexto falla otra vez tras pulsar «Reintentar» | termina la recarga | el foco pasa al aviso de error, que se anuncia con rol de alerta, y «Reintentar» sigue disponible |
| 6 | INFORMATIVA_TC45 y la relectura funciona a las 11:02 UTC | se pulsa «Actualizar» | el foco pasa al título «Tu viaje» y se anuncia «Información actualizada a las 11:02 UTC» |
| 7 | el contexto falló y la recarga funciona | se pulsa «Reintentar» | el foco pasa a «Tu viaje» y se anuncia «Información actualizada a las 11:02 UTC» |

**Acceptance Criteria**:

- [ ] El 100 % de los recorridos con teclado alcanza todas las acciones.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Detectar recarga → Mover foco → Anunciar actualización
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.90 FE-02.8 Cambio de puerta destacado

**Spec fuente**: [FE-02.8 Cambio de puerta destacado](90-fe-02-8-cambio-de-puerta-destacado.md)  
**Requisitos**: FR-004, FR-006, FR-068, FR-111, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-51, TC-52

Muestra siempre el cambio de puerta validado con una alerta destacada, su hora de información y la nota de confirmar en el aeropuerto, aunque no haya retraso.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | solo hay un cambio de puerta validado | se pinta | alerta destacada con título en negrita, borde izquierdo de marca, ícono de puerta, la puerta nueva y «Puerta informada a las HH:MM UTC» |
| 2 | hay retraso y cambio de puerta | se pinta | la alerta de puerta va justo después de la del retraso |
| 3 | GATE_SOLO_TC51 con E-1007 puerta 24 informada a las 10:55 UTC | se pinta | alerta «Cambio de puerta en tu vuelo LA500 (SCL → LIM)» con «Puerta informada a las 10:55 UTC» |

**Acceptance Criteria**:

- [ ] El cambio de puerta aparece en el 100 % de las vistas con un cambio validado y en el 0 % de los demás casos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Estado resuelto del segmento | segment_id, state, affected, delay_minutes, gate, gate_recorded_at, information_as_of, discarded_events | Resultado de validar los eventos de un segmento: qué se afirma de su salida y de su puerta. |

**Business Process (BPM)**:

```
Leer puerta validada → Pintar alerta destacada → Ordenar tras el retraso
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.91 FE-03 Aceptar opción (front)

**Spec fuente**: [FE-03 Aceptar opción (front)](91-fe-03-aceptar-opcion-front.md)  
**Requisitos**: FR-050, FR-051, FR-052, FR-054, FR-055, FR-056, FR-062, FR-070, FR-105, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-07, TC-14, TC-15, TC-22, TC-30, TC-31

El clic en el botón primario de la opción: se deshabilita mientras hay solicitud en curso, envía la decisión, la clave de itinerario y la huella (nunca el contenido de la opción) y pinta cada uno de los siete resultados.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | decisión automática | el pasajero pulsa «Aceptar esta opción» | el botón queda deshabilitado con «Procesando tu solicitud…» y luego se ve «Solicitud registrada, pendiente de confirmación, sujeta a disponibilidad» con el vencimiento y «Tu vuelo todavía no se cambia.» |
| 2 | decisión que exige aprobación | pulsa «Aceptar y enviar a una persona» | se ve el caso creado y que la reserva no cambió |
| 3 | el servidor responde estado cambiado | se recibe | se muestra la vista nueva y el foco va al aviso informativo |
| 4 | SIN_MENOR_TC07 con O1 LA2412 de 4 asientos | se pulsa «Aceptar esta opción» | el botón queda en «Procesando tu solicitud…» y luego se ve la solicitud RBK-88231 que vence a las 11:12 UTC |

**Acceptance Criteria**:

- [ ] El 100 % de los clics muestra antes la frase de efecto asociada al botón.
- [ ] El botón permanece deshabilitado durante toda la operación.
- [ ] Los siete resultados se pintan con una redacción aprobada.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |

**Business Process (BPM)**:

```
Leer frase de efecto → Pulsar botón → Esperar resultado → Pintar resultado
```

Subprocess detail (if applicable):

```
FE-03.1: Frase de efecto y texto del botón por efecto
FE-03.2: Envío y bloqueo
FE-03.3: Manejo de los siete resultados
FE-03.4: Refresco tras estado cambiado
FE-03.5: Segundo clic tras necesidad de confirmación
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.92 FE-03.1 Frase de efecto y texto del botón por efecto

**Spec fuente**: [FE-03.1 Frase de efecto y texto del botón por efecto](92-fe-03-1-frase-de-efecto-y-texto-del-boton-por-efecto.md)  
**Requisitos**: FR-050, FR-052, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01, TC-07

Cada efecto (crear cambio, caso con opción, caso con motivo conocido) tiene su botón y su frase de efecto antes del botón.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | efecto de crear cambio | se pinta | el botón primario «Aceptar esta opción» va precedido, y asociado a él para los lectores de pantalla, por la frase «Se creará una solicitud de cambio, pendiente de confirmación. Tu vuelo todavía no se cambia. Si no podemos confirmar el resultado, derivaremos tu caso a una persona.» |
| 2 | efecto de caso humano con opción | se pinta | el botón «Aceptar y enviar a una persona» va precedido de «Una persona revisará esta opción. Esto no cambia tu reserva.» y, pegado al botón, el aviso «Tu grupo incluye a un menor: esta decisión necesita la aprobación de una persona.» sin edad ni nombre del menor |
| 3 | CONFLICTO_TC03 con motivo conocido, y BASE_TC01 con el botón secundario | se pinta cada botón | «Hablar con una persona» de un clic va precedido de «Una persona revisará tu caso. Esto no cambia tu reserva.»; el secundario del caso base va precedido de «Se abrirá una solicitud para que una persona te ayude. Esto no cambia tu reserva.» |
| 4 | SIN_MENOR_TC07 con dos pasajeros adultos y O1 LA2412 | se pinta | el botón «Aceptar esta opción» va precedido de su frase de efecto completa |

**Acceptance Criteria**:

- [ ] El 100 % de los botones primarios tiene su frase de efecto asociada.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Elegir efecto → Pintar frase → Pintar botón
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.93 FE-03.2 Envío y bloqueo

**Spec fuente**: [FE-03.2 Envío y bloqueo](93-fe-03-2-envio-y-bloqueo.md)  
**Requisitos**: FR-062, FR-050, FR-065, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-22

Al pulsar, deshabilita el botón y envía la decisión, la clave de itinerario y la huella de la opción.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el botón está procesando | se pulsa otra vez | no se envía nada más |
| 2 | una solicitud en curso para O1 | se pulsa 2 veces en 100 ms | se envía una sola vez |

**Acceptance Criteria**:

- [ ] Cero envíos duplicados por doble clic.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Pulsar → Deshabilitar → Enviar identificadores
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.94 FE-03.3 Manejo de los siete resultados

**Spec fuente**: [FE-03.3 Manejo de los siete resultados](94-fe-03-3-manejo-de-los-siete-resultados.md)  
**Requisitos**: FR-051, FR-052, FR-054, FR-055, FR-056, FR-105, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-01, TC-14, TC-15, TC-30, TC-31, TC-33

Pinta cada resultado: solicitud registrada, solicitud existente, caso humano creado o existente, necesidad de confirmación, estado cambiado y fallo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | SIN_MENOR_TC07: el proveedor responde la solicitud RBK-88231 pendiente de confirmación con vencimiento 11:12:00Z | llega el resultado REBOOKING_CREATED | aviso informativo (no verde) que recibe el foco: «Solicitud registrada, pendiente de confirmación, sujeta a disponibilidad. Vence a las 11:12 UTC. Tu vuelo todavía no se cambia.» y «Código de seguimiento: RBK-88231» |
| 2 | el proveedor responde duplicado con RBK-88231 o ya hay una operación en curso para O1 LA2412 | llega el resultado EXISTING_REQUEST | aviso informativo: «Ya existe una solicitud en curso para esta opción.» y el botón «Aceptar esta opción» sigue con su texto y deshabilitado, con la explicación en un párrafo fuera del botón |
| 3 | BASE_TC01 con decisión PENDIENTE_APROBACION, o 3 llamadas indeterminadas del proveedor de cambios; el proveedor de casos responde HC-4471, cola DISRUPTION_L2, 45 minutos | llega el resultado HUMAN_CASE_CREATED | aviso de éxito con rol de estado: «Registramos tu solicitud. Una persona te atenderá; el tiempo objetivo de atención es de 45 minutos. Código de seguimiento: HC-4471.» y la reserva no cambió |
| 4 | ya existe el caso HC-4471 con la misma clave de deduplicación | llega el resultado EXISTING_CASE | aviso informativo: «Ya registramos una solicitud tuya para esta situación. Código de seguimiento: HC-4471.» sin enviar nada nuevo |
| 5 | el intento anterior del caso HC-4471 quedó indeterminado | llega el resultado NEEDS_CONFIRMATION | diálogo con aviso de advertencia (rol de alerta): «No pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté. Si la envías de nuevo, podría duplicarse.» y los botones «Cerrar» y «Enviar de nuevo igualmente» |
| 6 | los asientos de O1 LA2412 pasaron de 4 a 0 entre la vista y el clic | llega el resultado STATE_CHANGED con la vista nueva | se reemplaza la vista y el foco pasa a un aviso informativo al inicio: «La situación cambió: actualizamos tu viaje» |
| 7 | el proveedor de cambios rechaza con un error no reintentable, o el proveedor de casos responde un error explícito | llega el resultado FAILED | aviso de error con rol de alerta: para la solicitud de cambio «No pudimos procesar tu solicitud de cambio. Puedes hablar con una persona para que te ayude.» y para el caso humano «No pudimos registrar tu solicitud, puedes reintentar.»; nunca se afirma éxito |

**Acceptance Criteria**:

- [ ] Cada uno de los siete resultados tiene una redacción y estado visual propios.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | Respuesta a un clic de «Aceptar esta opción». |
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Leer resultado → Elegir redacción → Pintar estado
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.95 FE-03.4 Refresco tras estado cambiado

**Spec fuente**: [FE-03.4 Refresco tras estado cambiado](95-fe-03-4-refresco-tras-estado-cambiado.md)  
**Requisitos**: FR-070, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-31

Al recibir «estado cambiado» reemplaza la vista por la nueva y mueve el foco al aviso informativo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la huella difiere | se recibe | se muestra la vista nueva con «La situación cambió: actualizamos tu viaje» |
| 2 | los asientos de O1 pasaron de 4 a 0 | se recibe el estado cambiado | se reemplaza la vista y el foco va al aviso informativo |

**Acceptance Criteria**:

- [ ] El 100 % de los estados cambiados reemplaza la vista y mueve el foco.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, load_status, data_as_of, segments, alerts, derived_variables, policy, options, proposed_option_id, refund_notice, offer_deadline, actions, messages, operations, human_cases | Respuesta completa para el pasajero; solo contiene campos de la lista blanca. |

**Business Process (BPM)**:

```
Recibir vista nueva → Reemplazar → Mover foco
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.96 FE-03.5 Segundo clic tras necesidad de confirmación

**Spec fuente**: [FE-03.5 Segundo clic tras necesidad de confirmación](96-fe-03-5-segundo-clic-tras-necesidad-de-confirmacion.md)  
**Requisitos**: FR-050, FR-105, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-33

Tras un resultado indeterminado advierte del posible duplicado y exige un segundo clic explícito conservando la opción.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el intento previo fue indeterminado | el pasajero pulsa de nuevo | el diálogo dice «No pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté. Si la envías de nuevo, podría duplicarse.» con los botones «Cerrar» y «Enviar de nuevo igualmente»; el segundo repite la misma petición con la confirmación |
| 2 | el caso HC-4471 quedó indeterminado | se pulsa otra vez | se advierte del posible duplicado y se exige «Enviar de nuevo igualmente» |

**Acceptance Criteria**:

- [ ] El 100 % de los reenvíos tras indeterminado exige el segundo clic.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Mostrar advertencia → Esperar segundo clic → Reenviar con confirmación
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.97 FE-04 Hablar con una persona (front)

**Spec fuente**: [FE-04 Hablar con una persona (front)](97-fe-04-hablar-con-una-persona-front.md)  
**Requisitos**: FR-050, FR-057, FR-059, FR-060, FR-061, FR-067, FR-105, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-17, TC-20, TC-33, TC-46

El botón «Hablar con una persona» solo existe con una acción posible: con motivo conocido crea el caso con un solo clic; sin motivo conocido abre un diálogo con motivos neutros, sin preselección y sin texto libre, y muestra el resultado, incluyendo la advertencia de posible duplicado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | no hay motivo conocido | el pasajero pulsa «Hablar con una persona» | se abre un diálogo con «Necesito ayuda con mi vuelo» y «Necesito ayuda con mis datos o documentos», ninguno preseleccionado y sin campo de texto |
| 2 | hay compensación elegible | se abre el diálogo | aparece también «Tengo una consulta sobre compensaciones» |
| 3 | el motivo ya es conocido (conflicto, sin opción) | pulsa el botón | se crea el caso con un solo clic |
| 4 | el intento previo fue indeterminado | se pulsa de nuevo | se advierte y se exige un segundo clic |
| 5 | BASE_TC01 con compensación elegible (R4) y la variante SIN_COMPENSACION_TC46 | se abre «Hablar con una persona» | el caso base muestra 3 motivos y la variante 2, ninguno preseleccionado y sin campo de texto |

**Acceptance Criteria**:

- [ ] El diálogo nunca contiene un campo de texto libre ni un motivo preseleccionado.
- [ ] El motivo de compensación aparece solo con compensación elegible.
- [ ] El botón no existe en pantallas sin acción posible.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Resultado de caso humano | outcome, message, human_case, decision_id | Respuesta a un clic de «Hablar con una persona». |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Pulsar botón → Abrir diálogo o crear con un clic → Enviar motivo → Mostrar resultado
```

Subprocess detail (if applicable):

```
FE-04.1: Diálogo de motivo
FE-04.2: Clic único con motivo conocido
FE-04.3: Envío con la decisión
FE-04.4: Resultado y errores
FE-04.5: Advertencia de duplicado y segundo clic
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.98 FE-04.1 Diálogo de motivo

**Spec fuente**: [FE-04.1 Diálogo de motivo](98-fe-04-1-dialogo-de-motivo.md)  
**Requisitos**: FR-060, FR-067, NFR-011, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-17, TC-46

Diálogo modal con motivos neutros en un grupo de opciones, sin preselección ni campo de texto, y con el menú de compensación condicionado.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el diálogo se abre | se inspecciona | ningún motivo está preseleccionado y no hay campo de texto |
| 2 | no hay compensación elegible | se abre | el menú no ofrece compensación |
| 3 | el diálogo del caso base abierto con el teclado | se inspecciona | los motivos están en un grupo con la leyenda «¿Con qué necesitas ayuda?», el foco inicial está en el título, queda atrapado y Esc cierra devolviendo el foco al botón que lo abrió |
| 4 | SIN_COMPENSACION_TC46 | se abre el diálogo | muestra 2 motivos y la pista «Elige un motivo» |

**Acceptance Criteria**:

- [ ] Ningún motivo preseleccionado en el 100 % de las aperturas.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Abrir diálogo → Mostrar motivos ofrecidos → Esperar elección
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.99 FE-04.2 Clic único con motivo conocido

**Spec fuente**: [FE-04.2 Clic único con motivo conocido](99-fe-04-2-clic-unico-con-motivo-conocido.md)  
**Requisitos**: FR-050, FR-057, FR-060, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-03, TC-09

Cuando el sistema ya conoce el motivo, el botón «Hablar con una persona» crea el caso con un solo clic enviando «otra ayuda» y la decisión.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | conflicto de fuentes | se pulsa el botón | se crea el caso sin diálogo y con el texto de efecto previo |
| 2 | CONFLICTO_TC03 con la decisión mostrada | se pulsa «Hablar con una persona» | se crea el caso con 1 solo clic |

**Acceptance Criteria**:

- [ ] Con motivo conocido el caso se crea con un solo clic en el 100 % de los casos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Pulsar botón → Enviar con la decisión
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.100 FE-04.3 Envío con la decisión

**Spec fuente**: [FE-04.3 Envío con la decisión](100-fe-04-3-envio-con-la-decision.md)  
**Requisitos**: FR-059, FR-060, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-17

Envía el motivo con la decisión que el pasajero vio para que la evidencia salga de la decisión guardada.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | la vista tiene una decisión | se envía | la petición lleva la decisión mostrada |
| 2 | BASE_TC01 con compensación elegible (R4) y la decisión mostrada de ABC123 | se elige «Tengo una consulta sobre compensaciones» | la petición lleva esa decisión y fija la solicitud de compensación, sin montos |

**Acceptance Criteria**:

- [ ] El 100 % de los envíos lleva la decisión mostrada.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |

**Business Process (BPM)**:

```
Tomar decisión mostrada → Enviar
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.101 FE-04.4 Resultado y errores

**Spec fuente**: [FE-04.4 Resultado y errores](101-fe-04-4-resultado-y-errores.md)  
**Requisitos**: FR-059, FR-061, FR-105, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-20, TC-33

Muestra el caso creado, el existente o el error «puedes reintentar», con tono y rol adecuados.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el caso se creó | se pinta | aviso de éxito con rol de estado, que recibe el foco: «Registramos tu solicitud. Una persona te atenderá; el tiempo objetivo de atención es de 45 minutos. Código de seguimiento: HC-4471.» |
| 2 | error explícito del proveedor de casos | se pinta | aviso de error con rol de alerta, «No pudimos registrar tu solicitud, puedes reintentar.», y los botones «Cerrar» y «Reintentar» (texto de la variante de error del diálogo en el DESIGN_CONTRACT v1.5) |
| 3 | el pasajero eligió «Necesito ayuda con mis datos o documentos» y el caso HC-4471 quedó creado con 45 minutos | se pinta | dice el tiempo objetivo de 45 minutos y el código HC-4471, sin mostrar ningún dato personal |

**Acceptance Criteria**:

- [ ] Todos los resultados usan un texto del catálogo.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Resultado de caso humano | outcome, message, human_case, decision_id | Respuesta a un clic de «Hablar con una persona». |

**Business Process (BPM)**:

```
Leer resultado → Pintar mensaje
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.102 FE-04.5 Advertencia de duplicado y segundo clic

**Spec fuente**: [FE-04.5 Advertencia de duplicado y segundo clic](102-fe-04-5-advertencia-de-duplicado-y-segundo-clic.md)  
**Requisitos**: FR-050, FR-105, FR-VIS-001, FR-VIS-002, FR-VIS-003  
**Pruebas (TC)**: TC-33

Tras un resultado indeterminado advierte del posible duplicado y exige un segundo clic explícito.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | intento previo indeterminado | se pulsa de nuevo | el diálogo dice «No pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté. Si la envías de nuevo, podría duplicarse.» con los botones «Cerrar» y «Enviar de nuevo igualmente» |
| 2 | el caso HC-4471 anterior quedó indeterminado | se pulsa de nuevo | aparecen «Cerrar» y «Enviar de nuevo igualmente» |

**Acceptance Criteria**:

- [ ] Ningún reenvío ocurre sin la confirmación explícita.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | Estado visible del front según la vista recibida. |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, queue, sla_minutes, option, confirm_possible_duplicate | Escalamiento a una persona; cada intento queda registrado con su resultado. |

**Business Process (BPM)**:

```
Advertir → Esperar segundo clic → Reenviar
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.103 X-01 Requisitos transversales de calidad, privacidad y operación

**Spec fuente**: [X-01 Requisitos transversales de calidad, privacidad y operación](103-x-01-requisitos-transversales-de-calidad-privacidad-y.md)  
**Requisitos**: FR-001, FR-031, FR-091, FR-112, NFR-002, NFR-003, NFR-005, NFR-006, NFR-007, NFR-009, NFR-010, NFR-012, NFR-013  
**Pruebas (TC)**: TC-01, TC-21, TC-49, TC-50, TC-58

Reúne los requisitos no funcionales que no pertenecen a un solo flujo (privacidad, seguridad, operabilidad, calidad, estilo de desarrollo, portabilidad y confidencialidad) y declara dónde se materializan y cómo se verifican.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | los escenarios con datos ficticios | se recorren registros, respuestas y pantallas | ningún dato personal aparece fuera de la excepción del nombre de pila |
| 2 | el código del servicio | se mide | ninguna función excede 10 líneas ni 3 parámetros y el dominio no depende de la tecnología |
| 3 | el conjunto de pruebas | se ejecuta | los casos TC-01 a TC-56 están automatizados y la cobertura de líneas del dominio es de al menos 85 % |
| 4 | las consultas, la interfaz y la evaluación | se revisan | toda consulta es parametrizada con las consultas en archivos propios, los textos del proveedor se ven como texto plano y la evaluación aplica un límite de tasa |
| 5 | una instalación limpia | se siguen las instrucciones | el sistema corre sin contenedores |
| 6 | los escenarios de ABC123 con Ana Prueba, su correo ficticio y la clave de servicio válida | se buscan en registros, en la respuesta del modo sistema y en la pantalla | ningún dato de Ana Prueba aparece fuera de «Hola, Ana» y la respuesta del sistema no trae datos personales ni acepta una clave incorrecta |
| 7 | ABC123 con `EVALUATE_RATE_LIMIT_PER_MINUTE` de 30, una condición de regla con marcado HTML y un identificador de reserva con comillas | llega el 31.º `evaluate` del minuto y se muestran los textos del proveedor | el 31.º se rechaza por límite de tasa (igual en aceptar, caso humano y consulta de decisión, por reserva y por origen); el marcado HTML se ve como texto plano y la consulta con comillas no altera el registro |
| 8 | el caso base ABC123 (TC-01), TC-01 a TC-20 y el modo sistema (TC-42, TC-43, TC-44, TC-50) | se planifica la implementación en 3 horas | se implementan primero esos escenarios con funciones de a lo sumo 10 líneas; los demás TC quedan automatizados solo si alcanza el tiempo |

**Acceptance Criteria**:

- [ ] El 100 % de las pruebas TC-01 a TC-56 está automatizado.
- [ ] La cobertura de líneas del dominio es de al menos 85 %.
- [ ] El 100 % de las funciones cumple los límites de 10 líneas y 3 parámetros.
- [ ] El repositorio no contiene el enunciado original ni secretos.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Configuración | name, default, effective_value, validation, is_secret, effect | Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. |
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, needs_manual_review, policy_version, mct_provided, passenger_count, segments, message_hash, messages_blocked, reads, events, rules, options, notifications, outcomes | Instantánea de auditoría de una evaluación, sin información personal. |

**Business Process (BPM)**:

```
Verificar privacidad → Verificar seguridad → Verificar calidad y estilo → Verificar portabilidad y confidencialidad
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.104 X-02 Entregables de documentación

**Spec fuente**: [X-02 Entregables de documentación](104-x-02-entregables-de-documentacion.md)  
**Requisitos**: FR-100, FR-101, DOC-001, DOC-002, DOC-003, DOC-004, DOC-005, DOC-006, DOC-007, DOC-008, DOC-009, DOC-010, DOC-011, DOC-012, DOC-013, NFR-010  
**Pruebas (TC)**: TC-01

Reúne los entregables de documentación del proyecto (README, nota de IA, diseño técnico, decisiones, bitácora, guion, notas obligatorias, información a solicitar, runbook, preguntas a Producto y Legal, diseño de la aprobación humana y extensiones de contrato) y su contenido mínimo.

**User Stories** (Given-When-Then):

| # | Given | When | Then |
|---|-------|------|------|
| 1 | el repositorio entregado | se abre el README | dice el track elegido y por qué, cómo ejecutar, el alcance, las pruebas y las limitaciones |
| 2 | el documento de ingeniería | se revisa | ocupa dos páginas como máximo y clasifica cada paso como determinístico, asistido por IA, agéntico o humano con su razón, riesgo y control |
| 3 | los documentos de notas | se revisan | incluyen las seis notas obligatorias, la lista de información a solicitar (tiempo mínimo de conexión, campo de causa, semántica de «pendiente de confirmación», definición de menor) y las preguntas para Producto y Legal |
| 4 | los contratos propuestos | se revisan | documentan la reserva y los pasajeros en la solicitud de cambio, el aviso informativo sin referencia de política y el contrato reducido de opciones |
| 5 | 13 entregables y el README de ingeniería de 2 páginas | se revisan | los 13 existen y el README no excede 2 páginas |

**Acceptance Criteria**:

- [ ] Los 13 entregables DOC-001 a DOC-013 existen y cumplen su extensión máxima.
- [ ] El 100 % de los supuestos provisionales y riesgos declarados (H-xx) figura en la documentación de decisiones.

**Key Entities**:

| Entity | Fields | Description |
|--------|--------|-------------|
| Entregable de documentación | doc_id, title, audience, max_length, status | Documento que acompaña al producto. |

**Business Process (BPM)**:

```
Redactar documento → Revisar contra su requisito → Entregar
```

**👓 Lens Recommendations**: no se aplican en A2; las lentes de diseño (A4) incorporarán aquí sus recomendaciones para este flujo.

### 2.105 Cross-Cutting Lens Recommendations

**👓 Lens Recommendations globales**: no se aplican en A2; el análisis de lentes (A4) registrará aquí las recomendaciones que afecten a todo el sistema (por ejemplo, datos y operaciones). Las deudas de A1 y las preguntas de A2 se listan en `sdd/reports/A2_OPEN_QUESTIONS.md`: están resueltas OQ-A2-01 a 05, 07 a 09, 11 a 16, 18 a 20 y la deuda DEBT-A1-08; siguen abiertas como riesgo o pendiente del usuario OQ-A2-06 y OQ-A2-17, y OQ-A2-10 pasa a A5.

---

## 3. Glossary

> Términos de negocio y su correspondencia con las entidades de los specs. El glosario formal (`sdd/GLOSSARY.md`) se produce en el paso A3.

| Business Term | Code Mapping | Definition |
|---------------|-------------|------------|
| Decisión | entidad «Decisión» | Resultado de evaluar una reserva: INFORMATIVA, AUTOMATICA, PENDIENTE_APROBACION o BLOQUEADA (o nula si no hay anomalía o falló una lectura). |
| Política rota | entidad «Política y regla» | Al menos una regla cumplida concede un derecho de remedio; solo entonces hay opciones y soporte (FR-039). |
| Derecho de remedio | parámetro `REMEDY_RIGHTS` | Derecho que rompe la política: cambio sin costo, vale de comida o compensación en dinero (por defecto). |
| Evento relevante | entidad «Evento operacional» | Retraso validado de al menos `RELEVANT_DELAY_MIN_MINUTES` (1) minutos (FR-005). |
| Fuente degradada | entidad «Evento operacional» | Fuente declarada degradada: sus eventos no son evidencia (FR-010). |
| Conflicto de fuentes | entidad «Estado resuelto del segmento» | Dos eventos sanos del mismo segmento con el mismo instante y afirmaciones incompatibles (FR-013). |
| Tiempo mínimo de conexión (MCT) | parámetro `MIN_CONNECTION_MINUTES` | Tiempo mínimo para una conexión en un aeropuerto; 0 y rotulado «supuesto» si no se provee. |
| Conexión perdida | entidad «Variable derivada» | Estimación de si el retraso hace perder la conexión: verdadera, falsa o desconocida (FR-022). |
| Estimación | entidad «Variable derivada» | Valor derivado (nueva llegada, conexión) siempre rotulado y nunca presentado como garantía. |
| Opción viable | entidad «Opción de reprogramación» | Opción que cubre al grupo, tiene derecho que la respalda, política vigente, no vencida y coherente con el itinerario (FR-041). |
| Hora límite | entidad «Vista del viaje» | Mínimo de los vencimientos de las opciones mostradas (FR-071). |
| Huella de decisión | entidad «Decisión» | Resumen reproducible del estado resuelto, reglas y opción elegida, que no incluye marcas de tiempo ni identificadores de opción (FR-070). |
| Llave de idempotencia | entidad «Operación de reprogramación» | Llave no adivinable que evita duplicar un cambio (FR-053). |
| Generación | entidad «Operación de reprogramación» | Contador que habilita una operación nueva tras una expirada o fallida (FR-064). |
| Caso humano | entidad «Caso humano» | Escalamiento a una persona, con motivo de enumeración cerrada y evidencia sin información personal (FR-059). |
| Motivo de caso humano | entidad «Caso humano» | Uno de 13 códigos con prioridad fija (FR-057, FR-063). |
| Modo pasajero / modo sistema | entidad «Sesión y credencial» | Quién pide la evaluación: el pasajero con su sesión, u otro sistema con credencial de servicio (FR-120). |
| Notificación | entidad «Notificación» | Aviso de plantilla fija, solo en modo sistema, una por motivo, sin enlaces ni contacto (FR-122). |
| Revisión manual | entidad «Registro de decisión» | Marca interna de decisiones BLOQUEADAS o lecturas fallidas (FR-123). |
| Escenario | entidad «Escenario de desarrollo» | Conjunto de datos simulados de las siete herramientas, solo en desarrollo (FR-101). |
| Registro de decisión | entidad «Registro de decisión» | Instantánea de auditoría sin información personal (FR-090, FR-091). |

---

## 4. Architectural Attributes

> Resumen de los atributos de los specs. Detalle por flujo en cada spec; patrón candidato en `sdd/reports/ARCHITECTURE.md` §4.

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Interaction type | sync-http (flujos de evaluación, aceptación, caso humano, consulta); batch (purga, métricas, configuración al arrancar) | La evaluación es una consulta síncrona del pasajero o de otro sistema; el mantenimiento se ejecuta por comando. |
| Consistency | strong | Una operación de cambio y un caso humano deben escribirse una sola vez y con exclusión concurrente (FR-053, FR-059, FR-062). |
| Workflow | multi-step | La cadena de lecturas es secuencial: contexto, eventos, política, opciones (FR-009). |
| Read pattern | simple (analytics solo en las métricas de éxito) | Cada evaluación lee cuatro fuentes; las métricas leen el registro. |
| Auditability | full-history | Cada evaluación deja un registro sin información personal (FR-090, FR-091). |
| Domain complexity | high | Precedencia de eventos, lógica de tres valores, política, idempotencia y consentimiento. |
| Modularity | bounded-context | Un único contexto delimitado de disrupción de vuelos. |
| Deployment | monolith | Un solo servicio local; sin necesidad de microservicios en la versión 1. |

---

## 5. Architecture

> Candidata fijada en A1; se confirma en el paso de diseño (A5). Fuente: `sdd/reports/ARCHITECTURE.md`.

- **Pattern chosen**: arquitectura hexagonal (puertos y adaptadores) con elementos tácticos de diseño dirigido por el dominio (`ARCHITECTURE.md` §4).
- **Justification**: el dominio es complejo y debe ser independiente de la tecnología (NFR-007); las siete herramientas externas se simulan hoy y se reemplazarán por adaptadores reales sin tocar el dominio (FR-100). Se descartó Event Sourcing porque el registro es una instantánea sin cargas completas (FR-091).
- **Folder structure**: ver `ARCHITECTURE.md` §4 (dominio, aplicación, puertos, adaptadores, API; front con componentes y catálogo de textos). El DESIGN_CONTRACT (`sdd/reports/DESIGN_CONTRACT.md`) fija el inventario de componentes y los tokens del front.

---

## 6. Service Dependencies

> Capacidades funcionales requeridas por el sistema, sin nombrar tecnología. Detalle en `EXTERNAL_CONTRACTS.md` §2.

| Capability | Flow(s) | Description | Direction |
|------------|---------|-------------|-----------|
| Consulta del contexto del viaje (herramienta 1) | F-01, F-02, F-03, F-11 | Reserva, pasajeros, segmentos y condiciones de tarifa; puede venir parcial (FR-066). | outbound (lectura) |
| Consulta de eventos operacionales (herramienta 2) | F-01, F-02, F-11 | Retrasos, cambios de puerta y estados por segmento, con fuente e instante. | outbound (lectura) |
| Consulta de opciones elegibles (herramienta 3) | F-01, F-02 | Opciones candidatas con vigencia; solo con política rota y contexto reducido sin información personal. | outbound (lectura) |
| Consulta de reglas de política (herramienta 4) | F-01, F-02, F-11 | Reglas versionadas del escenario de retraso; única fuente de umbrales. | outbound (lectura) |
| Solicitud de cambio de reserva (herramienta 5) | F-02 | Escritura de alto impacto, idempotente, tras el clic del pasajero. | outbound (escritura) |
| Creación de caso humano (herramienta 6) | F-02, F-03 | Escalamiento a una persona; sin llave idempotente en el proveedor. | outbound (escritura) |
| Notificación al pasajero (herramienta 7) | F-08, F-11 | Aviso de plantilla fija solo en modo sistema. | outbound (escritura) |
| Almacenamiento persistente local | F-01, F-02, F-03, F-04, F-07, F-08, F-09, F-10 | Registro de decisiones, operaciones, casos y notificaciones, sin información personal. | both |
| Reloj | F-01, F-06, F-07, F-09 | Fuente única de tiempo inyectable (reloj del sistema, de escenario o fijo). | inbound |
| Configuración central | F-12 y todos | Valores por defecto con sobrescritura por entorno y validación al arrancar. | inbound |

---

## 7. API Contracts

> Fuente única: `sdd/reports/EXTERNAL_CONTRACTS.md` §1.1 (no se copian los esquemas aquí).

| Method | Path | Description | Request Body | Response Body | Error Codes |
|--------|------|-------------|-------------|--------------|-------------|
| GET | `/ping` | Verificación de vida (F-05). | ninguno | texto «pong» | ninguno |
| POST | `/api/v1/trips/{booking_id}/evaluate` | Evalúa el viaje con `caller` = user o system (F-01, F-11). | §1.1, fila 2 | TripView o SystemEvaluationResult | 401, 429, 404, 422, 502, 500 |
| POST | `/api/v1/trips/{booking_id}/options/{option_id}/accept` | Acepta una opción (F-02). | §1.1, fila 3 | AcceptResult (también con 409, 502) | 401, 404, 422, 500 |
| POST | `/api/v1/trips/{booking_id}/human-cases` | Hablar con una persona (F-03). | §1.1, fila 4 | HumanCaseResult (también con 409, 502, 504) | 401, 404, 422, 500 |
| GET | `/api/v1/decisions/{decision_id}` | Registro de decisión (F-04). | ninguno | DecisionRecord | 401, 404, 422, 500 |
| GET | `/api/dev/scenarios` | Solo desarrollo (F-06). | ninguno | catálogo de escenarios | 404 |
| PUT | `/api/dev/scenario` | Solo desarrollo (F-06). | scenario_id | escenario activo | 404, 422 |
| PUT | `/api/dev/clock` | Solo desarrollo (F-06). | advance_seconds | reloj vigente | 404, 422 |

### 7.1 Error Responses

> Esquema uniforme `{error, detail}` y catálogo de códigos en `EXTERNAL_CONTRACTS.md` («Catálogo de códigos de error propios»). Excepción: aceptar y caso humano devuelven su cuerpo de resultado también con 409, 502 y 504.

| Endpoint | HTTP Status | Condition | Response Body | Example |
|----------|-------------|-----------|--------------|---------|
| /api/v1/* | 401 | Falta la sesión o la credencial de servicio (FR-001, FR-120) | `{error: UNAUTHENTICATED, detail}` | modo system sin clave |
| /api/v1/* | 404 | Reserva o decisión ajena o inexistente; respuesta idéntica (FR-001) | `{error: NOT_FOUND, detail}` | reserva de otra sesión |
| evaluate | 429 | Se supera `EVALUATE_RATE_LIMIT_PER_MINUTE` por reserva y credencial (NFR-013) | `{error: RATE_LIMITED, detail}` | 31 solicitudes en un minuto |
| /api/v1/* | 422 | Cuerpo o ruta inválidos, opción no ofrecida, motivo no disponible, soporte no disponible | `{error: VALIDATION_ERROR | OPTION_NOT_OFFERED | REASON_NOT_AVAILABLE | SUPPORT_NOT_AVAILABLE, detail}` | texto libre en el caso humano |
| evaluate | 502 | No se pudo cargar el contexto del viaje (FR-105) | `{error: TRIP_CONTEXT_UNAVAILABLE, detail}` | contexto caído tras la re-consulta |
| * | 500 | Error no previsto, sin trazas | `{error: INTERNAL_ERROR, detail}` | falla inesperada |

### 7.2 Output Contracts

> Cómo el sistema llama a las siete herramientas externas; esquemas completos en `EXTERNAL_CONTRACTS.md` §2.1.

| Service | Method | Endpoint / Resource | Request Schema | Response Schema | Error Handling | Timeout |
|---------|--------|-------------------|---------------|----------------|----------------|---------|
| Contexto del viaje | lectura | herramienta 1 | booking_id | TripContext (§2.1) | 1 re-consulta; luego error de contexto no disponible | `UPSTREAM_READ_TIMEOUT_MS` (2000) |
| Eventos operacionales | lectura | herramienta 2 | lista de segment_id | OperationalEvents (§2.1) | 1 re-consulta; luego contexto sin estado | `UPSTREAM_READ_TIMEOUT_MS` (2000) |
| Opciones elegibles | lectura | herramienta 3 | contexto reducido sin información personal | EligibleOptions (§2.1) | 1 re-consulta; luego BLOQUEADA con soporte | `UPSTREAM_READ_TIMEOUT_MS` (2000) |
| Reglas de política | lectura | herramienta 4 | escenario | PolicyRules (§2.1) | 1 re-consulta; luego BLOQUEADA con soporte | `UPSTREAM_READ_TIMEOUT_MS` (2000) |
| Solicitud de cambio | escritura | herramienta 5 | opción, llave, reserva, pasajeros | 201, 409 o 503 (§2.1) | hasta `REBOOK_MAX_RETRIES` (2) con la misma llave; luego caso humano | `UPSTREAM_WRITE_TIMEOUT_MS` (5000) |
| Caso humano | escritura | herramienta 6 | motivo, evidencia sin información personal | 201 (§2.1) | sin reintento automático; segundo clic explícito | `UPSTREAM_WRITE_TIMEOUT_MS` (5000) |
| Notificación | escritura | herramienta 7 | mensaje de plantilla fija, tipo, motivo, destinatario, llave | 202 o 422 (§2.1) | hasta `NOTIFY_MAX_RETRIES` (2) con la misma llave | `UPSTREAM_WRITE_TIMEOUT_MS` (5000) |

---

## 8. Event Listeners & Non-HTTP Entry Points

> No hay consumidores de eventos, webhooks ni tareas programadas en la versión 1 (`EXTERNAL_CONTRACTS.md` §1.2 y §1.3). Los puntos de entrada no HTTP son comandos y el arranque; cada uno es un flujo de negocio.

| Type | Trigger / Source | Payload | Flow(s) | Description | Error Handling |
|------|-----------------|---------|---------|-------------|----------------|
| Comando | purga de retención, una vez al arrancar el servicio | ninguno | F-07 | Elimina registros antiguos y conserva minimizadas las operaciones vigentes (FR-092). | informa filas eliminadas; no borra operaciones no finalizadas |
| Comando | reporte de métricas (solo lectura) | ninguno | F-10 | Calcula las tres métricas de NFR-008 desde el registro. | informa ceros sin dividir por cero |
| Arranque | inicio del servicio y de las pruebas | variables de entorno | F-12 | Carga y valida la configuración (NFR-012). | no arranca y nombra el parámetro |
| Lectura perezosa | lectura de operaciones, casos y notificaciones | ninguno | F-09 | Aplica transiciones por tiempo (FR-064). | actualización condicional por estado esperado |

---

## 9. Data Models

> Modelo de datos físico: `EXTERNAL_CONTRACTS.md` §2.3 (registro propio). Las entidades de negocio y sus campos principales están en cada spec (sección Key Entities) y se resumen aquí.

| Entity | Fields | Types | Relationships | Constraints |
|--------|--------|-------|--------------|-------------|
| Contexto del viaje | booking_id, passenger_count, passengers, segments, fare_conditions, retrieved_at, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | Reserva 1..n Pasajero y Segmento | booking_id único; mínimo 1 segmento y 1 pasajero |
| Evento operacional | event_id, segment_id, type, delay_minutes, new_departure, gate, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n por Segmento | ordenado por instante de registro, nunca por identificador |
| Estado resuelto del segmento | segment_id, state, affected, delay_minutes, gate, gate_recorded_at, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por Segmento | derivado de eventos sanos |
| Variable derivada | name, segment_id, value, known, origin, estimated, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n por Decisión | con origen y supuestos |
| Política y regla | scenario, status, version, effective_from, superseded_versions, entitlements, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por Decisión; reglas 1..n | versión fijada en el registro |
| Opción de reprogramación | option_id, itinerary_key, type, flight_number, origin, destination, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n por Decisión | solo las viables se muestran; todas se registran |
| Decisión | decision_id, decision_state, anomaly_detected, fingerprint, human_case_reasons, support_offered, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por evaluación; 1 Registro de decisión | identificador no adivinable |
| Operación de reprogramación | itinerary_key, idempotency_key, generation, state, request_id, request_status, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n por Reserva | llave única por (reserva, itinerario, generación) |
| Caso humano | dedup_key, attempt, state, reason, reasons, case_id, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n intentos por clave de deduplicación | un solo intento en curso a la vez |
| Notificación | reason, kind, policy_ref, booking_id, recipient_passenger_id, motive_fingerprint, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n por Reserva y motivo | un solo intento vigente por clave |
| Mensaje validado | message_id, template_id, kind, text, evidence_refs, policy_ref, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n por Decisión | sin hechos sin evidencia |
| Vista del viaje | decision_id, generated_at, anomaly_detected, decision_state, holder_first_name, passenger_count, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por Decisión de modo pasajero | solo campos de la lista blanca |
| Resultado de evaluación del sistema | decision_id, decision_state, reason, notifications, needs_manual_review | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por Decisión de modo sistema | sin información personal |
| Resultado de aceptación | outcome, message, operation, human_case, retries, view | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por clic de aceptar | siete resultados posibles |
| Resultado de caso humano | outcome, message, human_case, decision_id | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por clic de hablar con una persona | cinco resultados posibles |
| Registro de decisión | decision_id, booking_id, created_at, caller, fingerprint, decision_state, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por evaluación | solo campos de la lista cerrada, sin campos internos para la sesión del pasajero; retención `AUDIT_RETENTION_DAYS` (30) |
| Configuración | name, default, effective_value, validation, is_secret, effect | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por parámetro | valores validados al arrancar; secretos solo por entorno |
| Escenario de desarrollo | scenario_id, booking_id, title, description, ui, tests | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | n en el catálogo | solo con las funciones de desarrollo habilitadas |
| Reloj de escenario | mode, now, offset_seconds, advance_seconds | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 activo | avance entre 0 y 86400 segundos |
| Reporte de métricas | situations_actionable, m1_resolution_without_human, m1_viable_option_shown, m2_human_cases_by_reason, m3_messages_blocked, m3_unsupported_claims, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por ejecución | solo lectura |
| Sesión y credencial | caller, session_booking, service_key, requests_last_minute, authorized | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por petición | modo user o system |
| Registro de retención | cutoff, deleted_decisions, deleted_operations, deleted_cases, deleted_notifications, expired_by_sweep, … | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por purga | conserva operaciones no finalizadas minimizadas |
| Pantalla del front de prueba | screen_state, components, texts, focus_target, aria_busy | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 1 por estado de la vista | texto solo del catálogo |
| Entregable de documentación | doc_id, title, audience, max_length, status | texto, enteros, booleanos, enumeraciones, marcas de tiempo UTC (tipos completos en los specs) | 13 documentos | extensión máxima según DOC |

---

## 10. Results

> Aún no hay resultados de implementación; se registran al cerrar el proyecto (paso A12).

- **Tests**: 0 implementados; 60 casos TC-01 a TC-60 asignados a specs (cobertura de líneas del dominio objetivo ≥ 85 %, NFR-006).
- **Traceability**: 0 de 96 FR implementados; 96 de 96 FR, 13 de 13 NFR y 13 de 13 DOC cubiertos por specs (`sdd/reports/FR_COVERAGE.md`).
- **Comparative Analysis**: no aplica antes de implementar; el análisis comparativo previo y posterior al SDD se redacta en A12.

---

## Appendix: Reconciliation Guide

This RFC supports a **bidirectional feedback cycle**:

1. **Workflow generates RFC** from individual specs
2. **Team reviews and edits RFC** — business and technical feedback goes here
3. **Agent detects changes** — diffs RFC against specs
4. **Agent updates specs** — reconciles feedback into the source of truth
5. **Agent regenerates RFC** — clean version reflecting updated specs

The spec remains the **source of truth**. The RFC is the communication channel. Changes flow: **Team feedback (RFC) -> Specs -> Code**. Never the reverse.
