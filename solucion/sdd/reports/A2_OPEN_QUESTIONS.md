# Preguntas abiertas y contradicciones detectadas en A2 (specs funcionales)

**Paso SDD:** A2 · **Fecha:** 2026-10-19 · **Ronda 4** (CTO: cobertura real de TC con palabras clave por TC, valores concretos fuertes, derivación numérica del caso base, purga conforme a FR-092, límite de tasa ampliado, identificadores de aviso distintos, parámetros operativos por nombre, riesgo de proporcionalidad) · **Ronda 3** (Step Reviewer y Designer: OQ-A2-20 cerrada por FR-122, DEBT-A1-08 cerrada con la alerta de pernocte en el DESIGN_CONTRACT v1.5, `check_specs.py` ampliado) · **Ronda 2** (resoluciones del orquestador, ya incorporadas en `docs/REQUERIMIENTOS_V1.md`: FR-001, 041, 064, 093, 122, 123, NFR-012, NFR-013, S-18, S-20, TC-57…60 y el estado canónico `PENDIENTE_APROBACION`).
**Regla aplicada:** el BUILDER no resuelve contradicciones por su cuenta; las anota aquí. En la ronda 2 los specs y los artefactos de A1 se actualizaron **solo** en lo que las resoluciones exigen (EXTERNAL_CONTRACTS v1.5, FLOW_INVENTORY v1.5, ARCHITECTURE v1.5, DESIGN_CONTRACT v1.4).

Estados: **Resuelta** (decisión tomada y reflejada en specs y A1) · **Riesgo del usuario** (se queda como riesgo o pendiente que decide el USUARIO) · **A5** (se resuelve en el diseño técnico) · **Propuesta** (la ronda 2 propuso algo nuevo que hay que confirmar).

