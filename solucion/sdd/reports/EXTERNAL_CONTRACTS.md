# ⚠️ CONTRATOS EXTERNOS SAGRADOS — Disruption Companion

> **ESTE DOCUMENTO ES INMUTABLE DURANTE REFACTORIZACIONES.**
> Los contratos aquí definidos representan el contrato del sistema con el mundo real.
> Cambiar cualquier elemento de este documento sin coordinación con todos los
> consumidores/proveedores implicados **rompe la operación en producción**.
>
> **Quién puede modificar este documento**: solo un cambio de API coordinado,
> versionado, con período de deprecación documentado y aprobado por el equipo.

**Versión:** v1.6 (ronda 7, CTO de A2: purga que aplica vencimientos primero, límite de tasa en evaluar, aceptar, caso humano y consulta de decisión y por origen en credenciales fallidas, identificadores de notificación distintos; v1.5, ronda 5, resoluciones de A2: vencimiento de `INDETERMINADA`, huella del aviso `DELAY`, aviso al titular adulto, registro de decisión sin campos internos para la sesión, límite de tasa en `evaluate`, `NFR-013`; antes v1.4: estado `NO_EVENTS`, huella de la notificación de puerta, purga que conserva operaciones vigentes) · **Fecha:** 2026-10-19 · **Paso SDD:** A1 (Entender el proyecto completo) · **Proyecto:** nuevo, sin código previo. Alineado con la versión final de `REQUERIMIENTOS_V1.md` (FR-001, 003, 040, 041, 053, 059, 060, 064, 065, 066, 071, 091, 093, 105, 122, 123; NFR-004, NFR-012, NFR-013).
**Fuente de verdad de requisitos:** `docs/REQUERIMIENTOS_V1.md` (FR/NFR/DOC, hallazgos H-xx, supuestos S-xx).
**Fuente de los contratos salientes:** `04_Analisis_de_Datos/01…06` (los JSON de ejemplo del PDF «Disruption Companion», copiados **tal cual**).

---

## Cómo usar este documento

- **Al hacer levantamiento**: este documento se redactó **antes** del código; lo que declara es el contrato que el código debe cumplir (no al revés).
- **Al refactorizar**: consultar este documento primero — lo que está aquí no cambia.
- **Al diseñar nuevas funcionalidades**: las nuevas funcionalidades AGREGAN contratos, nunca modifican los existentes.
- **Al detectar un contrato incumplido en código**: el código se corrige, no el contrato.

### Convenciones transversales de este documento

| Tema | Convención |
|---|---|
| Notación de schemas | `{campo: tipo}`; `tipo?` o `tipo \| null` indica que el campo puede estar ausente o valer `null` (se indica en cada caso); `[T]` es un arreglo de `T`. |
| Marcas de tiempo | ISO-8601 **UTC** con sufijo `Z` y segundos: `2026-09-15T11:02:31Z` (FR-018). Las horas locales de los vuelos son `HH:MM` **sin zona** (así vienen del PDF) y se comparan solo dentro del mismo aeropuerto (FR-022). |
| Enumeraciones | `MAYÚSCULAS_CON_GUION_BAJO`, **ASCII** en el cable (sin tildes). Los estados de decisión, de operación y de notificación conservan los nombres de los requisitos sin tilde: `INFORMATIVA`, `AUTOMATICA`, `PENDIENTE_APROBACION`, `BLOQUEADA`, `EN_CURSO`, `INDETERMINADA`, `CREADA`, `FALLIDA`, `QUEUED`. El valor de `caller` es la excepción: minúsculas `user` | `system` (FR-120). Las enumeraciones de **servicios externos** son abiertas (FR-102): un valor nuevo degrada a caso humano. |
| Codificación | JSON UTF-8 (acentos de punta a punta). `Content-Type: application/json; charset=utf-8`, salvo `/ping` (`text/plain; charset=utf-8`). |
| Identificadores | `booking_id`: 6 caracteres `[A-Z0-9]`. `decision_id`: UUID v4 en minúsculas. `option_id`, `segment_id`, `rule_id`, `event_id`, `request_id`, `case_id`: cadenas opacas (DAT-70). |
| Esquema de error uniforme (toda respuesta 4xx/5xx propia) | `{error: string, detail: string}` — `error` es un código estable en `MAYÚSCULAS_ASCII`; `detail` es una frase en español para personas, **fija por código**: no contiene PII, trazas ni repite la entrada recibida (FR-001). |
| Idioma de los textos | Español neutro sin localización (FR-113). Los textos dinámicos salen del catálogo de plantillas del backend (FR-080) y pasan por el validador (FR-081). |

**Excepciones al esquema `{error, detail}`:** `POST …/accept` y `POST …/human-cases` devuelven su cuerpo de resultado (`AcceptResult` / `HumanCaseResult`) **también con los códigos 409, 502 y 504**, porque esos códigos describen resultados de negocio (`STATE_CHANGED`, `NEEDS_CONFIRMATION`, `FAILED`, `INDETERMINATE`) y no errores de protocolo. Solo `401`, `404`, `422` y `500` usan `{error, detail}`. Un cliente distingue ambos por la presencia del campo `outcome`.

### Catálogo de códigos de error propios

| HTTP | `error` | Cuándo |
|---|---|---|
| 401 | `UNAUTHENTICATED` | `caller = "user"`: falta la cabecera `X-Session-Booking` o está vacía, o la cabecera de sesión simulada está deshabilitada (`DEV_SESSION_HEADER_ENABLED=false`, valor por defecto). `caller = "system"`: falta `X-Service-Key`, es incorrecta o `SERVICE_API_KEY` no está configurada (modo `system` apagado por defecto). Es **el único** caso de `401` (FR-001, FR-120). |
| 404 | `NOT_FOUND` | El `booking_id` de la ruta no coincide con la sesión (reserva ajena **o** inexistente) o el `decision_id` no existe **o** es de otra reserva. **Respuesta idéntica en todos los casos** (mismo código y mismo cuerpo: `{"error": "NOT_FOUND", "detail": "No encontramos el recurso solicitado."}`), para no confirmar la existencia de nada (FR-001, DAT-01). No hay `403` en v1. |
| 404 | `DEV_ENDPOINTS_DISABLED` | Se llama a `/api/dev/*` con `DEV_ENDPOINTS_ENABLED=false` (valor por defecto). |
| 404 | `SCENARIO_NOT_FOUND` | `scenario_id` fuera del catálogo de escenarios. |
| 429 | `RATE_LIMITED` | `POST …/evaluate`, `POST …/accept`, `POST …/human-cases` o `GET …/decisions/{id}` superan `EVALUATE_RATE_LIMIT_PER_MINUTE` (30) solicitudes por minuto para la misma reserva y el mismo origen (NFR-013); también se limitan por origen los intentos fallidos de credencial de servicio (`X-Service-Key` incorrecta), aunque después llegue la clave válida. Se evalúa tras comprobar la credencial y antes de la pertenencia, de modo que no depende de la existencia de la reserva. |
| 422 | `VALIDATION_ERROR` | Cuerpo, ruta o parámetro con formato inválido (incluye `reason` fuera de la enumeración cerrada). |
| 422 | `OPTION_NOT_OFFERED` | La opción no figura en la decisión indicada (no fue ofrecida). |
| 422 | `REASON_NOT_AVAILABLE` | `POST human-cases` con `COMPENSATION_REQUESTED` cuando la compensación no es elegible para esa reserva y decisión (FR-067). |
| 422 | `SUPPORT_NOT_AVAILABLE` | `POST human-cases` cuando no hay una acción posible (sin anomalía, decisión INFORMATIVA, solo evidencia degradada o lectura fallida; FR-004, FR-060). |
| 502 | `TRIP_CONTEXT_UNAVAILABLE` | `get_trip_context` falló (timeout, 5xx o 422) tras la re-consulta permitida (FR-105): la vista no puede construirse. |
| 500 | `INTERNAL_ERROR` | Error no previsto; `detail` es genérico, sin trazas. |

---

## 1. INBOUND — Cómo el mundo llama a este sistema

> Cada endpoint, consumer y entry point que el mundo externo utiliza para comunicarse con este sistema.
> **⚠️ SAGRADO**: Si esto cambia, los consumidores dejan de funcionar.
> **Consumidores reales:** el front React de prueba de este mismo repositorio (origen `http://localhost:5173`, modo `user`), las pruebas automatizadas y, con credencial de servicio, *otro sistema* en modo `system` (FR-120). No hay consumidores productivos externos.

### 1.1 Endpoints HTTP Públicos

**Autenticación simulada (FR-001, S-14):** el backend no emite ni valida credenciales. El front fija la cabecera `X-Session-Booking: <booking_id>` según el escenario elegido; la cabecera **solo se acepta con `DEV_SESSION_HEADER_ENABLED=true` (apagada por defecto)**. Todo endpoint `/api/v1/*` compara esa cabecera con el `booking_id` de la ruta (o con el dueño del `decision_id`): sin cabecera (o con la cabecera deshabilitada) responde `401 UNAUTHENTICATED`; si no coinciden, o el recurso no existe, responde `404 NOT_FOUND` **idéntico** (reserva ajena e inexistente son indistinguibles). El `decision_id` es un UUID v4 aleatorio no adivinable. La comprobación de pertenencia **sí** se implementa; la autenticación real queda fuera de v1. **Modo `system` (FR-120):** `POST …/evaluate` con `caller = "system"` se autentica con `X-Service-Key` contra `SERVICE_API_KEY` (apagada por defecto: sin la variable el modo `system` responde `401`); esa credencial **no** autoriza ningún otro endpoint de `/api/v1`.

| # | Método | Path | Descripción | Auth | Headers requeridos |
|---|--------|------|-------------|------|-------------------|
| 1 | GET | `/ping` | Verifica que el servicio responde. Devuelve el texto `pong`. | Ninguna | ninguno |
| 2 | POST | `/api/v1/trips/{booking_id}/evaluate` | Evalúa el viaje con cuerpo `{caller: "user" \| "system"}` (obligatorio). `user` ⇒ vista completa `TripView` (contexto, anomalías, reglas, opciones, acciones, plazos, mensajes, `decision_id`, huella). `system` ⇒ `SystemEvaluationResult` sin PII ni vista, y las notificaciones (política rota y/o cambio de puerta) (FR-002…FR-009, FR-039, FR-110, FR-120…FR-124). | `user`: sesión simulada · `system`: credencial de servicio | `Content-Type: application/json` + `X-Session-Booking` (user) o `X-Service-Key` (system) |
| 3 | POST | `/api/v1/trips/{booking_id}/options/{option_id}/accept` | El pasajero acepta una opción: rebooking, solicitud existente, caso humano (nuevo o existente, con confirmación de posible duplicado) o cambio de estado (FR-050…FR-056, FR-062, FR-070). | Sesión simulada | `X-Session-Booking`, `Content-Type: application/json` |
| 4 | POST | `/api/v1/trips/{booking_id}/human-cases` | El pasajero pide «Hablar con una persona» con un motivo de enumeración cerrada (FR-059…FR-061). | Sesión simulada | `X-Session-Booking`, `Content-Type: application/json` |
| 5 | GET | `/api/v1/decisions/{decision_id}` | Lee el registro de decisión (auditoría) de la reserva dueña de la sesión (FR-093). | Sesión simulada | `X-Session-Booking` |
| 6 | GET | `/api/dev/scenarios` | **Solo desarrollo.** Lista los escenarios del front de prueba. | Ninguna (flag `DEV_ENDPOINTS_ENABLED`, apagado por defecto) | ninguno |
| 7 | PUT | `/api/dev/scenario` | **Solo desarrollo.** Activa un escenario en los *mocks* y reinicia el reloj de escenario. | Ninguna (flag `DEV_ENDPOINTS_ENABLED`, apagado por defecto) | `Content-Type: application/json` |
| 8 | PUT | `/api/dev/clock` | **Solo desarrollo.** Avanza el reloj de escenario (`ScenarioClock`) para demostrar vigencias y vencimientos sin esperar. | Ninguna (flag `DEV_ENDPOINTS_ENABLED`, apagado por defecto) | `Content-Type: application/json` |

**CORS (NFR-003):** solo se permite el origen configurado en `CORS_ALLOWED_ORIGINS` (por defecto `http://localhost:5173`), métodos `GET, POST, PUT, OPTIONS` y cabeceras `Content-Type, X-Session-Booking`.

#### Detalle por endpoint

```
⚠️ SAGRADO: GET /ping
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH: Ninguna
HEADERS REQUERIDOS: ninguno

QUERY PARAMS: ninguno

REQUEST BODY: ninguno

RESPUESTAS:
  200 OK  (Content-Type: text/plain; charset=utf-8)
    pong

SLA: p99 < 50 ms | Timeout cliente recomendado: 2000 ms
```

