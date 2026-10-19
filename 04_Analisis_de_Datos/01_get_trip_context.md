# 04.01 · `get_trip_context("ABC123")` — contexto de la reserva

- **Fuente en el PDF:** `SRC-02-07` (p. 2) · **Contrato:** `SRC-01-17` — *Lectura · "Puede devolver información parcial."*
- **Cómo leer este archivo:** (1) el ejemplo **tal cual**; (2) diccionario de campos; (3) relaciones **dentro** de esta respuesta; (4) lo que llama la atención, con severidad; (5) cuidados. Las relaciones **entre** respuestas están en `06_Analisis_cruzado.md`.
- **Severidad:** `CRÍTICA` = puede producir un mensaje o acción **incorrectos** · `ALTA` = puede distorsionar una decisión · `MEDIA` = requiere criterio explícito · `BAJA` = cosmético / a tener presente.

## 1. Ejemplo tal cual (literal del PDF)
```json
get_trip_context("ABC123")
{
  "booking_id": "ABC123",
  "passengers": [
    { "passenger_id": "P1", "name": "María Silva", "type": "ADULT",
      "email": "maria.silva@example.com", "phone": "+56 9 8765 4321",
      "document_id": "12.345.678-9", "loyalty_tier": "GOLD" },
    { "passenger_id": "P2", "name": "Tomás Silva", "type": "CHILD", "age": 7 }
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
```

