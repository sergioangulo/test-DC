# ⚠️ DESIGN_CONTRACT — Disruption Companion

> **ESTE DOCUMENTO ES SAGRADO E INMUTABLE.**
> Define cómo se ve y se siente el producto. Cambiar el design system, los componentes base
> o los tokens visuales sin coordinación produce inconsistencia visual y rompe la experiencia.
> Solo modificar bajo el mismo proceso que un cambio de contrato externo.

**Tipo de proyecto**: fullstack (backend Python/FastAPI + front React de prueba; este contrato cubre el front)
**Versión:** v1.5 (ronda 6 de A2, diseñador: alerta de pernocte en la pantalla 2, textos de los siete resultados, variante de error del diálogo, estados del `ScenarioSelector`, foco tras un «Reintentar» fallido y cierre de DEBT-A1-08; v1.4, ronda 5, NFR-013: los textos del proveedor se muestran como texto plano; ronda 3: cambio de puerta destacado, botón «Actualizar»; ronda 4: segmentos `NO_EVENTS`, definición de la alerta `gate`, orden de alertas) · **Fecha:** 2026-10-19 · **Paso SDD:** A1 · **Fuentes:** `docs/REQUERIMIENTOS_V1.md` (FR-003, FR-004, FR-006, FR-014, FR-023, FR-039, FR-046, FR-050, FR-056, FR-058, FR-060, FR-066, FR-067, FR-068, FR-071, FR-105, FR-111…FR-113, NFR-004, NFR-011), `sdd/reports/EXTERNAL_CONTRACTS.md` (esquema `TripView`).
**Design System**: no existe una librería corporativa disponible para este proyecto. Se usa **CSS propio con tokens** (variables en `:root`), descrito en este documento.

---

## Framework y Librería de Diseño

El usuario pidió que el front tenga el *look & feel* del centro de ayuda de la aerolínea (`https://centro-ayuda.aerolinea.example/uy/es/centro-ayuda/preguntas/problemas-vuelo`) **sin logos ni marcas registradas** (FR-111). Por eso:

- **No se usa ninguna librería de componentes** (ni Material, ni Bootstrap, ni un design system de la aerolínea). Los componentes son propios, en React, con CSS plano y tokens.
- **Los valores de color, tipografía y radios de este documento son APROXIMACIONES de la identidad visual** (índigo profundo, rojo de acento, superficie clara). **No fueron extraídos de la web** (el sitio no se pudo inspeccionar desde este entorno: ver §Evidencia Visual). Si el equipo obtiene los valores oficiales, cambian los tokens, no los componentes (proceso al final).
- **Prohibido:** logotipos, isotipos, nombre comercial en el encabezado, imágenes, íconos o tipografías propietarias de la aerolínea. El encabezado muestra un texto genérico («Ayuda para tu viaje»).
- **Íconos:** SVG propio, en línea, siempre con `aria-hidden="true"` y acompañados de texto (`Icon` con las formas `info`, `alerta`, `error`, `check`, `cruz`, `pregunta`, `reloj`, `puerta`). **No se usan glifos de texto** (⚠ ✖ ℹ) porque su aspecto depende de la fuente del sistema. En los wireframes ASCII se representan como `(i)`, `(!)`, `(x)`, `(ok)`, `(?)`.
- Idioma: español neutro sin localización (FR-113). `<html lang="es">`. **Todo texto visible sale del catálogo de plantillas** (`frontend/src/i18n/`): ninguna cadena visible fuera del catálogo; un test recorre los componentes y lo verifica. Los mensajes dinámicos del backend (`messages[].text`) se pintan tal cual llegan, sin recomponerlos: salen del catálogo de plantillas del servidor (FR-080) y pasan por su validador (FR-081), por eso la prueba de catálogo del front (FR-113) los exime y verifica todo el resto (cierra la segunda parte de DEBT-A1-08).

### Importaciones base

```css
/* frontend/src/styles/tokens.css — única fuente de colores, tipografía, espaciado y radios */
@import "./tokens.css";
/* Los componentes solo usan var(--...); un color hexadecimal fuera de tokens.css es un defecto. */
```

```tsx
// Componentes propios: frontend/src/components/<Nombre>/<Nombre>.tsx + <Nombre>.css
import { Header } from "./components/Header/Header";
import { TripSummary } from "./components/TripSummary/TripSummary";
```

---

## Inventario de Componentes

Cada componente es propio. «Versión» es la del contrato (v1.3). La lista de componentes **no cambia**: el estado informativo y el cambio de puerta usan `TripSummary`, `SegmentRow`, `AlertBanner` (variante `gate`) y `RulesPanel`, y simplemente no incluyen `ActionBar`; solo se añade el auxiliar `RefreshButton`. Todos reciben datos del `TripView` ya validado; ninguno calcula reglas de negocio.

| Componente | Package | Versión | Dónde se usa | Variantes |
|-----------|---------|---------|-------------|---------|
| `Header` | propio (`components/Header`) | v1.3 | Parte superior de toda pantalla (`<header>`, contiene el `h1` «Ayuda para tu viaje», sin logo). Franja superior de 4 px en `--color-accent` (solo decorativa) | `default`; contiene el `ScenarioSelector` solo en desarrollo; el anillo de foco dentro del Header es blanco |
| `TripSummary` | propio (`components/TripSummary`) | v1.3 | Primera tarjeta de la vista (`h2` «Tu viaje»): saludo con el nombre de pila del primer pasajero adulto (única PII, FR-003/FR-112; sin adulto se omite el saludo), código de reserva, número de pasajeros y lista de segmentos | `default` · `sin_segmentos` («No hay tramos para mostrar.» cuando `segments` está vacío) |
| `SegmentRow` | propio (`components/SegmentRow`) | v1.3 | Una fila por segmento dentro de `TripSummary`: vuelo, ruta, fecha, «Salida programada», «Llegada programada», estado en un `Chip`, nueva salida, puerta y, si aplica, «Nueva llegada» rotulada **«Estimación»** | `ON_TIME` · `SCHEDULED` · `DELAYED` · **`NO_EVENTS`** (sin eventos o solo con eventos que no informan la salida, p. ej. `GATE_CHANGE`: texto plano «Horario programado», **sin `Chip` ni ícono de estado**) · `NO_VERIFIED_INFO` (**solo** evidencia degradada: «Sin información verificada») · `CONFLICT` · `UNSUPPORTED` · `INCONSISTENT` · `UNKNOWN` (estado `null` por falla de eventos) |
| `AlertBanner` | propio (`components/AlertBanner`) | v1.3 | Bajo el resumen, un banner por `alerts[]` (retraso, conexión en riesgo, conflicto, evento no soportado, pernocte) y, pegado al botón de acción, el aviso de menor | `info` (índigo) · `warning` (ámbar) · `critical` (rojo) · **`gate`** (cambio de puerta: tono `info` con ícono `puerta`, destacado); siempre con `Icon` y título, nunca solo color |
| `RulesPanel` | propio (`components/RulesPanel`) | v1.3 | Panel **plegado por defecto** (`h2` «Reglas de la política») con resumen «Se cumplen X de Y reglas»; desplegado, una frase legible por regla (del catálogo) y el código con sus valores como detalle (FR-008, FR-034). No se muestra si `policy` es `null` (p. ej. conflicto de fuentes) | regla `CUMPLE` · `NO_CUMPLE` · `INDETERMINADA` (rotulada «No evaluable»); política `RULE_ERROR` / `EMPTY` / `UNAVAILABLE` |
| `OptionCard` | propio (`components/OptionCard`) | v1.3 | Una tarjeta por opción viable (`options[]`): vuelo, ruta, fecha y hora, costo, asientos, respaldo de política, aviso de pernocte | `proposed` (etiqueta «Propuesta») · `alternative` |
| `RefundNotice` | propio (`components/RefundNotice`) | v1.3 | Bloque propio con rótulo «Si prefieres no viajar» (`h2`) y la redacción no afirmativa de FR-046 | `default` |
| `ActionBar` | propio (`components/ActionBar`) | v1.3 | Zona de acciones, **solo si la vista trae `actions`** (`h2` «Qué puedes hacer»): aviso de menor (si aplica), frase de efecto, botón primario, **cuenta regresiva «Quedan mm:ss (hasta HH:MM UTC)»** junto al botón, y «Hablar con una persona» con su propia frase de efecto | primario `CREATE_REBOOKING` · `CREATE_HUMAN_CASE_WITH_OPTION` · `CREATE_HUMAN_CASE` con motivo conocido (un clic) · secundario neutro · `disabled` por operación en curso. **No se renderiza** cuando no hay acción posible (sin anomalía, informativa, solo evidencia degradada, lectura fallida) |
| `HumanCaseDialog` | propio (`components/HumanCaseDialog`) | v1.3 | Diálogo modal de «Hablar con una persona» cuando el motivo no es conocido: `fieldset`/`legend` con los motivos de `offered_reasons` y rótulos neutros («Necesito ayuda con mi vuelo», «Necesito ayuda con mis datos o documentos» y, **solo si hay compensación elegible**, «Tengo una consulta sobre compensaciones»), mismo peso visual, **ninguno preseleccionado** y **sin campo de texto** (FR-060) | `closed` · `open` · `submitting` · `error` · `indeterminate` · `needs_confirmation` |
| `StatusNotice` | propio (`components/StatusNotice`) | v1.3 | Resultado de una acción o estado de la pantalla: solicitud registrada, solicitud existente, caso creado, cambio de estado, carga lenta, error de carga, aviso de eventos no disponibles | `info` · `success` (solo hechos ya ocurridos, p. ej. caso registrado) · `warning` · `error`; `role="status"` o `role="alert"` |
| `ScenarioSelector` | propio (`components/ScenarioSelector`) | v1.3 | **Solo desarrollo** (`import.meta.env.DEV`): lista desplegable de los escenarios con `ui = true` y botón «Avanzar reloj» dentro del `Header`; fija la sesión simulada | `default` · no se incluye en el build de producción |

