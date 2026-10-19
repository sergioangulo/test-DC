# 01 · Índice de la fuente (`SRC`) — cada enunciado del PDF con ID, página y sección

> **Para qué sirve.** Es la **única referencia primaria**. Todo requerimiento (`REQ-…`), brecha (`GAP-…`), observación de datos (`DAT-…`) y decisión (`DEC-…`) cita uno o más `SRC-pp-nn` (pp = página del PDF, nn = orden en la página). Si algo no tiene `SRC`, **no viene del PDF** y está marcado como **DERIVADO** o **SUPUESTO**.
> **Fuente:** `Disruption Companion.pdf` — 7 páginas, título interno `04_Caso_A_Disruption_Companion.docx`, generado por "Skia/PDF m156 Google Docs Renderer". Sin metadata, JavaScript, adjuntos ni texto oculto (ver análisis de seguridad previo en la conversación).
> **Citas:** textos literales del PDF (el PDF es tu documento de trabajo). Los fragmentos JSON están **completos y literales** en `04_Analisis_de_Datos`.

## Marcador de clasificación
| ID | Pág. | Texto |
|---|---|---|
| **SRC-00-01** | 1–7 (pie de página) | "Uso interno" en **todas** las páginas |

## Página 1
| ID | Sección | Texto fuente |
|---|---|---|
| SRC-01-01 | Portada | "Caso A — Disruption Companion" |
| SRC-01-02 | Portada · Tiempo de trabajo | "Máximo 3 horas efectivas" |
| SRC-01-03 | Portada · Plazo de preparación | "48 horas desde que recibes este documento (es el plazo disponible, no 48 horas de trabajo continuo)" |
| SRC-01-04 | Portada · Sesión con el comité | "10 minutos de presentación + preguntas, profundización y debate técnico (40 a 45 minutos en total), dentro de las 48 horas hábiles siguientes a tu entrega, ante un comité de dos evaluadores" |
| SRC-01-05 | Portada · Entregables | "Vertical slice técnico (track a elección) + README de ingeniería (2 pág.) + AI Usage & Decision Note (1 pág.) — Formato de entrega y soporte de presentación a tu elección" |
| SRC-01-06 | "Lee esto primero" | "No esperamos una aplicación terminada, ni despliegue, ni una presentación formal con diapositivas: presentarás tu propuesta en 10 minutos con el soporte que prefieras (ver sección 7)." |
| SRC-01-07 | "Lee esto primero" | "Este ejercicio no mide cuánto código produces: mide cómo diriges la construcción de una solución cuando la IA es parte activa de tu proceso de ingeniería." |
| SRC-01-08 | "Lee esto primero" | "Un candidato que construye menos, pero demuestra mejor criterio, control del proceso y fundamentos sólidos, puede obtener una mejor evaluación que alguien que entrega una aplicación completa sin poder explicar cómo fue producida." |
| SRC-01-09 | §1 Contexto | "Un equipo compacto —Product Manager, Product Designer, Engineering Team Lead y Software Engineer— está construyendo una funcionalidad para ayudar a pasajeros cuyo vuelo sufrió una modificación." |
| SRC-01-10 | §1 Contexto | "El producto debe ayudar al pasajero a entender qué ocurrió y cuál es su siguiente paso, sin entregar información no verificada y sin ejecutar acciones de alto impacto sin los controles correspondientes." |
| SRC-01-11 | §1 · Objetivo de negocio | "Reducir la incertidumbre del pasajero y los contactos evitables al call center, manteniendo exactitud, seguridad y trazabilidad." |
| SRC-01-12 | §1 · Primera versión (1) | "consulte el contexto de su viaje;" |
| SRC-01-13 | §1 · Primera versión (2) | "entienda si hubo una modificación relevante y qué implica;" |
| SRC-01-14 | §1 · Primera versión (3) | "reciba una explicación o recomendación accionable;" |
| SRC-01-15 | §1 · Primera versión (4) | "sea derivado a una persona, o inicie una acción controlada, cuando corresponda." |
| SRC-01-16 | §2 Sistemas disponibles | "Puedes asumir que existen interfaces equivalentes a las siguientes. No es obligatorio utilizarlas todas. Si trabajas con mocks propios, mantén estos contratos." |
| SRC-01-17 | §2 · Tabla | `get_trip_context(booking_id)` — Lectura — "Puede devolver información parcial." |
| SRC-01-18 | §2 · Tabla | `get_operational_events(segment_ids)` — Lectura — "Requiere controlar timestamp, fuente y frescura." |