```
⚠️ SAGRADO: POST /api/v1/trips/{booking_id}/evaluate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evalúa un viaje. La MISMA evaluación (FR-002…FR-009, FR-039) puede pedirla el pasajero (`caller = "user"`) u otro sistema (`caller = "system"`) (FR-120).
Reemplaza al antiguo GET …/view: ya no existe ningún GET de la vista.

AUTH (depende de `caller`):
  - caller = "user": sesión simulada (X-Session-Booking == booking_id de la ruta; solo con DEV_SESSION_HEADER_ENABLED=true, FR-001).
  - caller = "system": credencial de servicio en la cabecera X-Service-Key, comparada en tiempo constante con SERVICE_API_KEY. Está APAGADA por defecto:
    si SERVICE_API_KEY no está configurada, el modo system responde siempre 401. En este modo X-Session-Booking no se usa y no autoriza nada.
    La clave de servicio autoriza evaluar cualquier reserva, pero NUNCA devuelve PII ni la vista completa (FR-120).
HEADERS REQUERIDOS:
  Content-Type: application/json
  X-Session-Booking: <booking_id>             // solo caller = "user"
  X-Service-Key: <clave de servicio>          // solo caller = "system"

PATH PARAMS:
  booking_id (string, requerido): 6 caracteres [A-Z0-9], p. ej. "ABC123"

QUERY PARAMS: ninguno (cada llamada reconsulta get_trip_context y get_operational_events; no hay caché en v1, FR-002)

REQUEST BODY (obligatorio):
  {
    "caller": string                          // OBLIGATORIO. Enumeración cerrada: "user" | "system". Cualquier otro valor, ausencia o campo adicional ⇒ 422 VALIDATION_ERROR
  }

SEMÁNTICA:
  - caller = "user": devuelve la vista completa (TripView) para el pasajero. No invoca ninguna acción externa (FR-085).
  - caller = "system": ejecuta la misma evaluación y devuelve SOLO SystemEvaluationResult. NO ejecuta create_rebooking_request ni create_human_case (FR-121).
    La única acción externa permitida es notify_passenger (FR-050 excepción, FR-122) con NOTIFY_ENABLED = true: una notificación por motivo (hasta 2): DELAY con política rota (aunque la decisión sea BLOQUEADA o PENDIENTE_APROBACION) y GATE_CHANGE validado (aviso informativo sin policy_ref).
    La respuesta no se guarda para el front (FR-124): cuando el pasajero entra, el modo user vuelve a consultar siempre (FR-002).

RESPUESTAS:
  200 OK (caller = "user") → TripView
    {
      decision_id: string,                    // UUID v4 del registro de decisión de esta evaluación
      booking_id: string,
      generated_at: string,                   // ISO-8601 UTC, tomado del puerto Clock
      fingerprint: string,                    // huella de decisión SIN opción: SHA-256 en hex minúscula (64 caracteres); base de la deduplicación de casos humanos (FR-059). La huella que se contrasta al aceptar es POR OPCIÓN: options[].fingerprint (FR-070)
      anomaly_detected: boolean,              // true si hay un evento relevante validado (DELAY ≥ umbral o un tipo de NOTIFY_ONLY_EVENT_TYPES como GATE_CHANGE) o evidencia anómala; false ⇒ solo contexto completo, p. ej. solo STATUS (FR-004, FR-068)
      decision_state: string | null,          // "INFORMATIVA" | "AUTOMATICA" | "PENDIENTE_APROBACION" | "BLOQUEADA"; null si anomaly_detected == false o si falló o es inválida la lectura de contexto o de eventos («sin decisión», FR-066). El fallo de lectura de política u opciones da BLOQUEADA (con soporte). INFORMATIVA = DELAY validado SIN política rota, o viaje solo con GATE_CHANGE (FR-039, FR-068)
      mct_provided: boolean,                  // false ⇒ el MCT del aeropuerto de conexión no fue provisto (FR-022); distinto de un MCT = 0 real
      holder_first_name: string | null,       // nombre de pila del primer pasajero ADULT (única PII mostrada, FR-003/FR-112); null si no hay adulto: el saludo se omite
      passenger_count: integer,               // ≥ 1; 0 solo si load_status.trip_context == "INVALID"
      load_status: {
        trip_context: string,                 // "OK" | "INVALID" (integridad de lectura inválida, FR-066: sin decisión, aviso y reintento, sin soporte; si get_trip_context falla por transporte la respuesta es 502)
        events: string,                       // "OK" | "FAILED"
        policy: string,                       // "OK" | "FAILED" | "NOT_REQUESTED" (no hay DELAY relevante VALIDADO, o hay un bloqueo previo por conflicto, tipo desconocido, INCONSISTENT_DELAY o varios segmentos afectados)
        options: string                       // "OK" | "FAILED" | "NOT_REQUESTED" (se consulta SOLO con política rota; NOT_REQUESTED en INFORMATIVA, sin DELAY relevante validado, con bloqueo previo o si la política falló, está vacía o produjo RULE_ERROR)
      },
      data_as_of: {
        trip_context: string | null,          // _meta.retrieved_at de get_trip_context; null si faltó (vista inválida, FR-066)
        events: string | null,                // null si la lectura falló
        policy: string | null,                // null si no se consultó o falló
        options: string | null                // null si no se consultó o falló
      },
      segments: [SegmentView],
      alerts: [AlertView],                    // [] si anomaly_detected == false
      derived_variables: [DerivedVariableView],
      policy: PolicyView | null,              // política del escenario DELAY; null si no se consultó: sin DELAY relevante validado (p. ej. solo GATE_CHANGE, que NUNCA consulta política) o con bloqueo previo (conflicto/tipo desconocido/INCONSISTENT_DELAY/varios segmentos); en ese caso la pantalla NO muestra reglas
      options: [OptionView],                  // solo opciones VIABLES (FR-042); [] si no hay y siempre [] en INFORMATIVA
      proposed_option_id: string | null,      // opción propuesta (FR-045); null si no hay viable
      refund_notice: MessageView | null,      // vía de reembolso genérica, sin monto ni plazo (FR-046)
      offer_deadline: string | null,          // hora límite = min(expiración de las opciones mostradas), ISO UTC (FR-071); el front calcula la cuenta regresiva contra generated_at
      actions: [ActionView],                  // acciones OFRECIDAS; ninguna se ejecuta sin clic (FR-050). [] en INFORMATIVA, sin anomalía, con solo evidencia degradada y con lectura fallida o inválida; el soporte NO está siempre disponible (FR-004, FR-060)
      human_case_reasons: [string],           // motivos de caso humano que el sistema detecta, de mayor a menor prioridad (FR-063); [] si no hay o si el soporte no se ofrece
      messages: [MessageView],                // todos validados por FR-081
      operations: [OperationView],            // operaciones ACTIVAS (EN_CURSO, INDETERMINADA, CREADA) de la RESERVA, independientes de las opciones mostradas (una opción ya solicitada puede no volver a aparecer)
      human_cases: [HumanCaseView]            // intentos de caso humano de esta misma situación (misma clave de deduplicación) con su estado: permite mostrar el aviso de INDETERMINADO y exigir el segundo clic
    }

  SegmentView:
    {
      segment_id: string,
      flight_number: string,
      origin: string,                         // IATA, 3 letras
      destination: string,                    // IATA, 3 letras
      date: string,                           // YYYY-MM-DD (fecha de salida programada)
      scheduled_departure: string,            // HH:MM local, sin zona
      scheduled_arrival: string,              // HH:MM local, sin zona
      state: string | null,                   // "ON_TIME" | "SCHEDULED" | "DELAYED" | "NO_EVENTS" | "NO_VERIFIED_INFO" | "CONFLICT" | "UNSUPPORTED" | "INCONSISTENT"; null si la lectura de eventos falló (FR-105). NO_EVENTS = el segmento no tiene ningún evento, o solo eventos que no informan la salida (p. ej. GATE_CHANGE): se muestra su horario programado, sin afirmar estado ni alertar (FR-014). NO_VERIFIED_INFO = SOLO evidencia degradada (FR-014)
      affected: boolean,                      // true si es el segmento con DELAY relevante (FR-019)
      delay_minutes: integer | null,          // solo si state == "DELAYED"
      new_departure: string | null,           // HH:MM local, solo si state == "DELAYED"
      new_arrival_local: string | null,       // "YYYY-MM-DDTHH:MM" ESTIMADA (FR-021); null si no aplica
      gate: string | null,                    // puerta informada por GATE_CHANGE no degradado; SE MUESTRA SIEMPRE, destacada (FR-006)
      gate_recorded_at: string | null,        // recorded_at (ISO UTC) del GATE_CHANGE que sustenta la puerta: hora de la información de la puerta
      information_as_of: string | null        // recorded_at (ISO UTC) del evento que sustenta el estado
    }

  AlertView:
    {
      code: string,                           // "DELAY" | "GATE_CHANGE" | "SOURCE_CONFLICT" | "UNSUPPORTED_EVENT_TYPE" | "INCONSISTENT_DELAY" | "MULTIPLE_AFFECTED_SEGMENTS" | "CONNECTION_AT_RISK" | "OVERNIGHT"
      segment_id: string | null,
      severity: string,                       // "INFO" | "WARNING" | "CRITICAL"
      message_id: string                      // referencia a un elemento de messages[]
    }

  DerivedVariableView:                        // FR-028
    {
      name: string,                           // "delay_minutes" | "new_arrival" | "missed_connection" | "international" | "group_includes_minor" | "compensation_requested" | "overnight_required"
      segment_id: string | null,
      value: boolean | integer | string | null,  // null ⇒ desconocido
      known: boolean,                         // false ⇒ valor desconocido (lógica trivaluada, FR-033)
      origin: string,                         // "DATO" | "DERIVADA"
      estimated: boolean,                     // true ⇒ rotulada ESTIMADA (new_arrival, missed_connection)
      assumptions: [string]                   // códigos: "FULL_DELAY_PROPAGATION" | "MCT_NOT_PROVIDED" | "NEXT_SEGMENT_NOT_HELD" | "TIMEZONE_TABLE_V1" | "MINOR_IS_TYPE_CHILD" | "COMPENSATION_DEFAULT_FALSE"
    }

  PolicyView:
    {
      scenario: string,                       // escenario consultado (POLICY_SCENARIOS; en la Fase 1 solo "DELAY")
      status: string,                         // "EVALUATED" | "RULE_ERROR" (⇒ BLOQUEADA) | "EMPTY" (vacía o inexistente ⇒ BLOQUEADA, FR-008) | "UNAVAILABLE" (lectura fallida ⇒ BLOQUEADA con soporte)
      version: string | null,                 // p. ej. "POL-DELAY-2026-03"
      effective_from: string | null,          // YYYY-MM-DD
      entitlements: [string],                 // unión de derechos de las reglas cumplidas (FR-037); códigos tal cual
      requires_human_approval: boolean,       // true si cualquier regla cumplida la exige (FR-035) o por FR-008
      rules: [RuleView]
    }

  RuleView:                                   // FR-034
    {
      rule_id: string,
      condition: string,                      // texto de la regla tal como llegó
      entitlement: string,                    // código del derecho, sin interpretarlo si es desconocido
      requires_human_approval: boolean,
      result: string,                         // "CUMPLE" | "NO_CUMPLE" | "INDETERMINADA" (la interfaz muestra «no evaluable»)
      variables_used: [ {name: string, value: boolean | integer | null, known: boolean} ]
    }

  OptionView:                                 // solo viables (FR-041); `confidence` NO se expone (FR-044)
    {
      option_id: string,
      itinerary_key: string,                  // clave de itinerario: SHA-256 hex de (flight_number|date|origin|destination|departure); identifica la opción entre lecturas (option_id es local, DAT-44) y es lo que el cliente devuelve al aceptar (FR-065)
      type: string,                           // "REBOOK"
      flight_number: string,
      origin: string,
      destination: string,
      date: string,                           // YYYY-MM-DD
      departure: string,                      // HH:MM local, sin zona
      fare_difference: integer,               // entero sin decimales (CLP); 0 = sin diferencia
      currency: string | null,                // código ISO; presente si fare_difference > 0
      seats_available: integer,
      policy_ref: string,
      fingerprint: string,                    // huella FR-070 POR OPCIÓN (64 hex): decisión + itinerario de esta opción + (seats_available ≥ pasajeros) + fare_difference + policy_ref; es lo que el cliente devuelve al aceptar
      is_proposed: boolean,
      overnight: boolean | null,              // FR-029; null si no se deriva
      expires_at: string                      // retrieved_at + ttl_seconds, ISO UTC (FR-017)
    }

  ActionView:                                 // acción OFRECIDA, nunca ejecutada sin clic (FR-050)
    {
      action_id: string,
      kind: string,                           // "ACCEPT_OPTION" | "OPEN_HUMAN_CASE"
      option_id: string | null,               // solo en ACCEPT_OPTION
      effect: string,                         // "CREATE_REBOOKING" | "CREATE_HUMAN_CASE_WITH_OPTION" | "CREATE_HUMAN_CASE"
      enabled: boolean,                       // false mientras hay una operación en curso (FR-062)
      disabled_reason: string | null,         // "OPERATION_IN_PROGRESS" | null
      offered_reasons: [string]               // en OPEN_HUMAN_CASE: ["OTHER_HELP","PERSONAL_DATA_REQUEST"] y, SOLO si hay compensación elegible (FR-067), también "COMPENSATION_REQUESTED"; [] en ACCEPT_OPTION. OPEN_HUMAN_CASE solo existe cuando hay una acción posible (FR-060)
    }

  MessageView:
    {
      message_id: string,
      template_id: string,                    // plantilla del catálogo (FR-080)
      kind: string,                           // "INFO" | "ESTIMATE" | "WARNING" | "NEXT_STEP" | "DEADLINE"
      text: string,                           // español neutro; sin PII salvo el nombre de pila (FR-112)
      evidence_refs: [string],                // ids de evidencia que sustentan cada afirmación (FR-080)
      policy_ref: string | null               // obligatorio si el mensaje afirma una opción o un derecho (FR-081)
    }

  OperationView:
    {
      itinerary_key: string,                  // identifica el itinerario solicitado, aunque la opción ya no se muestre
      option_id: string | null,               // id local en la decisión actual; null si la opción ya no figura
      flight_number: string,                  // resumen del itinerario solicitado (hechos operacionales, FR-091)
      origin: string,
      destination: string,
      date: string,                           // YYYY-MM-DD
      departure: string,                      // HH:MM local, sin zona
      state: string,                          // "EN_CURSO" | "INDETERMINADA" | "CREADA" | "FALLIDA" | "EXPIRADA" (ciclo de vida de FR-064)
      generation: integer,                    // generación de la llave idempotente (1, 2, …)
      request_id: string | null,              // "RBK-…" opaco
      request_status: string | null,          // p. ej. "PENDING_CONFIRMATION"; enumeración abierta (DAT-69)
      expires_at: string | null               // ISO UTC
    }

  HumanCaseView:
    {
      state: string,                          // "EN_CURSO" | "CREADO" | "FALLIDO" | "INDETERMINADO" (resultado del último intento, FR-059/FR-105)
      case_id: string | null,                 // "HC-…" opaco; null si state != "CREADO"
      reason: string,                         // motivo de mayor prioridad (FR-063)
      reasons: [string],                      // todos los motivos simultáneos
      queue: string | null,                   // null si state != "CREADO"
      sla_minutes: integer | null             // null si state != "CREADO"
    }

  SystemEvaluationResult (200 OK cuando caller = "system"; sin PII, sin vista completa, sin opciones, sin acciones del pasajero):
    {
      decision_id: string,                    // UUID v4 del registro de decisión
      decision_state: string | null,          // "INFORMATIVA" | "AUTOMATICA" | "PENDIENTE_APROBACION" | "BLOQUEADA"; null si no hay anomalía o falló la lectura de contexto o de eventos
      reason: string | null,                  // causa principal del cambio, enumeración CERRADA: "DELAY" (si hay retraso relevante) | "GATE_CHANGE" (si solo hay cambio de puerta); null si no hay un cambio que informar
      notifications: [                        // una por motivo candidato (0 a 2): DELAY (política rota) y/o GATE_CHANGE (validado); [] si no hay ningún candidato
        {
          reason: string,                     // "DELAY" | "GATE_CHANGE"
          kind: string,                       // "POLICY" (con policy_ref) | "INFORMATIONAL" (sin policy_ref, H-21)
          status: string,                     // "EN_CURSO" (solo con deduplicated = true: el primer envío sigue pendiente) | "QUEUED" | "FALLIDA" | "INDETERMINADA" | "NOT_SENT"
          notification_id: string | null,     // "NT-…" opaco; solo con status "QUEUED"
          not_sent_reason: string | null,     // solo con "NOT_SENT": "NOTIFY_DISABLED" | "NO_BROKEN_POLICY" (DELAY sin política rota o con anomalía que impide evaluarla) | "NO_ADULT_RECIPIENT" (la reserva no tiene titular adulto: no se envía y se marca needs_manual_review, FR-122)
          deduplicated: boolean,              // true si se aplicó el enfriamiento: no se reenvió y status es el del envío previo (FR-123)
          attempts: integer                   // llamadas a notify_passenger realizadas ahora (0 … 1 + NOTIFY_MAX_RETRIES)
        }
      ],
      needs_manual_review: boolean            // true si la decisión es BLOQUEADA, hubo lectura fallida o la reserva no tiene titular adulto (FR-122): queda en la auditoría para revisión interna (FR-123); es independiente de las notificaciones (BLOQUEADA con política rota SÍ notifica y además queda en revisión)
    }

  401 Unauthorized:        {"error": "UNAUTHENTICATED", "detail": "Faltan las credenciales de la sesión o del servicio."}   // user: sin cabecera de sesión (o deshabilitada); system: sin X-Service-Key, clave incorrecta o SERVICE_API_KEY no configurada
  404 Not Found:           {"error": "NOT_FOUND", "detail": "No encontramos el recurso solicitado."}   // solo caller = "user": reserva ajena o inexistente, cuerpo idéntico (FR-001)
  422 Unprocessable:       {"error": "VALIDATION_ERROR", "detail": "El cuerpo debe incluir caller con el valor user o system."}
  422 Unprocessable:       {"error": "VALIDATION_ERROR", "detail": "El booking_id debe tener 6 caracteres alfanuméricos en mayúscula."}
  502 Bad Gateway:         {"error": "TRIP_CONTEXT_UNAVAILABLE", "detail": "No pudimos cargar tu viaje."}   // ambos modos
  429 Too Many Requests:   {"error": "RATE_LIMITED", "detail": "Demasiadas solicitudes. Intenta de nuevo en un minuto."}   // más de EVALUATE_RATE_LIMIT_PER_MINUTE solicitudes por minuto por reserva y credencial (NFR-013)
  500 Internal Server Error: {"error": "INTERNAL_ERROR", "detail": "Ocurrió un error inesperado."}

REGLAS:
  - Orden de comprobaciones: 422 (cuerpo y caller) → 401 (credenciales según caller) → 429 (límite de tasa por reserva y credencial, NFR-013) → 404 (pertenencia, solo user) → 422 (formato de booking_id) → lectura de datos.
    El 422 por formato de booking_id solo es alcanzable cuando la sesión y la ruta coinciden (user) o la credencial es válida (system); una reserva ajena con formato inválido recibe 404, no 422.
  - CONTEXTO COMPLETO (FR-068): la evaluación considera TODOS los eventos validados de TODOS los segmentos (retraso, puerta, estado) en conjunto, y la vista los muestra todos.
  - CAMBIO DE PUERTA (FR-006): en modo user la vista muestra SIEMPRE el cambio de puerta validado, destacado y con la hora de la información (SegmentView.gate + gate_recorded_at y una AlertView "GATE_CHANGE"),
    haya o no retraso, política rota u opciones. GATE_CHANGE NO consulta política (FR-068): solo se informa (user) o se notifica (system, FR-122 caso b).
  - EVENTOS ADMITIDOS (FR-068): SUPPORTED_EVENT_TYPES (por defecto DELAY, GATE_CHANGE, STATUS). Un tipo fuera de la lista no se interpreta ⇒ UNSUPPORTED_EVENT_TYPE (FR-007).
  - POLÍTICA SOLO PARA DELAY (FR-068, Fase 1): solo un DELAY relevante VALIDADO consulta get_policy_rules(escenario); POLICY_SCENARIOS (por defecto solo DELAY → "DELAY") es configurable para la Fase 2,
    pero los tipos de NOTIFY_ONLY_EVENT_TYPES (por defecto GATE_CHANGE) NUNCA consultan política, aunque figuren en POLICY_SCENARIOS (TC-53). No existe política mock para GATE_CHANGE.
  - Cadena de lecturas SECUENCIAL (FR-009, NFR-004): get_trip_context → get_operational_events (necesita los segment_ids) → SOLO con un DELAY relevante VALIDADO y ningún bloqueo previo, get_policy_rules("DELAY") →
    SOLO si hay POLÍTICA ROTA (y la política no está vacía ni dio RULE_ERROR), get_eligible_options. No hay llamadas en paralelo; con eso se arma la vista. Máximo 4 lecturas.
  - anomaly_detected = true si hay un evento relevante validado (DELAY ≥ RELEVANT_DELAY_MIN_MINUTES o un tipo de NOTIFY_ONLY_EVENT_TYPES) o evidencia anómala; false ⇒ solo contexto completo, p. ej. solo STATUS (FR-004).
  - Política rota (FR-039): al menos una regla CUMPLIDA de la política DELAY cuyos derechos incluyen un derecho de remedio (REMEDY_RIGHTS; por defecto REBOOK_NO_FEE, MEAL_VOUCHER, CASH_COMPENSATION).
    Los derechos que no son de remedio (PRIORITY_HANDLING) no la rompen por sí solos.
  - Estado de la decisión (en este orden):
      1. Lectura de contexto o de eventos fallida o inválida ⇒ decision_state = null (aviso y reintento, sin soporte).
      2. Bloqueo previo por evidencia (SOURCE_CONFLICT —empate de recorded_at—, UNSUPPORTED_EVENT_TYPE, INCONSISTENT_DELAY, MULTIPLE_AFFECTED_SEGMENTS) ⇒ BLOQUEADA; política y opciones NOT_REQUESTED (policy = null, sin reglas en pantalla).
         Cadena de segmentos rota o menor sin adulto ⇒ BLOQUEADA, pero sí se consulta la política.
      3. Sin evento relevante validado ⇒ anomaly_detected = false, decision_state = null (solo contexto).
      4. Solo eventos de NOTIFY_ONLY_EVENT_TYPES (p. ej. solo GATE_CHANGE) ⇒ INFORMATIVA: sin política, sin opciones, sin soporte (FR-068).
      5. Fallo de lectura de get_policy_rules o de get_eligible_options (timeout, 5xx o 422 tras la re-consulta) ⇒ BLOQUEADA, con una anomalía que exige validación manual (BLOCKING_PARTIAL_DATA);
         el soporte SÍ se ofrece y needs_manual_review = true (FR-105, FR-086). load_status.<lectura> = "FAILED".
      6. Política de DELAY vacía o inexistente, regla cumplida sin requires_human_approval booleano o RULE_ERROR ⇒ BLOQUEADA (opciones NOT_REQUESTED).
      7. Sin política rota ⇒ INFORMATIVA (salvo una regla «no evaluable» con derechos de remedio ⇒ BLOQUEADA, FR-033); la regla de aprobación no cambia el estado (FR-035); opciones NOT_REQUESTED.
      7b. Con `missed_connection` desconocido (FR-041 f) ninguna opción es viable por itinerario incierto: la decisión es BLOQUEADA, las opciones se consultan pero todas quedan descartadas con `ITINERARY_MISMATCH` y se ofrece soporte (TC-60).
      8. Con política rota: alguna regla «no evaluable» (p. ej. menor desconocido) **o** una composición de grupo desconocida (`group_includes_minor` desconocido, FR-024) ⇒ BLOQUEADA (validación manual, FR-024/FR-033/FR-038, `BLOCKING_PARTIAL_DATA`), **aunque la política no traiga una regla como R5** (el bloqueo por composición desconocida es independiente de R5); alguna regla cumplida exige aprobación ⇒ PENDIENTE_APROBACION; en otro caso ⇒ AUTOMATICA. Las opciones se consultan.
  - INFORMATIVA (FR-039): se informa el evento (retraso y/o puerta) y, si hubo política, se muestran las reglas evaluadas; SIN opciones, SIN acciones, SIN botón de soporte y SIN compensación. load_status.options = "NOT_REQUESTED".
    En modo system, un GATE_CHANGE validado se notifica aunque la decisión sea INFORMATIVA (FR-122 caso b).
  - Soporte («Hablar con una persona») ya NO está siempre disponible (FR-004, FR-060): solo hay una acción OPEN_HUMAN_CASE cuando hay una acción posible, es decir, decisión AUTOMATICA/PENDIENTE_APROBACION/BLOQUEADA
    (política rota o anomalía que exige validación manual, INCLUIDO el fallo de lectura de política u opciones del paso 5). No se ofrece con anomaly_detected = false, con INFORMATIVA (incluido el viaje solo con GATE_CHANGE),
    con solo evidencia degradada (FR-014), ni con fallo o invalidez de la lectura de contexto o de eventos (FR-066, FR-086).
  - Motivo de compensación elegible (FR-067): offered_reasons incluye COMPENSATION_REQUESTED solo si la política tiene una regla con derecho de COMPENSATION_RIGHTS (por defecto CASH_COMPENSATION) que, evaluada con compensation_requested = true y las demás variables ya calculadas, resulta verdadera, y la decisión no es INFORMATIVA.
  - Integridad de lecturas (FR-066): retrieved_at ausente, 0 segmentos, 0 pasajeros o formato inválido ⇒ lectura fallida: 200 con decision_state = null, load_status.<lectura> = "INVALID"/"FAILED", aviso y reintento (sin soporte ofrecido).
    Cadena de segmentos rota o menor sin adulto ⇒ decision_state = "BLOQUEADA" con missed_connection desconocido y BLOCKING_PARTIAL_DATA. Segmentos desordenados ⇒ se reordenan, sin bloqueo.
  - Falla solo get_operational_events ⇒ 200 con segments[].state = null, alerts = [], load_status.events = "FAILED", decision_state = null, un mensaje de aviso y sin soporte (FR-105).
  - Resultado cuando faltan datos por causa: «lectura fallida» de contexto o eventos (sin decisión, sin soporte) ≠ «BLOQUEADA» (decisión tomada que exige validación manual, con soporte), que incluye el fallo de política u opciones.
  - Eventos (FR-012, FR-013): un STATUS sano (SCHEDULED —vuelta al horario programado— u ON_TIME) más reciente que un DELAY lo reemplaza ⇒ el segmento queda SCHEDULED u ON_TIME y no hay retraso; uno más antiguo o degradado NO lo borra ni lo reemplaza.
    El conflicto (SOURCE_CONFLICT) existe SOLO ante un empate de recorded_at entre eventos sanos con afirmaciones incompatibles (tabla configurable ASSERTION_COMPATIBILITY).
  - Cada respuesta 200 crea un registro de decisión (FR-090) con el decision_id devuelto; la huella excluye marcas de tiempo, option_id, confidence y vigencia (FR-070). En modo system el registro incluye caller, needs_manual_review y el estado de cada notificación.
  - Notificación (caller = "system", FR-122/FR-123): ver el contrato OUTBOUND notify_passenger. Con NOTIFY_ENABLED = true se envía UNA notificación por motivo (hasta 2): (a) DELAY con POLÍTICA ROTA ⇒ kind POLICY con policy_ref, aunque la decisión sea BLOQUEADA o PENDIENTE_APROBACION;
    (b) GATE_CHANGE validado ⇒ kind INFORMATIONAL, sin policy_ref y sin consultar política. Sin política rota y sin GATE_CHANGE validado ⇒ nada se envía y, si la decisión es BLOQUEADA o la lectura falló, needs_manual_review = true.

SLA: p95 < 1500 ms con upstreams simulados de 100 ms (NFR-004: 4 × 100 ms + proceso) | PEOR CASO user 16 000 ms; system 47 200 ms (ver «Presupuesto de tiempos») | Timeout cliente recomendado: user 20000 ms; system 55000 ms
```

```
⚠️ SAGRADO: POST /api/v1/trips/{booking_id}/options/{option_id}/accept
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH: sesión simulada (X-Session-Booking == booking_id de la ruta)
HEADERS REQUERIDOS:
  X-Session-Booking: <booking_id>
  Content-Type: application/json

PATH PARAMS:
  booking_id (string, requerido): 6 caracteres [A-Z0-9]
  option_id (string, requerido): id de una opción de la decisión indicada (p. ej. "O1"); local a la respuesta de get_eligible_options (DAT-44)

QUERY PARAMS: ninguno

REQUEST BODY:
  {
    "decision_id": string,                    // UUID de la decisión mostrada al pasajero (su instantánea)
    "itinerary_key": string,                  // OptionView.itinerary_key de la opción elegida (FR-065)
    "fingerprint": string,                    // OptionView.fingerprint: la huella POR OPCIÓN mostrada (64 hex, FR-070)
    "confirm_possible_duplicate": boolean     // opcional, por defecto false: segundo clic explícito tras un intento INDETERMINADO de caso humano (FR-105)
  }
  - El cliente NUNCA aporta el contenido de la opción (vuelo, fecha, costo…): el servidor la resuelve con la decisión guardada y,
    para un rebooking, con las opciones recién consultadas, localizándola por itinerary_key (FR-065).
  - El servidor contrasta {itinerary_key, fingerprint} con SU instantánea guardada de la decisión: si option_id, itinerary_key y
    fingerprint no corresponden a la misma opción de esa decisión ⇒ 422 OPTION_NOT_OFFERED (o 422 VALIDATION_ERROR si la huella no coincide con la guardada).
  - `confirm_possible_duplicate` solo tiene efecto cuando la aceptación deriva a un caso humano (ver abajo); en un rebooking se ignora.

SEMÁNTICA (un clic autoriza exactamente una acción, FR-050):
  - decision_state == "AUTOMATICA": revalida (reconsulta contexto del viaje, eventos, política y opciones; recalcula la huella de esa opción, FR-070):
      · Huella distinta ⇒ NO se escribe: 409 STATE_CHANGED con la vista nueva.
      · Opción re-consultada vencida en el instante de escribir (FR-017) ⇒ se refresca UNA vez (FR-072); la viabilidad (FR-041) y la huella
        se recalculan sobre la NUEVA respuesta; si sigue vencida o ya no es viable ⇒ 409 STATE_CHANGED.
      · Huella igual y opción vigente: calcula la llave idempotente (FR-053) con la generación vigente, registra la operación (EN_CURSO)
        de forma atómica ANTES de llamar —si la llave no pudo persistirse, NO se escribe (FR-064)— e invoca create_rebooking_request con
        (option, idempotency_key, booking_id, passenger_ids de TODO el grupo) (FR-065) y hasta 2 reintentos con la MISMA llave (FR-054).
  - decision_state == "PENDIENTE_APROBACION" o "BLOQUEADA": NO se llama create_rebooking_request; se crea un caso humano con la opción
    elegida como evidencia, sin revalidar (FR-052, FR-059), con la misma reserva atómica de clave y el mismo registro de intentos que POST human-cases.
    El caso conserva la opción elegida: ante NEEDS_CONFIRMATION, el cliente repite la MISMA petición {decision_id, itinerary_key, fingerprint}
    añadiendo confirm_possible_duplicate = true, y el intento nuevo conserva esa opción como evidencia.
  - Operación ya EN_CURSO, INDETERMINADA o CREADA para el mismo itinerario: no se escribe de nuevo; se devuelve su estado (FR-062).
    EXPIRADA o FALLIDA permiten una operación nueva con la generación siguiente (FR-064).

RESPUESTAS (todas con el mismo cuerpo AcceptResult, incluidas 409, 502 y 504; solo 401/404/422/500 usan el esquema {error, detail}):
  AcceptResult:
    {
      outcome: string,                      // "REBOOKING_CREATED" | "EXISTING_REQUEST" | "HUMAN_CASE_CREATED" | "EXISTING_CASE" | "NEEDS_CONFIRMATION" | "STATE_CHANGED" | "FAILED"
      message: MessageView,                 // texto validado por FR-081
      operation: OperationView | null,      // presente en REBOOKING_CREATED, EXISTING_REQUEST y en FAILED por error del rebooking
      human_case: HumanCaseView | null,     // presente en HUMAN_CASE_CREATED, EXISTING_CASE, NEEDS_CONFIRMATION y en FAILED por fallo del caso humano
      retries: integer,                     // reintentos de create_rebooking_request realizados (0…2)
      view: TripView | null                 // vista nueva; presente solo en STATE_CHANGED
    }

  201 Created   outcome = "REBOOKING_CREATED"
      create_rebooking_request devolvió 201; operation.state = "CREADA", request_status = "PENDING_CONFIRMATION",
      expires_at presente. message: «solicitud registrada, pendiente de confirmación, sujeta a disponibilidad» (FR-056).
  200 OK        outcome = "EXISTING_REQUEST"
      create_rebooking_request devolvió 409 DUPLICATE_REQUEST, o la operación ya existía (EN_CURSO/INDETERMINADA/CREADA):
      «ya existe una solicitud en curso para esta opción» (FR-055, FR-062). Sin bucles.
      409 sin operación local: se registra una operación INDETERMINADA con el request_id devuelto y el mensaje dice
      «ya existe una solicitud para esta opción» (FR-064).
  201 Created   outcome = "HUMAN_CASE_CREATED"
      Caso humano creado: por decisión PENDIENTE_APROBACION/BLOQUEADA (FR-052), o tras 503/timeout persistente
      (motivo UPSTREAM_INDETERMINATE, FR-054; la operación queda INDETERMINADA). Nunca se informa éxito ni fracaso del rebooking.
  200 OK        outcome = "EXISTING_CASE"
      Ya hay un caso CREADO con la misma clave de deduplicación, o un intento EN_CURSO vigente (human_case.state = "CREADO" o "EN_CURSO"): no se envía nada nuevo.
  409 Conflict  outcome = "NEEDS_CONFIRMATION"
      Intento previo de caso humano INDETERMINADO y confirm_possible_duplicate = false: NO se reenvía; human_case.state = "INDETERMINADO";
      el mensaje advierte del posible duplicado («no pudimos confirmar si tu solicitud anterior quedó registrada; si la envías de nuevo podría duplicarse»).
  409 Conflict  outcome = "STATE_CHANGED"
      La huella recalculada difiere de la mostrada (o la opción ya no existe, no es viable o sigue vencida tras el refresco): NO se escribió nada;
      view contiene el nuevo estado (FR-070).
  502 Bad Gateway outcome = "FAILED"
      422 o error no reintentable de create_rebooking_request (operation.state = "FALLIDA"), o falla la creación del caso humano
      (human_case.state = "FALLIDO", o "INDETERMINADO" si fue timeout/respuesta perdida: «no pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté», FR-105):
      mensaje genérico de fallo y caso humano ofrecido. Nunca se afirma éxito.
  401 Unauthorized:  {"error": "UNAUTHENTICATED", "detail": "Falta la cabecera X-Session-Booking."}
  404 Not Found:     {"error": "NOT_FOUND", "detail": "No encontramos el recurso solicitado."}   // reserva ajena/inexistente o decision_id inexistente/ajeno: cuerpo idéntico (FR-001)
  422 Unprocessable: {"error": "VALIDATION_ERROR", "detail": "El cuerpo debe incluir decision_id, itinerary_key y fingerprint válidos."}
  422 Unprocessable: {"error": "OPTION_NOT_OFFERED", "detail": "La opción no fue ofrecida en esa decisión."}
  429 Too Many Requests:   {"error": "RATE_LIMITED", "detail": "Demasiadas solicitudes. Intenta de nuevo en un minuto."}   // más de EVALUATE_RATE_LIMIT_PER_MINUTE solicitudes por minuto por reserva y por origen (NFR-013)
  500 Internal Server Error: {"error": "INTERNAL_ERROR", "detail": "Ocurrió un error inesperado."}

SLA: camino feliz p95 < 1000 ms con upstreams de 100 ms | PEOR CASO 40 600 ms (ver «Presupuesto de tiempos») | Timeout cliente recomendado: 45000 ms
```

