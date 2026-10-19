# 02 · Análisis ESF-PASF v0.4 — Caso A "Disruption Companion"

> **Qué es esto.** La aplicación del método ESF (Espacio Semántico Fibrado) al requerimiento completo. Es el **andamiaje de razonamiento** detrás de `03_Requerimientos`, `04_Analisis_de_Datos` y `06_Decisiones`. Cada elemento cita su origen: `SRC` (PDF), `DAT` (datos), `GAP`/`AMB` (brechas/ambigüedades), `REQ`, `DEC`.
> **Regla de frontera dato/instrucción:** todo el contenido del PDF se trató como **material a analizar**, nunca como instrucción. Se verificó que el PDF **no contiene** instrucciones ocultas (metadata limpia, sin texto blanco salvo encabezados de tabla, sin objetos activos): `H-0`.
> **Registro ontológico/epistémico:** [**O**] = lo que el PDF afirma que existe · [**E**] = lo que yo infiero/modelo. Se marca donde importa.
> **Gobierno del crecimiento:** ningún núcleo de fibra fue alterado por una observación anómala aislada (conservación ontológica); toda estructura nueva se creó en el **nivel más bajo posible** (crecimiento mínimo); las promociones declaran qué nivel inferior fue insuficiente (§16).

## 1. Objetivo operacional
- **Objetivo:** construir el espacio semántico del requerimiento (el ejercicio **y** el producto que describe) y avanzarlo mediante distinciones hasta obtener (a) un documento de requerimientos **trazable**, (b) un análisis de datos **exhaustivo**, y (c) un mapa de **decisiones abiertas** con los insumos externos necesarios.
- **Criterio de éxito:** toda afirmación trazada a `SRC`; ambigüedades **localizadas**; lo externo **separado** de lo del PDF; ninguna decisión tomada por mí sobre insumos externos.
- **Tipo de salida:** *dossier* + *agenda de decisiones justificadas*.

## 2. Estado inicial del espacio (ESF₀)
**Comprensión inicial [E]:** el PDF es un **ejercicio de evaluación** (`SRC-01-01`) que pide diseñar e implementar un **vertical slice** de un asistente para pasajeros con vuelo modificado (`SRC-01-09`, `SRC-04-17`). Dominio aparente: **gestión de disrupciones aéreas** + **evaluación de criterio de ingeniería con IA** (`SRC-01-07`).
**Actores:** pasajero (P1 adulta, P2 niño de 7); equipo (PM, Designer, Team Lead, SWE: `SRC-01-09`); candidato; comité de 2 evaluadores (`SRC-01-04`); sistemas (7 tools).
**Hipótesis iniciales:** (i) hay un caso base resoluble combinando 3 fuentes; (ii) hay trampas deliberadas en los datos; (iii) lo no definido se debe decidir/documentar (`SRC-04-11`).

| Registro ontológico [O] (el PDF lo afirma) | Registro epistémico [E] (lo infiero) |
|---|---|
| 7 tools con firmas y consideraciones (`SRC-01-17…02-05`) | La conexión se pierde (`missed_connection`) |
| Ejemplo con 4 eventos, 3 opciones, 5 reglas | `E-1012` no es evidencia válida |
| 5 ambigüedades declaradas (`SRC-04-12…16`) | O2 es inviable; O1 es la candidata |
| Entregables y criterios (`SRC-05-02…07-09`) | Jurisdicción aplicable (CL/PE) |

## 3. Distinciones activadas
**Primitivas (de primer orden)**
| Distinción | Dónde se activó | Trazabilidad |
|---|---|---|
| ser / no ser | ¿existe el dato / la tool / la regla? (cuatro variables de política **no existen**) | `DAT-45` |
| mismo / otro | `E-1012` vs `E-1001`; `option_id` local vs global; evento vs segmento | `DAT-15`, `DAT-44` |
| conectado / no conectado | S1→S2 (conexión implícita); `booking_id` ausente en tools de escritura | `DAT-07`, `DAT-73` |
| dentro / fuera | alcance v1; jurisdicción (CL/PE/MX); lo del PDF vs lo externo | `GAP-01`, `GAP-14` |
| antes / después | `recorded_at`; TTL < expiración < SLA | `DAT-17`, `DAT-77` |
| posible / imposible | opción viable/inviable (cupos vs pasajeros) | `DAT-31` |

**Compuestas (con su composición)**
- *permanece / cambia* = (mismo/otro) ∘ (antes/después): versión de política, estado de S1 (`ON_TIME`→`DELAY`).
- *produce / no produce* = (conectado) ∘ (antes/después): retraso → llegada tardía → conexión perdida.
- *permitido / prohibido* = (posible/imposible) ∘ (dentro/fuera): "ejecutar rebooking" es **posible** (la tool existe) pero **prohibido** sin control (`SRC-04-06`).

**De apoyo:** conocido/desconocido (causa del retraso) · explícito/implícito (conexión) · literal/figurado ("sin costo" vs `fare_difference`) · real/hipotético (mundo vs modelo).

