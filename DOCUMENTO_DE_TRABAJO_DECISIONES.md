# Documento de trabajo final — Decisiones del Caso A «Disruption Companion»

> Generado: 19-10-2026, 2:47:59 p. m. · Catálogo de decisiones v1.0 · **35 de 37 decididas** · 2 pendientes.
> Este documento relaciona **cada decisión de trabajo** con el **documento de requerimientos** (`03_Requerimientos/REQUERIMIENTOS.md`). Lo escrito aquí por ti reemplaza cualquier recomendación del análisis.

## 1. Resumen

| ID | Decisión | Tipo | Tu elección | ¿Sigue la recomendación? | ¿Incorpora info externa? |
|---|---|---|---|---|---|
| DEC-01 | Track a implementar | Interna | a | Sí | No |
| DEC-02 | Rol de la IA en tiempo de ejecución | Interna | a | Sí | No |
| DEC-03 | Formato de entrega y soporte de presentación | Interna | Otra | **No** | No |
| DEC-04 | Alcance del vertical slice | Interna | Otra | **No** | No |
| DEC-05 | ¿Qué es una «modificación relevante»? (AMB-01) | EXTERNA (revisión estricta) | b | Sí | **Sí** |
| DEC-06 | Medición del retraso y llegada nueva | Interna | a | Sí | No |
| DEC-07 | Derivación de «conexión perdida» y tiempo mínimo de conexión | Interna | d | Sí | No |
| DEC-08 | Zonas horarias y fechas | Interna | a | Sí | No |
| DEC-09 | Fuentes contradictorias y precedencia (AMB-05) | Interna | d | **No** | No |
| DEC-10 | Frescura y vigencia de los datos | Interna | **PENDIENTE** | — | — |
| DEC-11 | Datos parciales (`completeness: PARTIAL`) | Interna | Otra | **No** | No |
| DEC-12 | Evaluación segura de reglas y variables derivadas | Interna | b | Sí | No |
| DEC-13 | Precedencia entre reglas (R3 vs R5) y aprobación humana | Interna | a | Sí | No |
| DEC-14 | Qué se entrega de forma automática (AMB-03) | Interna | a | Sí | No |
| DEC-15 | Cuándo interviene una persona (AMB-04) | Interna | b, c, d, e, f, g, h, i | **No** | No |
| DEC-16 | Menores y grupos familiares (producto) | Interna | a | Sí | No |
| DEC-17 | Selección y presentación de opciones | Interna | a | Sí | No |
| DEC-18 | Ciclo de vida del rebooking: idempotencia, 409, 503 y PENDING_CONFIRMATION | Interna | a | Sí | No |
| DEC-19 | Alineación de tiempos: TTL, expiración y SLA humano | Interna | a | Sí | No |
| DEC-20 | Contrato de `notify_passenger` y validación del mensaje | Interna | **PENDIENTE** | — | — |
| DEC-21 | Información visible al pasajero y verificación de identidad (AMB-02) | Interna | a | Sí | No |
| DEC-22 | Datos personales, mínimo privilegio y «qué nunca va a un modelo» | Interna | a | Sí | No |
| DEC-23 | Trazabilidad, auditoría y retención | Interna | a | Sí | No |
| DEC-24 | Validación mínima, operación, latencia, costo y métrica de éxito | Interna | b | **No** | No |
| DEC-35 | Marco: cómo se incorporan las políticas externas | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-25 | Jurisdicción aplicable por segmento | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-26 | Umbral de cambio sin costo por retraso: 180 min (PDF) vs 31 min (la aerolínea) | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-27 | Asistencia durante la espera (comunicación, comida, alojamiento, traslado) | EXTERNA (revisión estricta) | b | Sí | No |
| DEC-28 | Reembolso, tarifas no reembolsables y plazos | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-29 | Compensación económica (R4) | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-30 | Causa del evento y exenciones (clima, fuerza mayor) | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-31 | Cancelaciones, adelantos y otros eventos | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-32 | Definición de «menor» (R5) y derechos asociados | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-33 | Plazo y contenido de la notificación al pasajero | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-34 | México y otros países fuera de la fuente | EXTERNA (revisión estricta) | a | Sí | No |
| DEC-36 | Idioma, tono y localización de mensajes | Interna | c | **No** | No |
| DEC-37 | Uso de IA en este trabajo y confidencialidad del enunciado | Interna | a | **No** | No |

**Pendientes:** DEC-10, DEC-20. Mientras no se decidan, **ninguna recomendación del análisis se considera aprobada**.

## 2. Decisiones de trabajo (detalle)

### A · Alcance y enfoque del ejercicio

#### DEC-01 · Track a implementar

- **Pregunta:** ¿Implementas el track Backend/Integración o el track Frontend/Experience? (el otro queda como diseño)
- **Tu elección:** a) Backend/Integración
  - *a)* Servicio o función que combina reserva, eventos y política, con manejo de errores y al menos un test. La experiencia del pasajero queda como especificación del mensaje.
- **Recomendación del análisis:** a) Backend/Integración — El valor del ejercicio está en la lógica de decisión y en cómo se tratan los datos defectuosos; eso es backend. La pantalla se puede especificar sin implementarla.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Define cuál de REQ-F-07 o REQ-F-08 se cumple y qué debe especificarse en REQ-F-09. Cambia el contenido de REQ-D-02.
- **Requerimientos relacionados:**
  - `REQ-F-07` — [Opción A — Backend/Integración] Implementar la lógica del caso base como servicio o función invocable, con manejo de errores y ≥ 1 validación o test.
  - `REQ-F-08` — [Opción B — Frontend/Experience] Implementar la pantalla o flujo del pasajero que consume datos equivalentes a los de las tools y muestra estado del viaje, alerta y recomendación, con ≥ 1 validación.
  - `REQ-F-09` — Especificar (sin implementar) la capa complementaria: si el track fue Backend → cómo se vería/comunicaría al pasajero (pantalla, wireframe o especificación del mensaje); si fue Frontend → qué contrato/lógica de backend asume. Profundidad en un track; capacidad de diseñar la integración.
  - `REQ-D-02` — El Entregable 1 indica el track elegido (Backend/Integración o Frontend/Experience) y por qué.
- **Trazabilidad:** SRC: SRC-04-17, SRC-04-18, SRC-04-19, SRC-04-20, SRC-05-02, SRC-07-02, SRC-07-07

#### DEC-02 · Rol de la IA en tiempo de ejecución

- **Pregunta:** ¿Se usa IA dentro del producto (runtime)? Si sí, ¿para qué? Si no, ¿cómo lo justificas?
- **Tu elección:** a) Sin IA en runtime (determinístico + plantillas validadas)
  - *a)* La decisión y los mensajes se generan con reglas y plantillas. La IA aparece solo como diseño para la consulta libre.
- **Recomendación del análisis:** a) Sin IA en runtime (determinístico + plantillas validadas) — El núcleo del slice debe ser verificable y determinístico. Se documenta b y c como capa AI-assisted opcional para la consulta ambigua (REQ-F-06), explicando por qué no se activa en v1.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** La consulta no será libre. El usuario entrará y se le meostrara los datos de contexto de su/sus viajes. Dependiendo de si get_operational_events, muestra algo inusual, no se le muestra nada al usuario. Es decir el ususario al entrar vera los datos de su viaje y si hay un problema (solo get_operational_events validados) si hay entonces se miararan las politicas, y se traeran todas, las que cumple y las que no.  Dependiendo de las politicas, se hace el análisis de las opciones realmente viables. Tal vez en este punto sería bueno usar una IA, pero en el diseño inicial al menos, si todo cuadra, no deberiamos llamar a una IA. Pero hay que hacer los análisis completos, es decir si se rompe algo o algo no cuadra. En primera version haría el análisis estatico, pero tal vez en este punto se puede usar un JEV para que calcule la probabilidad de la decisison y si es mayor a 95, tomarla. Pero por ahora el diseño debe ser estatico, tomando en cuenta, todo lo obsercvado en el análisis del caso.
- **Efecto sobre los requerimientos:** Define el contenido de REQ-F-10 (justificación) y la clasificación de pasos de REQ-D-09. Condiciona REQ-N-06 (latencia/costo) y REQ-N-04 (qué ve un modelo).
- **Requerimientos relacionados:**
  - `REQ-F-06` — Diseñar el manejo de una consulta ambigua o compleja que combine reserva, eventos y políticas: cómo se descompone el trabajo, qué contexto se recupera, qué queda determinístico, qué se resuelve con IA o agente, y dónde se detiene para pedir intervención humana.
  - `REQ-F-10` — Decidir y justificar el uso de IA en runtime; si no se incorpora, explicar qué beneficio se esperaba y por qué el riesgo, costo o complejidad no lo justifican.
  - `REQ-N-06` — Considerar latencia, costo por interacción y dependencia de modelos.
  - `REQ-D-09` — La clasificación de pasos (determinístico / AI-assisted / agentic / human) debe aparecer (en el README o en la presentación) con razón, riesgo y control/fallback. La tabla es opcional como formato.
- **Trazabilidad:** SRC: SRC-05-01, SRC-06-05, SRC-04-09, SRC-07-07, SRC-04-22 · GAP: GAP-22, GAP-24 · DAT: DAT-65, DAT-79

#### DEC-03 · Formato de entrega y soporte de presentación

- **Pregunta:** ¿En qué formato entregas los tres entregables y con qué soporte presentas los 10 minutos?
- **Tu elección:** Otra decisión (descrita en las notas)
- **Recomendación del análisis:** a) Repositorio + Markdown — Minimiza trabajo no evaluado y maximiza evidencia localizable (SRC-07-05).
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Tus notas / condiciones:** Repositorio + Markdown. La presentación se basará en el md de diseño técnico que generara SDD-WORKFLOW.
- **Efecto sobre los requerimientos:** Determina cómo se presentan REQ-D-07, REQ-D-08 y el soporte REQ-D-11.
- **Requerimientos relacionados:**
  - `REQ-P-09` — Formato y herramientas libres (repositorio, Markdown, PDF, documento, diagrama, demo); la estética no se evalúa; el contenido de los 3 entregables es obligatorio.
  - `REQ-P-06` — La sesión comienza con 10 min de presentación con el soporte que prefieras; no se exige presentación formal ni diapositivas; no se espera aplicación terminada ni despliegue.
  - `REQ-D-11` — Soporte de presentación (libre) que cubra REQ-P-07.