**Estados del `ScenarioSelector` (solo desarrollo; mismos `StatusNotice` y tokens que el resto de la interfaz, textos del catálogo):**

| Estado | Presentación | Texto exacto |
|---|---|---|
| Cargando el catálogo | lista deshabilitada | «Cargando escenarios…» |
| Catálogo vacío | lista deshabilitada y `StatusNotice` `info` | «No hay escenarios disponibles.» |
| El catálogo no cargó | `StatusNotice` `warning`, no bloquea la vista | «No pudimos cargar los escenarios.» |
| Activando un escenario | lista y botón deshabilitados (`aria-disabled`) | «Activando escenario…» |
| Escenario no encontrado | `StatusNotice` `warning`; se conserva el escenario anterior | «El escenario ya no existe. Elige otro.» |
| Reloj no disponible | botón «Avanzar reloj» con `aria-disabled` y la explicación en un párrafo fuera del botón | «Avanzar reloj no está disponible en este modo.» |
| Error de autenticación (sesión simulada no habilitada) | `StatusNotice` `error`, `role="alert"`, con «Reintentar» | «No se pudo iniciar la sesión de prueba.» |

Componentes auxiliares permitidos (no cuentan como contrato visual independiente): `Button`, `Chip` (rótulo de estado), `Icon` (SVG propio), `Skeleton` (carga), `Countdown`, `RefreshButton` (botón secundario «Actualizar» con «Información de las HH:MM UTC»; relee la vista, no es una acción externa). Se definen con los mismos tokens.

### Dónde se usa cada componente por estado de pantalla

| Estado de pantalla (ver Evidencia Visual) | Componentes presentes |
|---|---|
| 1. Vista sin anomalía | `Header`, `TripSummary` + `SegmentRow`, `StatusNotice` (sin botones de acción), `RefreshButton` |
| 2. Retraso con opción propuesta y caso humano | `Header`, `TripSummary` + `SegmentRow` (`DELAYED`), `AlertBanner` ×3 (retraso, conexión y **cambio de puerta** `gate`), `RulesPanel` (plegado), `OptionCard` (`proposed`), `RefundNotice`, `ActionBar` (aviso de menor, frase de efecto, primario por efecto con cuenta regresiva, secundario), `HumanCaseDialog` |
| 3. Conflicto de fuentes | `Header`, `TripSummary` + `SegmentRow` (`CONFLICT`), `AlertBanner` (`critical`), `ActionBar` (primario `CREATE_HUMAN_CASE` de un clic). Sin `RulesPanel` (la política no se consulta) |
| 4. Sin opción viable | `Header`, `TripSummary`, `AlertBanner`, `RulesPanel` (plegado), `StatusNotice` (`warning`), `ActionBar` (primario `CREATE_HUMAN_CASE` de un clic) |
| 5. Solicitud registrada | `Header`, `TripSummary`, `StatusNotice` (`info`), `ActionBar` (solo secundario) |
| 6. Error de carga | `Header`, `StatusNotice` (`error`) con «Reintentar» (sin soporte) |
| 7. Carga | `Header`, `Skeleton`, `StatusNotice` (`info`, solo pasados 1,5 s) |
| 8. Segmentos vacíos (lectura inválida) | `Header`, `TripSummary` (`sin_segmentos`), `StatusNotice` (`warning`) con «Reintentar» (sin soporte) |
| 9. Informativa (retraso sin política rota) | `Header`, `TripSummary` + `SegmentRow` (`DELAYED`), `AlertBanner` (`info`), `RulesPanel` (plegado), `RefreshButton`. Sin `OptionCard`, `RefundNotice` ni `ActionBar` |
| 10. Solo cambio de puerta (informativa con puerta destacada) | `Header`, `TripSummary` + `SegmentRow` (`NO_EVENTS`), `AlertBanner` (`gate`), `RefreshButton`. Sin reglas (no se consulta política), opciones ni `ActionBar` |

---

## Tokens Visuales (Paleta)

> Usar SIEMPRE los tokens del design system, nunca colores hardcodeados.
> **APROXIMACIONES**: los valores siguientes imitan la identidad (índigo profundo, rojo de acento, superficies claras) y **no fueron extraídos de la web del centro de ayuda**.

```css
/* frontend/src/styles/tokens.css */
:root {
  /* Colores de marca (aproximaciones) */
  --color-brand:            #1B0088;   /* índigo profundo: encabezado, TODOS los botones primarios, enlaces, foco */
  --color-accent:           #E8112D;   /* rojo de acento: SOLO decorativo (franja del Header); nunca texto, botón ni estado */
  --color-surface:          #F4F4F8;   /* fondo de página */
  --color-surface-raised:   #FFFFFF;   /* tarjetas */
  --color-ink:              #1B1B2F;   /* texto principal (también el de los chips y banners) */
  --color-ink-muted:        #5A5B73;   /* texto secundario */
  --color-border:           #DADCE6;   /* separadores decorativos */
  --color-border-strong:    #7A7C95;   /* contorno de controles interactivos (≥ 3:1) */
  --color-on-brand:         #FFFFFF;   /* texto sobre índigo */
  --color-disabled-bg:      #E6E7EE;   /* fondo de botón deshabilitado (texto: --color-ink-muted) */

  /* Semánticos: solo para íconos y bordes de 4 px; el TEXTO sobre fondos tenues es siempre --color-ink */
  --color-positive:         #0A7F3F;
  --color-warning:          #B45F06;
  --color-negative:         #C8102E;

  /* Fondos tenues para banners y chips */
  --color-info-tint:        #EDEAF9;
  --color-positive-tint:    #E8F5EC;
  --color-warning-tint:     #FFF4E5;
  --color-negative-tint:    #FDECEF;

  /* Tipografía */
  --font-family:  system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono:    ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;   /* códigos de reglas */
  --font-size-sm: 0.875rem;   /* 14 px */
  --font-size-md: 1rem;       /* 16 px */
  --font-size-lg: 1.25rem;    /* 20 px */
  --font-size-xl: 1.5rem;     /* 24 px */
  --line-height:  1.5;
  --font-weight-regular: 400;
  --font-weight-strong:  600;

  /* Forma y espacio */
  --radius:       8px;
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px;  --space-4: 16px;  --space-5: 24px;  --space-6: 32px;
  --gutter:       16px;       /* margen lateral mínimo en móvil */
  --content-max:  720px;      /* ancho máximo del contenido */
  --focus-ring:          3px solid var(--color-brand);       /* sobre superficies claras */
  --focus-ring-on-brand: 3px solid var(--color-on-brand);    /* sobre el Header índigo */
  --focus-offset: 2px;
}
```

| Token | Uso | Valor actual (aproximación) |
|-------|-----|-------------|
| `--color-brand` | Color primario: `Header`, **todos** los botones primarios, anillo de foco, enlaces, ícono y rótulo de «Cumple» | `#1B0088` |
| `--color-accent` | Solo decorativo (franja de 4 px del `Header`). No se usa en botones, texto ni estados | `#E8112D` |
| `--color-surface` / `--color-surface-raised` | Fondo de página / tarjetas | `#F4F4F8` / `#FFFFFF` |
| `--color-ink` / `--color-ink-muted` | Texto principal (incluye chips y banners) / secundario | `#1B1B2F` / `#5A5B73` |
| `--color-border` / `--color-border-strong` | Separadores / contorno de controles | `#DADCE6` / `#7A7C95` |
| `--color-disabled-bg` | Fondo de botón deshabilitado | `#E6E7EE` |
| `--color-positive` | Ícono de hechos con evidencia (segmento `ON_TIME`, caso registrado). **Nunca** para una estimación ni para la conexión | `#0A7F3F` |
| `--color-warning` | Ícono y borde de retraso, estimación, vigencia próxima, «No evaluable» | `#B45F06` |
| `--color-negative` | Ícono y borde de fallo, conflicto o error | `#C8102E` |
| `--font-family` y escala | Tipografía del sistema, 14/16/20/24 px, interlineado 1,5 | `system-ui` … |
| `--radius` | Radio de tarjetas, botones y entradas | `8px` |