## Página 2
| ID | Sección | Texto fuente |
|---|---|---|
| SRC-02-01 | §2 · Tabla (cont.) | `get_eligible_options(trip_context)` — Lectura — "Entrega opciones candidatas, no una decisión final." |
| SRC-02-02 | §2 · Tabla | `get_policy_rules(scenario)` — Lectura — "Reglas versionadas y verificables." |
| SRC-02-03 | §2 · Tabla | `create_rebooking_request(option, idempotency_key)` — Escritura — "Acción de alto impacto." |
| SRC-02-04 | §2 · Tabla | `create_human_case(reason, evidence)` — Escritura — "Escalamiento a operación humana." |
| SRC-02-05 | §2 · Tabla | `notify_passenger(message)` — Escritura — "No debe enviar información no validada." |
| SRC-02-06 | Ejemplos de respuesta | "Estos ejemplos son representativos de lo que devuelven las tools. Úsalos como base de trabajo." |
| SRC-02-07 | Ejemplo | JSON de `get_trip_context("ABC123")` (completo; p. 2) |
| SRC-02-08 | Ejemplo | JSON de `get_operational_events(["S1","S2"])` — inicio: `E-1001`, `E-1007` (continúa en p. 3) |

## Página 3
| ID | Sección | Texto fuente |
|---|---|---|
| SRC-03-01 | Ejemplo (cont.) | Continuación de `get_operational_events`: `E-1012`, `E-2003`, `_meta` (con `sources_degraded`) |
| SRC-03-02 | Ejemplo | JSON de `get_eligible_options(trip_context)` (O1, O2, O3 + `_meta.ttl_seconds`) |
| SRC-03-03 | Ejemplo | JSON de `get_policy_rules("DELAY")` (R1–R5 + versión + `superseded_versions`) |
| SRC-03-04 | Tools de escritura | `create_rebooking_request` → `201` / `409` / `503` (el comentario "el resultado real es indeterminado" cruza a p. 4) |

## Página 4
| ID | Sección | Texto fuente |
|---|---|---|
| SRC-04-01 | Tools de escritura | `503 { "error": "UPSTREAM_TIMEOUT" } // el resultado real es indeterminado` (p. 3–4) |
| SRC-04-02 | Tools de escritura | `create_human_case` → `201 { case_id, queue, sla_minutes }` |
| SRC-04-03 | Tools de escritura | `notify_passenger` → `202 { notification_id, channel, status }` · `422 { error: "UNVALIDATED_CONTENT", detail: "falta policy_ref" }` |
| SRC-04-04 | §3 Restricciones | "Los datos operacionales pueden estar desactualizados o ser contradictorios entre fuentes." |
| SRC-04-05 | §3 | "Una recomendación incorrecta puede generar costo, un reclamo o el incumplimiento de una política." |
| SRC-04-06 | §3 | "Cambiar una reserva o emitir una compensación son acciones de alto impacto." |
| SRC-04-07 | §3 | "Deben protegerse los datos personales y aplicarse mínimo privilegio." |
| SRC-04-08 | §3 | "La primera versión debe poder ser operada por un equipo pequeño." |
| SRC-04-09 | §3 | "Deben considerarse latencia, costo por interacción y dependencia de modelos." |
| SRC-04-10 | §3 | "No existe una única solución correcta." |
| SRC-04-11 | §4 Ambigüedades | "El enunciado no las define a propósito. Puedes decidirlas, documentarlas o explicitar qué preguntarías y a quién." |
| SRC-04-12 | §4 (AMB-01) | "Qué se considera una modificación relevante." |
| SRC-04-13 | §4 (AMB-02) | "Qué información puede mostrarse al pasajero y cuál no." |
| SRC-04-14 | §4 (AMB-03) | "En qué casos una recomendación puede entregarse de forma automática." |
| SRC-04-15 | §4 (AMB-04) | "En qué casos debe intervenir una persona antes de actuar o comunicar." |
| SRC-04-16 | §4 (AMB-05) | "Qué hacer cuando las fuentes entregan información contradictoria." |
| SRC-04-17 | §5 Tu tarea | "Diseña una primera versión acotada del producto. Debes implementar un vertical slice técnico en uno de los dos tracks siguientes — la capa complementaria puedes dejarla como diseño, contrato o pseudocódigo." |
| SRC-04-18 | §5 · Track Backend/Integración | "implementa la lógica que resuelve el caso base — combinar reserva, eventos y políticas para determinar qué le corresponde al pasajero — como servicio o función invocable, con manejo de errores y al menos una validación o test." |
| SRC-04-19 | §5 · Track Frontend/Experience | "implementa la pantalla o flujo que vería el pasajero, consumiendo datos equivalentes a los que entregarían las tools, mostrando el estado del viaje, la alerta y la recomendación, con al menos una validación." |
| SRC-04-20 | §5 | "No se espera que domines ambos tracks con la misma profundidad: el requisito es demostrar profundidad en uno y capacidad de diseñar cómo se integra la capa complementaria." |
| SRC-04-21 | §5 · Tarea 1 | "Resuelve el caso base. A partir de la información disponible, determina qué ocurrió con el viaje y qué corresponde ofrecer o comunicar al pasajero." |
| SRC-04-22 | §5 · Tarea 2 | "Diseña el manejo de una consulta ambigua o compleja en la que el sistema deba combinar reserva, eventos operacionales y políticas para llegar a una respuesta. Explica cómo se descompone el trabajo, qué contexto se recupera, qué queda determinístico, qué se resuelve con IA o con un agente, y dónde se detiene para pedir intervención humana." |
| SRC-04-23 | §5 · Tarea 3 (p. 4–5) | "Implementa tu vertical slice según el track elegido, y especifica —sin necesidad de implementarla— la capa complementaria: si tu track fue Backend, cómo se vería o comunicaría al pasajero (pantalla, wireframe o especificación del mensaje); si tu track fue Frontend, qué contrato o lógica de backend asume como dado." |

