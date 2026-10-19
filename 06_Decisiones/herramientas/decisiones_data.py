# -*- coding: utf-8 -*-
"""
Fuente única del catálogo de decisiones.
De este archivo se generan: decisiones.json, DECISIONES_CATALOGO.md y FORMULARIO_DECISIONES.html
(ver generar.py). Para cambiar una decisión, edita aquí y vuelve a ejecutar generar.py.

Convenciones:
- tipo: "INTERNA" (diseño/criterio) o "EXTERNA" (usa información fuera del PDF: REVISIÓN ESTRICTA).
- Cada opción tiene `externas`: True si esa opción incorpora información de 05_Politicas_Externas.
- rec: opciones recomendadas por el análisis (lista, por si la decisión es de selección múltiple).
"""

P = "05_Politicas_Externas/"
POLREF = {
    "MATRIZ": (P + "15_Matriz_comparativa.md", "Comparación por tema entre todas las fuentes y las reglas del PDF."),
    "CRUCE": (P + "16_Referencias_cruzadas.md", "Qué política toca qué brecha, requerimiento y decisión."),
    "LEEME": (P + "00_LEEME_Politicas.md", "Estado de captura de cada fuente y qué país importa para el caso (§3)."),
    "POL-UY-01": (P + "01_Uruguay_articulos_centro_ayuda.md", "Retraso de 31 min o más y no conforme: cambio sin costo (mismo destino y cabina, 12 meses) o devolución sin cargo."),
    "POL-UY-02": (P + "01_Uruguay_articulos_centro_ayuda.md", "Adelanto de 16 min o más: mismas opciones que el retraso."),
    "POL-UY-03": (P + "01_Uruguay_articulos_centro_ayuda.md", "Cancelación: alternativa, nueva fecha sin costo o devolución total (incluye tasas)."),
    "POL-CL-00": (P + "03_Chile_conoce-tus-derechos.md", "Las soluciones valen solo en Chile (vuelos con origen en Chile)."),
    "POL-CL-01": (P + "03_Chile_conoce-tus-derechos.md", "Atraso en aeropuerto: más de 1 h conectividad; más de 2 h alimentación (y cada 3 h); más de 4 h de noche alojamiento y transporte; más de 11 h de día transporte. Excepto clima, fuerza mayor o caso fortuito."),
    "POL-CL-02": (P + "03_Chile_conoce-tus-derechos.md", "Atraso de más de 3 h y decide no volar: devolución de pasaje y tasas."),
    "POL-CL-03": (P + "03_Chile_conoce-tus-derechos.md", "Desde 31 min de atraso: cambio (fecha, hora o destino, misma cabina) o devolución."),
    "POL-CL-04": (P + "03_Chile_conoce-tus-derechos.md", "Reprogramación o cancelación: reubicación, cambio sin cargo ni diferencia tarifaria, devolución si espera más de 3 h; alojamiento si hay que pernoctar."),
    "POL-CL-06": (P + "03_Chile_conoce-tus-derechos.md", "Sobreventa: opciones, devolución en 10 días hábiles y compensación en UF (la tabla tiene una fila anómala)."),
    "POL-CL-07": (P + "03_Chile_conoce-tus-derechos.md", "Pérdida de conexión en la misma reserva: reubicación, cambio sin cargo ni diferencia tarifaria, devolución si decide no volar."),
    "POL-CL-13": (P + "03_Chile_conoce-tus-derechos.md", "Menores de 14 años: asientos contiguos a un adulto de su familia o de la misma reserva."),
    "POL-CL-16": (P + "03_Chile_conoce-tus-derechos.md", "Las tasas de embarque siempre son reembolsables; las tarifas baratas no admiten cambio ni devolución voluntaria; se evalúa por segmento."),
    "POL-PE-01": (P + "04_Peru_Decision_619_CAN.md", "Decisión 619 art. 2: aplica a quien inicia su viaje en un país andino, o es transferido allí por el transportista."),
    "POL-PE-02": (P + "04_Peru_Decision_619_CAN.md", "Definiciones: niños menores de 5 años son usuarios con necesidades especiales; valor neto sin tasas ni impuestos."),
    "POL-PE-03": (P + "04_Peru_Decision_619_CAN.md", "Art. 4: informar cambios al menos 4 h antes; información preferentemente escrita de derechos ante retraso, cancelación o sobreventa."),
    "POL-PE-06": (P + "04_Peru_Decision_619_CAN.md", "Art. 7: cancelación; liberación si avisó con 15 días o más; causas no imputables solo si las verifica la autoridad nacional."),
    "POL-PE-07": (P + "04_Peru_Decision_619_CAN.md", "Art. 8: retraso más de 2 h refrigerio y llamada; más de 4 h comida; más de 6 h compensación mínima 25 % y hospedaje o reembolso; cancelación; sobreventa; conexiones."),
    "POL-PE-09": (P + "04_Peru_Decision_619_CAN.md", "Art. 10: atención prioritaria a menores no acompañados y personas con necesidades especiales."),
    "POL-PE-10": (P + "04_Peru_Decision_619_CAN.md", "Art. 11: reembolso dentro de 5 días hábiles."),
    "POL-PE-16": (P + "04_Peru_Decision_619_CAN.md", "Art. 24: no se pueden imponer condiciones inferiores a las de la Decisión."),
    "POL-CO-02": (P + "05_Colombia.md", "Informar cambios por el medio más rápido, a más tardar 24 h antes."),
    "POL-CO-04": (P + "05_Colombia.md", "Demora: más de 1 h refrigerio; más de 3 h comida; más de 5 h compensación de al menos 30 % (no si sale antes de 6 h)."),
    "POL-CO-05": (P + "05_Colombia.md", "Cancelación: devolución más compensación de al menos 30 % y hospedaje."),
    "POL-CO-07": (P + "05_Colombia.md", "Adelanto de más de 1 h: devolución o siguiente vuelo."),
    "POL-UYN-02": (P + "06_Uruguay_cartilla_DINACIA.md", "Espera de más de 4 h: comidas, alojamiento y transporte; no aplica por clima."),
    "POL-UYN-04": (P + "06_Uruguay_cartilla_DINACIA.md", "Menores de 5 años, personas con discapacidad o mayores de 70: embarque preferente."),
    "POL-AR-03": (P + "07_Argentina_ANAC.md", "Demoras: hasta 4 h nada (salvo 00-06 h comidas); 4-8 h comidas; más de 8 h comidas, alojamiento y traslado."),
    "POL-BO-01": (P + "09_Bolivia.md", "Avisar cambios al menos 4 h antes (nacional) o 12 h (internacional)."),
    "POL-EC-01": (P + "10_Ecuador.md", "Ecuador (fuente secundaria): compensación mínima de 25 % del trayecto; las fuentes discrepan en los tramos."),
    "POL-UE-03": (P + "02_Union_Europea_Reg_261-2004.md", "UE: cancelación; adelanto de más de 1 h se considera cancelación; compensación salvo aviso de 14 días o circunstancias extraordinarias."),
}


def O(id, titulo, detalle, pros, contras, externas=False):
    return {"id": id, "titulo": titulo, "detalle": detalle, "pros": pros, "contras": contras, "externas": externas}


def D(id, grupo, titulo, tipo, pregunta, contexto, traz, opciones, rec, razon, efecto, refs=None, multiple=False, orden=None):
    z = {"src": [], "req": [], "amb": [], "gap": [], "dat": [], "pol": []}
    z.update(traz)
    return {
        "id": id, "grupo": grupo, "titulo": titulo, "tipo": tipo, "pregunta": pregunta, "contexto": contexto,
        "traz": z, "referencias": refs or [], "opciones": opciones,
        "rec": rec, "razon": razon, "efecto": efecto, "multiple": multiple, "orden": orden if orden is not None else int(id.split("-")[1]),
    }


GRUPOS = {
    "A": "A · Alcance y enfoque del ejercicio",
    "B": "B · Interpretación del caso y de los datos",
    "C": "C · Autonomía, intervención humana y acciones",
    "D": "D · Datos, seguridad y operación",
    "E": "E · Políticas externas (REVISIÓN ESTRICTA)",
    "F": "F · Presentación y uso de IA",
}


def refs(*ids):
    out = []
    for i in ids:
        a, r = POLREF[i]
        out.append({"etiqueta": i, "archivo": a, "resumen": r})
    return out


DEC = []

