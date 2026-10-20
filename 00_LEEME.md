# Caso A "Disruption Companion" — Análisis de requerimientos (ESF)

> **Fuente:** `Disruption Companion.pdf` (7 págs., "Uso interno").
> **Qué hay aquí:** el análisis completo del requerimiento, la documentación de los datos de ejemplo, las políticas externas rescatadas por separado y un **formulario para que tomes las decisiones**.
> **Principio:** lo que dice el PDF y lo que **no** dice están separados. Nada externo al PDF se incorporó al diseño: pasa por tu **revisión estricta**.

## Orden de lectura recomendado
| # | Carpeta / archivo | Para qué | Tiempo aprox. |
|---|---|---|---|
| 1 | `04_Analisis_de_Datos/00_LEEME_Analisis_de_Datos.md` | Las **5 observaciones críticas** de los datos, antes que nada | 5 min |
| 2 | `03_Requerimientos/REQUERIMIENTOS.md` | Requisitos con trazabilidad; ambigüedades; **27 brechas** | 30 min |
| 3 | `04_Analisis_de_Datos/01…06` | Cada ejemplo **tal cual**, explicación, relaciones y cuidados | 45 min |
| 4 | `05_Politicas_Externas/` | Políticas de la aerolínea y normas por país (por separado) | según interés |
| 5 | `06_Decisiones/FORMULARIO_DECISIONES.html` | **Tu parte:** 37 decisiones con opciones y recomendación | 60 min |
| 6 | (botón final del formulario) | Genera el **documento de trabajo final** | — |

## Estructura
```
00_LEEME.md                         ← este archivo
Disruption Companion.pdf            ← fuente (sin modificar)
01_Fuente_y_Trazabilidad/
  01_Indice_de_fuente_SRC.md        ← 78 enunciados del PDF con ID, página y texto literal
  02_Matriz_SRC_a_REQ.md            ← qué requisito cubre cada enunciado (generada por script)
02_Analisis_ESF/
  ANALISIS_ESF.md                   ← fibras, relaciones, dimensiones, tensiones, hipótesis, trayectoria
03_Requerimientos/
  REQUERIMIENTOS.md                 ← documento de requerimientos trazable
04_Analisis_de_Datos/               ← 82 observaciones (DAT) sobre los 7 ejemplos
05_Politicas_Externas/              ← información que NO está en el PDF (la aerolínea / países)
06_Decisiones/
  FORMULARIO_DECISIONES.html        ← ábrelo en el navegador (archivo único, sin internet)
  DECISIONES_CATALOGO.md            ← la misma información, legible como documento
  decisiones.json                   ← datos del catálogo
  herramientas/                     ← fuente y generador (para regenerar si cambias algo)
```

## Sistema de IDs (cómo se traza todo)
| ID | Qué es | Dónde está |
|---|---|---|
| `SRC-pp-nn` | Enunciado del PDF (página pp) | `01_Fuente_y_Trazabilidad` |
| `REQ-P/D/F/N/C/E-nn` | Requisito (proceso, entregable, funcional, no funcional, contrato, evaluación) | `03_Requerimientos` |
| `AMB-nn` | Ambigüedad **declarada** por el PDF | `03_Requerimientos §7` |
| `GAP-nn` | Brecha que **yo** detecté | `03_Requerimientos §8` |
| `DAT-nn` | Observación sobre los datos de ejemplo | `04_Analisis_de_Datos` |
| `DQ-nn` / `TC-nn` | Regla de calidad / caso de prueba **propuestos** | `04.../06_Analisis_cruzado.md` |
| `POL-xx-nn` | Política externa (xx = país) | `05_Politicas_Externas` |
| `DEC-nn` | Decisión pendiente (tuya) | `06_Decisiones` |

**Marcas de origen en los requisitos:** **E** explícito (lo dice el PDF) · **D** derivado (deducido, con su cadena) · **S** supuesto mío (requiere tu confirmación).

## Cifras
- **78** enunciados del PDF indexados; **77** citados por algún requisito (el que no, es el título).
- **12 + 11 + 31 + 10 + 8 + 9** requisitos de proceso / entregables / funcionales / no funcionales / contratos / evaluación.
- **5** ambigüedades declaradas por el PDF; **27** brechas detectadas por mí (11 relacionadas con política externa).
- **82** observaciones de datos: **5 críticas**, 32 altas, 34 medias, 11 bajas.
- **14** archivos de fuentes externas (cubren los 17 países de la lista de la aerolínea, agrupando la UE) + 3 de apoyo (leeme, matriz, cruces) · **37** decisiones (**12** externas con revisión estricta, 25 internas).
- Verificado por script: **todos los IDs citados existen** (78 SRC · 81 REQ · 5 AMB · 27 GAP · 82 DAT · 37 DEC · 92 POL · 30 DQ · 20 TC).

## Lo más importante que encontré (resumen de 30 segundos)
1. En el caso base, la regla `R1` (≥180 min) **no** se cumple con 160 min, pero **`R3`** (conexión perdida) **sí**, y hay un **menor** (`R5` exige aprobación humana). Leer solo "160 < 180" sería un error.
2. `E-1012` ("a tiempo") es **falso**: viene de una fuente degradada y es 78 min más antiguo; además tiene el id más alto, así que ordenar por id lo elegiría.
3. `O2` es **inviable**: 1 cupo para 2 pasajeros (adulto + niño de 7) y cuesta 180.000 CLP en un caso "sin costo".
4. **4 de las 5 variables** de las reglas no existen en los datos.
5. Las vigencias son incompatibles: opciones **2 min** < solicitud **≈9 min** < caso humano **45 min**.
6. La política externa de la aerolínea (≥31 min) y las normas (Chile >2 h, Perú-CAN >2 h/4 h/6 h) son **más favorables** que las reglas del PDF; **no sabemos** si es deliberado. Es la decisión `DEC-26`/`DEC-27`.

## Qué **no** pude verificar
Ver `05_Politicas_Externas/00_LEEME_Politicas.md` (tabla de estado). En breve: Brasil (CNJ bloqueado), Ecuador (PDF oficial 404), Argentina y Bolivia (extractos parciales), EE. UU. (página archivada), Sudáfrica (sin reglas aéreas), **México (sin fuente)**, y normas posteriores a la Decisión 619 de la CAN.

## Cómo regenerar el formulario
Si editas `06_Decisiones/herramientas/decisiones_data.py`: `python generar.py` (valida que cada referencia exista y regenera el catálogo y el formulario).
