# Implementation Plan: Disruption Companion V0 — Vertical Slice Backend + Visor Frontend

**Date**: 2026-10-19  
**Spec**: `sdd/specs/functional/01-f-01-evaluar-viaje-como-pasajero.md` (+ 14 specs en `sdd/specs/functional/`)  
**Status**: in-progress

## Summary

Implementación del vertical slice **Disruption Companion V0** enfocado en el Track **Backend/Integración** con un **visor Frontend mínimo** que muestra todo lo que recibe del backend.  
El sistema combina el contexto de la reserva (`get_trip_context`), los eventos operacionales (`get_operational_events`), las reglas versionadas de política (`get_policy_rules`) y las opciones elegibles (`get_eligible_options`) para determinar de forma 100 % determinística qué ocurrió con el viaje, qué corresponde ofrecer o comunicar al pasajero y ejecutar la acción controlada (`create_rebooking_request` con `idempotency_key` o escalamiento a `create_human_case`).

## Technical Context

**Language/Version**: Python 3.13 (Backend) + TypeScript / React 18 / Vite (Visor Frontend)  
**Primary Dependencies**: `fastapi==0.115.0`, `pydantic==2.9.2`, `uvicorn==0.30.6`  
**Storage**: `InMemoryDecisionStore` en memoria para V0 (supuesto explícito `S-V0-3`)  
**Testing**: `pytest==8.3.3`, `pytest-cov==5.0.0`, `httpx==0.27.2`  
**Target Platform**: Local / multiplataforma (Windows / Linux / macOS)  
**Project Type**: Fullstack acotado (foco Backend + visor Frontend ligero)  
**Performance Goals**: `< 1500 ms` p95 en evaluación secuencial  
**Constraints**: Funciones de máximo 10 líneas y máximo 3 parámetros; cero uso de `eval`/`exec`; cero exposición de PII en registros o respuestas salvo `holder_first_name` en la vista del pasajero  
**Scale/Scope**: 15 specs funcionales en `sdd/specs/functional/` (caso base `ABC123` y escenarios de validación)  
**Infrastructure Requirements**: Ejecución directa con Python 3.13 (`companion313`) y Node/Vite sin requerir Docker  
**Integration Points**: 6 herramientas simuladas (`MockToolsAdapter`) fieles a los contratos JSON del PDF (`SRC-01-16`)  
**Security Considerations**: Parser de reglas con lista blanca de tokens; proyección sin PII antes de invocar `get_eligible_options` y `create_human_case`; validador de mensajes con `policy_ref`

## Project Structure

### Documentation (this feature)

```text
sdd/specs/
├── functional/               # 15 specs de V0 activos
└── technical/
    └── 01-disruption-companion-v0-plan.md
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── domain/
│   │   ├── models.py            # Entidades y Value Objects inmutables (<=3 params)
│   │   ├── ports.py             # Interfaces/Protocolos de herramientas y reloj
│   │   ├── event_resolver.py    # SF-01.4 y SF-01.5: precedencia, degradación y conflicto
│   │   ├── variable_deriver.py  # SF-01.7: delay, new_arrival, missed_connection, menor
│   │   ├── rule_engine.py       # SF-01.8: parser seguro sin eval + lógica de Kleene
│   │   ├── option_filter.py     # SF-01.9: viabilidad de opciones (asientos, tarifa, policy_ref, TTL)
│   │   └── message_builder.py   # SF-01.11: plantillas determinísticas y validador con policy_ref
│   ├── application/
│   │   └── companion_service.py # F-01, F-02, F-06: orquestación secuencial y acciones
│   ├── adapters/
│   │   └── mock_tools.py        # Escenarios del PDF (ABC123 caso base y variantes TC)
│   └── api/
│       └── main.py              # Endpoints FastAPI (/ping, /evaluate, /accept, /scenarios)
└── tests/
    ├── unit/                    # Pruebas unitarias por módulo de dominio y calidad AST
    └── integration/             # Pruebas de contrato e integración extremo a extremo (TC-01..TC-16)

frontend/
├── index.html
├── package.json
├── vite.config.ts
└── src/
    ├── main.tsx
    ├── App.tsx                  # Visor sencillo que consume el backend y muestra la respuesta
    └── styles.css               # Estilos propios alineados con DESIGN_CONTRACT.md
```

