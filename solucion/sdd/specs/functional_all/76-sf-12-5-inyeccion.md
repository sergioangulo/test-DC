# Feature Specification: SF-12.5 — Inyección

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: [F-12 Carga y validación de la configuración](71-f-12-carga-y-validacion-de-la-configuracion.md) (subflujo)  
**Related Specs**: [F-12 Carga y validación de la configuración](71-f-12-carga-y-validacion-de-la-configuracion.md), [SF-12.4 Fallo de arranque](75-sf-12-4-fallo-de-arranque.md)  
**Origen (DEC/H)**: DEC-03, DEC-07, DEC-08, DEC-18, DEC-23, H-13  
**Pruebas (TC)**: TC-49  
**Contratos externos**: §2.4  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: Entrega los valores a los casos de uso y al dominio por inyección; el dominio no lee el entorno.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - La lógica de negocio no depende de dónde vienen los valores (Priority: P1)

Como arquitecto, quiero que el dominio reciba su configuración inyectada para probarlo con cualquier valor.

**Why this priority**: Es la base del test de TC-49.

**Independent Test**: Se prueba construyendo la configuración con valores distintos.

**Acceptance Scenarios**:

1. **Scenario**: Inyección
   - **Given** una configuración con un valor cambiado
   - **When** se construye el dominio
   - **Then** su comportamiento cambia sin tocar el código

2. **Scenario**: Umbral inyectado (TC-49)
   - **Given** el dominio construido con `MCT_UNCERTAINTY_MINUTES` en 45 y otro en 0
   - **When** se evalúa un margen de 10 min
   - **Then** con 45 es desconocido y con 0 es falso

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### Invalid Data
- [MUST-IMPLEMENT] Cuando el dominio fija un literal de los supuestos S-09 a S-19 → falla la prueba de calidad (NFR-007)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-022**: El margen de conexión es la salida programada del segmento siguiente menos la nueva llegada del segmento afectado (horas locales del mismo aeropuerto, con fecha). Si el afectado es el último segmento no hay conexión y la conexión perdida es falsa. La conexión perdida es verdadera si el margen es menor que el tiempo mínimo de conexión; desconocida si ese tiempo no fue provisto y el margen está entre cero y `MCT_UNCERTAINTY_MINUTES` (45); falsa en el resto. Siempre es una estimación.
- **FR-054**: Un resultado indeterminado (falla temporal del proveedor, tiempo agotado o respuesta perdida) DEBE reintentarse hasta `REBOOK_MAX_RETRIES` (2) veces con la misma llave; luego se deriva a caso humano (cubierto por el clic de FR-050). Nunca se informa éxito ni fracaso.
- **FR-064**: La operación de cambio DEBE seguir un ciclo de vida: en curso, creada, indeterminada, fallida y expirada. En curso pasa a indeterminada tras `OPERATION_STALE_SECONDS` (120) sin respuesta; creada pasa a expirada en su vencimiento; indeterminada pasa a expirada tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900, mayor que la vigencia de una solicitud) si nada la resuelve. Si la llave no pudo persistirse no se escribe. Expirada o fallida permiten una operación nueva con la generación siguiente; creada, en curso e indeterminada la bloquean y la vista muestra su estado. Un rechazo por duplicado sin operación local se muestra «ya existe una solicitud para esta opción».
- **FR-092**: El sistema DEBE aplicar una retención provisional (`AUDIT_RETENTION_DAYS`, 30) con una rutina de purga verificable del registro de decisiones, de operaciones, de casos y de notificaciones, que primero aplica los vencimientos de las operaciones (FR-064) y después conserva el registro mínimo solo de las operaciones que siguen no finalizadas (en curso, indeterminada o creada dentro de su vigencia) para no perder su bloqueo; una operación ya vencida se purga por antigüedad como cualquier otra.

### Non-Functional and Documentation Requirements

- **NFR-012**: Configuración: todos los parámetros de los supuestos S-09 a S-19 DEBEN ser variables configurables (archivo de configuración con sobrescritura por entorno, validadas al arrancar y con valor por defecto documentado) y ninguno puede estar fijado en la lógica; entre ellos `RELEVANT_DELAY_MIN_MINUTES` (1), `MIN_CONNECTION_MINUTES` (0 por aeropuerto), `MCT_UNCERTAINTY_MINUTES` (45), `CLOCK_SKEW_SECONDS` (60), `EVENT_MAX_AGE_SECONDS` (sin límite), `OPERATION_STALE_SECONDS` (120), `REBOOK_MAX_RETRIES` (2), `AUDIT_RETENTION_DAYS` (30), `PARSER_MAX_CONDITION_CHARS` (200), `PARSER_MAX_DEPTH` (10), `REMEDY_RIGHTS`, `COMPENSATION_RIGHTS`, `NOTIFY_ENABLED`, `NOTIFY_COOLDOWN_SECONDS` (86400), `NOTIFY_MAX_RETRIES` (2), `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900), `EVALUATE_RATE_LIMIT_PER_MINUTE` (30), `CHANGE_RIGHTS`, `SUPPORTED_EVENT_TYPES`, `NOTIFY_ONLY_EVENT_TYPES`, `POLICY_SCENARIOS`, `REASON_PRIORITY`, la tabla de compatibilidad de afirmaciones y los secretos `SERVICE_API_KEY` e `IDEMPOTENCY_SECRET` (solo por entorno). Una prueba cambia cada parámetro y comprueba que cambia el comportamiento. También son configurables los parámetros operativos de `sdd/reports/EXTERNAL_CONTRACTS.md` §2.4 (tiempos de espera, reintentos de lectura, modo de reloj, origen permitido, ubicación del registro y banderas de desarrollo).
- **NFR-007**: Estilo SDD: el desarrollo DEBE seguir TDD con revisión WTF, funciones de a lo sumo 10 líneas y 3 parámetros (verificado por una prueba que mide el código) y lógica de negocio independiente de la tecnología mediante puertos y adaptadores.

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

- **SC-001**: Ningún literal de los parámetros aparece en la lógica de negocio.

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-022 | DEC-07, DEC-08, H-13 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-054 | DEC-18 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-064 | DEC-18 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-092 | DEC-23 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-012 | Usuario (2026-10-19) | TC-49 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-007 | DEC-03 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-49 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Construir configuración → Entregar al dominio
```

```mermaid
flowchart LR
    A1["Construir configuración"]
    A2["Entregar al dominio"]
    A1 --> A2
```

