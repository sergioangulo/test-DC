# Feature Specification: SF-12.1 — Lectura de los valores por defecto

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: [F-12 Carga y validación de la configuración](71-f-12-carga-y-validacion-de-la-configuracion.md) (subflujo)  
**Related Specs**: [F-12 Carga y validación de la configuración](71-f-12-carga-y-validacion-de-la-configuracion.md), [SF-12.2 Sobrescritura por entorno](73-sf-12-2-sobrescritura-por-entorno.md)  
**Origen (DEC/H)**: DEC-05, DEC-09, DEC-10, DEC-31, H-09  
**Pruebas (TC)**: TC-49  
**Contratos externos**: §2.4  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: Carga el archivo de valores por defecto con el valor documentado de cada parámetro.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cada parámetro tiene un valor por defecto conocido (Priority: P1)

Como operador, quiero que el servicio arranque sin configuración con valores razonables y documentados.

**Why this priority**: Facilita el uso local y las pruebas.

**Independent Test**: Se prueba arrancando sin entorno.

**Acceptance Scenarios**:

1. **Scenario**: Defectos
   - **Given** sin variables de entorno
   - **When** se leen
   - **Then** cada parámetro tiene su valor documentado (por ejemplo `RELEVANT_DELAY_MIN_MINUTES` = 1)

2. **Scenario**: Valores por defecto (TC-49)
   - **Given** sin variables de entorno
   - **When** se arranca
   - **Then** `RELEVANT_DELAY_MIN_MINUTES` es 1, `MCT_UNCERTAINTY_MINUTES` es 45 y `AUDIT_RETENTION_DAYS` es 30

3. **Scenario**: Parámetros operativos por defecto (TC-49)
   - **Given** sin variables de entorno
   - **When** se leen los valores por defecto operativos
   - **Then** `UPSTREAM_READ_TIMEOUT_MS` es 2000, `UPSTREAM_WRITE_TIMEOUT_MS` es 5000, `READ_MAX_REQUERIES` es 1, `WRITE_RETRY_BACKOFF_MS` es 200, `DEV_SESSION_HEADER_ENABLED` y `DEV_ENDPOINTS_ENABLED` son falso, `CLOCK_MODE` es system, `CORS_ALLOWED_ORIGINS` es el origen del front de prueba y `DB_PATH` apunta al registro local

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### System Errors
- [MUST-IMPLEMENT] Cuando falta el archivo de valores por defecto → no arranca (NFR-012)

#### Invalid Data
- [MUST-IMPLEMENT] Cuando el archivo trae un parámetro desconocido → se ignora y se reporta (NFR-012)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-005**: El sistema DEBE tratar como evento relevante un retraso validado con minutos de retraso mayores o iguales a `RELEVANT_DELAY_MIN_MINUTES` (1); qué derechos otorga lo decide la política vigente (FR-034).
- **FR-016**: El sistema DEBE descartar los eventos de un segmento que no fue solicitado (`UNKNOWN_SEGMENT`) y los eventos con instante de registro posterior al de la lectura más la tolerancia `CLOCK_SKEW_SECONDS` (60) (`FUTURE_TIMESTAMP`).
- **FR-017**: El sistema DEBE usar siempre el dato más reciente y respetar la vigencia: las opciones vencen en el instante de su lectura más su vigencia en segundos (en el instante exacto ya están vencidas; sin vigencia declarada el conjunto se considera vencido). Los eventos no vencen por sí mismos (`EVENT_MAX_AGE_SECONDS`, por defecto sin límite). Al vencer se re-consulta una sola vez por acción, sin bucles.

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

- **SC-001**: Todo parámetro del contrato de configuración tiene valor por defecto documentado.

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-005 | DEC-05, DEC-31, H-09 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-016 | DEC-09 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-017 | DEC-10 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-012 | Usuario (2026-10-19) | TC-49 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-49 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Abrir archivo → Interpretar valores
```

```mermaid
flowchart LR
    A1["Abrir archivo"]
    A2["Interpretar valores"]
    A1 --> A2
```

