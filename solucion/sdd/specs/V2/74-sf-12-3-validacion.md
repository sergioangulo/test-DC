# Feature Specification: SF-12.3 — Validación

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: [F-12 Carga y validación de la configuración](71-f-12-carga-y-validacion-de-la-configuracion.md) (subflujo)  
**Related Specs**: [F-12 Carga y validación de la configuración](71-f-12-carga-y-validacion-de-la-configuracion.md), [SF-12.2 Sobrescritura por entorno](73-sf-12-2-sobrescritura-por-entorno.md), [SF-12.4 Fallo de arranque](75-sf-12-4-fallo-de-arranque.md)  
**Origen (DEC/H)**: DEC-02, DEC-05, DEC-12, DEC-29  
**Pruebas (TC)**: TC-49  
**Contratos externos**: §2.4 (columna de validación)  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: Valida tipo, rango, lista no vacía y longitud mínima de cada parámetro.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Un valor malo se descubre al arrancar, no en producción (Priority: P1)

Como operador, quiero enterarme al arrancar de que un parámetro es inválido.

**Why this priority**: Un umbral mal escrito cambia los derechos concedidos.

**Independent Test**: Se prueba con un valor inválido por parámetro.

**Acceptance Scenarios**:

1. **Scenario**: Rango
   - **Given** `REBOOK_MAX_RETRIES` = 9
   - **When** se valida
   - **Then** se rechaza (rango entre 0 y 5)

2. **Scenario**: Lista
   - **Given** `REMEDY_RIGHTS` vacía
   - **When** se valida
   - **Then** se rechaza

3. **Scenario**: Valor fuera de rango (TC-49)
   - **Given** `REBOOK_MAX_RETRIES` en 9 (rango de 0 a 5) y `OPERATION_INDETERMINATE_EXPIRY_SECONDS` en 100 con `OPERATION_STALE_SECONDS` de 120
   - **When** se valida
   - **Then** ambos se rechazan nombrando el parámetro

4. **Scenario**: Validación de parámetros operativos (TC-49)
   - **Given** `UPSTREAM_WRITE_TIMEOUT_MS` en 50 (mínimo 100), `READ_MAX_REQUERIES` en 5 (rango de 0 a 3) y `CLOCK_MODE` en wall
   - **When** se valida
   - **Then** los 3 se rechazan nombrando el parámetro

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### Invalid Data
- [MUST-IMPLEMENT] Cuando la prioridad de motivos no es una permutación exacta → se rechaza (NFR-012)
- [MUST-IMPLEMENT] Cuando un valor numérico no es entero → se rechaza (NFR-012)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-030**: El sistema DEBE evaluar las condiciones de política con un analizador acotado de lista blanca: variables permitidas (retraso, carácter internacional, conexión perdida, compensación solicitada, grupo con menor), comparadores de igualdad, desigualdad y orden, conectores Y/O (Y precede a O), literales enteros y verdadero/falso, y paréntesis; `EQ` equivale a igualdad y `NE` a desigualdad. Comparar un booleano con un entero, o usar orden sobre un booleano, es error de regla. Las condiciones miden como máximo `PARSER_MAX_CONDITION_CHARS` (200) caracteres y `PARSER_MAX_DEPTH` (10) niveles; todo lo demás es error.
- **FR-039**: Hay política rota si al menos una regla cumplida concede un derecho de remedio (`REMEDY_RIGHTS`; por defecto cambio sin costo, vale de comida y compensación en dinero). Un retraso sin política rota deja la decisión INFORMATIVA: se informa el retraso y se muestran las reglas evaluadas, sin consultar opciones, sin rebooking, compensación, soporte ni notificación de política, hasta que exista política rota. Los derechos que no son de remedio (trato prioritario) modifican el trato pero no rompen la política por sí solos.
- **FR-067**: El motivo de compensación del menú de soporte solo DEBE mostrarse si la política tiene una regla que concede un derecho de compensación (`COMPENSATION_RIGHTS`) que, evaluada con la solicitud de compensación verdadera y las demás variables, resulta verdadera, y la decisión no es INFORMATIVA.

### Non-Functional and Documentation Requirements

- **NFR-012**: Configuración: todos los parámetros de los supuestos S-09 a S-19 DEBEN ser variables configurables (archivo de configuración con sobrescritura por entorno, validadas al arrancar y con valor por defecto documentado) y ninguno puede estar fijado en la lógica; entre ellos `RELEVANT_DELAY_MIN_MINUTES` (1), `MIN_CONNECTION_MINUTES` (0 por aeropuerto), `MCT_UNCERTAINTY_MINUTES` (45), `CLOCK_SKEW_SECONDS` (60), `EVENT_MAX_AGE_SECONDS` (sin límite), `OPERATION_STALE_SECONDS` (120), `REBOOK_MAX_RETRIES` (2), `AUDIT_RETENTION_DAYS` (30), `PARSER_MAX_CONDITION_CHARS` (200), `PARSER_MAX_DEPTH` (10), `REMEDY_RIGHTS`, `COMPENSATION_RIGHTS`, `NOTIFY_ENABLED`, `NOTIFY_COOLDOWN_SECONDS` (86400), `NOTIFY_MAX_RETRIES` (2), `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900), `EVALUATE_RATE_LIMIT_PER_MINUTE` (30), `CHANGE_RIGHTS`, `SUPPORTED_EVENT_TYPES`, `NOTIFY_ONLY_EVENT_TYPES`, `POLICY_SCENARIOS`, `REASON_PRIORITY`, la tabla de compatibilidad de afirmaciones y los secretos `SERVICE_API_KEY` e `IDEMPOTENCY_SECRET` (solo por entorno). Una prueba cambia cada parámetro y comprueba que cambia el comportamiento. También son configurables los parámetros operativos de `sdd/reports/EXTERNAL_CONTRACTS.md` §2.4 (tiempos de espera, reintentos de lectura, modo de reloj, origen permitido, ubicación del registro y banderas de desarrollo).

### Key Entities *(include if feature involves data)*

- **Configuración**: Conjunto central de parámetros con valor por defecto, sobrescritura por entorno y validación al arrancar. Campos principales:
  - `name`: nombre del parámetro (p. ej. `RELEVANT_DELAY_MIN_MINUTES`)
  - `default`: valor por defecto documentado
  - `effective_value`: valor tras aplicar el entorno
  - `validation`: tipo, rango, lista no vacía o longitud mínima
  - `is_secret`: booleano (solo por entorno, nunca se muestra)
  - `effect`: comportamiento que cambia

## Architectural Attributes *(mandatory)*

| Attribute | Value |
|-----------|-------|
| **Interaction type** | batch |
| **Consistency** | strong |
| **Workflow** | single-step |
| **Read pattern** | simple |
| **Auditability** | full-history |
| **Domain complexity** | medium |
| **Modularity** | bounded-context |
| **Deployment** | monolith |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100 % de los valores inválidos probados es rechazado.

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-030 | DEC-12 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-039 | DEC-02, DEC-05 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-067 | DEC-29 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-012 | Usuario (2026-10-19) | TC-49 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-49 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Validar tipo → Validar rango y listas → Validar longitud de secretos
```

```mermaid
flowchart LR
    A1["Validar tipo"]
    A2["Validar rango y listas"]
    A3["Validar longitud de secretos"]
    A1 --> A2
    A2 --> A3
```