## 4. Conceptos candidatos
Pasajero · Menor · Reserva · Segmento · Conexión · Modificación · Retraso · Evento · Fuente · Frescura · Opción · Política/Regla/Derecho · Acción de alto impacto · Idempotencia · Escalamiento humano · Notificación · Información verificada · Dato personal · IA (rol) · Track · Entregable · Evidencia · Criterio de evaluación · Ambigüedad.

## 5. Fibras semánticas (concepto base, núcleo esquemático, realizaciones)
> Un concepto con una sola realización se marca **fibra unitaria provisional** y entra a la frontera como candidato a fibración (§17).

**F1 · MODIFICACIÓN** — *núcleo:* cambio respecto del plan contratado que altera la ejecución del viaje.
- `modificación@operación` (eventos `DELAY`/`GATE_CHANGE`/`STATUS`: `SRC-02-08`) · `@política` (umbral que otorga derechos: R1=180 min) · `@comercial-la aerolínea` (31 min retraso, 16 min adelanto: `POL-UY-01/02`) · `@ley-país` (retraso/cancelación/adelanto con umbrales por norma) · `@pasajero` (impacto: pierde conexión, pernocta) · `@producto` ("relevante": `AMB-01`).
- *Invariante:* diferencia respecto del plan. *Variaciones:* umbral, punto de medición, causa. *Transformación operación→pasajero:* derivar llegada y conexión (`DAT-19`, `DAT-75`).
- *Tensión:* relevancia **operativa** (un cambio de puerta) vs relevancia **para el pasajero** (`DAT-23`).

**F2 · RETRASO** — *núcleo:* diferencia temporal entre lo programado y lo real.
- `@ops` (`delay_minutes` de salida) · `@regla` (R1 ≥180, R2 ≥240) · `@la aerolínea-CL` (>1 h conectividad, >2 h comida, ≥31 min cambio, >3 h devolución: `POL-CL-01…03`) · `@CAN-619` (>2 h refrigerio, >4 h comida, >6 h compensación 25 %: `POL-PE-07`) · `@UE/UK` (llegada >3 h: `POL-UE-04`, `POL-UK-01`) · `@pasajero`.
- *Variaciones:* **dónde se mide** (salida vs llegada), inclusivo/exclusivo, causa. *Transformación @ops→@regla:* conserva minutos; **pierde** causa y punto de medición (`DAT-19`, `DAT-22`, `DAT-54`).

**F3 · CONEXIÓN** — *núcleo:* dependencia de un tramo respecto de la llegada de otro mediante un tiempo de transferencia.
- `@reserva` (cadena S1→S2, escala 70 min) · `@ops` (S2 `SCHEDULED`; MCT ausente) · `@regla` (R3 `missed_connection`) · `@ley` (CAN art. 8 f; Chile "pérdida de conexión": `POL-PE-07`, `POL-CL-07`).
- *Tensión:* dato **implícito** (no hay indicador de conexión) vs derecho **explícito** (`DAT-07`, `DAT-75`).

**F4 · OPCIÓN** — *núcleo:* alternativa candidata de resolución cuyo uso exige validación.
- `@tool` (`O1…O3`) · `@política` (`policy_ref`) · `@pasajero` (cupos vs grupo) · `@acción` (`option`→`create_rebooking_request`).
- *Tensión:* "candidata, no decisión" (`SRC-02-01`) vs necesidad de recomendar (`REQ-F-03`).

**F5 · POLÍTICA** (regla/derecho) — *núcleo:* norma que liga una **condición** a un **derecho**, con **versión**.
- `@get_policy_rules` (R1–R5, `POL-DELAY-2026-03`) · `@comercial-la aerolínea` · `@ley-país` (CL, PE-CAN, …) · `@gating` (`policy_ref` obligatorio en `notify`).
- *Tensión:* **tres capas** (reglas del PDF / política comercial / ley) con umbrales **distintos** (`GAP-01…05`).

**F6 · FUENTE/EVIDENCIA** — *núcleo:* origen y vigencia de un dato que determinan cuánto se puede afirmar.
- `@OPS_CORE` · `@AIRPORT_FEED` · `@LEGACY_MIRROR (degradada)` · `@tiempo` (`recorded_at`/`retrieved_at`/`ttl`) · `@auditoría`.
- *Invariante:* un dato sin fuente/hora no se puede afirmar. *Tensión:* recencia vs salud de la fuente (`DAT-15`, `DAT-26`).

**F7 · PASAJERO** — *núcleo:* persona afectada que recibe información y derechos.
- `@reserva` (P1, P2) · `@privacidad` (PII) · `@derecho` (menor ⇒ R5) · `@destinatario` (`notify`).
- *Tensión:* **utilidad** (mensaje personalizado) vs **privacidad** (mínimo privilegio) (`DAT-02`, `DAT-79`).

