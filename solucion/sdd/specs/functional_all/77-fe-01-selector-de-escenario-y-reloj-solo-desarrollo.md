# Feature Specification: FE-01 — Selector de escenario y reloj (solo desarrollo)

**Created**: 2026-10-19  
**Status**: draft  
**Flow**: FE-01 Selector de escenario y reloj (solo desarrollo)  
**Related Specs**: [FE-01.1 Carga del catálogo](78-fe-01-1-carga-del-catalogo.md), [FE-01.2 Activación del escenario](79-fe-01-2-activacion-del-escenario.md), [FE-01.3 Fijación de la sesión simulada](80-fe-01-3-fijacion-de-la-sesion-simulada.md), [FE-01.4 Avance del reloj de escenario](81-fe-01-4-avance-del-reloj-de-escenario.md), [F-06 Escenarios y reloj de desarrollo](42-f-06-escenarios-y-reloj-de-desarrollo.md), [FE-02 Vista de viaje](82-fe-02-vista-de-viaje.md)  
**Origen (DEC/H)**: DEC-04, DEC-21  
**Pruebas (TC)**: TC-01, TC-08, TC-27  
**Contratos externos**: §1.1 (filas 6 a 8: solo desarrollo)  

## Reglas de este documento

> Este spec es FUNCIONAL, no técnico: describe QUÉ hace el sistema, no CÓMO. Usa lenguaje de negocio; las siete herramientas externas se nombran por su función y se referencian por la sección de `sdd/reports/EXTERNAL_CONTRACTS.md`. Los casos borde se DOCUMENTAN; los valores de configuración se citan por el nombre del parámetro (NFR-012) con su valor por defecto entre paréntesis.

**Alcance**: En el front de prueba y solo en desarrollo: lista los escenarios visibles, activa el elegido, fija la sesión simulada, recarga la vista y ofrece «Avanzar reloj» para demostrar la vigencia. No aparece en la versión de producción.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - El evaluador elige una situación y la ve al instante (Priority: P1)

Como evaluador, quiero elegir un escenario de una lista y ver la pantalla correspondiente, y avanzar el reloj para ver cómo vence la hora límite.

**Why this priority**: Sin selector no hay demostración de las situaciones del reto.

**Independent Test**: Se prueba eligiendo el caso base, cambiando a otro y avanzando el reloj.

**Acceptance Scenarios**:

1. **Scenario**: Elegir escenario
   - **Given** el selector muestra los escenarios visibles
   - **When** el evaluador elige uno
   - **Then** se activa, se fija la sesión simulada de su reserva y la vista se recarga

2. **Scenario**: Avanzar reloj
   - **Given** hay un escenario activo
   - **When** el evaluador pulsa «Avanzar reloj»
   - **Then** el reloj avanza y la cuenta regresiva de la hora límite llega a cero

3. **Scenario**: Producción
   - **Given** versión de producción
   - **When** se abre la aplicación
   - **Then** el selector no existe

4. **Scenario**: Elegir el caso base y avanzar 120 s (TC-01, TC-08)
   - **Given** el selector con los escenarios visibles
   - **When** el evaluador elige BASE_TC01 y pulsa «Avanzar reloj» una vez de 120 s
   - **Then** ve la vista del caso base con «Quedan 01:48 (hasta 11:04 UTC)» y luego la hora límite vencida

---

### Edge Cases

> Solo se documentan; los marcados MUST-IMPLEMENT se vuelven requisito FR-XXX y se implementan con TDD, los DEFERRED quedan para una iteración posterior.

#### System Errors
- [MUST-IMPLEMENT] Cuando el catálogo no se puede cargar → el selector muestra un aviso y la vista no se bloquea (FR-111)

#### Invalid Data
- [DEFERRED] Estado global de un único escenario por proceso (AR-09): no apto para varias personas a la vez (FR-101)