### Color por estado (definición cerrada)

| Elemento | Fondo | Texto | Ícono / borde de 4 px |
|---|---|---|---|
| Chip `ON_TIME` («A tiempo») | `--color-positive-tint` | `--color-ink` | check en `--color-positive` |
| Chip `SCHEDULED` («Programado») | `--color-surface` con contorno `--color-border-strong` | `--color-ink` | reloj en `--color-ink-muted` |
| Chip `DELAYED` («Retrasado N min») | `--color-warning-tint` | `--color-ink` | alerta en `--color-warning` |
| Chip `NO_VERIFIED_INFO` («Sin información verificada», **solo** con evidencia degradada) | `--color-surface` con contorno `--color-border-strong` | `--color-ink` | pregunta en `--color-ink-muted` |
| Segmento `NO_EVENTS` («Horario programado») | sin fondo (texto plano, sin `Chip`) | `--color-ink` | **ninguno** (no es un estado: no afirma nada) |
| Alerta `gate` (cambio de puerta, **destacada**) | `--color-info-tint` | `--color-ink`; título en negrita (`--font-weight-strong`) | ícono `puerta` en `--color-brand`; **borde izquierdo de 4 px** en `--color-brand` |
| Chip `CONFLICT` / `UNSUPPORTED` / `INCONSISTENT` («En revisión») | `--color-negative-tint` | `--color-ink` | error en `--color-negative` |
| Regla **«Cumple»** | `--color-info-tint` | `--color-ink` | check en `--color-brand` (índigo, **no** verde: una regla puede apoyarse en una estimación) |
| Regla **«No cumple»** | `--color-surface` con contorno `--color-border-strong` | `--color-ink` | cruz en `--color-ink-muted` |
| Regla **«No evaluable»** | `--color-warning-tint` | `--color-ink` | pregunta en `--color-warning` |
| Estimación (nueva llegada, conexión en riesgo) | `--color-warning-tint` | `--color-ink` | alerta en `--color-warning` |
| Banner `info` (aviso de menor, solicitud registrada) | `--color-info-tint` | `--color-ink` | info en `--color-brand` |
| Botón primario | `--color-brand` | `--color-on-brand` | — |
| Botón secundario | `--color-surface-raised` con contorno `--color-brand` | `--color-brand` | — |
| Botón deshabilitado | `--color-disabled-bg` | `--color-ink-muted` (texto visible: «Procesando tu solicitud…») | — |

### Checklist de tokens (FR-111; lo verifica un test que lee los `.css`)

- [ ] Ningún color hexadecimal, `rgb()` ni `hsl()` fuera de `tokens.css`.
- [ ] Ninguna `font-family` fuera de `--font-family` y `--font-mono`.
- [ ] Ningún `border-radius` distinto de `var(--radius)` (salvo `50%` en puntos de estado).
- [ ] Todo espaciado sale de `--space-*`.
- [ ] `--color-accent` solo aparece en la franja decorativa del `Header` (ni en botones, ni en texto, ni en estados).
- [ ] **La estimación y la conexión nunca usan `--color-positive`** (ni como texto, ni como ícono, ni como fondo): el test falla si `Estimación`, `CONNECTION_AT_RISK` o `missed_connection` reciben una clase que lo use.
- [ ] El texto sobre cualquier fondo tenue es `--color-ink` (nunca `--color-warning`, `--color-positive` ni `--color-negative`).
- [ ] Los colores semánticos nunca son el único portador de significado (siempre texto + ícono SVG con `aria-hidden`).
- [ ] Todo contenedor de códigos y condiciones declara `overflow-wrap: anywhere`.

### Contraste verificado (WCAG 2.1, relación calculada; el test de contraste recalcula cada par)

| Par (texto / fondo) | Relación | Criterio |
|---|---|---|
| `--color-ink` / `--color-surface-raised` | 16,88 : 1 | AA ✔ |
| `--color-ink` / `--color-surface` | 15,38 : 1 | AA ✔ |
| `--color-ink` / `--color-info-tint` | 14,25 : 1 | AA ✔ |
| `--color-ink` / `--color-positive-tint` | 15,03 : 1 | AA ✔ |
| `--color-ink` / `--color-warning-tint` | 15,53 : 1 | AA ✔ |
| `--color-ink` / `--color-negative-tint` | 14,80 : 1 | AA ✔ |
| `--color-ink-muted` / `--color-surface-raised` | 6,61 : 1 | AA ✔ |
| `--color-ink-muted` / `--color-surface` | 6,02 : 1 | AA ✔ |
| `--color-ink-muted` / `--color-info-tint` | 5,58 : 1 | AA ✔ |
| `--color-ink-muted` / `--color-warning-tint` | 6,08 : 1 | AA ✔ |
| `--color-ink-muted` / `--color-disabled-bg` | 5,36 : 1 | AA ✔ |
| `--color-on-brand` / `--color-brand` | 14,98 : 1 | AAA ✔ (botón primario, texto del `Header`) |
| `--color-brand` / `--color-surface-raised` | 14,98 : 1 | AAA ✔ (enlaces, botón secundario) |
| `--color-brand` / `--color-surface` | 13,65 : 1 | AAA ✔ |
| `--color-brand` / `--color-info-tint` | 12,65 : 1 | AAA ✔ (rótulo «Cumple») |
| `--color-on-brand` (anillo de foco) / `--color-brand` | 14,98 : 1 | ≥ 3 : 1 ✔ (foco sobre el `Header`) |
| `--color-positive` / `--color-surface-raised` | 5,10 : 1 | ícono, ≥ 3 : 1 ✔ |
| `--color-positive` / `--color-positive-tint` | 4,54 : 1 | ícono, ≥ 3 : 1 ✔ |
| `--color-warning` / `--color-surface-raised` | 4,58 : 1 | ícono, ≥ 3 : 1 ✔ |
| `--color-warning` / `--color-warning-tint` | 4,22 : 1 | **NO pasa AA como texto (< 4,5)**: por eso el texto sobre fondos tenues es siempre `--color-ink`; como ícono o borde (≥ 3 : 1) ✔ |
| `--color-negative` / `--color-surface-raised` | 5,88 : 1 | ícono, ≥ 3 : 1 ✔ |
| `--color-negative` / `--color-negative-tint` | 5,16 : 1 | ícono, ≥ 3 : 1 ✔ |
| `--color-border-strong` / `--color-surface-raised` | 4,08 : 1 | ≥ 3 : 1 en controles ✔ |
| `--color-border-strong` / `--color-surface` | 3,72 : 1 | ≥ 3 : 1 en controles ✔ |
| `--color-border-strong` / cada `--color-*-tint` | 3,45 – 3,76 : 1 | ≥ 3 : 1 en controles ✔ |
| `--color-border` / `--color-surface-raised` | 1,37 : 1 | **solo decorativo**: nunca delimita un control |

El rojo `--color-accent` queda fuera de la tabla porque **no porta texto**.

---

## Contratos Sagrados de Diseño

> Estos patrones visuales NO DEBEN CAMBIAR sin coordinación.
> Cada ítem es un contrato con el usuario — cambiarlo rompe la expectativa visual establecida.