# ───────────────────────────── A · ALCANCE ─────────────────────────────
DEC.append(D(
    "DEC-01", "A", "Track a implementar", "INTERNA",
    "¿Implementas el track Backend/Integración o el track Frontend/Experience? (el otro queda como diseño)",
    "El PDF exige profundidad en uno solo y diseño del otro (SRC-04-17, SRC-04-20). El caso base es sobre todo lógica de decisión (reserva + eventos + políticas) con varias trampas en los datos; las dimensiones de evaluación 'Fundamentos de ingeniería' y 'Razonamiento agentic y control' se demuestran mejor con contratos, errores e idempotencia.",
    {"src": ["SRC-04-17", "SRC-04-18", "SRC-04-19", "SRC-04-20", "SRC-05-02", "SRC-07-02", "SRC-07-07"], "req": ["REQ-F-07", "REQ-F-08", "REQ-F-09", "REQ-D-02"]},
    [O("a", "Backend/Integración", "Servicio o función que combina reserva, eventos y política, con manejo de errores y al menos un test. La experiencia del pasajero queda como especificación del mensaje.",
       "Ejercita contratos, errores, idempotencia, calidad de datos; evidencia verificable por tests; encaja con 'control' y 'agentic'.",
       "La experiencia visible del pasajero queda solo como diseño."),
     O("b", "Frontend/Experience", "Pantalla o flujo que consume datos equivalentes y muestra estado del viaje, alerta y recomendación, con una validación.",
       "Resultado visible y fácil de mostrar en 10 minutos.",
       "Riesgo de esconder la lógica de decisión (donde están las trampas); consume datos simulados; la capa backend queda como supuesto.")],
    ["a"], "El valor del ejercicio está en la lógica de decisión y en cómo se tratan los datos defectuosos; eso es backend. La pantalla se puede especificar sin implementarla.",
    "Define cuál de REQ-F-07 o REQ-F-08 se cumple y qué debe especificarse en REQ-F-09. Cambia el contenido de REQ-D-02."))

DEC.append(D(
    "DEC-02", "A", "Rol de la IA en tiempo de ejecución", "INTERNA",
    "¿Se usa IA dentro del producto (runtime)? Si sí, ¿para qué? Si no, ¿cómo lo justificas?",
    "No es obligatorio usar IA en runtime y resolver de forma determinística 'puede ser una excelente decisión' (SRC-05-01). Aun así hay que diseñar cómo se manejaría una consulta ambigua y dónde intervendría IA o un agente (SRC-04-22).",
    {"src": ["SRC-05-01", "SRC-06-05", "SRC-04-09", "SRC-07-07", "SRC-04-22"], "req": ["REQ-F-06", "REQ-F-10", "REQ-N-06", "REQ-D-09"], "gap": ["GAP-22", "GAP-24"], "dat": ["DAT-65", "DAT-79"]},
    [O("a", "Sin IA en runtime (determinístico + plantillas validadas)", "La decisión y los mensajes se generan con reglas y plantillas. La IA aparece solo como diseño para la consulta libre.",
       "Máxima exactitud y trazabilidad; costo y latencia nulos; sin riesgo de PII hacia un modelo; fácil de operar por un equipo pequeño.",
       "Mensajes menos naturales; la consulta libre ambigua solo queda como diseño."),
     O("b", "IA solo para redactar el mensaje", "Un modelo parafrasea un mensaje construido con hechos ya validados; un validador determinístico revisa el resultado.",
       "Mejor experiencia de lectura.", "Costo y latencia por interacción; dependencia de un modelo; riesgo de alucinar; hay que validar cada salida."),
     O("c", "IA para entender la consulta libre", "Un modelo clasifica la intención y extrae entidades; la decisión sigue siendo determinística.",
       "Cubre consultas ambiguas del pasajero.", "Superficie de prompt injection; dependencia de modelo; necesita límites estrictos de lo que ve."),
     O("d", "Agente con tools", "Un agente decide qué tools llamar y con qué argumentos.",
       "Máxima flexibilidad.", "Alto riesgo con acciones de alto impacto; difícil de auditar; choca con 'control'.")],
    ["a"], "El núcleo del slice debe ser verificable y determinístico. Se documenta b y c como capa AI-assisted opcional para la consulta ambigua (REQ-F-06), explicando por qué no se activa en v1.",
    "Define el contenido de REQ-F-10 (justificación) y la clasificación de pasos de REQ-D-09. Condiciona REQ-N-06 (latencia/costo) y REQ-N-04 (qué ve un modelo)."))

DEC.append(D(
    "DEC-03", "A", "Formato de entrega y soporte de presentación", "INTERNA",
    "¿En qué formato entregas los tres entregables y con qué soporte presentas los 10 minutos?",
    "El formato es libre y la estética no se evalúa; no se exigen diapositivas (SRC-06-02, SRC-06-03).",
    {"src": ["SRC-01-05", "SRC-06-02", "SRC-06-03"], "req": ["REQ-P-09", "REQ-P-06", "REQ-D-11"]},
    [O("a", "Repositorio + Markdown", "Código y tests, README.md (≤2 págs.), AI_NOTE.md (≤1 pág.) y una tabla de clasificación de pasos; la presentación se hace directamente sobre estos archivos.",
       "Todo localizable y versionable; sin trabajo extra de diapositivas.", "Requiere que el comité pueda abrir el repo."),
     O("b", "Repositorio + PDFs generados", "Igual que a, pero exportando los documentos a PDF.", "Fácil de enviar por correo.", "Pasos extra de exportación dentro de las 3 horas."),
     O("c", "Un documento único + demo", "Un solo documento largo y una demostración.", "Narrativa continua.", "Difícil respetar los límites de 2 y 1 página por entregable.")],
    ["a"], "Minimiza trabajo no evaluado y maximiza evidencia localizable (SRC-07-05).",
    "Determina cómo se presentan REQ-D-07, REQ-D-08 y el soporte REQ-D-11."))

DEC.append(D(
    "DEC-04", "A", "Alcance del vertical slice", "INTERNA",
    "¿Qué cubre exactamente el slice dentro de las 3 horas?",
    "El tiempo es un límite, no una meta (SRC-06-01). El PDF habla de 'modificación' en general (SRC-01-09) pero solo muestra un retraso. El ejemplo es un único caso (DAT-82).",
    {"src": ["SRC-01-09", "SRC-04-21", "SRC-04-23", "SRC-06-01"], "req": ["REQ-F-00", "REQ-F-05", "REQ-D-04", "REQ-P-01"], "gap": ["GAP-07"], "dat": ["DAT-18", "DAT-82"]},
    [O("a", "Solo el caso base", "Retraso en S1 con pérdida de conexión, menor en el grupo y las tres opciones del ejemplo.", "Profundidad; cabe en 3 horas.", "No demuestra el manejo de las trampas de borde."),
     O("b", "Caso base + casos borde críticos", "Además: evento contradictorio (TC-02/03), opción sin cupos (TC-09), 503 (TC-14) y notificación sin validar (TC-16).", "Demuestra criterio donde están las trampas.", "Algo más de trabajo; hay que acotar."),
     O("c", "Caso base + otros tipos de evento", "Agrega cancelación y adelanto.", "Amplitud.", "Obliga a inventar política y datos que el PDF no define (GAP-07).")],
    ["b"], "El ejercicio mide criterio, no volumen (SRC-01-08). Los casos borde críticos muestran control sin inventar datos.",
    "Fija el alcance de REQ-D-04 y la lista de pruebas de REQ-D-05; delimita REQ-F-00."))

# ───────────────────────────── B · INTERPRETACIÓN ─────────────────────────────
DEC.append(D(
    "DEC-05", "B", "¿Qué es una «modificación relevante»? (AMB-01)", "EXTERNA",
    "¿Con qué criterio el sistema decide que un evento es una modificación relevante para el pasajero?",
    "El PDF no lo define a propósito (SRC-04-12). En el ejemplo hay un retraso de 160 min, un cambio de puerta y dos estados. La política del PDF usa 180 min (R1), pero la aerolínea trata como derecho de cambio desde 31 min de retraso y 16 min de adelanto (información externa).",
    {"src": ["SRC-04-12", "SRC-01-13"], "req": ["REQ-F-02", "REQ-F-11"], "amb": ["AMB-01"], "gap": ["GAP-02", "GAP-07"], "dat": ["DAT-15", "DAT-23"]},
    [O("a", "Solo lo que activa una regla del PDF", "Relevante si se cumple R1, R2, R3 o R5 (o alguna regla futura).", "Simple y verificable con la política devuelta por la tool.", "Ignora retrasos de 31 a 179 min que la aerolínea considera relevantes."),
     O("b", "Por impacto en el itinerario (con umbral configurable)", "Relevante si hay cancelación, retraso o adelanto sobre un umbral, conexión perdida, o cambio de aeropuerto o fecha. El cambio de puerta se informa como dato, sin tratarlo como modificación relevante.", "Alineado con el objetivo del pasajero; el umbral es un parámetro.", "Hay que elegir el umbral (ver DEC-26).", True),
     O("c", "Todo evento es relevante", "Se informa cualquier evento.", "Transparencia total.", "Ruido y riesgo de comunicar datos no verificados; más contactos al call center.")],
    ["b"], "Es la lectura más cercana a 'entienda si hubo una modificación relevante y qué implica' (SRC-01-13). El umbral queda como parámetro y su valor depende de DEC-26.",
    "Define el criterio de REQ-F-11 y la salida de REQ-F-02. Depende de DEC-26 y DEC-31.",
    refs("POL-UY-01", "POL-UY-02", "POL-CL-03", "MATRIZ")))