```
⚠️ SAGRADO: POST /api/v1/trips/{booking_id}/human-cases
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH: sesión simulada (X-Session-Booking == booking_id de la ruta)
HEADERS REQUERIDOS:
  X-Session-Booking: <booking_id>
  Content-Type: application/json

PATH PARAMS:
  booking_id (string, requerido): 6 caracteres [A-Z0-9]

QUERY PARAMS: ninguno

REQUEST BODY:
  {
    "reason": string,                         // enumeración CERRADA: "PERSONAL_DATA_REQUEST" | "OTHER_HELP" | "COMPENSATION_REQUESTED" (este último solo si hay compensación elegible, FR-067)
    "decision_id": string,                    // opcional (UUID): decisión que vio el pasajero (FR-059)
    "confirm_possible_duplicate": boolean     // opcional, por defecto false: segundo clic explícito tras un intento INDETERMINADO (FR-105)
  }
  - NO existe texto libre ni campo `note` (FR-060, FR-091). Cualquier otro campo ⇒ 422 VALIDATION_ERROR.
  - `confirm_possible_duplicate` es una extensión mínima del contrato para materializar el «segundo clic explícito» de FR-105.
  - Un clic sobre un botón con motivo ya conocido por el sistema (p. ej. SOURCE_CONFLICT) envía reason = "OTHER_HELP" con el decision_id:
    el servidor fija el motivo principal según FR-063.

SEMÁNTICA:
  - Con `decision_id` (de la sesión): la evidencia sale de la decisión GUARDADA (lo que el pasajero vio), incluida su proyección mínima persistida
    (passenger_count, estado por segmento, versión de política, data_as_of; sin PII), de modo que NO se relee ninguna lectura (FR-059).
    Sin `decision_id`: de una evaluación FRESCA en el instante del clic (mismo proceso de la vista; registra una decisión nueva).
  - Reúne TODOS los motivos aplicables (los del sistema + el elegido por el pasajero) y fija `reason` = el de mayor prioridad según FR-063; `reasons` conserva todos.
  - "COMPENSATION_REQUESTED" fija compensation_requested = true en la evaluación (FR-025, FR-060).
  - "PERSONAL_DATA_REQUEST" abre caso humano; la respuesta NUNCA contiene PII ni campos de la lista prohibida (FR-061).
  - Deduplicación local: SHA-256(booking_id ‖ motivos ordenados ‖ huella de decisión) (FR-059). Si ya hay un caso CREADO ⇒ EXISTING_CASE.
    La deduplicación NO bloquea el reintento explícito cuando el intento previo fue FALLIDO o INDETERMINADO.
  - RESERVA ATÓMICA ANTES DE LLAMAR: se inserta el intento (dedup_key, attempt) en estado EN_CURSO con un índice único parcial; un intento concurrente
    mientras existe uno EN_CURSO vigente NO envía nada y devuelve EXISTING_CASE con human_case.state = "EN_CURSO". Si la reserva no puede persistirse, no se envía.
  - RECUPERACIÓN TRAS CAÍDA: un intento EN_CURSO con más de OPERATION_STALE_SECONDS sin respuesta pasa a INDETERMINADO (el proceso pudo caer tras enviar) y exige confirm_possible_duplicate.
  - Cada intento y su resultado (CREADO | FALLIDO | INDETERMINADO) se registran (tabla human_cases, un registro por intento).
  - Intento previo INDETERMINADO y confirm_possible_duplicate = false ⇒ NO se reenvía: 409 NEEDS_CONFIRMATION con la advertencia del posible duplicado.
  - Timeout o respuesta perdida de create_human_case ⇒ INDETERMINADO: nunca se reenvía automáticamente (la tool no tiene llave idempotente) (FR-105).
  - Es una acción externa autorizada por el clic del pasajero (FR-050).
  - SOPORTE SOLO CON ACCIÓN POSIBLE (FR-004, FR-060): si la decisión es INFORMATIVA (incluido el viaje solo con GATE_CHANGE), no hay anomalía, solo hay evidencia degradada o falló/es inválida la lectura de contexto o de eventos ⇒ 422 SUPPORT_NOT_AVAILABLE.
    EXCEPCIÓN EXPLÍCITA: el fallo de lectura de get_policy_rules o de get_eligible_options deja la decisión BLOQUEADA con una anomalía que exige validación manual (BLOCKING_PARTIAL_DATA): ahí el soporte SÍ se ofrece y este endpoint NO devuelve 422 SUPPORT_NOT_AVAILABLE.
  - COMPENSATION_REQUESTED SOLO SI ES ELEGIBLE (FR-067): el servidor lo acepta solo si la política tiene una regla con derecho de COMPENSATION_RIGHTS que, evaluada con
    compensation_requested = true y las demás variables ya calculadas, resulta verdadera, y la decisión no es INFORMATIVA (con decision_id se usa la elegibilidad guardada de esa decisión);
    en otro caso ⇒ 422 REASON_NOT_AVAILABLE. El menú de la vista (offered_reasons) ya no lo ofrece.

RESPUESTAS (todas con el mismo cuerpo HumanCaseResult, incluidas 409, 502 y 504; solo 401/404/422/500 usan el esquema {error, detail}):
  HumanCaseResult:
    {
      outcome: string,                      // "HUMAN_CASE_CREATED" | "EXISTING_CASE" | "NEEDS_CONFIRMATION" | "INDETERMINATE" | "FAILED"
      message: MessageView,                 // «Registramos tu solicitud; una persona te contactará…» sin plazos distintos del sla_minutes devuelto
      human_case: HumanCaseView | null,     // null si no hay intento registrado todavía
      decision_id: string                   // decisión de la que salió la evidencia (la indicada o la evaluada en el clic)
    }

  201 Created   outcome = "HUMAN_CASE_CREATED"
  200 OK        outcome = "EXISTING_CASE"   (misma clave con un caso CREADO, o con un intento EN_CURSO vigente: se devuelve el existente)
  409 Conflict  outcome = "NEEDS_CONFIRMATION"   «no pudimos confirmar si tu solicitud anterior quedó registrada; si la envías de nuevo podría duplicarse»; requiere reenviar con confirm_possible_duplicate = true
  504 Gateway Timeout outcome = "INDETERMINATE"  «no pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté»; human_case.state = "INDETERMINADO"; sin reenvío automático
  502 Bad Gateway outcome = "FAILED"        error explícito (4xx/5xx con respuesta): «no pudimos registrar tu solicitud, puedes reintentar» (FR-105); no se afirma éxito; human_case.state = "FALLIDO"
  401 Unauthorized:  {"error": "UNAUTHENTICATED", "detail": "Falta la cabecera X-Session-Booking."}
  404 Not Found:     {"error": "NOT_FOUND", "detail": "No encontramos el recurso solicitado."}   // reserva o decision_id ajenos/inexistentes: cuerpo idéntico (FR-001)
  422 Unprocessable: {"error": "VALIDATION_ERROR", "detail": "El motivo debe ser COMPENSATION_REQUESTED, PERSONAL_DATA_REQUEST u OTHER_HELP."}
  422 Unprocessable: {"error": "REASON_NOT_AVAILABLE", "detail": "Ese motivo no está disponible para esta reserva."}
  422 Unprocessable: {"error": "SUPPORT_NOT_AVAILABLE", "detail": "No hay una acción de soporte disponible para esta reserva."}
  429 Too Many Requests:   {"error": "RATE_LIMITED", "detail": "Demasiadas solicitudes. Intenta de nuevo en un minuto."}   // más de EVALUATE_RATE_LIMIT_PER_MINUTE solicitudes por minuto por reserva y por origen (NFR-013)
  500 Internal Server Error: {"error": "INTERNAL_ERROR", "detail": "Ocurrió un error inesperado."}

SLA: p95 < 1500 ms con upstreams de 100 ms | PEOR CASO 5 000 ms con decision_id y 21 000 ms sin él (evaluación fresca) | Timeout cliente recomendado: 25000 ms
```

```
⚠️ SAGRADO: GET /api/v1/decisions/{decision_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH: sesión simulada (el booking_id dueño del registro == X-Session-Booking; si no coincide o no existe ⇒ el mismo 404 NOT_FOUND)
HEADERS REQUERIDOS:
  X-Session-Booking: <booking_id>
  Accept: application/json

PATH PARAMS:
  decision_id (string, requerido): UUID v4

QUERY PARAMS: ninguno

REQUEST BODY: ninguno

RESPUESTAS:
  200 OK  → DecisionRecord (solo campos de la lista cerrada de FR-091; sin payloads, nombres, contacto, documento ni edad).
    CAMPOS INTERNOS (FR-093, FR-123): la sesión del pasajero NO recibe `needs_manual_review` ni el detalle de `notifications` (estado, motivo y `notification_id` de cada aviso). Ambos se persisten en el registro de la decisión para la revisión interna y el reporte de métricas, pero esta lectura no los devuelve (TC-59).
    {
      decision_id: string,
      booking_id: string,
      created_at: string,                       // ISO UTC
      fingerprint: string,                      // 64 hex
      anomaly_detected: boolean,
      decision_state: string | null,            // "INFORMATIVA" | "AUTOMATICA" | "PENDIENTE_APROBACION" | "BLOQUEADA" | null
      caller: string,                           // "user" | "system"
      support_offered: boolean,                 // si la evaluación ofreció soporte (acción posible, FR-060)
      compensation_eligible: boolean,           // FR-067; base de la validación de COMPENSATION_REQUESTED con decision_id
      policy_version: string | null,
      mct_provided: boolean,                    // proyección mínima para el caso humano con decision_id (sin releer nada)
      passenger_count: integer,                 // ídem; 0 si trip_context INVALID
      segments: [ {segment_id: string, state: string | null, delay_minutes: integer | null} ],   // estado por segmento (sin PII)
      message_hash: string,                     // SHA-256 (hex) de los mensajes devueltos
      messages_blocked: integer,                // mensajes que el validador (FR-081) bloqueó y reemplazó por el texto neutro; base de la métrica «0 afirmaciones sin evidencia» (NFR-008)
      reads: [ {tool: string, retrieved_at: string | null, outcome: string} ],
                                                // tool: "get_trip_context" | "get_operational_events" | "get_policy_rules" | "get_eligible_options"
                                                // outcome: "OK" | "FAILED" | "INVALID" (integridad, FR-066) | "NOT_REQUESTED"
      events: [ {event_id: string, segment_id: string, event_type: string, disposition: string, reason: string | null} ],
                                                // disposition: "CHOSEN" | "DISCARDED" | "NOT_INTERPRETED"
                                                // reason: "SOURCE_DEGRADED" | "INCONSISTENT_DELAY" | "UNKNOWN_SEGMENT" | "FUTURE_TIMESTAMP" | "SUPERSEDED" | "SOURCE_CONFLICT" | "UNSUPPORTED_EVENT_TYPE" | null
      rules: [ {rule_id: string, result: string, requires_human_approval: boolean} ],
      variables: [ {segment_id: string | null, name: string, value_boolean: boolean | null, value_integer: integer | null,
                    value_timestamp: string | null, origin: string, assumptions: [string]} ],
      options: [ {option_id: string, itinerary_key: string | null, fingerprint: string | null, type: string, flight_number: string | null, origin: string | null,
                  destination: string | null, date: string | null, departure: string | null, fare_difference: integer | null, currency: string | null,
                  seats_available: integer | null, policy_ref: string, confidence: string, viable: boolean, discard_reasons: [string], is_proposed: boolean} ],
                                                // Campos por tipo: una opción REFUND (p. ej. O3) NO trae vuelo, costo ni cupos ⇒ esos campos y itinerary_key/fingerprint van null; se conserva con sus descartes (auditoría).
                                                // discard_reasons: TODAS las razones (FR-042); [] si es viable. Valores: "INSUFFICIENT_SEATS" | "FEE_CONFLICT" | "NO_ENTITLEMENT" | "POLICY_REF_UNVERIFIED" | "POLICY_REF_SUPERSEDED" | "UNSUPPORTED_TYPE" | "EXPIRED" | "MISSING_CURRENCY" | "ITINERARY_MISMATCH" (FR-041 f)
      actions: [ {kind: string, option_id: string | null, effect: string} ],
      human_case_reasons: [string],
      outcomes: [ {kind: string, reference_id: string | null, generation: integer | null, state: string, at: string} ]
                                                // kind: "REBOOKING" | "HUMAN_CASE"; reference_id: request_id o case_id (null si aún no existe);
                                                // generation: solo en REBOOKING; state: "EN_CURSO" | "INDETERMINADA" | "CREADA" | "FALLIDA" | "EXPIRADA" (operación) o "EN_CURSO" | "CREADO" | "FALLIDO" | "INDETERMINADO" (caso)
    }
  401 Unauthorized:  {"error": "UNAUTHENTICATED", "detail": "Falta la cabecera X-Session-Booking."}
  404 Not Found:     {"error": "NOT_FOUND", "detail": "No encontramos el recurso solicitado."}   // decision_id inexistente o ajeno: respuesta idéntica, no 403 (FR-001)
  422 Unprocessable: {"error": "VALIDATION_ERROR", "detail": "El decision_id debe ser un UUID válido."}
  429 Too Many Requests:   {"error": "RATE_LIMITED", "detail": "Demasiadas solicitudes. Intenta de nuevo en un minuto."}   // más de EVALUATE_RATE_LIMIT_PER_MINUTE solicitudes por minuto por reserva y por origen (NFR-013)
  500 Internal Server Error: {"error": "INTERNAL_ERROR", "detail": "Ocurrió un error inesperado."}

SLA: p95 < 200 ms (lectura local de SQLite) | Timeout cliente recomendado: 3000 ms
```

```
⚠️ SAGRADO (solo desarrollo): GET /api/dev/scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH: Ninguna; disponible solo si DEV_ENDPOINTS_ENABLED=true (apagado por defecto; el script de desarrollo lo enciende junto con DEV_SESSION_HEADER_ENABLED)
HEADERS REQUERIDOS: ninguno

QUERY PARAMS: ninguno

REQUEST BODY: ninguno

RESPUESTAS:
  200 OK
    {
      active_scenario_id: string,           // escenario activo en los mocks
      clock: { mode: string, now: string, offset_seconds: integer },   // mode: "scenario" | "system"; now: ISO UTC del reloj vigente
      scenarios: [
        {
          scenario_id: string,              // ver catálogo
          booking_id: string,               // valor que el front fija en X-Session-Booking
          title: string,                    // título corto en español
          description: string,              // qué reproduce (TC-xx)
          ui: boolean,                      // true ⇒ aparece en el ScenarioSelector del front; false ⇒ variante de fixture solo para pruebas automatizadas (también activable por PUT)
          tests: [string]                   // casos TC-xx relacionados
        }
      ]
    }
  404 Not Found: {"error": "DEV_ENDPOINTS_DISABLED", "detail": "Los endpoints de desarrollo están desactivados."}

SLA: p99 < 50 ms | Timeout cliente recomendado: 2000 ms
```

```
⚠️ SAGRADO (solo desarrollo): PUT /api/dev/scenario
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH: Ninguna; disponible solo si DEV_ENDPOINTS_ENABLED=true
HEADERS REQUERIDOS:
  Content-Type: application/json

QUERY PARAMS: ninguno

REQUEST BODY:
  {
    "scenario_id": string        // uno de los scenario_id devueltos por GET /api/dev/scenarios
  }

SEMÁNTICA: cambia, en memoria y para todo el proceso, el conjunto de datos que sirven los mocks de las 7 tools y reinicia el ScenarioClock
           (now = _meta.retrieved_at de get_trip_context del escenario, offset 0).
           No toca la base SQLite (los registros de decisión y operaciones ya creados se conservan).
           Con un único proceso y un único escenario activo, no es apto para uso concurrente de varias personas.

RESPUESTAS:
  200 OK
    {
      active_scenario_id: string,
      booking_id: string,
      title: string,
      clock_now: string                     // ISO UTC: instante base del escenario
    }
  404 Not Found:     {"error": "SCENARIO_NOT_FOUND", "detail": "El escenario no existe."}
  404 Not Found:     {"error": "DEV_ENDPOINTS_DISABLED", "detail": "Los endpoints de desarrollo están desactivados."}
  422 Unprocessable: {"error": "VALIDATION_ERROR", "detail": "El cuerpo debe incluir scenario_id."}

SLA: p99 < 50 ms | Timeout cliente recomendado: 2000 ms
```

```
⚠️ SAGRADO (solo desarrollo): PUT /api/dev/clock
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH: Ninguna; disponible solo si DEV_ENDPOINTS_ENABLED=true Y CLOCK_MODE=scenario
HEADERS REQUERIDOS:
  Content-Type: application/json

QUERY PARAMS: ninguno

REQUEST BODY:
  {
    "advance_seconds": integer     // ≥ 0 y ≤ 86400: segundos que se suman al offset del ScenarioClock
  }

SEMÁNTICA: el reloj de escenario es now = retrieved_at del escenario activo + offset; el offset solo cambia con este endpoint (los mocks NO caducan solos).
           Sirve para demostrar el TTL de 120 s, la hora límite y las expiraciones de operaciones sin esperar. En producción rige SystemClock y este endpoint no existe.

RESPUESTAS:
  200 OK
    {
      now: string,                         // ISO UTC del reloj tras avanzar
      offset_seconds: integer
    }
  404 Not Found:     {"error": "DEV_ENDPOINTS_DISABLED", "detail": "Los endpoints de desarrollo están desactivados."}
  422 Unprocessable: {"error": "VALIDATION_ERROR", "detail": "advance_seconds debe ser un entero entre 0 y 86400."}

SLA: p99 < 50 ms | Timeout cliente recomendado: 2000 ms
```

**Catálogo cerrado de escenarios v1** (FR-101: los 7 ejemplos del PDF —con los datos personales sustituidos por valores claramente ficticios— más las variantes TC; se amplía agregando entradas, sin cambiar el contrato del endpoint). **Reloj de los escenarios:** en desarrollo y demostración (`CLOCK_MODE=scenario`) rige un `ScenarioClock` con `now = retrieved_at del escenario + offset`; el offset solo avanza con `PUT /api/dev/clock` y se reinicia al cambiar de escenario, de modo que **los mocks no caducan solos**. En producción rige `SystemClock`. Las pruebas automatizadas usan `FixedClock`. **Modos de llamada:** todos los escenarios sirven a ambos modos de `POST …/evaluate`; los TC-42…TC-44 y TC-50 los ejercitan con `caller = "system"` y el resto con `caller = "user"`. Convenciones: el `booking_id` es `ABC123` salvo indicación; **`BASE_TC01` contiene el cambio de puerta `E-1007` del PDF; las variantes derivadas de él no lo incluyen salvo indicación** (así cada escenario prueba una sola cosa); «seq» = el mock devuelve una respuesta distinta por llamada (1.ª lectura vs. re-consulta); «BD» = además requiere una fila preparada en SQLite por el fixture de pruebas; «espía» = el mock registra si se invocó una tool y la prueba falla si se invoca. Salvo indicación, el mock de `notify_passenger` responde `202 QUEUED` y el de `create_human_case`, `201`. `ui = sí` ⇒ aparece en el `ScenarioSelector`; `ui = no` ⇒ variante de fixture para pruebas automatizadas (también activable por `PUT`).

