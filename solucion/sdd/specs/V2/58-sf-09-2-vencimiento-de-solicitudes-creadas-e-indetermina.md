# Feature Specification: SF-09.2 — Vencimiento de solicitudes creadas e indeterminadas

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: [F-09 Ciclo de vida de operaciones, intentos de caso y notificaciones (barrido perezoso)](56-f-09-ciclo-de-vida-de-operaciones-intentos-de-caso-y.md) (subflujo)  
**Related Specs**: [F-09 Ciclo de vida de operaciones, intentos de caso y notificaciones (barrido perezoso)](56-f-09-ciclo-de-vida-de-operaciones-intentos-de-caso-y.md), [SF-09.1 Detección de operaciones, casos y notificaciones colgados](57-sf-09-1-deteccion-de-operaciones-casos-y-notificaciones.md), [SF-09.3 Generación siguiente de la llave](59-sf-09-3-generacion-siguiente-de-la-llave.md)  
**Origen (DEC/H)**: DEC-18  
**Pruebas (TC)**: TC-38, TC-57  
**Contratos externos**: §2.1 (herramienta 5: vencimiento)  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: Pasa a expirada una solicitud creada cuando llega su vencimiento y una operación indeterminada cuando supera `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - La solicitud pendiente y la indeterminada caducan en su plazo (Priority: P1)

Como pasajero, quiero saber cuándo mi solicitud pendiente o indeterminada dejó de estar vigente y poder volver a intentar.

**Why this priority**: La confirmación está fuera de la versión 1; el vencimiento es el cierre de una solicitud creada y el plazo de expiración libera una indeterminada.

**Independent Test**: Se prueba avanzando el reloj hasta el vencimiento y hasta el plazo de expiración.

**Acceptance Scenarios**:

1. **Scenario**: Expiración
   - **Given** solicitud creada con vencimiento
   - **When** el reloj lo alcanza
   - **Then** pasa a expirada y no bloquea la siguiente

2. **Scenario**: Indeterminada vence
   - **Given** una operación indeterminada con 899 segundos de antigüedad y otra con 900
   - **When** se lee el registro
   - **Then** la primera sigue bloqueando y la segunda pasa a expirada y permite la generación siguiente

3. **Scenario**: 899 s contra 900 s e identidad conservada (TC-57)
   - **Given** dos operaciones indeterminadas de 899 s y 900 s y una purga previa que dejó `minimized` verdadero (solo identidad, estado y vigencia)
   - **When** se lee el registro
   - **Then** la de 900 s pasa a expirada y la de 899 s sigue bloqueando; el estado se conserva aunque la operación esté minimizada

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### System Errors
- [DEFERRED] Consulta del estado real de la solicitud pendiente (no existe herramienta, AR-11) (FR-056)

#### Invalid Data
- [MUST-IMPLEMENT] Cuando el instante es exactamente el vencimiento → ya está expirada (FR-064)
- [MUST-IMPLEMENT] Cuando `OPERATION_INDETERMINATE_EXPIRY_SECONDS` no es mayor que `OPERATION_STALE_SECONDS` → el servicio no arranca (NFR-012)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-064**: La operación de cambio DEBE seguir un ciclo de vida: en curso, creada, indeterminada, fallida y expirada. En curso pasa a indeterminada tras `OPERATION_STALE_SECONDS` (120) sin respuesta; creada pasa a expirada en su vencimiento; indeterminada pasa a expirada tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900, mayor que la vigencia de una solicitud) si nada la resuelve. Si la llave no pudo persistirse no se escribe. Expirada o fallida permiten una operación nueva con la generación siguiente; creada, en curso e indeterminada la bloquean y la vista muestra su estado. Un rechazo por duplicado sin operación local se muestra «ya existe una solicitud para esta opción».

### Non-Functional and Documentation Requirements

- **NFR-012**: Configuración: todos los parámetros de los supuestos S-09 a S-19 DEBEN ser variables configurables (archivo de configuración con sobrescritura por entorno, validadas al arrancar y con valor por defecto documentado) y ninguno puede estar fijado en la lógica; entre ellos `RELEVANT_DELAY_MIN_MINUTES` (1), `MIN_CONNECTION_MINUTES` (0 por aeropuerto), `MCT_UNCERTAINTY_MINUTES` (45), `CLOCK_SKEW_SECONDS` (60), `EVENT_MAX_AGE_SECONDS` (sin límite), `OPERATION_STALE_SECONDS` (120), `REBOOK_MAX_RETRIES` (2), `AUDIT_RETENTION_DAYS` (30), `PARSER_MAX_CONDITION_CHARS` (200), `PARSER_MAX_DEPTH` (10), `REMEDY_RIGHTS`, `COMPENSATION_RIGHTS`, `NOTIFY_ENABLED`, `NOTIFY_COOLDOWN_SECONDS` (86400), `NOTIFY_MAX_RETRIES` (2), `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900), `EVALUATE_RATE_LIMIT_PER_MINUTE` (30), `CHANGE_RIGHTS`, `SUPPORTED_EVENT_TYPES`, `NOTIFY_ONLY_EVENT_TYPES`, `POLICY_SCENARIOS`, `REASON_PRIORITY`, la tabla de compatibilidad de afirmaciones y los secretos `SERVICE_API_KEY` e `IDEMPOTENCY_SECRET` (solo por entorno). Una prueba cambia cada parámetro y comprueba que cambia el comportamiento. También son configurables los parámetros operativos de `sdd/reports/EXTERNAL_CONTRACTS.md` §2.4 (tiempos de espera, reintentos de lectura, modo de reloj, origen permitido, ubicación del registro y banderas de desarrollo).

### Key Entities *(include if feature involves data)*

- **Operación de reprogramación**: Intento de crear una solicitud de cambio, con su llave de idempotencia y su ciclo de vida. Campos principales:
  - `itinerary_key`: texto
  - `idempotency_key`: texto no adivinable
  - `generation`: entero ≥ 1
  - `state`: EN_CURSO | CREADA | INDETERMINADA | FALLIDA | EXPIRADA (INDETERMINADA pasa a EXPIRADA tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS`)
  - `request_id`: texto | nulo
  - `request_status`: enumeración abierta (p. ej. PENDING_CONFIRMATION) | nulo
  - `expires_at`: marca de tiempo UTC | nulo
  - `passenger_ids`: lista de texto con TODO el grupo
  - `minimized`: booleano: verdadero cuando la purga conservó solo la identidad, el estado y la vigencia de la operación (sin itinerario ni pasajeros) para no perder su bloqueo

## Architectural Attributes *(mandatory)*

| Attribute | Value |
|-----------|-------|
| **Interaction type** | sync-http |
| **Consistency** | strong |
| **Workflow** | single-step |
| **Read pattern** | simple |
| **Auditability** | full-history |
| **Domain complexity** | medium |
| **Modularity** | bounded-context |
| **Deployment** | monolith |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100 % de las solicitudes creadas pasa a expirada en su vencimiento.
- **SC-002**: El 100 % de las indeterminadas pasa a expirada al alcanzar `OPERATION_INDETERMINATE_EXPIRY_SECONDS`.

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-064 | DEC-18 | TC-38, TC-57 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-012 | Usuario (2026-10-19) | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-38, TC-57 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-002 | criterio medible de este spec | TC-38, TC-57 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Leer vencimiento → Comparar con el reloj → Pasar a expirada
```

```mermaid
flowchart LR
    A1["Leer vencimiento"]
    A2["Comparar con el reloj"]
    A3["Pasar a expirada"]
    A1 --> A2
    A2 --> A3
```