DEC.append(D(
    "DEC-06", "B", "Medición del retraso y llegada nueva", "INTERNA",
    "¿El retraso que usan las reglas es de salida o de llegada, y cómo se obtiene la llegada nueva?",
    "El evento solo trae `delay_minutes` y `new_departure` (salida). No existe `new_arrival` (DAT-19). Las normas externas miden unas a la salida y otras a la llegada, pero el PDF no dice cuál usan sus reglas.",
    {"src": ["SRC-03-03", "SRC-02-08"], "req": ["REQ-F-02", "REQ-F-30"], "gap": ["GAP-15"], "dat": ["DAT-19", "DAT-54", "DAT-75"]},
    [O("a", "Usar el retraso de salida y derivar la llegada por propagación", "Las reglas usan `delay_minutes` (salida). La llegada se deriva sumando el retraso a la llegada programada (supuesto A1) y se etiqueta como derivada.", "Usa solo datos existentes; supuesto explícito.", "Puede equivocarse si el retraso se recupera o crece en vuelo."),
     O("b", "Exigir `new_arrival` a la fuente", "Sin llegada real, no se evalúa la conexión; se degrada a humano.", "No hay supuestos.", "Casi nunca habrá dato; sube la carga humana."),
     O("c", "Evaluar ambos puntos de medición", "Salida para las reglas del PDF y llegada para las normas externas.", "Completo.", "Complejo; usa normas externas sin decidir su jurisdicción (DEC-25).")],
    ["a"], "Es el supuesto más simple y declarable; el resultado se presenta como estimación y exige confirmación antes de actuar (DEC-13).",
    "Define cómo se obtiene la variable `delay_minutes` y la llegada usada en REQ-F-30c."))

DEC.append(D(
    "DEC-07", "B", "Derivación de «conexión perdida» y tiempo mínimo de conexión", "INTERNA",
    "¿Cómo se decide que `missed_connection` es verdadero si no es un dato y falta el tiempo mínimo de conexión (MCT)?",
    "R3 depende de `missed_connection == true`, que no existe en ningún dato (DAT-45). En el caso base la escala planificada es de 70 min y el retraso de 160 min: la llegada derivada (20:35) es 90 min posterior a la salida de S2 (19:05). Supuestos: A1 propagación íntegra, A2 sin MCT, A3 S2 no se retiene.",
    {"src": ["SRC-02-07", "SRC-03-03"], "req": ["REQ-F-30", "REQ-F-18"], "gap": ["GAP-11"], "dat": ["DAT-07", "DAT-45", "DAT-75"]},
    [O("a", "Llegada derivada > salida del siguiente tramo (MCT = 0)", "Se evalúa en el mismo aeropuerto (sin zonas horarias).", "Simple, sin inventar un MCT.", "Podría marcar como salvable una conexión que en realidad no lo es."),
     O("b", "Igual, con MCT configurable", "El MCT es un parámetro (p. ej. 0 por defecto) documentado como dato faltante.", "Honesto sobre lo que falta; permite ajustar.", "Hay que decidir el valor por defecto."),
     O("c", "No derivar: informar «conexión en riesgo» y escalar", "Nunca se afirma que se perdió; siempre confirma una persona.", "Máxima prudencia.", "Menos automatización; el pasajero espera más."),
     O("d", "Derivar (b) y exigir confirmación humana antes de actuar", "El resultado se marca como estimado; el rebooking no se ejecuta sin confirmar.", "Equilibra utilidad y control.", "Requiere el flujo de aprobación (DEC-13, DEC-15).")],
    ["d"], "La derivación es útil pero no es un dato; por eso se muestra como estimación y la acción de alto impacto queda sujeta a confirmación.",
    "Define cómo se calcula la variable de R3 en REQ-F-30c y cómo se comunica (REQ-F-16)."))

DEC.append(D(
    "DEC-08", "B", "Zonas horarias y fechas", "INTERNA",
    "¿Cómo se tratan las horas «HH:MM» sin zona horaria?",
    "Verificado para el 15-sep-2026: Santiago UTC-3, Lima UTC-5, Ciudad de México UTC-6. Con zonas reales S1 duraría 5 h 25 min (sospechoso); con reloj único, 3 h 25 min (DAT-05). La conexión se evalúa en Lima con dos horas de Lima, así que no depende de zonas.",
    {"src": ["SRC-02-07", "SRC-02-08"], "req": ["REQ-F-21"], "gap": ["GAP-15"], "dat": ["DAT-05", "DAT-06", "DAT-20"]},
    [O("a", "Local del aeropuerto + comparar solo dentro del mismo aeropuerto + UTC para edades", "Se usa una tabla mínima versionada IATA→zona (SCL, LIM, MEX) solo cuando haya que convertir.", "Correcto y mínimo.", "Hay que mantener una tabla pequeña."),
     O("b", "Reloj único (ignorar zonas)", "Se suman y restan horas como si fueran del mismo reloj.", "Muy simple.", "Incorrecto para cálculos entre aeropuertos."),
     O("c", "Exigir offset en los datos", "Pedir que las tools devuelvan hora con zona.", "Elimina la ambigüedad.", "Modifica el contrato; el PDF pide mantenerlos (SRC-01-16).")],
    ["a"], "Evita errores sin cambiar contratos; la conexión (el caso crítico) no necesita zonas.",
    "Fija cómo se calculan las edades de datos (REQ-F-21) y la aritmética de fechas."))

DEC.append(D(
    "DEC-09", "B", "Fuentes contradictorias y precedencia (AMB-05)", "INTERNA",
    "¿Qué regla se usa cuando dos fuentes dicen cosas distintas del mismo segmento?",
    "E-1012 (LEGACY_MIRROR, degradada, 09:30Z) dice ON_TIME; E-1001 (OPS_CORE, 10:48Z) dice retraso de 160 min. Además E-1012 tiene el id más alto (DAT-16). Aquí recencia y salud de fuente coinciden, pero el PDF pide una regla general (SRC-04-16).",
    {"src": ["SRC-04-16", "SRC-04-04", "SRC-01-18"], "req": ["REQ-F-15", "REQ-F-21", "REQ-N-01"], "amb": ["AMB-05"], "gap": ["GAP-16"], "dat": ["DAT-15", "DAT-16", "DAT-26"]},
    [O("a", "Regla compuesta", "1) excluir fuentes en `sources_degraded` como evidencia primaria; 2) entre las sanas, gana el `recorded_at` más reciente; 3) empate: jerarquía OPS_CORE > AIRPORT_FEED > LEGACY_MIRROR; 4) si no queda fuente sana o el conflicto no se resuelve: mensaje cauto y humano.", "Cubre salud, recencia y empate; auditable.", "La jerarquía de fuentes es un supuesto mío que debes confirmar."),
     O("b", "Solo recencia", "Gana el evento más reciente.", "Muy simple.", "Elegiría un evento de una fuente degradada si fuera más nuevo."),
     O("c", "Solo jerarquía fija", "Gana siempre OPS_CORE.", "Predecible.", "Ignora que un dato sano puede ser viejo."),
     O("d", "Siempre humano ante conflicto", "Cualquier contradicción escala.", "Máxima prudencia.", "Más intervención humana y más contactos.")],
    ["a"], "Es la única que evita mostrar ON_TIME y a la vez maneja los casos que no son tan claros como el del ejemplo.",
    "Define el contenido de REQ-F-15 y la condición de bloqueo de REQ-F-16 cuando hay conflicto."))

DEC.append(D(
    "DEC-10", "B", "Frescura y vigencia de los datos", "INTERNA",
    "¿Qué antigüedad máxima se tolera para informar y para actuar?",
    "El PDF pide controlar la frescura (SRC-01-18) pero no da umbrales. Los eventos válidos del ejemplo tenían 14 y 7 minutos al recuperarlos; las opciones vencen a los 120 s (DAT-17, DAT-35).",
    {"src": ["SRC-01-18", "SRC-03-02"], "req": ["REQ-F-21", "REQ-F-25"], "gap": ["GAP-16"], "dat": ["DAT-17", "DAT-35"]},
    [O("a", "Umbrales distintos por tipo de uso", "Informar estado: hasta 15 min; actuar: datos recuperados en la misma operación y revalidados; opciones: respetar el TTL; política: revalidar versión antes de escribir. Los valores son parámetros.", "Proporcional al riesgo.", "Los números son propuestas mías que debes confirmar."),
     O("b", "Un umbral único", "Por ejemplo 10 minutos para todo.", "Simple.", "No distingue informar de actuar."),
     O("c", "Sin umbral; solo mostrar la hora", "El mensaje incluye la hora de la información.", "Nada que configurar.", "No cumple «controlar la frescura».")],
    ["a"], "El riesgo de un dato viejo es mayor al ejecutar que al informar.",
    "Fija parámetros de REQ-F-21 y REQ-F-25 y la regla DQ-14/DQ-15."))