**F8 · ACCIÓN DE ALTO IMPACTO** — *núcleo:* acción costosa o irreversible que exige control previo.
- `@tool` (`create_rebooking_request`) · `@política` (`requires_human_approval`) · `@riesgo` (`503` indeterminado, duplicados) · `@tiempo` (TTL/expiración).

**F9 · ESCALAMIENTO HUMANO** — *núcleo:* intervención de una persona como control.
- `@tool` (`create_human_case`, L2, SLA 45 min) · `@política` (R4, R5) · `@producto` (`AMB-04`) · `@evaluación` (`SRC-07-07`).

**F10 · IA** (rol) — *núcleo:* modelo usado como herramienta sin delegar el criterio.
- `@runtime` (opcional: `SRC-05-01`) · `@desarrollo` (asistido: `SRC-06-05`) · `@evaluación` (transparencia: `REQ-D-08`) · `@datos` ("qué nunca entregarías": `SRC-05-04`).

**F11 · VERIFICADO** — *núcleo:* enunciado sostenido por evidencia vigente.
- `@tool` (`policy_ref`) · `@producto` ("no información no verificada": `SRC-01-10`) · `@mensaje` (validador propio: `REQ-F-29`).

**Fibras unitarias provisionales (candidatas a fibración):** IDEMPOTENCIA (solo `@rebooking`; análogos en `human_case` y `notify`) · NOTIFICACIÓN (`@tool`; falta `@legal`, `@UX`) · TRAZABILIDAD (`@objetivo`; falta `@auditoría-técnica`).

## 6. Relaciones intra-fibra (tipadas con el conjunto primitivo)
| Relación | Tipo | Qué se conserva / transforma | Trazabilidad |
|---|---|---|---|
| `retraso@ops` → `retraso@regla` | TRANSFORMS | conserva minutos; pierde causa y punto de medición | `DAT-19`, `DAT-22` |
| `modificación@operación` → `modificación@pasajero` | CAUSES (vía derivación) | agrega llegada nueva y conexión | `DAT-75` |
| `conexión@reserva` → `conexión@ops` | DEPENDS_ON | requiere MCT y estado de S2 (ausentes) | `GAP-11` |
| `política@ley` → `política@comercial` | CONSTRAINS | la ley es **piso** de la política comercial | `POL-CL-00`, `POL-PE-16` |
| `opción@tool` → `opción@acción` | TRANSFORMS | `option + key` → `request` (pierde pasajeros y reserva) | `DAT-62` |
| `fuente@degradada` → `evidencia@uso` | CONSTRAINS | excluye como evidencia primaria | `DAT-26` |
| `pasajero@reserva` → `pasajero@derecho` | TRANSFORMS | `CHILD` ⇒ `group_includes_minor` | `DAT-45` |

**Relación compuesta (sin crear primitivas nuevas):** `MISSED_CONNECTION` = `DEPENDS_ON(nueva_llegada(S1))` ∘ `DEPENDS_ON(salida(S2) − MCT)` ∘ `CAUSES(retraso)`. No es primitiva ⇒ se expresa por composición.

## 7. Relaciones inter-fibra (tipadas)
| Desde → Hasta | Tipo | Descripción | Trazabilidad |
|---|---|---|---|
| `modificación` → `derecho` (vía `política`) | CAUSES | evento + regla ⇒ derecho | `SRC-03-03` |
| `política` → `opción` | CONSTRAINS | la opción debe tener `policy_ref` vigente | `DAT-34` |
| `opción` → `pasajero` | DEPENDS_ON | cupos ≥ pasajeros; no separar al menor | `DAT-31` |
| `pasajero(menor)` → `acción` | CONSTRAINS | R5 ⇒ humano | `DAT-47` |
| `evidencia` → `notificación` | CONSTRAINS | solo hechos verificados | `SRC-02-05` |
| `acción` → `tiempo` | DEPENDS_ON | TTL/expiración obligan a revalidar | `DAT-77` |
| `humano` → `acción` | CONSTRAINS | aprobación antes de escribir | `SRC-03-03` |
| `IA` → `datos personales` | DEPENDS_ON / CONSTRAINS | qué puede ver el modelo | `SRC-05-04`, `DAT-79` |
| `delay` → `evento` | ISA | un `DELAY` es un evento | `SRC-02-08` |
| `segmento`, `conexión` → `reserva` | PART_OF | — | `SRC-02-07` |
| `evento` → `fuente` | DEPENDS_ON | credibilidad por fuente | `DAT-15` |