- **Trazabilidad:** SRC: SRC-01-05, SRC-06-02, SRC-06-03

#### DEC-04 · Alcance del vertical slice

- **Pregunta:** ¿Qué cubre exactamente el slice dentro de las 3 horas?
- **Tu elección:** Otra decisión (descrita en las notas)
- **Recomendación del análisis:** b) Caso base + casos borde críticos — El ejercicio mide criterio, no volumen (SRC-01-08). Los casos borde críticos muestran control sin inventar datos.
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Tus notas / condiciones:** Los casos detectados. Se asumira que los eventos que aparecen son todos los eventos disponibles. Se debe solicitar los eventos y la documentracion completa de los endpoints que devuelven datos. PEro a paartie de los datos, esa es la fuente de verdad (universo conocido) Por lo que se debe generalizar esa interfaz. EL caso base será un test e2e. Se debe desarrollar desdpues del backend, una visualización simple de datos siguiendo un estilo visual como el de https://centro-ayuda.aerolinea.example/uy/es/centro-ayuda/preguntas/problemas-vuelo (tener ese look and feel) Y que muestre los datos (el backend entregara contexto, si hay problemas y botones para acciones que permitiran realizar la accion que solicite el ususario (revsion) Lo que me gustaría es que el el futuro el diseño fuera mas proactivo. En esta version, solo le mostraremos al usuario si tiene un problema. En una version futura, los evnetos operacionales deberían activar notificaciones de revision al usuario (pero eso sera otra fase)
- **Efecto sobre los requerimientos:** Fija el alcance de REQ-D-04 y la lista de pruebas de REQ-D-05; delimita REQ-F-00.
- **Requerimientos relacionados:**
  - `REQ-F-00` — Alcance v1: ayudar a pasajeros cuyo vuelo sufrió una modificación.
  - `REQ-F-05` — Resolver el caso base: a partir de la información disponible (reserva + eventos + políticas), determinar qué ocurrió y qué corresponde ofrecer o comunicar.
  - `REQ-D-04` — El Entregable 1 declara el alcance efectivamente implementado.
  - `REQ-P-01` — El trabajo efectivo tiene un máximo de 3 horas e incluye análisis, implementación, validaciones y documentación.
- **Trazabilidad:** SRC: SRC-01-09, SRC-04-21, SRC-04-23, SRC-06-01 · GAP: GAP-07 · DAT: DAT-18, DAT-82

### B · Interpretación del caso y de los datos

#### DEC-05 · ¿Qué es una «modificación relevante»? (AMB-01)  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Con qué criterio el sistema decide que un evento es una modificación relevante para el pasajero?
- **Tu elección:** b) Por impacto en el itinerario (con umbral configurable)
  - *b)* Relevante si hay cancelación, retraso o adelanto sobre un umbral, conexión perdida, o cambio de aeropuerto o fecha. El cambio de puerta se informa como dato, sin tratarlo como modificación relevante.
- **Recomendación del análisis:** b) Por impacto en el itinerario (con umbral configurable) — Es la lectura más cercana a 'entienda si hubo una modificación relevante y qué implica' (SRC-01-13). El umbral queda como parámetro y su valor depende de DEC-26.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** El umbral es configurable dinamicamente por las politicas. Las politicas indican el umbral . SOlo dejaría una nota en la presentación que las poliitcias publicadas no pueden entrar en conflicto con las politicas de sistema. Pero a efectos de este desafío las politicas del WS son los que valen. Omitiremos las políticas externas (reales) solo desafio.
- **Efecto sobre los requerimientos:** Define el criterio de REQ-F-11 y la salida de REQ-F-02. Depende de DEC-26 y DEC-31.
- **Requerimientos relacionados:**
  - `REQ-F-02` — El pasajero puede entender si hubo una modificación relevante y qué implica.
  - `REQ-F-11` — Definir qué se considera una modificación relevante (AMB-01).
