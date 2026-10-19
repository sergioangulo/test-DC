# 04.02 · `get_operational_events(["S1","S2"])` — eventos operacionales

- **Fuente en el PDF:** `SRC-02-08` (p. 2) + `SRC-03-01` (p. 3) · **Contrato:** `SRC-01-18` — *Lectura · "Requiere controlar timestamp, fuente y frescura."*
- **Restricción asociada:** "Los datos operacionales pueden estar desactualizados o ser contradictorios entre fuentes" (`SRC-04-04`) → es **la** respuesta que ejerce esa restricción.
- Severidades: ver `01_get_trip_context.md`.

## 1. Ejemplo tal cual (literal del PDF; cruza de la p. 2 a la p. 3)
```json
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
```

## 2. Diccionario de campos
| Campo | Tipo / formato | Valores observados | Qué se sabe | Qué **no** se sabe | Cuidado |
|---|---|---|---|---|---|
| `events[]` | array | 4 eventos | Lista de eventos de los segmentos pedidos. | Orden garantizado (no lo hay); si es lista completa o ventana. | No asumir orden ni completitud (`DAT-16`, `DAT-28`). |
| `event_id` | string `E-<n>` | `E-1001`, `E-1007`, `E-1012`, `E-2003` | Identificador del evento. | Si es secuencial en el tiempo (**no lo es**, ver `DAT-16`). | **Nunca** ordenar por id. |
| `segment_id` | string | `S1`, `S2` | Segmento afectado; coincide con `trip_context.segments[].segment_id`. | — | Llave de unión. |
| `type` | enum | `DELAY`, `GATE_CHANGE`, `STATUS` | Tipo de evento; **define qué campos trae** (polimórfico). | Lista completa de tipos (¿`CANCELLATION`? ¿`ADVANCE`? ¿`DIVERSION`? ¿`EQUIPMENT_CHANGE`?). | Tipo desconocido ⇒ **fallar seguro** (`DAT-18`). |
| `new_departure` | `HH:MM` sin zona ni fecha | `17:10` | Nueva hora de salida (solo en `DELAY`). | Zona (se asume SCL: `14:30 + 160 min = 17:10`) y fecha. | `DAT-20`. |
| `delay_minutes` | entero | `160` | Minutos de retraso **de salida** (solo en `DELAY`). | Si es retraso de salida o llegada; si es acumulado. | `DAT-19`. |
| `gate` | string | `"24"` | Nueva puerta (solo en `GATE_CHANGE`). | Puerta anterior, terminal, hora de efecto. | `DAT-23`. |
| `status` | enum | `ON_TIME`, `SCHEDULED` | Estado informado (solo en `STATUS`). | Lista completa; significado preciso de `SCHEDULED`. | `DAT-15`, `DAT-24`. |
| `source` | enum | `OPS_CORE`, `AIRPORT_FEED`, `LEGACY_MIRROR` | Sistema que reporta. | **Jerarquía de confianza** entre fuentes. | `DAT-15`, `GAP-16`. |
| `recorded_at` | ISO 8601 UTC (`Z`), segundos | ver ejemplo | Cuándo se **registró** el evento. | Cuándo **entra en vigencia**; si el registro tardó. | `DAT-17`, `DAT-30`. |
| `_meta.retrieved_at` | ISO UTC | `2026-09-15T11:02:33Z` | Cuándo se recuperó. | — | Ancla de frescura. |
| `_meta.sources_available` | array | 3 fuentes | Fuentes consultadas. | Si una fuente **faltante** se omite o se marca. | `DAT-27`. |
| `_meta.sources_degraded` | array | `["LEGACY_MIRROR"]` | Fuentes con degradación **al momento de la consulta**. | Desde cuándo; qué eventos se vieron afectados. | `DAT-26`. |