DEC.append(D(
    "DEC-11", "B", "Datos parciales (`completeness: PARTIAL`)", "INTERNA",
    "¿Qué se puede hacer y decir cuando faltan campos?",
    "Falta `change_penalty_amount`; además `missing_fields` no es exhaustivo (faltan cabina, estado del ticket, mapa pasajero-segmento) (DAT-09).",
    {"src": ["SRC-01-17", "SRC-02-07"], "req": ["REQ-F-22"], "gap": ["GAP-17"], "dat": ["DAT-09"]},
    [O("a", "Condicionar cada afirmación a los campos que necesita", "Hay una tabla afirmación → campos requeridos. Si falta alguno, no se afirma ni se cotiza.", "Preciso; permite responder lo que sí se sabe.", "Hay que mantener la tabla."),
     O("b", "Bloquear toda respuesta si es PARTIAL", "Si la reserva es parcial, no se responde.", "Muy seguro.", "Inutiliza el producto: casi siempre será parcial."),
     O("c", "Rellenar con valores por defecto", "Suponer el dato faltante.", "Siempre responde.", "Peligroso: inventa información.")],
    ["a"], "Es lo que permite 'tolerar información parcial' sin inventar.",
    "Define la tabla de gating de REQ-F-22 y la regla DQ-28."))

DEC.append(D(
    "DEC-12", "B", "Evaluación segura de reglas y variables derivadas", "INTERNA",
    "¿Cómo se evalúan las `condition` (texto) y se derivan las cuatro variables que no vienen en los datos?",
    "R1-R5 son cadenas con un mini-lenguaje no definido (solo se ven `>=`, `==`, `AND`). `international`, `missed_connection`, `compensation_requested` y `group_includes_minor` no existen en ningún dato (DAT-45, DAT-48).",
    {"src": ["SRC-03-03"], "req": ["REQ-F-19"], "gap": ["GAP-18"], "dat": ["DAT-45", "DAT-48"]},
    [O("a", "Mapear cada (versión, regla) a un predicado codificado", "Cada regla conocida tiene su función; una regla o versión desconocida escala a humano.", "Seguro y sencillo.", "Acopla el código a versiones concretas."),
     O("b", "Parser acotado con lista blanca", "Solo reconoce identificadores conocidos, `>=`, `==` y `AND`; lo demás es error.", "Genérico y seguro; entiende reglas nuevas del mismo estilo.", "Hay que escribir y probar el parser."),
     O("c", "Evaluar con un intérprete dinámico", "Ejecutar el texto de la condición.", "Muy rápido de escribir.", "Riesgo de inyección y comportamiento impredecible.")],
    ["b"], "Un parser mínimo con lista blanca es pequeño, generaliza a reglas nuevas y falla de forma segura. Si falta tiempo, a es el respaldo.",
    "Define cómo se implementa REQ-F-19 y registra cada variable derivada como DERIVADA con sus supuestos (REQ-F-28)."))

DEC.append(D(
    "DEC-13", "B", "Precedencia entre reglas (R3 vs R5) y aprobación humana", "INTERNA",
    "Si R3 no exige aprobación pero R5 sí (hay un menor), ¿se puede ejecutar el rebooking?",
    "El PDF no define cómo se combinan las reglas (DAT-47). Lecturas: L1 cada regla gobierna solo su propio derecho; L2 R5 condiciona toda acción del caso. Además cambiar una reserva es una acción de alto impacto (SRC-04-06).",
    {"src": ["SRC-03-03", "SRC-04-06"], "req": ["REQ-F-17", "REQ-F-14"], "amb": ["AMB-03", "AMB-04"], "gap": ["GAP-19"], "dat": ["DAT-46", "DAT-47"]},
    [O("a", "Gana la regla más restrictiva (L2)", "Si cualquier regla aplicable exige aprobación humana, el caso completo queda pendiente de esa aprobación.", "Seguro; protege al menor; simple de explicar.", "Más intervención humana."),
     O("b", "Cada derecho por separado (L1)", "El rebooking (R3) procede solo; la atención prioritaria (R5) pasa por humano.", "Más automatización.", "Se podría rebookear al grupo sin que una persona revise la situación del menor."),
     O("c", "R5 no bloquea, pero obliga a abrir caso y a un mensaje cauto", "El rebooking se prepara, pero se comunica «en revisión».", "Término medio.", "Mensaje ambiguo para el pasajero.")],
    ["a"], "Con un menor y una acción de alto impacto, la lectura conservadora es la defendible en v1.",
    "Define la regla de combinación que usa REQ-F-17 y los disparadores de REQ-F-14. Condiciona el resultado esperado REQ-F-30g."))

# ───────────────────────────── C · AUTONOMÍA ─────────────────────────────
DEC.append(D(
    "DEC-14", "C", "Qué se entrega de forma automática (AMB-03)", "INTERNA",
    "¿Qué acciones y mensajes puede producir el sistema sin intervención humana?",
    "El PDF no lo define (SRC-04-14). Las tools de escritura son de alto impacto; los mensajes no deben llevar información no validada (SRC-02-05).",
    {"src": ["SRC-04-14", "SRC-01-10"], "req": ["REQ-F-13", "REQ-F-17"], "amb": ["AMB-03"], "dat": ["DAT-47"]},
    [O("a", "Automático solo informar y explicar con hechos validados", "Estado del viaje, explicación de la modificación y propuesta de siguiente paso (como propuesta). Toda escritura requiere confirmación humana en v1.", "Seguro; cumple 'sin acciones de alto impacto sin controles'.", "El pasajero espera la confirmación para el cambio."),
     O("b", "Además recomendar y ejecutar cuando R1 o R3 y sin menor y con datos completos", "Rebooking automático bajo condiciones estrictas.", "Más resolución sin contacto humano.", "Riesgo alto en la primera versión; más superficie de error."),
     O("c", "Todo con humano", "Ni siquiera se informa sin revisión.", "Máximo control.", "No reduce contactos evitables (SRC-01-11).")],
    ["a"], "Equilibra el objetivo de reducir contactos con las restricciones de control (SRC-01-10, SRC-04-06).",
    "Define la matriz acción × condiciones de REQ-F-13 y qué escrituras requieren REQ-F-17."))

DEC.append(D(
    "DEC-15", "C", "Cuándo interviene una persona (AMB-04)", "INTERNA",
    "¿Qué situaciones obligan a crear un caso humano antes de actuar o comunicar? (selección múltiple)",
    "El PDF no lo define (SRC-04-15). `create_human_case` existe con cola DISRUPTION_L2 y SLA de 45 min; no define el esquema de `reason`/`evidence` (DAT-64).",
    {"src": ["SRC-04-15", "SRC-02-04"], "req": ["REQ-F-14", "REQ-F-26", "REQ-F-04"], "amb": ["AMB-04"], "gap": ["GAP-26"], "dat": ["DAT-64"]},
    [O("a", "Hay un menor en el grupo (R5)", "Siempre caso humano.", "Protege al menor.", "Aumenta casos."),
     O("b", "El pasajero solicita compensación (R4)", "Siempre caso humano, sin montos.", "Evita promesas.", "—"),
     O("c", "Datos parciales que bloquean la afirmación", "Si falta un campo necesario para el mensaje.", "Evita inventar.", "—"),
     O("d", "Fuentes en conflicto sin resolver", "Según DEC-09 punto 4.", "Evita mensajes falsos.", "—"),
     O("e", "Resultado indeterminado (503)", "Tras reintentos acotados.", "Evita duplicados y falsas confirmaciones.", "—"),
     O("f", "Evento de tipo desconocido", "Por ejemplo cancelación si no está soportada.", "Falla seguro.", "—"),
     O("g", "Ninguna opción cubre a todo el grupo", "Cupos menores que pasajeros.", "No separa familias.", "—"),
     O("h", "Pernocte u otra asistencia no cubierta por la política", "Alojamiento, comidas, traslados.", "No promete lo que no hay regla.", "—"),
     O("i", "Se solicitan datos personales", "Documento, correo, teléfono.", "Mínimo privilegio.", "—")],
    ["a", "b", "c", "d", "e", "f", "g", "h", "i"],
    "Son los puntos donde el sistema carece de dato, de regla o de control; escalar es lo defendible. La lista es ajustable casilla por casilla.",
    "Convierte AMB-04 en disparadores explícitos de REQ-F-14 y define cuándo se invoca REQ-F-26.", multiple=True))

DEC.append(D(
    "DEC-16", "C", "Menores y grupos familiares (producto)", "INTERNA",
    "¿Cómo trata el producto un grupo con menor al ofrecer y ejecutar opciones?",
    "O2 tiene 1 cupo para 2 pasajeros (DAT-31). Las opciones no indican qué pasajeros cubren ni cabina (DAT-43). `create_rebooking_request` no recibe pasajeros (DAT-62).",
    {"src": ["SRC-03-02", "SRC-03-03"], "req": ["REQ-F-17", "REQ-F-14"], "gap": ["GAP-08", "GAP-20"], "dat": ["DAT-03", "DAT-31", "DAT-43", "DAT-62"]},
    [O("a", "Regla dura: nunca separar al grupo", "Solo se ofrecen y ejecutan opciones que cubran a todo el grupo juntos; con un menor siempre se abre caso humano antes de rebookear.", "Protege al menor; simple.", "Reduce opciones ofrecidas."),
     O("b", "Permitir opciones parciales con aviso", "Se informa que solo hay lugar para parte del grupo.", "Más opciones.", "Riesgo de separar a un niño de su acompañante."),
     O("c", "Que decida el pasajero", "Se presentan todas las opciones y él elige.", "Autonomía.", "Traslada una decisión delicada a quien tiene menos información.")],
    ["a"], "Es la lectura más segura de 'cambiar una reserva es de alto impacto' con un menor.",
    "Añade una restricción explícita a REQ-F-17 y a la selección de opciones (REQ-F-20)."))