- **Trazabilidad:** SRC: SRC-04-12, SRC-01-13 · AMB: AMB-01 · GAP: GAP-02, GAP-07 · DAT: DAT-15, DAT-23
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-UY-01` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Retraso de 31 min o más y no conforme: cambio sin costo (mismo destino y cabina, 12 meses) o devolución sin cargo.
  - `POL-UY-02` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Adelanto de 16 min o más: mismas opciones que el retraso.
  - `POL-CL-03` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Desde 31 min de atraso: cambio (fecha, hora o destino, misma cabina) o devolución.
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** **Sí** — autorizaste usar los insumos externos listados.

#### DEC-06 · Medición del retraso y llegada nueva

- **Pregunta:** ¿El retraso que usan las reglas es de salida o de llegada, y cómo se obtiene la llegada nueva?
- **Tu elección:** a) Usar el retraso de salida y derivar la llegada por propagación
  - *a)* Las reglas usan `delay_minutes` (salida). La llegada se deriva sumando el retraso a la llegada programada (supuesto A1) y se etiqueta como derivada.
- **Recomendación del análisis:** a) Usar el retraso de salida y derivar la llegada por propagación — Es el supuesto más simple y declarable; el resultado se presenta como estimación y exige confirmación antes de actuar (DEC-13).
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Siempre y cuando no aparezca como source_degraded. Asumiremos que el delayes no se recupera.
- **Efecto sobre los requerimientos:** Define cómo se obtiene la variable `delay_minutes` y la llegada usada en REQ-F-30c.
- **Requerimientos relacionados:**
  - `REQ-F-02` — El pasajero puede entender si hubo una modificación relevante y qué implica.
  - `REQ-F-30` — Resultado esperado del caso base ABC123 (hipótesis; sub-resultados F-30a…h).
- **Trazabilidad:** SRC: SRC-03-03, SRC-02-08 · GAP: GAP-15 · DAT: DAT-19, DAT-54, DAT-75

#### DEC-07 · Derivación de «conexión perdida» y tiempo mínimo de conexión

- **Pregunta:** ¿Cómo se decide que `missed_connection` es verdadero si no es un dato y falta el tiempo mínimo de conexión (MCT)?
- **Tu elección:** d) Derivar (b) y exigir confirmación humana antes de actuar
  - *d)* El resultado se marca como estimado; el rebooking no se ejecuta sin confirmar.
- **Recomendación del análisis:** d) Derivar (b) y exigir confirmación humana antes de actuar — La derivación es útil pero no es un dato; por eso se muestra como estimación y la acción de alto impacto queda sujeta a confirmación.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Debe levantarse la necesidad del dato que falta para segunda etapa. Además debe consultarse cual es el minimo tiempo de escala. En la practica un pasajero no llegara de una puerta a otra instantaneamente, el tiempo de dtransito debe ser contemplado y debe solicitarse explicitamente para reducir la llamada a soporte.
- **Efecto sobre los requerimientos:** Define cómo se calcula la variable de R3 en REQ-F-30c y cómo se comunica (REQ-F-16).
- **Requerimientos relacionados:**
  - `REQ-F-30` — Resultado esperado del caso base ABC123 (hipótesis; sub-resultados F-30a…h).
  - `REQ-F-18` — Las recomendaciones deben ser exactas: una incorrecta genera costo, reclamo o incumplimiento de política.
- **Trazabilidad:** SRC: SRC-02-07, SRC-03-03 · GAP: GAP-11 · DAT: DAT-07, DAT-45, DAT-75

#### DEC-08 · Zonas horarias y fechas

- **Pregunta:** ¿Cómo se tratan las horas «HH:MM» sin zona horaria?
- **Tu elección:** a) Local del aeropuerto + comparar solo dentro del mismo aeropuerto + UTC para edades
  - *a)* Se usa una tabla mínima versionada IATA→zona (SCL, LIM, MEX) solo cuando haya que convertir.
- **Recomendación del análisis:** a) Local del aeropuerto + comparar solo dentro del mismo aeropuerto + UTC para edades — Evita errores sin cambiar contratos; la conexión (el caso crítico) no necesita zonas.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Fija cómo se calculan las edades de datos (REQ-F-21) y la aritmética de fechas.
- **Requerimientos relacionados:**
  - `REQ-F-21` — Controlar timestamp, fuente y frescura de los eventos operacionales.
- **Trazabilidad:** SRC: SRC-02-07, SRC-02-08 · GAP: GAP-15 · DAT: DAT-05, DAT-06, DAT-20

#### DEC-09 · Fuentes contradictorias y precedencia (AMB-05)

- **Pregunta:** ¿Qué regla se usa cuando dos fuentes dicen cosas distintas del mismo segmento?
- **Tu elección:** d) Siempre humano ante conflicto
  - *d)* Cualquier contradicción escala.
- **Recomendación del análisis:** a) Regla compuesta — Es la única que evita mostrar ON_TIME y a la vez maneja los casos que no son tan claros como el del ejemplo.
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Tus notas / condiciones:** Gana el veneto mas reciente si no es source_degraded. Si hay dos eventos contradictorios sin source_degraded, va a soporte.
- **Efecto sobre los requerimientos:** Define el contenido de REQ-F-15 y la condición de bloqueo de REQ-F-16 cuando hay conflicto.
- **Requerimientos relacionados:**
  - `REQ-F-15` — Definir qué hacer cuando las fuentes entregan información contradictoria (AMB-05).
  - `REQ-F-21` — Controlar timestamp, fuente y frescura de los eventos operacionales.
  - `REQ-N-01` — Los datos operacionales pueden estar desactualizados o ser contradictorios entre fuentes.
- **Trazabilidad:** SRC: SRC-04-16, SRC-04-04, SRC-01-18 · AMB: AMB-05 · GAP: GAP-16 · DAT: DAT-15, DAT-16, DAT-26

#### DEC-10 · Frescura y vigencia de los datos

- **Pregunta:** ¿Qué antigüedad máxima se tolera para informar y para actuar?
- **Tu elección:** **PENDIENTE**
- **Recomendación del análisis:** a) Umbrales distintos por tipo de uso — El riesgo de un dato viejo es mayor al ejecutar que al informar.
- **Tus notas / condiciones:** Usar el dato mas reciente, respetar TTL. Volver a consultar dato si esta vencido.
- **Efecto sobre los requerimientos:** Fija parámetros de REQ-F-21 y REQ-F-25 y la regla DQ-14/DQ-15.
- **Requerimientos relacionados:**
  - `REQ-F-21` — Controlar timestamp, fuente y frescura de los eventos operacionales.
  - `REQ-F-25` — Respetar la vigencia (TTL = 120 s) de las opciones; no actuar con opciones vencidas.
- **Trazabilidad:** SRC: SRC-01-18, SRC-03-02 · GAP: GAP-16 · DAT: DAT-17, DAT-35

#### DEC-11 · Datos parciales (`completeness: PARTIAL`)

- **Pregunta:** ¿Qué se puede hacer y decir cuando faltan campos?
- **Tu elección:** Otra decisión (descrita en las notas)
- **Recomendación del análisis:** a) Condicionar cada afirmación a los campos que necesita — Es lo que permite 'tolerar información parcial' sin inventar.
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Tus notas / condiciones:** Este campo es de get_trip_context, solo es información de contexto. Solo nos molestará si necesitamos tomar decisiones y hay un acontradiccion. En ese caso, atención humana.
- **Efecto sobre los requerimientos:** Define la tabla de gating de REQ-F-22 y la regla DQ-28.
- **Requerimientos relacionados:**
  - `REQ-F-22` — Tolerar información parcial del contexto (completeness: PARTIAL) y declararla.
- **Trazabilidad:** SRC: SRC-01-17, SRC-02-07 · GAP: GAP-17 · DAT: DAT-09

#### DEC-12 · Evaluación segura de reglas y variables derivadas

- **Pregunta:** ¿Cómo se evalúan las `condition` (texto) y se derivan las cuatro variables que no vienen en los datos?
- **Tu elección:** b) Parser acotado con lista blanca
  - *b)* Solo reconoce identificadores conocidos, `>=`, `==` y `AND`; lo demás es error.
- **Recomendación del análisis:** b) Parser acotado con lista blanca — Un parser mínimo con lista blanca es pequeño, generaliza a reglas nuevas y falla de forma segura. Si falta tiempo, a es el respaldo.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Pero el parser además debe tener todas las operaciones  de comparacion numerica >=, >,<, <=, ==, EQ, AND, OR
- **Efecto sobre los requerimientos:** Define cómo se implementa REQ-F-19 y registra cada variable derivada como DERIVADA con sus supuestos (REQ-F-28).
- **Requerimientos relacionados:**
  - `REQ-F-19` — Usar reglas versionadas y verificables; el mensaje debe llevar policy_ref (el servicio rechaza con 422 UNVALIDATED_CONTENT si falta).
- **Trazabilidad:** SRC: SRC-03-03 · GAP: GAP-18 · DAT: DAT-45, DAT-48

#### DEC-13 · Precedencia entre reglas (R3 vs R5) y aprobación humana

- **Pregunta:** Si R3 no exige aprobación pero R5 sí (hay un menor), ¿se puede ejecutar el rebooking?
- **Tu elección:** a) Gana la regla más restrictiva (L2)
  - *a)* Si cualquier regla aplicable exige aprobación humana, el caso completo queda pendiente de esa aprobación.
- **Recomendación del análisis:** a) Gana la regla más restrictiva (L2) — Con un menor y una acción de alto impacto, la lectura conservadora es la defendible en v1.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** La politica indica si se puede hacer automaticamente.
- **Efecto sobre los requerimientos:** Define la regla de combinación que usa REQ-F-17 y los disparadores de REQ-F-14. Condiciona el resultado esperado REQ-F-30g.
- **Requerimientos relacionados:**
  - `REQ-F-17` — No ejecutar acciones de alto impacto sin los controles correspondientes (cambiar una reserva; emitir una compensación).
  - `REQ-F-14` — Definir en qué casos debe intervenir una persona antes de actuar o comunicar (AMB-04).
- **Trazabilidad:** SRC: SRC-03-03, SRC-04-06 · AMB: AMB-03, AMB-04 · GAP: GAP-19 · DAT: DAT-46, DAT-47

### C · Autonomía, intervención humana y acciones

#### DEC-14 · Qué se entrega de forma automática (AMB-03)

- **Pregunta:** ¿Qué acciones y mensajes puede producir el sistema sin intervención humana?
- **Tu elección:** a) Automático solo informar y explicar con hechos validados
  - *a)* Estado del viaje, explicación de la modificación y propuesta de siguiente paso (como propuesta). Toda escritura requiere confirmación humana en v1.
- **Recomendación del análisis:** a) Automático solo informar y explicar con hechos validados — Equilibra el objetivo de reducir contactos con las restricciones de control (SRC-01-10, SRC-04-06).
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** El pasajero confirma siempre, el elige que hacer, nosostros le damos las opciones viables, que nos permiten las politicas, con datos verificados.
- **Efecto sobre los requerimientos:** Define la matriz acción × condiciones de REQ-F-13 y qué escrituras requieren REQ-F-17.
- **Requerimientos relacionados:**
  - `REQ-F-13` — Definir en qué casos una recomendación puede entregarse de forma automática (AMB-03).
  - `REQ-F-17` — No ejecutar acciones de alto impacto sin los controles correspondientes (cambiar una reserva; emitir una compensación).
- **Trazabilidad:** SRC: SRC-04-14, SRC-01-10 · AMB: AMB-03 · DAT: DAT-47

#### DEC-15 · Cuándo interviene una persona (AMB-04)

- **Pregunta:** ¿Qué situaciones obligan a crear un caso humano antes de actuar o comunicar? (selección múltiple)
- **Tu elección:** b) El pasajero solicita compensación (R4) · c) Datos parciales que bloquean la afirmación · d) Fuentes en conflicto sin resolver · e) Resultado indeterminado (503) · f) Evento de tipo desconocido · g) Ninguna opción cubre a todo el grupo · h) Pernocte u otra asistencia no cubierta por la política · i) Se solicitan datos personales
  - *b)* Siempre caso humano, sin montos.
  - *c)* Si falta un campo necesario para el mensaje.
  - *d)* Según DEC-09 punto 4.
  - *e)* Tras reintentos acotados.
  - *f)* Por ejemplo cancelación si no está soportada.
  - *g)* Cupos menores que pasajeros.
  - *h)* Alojamiento, comidas, traslados.
  - *i)* Documento, correo, teléfono.
- **Recomendación del análisis:** a) Hay un menor en el grupo (R5) · b) El pasajero solicita compensación (R4) · c) Datos parciales que bloquean la afirmación · d) Fuentes en conflicto sin resolver · e) Resultado indeterminado (503) · f) Evento de tipo desconocido · g) Ninguna opción cubre a todo el grupo · h) Pernocte u otra asistencia no cubierta por la política · i) Se solicitan datos personales — Son los puntos donde el sistema carece de dato, de regla o de control; escalar es lo defendible. La lista es ajustable casilla por casilla.
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Efecto sobre los requerimientos:** Convierte AMB-04 en disparadores explícitos de REQ-F-14 y define cuándo se invoca REQ-F-26.
- **Requerimientos relacionados:**
  - `REQ-F-14` — Definir en qué casos debe intervenir una persona antes de actuar o comunicar (AMB-04).
  - `REQ-F-26` — Escalar a operación humana con razón y evidencia mediante create_human_case (cola DISRUPTION_L2, SLA 45 min en el ejemplo).
  - `REQ-F-04` — El pasajero puede ser derivado a una persona, o iniciar una acción controlada, cuando corresponda.
- **Trazabilidad:** SRC: SRC-04-15, SRC-02-04 · AMB: AMB-04 · GAP: GAP-26 · DAT: DAT-64

#### DEC-16 · Menores y grupos familiares (producto)

- **Pregunta:** ¿Cómo trata el producto un grupo con menor al ofrecer y ejecutar opciones?
- **Tu elección:** a) Regla dura: nunca separar al grupo
  - *a)* Solo se ofrecen y ejecutan opciones que cubran a todo el grupo juntos; con un menor siempre se abre caso humano antes de rebookear.
- **Recomendación del análisis:** a) Regla dura: nunca separar al grupo — Es la lectura más segura de 'cambiar una reserva es de alto impacto' con un menor.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Nunca separar al grupo, pero esto solo restringe las opciones que se le pueden presentar al usuario. Debe explicitarse en el mensaje al usuario que no se estan mostrando opciones que dejan al menor solo) contacr sopsrte.
- **Efecto sobre los requerimientos:** Añade una restricción explícita a REQ-F-17 y a la selección de opciones (REQ-F-20).
- **Requerimientos relacionados:**
  - `REQ-F-17` — No ejecutar acciones de alto impacto sin los controles correspondientes (cambiar una reserva; emitir una compensación).
  - `REQ-F-14` — Definir en qué casos debe intervenir una persona antes de actuar o comunicar (AMB-04).
- **Trazabilidad:** SRC: SRC-03-02, SRC-03-03 · GAP: GAP-08, GAP-20 · DAT: DAT-03, DAT-31, DAT-43, DAT-62

#### DEC-17 · Selección y presentación de opciones

- **Pregunta:** ¿Qué opciones ve el pasajero y cómo se trata `confidence`?
- **Tu elección:** a) Mostrar solo opciones viables y coherentes, más la vía de reembolso como alternativa
  - *a)* O1 como propuesta principal; la devolución como otra vía sin montos ni plazos; O2 no se muestra (se registra por qué).
- **Recomendación del análisis:** a) Mostrar solo opciones viables y coherentes, más la vía de reembolso como alternativa — La viabilidad (cupos, costo, política) se valida; `confidence` se usa solo para ordenar, nunca para decidir.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Las opciones viables son las opciones que despues de aplicar politicas son viables y que en su logica, no rompen otra politica.
- **Efecto sobre los requerimientos:** Define el filtro de REQ-F-20 y el contenido del mensaje de REQ-F-03.
- **Requerimientos relacionados:**
  - `REQ-F-20` — Las opciones son candidatas, no una decisión final: el sistema selecciona y valida.
  - `REQ-F-03` — El pasajero recibe una explicación o recomendación accionable (qué ocurrió y cuál es su siguiente paso).
- **Trazabilidad:** SRC: SRC-02-01, SRC-03-02 · GAP: GAP-17, GAP-20 · DAT: DAT-31, DAT-32, DAT-33, DAT-36

#### DEC-18 · Ciclo de vida del rebooking: idempotencia, 409, 503 y PENDING_CONFIRMATION

- **Pregunta:** ¿Cómo se diseñan la llave idempotente y el manejo de 409/503, y qué se hace con PENDING_CONFIRMATION?
- **Tu elección:** a) Llave determinista persistida antes de llamar; 503 → mismos reintentos acotados → caso humano; 409 → existente
  - *a)* Llave derivada de la operación (reserva + vuelo/fecha + versión de política + decisión). 503: hasta 2 reintentos con la misma llave y luego caso humano, sin decirle al pasajero ni éxito ni fracaso. 409: tratar como solicitud existente. PENDING_CONFIRMATION: confirmación fuera de alcance de v1, documentada como supuesto.
- **Recomendación del análisis:** a) Llave determinista persistida antes de llamar; 503 → mismos reintentos acotados → caso humano; 409 → existente — Es la única variante que respeta que 503 es indeterminado y que el rebooking es de alto impacto.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Fija el contenido de REQ-F-23 y REQ-F-24 y la extensión documentada del contrato (reserva y pasajeros) de REQ-C-05.
- **Requerimientos relacionados:**
  - `REQ-F-23` — Idempotencia en create_rebooking_request con idempotency_key.
  - `REQ-F-24` — Manejar 409 DUPLICATE_REQUEST (existente) y 503 UPSTREAM_TIMEOUT (resultado indeterminado).
  - `REQ-C-05` — Contrato de create_rebooking_request(option, idempotency_key) — "Acción de alto impacto."
- **Trazabilidad:** SRC: SRC-02-03, SRC-03-04, SRC-04-01 · GAP: GAP-12 · DAT: DAT-59, DAT-60, DAT-61, DAT-62, DAT-63

#### DEC-19 · Alineación de tiempos: TTL, expiración y SLA humano

- **Pregunta:** ¿Cómo se concilian opciones que vencen en 2 min, una solicitud que expira en ~9 min y un caso humano con SLA de 45 min?
- **Tu elección:** a) Revalidar todo justo antes de escribir
  - *a)* La aprobación humana autoriza una decisión (qué opción), no la ejecución con datos viejos; al aprobar se recuperan de nuevo opciones y política. El mensaje dice «sujeto a disponibilidad».
- **Recomendación del análisis:** a) Revalidar todo justo antes de escribir — No hay mecanismo de reserva en el contrato; revalidar es lo único coherente.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** No deberia pasar por que cuando el usuario entra se le muestran los datos recien obtenidos. Si entra de nuevo y los datos no han vencido no se vana  abuscar de nuevo (este cache va en segunda version) en la primera, siempre que el usuario entra, se llama al endpoint. Se debe mostrar en la web que la aceptacipn debe ocurrir antes de min(TTL), en otro caso esta sujeto a disponibilidad
- **Efecto sobre los requerimientos:** Añade el paso de revalidación a REQ-F-25 y REQ-F-26 y al flujo de aprobación.
- **Requerimientos relacionados:**
  - `REQ-F-25` — Respetar la vigencia (TTL = 120 s) de las opciones; no actuar con opciones vencidas.
  - `REQ-F-26` — Escalar a operación humana con razón y evidencia mediante create_human_case (cola DISRUPTION_L2, SLA 45 min en el ejemplo).
- **Trazabilidad:** SRC: SRC-03-02, SRC-03-04, SRC-04-02 · GAP: GAP-25 · DAT: DAT-35, DAT-58, DAT-77

#### DEC-20 · Contrato de `notify_passenger` y validación del mensaje

- **Pregunta:** ¿Cómo se construyen y validan los mensajes, y a quién se envían si la firma no incluye destinatario?
- **Tu elección:** **PENDIENTE**
- **Recomendación del análisis:** a) Plantillas con hechos validados + `policy_ref` + destinatario (extensión del contrato) — Es la forma de cumplir REQ-F-16 con evidencia verificable por tests (TC-16).
- **Tus notas / condiciones:** El mensaje al usuario se muestra como confirmación. No lo usaremos. El ususario si entra ve el mensaje. El unico mensaje que le enviaremos al usuario en fase 2 es revise su cuienta acá por que han habido cambios en su vuelo.
- **Efecto sobre los requerimientos:** Define la capa complementaria de REQ-F-09 (especificación del mensaje) y el validador de REQ-F-29.
- **Requerimientos relacionados:**
  - `REQ-F-16` — No entregar información no verificada al pasajero; notify_passenger no debe enviar información no validada.
  - `REQ-F-29` — Validar mensajes antes de notificar: además del policy_ref exigido por el servicio, un validador propio que verifique que cada afirmación tiene evidencia vigente.
  - `REQ-F-09` — Especificar (sin implementar) la capa complementaria: si el track fue Backend → cómo se vería/comunicaría al pasajero (pantalla, wireframe o especificación del mensaje); si fue Frontend → qué contrato/lógica de backend asume. Profundidad en un track; capacidad de diseñar la integración.
  - `REQ-C-07` — Contrato de notify_passenger(message) — "No debe enviar información no validada."
- **Trazabilidad:** SRC: SRC-02-05, SRC-04-03 · GAP: GAP-13, GAP-22 · DAT: DAT-65, DAT-71

### D · Datos, seguridad y operación

#### DEC-21 · Información visible al pasajero y verificación de identidad (AMB-02)

- **Pregunta:** ¿Qué campos y hechos puede ver el pasajero, y cómo se sabe que es quien dice ser?
- **Tu elección:** a) Sesión ya autenticada (supuesto documentado) + lista blanca de campos
  - *a)* Se asume que el pasajero llega autenticado; se muestran segmentos, horarios, estado, opciones viables y derechos citados; nunca documento, correo, teléfono completo ni nivel de fidelidad; solo nombre de pila.
- **Recomendación del análisis:** a) Sesión ya autenticada (supuesto documentado) + lista blanca de campos — Acota v1 sin exponer datos y deja la dependencia explícita.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Define la lista blanca de REQ-F-12 y el supuesto de REQ-F-01.
- **Requerimientos relacionados:**
  - `REQ-F-12` — Definir qué información puede mostrarse al pasajero y cuál no (AMB-02).
  - `REQ-F-01` — El pasajero puede consultar el contexto de su viaje.
  - `REQ-N-04` — Proteger datos personales y aplicar mínimo privilegio.
- **Trazabilidad:** SRC: SRC-04-13, SRC-04-07, SRC-01-12 · AMB: AMB-02 · GAP: GAP-21 · DAT: DAT-01

#### DEC-22 · Datos personales, mínimo privilegio y «qué nunca va a un modelo»

- **Pregunta:** ¿Dónde se aplica la minimización de PII y qué información nunca se entrega a un modelo?
- **Tu elección:** a) Mantener las firmas y minimizar en todas las fronteras que controlas
  - *a)* Contexto mínimo para decidir (sin correo, teléfono, documento, nivel de fidelidad; nombre de pila; `has_minor` como booleano); logs enmascarados; evidencia de casos humanos solo con ids y hechos; ningún dato personal a un modelo. Se propone al equipo un contrato reducido para `get_eligible_options`.
- **Recomendación del análisis:** a) Mantener las firmas y minimizar en todas las fronteras que controlas — Es la lectura que cumple las dos instrucciones del PDF; la lista de lo que nunca va a un modelo alimenta el Entregable 3.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** No podemos enviar ningun dato, a un modelo LLM , se debe anonimizar los datos antes de enviar.
- **Efecto sobre los requerimientos:** Define el inventario de REQ-N-04, el límite de REQ-F-27 y el contenido de REQ-D-08 (d).
- **Requerimientos relacionados:**
  - `REQ-N-04` — Proteger datos personales y aplicar mínimo privilegio.
  - `REQ-F-27` — Si se usan mocks propios, mantener los contratos de las tools.
  - `REQ-D-08` — Entregable 3 — AI Usage & Decision Note (máx. 1 pág.): (a) herramientas de IA usadas y para qué; (b) outputs aceptados, rechazados o modificados y cómo se validaron; (c) decisiones tomadas personalmente; (d) qué información nunca se entregaría a un modelo.
- **Trazabilidad:** SRC: SRC-04-07, SRC-01-16, SRC-05-04 · GAP: GAP-27 · DAT: DAT-02, DAT-38, DAT-79

#### DEC-23 · Trazabilidad, auditoría y retención

- **Pregunta:** ¿Qué se registra de cada decisión y por cuánto tiempo?
- **Tu elección:** a) Registro de decisión estructurado y sin PII
  - *a)* Un `decision_id` que ata: lecturas usadas con su `retrieved_at`, eventos elegidos y descartados con razón, versión de política y regla, variables derivadas con supuestos, opción, acción, mensaje y hashes. La retención es un parámetro a definir.
- **Recomendación del análisis:** a) Registro de decisión estructurado y sin PII — Es lo que permite defender cada decisión en el debate técnico.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Deberia estar asociado al booking_id. Nunca loguear datos personales., deben estar truncados y nunca exponer edad de menor ni nombre. ni rut.
- **Efecto sobre los requerimientos:** Define el contenido de REQ-F-28 y la evidencia de REQ-E-05.
- **Requerimientos relacionados:**
  - `REQ-F-28` — Trazabilidad: cada decisión/acción debe poder reconstruirse (datos usados con su retrieved_at, versión de política y rule_id, evento(s) elegido(s) y descartado(s), opción, acción, mensaje).
  - `REQ-N-08` — Mantener exactitud, seguridad y trazabilidad.
- **Trazabilidad:** SRC: SRC-01-11, SRC-07-05 · GAP: GAP-27 · DAT: DAT-73, DAT-80

#### DEC-24 · Validación mínima, operación, latencia, costo y métrica de éxito

- **Pregunta:** ¿Qué pruebas, presupuestos y métricas se declaran?
- **Tu elección:** b) Batería amplia (TC-01 a TC-20)
  - *b)* Todas las pruebas sugeridas.
- **Recomendación del análisis:** a) Conjunto crítico + métricas propuestas + runbook de una página — Prioriza evidencia donde más importa (SRC-07-05).
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Efecto sobre los requerimientos:** Fija REQ-D-05, los presupuestos de REQ-N-05/06 y la métrica de REQ-N-09.
- **Requerimientos relacionados:**
  - `REQ-D-05` — El Entregable 1 lista tests o validaciones disponibles (y el slice incluye ≥ 1 validación o test).
  - `REQ-N-05` — La primera versión debe poder ser operada por un equipo pequeño.
  - `REQ-N-06` — Considerar latencia, costo por interacción y dependencia de modelos.
  - `REQ-N-09` — Resultado de negocio: reducir la incertidumbre del pasajero y los contactos evitables al call center. (No hay métrica definida.)
  - `REQ-E-01` — Pensamiento de producto: cómo entiendes y acotas, qué supuestos explicitas, qué priorizas y cómo lo medirías.
  - `REQ-E-04` — Calidad, seguridad y confiabilidad: comprobaciones, fallos, permisos, datos sensibles, operación.
- **Trazabilidad:** SRC: SRC-01-02, SRC-04-08, SRC-04-09, SRC-07-01, SRC-07-04 · GAP: GAP-23, GAP-24

### E · Políticas externas (REVISIÓN ESTRICTA)

#### DEC-35 · Marco: cómo se incorporan las políticas externas  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Las políticas de la aerolínea y las normas por país son fuente de verdad del producto, solo contexto, o se ignoran?
- **Tu elección:** a) Solo contexto: el producto usa únicamente `get_policy_rules`
  - *a)* Las políticas externas sirven para identificar brechas, riesgos y preguntas (README: supuestos y próximos pasos), no como reglas del motor.
- **Recomendación del análisis:** a) Solo contexto: el producto usa únicamente `get_policy_rules` — Es la opción defendible con el tiempo y la información disponibles: el PDF no pide derecho comparado, pero la defensa gana si se muestran las brechas y las preguntas.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Determina si REQ-F-19 se apoya solo en `get_policy_rules` y qué brechas GAP-01…10 pasan a «preguntas/próximos pasos» en el README (REQ-D-07).
- **Requerimientos relacionados:**
  - `REQ-P-11` — Si el enunciado es insuficiente, documentar el supuesto y por qué.
  - `REQ-N-07` — No existe una única solución correcta.
- **Trazabilidad:** SRC: SRC-02-02, SRC-04-11, SRC-04-10 · GAP: GAP-01, GAP-02, GAP-03, GAP-04, GAP-05, GAP-06, GAP-07, GAP-08, GAP-09, GAP-10, GAP-14
- **Insumos externos para esta decisión (para tu revisión):**
  - `LEEME` → `05_Politicas_Externas/00_LEEME_Politicas.md` — Estado de captura de cada fuente y qué país importa para el caso (§3).
  - `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-25 · Jurisdicción aplicable por segmento  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Qué ley o política de país se considera para S1 (SCL→LIM) y para S2 (LIM→MEX)?