| # | Patrón visual | Componente/CSS | Motivo de permanencia |
|---|--------------|---------------|----------------------|
| 1 | **Jerarquía de la vista** (de arriba abajo): encabezado → resumen del viaje → alertas → reglas (plegadas) → opción propuesta → vía alternativa → acciones. Solo una acción primaria por pantalla. `h1` único en el `Header`; `h2` por sección. | `Header`, `TripSummary`, `AlertBanner`, `RulesPanel`, `OptionCard`, `RefundNotice`, `ActionBar` | El pasajero lee primero qué pasó y al final qué puede hacer; dos acciones primarias inducen a error. |
| 2 | **Paleta de tokens** como aproximación de la identidad, sin logos ni marcas; **todos los botones primarios en `--color-brand`**; el rojo es solo decorativo. | `tokens.css` | Identidad coherente (FR-111) y un solo color de acción. |
| 3 | **Tipografía del sistema** (`system-ui`), escala 14/16/20/24 px, interlineado 1,5; códigos de reglas en monoespaciada con `overflow-wrap: anywhere`. | `--font-family`, `--font-mono` | Legibilidad y cero dependencias de fuentes propietarias. |
| 4 | **Contraste AA** (relación ≥ 4,5 : 1 en todo texto, verificada sobre los tokens por un test que calcula el contraste de cada par de la tabla, NFR-011) y ≥ 3 : 1 en contornos de controles; el color nunca es el único portador de significado. | tabla de contraste | NFR-011. |
| 5 | **Foco visible:** anillo de 3 px `--color-brand` con separación de 2 px en todo elemento interactivo; **blanco (`--focus-ring-on-brand`) dentro del `Header` índigo**; navegación completa por teclado; enlace «Saltar al contenido» como primer foco. | `--focus-ring`, `--focus-ring-on-brand`, `--focus-offset` | NFR-011. |
| 6 | **Hora límite y cuenta regresiva (FR-071):** dentro del `ActionBar`, junto al botón primario: «Quedan mm:ss (hasta HH:MM UTC)» (hora truncada al minuto hacia abajo) y «Pasada esa hora, la opción queda sujeta a disponibilidad.» La cuenta se calcula contra `generated_at` y no se anuncia segundo a segundo a lectores de pantalla (solo al llegar a cero). **Al llegar a 0 el texto del contador se reemplaza por completo** (no queda «Quedan 00:00») por «La hora límite pasó: la opción está sujeta a disponibilidad.» y **el botón sigue activo**; al aceptar, el servidor refresca y revalida (FR-072). | `ActionBar`, `Countdown` | El plazo real de las opciones es corto (TTL 120 s); omitirlo o desactivar el botón induce a error. |
| 7 | **Texto de solicitud registrada (FR-056):** «Solicitud registrada, pendiente de confirmación, sujeta a disponibilidad.» con la hora de vencimiento (`expires_at`) y la frase «Tu vuelo todavía no se cambia.» Nunca «cambio confirmado» ni «reserva modificada». Tono `info`, **no** verde. | `StatusNotice` | FR-056, FR-083: la confirmación está fuera de v1. |
| 8 | **Aviso de estimación (FR-021, FR-022, FR-023):** toda conexión perdida, nueva llegada o retraso derivado lleva el rótulo «Estimación» y, si el MCT no fue provisto, «sujeta al tiempo mínimo de conexión, que no tenemos». **Nunca verde ni «segura» para una conexión estimada:** un `missed_connection` falso se muestra neutro («No detectamos que pierdas la conexión. Es una estimación, sujeta al tiempo mínimo de conexión; no es una garantía») y jamás con la frase «tu conexión está segura». «Llegada programada» (dato) y «Nueva llegada» (estimación) son rótulos distintos. | `AlertBanner`, `SegmentRow` | H-13, FR-023. |
| 9 | **Frase de efecto ANTES del botón, asociada con `aria-describedby` (FR-050):** `CREATE_REBOOKING` ⇒ botón «Aceptar esta opción» + «Se creará una solicitud de cambio, pendiente de confirmación. Tu vuelo todavía no se cambia. Si no podemos confirmar el resultado, derivaremos tu caso a una persona.» · `CREATE_HUMAN_CASE_WITH_OPTION` ⇒ «Aceptar y enviar a una persona» + «Una persona revisará esta opción. Esto no cambia tu reserva.» · `CREATE_HUMAN_CASE` con motivo conocido ⇒ «Hablar con una persona» + «Una persona revisará tu caso. Esto no cambia tu reserva.» · «Hablar con una persona» secundario ⇒ «Se abrirá una solicitud para que una persona te ayude. Esto no cambia tu reserva.» | `ActionBar` | El clic autoriza exactamente una acción y el texto lo declara antes de pulsar. |
| 10 | **«Hablar con una persona» solo con una acción posible** (FR-004, FR-060): política rota (decisión AUTOMATICA o PENDIENTE_APROBACION) o anomalía que exige validación manual (BLOQUEADA). **No se ofrece** con sin anomalía, con retraso informativo, con solo evidencia degradada ni con lectura fallida o inválida. Con motivo conocido por el sistema (conflicto, sin opción) crea el caso con **un solo clic** (se envía `OTHER_HELP` con el `decision_id`; el servidor fija el motivo principal). Sin motivo conocido abre el diálogo: motivos cerrados con rótulos neutros, sin resaltar ni preseleccionar y **sin campo de texto**; el motivo «Tengo una consulta sobre compensaciones» **solo aparece si hay compensación elegible** (`offered_reasons`, FR-067). Su color es el de cualquier botón (índigo), nunca rojo. Tras un resultado indeterminado, advierte del posible duplicado y exige un segundo clic explícito (FR-105). La compensación nunca se ofrece de forma proactiva ni con montos. | `ActionBar`, `HumanCaseDialog` | FR-060, FR-067, FR-091, FR-105. |
| 11 | **Estados sin evidencia (FR-014, dos ramas):** un segmento con **solo evidencia degradada** muestra «Sin información verificada» (`NO_VERIFIED_INFO`), **nunca** «A tiempo», y sin botón de acción. Un segmento **sin ningún evento, o solo con eventos que no informan la salida** (p. ej. `GATE_CHANGE`) muestra su **«Horario programado»** del contexto (`NO_EVENTS`), como texto plano **sin ícono de estado**, sin afirmar estado ni alertar. Un conflicto de fuentes (empate de marcas de tiempo entre eventos sanos, FR-013) no afirma ningún estado y no muestra reglas. Un `STATUS` sano más reciente que un retraso lo reemplaza: el segmento se muestra «Programado» o «A tiempo» y no queda alerta (FR-012). | `SegmentRow`, `RulesPanel` | Mostrar «a tiempo» o «sin información» donde solo no hay eventos sería afirmar de más. |
| 12 | **Lista blanca de campos visibles (FR-112, §3.11):** nombre de pila del primer pasajero adulto, código de reserva, número de pasajeros, aviso «tu grupo incluye a un menor» (sin edad), segmentos, opciones, derechos con su `policy_ref`, reglas con sus variables, plazos, avisos, y la referencia de la solicitud (`request_id`) o del caso (`case_id`) recién creados. Nunca correo, teléfono, documento, edad, apellido ni nivel de fidelidad. Las cantidades en moneda se muestran con separador de miles y código (p. ej. «180.000 CLP»), sin decimales. **Texto plano (NFR-013):** todo texto del proveedor (`condition`, `entitlement`, puerta, mensajes) se inserta como texto, nunca como HTML (sin `dangerouslySetInnerHTML`); un marcado HTML se ve literal (TC-58). | todos | FR-003, FR-112, NFR-002. |
| 13 | **Reglas:** plegadas por defecto con el resumen «Se cumplen X de Y reglas»; cada regla con una frase legible del catálogo (el código y los valores como detalle, `overflow-wrap: anywhere`) y un rótulo «Cumple» / «No cumple» / «No evaluable» con ícono y texto. Un derecho de código desconocido se muestra **por su código, sin interpretarlo**; una condición sin frase en el catálogo se muestra en crudo. | `RulesPanel` | FR-033, FR-037. |
| 14 | **Prohibiciones de contenido (FR-083, FR-084):** ninguna pantalla afirma «tu conexión está segura» o «llegarás a tiempo», hora de llegada al destino final, retención del vuelo siguiente, hotel o comidas, montos, causa del retraso ni «ya está cambiado». El pernocte dice «podrías tener derecho a asistencia; un agente lo confirmará». | mensajes y plantillas | FR-058, FR-083. |
| 15 | **Vía de reembolso (FR-046):** bloque propio (`h2`) con rótulo «Si prefieres no viajar» y la redacción no afirmativa «Si prefieres no viajar, una persona puede revisar contigo las alternativas.» Sin monto, plazo ni afirmación de derecho. | `RefundNotice` | FR-046 la exime de `policy_ref` por no afirmar un derecho. |
| 16 | **Aviso de menor:** `AlertBanner` `info` pegado al botón de acción, con el texto «Tu grupo incluye a un menor: esta decisión necesita la aprobación de una persona.» (booleano de grupo, sin edad ni nombre). | `AlertBanner`, `ActionBar` | Explica por qué el botón deriva a una persona. |
| 17 | **Responsivo:** una columna con margen lateral de 16 px y ancho máximo de 720 px; sin scroll horizontal desde 320 px; los botones ocupan el ancho completo en móvil y tienen un área táctil mínima de 44 × 44 px. | `--gutter`, `--content-max` | Uso desde un teléfono. |
| 18 | **Carga y operación en curso:** esqueleto durante la carga; pasados **1,5 s** aparece el aviso «Esto está tardando más de lo habitual. Seguimos consultando tu viaje.» (`role="status"`), porque la vista encadena 4 lecturas en secuencia (peor caso 16 s). Con una operación en curso el botón primario usa `aria-disabled="true"` con el texto visible «Procesando tu solicitud…» (no se oculta ni se vacía); si un botón se deshabilita por otra causa (p. ej. solicitud ya existente), la explicación va **en un párrafo fuera del botón**, no dentro. Durante la carga el `main` lleva `aria-busy="true"`. | `Skeleton`, `ActionBar`, `StatusNotice` | FR-062, NFR-004, NFR-011. |
| 19 | **Accesibilidad estructural:** `lang="es"`, landmarks (`header`, `main`), `h1` único y `h2` por sección, enlace «Saltar al contenido». **Diálogo:** `role="dialog"` con `aria-modal`, `fieldset`/`legend` para los motivos, **foco inicial en el título**, el foco queda atrapado y vuelve al botón que lo abrió al cerrar, pista visible «Elige un motivo» mientras «Enviar solicitud» esté deshabilitado (`aria-disabled`), cierre con `Esc`. Al cerrar el diálogo con un resultado, **el foco pasa al `StatusNotice`** (`tabindex="-1"`). **Destino del foco tras recargar:** después de «Reintentar» o «Actualizar» el foco pasa al `h2` «Tu viaje» (`tabindex="-1"`) y una región `aria-live="polite"` anuncia «Información actualizada a las HH:MM UTC»; tras un `STATE_CHANGED` el foco pasa a un `StatusNotice` `info` al inicio de la vista («La situación cambió: actualizamos tu viaje»); **tras un «Reintentar» que vuelve a fallar** el foco pasa al `StatusNotice` de error (`tabindex="-1"`, `role="alert"`), que lo anuncia, y «Reintentar» sigue disponible. | `HumanCaseDialog`, `StatusNotice` | NFR-011. |
| 20 | **Estado informativo (FR-039):** cuando hay un retraso validado sin política rota, la pantalla muestra el retraso, la estimación de la conexión (rotulada «Estimación») y las reglas evaluadas (plegadas, «Se cumplen X de Y reglas»), con el texto «Con la información actual, este retraso no da lugar a acciones disponibles para ti. Vuelve a consultar tu viaje más tarde.» No hay opciones, reembolso, compensación, botón de soporte ni notificación. El tono es `info` (nunca `warning` ni `success`) y no afirma «llegarás a tiempo» ni «tu conexión está segura» (FR-083). | `AlertBanner`, `RulesPanel` | Un retraso que no rompe ninguna política solo se informa. |
| 21 | **Cambio de puerta destacado (FR-006):** en modo usuario un cambio de puerta validado se muestra **siempre**. «Destacado» significa una alerta `gate` con **fondo `--color-info-tint`, borde izquierdo de 4 px en `--color-brand`, título en negrita («Cambio de puerta en tu vuelo LAxxx (ORG → DST)») e ícono `puerta` en `--color-brand`**, la nueva puerta, la **hora en que se informó la puerta** («Puerta informada a las HH:MM UTC», separada de «Información de las HH:MM UTC» del estado del vuelo) y la nota «Confirma en las pantallas del aeropuerto.»; la puerta también aparece en la fila del segmento. Se muestra aunque no haya retraso ni política rota (viaje solo con `GATE_CHANGE`: estado informativo, sin reglas, sin opciones, sin botón de soporte). Nunca se muestra una puerta de una fuente degradada ni de un escenario sin `GATE_CHANGE` validado. | `AlertBanner` (`gate`), `SegmentRow` | FR-006, FR-068, DAT-23. |
| 22 | **Botón «Actualizar» (lectura, no acción externa):** en las vistas sin acción primaria (sin anomalía, informativa, solo puerta) hay un botón secundario «Actualizar» con el texto «Información de las HH:MM UTC»; relee la vista (`POST …/evaluate` con `caller = "user"`), no requiere consentimiento y no cambia nada. | `RefreshButton` | FR-002, FR-050 (solo las acciones externas requieren clic autorizante). |
| 23 | **Orden de las alertas** (de arriba abajo, bajo el resumen del viaje): (1) las `critical` (conflicto, evento no soportado, retraso incoherente, varios segmentos afectados); (2) el retraso (`DELAY`); (3) el **cambio de puerta (`gate`), justo después del retraso** para que se lea junto a él; (4) la conexión en riesgo (`CONNECTION_AT_RISK`, «Estimación»); (5) el pernocte (`OVERNIGHT`). Sin retraso, el cambio de puerta va primero. | `AlertBanner` | La puerta es información accionable inmediata y debe quedar pegada a lo que ya cambió. |