## 3. Relaciones dentro de la respuesta (invariantes verificables)
| # | Invariante | ¿Se cumple? |
|---|---|---|
| I-1 | Todo `segment_id` de evento ∈ segmentos pedidos | ✔ (`S1`, `S2`) |
| I-2 | `recorded_at ≤ retrieved_at` | ✔ (el más reciente `10:55:00Z` < `11:02:33Z`) |
| I-3 | `source ∈ sources_available` | ✔ |
| I-4 | `source ∈ sources_degraded` ⇒ evento **sospechoso** | **`E-1012` cae aquí** |
| I-5 | `DELAY`: `scheduled_departure + delay_minutes == new_departure` | ✔ con datos de `trip_context`: `14:30 + 160 min = 17:10` (**relación entre dos requests**) |
| I-6 | Orden por `recorded_at` | `E-1012` (09:30) < `E-1001` = `E-2003` (10:48) < `E-1007` (10:55) |
| I-7 | Orden por `event_id` numérico | `1001 < 1007 < 1012 < 2003` → **no coincide con el tiempo** |
| I-8 | No hay dos eventos del **mismo tipo y segmento** en conflicto, salvo `STATUS` vs `DELAY` en S1 | **Hay conflicto**: `E-1012` ("ON_TIME") vs `E-1001` ("DELAY 160") |

**Edad de cada evento al recuperarlos (`11:02:33Z`):** `E-1001` 14 min 33 s · `E-1007` 7 min 33 s · `E-1012` **1 h 32 min 33 s** · `E-2003` 14 min 33 s. `E-1012` es **1 h 18 min más viejo** que `E-1001`.

## 4. Lo que llama la atención

### DAT-15 · Contradicción en S1: `ON_TIME` vs `DELAY` — `CRÍTICA`
`E-1012` (LEGACY_MIRROR, 09:30Z) dice `ON_TIME`; `E-1001` (OPS_CORE, 10:48Z) dice retraso de 160 min. Aquí **dos criterios independientes coinciden** en descartar `E-1012`: es **más antiguo** y viene de una fuente **degradada**. Pero el enunciado pide una regla general (`AMB-05`, `SRC-04-16`): ¿qué pasa si el evento más reciente viene de la fuente degradada y el sano es más viejo?
**Cuidado:** mostrar `ON_TIME` a la pasajera sería **información falsa** (`SRC-01-10`). Definir y **registrar** el criterio de resolución (`DEC-09`).

### DAT-16 · `event_id` no ordena en el tiempo — `ALTA`
`E-1012` tiene el id **más alto** de S1 pero el timestamp **más antiguo**. Si se eligiera "el último por id", se elegiría el evento degradado y obsoleto.
**Cuidado:** ordenar siempre por `recorded_at` (y desempatar por jerarquía de fuente), **jamás** por `event_id`.

### DAT-17 · Frescura: no hay umbral y hay una espera oculta — `ALTA`
Los eventos válidos tienen 14 y 7 min al recuperarse; todavía pasarán minutos hasta mostrar algo al pasajero. `recorded_at` es de **registro**, no de vigencia (`DAT-30`). El enunciado pide "controlar timestamp, fuente y frescura" (`SRC-01-18`) pero **no da umbral** (`GAP-16`).
**Cuidado:** calcular la edad **al momento de usar el dato** (no al recuperarlo), con umbral por tipo de acción (informar vs. ejecutar) (`DEC-10`).

### DAT-18 · Payload polimórfico y tipos desconocidos — `ALTA`
Los campos dependen de `type`. Hay 3 tipos; el negocio hablará también de **cancelación**, **adelanto** (la política de la aerolínea tiene umbral de **16 min** para adelantos: `POL-UY-02`; UE/Colombia: **> 1 h**), **desvío**, **cambio de equipo**. Un tipo nuevo no debe ignorarse en silencio (`GAP-07`).
**Cuidado:** validación por `type`; tipo o campo desconocido ⇒ **degradar a revisión humana / mensaje cauto**, no a "sin novedad".

### DAT-19 · `delay_minutes` mide la **salida**; no hay llegada — `ALTA`
Las normas se miden distinto: **a la salida** (Chile, Decisión 619, Colombia) o **a la llegada al destino final** (UE/UK). El evento no trae `new_arrival`. Para evaluar la conexión hay que **derivar** la llegada (supuesto: el retraso se propaga íntegro al tramo: `17:55 + 160 min = 20:35` en Lima).
**Cuidado:** declarar el supuesto de propagación (podría recuperarse tiempo en vuelo o empeorar) (`DEC-06`, `DEC-07`).

### DAT-20 · `new_departure` sin fecha ni zona — `MEDIA`
`17:10` es solo hora. Se asume **hora local de SCL** porque `14:30 + 160 = 17:10`.
**Cuidado:** validar la hora contra `scheduled_departure + delay` y registrar la zona asumida (`DEC-08`).