- **Tu elección:** a) Solo `get_policy_rules`; jurisdicción como punto de extensión
  - *a)* v1 no aplica ley por país; se deja el campo `jurisdiction` previsto y la pregunta documentada para Producto/Legal.
- **Recomendación del análisis:** a) Solo `get_policy_rules`; jurisdicción como punto de extensión — Con el dato disponible no se puede decidir jurisdicción sin inventar. Se documenta como supuesto bloqueante («qué preguntarías y a quién»: SRC-04-11) y se prevé la extensión.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Define el alcance de REQ-F-19 y la lista de preguntas del README (REQ-D-07 b, e). Condiciona DEC-26 a DEC-33.
- **Requerimientos relacionados:**
  - `REQ-F-19` — Usar reglas versionadas y verificables; el mensaje debe llevar policy_ref (el servicio rechaza con 422 UNVALIDATED_CONTENT si falta).
  - `REQ-F-18` — Las recomendaciones deben ser exactas: una incorrecta genera costo, reclamo o incumplimiento de política.
- **Trazabilidad:** SRC: SRC-03-03 · GAP: GAP-01, GAP-14 · DAT: DAT-51 · POL: POL-CL-00, POL-PE-01, POL-PE-16
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-CL-00` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Las soluciones valen solo en Chile (vuelos con origen en Chile).
  - `POL-PE-01` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Decisión 619 art. 2: aplica a quien inicia su viaje en un país andino, o es transferido allí por el transportista.
  - `POL-PE-16` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 24: no se pueden imponer condiciones inferiores a las de la Decisión.
  - `LEEME` → `05_Politicas_Externas/00_LEEME_Politicas.md` — Estado de captura de cada fuente y qué país importa para el caso (§3).
  - `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-26 · Umbral de cambio sin costo por retraso: 180 min (PDF) vs 31 min (la aerolínea)  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Se sigue R1 (≥ 180 min) o se adopta el umbral comercial de la aerolínea (≥ 31 min)?
