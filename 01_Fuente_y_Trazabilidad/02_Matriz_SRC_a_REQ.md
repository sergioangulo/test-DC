# 01.02 · Matriz de trazabilidad inversa: `SRC` → `REQ`

> Generada por script a partir de `01_Indice_de_fuente_SRC.md` y `03_Requerimientos/REQUERIMIENTOS.md`. Para cada enunciado del PDF, qué requisitos (`REQ`) o ambigüedades (`AMB`) lo citan.

| SRC | Sección | Texto (recortado) | Cubierto por |
|---|---|---|---|
| `SRC-00-01` | 1–7 (pie de página) | "Uso interno" en **todas** las páginas | `REQ-N-10`, `REQ-P-12` |
| `SRC-01-01` | Portada | "Caso A — Disruption Companion" | — *(contexto, sin requisito propio)* |
| `SRC-01-02` | Portada · Tiempo de trabajo | "Máximo 3 horas efectivas" | `REQ-P-01` |
| `SRC-01-03` | Portada · Plazo de preparación | "48 horas desde que recibes este documento (es el plazo disponible, no 48 horas de trabajo cont… | `REQ-P-02` |
| `SRC-01-04` | Portada · Sesión con el comité | "10 minutos de presentación + preguntas, profundización y debate técnico (40 a 45 minutos en to… | `REQ-P-05` |
| `SRC-01-05` | Portada · Entregables | "Vertical slice técnico (track a elección) + README de ingeniería (2 pág.) + AI Usage & Decisio… | `REQ-D-01`, `REQ-D-07`, `REQ-P-09` |
| `SRC-01-06` | "Lee esto primero" | "No esperamos una aplicación terminada, ni despliegue, ni una presentación formal con diapositi… | `REQ-D-11`, `REQ-P-06` |
| `SRC-01-07` | "Lee esto primero" | "Este ejercicio no mide cuánto código produces: mide cómo diriges la construcción de una soluci… | `REQ-P-04`, `REQ-P-10` |
| `SRC-01-08` | "Lee esto primero" | "Un candidato que construye menos, pero demuestra mejor criterio, control del proceso y fundame… | `REQ-E-09` |
| `SRC-01-09` | §1 Contexto | "Un equipo compacto —Product Manager, Product Designer, Engineering Team Lead y Software Engine… | `REQ-F-00` |
| `SRC-01-10` | §1 Contexto | "El producto debe ayudar al pasajero a entender qué ocurrió y cuál es su siguiente paso, sin en… | `REQ-F-03`, `REQ-F-16`, `REQ-F-17` |
| `SRC-01-11` | §1 · Objetivo de negocio | "Reducir la incertidumbre del pasajero y los contactos evitables al call center, manteniendo ex… | `REQ-F-28`, `REQ-N-08`, `REQ-N-09` |
| `SRC-01-12` | §1 · Primera versión (1) | "consulte el contexto de su viaje;" | `REQ-F-01` |
| `SRC-01-13` | §1 · Primera versión (2) | "entienda si hubo una modificación relevante y qué implica;" | `REQ-F-02` |
| `SRC-01-14` | §1 · Primera versión (3) | "reciba una explicación o recomendación accionable;" | `REQ-F-03` |
| `SRC-01-15` | §1 · Primera versión (4) | "sea derivado a una persona, o inicie una acción controlada, cuando corresponda." | `REQ-F-04` |
| `SRC-01-16` | §2 Sistemas disponibles | "Puedes asumir que existen interfaces equivalentes a las siguientes. No es obligatorio utilizar… | `REQ-F-27` |
| `SRC-01-17` | §2 · Tabla | `get_trip_context(booking_id)` — Lectura — "Puede devolver información parcial." | `REQ-C-01`, `REQ-F-01`, `REQ-F-22` |
| `SRC-01-18` | §2 · Tabla | `get_operational_events(segment_ids)` — Lectura — "Requiere controlar timestamp, fuente y fresc… | `REQ-C-02`, `REQ-F-02`, `REQ-F-21` |
| `SRC-02-01` | §2 · Tabla (cont.) | `get_eligible_options(trip_context)` — Lectura — "Entrega opciones candidatas, no una decisión … | `REQ-C-03`, `REQ-F-20` |
| `SRC-02-02` | §2 · Tabla | `get_policy_rules(scenario)` — Lectura — "Reglas versionadas y verificables." | `REQ-C-04`, `REQ-F-19` |
| `SRC-02-03` | §2 · Tabla | `create_rebooking_request(option, idempotency_key)` — Escritura — "Acción de alto impacto." | `REQ-C-05`, `REQ-F-04`, `REQ-F-17`, `REQ-F-23` |
| `SRC-02-04` | §2 · Tabla | `create_human_case(reason, evidence)` — Escritura — "Escalamiento a operación humana." | `REQ-C-06`, `REQ-F-04`, `REQ-F-26` |
| `SRC-02-05` | §2 · Tabla | `notify_passenger(message)` — Escritura — "No debe enviar información no validada." | `REQ-C-07`, `REQ-F-16`, `REQ-F-29` |
| `SRC-02-06` | Ejemplos de respuesta | "Estos ejemplos son representativos de lo que devuelven las tools. Úsalos como base de trabajo.… | `REQ-C-08` |
| `SRC-02-07` | Ejemplo | JSON de `get_trip_context("ABC123")` (completo; p. 2) | `REQ-C-01`, `REQ-F-22`, `REQ-F-30` |
| `SRC-02-08` | Ejemplo | JSON de `get_operational_events(["S1","S2"])` — inicio: `E-1001`, `E-1007` (continúa en p. 3) | `REQ-C-02`, `REQ-F-30` |
| `SRC-03-01` | Ejemplo (cont.) | Continuación de `get_operational_events`: `E-1012`, `E-2003`, `_meta` (con `sources_degraded`) | `REQ-C-02`, `REQ-F-30` |
| `SRC-03-02` | Ejemplo | JSON de `get_eligible_options(trip_context)` (O1, O2, O3 + `_meta.ttl_seconds`) | `REQ-C-03`, `REQ-F-20`, `REQ-F-25`, `REQ-F-30` |
| `SRC-03-03` | Ejemplo | JSON de `get_policy_rules("DELAY")` (R1–R5 + versión + `superseded_versions`) | `REQ-C-04`, `REQ-F-19`, `REQ-F-30` |
| `SRC-03-04` | Tools de escritura | `create_rebooking_request` → `201` / `409` / `503` (el comentario "el resultado real es indeter… | `REQ-C-05`, `REQ-F-23`, `REQ-F-24` |
| `SRC-04-01` | Tools de escritura | `503 { "error": "UPSTREAM_TIMEOUT" } // el resultado real es indeterminado` (p. 3–4) | `REQ-C-05`, `REQ-F-24` |
| `SRC-04-02` | Tools de escritura | `create_human_case` → `201 { case_id, queue, sla_minutes }` | `REQ-C-06`, `REQ-F-26` |
| `SRC-04-03` | Tools de escritura | `notify_passenger` → `202 { notification_id, channel, status }` · `422 { error: "UNVALIDATED_CO… | `REQ-C-07`, `REQ-F-16`, `REQ-F-19`, `REQ-F-29` |
| `SRC-04-04` | §3 Restricciones | "Los datos operacionales pueden estar desactualizados o ser contradictorios entre fuentes." | `REQ-F-21`, `REQ-N-01` |
| `SRC-04-05` | §3 | "Una recomendación incorrecta puede generar costo, un reclamo o el incumplimiento de una políti… | `REQ-F-18`, `REQ-N-02` |
| `SRC-04-06` | §3 | "Cambiar una reserva o emitir una compensación son acciones de alto impacto." | `REQ-F-17`, `REQ-N-03` |
| `SRC-04-07` | §3 | "Deben protegerse los datos personales y aplicarse mínimo privilegio." | `REQ-N-04` |
| `SRC-04-08` | §3 | "La primera versión debe poder ser operada por un equipo pequeño." | `REQ-N-05` |
| `SRC-04-09` | §3 | "Deben considerarse latencia, costo por interacción y dependencia de modelos." | `REQ-N-06` |
| `SRC-04-10` | §3 | "No existe una única solución correcta." | `REQ-N-07` |
| `SRC-04-11` | §4 Ambigüedades | "El enunciado no las define a propósito. Puedes decidirlas, documentarlas o explicitar qué preg… | `REQ-P-11` |
| `SRC-04-12` | §4 (AMB-01) | "Qué se considera una modificación relevante." | `AMB-01`, `REQ-F-11` |
| `SRC-04-13` | §4 (AMB-02) | "Qué información puede mostrarse al pasajero y cuál no." | `AMB-02`, `REQ-F-12` |
| `SRC-04-14` | §4 (AMB-03) | "En qué casos una recomendación puede entregarse de forma automática." | `AMB-03`, `REQ-F-13` |
| `SRC-04-15` | §4 (AMB-04) | "En qué casos debe intervenir una persona antes de actuar o comunicar." | `AMB-04`, `REQ-F-14` |
| `SRC-04-16` | §4 (AMB-05) | "Qué hacer cuando las fuentes entregan información contradictoria." | `AMB-05`, `REQ-F-15` |
| `SRC-04-17` | §5 Tu tarea | "Diseña una primera versión acotada del producto. Debes implementar un vertical slice técnico e… | `REQ-D-01`, `REQ-F-07`, `REQ-F-08` |
| `SRC-04-18` | §5 · Track Backend/Integración | "implementa la lógica que resuelve el caso base — combinar reserva, eventos y políticas para de… | `REQ-D-05`, `REQ-F-05`, `REQ-F-07`, `REQ-F-30` |
| `SRC-04-19` | §5 · Track Frontend/Experience | "implementa la pantalla o flujo que vería el pasajero, consumiendo datos equivalentes a los que… | `REQ-D-05`, `REQ-F-08` |
| `SRC-04-20` | §5 | "No se espera que domines ambos tracks con la misma profundidad: el requisito es demostrar prof… | `REQ-F-09` |
| `SRC-04-21` | §5 · Tarea 1 | "Resuelve el caso base. A partir de la información disponible, determina qué ocurrió con el via… | `REQ-F-05`, `REQ-F-30` |
| `SRC-04-22` | §5 · Tarea 2 | "Diseña el manejo de una consulta ambigua o compleja en la que el sistema deba combinar reserva… | `REQ-F-06` |
| `SRC-04-23` | §5 · Tarea 3 (p. 4–5) | "Implementa tu vertical slice según el track elegido, y especifica —sin necesidad de implementa… | `REQ-F-09` |
| `SRC-05-01` | §5 · IA en el producto | "No es obligatorio incorporar IA en runtime. Si decides no hacerlo, explica qué beneficio esper… | `REQ-F-10` |
| `SRC-05-02` | §6 · Entregable 1 | "Tu vertical slice del track elegido, más diseño, contrato o pseudocódigo para la capa compleme… | `REQ-D-01`, `REQ-D-02`, `REQ-D-03`, `REQ-D-04`, `REQ-D-05`, `REQ-D-06` |
| `SRC-05-03` | §6 · Entregable 2 | "README de ingeniería (máx. 2 páginas): problema entendido y outcome esperado; supuestos y alca… | `REQ-D-07`, `REQ-D-09` |
| `SRC-05-04` | §6 · Entregable 3 | "AI Usage & Decision Note (máx. 1 página): herramientas de IA utilizadas y para qué; outputs ac… | `REQ-D-08` |
| `SRC-05-05` | §6 · Tabla de clasificación | "Puedes usar esta tabla para mostrar la clasificación de pasos que pide el README (también pued… | `REQ-D-09` |
| `SRC-05-06` | §7 · Cómo funciona el proceso | "Recibes el desafío → preparas tu propuesta (48 horas) → la entregas en el formato que elijas →… | `REQ-P-02`, `REQ-P-06` |
| `SRC-05-07` | §7 · Preparación (p. 5–6) | "Tienes 48 horas desde que recibes este documento para preparar y enviar tu propuesta. Las 48 h… | `REQ-P-02`, `REQ-P-03` |
| `SRC-06-01` | §7 · Preparación | "Las 3 horas incluyen el análisis del caso, la implementación, las validaciones y la documentac… | `REQ-P-01`, `REQ-P-04` |
| `SRC-06-02` | §7 · Entrega y formato | "Los tres entregables de la sección 6 son obligatorios en su contenido. Tú eliges el formato y … | `REQ-D-10`, `REQ-P-09` |
| `SRC-06-03` | §7 · Presentación | "La sesión con el comité se agenda dentro de las 48 horas hábiles siguientes a tu entrega y dur… | `REQ-D-11`, `REQ-P-05`, `REQ-P-06`, `REQ-P-07` |
| `SRC-06-04` | §7 · Preguntas y debate técnico | "Esta instancia forma parte integral de la evaluación. El comité podrá: preguntar por tus decis… | `REQ-P-08` |
| `SRC-06-05` | §7 · Uso de IA | "Puedes utilizar libremente LLMs, coding assistants, agentes, búsqueda, scripts, automatizacion… | `REQ-D-08`, `REQ-P-10` |
| `SRC-06-06` | §8 Cómo evaluamos | "La evaluación combina tus entregables con tu presentación y la conversación técnica. No se cen… | `REQ-E-09` |
| `SRC-06-07` | §8 | "No existe una única solución correcta. Una solución distinta a la que habríamos elegido no es … | `REQ-E-09`, `REQ-N-07` |
| `SRC-07-01` | Pensamiento de producto | "Cómo entiendes y acotas el problema, qué supuestos explicitas, qué resultado priorizas y cómo … | `REQ-E-01` |
| `SRC-07-02` | Fundamentos de ingeniería | "Coherencia técnica de lo que implementas: contratos, estados, errores, límites e integración c… | `REQ-E-02` |
| `SRC-07-03` | Desarrollo asistido por IA | "Cómo usas IA en tu proceso sin delegar el criterio: qué controles defines, qué verificas y qué… | `REQ-E-03` |
| `SRC-07-04` | Calidad, seguridad y confiabilidad | "Qué comprobaciones haces y cómo manejas fallos, permisos, datos sensibles y operación." | `REQ-E-04` |
| `SRC-07-05` | Priorización y evidencia | "Si concentras el tiempo en lo importante y dejas evidencia localizable y pendientes explícitos… | `REQ-E-05`, `REQ-F-28` |
| `SRC-07-06` | Juicio técnico y trade-offs | "Cómo comparas alternativas considerando consecuencias, costos, riesgos y reversibilidad." | `REQ-E-06` |
| `SRC-07-07` | Razonamiento agentic y control | "Dónde aporta valor un agente o la IA y dónde conviene lógica determinística o intervención hum… | `REQ-E-07`, `REQ-F-06` |
| `SRC-07-08` | Responsabilidad y adaptación | "Si asumes el resultado, reconoces límites y revisas tus decisiones ante información nueva dura… | `REQ-E-08` |
| `SRC-07-09` | Qué no evaluamos | "No penalizamos no terminar la capa complementaria al track elegido …, no usar IA en runtime, n… | `REQ-E-09`, `REQ-F-09`, `REQ-F-10` |
| `SRC-07-10` | Cierre | "Si algo del enunciado te resulta insuficiente para avanzar, esa también es información útil: d… | `REQ-P-11` |

**Cobertura:** 77 de 78 entradas citadas por al menos un requisito.
**Sin requisito propio:** `SRC-01-01`. Son enunciados de contexto/portada que no imponen una obligación por sí mismos.