---

## Evidencia Visual (Screenshots)

> **LIMITACIÓN DECLARADA:** en esta etapa **NO se pueden capturar screenshots**. El navegador remoto disponible no alcanza `localhost` y no se instalará Playwright sin permiso del usuario; además, el front todavía no existe (proyecto nuevo) y la web del centro de ayuda no pudo inspeccionarse desde este entorno. Por lo tanto la evidencia visual de este contrato son **wireframes ASCII por pantalla y estado**.
> **Obligación diferida:** cuando exista el front y el usuario autorice Playwright (o la captura manual), se capturarán las pantallas en `sdd/screenshots/design/` y se reemplazará esta evidencia; hasta entonces, el wireframe y los textos de este documento son la definición de «correcto» y un test de componentes (Vitest + Testing Library) verifica la presencia de cada texto obligatorio.

Convenciones de los wireframes: `[Botón]` = botón; `( )` / `(•)` = opción sin marcar / marcada; `▸` / `▾` = panel plegado / desplegado; `(i)` `(!)` `(x)` `(ok)` `(?)` = íconos SVG con `aria-hidden`; las horas locales no llevan zona (así llegan del PDF) y las marcas de tiempo del sistema se muestran en UTC. Datos del caso base del PDF con el nombre ficticio «Ana»; tamaño: móvil, una columna.

### Pantalla 1 — Vista sin anomalía (escenario `SIN_ANOMALIA`)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀| <- franja decorativa (acento)
| Ayuda para tu viaje  (h1)          Escenario: [Sin anom. v]|  <- Header (índigo; selector solo en dev)
+----------------------------------------------------------+
| Tu viaje (h2)                                            |
|  Hola, Ana                                               |  <- TripSummary
|  Reserva ABC123 · 2 pasajeros                            |
|  ------------------------------------------------------- |
|  LA500   SCL → LIM · 15 sep 2026                         |  <- SegmentRow
|  Salida programada 14:30 · Llegada programada 17:55      |
|  (clock) [Programado]  Información de las 10:48 UTC      |
|  LA2410  LIM → MEX · 15 sep 2026                         |
|  Salida programada 19:05 · Llegada programada 23:40      |
|  (clock) [Programado]  Información de las 10:48 UTC      |
|                                                          |
|  (i) No encontramos novedades verificadas en tu viaje.   |  <- StatusNotice info
|                                                          |
|  [ Actualizar ]  Información de las 11:02 UTC            |  <- botón secundario: relectura, no es una acción externa
+----------------------------------------------------------+
```

Sin alertas, reglas, opciones ni botones de acción (FR-004); solo el botón secundario «Actualizar» (lectura). Un segmento con **solo evidencia degradada** se rotula `(?) [Sin información verificada]`, nunca `[A tiempo]` (FR-014), sin botón de acción. Un segmento **sin eventos** (escenario `SIN_EVENTOS_TC54`) o solo con eventos que no informan la salida se rotula **«Horario programado»**, texto plano **sin ícono de estado** (`NO_EVENTS`). Con `SCHEDULED_POSTERIOR_TC24` el segmento muestra `(ok) [Programado]` o `(ok) [A tiempo]` sin alerta (FR-012).

### Pantalla 2 — Retraso con opción propuesta y caso humano (escenario `BASE_TC01`)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje                Escenario: [Caso base v]|
+----------------------------------------------------------+
| Tu viaje                                                 |
|  Hola, Ana · Reserva ABC123 · 2 pasajeros                |
|  LA500   SCL → LIM · 15 sep 2026                         |
|  Salida programada 14:30 · Llegada programada 17:55      |
|  (!) [Retrasado 160 min]  Nueva salida 17:10             |
|  Puerta 24 (informada a las 10:55 UTC)                   |
|  Nueva llegada (Estimación): 20:35                       |
|  Información de las 10:48 UTC                            |
|  LA2410  LIM → MEX · 15 sep 2026                         |
|  Salida programada 19:05 · Llegada programada 23:40      |
|  (clock) [Programado]  Información de las 10:48 UTC      |
|                                                          |
|  (!) Retraso en tu vuelo LA500 (SCL → LIM)               |  <- AlertBanner warning (texto en tinta)
|      Tiene un retraso de 160 minutos. Nueva salida:      |
|      17:10. Información de las 10:48 UTC.                |
|                                                          |
|  (puerta) Cambio de puerta en tu vuelo LA500 (SCL → LIM) |  <- AlertBanner gate JUSTO tras el retraso: fondo info,
|      Ahora sale por la puerta 24. Puerta informada a las |     borde izq. 4 px índigo, título en negrita
|      10:55 UTC. Confirma en las pantallas del aeropuerto.|
|                                                          |
|  (!) Tu conexión podría perderse (Estimación)            |  <- AlertBanner warning
|      Estimamos que no alcanzarías tu vuelo LA2410        |
|      (LIM → MEX). Es una estimación del sistema, sujeta  |
|      al tiempo mínimo de conexión, que no tenemos. No es |
|      un hecho confirmado.                                |
|                                                          |
|  (!) Posible asistencia por pernocte                     |  <- AlertBanner warning (OVERNIGHT), última alerta
|      Tu nueva salida es al día siguiente: podrías tener  |
|      derecho a asistencia; un agente lo confirmará.      |
|                                                          |
|  Reglas de la política (h2)                              |  <- RulesPanel, PLEGADO por defecto
|  [ ▸ Ver reglas ]  Se cumplen 2 de 5 reglas              |
|                                                          |
|  Opción propuesta (h2)                                   |  <- OptionCard proposed
|  ┌────────────────────────────────────────────────────┐  |
|  │ [Propuesta]  LA2412 · LIM → MEX                     │  |
|  │ 16 sep 2026 · sale a las 08:15 (hora local de LIM)  │  |
|  │ Sin costo adicional · 4 asientos disponibles        │  |
|  │ Respaldo: POL-DELAY-2026-03                         │  |
|  │ Esta salida es al día siguiente: podrías tener      │  |
|  │ derecho a asistencia; un agente lo confirmará.      │  |
|  └────────────────────────────────────────────────────┘  |
|                                                          |
|  Si prefieres no viajar (h2)                             |  <- RefundNotice (bloque propio)
|  Si prefieres no viajar, una persona puede revisar       |
|  contigo las alternativas.                               |
|                                                          |
|  Qué puedes hacer (h2)                                   |  <- ActionBar
|  (i) Tu grupo incluye a un menor: esta decisión necesita |  <- AlertBanner info pegado al botón
|      la aprobación de una persona.                       |
|  Una persona revisará esta opción. Esto no cambia tu     |  <- frase de efecto (aria-describedby del botón)
|  reserva.                                                |
|  [ Aceptar y enviar a una persona ]   <- primario índigo |
|  Quedan 01:48 (hasta 11:04 UTC). Pasada esa hora, la     |  <- Countdown junto al botón
|  opción queda sujeta a disponibilidad.                   |
|  ------------------------------------------------------- |
|  Se abrirá una solicitud para que una persona te ayude.  |  <- frase de efecto del secundario
|  Esto no cambia tu reserva.                              |
|  [ Hablar con una persona ]           <- secundario      |
+----------------------------------------------------------+
```