| `scenario_id` | `booking_id` | ui | Qué reproduce | TC |
|---|---|---|---|---|
| `BASE_TC01` | `ABC123` | sí | Caso base del PDF: retraso 160 min y cambio de puerta (`E-1007`, puerta 24) en S1, `E-1012` degradado, R1/R2/R4 no se cumplen, R3 y R5 sí ⇒ **política rota** (R3 concede `REBOOK_NO_FEE`); O1 viable, O2 (1 cupo, 180.000 CLP) y O3 (`POL-REFUND-2026-01` no recuperada) no viables; decisión PENDIENTE_APROBACION; la compensación es elegible (R4 concede `CASH_COMPENSATION`); sirve también para pedido de datos personales, pernocte y, con `caller = "system"`, para la notificación | TC-01, TC-11, TC-12, TC-17, TC-20, TC-28, TC-42, TC-46, TC-50 |
| `SIN_ANOMALIA` | `ABC123` | sí | `STATUS: SCHEDULED` de `OPS_CORE` en S1 y S2, sin retraso ⇒ solo contexto (segmentos `SCHEDULED`), sin botón | FR-004 |
| `SOLO_DEGRADADO_TC02` | `ABC123` | sí | Solo `E-1012` (`LEGACY_MIRROR` degradada) en S1 ⇒ `NO_VERIFIED_INFO` («sin información verificada», **solo** por evidencia degradada), sin alerta ni botón | TC-02 |
| `DEGRADADA_OPS_CORE_TC19` | `ABC123` | no | `sources_degraded = ["OPS_CORE","LEGACY_MIRROR"]`: S1 sin fuente sana ⇒ sin botón | TC-19 |
| `CONFLICTO_TC03` | `ABC123` | sí | Escenario sintético: dos eventos de fuentes **no degradadas** en S1 con el **mismo `recorded_at`** (empate) y afirmaciones incompatibles (`STATUS: ON_TIME` de `OPS_CORE` y `DELAY` de `AIRPORT_FEED`) ⇒ BLOQUEADA; política y opciones `NOT_REQUESTED`, sin reglas en pantalla; con `caller = "system"` no se notifica (sin política rota y sin puerta) y queda `needs_manual_review` | TC-03, TC-43 |
| `RETRASO_179_TC04` | `ABC123` | no | `DELAY` de 179 min (borde de R1) | TC-04 |
| `RETRASO_180_TC04` | `ABC123` | no | `DELAY` de 180 min (borde de R1) | TC-04 |
| `RETRASO_239_TC05` | `ABC123` | no | `DELAY` de 239 min (borde de R2) | TC-05 |
| `RETRASO_240_TC05` | `ABC123` | no | `DELAY` de 240 min (borde de R2) | TC-05 |
| `MCT_INCIERTO_TC06A` | `ABC123` | sí | `DELAY` de 60 min (margen 10 min, MCT no provisto) ⇒ `missed_connection` desconocido; R3 «no evaluable» con derecho de remedio ⇒ BLOQUEADA | TC-06 |
| `CONEXION_FALSA_TC06B` | `ABC123` | no | `DELAY` de 10 min (margen 60 min) ⇒ conexión «falsa, ESTIMADA, sujeta a MCT»; ninguna regla de remedio se cumple (R5 concede `PRIORITY_HANDLING`, que no es remedio) ⇒ INFORMATIVA | TC-06 |
| `NOTIFY_BLOQUEADA_POLITICA_ROTA_TC43` | `ABC123` | no | Como `PASAJERO_INFANT_TC23` con `caller = "system"`: `DELAY` de 160 min (R3 cumplida ⇒ política rota) y menor desconocido (R5 «no evaluable») ⇒ decisión BLOQUEADA, pero **sí se notifica** (`NT-9912`); además `needs_manual_review = true` | TC-43 |
| `INFORMATIVA_TC45` | `ABC123` | sí | `DELAY` de 5 min (margen 65 min): se informa el retraso y se muestran las reglas evaluadas; decisión INFORMATIVA; espía: `get_eligible_options` NO debe invocarse; sin opciones, sin botón de soporte, sin notificación en modo `system` | TC-45, TC-43 |
| `SIN_MENOR_TC07` | `ABC123` | sí | Dos pasajeros `ADULT`: R5 falsa ⇒ AUTOMATICA; `create_rebooking_request` responde `201 PENDING_CONFIRMATION` | TC-07, TC-30, TC-34 |
| `OPCIONES_VENCIDAS_TC08` | `ABC123` | no | seq: la 1.ª lectura de opciones llega ya vencida; la re-consulta trae opciones vigentes | TC-08 |
| `SIN_OPCION_TC09` | `ABC123` | sí | Dos pasajeros `ADULT` (R5 falsa ⇒ AUTOMATICA) y solo O2 (1 cupo, 180.000 CLP) ⇒ sin opción viable; el motivo principal es `NO_OPTION_COVERS_GROUP` | TC-09 |
| `POLITICA_SUPERSEDED_TC10` | `ABC123` | no | `policy_ref` de las opciones en `superseded_versions` | TC-10 |
| `PARCIAL_BLOQUEANTE_TC12` | `ABC123` | no | `completeness = PARTIAL` con un campo necesario ausente (`segments[1].scheduled_departure`) ⇒ lectura fallida: aviso y reintento, sin soporte | TC-12, FR-086 |
| `CANCELACION_TC13` | `ABC123` | sí | Evento `CANCELLATION` (tipo no soportado) ⇒ BLOQUEADA; política y opciones `NOT_REQUESTED` | TC-13 |
| `REBOOKING_503_TC14` | `ABC123` | sí | Como `SIN_MENOR_TC07`, pero `create_rebooking_request` responde `503 UPSTREAM_TIMEOUT` siempre | TC-14 |
| `REBOOKING_409_TC15` | `ABC123` | no | Como `SIN_MENOR_TC07`, pero `create_rebooking_request` responde `409 DUPLICATE_REQUEST` con `RBK-88231` | TC-15 |
| `NOTIFY_422_TC16` | `ABC123` | no | Como `BASE_TC01`; `notify_passenger` responde `422 UNVALIDATED_CONTENT` («falta policy_ref») ante un mensaje sin `policy_ref`; se ejercita por el puerto | TC-16 |
| `CRUCE_MEDIANOCHE_TC18` | `ABC123` | no | S1 llega 23:30 con `DELAY` de 120 min ⇒ `new_arrival` 01:30 del día siguiente | TC-18 |
| `OTRA_RESERVA_TC21` | `XYZ789` | no | Segunda reserva; con `ABC123` permite verificar la respuesta `404` idéntica entre sesiones y ante un recurso inexistente | TC-21 |
| `REBOOKING_LENTO_TC22` | `ABC123` | no | Como `SIN_MENOR_TC07`, con latencia de 300 ms en `create_rebooking_request` (mantiene la operación `EN_CURSO`) | TC-22 |
| `MULTI_SEGMENTO_TC23` | `ABC123` | no | `DELAY` relevante en S1 y en S2 ⇒ `MULTIPLE_AFFECTED_SEGMENTS` | TC-23 |
| `PASAJERO_INFANT_TC23` | `ABC123` | no | Un pasajero de tipo `INFANT` con `DELAY` de 160 min ⇒ `group_includes_minor` desconocido; con política rota (R3) R5 «no evaluable» ⇒ BLOQUEADA (validación manual) | TC-23, TC-47 |
| `SCHEDULED_POSTERIOR_TC24` | `ABC123` | no | `DELAY` 10:48 y un `STATUS: SCHEDULED` **más reciente y sano** (11:00) en S1 ⇒ el retraso se borra: S1 queda `SCHEDULED`, solo contexto | TC-24 |
| `ON_TIME_POSTERIOR_TC24` | `ABC123` | no | `DELAY` 10:48 y un `STATUS: ON_TIME` **más reciente y sano** (11:00) en S1 ⇒ el retraso se borra: S1 queda `ON_TIME`, solo contexto | TC-24 |
| `SCHEDULED_ANTERIOR_TC24` | `ABC123` | no | `STATUS: SCHEDULED` **más antiguo** (10:00) que el `DELAY` de 10:48 ⇒ el retraso se mantiene | TC-24 |
| `ON_TIME_ANTERIOR_TC24` | `ABC123` | no | `STATUS: ON_TIME` **más antiguo** (10:00) que el `DELAY` de 10:48 ⇒ el retraso se mantiene (sin conflicto) | TC-24 |
| `SCHEDULED_DEGRADADO_TC24` | `ABC123` | no | `STATUS: SCHEDULED` posterior pero de una fuente **degradada** ⇒ no borra el `DELAY` | TC-24 |
| `ON_TIME_DEGRADADO_TC24` | `ABC123` | no | `STATUS: ON_TIME` posterior pero de una fuente **degradada** ⇒ no borra el `DELAY` | TC-24 |
| `DOS_DELAY_TC25` | `ABC123` | no | Dos `DELAY` en S1 (100 min y luego 160 min) ⇒ gana el más reciente | TC-25 |
| `EVENTOS_INVALIDOS_TC26` | `ABC123` | no | Un `DELAY` incoherente, un evento de `S9` (segmento no pedido) y un evento con `recorded_at` futuro | TC-26 |
| `TTL_TC27` | `ABC123` | no | `ttl_seconds = 120` con `retrieved_at` conocido (la prueba mueve el reloj a +119 s y +120 s con `FixedClock`; en demostración, con `PUT /api/dev/clock`) | TC-27 |
| `TTL_AUSENTE_TC27` | `ABC123` | no | Opciones sin `ttl_seconds` ⇒ conjunto vencido | TC-27 |
| `SIN_PERNOCTE_TC28` | `ABC123` | no | O1 con salida el mismo día de la nueva llegada ⇒ `overnight_required` no se deriva | TC-28 |
| `SIN_MONEDA_TC29` | `ABC123` | no | Opción con `fare_difference > 0` sin `currency` | TC-29 |
| `CUPOS_AGOTADOS_TC31` | `ABC123` | no | seq: la 1.ª lectura de O1 trae 4 cupos; la re-consulta, 1 ⇒ huella distinta | TC-31 |
| `ITINERARIO_SUSTITUIDO_TC31` | `ABC123` | no | seq: la re-consulta trae otro vuelo con el mismo `option_id` ⇒ huella distinta; una variante cambia solo `retrieved_at` ⇒ huella igual | TC-31 |
| `REGISTROS_ANTIGUOS_TC32` | `ABC123` | no | BD: decisiones, operaciones (en estado final), casos y notificaciones de 29, 30 y 31 días de antigüedad (`FixedClock`); las operaciones vigentes se prueban en `PURGA_OPERACIONES_VIGENTES_TC56` | TC-32 |
| `ERROR_CONTEXTO` | `ABC123` | sí | `get_trip_context` responde `503` ⇒ `502`: «no pudimos cargar tu viaje» con reintento, sin soporte | TC-33 |
| `ERROR_EVENTOS` | `ABC123` | sí | `get_operational_events` responde `503` ⇒ contexto sin estado, con aviso y sin soporte (decisión nula) | TC-33 |
| `ERROR_POLITICA_TC33` | `ABC123` | no | `get_policy_rules` responde `503` ⇒ decisión BLOQUEADA con anomalía que exige validación manual: sin opciones, `needs_manual_review`, soporte **ofrecido**; `POST human-cases` NO devuelve `422 SUPPORT_NOT_AVAILABLE` | TC-33 |
| `ERROR_OPCIONES_TC33` | `ABC123` | no | `get_eligible_options` responde `503` ⇒ BLOQUEADA, sin opciones, soporte **ofrecido** (`BLOCKING_PARTIAL_DATA`) | TC-33 |
| `LECTURA_422_POLITICA_TC33` | `ABC123` | no | `get_policy_rules` responde `422` ⇒ igual que `ERROR_POLITICA_TC33` (BLOQUEADA con soporte) | TC-33 |
| `LECTURA_422_EVENTOS_TC33` | `ABC123` | no | `get_operational_events` responde `422` ⇒ igual que `ERROR_EVENTOS` (sin soporte) | TC-33 |
| `TIMEOUT_EVENTOS_TC33` | `ABC123` | no | `get_operational_events` no responde antes del timeout ⇒ una re-consulta y luego contexto sin estado, sin soporte | TC-33 |
| `TIMEOUT_OPCIONES_TC33` | `ABC123` | no | `get_eligible_options` no responde antes del timeout ⇒ BLOQUEADA con soporte | TC-33 |
| `TIMEOUT_REBOOKING_TC33` | `ABC123` | no | Como `SIN_MENOR_TC07`, pero `create_rebooking_request` no responde antes del timeout ⇒ `INDETERMINADA`, reintentos con la misma llave y caso humano | TC-33, TC-14 |
| `HUMANCASE_ERROR_TC33` | `ABC123` | no | `create_human_case` responde con un error explícito `5xx` | TC-33 |
| `HUMANCASE_TIMEOUT_TC33` | `ABC123` | no | `create_human_case` no responde antes del timeout ⇒ INDETERMINADO | TC-33 |
| `POLITICA_NUEVA_VERSION_TC34` | `ABC123` | no | seq: la re-consulta trae `POL-DELAY-2026-04` y las opciones con ese `policy_ref` | TC-34 |
| `ULTIMO_SEGMENTO_TC35` | `ABC123` | no | `DELAY` de 200 min solo en S2 (último segmento): R1 se cumple (política rota) y no hay conexión ⇒ las opciones reemplazan al segmento afectado | TC-35 |
| `POLITICA_VACIA_TC35` | `ABC123` | no | `get_policy_rules("DELAY")` devuelve `rules: []` ⇒ BLOQUEADA (para `DELAY` la política vacía sí bloquea) | TC-35, TC-53 |
| `DEGRADADO_POSTERIOR_TC36` | `ABC123` | no | `E-1012` (degradado, `ON_TIME`) con `recorded_at` posterior al de `E-1001` | TC-36 |
| `OPCION_INCOHERENTE_TC37` | `ABC123` | no | Tres opciones: destino distinto, origen distinto y salida anterior a `new_arrival` + MCT | TC-37 |
| `OPERACION_COLGADA_TC38` | `ABC123` | no | BD: operación `EN_CURSO` con más de `OPERATION_STALE_SECONDS` ⇒ pasa a `INDETERMINADA` | TC-38 |
| `CREADA_VENCIDA_TC38` | `ABC123` | no | BD: operación `CREADA` con `expires_at` pasado ⇒ `EXPIRADA`; permite la generación siguiente | TC-38 |
| `LLAVE_NO_PERSISTIBLE_TC38` | `ABC123` | no | Repositorio que falla al insertar la llave ⇒ no se llama a la tool | TC-38 |
| `INTEGRIDAD_CADENA_ROTA_TC39` | `ABC123` | no | `destino[0] != origen[1]` ⇒ BLOQUEADA, conexión desconocida | TC-39 |
| `INTEGRIDAD_DELAY_NO_POSITIVO_TC39` | `ABC123` | no | `DELAY` con `delay_minutes` ≤ 0 ⇒ `INCONSISTENT_DELAY` | TC-39 |
| `INTEGRIDAD_DESORDENADOS_TC39` | `ABC123` | no | Segmentos en orden inverso ⇒ se reordenan, sin bloqueo | TC-39 |
| `INTEGRIDAD_MENOR_SIN_ADULTO_TC39` | `ABC123` | no | Solo un pasajero `CHILD` ⇒ BLOQUEADA, `BLOCKING_PARTIAL_DATA` | TC-39 |
| `REBOOKING_ESTRICTO_TC40` | `ABC123` | no | Como `SIN_MENOR_TC07`; el mock verifica `booking_id` y que `passenger_ids` cubra todo el grupo (si no, `422 PASSENGERS_NOT_COVERED`) | TC-40 |
| `POLITICA_CONDICIONES_TC41` | `ABC123` | no | Política con condiciones `EQ`/`==` y `NE`/`!=` (equivalentes entre sí), precedencia `AND`/`OR`, tipos mezclados, 201 caracteres y 11 niveles de anidación | TC-41 |
| `NOTIFY_OK_TC42` | `ABC123` | no | Como `BASE_TC01` **sin el evento de puerta** y con `caller = "system"`: política rota ⇒ **una** llamada a `notify_passenger` (`kind = POLICY`, `reason = DELAY`, `202 QUEUED`, `NT-9912`) con la plantilla fija, sin URL, con `policy_ref` y `booking_id` | TC-42 |
| `GATE_SOLO_TC51` | `ABC123` | sí | Solo `GATE_CHANGE` (`E-1007`, puerta 24, `AIRPORT_FEED`, 10:55 UTC) en S1, sin retraso: la vista muestra el cambio de puerta **destacado con su hora**; **S1 y S2 quedan `NO_EVENTS`** («Horario programado»: S1 solo tiene un evento que no informa la salida y S2 no tiene eventos); espía: `get_policy_rules` **NO** se invoca; decisión INFORMATIVA sin opciones ni soporte; con `caller = "system"` se envía **una** notificación `kind = INFORMATIONAL`, `reason = GATE_CHANGE`, **sin `policy_ref`** (el mock la acepta, H-21) | TC-51 |
| `DELAY_Y_PUERTA_TC52` | `ABC123` | no | `DELAY` de 160 min en S1 y `GATE_CHANGE` en S2: contexto completo (ambos visibles); espía: **una** sola llamada a `get_policy_rules("DELAY")`; con `caller = "system"` se envían **dos** notificaciones, una por motivo (`DELAY` con `policy_ref` y `GATE_CHANGE` sin él), con **identificadores distintos** (`NT-9912` y `NT-9913`). `BASE_TC01` (retraso y puerta en S1) también lo ejercita | TC-52 |
| `GATE_POLITICA_CONFIG_TC53` | `ABC123` | no | Como `GATE_SOLO_TC51`, con una configuración que **incluye `GATE_CHANGE` en `POLICY_SCENARIOS`**: aun así no se consulta política (espía: 0 llamadas) y la decisión sigue INFORMATIVA | TC-53 |
| `SIN_EVENTOS_TC54` | `ABC123` | no | S1 y S2 **sin ningún evento** (`events: []`) ⇒ solo contexto: ambos segmentos `NO_EVENTS` («Horario programado»), sin «sin información verificada», sin alertas, sin reglas ni botones de acción | TC-54 |
| `NOTIFY_COOLDOWN_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`, con dos llamadas `system` iguales dentro de `NOTIFY_COOLDOWN_SECONDS` (reloj de escenario) ⇒ una sola notificación; la 2.ª responde `deduplicated = true` | TC-44 |
| `NOTIFY_REINTENTO_TRAS_FALLIDA_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`: la 1.ª llamada `system` termina `FALLIDA` (`422`); la 2.ª, con la misma huella, hace una **nueva reserva** inmediata (intento 2) y queda `QUEUED` | TC-44 |
| `NOTIFY_ENFRIAMIENTO_VENCIDO_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`: una notificación `QUEUED`; el reloj de escenario avanza más de `NOTIFY_COOLDOWN_SECONDS`; la siguiente llamada marca el intento previo `VENCIDA` y hace una **nueva reserva** (intento 2) | TC-44 |
| `NOTIFY_CONCURRENTE_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`, con dos llamadas `system` simultáneas: solo una inserta la reserva `EN_CURSO` y se envía **una** notificación; la otra devuelve `deduplicated = true` | TC-44 |
| `NOTIFY_EN_CURSO_COLGADO_TC44` | `ABC123` | no | BD: intento `EN_CURSO` con más de `OPERATION_STALE_SECONDS` ⇒ pasa a `INDETERMINADA` y bloquea hasta vencer el enfriamiento | TC-44, TC-38 |
| `NOTIFY_PRIMER_ENVIO_PENDIENTE_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`, con latencia de 300 ms en `notify_passenger`: dos llamadas `system` simultáneas ⇒ la 2.ª responde `deduplicated = true` con `status = EN_CURSO` (el primer envío sigue pendiente) y se envía **una** notificación | TC-44 |
| `NOTIFY_RESPUESTA_FUERA_DE_ORDEN_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`: el intento 1 queda `INDETERMINADA` y luego `VENCIDA`, se reserva el intento 2 y la respuesta `202` tardía del intento 1 llega después: `mark(clave, 1, …)` no modifica el intento 2 ni sobrescribe `VENCIDA` (0 filas afectadas) | TC-44 |
| `NOTIFY_PUERTA_CAMBIA_TC55` | `ABC123` | no | Como `GATE_SOLO_TC51` con `caller = "system"`: 1.ª llamada con la puerta 24 ⇒ aviso `GATE_CHANGE` `QUEUED`; 2.ª llamada con un `GATE_CHANGE` posterior a la puerta 25 ⇒ la huella del motivo cambia ⇒ aviso **nuevo** | TC-55 |
| `NOTIFY_PUERTA_IGUAL_TC55` | `ABC123` | no | Como `GATE_SOLO_TC51` con `caller = "system"`: dos llamadas con la misma puerta 24 dentro del enfriamiento ⇒ una sola notificación (`deduplicated = true`) | TC-55 |
| `NOTIFY_422_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`, pero el proveedor responde `422` ⇒ estado `FALLIDA`, sin reintento | TC-44 |
| `NOTIFY_TIMEOUT_TC44` | `ABC123` | no | Como `NOTIFY_OK_TC42`, pero `notify_passenger` no responde ⇒ `NOTIFY_MAX_RETRIES` reintentos con la misma clave y estado `INDETERMINADA`, sin afirmar éxito | TC-44 |
| `SIN_COMPENSACION_TC46` | `ABC123` | no | Como `BASE_TC01`, pero la política no trae regla con derecho de `COMPENSATION_RIGHTS` ⇒ el menú de soporte no ofrece `COMPENSATION_REQUESTED`; `POST human-cases` con ese motivo ⇒ `422` | TC-46 |
| `PASAJERO_INFANT_INFORMATIVA_TC47` | `ABC123` | no | Un pasajero `INFANT` con `DELAY` de 5 min: R5 «no evaluable» sin derechos de remedio y sin política rota se ignora ⇒ INFORMATIVA (solo se informa) | TC-47 |
| `PASAJERO_INFANT_SIN_R5_TC47` | `ABC123` | no | Un pasajero `INFANT` con `DELAY` de 160 min y una política **sin regla R5** (solo R1…R4): hay política rota (R3) y composición de grupo desconocida ⇒ BLOQUEADA por validación manual (`BLOCKING_PARTIAL_DATA`), independiente de R5 | TC-23, TC-47 |
| `PURGA_OPERACIONES_VIGENTES_TC56` | `ABC123` | no | BD con `FixedClock` 2026-10-19T00:00:00Z y `AUDIT_RETENTION_DAYS` = 30 (corte 2026-09-19): **3 operaciones jóvenes** (`EN_CURSO` de 10 s, `INDETERMINADA` de 300 s, `CREADA` con vencimiento a +10 min) y **3 vencidas** (`EN_CURSO` de 40 días, `INDETERMINADA` de 40 días, `CREADA` con vencimiento hace 40 días), más una `FALLIDA`, una `EXPIRADA` y una decisión de 31 días ⇒ la purga **primero aplica los vencimientos** (las 3 vencidas pasan a `EXPIRADA`) y luego borra por antigüedad: elimina las vencidas, las finales y la decisión, conserva las 3 jóvenes; una `CREADA` de 31 días con vencimiento aún futuro (reloj anómalo) se **conserva minimizada** y su bloqueo (`uq_operations_active`) sigue impidiendo una operación nueva | TC-56, TC-32 |
| `INDETERMINADA_VENCE_TC57` | `ABC123` | no | BD con `FixedClock`: operación `INDETERMINADA`; antes de `OPERATION_INDETERMINATE_EXPIRY_SECONDS` sigue bloqueando una operación nueva; pasado ese plazo (reloj de escenario) pasa a `EXPIRADA` y permite la generación siguiente | TC-57, TC-38 |
| `LIMITE_TASA_TEXTO_PLANO_TC58` | `ABC123` | no | `POST …/evaluate` más de `EVALUATE_RATE_LIMIT_PER_MINUTE` veces en un minuto con la misma sesión ⇒ `429`; el proveedor de política devuelve `condition` y `entitlement` con marcado HTML y una puerta con HTML ⇒ el front los muestra como texto plano; el test de código verifica consultas parametrizadas | TC-58 |
| `DECISION_SESION_SIN_INTERNOS_TC59` | `ABC123` | no | Como `NOTIFY_BLOQUEADA_POLITICA_ROTA_TC43` evaluada con `caller = "system"` y luego `GET /api/v1/decisions/{id}` con la sesión de `ABC123` ⇒ la respuesta no contiene `needs_manual_review` ni `notifications`; el registro interno sí conserva ambos | TC-59 |
| `AVISO_TITULAR_ADULTO_TC60` | `ABC123` | no | Como `NOTIFY_OK_TC42` con el niño P2 listado antes que el adulto P1 ⇒ `recipient_passenger_id = P1` (titular adulto), nunca el menor; sin ningún adulto ⇒ `NOT_SENT` (`NO_ADULT_RECIPIENT`) | TC-60 |
| `NOTIFY_DELAY_SOLO_MINUTOS_TC60` | `ABC123` | no | Como `NOTIFY_OK_TC42`: 1.ª llamada `system` con `DELAY` de 160 min y 2.ª con 170 min, mismas reglas cumplidas y misma versión de política ⇒ la huella del motivo no cambia ⇒ un solo aviso (`deduplicated = true`) | TC-60 |
| `OPCIONES_CONEXION_DESCONOCIDA_TC60` | `ABC123` | no | Como `MCT_INCIERTO_TC06A` con la política y las opciones del caso base: `missed_connection` desconocido ⇒ ninguna opción viable (`ITINERARY_MISMATCH`), decisión BLOQUEADA y soporte ofrecido | TC-60, TC-06 |
| `PASAJERO_SIN_TIPO_TC47` | `ABC123` | no | Un pasajero sin campo `type` con `DELAY` de 160 min ⇒ menor desconocido; con política rota ⇒ BLOQUEADA (validación manual) | TC-47 |
| `NOTIFY_CONTENIDO_PROHIBIDO_TC48` | `ABC123` | no | Mensajes de notificación con URL, enlace, dominio, teléfono o correo ⇒ el validador los bloquea antes de llamar; se ejercita por el puerto | TC-48 |
| `CONFIG_PARAMETROS_TC49` | `ABC123` | no | Conjunto de archivos y variables de configuración: valores por defecto, un valor cambiado **por nombre para cada parámetro de §2.4** (incluidos los operativos `DEV_SESSION_HEADER_ENABLED`, `DEV_ENDPOINTS_ENABLED`, `CLOCK_MODE`, `CORS_ALLOWED_ORIGINS`, `DB_PATH`, `UPSTREAM_READ_TIMEOUT_MS`, `UPSTREAM_WRITE_TIMEOUT_MS`, `READ_MAX_REQUERIES`, `WRITE_RETRY_BACKOFF_MS` y `ASSERTION_COMPATIBILITY`) y valores inválidos (el arranque falla) | TC-49 |
| `SYSTEM_CLAVE_SERVICIO_TC50` | `ABC123` | no | Como `BASE_TC01` con `SERVICE_API_KEY` configurada: sin `X-Service-Key`, con clave incorrecta y con `SERVICE_API_KEY` ausente ⇒ `401`; con clave válida ⇒ `SystemEvaluationResult` sin PII ni vista completa, sin `create_rebooking_request` ni `create_human_case` | TC-50 |

