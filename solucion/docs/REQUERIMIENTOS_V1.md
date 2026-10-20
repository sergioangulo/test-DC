# Requerimientos v1 — Disruption Companion (derivados de las decisiones)

> **Fuente:** `DOCUMENTO_DE_TRABAJO_DECISIONES.md` (35 de 37 decisiones tomadas; DEC-10 y DEC-20 pendientes con notas). **Ronda 2 (2026-10-19):** el usuario añadió el modo `system`/`user`, la notificación, el estado informativo sin política rota, el menú de compensación condicionado, `SCHEDULED` como reemplazo de un retraso, el menor desconocido y la configuración (ver H-17…H-19).
> **Base:** `03_Requerimientos/REQUERIMIENTOS.md` (REQ-*), `04_Analisis_de_Datos/` (DAT/DQ/TC), `01_Fuente_y_Trazabilidad` (SRC).
> **Formato:** `FR-nnn` funcionales · `NFR-nnn` no funcionales · `DOC-nnn` documentación. Cada uno traza a `DEC-nn` y a `REQ-*`/`SRC-*`/`GAP-*`/`DAT-*`/`DQ-*`/`TC-*`.
> **Alcance v1:** backend Python (servicio de decisión) + front React de prueba, ambos sin IA en runtime.

## 0. Cómo se resolvieron los conflictos entre decisiones

Orden de precedencia aplicado: **(1) notas escritas por ti** › **(2) opción marcada** › **(3) recomendación del análisis**. Una decisión **PENDIENTE** con notas se trata como **supuesto provisional** (marcado `PROV`) hasta que la confirmes.

## 1. Hallazgos: puntos donde las decisiones se contradicen o quedan abiertas

| ID | Hallazgo | Cómo lo traté | Confirmar |
|---|---|---|---|
| **H-01** | **DEC-05** figura «incorpora info externa: Sí», pero tus notas dicen «omitiremos las políticas externas (reales)»; DEC-26 y DEC-33 también. | Prevalecen las notas: **ninguna política externa entra al diseño**. El umbral sale solo de `get_policy_rules`. | Sí |
| **H-02** | **DEC-09**: marcaste «d) siempre humano ante conflicto», pero tus notas describen otra regla: gana el evento más reciente si **no** es `source_degraded`; dos eventos contradictorios **sin** degradación → soporte. | Implemento **las notas** (FR-010 a FR-014), precisadas por ti el 2026-10-19: un `ON_TIME` o `SCHEDULED` más reciente y sano sobrescribe al `DELAY`; el conflicto queda para empates de marca de tiempo. | Sí |
| **H-03** | **DEC-15** no incluye «a) hay un menor» como disparador, pero **DEC-16** dice «con un menor siempre se abre caso humano» y **DEC-13** dice «la política indica si se puede automatizar». | El menor **no** es un disparador fijo: lo decide `requires_human_approval` de la regla R5 (FR-035, FR-052). En el caso base resulta en caso humano. | Sí |
| **H-04** | **DEC-14** («toda escritura requiere confirmación humana») vs **DEC-16**. | «Confirmación» = **clic del pasajero**; «aprobación humana» = **agente**, solo cuando la política la exige. Son dos controles distintos. | Sí |
| **H-05** | **DEC-01** elige track Backend, pero las notas de **DEC-04** piden además una visualización simple (y hoy pides React). | Se entregan ambos: backend como evidencia principal y front de prueba. `REQ-F-08` queda cubierto parcialmente. | No |
| **H-06** | **DEC-10 PENDIENTE**: tus notas dicen «usar el dato más reciente, respetar TTL, re-consultar si venció». | `PROV`: sin umbral numérico de antigüedad para eventos (parámetro `EVENT_MAX_AGE_SECONDS`, por defecto **sin límite**). | Sí |
| **H-07** | **DEC-20 PENDIENTE**: tus notas dicen que `notify_passenger` no se usaría en v1; el 2026-10-19 añadiste el modo `system`. | **Resuelto por tu mensaje:** `notify_passenger` se usa solo en modo `system` con plantilla fija (FR-085, FR-122). | Sí |
| **H-08** | **DEC-07**: falta el tiempo mínimo de conexión (MCT) y pides solicitarlo. | `MIN_CONNECTION_MINUTES` por aeropuerto, **0 por defecto** y rotulado «supuesto»; se lista como dato a solicitar (DOC-009). | Sí |
| **H-09** | **DEC-05** exige umbral «configurable por las políticas»; las reglas del PDF solo traen umbrales de retraso para derechos (R1=180, R2=240). | Un retraso validado se **informa siempre** (`RELEVANT_DELAY_MIN_MINUTES`=1); qué derechos otorga lo dice la política (FR-005, FR-034). | Sí |
| **H-10** | **DEC-23** pide asociar al `booking_id` y a la vez nunca registrar PII. | `booking_id` va en el registro de auditoría; en los logs de aplicación se **trunca**. Nunca nombre, edad del menor ni RUT. | Sí |
| **H-11** | **DEC-02** menciona un futuro «JEV» con decisión si probabilidad > 95 %. | Fuera de v1 (Fase 2); v1 es estático y determinístico. | No |
| **H-12** | **DEC-37** eligió solo «a» (registrar uso de IA); no adoptó «b) no publicar artefactos». | Se respeta. `REQ-N-10` sigue vigente: el repositorio es local; **cualquier envío a un servicio externo** (incluida la revisión /codex) se anota en la bitácora de IA (DOC-006). | No |
| **H-14** | **FR-053** excluye el `decision_id` de la llave idempotente (DEC-18 decía «+ decisión») para que sea estable entre reevaluaciones. Sobre el menor: DEC-32 decía solo `type == CHILD`. | La llave estable queda como desviación deliberada. **Menor: aclarado por ti** el 2026-10-19: tipo desconocido = posible menor ⇒ validación manual si hay política rota (FR-024). | Sí (solo la llave) |
| **H-15** | Revisión CTO (mejora M1): si la política recuperada **no** trae una regla como R5, un menor podría rebookearse sin aprobación; DEC-16 decía «con un menor siempre caso humano» y tus notas dicen «la política indica». | Se sigue tu nota (lo decide la política). **Riesgo declarado.** | **Sí** |
| **H-16** | La opción «consulta sobre compensación» del menú podría sugerir el derecho; y FR-013 envía a soporte una secuencia sana «a tiempo» → «retraso». | **Aclarado por ti:** el motivo de compensación solo aparece si hay compensación elegible (FR-067) y un retraso sin política rota solo se informa, sin soporte (FR-039). H-18 quedó resuelto. | Sí |
| **H-17** | Ronda 2: el modo `system`/`user`. La **creación del disparo automático** por evento operacional (quién llama con `system`) y **guardar la respuesta para el front** son Fase 2; v1 solo expone la entrada y envía la notificación. | FR-120…124. | Sí |
| **H-18** | `SCHEDULED` y `ON_TIME` más recientes que un `DELAY` (el avión puede llegar antes por el viento). | **Resuelto por ti (2026-10-19):** el más reciente sano sobrescribe al `DELAY`; un evento degradado nunca lo hace (FR-012, FR-013). | Resuelto |
| **H-19** | Ronda 2: en modo `system`, una anomalía (conflicto de fuentes, tipo desconocido) **no** notifica al pasajero porque no es una política rota. | Se registra para revisión interna; alerta interna en Fase 2 (FR-123). **Confirmado por ti** el 2026-10-19; al entrar, el cliente (modo `user`) ve su estado normal. | Confirmado |
| **H-20** | `GATE_CHANGE` debe indicarse al usuario y, en modo `system`, **notificarse**; no consulta reglas en la Fase 1 (solo `DELAY` lanza política). | **Resuelto por ti (2026-10-19):** FR-006, FR-068, FR-122. | Resuelto |
| **H-21** | La notificación de `GATE_CHANGE` no tiene política: el contrato de `notify_passenger` exige `policy_ref` (`422 UNVALIDATED_CONTENT` si falta). | Se propone al equipo (DOC-013) permitir un aviso **informativo** sin `policy_ref`; el *mock* de v1 lo acepta marcado `kind: INFORMATIONAL`. **No se inventa un `policy_ref`.** | **Sí** |
| **H-13** | Revisión CTO de la Etapa 0 (Codex): con MCT desconocido (0), un «sin conexión perdida» usaría un dato que falta; el análisis original (TC-06) lo daba por falso. | El resultado pasa a **desconocido** en el margen `[0, 45)` min (FR-022); cambia el resultado esperado de TC-06. `MCT_UNCERTAINTY_MINUTES` es un supuesto mío **que no prueba que la conexión sea viable**: un «falso» con MCT no provisto se rotula «ESTIMADA, sujeta a MCT» y la interfaz nunca dice «tu conexión está segura». | **Sí** |

## 2. Flujo funcional resumido

```
Entrada: caller=user (sesión del pasajero) o caller=system (credencial de servicio) + booking_id   FR-120
 └─ [siempre] get_trip_context + get_operational_events(segment_ids)      FR-002
     ├─ validar eventos: excluir degradados; más reciente gana; conflicto → humano   FR-010..017
     ├─ ¿evento relevante validado? NO → solo contexto, sin alertas                  FR-004
     └─ SÍ (DELAY) → get_policy_rules("DELAY") → evaluar TODAS las reglas       FR-008, 030..037
              └─ derivar variables (delay, llegada nueva, conexión perdida, menor…)   FR-020..029
                   └─ get_eligible_options(contexto mínimo) → filtrar viables          FR-040..049
                        └─ mostrar: contexto + alerta + reglas + opción propuesta
                           + vía de reembolso + avisos + botones                        FR-110..113
 Acciones externas (solo por clic del pasajero)                                          FR-050
   ├─ Aceptar opción  → ¿decisión BLOQUEADA o exige aprobación? sí → caso humano (con      FR-038, 052, 059
   │                     instantánea, sin revalidar)
   │                     no → revalidar todo (huella) → create_rebooking_request           FR-051, 053..056, 070
   └─ Hablar con una persona → create_human_case (reason + evidence sin PII)           FR-057..063
 caller=system: política rota (DELAY) o GATE_CHANGE → notify_passenger (plantilla fija, sin URL); resto → solo se informa     FR-039, 120..124
Todo queda en el registro de decisión (decision_id, sin PII)                            FR-090..093
```

## 3. Requisitos funcionales (`FR`)