## 2. Diccionario de campos
| Campo (ruta) | Tipo / formato observado | Valor | Qué se sabe | Qué **no** se sabe | Cuidado |
|---|---|---|---|---|---|
| `booking_id` | string, 6 alfanum. mayúsculas | `ABC123` | Llave de la reserva (como un PNR). Es el **argumento** de entrada. | Si es secreto, si caduca, si identifica por sí solo al titular. | **No es una credencial** (`DAT-01`). |
| `passengers[]` | array de objetos | 2 elementos | Pasajeros de la reserva. | Orden, máximo, si todos viajan en todos los segmentos (no hay mapa pasajero↔segmento). | Ver `DAT-04`. |
| `passengers[].passenger_id` | string `P<n>` | `P1`, `P2` | Identificador **local a la reserva**. | Si es estable entre llamadas o entre reservas. | Nunca usarlo como identidad global. |
| `passengers[].name` | string UTF-8 con acento | `María Silva`, `Tomás Silva` | Nombre completo. | Formato (nombre/apellido separados no existen). | **PII.** Acentos: manejar UTF-8 de punta a punta. |
| `passengers[].type` | enum observado: `ADULT`, `CHILD` | `ADULT`/`CHILD` | Clasificación del pasajero. | Si existen `INFANT`, `UNACCOMPANIED_MINOR`, etc.; **edad límite** de `CHILD`. | La política `R5` usa "menor" (`DAT-03`). |
| `passengers[].age` | entero | `7` | Solo aparece en el `CHILD`. | Si falta en adultos por diseño o por dato parcial. | **PII de menor.** |
| `passengers[].email` | string | `maria.silva@example.com` | Solo en `P1`. | Si es verificado, si es el canal preferido. | **PII.** |
| `passengers[].phone` | string E.164 con espacios | `+56 9 8765 4321` | Solo en `P1`. Prefijo **+56 = Chile**. | Si es móvil verificado; formato no normalizado (hay espacios). | **PII.** Normalizar antes de comparar. |
| `passengers[].document_id` | string con puntos y guion | `12.345.678-9` | Solo en `P1`. Formato **RUT chileno** (puntos + dígito verificador). | Tipo de documento (RUT vs pasaporte). | **PII sensible / identificador gubernamental** (`DAT-02`). |
| `passengers[].loyalty_tier` | enum observado `GOLD` | `GOLD` | Solo `P1`. | Si cambia derechos (la política del PDF **no** lo usa). | No usarlo para decidir derechos sin regla. |
| `segments[]` | array | 2 elementos | Tramos de la reserva, en orden. | Si el orden del array es el orden de viaje (parece, pero no se declara). | Ordenar por fecha/hora, no por posición. |
| `segments[].segment_id` | string `S<n>` | `S1`, `S2` | Llave usada por `get_operational_events`. | — | Es la **llave de unión** con eventos. |
| `segments[].flight_number` | string | `LA500`, `LA2410` | Prefijo `LA` = la aerolínea. | Si hay **código compartido** u otro operador. | Distinto de `option.flight_number`. |
| `segments[].origin` / `.destination` | código IATA 3 letras | `SCL→LIM`, `LIM→MEX` | Cadena continua: destino de S1 = origen de S2. | País de cada aeropuerto (no viene). | País/zona horaria deben venir de una **tabla externa** (`DAT-05`, `GAP-01`). |
| `segments[].date` | ISO `YYYY-MM-DD` | `2026-09-15` | Fecha **de salida programada** (se asume). | Fecha de **llegada**. | Retrasos que crucen medianoche (`DAT-06`). |
| `segments[].scheduled_departure` | `HH:MM` 24 h, **sin zona horaria** | `14:30`, `19:05` | Hora local (se asume del aeropuerto de salida). | **Zona horaria / offset.** | `DAT-05`. |
| `segments[].scheduled_arrival` | `HH:MM` 24 h, **sin zona horaria** | `17:55`, `23:40` | Hora local (se asume del aeropuerto de llegada). | Fecha y zona. | `DAT-05`, `DAT-06`. |
| `fare_conditions.changeable` | boolean | `true` | Cambios voluntarios permitidos (según tarifa). | Condiciones y costo. | No aplica a cambios **involuntarios** (`DAT-11`). |
| `fare_conditions.refundable` | boolean | `false` | Tarifa no reembolsable (voluntario). | Cómo se trata una devolución por **disrupción**. | `DAT-11`. |
| `fare_conditions.fare_family` | string enum | `LIGHT` | Familia tarifaria. | Equivalencia con **cabina** (la política de la aerolínea exige "misma cabina"). | `DAT-08`. |
| `fare_conditions.change_penalty_amount` | — | **ausente** | Declarado faltante en `_meta.missing_fields`. | Monto y moneda. | No inventar un costo (`DAT-09`). |
| `_meta.retrieved_at` | ISO 8601 UTC (`Z`) | `2026-09-15T11:02:31Z` | Momento de la **recuperación** (no de validez del dato). | Desde cuándo es válido cada dato. | Ancla de frescura (`DAT-10`). |
| `_meta.completeness` | enum observado `PARTIAL` | `PARTIAL` | La respuesta es incompleta. | Otros valores (¿`COMPLETE`?). | `DAT-09`. |
| `_meta.missing_fields` | array de rutas con puntos | `["fare_conditions.change_penalty_amount"]` | Qué falta. | Si la lista es **exhaustiva** (hay otros campos ausentes: cabina, estado del ticket, mapa pasajero↔segmento…). | `DAT-09`. |

## 3. Relaciones dentro de la respuesta (invariantes verificables)
| # | Invariante | ¿Se cumple en el ejemplo? |
|---|---|---|
| I-1 | `segments[0].destination == segments[1].origin` (cadena continua) | **Sí** (`LIM`). Define una **conexión**. |
| I-2 | Para cada tramo, salida < llegada (mismo reloj) | S1 `14:30 < 17:55` ✔; S2 `19:05 < 23:40` ✔ |
| I-3 | Llegada de S1 < salida de S2 en el aeropuerto de conexión | `17:55 < 19:05` ✔ → **escala planificada de 70 min** en LIM (ambas horas son de Lima: comparación **independiente de zona horaria**) |
| I-4 | `completeness == "PARTIAL"` ⇔ `missing_fields` no vacío | ✔ |
| I-5 | Cada entrada de `missing_fields` debe ser una ruta del esquema | ✔ (`fare_conditions.change_penalty_amount`) |
| I-6 | `type == "CHILD"` ⇒ existe `age` | ✔ (`P2`) |
| I-7 | Hay ≥ 1 adulto en la reserva con un menor | ✔ (`P1` adulto, `P2` niño) — **no hay campo que los vincule** (`DAT-03`) |
| I-8 | `scheduled_*` consistentes con zona horaria real | **No se puede verificar** sin zona (`DAT-05`) |