Orden de las alertas de la pantalla 2 (contrato 23): retraso, cambio de puerta, conexión en riesgo y **pernocte**; la alerta `OVERNIGHT` es obligatoria cuando se deriva el pernocte (FR-029, FR-058) y repite sin cifras «podrías tener derecho a asistencia; un agente lo confirmará». Con esto queda cerrada la primera parte de DEBT-A1-08.

`RulesPanel` desplegado (tras «Ver reglas»; cada regla con rótulo, ícono y frase legible, el código como detalle):

```
|  Reglas de la política (h2)                              |
|  [ ▾ Ocultar reglas ]  Se cumplen 2 de 5 reglas          |
|  Política POL-DELAY-2026-03 · vigente desde 2026-03-01   |
|  (x) No cumple · R1                                      |
|      El retraso (160 min) no llega a los 180 min.        |
|      delay_minutes >= 180 · delay_minutes = 160          |
|  (x) No cumple · R2                                      |
|      Pide 240 min de retraso en un vuelo internacional;  |
|      el retraso es de 160 min.                           |
|      delay_minutes >= 240 AND international              |
|  (ok) Cumple · R3 (Estimación)                           |
|      Estimamos que se pierde la conexión.                |
|      missed_connection == true · missed_connection =     |
|      verdadero (estimada) · Derecho: REBOOK_NO_FEE       |
|  (x) No cumple · R4                                      |
|      No se solicitó compensación.                        |
|      compensation_requested == true · = falso            |
|  (ok) Cumple · R5                                        |
|      El grupo incluye a un menor.                        |
|      group_includes_minor == true · Derecho:             |
|      PRIORITY_HANDLING · requiere aprobación de una      |
|      persona                                             |
```

Variante del `ActionBar` cuando la decisión es AUTOMATICA (escenario `SIN_MENOR_TC07`; sin aviso de menor):

```
|  Qué puedes hacer (h2)                                   |
|  Se creará una solicitud de cambio, pendiente de         |
|  confirmación. Tu vuelo todavía no se cambia. Si no      |
|  podemos confirmar el resultado, derivaremos tu caso a   |
|  una persona.                                            |
|  [ Aceptar esta opción ]              <- primario índigo |
|  La hora límite pasó: la opción está sujeta a            |  <- el contador se REEMPLAZA por este texto;
|  disponibilidad.                                         |  el botón SIGUE activo
```

Diálogo del botón secundario (`HumanCaseDialog`, sin campo de texto, ningún motivo preseleccionado, foco inicial en el título). El motivo de compensación aparece **solo si la compensación es elegible** (caso base, R4 concede `CASH_COMPENSATION`); en `SIN_COMPENSACION_TC46` el diálogo muestra solo los dos primeros motivos:

```
+------------------------------------------------+
|  Hablar con una persona (título, foco inicial) [X]|
|  ---------------------------------------------- |
|  ┌ ¿Con qué necesitas ayuda? (legend) ─────────┐ |
|  │ ( ) Necesito ayuda con mi vuelo             │ |  OTHER_HELP
|  │ ( ) Necesito ayuda con mis datos o          │ |  PERSONAL_DATA_REQUEST
|  │     documentos                              │ |
|  │ ( ) Tengo una consulta sobre compensaciones │ |  COMPENSATION_REQUESTED
|  └─────────────────────────────────────────────┘ |
|  Una persona del equipo recibirá tu solicitud.   |
|  Elige un motivo.                                |  <- pista visible mientras está deshabilitado
|  [ Cancelar ]   [ Enviar solicitud ] (aria-disabled)|
+------------------------------------------------+
```

Resultado esperado tras enviar: se cierra el diálogo, el foco pasa al `StatusNotice success`: «Registramos tu solicitud. Una persona te atenderá; el tiempo objetivo de atención es de 45 minutos. Código de seguimiento: HC-4471.» (el 45 sale de `sla_minutes`, no del texto estático).

Variante tras un resultado indeterminado (FR-105: sin reenvío automático):

```
+------------------------------------------------+
|  Hablar con una persona                    [X] |
|  (!) No pudimos confirmar si tu solicitud      |  <- StatusNotice warning (role="alert")
|      quedó registrada; puede que ya lo esté.   |
|  Si la envías de nuevo, podría duplicarse.     |
|     [ Cerrar ]   [ Enviar de nuevo igualmente ]|  <- segundo clic explícito (confirm_possible_duplicate)
+------------------------------------------------+
```

Variante tras un error explícito del proveedor de casos (FR-105: el pasajero puede reintentar libremente, no hay riesgo de duplicado):

```
+------------------------------------------------+
|  Hablar con una persona                    [X] |
|  (x) No pudimos registrar tu solicitud,        |  <- StatusNotice error (role="alert")
|      puedes reintentar.                        |
|     [ Cerrar ]   [ Reintentar ]                |
+------------------------------------------------+
```

