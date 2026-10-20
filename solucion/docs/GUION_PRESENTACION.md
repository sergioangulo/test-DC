# Guion de Presentación (10 minutos) — Disruption Companion (`DOC-007`)

> **Audiencia**: Comité evaluador (2 evaluadores, sesión de 40–45 min que inicia con 10 min de presentación, `SRC-01-04`, `SRC-06-03`).  
> **Soporte**: `sdd/reports/RFC_FINAL.md`, `docs/README_INGENIERIA.md` y demo en vivo en `http://127.0.0.1:8000/`.

---

## Minuto 0:00 – 2:00 · 1. Cómo entendí y acoté el problema (`SRC-07-01`)

- **El problema real**: No es solo mostrar que un vuelo se atrasó; es combinar datos de distintas fuentes (que pueden venir degradadas o en conflicto), derivar qué implica para el itinerario completo del pasajero (como perder su conexión en Lima) y determinar con exactitud qué le corresponde según la política vigente **sin prometer nada no verificado** y **sin ejecutar cambios de alto impacto sin control**.
- **Priorización frente al límite de 3 horas (`SRC-01-02`)**:
  - Primero realizamos un levantamiento exhaustivo de **104 specs funcionales** (`sdd/specs/functional_all/`).
  - Aplicando juicio de ingeniería y alcance, dividimos los specs en **`V0` (15 specs esenciales que cumplen el 100 % del PDF)**, **`V1` (34 specs de endurecimiento y persistencia SQLite)** y **`V2` (55 specs de automatizaciones CLI, notificaciones proactivas `caller=system` y micro-interacciones avanzadas de UI)**.
  - Elegimos el **Track Backend/Integración** en **Python 3.13** acompañado de un **visor web dividido en dos zonas (`FR-114`)**: arriba la **Vista Limpia del Pasajero** (clara, amable y libre de códigos internos) y abajo el **Panel Gris de Soporte y Debug Operacional** (donde el comité y soporte pueden inspeccionar reglas, `POL-DELAY-2026-03`, opciones descartadas y trazabilidad).

---

## Minuto 2:00 – 5:00 · 2. Resolución del Caso Base y Trampas Detectadas en los Datos (`SRC-04-21`)

*(Mostrar en pantalla `http://127.0.0.1:8000/` con el escenario `BASE_TC01`)*

1. **Trampa 1 — Evento obsoleto de fuente degradada (`E-1012`)**:
   - `E-1012` afirma `ON_TIME`, tiene el ID numérico más alto (`1012 > 1001`), pero proviene de `MONITORING_FEED` (listada en `_meta.sources_degraded`) y es 8 minutos más antiguo que `E-1001` (`DELAY 160 min`).
   - Nuestro `EventResolver` excluye fuentes degradadas y ordena siempre por `recorded_at` UTC, nunca por `event_id`.
2. **Trampa 2 — Variables implícitas y regla `R1` vs `R3` y `R5`**:
   - Si alguien mira solo `160 min < 180 min` (`R1 = FALSE`), concluiría erróneamente que al pasajero no le corresponde cambio sin costo.
   - Nuestro `VariableDeriver` propaga los `160 min` sobre la llegada a Lima (`17:55 + 160m = 20:35`), detectando que supera la salida de `S2` (`19:05` → margen `-90 min` → `missed_connection = true`). Eso activa **`R3 = TRUE` (`REBOOK_NO_FEE`)**.
   - Además, al viajar un niño (`P2 CHILD`), se activa **`R5 = TRUE`**, cuya definición en la política exige **`requires_human_approval: true`**. Por lo tanto, la decisión pasa a **`PENDIENTE_APROBACION`** (gobernada por la política, no cableada en código).
3. **Trampa 3 — Opciones candidatas (`O1`, `O2`, `O3`)**:
   - `O1` (`LA2412`, 4 asientos ≥ 2 pasajeros, costo 0, `POL-DELAY-2026-03`) se selecciona como propuesta.
   - `O2` se descarta por tener solo **1 asiento para 2 pasajeros** (`INSUFFICIENT_SEATS`, no separamos a la familia) y cobrar `180.000 CLP` (`FEE_CONFLICT`).
   - `O3` (`REFUND`) cita `POL-REFUND-2025-09` (no recuperada), por lo que no se ofrece como botón automático y solo se informa como orientación no afirmativa.

---

## Minuto 5:00 – 8:00 · 3. Arquitectura, Decisiones Técnicas y Trade-offs (`SRC-07-02`, `SRC-07-06`)

- **Arquitectura Hexagonal + Clean Code verificado por AST**:
  - Dominio puro en `backend/app/domain/` sin dependencias de FastAPI ni I/O; test AST automatizado que verifica que el **100 % de las funciones tienen ≤ 10 líneas, ≤ 3 parámetros y 0 llamadas a `eval`/`exec`**.
- **Trade-off 1 — Cero IA en runtime vs Diseño híbrido para consulta ambigua (`SRC-05-01`, `SRC-07-07`)**:
  - En el camino crítico de elegibilidad y ejecución, usar un LLM introduciría riesgo de alucinación sobre costos/políticas, latencia y exposición de PII. Resolverlo con un parser determinístico y lógica trivaluada de Kleene garantiza costo 0 y 0 afirmaciones sin evidencia.
  - Para consultas libres o multi-pregunta (Tarea 2), diseñamos un clasificador AI-assisted acotado que solo mapea intenciones sobre contexto anonimizado sin permiso para invocar herramientas de escritura.
- **Trade-off 2 — Manejo de `503 UPSTREAM_TIMEOUT` indeterminado (`TC-14`)**:
  - Un `503` en `create_rebooking_request` es indeterminado: no sabemos si la reserva se modificó aguas arriba. El servicio calcula una `idempotency_key` determinística por itinerario, reintenta hasta 2 veces con la **misma llave** y, si el fallo persiste, deriva automáticamente a un especialista humano (`UPSTREAM_INDETERMINATE`).

---

## Minuto 8:00 – 10:00 · 4. Validación, Uso de IA y Próximos Pasos (`SRC-07-03`, `SRC-07-08`)

- **Evidencia verificable**: 19 tests automatizados (`19 passed`, **93 % de cobertura**) incluyendo suite E2E de los 6 escenarios y capturas reales en `sdd/screenshots/result/`.
- **Control humano sobre la IA**: Documentado en `docs/AI_USAGE_NOTE.md`. Primero, ante las ambigüedades del PDF se generó un formulario interactivo (`06_Decisiones/FORMULARIO_DECISIONES.html`) donde tomé y anoté a mano las 37 decisiones de diseño (`DOCUMENTO_DE_TRABAJO_DECISIONES.md`). Segundo, todo el desarrollo fue gobernado por un **workflow de trabajo diseñado por mí (`sdd-workflow` MCP + reglas universales de Clean Code, BPM, niveles de abstracción, SDD-TDD con WTF Review y Development Lenses `A`–`L`)**, junto con el recorte a 15 specs en V0, el desacoplamiento de la aprobación por política y la separación visual entre la vista del pasajero y el panel gris de soporte/debug.