#### Security & Permissions
- [MUST-IMPLEMENT] Cuando la versión es de producción → el selector y el avance del reloj no se incluyen (FR-001)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-VIS-001**: La interfaz DEBE aplicar estilos coherentes con la identidad visual definida: CSS propio alineado con `sdd/reports/DESIGN_CONTRACT.md` (tokens de color, tipografía, espaciado y radios), sin logos ni marcas de terceros.
- **FR-VIS-002**: Está PROHIBIDO entregar HTML sin estilos: cada pantalla y cada estado de este flujo DEBE renderizarse con los estilos de la identidad, nunca con el aspecto por defecto del navegador.
- **FR-VIS-003**: La interfaz DEBE ser consistente con `sdd/reports/DESIGN_CONTRACT.md`: usa solo los componentes de su inventario y solo sus tokens; toda diferencia respecto del contrato es un defecto de la implementación, no del contrato.
- **FR-001**: El sistema DEBE operar sobre la sesión autenticada del pasajero y comprobar que la reserva y la decisión solicitadas pertenezcan a esa sesión; una reserva ajena y una inexistente DEBEN producir exactamente la misma respuesta de «no encontrado», sin confirmar la existencia de ninguna. La sesión simulada solo existe con el parámetro `DEV_SESSION_HEADER_ENABLED` (apagado por defecto): en cualquier otro perfil toda petición del pasajero sin sesión DEBE rechazarse por falta de autenticación, y toda petición del sistema DEBE exigir la credencial de servicio (FR-120). Los errores NO DEBEN mostrar trazas ni repetir la entrada, nunca se pide ni se muestra documento de identidad, y el identificador de decisión DEBE ser aleatorio y no adivinable.
- **FR-101**: La fuente de verdad es el universo del enunciado: los escenarios de prueba reproducen los siete ejemplos (con datos personales claramente ficticios) y las variantes de prueba; los tipos de evento son retraso, cambio de puerta y estado; un test verifica que los datos ficticios no aparecen en registros ni en el historial.
- **FR-111**: El front de prueba DEBE tener el aspecto y la sensación del centro de ayuda de una aerolínea (sin logos ni marcas), verificable con la lista de componentes y la lista de verificación de tokens de `sdd/reports/DESIGN_CONTRACT.md`: selector de escenario, contexto, alerta, reglas cumplidas y no cumplidas, opción propuesta, vía de reembolso, avisos de estimación, hora límite y «sujeto a disponibilidad», y botones de acción.

### Non-Functional and Documentation Requirements