## 8. Dimensiones nucleares recorridas (sobre las **realizaciones**) — artefactos
| Dimensión | Aplicada a | Artefacto | Hallazgos clave | Trazabilidad |
|---|---|---|---|---|
| **Existencia** | todas las fibras | **Entidades por contexto**: existen 7 tools, 5 reglas, 3 opciones, 4 eventos. **No existen** (ausentes): tool de confirmar/consultar rebooking, causa del evento, MCT, jurisdicción, cabina, `booking_id` en escritura. | Las ausencias son **datos** | `GAP-11`, `GAP-12`, `DAT-62` |
| **Identidad** | evento, opción, regla, pasajero | **Núcleos**: un evento se identifica por `(segment, source, recorded_at, type)`, **no por `event_id`**; una regla por `(version, rule_id)`; `option_id`/`passenger_id` son **locales** | Ordenar por id es un error | `DAT-16`, `DAT-44` |
| **Relación** | §6–§7 | **Grafo relacional fibrado** (§13) | Nodos críticos: `policy_ref`, `segment_id`, "menor" | §16 |
| **Contexto** | política, ley, texto | **Mapa de validez**: `POL-DELAY-2026-03` desde 2026-03-01; ley chilena "solo en Chile (origen)"; CAN 619 "inicien su viaje"; PDF "Uso interno" | Jurisdicción no definida | `GAP-01`, `POL-CL-00`, `POL-PE-01` |
| **Temporalidad** | eventos, tools | **Secuencia temporal fibrada**: 09:30Z→10:48Z→10:55Z→lecturas 11:02Z→TTL 11:04:35Z→expira 11:12Z→SLA 45′ | TTL < expiración < SLA | `DAT-74`, `DAT-77` |
| **Cambio** | S1, rebooking, notificación | **Estados y transiciones**: S1 `ON_TIME`→`DELAY`; rebooking `∅`→`PENDING_CONFIRMATION`→**?**; notificación `∅`→`QUEUED`→**?** | Estados finales no definidos | `DAT-61`, `DAT-69` |
| **Causalidad** | caso base | **Cadena causal:** `DELAY 160` → llegada 20:35 → salida S2 19:05 ⇒ conexión perdida → `R3` → `REBOOK_NO_FEE` → `O1`; `menor` → `R5` → aprobación humana; `TTL` → revalidación. **Causalidad no probada:** causa del retraso. | La conexión perdida es **derivada** | `DAT-75`, `DAT-22` |
| **Posibilidad** | diseño y datos | **Espacio de posibilidades:** `TC-01…20`; alternativas determinístico/AI-assisted/agentic/humano por paso | Ver `06_Analisis_cruzado §9` | `REQ-F-06` |
| **Restricción** | global y contextual | **Restricciones:** 3 h; README ≤2 págs; nota ≤1 pág; no información no verificada; no alto impacto sin control; mínimo privilegio; operable por equipo pequeño; contratos de tools | Invariantes que se deben preservar | `SRC-04-04…10`, `REQ-N-*` |

## 9. Dimensiones puente (con su derivación)
| Dimensión | Se deriva de | Aplicación |
|---|---|---|
| **Propiedad** | identidad + relación + contexto | `confidence`, `completeness`, `seats_available` son **propiedades relacionales** (dependen de la opción, del grupo y del instante); **no son intrínsecas** (`DAT-36`) |
| **Información** | diferencia + posibilidad + interpretación | Qué evidencia sostiene cada afirmación; qué dato faltante cambiaría la conclusión (`change_penalty_amount`, MCT, causa) |
| **Valor** | agente + objetivo + contexto | **Pasajero:** certeza y siguiente paso. **Negocio:** menos contactos al call center. **Equipo:** operable. **Comité:** criterio. Conflictos: rapidez vs trazabilidad; automatizar vs escalar |
| **Interpretación** | contexto + relación + observador | Lecturas rivales en §12 |

## 10. Dimensiones emergentes detectadas
| Dimensión | Patrón que la justifica | Operación que la detectó |
|---|---|---|
| **Regulación** (control con feedback) | "validar antes de actuar" aparece en `422 policy_ref`, TTL de opciones, versión de política, frescura de eventos, aprobación humana | **Patrones recurrentes** |
| **Sistema** | las 7 tools + reglas + humano forman un flujo con límites | **Comunidades** |
| **Función** | la función de `create_human_case` es **absorber la incertidumbre** que el sistema no resuelve | Causalidad + Valor |
| **Adaptación** | la defensa pide "revisar decisiones ante información nueva" (`SRC-07-08`) | Regulación + Contexto |
| **Emergencia** | el **control de alto impacto** no está en ninguna tool: emerge de (evidencia vigente ∧ política vigente ∧ opción vigente ∧ idempotencia ∧ humano si aplica) | **Compresión de estructura** |