**Índice TC → escenarios** (verificación de cobertura: cada TC de `REQUERIMIENTOS_V1.md` §6, TC-01…TC-60, tiene al menos un escenario o variante de fixture; TC-51…TC-60 en el índice complementario):

| TC | Escenario(s) | TC | Escenario(s) |
|---|---|---|---|
| TC-01 | `BASE_TC01` | TC-26 | `EVENTOS_INVALIDOS_TC26` |
| TC-02 | `SOLO_DEGRADADO_TC02` | TC-27 | `TTL_TC27`, `TTL_AUSENTE_TC27` |
| TC-03 | `CONFLICTO_TC03` (sintético: empate de `recorded_at`) | TC-28 | `BASE_TC01`, `SIN_PERNOCTE_TC28` |
| TC-04 | `RETRASO_179_TC04`, `RETRASO_180_TC04` | TC-29 | `SIN_MONEDA_TC29` |
| TC-05 | `RETRASO_239_TC05`, `RETRASO_240_TC05` | TC-30 | `SIN_MENOR_TC07` |
| TC-06 | `MCT_INCIERTO_TC06A`, `CONEXION_FALSA_TC06B` | TC-31 | `CUPOS_AGOTADOS_TC31`, `ITINERARIO_SUSTITUIDO_TC31` |
| TC-07 | `SIN_MENOR_TC07` | TC-32 | `REGISTROS_ANTIGUOS_TC32` |
| TC-08 | `OPCIONES_VENCIDAS_TC08` | TC-33 | `ERROR_CONTEXTO`, `ERROR_EVENTOS`, `ERROR_POLITICA_TC33`, `ERROR_OPCIONES_TC33`, `LECTURA_422_POLITICA_TC33`, `LECTURA_422_EVENTOS_TC33`, `TIMEOUT_EVENTOS_TC33`, `TIMEOUT_OPCIONES_TC33`, `TIMEOUT_REBOOKING_TC33`, `HUMANCASE_ERROR_TC33`, `HUMANCASE_TIMEOUT_TC33` |
| TC-09 | `SIN_OPCION_TC09` | TC-34 | `SIN_MENOR_TC07`, `POLITICA_NUEVA_VERSION_TC34` |
| TC-10 | `POLITICA_SUPERSEDED_TC10` | TC-35 | `ULTIMO_SEGMENTO_TC35`, `POLITICA_VACIA_TC35` |
| TC-11 | `BASE_TC01` (O3) | TC-36 | `DEGRADADO_POSTERIOR_TC36` |
| TC-12 | `BASE_TC01`, `PARCIAL_BLOQUEANTE_TC12` | TC-37 | `OPCION_INCOHERENTE_TC37` |
| TC-13 | `CANCELACION_TC13` | TC-38 | `OPERACION_COLGADA_TC38`, `CREADA_VENCIDA_TC38`, `LLAVE_NO_PERSISTIBLE_TC38` |
| TC-14 | `REBOOKING_503_TC14`, `TIMEOUT_REBOOKING_TC33` | TC-39 | `INTEGRIDAD_CADENA_ROTA_TC39`, `INTEGRIDAD_DELAY_NO_POSITIVO_TC39`, `INTEGRIDAD_DESORDENADOS_TC39`, `INTEGRIDAD_MENOR_SIN_ADULTO_TC39` |
| TC-15 | `REBOOKING_409_TC15` | TC-40 | `REBOOKING_ESTRICTO_TC40`, `SIN_MENOR_TC07` |
| TC-16 | `NOTIFY_422_TC16` | TC-41 | `POLITICA_CONDICIONES_TC41` |
| TC-17 | `BASE_TC01` (compensación elegible) | TC-42 | `NOTIFY_OK_TC42` (una notificación; `BASE_TC01` con `caller = "system"` envía dos, TC-52) |
| TC-18 | `CRUCE_MEDIANOCHE_TC18` | TC-43 | `CONFLICTO_TC03` (anomalía que impide evaluar ⇒ no notifica, `needs_manual_review`), `INFORMATIVA_TC45` (sin política rota ⇒ no notifica), `NOTIFY_BLOQUEADA_POLITICA_ROTA_TC43` (BLOQUEADA con política rota ⇒ **sí** notifica), todos con `caller = "system"` |
| TC-19 | `DEGRADADA_OPS_CORE_TC19` | TC-44 | `NOTIFY_COOLDOWN_TC44`, `NOTIFY_422_TC44`, `NOTIFY_TIMEOUT_TC44`, `NOTIFY_REINTENTO_TRAS_FALLIDA_TC44`, `NOTIFY_ENFRIAMIENTO_VENCIDO_TC44`, `NOTIFY_CONCURRENTE_TC44`, `NOTIFY_EN_CURSO_COLGADO_TC44`, `NOTIFY_PRIMER_ENVIO_PENDIENTE_TC44`, `NOTIFY_RESPUESTA_FUERA_DE_ORDEN_TC44` |
| TC-20 | `BASE_TC01` (motivo `PERSONAL_DATA_REQUEST`) | TC-45 | `INFORMATIVA_TC45` (y `CONEXION_FALSA_TC06B`) |
| TC-21 | `OTRA_RESERVA_TC21`, `BASE_TC01` | TC-46 | `BASE_TC01` (elegible), `SIN_COMPENSACION_TC46` (no elegible), `INFORMATIVA_TC45` (INFORMATIVA ⇒ no elegible) |
| TC-22 | `REBOOKING_LENTO_TC22` | TC-47 | `PASAJERO_INFANT_TC23`, `PASAJERO_SIN_TIPO_TC47`, `PASAJERO_INFANT_SIN_R5_TC47` (con política rota), `PASAJERO_INFANT_INFORMATIVA_TC47` (sin política rota) |
| TC-23 | `MULTI_SEGMENTO_TC23`, `PASAJERO_INFANT_TC23`, `PASAJERO_INFANT_SIN_R5_TC47` | TC-48 | `NOTIFY_CONTENIDO_PROHIBIDO_TC48` |
| TC-24 | `SCHEDULED_POSTERIOR_TC24`, `ON_TIME_POSTERIOR_TC24`, `SCHEDULED_ANTERIOR_TC24`, `ON_TIME_ANTERIOR_TC24`, `SCHEDULED_DEGRADADO_TC24`, `ON_TIME_DEGRADADO_TC24` | TC-49 | `CONFIG_PARAMETROS_TC49` |
| TC-25 | `DOS_DELAY_TC25` | TC-50 | `SYSTEM_CLAVE_SERVICIO_TC50` |

**Índice complementario TC-51…TC-60 (`GATE_CHANGE`, política solo para `DELAY`, segmentos sin eventos, aviso de puerta, purga, vencimiento de `INDETERMINADA`, límite de tasa, registro sin campos internos y aviso al titular adulto):**

