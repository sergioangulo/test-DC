# 06 · Catálogo de decisiones

> **Es la versión legible del formulario** (`FORMULARIO_DECISIONES.html`). Las decisiones **EXTERNAS** usan información que no está en el PDF y requieren tu **revisión estricta**. Ninguna está tomada: lo que ves como *recomendación* es solo mi propuesta razonada.
> Total: **37 decisiones** (12 externas, 25 internas).

## Índice

| ID | Grupo | Decisión | Tipo | Recomendación |
|---|---|---|---|---|
| DEC-01 | A | Track a implementar | Interna | a |
| DEC-02 | A | Rol de la IA en tiempo de ejecución | Interna | a |
| DEC-03 | A | Formato de entrega y soporte de presentación | Interna | a |
| DEC-04 | A | Alcance del vertical slice | Interna | b |
| DEC-05 | B | ¿Qué es una «modificación relevante»? (AMB-01) | **EXTERNA** | b |
| DEC-06 | B | Medición del retraso y llegada nueva | Interna | a |
| DEC-07 | B | Derivación de «conexión perdida» y tiempo mínimo de conexión | Interna | d |
| DEC-08 | B | Zonas horarias y fechas | Interna | a |
| DEC-09 | B | Fuentes contradictorias y precedencia (AMB-05) | Interna | a |
| DEC-10 | B | Frescura y vigencia de los datos | Interna | a |
| DEC-11 | B | Datos parciales (`completeness: PARTIAL`) | Interna | a |
| DEC-12 | B | Evaluación segura de reglas y variables derivadas | Interna | b |
| DEC-13 | B | Precedencia entre reglas (R3 vs R5) y aprobación humana | Interna | a |
| DEC-14 | C | Qué se entrega de forma automática (AMB-03) | Interna | a |
| DEC-15 | C | Cuándo interviene una persona (AMB-04) | Interna | a, b, c, d, e, f, g, h, i |
| DEC-16 | C | Menores y grupos familiares (producto) | Interna | a |
| DEC-17 | C | Selección y presentación de opciones | Interna | a |
| DEC-18 | C | Ciclo de vida del rebooking: idempotencia, 409, 503 y PENDING_CONFIRMATION | Interna | a |
| DEC-19 | C | Alineación de tiempos: TTL, expiración y SLA humano | Interna | a |
| DEC-20 | C | Contrato de `notify_passenger` y validación del mensaje | Interna | a |
| DEC-21 | D | Información visible al pasajero y verificación de identidad (AMB-02) | Interna | a |
| DEC-22 | D | Datos personales, mínimo privilegio y «qué nunca va a un modelo» | Interna | a |
| DEC-23 | D | Trazabilidad, auditoría y retención | Interna | a |
| DEC-24 | D | Validación mínima, operación, latencia, costo y métrica de éxito | Interna | a |
| DEC-35 | E | Marco: cómo se incorporan las políticas externas | **EXTERNA** | a |
| DEC-25 | E | Jurisdicción aplicable por segmento | **EXTERNA** | a |
| DEC-26 | E | Umbral de cambio sin costo por retraso: 180 min (PDF) vs 31 min (la aerolínea) | **EXTERNA** | a |
| DEC-27 | E | Asistencia durante la espera (comunicación, comida, alojamiento, traslado) | **EXTERNA** | b |
| DEC-28 | E | Reembolso, tarifas no reembolsables y plazos | **EXTERNA** | a |
| DEC-29 | E | Compensación económica (R4) | **EXTERNA** | a |
| DEC-30 | E | Causa del evento y exenciones (clima, fuerza mayor) | **EXTERNA** | a |
| DEC-31 | E | Cancelaciones, adelantos y otros eventos | **EXTERNA** | a |
| DEC-32 | E | Definición de «menor» (R5) y derechos asociados | **EXTERNA** | a |
| DEC-33 | E | Plazo y contenido de la notificación al pasajero | **EXTERNA** | a |
| DEC-34 | E | México y otros países fuera de la fuente | **EXTERNA** | a |
| DEC-36 | F | Idioma, tono y localización de mensajes | Interna | a |
| DEC-37 | F | Uso de IA en este trabajo y confidencialidad del enunciado | Interna | a, b |

---

## A · Alcance y enfoque del ejercicio

### DEC-01 · Track a implementar

**Pregunta:** ¿Implementas el track Backend/Integración o el track Frontend/Experience? (el otro queda como diseño)

**Contexto:** El PDF exige profundidad en uno solo y diseño del otro (SRC-04-17, SRC-04-20). El caso base es sobre todo lógica de decisión (reserva + eventos + políticas) con varias trampas en los datos; las dimensiones de evaluación 'Fundamentos de ingeniería' y 'Razonamiento agentic y control' se demuestran mejor con contratos, errores e idempotencia.

**Trazabilidad:** SRC: `SRC-04-17`, `SRC-04-18`, `SRC-04-19`, `SRC-04-20`, `SRC-05-02`, `SRC-07-02`, `SRC-07-07` · REQ: `REQ-F-07`, `REQ-F-08`, `REQ-F-09`, `REQ-D-02`

**Opciones:**

- **a) Backend/Integración** ★ *recomendada* — Servicio o función que combina reserva, eventos y política, con manejo de errores y al menos un test. La experiencia del pasajero queda como especificación del mensaje.
  - A favor: Ejercita contratos, errores, idempotencia, calidad de datos; evidencia verificable por tests; encaja con 'control' y 'agentic'.
  - En contra: La experiencia visible del pasajero queda solo como diseño.
- **b) Frontend/Experience** — Pantalla o flujo que consume datos equivalentes y muestra estado del viaje, alerta y recomendación, con una validación.
  - A favor: Resultado visible y fácil de mostrar en 10 minutos.
  - En contra: Riesgo de esconder la lógica de decisión (donde están las trampas); consume datos simulados; la capa backend queda como supuesto.

**Recomendación:** a — El valor del ejercicio está en la lógica de decisión y en cómo se tratan los datos defectuosos; eso es backend. La pantalla se puede especificar sin implementarla.

**Efecto en los requerimientos:** Define cuál de REQ-F-07 o REQ-F-08 se cumple y qué debe especificarse en REQ-F-09. Cambia el contenido de REQ-D-02.

### DEC-02 · Rol de la IA en tiempo de ejecución

**Pregunta:** ¿Se usa IA dentro del producto (runtime)? Si sí, ¿para qué? Si no, ¿cómo lo justificas?

**Contexto:** No es obligatorio usar IA en runtime y resolver de forma determinística 'puede ser una excelente decisión' (SRC-05-01). Aun así hay que diseñar cómo se manejaría una consulta ambigua y dónde intervendría IA o un agente (SRC-04-22).

**Trazabilidad:** SRC: `SRC-05-01`, `SRC-06-05`, `SRC-04-09`, `SRC-07-07`, `SRC-04-22` · REQ: `REQ-F-06`, `REQ-F-10`, `REQ-N-06`, `REQ-D-09` · GAP: `GAP-22`, `GAP-24` · DAT: `DAT-65`, `DAT-79`

**Opciones:**

- **a) Sin IA en runtime (determinístico + plantillas validadas)** ★ *recomendada* — La decisión y los mensajes se generan con reglas y plantillas. La IA aparece solo como diseño para la consulta libre.
  - A favor: Máxima exactitud y trazabilidad; costo y latencia nulos; sin riesgo de PII hacia un modelo; fácil de operar por un equipo pequeño.
  - En contra: Mensajes menos naturales; la consulta libre ambigua solo queda como diseño.
- **b) IA solo para redactar el mensaje** — Un modelo parafrasea un mensaje construido con hechos ya validados; un validador determinístico revisa el resultado.
  - A favor: Mejor experiencia de lectura.
  - En contra: Costo y latencia por interacción; dependencia de un modelo; riesgo de alucinar; hay que validar cada salida.
- **c) IA para entender la consulta libre** — Un modelo clasifica la intención y extrae entidades; la decisión sigue siendo determinística.
  - A favor: Cubre consultas ambiguas del pasajero.
  - En contra: Superficie de prompt injection; dependencia de modelo; necesita límites estrictos de lo que ve.
- **d) Agente con tools** — Un agente decide qué tools llamar y con qué argumentos.
  - A favor: Máxima flexibilidad.
  - En contra: Alto riesgo con acciones de alto impacto; difícil de auditar; choca con 'control'.

**Recomendación:** a — El núcleo del slice debe ser verificable y determinístico. Se documenta b y c como capa AI-assisted opcional para la consulta ambigua (REQ-F-06), explicando por qué no se activa en v1.

**Efecto en los requerimientos:** Define el contenido de REQ-F-10 (justificación) y la clasificación de pasos de REQ-D-09. Condiciona REQ-N-06 (latencia/costo) y REQ-N-04 (qué ve un modelo).

### DEC-03 · Formato de entrega y soporte de presentación

**Pregunta:** ¿En qué formato entregas los tres entregables y con qué soporte presentas los 10 minutos?

**Contexto:** El formato es libre y la estética no se evalúa; no se exigen diapositivas (SRC-06-02, SRC-06-03).

**Trazabilidad:** SRC: `SRC-01-05`, `SRC-06-02`, `SRC-06-03` · REQ: `REQ-P-09`, `REQ-P-06`, `REQ-D-11`

**Opciones:**

- **a) Repositorio + Markdown** ★ *recomendada* — Código y tests, README.md (≤2 págs.), AI_NOTE.md (≤1 pág.) y una tabla de clasificación de pasos; la presentación se hace directamente sobre estos archivos.
  - A favor: Todo localizable y versionable; sin trabajo extra de diapositivas.
  - En contra: Requiere que el comité pueda abrir el repo.
- **b) Repositorio + PDFs generados** — Igual que a, pero exportando los documentos a PDF.
  - A favor: Fácil de enviar por correo.
  - En contra: Pasos extra de exportación dentro de las 3 horas.
