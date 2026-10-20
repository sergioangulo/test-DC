# Glosario de Interfaces de Disruption Companion V0

Este documento define el vocabulario técnico del proyecto **Disruption Companion V0** (vertical slice acotado de 15 specs funcionales en `sdd/specs/functional/`).
Sirve como puente entre el lenguaje natural de los requerimientos funcionales y el código en inglés.

---

## Cómo usar este glosario

1. **Para crear requerimientos**: Busca el concepto que necesitas y usa el nombre exacto de la interfaz/método.
2. **Para entender specs**: Cada método tiene una descripción en lenguaje natural.
3. **Para el agente**: Traduce lenguaje natural (español) → vocabulario del proyecto (inglés).

---

## Categorías de Interfaces

| Categoría | Propósito | Ubicación |
|-----------|-----------|-----------|
| **Ports (Tools Externas)** | Contratos de lectura/escritura hacia las herramientas del PDF (`SRC-01-16`) | `backend/app/domain/ports.py` |
| **Domain (Lógica de Negocio)** | Validación de eventos, derivación de variables, motor de reglas, filtrado de opciones y validador de mensajes | `backend/app/domain/` |
| **Application (Casos de Uso)** | Orquestación secuencial de evaluación (`EvaluateTrip`), ejecución de acción (`AcceptOption`) y escenarios (`ScenarioManager`) | `backend/app/application/` |
| **API / UI** | Endpoints FastAPI y visor React mínimo que muestra lo que recibe del backend | `backend/app/api/`, `frontend/src/` |

---

## 1. Ports - Herramientas Externas y Almacenamiento

### ITripContextPort
**Propósito**: Consultar el contexto de la reserva (`get_trip_context(booking_id)`).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `get_trip_context(booking_id)` | "consultar el contexto del viaje" | Recupera pasajeros, segmentos, condiciones tarifarias y `_meta` (`retrieved_at`, `completeness`, `missing_fields`) |

### IOperationalEventsPort
**Propósito**: Consultar eventos operacionales por segmento (`get_operational_events(segment_ids)`).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `get_operational_events(segment_ids)` | "consultar eventos operacionales" | Recupera lista de eventos (`DELAY`, `GATE_CHANGE`, `STATUS`, etc.) y `_meta` (`sources_degraded`) |

### IPolicyRulesPort
**Propósito**: Consultar reglas versionadas de política (`get_policy_rules(scenario)`).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `get_policy_rules(scenario)` | "consultar reglas de política" | Recupera versión vigente, reglas `R1..R5` y `_meta.superseded_versions` para el escenario `DELAY` |

### IEligibleOptionsPort
**Propósito**: Consultar opciones candidatas de reprogramación/reembolso (`get_eligible_options(trip_context)`).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `get_eligible_options(reduced_context)` | "consultar opciones elegibles" | Recupera opciones candidatas (`O1..O3`) y `_meta.ttl_seconds` enviando contexto reducido sin PII |

### IRebookingPort
**Propósito**: Solicitar cambio de reserva controlado (`create_rebooking_request(option, idempotency_key)`).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `create_rebooking_request(request)` | "crear solicitud de cambio" | Ejecuta cambio con llave idempotente; devuelve `201 PENDING_CONFIRMATION`, `409 DUPLICATE_REQUEST` o `503 UPSTREAM_TIMEOUT` |

### IHumanCasePort
**Propósito**: Escalar a operación humana (`create_human_case(reason, evidence)`).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `create_human_case(reason, evidence)` | "crear caso humano / derivar a una persona" | Abre caso en cola `DISRUPTION_L2` con motivo principal y evidencia validada sin PII |

### IDecisionStore
**Propósito**: Guardar y recuperar la traza de decisiones y operaciones en memoria (supuesto S-V0-3).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `save_decision(record)` | "registrar la decisión" | Guarda la instantánea de auditoría sin PII (`decision_id`) |
| `get_decision(decision_id)` | "obtener registro de decisión" | Recupera la decisión guardada por su identificador |

---

## 2. Domain - Lógica de Negocio

### EventResolver
**Propósito**: Validar eventos operacionales, excluir fuentes degradadas y resolver precedencia o conflictos (SF-01.4, SF-01.5).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `resolve_events(segments, events_payload)` | "validar eventos y resolver estado por segmento" | Excluye `SOURCE_DEGRADED`, `INCONSISTENT_DELAY`, `UNKNOWN_SEGMENT` y `FUTURE_TIMESTAMP`; detecta `SOURCE_CONFLICT` y elige el evento sano más reciente |

### VariableDeriver
**Propósito**: Derivar las variables del caso base con sus supuestos explícitos A1, A2 y A3 (SF-01.7).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `derive_variables(trip, resolution)` | "derivar variables del viaje" | Calcula `delay_minutes`, `new_arrival`, `missed_connection`, `international`, `group_includes_minor` y `compensation_requested` |

### RuleEngine
**Propósito**: Evaluar condiciones de reglas sin ejecución dinámica (`eval`) usando lógica trivaluada de Kleene (SF-01.8).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `evaluate_policy(policy, variables)` | "evaluar reglas de política y estado de decisión" | Evalúa `R1..R5`, determina si hay política rota (`REMEDY_RIGHTS`) y clasifica la decisión en `INFORMATIVA`, `AUTOMATICA`, `PENDIENTE_APROBACION` o `BLOQUEADA` |

