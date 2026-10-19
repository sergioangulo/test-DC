# Notas Obligatorias, Información a Solicitar, Preguntas a Producto/Legal y Extensiones (`DOC-008`, `DOC-009`, `DOC-011`, `DOC-012`, `DOC-013`)

---

## 1. Seis Notas Obligatorias de Diseño (`DOC-008`)

1. **Soberanía de `get_policy_rules`**: Las políticas publicadas en portales externos no pueden contradecir en runtime las reglas versionadas del sistema; en V0 rigen exclusivamente las reglas devueltas por `get_policy_rules`.
2. **Necesidad del campo `cause`**: Sería altamente útil contar con la causa del evento operacional (clima/fuerza mayor vs imputable a la aerolínea) en `get_operational_events`, ya que en múltiples jurisdicciones la compensación económica depende de la causa.
3. **Cancelación y adelanto de vuelo**: Quedan acotados para una segunda etapa (`V1`/`V2`); en V0 un evento `CANCELLATION` no se interpreta a ciegas y deriva de forma segura a un agente humano (`UNSUPPORTED_EVENT_TYPE`).
4. **Definición de «menor» por país**: En V0 se deriva de `type == "CHILD"`; la edad límite exacta según legislación local debe parametrizarse por jurisdicción.
5. **Idioma neutro**: En V0 todos los mensajes utilizan español neutro sin localización regional.
6. **Visión futura proactiva**: La evolución en `V2` contempla la invocación proactiva por evento operacional (`caller = "system"` + `notify_passenger` con plantilla fija sin enlaces).

---

## 2. Información Técnica a Solicitar al Equipo (`DOC-009`)

1. **Tiempo Mínimo de Conexión (MCT) oficial por aeropuerto y terminal**: hoy ausente en `get_trip_context` (asumido `0 min` con banda de incertidumbre de `45 min`).
2. **Catálogo cerrado de tipos de evento y estados**: lista oficial de valores posibles de `type` y `status` en `get_operational_events`.
3. **Semántica operativa de `PENDING_CONFIRMATION`**: cómo y cuándo se confirma finalmente la solicitud `RBK-*` creada por `create_rebooking_request` (webhook, polling o confirmación síncrona).
4. **Campo `cause` en eventos operacionales**: tipificación de la causa del retraso.
5. **Regla formal de mayoría de edad / menor no acompañado** en el maestro de pasajeros.

---

## 3. Preguntas para Producto y Legal (`DOC-011`)

1. **Jurisdicción aplicable en itinerarios multi-país (`SCL → LIM → MEX`)**: ¿la política aplicable se determina por el país de compra, el país de origen del tramo afectado (`CL`) o el país donde ocurre la pérdida de conexión (`PE`)?
2. **Tratamiento de reembolsos (`O3`) en tarifas con `refundable: false`**: ante una disrupción severa o pérdida de conexión, ¿cuándo prevalece el derecho regulatorio de devolución por desistimiento sobre la condición tarifaria comercial?
3. **Asistencia por pernocte (`overnight_required`)**: cuando la única opción viable sale al día siguiente (`LA2412` a las `08:15` del 16 de septiembre) pero el retraso inicial fue de `160 min` (`< 240 min` de `R2`), ¿debe otorgarse asistencia de alojamiento de forma automática o por evaluación del agente?

---

## 4. Diseño de la Aprobación Humana (`DOC-012`)

Cuando una decisión queda en `PENDIENTE_APROBACION` (porque una regla cumplida de la política, como `R5` o `R2`, exige `requires_human_approval: true`) y se crea el caso humano (`HC-4471`):
- La aprobación del agente **autoriza la decisión**, pero **no ejecuta a ciegas con datos envejecidos**: dado que el SLA humano (`45 min`) es mayor que el TTL de las opciones (`120 s`), al momento en que el agente aprueba el caso el sistema debe **revalidar la disponibilidad de asientos y la huella del itinerario** antes de confirmar el cambio definitivo.

---

## 5. Extensiones de Contrato Propuestas (`DOC-013`)

1. **`create_rebooking_request`**: incluir explícitamente `booking_id` y `passenger_ids` junto a `(option, idempotency_key)` para garantizar a nivel de contrato que el cambio cubra a todo el grupo familiar sin dividir la reserva.
2. **`get_eligible_options`**: formalizar el contrato de entrada reducido (`ReducedTripContext` sin nombre completo, documento ni edad) aplicando privacidad por diseño y mínimo privilegio.
3. **`notify_passenger` (para Fase 2 / V2)**: admitir avisos informativos de cambio de puerta (`kind: "INFORMATIONAL"`) sin requerir un `policy_ref` de compensación/reprogramación.