- **c) Un documento único + demo** — Un solo documento largo y una demostración.
  - A favor: Narrativa continua.
  - En contra: Difícil respetar los límites de 2 y 1 página por entregable.

**Recomendación:** a — Minimiza trabajo no evaluado y maximiza evidencia localizable (SRC-07-05).

**Efecto en los requerimientos:** Determina cómo se presentan REQ-D-07, REQ-D-08 y el soporte REQ-D-11.

### DEC-04 · Alcance del vertical slice

**Pregunta:** ¿Qué cubre exactamente el slice dentro de las 3 horas?

**Contexto:** El tiempo es un límite, no una meta (SRC-06-01). El PDF habla de 'modificación' en general (SRC-01-09) pero solo muestra un retraso. El ejemplo es un único caso (DAT-82).

**Trazabilidad:** SRC: `SRC-01-09`, `SRC-04-21`, `SRC-04-23`, `SRC-06-01` · REQ: `REQ-F-00`, `REQ-F-05`, `REQ-D-04`, `REQ-P-01` · GAP: `GAP-07` · DAT: `DAT-18`, `DAT-82`

**Opciones:**

- **a) Solo el caso base** — Retraso en S1 con pérdida de conexión, menor en el grupo y las tres opciones del ejemplo.
  - A favor: Profundidad; cabe en 3 horas.
  - En contra: No demuestra el manejo de las trampas de borde.
- **b) Caso base + casos borde críticos** ★ *recomendada* — Además: evento contradictorio (TC-02/03), opción sin cupos (TC-09), 503 (TC-14) y notificación sin validar (TC-16).
  - A favor: Demuestra criterio donde están las trampas.
  - En contra: Algo más de trabajo; hay que acotar.
- **c) Caso base + otros tipos de evento** — Agrega cancelación y adelanto.
  - A favor: Amplitud.
  - En contra: Obliga a inventar política y datos que el PDF no define (GAP-07).

**Recomendación:** b — El ejercicio mide criterio, no volumen (SRC-01-08). Los casos borde críticos muestran control sin inventar datos.

**Efecto en los requerimientos:** Fija el alcance de REQ-D-04 y la lista de pruebas de REQ-D-05; delimita REQ-F-00.

---

## B · Interpretación del caso y de los datos

### DEC-05 · ¿Qué es una «modificación relevante»? (AMB-01)  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Con qué criterio el sistema decide que un evento es una modificación relevante para el pasajero?

**Contexto:** El PDF no lo define a propósito (SRC-04-12). En el ejemplo hay un retraso de 160 min, un cambio de puerta y dos estados. La política del PDF usa 180 min (R1), pero la aerolínea trata como derecho de cambio desde 31 min de retraso y 16 min de adelanto (información externa).

**Trazabilidad:** SRC: `SRC-04-12`, `SRC-01-13` · REQ: `REQ-F-02`, `REQ-F-11` · AMB: `AMB-01` · GAP: `GAP-02`, `GAP-07` · DAT: `DAT-15`, `DAT-23`

**Información externa para tu revisión:**

- `POL-UY-01` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Retraso de 31 min o más y no conforme: cambio sin costo (mismo destino y cabina, 12 meses) o devolución sin cargo.
- `POL-UY-02` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Adelanto de 16 min o más: mismas opciones que el retraso.
- `POL-CL-03` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Desde 31 min de atraso: cambio (fecha, hora o destino, misma cabina) o devolución.
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Solo lo que activa una regla del PDF** — Relevante si se cumple R1, R2, R3 o R5 (o alguna regla futura).
  - A favor: Simple y verificable con la política devuelta por la tool.
  - En contra: Ignora retrasos de 31 a 179 min que la aerolínea considera relevantes.
- **b) Por impacto en el itinerario (con umbral configurable)** ★ *recomendada* · *usa información externa* — Relevante si hay cancelación, retraso o adelanto sobre un umbral, conexión perdida, o cambio de aeropuerto o fecha. El cambio de puerta se informa como dato, sin tratarlo como modificación relevante.
  - A favor: Alineado con el objetivo del pasajero; el umbral es un parámetro.
  - En contra: Hay que elegir el umbral (ver DEC-26).
- **c) Todo evento es relevante** — Se informa cualquier evento.
  - A favor: Transparencia total.
  - En contra: Ruido y riesgo de comunicar datos no verificados; más contactos al call center.

**Recomendación:** b — Es la lectura más cercana a 'entienda si hubo una modificación relevante y qué implica' (SRC-01-13). El umbral queda como parámetro y su valor depende de DEC-26.

**Efecto en los requerimientos:** Define el criterio de REQ-F-11 y la salida de REQ-F-02. Depende de DEC-26 y DEC-31.

### DEC-06 · Medición del retraso y llegada nueva

**Pregunta:** ¿El retraso que usan las reglas es de salida o de llegada, y cómo se obtiene la llegada nueva?

**Contexto:** El evento solo trae `delay_minutes` y `new_departure` (salida). No existe `new_arrival` (DAT-19). Las normas externas miden unas a la salida y otras a la llegada, pero el PDF no dice cuál usan sus reglas.

**Trazabilidad:** SRC: `SRC-03-03`, `SRC-02-08` · REQ: `REQ-F-02`, `REQ-F-30` · GAP: `GAP-15` · DAT: `DAT-19`, `DAT-54`, `DAT-75`

**Opciones:**

- **a) Usar el retraso de salida y derivar la llegada por propagación** ★ *recomendada* — Las reglas usan `delay_minutes` (salida). La llegada se deriva sumando el retraso a la llegada programada (supuesto A1) y se etiqueta como derivada.
  - A favor: Usa solo datos existentes; supuesto explícito.
  - En contra: Puede equivocarse si el retraso se recupera o crece en vuelo.
- **b) Exigir `new_arrival` a la fuente** — Sin llegada real, no se evalúa la conexión; se degrada a humano.
  - A favor: No hay supuestos.
  - En contra: Casi nunca habrá dato; sube la carga humana.
- **c) Evaluar ambos puntos de medición** — Salida para las reglas del PDF y llegada para las normas externas.
  - A favor: Completo.
  - En contra: Complejo; usa normas externas sin decidir su jurisdicción (DEC-25).

**Recomendación:** a — Es el supuesto más simple y declarable; el resultado se presenta como estimación y exige confirmación antes de actuar (DEC-13).

**Efecto en los requerimientos:** Define cómo se obtiene la variable `delay_minutes` y la llegada usada en REQ-F-30c.

### DEC-07 · Derivación de «conexión perdida» y tiempo mínimo de conexión

**Pregunta:** ¿Cómo se decide que `missed_connection` es verdadero si no es un dato y falta el tiempo mínimo de conexión (MCT)?

**Contexto:** R3 depende de `missed_connection == true`, que no existe en ningún dato (DAT-45). En el caso base la escala planificada es de 70 min y el retraso de 160 min: la llegada derivada (20:35) es 90 min posterior a la salida de S2 (19:05). Supuestos: A1 propagación íntegra, A2 sin MCT, A3 S2 no se retiene.

**Trazabilidad:** SRC: `SRC-02-07`, `SRC-03-03` · REQ: `REQ-F-30`, `REQ-F-18` · GAP: `GAP-11` · DAT: `DAT-07`, `DAT-45`, `DAT-75`

**Opciones:**

- **a) Llegada derivada > salida del siguiente tramo (MCT = 0)** — Se evalúa en el mismo aeropuerto (sin zonas horarias).
  - A favor: Simple, sin inventar un MCT.
  - En contra: Podría marcar como salvable una conexión que en realidad no lo es.
- **b) Igual, con MCT configurable** — El MCT es un parámetro (p. ej. 0 por defecto) documentado como dato faltante.
  - A favor: Honesto sobre lo que falta; permite ajustar.
  - En contra: Hay que decidir el valor por defecto.
- **c) No derivar: informar «conexión en riesgo» y escalar** — Nunca se afirma que se perdió; siempre confirma una persona.
  - A favor: Máxima prudencia.
  - En contra: Menos automatización; el pasajero espera más.
- **d) Derivar (b) y exigir confirmación humana antes de actuar** ★ *recomendada* — El resultado se marca como estimado; el rebooking no se ejecuta sin confirmar.
  - A favor: Equilibra utilidad y control.
  - En contra: Requiere el flujo de aprobación (DEC-13, DEC-15).

**Recomendación:** d — La derivación es útil pero no es un dato; por eso se muestra como estimación y la acción de alto impacto queda sujeta a confirmación.

**Efecto en los requerimientos:** Define cómo se calcula la variable de R3 en REQ-F-30c y cómo se comunica (REQ-F-16).

### DEC-08 · Zonas horarias y fechas

**Pregunta:** ¿Cómo se tratan las horas «HH:MM» sin zona horaria?

**Contexto:** Verificado para el 15-sep-2026: Santiago UTC-3, Lima UTC-5, Ciudad de México UTC-6. Con zonas reales S1 duraría 5 h 25 min (sospechoso); con reloj único, 3 h 25 min (DAT-05). La conexión se evalúa en Lima con dos horas de Lima, así que no depende de zonas.

**Trazabilidad:** SRC: `SRC-02-07`, `SRC-02-08` · REQ: `REQ-F-21` · GAP: `GAP-15` · DAT: `DAT-05`, `DAT-06`, `DAT-20`

**Opciones:**

- **a) Local del aeropuerto + comparar solo dentro del mismo aeropuerto + UTC para edades** ★ *recomendada* — Se usa una tabla mínima versionada IATA→zona (SCL, LIM, MEX) solo cuando haya que convertir.
  - A favor: Correcto y mínimo.
  - En contra: Hay que mantener una tabla pequeña.