| TC | Escenario(s) |
|---|---|
| TC-51 | `GATE_SOLO_TC51` (usuario: puerta destacada con hora, sin política; sistema: una notificación informativa sin `policy_ref`) |
| TC-52 | `DELAY_Y_PUERTA_TC52`, `BASE_TC01` (contexto completo, una política `DELAY`, hasta dos notificaciones) |
| TC-53 | `POLITICA_VACIA_TC35` (`DELAY` vacía ⇒ BLOQUEADA), `GATE_POLITICA_CONFIG_TC53` (`GATE_CHANGE` nunca consulta política aunque la configuración incluya otros escenarios) |
| TC-54 | `SIN_EVENTOS_TC54` (sin eventos ⇒ `NO_EVENTS`), `GATE_SOLO_TC51` (S1 solo con puerta y S2 sin eventos ⇒ `NO_EVENTS`); `SOLO_DEGRADADO_TC02` cubre la otra rama de FR-014 (`NO_VERIFIED_INFO`) |
| TC-55 | `NOTIFY_PUERTA_CAMBIA_TC55` (24 → 25 ⇒ aviso nuevo), `NOTIFY_PUERTA_IGUAL_TC55` (misma puerta ⇒ sin reenvío) |
| TC-56 | `PURGA_OPERACIONES_VIGENTES_TC56` |
| TC-57 | `INDETERMINADA_VENCE_TC57` (INDETERMINADA ⇒ EXPIRADA tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS`, permite la generación siguiente) |
| TC-58 | `LIMITE_TASA_TEXTO_PLANO_TC58` (429, texto plano, consultas parametrizadas) |
| TC-59 | `DECISION_SESION_SIN_INTERNOS_TC59` (lectura de la decisión sin campos internos) |
| TC-60 | `AVISO_TITULAR_ADULTO_TC60`, `NOTIFY_DELAY_SOLO_MINUTOS_TC60`, `OPCIONES_CONEXION_DESCONOCIDA_TC60` |

**Datos personales ficticios (FR-101, NFR-010):** los fixtures sustituyen los datos del ejemplo del PDF por `Ana Prueba` (P1, `ADULT`, `ana.prueba@example.test`, `+00 0 0000 0000`, `00.000.000-0`, `GOLD`) y `Luis Prueba` (P2, `CHILD`, 7 años). Un test verifica que ninguno de esos valores aparece en logs ni en el registro.

### 1.2 Event Consumers — Mensajes que el sistema consume

| # | Tipo | Topic / Queue | Consumer Group | Payload Schema | DLQ |
|---|------|--------------|---------------|---------------|-----|
| — | Ninguno | Ninguno | Ninguno | Ninguno | Ninguno |

**No hay consumers.** Razón: la v1 es un servicio síncrono de petición/respuesta, estático y determinístico (H-11, DEC-02). La notificación proactiva por evento operacional es Fase 2 (§7 de `REQUERIMIENTOS_V1.md`); `get_operational_events` se **consulta** cada vez que el pasajero entra a la vista (FR-002), no se suscribe. Si en el futuro se agrega un consumer, se documentará aquí como un contrato nuevo (§5).

### 1.3 Webhooks y Otros Entry Points

| # | Tipo | Trigger | Path/Endpoint | Payload | Validación |
|---|------|---------|--------------|---------|-----------|
| — | Ninguno | Ninguno | Ninguno | Ninguno | Ninguno |

**No hay webhooks ni cron.** Razones: (1) ningún sistema externo empuja datos a este servicio (las 7 tools son de **consulta/acción iniciada por nosotros**); (2) el único trabajo periódico, la purga de retención de FR-092 (`AUDIT_RETENTION_DAYS` = 30), **no corre como cron**: es una rutina verificable invocada manualmente con el comando `python -m app.maintenance purge` y automáticamente una vez al iniciar el servicio. Tampoco es cron el reporte de métricas de NFR-008 (`python -m app.maintenance metrics`, solo lectura). Ninguno es un entry point accesible desde fuera del proceso.

---

## 2. OUTBOUND — Cómo este sistema llama al mundo

> Cada API externa, servicio Platform, base de datos o sistema externo que este sistema invoca.
> **⚠️ SAGRADO**: Si esto cambia (URL, auth, schema), el sistema deja de funcionar.

### 2.1 Las 7 tools del PDF como dependencias externas

**Estado del transporte.** El enunciado define las 7 tools como «interfaces equivalentes» con **firma lógica y ejemplos de respuesta**, y pide: «si trabajas con mocks propios, mantén estos contratos» (SRC-01-16). **No entrega URL base, rutas HTTP, autenticación ni documentación de endpoints** (se solicitan en DOC-009). Por eso:

- v1 define cada tool como un **puerto** (interfaz del dominio) con adaptador *mock* (FR-100, FR-103). El adaptador HTTP real queda fuera de v1 y se escribirá cuando exista la documentación.
- Las columnas «Base URL» y «Auth» de la tabla siguiente son, por lo tanto, **«no provistas por el enunciado»**; el contrato vinculante es la **firma lógica y el schema de respuesta** copiados de los ejemplos.
- Los parámetros de timeout y reintento **no vienen del PDF**: son parámetros propios, configurables por variable de entorno (ver «Parámetros de resiliencia»).

| # | Servicio (tool) | Tipo | Base URL | Auth | Timeout | Retry | Circuit Breaker |
|---|---------|------|---------|------|---------|-------|----------------|
| 1 | `get_trip_context(booking_id)` | Lectura | no provista por el enunciado | no provista | 2000 ms | 1 re-consulta | No |
| 2 | `get_operational_events(segment_ids)` | Lectura | no provista por el enunciado | no provista | 2000 ms | 1 re-consulta | No |
| 3 | `get_eligible_options(trip_context)` | Lectura | no provista por el enunciado | no provista | 2000 ms | 1 re-consulta | No |
| 4 | `get_policy_rules(scenario)` | Lectura | no provista por el enunciado | no provista | 2000 ms | 1 re-consulta | No |
| 5 | `create_rebooking_request(option, idempotency_key)` | Escritura (alto impacto) | no provista por el enunciado | no provista | 5000 ms | hasta 2 con la MISMA llave | No |
| 6 | `create_human_case(reason, evidence)` | Escritura | no provista por el enunciado | no provista | 5000 ms | 0 automáticos; el reintento exige un segundo clic explícito (FR-105) | No |
| 7 | `notify_passenger(message)` | Escritura | no provista por el enunciado | no provista | 5000 ms | hasta `NOTIFY_MAX_RETRIES` (2) con la misma clave; solo `caller = "system"`; hasta 2 notificaciones por evaluación | No |

**Circuit breaker: No.** Razón: servicio de una sola instancia local con un máximo de 3 llamadas de escritura por acción; el límite de reintentos de FR-054 y la matriz de FR-105 ya acotan la carga; un breaker añadiría estado compartido sin beneficio en v1.

**Parámetros de resiliencia y demás configuración:** los timeouts, reintentos, esperas, secretos y flags tienen valores por defecto propios (no del PDF) y están **todos** en la tabla de §2.4 «Configuración central (NFR-012)» (`UPSTREAM_READ_TIMEOUT_MS` = 2000, `UPSTREAM_WRITE_TIMEOUT_MS` = 5000, `READ_MAX_REQUERIES` = 1, `REBOOK_MAX_RETRIES` = 2, `WRITE_RETRY_BACKOFF_MS` = 200, `NOTIFY_MAX_RETRIES` = 2, `OPERATION_STALE_SECONDS` = 120, `OPERATION_INDETERMINATE_EXPIRY_SECONDS` = 900, `EVALUATE_RATE_LIMIT_PER_MINUTE` = 30…); ninguno está fijado en la lógica. NFR-012 incluye los parámetros operativos de §2.4.

**Presupuesto de tiempos (peor caso, con los valores por defecto y la cadena de lecturas secuencial):** una lectura con timeout se re-consulta una vez ⇒ 2 × 2 000 ms = 4 000 ms por lectura; la evaluación encadena hasta 4 lecturas (contexto, eventos, política DELAY y opciones). Una notificación tarda como máximo 3 llamadas × 5 000 ms + esperas 200 + 400 = 15 600 ms y el modo `system` puede enviar hasta 2 (DELAY y GATE_CHANGE), una tras otra. **Cifras únicas de peor caso: evaluar como usuario = 16 000 ms; evaluar como sistema con 2 notificaciones = 47 200 ms; `/accept` = 40 600 ms.**

| Operación | Cálculo | Peor caso |
|---|---|---|
| `POST …/evaluate` (`caller = "user"`) | contexto 4 000 + eventos 4 000 + política 4 000 + opciones 4 000 (cadena secuencial de 4 lecturas) | **16 000 ms** |
| `POST …/evaluate` (`caller = "system"`) | evaluación 16 000 + 2 notificaciones × (3 llamadas × 5 000 + esperas 200 + 400) | **47 200 ms** |
| `POST …/accept` (AUTOMATICA) | revalidación 16 000 + refresco de opciones vencidas 4 000 (FR-072, SF-02.4) + 3 escrituras × 5 000 + esperas 200 + 400 + caso humano por 503 persistente 5 000 | **40 600 ms** |
| `POST …/accept` (PENDIENTE_APROBACION / BLOQUEADA) | un `create_human_case` sin releer | 5 000 ms |
| `POST …/human-cases` | con `decision_id`: 5 000; sin él: evaluación fresca 16 000 + 5 000 | 5 000 / 21 000 ms |

Los timeouts de cliente recomendados (evaluar usuario 20 s, evaluar sistema 55 s, aceptar 45 s, caso humano 25 s) son el peor caso más un margen; si se cambian los timeouts de upstream o los reintentos, se recalculan estas cifras. La vista del front muestra un mensaje de lentitud pasados 1,5 s (ver `DESIGN_CONTRACT.md`).

**Matriz de errores por tool (FR-105, FR-054):**

| Tool | Falla | Comportamiento del sistema |
|---|---|---|
| `get_trip_context` | timeout, 5xx o 422 | 1 re-consulta; si persiste ⇒ `502 TRIP_CONTEXT_UNAVAILABLE`; el front muestra «no pudimos cargar tu viaje» con botón de reintento. |
| `get_operational_events` | timeout, 5xx o 422 | 1 re-consulta; si persiste ⇒ se muestra el contexto sin estado ni alerta, con aviso (`load_status.events = "FAILED"`). |
| `get_policy_rules` (solo con un DELAY relevante validado y sin bloqueo previo; GATE_CHANGE nunca la consulta) | timeout, 5xx o 422 | 1 re-consulta; si persiste ⇒ decisión **BLOQUEADA** con una anomalía que exige validación manual: sin opciones, `needs_manual_review`, soporte **ofrecido** (`BLOCKING_PARTIAL_DATA`) (FR-105, FR-086). Política **vacía** (lectura válida) ⇒ BLOQUEADA (FR-008). |
| `get_eligible_options` | timeout, 5xx o 422 | Igual que `get_policy_rules` (BLOQUEADA con soporte ofrecido). |
| (cualquier lectura) | respuesta que viola la integridad (FR-066): `retrieved_at` ausente, 0 segmentos o pasajeros, formato inválido | **Aviso y reintento, sin soporte** (sin decisión). Cadena de segmentos rota o menor sin adulto ⇒ BLOQUEADA (con soporte, `BLOCKING_PARTIAL_DATA`). |
| `create_rebooking_request` | `201` | `REBOOKING_CREATED`; operación `CREADA` (pasa a `EXPIRADA` en `expires_at`). |
| `create_rebooking_request` | `409 DUPLICATE_REQUEST` | `EXISTING_REQUEST` con el `request_id` devuelto; sin reintento ni bucle (FR-055). |
| `create_rebooking_request` | `503 UPSTREAM_TIMEOUT`, timeout de transporte o respuesta perdida | **Resultado indeterminado**: operación `INDETERMINADA`; hasta 2 reintentos con la **misma** llave; si persiste ⇒ caso humano `UPSTREAM_INDETERMINATE` (`HUMAN_CASE_CREATED`). Nunca se informa éxito ni fracaso. |
| `create_rebooking_request` | `422` u otro error no reintentable | Sin reintento; operación `FALLIDA`; `FAILED` con mensaje genérico y caso humano ofrecido. |
| `create_human_case` | error explícito (4xx/5xx con respuesta) | Intento `FALLIDO`: «no pudimos registrar tu solicitud, puedes reintentar»; el reintento es libre. |
| `create_human_case` | timeout o respuesta perdida | Intento `INDETERMINADO`: «no pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté». **No se reenvía automáticamente** (la tool no tiene llave idempotente); el reintento exige un segundo clic explícito tras advertir del posible duplicado (`confirm_possible_duplicate`). Nunca se afirma éxito (FR-105). |
| `notify_passenger` | `202` | `QUEUED` (encolada, no entregada); nunca se afirma entrega. |
| `notify_passenger` | `422 UNVALIDATED_CONTENT` o error explícito | `FALLIDA`; sin reintento. |
| `notify_passenger` | `503`, timeout o respuesta perdida | Hasta `NOTIFY_MAX_RETRIES` reintentos con la **misma** clave; si persiste ⇒ `INDETERMINADA`; nunca se afirma éxito (FR-123). |

> Los errores `400/401/403/404/429/5xx` no están definidos por el PDF (DAT-66). Política por defecto: error no listado ⇒ **no reintentar a ciegas**, registrar y escalar a caso humano.

#### Detalle por tool

```
⚠️ SAGRADO: OUTBOUND get_trip_context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIDERACIÓN LITERAL DEL PDF: «Puede devolver información parcial.»  (Lectura; SRC-01-17)
FIRMA: get_trip_context(booking_id: string) → TripContext
TIMEOUT: 2000 ms | REINTENTOS: 1 re-consulta | BASE URL / AUTH: no provistas por el enunciado

REQUEST:
  {
    "booking_id": string        // 6 caracteres [A-Z0-9]; NO es una credencial (DAT-01)
  }

RESPUESTA ESPERADA (ejemplo del PDF; los datos personales se sustituyen por valores claramente ficticios, FR-101; el resto, tal cual):
  get_trip_context("ABC123")
  {
    "booking_id": "ABC123",
    "passengers": [
      { "passenger_id": "P1", "name": "Ana Prueba", "type": "ADULT",
        "email": "ana.prueba@example.test", "phone": "+00 0 0000 0000",
        "document_id": "00.000.000-0", "loyalty_tier": "GOLD" },
      { "passenger_id": "P2", "name": "Luis Prueba", "type": "CHILD", "age": 7 }
    ],
    "segments": [
      { "segment_id": "S1", "flight_number": "LA500",  "origin": "SCL",
        "destination": "LIM", "date": "2026-09-15",
        "scheduled_departure": "14:30", "scheduled_arrival": "17:55" },
      { "segment_id": "S2", "flight_number": "LA2410", "origin": "LIM",
        "destination": "MEX", "date": "2026-09-15",
        "scheduled_departure": "19:05", "scheduled_arrival": "23:40" }
    ],
    "fare_conditions": { "changeable": true, "refundable": false,
                         "fare_family": "LIGHT" },
    "_meta": { "retrieved_at": "2026-09-15T11:02:31Z",
               "completeness": "PARTIAL",
               "missing_fields": ["fare_conditions.change_penalty_amount"] }
  }

SCHEMA COMPLETO:
  TripContext {
    booking_id: string,
    passengers: [ {
      passenger_id: string,               // "P<n>", local a la reserva
      name: string,                       // PII (UTF-8 con acentos)
      type?: string,                      // OPCIONAL (R2-03): observados "ADULT" | "CHILD"; enumeración abierta; ausente u otro valor ⇒ menor desconocido (FR-024). El JSON de ejemplo no cambia
      age?: integer,                      // PII de menor; solo en el CHILD del ejemplo
      email?: string,                     // PII; solo en P1
      phone?: string,                     // PII; E.164 con espacios; solo en P1
      document_id?: string,               // PII sensible; solo en P1
      loyalty_tier?: string               // observado: "GOLD"; no se usa para decidir
    } ],
    segments: [ {
      segment_id: string,                 // "S<n>"; llave de unión con eventos
      flight_number: string,
      origin: string,                     // IATA
      destination: string,                // IATA
      date: string,                       // YYYY-MM-DD, salida programada
      scheduled_departure: string,        // HH:MM local, sin zona
      scheduled_arrival: string           // HH:MM local, sin zona
    } ],
    fare_conditions: {
      changeable: boolean,                // condiciones de cambio VOLUNTARIO (DAT-11)
      refundable: boolean,                // idem; NO se usa para negar un reembolso por disrupción (FR-046)
      fare_family: string,                // observado: "LIGHT"
      change_penalty_amount?: integer     // AUSENTE en el ejemplo; declarado faltante en _meta.missing_fields (FR-049)
    },
    _meta: {
      retrieved_at: string,               // ISO UTC
      completeness: string,               // observado: "PARTIAL"; enumeración abierta
      missing_fields: [string]            // rutas con puntos; es un mínimo, no una lista exhaustiva (DAT-09)
    }
  }

ERRORES MANEJADOS: los de la matriz de errores (timeout, 5xx, 422 ⇒ 1 re-consulta y luego 502 propio).
INVARIANTES QUE EL SISTEMA VERIFICA: destino de S1 == origen de S2 (conexión implícita); completeness PARTIAL ⇔ missing_fields no vacío.
PRIVACIDAD: la respuesta contiene PII; no se persiste ni se registra (FR-091) y nunca se reenvía completa (FR-040).
```

```
⚠️ SAGRADO: OUTBOUND get_operational_events
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIDERACIÓN LITERAL DEL PDF: «Requiere controlar timestamp, fuente y frescura.»  (Lectura; SRC-01-18)
RESTRICCIÓN ASOCIADA: «Los datos operacionales pueden estar desactualizados o ser contradictorios entre fuentes.» (SRC-04-04)
FIRMA: get_operational_events(segment_ids: [string]) → OperationalEvents
TIMEOUT: 2000 ms | REINTENTOS: 1 re-consulta | BASE URL / AUTH: no provistas por el enunciado

REQUEST:
  [ "S1", "S2" ]                        // segment_ids de get_trip_context (DAT-29)

RESPUESTA ESPERADA (ejemplo del PDF, tal cual):
  get_operational_events(["S1","S2"])
  {
    "events": [
      { "event_id": "E-1001", "segment_id": "S1", "type": "DELAY",
        "new_departure": "17:10", "delay_minutes": 160,
        "source": "OPS_CORE",      "recorded_at": "2026-09-15T10:48:00Z" },
      { "event_id": "E-1007", "segment_id": "S1", "type": "GATE_CHANGE",
        "gate": "24",
        "source": "AIRPORT_FEED",  "recorded_at": "2026-09-15T10:55:00Z" },
      { "event_id": "E-1012", "segment_id": "S1", "type": "STATUS",
        "status": "ON_TIME",
        "source": "LEGACY_MIRROR", "recorded_at": "2026-09-15T09:30:00Z" },
      { "event_id": "E-2003", "segment_id": "S2", "type": "STATUS",
        "status": "SCHEDULED",
        "source": "OPS_CORE",      "recorded_at": "2026-09-15T10:48:00Z" }
    ],
    "_meta": { "retrieved_at": "2026-09-15T11:02:33Z",
               "sources_available": ["OPS_CORE","AIRPORT_FEED","LEGACY_MIRROR"],
               "sources_degraded":  ["LEGACY_MIRROR"] }
  }

SCHEMA COMPLETO:
  OperationalEvents {
    events: [ {
      event_id: string,                   // "E-<n>"; NUNCA se usa para ordenar (FR-011)
      segment_id: string,                 // debe estar entre los pedidos (FR-016)
      type: string,                       // observados: "DELAY" | "GATE_CHANGE" | "STATUS"; enumeración abierta (otro ⇒ UNSUPPORTED_EVENT_TYPE, FR-007)
      new_departure?: string,             // HH:MM sin zona ni fecha; solo en DELAY
      delay_minutes?: integer,            // retraso de SALIDA; solo en DELAY
      gate?: string,                      // solo en GATE_CHANGE (cadena, "24")
      status?: string,                    // solo en STATUS; observados "ON_TIME" | "SCHEDULED"
      source: string,                     // observados: "OPS_CORE" | "AIRPORT_FEED" | "LEGACY_MIRROR"
      recorded_at: string                 // ISO UTC; momento del REGISTRO, no de vigencia
    } ],
    _meta: {
      retrieved_at: string,               // ISO UTC
      sources_available: [string],
      sources_degraded: [string]          // evento con source aquí ⇒ no es evidencia (FR-010)
    }
  }

ERRORES MANEJADOS: matriz de errores. FR-014 distingue dos ramas: un segmento con SOLO evidencia degradada ⇒ estado NO_VERIFIED_INFO («sin información verificada»); un segmento sin ningún evento, o solo con eventos que no informan la salida (p. ej. GATE_CHANGE) ⇒ estado NO_EVENTS (se muestra su horario programado, sin alerta). El PDF no define qué devuelve la tool para un segmento sin eventos (DAT-28).
INVARIANTES QUE EL SISTEMA VERIFICA: recorded_at ≤ retrieved_at + CLOCK_SKEW_SECONDS (60); scheduled_departure + delay_minutes == new_departure (FR-015).
```

```
⚠️ SAGRADO: OUTBOUND get_eligible_options
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIDERACIÓN LITERAL DEL PDF: «Entrega opciones candidatas, no una decisión final.»  (Lectura; SRC-02-01)
FIRMA: get_eligible_options(trip_context) → EligibleOptions
TIMEOUT: 2000 ms | REINTENTOS: 1 re-consulta | BASE URL / AUTH: no provistas por el enunciado
VIABILIDAD CON CONEXIÓN DESCONOCIDA (FR-041 f): con `missed_connection` desconocido no se puede verificar la coherencia con el itinerario ⇒ ninguna opción es viable (todas se registran con `ITINERARY_MISMATCH`), la decisión es BLOQUEADA y se ofrece soporte.
SE INVOCA solo DESPUÉS de evaluar la política DELAY (cadena secuencial, FR-009) y solo si hay POLÍTICA ROTA (FR-039): DELAY relevante validado, sin bloqueo previo, política EVALUATED (no vacía, sin RULE_ERROR ni fallo de lectura) y al menos una regla cumplida con derecho de remedio. Con decisión INFORMATIVA (incluido el viaje solo con GATE_CHANGE) NO se invoca (TC-45, TC-51). Su request solo depende del contexto del viaje.

REQUEST (contrato efectivo v1, FR-040): la firma no cambia, pero el contenido es un SUBCONJUNTO del esquema de get_trip_context:
sin correo, teléfono, documento ni nivel de fidelidad; pasajeros solo con passenger_id y type, sin edad (se envía el booleano has_minor a nivel de grupo).
Los mocks aceptan el subconjunto; se propone al equipo formalizar un contrato reducido (DOC-013).
  {
    "booking_id": "ABC123",
    "passengers": [
      { "passenger_id": "P1", "type": "ADULT" },
      { "passenger_id": "P2", "type": "CHILD" }
    ],
    "has_minor": true,
    "segments": [
      { "segment_id": "S1", "flight_number": "LA500",  "origin": "SCL",
        "destination": "LIM", "date": "2026-09-15",
        "scheduled_departure": "14:30", "scheduled_arrival": "17:55" },
      { "segment_id": "S2", "flight_number": "LA2410", "origin": "LIM",
        "destination": "MEX", "date": "2026-09-15",
        "scheduled_departure": "19:05", "scheduled_arrival": "23:40" }
    ],
    "fare_conditions": { "changeable": true, "refundable": false, "fare_family": "LIGHT" },
    "_meta": { "retrieved_at": "2026-09-15T11:02:31Z",
               "completeness": "PARTIAL",
               "missing_fields": ["fare_conditions.change_penalty_amount"] }
  }
  Schema del request: {booking_id: string, passengers: [{passenger_id: string, type?: string (ausente ⇒ desconocido)}],
  has_minor: boolean | null (null = desconocido, FR-024), segments: [igual que TripContext.segments],
  fare_conditions: {changeable: boolean, refundable: boolean, fare_family: string, change_penalty_amount?: integer},
  _meta: {retrieved_at: string, completeness: string, missing_fields: [string]}}

RESPUESTA ESPERADA (ejemplo del PDF, tal cual):
  get_eligible_options(trip_context)
  {
    "options": [
      { "option_id": "O1", "type": "REBOOK", "flight_number": "LA2412",
        "origin": "LIM", "destination": "MEX", "date": "2026-09-16",
        "departure": "08:15", "fare_difference": 0, "seats_available": 4,
        "policy_ref": "POL-DELAY-2026-03", "confidence": "HIGH" },
      { "option_id": "O2", "type": "REBOOK", "flight_number": "LA2450",
        "origin": "LIM", "destination": "MEX", "date": "2026-09-15",
        "departure": "23:40", "fare_difference": 180000, "currency": "CLP",
        "seats_available": 1,
        "policy_ref": "POL-DELAY-2026-03", "confidence": "MEDIUM" },
      { "option_id": "O3", "type": "REFUND",
        "policy_ref": "POL-REFUND-2026-01", "confidence": "LOW" }
    ],
    "_meta": { "retrieved_at": "2026-09-15T11:02:35Z", "ttl_seconds": 120 }
  }

SCHEMA COMPLETO:
  EligibleOptions {
    options: [ {
      option_id: string,                  // "O<n>", local a la respuesta (DAT-44)
      type: string,                       // observados: "REBOOK" | "REFUND"; enumeración abierta (otro ⇒ no viable, FR-041 d)
      flight_number?: string,             // solo en REBOOK
      origin?: string,                    // solo en REBOOK
      destination?: string,               // solo en REBOOK
      date?: string,                      // solo en REBOOK, YYYY-MM-DD
      departure?: string,                 // solo en REBOOK, HH:MM local sin zona
      fare_difference?: integer,          // solo en REBOOK; sin decimales; si > 0 exige currency (FR-048)
      currency?: string,                  // ISO; solo cuando hay monto
      seats_available?: integer,          // solo en REBOOK
      policy_ref: string,                 // "POL-<ESCENARIO>-<AAAA>-<NN>"; debe coincidir con una versión recuperada y no superseded (FR-041 c)
      confidence: string                  // observados "HIGH" | "MEDIUM" | "LOW"; enumeración ABIERTA (FR-102): un valor desconocido se ordena como el más bajo, se registra tal cual y nunca decide (FR-044)
    } ],
    _meta: {
      retrieved_at: string,               // ISO UTC
      ttl_seconds: integer                // vigencia de TODA la respuesta; vence en retrieved_at + ttl_seconds (instante exacto = vencida, FR-017)
    }
  }

ERRORES MANEJADOS: matriz de errores. Sin ttl_seconds ⇒ conjunto vencido (FR-017).
```

```
⚠️ SAGRADO: OUTBOUND get_policy_rules
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIDERACIÓN LITERAL DEL PDF: «Reglas versionadas y verificables.»  (Lectura; SRC-02-02)
FIRMA: get_policy_rules(scenario: string) → PolicyRules
TIMEOUT: 2000 ms | REINTENTOS: 1 re-consulta | BASE URL / AUTH: no provistas por el enunciado
SE INVOCA solo para DELAY (FR-068, Fase 1), con un DELAY relevante VALIDADO y ningún bloqueo previo por evidencia (conflicto, tipo desconocido, INCONSISTENT_DELAY, varios segmentos afectados) (FR-008, FR-038). GATE_CHANGE NUNCA consulta política: no existe política (ni mock) para ese escenario. Es la ÚNICA fuente de umbrales: ninguna política externa entra al diseño (H-01).

REQUEST:
  "DELAY"                               // scenario (string); sale de POLICY_SCENARIOS (en la Fase 1 solo DELAY → "DELAY"; en la Fase 2 podrán añadirse escenarios). La lista de escenarios del proveedor no está definida (DAT-50)

RESPUESTA ESPERADA (ejemplo del PDF, tal cual):
  get_policy_rules("DELAY")
  {
    "scenario": "DELAY", "version": "POL-DELAY-2026-03",
    "effective_from": "2026-03-01",
    "rules": [
      { "rule_id": "R1", "condition": "delay_minutes >= 180",
        "entitlement": "REBOOK_NO_FEE",   "requires_human_approval": false },
      { "rule_id": "R2", "condition": "delay_minutes >= 240 AND international",
        "entitlement": "MEAL_VOUCHER",    "requires_human_approval": false },
      { "rule_id": "R3", "condition": "missed_connection == true",
        "entitlement": "REBOOK_NO_FEE",   "requires_human_approval": false },
      { "rule_id": "R4", "condition": "compensation_requested == true",
        "entitlement": "CASH_COMPENSATION","requires_human_approval": true },
      { "rule_id": "R5", "condition": "group_includes_minor == true",
        "entitlement": "PRIORITY_HANDLING","requires_human_approval": true }
    ],
    "_meta": { "retrieved_at": "2026-09-15T11:02:36Z",
               "superseded_versions": ["POL-DELAY-2025-11"] }
  }

SCHEMA COMPLETO:
  PolicyRules {
    scenario: string,                     // "DELAY"
    version: string,                      // "POL-<ESC>-<AAAA>-<NN>"; se fija en el registro (FR-036)
    effective_from: string,               // YYYY-MM-DD
    rules: [ {
      rule_id: string,                    // "R<n>"
      condition: string,                  // mini-lenguaje; se evalúa SOLO con el parser acotado (FR-030, FR-031); jamás eval/exec
      entitlement: string,                // observados: "REBOOK_NO_FEE" | "MEAL_VOUCHER" | "CASH_COMPENSATION" | "PRIORITY_HANDLING"; abierto (FR-037)
      requires_human_approval: boolean    // faltante o no booleano en una regla cumplida ⇒ se asume que exige aprobación (FR-008)
    } ],
    _meta: {
      retrieved_at: string,               // ISO UTC
      superseded_versions: [string]       // una opción cuyo policy_ref esté aquí no es viable (FR-041 c)
    }
  }

GRAMÁTICA ACEPTADA (lista blanca, FR-030): identificadores delay_minutes, international, missed_connection, compensation_requested,
group_includes_minor; operadores >=, >, <, <=, ==, EQ, !=, NE, AND, OR (EQ ≡ == y NE ≡ !=); AND precede a OR; literales entero y true/false; paréntesis; comparar booleano con entero o usar >/< sobre un booleano ⇒ RULE_ERROR; condición ≤ PARSER_MAX_CONDITION_CHARS (200) caracteres y ≤ PARSER_MAX_DEPTH (10) niveles. Todo lo demás ⇒ RULE_ERROR (FR-032).
ERRORES MANEJADOS: matriz de errores. Política vacía ⇒ BLOQUEADA, se asume que exige aprobación y se ofrece caso humano (FR-008). Política sin regla cumplida con derecho de remedio ⇒ INFORMATIVA (FR-039).
```

```
⚠️ SAGRADO: OUTBOUND create_rebooking_request
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIDERACIÓN LITERAL DEL PDF: «Acción de alto impacto.»  (Escritura; SRC-02-03) y «Cambiar una reserva o emitir una compensación son acciones de alto impacto.» (SRC-04-06)
FIRMA: create_rebooking_request(option, idempotency_key) → 201 | 409 | 503
TIMEOUT: 5000 ms | REINTENTOS: hasta 2 con la MISMA llave (FR-054) | BASE URL / AUTH: no provistas por el enunciado
SOLO se invoca tras el clic explícito del pasajero (FR-050), con decisión AUTOMATICA y tras revalidar (FR-051, FR-070).

REQUEST (contrato efectivo v1, FR-065): la firma del PDF (option, idempotency_key) MÁS la extensión documentada en DOC-013 (booking_id y ids de pasajeros):
  {
    "option": { …objeto de opción tal como lo devolvió la re-consulta de get_eligible_options, p. ej. O1… },
    "idempotency_key": string,           // HMAC-SHA256 en hex (64 caracteres), ver «Llave idempotente»
    "booking_id": string,                // extensión FR-065 / DOC-013
    "passenger_ids": [string]            // extensión FR-065 / DOC-013: TODOS los pasajeros del grupo (todo el grupo junto, FR-041 a)
  }
  Schema: {option: {option_id: string, type: "REBOOK", flight_number: string, origin: string, destination: string, date: string,
           departure: string, fare_difference: integer, currency?: string, seats_available: integer, policy_ref: string, confidence: string},
           idempotency_key: string, booking_id: string, passenger_ids: [string]}
  - El `option` lo resuelve el SERVIDOR con las opciones recién consultadas (por itinerary_key); el cliente nunca aporta su contenido (FR-065).
  - Los mocks aceptan la extensión y la verifican: sin `booking_id`, o con `passenger_ids` que no cubran todo el grupo de la reserva,
    responden 422 {"error": "PASSENGERS_NOT_COVERED", "detail": "…"} (comportamiento del mock, no del PDF; no reintentable).
  - Si el proveedor real no acepta los campos extra, se propone formalizarlos con el equipo (DOC-013); mientras tanto la llave incorpora el booking_id.

LLAVE IDEMPOTENTE (FR-053):
  idempotency_key = hex( HMAC-SHA256( clave = UTF-8(IDEMPOTENCY_SECRET),
                                      mensaje = UTF-8( JSON canónico de [booking_id, flight_number, date, departure, policy_version, generation] ) ) )
  - JSON canónico: arreglo de 6 elementos, serializado sin espacios (separators=(",",":")) y sin escapar caracteres no ASCII; `generation` es un entero ≥ 1.
  - Sin decision_id, sin huella, sin marcas de tiempo.
  - Se guarda en el registro de operaciones de forma atómica (unicidad) ANTES de llamar; si no pudo persistirse, NO se escribe (FR-064).
  - Mientras la operación no esté en un estado final de fracaso, toda reevaluación reutiliza su llave, aunque la versión de política cambie.

CICLO DE VIDA DE LA OPERACIÓN (FR-064):
  EN_CURSO ──201──▶ CREADA ──(expires_at)──▶ EXPIRADA
     │ ├─503/timeout agotado─▶ INDETERMINADA
     │ ├─422/error no reintentable─▶ FALLIDA
     └─ sin respuesta tras OPERATION_STALE_SECONDS (120 s)─▶ INDETERMINADA ──(OPERATION_INDETERMINATE_EXPIRY_SECONDS = 900 s sin resolverse)──▶ EXPIRADA
  - CREADA, EN_CURSO e INDETERMINADA bloquean una operación nueva sobre el mismo itinerario y la vista muestra su estado. Una INDETERMINADA deja de bloquear al pasar a EXPIRADA tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900, mayor que la vigencia de una solicitud; S-20). Riesgo conocido (S-20): si la solicitud indeterminada sí se creó y su vigencia fuera mayor, un intento nuevo podría duplicarla (TC-57).
  - EXPIRADA y FALLIDA permiten una operación nueva con la llave de generación siguiente (generation + 1).
  - Un 409 sin operación local se muestra «ya existe una solicitud para esta opción».

RESPUESTAS ESPERADAS (ejemplo del PDF, tal cual):
  create_rebooking_request(option, idempotency_key)
    → 201 { "request_id": "RBK-88231", "status": "PENDING_CONFIRMATION",
            "expires_at": "2026-09-15T11:12:00Z" }
    → 409 { "error": "DUPLICATE_REQUEST", "request_id": "RBK-88231" }
    → 503 { "error": "UPSTREAM_TIMEOUT" }   // el resultado real es indeterminado
  Nota de formato: el comentario `// el resultado real es indeterminado` NO es JSON válido; es una anotación del PDF y no se parsea,
  pero contiene la regla de negocio: 503 ⇒ resultado INDETERMINADO (DAT-67).

SCHEMA COMPLETO:
  201 Created:  {request_id: string ("RBK-<n>", opaco), status: string (observado "PENDING_CONFIRMATION"; enumeración abierta, DAT-69), expires_at: string (ISO UTC)}
  409 Conflict: {error: string ("DUPLICATE_REQUEST"), request_id: string (el MISMO del 201 original)}
  503 Service Unavailable: {error: string ("UPSTREAM_TIMEOUT")}
  422 / otros (no definidos por el PDF): {error: string, detail?: string} ⇒ no reintentable (FR-105)

ERRORES MANEJADOS:
  201: operación CREADA con request_id, status y expires_at; mensaje «pendiente de confirmación, sujeta a disponibilidad» (FR-056). La confirmación queda fuera de v1.
  409: se trata como solicitud existente («ya existe una solicitud en curso para esta opción»), sin bucles (FR-055).
  503 / timeout de transporte / respuesta perdida: INDETERMINADA ⇒ hasta 2 reintentos con la misma llave ⇒ caso humano UPSTREAM_INDETERMINATE (FR-054).
  422 u otro: no se reintenta; operación FALLIDA; mensaje genérico de fallo y caso humano ofrecido (FR-105).
```

```
⚠️ SAGRADO: OUTBOUND create_human_case
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIDERACIÓN LITERAL DEL PDF: «Escalamiento a operación humana.»  (Escritura; SRC-02-04)
FIRMA: create_human_case(reason, evidence) → 201
TIMEOUT: 5000 ms | REINTENTOS: 0 automáticos (el reintento exige un segundo clic explícito, FR-105) | BASE URL / AUTH: no provistas por el enunciado
SOLO se invoca tras el clic explícito del pasajero (FR-050). La tool NO tiene llave idempotente: la deduplicación es local y registra cada intento (FR-059).