## 4. Lo que llama la atención

### DAT-01 · `booking_id` abre PII y no es una credencial — `ALTA`
Con solo `ABC123` la tool devuelve nombre, correo, teléfono y RUT. El enunciado dice que el pasajero "consulte el contexto de su viaje" (`SRC-01-12`) y exige "proteger datos personales y mínimo privilegio" (`SRC-04-07`), pero **no define cómo se identifica al pasajero** (`GAP-21`).
**Cuidado:** no mostrar PII ni confirmar existencia de la reserva con solo el código; decidir el mecanismo de verificación (`DEC-21`).

### DAT-02 · Concentración de PII y propagación — `ALTA`
`email`, `phone`, `document_id`, `name` y `age` del menor viajan en una **lectura**. Además `get_eligible_options` recibe **todo** el `trip_context` (`SRC-02-01`), y `create_human_case` recibe `evidence` (`SRC-02-04`): la PII puede propagarse a otras tools, logs y a un modelo. "Mantén estos contratos" (`SRC-01-16`) entra en tensión con "mínimo privilegio" (`SRC-04-07`).
**Cuidado:** inventario de PII y minimización antes de cualquier LLM o log (`06_Analisis_cruzado §7`, `DEC-22`).

### DAT-03 · El menor (`P2`) cambia el tratamiento y casi no tiene datos — `ALTA`
`P2` tiene solo `type` y `age`; no tiene contacto, ni vínculo explícito con un tutor, ni asiento. La regla `R5` (`group_includes_minor == true` ⇒ `PRIORITY_HANDLING`, `requires_human_approval: true`) se activa por su presencia (`SRC-03-03`). Además "menor" no está definido (¿`type==CHILD`? ¿`age<18`? ¿`<12`?) (`GAP-08`).
**Cuidado:** a un menor no se le notifica directamente; **no separar** al menor del adulto en ninguna opción (`DAT-31`); minimizar su dato (basta un booleano `has_minor`).

### DAT-04 · Campos opcionales según pasajero y ausencia de mapa pasajero↔segmento — `MEDIA`
`P1` tiene contacto, documento y nivel; `P2` no. El adulto no trae `age`. No hay mapa que diga qué pasajero viaja en qué segmento (se asume "todos en todos"). Un esquema estricto fallaría; uno laxo podría asumir de más.
**Cuidado:** validadores tolerantes con **valores faltantes explícitos** (`UNKNOWN`), no ceros ni cadenas vacías.

### DAT-05 · Horas locales **sin zona horaria** — `ALTA`
Verificado con la base de zonas horarias (tzdata) para el **2026-09-15**: Santiago **UTC-3**, Lima **UTC-5**, Ciudad de México **UTC-6**.
- **S1** SCL 14:30 → LIM 17:55: con zonas reales dura **5 h 25 min**; con "reloj único" (ignorando zonas) **3 h 25 min**.
- **S2** LIM 19:05 → MEX 23:40: con zonas reales **5 h 35 min**; con reloj único 4 h 35 min.
- La duración de S1 con zonas reales es **sospechosa** (un SCL–LIM suele ser bastante más corto; **orden de magnitud 3,5–4 h, conocimiento general, no verificado aquí**). El dato parece **sintético** y mezcla convenciones.
**Cuidado:** comparar horas **solo dentro del mismo aeropuerto** (la conexión en LIM se puede evaluar sin zonas); convertir a UTC **solo** con una tabla de zonas explícita y versionada; **nunca** calcular duraciones entre aeropuertos con horas "locales" sin offset (`GAP-15`, `DEC-08`).

### DAT-06 · No hay fecha de llegada — `MEDIA`
`date` es una sola por tramo. Si un retraso empuja la llegada pasada la medianoche (por ejemplo S2 con +90 min llegaría `01:10` del día siguiente), el dato no puede representarlo.
**Cuidado:** aritmética con fecha completa; no sumar minutos a `HH:MM` sin manejar el cambio de día.