- **b) Reloj único (ignorar zonas)** — Se suman y restan horas como si fueran del mismo reloj.
  - A favor: Muy simple.
  - En contra: Incorrecto para cálculos entre aeropuertos.
- **c) Exigir offset en los datos** — Pedir que las tools devuelvan hora con zona.
  - A favor: Elimina la ambigüedad.
  - En contra: Modifica el contrato; el PDF pide mantenerlos (SRC-01-16).

**Recomendación:** a — Evita errores sin cambiar contratos; la conexión (el caso crítico) no necesita zonas.

**Efecto en los requerimientos:** Fija cómo se calculan las edades de datos (REQ-F-21) y la aritmética de fechas.

### DEC-09 · Fuentes contradictorias y precedencia (AMB-05)

**Pregunta:** ¿Qué regla se usa cuando dos fuentes dicen cosas distintas del mismo segmento?

**Contexto:** E-1012 (LEGACY_MIRROR, degradada, 09:30Z) dice ON_TIME; E-1001 (OPS_CORE, 10:48Z) dice retraso de 160 min. Además E-1012 tiene el id más alto (DAT-16). Aquí recencia y salud de fuente coinciden, pero el PDF pide una regla general (SRC-04-16).

**Trazabilidad:** SRC: `SRC-04-16`, `SRC-04-04`, `SRC-01-18` · REQ: `REQ-F-15`, `REQ-F-21`, `REQ-N-01` · AMB: `AMB-05` · GAP: `GAP-16` · DAT: `DAT-15`, `DAT-16`, `DAT-26`

**Opciones:**

- **a) Regla compuesta** ★ *recomendada* — 1) excluir fuentes en `sources_degraded` como evidencia primaria; 2) entre las sanas, gana el `recorded_at` más reciente; 3) empate: jerarquía OPS_CORE > AIRPORT_FEED > LEGACY_MIRROR; 4) si no queda fuente sana o el conflicto no se resuelve: mensaje cauto y humano.
  - A favor: Cubre salud, recencia y empate; auditable.
  - En contra: La jerarquía de fuentes es un supuesto mío que debes confirmar.
- **b) Solo recencia** — Gana el evento más reciente.
  - A favor: Muy simple.
  - En contra: Elegiría un evento de una fuente degradada si fuera más nuevo.
- **c) Solo jerarquía fija** — Gana siempre OPS_CORE.
  - A favor: Predecible.
  - En contra: Ignora que un dato sano puede ser viejo.
- **d) Siempre humano ante conflicto** — Cualquier contradicción escala.
  - A favor: Máxima prudencia.
  - En contra: Más intervención humana y más contactos.

**Recomendación:** a — Es la única que evita mostrar ON_TIME y a la vez maneja los casos que no son tan claros como el del ejemplo.

**Efecto en los requerimientos:** Define el contenido de REQ-F-15 y la condición de bloqueo de REQ-F-16 cuando hay conflicto.

### DEC-10 · Frescura y vigencia de los datos

**Pregunta:** ¿Qué antigüedad máxima se tolera para informar y para actuar?

**Contexto:** El PDF pide controlar la frescura (SRC-01-18) pero no da umbrales. Los eventos válidos del ejemplo tenían 14 y 7 minutos al recuperarlos; las opciones vencen a los 120 s (DAT-17, DAT-35).

**Trazabilidad:** SRC: `SRC-01-18`, `SRC-03-02` · REQ: `REQ-F-21`, `REQ-F-25` · GAP: `GAP-16` · DAT: `DAT-17`, `DAT-35`

**Opciones:**

- **a) Umbrales distintos por tipo de uso** ★ *recomendada* — Informar estado: hasta 15 min; actuar: datos recuperados en la misma operación y revalidados; opciones: respetar el TTL; política: revalidar versión antes de escribir. Los valores son parámetros.
  - A favor: Proporcional al riesgo.
  - En contra: Los números son propuestas mías que debes confirmar.
- **b) Un umbral único** — Por ejemplo 10 minutos para todo.
  - A favor: Simple.
  - En contra: No distingue informar de actuar.
- **c) Sin umbral; solo mostrar la hora** — El mensaje incluye la hora de la información.
  - A favor: Nada que configurar.
  - En contra: No cumple «controlar la frescura».

**Recomendación:** a — El riesgo de un dato viejo es mayor al ejecutar que al informar.

**Efecto en los requerimientos:** Fija parámetros de REQ-F-21 y REQ-F-25 y la regla DQ-14/DQ-15.

### DEC-11 · Datos parciales (`completeness: PARTIAL`)

**Pregunta:** ¿Qué se puede hacer y decir cuando faltan campos?

**Contexto:** Falta `change_penalty_amount`; además `missing_fields` no es exhaustivo (faltan cabina, estado del ticket, mapa pasajero-segmento) (DAT-09).

**Trazabilidad:** SRC: `SRC-01-17`, `SRC-02-07` · REQ: `REQ-F-22` · GAP: `GAP-17` · DAT: `DAT-09`

**Opciones:**

- **a) Condicionar cada afirmación a los campos que necesita** ★ *recomendada* — Hay una tabla afirmación → campos requeridos. Si falta alguno, no se afirma ni se cotiza.
  - A favor: Preciso; permite responder lo que sí se sabe.
  - En contra: Hay que mantener la tabla.
- **b) Bloquear toda respuesta si es PARTIAL** — Si la reserva es parcial, no se responde.
  - A favor: Muy seguro.
  - En contra: Inutiliza el producto: casi siempre será parcial.
- **c) Rellenar con valores por defecto** — Suponer el dato faltante.
  - A favor: Siempre responde.
  - En contra: Peligroso: inventa información.

**Recomendación:** a — Es lo que permite 'tolerar información parcial' sin inventar.

**Efecto en los requerimientos:** Define la tabla de gating de REQ-F-22 y la regla DQ-28.

### DEC-12 · Evaluación segura de reglas y variables derivadas

**Pregunta:** ¿Cómo se evalúan las `condition` (texto) y se derivan las cuatro variables que no vienen en los datos?

**Contexto:** R1-R5 son cadenas con un mini-lenguaje no definido (solo se ven `>=`, `==`, `AND`). `international`, `missed_connection`, `compensation_requested` y `group_includes_minor` no existen en ningún dato (DAT-45, DAT-48).

**Trazabilidad:** SRC: `SRC-03-03` · REQ: `REQ-F-19` · GAP: `GAP-18` · DAT: `DAT-45`, `DAT-48`

**Opciones:**

- **a) Mapear cada (versión, regla) a un predicado codificado** — Cada regla conocida tiene su función; una regla o versión desconocida escala a humano.
  - A favor: Seguro y sencillo.
  - En contra: Acopla el código a versiones concretas.
- **b) Parser acotado con lista blanca** ★ *recomendada* — Solo reconoce identificadores conocidos, `>=`, `==` y `AND`; lo demás es error.
  - A favor: Genérico y seguro; entiende reglas nuevas del mismo estilo.
  - En contra: Hay que escribir y probar el parser.
- **c) Evaluar con un intérprete dinámico** — Ejecutar el texto de la condición.
  - A favor: Muy rápido de escribir.
  - En contra: Riesgo de inyección y comportamiento impredecible.

**Recomendación:** b — Un parser mínimo con lista blanca es pequeño, generaliza a reglas nuevas y falla de forma segura. Si falta tiempo, a es el respaldo.

**Efecto en los requerimientos:** Define cómo se implementa REQ-F-19 y registra cada variable derivada como DERIVADA con sus supuestos (REQ-F-28).

### DEC-13 · Precedencia entre reglas (R3 vs R5) y aprobación humana

**Pregunta:** Si R3 no exige aprobación pero R5 sí (hay un menor), ¿se puede ejecutar el rebooking?

**Contexto:** El PDF no define cómo se combinan las reglas (DAT-47). Lecturas: L1 cada regla gobierna solo su propio derecho; L2 R5 condiciona toda acción del caso. Además cambiar una reserva es una acción de alto impacto (SRC-04-06).

**Trazabilidad:** SRC: `SRC-03-03`, `SRC-04-06` · REQ: `REQ-F-17`, `REQ-F-14` · AMB: `AMB-03`, `AMB-04` · GAP: `GAP-19` · DAT: `DAT-46`, `DAT-47`

**Opciones:**

- **a) Gana la regla más restrictiva (L2)** ★ *recomendada* — Si cualquier regla aplicable exige aprobación humana, el caso completo queda pendiente de esa aprobación.
  - A favor: Seguro; protege al menor; simple de explicar.
  - En contra: Más intervención humana.
- **b) Cada derecho por separado (L1)** — El rebooking (R3) procede solo; la atención prioritaria (R5) pasa por humano.
  - A favor: Más automatización.
  - En contra: Se podría rebookear al grupo sin que una persona revise la situación del menor.
- **c) R5 no bloquea, pero obliga a abrir caso y a un mensaje cauto** — El rebooking se prepara, pero se comunica «en revisión».
  - A favor: Término medio.
  - En contra: Mensaje ambiguo para el pasajero.

**Recomendación:** a — Con un menor y una acción de alto impacto, la lectura conservadora es la defendible en v1.

**Efecto en los requerimientos:** Define la regla de combinación que usa REQ-F-17 y los disparadores de REQ-F-14. Condiciona el resultado esperado REQ-F-30g.

---

## C · Autonomía, intervención humana y acciones

### DEC-14 · Qué se entrega de forma automática (AMB-03)

**Pregunta:** ¿Qué acciones y mensajes puede producir el sistema sin intervención humana?

**Contexto:** El PDF no lo define (SRC-04-14). Las tools de escritura son de alto impacto; los mensajes no deben llevar información no validada (SRC-02-05).

**Trazabilidad:** SRC: `SRC-04-14`, `SRC-01-10` · REQ: `REQ-F-13`, `REQ-F-17` · AMB: `AMB-03` · DAT: `DAT-47`