## 11. Tensiones semánticas (los 6 lugares)
| # | Lugar | Tensión encontrada | Trazabilidad |
|---|---|---|---|
| 1 | **Entre realizaciones de una misma fibra** | `retraso@regla (180)` vs `@la aerolínea (31)` vs `@CAN (2/4/6 h)`; `modificación@operación` vs `@pasajero` | `GAP-02`, `GAP-03` |
| 2 | **Entre fibras distintas** | `pasajero` (privacidad) vs `opción` (el contrato pasa `trip_context` completo); `acción` (TTL 2 min) vs `humano` (SLA 45 min) | `DAT-38`, `DAT-77` |
| 3 | **Contexto declarado vs implícito** | "mantén estos contratos" vs "mínimo privilegio"; "Uso interno" vs "uso libre de IA"; CLP/+56/SCL (Chile) vs política sin país | `SRC-01-16`, `SRC-04-07`, `SRC-00-01`, `SRC-06-05` |
| 4 | **Valor vs restricción** | reducir contactos al call center (automatizar) vs "no acciones de alto impacto sin controles" (escalar) | `SRC-01-11`, `SRC-01-10` |
| 5 | **Posibilidad vs prohibición** | **es posible** ejecutar el rebooking y notificar (las tools existen) · **está prohibido** sin control y sin validación | `SRC-04-06`, `SRC-02-05` |
| 6 | **Literal vs figurado** | "sin costo" (R3) vs `O2` con 180.000 CLP; "candidatas"; "indeterminado"; `confidence`; "relevante" | `DAT-32`, `DAT-36` |

**Objetivos en competencia (misma fibra POLÍTICA):** `@comercial` (costo mínimo) · `@ley` (protección) · `@producto` (exactitud y trazabilidad). No es contradicción lógica: es una interacción **productiva** que se resuelve en `DEC-25…35`.

## 12. Interpretaciones activas (sin colapsar) y colapsadas
**Activas** (no hay evidencia que las discrimine → frontera):
| ID | Enunciado ambiguo | Lecturas viables |
|---|---|---|
| I-1 | `delay_minutes` | retraso de **salida** / de **llegada** / acumulado |
| I-2 | alcance de `R5` | L1: gobierna solo `PRIORITY_HANDLING` · L2: condiciona **toda** acción |
| I-3 | `international` | por segmento / por reserva |
| I-4 | `409` | éxito idempotente / estado desconocido |
| I-5 | jurisdicción | Chile (S1) / Perú-CAN (S2) / ambas / la más favorable / ninguna (solo reglas del PDF) |
| I-6 | "modificación relevante" | umbral de política / impacto en itinerario / cualquier evento |
| I-7 | `confidence` | elegibilidad / disponibilidad / encaje con la política |
| I-8 | "mantén estos contratos" | firmas exactas / semántica |
| I-9 | track | Backend / Frontend |

**Colapsadas (con la evidencia que las colapsó):**
| Interpretación | Colapso | Evidencia |
|---|---|---|
| `E-1012` es el estado vigente de S1 | **Descartada** | más antiguo (−78 min) **y** fuente en `sources_degraded` (`DAT-15`) |
| `E-2003 SCHEDULED` = la conexión está a salvo | **Descartada** | mismo `recorded_at` que el retraso; no incorpora su efecto (`DAT-24`) |
| El PDF contiene instrucciones ocultas | **Descartada** | análisis de metadata, streams, render (`H-0`) |

## 13. Hipótesis revisables (con condiciones de invalidez)
> Formato obligatorio: Conclusión · Fibra · Realización · Evidencia · Supuestos · Confianza · **Condiciones de invalidez**.

**H-0 · El PDF no contiene instrucciones ocultas ni vectores activos.** *Fibra:* CONTEXTO · *Evidencia:* metadata vacía; 0 objetos JS/archivos/anotaciones; 2.563 spans visibles; texto blanco solo en encabezados sobre fondo `RGB(18,40,74)`. *Supuestos:* el análisis cubrió el archivo `Disruption Companion.pdf` tal como estaba. *Confianza:* alta. **Invalidez:** una versión distinta del archivo; un renderizador que muestre contenido distinto.

**H-1 · `E-1012` no es evidencia vigente de S1.** *Fibra:* FUENTE · *Realización:* `fuente@degradada` · *Evidencia:* −78 min respecto de `E-1001`; `LEGACY_MIRROR ∈ sources_degraded` · *Supuestos:* `recorded_at` es fiable · *Confianza:* alta. **Invalidez:** `E-1001` retractado por OPS_CORE; `OPS_CORE` marcado como degradado; evidencia de que `recorded_at` de `E-1012` es posterior.

**H-2 · `missed_connection = true` en el caso base.** *Fibra:* CONEXIÓN · *Realización:* `@reserva`/`@ops` · *Evidencia:* escala 70 min < retraso 160 min; llegada derivada 20:35 > 19:05 · *Supuestos:* **A1** propagación íntegra, **A2** sin MCT, **A3** S2 no se retiene · *Confianza:* media-alta (derivada). **Invalidez:** evento que retenga S2; `new_arrival` real ≤ 19:05 − MCT; hora de llegada de S1 distinta a la derivada.

**H-3 · El caso base exige intervención humana antes de ejecutar el rebooking.** *Fibra:* ACCIÓN/ESCALAMIENTO · *Evidencia:* `R5` (`requires_human_approval: true`) + `SRC-04-06` · *Supuestos:* **L2** de `I-2` (R5 condiciona toda acción) · *Confianza:* media. **Invalidez:** definición de "menor" que excluya a un niño de 7 años; confirmación de que `R5` solo gobierna `PRIORITY_HANDLING` (L1).

