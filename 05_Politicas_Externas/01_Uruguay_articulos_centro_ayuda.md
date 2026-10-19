# 01 · la aerolínea en Uruguay — artículos del Centro de ayuda "Problemas con el vuelo"

- **Fuente (índice):** https://centro-ayuda.aerolinea.example/uy/es/centro-ayuda/preguntas/problemas-vuelo
- **Capturado:** 2026-10-19 · **Fidelidad:** la aerolínea (paráfrasis) · **Alcance geográfico:** página de Uruguay (la política comercial parece global, pero **no lo declara**; ver `[ANOMALÍA]` al final).
- El índice tiene 2 categorías: **Cambio de Itinerario** y **Cancelaciones**. La versión `/cl/` del mismo índice tiene la misma estructura.

## Estructura de artículos
| Categoría | Artículo | URL |
|---|---|---|
| Cambio de itinerario | ¿Qué pasa si mi vuelo se retrasó? | `…/cambio-itinerario/vuelo-retrasado` |
| Cambio de itinerario | ¿Qué pasa si mi vuelo se adelantó? | `…/cambio-itinerario/vuelo-adelantado` |
| Cambio de itinerario | Si mi vuelo se atrasa o se cancela, ¿cuáles son mis derechos como pasajero? | `…/cambio-itinerario/derechos-del-pasajero` |
| Cambio de itinerario | Problema con vuelos en Bogotá | `…/cambio-itinerario/problema-vuelos-bogota` |
| Cancelaciones | ¿Qué pasa si mi vuelo se canceló? | `…/cancelaciones/vuelo-cancelado` |

## POL-UY-01 · Vuelo retrasado
- **Umbral de activación:** retraso de **31 minutos o más** *y* el pasajero **no está conforme** con el nuevo horario.
- **Opciones:** (1) cambiar hora o fecha del vuelo; (2) pedir devolución del pasaje.
- **Cambio:** **sin costo**, siempre que viaje al **mismo destino y en la misma cabina**.
- **Plazo para cambiar:** hasta **12 meses desde la fecha del primer vuelo original** comprado, solo para viajes **no realizados** (el ejemplo del artículo: viaje del 10-jun-2022 → hasta 10-jun-2023).
- **Proceso:** con **número de orden / código de reserva**: (1) ver el itinerario propuesto — si lo acepta, **no debe hacer nada**; (2) si cambia, elegir otra fecha y ver vuelos disponibles; (3) elegir vuelo (puede modificar también otros vuelos del itinerario); (4) aceptar términos y confirmar.
- **Devolución:** **sin cargo**, desde "Mis viajes". Si el pasaje se pagó con **Millas la aerolínea Pass**, según la fecha del canje se abona **a la aerolínea Wallet**.

## POL-UY-02 · Vuelo adelantado
- **Umbral:** adelanto de **16 minutos o más** *y* no conforme.
- Mismas opciones, condiciones, plazo de 12 meses y proceso que POL-UY-01.
- **Devolución con millas:** según fecha del canje, se abona **a cuenta bancaria o a la aerolínea Wallet** (difiere de POL-UY-01, que solo menciona Wallet). `[ANOMALÍA]`: la diferencia entre ambos artículos no se explica.

## POL-UY-03 · Vuelo cancelado
- El pasajero puede quedarse con la alternativa ofrecida, **elegir nueva fecha** o **pedir devolución**.
- **Nueva fecha:** sin costo, mismo destino y cabina; 12 meses; mismo proceso (itinerario propuesto → otras fechas → confirmar).
- **Devolución:** se devuelve la **totalidad de vuelos y servicios comprados y no usados, más tasas e impuestos aplicables**. Se solicita en "Mis viajes → Devolución de pasajes". (Hay una sub-pregunta "¿Cómo recibiré la devolución?" cuyo contenido no se desplegó en la captura: **[NO DISPONIBLE]**).
- **Contactar al Contact Center solo si:** quiere **cambiar el destino**, o quiere cambiar y tiene **reserva de hotel u otro servicio la aerolínea Travel**.

## POL-UY-04 · Derechos del pasajero (índice por país)
Página que lista **17 países** "desde donde despegan los vuelos de la aerolínea": Alemania, Argentina, Bolivia, Brasil, Chile, Colombia, Ecuador, Estados Unidos, España, Francia, Italia, Paraguay, Perú, Portugal, Sudáfrica, Reino Unido, Uruguay. **Cada país es un enlace externo** (regulador o página legal de la aerolínea; ver `00_LEEME`). Debajo muestra, por defecto, el texto del **Reglamento europeo 261/2004** (ver `02_Union_Europea_Reg_261-2004.md`).
- **No aparece México** en la lista.

## POL-UY-05 · "Problema con vuelos en Bogotá"
- Contexto: el aeropuerto El Dorado supera su capacidad operacional en ciertas horas; la Aerocivil aplica con frecuencia el **Programa de Demoras en Tierra (GDP)**, que genera retrasos/reprogramaciones. Se aplica ante situaciones extremas (clima adverso, falta de personal aeronáutico) y, según el artículo, **desde el 29 de mayo** de forma regular por la sobredemanda de aviación no regular y de Estado (el año **no se indica**; `[ANOMALÍA]`).
- Si un vuelo fue cancelado o reprogramado, el pasajero puede **aceptar el nuevo itinerario**, **elegir nueva fecha** o **pedir devolución**; se verifica en "Mis viajes".

## `[ANOMALÍA]` / puntos a revisar
1. Los artículos **no declaran jurisdicción** ni si aplican a vuelos con origen fuera de Uruguay. El artículo Chile (`03`) sí declara "válido solo en Chile".
2. El umbral **31 min** (retraso) coincide con Chile (`POL-CL-03`); el umbral de **16 min** (adelanto) aparece solo aquí.
3. Las reglas del PDF (`R1: delay_minutes ≥ 180`) **no coinciden** con el umbral comercial de 31 min → ver `GAP-02`, `DEC-26`.
