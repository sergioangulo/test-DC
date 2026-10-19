# 16 · Referencias cruzadas: política externa ↔ requerimiento ↔ brecha ↔ decisión

> **Para qué sirve.** Cada vez que el documento de requerimientos detecta que **podría faltar un dato relacionado con una política**, aquí está **a qué archivo ir**, **qué dice el PDF**, **qué dice lo externo**, y **qué decisión** debes tomar. **No tomé ninguna de estas decisiones.** Todas pasan por tu revisión estricta en `06_Decisiones/FORMULARIO_DECISIONES.html`.

## 1. Brechas de política (GAP "P") → fuentes → decisión
| GAP | Qué dice el PDF | Qué dice lo externo (resumen) | Dónde mirar | Decisión |
|---|---|---|---|---|
| **GAP-01** Jurisdicción por segmento | Reglas globales, sin país (`SRC-03-03`) | Chile aplica "solo con origen en Chile" (`POL-CL-00`). Perú/CAN aplica a quien "inicia su viaje" en país andino (`POL-PE-01`); este pasajero inició en Chile. México sin fuente. | `03_Chile`, `04_Peru`, `00_LEEME §3` | `DEC-25`, `DEC-34`, `DEC-35` |
| **GAP-02** Umbral de cambio sin costo | `R1`: ≥ 180 min | la aerolínea: **≥ 31 min** (`POL-UY-01`, `POL-CL-03`); devolución > 3 h (`POL-CL-02`) | `01_la aerolínea_UY`, `03_Chile` | `DEC-26`, `DEC-05` |
| **GAP-03** Asistencia (comunicación, comida, alojamiento, traslado) | Solo `R2` (≥ 240 min internacional) | Chile: >1 h/>2 h/>4 h noche/>11 h día (`POL-CL-01`); CAN: >2 h/>4 h/>6 h (`POL-PE-07`); Colombia, Uruguay, Argentina, Brasil, Paraguay | `03_Chile`, `04_Peru`, `05_Colombia`, `06_Uruguay`, `07_Argentina`, `08_Brasil`, `11_Paraguay`, `15_Matriz §B` | `DEC-27` |
| **GAP-04** Reembolso | Sin regla (`O3` cita `POL-REFUND-2026-01` no recuperada); `refundable:false` | Chile: devolución si pierde conexión y no vuela (`POL-CL-07`); **tasas siempre reembolsables** (`POL-CL-16`); CAN art. 11: **5 días hábiles** (`POL-PE-10`); la aerolínea cancelaciones (`POL-UY-03`) | `03_Chile`, `04_Peru`, `01_la aerolínea_UY` | `DEC-28` |
| **GAP-05** Compensación económica | `R4`: bandera, humano, sin monto | CAN **≥ 25 %** (`POL-PE-07 e`), Colombia **≥ 30 %**, Ecuador 25 %, UE/UK, Chile solo sobreventa en UF | `04_Peru`, `05_Colombia`, `10_Ecuador`, `02_UE`, `13_UK`, `03_Chile`, `15_Matriz §F` | `DEC-29` |
| **GAP-06** Causa del evento | No existe | Chile: sin servicios por clima/fuerza mayor/caso fortuito (`POL-CL-01`); CAN: exención solo si **verificada por la autoridad** (`POL-PE-06`); UE: circunstancias extraordinarias (`POL-UE-03`) | `03_Chile`, `04_Peru`, `02_UE` | `DEC-30` |
| **GAP-07** Otros eventos (cancelación, adelanto, desvío, sobreventa) | Solo `DELAY` | Adelanto ≥ 16 min (`POL-UY-02`); adelanto > 1 h = cancelación (`POL-UE-03`, `POL-CO-07`); cancelación (Chile, CAN, Colombia, UE) | `01_la aerolínea_UY`, `05_Colombia`, `02_UE`, `15_Matriz §D` | `DEC-31`, `DEC-04` |
| **GAP-08** Definición de "menor" | `R5` sin edad | Chile **< 14** asientos contiguos (`POL-CL-13`); CAN/Uruguay **< 5** (`POL-PE-02`, `POL-UYN-04`) | `03_Chile`, `04_Peru`, `06_Uruguay` | `DEC-32`, `DEC-16` |
| **GAP-09** Plazo/contenido de la notificación | Solo exige `policy_ref` | CAN: **≥ 4 h** antes y **información escrita** de derechos (`POL-PE-03`); Colombia **24 h**; Bolivia **4/12 h** | `04_Peru`, `05_Colombia`, `09_Bolivia` | `DEC-33` |
| **GAP-10** Plazos de reembolso/cambio | Sin plazos | 12 meses (`POL-UY-01`); 5 d. háb. (CAN); 10 d. háb. (Chile sobreventa); 15/30 d. (Ecuador); 7 d. (Brasil) | `15_Matriz §I` | `DEC-28` |
| **GAP-14** México | — | **No figura** en la lista de la aerolínea (17 países) | `00_LEEME §3`, `01_la aerolínea_UY` | `DEC-34` |