DEC.append(D(
    "DEC-17", "C", "Selección y presentación de opciones", "INTERNA",
    "¿Qué opciones ve el pasajero y cómo se trata `confidence`?",
    "Las opciones son candidatas, no decisión final (SRC-02-01). O1 es viable; O2 no (cupo y costo); O3 es un cascarón sin monto y sin política recuperada (DAT-31 a DAT-33). `confidence` no está definida (DAT-36).",
    {"src": ["SRC-02-01", "SRC-03-02"], "req": ["REQ-F-20", "REQ-F-03"], "gap": ["GAP-17", "GAP-20"], "dat": ["DAT-31", "DAT-32", "DAT-33", "DAT-36"]},
    [O("a", "Mostrar solo opciones viables y coherentes, más la vía de reembolso como alternativa", "O1 como propuesta principal; la devolución como otra vía sin montos ni plazos; O2 no se muestra (se registra por qué).", "Evita confundir; cumple 'no información no verificada'.", "El pasajero no ve que existía O2."),
     O("b", "Mostrar todas ordenadas por `confidence` con advertencias", "Transparencia completa.", "Todo a la vista.", "Muestra opciones inviables y un campo sin definición."),
     O("c", "Mostrar solo la recomendada", "Una única propuesta.", "Muy claro.", "Poca autonomía.")],
    ["a"], "La viabilidad (cupos, costo, política) se valida; `confidence` se usa solo para ordenar, nunca para decidir.",
    "Define el filtro de REQ-F-20 y el contenido del mensaje de REQ-F-03."))

DEC.append(D(
    "DEC-18", "C", "Ciclo de vida del rebooking: idempotencia, 409, 503 y PENDING_CONFIRMATION", "INTERNA",
    "¿Cómo se diseñan la llave idempotente y el manejo de 409/503, y qué se hace con PENDING_CONFIRMATION?",
    "503 deja el resultado indeterminado y no hay tool para consultar estado (DAT-59, GAP-12). 409 devuelve el mismo request_id (DAT-60). PENDING_CONFIRMATION no tiene tool de confirmación y expira en ~9 min (DAT-61). La llamada no incluye reserva ni pasajeros (DAT-62).",
    {"src": ["SRC-02-03", "SRC-03-04", "SRC-04-01"], "req": ["REQ-F-23", "REQ-F-24", "REQ-C-05"], "gap": ["GAP-12"], "dat": ["DAT-59", "DAT-60", "DAT-61", "DAT-62", "DAT-63"]},
    [O("a", "Llave determinista persistida antes de llamar; 503 → mismos reintentos acotados → caso humano; 409 → existente", "Llave derivada de la operación (reserva + vuelo/fecha + versión de política + decisión). 503: hasta 2 reintentos con la misma llave y luego caso humano, sin decirle al pasajero ni éxito ni fracaso. 409: tratar como solicitud existente. PENDING_CONFIRMATION: confirmación fuera de alcance de v1, documentada como supuesto.", "Evita duplicados y falsas confirmaciones; coherente con el contrato.", "Hay que documentar que la confirmación queda fuera."),
     O("b", "503 → caso humano inmediato", "Sin reintentos.", "Más simple.", "Más carga humana por fallas transitorias."),
     O("c", "Llave aleatoria por intento", "UUID nuevo en cada llamada.", "Trivial.", "No es idempotente: puede duplicar un cambio de reserva.")],
    ["a"], "Es la única variante que respeta que 503 es indeterminado y que el rebooking es de alto impacto.",
    "Fija el contenido de REQ-F-23 y REQ-F-24 y la extensión documentada del contrato (reserva y pasajeros) de REQ-C-05."))

DEC.append(D(
    "DEC-19", "C", "Alineación de tiempos: TTL, expiración y SLA humano", "INTERNA",
    "¿Cómo se concilian opciones que vencen en 2 min, una solicitud que expira en ~9 min y un caso humano con SLA de 45 min?",
    "Una aprobación humana siempre llegará con opciones vencidas y con la solicitud caducada (DAT-77, GAP-25).",
    {"src": ["SRC-03-02", "SRC-03-04", "SRC-04-02"], "req": ["REQ-F-25", "REQ-F-26"], "gap": ["GAP-25"], "dat": ["DAT-35", "DAT-58", "DAT-77"]},
    [O("a", "Revalidar todo justo antes de escribir", "La aprobación humana autoriza una decisión (qué opción), no la ejecución con datos viejos; al aprobar se recuperan de nuevo opciones y política. El mensaje dice «sujeto a disponibilidad».", "Respeta TTL y versión de política.", "El cupo puede ya no existir: hay que prever el reintento o el caso humano."),
     O("b", "Reservar cupo durante la aprobación", "Un «hold» de asiento.", "Asegura el cupo.", "No existe tool para ello."),
     O("c", "Ignorar el TTL", "Usar la opción aunque haya vencido.", "Simple.", "Viola REQ-F-25; puede fallar o rebookear mal.")],
    ["a"], "No hay mecanismo de reserva en el contrato; revalidar es lo único coherente.",
    "Añade el paso de revalidación a REQ-F-25 y REQ-F-26 y al flujo de aprobación."))

DEC.append(D(
    "DEC-20", "C", "Contrato de `notify_passenger` y validación del mensaje", "INTERNA",
    "¿Cómo se construyen y validan los mensajes, y a quién se envían si la firma no incluye destinatario?",
    "La firma es `notify_passenger(message)`; el 422 solo comprueba que haya `policy_ref` (DAT-65). El requisito es más estricto: no enviar información no validada (SRC-02-05). El canal visto es PUSH y el menor no tiene contacto (DAT-71).",
    {"src": ["SRC-02-05", "SRC-04-03"], "req": ["REQ-F-16", "REQ-F-29", "REQ-F-09", "REQ-C-07"], "gap": ["GAP-13", "GAP-22"], "dat": ["DAT-65", "DAT-71"]},
    [O("a", "Plantillas con hechos validados + `policy_ref` + destinatario (extensión del contrato)", "Cada mensaje sale de una plantilla cuyos huecos solo admiten hechos de una lista blanca con evidencia vigente. Un validador propio bloquea el envío si falta evidencia, `policy_ref` o destinatario. Un envío por decisión (con llave de deduplicación).", "Cumple 'no información no validada' con evidencia; fácil de probar.", "Mensajes menos flexibles; hay que extender el contrato en el mock."),
     O("b", "Texto libre generado y validado luego", "Un modelo redacta y un validador revisa.", "Más natural.", "Validar texto libre es difícil; ver DEC-02."),
     O("c", "Solo `policy_ref`, confiando en el 422", "Sin validador propio.", "Mínimo esfuerzo.", "El 422 no valida que el contenido sea verdadero.")],
    ["a"], "Es la forma de cumplir REQ-F-16 con evidencia verificable por tests (TC-16).",
    "Define la capa complementaria de REQ-F-09 (especificación del mensaje) y el validador de REQ-F-29."))

# ───────────────────────────── D · DATOS Y OPERACIÓN ─────────────────────────────
DEC.append(D(
    "DEC-21", "D", "Información visible al pasajero y verificación de identidad (AMB-02)", "INTERNA",
    "¿Qué campos y hechos puede ver el pasajero, y cómo se sabe que es quien dice ser?",
    "`booking_id` abre PII y no es una credencial (DAT-01). El PDF pide proteger datos y aplicar mínimo privilegio (SRC-04-07) pero no define identificación (GAP-21).",
    {"src": ["SRC-04-13", "SRC-04-07", "SRC-01-12"], "req": ["REQ-F-12", "REQ-F-01", "REQ-N-04"], "amb": ["AMB-02"], "gap": ["GAP-21"], "dat": ["DAT-01"]},
    [O("a", "Sesión ya autenticada (supuesto documentado) + lista blanca de campos", "Se asume que el pasajero llega autenticado; se muestran segmentos, horarios, estado, opciones viables y derechos citados; nunca documento, correo, teléfono completo ni nivel de fidelidad; solo nombre de pila.", "Realista para v1; cumple mínimo privilegio.", "Deja la autenticación como dependencia externa."),
     O("b", "Mostrar todo lo que devuelve la tool", "Sin filtro.", "Sin trabajo.", "Expone PII; viola SRC-04-07."),
     O("c", "Verificación explícita en cada consulta", "Segundo factor o datos de la reserva.", "Más seguro.", "Mucho más alcance y fricción.")],
    ["a"], "Acota v1 sin exponer datos y deja la dependencia explícita.",
    "Define la lista blanca de REQ-F-12 y el supuesto de REQ-F-01."))

