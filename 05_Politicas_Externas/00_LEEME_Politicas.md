# 05 · Políticas externas (la aerolínea y normativa por país)

> **Qué es esta carpeta.** Información que **no está en el PDF** `Disruption Companion.pdf` y que se rescató de la fuente que indicaste:
> `https://centro-ayuda.aerolinea.example/uy/es/centro-ayuda/preguntas/problemas-vuelo` y de los enlaces por país que esa página publica.
> **Nada de esto es parte del requerimiento.** Todo lo que de aquí se quiera usar es una **decisión tuya** (ver `06_Decisiones`).
> Fecha de captura: **2026-10-19**. Todo es revisable: las normas cambian (ver "Estado" abajo).

## 1. Convenciones

| Elemento | Significado |
|---|---|
| `POL-<país>-nn` | Un enunciado de política con ID. Se cita desde requerimientos, datos y decisiones. País: `UY` (artículos la aerolínea en Uruguay), `UE`, `CL`, `PE`, `CO`, `UYN` (norma uruguaya DINACIA), `AR`, `BR`, `BO`, `EC`, `PY`, `US`, `UK`, `ZA`. |
| **Fidelidad** | `PRIMARIA` = texto oficial de la norma · `la aerolínea` = página de la aerolínea · `REGULADOR` = página de la autoridad · `SECUNDARIA` = prensa/estudio jurídico (no oficial) · `VISUAL` = leído de una imagen. |
| **Paráfrasis** | Los textos están **resumidos con mis palabras**, conservando todos los umbrales, montos, plazos y artículos. No son copia literal. Para verificación estricta, abre la URL de cada archivo. |
| `[ANOMALÍA]` | Algo raro o inconsistente **dentro de la propia fuente** (no es un error mío). |
| `[NO DISPONIBLE]` | La fuente no lo dice. No lo completé de memoria. |

## 2. Estado de captura de cada fuente

| Fuente (según la página de la aerolínea) | Archivo | Estado | Fidelidad |
|---|---|---|---|
| la aerolínea en Uruguay – 5 artículos del Centro de ayuda | `01_Uruguay_articulos_centro_ayuda.md` | Completo | la aerolínea |
| **Unión Europea** (Reg. 261/2004: texto que la aerolínea publica) + DE, ES, FR, IT, PT | `02_Union_Europea_Reg_261-2004.md` | Texto de la aerolínea completo; páginas de reguladores son **índices** | la aerolínea / REGULADOR |
| **Chile** – la aerolínea "Conoce tus derechos y deberes" | `03_Chile_conoce-tus-derechos.md` | Completo (15 secciones + deberes) | la aerolínea |
| **Perú** – Decisión 619 Comunidad Andina | `04_Peru_Decision_619_CAN.md` | **Completo, texto oficial** (el enlace SICE da error SSL; se usó el PDF oficial de comunidadandina.org) | PRIMARIA |
| **Colombia** – la aerolínea | `05_Colombia.md` | 5 de 19 secciones (las de retrasos/cancelaciones/retracto/reclamos/menores); el resto (equipaje, mascotas, etc.) no se rescató por estar fuera del alcance | la aerolínea |
| **Uruguay** – Cartilla DINACIA (Res. 422/2024) | `06_Uruguay_cartilla_DINACIA.md` | PDF sin capa de texto; **leído visualmente** | VISUAL |
| **Argentina** – ANAC | `07_Argentina_ANAC.md` | **Parcial** (sin sobreventa, montos ni reclamos) | REGULADOR |
| **Brasil** – CNJ (cartilla PDF) / ANAC Res. 400 | `08_Brasil_ANAC_Res400.md` | El PDF del CNJ responde **HTTP 403**; se usó prensa/búsqueda | SECUNDARIA |
| **Bolivia** – mireclamo.bo | `09_Bolivia.md` | **Parcial** (no muestra montos ni umbrales; remite al DS 285) | REGULADOR |
| **Ecuador** – DGAC (guía PDF) | `10_Ecuador.md` | PDF oficial responde **HTTP 404**; se usó prensa y un estudio jurídico (Res. CNAC 009/2024) | SECUNDARIA |
| **Paraguay** – DINAC (guía resumida, 2015) | `11_Paraguay_guia_DINAC.md` | PDF con texto, completo; **documento de 2015**, sin umbrales numéricos | REGULADOR |
| **Estados Unidos** – DOT Fly Rights | `12_Estados_Unidos_DOT.md` | Completo, pero la página está **archivada** y advierte que puede estar superada | REGULADOR |
| **Reino Unido** – CAA | `13_Reino_Unido_CAA_UK261.md` | Completo (retrasos y cancelaciones) | REGULADOR |
| **Sudáfrica** – gov.za (Consumer Protection Act) | `14_Sudafrica.md` | La página **no trae reglas de aviación** | REGULADOR |
| (cruce) Comparativa por tema | `15_Matriz_comparativa.md` | Derivado de los anteriores | — |
| (cruce) Qué política toca qué requerimiento/brecha/decisión | `16_Referencias_cruzadas.md` | Derivado | — |

## 3. Qué país importa para el caso del PDF (hipótesis a validar)
El ejemplo del PDF es **SCL → LIM → MEX** en una sola reserva (`SRC-02-07`), con tarifa en **CLP** y teléfono **+56**. Eso sugiere:
- Tramo **S1 (SCL→LIM)**: sale de **Chile** → aplica lo de `03_Chile…`.
- Tramo **S2 (LIM→MEX)**: sale de **Perú** → aplica lo de `04_Peru…`, **pero** la Decisión 619 aplica a pasajeros que "inicien su viaje" en un país andino (art. 2 a), y este pasajero inició en Chile (que no es miembro de la CAN). **Es una ambigüedad real** (ver `GAP-01`, `DEC-25`).
- **México** (destino final) **no figura** en la lista de países de la página de la aerolínea (`GAP-14`).

## 4. Regla de uso
Ningún dato de esta carpeta se incorpora al diseño sin pasar por tu revisión. Cada punto que podría afectar al diseño está listado, con opciones y recomendación, en `06_Decisiones/FORMULARIO_DECISIONES.html`.