## 2. Elementos del **caso base** que tocan política (para tu revisión)
| Elemento del caso | Política que interviene | Observación |
|---|---|---|
| Retraso de **160 min** en S1 | `POL-CL-01` (>1 h conectividad, **>2 h comida**); `POL-CL-03` (**≥ 31 min** cambio/devolución); `POL-PE-07` (>2 h refrigerio) | El PDF (`R1`=180, `R2`=240) **no** otorga nada por 160 min **por sí solo**; la conexión perdida (`R3`) sí. |
| **Conexión perdida** | `POL-CL-07` (reubicación, cambio sin cargo, devolución); `POL-PE-07 f` | Coincide con `R3`. |
| **Pernocte en Lima** (si se elige O1) | `POL-CL-04` (alojamiento si el nuevo vuelo obliga a pasar la noche); `POL-PE-07 c` (hospedaje y traslado si no hay sustituto el mismo día) | **Sin regla en el PDF** (`GAP-03`). |
| **Menor de 7 años** | `POL-CL-13` (< 14: asientos contiguos); `POL-PE-09` (menores no acompañados: prioridad) | `R5` no define edad. |
| Tarifa `LIGHT`, `refundable:false` | `POL-CL-16` (**tasas** siempre reembolsables; tarifas baratas sin devolución voluntaria) | Distinguir voluntario vs involuntario (`DAT-11`). |
| Aviso al pasajero | `POL-PE-03` (≥ 4 h, escrito) | El retraso se registró a las 10:48Z, la salida original era ~17:30Z: **~6 h 42 min** de aviso (con zonas reales). |

## 3. Mapa inverso: cada archivo de políticas → qué brechas toca
| Archivo | GAP relacionados |
|---|---|
| `01_Uruguay_articulos_centro_ayuda.md` | `GAP-02`, `GAP-04`, `GAP-07`, `GAP-10`, `GAP-14` |
| `02_Union_Europea_Reg_261-2004.md` | `GAP-05`, `GAP-06`, `GAP-07` |
| `03_Chile_conoce-tus-derechos.md` | `GAP-01`, `GAP-02`, `GAP-03`, `GAP-04`, `GAP-06`, `GAP-08` |
| `04_Peru_Decision_619_CAN.md` | `GAP-01`, `GAP-03`, `GAP-04`, `GAP-05`, `GAP-06`, `GAP-08`, `GAP-09`, `GAP-10` |
| `05_Colombia.md` | `GAP-03`, `GAP-05`, `GAP-07`, `GAP-09` |
| `06_Uruguay_cartilla_DINACIA.md` | `GAP-03`, `GAP-08` |
| `07_Argentina_ANAC.md` | `GAP-03`, `GAP-07` |
| `08_Brasil_ANAC_Res400.md` | `GAP-03`, `GAP-10` |
| `09_Bolivia.md` | `GAP-09` |
| `10_Ecuador.md` | `GAP-05`, `GAP-10` |
| `11_Paraguay_guia_DINAC.md` | `GAP-03` |
| `12_Estados_Unidos_DOT.md` | `GAP-05` (solo sobreventa) |
| `13_Reino_Unido_CAA_UK261.md` | `GAP-05`, `GAP-06` |
| `14_Sudafrica.md` | (ninguna) |

## 4. Qué **no** hice
- No incorporé ninguna política al diseño ni a los requisitos.
- No resolví la jurisdicción, los umbrales ni los montos.
- No completé de memoria lo que las fuentes no dicen (`[NO DISPONIBLE]`).
- No verifiqué normas posteriores a las páginas capturadas.