DEC.append(D(
    "DEC-22", "D", "Datos personales, mínimo privilegio y «qué nunca va a un modelo»", "INTERNA",
    "¿Dónde se aplica la minimización de PII y qué información nunca se entrega a un modelo?",
    "Cinco campos PII viajan en una sola lectura y el contrato de `get_eligible_options` exige el `trip_context` completo (DAT-02, DAT-79). Mantener los contratos choca con mínimo privilegio.",
    {"src": ["SRC-04-07", "SRC-01-16", "SRC-05-04"], "req": ["REQ-N-04", "REQ-F-27", "REQ-D-08"], "gap": ["GAP-27"], "dat": ["DAT-02", "DAT-38", "DAT-79"]},
    [O("a", "Mantener las firmas y minimizar en todas las fronteras que controlas", "Contexto mínimo para decidir (sin correo, teléfono, documento, nivel de fidelidad; nombre de pila; `has_minor` como booleano); logs enmascarados; evidencia de casos humanos solo con ids y hechos; ningún dato personal a un modelo. Se propone al equipo un contrato reducido para `get_eligible_options`.", "Respeta SRC-01-16 y SRC-04-07 a la vez.", "La tool sigue recibiendo todo."),
     O("b", "Contrato reducido en el mock", "El mock de `get_eligible_options` recibe solo el contexto mínimo.", "Mejor privilegio.", "Rompe «mantén estos contratos»."),
     O("c", "Sin minimización", "Pasar y registrar todo.", "Sin trabajo.", "Incumple SRC-04-07.")],
    ["a"], "Es la lectura que cumple las dos instrucciones del PDF; la lista de lo que nunca va a un modelo alimenta el Entregable 3.",
    "Define el inventario de REQ-N-04, el límite de REQ-F-27 y el contenido de REQ-D-08 (d)."))

DEC.append(D(
    "DEC-23", "D", "Trazabilidad, auditoría y retención", "INTERNA",
    "¿Qué se registra de cada decisión y por cuánto tiempo?",
    "Objetivo: exactitud, seguridad y trazabilidad (SRC-01-11). No hay identificador de correlación de punta a punta (DAT-73). El marco legal de retención no está definido (GAP-27).",
    {"src": ["SRC-01-11", "SRC-07-05"], "req": ["REQ-F-28", "REQ-N-08"], "gap": ["GAP-27"], "dat": ["DAT-73", "DAT-80"]},
    [O("a", "Registro de decisión estructurado y sin PII", "Un `decision_id` que ata: lecturas usadas con su `retrieved_at`, eventos elegidos y descartados con razón, versión de política y regla, variables derivadas con supuestos, opción, acción, mensaje y hashes. La retención es un parámetro a definir.", "Reconstruible; auditable; defendible.", "Hay que definir la retención."),
     O("b", "Logs de aplicación sin estructura", "Mensajes de texto.", "Rápido.", "Difícil de reconstruir y de auditar."),
     O("c", "Solo el resultado final", "Guardar la salida.", "Mínimo.", "No cumple trazabilidad.")],
    ["a"], "Es lo que permite defender cada decisión en el debate técnico.",
    "Define el contenido de REQ-F-28 y la evidencia de REQ-E-05."))

DEC.append(D(
    "DEC-24", "D", "Validación mínima, operación, latencia, costo y métrica de éxito", "INTERNA",
    "¿Qué pruebas, presupuestos y métricas se declaran?",
    "El slice necesita al menos una validación o test (SRC-04-18). La operación debe ser viable para un equipo pequeño y hay que considerar latencia, costo y dependencia de modelos (SRC-04-08, SRC-04-09). Se pide decir cómo se mediría el resultado (SRC-07-01).",
    {"src": ["SRC-01-02", "SRC-04-08", "SRC-04-09", "SRC-07-01", "SRC-07-04"], "req": ["REQ-D-05", "REQ-N-05", "REQ-N-06", "REQ-N-09", "REQ-E-01", "REQ-E-04"], "gap": ["GAP-23", "GAP-24"]},
    [O("a", "Conjunto crítico + métricas propuestas + runbook de una página", "Pruebas: TC-01, 02, 03, 09, 14, 16 y borde de R1. Métricas propuestas: contactos al call center tras la notificación; mensajes validados sin corrección humana; casos escalados. Presupuestos como parámetros. Runbook mínimo.", "Cubre calidad y operación con poco trabajo.", "Las métricas son propuestas mías."),
     O("b", "Batería amplia (TC-01 a TC-20)", "Todas las pruebas sugeridas.", "Máxima cobertura.", "No cabe bien en 3 horas."),
     O("c", "Solo el caso base", "Una prueba.", "Mínimo.", "No demuestra criterio sobre las trampas.")],
    ["a"], "Prioriza evidencia donde más importa (SRC-07-05).",
    "Fija REQ-D-05, los presupuestos de REQ-N-05/06 y la métrica de REQ-N-09."))

# ───────────────────────────── E · POLÍTICAS EXTERNAS ─────────────────────────────
DEC.append(D(
    "DEC-35", "E", "Marco: cómo se incorporan las políticas externas", "EXTERNA",
    "¿Las políticas de la aerolínea y las normas por país son fuente de verdad del producto, solo contexto, o se ignoran?",
    "El PDF solo define `get_policy_rules` como fuente de reglas «versionadas y verificables» (SRC-02-02). Las páginas de la aerolínea y normas por país traen umbrales distintos (por ejemplo 31 min vs 180 min; 2 h vs 240 min). Esta decisión enmarca DEC-25 a DEC-34 y conviene tomarla primero.",
    {"src": ["SRC-02-02", "SRC-04-11", "SRC-04-10"], "req": ["REQ-P-11", "REQ-N-07"], "gap": ["GAP-01", "GAP-02", "GAP-03", "GAP-04", "GAP-05", "GAP-06", "GAP-07", "GAP-08", "GAP-09", "GAP-10", "GAP-14"]},
    [O("a", "Solo contexto: el producto usa únicamente `get_policy_rules`", "Las políticas externas sirven para identificar brechas, riesgos y preguntas (README: supuestos y próximos pasos), no como reglas del motor.", "Coherente con el PDF; evita afirmar derechos incorrectos; poco trabajo.", "El producto no reflejará derechos legales que la política del PDF no incluya."),
     O("b", "Tabla propia de políticas por jurisdicción", "Se carga una tabla versionada, revisada por Legal, que complementa a `get_policy_rules`.", "Más completo y cercano a la realidad.", "Fuera del alcance de 3 horas; requiere revisión legal; hay fuentes parciales o secundarias.", True),
     O("c", "Ignorarlas por completo", "No se menciona nada externo.", "Máxima simplicidad.", "Pierde una fuente de supuestos y preguntas valiosas para la defensa.")],
    ["a"], "Es la opción defendible con el tiempo y la información disponibles: el PDF no pide derecho comparado, pero la defensa gana si se muestran las brechas y las preguntas.",
    "Determina si REQ-F-19 se apoya solo en `get_policy_rules` y qué brechas GAP-01…10 pasan a «preguntas/próximos pasos» en el README (REQ-D-07).",
    refs("LEEME", "CRUCE", "MATRIZ"), orden=0))

DEC.append(D(
    "DEC-25", "E", "Jurisdicción aplicable por segmento", "EXTERNA",
    "¿Qué ley o política de país se considera para S1 (SCL→LIM) y para S2 (LIM→MEX)?",
    "Las reglas del PDF no traen país (DAT-51). Chile aplica «solo a vuelos con origen en Chile» (S1). Perú/CAN-619 aplica a quien «inicia su viaje» en un país andino; este pasajero inició en Chile, que no es miembro, así que su aplicación a S2 es ambigua. México no figura en la fuente (GAP-14).",
    {"src": ["SRC-03-03"], "req": ["REQ-F-19", "REQ-F-18"], "gap": ["GAP-01", "GAP-14"], "dat": ["DAT-51"], "pol": ["POL-CL-00", "POL-PE-01", "POL-PE-16"]},
    [O("a", "Solo `get_policy_rules`; jurisdicción como punto de extensión", "v1 no aplica ley por país; se deja el campo `jurisdiction` previsto y la pregunta documentada para Producto/Legal.", "No afirma derechos que dependen de jurisdicción y causa no modeladas.", "No refleja diferencias legales."),
     O("b", "Chile para S1 y CAN-619 para S2 como piso informativo", "Los mensajes citan derechos legales de cada país con revisión humana.", "Más fiel a la realidad.", "Ambigüedad del art. 2 de la Decisión 619; se mezclan política interna y ley.", True),
     O("c", "La más favorable al pasajero", "Se aplica entre PDF, Chile y Perú lo que más beneficie.", "Protege al pasajero.", "Costo e incumplimiento si la política comercial es menor; requiere criterio legal.", True),
     O("d", "Escalar a humano toda disputa de jurisdicción", "El sistema no decide; abre caso.", "Evita error legal.", "Más carga humana.")],
    ["a"], "Con el dato disponible no se puede decidir jurisdicción sin inventar. Se documenta como supuesto bloqueante («qué preguntarías y a quién»: SRC-04-11) y se prevé la extensión.",
    "Define el alcance de REQ-F-19 y la lista de preguntas del README (REQ-D-07 b, e). Condiciona DEC-26 a DEC-33.",
    refs("POL-CL-00", "POL-PE-01", "POL-PE-16", "LEEME", "CRUCE"), orden=1))