**H-4 · `O2` no es viable.** *Evidencia:* 1 cupo < 2 pasajeros; `fare_difference 180000` contradice `REBOOK_NO_FEE` · *Supuestos:* el menor viaja y no se puede separar · *Confianza:* alta. **Invalidez:** reserva con un solo pasajero a rebookear; aclaración de que el monto es de otra cabina/opción no cubierta.

**H-5 · `O3` (reembolso) no se puede afirmar con la información disponible.** *Evidencia:* `POL-REFUND-2026-01` no recuperada; sin monto/plazo; `refundable:false` · *Confianza:* alta. **Invalidez:** recuperar `get_policy_rules("REFUND")` con regla aplicable.

**H-6 · Las horas del ejemplo están "sin zona" y el dato es sintético.** *Evidencia:* con zonas reales S1 = 5 h 25 min vs 3 h 25 min con reloj único · *Confianza:* media. **Invalidez:** documentación de que las horas son locales con tabla de zonas, y duración real de S1 coincidente.

**H-7 · Aplican a este caso la norma chilena (S1) y la CAN-619 (S2, con ambigüedad).** *Evidencia:* `POL-CL-00` ("origen en Chile"), `POL-PE-01` ("inicien su viaje") · *Confianza:* baja-media. **Invalidez:** que el producto use una política **única global** y no por país; criterio legal distinto.

**H-8 · Una aprobación humana siempre llegará con opciones vencidas.** *Evidencia:* TTL 120 s; expiración ≈ 9 min; SLA 45 min · *Confianza:* alta. **Invalidez:** SLA de caso humano < TTL (improbable) o TTL renovable.

## 14. Ambigüedades y riesgos
**Ambigüedades priorizadas (término · lecturas · impacto de no resolver)**
| # | Término | Lecturas | Impacto |
|---|---|---|---|
| 1 | "modificación relevante" (`AMB-01`) | umbral / impacto / evento | Qué se comunica y a quién |
| 2 | alcance de `R5` | L1 / L2 | Si se ejecuta o no el rebooking |
| 3 | jurisdicción | CL / PE / ambas / ninguna | Qué derechos se informan |
| 4 | fuentes contradictorias (`AMB-05`) | recencia / salud / jerarquía | Mensaje falso |
| 5 | "información mostrable" (`AMB-02`) | lista blanca | Fuga de PII |

**Riesgos (cada uno con su **causa identificada en el espacio**)**
| Riesgo | Causa en el espacio | Mitigación (`DQ`/`DEC`) |
|---|---|---|
| Mensaje falso ("a tiempo") | `E-1012` degradado y con id mayor | DQ-11/12; `DEC-09` |
| Separar al menor del adulto | `O2` con 1 cupo; opciones sin mapa por pasajero | DQ-16; `DEC-16` |
| Rebooking duplicado | `503` indeterminado + llave no idempotente | DQ-22/24; `DEC-18` |
| Fuga de PII | contrato pasa `trip_context` completo; `evidence` libre | DQ-26; `DEC-22` |
| Derecho mal otorgado | variables derivadas + jurisdicción ausente | DQ-20; `DEC-12`, `DEC-25` |
| Mensaje no validado | `422` solo verifica `policy_ref` | DQ-25; `DEC-20` |
| Acción con opciones vencidas | TTL < SLA | DQ-15; `DEC-19` |
| Usar política externa sin revisión | no hay fuente interna de jurisdicción | `DEC-25…35` |