- **NFR-011**: Accesibilidad básica: la interfaz DEBE ofrecer roles semánticos, foco visible, navegación por teclado y contraste AA (relación de al menos 4,5:1 verificada sobre los tokens por una prueba que la calcula).
- **NFR-012**: Configuración: todos los parámetros de los supuestos S-09 a S-19 DEBEN ser variables configurables (archivo de configuración con sobrescritura por entorno, validadas al arrancar y con valor por defecto documentado) y ninguno puede estar fijado en la lógica; entre ellos `RELEVANT_DELAY_MIN_MINUTES` (1), `MIN_CONNECTION_MINUTES` (0 por aeropuerto), `MCT_UNCERTAINTY_MINUTES` (45), `CLOCK_SKEW_SECONDS` (60), `EVENT_MAX_AGE_SECONDS` (sin límite), `OPERATION_STALE_SECONDS` (120), `REBOOK_MAX_RETRIES` (2), `AUDIT_RETENTION_DAYS` (30), `PARSER_MAX_CONDITION_CHARS` (200), `PARSER_MAX_DEPTH` (10), `REMEDY_RIGHTS`, `COMPENSATION_RIGHTS`, `NOTIFY_ENABLED`, `NOTIFY_COOLDOWN_SECONDS` (86400), `NOTIFY_MAX_RETRIES` (2), `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900), `EVALUATE_RATE_LIMIT_PER_MINUTE` (30), `CHANGE_RIGHTS`, `SUPPORTED_EVENT_TYPES`, `NOTIFY_ONLY_EVENT_TYPES`, `POLICY_SCENARIOS`, `REASON_PRIORITY`, la tabla de compatibilidad de afirmaciones y los secretos `SERVICE_API_KEY` e `IDEMPOTENCY_SECRET` (solo por entorno). Una prueba cambia cada parámetro y comprueba que cambia el comportamiento. También son configurables los parámetros operativos de `sdd/reports/EXTERNAL_CONTRACTS.md` §2.4 (tiempos de espera, reintentos de lectura, modo de reloj, origen permitido, ubicación del registro y banderas de desarrollo).

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
- **Pantalla del front de prueba**: Estado visible del front según la vista recibida. Campos principales:
  - `screen_state`: carga | sin anomalía | informativa | solo puerta | retraso con opción | conflicto | sin opción viable | solicitud registrada | lectura fallida | error de carga
  - `components`: lista de componentes del inventario del DESIGN_CONTRACT presentes
  - `texts`: claves del catálogo de textos usadas
  - `focus_target`: elemento que recibe el foco tras una acción
  - `aria_busy`: booleano (verdadero durante la carga)

## Architectural Attributes *(mandatory)*

| Attribute | Value |
|-----------|-------|
| **Interaction type** | sync-http |
| **Consistency** | strong |
| **Workflow** | multi-step |
| **Read pattern** | simple |
| **Auditability** | none |
| **Domain complexity** | medium |
| **Modularity** | feature-slice |
| **Deployment** | monolith |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El evaluador activa cualquier escenario visible en 2 clics o menos.
- **SC-002**: El 100 % de los escenarios visibles recarga la vista con el escenario elegido.
- **SC-003**: El selector no existe en la versión de producción.

## UI Constraints *(include for frontend/web projects)*

### Visual Requirements
- **Design system**: propio, definido en `sdd/reports/DESIGN_CONTRACT.md` (CSS propio con tokens de color, tipografía, espaciado y radios; sin librería de componentes ni logos de terceros).
- **Responsive**: sí; una columna con margen lateral de 16 px y ancho máximo de 720 px, sin desplazamiento horizontal desde 320 px; botones a ancho completo en móvil con área táctil mínima de 44 × 44 px.
- **Accessibility**: WCAG 2.1 nivel AA (NFR-011): roles semánticos, foco visible, navegación por teclado, contraste de al menos 4,5:1 en texto y 3:1 en contornos de controles; el color nunca es el único portador de significado.

### Interaction Patterns
- **Loading states**: el selector muestra un texto de carga mientras se pide el catálogo.
- **Error states**: «No pudimos cargar los escenarios.» (aviso de advertencia, no bloquea la vista), «El escenario ya no existe. Elige otro.», «Avanzar reloj no está disponible en este modo.» y «No se pudo iniciar la sesión de prueba.» (error con rol de alerta y «Reintentar»), todos definidos en el DESIGN_CONTRACT v1.5.
- **Empty states**: «No hay escenarios disponibles.» si el catálogo está vacío.

### Style Constraints
- **Color palette**: tokens de color del DESIGN_CONTRACT (marca índigo para acciones primarias y foco, rojo solo decorativo, tintes para banners y chips); el color nunca es el único portador de significado: siempre va acompañado de texto e ícono.
- **Typography**: tipografía del sistema con escala de 14, 16, 20 y 24 px, interlineado 1,5; códigos de reglas en monoespaciada.
- **Spacing**: escala de espaciado de 4 a 32 px del DESIGN_CONTRACT; radio único de 8 px.

### Visual Spec *(mandatory for web/mobile)*

| Screen | Image | Source | Description |
|--------|-------|--------|-------------|
| Pantalla 2: retraso con opción propuesta y caso humano | Wireframe ASCII de `sdd/reports/DESIGN_CONTRACT.md` (§Evidencia Visual); captura de imagen diferida hasta que exista el front | Wireframe de texto (alternativa autorizada cuando no hay imagen) | alertas, reglas plegadas, opción propuesta, vía de reembolso, acciones con cuenta regresiva y diálogo |
| Pantalla 5: solicitud registrada | Wireframe ASCII de `sdd/reports/DESIGN_CONTRACT.md` (§Evidencia Visual); captura de imagen diferida hasta que exista el front | Wireframe de texto (alternativa autorizada cuando no hay imagen) | «pendiente de confirmación, sujeta a disponibilidad» con vencimiento, tono informativo |

## Traceability *(mandatory after implementation)*

> Las columnas de archivo y línea se registran en la verificación de trazabilidad posterior a la implementación; hoy cada criterio queda enlazado a su origen y a las pruebas que lo verifican.

| Criterion | Origen | Prueba (TC) | Source File | Line(s) |
|-----------|--------|-------------|-------------|---------|
| FR-VIS-001 | Usuario (2026-10-19) | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-VIS-002 | Usuario (2026-10-19) | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-VIS-003 | Usuario (2026-10-19) | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-001 | DEC-21 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-101 | DEC-04 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| FR-111 | DEC-04 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-011 | DEC-04 | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| NFR-012 | Usuario (2026-10-19) | sin TC en el mapa §6 de REQUERIMIENTOS_V1 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-001 | criterio medible de este spec | TC-01, TC-08, TC-27 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-002 | criterio medible de este spec | TC-01, TC-08, TC-27 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |
| SC-003 | criterio medible de este spec | TC-01, TC-08, TC-27 | se registra en la verificación posterior a la implementación | se registra en la verificación posterior a la implementación |

## Business Process (BPM View)

```
Cargar catálogo → Activar escenario → Fijar sesión simulada → Recargar vista → Avanzar reloj
```

```mermaid
flowchart LR
    A1["Cargar catálogo"]
    A2["Activar escenario"]
    A3["Fijar sesión simulada"]
    A4["Recargar vista"]
    A5["Avanzar reloj"]
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
```

### Subprocesses (if applicable)

```
FE-01.1: Carga del catálogo
FE-01.2: Activación del escenario
FE-01.3: Fijación de la sesión simulada
FE-01.4: Avance del reloj de escenario
```