**Opciones:**

- **a) Automático solo informar y explicar con hechos validados** ★ *recomendada* — Estado del viaje, explicación de la modificación y propuesta de siguiente paso (como propuesta). Toda escritura requiere confirmación humana en v1.
  - A favor: Seguro; cumple 'sin acciones de alto impacto sin controles'.
  - En contra: El pasajero espera la confirmación para el cambio.
- **b) Además recomendar y ejecutar cuando R1 o R3 y sin menor y con datos completos** — Rebooking automático bajo condiciones estrictas.
  - A favor: Más resolución sin contacto humano.
  - En contra: Riesgo alto en la primera versión; más superficie de error.
- **c) Todo con humano** — Ni siquiera se informa sin revisión.
  - A favor: Máximo control.
  - En contra: No reduce contactos evitables (SRC-01-11).

**Recomendación:** a — Equilibra el objetivo de reducir contactos con las restricciones de control (SRC-01-10, SRC-04-06).

**Efecto en los requerimientos:** Define la matriz acción × condiciones de REQ-F-13 y qué escrituras requieren REQ-F-17.

### DEC-15 · Cuándo interviene una persona (AMB-04)

**Pregunta:** ¿Qué situaciones obligan a crear un caso humano antes de actuar o comunicar? (selección múltiple)

**Contexto:** El PDF no lo define (SRC-04-15). `create_human_case` existe con cola DISRUPTION_L2 y SLA de 45 min; no define el esquema de `reason`/`evidence` (DAT-64).

**Trazabilidad:** SRC: `SRC-04-15`, `SRC-02-04` · REQ: `REQ-F-14`, `REQ-F-26`, `REQ-F-04` · AMB: `AMB-04` · GAP: `GAP-26` · DAT: `DAT-64`

**Opciones:**

- **a) Hay un menor en el grupo (R5)** ★ *recomendada* — Siempre caso humano.
  - A favor: Protege al menor.
  - En contra: Aumenta casos.
- **b) El pasajero solicita compensación (R4)** ★ *recomendada* — Siempre caso humano, sin montos.
  - A favor: Evita promesas.
  - En contra: —
- **c) Datos parciales que bloquean la afirmación** ★ *recomendada* — Si falta un campo necesario para el mensaje.
  - A favor: Evita inventar.
  - En contra: —
- **d) Fuentes en conflicto sin resolver** ★ *recomendada* — Según DEC-09 punto 4.
  - A favor: Evita mensajes falsos.
  - En contra: —
- **e) Resultado indeterminado (503)** ★ *recomendada* — Tras reintentos acotados.
  - A favor: Evita duplicados y falsas confirmaciones.
  - En contra: —
- **f) Evento de tipo desconocido** ★ *recomendada* — Por ejemplo cancelación si no está soportada.
  - A favor: Falla seguro.
  - En contra: —
- **g) Ninguna opción cubre a todo el grupo** ★ *recomendada* — Cupos menores que pasajeros.
  - A favor: No separa familias.
  - En contra: —
- **h) Pernocte u otra asistencia no cubierta por la política** ★ *recomendada* — Alojamiento, comidas, traslados.
  - A favor: No promete lo que no hay regla.
  - En contra: —
- **i) Se solicitan datos personales** ★ *recomendada* — Documento, correo, teléfono.
  - A favor: Mínimo privilegio.
  - En contra: —

**Recomendación:** a, b, c, d, e, f, g, h, i — Son los puntos donde el sistema carece de dato, de regla o de control; escalar es lo defendible. La lista es ajustable casilla por casilla.

**Efecto en los requerimientos:** Convierte AMB-04 en disparadores explícitos de REQ-F-14 y define cuándo se invoca REQ-F-26.

### DEC-16 · Menores y grupos familiares (producto)

**Pregunta:** ¿Cómo trata el producto un grupo con menor al ofrecer y ejecutar opciones?

**Contexto:** O2 tiene 1 cupo para 2 pasajeros (DAT-31). Las opciones no indican qué pasajeros cubren ni cabina (DAT-43). `create_rebooking_request` no recibe pasajeros (DAT-62).

**Trazabilidad:** SRC: `SRC-03-02`, `SRC-03-03` · REQ: `REQ-F-17`, `REQ-F-14` · GAP: `GAP-08`, `GAP-20` · DAT: `DAT-03`, `DAT-31`, `DAT-43`, `DAT-62`

**Opciones:**

- **a) Regla dura: nunca separar al grupo** ★ *recomendada* — Solo se ofrecen y ejecutan opciones que cubran a todo el grupo juntos; con un menor siempre se abre caso humano antes de rebookear.
  - A favor: Protege al menor; simple.
  - En contra: Reduce opciones ofrecidas.
- **b) Permitir opciones parciales con aviso** — Se informa que solo hay lugar para parte del grupo.
  - A favor: Más opciones.
  - En contra: Riesgo de separar a un niño de su acompañante.
- **c) Que decida el pasajero** — Se presentan todas las opciones y él elige.
  - A favor: Autonomía.
  - En contra: Traslada una decisión delicada a quien tiene menos información.

**Recomendación:** a — Es la lectura más segura de 'cambiar una reserva es de alto impacto' con un menor.

**Efecto en los requerimientos:** Añade una restricción explícita a REQ-F-17 y a la selección de opciones (REQ-F-20).

### DEC-17 · Selección y presentación de opciones

**Pregunta:** ¿Qué opciones ve el pasajero y cómo se trata `confidence`?

**Contexto:** Las opciones son candidatas, no decisión final (SRC-02-01). O1 es viable; O2 no (cupo y costo); O3 es un cascarón sin monto y sin política recuperada (DAT-31 a DAT-33). `confidence` no está definida (DAT-36).

**Trazabilidad:** SRC: `SRC-02-01`, `SRC-03-02` · REQ: `REQ-F-20`, `REQ-F-03` · GAP: `GAP-17`, `GAP-20` · DAT: `DAT-31`, `DAT-32`, `DAT-33`, `DAT-36`

**Opciones:**

- **a) Mostrar solo opciones viables y coherentes, más la vía de reembolso como alternativa** ★ *recomendada* — O1 como propuesta principal; la devolución como otra vía sin montos ni plazos; O2 no se muestra (se registra por qué).
  - A favor: Evita confundir; cumple 'no información no verificada'.
  - En contra: El pasajero no ve que existía O2.
- **b) Mostrar todas ordenadas por `confidence` con advertencias** — Transparencia completa.
  - A favor: Todo a la vista.
  - En contra: Muestra opciones inviables y un campo sin definición.
- **c) Mostrar solo la recomendada** — Una única propuesta.
  - A favor: Muy claro.
  - En contra: Poca autonomía.

**Recomendación:** a — La viabilidad (cupos, costo, política) se valida; `confidence` se usa solo para ordenar, nunca para decidir.

**Efecto en los requerimientos:** Define el filtro de REQ-F-20 y el contenido del mensaje de REQ-F-03.

### DEC-18 · Ciclo de vida del rebooking: idempotencia, 409, 503 y PENDING_CONFIRMATION

**Pregunta:** ¿Cómo se diseñan la llave idempotente y el manejo de 409/503, y qué se hace con PENDING_CONFIRMATION?

**Contexto:** 503 deja el resultado indeterminado y no hay tool para consultar estado (DAT-59, GAP-12). 409 devuelve el mismo request_id (DAT-60). PENDING_CONFIRMATION no tiene tool de confirmación y expira en ~9 min (DAT-61). La llamada no incluye reserva ni pasajeros (DAT-62).

**Trazabilidad:** SRC: `SRC-02-03`, `SRC-03-04`, `SRC-04-01` · REQ: `REQ-F-23`, `REQ-F-24`, `REQ-C-05` · GAP: `GAP-12` · DAT: `DAT-59`, `DAT-60`, `DAT-61`, `DAT-62`, `DAT-63`

**Opciones:**

- **a) Llave determinista persistida antes de llamar; 503 → mismos reintentos acotados → caso humano; 409 → existente** ★ *recomendada* — Llave derivada de la operación (reserva + vuelo/fecha + versión de política + decisión). 503: hasta 2 reintentos con la misma llave y luego caso humano, sin decirle al pasajero ni éxito ni fracaso. 409: tratar como solicitud existente. PENDING_CONFIRMATION: confirmación fuera de alcance de v1, documentada como supuesto.
  - A favor: Evita duplicados y falsas confirmaciones; coherente con el contrato.
  - En contra: Hay que documentar que la confirmación queda fuera.
- **b) 503 → caso humano inmediato** — Sin reintentos.
  - A favor: Más simple.
  - En contra: Más carga humana por fallas transitorias.
- **c) Llave aleatoria por intento** — UUID nuevo en cada llamada.
  - A favor: Trivial.
  - En contra: No es idempotente: puede duplicar un cambio de reserva.

**Recomendación:** a — Es la única variante que respeta que 503 es indeterminado y que el rebooking es de alto impacto.

**Efecto en los requerimientos:** Fija el contenido de REQ-F-23 y REQ-F-24 y la extensión documentada del contrato (reserva y pasajeros) de REQ-C-05.

### DEC-19 · Alineación de tiempos: TTL, expiración y SLA humano

**Pregunta:** ¿Cómo se concilian opciones que vencen en 2 min, una solicitud que expira en ~9 min y un caso humano con SLA de 45 min?

**Contexto:** Una aprobación humana siempre llegará con opciones vencidas y con la solicitud caducada (DAT-77, GAP-25).

**Trazabilidad:** SRC: `SRC-03-02`, `SRC-03-04`, `SRC-04-02` · REQ: `REQ-F-25`, `REQ-F-26` · GAP: `GAP-25` · DAT: `DAT-35`, `DAT-58`, `DAT-77`

**Opciones:**

