# Feature Specification: SF-10.2 — Cálculo de las tres métricas

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: [F-10 Reporte de métricas de éxito](60-f-10-reporte-de-metricas-de-exito.md) (subflujo)  
**Related Specs**: [F-10 Reporte de métricas de éxito](60-f-10-reporte-de-metricas-de-exito.md), [SF-10.1 Selección de decisiones con anomalía y deduplicación por huella](61-sf-10-1-seleccion-de-decisiones-con-anomalia-y-deduplica.md), [SF-10.3 Informe](63-sf-10-3-informe.md)  
**Origen (DEC/H)**: DEC-23, DEC-24  
**Pruebas (TC)**: TC-16  
**Contratos externos**: ARCHITECTURE.md §7  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: Calcula la resolución sin contacto humano, la tasa de casos por motivo y las afirmaciones sin evidencia.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Las cifras son verificables (Priority: P1)

Como responsable de producto, quiero ver definiciones claras de cada métrica.

**Why this priority**: Sin definición, la métrica no se puede discutir.

**Independent Test**: Se prueba con un registro de tamaño conocido.

**Acceptance Scenarios**:

1. **Scenario**: Métrica 1
   - **Given** situaciones accionables con opción viable y operación creada o expirada sin caso
   - **When** se calcula
   - **Then** es el cociente sobre las situaciones accionables

2. **Scenario**: Métrica 3
   - **Given** mensajes bloqueados por el validador
   - **When** se calcula
   - **Then** se suman y las afirmaciones sin evidencia son 0 por construcción

3. **Scenario**: Casos por motivo
   - **Given** 3 casos humanos CREADO, 2 por aprobación de política y 1 por conflicto de fuentes, sobre 10 situaciones
   - **When** se calcula M2
   - **Then** aprobación de política 2 de 10 y conflicto 1 de 10

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### Invalid Data
- [MUST-IMPLEMENT] Cuando solo hay informativas → no hay denominador y se reporta aparte (NFR-008)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-091**: Solo se persisten campos de una lista cerrada: hechos operacionales no personales, identificadores seudónimos, enumeraciones, números, marcas de tiempo y huellas. NUNCA se guardan cargas completas, nombre, contacto, documento ni edad del menor; los identificadores son seudónimos, no anónimos, y la reserva se trunca en los registros de aplicación.

### Non-Functional and Documentation Requirements

- **NFR-008**: Métricas de éxito: el sistema DEBE permitir medir desde el registro de decisiones el porcentaje de sesiones con problema donde el pasajero ve una opción viable y la acepta sin contacto humano, la tasa de casos humanos por motivo y que no haya afirmaciones sin evidencia.

### Key Entities *(include if feature involves data)*

- **Reporte de métricas**: Cálculo de las tres métricas de éxito desde el registro, sin información personal. Campos principales:
  - `situations_actionable`: entero
  - `m1_resolution_without_human`: razón entre 0 y 1
  - `m1_viable_option_shown`: razón entre 0 y 1
  - `m2_human_cases_by_reason`: lista de {reason: texto, rate: razón entre 0 y 1}
  - `m3_messages_blocked`: entero
  - `m3_unsupported_claims`: entero (debe ser 0)
  - `informative_count`: entero (se reporta aparte)

## Architectural Attributes *(mandatory)*

| Attribute | Value |
|-----------|-------|
| **Interaction type** | batch |
| **Consistency** | strong |
| **Workflow** | single-step |
| **Read pattern** | analytics |
| **Auditability** | full-history |
| **Domain complexity** | medium |
| **Modularity** | bounded-context |
| **Deployment** | monolith |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Los resultados coinciden con los esperados en un registro de prueba.

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-091 | DEC-23 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-008 | DEC-24 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-16 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Contar situaciones accionables → Calcular tres métricas
```

```mermaid
flowchart LR
    A1["Contar situaciones accionables"]
    A2["Calcular tres métricas"]
    A1 --> A2
```