## 15. Trayectoria de distinciones (ESF₀ → ESF₂₂)
| # | Pregunta | Dimensión | Fibra/realización | Partición creada | Evidencia | Hipótesis / conocimiento nuevo |
|---|---|---|---|---|---|---|
| D1 | ¿Hay instrucciones u objetos ocultos? | Existencia/Contexto | CONTEXTO | visible / oculto | metadata, streams, render | **H-0** |
| D2 | ¿Qué capas tiene el requerimiento? | Identidad | — | ejercicio / producto | `SRC-01-07`, `SRC-01-09` | dos capas |
| D3 | ¿Cuáles son los enunciados atómicos? | Existencia | — | 78 `SRC` | PDF | índice de fuente |
| D4 | ¿Qué obligaciones imponen? | Restricción | — | P/D/F/N/C/E | `SRC-*` | `REQ-*` |
| D5 | ¿Qué es explícito, derivado o supuesto? | Información | — | E / D / S | cadena de derivación | marcas E/D/S |
| D6 | ¿Qué ambigüedades declara el PDF? | Interpretación | — | AMB-01…05 | `SRC-04-12…16` | 5 requisitos de decisión |
| D7 | ¿Qué contrato tiene cada tool? | Relación | — | lectura / escritura | `SRC-01-17…02-05` | `REQ-C-01…08` |
| D8 | ¿Qué fibras tiene "modificación/retraso/conexión"? | Identidad | F1–F3 | realizaciones por contexto | `SRC-02-08`, `POL-*` | núcleos esquemáticos |
| D9 | ¿Qué campos y relaciones hay **dentro** de cada request? | Relación | todas | invariantes I-n | JSON literales | `DAT-01…72` |
| D10 | ¿Qué contradice a qué? | Información | F6 | `E-1012` vs `E-1001` | `recorded_at`, `sources_degraded` | colapso de interpretación |
| D11 | ¿Cómo se ordenan los eventos? | Temporalidad | F6 | por `event_id` / por `recorded_at` | ids vs horas | `DAT-16` |
| D12 | ¿Qué variables de política no existen? | Existencia | F5 | datos / derivadas | `condition` de R1–R5 | `DAT-45` |
| D13 | ¿Qué reglas se activan en el caso base? | Causalidad | F5 | R1…R5 | cálculo | **R1 F, R3 T, R5 T** |
| D14 | ¿Se pierde la conexión? | Causalidad/Posibilidad | F3 | derivado / dato | 70 vs 160 min | **H-2** |
| D15 | ¿Qué opciones son viables? | Posibilidad/Restricción | F4 | viable / inviable | cupos, costo | **H-4**, **H-5** |
| D16 | ¿Qué pasa con los tiempos? | Temporalidad | F8/F9 | vigencias | TTL, expiración, SLA | **H-8** |
| D17 | ¿Qué falta que una política externa podría completar? | Información | F5 | PDF / externo | `GAP-01…10` | rescate de políticas |
| D18 | ¿Qué norma aplica a qué segmento? | Contexto | F5 | CL / PE | `POL-CL-00`, `POL-PE-01` | **H-7** |
| D19 | ¿Qué contradice la política externa a las reglas del PDF? | Relación | F2/F5 | 180 vs 31; R2 vs 2 h | `POL-*` | tensión de capas |
| D20 | ¿Qué decisiones requiere el diseño? | Valor | — | interna / externa | `GAP-*` | `DEC-01…37` |
| D21 | ¿Qué cubre la evaluación? | Valor | — | 8 dimensiones | `SRC-07-*` | `REQ-E-*` |
| D22 | ¿Qué falta por verificar? | Información | — | verificado / no | fuentes bloqueadas | frontera §17 |

## 16. Estructuras descubiertas (y la operación que las detectó)
| Estructura | Operación | Detalle |
|---|---|---|
| **Control de alto impacto** (estructura emergente) | **Patrones recurrentes** + **Compresión de estructura** | "validar antes de actuar" se repite en 5 sitios (422, TTL, versión, frescura, humano). **Promoción:** de 5 relaciones `CONSTRAINS` sueltas a una **relación emergente** `HIGH_IMPACT_GUARD`. **Nivel inferior insuficiente:** ninguna relación individual expresa que **todas** deben cumplirse a la vez. |
| **Cuatro comunidades** | **Comunidades** | (a) operación (eventos, fuentes) · (b) derechos (política, ley, opciones) · (c) riesgo/privacidad (acciones, PII) · (d) evaluación (REQ-E) |
| **Nodos centrales** | **Centralidad** | `policy_ref`/`version`, `segment_id`, "pasajero con menor" aparecen en la mayoría de las relaciones |
| **Patrón "operación única"** | **Correspondencia parcial** | `idempotency_key` (rebooking) ≈ llave de negocio de `human_case` ≈ deduplicación de `notify` |
| **Camino evento→mensaje (9 saltos)** | **Caminos mínimos** | evento → resolución → retraso → derivación → conexión → regla → derecho → opción → acción → validación → mensaje. **Huecos:** *derivación* y *validación* (no son tools) |
| **Propagación del menor** | **Propagación de activación** | menor → R5 → humano → SLA → TTL → revalidación |
| **Percolación de contradicción** | **Robustez/percolación** | si `E-1012` no se filtra: `ON_TIME` → mensaje falso → reclamo |

## 17. Frontera actual de incertidumbre
- **Fuentes externas parciales o no verificadas:** Perú (normas posteriores a la Decisión 619), Brasil (CNJ bloqueado; Res. 400 por prensa), Ecuador (PDF oficial 404; Res. CNAC 009/2024 por prensa), Argentina y Bolivia (extractos), EE. UU. (página archivada), Sudáfrica (sin reglas aéreas), México (sin fuente).
- **Interpretaciones sin discriminar:** `I-1…I-9` (§12).
- **Fibras unitarias provisionales:** IDEMPOTENCIA, NOTIFICACIÓN, TRAZABILIDAD.
- **Relaciones no tipadas:** cómo se combinan `R3` y `R5` (`DAT-47`).
- **Anomalías no acomodadas** (sin tocar ningún núcleo): duración de S1 con zonas reales; fila de la tabla de sobreventa chilena (4/3/5 UF); número de WhatsApp colombiano en la página de Chile; ventana "día" inconsistente en Chile (`POL-CL-05`).
- **Decisiones abiertas:** `DEC-01…37`.
- **Hipótesis rivales activas:** jurisdicción (`H-7`); alcance de `R5` (`H-3`).