- **Tu elección:** a) Seguir R1 como regla del producto y documentar la discrepancia
  - *a)* El README registra que la política comercial publicada es más favorable y plantea la pregunta a Producto/Legal.
- **Recomendación del análisis:** a) Seguir R1 como regla del producto y documentar la discrepancia — En el caso base lo que otorga el cambio sin costo es R3 (conexión), no R1; la discrepancia se declara sin alterar la política del PDF.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Omitir el conocimiento de reglas externas, no aplica a version 1 de este desafio.
- **Efecto sobre los requerimientos:** Fija el umbral de REQ-F-11 y su justificación; relacionado con DEC-05.
- **Requerimientos relacionados:**
  - `REQ-F-11` — Definir qué se considera una modificación relevante (AMB-01).
  - `REQ-F-18` — Las recomendaciones deben ser exactas: una incorrecta genera costo, reclamo o incumplimiento de política.
- **Trazabilidad:** SRC: SRC-03-03, SRC-04-12 · GAP: GAP-02 · DAT: DAT-46, DAT-55 · POL: POL-UY-01, POL-CL-02, POL-CL-03
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-UY-01` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Retraso de 31 min o más y no conforme: cambio sin costo (mismo destino y cabina, 12 meses) o devolución sin cargo.
  - `POL-CL-02` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Atraso de más de 3 h y decide no volar: devolución de pasaje y tasas.
  - `POL-CL-03` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Desde 31 min de atraso: cambio (fecha, hora o destino, misma cabina) o devolución.
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-27 · Asistencia durante la espera (comunicación, comida, alojamiento, traslado)  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Qué se dice sobre asistencia si la política del PDF solo tiene un vale de comida a ≥ 240 min internacional?
- **Tu elección:** b) Mensaje genérico + caso humano si hay pernocte
  - *b)* «Podrías tener derecho a asistencia; un agente lo confirmará», sin cifras; se abre caso humano por el pernocte.
- **Recomendación del análisis:** b) Mensaje genérico + caso humano si hay pernocte — El pernocte es un hecho derivable de los datos (O1 sale al día siguiente); decirlo sin cifras ni promesas es veraz.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Añade a REQ-F-18/REQ-F-03 la mención cautelosa de asistencia y el disparador de caso humano por pernocte (REQ-F-14).
- **Requerimientos relacionados:**
  - `REQ-F-18` — Las recomendaciones deben ser exactas: una incorrecta genera costo, reclamo o incumplimiento de política.
  - `REQ-F-03` — El pasajero recibe una explicación o recomendación accionable (qué ocurrió y cuál es su siguiente paso).
- **Trazabilidad:** SRC: SRC-03-03 · GAP: GAP-03 · DAT: DAT-39, DAT-55 · POL: POL-CL-01, POL-CL-04, POL-PE-07, POL-CO-04, POL-UYN-02, POL-AR-03
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-CL-01` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Atraso en aeropuerto: más de 1 h conectividad; más de 2 h alimentación (y cada 3 h); más de 4 h de noche alojamiento y transporte; más de 11 h de día transporte. Excepto clima, fuerza mayor o caso fortuito.
  - `POL-CL-04` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Reprogramación o cancelación: reubicación, cambio sin cargo ni diferencia tarifaria, devolución si espera más de 3 h; alojamiento si hay que pernoctar.
  - `POL-PE-07` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 8: retraso más de 2 h refrigerio y llamada; más de 4 h comida; más de 6 h compensación mínima 25 % y hospedaje o reembolso; cancelación; sobreventa; conexiones.
  - `POL-CO-04` → `05_Politicas_Externas/05_Colombia.md` — Demora: más de 1 h refrigerio; más de 3 h comida; más de 5 h compensación de al menos 30 % (no si sale antes de 6 h).
  - `POL-UYN-02` → `05_Politicas_Externas/06_Uruguay_cartilla_DINACIA.md` — Espera de más de 4 h: comidas, alojamiento y transporte; no aplica por clima.
  - `POL-AR-03` → `05_Politicas_Externas/07_Argentina_ANAC.md` — Demoras: hasta 4 h nada (salvo 00-06 h comidas); 4-8 h comidas; más de 8 h comidas, alojamiento y traslado.
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-28 · Reembolso, tarifas no reembolsables y plazos  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Qué se dice de la opción de reembolso (O3) si no hay regla ni monto y la tarifa es «no reembolsable»?
- **Tu elección:** a) Mencionar que existe la vía de reembolso, sin monto ni plazo, y derivar
  - *a)* No se usa `refundable:false` para negar; el detalle lo confirma un agente.
- **Recomendación del análisis:** a) Mencionar que existe la vía de reembolso, sin monto ni plazo, y derivar — Es veraz con la evidencia disponible y no usa la tarifa voluntaria como excusa.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Define el tratamiento de O3 en REQ-F-20 y el contenido de REQ-F-03; marca GAP-04 y GAP-10 como pregunta abierta.
- **Requerimientos relacionados:**
  - `REQ-F-18` — Las recomendaciones deben ser exactas: una incorrecta genera costo, reclamo o incumplimiento de política.
  - `REQ-F-03` — El pasajero recibe una explicación o recomendación accionable (qué ocurrió y cuál es su siguiente paso).
