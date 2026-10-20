# Feature Specification: SF-09.3 — Generación siguiente de la llave

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: [F-09 Ciclo de vida de operaciones, intentos de caso y notificaciones (barrido perezoso)](56-f-09-ciclo-de-vida-de-operaciones-intentos-de-caso-y.md) (subflujo)  
**Related Specs**: [F-09 Ciclo de vida de operaciones, intentos de caso y notificaciones (barrido perezoso)](56-f-09-ciclo-de-vida-de-operaciones-intentos-de-caso-y.md), [SF-09.2 Vencimiento de solicitudes creadas e indeterminadas](58-sf-09-2-vencimiento-de-solicitudes-creadas-e-indetermina.md)  
**Origen (DEC/H)**: DEC-18  
**Pruebas (TC)**: TC-22, TC-34, TC-38  
**Contratos externos**: §2.1 (herramienta 5: llave idempotente)  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: Permite una operación nueva con la llave de la generación siguiente cuando la anterior está expirada o fallida.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Se puede volver a intentar sin duplicar (Priority: P1)

Como pasajero, quiero poder pedir de nuevo el cambio cuando el anterior venció o falló, sin que se confunda con el viejo.

**Why this priority**: La generación distingue intentos legítimos de duplicados.

**Independent Test**: Se prueba con una operación expirada seguida de una nueva aceptación.

**Acceptance Scenarios**:

1. **Scenario**: Nueva generación
   - **Given** la operación previa está expirada (incluida una indeterminada vencida) o fallida
   - **When** se acepta de nuevo
   - **Then** se usa la llave con la generación siguiente

2. **Scenario**: Bloqueo
   - **Given** la operación previa está creada, en curso o indeterminada
   - **When** se acepta de nuevo
   - **Then** se bloquea y se muestra su estado

3. **Scenario**: Generación 2 (TC-34)
   - **Given** una operación expirada de generación 1 para LA2412
   - **When** se acepta de nuevo
   - **Then** se usa la llave de la generación 2 y una creada de generación 1 sigue bloqueando

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### Race Conditions
- [MUST-IMPLEMENT] Cuando dos aceptaciones piden la generación siguiente → solo una la reserva (FR-062)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-053**: La identidad de una operación de cambio es la reserva más el itinerario de la opción. Al crearla se calcula una llave de idempotencia no adivinable a partir de reserva, vuelo, fecha, salida, versión de política y generación (sin identificador de decisión ni marcas de tiempo), se guarda en el registro de operaciones de forma atómica y única antes de llamar, y toda reevaluación la reutiliza mientras la operación no haya fracasado, aunque cambie la versión de política.
- **FR-062**: Dos aceptaciones simultáneas, o una aceptación mientras la operación está en curso, indeterminada o creada, DEBEN resultar en una sola escritura; la segunda devuelve el estado de la primera y el botón se deshabilita mientras hay una solicitud en curso.
- **FR-064**: La operación de cambio DEBE seguir un ciclo de vida: en curso, creada, indeterminada, fallida y expirada. En curso pasa a indeterminada tras `OPERATION_STALE_SECONDS` (120) sin respuesta; creada pasa a expirada en su vencimiento; indeterminada pasa a expirada tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900, mayor que la vigencia de una solicitud) si nada la resuelve. Si la llave no pudo persistirse no se escribe. Expirada o fallida permiten una operación nueva con la generación siguiente; creada, en curso e indeterminada la bloquean y la vista muestra su estado. Un rechazo por duplicado sin operación local se muestra «ya existe una solicitud para esta opción».

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

- **SC-001**: Cero operaciones duplicadas en generaciones sucesivas.

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-053 | DEC-18 | TC-22, TC-34 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-062 | DEC-18 | TC-22 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-064 | DEC-18 | TC-38 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-22, TC-34, TC-38 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Revisar estado previo → Calcular generación → Permitir o bloquear
```

```mermaid
flowchart LR
    A1["Revisar estado previo"]
    A2["Calcular generación"]
    A3["Permitir o bloquear"]
    A1 --> A2
    A2 --> A3
```