**Architecture Decision**: Arquitectura Hexagonal (Puertos y Adaptadores) combinada con patrones tácticos de DDD (Value Objects para agrupar parámetros y respetar el límite de ≤ 3 parámetros y ≤ 10 líneas por función).

---

## API Contracts

| Endpoint | Method | Path | Request Schema | Response Schema | Error Codes | Auth |
|----------|--------|------|----------------|-----------------|-------------|------|
| Ping | GET | `/ping` | Ninguno | `pong` (`text/plain`) | 500 | Ninguna |
| Listar escenarios | GET | `/api/dev/scenarios` | Ninguno | `{ active_scenario_id: string, clock_utc: string, scenarios: [{ scenario_id: string, booking_id: string, title: string, description: string }] }` | 500 | Solo dev |
| Activar escenario | PUT | `/api/dev/scenario` | `{ scenario_id: string }` | `{ active_scenario_id: string, booking_id: string, clock_utc: string }` | 404, 422 | Solo dev |
| Evaluar viaje | POST | `/api/v1/trips/{booking_id}/evaluate` | `{ caller: "user" }` | `{ decision_id: string, booking_id: string, generated_at: string, anomaly_detected: bool, decision_state: string o null, holder_first_name: string o null, passenger_count: int, segments: [object], derived_variables: [object], policy: object o null, options: [object], discarded_options: [object], proposed_option_id: string o null, messages: [object], actions: [object] }` | 404, 422, 502 | Sesión simulada / V0 |
| Aceptar opción | POST | `/api/v1/trips/{booking_id}/options/{option_id}/accept` | `{ decision_id: string }` | `{ outcome: string, message: object, operation: object o null, human_case: object o null, retries: int }` | 404, 409, 422, 502 | Sesión simulada / V0 |

### Error Response Schema

```json
{
  "error": "ERROR_CODE",
  "detail": "Mensaje legible en español neutro sin PII ni trazas"
}
```

### Output Contracts

| Service | Method | Endpoint / Resource | Request Schema | Response Schema | Error Handling | Timeout |
|---------|--------|---------------------|----------------|-----------------|----------------|---------|
| `TripContextPort` | `get_trip_context` | `booking_id` | `{ booking_id: string }` | `{ booking_id: string, passengers: [object], segments: [object], fare_conditions: object, _meta: { retrieved_at: string, completeness: string, missing_fields: [string] } }` | 1 re-consulta; si falla → `502 TRIP_CONTEXT_UNAVAILABLE` | 2000 ms |
| `OperationalEventsPort` | `get_operational_events` | `segment_ids` | `{ segment_ids: [string] }` | `{ events: [object], _meta: { retrieved_at: string, sources_available: [string], sources_degraded: [string] } }` | 1 re-consulta; si falla → vista de contexto con aviso sin alerta | 2000 ms |
| `PolicyRulesPort` | `get_policy_rules` | `scenario` | `{ scenario: "DELAY" }` | `{ scenario: string, version: string, effective_from: string, rules: [object], _meta: { superseded_versions: [string] } }` | 1 re-consulta; si falla → decisión `BLOQUEADA` con soporte | 2000 ms |
| `EligibleOptionsPort` | `get_eligible_options` | `reduced_context` | `{ booking_id: string, passengers: [{ passenger_id: string, type: string }], has_minor: bool, segments: [object] }` | `{ options: [object], _meta: { retrieved_at: string, ttl_seconds: int } }` | 1 re-consulta; si falla → decisión `BLOQUEADA` con soporte | 2000 ms |
| `RebookingPort` | `create_rebooking_request` | `option, idempotency_key` | `{ option_id: string, idempotency_key: string, booking_id: string, passenger_ids: [string] }` | `201 { request_id: string, status: string, expires_at: string }` / `409 DUPLICATE_REQUEST` / `503 UPSTREAM_TIMEOUT` | `409` → existente; `503` → hasta 2 reintentos con misma llave y luego `create_human_case` | 5000 ms |
| `HumanCasePort` | `create_human_case` | `reason, evidence` | `{ reason: string, evidence: { booking_id: string, decision_id: string, reasons: [string], policy_version: string o null, selected_option_id: string o null } }` | `201 { case_id: string, queue: string, sla_minutes: int }` | Deduplicación en memoria por reserva y decisión | 5000 ms |