- **a) Revalidar todo justo antes de escribir** ★ *recomendada* — La aprobación humana autoriza una decisión (qué opción), no la ejecución con datos viejos; al aprobar se recuperan de nuevo opciones y política. El mensaje dice «sujeto a disponibilidad».
  - A favor: Respeta TTL y versión de política.
  - En contra: El cupo puede ya no existir: hay que prever el reintento o el caso humano.
- **b) Reservar cupo durante la aprobación** — Un «hold» de asiento.
  - A favor: Asegura el cupo.
  - En contra: No existe tool para ello.
- **c) Ignorar el TTL** — Usar la opción aunque haya vencido.
  - A favor: Simple.
  - En contra: Viola REQ-F-25; puede fallar o rebookear mal.

**Recomendación:** a — No hay mecanismo de reserva en el contrato; revalidar es lo único coherente.

**Efecto en los requerimientos:** Añade el paso de revalidación a REQ-F-25 y REQ-F-26 y al flujo de aprobación.

### DEC-20 · Contrato de `notify_passenger` y validación del mensaje

**Pregunta:** ¿Cómo se construyen y validan los mensajes, y a quién se envían si la firma no incluye destinatario?

**Contexto:** La firma es `notify_passenger(message)`; el 422 solo comprueba que haya `policy_ref` (DAT-65). El requisito es más estricto: no enviar información no validada (SRC-02-05). El canal visto es PUSH y el menor no tiene contacto (DAT-71).

**Trazabilidad:** SRC: `SRC-02-05`, `SRC-04-03` · REQ: `REQ-F-16`, `REQ-F-29`, `REQ-F-09`, `REQ-C-07` · GAP: `GAP-13`, `GAP-22` · DAT: `DAT-65`, `DAT-71`

**Opciones:**

- **a) Plantillas con hechos validados + `policy_ref` + destinatario (extensión del contrato)** ★ *recomendada* — Cada mensaje sale de una plantilla cuyos huecos solo admiten hechos de una lista blanca con evidencia vigente. Un validador propio bloquea el envío si falta evidencia, `policy_ref` o destinatario. Un envío por decisión (con llave de deduplicación).
  - A favor: Cumple 'no información no validada' con evidencia; fácil de probar.
  - En contra: Mensajes menos flexibles; hay que extender el contrato en el mock.
- **b) Texto libre generado y validado luego** — Un modelo redacta y un validador revisa.
  - A favor: Más natural.
  - En contra: Validar texto libre es difícil; ver DEC-02.
- **c) Solo `policy_ref`, confiando en el 422** — Sin validador propio.
  - A favor: Mínimo esfuerzo.
  - En contra: El 422 no valida que el contenido sea verdadero.

**Recomendación:** a — Es la forma de cumplir REQ-F-16 con evidencia verificable por tests (TC-16).

**Efecto en los requerimientos:** Define la capa complementaria de REQ-F-09 (especificación del mensaje) y el validador de REQ-F-29.

---

## D · Datos, seguridad y operación

### DEC-21 · Información visible al pasajero y verificación de identidad (AMB-02)

**Pregunta:** ¿Qué campos y hechos puede ver el pasajero, y cómo se sabe que es quien dice ser?

**Contexto:** `booking_id` abre PII y no es una credencial (DAT-01). El PDF pide proteger datos y aplicar mínimo privilegio (SRC-04-07) pero no define identificación (GAP-21).

**Trazabilidad:** SRC: `SRC-04-13`, `SRC-04-07`, `SRC-01-12` · REQ: `REQ-F-12`, `REQ-F-01`, `REQ-N-04` · AMB: `AMB-02` · GAP: `GAP-21` · DAT: `DAT-01`

**Opciones:**

- **a) Sesión ya autenticada (supuesto documentado) + lista blanca de campos** ★ *recomendada* — Se asume que el pasajero llega autenticado; se muestran segmentos, horarios, estado, opciones viables y derechos citados; nunca documento, correo, teléfono completo ni nivel de fidelidad; solo nombre de pila.
  - A favor: Realista para v1; cumple mínimo privilegio.
  - En contra: Deja la autenticación como dependencia externa.
- **b) Mostrar todo lo que devuelve la tool** — Sin filtro.
  - A favor: Sin trabajo.
  - En contra: Expone PII; viola SRC-04-07.
- **c) Verificación explícita en cada consulta** — Segundo factor o datos de la reserva.
  - A favor: Más seguro.
  - En contra: Mucho más alcance y fricción.

**Recomendación:** a — Acota v1 sin exponer datos y deja la dependencia explícita.

**Efecto en los requerimientos:** Define la lista blanca de REQ-F-12 y el supuesto de REQ-F-01.

### DEC-22 · Datos personales, mínimo privilegio y «qué nunca va a un modelo»

**Pregunta:** ¿Dónde se aplica la minimización de PII y qué información nunca se entrega a un modelo?

**Contexto:** Cinco campos PII viajan en una sola lectura y el contrato de `get_eligible_options` exige el `trip_context` completo (DAT-02, DAT-79). Mantener los contratos choca con mínimo privilegio.

**Trazabilidad:** SRC: `SRC-04-07`, `SRC-01-16`, `SRC-05-04` · REQ: `REQ-N-04`, `REQ-F-27`, `REQ-D-08` · GAP: `GAP-27` · DAT: `DAT-02`, `DAT-38`, `DAT-79`

**Opciones:**

- **a) Mantener las firmas y minimizar en todas las fronteras que controlas** ★ *recomendada* — Contexto mínimo para decidir (sin correo, teléfono, documento, nivel de fidelidad; nombre de pila; `has_minor` como booleano); logs enmascarados; evidencia de casos humanos solo con ids y hechos; ningún dato personal a un modelo. Se propone al equipo un contrato reducido para `get_eligible_options`.
  - A favor: Respeta SRC-01-16 y SRC-04-07 a la vez.
  - En contra: La tool sigue recibiendo todo.
- **b) Contrato reducido en el mock** — El mock de `get_eligible_options` recibe solo el contexto mínimo.
  - A favor: Mejor privilegio.
  - En contra: Rompe «mantén estos contratos».
- **c) Sin minimización** — Pasar y registrar todo.
  - A favor: Sin trabajo.
  - En contra: Incumple SRC-04-07.

**Recomendación:** a — Es la lectura que cumple las dos instrucciones del PDF; la lista de lo que nunca va a un modelo alimenta el Entregable 3.

**Efecto en los requerimientos:** Define el inventario de REQ-N-04, el límite de REQ-F-27 y el contenido de REQ-D-08 (d).

### DEC-23 · Trazabilidad, auditoría y retención

**Pregunta:** ¿Qué se registra de cada decisión y por cuánto tiempo?

**Contexto:** Objetivo: exactitud, seguridad y trazabilidad (SRC-01-11). No hay identificador de correlación de punta a punta (DAT-73). El marco legal de retención no está definido (GAP-27).

**Trazabilidad:** SRC: `SRC-01-11`, `SRC-07-05` · REQ: `REQ-F-28`, `REQ-N-08` · GAP: `GAP-27` · DAT: `DAT-73`, `DAT-80`

**Opciones:**

- **a) Registro de decisión estructurado y sin PII** ★ *recomendada* — Un `decision_id` que ata: lecturas usadas con su `retrieved_at`, eventos elegidos y descartados con razón, versión de política y regla, variables derivadas con supuestos, opción, acción, mensaje y hashes. La retención es un parámetro a definir.
  - A favor: Reconstruible; auditable; defendible.
  - En contra: Hay que definir la retención.
- **b) Logs de aplicación sin estructura** — Mensajes de texto.
  - A favor: Rápido.
  - En contra: Difícil de reconstruir y de auditar.
- **c) Solo el resultado final** — Guardar la salida.
  - A favor: Mínimo.
  - En contra: No cumple trazabilidad.

**Recomendación:** a — Es lo que permite defender cada decisión en el debate técnico.

**Efecto en los requerimientos:** Define el contenido de REQ-F-28 y la evidencia de REQ-E-05.

### DEC-24 · Validación mínima, operación, latencia, costo y métrica de éxito

**Pregunta:** ¿Qué pruebas, presupuestos y métricas se declaran?

**Contexto:** El slice necesita al menos una validación o test (SRC-04-18). La operación debe ser viable para un equipo pequeño y hay que considerar latencia, costo y dependencia de modelos (SRC-04-08, SRC-04-09). Se pide decir cómo se mediría el resultado (SRC-07-01).

**Trazabilidad:** SRC: `SRC-01-02`, `SRC-04-08`, `SRC-04-09`, `SRC-07-01`, `SRC-07-04` · REQ: `REQ-D-05`, `REQ-N-05`, `REQ-N-06`, `REQ-N-09`, `REQ-E-01`, `REQ-E-04` · GAP: `GAP-23`, `GAP-24`

**Opciones:**

- **a) Conjunto crítico + métricas propuestas + runbook de una página** ★ *recomendada* — Pruebas: TC-01, 02, 03, 09, 14, 16 y borde de R1. Métricas propuestas: contactos al call center tras la notificación; mensajes validados sin corrección humana; casos escalados. Presupuestos como parámetros. Runbook mínimo.
  - A favor: Cubre calidad y operación con poco trabajo.
  - En contra: Las métricas son propuestas mías.
- **b) Batería amplia (TC-01 a TC-20)** — Todas las pruebas sugeridas.
  - A favor: Máxima cobertura.
  - En contra: No cabe bien en 3 horas.
- **c) Solo el caso base** — Una prueba.
  - A favor: Mínimo.
  - En contra: No demuestra criterio sobre las trampas.

**Recomendación:** a — Prioriza evidencia donde más importa (SRC-07-05).

**Efecto en los requerimientos:** Fija REQ-D-05, los presupuestos de REQ-N-05/06 y la métrica de REQ-N-09.

---

## E · Políticas externas (REVISIÓN ESTRICTA)

