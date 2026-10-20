# Feature Specification: SF-06.3 — Activación del escenario y reinicio del reloj

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: [F-06 Escenarios y reloj de desarrollo](42-f-06-escenarios-y-reloj-de-desarrollo.md) (subflujo)  
**Related Specs**: [F-06 Escenarios y reloj de desarrollo](42-f-06-escenarios-y-reloj-de-desarrollo.md), [SF-06.2 Listado del catálogo](44-sf-06-2-listado-del-catalogo.md), [SF-06.4 Avance del reloj de escenario](46-sf-06-4-avance-del-reloj-de-escenario.md)  
**Origen (DEC/H)**: DEC-04  
**Pruebas (TC)**: TC-27  
**Contratos externos**: §1.1 (fila 7), §2.4 (`CLOCK_MODE`)  
**Deuda conocida de A1 (no se resuelve aquí)**: DEBT-A1-02  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: Cambia el conjunto de datos de las simulaciones y reinicia el reloj de escenario al instante de lectura del contexto del escenario.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cada demostración parte de un estado conocido (Priority: P1)

Como evaluador, quiero que al elegir un escenario el reloj vuelva a su instante base para que las opciones nazcan vigentes.

**Why this priority**: Evita demostraciones inestables por vencimientos espurios.

**Independent Test**: Se prueba activando dos escenarios seguidos.

**Acceptance Scenarios**:

1. **Scenario**: Activación
   - **Given** un escenario válido
   - **When** se activa
   - **Then** el reloj queda en el instante de lectura del escenario con desplazamiento cero

2. **Scenario**: Escenario inexistente
   - **Given** un identificador fuera del catálogo
   - **When** se activa
   - **Then** respuesta de escenario no encontrado

3. **Scenario**: Reinicio del reloj (TC-27)
   - **Given** BASE_TC01 activo con el reloj avanzado 120 s
   - **When** se activa SIN_MENOR_TC07
   - **Then** el reloj vuelve a 11:02:35Z con desplazamiento 0

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### System Errors
- [MUST-IMPLEMENT] Cuando se activa un escenario → no se toca el registro persistente existente (FR-101)

#### Race Conditions
- [DEFERRED] Dos pestañas con escenarios distintos se pisan (AR-09) (FR-101)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-100**: El sistema DEBE definir interfaces para las siete herramientas externas con los contratos del enunciado y simulaciones intercambiables por un adaptador real cuando exista su documentación.
- **FR-101**: La fuente de verdad es el universo del enunciado: los escenarios de prueba reproducen los siete ejemplos (con datos personales claramente ficticios) y las variantes de prueba; los tipos de evento son retraso, cambio de puerta y estado; un test verifica que los datos ficticios no aparecen en registros ni en el historial.
- **FR-103**: Las simulaciones DEBEN respetar los metadatos de lectura y los errores de duplicado, indisponibilidad y validación.

### Key Entities *(include if feature involves data)*

- **Escenario de desarrollo**: Conjunto de datos simulados de las siete herramientas, activable solo en desarrollo. Campos principales:
  - `scenario_id`: texto
  - `booking_id`: texto
  - `title`: texto en español
  - `description`: texto
  - `ui`: booleano (visible en el selector)
  - `tests`: lista de TC-nn
- **Reloj de escenario**: Reloj controlado de desarrollo: instante base del escenario más un desplazamiento que solo avanza a pedido. Campos principales:
  - `mode`: scenario | system
  - `now`: marca de tiempo UTC
  - `offset_seconds`: entero ≥ 0
  - `advance_seconds`: entero entre 0 y 86400 (entrada)

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

- **SC-001**: Tras activar, el desplazamiento del reloj es 0 en el 100 % de los casos.

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-100 | DEC-04 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-101 | DEC-04 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-103 | DEC-04 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-27 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Validar escenario → Cambiar datos simulados → Reiniciar reloj
```

```mermaid
flowchart LR
    A1["Validar escenario"]
    A2["Cambiar datos simulados"]
    A3["Reiniciar reloj"]
    A1 --> A2
    A2 --> A3
```