- **Trazabilidad:** SRC: SRC-03-02, SRC-02-07 · GAP: GAP-04, GAP-10 · DAT: DAT-11, DAT-33 · POL: POL-CL-07, POL-CL-16, POL-PE-10, POL-UY-03
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-CL-07` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Pérdida de conexión en la misma reserva: reubicación, cambio sin cargo ni diferencia tarifaria, devolución si decide no volar.
  - `POL-CL-16` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Las tasas de embarque siempre son reembolsables; las tarifas baratas no admiten cambio ni devolución voluntaria; se evalúa por segmento.
  - `POL-PE-10` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 11: reembolso dentro de 5 días hábiles.
  - `POL-UY-03` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Cancelación: alternativa, nueva fecha sin costo o devolución total (incluye tasas).
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-29 · Compensación económica (R4)  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Cuándo y cómo se habla de compensación económica?
- **Tu elección:** a) Nunca proactivo; solo si el pasajero lo pide; sin montos; caso humano
  - *a)* Se cumple R4: se abre caso humano.
- **Recomendación del análisis:** a) Nunca proactivo; solo si el pasajero lo pide; sin montos; caso humano — Emitir una compensación es de alto impacto (SRC-04-06) y no hay base de montos en el PDF.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Fija el control de REQ-F-17 para compensación y el disparador de REQ-F-14.
- **Requerimientos relacionados:**
  - `REQ-F-17` — No ejecutar acciones de alto impacto sin los controles correspondientes (cambiar una reserva; emitir una compensación).
- **Trazabilidad:** SRC: SRC-03-03, SRC-04-06 · GAP: GAP-05 · DAT: DAT-50 · POL: POL-PE-07, POL-CO-04, POL-CO-05, POL-EC-01, POL-CL-06
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-PE-07` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 8: retraso más de 2 h refrigerio y llamada; más de 4 h comida; más de 6 h compensación mínima 25 % y hospedaje o reembolso; cancelación; sobreventa; conexiones.
  - `POL-CO-04` → `05_Politicas_Externas/05_Colombia.md` — Demora: más de 1 h refrigerio; más de 3 h comida; más de 5 h compensación de al menos 30 % (no si sale antes de 6 h).
  - `POL-CO-05` → `05_Politicas_Externas/05_Colombia.md` — Cancelación: devolución más compensación de al menos 30 % y hospedaje.
  - `POL-EC-01` → `05_Politicas_Externas/10_Ecuador.md` — Ecuador (fuente secundaria): compensación mínima de 25 % del trayecto; las fuentes discrepan en los tramos.
  - `POL-CL-06` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Sobreventa: opciones, devolución en 10 días hábiles y compensación en UF (la tabla tiene una fila anómala).
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-30 · Causa del evento y exenciones (clima, fuerza mayor)  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Cómo se trata que el evento no traiga causa si muchas normas la usan para conceder o negar derechos?
- **Tu elección:** a) Tratar como «causa no informada»
  - *a)* No afirmar ni negar derechos que dependan de la causa; mensaje neutral; escalar los casos donde la causa cambiaría el derecho; documentar la brecha.
- **Recomendación del análisis:** a) Tratar como «causa no informada» — No hay dato para otra cosa; se sugiere c como siguiente paso en el README.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Dejarmencionado que seria util tener un campo cause. POr el análisis de las politicaspero no va para version 1
- **Efecto sobre los requerimientos:** Añade la regla DQ-29 a REQ-F-18/REQ-F-16 y una pregunta abierta en REQ-D-07.
- **Requerimientos relacionados:**
  - `REQ-F-18` — Las recomendaciones deben ser exactas: una incorrecta genera costo, reclamo o incumplimiento de política.
  - `REQ-F-16` — No entregar información no verificada al pasajero; notify_passenger no debe enviar información no validada.
- **Trazabilidad:** SRC: SRC-02-08 · GAP: GAP-06 · DAT: DAT-22, DAT-49 · POL: POL-CL-01, POL-PE-06, POL-UE-03
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-CL-01` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Atraso en aeropuerto: más de 1 h conectividad; más de 2 h alimentación (y cada 3 h); más de 4 h de noche alojamiento y transporte; más de 11 h de día transporte. Excepto clima, fuerza mayor o caso fortuito.
  - `POL-PE-06` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 7: cancelación; liberación si avisó con 15 días o más; causas no imputables solo si las verifica la autoridad nacional.
  - `POL-UE-03` → `05_Politicas_Externas/02_Union_Europea_Reg_261-2004.md` — UE: cancelación; adelanto de más de 1 h se considera cancelación; compensación salvo aviso de 14 días o circunstancias extraordinarias.
  - `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-31 · Cancelaciones, adelantos y otros eventos  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿El slice cubre solo retrasos o también cancelación y adelanto?
- **Tu elección:** a) Solo DELAY; el resto degrada a humano
  - *a)* Se reconocen GATE_CHANGE y STATUS; cualquier otro tipo (cancelación, adelanto) escala.
- **Recomendación del análisis:** a) Solo DELAY; el resto degrada a humano — No hay datos ni política en el PDF para esos casos; declararlos fuera de alcance es lo defendible.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Mencionar que se debe tranajar en un a segunda etapa.
- **Efecto sobre los requerimientos:** Delimita REQ-F-00 y deja GAP-07 documentado como próximo paso.
- **Requerimientos relacionados:**
  - `REQ-F-00` — Alcance v1: ayudar a pasajeros cuyo vuelo sufrió una modificación.
  - `REQ-F-02` — El pasajero puede entender si hubo una modificación relevante y qué implica.
- **Trazabilidad:** SRC: SRC-01-09, SRC-03-03 · GAP: GAP-07 · DAT: DAT-18, DAT-50 · POL: POL-UY-02, POL-UY-03, POL-CO-07, POL-UE-03
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-UY-02` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Adelanto de 16 min o más: mismas opciones que el retraso.
  - `POL-UY-03` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Cancelación: alternativa, nueva fecha sin costo o devolución total (incluye tasas).
  - `POL-CO-07` → `05_Politicas_Externas/05_Colombia.md` — Adelanto de más de 1 h: devolución o siguiente vuelo.
  - `POL-UE-03` → `05_Politicas_Externas/02_Union_Europea_Reg_261-2004.md` — UE: cancelación; adelanto de más de 1 h se considera cancelación; compensación salvo aviso de 14 días o circunstancias extraordinarias.
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-32 · Definición de «menor» (R5) y derechos asociados  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Qué es un menor para activar R5?
- **Tu elección:** a) `type == CHILD` (el dato del sistema)
  - *a)* Se usa la clasificación que ya trae la reserva.
- **Recomendación del análisis:** a) `type == CHILD` (el dato del sistema) — Usa el dato disponible sin importar una edad externa.
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** Se debe definir por paia, pero para esta version esta ok.
- **Efecto sobre los requerimientos:** Fija la variable `group_includes_minor` de REQ-F-14/REQ-F-17 (REQ-F-30d).
- **Requerimientos relacionados:**
  - `REQ-F-14` — Definir en qué casos debe intervenir una persona antes de actuar o comunicar (AMB-04).
  - `REQ-F-17` — No ejecutar acciones de alto impacto sin los controles correspondientes (cambiar una reserva; emitir una compensación).
- **Trazabilidad:** SRC: SRC-03-03 · GAP: GAP-08 · DAT: DAT-03, DAT-45 · POL: POL-CL-13, POL-PE-02, POL-UYN-04
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-CL-13` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Menores de 14 años: asientos contiguos a un adulto de su familia o de la misma reserva.
  - `POL-PE-02` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Definiciones: niños menores de 5 años son usuarios con necesidades especiales; valor neto sin tasas ni impuestos.
  - `POL-UYN-04` → `05_Politicas_Externas/06_Uruguay_cartilla_DINACIA.md` — Menores de 5 años, personas con discapacidad o mayores de 70: embarque preferente.
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-33 · Plazo y contenido de la notificación al pasajero  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Qué debe contener el mensaje y con cuánta anticipación se avisa?
- **Tu elección:** a) Mensaje con qué cambió (con hora), qué implica, siguiente paso, `policy_ref`, aviso de estimación y vía humana; sin plazos legales
  - *a)* No se codifican plazos legales en v1; se documentan como referencia.
- **Recomendación del análisis:** a) Mensaje con qué cambió (con hora), qué implica, siguiente paso, `policy_ref`, aviso de estimación y vía humana; sin plazos legales — Cumple los requisitos del PDF y deja los plazos legales como referencia para la jurisdicción (DEC-25).
- **¿Coincide con la recomendación?** Sí.
- **Tus notas / condiciones:** No tomamos en cuenta la data externa, solo es referencia.
- **Efecto sobre los requerimientos:** Define el contenido mínimo del mensaje de REQ-F-03/REQ-F-16 y la especificación de REQ-F-09.
- **Requerimientos relacionados:**
  - `REQ-F-03` — El pasajero recibe una explicación o recomendación accionable (qué ocurrió y cuál es su siguiente paso).
  - `REQ-F-16` — No entregar información no verificada al pasajero; notify_passenger no debe enviar información no validada.