DEC.append(D(
    "DEC-26", "E", "Umbral de cambio sin costo por retraso: 180 min (PDF) vs 31 min (la aerolínea)", "EXTERNA",
    "¿Se sigue R1 (≥ 180 min) o se adopta el umbral comercial de la aerolínea (≥ 31 min)?",
    "R1 otorga REBOOK_NO_FEE desde 180 min. la aerolínea (artículos de Uruguay y página de Chile) lo da desde 31 min de retraso, y devolución si el atraso supera 3 h y el pasajero no vuela. En el caso base el retraso es de 160 min: R1 no se cumple, pero la política comercial sí daría cambio.",
    {"src": ["SRC-03-03", "SRC-04-12"], "req": ["REQ-F-11", "REQ-F-18"], "gap": ["GAP-02"], "dat": ["DAT-46", "DAT-55"], "pol": ["POL-UY-01", "POL-CL-02", "POL-CL-03"]},
    [O("a", "Seguir R1 como regla del producto y documentar la discrepancia", "El README registra que la política comercial publicada es más favorable y plantea la pregunta a Producto/Legal.", "Respeta la fuente de verdad del PDF.", "Puede decir «no corresponde» donde la aerolínea sí ofrece cambio."),
     O("b", "Adoptar 31 min en lugar de R1", "Se reemplaza el umbral.", "Más favorable al pasajero.", "Contradice `get_policy_rules`; dato externo sin validar.", True),
     O("c", "Escalar a humano entre 31 y 179 min", "Sin R1 ni R3, un agente confirma.", "No promete ni niega.", "Más casos humanos.", True)],
    ["a"], "En el caso base lo que otorga el cambio sin costo es R3 (conexión), no R1; la discrepancia se declara sin alterar la política del PDF.",
    "Fija el umbral de REQ-F-11 y su justificación; relacionado con DEC-05.",
    refs("POL-UY-01", "POL-CL-02", "POL-CL-03", "MATRIZ"), orden=2))

DEC.append(D(
    "DEC-27", "E", "Asistencia durante la espera (comunicación, comida, alojamiento, traslado)", "EXTERNA",
    "¿Qué se dice sobre asistencia si la política del PDF solo tiene un vale de comida a ≥ 240 min internacional?",
    "Con 160 min de retraso R2 no aplica, pero Chile da alimentación a más de 2 h, y O1 obliga a pernoctar en Lima con un niño de 7 años (Chile y la Decisión 619 dan alojamiento y traslado en esos casos). Las reglas del PDF no tienen regla de alojamiento.",
    {"src": ["SRC-03-03"], "req": ["REQ-F-18", "REQ-F-03"], "gap": ["GAP-03"], "dat": ["DAT-39", "DAT-55"], "pol": ["POL-CL-01", "POL-CL-04", "POL-PE-07", "POL-CO-04", "POL-UYN-02", "POL-AR-03"]},
    [O("a", "Solo lo que devuelve la política (R2)", "No se menciona otra asistencia.", "Coherente con el PDF.", "Silencia un pernocte que existe."),
     O("b", "Mensaje genérico + caso humano si hay pernocte", "«Podrías tener derecho a asistencia; un agente lo confirmará», sin cifras; se abre caso humano por el pernocte.", "No inventa umbrales ni calla el pernocte.", "No resuelve el detalle de inmediato."),
     O("c", "Incorporar umbrales de Chile como reglas adicionales", "Más de 2 h comida; más de 4 h de noche alojamiento.", "Cercano a la ley.", "Depende de DEC-25; datos con anomalías de la fuente.", True)],
    ["b"], "El pernocte es un hecho derivable de los datos (O1 sale al día siguiente); decirlo sin cifras ni promesas es veraz.",
    "Añade a REQ-F-18/REQ-F-03 la mención cautelosa de asistencia y el disparador de caso humano por pernocte (REQ-F-14).",
    refs("POL-CL-01", "POL-CL-04", "POL-PE-07", "POL-CO-04", "POL-UYN-02", "POL-AR-03", "MATRIZ"), orden=3))

DEC.append(D(
    "DEC-28", "E", "Reembolso, tarifas no reembolsables y plazos", "EXTERNA",
    "¿Qué se dice de la opción de reembolso (O3) si no hay regla ni monto y la tarifa es «no reembolsable»?",
    "`refundable:false` describe cambios voluntarios; en una modificación hecha por la aerolínea la aerolínea da derecho de devolución, y siempre devuelve las tasas de embarque. La Decisión 619 fija 5 días hábiles; Chile 10 días hábiles en sobreventa. La política `POL-REFUND-2026-01` citada por O3 no se recuperó.",
    {"src": ["SRC-03-02", "SRC-02-07"], "req": ["REQ-F-18", "REQ-F-03"], "gap": ["GAP-04", "GAP-10"], "dat": ["DAT-11", "DAT-33"], "pol": ["POL-CL-07", "POL-CL-16", "POL-PE-10", "POL-UY-03"]},
    [O("a", "Mencionar que existe la vía de reembolso, sin monto ni plazo, y derivar", "No se usa `refundable:false` para negar; el detalle lo confirma un agente.", "Veraz; no promete.", "El pasajero no ve montos."),
     O("b", "Omitir O3 hasta tener política recuperable", "No se menciona el reembolso.", "No afirma nada no verificable.", "Oculta un derecho probable."),
     O("c", "Incluir plazos y reglas de las normas", "Cinco días hábiles, 10 días hábiles, devolución de tasas.", "Informativo.", "Depende de DEC-25; datos externos.", True)],
    ["a"], "Es veraz con la evidencia disponible y no usa la tarifa voluntaria como excusa.",
    "Define el tratamiento de O3 en REQ-F-20 y el contenido de REQ-F-03; marca GAP-04 y GAP-10 como pregunta abierta.",
    refs("POL-CL-07", "POL-CL-16", "POL-PE-10", "POL-UY-03", "MATRIZ"), orden=4))

DEC.append(D(
    "DEC-29", "E", "Compensación económica (R4)", "EXTERNA",
    "¿Cuándo y cómo se habla de compensación económica?",
    "R4 solo es una bandera (`compensation_requested`), requiere humano y no trae montos. Las normas externas fijan porcentajes distintos (25 % CAN, 30 % Colombia, tablas en UF en Chile para sobreventa, euros en la UE).",
    {"src": ["SRC-03-03", "SRC-04-06"], "req": ["REQ-F-17"], "gap": ["GAP-05"], "dat": ["DAT-50"], "pol": ["POL-PE-07", "POL-CO-04", "POL-CO-05", "POL-EC-01", "POL-CL-06"]},
    [O("a", "Nunca proactivo; solo si el pasajero lo pide; sin montos; caso humano", "Se cumple R4: se abre caso humano.", "Evita promesas y errores.", "El pasajero no recibe información proactiva."),
     O("b", "Informar proactivamente que podría haber compensación", "Mencionar sin cifras.", "Transparente.", "Riesgo de promesa; depende de la causa (GAP-06)."),
     O("c", "Calcular montos con normas externas", "Usar CAN 25 %, etc.", "Informativo.", "Contradice la regla; sin jurisdicción ni causa.", True)],
    ["a"], "Emitir una compensación es de alto impacto (SRC-04-06) y no hay base de montos en el PDF.",
    "Fija el control de REQ-F-17 para compensación y el disparador de REQ-F-14.",
    refs("POL-PE-07", "POL-CO-04", "POL-CO-05", "POL-EC-01", "POL-CL-06", "MATRIZ"), orden=5))

DEC.append(D(
    "DEC-30", "E", "Causa del evento y exenciones (clima, fuerza mayor)", "EXTERNA",
    "¿Cómo se trata que el evento no traiga causa si muchas normas la usan para conceder o negar derechos?",
    "Chile no da servicios por clima, fuerza mayor o caso fortuito; la Decisión 619 exige que la autoridad verifique esas causas; la UE habla de circunstancias extraordinarias. El evento DELAY no trae causa.",
    {"src": ["SRC-02-08"], "req": ["REQ-F-18", "REQ-F-16"], "gap": ["GAP-06"], "dat": ["DAT-22", "DAT-49"], "pol": ["POL-CL-01", "POL-PE-06", "POL-UE-03"]},
    [O("a", "Tratar como «causa no informada»", "No afirmar ni negar derechos que dependan de la causa; mensaje neutral; escalar los casos donde la causa cambiaría el derecho; documentar la brecha.", "Veraz.", "Menos específico."),
     O("b", "Inferir la causa", "Deducirla de otros eventos.", "Más información.", "Especulativo."),
     O("c", "Pedir un campo `cause` (extensión del contrato)", "Proponer ese campo en `get_operational_events`.", "Soluciona la raíz.", "Cambia el contrato; es una recomendación al equipo.")],
    ["a"], "No hay dato para otra cosa; se sugiere c como siguiente paso en el README.",
    "Añade la regla DQ-29 a REQ-F-18/REQ-F-16 y una pregunta abierta en REQ-D-07.",
    refs("POL-CL-01", "POL-PE-06", "POL-UE-03", "CRUCE"), orden=6))