## 18. Próximas distinciones recomendadas (por valor esperado)
> `Valor = reducción de incertidumbre + impacto en objetivo + resolución de tensiones + potencial estructural − costo` (escala 1–5). **Regla de empate:** prima la relevancia para el objetivo.

| # | Distinción a hacer | Red. inc. | Impacto | Tensiones | Estructura | Costo | **Valor** | Decisión |
|---|---|---|---|---|---|---|---|---|
| 1 | **Alcance de `R5` y precedencia con `R3`** (¿se ejecuta el rebooking con un menor?) | 5 | 5 | 4 | 3 | 1 | **16** | `DEC-13`, `DEC-16` |
| 2 | **Derivación de `missed_connection`** (A1–A3, MCT) | 5 | 5 | 3 | 3 | 1 | **15** | `DEC-07` |
| 3 | **Jurisdicción por segmento** | 5 | 4 | 4 | 3 | 2 | **14** | `DEC-25` |
| 4 | **Resolución de fuentes contradictorias y frescura** | 4 | 5 | 3 | 3 | 1 | **14** | `DEC-09`, `DEC-10` |
| 5 | **Criterio de "modificación relevante"** | 4 | 4 | 3 | 2 | 1 | **12** | `DEC-05`, `DEC-26` |
| 6 | **Ciclo de vida del rebooking** (503/409/PENDING) | 4 | 4 | 3 | 3 | 2 | **12** | `DEC-18`, `DEC-19` |
| 7 | **Track** (Backend vs Frontend) | 3 | 4 | 1 | 1 | 1 | **8** | `DEC-01` |

*(Empate 3–4: se prioriza la 3 por impacto en derechos comunicados al pasajero.)*

## 19. Síntesis provisional
**Qué se sabe.** El PDF es un ejercicio de **criterio** con dos capas (ejercicio + producto). Impone 12 requisitos de proceso, 11 de entregables, 30 funcionales (`REQ-F-00…29`, más el resultado esperado del caso base `REQ-F-30`), 10 no funcionales, 8 contratos y 9 criterios de evaluación; declara 5 ambigüedades; y yo detecté 27 brechas (`GAP`). Sus datos de ejemplo contienen **trampas verificables**: un evento obsoleto de fuente degradada, un `event_id` que no ordena, una opción inviable (1 cupo para 2 pasajeros), 4 variables de política inexistentes y vigencias incompatibles.
**Qué se ignora.** Jurisdicción, causa del evento, MCT, zonas horarias, ciclo de vida del rebooking, autenticación, métricas.
**Tensiones principales.** Automatizar vs escalar; contrato vs privacidad; tres capas de política (PDF / la aerolínea / ley).
**Hipótesis abiertas.** `H-2`, `H-3`, `H-7`.
**Interpretaciones activas.** `I-1…I-9`.
**Lo recomendable después.** Resolver, en este orden, `DEC-13/16`, `DEC-07`, `DEC-25`, `DEC-09/10`, `DEC-05/26`, `DEC-18/19`.
**Condiciones para continuar:** hay tensiones críticas no resueltas, hipótesis rivales y fuentes sin verificar. **Condiciones para detenerse provisionalmente (cumplidas):** objetivo operativo satisfecho (documentos generados), tensiones explicitadas, hipótesis con invalidez declarada, frontera declarada, próximas distinciones recomendadas. **No es un cierre absoluto.**

## Anexo · Grafo semántico fibrado (formato §21 paso 13, núcleo del caso)
```
MODIFICACIÓN
  Fibra:
    modificación@operación
      relaciones: CAUSES → modificación@pasajero (vía derivación nueva_llegada)
      propiedades: tipo∈{DELAY,GATE_CHANGE,STATUS}; fuente; recorded_at
      restricciones: ordenar por recorded_at, nunca por event_id
      incertidumbres: causa; tipos no vistos (cancelación, adelanto)
    modificación@política
      relaciones: CAUSES → derecho (R1…R5)
      propiedades: umbral R1=180 min
      restricciones: versión vigente, no superseded
      incertidumbres: jurisdicción; 31 min (la aerolínea) vs 180 min
    modificación@pasajero
      relaciones: DEPENDS_ON → conexión@reserva
      propiedades: conexión perdida (derivada), pernocte
      restricciones: no afirmar lo no verificado
      incertidumbres: MCT; retención de S2

CONEXIÓN
  Fibra:
    conexión@reserva  (S1→S2, escala 70 min)  PART_OF reserva
    conexión@regla    (R3 missed_connection)  DEPENDS_ON conexión@reserva ∘ retraso@ops
    conexión@ley      (CL pérdida de conexión; CAN art. 8 f)  CONSTRAINS política@comercial

OPCIÓN
  Fibra:
    opción@tool   (O1 viable · O2 inviable · O3 no verificable)
      restricciones: cupos ≥ pasajeros; policy_ref vigente; TTL 120 s
    opción@acción (option+key → request)  DEPENDS_ON idempotencia, humano (R5)
```