### OptionFilter
**Propósito**: Filtrar opciones candidatas y elegir la opción propuesta (SF-01.9).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `filter_options(options_payload, evaluation_ctx)` | "filtrar opciones viables y elegir propuesta" | Verifica asientos ≥ pasajeros, derecho `REBOOK_NO_FEE` con costo 0, `policy_ref` vigente y no superada, TTL y coherencia de itinerario |

### MessageBuilder
**Propósito**: Construir y validar mensajes determinísticos con evidencia y `policy_ref` (SF-01.11).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `build_messages(context)` | "construir y validar mensajes" | Genera mensajes desde plantillas en español neutro y bloquea afirmaciones sin evidencia o sin `policy_ref` |

---

## 3. Application & API - Orquestación y Exposición

### DisruptionCompanionService
**Propósito**: Orquestar los flujos `F-01` (evaluar viaje), `F-02` (aceptar opción / escalar a humano) y `F-06` (escenarios de desarrollo).

| Método | Lenguaje Natural | Descripción |
|--------|------------------|-------------|
| `evaluate_trip(booking_id)` | "evaluar viaje como pasajero" | Ejecuta la cadena secuencial contexto → eventos → política → opciones → mensajes y devuelve `TripView` |
| `accept_option(booking_id, option_id, request)` | "aceptar opción propuesta" | Si la decisión es `AUTOMATICA` invoca `create_rebooking_request` con reintentos e idempotencia; si exige aprobación o está bloqueada invoca `create_human_case` |
| `activate_scenario(scenario_id)` | "activar escenario de desarrollo" | Selecciona el escenario activo en los adaptadores mock |

---

## Tipos de Datos Importantes

### TripView
Respuesta ensamblada para el pasajero y el visor frontend (SF-01.14):
- `decision_id`: Identificador UUID de la evaluación
- `booking_id`: Código de reserva
- `holder_first_name`: Nombre de pila del primer adulto (única excepción de PII en pantalla)
- `passenger_count`: Cantidad total de pasajeros del grupo
- `decision_state`: `INFORMATIVA` | `AUTOMATICA` | `PENDIENTE_APROBACION` | `BLOQUEADA` | `null`
- `segments`: Estado resuelto por segmento (`DELAYED`, `ON_TIME`, `NO_VERIFIED_INFO`, `NO_EVENTS`, `CONFLICT`) y puerta
- `derived_variables`: Variables derivadas con su valor, origen y supuestos (`A1`, `A2`, `A3`)
- `policy`: Versión de política, reglas evaluadas (`R1..R5`), derechos concedidos y si hay política rota
- `options`: Opciones viables y opciones descartadas con todas sus razones de descarte (`INSUFFICIENT_SEATS`, `FEE_CONFLICT`, `SUPERSEDED_POLICY`, `UNVERIFIED_POLICY`, `EXPIRED_TTL`)
- `proposed_option_id`: Identificador de la opción recomendada (`O1` en el caso base)
- `messages`: Mensajes validados con `evidence_refs` y `policy_ref`
- `actions`: Acción controlada disponible (`ACCEPT_OPTION` con efecto `CREATE_REBOOKING` o `CREATE_HUMAN_CASE`)

### AcceptResult
Respuesta al ejecutar la acción sobre una opción (`F-02`):
- `outcome`: `REBOOKING_CREATED` | `EXISTING_REQUEST` | `HUMAN_CASE_CREATED` | `STATE_CHANGED` | `FAILED`
- `message`: Mensaje validado del resultado
- `operation`: Datos de la solicitud de rebooking (`request_id`, `status`, `expires_at`, `idempotency_key`) o `null`
- `human_case`: Datos del caso humano (`case_id`, `queue`, `sla_minutes`, `reason`, `reasons`) o `null`

---

## Guía de Traducción: Lenguaje Natural → Código

| Cuando el usuario dice... | Usa... |
|--------------------------|--------|
| "consultar el contexto del viaje" | `ITripContextPort.get_trip_context` |
| "consultar los eventos operacionales" | `IOperationalEventsPort.get_operational_events` |
| "excluir fuentes degradadas / resolver eventos" | `EventResolver.resolve_events` |
| "derivar variables del viaje (retraso, llegada, conexión perdida, menor)" | `VariableDeriver.derive_variables` |
| "evaluar las reglas de política R1 a R5" | `RuleEngine.evaluate_policy` |
| "filtrar opciones elegibles y descartar no viables" | `OptionFilter.filter_options` |
| "construir y validar mensajes con policy_ref" | `MessageBuilder.build_messages` |
| "evaluar viaje como pasajero" | `DisruptionCompanionService.evaluate_trip` |
| "aceptar opción / iniciar acción controlada o caso humano" | `DisruptionCompanionService.accept_option` |
| "cambiar escenario de prueba" | `DisruptionCompanionService.activate_scenario` |

---

## Versionado

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2026-10-19 | Versión inicial del glosario para Disruption Companion V0 (15 specs) |