### DAT-07 · La conexión es **implícita** — `ALTA`
No hay indicador de conexión, **tiempo mínimo de conexión (MCT)**, terminales ni protección de la conexión. Solo se infiere por la cadena `S1.destination == S2.origin` en una misma reserva. La escala planificada es de **70 min**. Que la conexión se "pierda" (`R3`) **no es un dato**: es una **conclusión derivada** (`GAP-11`).
**Cuidado:** marcar `missed_connection` como **derivado** con sus supuestos visibles (`06_Analisis_cruzado §3`, `DEC-07`).

### DAT-08 · No hay cabina ni estado del ticket — `MEDIA`
Las políticas comerciales de la aerolínea condicionan el cambio sin costo a "**misma cabina**" (`POL-UY-01`, `POL-CL-03`). Aquí solo hay `fare_family: LIGHT`. Tampoco hay estado del ticket/reserva (¿confirmada? ¿emitida?).
**Cuidado:** no afirmar "misma cabina" ni "reserva confirmada" si el dato no existe (`GAP-20`).

### DAT-09 · `PARTIAL`: qué bloquea cada dato faltante — `ALTA`
Falta `change_penalty_amount`. Si el derecho es `REBOOK_NO_FEE` (`R1`/`R3`), el costo del cambio **no debería importar**; si en cambio la regla no aplica, **no se puede cotizar** el cambio voluntario. `missing_fields` **no es exhaustivo** (cabina, estado, mapa pasajero↔segmento no figuran).
**Cuidado:** gating **por afirmación**, no por respuesta completa: p. ej. "puedes cambiar sin costo" exige regla aplicable; "costaría X" exige el monto. Nunca rellenar el monto (`GAP-17`, `DEC-11`).

### DAT-10 · `retrieved_at` es de recuperación, no de validez — `BAJA`
Las cuatro lecturas traen `_meta.retrieved_at` en UTC (`11:02:31Z` aquí). Es buena ancla de frescura de la **lectura**, pero no dice desde cuándo el dato es válido ni hasta cuándo.
**Cuidado:** guardar `retrieved_at` por dato usado en la decisión (auditoría).

### DAT-11 · `refundable:false` / `changeable:true` describen **cambios voluntarios** — `MEDIA`
Ante una **modificación hecha por la aerolínea**, la política de la aerolínea da derechos distintos a los de la tarifa (cambio sin costo; devolución sin cargo; y "siempre" devolución de tasas aunque la tarifa no sea reembolsable) (`POL-CL-16`, `POL-CL-07`, `POL-UY-01`). Usar `refundable:false` para negar una devolución sería un **error de producto**.
**Cuidado:** tratar `fare_conditions` como condiciones **voluntarias**; la decisión por disrupción debe salir de la política (`GAP-04`, `DEC-28`).

### DAT-12 · Codificación y nombres — `BAJA`
`María`, `Tomás`: UTF-8 y normalización Unicode; comparaciones sin acentos pueden causar falsos negativos.

### DAT-13 · `flight_number` — `BAJA`
`LA500` y `LA2410`: sin ceros a la izquierda, longitud variable; el prefijo es la aerolínea comercial (puede no ser el operador). No usar el número de vuelo como clave sin fecha.

### DAT-14 · `date` repetida y atada a la hora — `MEDIA`
Ambos segmentos son del mismo día; si el retraso mueve S2 al día siguiente, la `date` del tramo ya no sirve. Toda hora derivada necesita su fecha.

## 5. Cuidados (resumen operativo)
1. No confiar en `booking_id` como autenticación (`DAT-01`).
2. Minimizar PII hacia otras tools, logs y modelos (`DAT-02`).
3. Tratar `missing_fields` como **mínimo**, no como lista completa (`DAT-09`).
4. Comparaciones de hora **en el mismo aeropuerto**; conversiones solo con tabla de zonas (`DAT-05`).
5. Tratar al menor como **condición de escalamiento**, nunca como dato a exponer (`DAT-03`).
6. Distinguir **cambios voluntarios** (tarifa) de **involuntarios** (disrupción) (`DAT-11`).
