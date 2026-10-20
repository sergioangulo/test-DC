# RFC Técnico: Disruption Companion V0 (Modelo 4+1 Vistas)

**Estado**: APROBADO (Modo Cumplimiento / Pragmático)  
**Fecha**: 2026-10-19  
**Autor**: `sdd-workflow` MCP + Equipo de Ingeniería  
**Alcance**: `sdd/specs/functional/` (15 specs de V0)

---

## 1. Introducción y Motivación

**Disruption Companion V0** resuelve el problema central del pasajero cuyo vuelo sufre una modificación operacional (`Disruption Companion.pdf`, `SRC-01-09`..`SRC-01-15`): combinar el contexto de la reserva (`get_trip_context`), los eventos operacionales (`get_operational_events`), las políticas versionadas (`get_policy_rules`) y las opciones candidatas (`get_eligible_options`) para explicar qué ocurrió, qué implica para su conexión y ejecutar la acción controlada (`create_rebooking_request` con llave idempotente o escalamiento a `create_human_case` cuando se requiere aprobación humana o hay anomalía), sin exponer PII ni afirmar hechos no verificados.

---

## 2. Vista de Escenarios (+1) — Flujos de Negocio Implementados

### 2.1 F-01: Evaluar viaje como pasajero (`POST /api/v1/trips/{booking_id}/evaluate`)

```mermaid
flowchart LR
    A1["Paso 1 : Leer contexto del viaje"]
    A2["Paso 2 : Leer y validar eventos operacionales"]
    A3["Paso 3 : Derivar variables del viaje"]
    A4["Paso 4 : Evaluar reglas R1 a R5 de politica"]
    A5["Paso 5 : Filtrar opciones candidatas O1 a O3"]
    A6["Paso 6 : Validar mensajes y armar TripView"]
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> A6
```

### 2.2 F-02: Aceptar opción / Acción controlada (`POST /api/v1/trips/{booking_id}/options/{option_id}/accept`)


```mermaid
flowchart LR
    A1["Paso 1: Recibir clic con identificador de decision"]
    A2["Paso 2: Evaluar estado de la decision guardada"]
    D1{"Estado de la decision"}

    A3["Calcular llave idempotente y solicitar rebooking"]
    D2{"Resultado del rebooking"}

    A4["503 tras 2 reintentos: Escalar a caso humano"]
    A5["201 o 409: Devolver solicitud creada o existente"]
    A6["Crear caso humano sin PII"]

    A1 --> A2
    A2 --> D1

    D1 -->|AUTOMATICA| A3
    D1 -->|PENDIENTE APROBACION o BLOQUEADA| A6

    A3 --> D2
    D2 -->|503| A4
    D2 -->|201 o 409| A5
```

---

## 3. Vista Lógica (Arquitectura Hexagonal y Dominio)

```mermaid
flowchart TD
    C1["FastApiAdapter - Endpoints HTTP"]
    C2["DisruptionCompanionService - Orquestacion de Casos de Uso"]
    C3["EventResolver - Precedencia UTC y exclusion de fuentes degradadas"]
    C4["VariableDeriver - Calculo de nueva llegada, margen y menor"]
    C5["RuleEngine - Parser seguro con lista blanca y logica de Kleene"]
    C6["OptionFilter - Viabilidad de opciones por asientos, tarifa, politica y TTL"]
    C7["MessageBuilder - Plantillas deterministicas y validador de politica"]
    C8["MockToolsAdapter - Contratos de las 6 herramientas del PDF"]
    C1 --> C2
    C2 --> C3
    C2 --> C4
    C2 --> C5
    C2 --> C6
    C2 --> C7
    C2 --> C8
```

---

## 4. Vista de Procesos (Secuencia del Caso Base `ABC123`)

```mermaid
sequenceDiagram
    participant UI as Visor React
    participant API as FastAPI
    participant SVC as DisruptionCompanionService
    participant MOCK as MockToolsAdapter
    UI->>API: POST /api/v1/trips/ABC123/evaluate
    API->>SVC: evaluateTrip(ABC123)
    SVC->>MOCK: getTripContext(ABC123)
    SVC->>MOCK: getOperationalEvents(S1, S2)
    Note over SVC: Excluye E-1012 de fuente degradada y aplica retraso 160m y Puerta 24
    SVC->>MOCK: getPolicyRules(DELAY)
    Note over SVC: Deriva llegada 20:35 mayor a 19:05 con menor presente (R3 y R5 verdaderas)
    SVC->>MOCK: getEligibleOptions(ReducedTripContext sin PII)
    Note over SVC: O1 viable (4 asientos y costo 0) y descarta O2 y O3 con razones
    SVC-->>UI: 200 TripView (propuesta O1 y estado pendiente de aprobacion)
```

---

## 5. Vista de Desarrollo y Calidad Verificada

- **Runtime**: Python `3.13.16` (entorno `companion313`), FastAPI `0.115.0`, Pydantic `2.9.2`, Pytest `8.3.3`.
- **Métricas de pruebas y código**:
  - **Tests**: `17 passed` (unitarios de dominio, adaptadores, casos de uso, integración API + AST y suite E2E `backend/tests/e2e/test_e2e_scenarios.py`).
  - **Cobertura**: **93 % total** (`>= 87 %` en todos los módulos de dominio).
  - **Clean Code verificado por AST (`test_clean_code_ast_limits_and_domain_isolation`)**: 100 % de las funciones en `backend/app/` tienen **≤ 10 líneas** y **≤ 3 parámetros**, con **0 llamadas a `eval`/`exec`**.

---

## 6. Evidencia E2E y Visual (`§Visual Evidence`)

Detalle completo en `sdd/reports/E2E_EVIDENCE.md` y pruebas automatizadas en `backend/tests/e2e/test_e2e_scenarios.py`.

| Pantalla / Escenario E2E | Archivo de Evidencia | Estado |
|--------------------------|----------------------|--------|
| 1. Caso Base `ABC123` (`BASE_TC01` — `PENDIENTE_APROBACION` + caso humano `HC-4471`) | `sdd/screenshots/result/01-base-tc01.png` | Verificado |
| 2. Rebooking Automático sin Menor (`ADULTOS_AUTOMATICO_TC07` — `RBK-88231`) | `sdd/screenshots/result/02-adultos-automatico-tc07.png` | Verificado |
| 3. Conflicto de Fuentes (`CONFLICTO_FUENTES_TC03` — `BLOQUEADA` por `SOURCE_CONFLICT`) | `sdd/screenshots/result/03-conflicto-fuentes-tc03.png` | Verificado |
| 4. Sin Opción Viable para el Grupo (`SIN_OPCION_VIABLE_TC09` — `INSUFFICIENT_SEATS`) | `sdd/screenshots/result/04-sin-opcion-viable-tc09.png` | Verificado |

### 6.1 Caso Base (`BASE_TC01`)
![Caso Base ABC123](../screenshots/result/01-base-tc01.png)

### 6.2 Rebooking Automático (`ADULTOS_AUTOMATICO_TC07`)
![Rebooking Automatico](../screenshots/result/02-adultos-automatico-tc07.png)

### 6.3 Conflicto de Fuentes (`CONFLICTO_FUENTES_TC03`)
![Conflicto de Fuentes](../screenshots/result/03-conflicto-fuentes-tc03.png)

### 6.4 Sin Opción Viable (`SIN_OPCION_VIABLE_TC09`)
![Sin Opcion Viable](../screenshots/result/04-sin-opcion-viable-tc09.png)