## Página 5
| ID | Sección | Texto fuente |
|---|---|---|
| SRC-05-01 | §5 · IA en el producto | "No es obligatorio incorporar IA en runtime. Si decides no hacerlo, explica qué beneficio esperabas y por qué el riesgo, el costo o la complejidad no lo justifican. Resolver algo de forma determinística puede ser una excelente decisión de ingeniería." |
| SRC-05-02 | §6 · Entregable 1 | "Tu vertical slice del track elegido, más diseño, contrato o pseudocódigo para la capa complementaria. Debe permitir verificar al menos una decisión relevante del caso. Incluye: track elegido (Backend/Integración o Frontend/Experience) y por qué; instrucciones para revisarlo o ejecutarlo; alcance efectivamente implementado; tests o validaciones disponibles; limitaciones conocidas." |
| SRC-05-03 | §6 · Entregable 2 | "README de ingeniería (máx. 2 páginas): problema entendido y outcome esperado; supuestos y alcance; decisiones principales y sus alternativas descartadas; qué quedó determinístico, AI-assisted, agentic o human-controlled; riesgos y próximos pasos; cómo validaste la solución." |
| SRC-05-04 | §6 · Entregable 3 | "AI Usage & Decision Note (máx. 1 página): herramientas de IA utilizadas y para qué; outputs aceptados, rechazados o modificados, y cómo los validaste; decisiones que tomaste personalmente; qué información nunca entregarías a un modelo." |
| SRC-05-05 | §6 · Tabla de clasificación | "Puedes usar esta tabla para mostrar la clasificación de pasos que pide el README (también puedes incluirla directamente en el README o en tu presentación)": columnas **Paso · Clasificación · Razón · Riesgo · Control / fallback**; valores de clasificación: determinístico / AI-assisted / agentic / human |
| SRC-05-06 | §7 · Cómo funciona el proceso | "Recibes el desafío → preparas tu propuesta (48 horas) → la entregas en el formato que elijas → presentas durante 10 minutos ante el comité → preguntas, profundización y debate técnico → evaluación." |
| SRC-05-07 | §7 · Preparación (p. 5–6) | "Tienes 48 horas desde que recibes este documento para preparar y enviar tu propuesta. Las 48 horas son el plazo disponible, no 48 horas de trabajo continuo: el trabajo efectivo tiene un máximo de 3 horas, que puedes distribuir en varias sesiones." |