### Pantalla 3 — Conflicto de fuentes (escenario `CONFLICTO_TC03`)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje                Escenario: [Conflicto v]|
+----------------------------------------------------------+
|  Hola, Ana · Reserva ABC123 · 2 pasajeros                |
|  LA500   SCL → LIM · 15 sep 2026                         |
|  Salida programada 14:30 · Llegada programada 17:55      |
|  (x) [En revisión]                                       |  <- no afirma estado (FR-013)
|  LA2410  LIM → MEX · 15 sep 2026                         |
|  Salida programada 19:05 · Llegada programada 23:40      |
|  (clock) [Programado]                                    |
|                                                          |
|  (x) No podemos confirmar el estado de tu vuelo LA500    |  <- AlertBanner critical
|      Nuestras fuentes de información no coinciden. Una   |
|      persona debe revisar tu vuelo.                      |
|                                                          |
|  Una persona revisará tu caso. Esto no cambia tu reserva.|  <- frase de efecto
|  [ Hablar con una persona ]   <- primario índigo, UN clic|  <- ActionBar: crea el caso sin pedir motivo
+----------------------------------------------------------+
```

Sin reglas ni opciones: la decisión es BLOQUEADA y la política y las opciones no se consultan (`NOT_REQUESTED`). El conflicto es un empate de marcas de tiempo entre eventos sanos con afirmaciones incompatibles (escenario sintético). El clic envía `OTHER_HELP` con el `decision_id`; el servidor fija `SOURCE_CONFLICT` como motivo principal. **Puerta:** el escenario `CONFLICTO_TC03` no trae `GATE_CHANGE`, por eso no se dibuja ninguna puerta; si lo trajera (fuente sana y sin empate propio) se mostraría la alerta `gate` y la puerta en la fila del segmento, como en la pantalla 2 (el cambio de puerta no depende del conflicto sobre la salida).

### Pantalla 4 — Sin opción viable (escenario `SIN_OPCION_TC09`: dos pasajeros `ADULT`, R5 falsa)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje              Escenario: [Sin opción v] |
+----------------------------------------------------------+
|  (resumen del viaje y alertas como en la pantalla 2)     |
|  Reglas de la política (h2)                              |
|  [ ▸ Ver reglas ]  Se cumplen 1 de 5 reglas              |  <- solo R3 (R5 es falsa: no hay menor)
|                                                          |
|  (!) No encontramos una opción que cubra a todo tu grupo |  <- StatusNotice warning
|      Las opciones disponibles no tienen asientos para los|
|      2 pasajeros juntos, y no ofrecemos separar al grupo.|
|      Una persona puede ayudarte con otras alternativas.  |
|                                                          |
|  Una persona revisará tu caso. Esto no cambia tu reserva.|
|  [ Hablar con una persona ]   <- primario índigo, UN clic|
+----------------------------------------------------------+
```

Como R5 es falsa (no hay menor), la decisión es AUTOMATICA y no aparece el aviso de menor ni `POLICY_APPROVAL_REQUIRED`: el motivo principal del caso es `NO_OPTION_COVERS_GROUP` (FR-047, FR-063). No se muestran opciones no viables (FR-042); el mensaje explica la exclusión y remite a soporte (FR-043). **Puerta:** `SIN_OPCION_TC09` no trae `GATE_CHANGE`, por eso no se dibuja; si lo trajera se mostraría la alerta `gate` tras la del retraso (contrato 23).

### Pantalla 5 — Solicitud registrada (escenario `SIN_MENOR_TC07`, tras aceptar)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje                Escenario: [Sin menor v]|
+----------------------------------------------------------+
|  Hola, Ana · Reserva ABC123 · 2 pasajeros                |
|                                                          |
|  (i) Solicitud registrada                                |  <- StatusNotice info (NO verde); recibe el foco
|      Solicitud registrada, pendiente de confirmación,    |
|      sujeta a disponibilidad. Vence a las 11:12 UTC.     |
|      Tu vuelo todavía no se cambia.                      |
|      Código de seguimiento: RBK-88231                    |
|                                                          |
|  LA2412 · LIM → MEX · 16 sep 2026 · 08:15                |  <- resumen de la opción solicitada
|                                                          |
|  [ Aceptar esta opción ]  (aria-disabled)                |  <- el texto del botón no cambia
|  Ya existe una solicitud en curso para esta opción.      |  <- explicación FUERA del botón
|  Se abrirá una solicitud para que una persona te ayude.  |
|  Esto no cambia tu reserva.                              |
|  [ Hablar con una persona ]                              |
+----------------------------------------------------------+
```

Si la respuesta fue `EXISTING_REQUEST`, el aviso dice «Ya existe una solicitud en curso para esta opción.» (FR-055). **Puerta:** esta pantalla solo muestra el resultado de la acción y el resumen de la opción solicitada, no la lista de segmentos ni sus alertas; `SIN_MENOR_TC07` tampoco trae `GATE_CHANGE`. La alerta `gate` volvería a mostrarse en la vista completa si existiera.

**Textos de los siete resultados de aceptar una opción (`AcceptResult.outcome`; el pasajero nunca ve un código):**

| Resultado | Componente y rol | Texto exacto |
|---|---|---|
| `REBOOKING_CREATED` | `StatusNotice` `info`, `role="status"`, recibe el foco | «Solicitud registrada, pendiente de confirmación, sujeta a disponibilidad. Vence a las 11:12 UTC. Tu vuelo todavía no se cambia.» y «Código de seguimiento: RBK-88231» |
| `EXISTING_REQUEST` | `StatusNotice` `info`, `role="status"` | «Ya existe una solicitud en curso para esta opción.» |
| `HUMAN_CASE_CREATED` | `StatusNotice` `success`, `role="status"` (solo un hecho ocurrido) | «Registramos tu solicitud. Una persona te atenderá; el tiempo objetivo de atención es de 45 minutos. Código de seguimiento: HC-4471.» |
| `EXISTING_CASE` | `StatusNotice` `info`, `role="status"` | «Ya registramos una solicitud tuya para esta situación. Código de seguimiento: HC-4471.» |
| `NEEDS_CONFIRMATION` | diálogo con `StatusNotice` `warning`, `role="alert"` | «No pudimos confirmar si tu solicitud quedó registrada; puede que ya lo esté. Si la envías de nuevo, podría duplicarse.» con los botones «Cerrar» y «Enviar de nuevo igualmente» |
| `STATE_CHANGED` | `StatusNotice` `info` al inicio de la vista nueva, recibe el foco | «La situación cambió: actualizamos tu viaje» |
| `FAILED` | `StatusNotice` `error`, `role="alert"` | solicitud de cambio: «No pudimos procesar tu solicitud de cambio. Puedes hablar con una persona para que te ayude.»; caso humano: «No pudimos registrar tu solicitud, puedes reintentar.» |

Los textos de `EXISTING_CASE` y de `FAILED` de la solicitud de cambio se definen aquí en v1.5 porque el contrato no los fijaba; el resto proviene de FR-055, FR-056, FR-105 y del contrato 19.

### Pantalla 6 — Error de carga (escenario `ERROR_CONTEXTO`)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje              Escenario: [Error ctx v]  |
+----------------------------------------------------------+
|                                                          |
|  (x) No pudimos cargar tu viaje                          |  <- StatusNotice error (role="alert")
|      Ocurrió un problema al consultar tu reserva.        |
|      Inténtalo de nuevo en unos segundos.                |
|                                                          |
|  [ Reintentar ]                                          |  <- primario índigo (única acción)
+----------------------------------------------------------+
```

No hay botón de soporte: sin datos del viaje no hay una acción posible que ofrecer (FR-105, FR-066); el pasajero solo puede reintentar.

### Pantalla 7 — Carga (escenario cualquiera, mientras responde `POST …/evaluate`; el `main` lleva `aria-busy="true"`)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje                                      |
+----------------------------------------------------------+
|  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                               |  <- Skeleton: saludo
|  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                 |  <- Skeleton: segmentos
|  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                 |
|                                                          |
|  (i) Esto está tardando más de lo habitual. Seguimos     |  <- solo pasados 1,5 s (role="status")
|      consultando tu viaje.                               |
+----------------------------------------------------------+
```

### Pantalla 8 — Segmentos vacíos por lectura inválida (escenario `PARCIAL_BLOQUEANTE_TC12`, FR-066)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje                                      |
+----------------------------------------------------------+
|  Tu viaje (h2)                                           |
|  Reserva ABC123                                          |  <- sin saludo ni pasajeros si faltan datos
|  No hay tramos para mostrar.                             |  <- TripSummary sin_segmentos
|                                                          |
|  (!) No pudimos validar los datos de tu reserva.         |  <- StatusNotice warning
|      Inténtalo de nuevo en unos segundos.                |
|                                                          |
|  [ Reintentar ]                                          |  <- primario índigo (única acción)
+----------------------------------------------------------+
```

FR-066 define la lectura inválida como «aviso y reintento»: no hay una acción posible que ofrecer, por lo que no hay botón de soporte.

Variante `ERROR_EVENTOS`: se muestra el contexto con los segmentos sin estado y un `StatusNotice warning` «No pudimos consultar el estado de tus vuelos. Te mostramos los datos de tu reserva.» Sin botón de soporte.

