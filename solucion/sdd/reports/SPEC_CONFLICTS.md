# Reporte de Conflictos entre Specs — Disruption Companion V0

**Paso SDD**: A6 (Detección de conflictos previa al Plan Técnico)  
**Alcance escaneado**: 15 specs funcionales en `sdd/specs/functional/`

---

## 1. Resumen del Escaneo (4 Categorías)

| Categoría | Elementos escaneados | Conflictos bloqueantes | Resoluciones / Anotaciones |
|-----------|----------------------|------------------------|----------------------------|
| **ENDPOINT** | `POST /api/v1/trips/{booking_id}/evaluate`, `POST /api/v1/trips/{booking_id}/options/{option_id}/accept`, `GET /api/dev/scenarios`, `PUT /api/dev/scenario`, `GET /ping` | 0 | Sin colisión de método HTTP + ruta entre `F-01`, `F-02` y `F-06`. |
| **ENTITY** | `TripView`, `AcceptResult`, `DecisionRecord`, `ResolvedSegment`, `DerivedVariable`, `EvaluatedRule`, `CandidateOption`, `ValidatedMessage` | 0 | `15-sf-01-14` y `82-fe-02` comparten la misma definición de `TripView` (`extends` lectura visual sin alterar campos). |
| **SERVICE** | `DisruptionCompanionService` (monolito modular Python 3.13 + FastAPI) | 0 | Un único servicio de backend expone los endpoints para el visor frontend. |
| **TABLE / STORAGE** | `InMemoryDecisionStore` (supuesto explícito `S-V0-3` para V0) | 0 | En V0 la traza de decisiones y operaciones se almacena en memoria y se devuelve en la respuesta de evaluación, difiriendo las tablas SQLite de retención/purga a V1/V2. |

---

## 2. Anotaciones de Alcance V0 (Supuestos explícitos `SRC-07-10`)

| ID | Relación entre Specs | Anotación | Resolución aplicada en V0 |
|----|----------------------|-----------|---------------------------|
| **CONF-V0-01** | `01-f-01` vs specs diferidos a V1 (`02-sf-01-1`, `04-sf-01-3`, `14-sf-01-13`) | `overrides (V0 scope)` | `F-01` ejecuta la cadena completa de negocio (`SF-01.2`, `SF-01.4`, `SF-01.5`, `SF-01.6`, `SF-01.7`, `SF-01.8`, `SF-01.9`, `SF-01.11`, `SF-01.14`) asumiendo sesión pre-autorizada o cabecera opcional compatible (`S-V0-1`) y guardando el registro de decisión en memoria (`S-V0-3`). |
| **CONF-V0-02** | `16-f-02` vs subflujos diferidos a V1 (`17`..`26`) | `overrides (V0 scope)` | `F-02` implementa en el servicio la bifurcación completa (`AUTOMATICA` → `create_rebooking_request` con `idempotency_key` y reintentos ante `503` con fallback a `create_human_case`; `PENDIENTE_APROBACION`/`BLOQUEADA` → `create_human_case` con evidencia sin PII) como flujo cohesivo en memoria (`S-V0-4`). |
| **CONF-V0-03** | `82-fe-02` vs sub-specs de UI diferidos a V2 (`83`..`102`) | `overrides (V0 scope)` | El frontend V0 implementa un visor limpio con CSS propio alineado con `DESIGN_CONTRACT.md` que permite elegir el escenario (`F-06`), consultar la evaluación (`F-01`), inspeccionar toda la respuesta recibida del backend y ejecutar la acción (`F-02`). |