REQUEST:
  {
    "reason": string,                    // el motivo de mayor prioridad (FR-063)
    "evidence": object                   // esquema propio, sin PII (FR-059)
  }
  reason ∈ {"UPSTREAM_INDETERMINATE","SOURCE_CONFLICT","UNSUPPORTED_EVENT_TYPE","INCONSISTENT_DELAY","MULTIPLE_AFFECTED_SEGMENTS",
            "BLOCKING_PARTIAL_DATA","COMPENSATION_REQUESTED","PERSONAL_DATA_REQUEST","POLICY_APPROVAL_REQUIRED",
            "NO_OPTION_COVERS_GROUP","NO_VIABLE_OPTION","OVERNIGHT_ASSISTANCE","OTHER_HELP"}   // en orden de prioridad (FR-063)
  evidence {
    booking_id: string,                  // identificador seudónimo
    decision_id: string,
    decision_fingerprint: string,        // 64 hex
    dedup_key: string,                   // SHA-256(booking_id ‖ motivos ordenados ‖ huella), hex
    reasons: [string],                   // TODOS los motivos simultáneos, de mayor a menor prioridad
    decision_state: string | null,       // "INFORMATIVA" | "AUTOMATICA" | "PENDIENTE_APROBACION" | "BLOQUEADA" | null
    policy_version: string | null,
    passenger_count: integer,
    group_includes_minor: boolean | null,   // solo el booleano; nunca la edad (FR-091)
    segments: [ {segment_id: string, state: string | null, delay_minutes: integer | null} ],
    option: { option_id: string, flight_number: string, origin: string, destination: string, date: string, departure: string,
              fare_difference: integer, currency: string | null, policy_ref: string } | null,   // opción elegida (FR-052); null si no aplica
    data_as_of: { trip_context: string, events: string | null, policy: string | null, options: string | null }   // retrieved_at de la instantánea
  }
  PROHIBIDO en evidence: nombre, contacto, documento, edad del menor, payloads completos de las lecturas.

RESPUESTA ESPERADA (ejemplo del PDF, tal cual):
  create_human_case(reason, evidence)
    → 201 { "case_id": "HC-4471", "queue": "DISRUPTION_L2", "sla_minutes": 45 }

SCHEMA COMPLETO:
  201 Created: {case_id: string ("HC-<n>", opaco), queue: string (observado "DISRUPTION_L2"), sla_minutes: integer (observado 45)}
  Errores: el PDF no define ninguno. Error explícito (4xx/5xx con respuesta) ⇒ intento FALLIDO, «no pudimos registrar tu solicitud, puedes reintentar».
  Timeout o respuesta perdida ⇒ intento INDETERMINADO, «no pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté»: NO se reenvía automáticamente;
  el reintento exige un segundo clic explícito tras advertir del posible duplicado (FR-105). Nunca se afirma éxito.
RIESGO CONOCIDO: la tool no admite llave idempotente (DAT-64): un reintento tras un INDETERMINADO puede duplicar el caso. Se mitiga impidiendo el reenvío automático y registrando cada intento y su resultado (FR-059).
```

```
⚠️ SAGRADO: OUTBOUND notify_passenger  (SE INVOCA SOLO con caller = "system" y NOTIFY_ENABLED = true; FR-085, FR-122, H-07, H-20, H-21)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIDERACIÓN LITERAL DEL PDF: «No debe enviar información no validada.»  (Escritura; SRC-02-05)
FIRMA: notify_passenger(message) → 202 | 422
TIMEOUT: 5000 ms | REINTENTOS: hasta NOTIFY_MAX_RETRIES (2) con la MISMA clave | BASE URL / AUTH: no provistas por el enunciado
Es la ÚNICA acción externa permitida en modo system y la única que se ejecuta SIN clic del pasajero (excepción de FR-050); ni create_rebooking_request ni
create_human_case se ejecutan en modo system (FR-121). En modo user no se invoca nunca: el mensaje se ve en la pantalla.

CUÁNDO SE ENVÍA (FR-122, FR-123): caller = "system", NOTIFY_ENABLED = true y UNA notificación POR MOTIVO (hasta 2 por evaluación, secuenciales):
  (a) reason = "DELAY", kind = "POLICY": la decisión tiene POLÍTICA ROTA (FR-039: regla cumplida con derecho de remedio). Se notifica AUNQUE la decisión sea BLOQUEADA o PENDIENTE_APROBACION
      (p. ej. menor desconocido, regla no evaluable): el problema para el pasajero existe y la validación manual es otra vía. Lleva el policy_ref de la política DELAY evaluada.
  (b) reason = "GATE_CHANGE", kind = "INFORMATIONAL": hay un GATE_CHANGE VALIDADO (fuente sana, sin empate conflictivo). NO consulta política (FR-068) y NO lleva policy_ref (aviso informativo, H-21).
  - Sin política rota y sin GATE_CHANGE validado NO se notifica: INFORMATIVA por un DELAY sin política rota, sin evento relevante, o anomalías que impiden evaluar la política
    (conflicto de fuentes, tipo de evento desconocido, lectura fallida, política vacía, RULE_ERROR). Esas anomalías quedan con needs_manual_review en la auditoría (alerta interna en Fase 2).
    El cliente que entra después (caller = "user") ve su estado normal (H-19).

REQUEST (contrato efectivo v1; extensión de contrato documentada en DOC-013):
  {
    "message": {
      "template_id": "NOTIFY_CHANGE_V1",                // plantilla fija
      "kind": "POLICY",                                 // extensión (H-21): "POLICY" | "INFORMATIONAL"
      "reason": "DELAY",                                // enumeración CERRADA: "DELAY" → «un retraso» | "GATE_CHANGE" → «un cambio de puerta»
      "text": "Hubo un cambio en tu vuelo asociado a un retraso. Revisa tu reserva en la web o en la aplicación.",
      "policy_ref": "POL-DELAY-2026-03",                // OBLIGATORIO con kind "POLICY" (versión de la política DELAY que se rompió); AUSENTE con kind "INFORMATIONAL"
      "booking_id": "ABC123",                           // destinatario (extensión: el PDF no define destinatario, DAT-65)
    "recipient_passenger_id": "P1",                    // extensión DOC-013 (FR-122): id seudónimo del TITULAR ADULTO de la reserva (el primer pasajero ADULT); NUNCA un menor. Sin titular adulto no se envía (NOT_SENT con not_sent_reason = NO_ADULT_RECIPIENT) y needs_manual_review = true (FR-122)
      "idempotency_key": "<HMAC-SHA256 en hex, 64 caracteres>"   // extensión: misma clave en los reintentos
    }
  }
  Schema: {message: {template_id: string, kind: string, reason: string, text: string, policy_ref?: string (solo kind POLICY), booking_id: string, recipient_passenger_id: string (titular adulto, FR-122), idempotency_key: string}}
  Ejemplo informativo: {"message": {"template_id": "NOTIFY_CHANGE_V1", "kind": "INFORMATIONAL", "reason": "GATE_CHANGE",
    "text": "Hubo un cambio en tu vuelo asociado a un cambio de puerta. Revisa tu reserva en la web o en la aplicación.", "booking_id": "ABC123", "idempotency_key": "<hex64>"}}
  H-21: el contrato del PDF exige policy_ref y responde 422 UNVALIDATED_CONTENT si falta. NO se inventa un policy_ref: se propone al equipo (DOC-013) admitir un aviso informativo sin policy_ref;
  el mock de v1 lo acepta cuando kind = "INFORMATIONAL" (un proveedor real que no lo acepte respondería 422 ⇒ FALLIDA).

PLANTILLA FIJA (catálogo; FR-122): «Hubo un cambio en tu vuelo asociado a {reason}. Revisa tu reserva en la web o en la aplicación.»
  - {reason} solo toma valores de una enumeración cerrada: DELAY → «un retraso», GATE_CHANGE → «un cambio de puerta». No hay otros campos libres.
  - PROHIBIDO (anti-phishing): URL, enlace, dominio, teléfono, correo u otro dato de contacto. Se invita al pasajero a entrar por sus canales habituales.
  - El validador propio (FR-081) lo bloquea ANTES de llamar: rechaza cualquier texto distinto de la plantilla con su {reason}; exige policy_ref con kind POLICY y su ausencia con kind INFORMATIONAL;
    y detecta "://", "www.", dominios con sufijo de nivel superior, "@", secuencias de 7 o más dígitos (con o sin separadores) y "wa.me". Un mensaje bloqueado nunca se envía (TC-48, TC-16).

IDEMPOTENCIA Y ENFRIAMIENTO (FR-123):
  idempotency_key = hex( HMAC-SHA256( clave = UTF-8(IDEMPOTENCY_SECRET), mensaje = UTF-8( JSON canónico de [booking_id, reason, motive_fingerprint, template_id] ) ) )
  - `motive_fingerprint` (FR-123): para reason = DELAY es el SHA-256 hex del JSON canónico de [versión de política, rule_id de las reglas cumplidas ordenados] (versión de política + reglas disparadas, FR-123): un cambio solo de minutos del retraso que no altera las reglas disparadas NO repite el aviso (TC-60); para reason = GATE_CHANGE es el SHA-256 hex del JSON canónico de la lista ordenada [[segment_id, gate], …] con la PUERTA VALIDADA de cada segmento.
    Así un cambio posterior de puerta (24 → 25) produce una clave y un aviso NUEVOS (TC-55) y la misma puerta no se reenvía. Misma (reserva + motivo + huella del motivo + plantilla) dentro de NOTIFY_COOLDOWN_SECONDS (86400) ⇒ NO se reenvía:
    la respuesta indica deduplicated = true con el estado del envío previo. DELAY y GATE_CHANGE son claves distintas.
  - Se reserva atómicamente la clave (registro EN_CURSO en la tabla notifications, con la transición de «nueva reserva» descrita allí) ANTES de llamar. Un intento FALLIDO o VENCIDO no cuenta para el enfriamiento.
  - Resultados: 202 ⇒ QUEUED (encolada, NO entregada) · 422 UNVALIDATED_CONTENT o error explícito ⇒ FALLIDA (sin reintento) ·
    503, timeout o respuesta perdida ⇒ hasta NOTIFY_MAX_RETRIES reintentos con la MISMA clave y espera de WRITE_RETRY_BACKOFF_MS (el segundo, el doble); si persiste ⇒ INDETERMINADA.
    Nunca se afirma éxito: QUEUED significa aceptada, no recibida. Cada notificación tiene su propio resultado.

RESPUESTAS ESPERADAS (ejemplo del PDF, tal cual):
  notify_passenger(message)
    → 202 { "notification_id": "NT-9912", "channel": "PUSH", "status": "QUEUED" }
    // El simulador (mock) asigna un identificador DISTINTO a cada aviso aceptado: NT-9912, NT-9913, … (dos notificaciones de una misma evaluación nunca comparten `notification_id`).
    → 422 { "error": "UNVALIDATED_CONTENT", "detail": "falta policy_ref" }

SCHEMA COMPLETO:
  202 Accepted: {notification_id: string ("NT-<n>", opaco), channel: string (observado "PUSH"; abierto), status: string (observado "QUEUED" = encolada, NO entregada; abierto)}
  422 Unprocessable: {error: string ("UNVALIDATED_CONTENT"), detail: string (p. ej. "falta policy_ref")}

VALIDADOR PROPIO PREVIO (más estricto que el 422 del proveedor): bloquea un hecho sin evidencia vigente, un campo fuera de la lista blanca, cualquier URL o dato de contacto, y exige policy_ref para kind POLICY.
PUERTO: NotifyPort.notify_passenger(message) con el objeto de valor NotificationMessage (incluye kind); en uso real (con NOTIFY_ENABLED) desde el flujo F-11 (evaluar como sistema).
```

### 2.2 Servicios Platform Internos

| # | Servicio | Recurso / Key Pattern | Operaciones | TTL / Config |
|---|---------|----------------------|-------------|-------------|
| — | Ninguno | Ninguno | Ninguno | Ninguno |

**No hay servicios Platform.** Razón: el proyecto es un ejercicio local (NFR-010: el repositorio es local, sin envío a servicios externos). No usa KVS, colas ni bases corporativas; la persistencia es una base SQLite propia (§2.3) y las dependencias externas son solo las 7 tools del PDF (§2.1).

### 2.3 Bases de Datos

| # | Tipo | Base / Schema | Tablas usadas | Acceso |
|---|------|--------------|---------------|--------|
| 1 | SQLite 3 (archivo local) | `DB_PATH` (por defecto `backend/data/disruption.db`), modo WAL, `PRAGMA foreign_keys=ON` | `decisions`, `decision_segments`, `notifications`, `decision_reads`, `decision_events`, `decision_rules`, `decision_variables`, `decision_options`, `decision_actions`, `operations`, `human_cases` | read-write (solo este servicio) |

**Reglas de persistencia (FR-091, S-13):** lista cerrada: **hechos operacionales no personales** (número de vuelo, fecha, origen, destino, hora de salida, códigos de aeropuerto), identificadores seudónimos (`decision_id`, `booking_id`, `passenger_id`, `segment_id`, `option_id`, `event_id`, `rule_id`, `case_id`, `request_id`), enumeraciones, números, marcas de tiempo y hashes. **Nunca** se guardan payloads completos, nombre, correo, teléfono, documento, edad del menor, `loyalty_tier` ni texto de mensajes (solo su hash). Los identificadores se consideran **seudónimos, no anónimos**; en los logs de aplicación `booking_id` va truncado. Retención: `AUDIT_RETENTION_DAYS` = 30 con una rutina de purga verificable del registro de decisiones y del de operaciones, casos y notificaciones (FR-092, provisional).

```
⚠️ SAGRADO: DATABASE SQLite (disruption.db)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TABLE decisions                              // FR-090: una fila por evaluación
  decision_id TEXT PRIMARY KEY               // UUID v4
  booking_id TEXT NOT NULL                   // seudónimo; índice
  created_at TEXT NOT NULL                   // ISO UTC; índice (purga)
  fingerprint TEXT NOT NULL                  // 64 hex
  anomaly_detected INTEGER NOT NULL          // 0 | 1
  decision_state TEXT NULL                   // 'INFORMATIVA' | 'AUTOMATICA' | 'PENDIENTE_APROBACION' | 'BLOQUEADA'
  policy_version TEXT NULL
  message_hash TEXT NOT NULL                 // SHA-256 hex
  human_case_reasons TEXT NOT NULL           // motivos en orden de prioridad, separados por coma (enumeraciones)
  caller TEXT NOT NULL                       // 'user' | 'system'
  needs_manual_review INTEGER NOT NULL       // 0 | 1: decisión BLOQUEADA, lectura fallida o reserva sin titular adulto (FR-122, FR-123); independiente de si se notificó
  support_offered INTEGER NOT NULL           // 0 | 1: hubo acción posible (FR-060)
  compensation_eligible INTEGER NOT NULL     // 0 | 1 (FR-067)
  mct_provided INTEGER NOT NULL              // 0 | 1; proyección mínima para la evidencia del caso humano (sin releer)
  passenger_count INTEGER NOT NULL           // 0 si trip_context INVALID; sin PII
  group_includes_minor INTEGER NULL          // 0 | 1 | NULL (desconocido); solo el booleano, nunca la edad (FR-091)
  messages_blocked INTEGER NOT NULL          // mensajes bloqueados por el validador FR-081 (métrica NFR-008)

TABLE decision_segments                      // estado resuelto por segmento: proyección mínima de la instantánea (FR-059)
  decision_id TEXT NOT NULL REFERENCES decisions(decision_id) ON DELETE CASCADE
  segment_id TEXT NOT NULL
  state TEXT NULL                            // 'ON_TIME' | 'SCHEDULED' | 'DELAYED' | 'NO_EVENTS' | 'NO_VERIFIED_INFO' | 'CONFLICT' | 'UNSUPPORTED' | 'INCONSISTENT' | NULL (eventos no leídos)
  delay_minutes INTEGER NULL
  PRIMARY KEY (decision_id, segment_id)

TABLE decision_reads                         // lecturas con retrieved_at
  decision_id TEXT NOT NULL REFERENCES decisions(decision_id) ON DELETE CASCADE
  tool TEXT NOT NULL                         // 'get_trip_context' | 'get_operational_events' | 'get_policy_rules' | 'get_eligible_options'
  retrieved_at TEXT NULL                     // ISO UTC
  outcome TEXT NOT NULL                      // 'OK' | 'FAILED' | 'INVALID' | 'NOT_REQUESTED'
  PRIMARY KEY (decision_id, tool)

TABLE decision_events                        // eventos elegidos y descartados con razón
  decision_id TEXT NOT NULL REFERENCES decisions(decision_id) ON DELETE CASCADE
  event_id TEXT NOT NULL
  segment_id TEXT NOT NULL
  event_type TEXT NOT NULL                   // enumeración abierta
  disposition TEXT NOT NULL                  // 'CHOSEN' | 'DISCARDED' | 'NOT_INTERPRETED'
  reason TEXT NULL                           // 'SOURCE_DEGRADED' | 'INCONSISTENT_DELAY' | 'UNKNOWN_SEGMENT' | 'FUTURE_TIMESTAMP' | 'SUPERSEDED' | 'SOURCE_CONFLICT' | 'UNSUPPORTED_EVENT_TYPE'
  PRIMARY KEY (decision_id, event_id)

TABLE decision_rules                         // versión de política y reglas evaluadas (FR-036)
  decision_id TEXT NOT NULL REFERENCES decisions(decision_id) ON DELETE CASCADE
  rule_id TEXT NOT NULL
  result TEXT NOT NULL                       // 'CUMPLE' | 'NO_CUMPLE' | 'INDETERMINADA'
  requires_human_approval INTEGER NOT NULL   // 0 | 1
  PRIMARY KEY (decision_id, rule_id)

TABLE decision_variables                     // FR-028
  decision_id TEXT NOT NULL REFERENCES decisions(decision_id) ON DELETE CASCADE
  segment_id TEXT NOT NULL                   // '' cuando la variable no es por segmento
  name TEXT NOT NULL                         // delay_minutes | new_arrival | missed_connection | international | group_includes_minor | compensation_requested | overnight_required
  value_boolean INTEGER NULL                 // 0 | 1 | NULL (desconocido)
  value_integer INTEGER NULL
  value_timestamp TEXT NULL                  // 'YYYY-MM-DDTHH:MM' local (new_arrival)
  origin TEXT NOT NULL                       // 'DATO' | 'DERIVADA'
  assumptions TEXT NOT NULL                  // códigos separados por coma
  PRIMARY KEY (decision_id, segment_id, name)

TABLE decision_options                       // opciones viables y descartadas con razón
  decision_id TEXT NOT NULL REFERENCES decisions(decision_id) ON DELETE CASCADE
  option_id TEXT NOT NULL
  itinerary_key TEXT NULL                    // SHA-256 hex de (flight_number|date|origin|destination|departure); es OptionView.itinerary_key; NULL en opciones sin itinerario (p. ej. REFUND)
  fingerprint TEXT NULL                      // huella FR-070 por opción (64 hex); NULL si la opción no es viable o no tiene itinerario
  type TEXT NOT NULL                         // 'REBOOK' | 'REFUND' | otros valores abiertos (FR-102)
  flight_number TEXT NULL
  origin TEXT NULL
  destination TEXT NULL
  date TEXT NULL
  departure TEXT NULL
  fare_difference INTEGER NULL
  currency TEXT NULL
  seats_available INTEGER NULL
  policy_ref TEXT NOT NULL
  confidence TEXT NOT NULL                   // observados HIGH | MEDIUM | LOW; enumeración abierta
  viable INTEGER NOT NULL                    // 0 | 1
  discard_reasons TEXT NOT NULL              // TODAS las razones separadas por coma (FR-042); '' si es viable: 'INSUFFICIENT_SEATS' | 'FEE_CONFLICT' | 'NO_ENTITLEMENT' | 'POLICY_REF_UNVERIFIED' | 'POLICY_REF_SUPERSEDED' | 'UNSUPPORTED_TYPE' | 'EXPIRED' | 'MISSING_CURRENCY' | 'ITINERARY_MISMATCH'
  is_proposed INTEGER NOT NULL               // 0 | 1
  PRIMARY KEY (decision_id, option_id)

TABLE decision_actions                       // acciones ofrecidas (FR-090 «acción»)
  decision_id TEXT NOT NULL REFERENCES decisions(decision_id) ON DELETE CASCADE
  kind TEXT NOT NULL                         // 'ACCEPT_OPTION' | 'OPEN_HUMAN_CASE'
  option_id TEXT NOT NULL                    // '' si no aplica
  effect TEXT NOT NULL                       // 'CREATE_REBOOKING' | 'CREATE_HUMAN_CASE_WITH_OPTION' | 'CREATE_HUMAN_CASE'
  PRIMARY KEY (decision_id, kind, option_id)

TABLE operations                             // registro de operaciones de rebooking (FR-053, FR-062, FR-064)
  idempotency_key TEXT PRIMARY KEY           // HMAC-SHA256 hex (FR-053); unicidad atómica
  booking_id TEXT NOT NULL
  itinerary_key TEXT NOT NULL
  flight_number TEXT NULL                    // NULL cuando la fila quedó minimizada por la purga
  date TEXT NULL
  departure TEXT NULL
  passenger_ids TEXT NULL                    // ids de pasajeros cubiertos, separados por coma (FR-065); NULL si minimizada
  policy_version TEXT NOT NULL               // versión usada al crear la llave
  generation INTEGER NOT NULL                // generación de la llave (≥ 1); entra en el HMAC
  decision_id TEXT NULL                      // decisión que originó la operación (no entra en la llave); NULL si minimizada
  minimized INTEGER NOT NULL                 // 0 | 1: 1 = registro mínimo conservado por la purga (solo columnas de identidad, estado y vigencia)
  state TEXT NOT NULL                        // 'EN_CURSO' | 'INDETERMINADA' | 'CREADA' | 'FALLIDA' | 'EXPIRADA' (FR-064); INDETERMINADA con updated_at anterior a ahora − OPERATION_INDETERMINATE_EXPIRY_SECONDS pasa a EXPIRADA
  request_id TEXT NULL                       // 'RBK-…'
  request_status TEXT NULL
  expires_at TEXT NULL                       // ISO UTC; al llegar, CREADA pasa a EXPIRADA
  attempts INTEGER NOT NULL                  // llamadas realizadas (1…3)
  last_error TEXT NULL                       // código ('UPSTREAM_TIMEOUT', 'UNPROCESSABLE', …)
  created_at TEXT NOT NULL
  updated_at TEXT NOT NULL                   // EN_CURSO con updated_at anterior a ahora − OPERATION_STALE_SECONDS pasa a INDETERMINADA
  UNIQUE (booking_id, itinerary_key, generation)
  UNIQUE INDEX uq_operations_active ON operations(booking_id, itinerary_key) WHERE state IN ('EN_CURSO','INDETERMINADA','CREADA')