### DEC-35 · Marco: cómo se incorporan las políticas externas  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Las políticas de la aerolínea y las normas por país son fuente de verdad del producto, solo contexto, o se ignoran?

**Contexto:** El PDF solo define `get_policy_rules` como fuente de reglas «versionadas y verificables» (SRC-02-02). Las páginas de la aerolínea y normas por país traen umbrales distintos (por ejemplo 31 min vs 180 min; 2 h vs 240 min). Esta decisión enmarca DEC-25 a DEC-34 y conviene tomarla primero.

**Trazabilidad:** SRC: `SRC-02-02`, `SRC-04-11`, `SRC-04-10` · REQ: `REQ-P-11`, `REQ-N-07` · GAP: `GAP-01`, `GAP-02`, `GAP-03`, `GAP-04`, `GAP-05`, `GAP-06`, `GAP-07`, `GAP-08`, `GAP-09`, `GAP-10`, `GAP-14`

**Información externa para tu revisión:**

- `LEEME` → `05_Politicas_Externas/00_LEEME_Politicas.md` — Estado de captura de cada fuente y qué país importa para el caso (§3).
- `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Solo contexto: el producto usa únicamente `get_policy_rules`** ★ *recomendada* — Las políticas externas sirven para identificar brechas, riesgos y preguntas (README: supuestos y próximos pasos), no como reglas del motor.
  - A favor: Coherente con el PDF; evita afirmar derechos incorrectos; poco trabajo.
  - En contra: El producto no reflejará derechos legales que la política del PDF no incluya.
- **b) Tabla propia de políticas por jurisdicción** · *usa información externa* — Se carga una tabla versionada, revisada por Legal, que complementa a `get_policy_rules`.
  - A favor: Más completo y cercano a la realidad.
  - En contra: Fuera del alcance de 3 horas; requiere revisión legal; hay fuentes parciales o secundarias.
- **c) Ignorarlas por completo** — No se menciona nada externo.
  - A favor: Máxima simplicidad.
  - En contra: Pierde una fuente de supuestos y preguntas valiosas para la defensa.

**Recomendación:** a — Es la opción defendible con el tiempo y la información disponibles: el PDF no pide derecho comparado, pero la defensa gana si se muestran las brechas y las preguntas.

**Efecto en los requerimientos:** Determina si REQ-F-19 se apoya solo en `get_policy_rules` y qué brechas GAP-01…10 pasan a «preguntas/próximos pasos» en el README (REQ-D-07).

### DEC-25 · Jurisdicción aplicable por segmento  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Qué ley o política de país se considera para S1 (SCL→LIM) y para S2 (LIM→MEX)?

**Contexto:** Las reglas del PDF no traen país (DAT-51). Chile aplica «solo a vuelos con origen en Chile» (S1). Perú/CAN-619 aplica a quien «inicia su viaje» en un país andino; este pasajero inició en Chile, que no es miembro, así que su aplicación a S2 es ambigua. México no figura en la fuente (GAP-14).

**Trazabilidad:** SRC: `SRC-03-03` · REQ: `REQ-F-19`, `REQ-F-18` · GAP: `GAP-01`, `GAP-14` · DAT: `DAT-51` · POL: `POL-CL-00`, `POL-PE-01`, `POL-PE-16`

**Información externa para tu revisión:**

- `POL-CL-00` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Las soluciones valen solo en Chile (vuelos con origen en Chile).
- `POL-PE-01` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Decisión 619 art. 2: aplica a quien inicia su viaje en un país andino, o es transferido allí por el transportista.
- `POL-PE-16` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 24: no se pueden imponer condiciones inferiores a las de la Decisión.
- `LEEME` → `05_Politicas_Externas/00_LEEME_Politicas.md` — Estado de captura de cada fuente y qué país importa para el caso (§3).
- `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.

**Opciones:**

- **a) Solo `get_policy_rules`; jurisdicción como punto de extensión** ★ *recomendada* — v1 no aplica ley por país; se deja el campo `jurisdiction` previsto y la pregunta documentada para Producto/Legal.
  - A favor: No afirma derechos que dependen de jurisdicción y causa no modeladas.
  - En contra: No refleja diferencias legales.
- **b) Chile para S1 y CAN-619 para S2 como piso informativo** · *usa información externa* — Los mensajes citan derechos legales de cada país con revisión humana.
  - A favor: Más fiel a la realidad.
  - En contra: Ambigüedad del art. 2 de la Decisión 619; se mezclan política interna y ley.
- **c) La más favorable al pasajero** · *usa información externa* — Se aplica entre PDF, Chile y Perú lo que más beneficie.
  - A favor: Protege al pasajero.
  - En contra: Costo e incumplimiento si la política comercial es menor; requiere criterio legal.
- **d) Escalar a humano toda disputa de jurisdicción** — El sistema no decide; abre caso.
  - A favor: Evita error legal.
  - En contra: Más carga humana.

**Recomendación:** a — Con el dato disponible no se puede decidir jurisdicción sin inventar. Se documenta como supuesto bloqueante («qué preguntarías y a quién»: SRC-04-11) y se prevé la extensión.

**Efecto en los requerimientos:** Define el alcance de REQ-F-19 y la lista de preguntas del README (REQ-D-07 b, e). Condiciona DEC-26 a DEC-33.

### DEC-26 · Umbral de cambio sin costo por retraso: 180 min (PDF) vs 31 min (la aerolínea)  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Se sigue R1 (≥ 180 min) o se adopta el umbral comercial de la aerolínea (≥ 31 min)?

**Contexto:** R1 otorga REBOOK_NO_FEE desde 180 min. la aerolínea (artículos de Uruguay y página de Chile) lo da desde 31 min de retraso, y devolución si el atraso supera 3 h y el pasajero no vuela. En el caso base el retraso es de 160 min: R1 no se cumple, pero la política comercial sí daría cambio.

**Trazabilidad:** SRC: `SRC-03-03`, `SRC-04-12` · REQ: `REQ-F-11`, `REQ-F-18` · GAP: `GAP-02` · DAT: `DAT-46`, `DAT-55` · POL: `POL-UY-01`, `POL-CL-02`, `POL-CL-03`

**Información externa para tu revisión:**

- `POL-UY-01` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Retraso de 31 min o más y no conforme: cambio sin costo (mismo destino y cabina, 12 meses) o devolución sin cargo.
- `POL-CL-02` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Atraso de más de 3 h y decide no volar: devolución de pasaje y tasas.
- `POL-CL-03` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Desde 31 min de atraso: cambio (fecha, hora o destino, misma cabina) o devolución.
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Seguir R1 como regla del producto y documentar la discrepancia** ★ *recomendada* — El README registra que la política comercial publicada es más favorable y plantea la pregunta a Producto/Legal.
  - A favor: Respeta la fuente de verdad del PDF.
  - En contra: Puede decir «no corresponde» donde la aerolínea sí ofrece cambio.
- **b) Adoptar 31 min en lugar de R1** · *usa información externa* — Se reemplaza el umbral.
  - A favor: Más favorable al pasajero.
  - En contra: Contradice `get_policy_rules`; dato externo sin validar.
- **c) Escalar a humano entre 31 y 179 min** · *usa información externa* — Sin R1 ni R3, un agente confirma.
  - A favor: No promete ni niega.
  - En contra: Más casos humanos.

**Recomendación:** a — En el caso base lo que otorga el cambio sin costo es R3 (conexión), no R1; la discrepancia se declara sin alterar la política del PDF.

**Efecto en los requerimientos:** Fija el umbral de REQ-F-11 y su justificación; relacionado con DEC-05.

### DEC-27 · Asistencia durante la espera (comunicación, comida, alojamiento, traslado)  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Qué se dice sobre asistencia si la política del PDF solo tiene un vale de comida a ≥ 240 min internacional?

**Contexto:** Con 160 min de retraso R2 no aplica, pero Chile da alimentación a más de 2 h, y O1 obliga a pernoctar en Lima con un niño de 7 años (Chile y la Decisión 619 dan alojamiento y traslado en esos casos). Las reglas del PDF no tienen regla de alojamiento.

**Trazabilidad:** SRC: `SRC-03-03` · REQ: `REQ-F-18`, `REQ-F-03` · GAP: `GAP-03` · DAT: `DAT-39`, `DAT-55` · POL: `POL-CL-01`, `POL-CL-04`, `POL-PE-07`, `POL-CO-04`, `POL-UYN-02`, `POL-AR-03`

**Información externa para tu revisión:**

- `POL-CL-01` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Atraso en aeropuerto: más de 1 h conectividad; más de 2 h alimentación (y cada 3 h); más de 4 h de noche alojamiento y transporte; más de 11 h de día transporte. Excepto clima, fuerza mayor o caso fortuito.
- `POL-CL-04` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Reprogramación o cancelación: reubicación, cambio sin cargo ni diferencia tarifaria, devolución si espera más de 3 h; alojamiento si hay que pernoctar.
- `POL-PE-07` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 8: retraso más de 2 h refrigerio y llamada; más de 4 h comida; más de 6 h compensación mínima 25 % y hospedaje o reembolso; cancelación; sobreventa; conexiones.
- `POL-CO-04` → `05_Politicas_Externas/05_Colombia.md` — Demora: más de 1 h refrigerio; más de 3 h comida; más de 5 h compensación de al menos 30 % (no si sale antes de 6 h).
- `POL-UYN-02` → `05_Politicas_Externas/06_Uruguay_cartilla_DINACIA.md` — Espera de más de 4 h: comidas, alojamiento y transporte; no aplica por clima.
- `POL-AR-03` → `05_Politicas_Externas/07_Argentina_ANAC.md` — Demoras: hasta 4 h nada (salvo 00-06 h comidas); 4-8 h comidas; más de 8 h comidas, alojamiento y traslado.
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Solo lo que devuelve la política (R2)** — No se menciona otra asistencia.
  - A favor: Coherente con el PDF.
  - En contra: Silencia un pernocte que existe.