### DAT-21 · Redundancia `new_departure` / `delay_minutes` — `MEDIA`
Dos campos expresan lo mismo. Si no coinciden, no hay dato de cuál manda.
**Cuidado:** regla de consistencia; ante inconsistencia, **no** actuar y degradar.

### DAT-22 · No hay **causa** del retraso — `ALTA`
Casi todas las normas y políticas dependen de la causa: clima, fuerza mayor, falla técnica, control de tránsito aéreo. En Chile los servicios al pasajero **no** se dan por "eventos climáticos, fuerza mayor, caso fortuito" (`POL-CL-01`); la Decisión 619 exige que esas causas estén "debidamente verificadas por la autoridad nacional competente" (`POL-PE-06`). El evento **no trae causa** (`GAP-06`).
**Cuidado:** el sistema **no puede** afirmar ni negar derechos que dependan de la causa; debe tratarlo como "**causa no informada**" (`DEC-30`).

### DAT-23 · `GATE_CHANGE` es útil pero perecedero — `MEDIA`
Solo trae la puerta nueva (`"24"`, **string**). No hay puerta anterior, terminal ni hora de efecto. Viene de `AIRPORT_FEED` (no degradada). Las puertas cambian con frecuencia.
**Cuidado:** si se comunica, hacerlo con su hora y con la advertencia "confirma en las pantallas del aeropuerto"; no es una "modificación relevante" por sí sola (`DEC-05`).

### DAT-24 · `STATUS: SCHEDULED` del S2 no prueba que la conexión se sostenga — `ALTA`
`E-2003` se registró **en el mismo instante** que el retraso de S1 (`10:48:00Z`, `OPS_CORE`). Dice que S2 sigue programado, pero **no incorpora** el efecto de S1 sobre la conexión. **Ausencia de evento ≠ ausencia de impacto.** Tampoco hay evento "conexión protegida/retenida".
**Cuidado:** no concluir "S2 sale a la hora, la conexión está a salvo"; la conclusión correcta es "**no hay información de S2 posterior al retraso**".

### DAT-25 · Marcas de tiempo idénticas — `MEDIA`
`E-1001` y `E-2003` comparten `10:48:00Z` (probablemente un lote). Dentro de un mismo segmento, dos eventos con el mismo segundo requieren **desempate** (por jerarquía de fuente, no por id).

### DAT-26 · `sources_degraded` es a nivel de consulta — `MEDIA`
No indica **desde cuándo** está degradada la fuente: `E-1012` pudo registrarse **antes** de la degradación y ser válido en su momento; lo que sí sabemos es que ya **no es la verdad actual** porque hay un evento más nuevo de la fuente sana.
**Cuidado:** degradada ⇒ **no usar como evidencia primaria**, aunque se conserve para auditoría.

### DAT-27 · Una fuente caída no deja rastro de evento — `MEDIA`
`sources_available` incluye las tres. Si una fuente faltara, no habría eventos de ella y no habría una marca por segmento. **Ausencia de evidencia ≠ evidencia de ausencia.**

### DAT-28 · Segmentos sin eventos — `BAJA`
Se pidieron `S1` y `S2`; ambos devolvieron eventos. No se sabe qué devuelve la tool para un segmento **sin** eventos (¿lista vacía, omisión, error?).

### DAT-29 · Dependencia del `trip_context` — `MEDIA`
`segment_ids` salen de `get_trip_context`. Si esa respuesta es parcial o falta un segmento, los eventos serán incompletos sin aviso.

### DAT-30 · Los timestamps UTC son la parte **inequívoca** — `BAJA`
`recorded_at`/`retrieved_at` en UTC con segundos son la única referencia temporal sin ambigüedad en todo el ejemplo (contraste con las horas locales sin zona). Úsalos como **ancla**; considerar desfase de relojes entre sistemas.

## 5. Cuidados (resumen operativo)
1. Ordenar por `recorded_at` y desempatar por **fuente**; jamás por `event_id` (`DAT-16`, `DAT-25`).
2. Fuente degradada ⇒ no evidencia primaria (`DAT-15`, `DAT-26`).
3. Evento de tipo desconocido ⇒ degradar a humano/mensaje cauto (`DAT-18`).
4. Sin causa del evento ⇒ no afirmar derechos que dependan de ella (`DAT-22`).
5. Sin evento de S2 posterior ⇒ "sin información", **no** "sin problema" (`DAT-24`).
6. Calcular la edad del dato **al usarlo**, no al recuperarlo (`DAT-17`).