### 3.1 Entrada, alcance y detección

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-001** | Se asume sesión autenticada: el backend recibe el `booking_id` de la sesión (en el front de prueba, un selector de escenario que fija una cabecera de sesión simulada, **habilitada solo con `DEV_SESSION_HEADER_ENABLED=true`, apagada por defecto**). **Autorización:** todo endpoint verifica que el `booking_id` y el `decision_id` solicitados pertenezcan a la sesión; una reserva ajena y una inexistente producen **la misma respuesta** (`404 NOT_FOUND`, mismo cuerpo), para no confirmar su existencia. El `decision_id` es un UUID aleatorio no adivinable. Los scripts de arranque de desarrollo habilitan la cabecera; en cualquier otro perfil toda petición `caller = user` sin sesión responde `401`, y `caller = system` exige la credencial de servicio (FR-120). Los errores nunca muestran trazas ni repiten la entrada. Nunca se pide ni muestra documento de identidad. | DEC-21 | REQ-F-01, REQ-N-04, GAP-21, DAT-01 |
| **FR-002** | Cada entrada del pasajero a la vista (modo `user`) consulta de nuevo `get_trip_context` y `get_operational_events`. No hay caché en v1 (Fase 2). | DEC-19, DEC-10 | REQ-F-21, REQ-F-25 |
| **FR-003** | El contexto del viaje se muestra siempre: segmentos (origen, destino, fecha, hora programada, estado), número de pasajeros y nombre de pila del titular —el primer pasajero adulto de la reserva; sin adulto se omite el saludo— (**única excepción de PII autorizada** en pantalla; ver FR-112). | DEC-04, DEC-21 | REQ-F-01, REQ-F-12 |
| **FR-004** | Si **no hay anomalía** (ningún `DELAY` relevante ni `GATE_CHANGE` validado y ninguna evidencia anómala: conflicto, tipo desconocido o evento incoherente), solo se muestra el contexto: sin alertas, reglas, opciones ni botones **de acción** (puede haber un botón «Actualizar», que solo vuelve a consultar y no es una acción externa); el cliente ve que todo está en orden. Con un `GATE_CHANGE` validado sin retraso, la decisión es `INFORMATIVA` con el cambio de puerta destacado (FR-006, FR-068). La evidencia **degradada** no genera alerta ni estado propio, pero aplica FR-014 (rótulo «sin información verificada»). **El soporte no está siempre disponible:** solo se ofrece cuando hay una acción posible (FR-039, FR-060). | DEC-02 | REQ-F-02 |
| **FR-005** | Evento relevante en v1 = `DELAY` validado con `delay_minutes` ≥ `RELEVANT_DELAY_MIN_MINUTES` (config, 1). Qué derechos otorga lo decide la política (FR-034). | DEC-05, DEC-31 | REQ-F-11, H-09 |
| **FR-006** | `GATE_CHANGE` **se informa siempre al usuario**: modo `user`, la vista muestra el cambio de puerta de forma destacada, con la hora de la información; modo `system`, se envía `notify_passenger` (FR-122, caso b). **No consulta reglas de política en la Fase 1** (FR-068). No abre por sí solo el flujo de problema. `STATUS` se reconoce. | DEC-05, DEC-31 (precisado por el usuario 2026-10-19) | REQ-F-11, DAT-23 |
| **FR-007** | Un evento de tipo desconocido o no soportado (p. ej. `CANCELLATION`) no se interpreta: se muestra un aviso neutro («una persona debe revisar tu vuelo») y se **ofrece** el botón de caso humano con razón `UNSUPPORTED_EVENT_TYPE`. | DEC-31, DEC-15 | TC-13, DQ-08, DQ-27 |
| **FR-008** | Con un `DELAY` relevante validado se llama `get_policy_rules("DELAY")` (FR-068) y se evalúan **todas** las reglas; la vista muestra las que se cumplen y las que no, con los valores usados. Política **vacía**, una regla cumplida cuyo campo `requires_human_approval` falta o no es booleano, ⇒ decisión **BLOQUEADA** (se asume que exige aprobación), sin opciones por política y con caso humano ofrecido; un **fallo de lectura** del contexto o de los eventos no produce decisión (`decision_state` nulo, FR-105); un fallo de lectura de la política o de las opciones deja la decisión BLOQUEADA con soporte ofrecido (FR-105). | DEC-02, DEC-12 | REQ-F-19, DAT-46 |
| **FR-009** | `get_eligible_options` solo se invoca **después** de evaluar la política (cadena secuencial: contexto → eventos → política → opciones); con eso se arma la vista. | DEC-02 | REQ-F-05 |
| **FR-019** | **Segmentos afectados:** se evalúa cada segmento con `DELAY` relevante. Si hay **más de uno**, v1 no decide: se muestra el contexto, se informa y se ofrece caso humano `MULTIPLE_AFFECTED_SEGMENTS` (limitación declarada). Con uno solo, todas las variables se calculan sobre ese segmento y su conexión con el siguiente. | DEC-31 | DAT-82, GAP-07 |

### 3.2 Validación de eventos y frescura

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-010** | Un evento cuya `source` está en `_meta.sources_degraded` no es evidencia: se excluye y se registra la razón `SOURCE_DEGRADED`. | DEC-09, DEC-06 | REQ-F-15, REQ-F-21, DQ-12, TC-02 |
| **FR-011** | Los eventos se ordenan por `recorded_at` (UTC), **nunca** por `event_id`. | DEC-09 | DQ-11, DAT-15 |
| **FR-012** | **Precedencia (orden fijo):** (1) se excluyen eventos degradados e inválidos (FR-010, FR-015, FR-016); (2) con los restantes de un segmento se busca **conflicto** (FR-013: empate de `recorded_at`); (3) sin conflicto, por segmento y atributo —salida (`DELAY`, `STATUS`) y puerta (`GATE_CHANGE`)— **gana el `recorded_at` más reciente entre los eventos sanos**. Un `STATUS` sano (`SCHEDULED` —vuelta al horario programado— u `ON_TIME`) **más reciente** que un `DELAY` **lo reemplaza** (un vuelo puede recuperar tiempo, p. ej. por el viento); si es más antiguo, el `DELAY` se mantiene; un evento degradado nunca reemplaza ni borra. Un empate de `recorded_at` con valores incompatibles es conflicto. | DEC-09 | REQ-F-15, AMB-05 |
| **FR-013** | **Conflicto:** dos eventos **no degradados** del mismo segmento con el **mismo `recorded_at`** y afirmaciones incompatibles sobre la salida (`DELAY` > 0 = «retrasado»; `STATUS: ON_TIME` = «a tiempo»; `STATUS: SCHEDULED` = «horario programado»; tabla configurable). Con distinto `recorded_at` no hay conflicto: gana el más reciente (FR-012). No se afirma estado: aviso neutro y botón de caso humano `SOURCE_CONFLICT`. Dos `DELAY` compatibles (100 → 160) **no** son conflicto: gana el más reciente. | DEC-09, DEC-15 | TC-03, DQ-13 |
| **FR-014** | Si un segmento solo tiene evidencia **degradada**, el estado se muestra como «sin información verificada» (**nunca** «a tiempo»), sin alerta ni botón (no hay un problema que atender). Si no tiene **ningún** evento, o solo eventos que no informan la salida (p. ej. `GATE_CHANGE`), se muestra su horario programado del contexto, sin afirmar estado ni alertar. | DEC-09 | TC-02, TC-19, DQ-13 |
| **FR-015** | Un `DELAY` incoherente (`scheduled_departure + delay_minutes ≠ new_departure`) se descarta como evidencia (razón `INCONSISTENT_DELAY`) y se ofrece caso humano. | DEC-12 | DQ-09 |
| **FR-016** | Se descartan eventos con `segment_id` no solicitado (`UNKNOWN_SEGMENT`) y eventos con `recorded_at` posterior a `retrieved_at` + `CLOCK_SKEW_SECONDS` (60) (`FUTURE_TIMESTAMP`). | DEC-09 | DQ-07, DQ-10 |
| **FR-017** | Siempre se usa el dato más reciente y se respeta el TTL. **Vigencia de las opciones** = `get_eligible_options._meta.retrieved_at + ttl_seconds`; en el instante exacto **ya está vencida**; sin `ttl_seconds` el conjunto se considera vencido. Los eventos no tienen vencimiento propio (`EVENT_MAX_AGE_SECONDS`, por defecto sin límite). Al vencer se re-consulta **una vez por acción**; si devuelve lo mismo no se reintenta en bucle. | DEC-10 `PROV` | REQ-F-21, REQ-F-25, DQ-14, DQ-15 |
| **FR-018** | Las edades de datos se calculan en UTC (`ahora − recorded_at/retrieved_at`). | DEC-08 | REQ-F-21, DAT-05 |

