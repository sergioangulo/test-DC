# 06 · Decisiones

## Qué hay
| Archivo | Para qué |
|---|---|
| **`FORMULARIO_DECISIONES.html`** | **El formulario.** Archivo único: ábrelo con doble clic en tu navegador (funciona sin internet). |
| `DECISIONES_CATALOGO.md` | Exactamente el mismo contenido, para leerlo como documento. |
| `decisiones.json` | Datos del catálogo (los usa el formulario). |
| `herramientas/decisiones_data.py` | **Fuente única** de las decisiones. |
| `herramientas/generar.py` | Regenera los tres archivos y **valida** que cada referencia (REQ, GAP, DAT, SRC, POL, archivos) exista. |
| `herramientas/plantilla_formulario.html` | Plantilla del formulario. |

## Cómo funciona el formulario
1. **37 decisiones** agrupadas (A–F). Cada una trae: pregunta, contexto, trazabilidad (pasa el cursor sobre los códigos para ver su texto), opciones con **a favor / en contra**, **recomendación** razonada y **efecto en los requerimientos**.
2. Las **12 decisiones EXTERNAS** (borde morado) usan información que **no está en el PDF**. Listan **todas las referencias** (`POL-…`) con el archivo de `05_Politicas_Externas` donde está el detalle. Cada opción indica si **"usa información externa"**.
3. Para cada una puedes: elegir una opción (o varias, donde aplica), elegir **"Otra decisión"** (descríbela en las notas), **"Posponer"**, o escribir **notas y condiciones**. Hay un botón para **aceptar la recomendación**.
4. Se **guarda solo** en tu navegador. Puedes **descargar un borrador (.json)** y **cargarlo** después (incluso en otro equipo).
5. Botón final **"Generar y descargar documento (.md)"** → `DOCUMENTO_DE_TRABAJO_DECISIONES.md`.

## Qué contiene el documento final
1. **Resumen:** una fila por decisión (tu elección, si sigue o no la recomendación, si incorpora información externa).
2. **Decisiones de trabajo (detalle):** tu elección, tus notas, el **efecto en los requerimientos** y el **texto de cada requerimiento relacionado**; para las externas, los insumos y si **autorizaste** usarlos.
3. **Matriz requerimiento → decisiones:** para cada `REQ`, qué decisiones lo afectan y cómo quedaron.
4. **Insumos externos:** autorizados / solo contexto / sin decidir.
5. **Lista de cambios** a aplicar en `REQUERIMIENTOS.md`.
6. **Supuestos pendientes** (las decisiones sin resolver quedan marcadas y **ninguna recomendación se considera aprobada**).

## Orden sugerido
1. **`DEC-35`** (marco de políticas externas): enmarca todo el grupo E.
2. Las "críticas" del análisis: `DEC-13`/`DEC-16` (menor y aprobación), `DEC-07` (conexión perdida), `DEC-25` (jurisdicción), `DEC-09`/`DEC-10` (fuentes y frescura).
3. El resto.

## Garantías
- **Ninguna decisión está tomada.** Todo formulario arranca vacío.
- Las recomendaciones son **mías** y están marcadas con ★; los números de umbrales que propongo (p. ej. frescura de 15 min) son **parámetros a confirmar**, no datos del PDF.
- Probado: la lógica del documento final (22 comprobaciones) y la interfaz (35 comprobaciones: clics, guardado, recarga, filtros, descarga, borrador).