| ID | Estado | Hallazgo | Resolución y dónde quedó reflejada |
|---|---|---|---|
| OQ-A2-01 | **Resuelta** | FR-001 («todo `/api/v1` responde 401») chocaba con el modo `system` (FR-120). | FR-001 aclarado: `401` solo para `caller = user` sin sesión; `system` exige la credencial de servicio. SF-01.1, SF-11.1 y X-01. |
| OQ-A2-02 | **Resuelta** | FR-110/FR-091 nombran tecnología en un requisito funcional. | Aceptada la reescritura en lenguaje de negocio (todos los specs). |
| OQ-A2-03 | **Resuelta** | X-01 y X-02 no están en el inventario. | Se aceptan como specs de apoyo (104 en total). |
| OQ-A2-04 | **Resuelta** | Huecos en la numeración de FR. | Sin faltantes; el script calcula contra los FR definidos. |
| OQ-A2-05 | **Resuelta** | Una `INDETERMINADA` bloqueaba para siempre en v1. | FR-064/S-18: `INDETERMINADA` pasa a `EXPIRADA` tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900) y permite la generación siguiente. Specs: F-02, SF-01.12, SF-02.5, F-07, SF-07.2, F-09, SF-09.2, SF-09.3, F-12; TC-57. A1: ciclo de vida, esquema de operaciones, purga. Riesgo residual S-20 (duplicado si la solicitud sí se creó y su vigencia fuera mayor) declarado como DEFERRED. |
| OQ-A2-06 | **Riesgo del usuario** | DEBT-A1-01: dos pestañas con opciones distintas crean dos rebookings (unicidad por reserva + itinerario). | Sigue como riesgo declarado en F-02, SF-02.5, F-01 y FE-03 (DEFERRED); lo decide el usuario. |
| OQ-A2-07 | **Resuelta** | DEBT-A1-04: el aviso `DELAY` se repetía al cambiar solo los minutos. | FR-123: la huella del motivo `DELAY` es versión de política + reglas disparadas. F-08, SF-08.2, F-11; TC-60. A1: contrato de notificación, esquema, escenario `NOTIFY_DELAY_SOLO_MINUTOS_TC60`. |
| OQ-A2-08 | **Resuelta** | DEBT-A1-07: la lectura de la decisión exponía campos internos. | FR-093: sin `needs_manual_review` ni detalle de notificaciones para la sesión del pasajero. F-04, SF-04.3, SF-01.13, SF-11.5; TC-59. A1: DecisionRecord, escenario `DECISION_SESION_SIN_INTERNOS_TC59`. |
| OQ-A2-09 | **Resuelta** | DEBT-A1-10: destinatario del aviso. | FR-122: el aviso va al titular adulto, nunca al menor. F-08, SF-08.1, SF-11.4, F-11; TC-60. A1: `recipient_passenger_id` en el contrato de notificación. Ver OQ-A2-20. |
| OQ-A2-10 | **A5** | DEBT-A1-02: el reloj de escenario debe partir del último `retrieved_at`; el «Quedan 01:48» del wireframe no sale de ningún cálculo. | Se resuelve en el diseño (A5). Los specs usan la cuenta de 01:48 con vencimiento 11:04:35Z (11:02:35Z + 120 s) y generación 11:02:47Z; SF-06.3, SF-06.4, FE-01.4 y FE-02.3 lo citan. |
| OQ-A2-11 | **Resuelta** | DEBT-A1-03: FR-041(f) con `missed_connection` desconocido. | FR-041: ninguna opción es viable, decisión BLOQUEADA y soporte ofrecido. F-01, SF-01.9, FE-02, FE-02.2; TC-60 (`OPCIONES_CONEXION_DESCONOCIDA_TC60`). A1: evaluación y herramienta de opciones. |
| OQ-A2-12 | **Resuelta** | DEBT-A1-05/06: faltaban SQL parametrizado, texto plano en la interfaz y límite de tasa. | NFR-013 (nuevo) y parámetro `EVALUATE_RATE_LIMIT_PER_MINUTE` (30). SF-01.1, SF-01.13, F-01, F-11, SF-11.1, X-01, FE-02, FE-02.5, F-12; TC-58. A1: error `429 RATE_LIMITED`, DESIGN_CONTRACT (texto plano), ARCHITECTURE (norma 7). El riesgo de alcance de NFR-007 frente al plazo queda como DEFERRED en X-01. |
| OQ-A2-13 | **Resuelta** | NFR-012 no listaba los parámetros operativos de EXTERNAL_CONTRACTS §2.4. | NFR-012 los incluye. F-12 y sus subflujos. |
| OQ-A2-14 | **Resuelta** | `PENDIENTE_APROBACIÓN` con y sin tilde. | Forma canónica `PENDIENTE_APROBACION` (FR-035 ya corregido; los specs la usan). |
| OQ-A2-15 | **Resuelta (diferida)** | La plantilla pide imagen de Visual Spec y no existe ninguna. | La captura visual queda diferida: requiere autorización del usuario; los specs de front citan el wireframe ASCII del DESIGN_CONTRACT. |
| OQ-A2-16 | **Resuelta** | Traceability exige archivo y línea, que solo existen tras implementar. | Se rellena con origen y TC; las columnas de código se registran tras la implementación. |
| OQ-A2-17 | **Riesgo del usuario** | H-13, H-15 y H-21 siguen pendientes de confirmación. | Los specs los reflejan tal cual (SF-01.8, SF-08.1, F-11, X-02). |
| OQ-A2-18 | **Resuelta** | F-08 y F-09 no son interacciones directas del usuario. | Informativo; tienen spec propio con escenarios de negocio indirectos. |
| OQ-A2-19 | **Resuelta** | La vuelta 4 de /codex sobre A1 no se ejecutó por límite de uso. | Sin cambios; queda anotada en el REVIEW_SCORECARD. |
| OQ-A2-20 | **Resuelta** (ronda 3) | FR-122 exigía dirigir el aviso al titular adulto pero no definía el caso sin adulto ni el campo del contrato. | FR-122 vigente: sin titular adulto **no se envía** (`NOT_SENT / NO_ADULT_RECIPIENT`) y se marca `needs_manual_review`. EXTERNAL_CONTRACTS conserva el campo `recipient_passenger_id` (extensión DOC-013) y FLOW_INVENTORY lo refleja. Specs F-08, SF-08.1, SF-11.3, SF-11.4 y F-11 con escenario «reserva sin titular adulto» (TC-60). |
| OQ-A2-21 | **Riesgo declarado** (nuevo, ronda 4) | Proporcionalidad: 104 specs y unos 400 escenarios frente al plazo de 3 horas del reto (REQ-P-01). | Se declara en X-01, en RFC_DESIGN y aquí. **Slice de implementación prioritario:** el caso base (TC-01), TC-01 a TC-20 y el modo sistema (TC-42 a TC-44, TC-50 a TC-52 y TC-55); el resto de TC se automatiza solo si alcanza el tiempo. Lo decide el usuario. |

## Deuda A1 (DEBT-A1-xx): estado tras la ronda 2

| DEBT | Estado | Specs que la citan |
|---|---|---|
| DEBT-A1-01 | Riesgo del usuario (OQ-A2-06) | F-01, F-02, SF-02.5, FE-03 |
| DEBT-A1-02 | A5 (OQ-A2-10) | F-06, SF-06.3, SF-06.4, SF-02.4, FE-01.4, FE-02.3 |
| DEBT-A1-03 | Resuelta (FR-041 f) | ninguno |
| DEBT-A1-04 | Resuelta (FR-123) | ninguno |
| DEBT-A1-05 | Resuelta (NFR-013) | ninguno |
| DEBT-A1-06 | Resuelta (NFR-013; riesgo de alcance de NFR-007 queda DEFERRED en X-01) | ninguno |
| DEBT-A1-07 | Resuelta (FR-093) | ninguno |
| DEBT-A1-08 | **Resuelta** (DESIGN_CONTRACT v1.5: alerta de pernocte en la pantalla 2 y mensajes del servidor eximidos de la prueba de catálogo por provenir de plantillas validadas) | ninguno |
| DEBT-A1-09 | **Resuelta** (ronda 4: el simulador asigna identificadores distintos, `NT-9912` y `NT-9913`) | ninguno |
| DEBT-A1-10 | Resuelta (OQ-A2-01 y OQ-A2-09) | ninguno |