- **b) Mensaje genérico + caso humano si hay pernocte** ★ *recomendada* — «Podrías tener derecho a asistencia; un agente lo confirmará», sin cifras; se abre caso humano por el pernocte.
  - A favor: No inventa umbrales ni calla el pernocte.
  - En contra: No resuelve el detalle de inmediato.
- **c) Incorporar umbrales de Chile como reglas adicionales** · *usa información externa* — Más de 2 h comida; más de 4 h de noche alojamiento.
  - A favor: Cercano a la ley.
  - En contra: Depende de DEC-25; datos con anomalías de la fuente.

**Recomendación:** b — El pernocte es un hecho derivable de los datos (O1 sale al día siguiente); decirlo sin cifras ni promesas es veraz.

**Efecto en los requerimientos:** Añade a REQ-F-18/REQ-F-03 la mención cautelosa de asistencia y el disparador de caso humano por pernocte (REQ-F-14).

### DEC-28 · Reembolso, tarifas no reembolsables y plazos  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Qué se dice de la opción de reembolso (O3) si no hay regla ni monto y la tarifa es «no reembolsable»?

**Contexto:** `refundable:false` describe cambios voluntarios; en una modificación hecha por la aerolínea la aerolínea da derecho de devolución, y siempre devuelve las tasas de embarque. La Decisión 619 fija 5 días hábiles; Chile 10 días hábiles en sobreventa. La política `POL-REFUND-2026-01` citada por O3 no se recuperó.

**Trazabilidad:** SRC: `SRC-03-02`, `SRC-02-07` · REQ: `REQ-F-18`, `REQ-F-03` · GAP: `GAP-04`, `GAP-10` · DAT: `DAT-11`, `DAT-33` · POL: `POL-CL-07`, `POL-CL-16`, `POL-PE-10`, `POL-UY-03`

**Información externa para tu revisión:**

- `POL-CL-07` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Pérdida de conexión en la misma reserva: reubicación, cambio sin cargo ni diferencia tarifaria, devolución si decide no volar.
- `POL-CL-16` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Las tasas de embarque siempre son reembolsables; las tarifas baratas no admiten cambio ni devolución voluntaria; se evalúa por segmento.
- `POL-PE-10` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 11: reembolso dentro de 5 días hábiles.
- `POL-UY-03` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Cancelación: alternativa, nueva fecha sin costo o devolución total (incluye tasas).
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Mencionar que existe la vía de reembolso, sin monto ni plazo, y derivar** ★ *recomendada* — No se usa `refundable:false` para negar; el detalle lo confirma un agente.
  - A favor: Veraz; no promete.
  - En contra: El pasajero no ve montos.
- **b) Omitir O3 hasta tener política recuperable** — No se menciona el reembolso.
  - A favor: No afirma nada no verificable.
  - En contra: Oculta un derecho probable.
- **c) Incluir plazos y reglas de las normas** · *usa información externa* — Cinco días hábiles, 10 días hábiles, devolución de tasas.
  - A favor: Informativo.
  - En contra: Depende de DEC-25; datos externos.

**Recomendación:** a — Es veraz con la evidencia disponible y no usa la tarifa voluntaria como excusa.

**Efecto en los requerimientos:** Define el tratamiento de O3 en REQ-F-20 y el contenido de REQ-F-03; marca GAP-04 y GAP-10 como pregunta abierta.

### DEC-29 · Compensación económica (R4)  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Cuándo y cómo se habla de compensación económica?

**Contexto:** R4 solo es una bandera (`compensation_requested`), requiere humano y no trae montos. Las normas externas fijan porcentajes distintos (25 % CAN, 30 % Colombia, tablas en UF en Chile para sobreventa, euros en la UE).

**Trazabilidad:** SRC: `SRC-03-03`, `SRC-04-06` · REQ: `REQ-F-17` · GAP: `GAP-05` · DAT: `DAT-50` · POL: `POL-PE-07`, `POL-CO-04`, `POL-CO-05`, `POL-EC-01`, `POL-CL-06`

**Información externa para tu revisión:**

- `POL-PE-07` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 8: retraso más de 2 h refrigerio y llamada; más de 4 h comida; más de 6 h compensación mínima 25 % y hospedaje o reembolso; cancelación; sobreventa; conexiones.
- `POL-CO-04` → `05_Politicas_Externas/05_Colombia.md` — Demora: más de 1 h refrigerio; más de 3 h comida; más de 5 h compensación de al menos 30 % (no si sale antes de 6 h).
- `POL-CO-05` → `05_Politicas_Externas/05_Colombia.md` — Cancelación: devolución más compensación de al menos 30 % y hospedaje.
- `POL-EC-01` → `05_Politicas_Externas/10_Ecuador.md` — Ecuador (fuente secundaria): compensación mínima de 25 % del trayecto; las fuentes discrepan en los tramos.
- `POL-CL-06` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Sobreventa: opciones, devolución en 10 días hábiles y compensación en UF (la tabla tiene una fila anómala).
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Nunca proactivo; solo si el pasajero lo pide; sin montos; caso humano** ★ *recomendada* — Se cumple R4: se abre caso humano.
  - A favor: Evita promesas y errores.
  - En contra: El pasajero no recibe información proactiva.
- **b) Informar proactivamente que podría haber compensación** — Mencionar sin cifras.
  - A favor: Transparente.
  - En contra: Riesgo de promesa; depende de la causa (GAP-06).
- **c) Calcular montos con normas externas** · *usa información externa* — Usar CAN 25 %, etc.
  - A favor: Informativo.
  - En contra: Contradice la regla; sin jurisdicción ni causa.

**Recomendación:** a — Emitir una compensación es de alto impacto (SRC-04-06) y no hay base de montos en el PDF.

**Efecto en los requerimientos:** Fija el control de REQ-F-17 para compensación y el disparador de REQ-F-14.

### DEC-30 · Causa del evento y exenciones (clima, fuerza mayor)  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Cómo se trata que el evento no traiga causa si muchas normas la usan para conceder o negar derechos?

**Contexto:** Chile no da servicios por clima, fuerza mayor o caso fortuito; la Decisión 619 exige que la autoridad verifique esas causas; la UE habla de circunstancias extraordinarias. El evento DELAY no trae causa.

**Trazabilidad:** SRC: `SRC-02-08` · REQ: `REQ-F-18`, `REQ-F-16` · GAP: `GAP-06` · DAT: `DAT-22`, `DAT-49` · POL: `POL-CL-01`, `POL-PE-06`, `POL-UE-03`

**Información externa para tu revisión:**