### 3.3 Variables derivadas

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-020** | `delay_minutes` = retraso de **salida** del evento resuelto del segmento afectado, solo si no es degradado. | DEC-06 | DAT-19, DAT-54 |
| **FR-021** | `new_arrival` = llegada programada + `delay_minutes` (el retraso no se recupera), con fecha completa: la fecha de la llegada programada es la de salida y **+1 día si su hora es menor que la de salida**; la suma cruza medianoche en aritmética módulo 24 h con fecha. Etiquetada **DERIVADA/ESTIMADA**. | DEC-06, DEC-08 | TC-18, DQ-30, DAT-75 |
| **FR-022** | `margen = scheduled_departure(Si+1) − new_arrival(Si)` (horas locales del **mismo** aeropuerto, con fecha). Si el segmento afectado es el **último**, no hay conexión: `missed_connection` = **falso**. `mct_provided` es un indicador explícito (distinto de un MCT = 0 real). `missed_connection` = **verdadero** si `margen < MCT`; **desconocido** si el MCT no fue provisto y `0 ≤ margen < MCT_UNCERTAINTY_MINUTES` (45); **falso** en el resto. Siempre **ESTIMADA**. | DEC-07, DEC-08 | TC-06, GAP-11, DAT-75, H-13 |
| **FR-023** | El MCT es dato requerido: `MIN_CONNECTION_MINUTES` por aeropuerto (0 por defecto, rotulado «supuesto, no provisto»). Con MCT no provisto, **un «falso» nunca se afirma en el rango incierto** (FR-022): R3 queda indeterminada y se ofrece caso humano. La conexión perdida nunca se presenta como hecho. Un «falso» con MCT no provisto se rotula «ESTIMADA, sujeta a MCT» y la interfaz nunca dice «tu conexión está segura» (H-13). Supuestos registrados con la variable: **A1** el retraso se propaga íntegro, **A2** MCT no provisto, **A3** el segmento siguiente no se retiene. Queda en la lista de datos a solicitar. | DEC-07 | GAP-11, H-08 |
| **FR-024** | `group_includes_minor` = verdadero si algún pasajero tiene `type == CHILD`; falso solo si **todos** son `ADULT`; cualquier otro tipo o tipo ausente (p. ej. `INFANT`) ⇒ **desconocido**, y un desconocido se trata como **posible menor**: si hay política rota (FR-039) pasa a **validación manual** (FR-033, FR-038) **aunque la política no traiga una regla como R5**; sin política rota solo se informa. | DEC-32 | REQ-F-14, DAT-03 |
| **FR-025** | `compensation_requested` es `false` por defecto; solo es `true` si el pasajero lo solicita explícitamente. | DEC-29 | TC-17, GAP-05 |
| **FR-026** | `international` = país de origen ≠ país de destino del segmento, según la tabla de referencia versionada; aeropuerto desconocido ⇒ variable **desconocida**. | DEC-08 | DAT-76 |
| **FR-027** | Tabla de referencia versionada mínima IATA→{país, zona horaria}: `SCL`, `LIM`, `MEX`. Solo se usa para `international` y conversiones. | DEC-08 | GAP-15 |
| **FR-028** | Toda variable derivada se registra con valor, origen (`DATO`/`DERIVADA`) y supuestos. | DEC-12, DEC-23 | REQ-F-28, DAT-76 |
| **FR-029** | `overnight_required` = la salida de la opción propuesta cae en una fecha local posterior a la de `new_arrival(Si)` del segmento con conexión perdida; sin conexión perdida —o con `missed_connection` desconocido— no se deriva (la decisión ya es BLOQUEADA por FR-033/FR-038). Activa el aviso de asistencia (FR-058) y **ofrece** el caso humano `OVERNIGHT_ASSISTANCE`. | DEC-27, DEC-15 | GAP-03, DAT-39 |

### 3.4 Motor de reglas

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-030** | Parser acotado con lista blanca: identificadores `delay_minutes`, `international`, `missed_connection`, `compensation_requested`, `group_includes_minor`; operadores `>=`, `>`, `<`, `<=`, `==`, `EQ`, `!=`, `NE`, `AND`, `OR`; literales entero y `true`/`false`; paréntesis. `EQ` ≡ `==` y `NE` ≡ `!=` (ambos válidos); `AND` precede a `OR`; comparar booleano con entero, o usar `>`/`<` sobre un booleano, es `RULE_ERROR`; la condición mide ≤ 200 caracteres y ≤ 10 niveles de anidación. Todo lo demás es error. | DEC-12 | REQ-F-19, GAP-18, DQ-20 |
| **FR-031** | Prohibido `eval`/`exec` o acceso a atributos al evaluar `condition`. | DEC-12 | REQ-F-19 |
| **FR-032** | **Error de expresión** (sintaxis o identificador fuera de la lista blanca) ⇒ `RULE_ERROR`: toda la evaluación es indeterminada, no se ofrecen opciones por política y se ofrece caso humano `BLOCKING_PARTIAL_DATA`. | DEC-12, DEC-15 | DQ-20 |
| **FR-033** | **Valor desconocido** (variable válida sin valor resoluble) ⇒ lógica trivaluada de Kleene (`false AND desconocido = falso`; `true OR desconocido = verdadero`). Una regla cuyo resultado sea desconocido se muestra «no evaluable» y **impide la aceptación automática** (la aceptación pasa por caso humano). Una regla «no evaluable» solo bloquea (FR-038) si sus derechos incluyen un derecho de remedio (FR-039) o si ya existe una política rota; una no evaluable sin derechos de remedio y sin política rota se ignora (p. ej. R5 desconocida con un retraso que no rompe ninguna política). | DEC-12 | DAT-48 |
| **FR-034** | Cada regla de la versión recuperada produce: cumple / no cumple / indeterminada, con las variables usadas. | DEC-02 | REQ-F-19 |
| **FR-035** | Precedencia: si **cualquier** regla cumplida exige aprobación humana (`requires_human_approval`), y existe **política rota** (FR-039), la decisión del caso es **PENDIENTE_APROBACION** (gana la más restrictiva); sin política rota (`INFORMATIVA`) una regla de aprobación no cambia el estado; lo determina la política. | DEC-13 | REQ-F-14, REQ-F-17, GAP-19, DAT-47 |
| **FR-036** | Se fijan en el registro la versión de política y los `rule_id` evaluados. | DEC-23 | DQ-21, REQ-F-28 |
| **FR-038** | **Bloqueo global por anomalía:** si en **cualquier** segmento existe `SOURCE_CONFLICT`, `UNSUPPORTED_EVENT_TYPE`, `INCONSISTENT_DELAY`, `MULTIPLE_AFFECTED_SEGMENTS`, `RULE_ERROR`, una regla «no evaluable» en los términos de FR-033 o una lectura íntegra inválida (FR-066), la decisión del caso es **BLOQUEADA**: ninguna regla cumplida habilita `create_rebooking_request`; aceptar una opción solo puede abrir caso humano (FR-052). | DEC-09, DEC-13, DEC-31 | REQ-F-14, REQ-F-17 |
| **FR-037** | El conjunto de derechos concedidos es la unión de los de las reglas cumplidas. Un derecho de código desconocido se **muestra por su código sin interpretarlo** y no habilita ninguna acción automática. (Distinto de FR-102: un **tipo de evento** u **opción** desconocido sí degrada a humano.) | DEC-13 | DAT-52, GAP-19 |
| **FR-039** | **Política rota:** hay al menos una regla **cumplida** cuyos derechos incluyen un **derecho de remedio** (`REMEDY_RIGHTS`, configurable; por defecto `REBOOK_NO_FEE`, `MEAL_VOUCHER`, `CASH_COMPENSATION`). Un retraso **sin política rota** deja la decisión en **`INFORMATIVA`**: se informa el retraso y se muestran las reglas evaluadas (las que se cumplen y las que no), **no se consulta `get_eligible_options`** y no hay opciones de rebooking, de compensación ni de soporte, ni notificación de política en modo `system` (el `GATE_CHANGE` sí se notifica, FR-122), hasta que exista una política rota. Los derechos que no son de remedio (p. ej. `PRIORITY_HANDLING` de R5) modifican el trato pero no rompen la política por sí solos. | DEC-02, DEC-05 | REQ-F-11, REQ-F-17 |

### 3.5 Opciones

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-040** | **Contrato efectivo v1:** la firma no cambia (`trip_context`), pero el contenido enviado es un **subconjunto** del esquema: sin correo, teléfono, documento, nombre ni nivel de fidelidad (el nombre de pila solo se muestra en pantalla, FR-003); `has_minor` booleano a nivel de grupo; pasajeros solo con `passenger_id` y `type`, sin edad. Los *mocks* aceptan el subconjunto. Se propone al equipo formalizar un contrato reducido. | DEC-22 | REQ-N-04, DAT-79 |
| **FR-041** | Una opción es **viable** si: (a) `seats_available` ≥ nº de pasajeros del grupo (todo el grupo junto); (b) **existe un derecho concedido que la respalda**: en v1 el único derecho de cambio es `REBOOK_NO_FEE` (supuesto S-10) y exige costo cero; sin ese derecho ninguna opción es viable; (c) su `policy_ref` coincide con una versión vigente recuperada y no superseded; (d) su tipo está soportado; (e) no está vencida (FR-017); (f) es **coherente con el itinerario** (invariante I-6 de `03_get_eligible_options`): **con `missed_connection` verdadero** su origen es el origen del segmento siguiente (la conexión), su destino es el destino final del itinerario y su salida es posterior a `new_arrival` + MCT; **sin conexión perdida** (p. ej. R1 concede el cambio, o el afectado es el último segmento) reemplaza al segmento afectado: mismo origen y destino que él y salida posterior a `retrieved_at`; con `missed_connection` **desconocido** no se puede verificar (f): ninguna opción es viable por itinerario incierto, la decisión es BLOQUEADA y se ofrece soporte. | DEC-17, DEC-16 | DQ-15..19, TC-09, TC-10 |
| **FR-042** | Las opciones no viables no se muestran; se registran con **todas** sus razones (p. ej. `INSUFFICIENT_SEATS` y `FEE_CONFLICT` a la vez). | DEC-17 | DAT-31, DAT-32 |
| **FR-043** | Si se excluyó una opción por no cubrir al grupo o dejar al menor solo, el mensaje lo dice explícitamente y remite a soporte. | DEC-16 | GAP-20, DAT-43 |
| **FR-044** | `confidence` solo ordena entre viables; nunca decide. | DEC-17 | DAT-36 |
| **FR-045** | La propuesta principal es la viable de mayor `confidence`; desempate por salida más temprana y luego `option_id`. Se presenta como **propuesta**. | DEC-17 | REQ-F-20 |
| **FR-046** | La vía de reembolso se menciona con una redacción **no afirmativa** («si prefieres no viajar, una persona puede revisar contigo las alternativas»): no afirma un derecho, por eso queda exenta de `policy_ref` (FR-081) y se verifica con un test (TC-11); `refundable:false` no se usa para negar. | DEC-17, DEC-28 | GAP-04, DAT-33 |
| **FR-047** | Sin opción viable ⇒ mensaje claro y caso humano ofrecido con razón `NO_OPTION_COVERS_GROUP` si la causa son cupos o separar al grupo, o `NO_VIABLE_OPTION` en otro caso (FR-063). | DEC-15 | TC-09 |
| **FR-048** | Opción con `fare_difference > 0` sin `currency` ⇒ no viable. | DEC-17 | DQ-18 |
| **FR-049** | Sin `change_penalty_amount` no se cotizan cambios voluntarios ni se afirma costo. | DEC-11 | DQ-28, TC-12 |

