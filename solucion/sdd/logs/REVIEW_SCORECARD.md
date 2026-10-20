# Review Scorecard

| Step | Team | CTO | Event | Disputes | Arbiter |
|------|------|-----|-------|----------|---------|
| E0 · /codex vuelta 1 | -1 | +2 | 8 defectos ALTA (FR-004/007, revalidación vs. caso humano, llave idempotente, MCT=0, autorización) | 0 | — |
| E0 · /codex vuelta 2 | -1 | +2 | 5 defectos ALTA (huella con vigencia, anomalía global, llave vs. versión de política, timeout de transporte) | 0 | — |
| E0 · Step Reviewer | +2 | 0 | Autocorrección antes del CTO: 15 puntos (STATUS neutro, prioridad de motivos, formato FR-nnn, tests sin cubrir, matriz DEC→FR) | 0 | — |
| E0 · /codex vuelta 3 | -1 | +2 | 2 defectos ALTA (revalidación sin contexto del viaje; caso humano con respuesta perdida) | 0 | — |
| E0 · CTO interno vuelta 1 | -1 | +2 | 9 defectos (404 uniforme, coherencia de itinerario en opciones, ciclo de vida de la operación, contrato de escritura, integridad de lecturas…) | 0 | — |
| E0 · CTO interno vuelta 2 | -1 | +2 | 3 defectos (FR-041(f) general, FR-066 vs. FR-038, rótulo de compensación) | 0 | — |
| E0 · CTO interno vuelta 3 | +1 | 0 | **APROBADO** (solo 6 mejoras no bloqueantes: M1–M6) | 0 | — |
| A1 · Step Reviewer (4 vueltas) | +2 | 0 | Autocorrecciones antes del CTO: NFR sin flujo, contradicciones entre artefactos, ≤3 parámetros, NO_EVENTS, notificación | 0 | — |
| A1 · Designer (3 vueltas) | 0 | 0 | 10 + 2 + 4 cambios de diseño (cuenta regresiva, reembolso no afirmativo, gate destacado, accesibilidad) aplicados | 0 | — |
| A1 · /codex vueltas 1-3 | -1 | +2 | 7 + 4 + 5 defectos ALTA (autorización, huellas, purga, menor desconocido…) corregidos | 0 | — |
| A1 · /codex vuelta 4 | 0 | 0 | NO EJECUTADA: límite de uso de Codex (reinicio 19:56); pendiente de reintento | 0 | — |
| A1 · CTO interno | +1 | 0 | **APROBADO** sin defectos; 10 mejoras no bloqueantes (DEBT-A1-01…10) | 0 | — |
| A2 · Step Reviewer | +2 | 0 | Autocorrección: FR-122 en specs, duplicados, escenarios sin valores del caso base, FE-03.3, check_specs, trazabilidad inflada | 0 | — |
| A2 · Designer | 0 | 0 | 7 cambios: textos exactos verificables, pantalla 4, pernocte, accesibilidad, ScenarioSelector | 0 | — |
| A2 · CTO interno vuelta 1 | -1 | +2 | 3 defectos: cobertura de TC nominal (TC-10/35/27), caso base sin derivación numérica, purga contradictoria con FR-064 | 0 | — |
| A2 · /codex | 0 | 0 | NO EJECUTADA: límite de uso de Codex (reinicio 19:56); pendiente de reintento | 0 | — |
| A2 · CTO interno vuelta 2 | +1 | 0 | **APROBADO**; 5 mejoras no bloqueantes (DEBT-A2-01…05) | 0 | — |

## Mejoras no bloqueantes registradas (IDEA/DEBT) de la etapa 0
- M1: TC-37 y TC-39 deben probar la rama sin conexión perdida de FR-041(f) y cada resultado por causa de FR-066.
- M2: aclarar que «lectura fallida» (FR-066 → FR-105) ofrece el caso humano mediante el botón siempre disponible (FR-060).
- M3: validar con Producto el rótulo «Tengo una consulta sobre compensaciones».
- M4: anotar en DOC-002 la limitación de la regla «+1 día» (FR-021) con diferencias horarias extremas.
- M5: orden cosmético de filas (H-13/H-16, S-14, FR-036/038, FR-062/064).
- M6: H-15 (política sin R5 ⇒ un menor podría rebookearse sin aprobación) necesita confirmación del usuario.

## Totals
- Team: -3 points
- CTO: +10 points
- Disputes resolved: 0

## Mejoras no bloqueantes de A1 (DEBT) — a resolver en A5-A7 o declarar como riesgo
- DEBT-A1-01: dos pestañas con opciones distintas crean dos rebookings (unicidad por reserva+itinerario). Requiere decisión del usuario (índice por reserva) o riesgo declarado.
- DEBT-A1-02: `ScenarioClock` debe partir del último `retrieved_at` del escenario (TTL 120 s medido desde 11:02:35, no 11:02:31); el «Quedan 01:48» del wireframe no sale de ningún cálculo.
- DEBT-A1-03: FR-041(f) con `missed_connection` desconocido no está definido (mitigado: decisión BLOQUEADA).
- DEBT-A1-04: la notificación `DELAY` repite aviso idéntico al cambiar solo los minutos; usar política rota (versión + reglas) o enfriamiento por (reserva + motivo).
- DEBT-A1-05: faltan requisito de SQL parametrizado, prohibir `dangerouslySetInnerHTML` y límite de tasa en `evaluate`.
- DEBT-A1-06: NFR-007 (≤10 líneas, ≤3 parámetros): SQL en archivos `.sql` y handlers con objeto de valor; riesgo de alcance frente a REQ-P-01 (3 h).
- DEBT-A1-07: `GET /decisions` expone `needs_manual_review` y `notifications` a la sesión del pasajero (FR-123 los define internos).
- DEBT-A1-08: pantalla 2 omite la alerta `OVERNIGHT`; `messages[].text` vs. test de catálogo (FR-113).
- DEBT-A1-09: el mock devuelve el mismo `NT-9912` en dos notificaciones (ids distintos). `.gitignore` ya excluye `*.pdf` y `datos_fuente/`.
- DEBT-A1-10: destinatario de `notify_passenger` = titular adulto, nunca el menor; FR-001 («todo /api/v1 responde 401») vs. modo `system`; IDs de riesgo desordenados.
- PENDIENTE: 4.ª vuelta de /codex sobre A1 (límite de uso).

## Mejoras no bloqueantes de A2 (DEBT)
- DEBT-A2-01: FR-064 no fija el instante de referencia de los plazos encadenados EN_CURSO → INDETERMINADA → EXPIRADA (¿desde la creación, o 120 s + 900 s?).
- DEBT-A2-02: `TC_KEYWORDS` de check_specs.py sigue laxo en TC-24, TC-23 y TC-33.
- DEBT-A2-03: F-12 no enumera por nombre todos los parámetros operativos (p. ej. `UPSTREAM_WRITE_TIMEOUT_MS`).
- DEBT-A2-04: siguen abiertos DEBT-A1-01 (doble rebooking de itinerarios distintos) y DEBT-A1-02 (reloj de escenario, A5).
- DEBT-A2-05: columnas archivo/línea de Traceability con relleno uniforme (OQ-A2-16).
- PENDIENTE: /codex de A1 (vuelta 4) y de A2.