### Pantalla 9 — Informativa: retraso sin política rota (escenario `INFORMATIVA_TC45`, FR-039)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje             Escenario: [Informativa v] |
+----------------------------------------------------------+
| Tu viaje (h2)                                            |
|  Hola, Ana · Reserva ABC123 · 2 pasajeros                |
|  LA500   SCL → LIM · 15 sep 2026                         |
|  Salida programada 14:30 · Llegada programada 17:55      |
|  (!) [Retrasado 5 min]  Nueva salida 14:35               |
|  Nueva llegada (Estimación): 18:00                       |
|  Información de las 10:48 UTC                            |
|  LA2410  LIM → MEX · 15 sep 2026                         |
|  Salida programada 19:05 · Llegada programada 23:40      |
|  (clock) [Programado]                                    |
|                                                          |
|  (i) Retraso en tu vuelo LA500 (SCL → LIM)               |  <- AlertBanner info (no warning)
|      Tiene un retraso de 5 minutos. Nueva salida: 14:35. |
|      Con la información actual, este retraso no da lugar |
|      a acciones disponibles para ti. Vuelve a consultar  |
|      tu viaje más tarde.                                 |
|                                                          |
|  (i) Estimación de tu conexión                           |  <- título con el rótulo «Estimación»
|      No detectamos que pierdas la conexión. Es una       |
|      estimación, sujeta al tiempo mínimo de conexión;    |
|      no es una garantía.                                 |
|                                                          |
|  Reglas de la política (h2)                              |  <- RulesPanel plegado
|  [ ▸ Ver reglas ]  Se cumplen 1 de 5 reglas              |  <- R5 (PRIORITY_HANDLING) no es remedio
|  Cumplir una regla no siempre da lugar a una acción.     |
|                                                          |
|  [ Actualizar ]  Información de las 11:02 UTC            |  <- botón secundario: relectura, no es una acción externa
+----------------------------------------------------------+
```

Sin opciones, reembolso, compensación ni botón de soporte: no hay una acción posible hasta que exista una política rota. `get_eligible_options` no se consulta (`NOT_REQUESTED`) y, con `caller = "system"`, el retraso tampoco se notifica (no hay política rota; un cambio de puerta sí se notificaría). El tono es `info` y el texto no afirma «llegarás a tiempo» ni «tu conexión está segura» (FR-083).

### Pantalla 10 — Solo cambio de puerta: informativa con puerta destacada (escenario `GATE_SOLO_TC51`, FR-006, FR-068, FR-014)

```
+----------------------------------------------------------+
|▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀|
| Ayuda para tu viaje             Escenario: [Solo puerta v] |
+----------------------------------------------------------+
| Tu viaje (h2)                                            |
|  Hola, Ana · Reserva ABC123 · 2 pasajeros                |
|  LA500   SCL → LIM · 15 sep 2026                         |
|  Salida programada 14:30 · Llegada programada 17:55      |
|  Estado del vuelo: Horario programado                    |  <- NO_EVENTS: texto plano, SIN ícono de estado
|  Puerta 24 (informada a las 10:55 UTC)                   |  <- la puerta va separada del estado del vuelo
|  LA2410  LIM → MEX · 15 sep 2026                         |
|  Salida programada 19:05 · Llegada programada 23:40      |
|  Estado del vuelo: Horario programado                    |  <- NO_EVENTS (S2 no tiene eventos)
|                                                          |
|  (puerta) Cambio de puerta en tu vuelo LA500 (SCL → LIM) |  <- AlertBanner gate (destacado)
|      Ahora sale por la puerta 24. Puerta informada a las |
|      10:55 UTC. Confirma en las pantallas del aeropuerto.|
|                                                          |
|  Con la información actual no hay acciones disponibles   |
|  para ti. Vuelve a consultar tu viaje más tarde.         |
|                                                          |
|  [ Actualizar ]  Información de las 11:02 UTC            |  <- botón secundario: relectura
+----------------------------------------------------------+
```

La decisión es INFORMATIVA y **no se consulta política** (no hay reglas ni resumen de reglas), ni opciones, ni soporte. En esta pantalla S1 solo tiene un evento que no informa la salida y S2 no tiene eventos: ambos se rotulan «Horario programado» (`NO_EVENTS`), **sin** «Sin información verificada» (que queda solo para evidencia degradada, FR-014). El cambio de puerta nunca se omite: se muestra aunque no haya retraso (FR-006).

### Tabla de evidencia visual

| Pantalla | Descripción | Evidencia | Fecha |
|---------|-------------|-----------|-------|
| 1. Vista sin anomalía | Solo contexto del viaje, sin botones | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 2. Retraso con opción propuesta y caso humano | Caso base: alertas, reglas plegadas, opción, reembolso, acciones con cuenta regresiva y diálogo | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 3. Conflicto de fuentes | Aviso neutro, sin reglas, caso humano de un clic | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 4. Sin opción viable | Mensaje de grupo no cubierto y caso humano de un clic | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 5. Solicitud registrada | `PENDING_CONFIRMATION` con vencimiento | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 6. Error de carga | «No pudimos cargar tu viaje» con reintento (sin soporte) | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 7. Carga | Esqueleto y mensaje de lentitud tras 1,5 s | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 8. Segmentos vacíos | Lectura inválida (FR-066): aviso y reintento, sin soporte | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 9. Informativa | Retraso sin política rota: se informa y se muestran las reglas, sin botones de acción (solo «Actualizar») | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |
| 10. Solo cambio de puerta | Informativa con puerta destacada, segmentos «Horario programado» (`NO_EVENTS`), sin política | Wireframe ASCII (arriba); screenshot diferido | 2026-10-19 |

**Referencia DESIGN_CONTRACT**: los wireframes y los textos obligatorios de este documento son la definición de «correcto» hasta que existan capturas reales. Si una implementación se ve o se lee distinto, es un bug, no una preferencia de estilo.

---

## Verificación Visual en TDD

Al agregar o modificar cualquier feature con UI, verificar contra este contrato:

1. `npm run test` (Vitest + Testing Library con jsdom): por cada estado de pantalla, comprobar que un segmento `NO_EVENTS` muestra «Horario programado» sin ícono de estado y que «Sin información verificada» solo aparece con evidencia degradada, que la alerta `gate` usa fondo `--color-info-tint`, borde izquierdo de 4 px `--color-brand` y título en negrita y aparece justo tras la del retraso, que el cambio de puerta aparece siempre destacado con su hora (también sin retraso), que `aria-busy` está activo durante la carga, que el texto de un botón deshabilitado no cambia, que el foco va al destino definido tras «Reintentar», «Actualizar» y `STATE_CHANGED`, que `ActionBar` no se renderiza sin `actions` (sin anomalía, informativa, evidencia degradada, lectura fallida), que el menú del diálogo omite la compensación cuando no es elegible, y los textos obligatorios (hora límite y cuenta regresiva, «sujeta a disponibilidad», «pendiente de confirmación», «Estimación», «Sin información verificada», frases de efecto con `aria-describedby`), los roles (`status`, `alert`, `dialog`), `fieldset`/`legend`, foco inicial, retorno del foco y la ausencia de campo de texto libre.
2. Test del catálogo (FR-113): recorre los componentes y falla si encuentra una cadena visible fuera del catálogo.
3. Test de tokens y de contraste: lee los `.css`, verifica el checklist de tokens (sin colores fuera de `tokens.css`, acento solo decorativo, estimación y conexión sin `--color-positive`) y calcula la relación de contraste de cada par texto/fondo de la tabla (≥ 4,5 : 1; NFR-011).
4. Test de PII: renderiza el escenario base y verifica que no aparezcan correo, teléfono, documento, edad, apellido ni nombre completo.
5. Si hay diferencia con este contrato: corregir el código, no el contrato.
6. **Diferido:** cuando el usuario autorice Playwright, capturar las 10 pantallas en `sdd/screenshots/design/` (`npx playwright screenshot --browser chromium http://localhost:5173 sdd/screenshots/design/<pantalla>.png`) y adjuntarlas aquí **sin quitar** los wireframes.

---

## Proceso para Cambiar el Design System

Si por razones de negocio se debe cambiar la librería de diseño o los tokens base (por ejemplo, al obtener los valores oficiales de la identidad):

1. **Proponer** el cambio con justificación de UX/negocio.
2. **Identificar** todas las pantallas afectadas (las 10 de este documento y el diálogo).
3. **Actualizar** wireframes o screenshots de referencia CON el nuevo diseño aprobado.
4. **Actualizar** las tablas de componentes, tokens, color por estado y contraste de este documento (recalcular la relación de contraste de cada par).
5. **Verificar** que TODOS los tests visuales, de tokens y de contraste pasan con el nuevo diseño.
6. Solo entonces el cambio es aceptado. Cambiar solo valores de `tokens.css` por otros aproximados a la identidad oficial **no** altera los componentes; cambiar un texto obligatorio sí requiere pasar por FR-046, FR-050, FR-056, FR-071 o FR-023.

---

## Referencia Design System

- **Design System**: propio, definido en este documento y en `frontend/src/styles/tokens.css` (aún no existe: se crea en la etapa de construcción). Inspirado, sin copiar activos, en el centro de ayuda `https://centro-ayuda.aerolinea.example/uy/es/centro-ayuda/preguntas/problemas-vuelo` (referencia visual indicada por el usuario; valores aproximados, sin logos ni marcas).
- **Component Library**: componentes propios en `frontend/src/components/` (inventario arriba); no hay Storybook en v1.
- **Tokens**: `frontend/src/styles/tokens.css` y la tabla de tokens de este documento.