- **Trazabilidad:** SRC: SRC-02-05, SRC-04-03 · GAP: GAP-09 · DAT: DAT-65 · POL: POL-PE-03, POL-CO-02, POL-BO-01
- **Insumos externos para esta decisión (para tu revisión):**
  - `POL-PE-03` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 4: informar cambios al menos 4 h antes; información preferentemente escrita de derechos ante retraso, cancelación o sobreventa.
  - `POL-CO-02` → `05_Politicas_Externas/05_Colombia.md` — Informar cambios por el medio más rápido, a más tardar 24 h antes.
  - `POL-BO-01` → `05_Politicas_Externas/09_Bolivia.md` — Avisar cambios al menos 4 h antes (nacional) o 12 h (internacional).
  - `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

#### DEC-34 · México y otros países fuera de la fuente  ·  EXTERNA — revisión estricta

- **Pregunta:** ¿Qué se hace con México, que no figura en la lista de países de la aerolínea?
- **Tu elección:** a) Fuera de alcance de v1; pregunta documentada
  - *a)* Se registra como pregunta para Producto/Legal.
- **Recomendación del análisis:** a) Fuera de alcance de v1; pregunta documentada — La fuente que indicaste no cubre México y el PDF no lo pide.
- **¿Coincide con la recomendación?** Sí.
- **Efecto sobre los requerimientos:** Queda como pregunta abierta en REQ-D-07 (b, e).
- **Requerimientos relacionados:**
  - `REQ-F-00` — Alcance v1: ayudar a pasajeros cuyo vuelo sufrió una modificación.
- **Trazabilidad:** GAP: GAP-14
- **Insumos externos para esta decisión (para tu revisión):**
  - `LEEME` → `05_Politicas_Externas/00_LEEME_Politicas.md` — Estado de captura de cada fuente y qué país importa para el caso (§3).
  - `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.
- **Tu elección ¿incorpora información externa al diseño?** No — los insumos externos quedan solo como contexto.

### F · Presentación y uso de IA

#### DEC-36 · Idioma, tono y localización de mensajes

- **Pregunta:** ¿En qué idioma y con qué formato se redactan los mensajes al pasajero?
- **Tu elección:** c) Español neutro sin localización
  - *c)* Texto genérico.
- **Recomendación del análisis:** a) Español (es-CL) con plantillas y formato local — Es lo que sugieren los datos del ejemplo.
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Tus notas / condiciones:** Se deja asi para version 1, de debe dejar nota de esto.
- **Efecto sobre los requerimientos:** Define la especificación del mensaje de REQ-F-03/REQ-F-09.
- **Requerimientos relacionados:**
  - `REQ-F-03` — El pasajero recibe una explicación o recomendación accionable (qué ocurrió y cuál es su siguiente paso).
- **Trazabilidad:** SRC: SRC-01-14 · GAP: GAP-22

#### DEC-37 · Uso de IA en este trabajo y confidencialidad del enunciado

- **Pregunta:** ¿Qué registras sobre el uso de IA y cómo tratas el PDF marcado «Uso interno»? (selección múltiple)
- **Tu elección:** a) Registrar el uso de IA para el Entregable 3
  - *a)* Herramientas (p. ej. Claude Code y el método ESF), para qué se usaron, qué se aceptó, rechazó o modificó, cómo se validó, decisiones personales y qué nunca se envía a un modelo.
- **Recomendación del análisis:** a) Registrar el uso de IA para el Entregable 3 · b) No publicar los artefactos fuera de tu entorno — a es obligatoria; b es una precaución barata coherente con la marca de confidencialidad.
- **¿Coincide con la recomendación?** **No**: elegiste distinto.
- **Tus notas / condiciones:** Dejar explicitas en un .md, las decisiones aqui tomadas. Y dejar un paso a paso de las interacciones con claude.
- **Efecto sobre los requerimientos:** Fija el contenido de REQ-D-08 y el tratamiento de REQ-P-12/REQ-N-10.
- **Requerimientos relacionados:**
  - `REQ-P-10` — Se puede usar IA libremente; se pide transparencia en el Entregable 3 y se conversará sobre decisiones concretas del proceso.
  - `REQ-P-12` — Tratar el documento como confidencial: cada página está marcada "Uso interno".
  - `REQ-D-08` — Entregable 3 — AI Usage & Decision Note (máx. 1 pág.): (a) herramientas de IA usadas y para qué; (b) outputs aceptados, rechazados o modificados y cómo se validaron; (c) decisiones tomadas personalmente; (d) qué información nunca se entregaría a un modelo.
  - `REQ-N-10` — Confidencialidad del documento ("Uso interno") y de los datos del caso.
- **Trazabilidad:** SRC: SRC-06-05, SRC-05-04, SRC-00-01

## 3. Matriz requerimiento → decisiones

Para cada requerimiento afectado: qué decisiones lo modifican o precisan y cómo quedaron.