- `POL-CL-01` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Atraso en aeropuerto: más de 1 h conectividad; más de 2 h alimentación (y cada 3 h); más de 4 h de noche alojamiento y transporte; más de 11 h de día transporte. Excepto clima, fuerza mayor o caso fortuito.
- `POL-PE-06` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 7: cancelación; liberación si avisó con 15 días o más; causas no imputables solo si las verifica la autoridad nacional.
- `POL-UE-03` → `05_Politicas_Externas/02_Union_Europea_Reg_261-2004.md` — UE: cancelación; adelanto de más de 1 h se considera cancelación; compensación salvo aviso de 14 días o circunstancias extraordinarias.
- `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.

**Opciones:**

- **a) Tratar como «causa no informada»** ★ *recomendada* — No afirmar ni negar derechos que dependan de la causa; mensaje neutral; escalar los casos donde la causa cambiaría el derecho; documentar la brecha.
  - A favor: Veraz.
  - En contra: Menos específico.
- **b) Inferir la causa** — Deducirla de otros eventos.
  - A favor: Más información.
  - En contra: Especulativo.
- **c) Pedir un campo `cause` (extensión del contrato)** — Proponer ese campo en `get_operational_events`.
  - A favor: Soluciona la raíz.
  - En contra: Cambia el contrato; es una recomendación al equipo.

**Recomendación:** a — No hay dato para otra cosa; se sugiere c como siguiente paso en el README.

**Efecto en los requerimientos:** Añade la regla DQ-29 a REQ-F-18/REQ-F-16 y una pregunta abierta en REQ-D-07.

### DEC-31 · Cancelaciones, adelantos y otros eventos  —  EXTERNA (revisión estricta)

**Pregunta:** ¿El slice cubre solo retrasos o también cancelación y adelanto?

**Contexto:** El PDF habla de «modificación» (SRC-01-09) pero solo muestra DELAY, GATE_CHANGE y STATUS, y una política DELAY. la aerolínea trata los adelantos desde 16 min; Colombia y la UE desde más de 1 h; las políticas de cancelación existen en varias normas.

**Trazabilidad:** SRC: `SRC-01-09`, `SRC-03-03` · REQ: `REQ-F-00`, `REQ-F-02` · GAP: `GAP-07` · DAT: `DAT-18`, `DAT-50` · POL: `POL-UY-02`, `POL-UY-03`, `POL-CO-07`, `POL-UE-03`

**Información externa para tu revisión:**

- `POL-UY-02` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Adelanto de 16 min o más: mismas opciones que el retraso.
- `POL-UY-03` → `05_Politicas_Externas/01_Uruguay_articulos_centro_ayuda.md` — Cancelación: alternativa, nueva fecha sin costo o devolución total (incluye tasas).
- `POL-CO-07` → `05_Politicas_Externas/05_Colombia.md` — Adelanto de más de 1 h: devolución o siguiente vuelo.
- `POL-UE-03` → `05_Politicas_Externas/02_Union_Europea_Reg_261-2004.md` — UE: cancelación; adelanto de más de 1 h se considera cancelación; compensación salvo aviso de 14 días o circunstancias extraordinarias.
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Solo DELAY; el resto degrada a humano** ★ *recomendada* — Se reconocen GATE_CHANGE y STATUS; cualquier otro tipo (cancelación, adelanto) escala.
  - A favor: Honesto sobre el alcance; coherente con DEC-04.
  - En contra: No cubre cancelaciones.
- **b) Incluir cancelación y adelanto con política mock** — Se simula `get_policy_rules('CANCELLATION')`.
  - A favor: Más amplio.
  - En contra: Se inventa política y datos.
- **c) Incluirlos con umbrales de la aerolínea** · *usa información externa* — Por ejemplo 16 min para adelanto.
  - A favor: Cercano a la práctica.
  - En contra: Información externa sin validar.

**Recomendación:** a — No hay datos ni política en el PDF para esos casos; declararlos fuera de alcance es lo defendible.

**Efecto en los requerimientos:** Delimita REQ-F-00 y deja GAP-07 documentado como próximo paso.

### DEC-32 · Definición de «menor» (R5) y derechos asociados  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Qué es un menor para activar R5?

**Contexto:** R5 no define edad. En el ejemplo P2 es `type: CHILD`, 7 años. Chile da asientos contiguos hasta los 14 años; la Decisión 619 y Uruguay tratan como especiales a los menores de 5.

**Trazabilidad:** SRC: `SRC-03-03` · REQ: `REQ-F-14`, `REQ-F-17` · GAP: `GAP-08` · DAT: `DAT-03`, `DAT-45` · POL: `POL-CL-13`, `POL-PE-02`, `POL-UYN-04`

**Información externa para tu revisión:**

- `POL-CL-13` → `05_Politicas_Externas/03_Chile_conoce-tus-derechos.md` — Menores de 14 años: asientos contiguos a un adulto de su familia o de la misma reserva.
- `POL-PE-02` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Definiciones: niños menores de 5 años son usuarios con necesidades especiales; valor neto sin tasas ni impuestos.
- `POL-UYN-04` → `05_Politicas_Externas/06_Uruguay_cartilla_DINACIA.md` — Menores de 5 años, personas con discapacidad o mayores de 70: embarque preferente.
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) `type == CHILD` (el dato del sistema)** ★ *recomendada* — Se usa la clasificación que ya trae la reserva.
  - A favor: No inventa edades; simple.
  - En contra: Depende de cómo clasifique el sistema de reservas.
- **b) Menor de 18 años** · *usa información externa* — Criterio general de minoría de edad.
  - A favor: Conservador.
  - En contra: Requiere la edad; los adultos no la traen.
- **c) Menor de 14 años** · *usa información externa* — Criterio chileno de asientos contiguos.
  - A favor: Cercano a una norma.
  - En contra: Depende de jurisdicción (DEC-25).

**Recomendación:** a — Usa el dato disponible sin importar una edad externa.

**Efecto en los requerimientos:** Fija la variable `group_includes_minor` de REQ-F-14/REQ-F-17 (REQ-F-30d).

### DEC-33 · Plazo y contenido de la notificación al pasajero  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Qué debe contener el mensaje y con cuánta anticipación se avisa?

**Contexto:** El PDF solo exige `policy_ref` y que no haya información no validada. La Decisión 619 pide avisar al menos 4 h antes y dar información preferentemente escrita de derechos; Colombia 24 h; Bolivia 4/12 h. En el ejemplo, el retraso se registró ~6 h 42 min antes de la salida original.

**Trazabilidad:** SRC: `SRC-02-05`, `SRC-04-03` · REQ: `REQ-F-03`, `REQ-F-16` · GAP: `GAP-09` · DAT: `DAT-65` · POL: `POL-PE-03`, `POL-CO-02`, `POL-BO-01`

**Información externa para tu revisión:**

- `POL-PE-03` → `05_Politicas_Externas/04_Peru_Decision_619_CAN.md` — Art. 4: informar cambios al menos 4 h antes; información preferentemente escrita de derechos ante retraso, cancelación o sobreventa.
- `POL-CO-02` → `05_Politicas_Externas/05_Colombia.md` — Informar cambios por el medio más rápido, a más tardar 24 h antes.
- `POL-BO-01` → `05_Politicas_Externas/09_Bolivia.md` — Avisar cambios al menos 4 h antes (nacional) o 12 h (internacional).
- `MATRIZ` → `05_Politicas_Externas/15_Matriz_comparativa.md` — Comparación por tema entre todas las fuentes y las reglas del PDF.

**Opciones:**

- **a) Mensaje con qué cambió (con hora), qué implica, siguiente paso, `policy_ref`, aviso de estimación y vía humana; sin plazos legales** ★ *recomendada* — No se codifican plazos legales en v1; se documentan como referencia.
  - A favor: Cumple el PDF sin importar normas.
  - En contra: No garantiza cumplir plazos de una norma si aplicara.
- **b) Además información escrita de derechos y alerta si faltan menos de 4 h** · *usa información externa* — Incorpora el art. 4 de la Decisión 619.
  - A favor: Más completo.
  - En contra: Depende de DEC-25.
- **c) Solo el estado** — Mensaje mínimo.
  - A favor: Muy simple.
  - En contra: No cumple 'siguiente paso' (SRC-01-10).

**Recomendación:** a — Cumple los requisitos del PDF y deja los plazos legales como referencia para la jurisdicción (DEC-25).

**Efecto en los requerimientos:** Define el contenido mínimo del mensaje de REQ-F-03/REQ-F-16 y la especificación de REQ-F-09.

### DEC-34 · México y otros países fuera de la fuente  —  EXTERNA (revisión estricta)

**Pregunta:** ¿Qué se hace con México, que no figura en la lista de países de la aerolínea?

**Contexto:** El destino final del caso es México. La lista de 17 países de la página de la aerolínea no lo incluye; no hay fuente en esta carpeta.

**Trazabilidad:** REQ: `REQ-F-00` · GAP: `GAP-14`

**Información externa para tu revisión:**

- `LEEME` → `05_Politicas_Externas/00_LEEME_Politicas.md` — Estado de captura de cada fuente y qué país importa para el caso (§3).
- `CRUCE` → `05_Politicas_Externas/16_Referencias_cruzadas.md` — Qué política toca qué brecha, requerimiento y decisión.

**Opciones:**

- **a) Fuera de alcance de v1; pregunta documentada** ★ *recomendada* — Se registra como pregunta para Producto/Legal.
  - A favor: Honesto; sin inventar.
  - En contra: Sin información de México.
- **b) Investigar la normativa mexicana como insumo adicional** · *usa información externa* — Una nueva ronda de recopilación.
  - A favor: Más completo.
  - En contra: No hay garantía de que el producto la use; fuera de la fuente indicada.
- **c) Asumir equivalencia con la política del PDF** — Misma regla para todo.
  - A favor: Simple.
  - En contra: Sin base.

**Recomendación:** a — La fuente que indicaste no cubre México y el PDF no lo pide.

**Efecto en los requerimientos:** Queda como pregunta abierta en REQ-D-07 (b, e).

---

## F · Presentación y uso de IA

### DEC-36 · Idioma, tono y localización de mensajes

**Pregunta:** ¿En qué idioma y con qué formato se redactan los mensajes al pasajero?

**Contexto:** El ejemplo tiene teléfono +56, tarifa en CLP y nombres en español; el PDF indica idioma es-CL en su metadata. No hay requisito de idioma en el texto.

**Trazabilidad:** SRC: `SRC-01-14` · REQ: `REQ-F-03` · GAP: `GAP-22`

**Opciones:**

- **a) Español (es-CL) con plantillas y formato local** ★ *recomendada* — Moneda CLP sin decimales; horas con zona o aeropuerto de referencia.
  - A favor: Coherente con los datos.
  - En contra: Un solo idioma.
- **b) Multiidioma** — Plantillas por idioma.
  - A favor: Más alcance.
  - En contra: Fuera de v1.
- **c) Español neutro sin localización** — Texto genérico.
  - A favor: Simple.
  - En contra: Menos preciso con moneda y horas.

**Recomendación:** a — Es lo que sugieren los datos del ejemplo.

**Efecto en los requerimientos:** Define la especificación del mensaje de REQ-F-03/REQ-F-09.

### DEC-37 · Uso de IA en este trabajo y confidencialidad del enunciado

**Pregunta:** ¿Qué registras sobre el uso de IA y cómo tratas el PDF marcado «Uso interno»? (selección múltiple)

**Contexto:** El PDF permite usar IA libremente pero exige transparencia en el Entregable 3 (SRC-06-05, SRC-05-04) y está marcado «Uso interno» en todas sus páginas (SRC-00-01).

**Trazabilidad:** SRC: `SRC-06-05`, `SRC-05-04`, `SRC-00-01` · REQ: `REQ-P-10`, `REQ-P-12`, `REQ-D-08`, `REQ-N-10`

**Opciones:**

- **a) Registrar el uso de IA para el Entregable 3** ★ *recomendada* — Herramientas (p. ej. Claude Code y el método ESF), para qué se usaron, qué se aceptó, rechazó o modificó, cómo se validó, decisiones personales y qué nunca se envía a un modelo.
  - A favor: Cumple SRC-05-04 y SRC-06-05.
  - En contra: Requiere llevar el registro.
- **b) No publicar los artefactos fuera de tu entorno** ★ *recomendada* — Los documentos generados se mantienen locales; no se suben a servicios externos ni se comparten públicamente.
  - A favor: Respeta la marca «Uso interno».
  - En contra: —
- **c) Consultar a quien envió el desafío** — Confirmar si hay restricciones adicionales de confidencialidad.
  - A favor: Certeza.
  - En contra: Costo de coordinación; el PDF ya permite IA.

**Recomendación:** a, b — a es obligatoria; b es una precaución barata coherente con la marca de confidencialidad.

**Efecto en los requerimientos:** Fija el contenido de REQ-D-08 y el tratamiento de REQ-P-12/REQ-N-10.