### 3.6 Acciones y casos humanos

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-050** | **Consentimiento:** toda **acción externa** (`create_rebooking_request`, `create_human_case`, `notify_passenger`) requiere un **clic explícito del pasajero**; el sistema solo propone y **ofrece**. La persistencia técnica interna (registro de decisión, registro de operaciones) no es una acción externa y no requiere clic. **Excepción:** con `caller = system` (FR-120) el sistema puede enviar `notify_passenger` **sin clic**, solo con la plantilla fija de FR-122; ninguna otra acción externa se ejecuta en modo `system`. Un clic autoriza exactamente: «Aceptar esta opción» ⇒ el rebooking **o**, si la decisión exige aprobación o es BLOQUEADA (FR-038), el caso humano con esa opción; «Hablar con una persona» ⇒ un caso humano. Los textos de los botones lo declaran, incluida la derivación posterior a un `503` persistente. | DEC-14 | REQ-F-13, REQ-F-17 |
| **FR-051** | Aceptar una opción cuando la decisión **no** exige aprobación: revalidar (FR-070) → llave idempotente → `create_rebooking_request`. | DEC-14, DEC-19 | REQ-F-17, TC-07 |
| **FR-052** | Aceptar una opción cuando la decisión exige aprobación (p. ej. R5), es BLOQUEADA (FR-038) o tiene reglas «no evaluables»: **no** se llama `create_rebooking_request`; se crea un caso humano con la opción elegida como evidencia. | DEC-13, DEC-16 | REQ-F-14, DAT-47 |
| **FR-053** | **Identidad de la operación** = (`booking_id`, itinerario de la opción). Al crearla se calcula la llave `HMAC-SHA256(IDEMPOTENCY_SECRET, JSON canónico de [booking_id, vuelo, fecha, salida, versión de política, generación])` (sin `decision_id`, decisión ni marcas de tiempo) y se guarda en un **registro de operaciones**, de forma atómica (unicidad) **antes** de llamar. Mientras la operación no esté en un estado final de fracaso, toda reevaluación **reutiliza su llave** aunque la versión de política haya cambiado. | DEC-18 | REQ-F-23, DQ-22 |
| **FR-062** | **Concurrencia y pendientes:** dos aceptaciones simultáneas, o una aceptación mientras la operación está `EN_CURSO`, `INDETERMINADA` o `CREADA`, resultan en **una sola** escritura; la segunda devuelve el estado de la primera. El botón se deshabilita mientras hay una solicitud en curso. | DEC-18 | REQ-F-23, DQ-23 |
| **FR-064** | **Ciclo de vida de la operación** (registro de operaciones): `EN_CURSO` → `CREADA` (201) · `INDETERMINADA` (503/timeout agotado) · `FALLIDA` (error no reintentable) · `EXPIRADA`. `EN_CURSO` pasa a `INDETERMINADA` tras `OPERATION_STALE_SECONDS` (120) sin respuesta (el proceso pudo caer); `CREADA` pasa a `EXPIRADA` en el `expires_at` devuelto; `INDETERMINADA` pasa a `EXPIRADA` tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` (900, mayor que la vigencia de una solicitud) si nada la resuelve. Si la llave **no pudo persistirse**, no se escribe (DQ-22). Una `EXPIRADA` o `FALLIDA` permite una nueva operación con llave de **generación** siguiente; `CREADA`, `EN_CURSO` e `INDETERMINADA` la bloquean y la vista muestra su estado. Un `409` sin operación local se muestra «ya existe una solicitud para esta opción». | DEC-18 | REQ-F-23, REQ-F-24, DQ-22, DQ-23 |
| **FR-065** | **Contrato efectivo de `create_rebooking_request` en v1:** además de `(option, idempotency_key)` se envían `booking_id` e ids de pasajeros (extensión documentada en DOC-013; los *mocks* la aceptan y verifican que cubre a todo el grupo). El cliente **nunca** aporta el contenido de la opción: envía `decision_id` + clave de itinerario y el servidor la resuelve con las opciones recién consultadas. | DEC-18, DEC-16 | DAT-62, REQ-C-05 |
| **FR-066** | **Integridad de lecturas** (DQ-01…06): `_meta.retrieved_at` presente y UTC; ≥ 1 segmento y ≥ 1 pasajero; segmentos ordenados por (fecha, `scheduled_departure`) y encadenados (`destino[i] == origen[i+1]`, DQ-03: si se rompe, no se deriva conexión y se bloquea); horas `HH:MM` y fechas ISO; `CHILD` con `age`; menor sin adulto en la reserva ⇒ `BLOCKING_PARTIAL_DATA`. En `DELAY`, `delay_minutes` es entero ≥ 1 y `new_departure` está presente; un `DELAY` ≤ 0 es `INCONSISTENT_DELAY` (en realidad sería un adelanto, DEC-31). **Resultados:** `retrieved_at` ausente, 0 segmentos, 0 pasajeros o formato inválido ⇒ **lectura fallida** (FR-105: sin decisión, aviso y reintento); cadena rota o menor sin adulto ⇒ `missed_connection` **desconocido**, decisión **BLOQUEADA** y `BLOCKING_PARTIAL_DATA`; segmentos desordenados ⇒ se reordenan, sin bloqueo. | DEC-12, DEC-31 | DQ-01…06, DQ-09 |
| **FR-054** | Resultado **indeterminado** = `503 UPSTREAM_TIMEOUT`, timeout de transporte o respuesta perdida tras enviar ⇒ hasta 2 reintentos con la **misma** llave; luego caso humano (cubierto por el clic de FR-050). Nunca se informa éxito ni fracaso. | DEC-18 | REQ-F-24, TC-14 |
| **FR-055** | `409 DUPLICATE_REQUEST` ⇒ se trata como solicitud existente; la vista muestra «ya existe una solicitud en curso para esta opción»; sin bucles. | DEC-18 | REQ-F-24, TC-15, DQ-23 |
| **FR-056** | `201 PENDING_CONFIRMATION` ⇒ «solicitud registrada, pendiente de confirmación, sujeta a disponibilidad» con `expires_at`. La confirmación queda fuera de v1 (supuesto documentado). | DEC-18, DEC-19 | GAP-12, DAT-61 |
| **FR-057** | Disparadores de caso humano (códigos): `COMPENSATION_REQUESTED`, `BLOCKING_PARTIAL_DATA`, `SOURCE_CONFLICT`, `UPSTREAM_INDETERMINATE`, `UNSUPPORTED_EVENT_TYPE`, `NO_OPTION_COVERS_GROUP`, `OVERNIGHT_ASSISTANCE`, `PERSONAL_DATA_REQUEST`, `POLICY_APPROVAL_REQUIRED`, `MULTIPLE_AFFECTED_SEGMENTS`, `INCONSISTENT_DELAY`, `NO_VIABLE_OPTION`, `OTHER_HELP`. Prioridad en FR-063. En la vista, el sistema los **ofrece**; el caso se crea con el clic (FR-050). | DEC-15, DEC-13, DEC-27 | REQ-F-14, REQ-F-26, GAP-26 |
| **FR-063** | **Causa → motivo y prioridad** (de mayor a menor; el `reason` del caso es el primero que aplique y `evidence.reasons` conserva todos): (1) `UPSTREAM_INDETERMINATE` (503/timeout persistente); (2) `SOURCE_CONFLICT`; (3) `UNSUPPORTED_EVENT_TYPE`; (4) `INCONSISTENT_DELAY`; (5) `MULTIPLE_AFFECTED_SEGMENTS`; (6) `BLOCKING_PARTIAL_DATA` (política vacía, fallo de lectura, `RULE_ERROR`, regla «no evaluable», `missed_connection` desconocido, cadena de segmentos rota, menor sin adulto); (7) `COMPENSATION_REQUESTED`; (8) `PERSONAL_DATA_REQUEST`; (9) `POLICY_APPROVAL_REQUIRED`; (10) `NO_OPTION_COVERS_GROUP` (exclusión por cupos o por separar al grupo); (11) `NO_VIABLE_OPTION` (sin derecho que respalde una opción, o ninguna vigente); (12) `OVERNIGHT_ASSISTANCE`; (13) `OTHER_HELP`. | DEC-15 | REQ-F-14, REQ-F-26 |
| **FR-058** | Pernocte (FR-029) ⇒ el mensaje dice «podrías tener derecho a asistencia; un agente lo confirmará», sin cifras. | DEC-27 | REQ-F-18, GAP-03 |
| **FR-059** | `create_human_case(reason, evidence)`: `reason` = el motivo de mayor prioridad (FR-063); `evidence.reasons` conserva **todos** los motivos simultáneos; `evidence` solo con ids, enumeraciones y hechos validados (versión de política, `decision_id`, opción), sin PII; se toma de la **decisión guardada** si la petición trae `decision_id` (lo que el pasajero vio) y, si no, de una evaluación fresca en el instante del clic. Deduplicación por `SHA-256(booking_id ‖ motivos ordenados ‖ huella de decisión)`. La deduplicación es **local** y no bloquea el reintento explícito cuando el intento previo fue `FALLIDO` o `INDETERMINADO` (FR-105) (la tool no ofrece llave: un duplicado externo solo se evita impidiendo el reenvío automático y registrando cada intento y su resultado `CREADO`/`FALLIDO`/`INDETERMINADO` en el registro de casos). No requiere revalidación (lleva una *instantánea* con sus `retrieved_at`). | DEC-15, DEC-23 | REQ-F-26, DAT-64, GAP-26 |
| **FR-060** | Botón neutro «Hablar con una persona», **solo cuando hay una acción posible** (decisión distinta de `INFORMATIVA` con política rota, FR-039, o anomalía que exige validación manual), con un **motivo de enumeración cerrada**: `OTHER_HELP`, `PERSONAL_DATA_REQUEST` y, **solo si hay compensación elegible** (FR-067), `COMPENSATION_REQUESTED`. Rótulos neutros, sin resaltar ni preseleccionar: «Necesito ayuda con mi vuelo», «Necesito ayuda con mis datos o documentos», «Tengo una consulta sobre compensaciones» (un test recorre el catálogo, FR-113); **no existe texto libre** (DEC-02; FR-091). Compensación nunca proactiva ni con montos; `COMPENSATION_REQUESTED` fija `compensation_requested` y abre caso humano al hacer clic. | DEC-29 | REQ-F-17, TC-17 |
| **FR-061** | El motivo `PERSONAL_DATA_REQUEST` («necesito datos personales o mis documentos») nunca devuelve PII: abre caso humano y la respuesta no contiene ningún campo de la lista prohibida. | DEC-15, DEC-22 | TC-20, DQ-26 |
| **FR-067** | **Compensación elegible:** el motivo de compensación del menú de soporte solo se muestra si la política recuperada tiene una regla que concede un derecho de compensación (`COMPENSATION_RIGHTS`, configurable; por defecto `CASH_COMPENSATION`) que, evaluada con `compensation_requested = true` y las demás variables ya calculadas, resulta verdadera, y la decisión no es `INFORMATIVA`. En otro caso el menú no la ofrece. | DEC-29 | GAP-05, TC-17 |
| **FR-068** | **Contexto completo y política solo para `DELAY`:** la evaluación considera todos los eventos validados de todos los segmentos (retraso, puerta, estado) en conjunto y la vista los muestra todos. En la Fase 1 **solo `DELAY` consulta `get_policy_rules`** (`POLICY_SCENARIOS`, configurable, por defecto `DELAY`→`DELAY`); `GATE_CHANGE` **no** consulta política: solo se informa (usuario) o se notifica (sistema). Los tipos admitidos son `SUPPORTED_EVENT_TYPES` (por defecto `DELAY`, `GATE_CHANGE`, `STATUS`); uno fuera de la lista no se interpreta (FR-007: no se tiene información sobre otros). Un viaje solo con `GATE_CHANGE` queda `INFORMATIVA`. En la Fase 2 se podrán añadir escenarios a `POLICY_SCENARIOS`. | Usuario (2026-10-19) | REQ-F-02, REQ-F-19, GAP-07 |

### 3.7 Revalidación y vigencias

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-070** | Antes de un **rebooking** se reconsultan el **contexto del viaje** (pasajeros, tipos, segmentos), los eventos, las opciones y la política y se recalcula la decisión. Se calcula una **huella de decisión** (hash de: estado resuelto de cada segmento —tipo, `delay_minutes`, `new_departure`—, reglas cumplidas, derechos, aprobación, versión de política, composición del grupo y, de la opción elegida, su **itinerario** —vuelo, fecha, origen, destino, salida— más el booleano «`seats_available` ≥ nº de pasajeros», `fare_difference` y `policy_ref`). Si la huella difiere de la mostrada, **no se escribe** y se muestra el nuevo estado; marcas de tiempo, ids de eventos descartados, `option_id` y `confidence` no cuentan. **La vigencia no entra en la huella:** es una condición de ejecución independiente (la opción re-consultada debe estar vigente en el instante de escribir, FR-017). Los **casos humanos** no se revalidan (FR-059). | DEC-19 | REQ-F-25, DAT-77 |
| **FR-071** | La vista muestra la hora límite `min(expiración de las opciones mostradas)` para aceptar, en UTC y como cuenta regresiva; pasada esa hora, «sujeto a disponibilidad». | DEC-19 | REQ-F-25, GAP-25 |
| **FR-072** | Opciones vencidas al usarlas ⇒ se refrescan antes de escribir. | DEC-10, DEC-19 | TC-08, DQ-15 |

### 3.8 Mensajes

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-080** | Los mensajes salen de plantillas determinísticas; cada afirmación dinámica referencia su evidencia. Español neutro sin localización (nota obligatoria). | DEC-02, DEC-36 | REQ-F-03, REQ-F-16 |
| **FR-081** | Validador propio, aplicado a **todo mensaje dinámico antes de devolverlo por la API** (y al contrato de `notify_passenger`): bloquea un hecho sin evidencia vigente o un campo fuera de la lista blanca; exige `policy_ref` a los mensajes que afirman una **opción o un derecho** y en toda notificación de política (FR-122, caso a; TC-16); el aviso informativo de `GATE_CHANGE` va sin `policy_ref` (H-21). Los textos estáticos de la interfaz quedan exentos. | DEC-20 `PROV` | REQ-F-29, TC-16, DQ-25 |
| **FR-082** | Contenido mínimo: qué cambió (con la hora de la información), qué implica, siguiente paso, aviso de estimación y vía humana; `policy_ref` solo cuando el mensaje afirma una opción o un derecho (FR-081). Sin plazos legales ni derechos de normas externas. | DEC-33 | REQ-F-03, REQ-F-16 |
| **FR-083** | Nunca se afirma: «tu conexión está segura» o «llegarás a tiempo», hora de llegada al destino final, retención de un segmento posterior, hotel/comidas, montos, causa, «ya está cambiado». | DEC-30, DEC-27 | REQ-F-30h, DQ-29 |
| **FR-084** | Sin campo de causa: mensaje neutro; no se afirman ni niegan derechos que dependan de la causa. | DEC-30 | GAP-06, DQ-29 |
| **FR-085** | `notify_passenger` se invoca **solo** en modo `system` (FR-122) con una plantilla fija; en modo `user` no se invoca (el mensaje se ve en la pantalla). Se activa con `NOTIFY_ENABLED` (configuración). | DEC-20 (notas de 2026-10-19) | GAP-13, DAT-65 |
| **FR-086** | `completeness: PARTIAL` es información de contexto: solo bloquea si falta un campo necesario para decidir. Una lectura fallida o inválida (FR-066, FR-105) da aviso y reintento, **sin soporte**; el caso humano `BLOCKING_PARTIAL_DATA` solo se ofrece si la decisión queda BLOQUEADA por una anomalía que exige validación manual (p. ej. cadena de segmentos rota, menor sin adulto, regla no evaluable con política rota). | DEC-11 | REQ-F-22, TC-12 |

### 3.9 Trazabilidad y auditoría

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-090** | Cada evaluación genera un registro con `decision_id`, `booking_id`, lecturas con `retrieved_at`, eventos elegidos y descartados con razón, versión de política y reglas, variables derivadas con supuestos, opciones viables y descartadas con razón, acción, y hash del mensaje. | DEC-23 | REQ-F-28, REQ-N-08, DAT-80 |
| **FR-091** | **Campos persistibles (lista cerrada):** **hechos operacionales no personales** (número de vuelo, fecha, origen, destino, hora de salida, códigos de aeropuerto), identificadores seudónimos (`decision_id`, `booking_id`, `passenger_id`, `segment_id`, `option_id`, `event_id`, `rule_id`, `case_id`, `request_id`, `notification_id`), enumeraciones, números, marcas de tiempo y hashes. **Nunca** se guardan payloads completos, nombre, contacto, documento ni edad del menor. Los identificadores se consideran **seudónimos, no anónimos**. `booking_id` truncado en los logs de aplicación. | DEC-23 | REQ-N-04, DQ-26 |
| **FR-092** | Retención provisional `PROV`: `AUDIT_RETENTION_DAYS` = 30 con una rutina de purga verificable **del registro de decisiones, del de operaciones/casos y del de notificaciones**, que **primero aplica los vencimientos de FR-064** y después conserva el registro mínimo solo de las operaciones que siguen **no finalizadas** (`EN_CURSO`, `INDETERMINADA` o `CREADA` dentro de su vigencia) para no perder su bloqueo; una operación ya vencida se purga por antigüedad como cualquier otra (FR-064); el valor definitivo queda por decidir. | DEC-23 | GAP-27 |
| **FR-093** | Endpoint de lectura del registro por `decision_id`, sujeto a FR-001 (solo la reserva dueña de la sesión); la sesión del pasajero **no** recibe `needs_manual_review` ni el detalle de las notificaciones (campos internos, FR-123). | DEC-23 | REQ-E-05 |

### 3.10 Interfaces y front de prueba

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-100** | Puertos (interfaces) para las 7 tools con los contratos del PDF; adaptadores *mock* intercambiables por uno HTTP real (pendiente de la documentación de endpoints). | DEC-04 | REQ-F-27, REQ-C-01…07 |
| **FR-101** | La fuente de verdad es el universo del PDF (los datos personales de los ejemplos se sustituyen por valores claramente ficticios; un test verifica que no aparecen en logs ni en el registro): tipos de evento `DELAY`, `GATE_CHANGE`, `STATUS`; los escenarios de prueba reproducen los 7 ejemplos (tal cual, salvo los datos personales) y las variantes TC. | DEC-04 | DAT-82, REQ-C-08 |
| **FR-102** | Las enumeraciones abiertas se toleran: un valor nuevo degrada a humano. | DEC-31 | DQ-27 |
| **FR-103** | Los *mocks* respetan `_meta` y los errores `409`, `503`, `422`. | DEC-04 | REQ-F-27 |
| **FR-105** | **Matriz de errores por tool.** Lecturas con timeout, `5xx` o `422`: sin reintento en bucle (una re-consulta); `get_trip_context` falla ⇒ pantalla «no pudimos cargar tu viaje» con reintento; solo `get_operational_events` falla ⇒ se muestra el contexto, sin estado ni alerta, con aviso; `get_policy_rules` o `get_eligible_options` fallan ⇒ sin opciones y caso humano ofrecido. `create_rebooking_request` `422`/error no reintentable ⇒ no se reintenta, mensaje genérico de fallo y caso humano ofrecido. `create_human_case`: un error explícito (4xx/5xx con respuesta) ⇒ «no pudimos registrar tu solicitud, puedes reintentar»; un **timeout o respuesta perdida** es **indeterminado** (la tool no tiene llave idempotente): se muestra «no pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté», **no se reenvía automáticamente**, y el reintento exige un segundo clic explícito tras advertir del posible duplicado (cuerpo `confirm_possible_duplicate: true`; sin él, `409 NEEDS_CONFIRMATION`). Nunca se afirma éxito. | DEC-18, DEC-15 | REQ-F-24, REQ-E-02 |
| **FR-110** | API HTTP (FastAPI): evaluación de un viaje con `booking_id` y `caller` (FR-120), vista de viaje, aceptar opción, caso humano, registro de decisión, `GET /ping` → `pong`. | DEC-04 | REQ-F-07 |
| **FR-111** | Front React de prueba con el *look & feel* del centro de ayuda de la aerolínea (sin logos ni marcas), verificable con la **lista de componentes** de `DESIGN_CONTRACT.md` y su *checklist* de tokens: selector de escenario; contexto; alerta; reglas cumplidas y no cumplidas; opción propuesta; vía de reembolso; avisos de estimación, hora límite y «sujeto a disponibilidad»; botones de acción. | DEC-04 | REQ-F-08, REQ-F-09 |
| **FR-112** | La interfaz no muestra PII salvo la **excepción autorizada** de FR-003 (nombre de pila) ni identificadores internos innecesarios. Lista blanca cerrada de campos. | DEC-21 | REQ-F-12, REQ-N-04 |
| **FR-113** | Todo el texto visible está en español neutro y sale del catálogo de plantillas: **ninguna cadena visible fuera del catálogo** (verificado por un test que recorre los componentes). | DEC-36 | REQ-F-03 |
| **FR-114** | **Separación entre Vista del Pasajero y Panel Gris de Soporte/Debug Operacional:** la interfaz separa en la parte superior la vista limpia y amable para el cliente (saludo `Hola, {nombre}`, aviso comprensible como «Tienes una sugerencia pendiente de aprobación», sección «Estado de tu viaje», mensajes sin prefijos `[INFO]`/`[ESTIMATE]`/`[NEXT_STEP]` ni códigos `POL-DELAY-*`, conexión comprometida destacada como «Observación: ...», propuesta «Te proponemos: Cambiar tu vuelo a ...», nota de validación por agente y botón «Aceptar opción y contactar a un agente de soporte» o «Contactar a un ejecutivo») y en la parte inferior un contenedor gris de soporte/debug con `completeness: PARTIAL`, `decision_id`, reglas activadas `R1..R5`, `POL-DELAY-2026-03`, opciones descartadas (`O2`, `O3`) y el JSON completo. | Usuario (2026-10-19) | REQ-F-09, AMB-02 |

### 3.11 Listas cerradas (DEC-21)

- **Campos visibles al pasajero (lista blanca):** segmentos (origen, destino, fecha, hora programada, hora nueva, puerta, estado), nombre de pila, número de pasajeros, opciones viables (vuelo, fecha, salida, costo), derechos citados con su `policy_ref`, reglas evaluadas con sus variables, plazos y avisos, el código de la propia reserva, la referencia de la solicitud (`request_id`) o del caso (`case_id`) recién creados, y el aviso «tu grupo incluye a un menor» (booleano de grupo, sin edad).
- **Campos prohibidos (nunca en pantalla, logs, registro ni modelos):** documento de identidad, correo, teléfono, nivel de fidelidad, nombre completo, edad del menor, apellidos.

### 3.12 Invocación por el sistema (`caller`)

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **FR-120** | **Parámetro `caller`** (obligatorio, `user` o `system`) junto al `booking_id`: la misma evaluación (FR-002…FR-009, FR-039) puede pedirla el pasajero o *otro sistema*. `user` exige sesión del pasajero (FR-001). `system` exige una credencial de servicio (`X-Service-Key` contra `SERVICE_API_KEY`, apagada por defecto) y **nunca** recibe PII ni la vista completa: recibe `decision_id`, `decision_state`, el `reason` del cambio, el estado de la notificación y `needs_manual_review`. | Usuario (2026-10-19) | REQ-F-04, GAP-13 |
| **FR-121** | En modo `system` no se ejecuta ninguna acción del pasajero (ni `create_rebooking_request` ni `create_human_case`); la única acción externa permitida es la notificación de FR-122. | Usuario (2026-10-19) | REQ-F-17 |
| **FR-122** | **Notificación del sistema:** con `caller = system` se envía `notify_passenger` con la plantilla fija «Hubo un cambio en tu vuelo asociado a {reason}. Revisa tu reserva en la web o en la aplicación.» en dos casos: **(a)** la decisión tiene **política rota** (FR-039), con `{reason}` = `DELAY` («un retraso») y el `policy_ref` evaluado; **(b)** hay un `GATE_CHANGE` **validado**, con `{reason}` = `GATE_CHANGE` («un cambio de puerta»), **sin consultar política** (FR-068) y sin `policy_ref` (aviso informativo, H-21). `{reason}` es una enumeración cerrada y se envía una notificación por motivo. El `booking_id` es el destinatario y el aviso se dirige al **titular adulto** de la reserva, nunca al menor (extensión de contrato, DOC-013); si la reserva no tiene titular adulto, **no se envía** (`NOT_SENT / NO_ADULT_RECIPIENT`) y se marca `needs_manual_review`. **El mensaje no contiene URL, enlace, teléfono ni dato de contacto** (anti-*phishing*): se invita al pasajero a entrar por sus canales habituales. El validador (FR-081) bloquea cualquier URL o dato de contacto. | Usuario (2026-10-19) | REQ-F-16, GAP-13, DAT-65 |
| **FR-123** | La notificación es **idempotente**: no se reenvía la misma (reserva + motivo + huella del motivo + plantilla) dentro de `NOTIFY_COOLDOWN_SECONDS` (configurable); `202` ⇒ `QUEUED`; `422` o error explícito ⇒ `FALLIDA`; timeout o respuesta perdida ⇒ `INDETERMINADA`, con hasta `NOTIFY_MAX_RETRIES` reintentos con la misma clave y sin afirmar éxito. La huella del motivo `GATE_CHANGE` incluye la **puerta validada de cada segmento**, de modo que un cambio posterior de puerta genera un aviso nuevo; la del motivo `DELAY` es la versión de política más las reglas disparadas (un cambio solo de minutos no repite el aviso). **Sin política rota y sin `GATE_CHANGE` validado no se notifica**: esto incluye las anomalías que impiden evaluar la política (conflicto de fuentes, tipo de evento desconocido, lectura fallida), que se registran con `needs_manual_review` en la auditoría (alerta interna en Fase 2). **Con política rota se notifica aunque la decisión sea BLOQUEADA o PENDIENTE_APROBACION** (p. ej. menor desconocido, reglas no evaluables): el problema para el pasajero existe y la validación manual es otra vía. | Usuario (2026-10-19) | DQ-22, DQ-23 |
| **FR-124** | La respuesta del modo `system` **no se guarda** para el front en v1 (Fase 2); cuando el pasajero entra, el modo `user` vuelve a consultar siempre (FR-002). | Usuario (2026-10-19) | GAP-22 |

## 4. Requisitos no funcionales (`NFR`)

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **NFR-001** | **Determinismo:** con el mismo reloj inyectado (puerto `Clock`) y las mismas lecturas, la misma huella de decisión y los mismos mensajes; sin IA ni modelos en runtime; costo por interacción en modelos = 0. | DEC-02 | REQ-F-10, REQ-N-06 |
| **NFR-002** | **Privacidad:** minimización en todas las fronteras propias; ningún dato personal a un modelo (si en el futuro se usara, se anonimiza antes). | DEC-22 | REQ-N-04, DAT-79 |
| **NFR-003** | **Seguridad:** parser sin ejecución dinámica; validación estricta de entradas; CORS acotado al front; sin secretos en el repositorio. | DEC-12 | REQ-E-04 |
| **NFR-004** | **Latencia:** presupuesto declarado: la vista responde < 1,5 s (p95) con *upstreams* simulados de 100 ms fijos. **Protocolo de aceptación:** 50 solicitudes secuenciales del caso base en la máquina de desarrollo; se reporta p50/p95. Cadena de lecturas **secuencial**: `get_trip_context` → `get_operational_events` → (solo si hay un evento relevante validado) `get_policy_rules` → `get_eligible_options`; con eso se muestra la vista (presupuesto: 4 × 100 ms + proceso). | DEC-24 | REQ-N-06 |
| **NFR-005** | **Operabilidad:** configuración por variables de entorno, logs estructurados sin PII, runbook de una página; lo opera un equipo pequeño. | DEC-24 | REQ-N-05 |
| **NFR-006** | **Calidad:** los TC-01 a TC-20 **y los añadidos TC-21 en adelante** automatizados; el caso base como prueba e2e; cobertura de líneas del dominio ≥ 85 %. | DEC-24, DEC-04 | REQ-D-05, REQ-E-04 |
| **NFR-007** | **Estilo SDD-WORKFLOW:** TDD con revisión WTF, funciones ≤ 10 líneas y ≤ 3 parámetros (verificado por un test que mide el código), lógica de negocio independiente de la tecnología (puertos/adaptadores). | DEC-03 | REQ-E-04 |
| **NFR-008** | **Métrica de éxito propuesta:** % de sesiones con problema donde el pasajero ve una opción viable y la acepta sin contacto humano; tasa de casos humanos por razón; 0 afirmaciones sin evidencia. Instrumentadas desde el registro de decisión. | DEC-24 | REQ-N-09, GAP-23 |
| **NFR-009** | **Portabilidad:** corre sin Docker (venv + npm); Docker Compose opcional. | DEC-03 | REQ-D-03 |
| **NFR-010** | **Confidencialidad:** el repositorio no incluye el PDF y no se publica sin autorización expresa del usuario (no es la opción «b» de DEC-37, que no elegiste: es la consecuencia de `REQ-N-10`); los *fixtures* usan datos personales ficticios; todo envío a un servicio externo se anota en la bitácora de IA. | DEC-37 | REQ-N-10, REQ-P-12 |
| **NFR-011** | **Accesibilidad básica:** roles semánticos, foco visible, navegación por teclado y contraste AA (relación ≥ 4,5:1 verificada sobre los tokens por un test que calcula el contraste). | DEC-04 | REQ-E-04 |
| **NFR-012** | **Configuración:** todos los parámetros de los supuestos S-09…S-19 son **variables configurables** (archivo de configuración con sobrescritura por entorno, validadas al arrancar, valor por defecto documentado) y ninguno está fijado en la lógica: `RELEVANT_DELAY_MIN_MINUTES`=1, `MIN_CONNECTION_MINUTES` (por aeropuerto)=0, `MCT_UNCERTAINTY_MINUTES`=45, `CLOCK_SKEW_SECONDS`=60, `EVENT_MAX_AGE_SECONDS`=sin límite, `OPERATION_STALE_SECONDS`=120, `REBOOK_MAX_RETRIES`=2, `AUDIT_RETENTION_DAYS`=30, `PARSER_MAX_CONDITION_CHARS`=200, `PARSER_MAX_DEPTH`=10, `REMEDY_RIGHTS`, `COMPENSATION_RIGHTS`, `NOTIFY_ENABLED`, `NOTIFY_COOLDOWN_SECONDS`=86400, `NOTIFY_MAX_RETRIES`=2, `OPERATION_INDETERMINATE_EXPIRY_SECONDS`=900, `EVALUATE_RATE_LIMIT_PER_MINUTE`=30, `CHANGE_RIGHTS` (por defecto `REBOOK_NO_FEE`, S-10), `SUPPORTED_EVENT_TYPES`, `NOTIFY_ONLY_EVENT_TYPES` (por defecto `GATE_CHANGE`), `POLICY_SCENARIOS`, `REASON_PRIORITY` (orden de FR-063), tabla de compatibilidad de afirmaciones (FR-013) y `SERVICE_API_KEY`/`IDEMPOTENCY_SECRET` (secretos solo por entorno). Un test cambia cada parámetro y comprueba que cambia el comportamiento. También son configurables los parámetros operativos de `EXTERNAL_CONTRACTS.md` §2.4 (timeouts, reintentos de lectura, `CLOCK_MODE`, `CORS_ALLOWED_ORIGINS`, `DB_PATH`, banderas de desarrollo). | Usuario (2026-10-19) | REQ-N-05 |
| **NFR-013** | **Seguridad de entradas:** todo acceso a la base usa consultas parametrizadas (el SQL vive en archivos `.sql`); la interfaz muestra los textos del proveedor (`condition`, `entitlement`, puerta, mensajes) como **texto plano**, sin insertar HTML; `evaluate`, aceptar, caso humano y consulta de decisión tienen límite de tasa (`EVALUATE_RATE_LIMIT_PER_MINUTE`, por reserva y por origen), y los intentos fallidos de credencial de servicio también se limitan por origen. | Revisión CTO A1 (DEBT-A1-05/06) | REQ-E-04, REQ-N-04 |

## 5. Documentación y entregables (`DOC`)

| ID | Requisito | Decisión | Traza |
|---|---|---|---|
| **DOC-001** | **Entregable 1:** README raíz con track elegido y por qué, instrucciones de ejecución, alcance implementado, tests disponibles y limitaciones. | DEC-01, DEC-04 | REQ-D-01…06 |
| **DOC-002** | **Entregable 2:** README de ingeniería (≤ 2 págs.): problema, supuestos y alcance, decisiones y alternativas descartadas, clasificación de pasos (determinístico / AI-assisted / agentic / human) con razón, riesgo y control, riesgos y próximos pasos, cómo se validó. | DEC-02 | REQ-D-07, REQ-D-09, REQ-F-06, REQ-F-10 |
| **DOC-003** | **Entregable 3:** nota de uso de IA (≤ 1 pág.). | DEC-22, DEC-37 | REQ-D-08 |
| **DOC-004** | **Diseño técnico** (RFC técnico generado por SDD-WORKFLOW) en Markdown: base de la presentación. | DEC-03 | REQ-D-11 |
| **DOC-005** | Las decisiones tomadas, explícitas en un `.md` dentro del repositorio. | DEC-37 | REQ-P-10 |
| **DOC-006** | Bitácora paso a paso de las interacciones con Claude (incluye revisiones /codex). | DEC-37 | REQ-P-10, REQ-E-03 |
| **DOC-007** | Guion de presentación de 10 min derivado del diseño técnico. | DEC-03 | REQ-P-06, REQ-P-07 |
| **DOC-008** | Notas obligatorias: (1) las políticas publicadas no pueden entrar en conflicto con las políticas del sistema y en el desafío valen las del `get_policy_rules`; (2) sería útil un campo `cause`; (3) cancelación y adelanto, para una segunda etapa; (4) la definición de «menor» debe fijarse por país; (5) idioma neutro sin localización en v1; (6) visión futura más proactiva (notificaciones por evento operacional). | DEC-05, 30, 31, 32, 36, 04 | REQ-D-07 |
| **DOC-009** | **Información a solicitar:** lista completa de tipos de evento y documentación de cada endpoint; MCT por aeropuerto; campo `cause`; semántica de `PENDING_CONFIRMATION`; definición de «menor». | DEC-04, DEC-07 | GAP-11, GAP-12 |
| **DOC-010** | Runbook de una página. | DEC-24 | REQ-N-05 |
| **DOC-011** | **Preguntas para Producto/Legal** (sin cotejo de umbrales externos, DEC-26): jurisdicción por segmento y campo `jurisdiction` previsto (DEC-25); tratamiento de México (DEC-34); reembolso, tarifas no reembolsables y plazos (DEC-28, GAP-04/10); brechas GAP-01…10 convertidas en preguntas (DEC-35); causa del evento (DEC-30). | DEC-25, 28, 30, 34, 35 | REQ-D-07, GAP-01…10, GAP-14 |
| **DOC-012** | Diseño documentado de la aprobación humana: al aprobar un agente se revalida de nuevo; la aprobación autoriza una **decisión**, no una ejecución con datos viejos (antes FR-073). | DEC-19 | GAP-25 |
| **DOC-013** | Extensiones de contrato propuestas al equipo: reserva y pasajeros en `create_rebooking_request`, destinatario y tipo de aviso (`INFORMATIONAL` sin `policy_ref`) en `notify_passenger`, contrato reducido en opciones (antes FR-104). | DEC-18, 20, 22 | DAT-62, DAT-65, DAT-79 |

## 6. Pruebas (DEC-24 b: batería completa) — mapeo TC → requisitos

| TC | Qué verifica | FR |
|---|---|---|
| TC-01 (**e2e caso base**) | Combina reserva + eventos + política: retraso 160 min, R1 falso, R3 y R5 verdaderos, O1 viable, O2 no viable, O3 no verificable; propuesta O1 + reembolso genérico; **se ofrece** caso humano por aprobación del menor (motivo principal `POLICY_APPROVAL_REQUIRED`) y pernocte; sin `create_rebooking_request` | FR-004…063 |
| TC-02 | Solo `E-1012` (degradado) ⇒ no concluir «a tiempo» | FR-010, FR-014 |
| TC-03 | Conflicto: dos eventos **sanos** con el **mismo `recorded_at`** e incompatibles ⇒ humano (escenario sintético; con `E-1012` degradado no hay conflicto: se excluye y gana `E-1001`, ver TC-36) | FR-012, FR-013 |
| TC-04 / TC-05 | Bordes 179/180 y 239/240: se afirman solo **R1/R2** (con la reserva base R3 y R5 también aplican) | FR-030…034 |
| TC-06 | Retraso 60 min (margen 10 min, MCT no provisto) ⇒ `missed_connection` **desconocido** ⇒ humano; y retraso 10 min (margen 60 min) ⇒ **falso** (ver H-13) | FR-022, FR-023 |
| TC-21 *(añadido)* | Una sesión no puede leer otra reserva ni un registro ajeno: respuesta **idéntica** a la de un recurso inexistente (`404`) | FR-001, FR-093 |
| TC-22 *(añadido)* | Dos aceptaciones simultáneas ⇒ una sola escritura | FR-053, FR-062 |
| TC-24 *(añadido)* | `SCHEDULED` u `ON_TIME` **más reciente y sano** que un `DELAY` ⇒ el retraso se borra (solo contexto); más antiguo ⇒ el retraso se mantiene; posterior pero **degradado** ⇒ no lo borra | FR-012, FR-013 |
| TC-25 *(añadido)* | Dos `DELAY` compatibles (100 → 160) ⇒ gana el más reciente | FR-012 |
| TC-26 *(añadido)* | `DELAY` incoherente, segmento desconocido y marca de tiempo futura ⇒ descartados con su razón | FR-015, FR-016 |
| TC-27 *(añadido)* | TTL: a 119 s vigente; a 120 s vencida; sin `ttl_seconds` vencida | FR-017, FR-072 |
| TC-28 *(añadido)* | Pernocte derivada (O1 al día siguiente) y no derivada (misma fecha) | FR-029 |
| TC-29 *(añadido)* | Opción con `fare_difference > 0` sin `currency` ⇒ no viable | FR-048 |
| TC-30 *(añadido)* | `201 PENDING_CONFIRMATION` ⇒ texto «pendiente… sujeta a disponibilidad» con `expires_at` | FR-056 |
| TC-31 *(añadido)* | Huella distinta (cupos agotados, itinerario sustituido) ⇒ no escribe; cambia solo una marca de tiempo ⇒ sí escribe | FR-070 |
| TC-32 *(añadido)* | Purga del registro a los `AUDIT_RETENTION_DAYS` | FR-092 |
| TC-33 *(añadido)* | Matriz de errores: lectura caída, `422`, timeout de transporte, fallo de `create_human_case` | FR-105, FR-054 |
| TC-34 *(añadido)* | La llave idempotente es estable ante reevaluaciones y se reutiliza si cambia la versión de política | FR-053 |
| TC-35 *(añadido)* | Segmento afectado último ⇒ sin conexión; política vacía ⇒ BLOQUEADA | FR-022, FR-008 |
| TC-36 *(añadido)* | Un evento degradado **más reciente** no gana a uno sano más antiguo (`E-1012` posterior a `E-1001`) | FR-010, FR-012 |
| TC-37 *(añadido)* | Opción con destino distinto, origen distinto o salida anterior a `new_arrival` + MCT ⇒ no viable | FR-041 |
| TC-38 *(añadido)* | Ciclo de vida: `EN_CURSO` colgado ⇒ `INDETERMINADA`; `CREADA` vencida ⇒ `EXPIRADA` y permite generación siguiente; llave no persistible ⇒ no escribe | FR-064 |
| TC-39 *(añadido)* | Integridad de lecturas: cadena rota, `DELAY` ≤ 0, segmentos desordenados, menor sin adulto | FR-066 |
| TC-40 *(añadido)* | El contrato enviado a `create_rebooking_request` incluye reserva y pasajeros y el cliente no puede alterar la opción | FR-065 |
| TC-41 *(añadido)* | Parser: `EQ`/`==` y `NE`/`!=`, precedencia `AND`/`OR`, tipos mezclados, longitud y profundidad máximas | FR-030 |
| TC-42 *(añadido)* | `caller = system` con política rota ⇒ se envía **una** notificación con la plantilla fija, sin URL, con `policy_ref` y `booking_id` | FR-120, FR-122 |
| TC-43 *(añadido)* | `caller = system` sin política rota (incluidas anomalías que impiden evaluarla) ⇒ no se notifica y queda `needs_manual_review`; con política rota y decisión BLOQUEADA (menor desconocido) ⇒ **sí** se notifica | FR-123, FR-039 |
| TC-44 *(añadido)* | Dos llamadas `system` iguales dentro del enfriamiento ⇒ una sola notificación; `422` ⇒ `FALLIDA`; timeout ⇒ `INDETERMINADA` sin éxito afirmado | FR-123 |
| TC-45 *(añadido)* | Retraso que no rompe ninguna política (`INFORMATIVA`) ⇒ se informa y se muestran las reglas; **no** se consulta `get_eligible_options`; sin botón de soporte ni opciones | FR-039, FR-004 |
| TC-46 *(añadido)* | El motivo de compensación del menú solo aparece si hay compensación elegible por política | FR-067, FR-060 |
| TC-47 *(añadido)* | Tipo de pasajero desconocido: con política rota ⇒ validación manual; sin política rota ⇒ solo se informa | FR-024, FR-033, FR-039 |
| TC-48 *(añadido)* | Un mensaje con URL, enlace, teléfono o correo es bloqueado por el validador | FR-122, FR-081 |
| TC-49 *(añadido)* | Cambiar cada parámetro de configuración cambia el comportamiento; un valor inválido impide arrancar | NFR-012 |
| TC-50 *(añadido)* | El modo `system` exige credencial de servicio, no devuelve PII ni la vista completa y no ejecuta acciones del pasajero | FR-120, FR-121 |
| TC-51 *(añadido)* | Solo `GATE_CHANGE` ⇒ la vista informa el cambio de puerta; **no** se consulta política; decisión `INFORMATIVA`; en modo `system` se envía una notificación `GATE_CHANGE` sin `policy_ref` | FR-006, FR-068, FR-122 |
| TC-52 *(añadido)* | `DELAY` + `GATE_CHANGE` ⇒ contexto completo (ambos visibles); política consultada solo para `DELAY`; en `system`, una notificación por motivo (hasta 2) | FR-068, FR-122 |
| TC-53 *(añadido)* | Política vacía para `DELAY` ⇒ BLOQUEADA; `GATE_CHANGE` nunca consulta política aunque la configuración incluya otros escenarios | FR-068, FR-008 |
| TC-54 *(añadido)* | Segmento sin eventos, o solo con `GATE_CHANGE` ⇒ se muestra su horario programado (estado `NO_EVENTS`), sin «sin información verificada» ni alertas | FR-014, FR-004 |
| TC-55 *(añadido)* | Puerta 24 → 25 en modo `system` ⇒ aviso nuevo (la huella incluye la puerta); misma puerta ⇒ sin reenvío | FR-123 |
| TC-56 *(añadido)* | La purga conserva las operaciones `INDETERMINADA`/`EN_CURSO`/`CREADA` vigentes y su bloqueo | FR-092, FR-064 |
| TC-57 *(añadido)* | Una operación `INDETERMINADA` pasa a `EXPIRADA` tras `OPERATION_INDETERMINATE_EXPIRY_SECONDS` y permite la generación siguiente | FR-064 |
| TC-58 *(añadido)* | `evaluate` supera `EVALUATE_RATE_LIMIT_PER_MINUTE` ⇒ rechazo; un texto del proveedor con HTML se muestra como texto plano; las consultas a la base son parametrizadas | NFR-013 |
| TC-59 *(añadido)* | La consulta de una decisión por la sesión del pasajero no incluye `needs_manual_review` ni el detalle de notificaciones | FR-093 |
| TC-60 *(añadido)* | El aviso se dirige al titular adulto, nunca al menor; un cambio solo de minutos del `DELAY` no repite el aviso; con `missed_connection` desconocido ninguna opción es viable | FR-122, FR-123, FR-041 |
| TC-23 *(añadido)* | Varios segmentos retrasados ⇒ humano `MULTIPLE_AFFECTED_SEGMENTS`; tipo de pasajero desconocido ⇒ menor desconocido y, con política rota **sin regla R5**, validación manual | FR-019, FR-024 |
| TC-07 | Sin menor ⇒ R5 falso ⇒ se permite `create_rebooking_request` | FR-035, FR-051 |
| TC-08 | Opciones vencidas ⇒ refrescar | FR-072 |
| TC-09 | Solo O2 con 2 pasajeros ⇒ sin opción viable ⇒ humano | FR-041, FR-047 |
| TC-10 | `policy_ref` superseded ⇒ opción sin respaldo | FR-041 |
| TC-11 | O3 con `POL-REFUND` no recuperada ⇒ sin afirmación | FR-041, FR-046 |
| TC-12 | Sin `change_penalty_amount` ⇒ no cotizar | FR-049, FR-086 |
| TC-13 | `CANCELLATION` ⇒ humano | FR-007 |
| TC-14 | `503` ⇒ misma llave, 2 reintentos, caso humano | FR-054 |
| TC-15 | `409` ⇒ solicitud existente | FR-055 |
| TC-16 | `notify` sin `policy_ref` o con afirmación no validada ⇒ bloqueo | FR-081 |
| TC-17 | `compensation_requested` ⇒ humano, sin montos | FR-060 |
| TC-18 | Retraso que cruza medianoche ⇒ fecha correcta | FR-021 |
| TC-19 | `OPS_CORE` degradada ⇒ sin fuente sana ⇒ humano | FR-014 |
| TC-20 | Pedido de PII ⇒ rechazo | FR-061 |

Además: pruebas unitarias del parser (todas las operaciones), de la llave idempotente y del enmascaramiento de PII; pruebas del front con simulación de DOM.

## 7. Fuera de v1 / Fase 2

Caché de lecturas · disparo automático del modo `system` por evento operacional · respuesta del modo `system` guardada para el front · JEV/probabilidad ≥ 95 % para decisión automática · políticas externas y jurisdicción por segmento · cancelación y adelanto · campo `cause` · definición de «menor» por país · localización · confirmación de `PENDING_CONFIRMATION` · flujo operativo de aprobación humana · MCT real · retención definitiva · adaptador HTTP real.

## 8. Matriz decisión → requisitos

| DEC | Requisitos | DEC | Requisitos |
|---|---|---|---|
| 01 | DOC-001, FR-110, FR-111 | 20 | FR-081, FR-085, FR-120…124 |
| 02 | FR-004, FR-008, FR-009, NFR-001, DOC-002 | 21 | FR-001, FR-003, FR-112 |
| 03 | DOC-004, DOC-007 | 22 | FR-040, FR-061, NFR-002 |
| 04 | FR-100, FR-101, FR-111, NFR-006, DOC-008, DOC-009 | 23 | FR-036, FR-059, FR-090…093 |
| 05 | FR-005, FR-006, H-01, H-09 | 24 | NFR-004…006, NFR-008, DOC-010 |
| 06 | FR-020, FR-021 | 25 | (solo `get_policy_rules`; DOC-008) |
| 07 | FR-022, FR-023 | 26 | (solo `get_policy_rules`; DOC-008) |
| 08 | FR-018, FR-026, FR-027 | 27 | FR-029, FR-057, FR-058 |
| 09 | FR-010…016, FR-038 | 28 | FR-046, FR-049, DOC-011 |
| 10 `PROV` | FR-002, FR-017, FR-072 | 29 | FR-025, FR-060 |
| 11 | FR-086, FR-049 | 30 | FR-083, FR-084, DOC-008, DOC-011 |
| 12 | FR-015, FR-028, FR-030…033 | 31 | FR-007, FR-019, FR-102, DOC-008 |
| 13 | FR-035, FR-038, FR-052 | 32 | FR-024, DOC-008 |
| 14 | FR-050, FR-051 | 33 | FR-082 |
| 15 | FR-007, FR-013, FR-047, FR-057, FR-059, FR-063 | 34 | (fuera de alcance; DOC-009, DOC-011) |
| 16 | FR-041, FR-043, FR-052 | 35 | (solo contexto; §0 y H-01) |
| 17 | FR-041…048 | 36 | FR-080, FR-113, DOC-008 |
| 18 | FR-053…056, FR-062, FR-105, DOC-013 | 37 | DOC-003, DOC-005, DOC-006, NFR-010 |
| 19 | FR-002, FR-051, FR-070…072, DOC-012 | | |

## 8b. Supuestos técnicos míos añadidos tras la revisión CTO (confírmalos)

**Todos los valores numéricos y listas de esta tabla son variables de configuración (NFR-012), no constantes del código.**

| ID | Supuesto | Dónde |
|---|---|---|
| S-09 | `RELEVANT_DELAY_MIN_MINUTES` = 1: todo retraso validado se informa; la política decide los derechos. | FR-005, H-09 |
| S-10 | En v1 el único derecho de cambio es `REBOOK_NO_FEE` (el de las reglas del PDF). | FR-041 |
| S-11 | `MCT_UNCERTAINTY_MINUTES` = 45 y `CLOCK_SKEW_SECONDS` = 60. | FR-022, FR-016 |
| S-12 | Más de un segmento retrasado ⇒ caso humano; v1 no decide itinerarios complejos. | FR-019 |
| S-13 | Persistencia local en SQLite (llaves idempotentes, registro de decisiones, deduplicación de casos); retención provisional 30 días. | FR-053, FR-059, FR-092 |
| S-15 | Cifras de aceptación inventadas por mí: p95 < 1,5 s con *upstreams* de 100 ms (NFR-004) y cobertura ≥ 85 % (NFR-006). | NFR-004, NFR-006 |
| S-16 | Prioridad de motivos de caso humano (FR-063). | FR-063 |
| S-17 | Tabla de compatibilidad de afirmaciones: `DELAY` > 0 = «retrasado»; `STATUS: ON_TIME` = «a tiempo»; `SCHEDULED` = «vuelta al horario programado» (reemplaza a un `DELAY` anterior, FR-012). | FR-013 |
| S-18 | `INDETERMINADA` bloquea nuevas operaciones hasta que se resuelva el caso humano o venza `OPERATION_INDETERMINATE_EXPIRY_SECONDS`; `EXPIRADA` permite una operación nueva con la generación siguiente (la confirmación queda fuera de v1, DAT-61). | FR-064 |
| S-19 | Constantes mías: `OPERATION_STALE_SECONDS` = 120; condición del parser ≤ 200 caracteres y ≤ 10 niveles; fecha de llegada +1 día si la hora es menor que la de salida. | FR-064, FR-030, FR-021 |
| S-20 | `OPERATION_INDETERMINATE_EXPIRY_SECONDS`=900 y `EVALUATE_RATE_LIMIT_PER_MINUTE`=30 son valores míos; riesgo conocido: si una solicitud indeterminada sí se creó y su vigencia fuera mayor, un nuevo intento podría duplicarla. | FR-064, NFR-013 |
| S-14 | Sesión simulada por cabecera; la autenticación real queda fuera, pero la **comprobación de pertenencia** sí se implementa. | FR-001 |

## 9. Cobertura de los `REQ-*` originales

Todos los `REQ-F-00…30`, `REQ-N-01…10`, `REQ-C-01…07`, `REQ-D-01…11` y `REQ-E-01…09` quedan cubiertos por al menos un FR/NFR/DOC arriba o por una decisión de «solo contexto». `REQ-F-08` se cubre parcialmente (front de prueba). `REQ-P-*` (proceso del ejercicio) se gestionan fuera del código: tiempo, formato, defensa.