DEC.append(D(
    "DEC-31", "E", "Cancelaciones, adelantos y otros eventos", "EXTERNA",
    "¿El slice cubre solo retrasos o también cancelación y adelanto?",
    "El PDF habla de «modificación» (SRC-01-09) pero solo muestra DELAY, GATE_CHANGE y STATUS, y una política DELAY. la aerolínea trata los adelantos desde 16 min; Colombia y la UE desde más de 1 h; las políticas de cancelación existen en varias normas.",
    {"src": ["SRC-01-09", "SRC-03-03"], "req": ["REQ-F-00", "REQ-F-02"], "gap": ["GAP-07"], "dat": ["DAT-18", "DAT-50"], "pol": ["POL-UY-02", "POL-UY-03", "POL-CO-07", "POL-UE-03"]},
    [O("a", "Solo DELAY; el resto degrada a humano", "Se reconocen GATE_CHANGE y STATUS; cualquier otro tipo (cancelación, adelanto) escala.", "Honesto sobre el alcance; coherente con DEC-04.", "No cubre cancelaciones."),
     O("b", "Incluir cancelación y adelanto con política mock", "Se simula `get_policy_rules('CANCELLATION')`.", "Más amplio.", "Se inventa política y datos."),
     O("c", "Incluirlos con umbrales de la aerolínea", "Por ejemplo 16 min para adelanto.", "Cercano a la práctica.", "Información externa sin validar.", True)],
    ["a"], "No hay datos ni política en el PDF para esos casos; declararlos fuera de alcance es lo defendible.",
    "Delimita REQ-F-00 y deja GAP-07 documentado como próximo paso.",
    refs("POL-UY-02", "POL-UY-03", "POL-CO-07", "POL-UE-03", "MATRIZ"), orden=7))

DEC.append(D(
    "DEC-32", "E", "Definición de «menor» (R5) y derechos asociados", "EXTERNA",
    "¿Qué es un menor para activar R5?",
    "R5 no define edad. En el ejemplo P2 es `type: CHILD`, 7 años. Chile da asientos contiguos hasta los 14 años; la Decisión 619 y Uruguay tratan como especiales a los menores de 5.",
    {"src": ["SRC-03-03"], "req": ["REQ-F-14", "REQ-F-17"], "gap": ["GAP-08"], "dat": ["DAT-03", "DAT-45"], "pol": ["POL-CL-13", "POL-PE-02", "POL-UYN-04"]},
    [O("a", "`type == CHILD` (el dato del sistema)", "Se usa la clasificación que ya trae la reserva.", "No inventa edades; simple.", "Depende de cómo clasifique el sistema de reservas."),
     O("b", "Menor de 18 años", "Criterio general de minoría de edad.", "Conservador.", "Requiere la edad; los adultos no la traen.", True),
     O("c", "Menor de 14 años", "Criterio chileno de asientos contiguos.", "Cercano a una norma.", "Depende de jurisdicción (DEC-25).", True)],
    ["a"], "Usa el dato disponible sin importar una edad externa.",
    "Fija la variable `group_includes_minor` de REQ-F-14/REQ-F-17 (REQ-F-30d).",
    refs("POL-CL-13", "POL-PE-02", "POL-UYN-04", "MATRIZ"), orden=8))

DEC.append(D(
    "DEC-33", "E", "Plazo y contenido de la notificación al pasajero", "EXTERNA",
    "¿Qué debe contener el mensaje y con cuánta anticipación se avisa?",
    "El PDF solo exige `policy_ref` y que no haya información no validada. La Decisión 619 pide avisar al menos 4 h antes y dar información preferentemente escrita de derechos; Colombia 24 h; Bolivia 4/12 h. En el ejemplo, el retraso se registró ~6 h 42 min antes de la salida original.",
    {"src": ["SRC-02-05", "SRC-04-03"], "req": ["REQ-F-03", "REQ-F-16"], "gap": ["GAP-09"], "dat": ["DAT-65"], "pol": ["POL-PE-03", "POL-CO-02", "POL-BO-01"]},
    [O("a", "Mensaje con qué cambió (con hora), qué implica, siguiente paso, `policy_ref`, aviso de estimación y vía humana; sin plazos legales", "No se codifican plazos legales en v1; se documentan como referencia.", "Cumple el PDF sin importar normas.", "No garantiza cumplir plazos de una norma si aplicara."),
     O("b", "Además información escrita de derechos y alerta si faltan menos de 4 h", "Incorpora el art. 4 de la Decisión 619.", "Más completo.", "Depende de DEC-25.", True),
     O("c", "Solo el estado", "Mensaje mínimo.", "Muy simple.", "No cumple 'siguiente paso' (SRC-01-10).")],
    ["a"], "Cumple los requisitos del PDF y deja los plazos legales como referencia para la jurisdicción (DEC-25).",
    "Define el contenido mínimo del mensaje de REQ-F-03/REQ-F-16 y la especificación de REQ-F-09.",
    refs("POL-PE-03", "POL-CO-02", "POL-BO-01", "MATRIZ"), orden=9))

DEC.append(D(
    "DEC-34", "E", "México y otros países fuera de la fuente", "EXTERNA",
    "¿Qué se hace con México, que no figura en la lista de países de la aerolínea?",
    "El destino final del caso es México. La lista de 17 países de la página de la aerolínea no lo incluye; no hay fuente en esta carpeta.",
    {"src": [], "req": ["REQ-F-00"], "gap": ["GAP-14"], "pol": []},
    [O("a", "Fuera de alcance de v1; pregunta documentada", "Se registra como pregunta para Producto/Legal.", "Honesto; sin inventar.", "Sin información de México."),
     O("b", "Investigar la normativa mexicana como insumo adicional", "Una nueva ronda de recopilación.", "Más completo.", "No hay garantía de que el producto la use; fuera de la fuente indicada.", True),
     O("c", "Asumir equivalencia con la política del PDF", "Misma regla para todo.", "Simple.", "Sin base.")],
    ["a"], "La fuente que indicaste no cubre México y el PDF no lo pide.",
    "Queda como pregunta abierta en REQ-D-07 (b, e).",
    refs("LEEME", "CRUCE"), orden=10))

# ───────────────────────────── F · PRESENTACIÓN Y USO DE IA ─────────────────────────────
DEC.append(D(
    "DEC-36", "F", "Idioma, tono y localización de mensajes", "INTERNA",
    "¿En qué idioma y con qué formato se redactan los mensajes al pasajero?",
    "El ejemplo tiene teléfono +56, tarifa en CLP y nombres en español; el PDF indica idioma es-CL en su metadata. No hay requisito de idioma en el texto.",
    {"src": ["SRC-01-14"], "req": ["REQ-F-03"], "gap": ["GAP-22"]},
    [O("a", "Español (es-CL) con plantillas y formato local", "Moneda CLP sin decimales; horas con zona o aeropuerto de referencia.", "Coherente con los datos.", "Un solo idioma."),
     O("b", "Multiidioma", "Plantillas por idioma.", "Más alcance.", "Fuera de v1."),
     O("c", "Español neutro sin localización", "Texto genérico.", "Simple.", "Menos preciso con moneda y horas.")],
    ["a"], "Es lo que sugieren los datos del ejemplo.",
    "Define la especificación del mensaje de REQ-F-03/REQ-F-09."))

DEC.append(D(
    "DEC-37", "F", "Uso de IA en este trabajo y confidencialidad del enunciado", "INTERNA",
    "¿Qué registras sobre el uso de IA y cómo tratas el PDF marcado «Uso interno»? (selección múltiple)",
    "El PDF permite usar IA libremente pero exige transparencia en el Entregable 3 (SRC-06-05, SRC-05-04) y está marcado «Uso interno» en todas sus páginas (SRC-00-01).",
    {"src": ["SRC-06-05", "SRC-05-04", "SRC-00-01"], "req": ["REQ-P-10", "REQ-P-12", "REQ-D-08", "REQ-N-10"]},
    [O("a", "Registrar el uso de IA para el Entregable 3", "Herramientas (p. ej. Claude Code y el método ESF), para qué se usaron, qué se aceptó, rechazó o modificó, cómo se validó, decisiones personales y qué nunca se envía a un modelo.", "Cumple SRC-05-04 y SRC-06-05.", "Requiere llevar el registro."),
     O("b", "No publicar los artefactos fuera de tu entorno", "Los documentos generados se mantienen locales; no se suben a servicios externos ni se comparten públicamente.", "Respeta la marca «Uso interno».", "—"),
     O("c", "Consultar a quien envió el desafío", "Confirmar si hay restricciones adicionales de confidencialidad.", "Certeza.", "Costo de coordinación; el PDF ya permite IA.")],
    ["a", "b"], "a es obligatoria; b es una precaución barata coherente con la marca de confidencialidad.",
    "Fija el contenido de REQ-D-08 y el tratamiento de REQ-P-12/REQ-N-10.", multiple=True))