## Data Models

### TripView / DecisionRecord

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `decision_id` | `str` (UUID v4) | NOT NULL, PK | Identificador único de la evaluación |
| `booking_id` | `str` | NOT NULL | Código de reserva (6 caracteres) |
| `generated_at` | `str` (ISO UTC) | NOT NULL | Marca de tiempo del reloj inyectado |
| `anomaly_detected` | `bool` | NOT NULL | Verdadero si hay retraso relevante, puerta o anomalía |
| `decision_state` | `str o None` | Enum / NULL | `INFORMATIVA`, `AUTOMATICA`, `PENDIENTE_APROBACION`, `BLOQUEADA` o `None` |
| `holder_first_name` | `str o None` | Nullable | Nombre de pila del primer pasajero adulto |
| `passenger_count` | `int` | `>= 1` | Total de pasajeros del grupo |
| `segments` | `list[ResolvedSegment]` | NOT NULL | Estado resuelto y puerta de cada segmento |
| `derived_variables` | `list[DerivedVariable]` | NOT NULL | Variables derivadas con origen y supuestos |
| `policy` | `PolicyEvaluation o None` | Nullable | Reglas evaluadas, versión y derechos concedidos |
| `options` | `list[CandidateOption]` | NOT NULL | Opciones viables ordenadas por confianza |
| `discarded_options` | `list[CandidateOption]` | NOT NULL | Opciones descartadas con todas sus razones (`reasons`) |
| `proposed_option_id` | `str o None` | Nullable | ID de la mejor opción viable (`O1` en caso base) |
| `messages` | `list[ValidatedMessage]` | NOT NULL | Mensajes validados con `evidence_refs` y `policy_ref` |
| `actions` | `list[OfferedAction]` | NOT NULL | Acciones ofrecidas al pasajero |

### DTO ↔ Domain Mapping Rules

| DTO Field | Type | Domain Field | Type | Transformation |
|-----------|------|-------------|------|----------------|
| `passengers[].name` | `str` | `holder_first_name` | `str o None` | Toma solo el primer token (`split()[0]`) del primer `ADULT`; descarta apellidos, RUT/documento y edad |
| `events[]` | `list[dict]` | `ResolvedSegment` | `ResolvedSegment` | Excluye fuentes en `_meta.sources_degraded` y resuelve por `recorded_at` UTC |
| `options[]` | `list[dict]` | `CandidateOption` | `CandidateOption` | Evalúa las 6 invariantes de viabilidad y adjunta `viable: bool` y `discard_reasons: list[str]` |

---

## Plan de Ejecución TDD por Ciclos (Paso A7)

- [x] **Ciclo 1**: `DomainModels` (`backend/app/domain/models.py`) + `tests/unit/test_models.py`
- [x] **Ciclo 2**: `DomainPorts` (`backend/app/domain/ports.py`) + `tests/unit/test_ports.py`
- [x] **Ciclo 3**: `MockToolsAdapter` (`backend/app/adapters/mock_tools.py`) + `tests/unit/test_mock_tools.py`
- [x] **Ciclo 4**: `EventResolver` (`backend/app/domain/event_resolver.py`) + `tests/unit/test_event_resolver.py`
- [x] **Ciclo 5**: `VariableDeriver` (`backend/app/domain/variable_deriver.py`) + `tests/unit/test_variable_deriver.py`
- [x] **Ciclo 6**: `RuleEngine` (`backend/app/domain/rule_engine.py`) + `tests/unit/test_rule_engine.py`
- [x] **Ciclo 7**: `OptionFilter` (`backend/app/domain/option_filter.py`) + `tests/unit/test_option_filter.py`
- [x] **Ciclo 8**: `MessageBuilder` (`backend/app/domain/message_builder.py`) + `tests/unit/test_message_builder.py`
- [x] **Ciclo 9**: `DisruptionCompanionService` (`backend/app/application/companion_service.py`) + `tests/unit/test_companion_service.py`
- [x] **Ciclo 10**: `FastApiAdapter` (`backend/app/api/main.py`) + `tests/integration/test_api_and_quality.py` (incluye test AST de ≤ 10 líneas y ≤ 3 parámetros)