TABLE notifications                          // un registro POR INTENTO de notificación del modo system (FR-122, FR-123); hasta 2 notificaciones por evaluación (una por motivo)
  notification_key TEXT NOT NULL             // HMAC-SHA256 hex de [booking_id, reason, motive_fingerprint, template_id]
  attempt INTEGER NOT NULL                   // 1, 2, … (cada «nueva reserva» tras FALLIDA o tras vencer el enfriamiento es un intento nuevo)
  booking_id TEXT NOT NULL                   // seudónimo
  decision_id TEXT NOT NULL
  motive_fingerprint TEXT NOT NULL           // DELAY: hash de [versión de política, rule_id de las reglas cumplidas ordenados]; GATE_CHANGE: hash de la lista ordenada [segment_id, puerta validada] (FR-123)
  template_id TEXT NOT NULL                  // 'NOTIFY_CHANGE_V1'
  reason TEXT NOT NULL                       // enumeración cerrada: 'DELAY' | 'GATE_CHANGE'
  kind TEXT NOT NULL                         // 'POLICY' (reason DELAY, con policy_ref) | 'INFORMATIONAL' (reason GATE_CHANGE, sin policy_ref; extensión H-21)
  policy_ref TEXT NULL                       // versión de la política DELAY que se rompió; NULL con kind 'INFORMATIONAL' (no se inventa un policy_ref)
  state TEXT NOT NULL                        // 'EN_CURSO' | 'QUEUED' | 'FALLIDA' | 'INDETERMINADA' | 'VENCIDA'; EN_CURSO se inserta ANTES de llamar
  notification_id TEXT NULL                  // 'NT-…' (identificador seudónimo, FR-091); solo con state == 'QUEUED'
  channel TEXT NULL                          // observado 'PUSH'
  attempts INTEGER NOT NULL                  // llamadas a la tool realizadas en este intento (1 … 1 + NOTIFY_MAX_RETRIES)
  last_error TEXT NULL                       // código ('UNVALIDATED_CONTENT', 'UPSTREAM_TIMEOUT', …)
  created_at TEXT NOT NULL
  updated_at TEXT NOT NULL
  PRIMARY KEY (notification_key, attempt)
  UNIQUE INDEX uq_notifications_active ON notifications(notification_key) WHERE state IN ('EN_CURSO','QUEUED','INDETERMINADA')
  // TRANSICIÓN ATÓMICA DE «NUEVA RESERVA» (R2-04). `reserve(attempt)` ejecuta UNA transacción BEGIN IMMEDIATE:
  //   1. UPDATE … SET state = 'INDETERMINADA' WHERE state = 'EN_CURSO' AND updated_at <= ahora − OPERATION_STALE_SECONDS   (recuperación tras caída).
  //   2. UPDATE … SET state = 'VENCIDA' WHERE state IN ('QUEUED','INDETERMINADA') AND updated_at <= ahora − NOTIFY_COOLDOWN_SECONDS   (fin del enfriamiento).
  //   3. INSERT del intento n+1 en estado 'EN_CURSO' (n = máximo attempt de esa clave).
  //   Si el INSERT viola uq_notifications_active hay un intento vigente (EN_CURSO, QUEUED o INDETERMINADA dentro del enfriamiento): NO se envía y se devuelve su estado con deduplicated = true.
  //   FALLIDA y VENCIDA no figuran en el índice parcial: permiten una nueva reserva inmediata. Dos llamadas concurrentes: solo una inserta; la otra recibe la violación y devuelve deduplicated = true.
  // La clave incluye el motivo: DELAY y GATE_CHANGE de la misma reserva son claves distintas e independientes; la del motivo GATE_CHANGE cambia cuando cambia la puerta validada de cualquier segmento.
  // ACTUALIZACIÓN DE RESULTADOS (R3-03): `mark(notification_key, attempt, outcome)` actualiza SOLO la fila (notification_key, attempt) con una transición CONDICIONAL en una sentencia atómica
  //   (UPDATE … WHERE notification_key = ? AND attempt = ? AND state = <estado esperado>), nunca solo por clave. Transiciones permitidas:
  //   EN_CURSO → QUEUED | FALLIDA | INDETERMINADA · INDETERMINADA → QUEUED (una respuesta 202 tardía confirma el envío del MISMO intento).
  //   Se ignoran (0 filas afectadas) las respuestas fuera de orden: una respuesta tardía de un intento viejo nunca modifica un intento nuevo, ni sobrescribe QUEUED, FALLIDA ni VENCIDA.
  //   La misma regla de «actualizar por identidad exacta y estado esperado» rige para operations (por idempotency_key) y human_cases (por dedup_key y attempt).
  // Nunca se guarda el texto del mensaje (es una plantilla fija; solo su template_id y reason).

TABLE human_cases                            // un registro POR INTENTO de caso humano (FR-059, FR-105)
  dedup_key TEXT NOT NULL                    // SHA-256(booking_id ‖ motivos ordenados ‖ huella), hex
  attempt INTEGER NOT NULL                   // 1, 2, … (cada reenvío explícito es un intento nuevo)
  booking_id TEXT NOT NULL
  decision_id TEXT NOT NULL
  decision_fingerprint TEXT NOT NULL
  reason TEXT NOT NULL                       // motivo de mayor prioridad
  reasons TEXT NOT NULL                      // todos, en orden de prioridad, separados por coma
  option_id TEXT NULL                        // opción elegida (FR-052)
  itinerary_key TEXT NULL
  state TEXT NOT NULL                        // 'EN_CURSO' | 'CREADO' | 'FALLIDO' | 'INDETERMINADO'; el intento se inserta EN_CURSO ANTES de llamar; EN_CURSO con updated_at anterior a ahora − OPERATION_STALE_SECONDS pasa a INDETERMINADO
  case_id TEXT NULL                          // 'HC-…'; solo si state == 'CREADO'
  queue TEXT NULL
  sla_minutes INTEGER NULL
  created_at TEXT NOT NULL
  updated_at TEXT NOT NULL
  PRIMARY KEY (dedup_key, attempt)
  UNIQUE INDEX uq_human_cases_active ON human_cases(dedup_key) WHERE state IN ('EN_CURSO','CREADO')
  // Reserva atómica: el INSERT del intento EN_CURSO falla si ya hay uno EN_CURSO o CREADO con la misma dedup_key ⇒ no se envía (EXISTING_CASE).
  // Deduplicación: un intento CREADO con la misma dedup_key ⇒ EXISTING_CASE. FALLIDO o INDETERMINADO NO bloquean el reintento explícito.

ESTADO EN MEMORIA (no persistido): escenario activo de los mocks (solo desarrollo).
PURGA (FR-092): **primero aplica los vencimientos de FR-064** (EN_CURSO sin respuesta ⇒ INDETERMINADA tras `OPERATION_STALE_SECONDS`; INDETERMINADA ⇒ EXPIRADA tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS`; CREADA ⇒ EXPIRADA en su expires_at) y **después** elimina filas con created_at anterior a ahora − AUDIT_RETENTION_DAYS de decisions (en cascada), human_cases, notifications y operations en estado final (FALLIDA, EXPIRADA, incluidas las que acaban de vencer). **Conserva el registro mínimo solo de las operaciones que siguen no finalizadas tras ese barrido** (EN_CURSO, INDETERMINADA aún no vencida o CREADA dentro de su vigencia, es decir, con expires_at futuro) para no perder su bloqueo (FR-064): en vez de borrarlas, anula flight_number, date, departure, passenger_ids y decision_id y marca minimized = 1; el índice uq_operations_active sigue aplicando. Una operación ya vencida se purga por antigüedad como cualquier otra y no se conserva. En v1 no existe un flujo de resolución por agente. Verificada por TC-56 y TC-57.
```

### 2.4 Configuración central (NFR-012)

> Los valores por defecto de esta tabla son los que se cargan desde `backend/config/defaults.json` (incluidos `OPERATION_INDETERMINATE_EXPIRY_SECONDS` = 900 y `EVALUATE_RATE_LIMIT_PER_MINUTE` = 30, v1.5) y se validan al arrancar.

**Diseño.** Existe **una sola clase de configuración**, `Settings` (objeto de valor inmutable, `backend/app/config.py`), que se construye al arrancar con `Settings.load(entorno)`:
1. lee el archivo de valores por defecto `backend/config/defaults.json` (cada parámetro con su valor por defecto documentado);
2. lo **sobrescribe con las variables de entorno** (prioridad máxima; los **secretos solo existen por entorno** y nunca se versionan);
3. **valida cada parámetro al arrancar** (tipo, rango, lista no vacía, longitud mínima del secreto): un valor inválido **impide el arranque** con un error `ConfigError` que nombra el parámetro (nunca muestra el valor de un secreto);
4. el dominio recibe los valores **inyectados** (por constructor o por el objeto `Settings`); **ninguno está fijado en la lógica** ni se lee de `os.environ` dentro del dominio.

**Parámetros** (todos los de los supuestos S-09…S-19 más los de operación). «Efecto» es el comportamiento que el test `TC-49` cambia y verifica.

| Parámetro (variable de entorno) | Supuesto | Defecto | Validación al arrancar | Efecto |
|---|---|---|---|---|
| `RELEVANT_DELAY_MIN_MINUTES` | S-09 | `1` | entero ≥ 1 | Retraso mínimo para tratarlo como evento relevante (FR-005) |
| `CHANGE_RIGHTS` | S-10 | `["REBOOK_NO_FEE"]` | lista no vacía de códigos | Derechos de cambio que respaldan una opción (FR-041 b) |
| `MIN_CONNECTION_MINUTES` | H-08 | mapa vacío; MCT = `0` y `mct_provided = false` para el aeropuerto que no figure | mapa IATA → entero ≥ 0 | MCT por aeropuerto (FR-022, FR-023) |
| `MCT_UNCERTAINTY_MINUTES` | S-11 | `45` | entero ≥ 0 | Ancho del margen en que `missed_connection` es desconocido (FR-022) |
| `CLOCK_SKEW_SECONDS` | S-11 | `60` | entero ≥ 0 | Tolerancia para descartar eventos con marca futura (FR-016) |
| `AUDIT_RETENTION_DAYS` | S-13 | `30` | entero ≥ 1 | Antigüedad a partir de la cual se purga el registro (FR-092) |
| `REASON_PRIORITY` | S-16 | el orden de FR-063 (13 motivos) | permutación exacta de los 13 códigos | Orden de prioridad de motivos de caso humano |
| `ASSERTION_COMPATIBILITY` | S-17 | `DELAY` > 0 = «retrasado»; `STATUS: ON_TIME` = «a tiempo»; `STATUS: SCHEDULED` = «horario programado» | cada entrada con una afirmación del conjunto cerrado | Tabla de afirmaciones incompatibles para el conflicto (FR-013) |
| `OPERATION_STALE_SECONDS` | S-18, S-19 | `120` | entero ≥ 1 | Una operación o intento `EN_CURSO` sin respuesta pasa a `INDETERMINADA`/`INDETERMINADO` (FR-064) |
| `OPERATION_INDETERMINATE_EXPIRY_SECONDS` | S-18, S-20 | `900` | entero > `OPERATION_STALE_SECONDS` | Una operación `INDETERMINADA` pasa a `EXPIRADA` y deja de bloquear (FR-064, TC-57) |
| `EVALUATE_RATE_LIMIT_PER_MINUTE` | S-20 | `30` | entero ≥ 1 | Máximo de solicitudes por minuto a `evaluate`, aceptar, caso humano y consulta de decisión, por reserva y por origen (y de intentos fallidos de credencial de servicio por origen); el exceso responde `429 RATE_LIMITED` (NFR-013, TC-58) |
| `PARSER_MAX_CONDITION_CHARS` | S-19 | `200` | entero ≥ 1 | Longitud máxima de una condición de política (FR-030) |
| `PARSER_MAX_DEPTH` | S-19 | `10` | entero ≥ 1 | Niveles máximos de anidación (FR-030) |
| `EVENT_MAX_AGE_SECONDS` | H-06 | sin límite (`null`) | entero ≥ 1 o `null` | Antigüedad máxima de un evento como evidencia (FR-017) |
| `SUPPORTED_EVENT_TYPES` | FR-068 | `["DELAY","GATE_CHANGE","STATUS"]` | lista no vacía de códigos | Tipos de evento que se interpretan; otro ⇒ `UNSUPPORTED_EVENT_TYPE` (FR-007, FR-068) |
| `NOTIFY_ONLY_EVENT_TYPES` | FR-068, FR-122 | `["GATE_CHANGE"]` | subconjunto de `SUPPORTED_EVENT_TYPES` | Tipos que se informan al usuario y se notifican al sistema **sin consultar política** (aviso `INFORMATIONAL` sin `policy_ref`); un viaje solo con ellos queda INFORMATIVA |
| `POLICY_SCENARIOS` | FR-068 | `{"DELAY":"DELAY"}` | claves ⊆ `SUPPORTED_EVENT_TYPES`; valores no vacíos | Escenario de `get_policy_rules` por tipo de evento (Fase 1: solo `DELAY`). Un tipo de `NOTIFY_ONLY_EVENT_TYPES` nunca consulta política aunque figure aquí (TC-53) |
| `REBOOK_MAX_RETRIES` | — | `2` | entero entre 0 y 5 | Reintentos de `create_rebooking_request` con la misma llave (FR-054) |
| `REMEDY_RIGHTS` | — | `["REBOOK_NO_FEE","MEAL_VOUCHER","CASH_COMPENSATION"]` | lista no vacía de códigos | Derechos que rompen la política (FR-039) |
| `COMPENSATION_RIGHTS` | — | `["CASH_COMPENSATION"]` | lista de códigos | Derechos que hacen elegible el motivo de compensación (FR-067) |
| `NOTIFY_ENABLED` | — | `false` | booleano | Activa `notify_passenger` en modo `system` (FR-085) |
| `NOTIFY_COOLDOWN_SECONDS` | — | `86400` | entero ≥ 0 | Enfriamiento de la notificación idempotente (FR-123) |
| `NOTIFY_MAX_RETRIES` | — | `2` | entero entre 0 y 5 | Reintentos de la notificación con la misma clave (FR-123) |
| `SERVICE_API_KEY` (solo entorno) | — | sin valor: **modo `system` apagado** | si existe, ≥ 16 caracteres | Credencial `X-Service-Key` del modo `system` (FR-120) |
| `IDEMPOTENCY_SECRET` (solo entorno) | — | sin valor: **el servicio no arranca** | ≥ 16 caracteres | Clave del HMAC de las llaves de rebooking y de notificación (FR-053, FR-123) |
| `UPSTREAM_READ_TIMEOUT_MS` | — | `2000` | entero ≥ 100 | Timeout de cada lectura (FR-105) |
| `UPSTREAM_WRITE_TIMEOUT_MS` | — | `5000` | entero ≥ 100 | Timeout de cada escritura |
| `READ_MAX_REQUERIES` | — | `1` | entero entre 0 y 3 | Re-consultas de una lectura fallida o vencida (FR-017, FR-105) |
| `WRITE_RETRY_BACKOFF_MS` | — | `200` | entero ≥ 0 | Espera antes del primer reintento; el segundo espera el doble |
| `DEV_SESSION_HEADER_ENABLED` | — | `false` | booleano | Habilita la cabecera de sesión simulada (FR-001) |
| `DEV_ENDPOINTS_ENABLED` | — | `false` | booleano | Habilita `/api/dev/*` |
| `CLOCK_MODE` | — | `system` | `system` o `scenario` | `SystemClock` o `ScenarioClock` |
| `CORS_ALLOWED_ORIGINS` | — | `http://localhost:5173` | lista de orígenes | CORS acotado al front (NFR-003) |
| `DB_PATH` | — | `backend/data/disruption.db` | ruta escribible | Archivo SQLite |

`CHANGE_RIGHTS` (S-10) y `REASON_PRIORITY` (S-16) figuran en la lista de NFR-012.
Fuera de la configuración de ejecución quedan las reglas de producto sin parámetro (S-12: más de un segmento retrasado ⇒ caso humano; S-19: la fecha de llegada suma un día si la hora es menor que la de salida) y las cifras de aceptación de S-15 (p95 < 1,5 s y cobertura ≥ 85 %), que son umbrales de las pruebas (`PERF_P95_BUDGET_MS`, `COVERAGE_MIN` en la configuración de pruebas).

**Verificación (TC-49, `backend/tests/unit/test_config.py`):** un test parametrizado recorre esta tabla; para cada parámetro construye un `Settings` con un valor cambiado y comprueba que el comportamiento cambia (p. ej. `RELEVANT_DELAY_MIN_MINUTES = 20` deja un retraso de 10 min sin alerta; `REMEDY_RIGHTS` sin `REBOOK_NO_FEE` convierte el caso base en INFORMATIVA), y para cada valor inválido comprueba que `Settings.load` falla nombrando el parámetro. Otro test (AST) comprueba que ningún literal de estos valores aparece en la lógica del dominio.

---

## 3. Matriz de Dependencias

```
SISTEMA: Disruption Companion
│
├── INBOUND (el mundo nos llama)
│   ├── HTTP: GET /ping                                  (verificación de vida)
│   ├── HTTP: /api/v1/*                                  (consumer: front React de prueba y pruebas automatizadas)
│   │   ├── POST /trips/{booking_id}/evaluate          (caller = user | system; system con X-Service-Key)
│   │   ├── POST /trips/{booking_id}/options/{option_id}/accept
│   │   ├── POST /trips/{booking_id}/human-cases
│   │   └── GET  /decisions/{decision_id}
│   ├── HTTP: /api/dev/*                                 (solo desarrollo: GET scenarios, PUT scenario, PUT clock)
│   ├── Event consumers: ninguno                          (servicio síncrono; Fase 2 para eventos)
│   └── Webhooks / cron: ninguno                          (purga y métricas por comando; purga también al arranque)
│
└── OUTBOUND (llamamos al mundo)
    ├── get_trip_context          (lectura)    → contexto de la reserva
    ├── get_operational_events    (lectura)    → eventos por segmento
    ├── get_eligible_options      (lectura)    → opciones candidatas
    ├── get_policy_rules          (lectura)    → reglas versionadas
    ├── create_rebooking_request  (escritura)  → rebooking idempotente (alto impacto)
    ├── create_human_case         (escritura)  → escalamiento humano
    ├── notify_passenger          (escritura)  → solo caller = system: política rota (kind POLICY) y/o cambio de puerta (kind INFORMATIONAL, sin policy_ref); plantilla fija, sin URL
    ├── Servicios Platform: ninguno
    └── SQLite local (disruption.db): decisiones, operaciones, casos humanos
```

---

## 4. Historial de Cambios de Contratos

> Los cambios a este documento deben ser coordinados, versionados y con período de deprecación.

| Fecha | Versión | Cambio | Impacto | Coordinado con |
|-------|---------|--------|---------|---------------|
| 2026-10-19 | v1.0 | Creación inicial: 7 endpoints inbound, 7 tools outbound, base SQLite propia | Ninguno: proyecto nuevo, sin consumidores productivos | Usuario (modo auto) y equipo SDD (Builder, Step Reviewer, CTO) |
| 2026-10-19 | v1.2 | Ronda 2 antes de cualquier consumidor: `GET …/view` reemplazado por `POST …/evaluate` con `caller`; modo `system` con `X-Service-Key`; `notify_passenger` en uso real con plantilla fija; estado `INFORMATIVA`; soporte solo con acción posible y compensación condicionada; `STATUS` sano más reciente reemplaza al `DELAY`; parser con `!=`/`NE`; configuración central (§2.4); tabla `notifications`; escenarios TC-42…TC-50 | Ninguno: el contrato v1.0 no tuvo consumidores externos ni de producción | Usuario (2026-10-19) |
| 2026-10-19 | v1.3 | Ronda 3: `GATE_CHANGE` siempre visible y destacado en la vista (`gate_recorded_at`, alerta `GATE_CHANGE`) y notificado en modo `system` como aviso informativo sin `policy_ref` (`kind`); política solo para `DELAY`; `notifications` por motivo con reserva atómica y estado `VENCIDA`; fallo de política u opciones ⇒ BLOQUEADA con soporte; `passengers[].type` opcional; parámetros `SUPPORTED_EVENT_TYPES`, `NOTIFY_ONLY_EVENT_TYPES`, `POLICY_SCENARIOS`; escenarios TC-51…TC-53 | Ninguno: aún sin consumidores | Usuario (2026-10-19) |
| 2026-10-19 | v1.6 | Ronda 7 (CTO de A2): la purga aplica primero los vencimientos de FR-064 y solo conserva minimizadas las operaciones aún no finalizadas (escenario `PURGA_OPERACIONES_VIGENTES_TC56` redefinido: jóvenes retenidas, vencidas purgadas); límite de tasa `429` también en aceptar, caso humano y consulta de decisión, por reserva y por origen, y en los intentos fallidos de credencial de servicio; el simulador asigna identificadores de notificación distintos (`NT-9912`, `NT-9913`; cierra DEBT-A1-09); `CONFIG_PARAMETROS_TC49` cubre por nombre los parámetros operativos | Ninguno: aún sin consumidores | Usuario (2026-10-19, resoluciones del orquestador) |
| 2026-10-19 | v1.5 | Ronda 5 (resoluciones de A2, OQ-A2-01…15): `INDETERMINADA` pasa a `EXPIRADA` tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900); la lectura de la decisión no devuelve `needs_manual_review` ni `notifications` a la sesión del pasajero; la huella del aviso `DELAY` es versión de política + reglas cumplidas; el aviso se dirige al titular adulto (`recipient_passenger_id`, `NO_ADULT_RECIPIENT`); `POST …/evaluate` con límite de tasa `429 RATE_LIMITED` (`EVALUATE_RATE_LIMIT_PER_MINUTE` = 30); con `missed_connection` desconocido ninguna opción es viable (BLOQUEADA con soporte); parámetros nuevos en §2.4 y `NFR-013`; escenarios TC-57…TC-60; ronda 6 (A2): sin titular adulto el aviso no se envía y se marca `needs_manual_review` (FR-122) | Ninguno: aún sin consumidores | Usuario (2026-10-19, resoluciones del orquestador) |
| 2026-10-19 | v1.4 | Ronda 4: estado de segmento `NO_EVENTS`; la notificación de `GATE_CHANGE` usa como huella la puerta validada de cada segmento (24 → 25 ⇒ aviso nuevo); `notifications[].status` admite `EN_CURSO`; `mark` condicional por (clave, intento) con respuestas fuera de orden; la purga conserva el registro mínimo de las operaciones vigentes; bloqueo por menor desconocido independiente de R5; escenarios TC-54…TC-56 | Ninguno: aún sin consumidores | Usuario (2026-10-19) |

---

## 5. Proceso para Cambiar un Contrato

Si por razones de negocio un contrato debe cambiar, el proceso es:

1. **Proponer** el cambio con justificación de negocio (y traza a un `FR-xxx`/`DEC-xx`; los requisitos solo cambian con aprobación del usuario).
2. **Identificar** todos los consumidores/proveedores afectados (en v1: el front React, las pruebas de contrato y los *mocks* de las 7 tools).
3. **Coordinar** con cada equipo afectado.
4. **Versionar** el API (`/api/v2`, …) — NO romper la versión actual. Los contratos salientes de las 7 tools **no los controla este equipo**: un cambio del proveedor se absorbe en el adaptador, nunca en el dominio.
5. **Período de deprecación** mínimo de 3 meses para la versión anterior (en el ejercicio, hasta la entrega).
6. **Actualizar** este documento DESPUÉS de que todos hayan migrado.
7. **Eliminar** la versión vieja solo cuando no haya tráfico.

Agregar un campo opcional a una respuesta o un `scenario_id` al catálogo de desarrollo **agrega** contrato (v1.x); quitar o renombrar un campo, cambiar un código HTTP o un valor de enumeración **modifica** contrato (v2).