| Requerimiento | Texto | Decisiones que lo afectan (elección) |
|---|---|---|
| `REQ-C-05` | Contrato de create_rebooking_request(option, idempotency_key) — "Acción de alto impacto." | DEC-18 (a) |
| `REQ-C-07` | Contrato de notify_passenger(message) — "No debe enviar información no validada." | DEC-20 (pendiente) |
| `REQ-D-02` | El Entregable 1 indica el track elegido (Backend/Integración o Frontend/Experience) y por qué. | DEC-01 (a) |
| `REQ-D-04` | El Entregable 1 declara el alcance efectivamente implementado. | DEC-04 (otra) |
| `REQ-D-05` | El Entregable 1 lista tests o validaciones disponibles (y el slice incluye ≥ 1 validación o test). | DEC-24 (b) |
| `REQ-D-08` | Entregable 3 — AI Usage & Decision Note (máx. 1 pág.): (a) herramientas de IA usadas y para qué; (b) outputs aceptados, rechazados o modi… | DEC-22 (a); DEC-37 (a) |
| `REQ-D-09` | La clasificación de pasos (determinístico / AI-assisted / agentic / human) debe aparecer (en el README o en la presentación) con razón, r… | DEC-02 (a) |
| `REQ-D-11` | Soporte de presentación (libre) que cubra REQ-P-07. | DEC-03 (otra) |
| `REQ-E-01` | Pensamiento de producto: cómo entiendes y acotas, qué supuestos explicitas, qué priorizas y cómo lo medirías. | DEC-24 (b) |
| `REQ-E-04` | Calidad, seguridad y confiabilidad: comprobaciones, fallos, permisos, datos sensibles, operación. | DEC-24 (b) |
| `REQ-F-00` | Alcance v1: ayudar a pasajeros cuyo vuelo sufrió una modificación. | DEC-04 (otra); DEC-31 (a); DEC-34 (a) |
| `REQ-F-01` | El pasajero puede consultar el contexto de su viaje. | DEC-21 (a) |
| `REQ-F-02` | El pasajero puede entender si hubo una modificación relevante y qué implica. | DEC-05 (b); DEC-06 (a); DEC-31 (a) |
| `REQ-F-03` | El pasajero recibe una explicación o recomendación accionable (qué ocurrió y cuál es su siguiente paso). | DEC-17 (a); DEC-27 (b); DEC-28 (a); DEC-33 (a); DEC-36 (c) |
| `REQ-F-04` | El pasajero puede ser derivado a una persona, o iniciar una acción controlada, cuando corresponda. | DEC-15 (b+c+d+e+f+g+h+i) |
| `REQ-F-05` | Resolver el caso base: a partir de la información disponible (reserva + eventos + políticas), determinar qué ocurrió y qué corresponde of… | DEC-04 (otra) |
| `REQ-F-06` | Diseñar el manejo de una consulta ambigua o compleja que combine reserva, eventos y políticas: cómo se descompone el trabajo, qué context… | DEC-02 (a) |
| `REQ-F-07` | [Opción A — Backend/Integración] Implementar la lógica del caso base como servicio o función invocable, con manejo de errores y ≥ 1 valid… | DEC-01 (a) |
| `REQ-F-08` | [Opción B — Frontend/Experience] Implementar la pantalla o flujo del pasajero que consume datos equivalentes a los de las tools y muestra… | DEC-01 (a) |
| `REQ-F-09` | Especificar (sin implementar) la capa complementaria: si el track fue Backend → cómo se vería/comunicaría al pasajero (pantalla, wirefram… | DEC-01 (a); DEC-20 (pendiente) |
| `REQ-F-10` | Decidir y justificar el uso de IA en runtime; si no se incorpora, explicar qué beneficio se esperaba y por qué el riesgo, costo o complej… | DEC-02 (a) |
| `REQ-F-11` | Definir qué se considera una modificación relevante (AMB-01). | DEC-05 (b); DEC-26 (a) |
| `REQ-F-12` | Definir qué información puede mostrarse al pasajero y cuál no (AMB-02). | DEC-21 (a) |
| `REQ-F-13` | Definir en qué casos una recomendación puede entregarse de forma automática (AMB-03). | DEC-14 (a) |
| `REQ-F-14` | Definir en qué casos debe intervenir una persona antes de actuar o comunicar (AMB-04). | DEC-13 (a); DEC-15 (b+c+d+e+f+g+h+i); DEC-16 (a); DEC-32 (a) |
| `REQ-F-15` | Definir qué hacer cuando las fuentes entregan información contradictoria (AMB-05). | DEC-09 (d) |
| `REQ-F-16` | No entregar información no verificada al pasajero; notify_passenger no debe enviar información no validada. | DEC-20 (pendiente); DEC-30 (a); DEC-33 (a) |
| `REQ-F-17` | No ejecutar acciones de alto impacto sin los controles correspondientes (cambiar una reserva; emitir una compensación). | DEC-13 (a); DEC-14 (a); DEC-16 (a); DEC-29 (a); DEC-32 (a) |
| `REQ-F-18` | Las recomendaciones deben ser exactas: una incorrecta genera costo, reclamo o incumplimiento de política. | DEC-07 (d); DEC-25 (a); DEC-26 (a); DEC-27 (b); DEC-28 (a); DEC-30 (a) |
| `REQ-F-19` | Usar reglas versionadas y verificables; el mensaje debe llevar policy_ref (el servicio rechaza con 422 UNVALIDATED_CONTENT si falta). | DEC-12 (b); DEC-25 (a) |
| `REQ-F-20` | Las opciones son candidatas, no una decisión final: el sistema selecciona y valida. | DEC-17 (a) |
| `REQ-F-21` | Controlar timestamp, fuente y frescura de los eventos operacionales. | DEC-08 (a); DEC-09 (d); DEC-10 (pendiente) |
| `REQ-F-22` | Tolerar información parcial del contexto (completeness: PARTIAL) y declararla. | DEC-11 (otra) |
| `REQ-F-23` | Idempotencia en create_rebooking_request con idempotency_key. | DEC-18 (a) |
| `REQ-F-24` | Manejar 409 DUPLICATE_REQUEST (existente) y 503 UPSTREAM_TIMEOUT (resultado indeterminado). | DEC-18 (a) |
| `REQ-F-25` | Respetar la vigencia (TTL = 120 s) de las opciones; no actuar con opciones vencidas. | DEC-10 (pendiente); DEC-19 (a) |
| `REQ-F-26` | Escalar a operación humana con razón y evidencia mediante create_human_case (cola DISRUPTION_L2, SLA 45 min en el ejemplo). | DEC-15 (b+c+d+e+f+g+h+i); DEC-19 (a) |
| `REQ-F-27` | Si se usan mocks propios, mantener los contratos de las tools. | DEC-22 (a) |
| `REQ-F-28` | Trazabilidad: cada decisión/acción debe poder reconstruirse (datos usados con su retrieved_at, versión de política y rule_id, evento(s) e… | DEC-23 (a) |
| `REQ-F-29` | Validar mensajes antes de notificar: además del policy_ref exigido por el servicio, un validador propio que verifique que cada afirmación… | DEC-20 (pendiente) |
| `REQ-F-30` | Resultado esperado del caso base ABC123 (hipótesis; sub-resultados F-30a…h). | DEC-06 (a); DEC-07 (d) |
| `REQ-N-01` | Los datos operacionales pueden estar desactualizados o ser contradictorios entre fuentes. | DEC-09 (d) |
| `REQ-N-04` | Proteger datos personales y aplicar mínimo privilegio. | DEC-21 (a); DEC-22 (a) |
| `REQ-N-05` | La primera versión debe poder ser operada por un equipo pequeño. | DEC-24 (b) |
| `REQ-N-06` | Considerar latencia, costo por interacción y dependencia de modelos. | DEC-02 (a); DEC-24 (b) |
| `REQ-N-07` | No existe una única solución correcta. | DEC-35 (a) |
| `REQ-N-08` | Mantener exactitud, seguridad y trazabilidad. | DEC-23 (a) |
| `REQ-N-09` | Resultado de negocio: reducir la incertidumbre del pasajero y los contactos evitables al call center. (No hay métrica definida.) | DEC-24 (b) |
| `REQ-N-10` | Confidencialidad del documento ("Uso interno") y de los datos del caso. | DEC-37 (a) |
| `REQ-P-01` | El trabajo efectivo tiene un máximo de 3 horas e incluye análisis, implementación, validaciones y documentación. | DEC-04 (otra) |
| `REQ-P-06` | La sesión comienza con 10 min de presentación con el soporte que prefieras; no se exige presentación formal ni diapositivas; no se espera… | DEC-03 (otra) |
| `REQ-P-09` | Formato y herramientas libres (repositorio, Markdown, PDF, documento, diagrama, demo); la estética no se evalúa; el contenido de los 3 en… | DEC-03 (otra) |
| `REQ-P-10` | Se puede usar IA libremente; se pide transparencia en el Entregable 3 y se conversará sobre decisiones concretas del proceso. | DEC-37 (a) |
| `REQ-P-11` | Si el enunciado es insuficiente, documentar el supuesto y por qué. | DEC-35 (a) |
| `REQ-P-12` | Tratar el documento como confidencial: cada página está marcada "Uso interno". | DEC-37 (a) |

## 4. Insumos externos: autorizados y no autorizados

**Autorizados a incorporarse al diseño (tu elección los usa):** DEC-05.

**Solo contexto (no se incorporan):** DEC-35, DEC-25, DEC-26, DEC-27, DEC-28, DEC-29, DEC-30, DEC-31, DEC-32, DEC-33, DEC-34.

**Sin decidir:** ninguno.

Detalle de lo autorizado:
- **DEC-05** — ¿Qué es una «modificación relevante»? (AMB-01): `POL-UY-01`, `POL-UY-02`, `POL-CL-03`, `MATRIZ`

## 5. Cambios a incorporar en el documento de requerimientos

Lista de verificación derivada de tus decisiones (marca cada una al actualizar `REQUERIMIENTOS.md`):

- [ ] **DEC-01 → a**: Define cuál de REQ-F-07 o REQ-F-08 se cumple y qué debe especificarse en REQ-F-09. Cambia el contenido de REQ-D-02.
- [ ] **DEC-02 → a**: Define el contenido de REQ-F-10 (justificación) y la clasificación de pasos de REQ-D-09. Condiciona REQ-N-06 (latencia/costo) y REQ-N-04 (qué ve un modelo).
- [ ] **DEC-03 → otra**: Determina cómo se presentan REQ-D-07, REQ-D-08 y el soporte REQ-D-11.
- [ ] **DEC-04 → otra**: Fija el alcance de REQ-D-04 y la lista de pruebas de REQ-D-05; delimita REQ-F-00.
- [ ] **DEC-05 → b**: Define el criterio de REQ-F-11 y la salida de REQ-F-02. Depende de DEC-26 y DEC-31.
- [ ] **DEC-06 → a**: Define cómo se obtiene la variable `delay_minutes` y la llegada usada en REQ-F-30c.
- [ ] **DEC-07 → d**: Define cómo se calcula la variable de R3 en REQ-F-30c y cómo se comunica (REQ-F-16).
- [ ] **DEC-08 → a**: Fija cómo se calculan las edades de datos (REQ-F-21) y la aritmética de fechas.
- [ ] **DEC-09 → d**: Define el contenido de REQ-F-15 y la condición de bloqueo de REQ-F-16 cuando hay conflicto.
- [ ] **DEC-11 → otra**: Define la tabla de gating de REQ-F-22 y la regla DQ-28.
- [ ] **DEC-12 → b**: Define cómo se implementa REQ-F-19 y registra cada variable derivada como DERIVADA con sus supuestos (REQ-F-28).
- [ ] **DEC-13 → a**: Define la regla de combinación que usa REQ-F-17 y los disparadores de REQ-F-14. Condiciona el resultado esperado REQ-F-30g.
- [ ] **DEC-14 → a**: Define la matriz acción × condiciones de REQ-F-13 y qué escrituras requieren REQ-F-17.
- [ ] **DEC-15 → b+c+d+e+f+g+h+i**: Convierte AMB-04 en disparadores explícitos de REQ-F-14 y define cuándo se invoca REQ-F-26.
- [ ] **DEC-16 → a**: Añade una restricción explícita a REQ-F-17 y a la selección de opciones (REQ-F-20).
- [ ] **DEC-17 → a**: Define el filtro de REQ-F-20 y el contenido del mensaje de REQ-F-03.
- [ ] **DEC-18 → a**: Fija el contenido de REQ-F-23 y REQ-F-24 y la extensión documentada del contrato (reserva y pasajeros) de REQ-C-05.
- [ ] **DEC-19 → a**: Añade el paso de revalidación a REQ-F-25 y REQ-F-26 y al flujo de aprobación.
- [ ] **DEC-21 → a**: Define la lista blanca de REQ-F-12 y el supuesto de REQ-F-01.
- [ ] **DEC-22 → a**: Define el inventario de REQ-N-04, el límite de REQ-F-27 y el contenido de REQ-D-08 (d).
- [ ] **DEC-23 → a**: Define el contenido de REQ-F-28 y la evidencia de REQ-E-05.
- [ ] **DEC-24 → b**: Fija REQ-D-05, los presupuestos de REQ-N-05/06 y la métrica de REQ-N-09.
- [ ] **DEC-35 → a**: Determina si REQ-F-19 se apoya solo en `get_policy_rules` y qué brechas GAP-01…10 pasan a «preguntas/próximos pasos» en el README (REQ-D-07).
- [ ] **DEC-25 → a**: Define el alcance de REQ-F-19 y la lista de preguntas del README (REQ-D-07 b, e). Condiciona DEC-26 a DEC-33.
- [ ] **DEC-26 → a**: Fija el umbral de REQ-F-11 y su justificación; relacionado con DEC-05.
- [ ] **DEC-27 → b**: Añade a REQ-F-18/REQ-F-03 la mención cautelosa de asistencia y el disparador de caso humano por pernocte (REQ-F-14).
- [ ] **DEC-28 → a**: Define el tratamiento de O3 en REQ-F-20 y el contenido de REQ-F-03; marca GAP-04 y GAP-10 como pregunta abierta.
- [ ] **DEC-29 → a**: Fija el control de REQ-F-17 para compensación y el disparador de REQ-F-14.
- [ ] **DEC-30 → a**: Añade la regla DQ-29 a REQ-F-18/REQ-F-16 y una pregunta abierta en REQ-D-07.
- [ ] **DEC-31 → a**: Delimita REQ-F-00 y deja GAP-07 documentado como próximo paso.
- [ ] **DEC-32 → a**: Fija la variable `group_includes_minor` de REQ-F-14/REQ-F-17 (REQ-F-30d).
- [ ] **DEC-33 → a**: Define el contenido mínimo del mensaje de REQ-F-03/REQ-F-16 y la especificación de REQ-F-09.
- [ ] **DEC-34 → a**: Queda como pregunta abierta en REQ-D-07 (b, e).
- [ ] **DEC-36 → c**: Define la especificación del mensaje de REQ-F-03/REQ-F-09.
- [ ] **DEC-37 → a**: Fija el contenido de REQ-D-08 y el tratamiento de REQ-P-12/REQ-N-10.

## 6. Supuestos pendientes y preguntas abiertas

- **DEC-10** — Frescura y vigencia de los datos. Recomendación del análisis (**no aprobada**): a) Umbrales distintos por tipo de uso.
- **DEC-20** — Contrato de `notify_passenger` y validación del mensaje. Recomendación del análisis (**no aprobada**): a) Plantillas con hechos validados + `policy_ref` + destinatario (extensión del contrato).

## Anexo · Archivos de referencia

- Fuente indexada: `01_Fuente_y_Trazabilidad/01_Indice_de_fuente_SRC.md`
- Requerimientos: `03_Requerimientos/REQUERIMIENTOS.md`
- Análisis de datos: `04_Analisis_de_Datos/`
- Políticas externas: `05_Politicas_Externas/` (matriz comparativa en `15_Matriz_comparativa.md`; cruces en `16_Referencias_cruzadas.md`)
- Catálogo legible de decisiones: `06_Decisiones/DECISIONES_CATALOGO.md`