## Página 6
| ID | Sección | Texto fuente |
|---|---|---|
| SRC-06-01 | §7 · Preparación | "Las 3 horas incluyen el análisis del caso, la implementación, las validaciones y la documentación. El tiempo es un límite, no una meta: no evaluamos cuánto alcanzaste a producir dentro de él." |
| SRC-06-02 | §7 · Entrega y formato | "Los tres entregables de la sección 6 son obligatorios en su contenido. Tú eliges el formato y los archivos más adecuados … (por ejemplo, repositorio, Markdown, PDF, documento, diagrama o demo). No exigimos una herramienta ni un formato específico, y no evaluamos la estética del material." |
| SRC-06-03 | §7 · Presentación | "La sesión con el comité se agenda dentro de las 48 horas hábiles siguientes a tu entrega y dura entre 40 y 45 minutos. Comienza con 10 minutos … puedes usar directamente tus entregables y no necesitas preparar diapositivas. Usa ese tiempo para explicar: cómo entendiste el problema; cómo estructuraste tu solución; tus decisiones principales y los supuestos que tomaste; los criterios que usaste para decidir; los trade-offs más relevantes. No es necesario recorrer cada detalle de tu solución: el resto se conversa después." |
| SRC-06-04 | §7 · Preguntas y debate técnico | "Esta instancia forma parte integral de la evaluación. El comité podrá: preguntar por tus decisiones y cuestionar tus supuestos; explorar alternativas que descartaste y profundizar en trade-offs; plantear escenarios o cambiar restricciones para conversar sobre cómo adaptarías tu propuesta; preguntar por riesgos y por cómo evolucionaría la solución. … Los escenarios que se planteen no requieren desarrollo nuevo: buscamos conversar sobre tu razonamiento." |
| SRC-06-05 | §7 · Uso de IA | "Puedes utilizar libremente LLMs, coding assistants, agentes, búsqueda, scripts, automatizaciones, skills, MCPs y frameworks equivalentes. No evaluamos una herramienta específica ni la cantidad de herramientas usadas. … Sí te pedimos transparencia: el uso de IA debe quedar reflejado en el Entregable 3, y en la defensa vamos a conversar sobre decisiones concretas de tu proceso." |
| SRC-06-06 | §8 Cómo evaluamos | "La evaluación combina tus entregables con tu presentación y la conversación técnica. No se centra únicamente en el resultado final: buscamos comprender cómo interpretas el problema, cómo estructuras tu razonamiento, cómo tomas decisiones, cómo evalúas alternativas y trade-offs, y cómo defiendes y adaptas técnicamente tu propuesta." |
| SRC-06-07 | §8 | "No existe una única solución correcta. Una solución distinta a la que habríamos elegido no es incorrecta si está bien razonada y es técnicamente consistente. Una solución más compleja no es automáticamente mejor, y una más simple tampoco." |

## Página 7 — Tabla de evaluación
| ID | Dimensión | Qué observamos (literal) |
|---|---|---|
| SRC-07-01 | Pensamiento de producto | "Cómo entiendes y acotas el problema, qué supuestos explicitas, qué resultado priorizas y cómo lo medirías." |
| SRC-07-02 | Fundamentos de ingeniería | "Coherencia técnica de lo que implementas: contratos, estados, errores, límites e integración con el resto del sistema." |
| SRC-07-03 | Desarrollo asistido por IA | "Cómo usas IA en tu proceso sin delegar el criterio: qué controles defines, qué verificas y qué aceptas, corriges o rechazas." |
| SRC-07-04 | Calidad, seguridad y confiabilidad | "Qué comprobaciones haces y cómo manejas fallos, permisos, datos sensibles y operación." |
| SRC-07-05 | Priorización y evidencia | "Si concentras el tiempo en lo importante y dejas evidencia localizable y pendientes explícitos." |
| SRC-07-06 | Juicio técnico y trade-offs | "Cómo comparas alternativas considerando consecuencias, costos, riesgos y reversibilidad." |
| SRC-07-07 | Razonamiento agentic y control | "Dónde aporta valor un agente o la IA y dónde conviene lógica determinística o intervención humana; qué contexto, herramientas y permisos usa; dónde se detiene y cómo detectas un output incorrecto." |
| SRC-07-08 | Responsabilidad y adaptación | "Si asumes el resultado, reconoces límites y revisas tus decisiones ante información nueva durante la conversación." |
| SRC-07-09 | Qué no evaluamos | "No penalizamos no terminar la capa complementaria al track elegido …, no usar IA en runtime, no usar MCP ni un framework específico, entregar pseudocódigo en una parte no esencial, una interfaz poco pulida, ni proponer una solución distinta a la que habríamos elegido nosotros. Tampoco evaluamos velocidad de escritura ni conocimiento detallado del dominio aéreo. Tampoco evaluamos la estética ni el formato del material que uses para presentar, ni el uso o no uso de IA por sí mismo." |
| SRC-07-10 | Cierre | "Si algo del enunciado te resulta insuficiente para avanzar, esa también es información útil: documenta el supuesto que tomaste y por qué. Nos interesa más tu criterio." |

## Cobertura
- **78 entradas** indexadas (1 marcador de clasificación + 77 enunciados, incluidas las 8 dimensiones de evaluación). No se omitió ningún párrafo del PDF; los bloques JSON se tratan como `SRC-02-07`, `SRC-02-08`/`SRC-03-01`, `SRC-03-02`, `SRC-03-03`, `SRC-03-04`/`SRC-04-01…03`.
- **Excepciones de edición:** en `SRC-06-02/03/04/05` se marcó con "…" lo omitido por brevedad; el resto del párrafo no cambia el requerimiento. Texto íntegro en el PDF.
