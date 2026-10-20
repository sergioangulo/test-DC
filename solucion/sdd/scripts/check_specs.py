# -*- coding: utf-8 -*-
"""Chequeo de los specs funcionales del paso A2 del flujo SDD.

Comprueba, sobre sdd/specs/functional/*.md, docs/REQUERIMIENTOS_V1.md y sdd/reports/*.md:
 1. cobertura de cada FR/NFR/DOC en al menos un spec;
 2. cobertura de cada TC: figura en la cabecera de un spec Y hay un escenario que lo nombra;
 3. formato: secciones de la plantilla, FR-XXX, cero placeholders, entidades como {campo: tipo};
 4. cada escenario tiene Given, When y Then;
 5. cada spec tiene al menos un escenario con valores concretos del caso base o de su variante TC;
 6. los 26 specs de front incluyen FR-VIS-001/002/003;
 7. correspondencia 1 a 1 con el inventario de flujos (F-xx, SF-xx.x, FE-xx, FE-xx.x) y solo X-xx como extras;
 8. todos los FR/NFR/DOC/TC citados existen en REQUERIMIENTOS_V1;
 9. patrones prohibidos (tecnologías y rutas de código), sin distinguir mayúsculas. «sync-http» y los demás valores
    de la tabla de atributos arquitectónicos son valores de la plantilla de spec del workflow y no se revisan;
10. unicidad: sin escenarios, bordes, requisitos o criterios duplicados dentro de un spec, ni líneas
    consecutivas repetidas, ni filas duplicadas en las tablas del RFC.
Con --write-report regenera sdd/reports/FR_COVERAGE.md.
Uso: python -I sdd/scripts/check_specs.py [--write-report]
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SPECS = os.path.join(ROOT, "sdd", "specs", "functional")
REQ = os.path.join(ROOT, "docs", "REQUERIMIENTOS_V1.md")
INVENTORY = os.path.join(ROOT, "sdd", "reports", "FLOW_INVENTORY.md")
RFC = os.path.join(ROOT, "sdd", "reports", "RFC_DESIGN.md")
REPORT = os.path.join(ROOT, "sdd", "reports", "FR_COVERAGE.md")

SECTIONS = ["## User Scenarios & Testing", "### Edge Cases", "## Requirements", "### Functional Requirements",
            "### Key Entities", "## Architectural Attributes", "## Success Criteria", "## Traceability",
            "## Business Process (BPM View)", "```mermaid"]
BANNED = [r"FastAPI", r"SQLite", r"\bReact\b", r"\bVite\b", r"HMAC", r"SHA-?256", r"\bJSON\b", r"\bHTTP\b", r"endpoint",
          r"Python", r"pytest", r"UUID", r"\bCORS\b", r"Docker", r"\bnpm\b", r"TypeScript", r"Vitest", r"pydantic",
          r"\.py\b", r"\.tsx?\b", r"\bmock", r"get_trip_context", r"get_operational_events", r"get_policy_rules",
          r"get_eligible_options", r"create_rebooking_request", r"create_human_case", r"notify_passenger", r"\bAPI\b",
          r"\bhash\b", r"\bPOST\b", r"\bGET\b", r"\bPUT\b", r"\bSQL\b", r"\bsrc/", r"\bclass\b", r"\bdef\b"]
PLACEHOLDERS = [r"\bTBD\b", r"N/A", r"To be completed", r"\[NEEDS CLARIFICATION", r"\[DATE\]", r"\[Brief", r"\[Describe"]
# Valores concretos FUERTES: datos del caso base del enunciado (reserva ABC123, vuelos y horas, eventos, reglas, opciones, referencias,
# marcas de tiempo de lectura), cifras de sus variantes TC, identificadores de escenario o valores de parámetros de configuración.
# Un número suelto no cuenta.
CONCRETE = re.compile(
    r"ABC123|XYZ789|ZZZ999|E-\d{4}|\bR[1-5]\b|\bO[1-3]\b|\bP[12]\b|\bS[12]\b|LA\d{3,4}|\b11:0[0-4]:\d\dZ|\b10:[45]\d:00Z|"
    r"\bPOL-[A-Z]+-\d{4}|RBK-\d+|HC-\d+|NT-\d+|DISRUPTION_L2|"
    r"\b(?:14:30|17:55|19:05|23:40|20:35|17:10|08:15|10:48|10:55|11:02|11:04|11:12|01:30)\b|[−-]90 min|"
    r"\b(?:5|10|60|100|120|160|170|179|180|200|239|240) min\b|\b(?:0|1|4) asientos?\b|[Pp]uerta (?:24|25)\b|\b180\.000 CLP|"
    r"\b(?:119|120|121|299|300|899|900|2000|5000|50) (?:s|ms)\b|\b(?:200 ms|400 ms)\b|\b(?:29|30|31|40) días\b|"
    r"[A-Z]+_TC\d{2}|\bBASE_TC01|`[A-Z][A-Z0-9_]{5,}` (?:en|de|=|con|es) \d+|\bDOC-0\d\d\b|"
    r"\b(?:3|5|10) (?:filas|llamadas|reintentos|situaciones|escenarios|segmentos)\b|\b\d+ de 10\b|intento [12]\b|\b13 entregables\b|\b7 proveedores\b|\b31\.º\b")
# Dato característico de cada TC: un escenario etiquetado con ese TC debe usarlo (texto del escenario, sin distinguir mayúsculas).
TC_KEYWORDS = {
 "TC-01": r"160 min|BASE_TC01|caso base", "TC-02": r"E-1012.*(?:degradad|solo)|solo evidencia degradada|solo E-1012|SOLO_DEGRADADO",
 "TC-03": r"mismo instante|empate|conflicto", "TC-04": r"\b179\b|\b180 min", "TC-05": r"\b239\b|\b240 min",
 "TC-06": r"margen (?:de )?(?:10|60) min|60 min|10 min", "TC-07": r"sin menor|dos pasajeros adultos|dos adultos|R5 falsa",
 "TC-08": r"venc|refresc|120 s", "TC-09": r"solo O2|sin opción viable|no cubre|1 asiento|ninguna opción", "TC-10": r"superseded|superada|2025-11",
 "TC-11": r"O3|POL-REFUND", "TC-12": r"penalidad|PARCIAL|parcial|instante de lectura", "TC-13": r"CANCELLATION|cancelaci",
 "TC-14": r"indeterminad|reintentos|falla persistente|3 llamadas|503", "TC-15": r"duplicado|ya existe|RBK-88231", "TC-16": r"referencia de política|conexión está segura|policy_ref|POL-DELAY",
 "TC-17": r"compensaci", "TC-18": r"medianoche|23:30|día siguiente", "TC-19": r"OPS_CORE", "TC-20": r"datos personales|datos o documentos|PERSONAL_DATA|sin ningún dato personal|ningún dato",
 "TC-21": r"XYZ789|ajena", "TC-22": r"simult|doble clic|dos clics|concurren|2 solicitudes|2 veces", "TC-23": r"varios segmentos|S1 y S2|sin tipo|menor desconocido|desconocido",
 "TC-24": r"horario programado|programado|ON_TIME|SCHEDULED|más reciente|posterior", "TC-25": r"100 min|compatibles", "TC-26": r"S9|segmento desconocido|marca futura|incoherente|inválid",
 "TC-27": r"119 s|120 s|sin vigencia|ttl|vigencia|11:04", "TC-28": r"pernocte|día siguiente|16 sep", "TC-29": r"sin moneda|moneda", "TC-30": r"pendiente de confirmación|RBK-88231|solicitud",
 "TC-31": r"huella|asientos|cupos", "TC-32": r"29|31 días|30 días|retención|corte", "TC-33": r"falla|error|no responde|tiempo agotado|indeterminad|reintent|timeout",
 "TC-34": r"llave|POL-DELAY-2026-04|generación", "TC-35": r"último segmento|política vacía|0 reglas|200 min|sin conexión", "TC-36": r"posterior|E-1012",
 "TC-37": r"destino distinto|origen distinto|itinerario|anterior a", "TC-38": r"121 s|colgad|en curso|expirad|vencid", "TC-39": r"cadena|desordenad|menor sin adulto|≤ 0|no positivo|instante de lectura|cero segmentos",
 "TC-40": r"pasajeros|P1 y P2|cubr|contenido de la opción", "TC-41": r"\bEQ\b|\bNE\b|201 caracteres|anidación|parser|condición", "TC-42": r"una notificación|NT-9912|aviso de política|política rota|2 avisos",
 "TC-43": r"BLOQUEADA|sin política rota|revisión manual", "TC-44": r"enfriamiento|deduplic|cooldown|reintentos|indeterminad|fuera de orden|en cola|no se repite|se repite",
 "TC-45": r"INFORMATIVA|5 min|informativ", "TC-46": r"compensaci|SIN_COMPENSACION|menú", "TC-47": r"INFANT|sin tipo|sin campo de tipo|tipo desconocido|menor desconocido|sin regla R5",
 "TC-48": r"enlace|www|dominio|teléfono|correo|URL", "TC-49": r"`[A-Z][A-Z0-9_]{5,}`|parámetro", "TC-50": r"clave|credencial",
 "TC-51": r"puerta 24|solo cambio de puerta|GATE_SOLO|solo E-1007|E-1007", "TC-52": r"2 notificaciones|dos motivos|retraso.*puerta|puerta.*retraso|2 avisos|dos avisos|hasta 2",
 "TC-53": r"política vacía|0 reglas|nunca consulta|POLICY_SCENARIOS|no se consulta", "TC-54": r"sin eventos|NO_EVENTS|horario programado", "TC-55": r"puerta 25|24 a 25|misma puerta|puerta 24 repetida",
 "TC-56": r"minimiz|vigente|retención|31 días|40 días", "TC-57": r"900|indeterminad", "TC-58": r"429|límite de tasa|HTML|texto plano|31\.º",
 "TC-59": r"campos internos|revisión manual|notificaciones", "TC-60": r"titular adulto|AVISO_TITULAR|NO_ADULT|solo minutos|170 min|conexión desconocida|desconocida|cambian los minutos|cambian solo los minutos"}


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def spec_id(text):
    return re.match(r"# Feature Specification: (\S+)", text).group(1)


def scenarios(text):
    return re.findall(r"^\d+\. \*\*Scenario\*\*: (.*)\n   - \*\*Given\*\* (.*)\n   - \*\*When\*\* (.*)\n   - \*\*Then\*\* (.*)$", text, re.M)


def dup(items):
    seen, out = set(), []
    for it in items:
        if it in seen:
            out.append(it)
        seen.add(it)
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    req = read(REQ)
    ids = {p: sorted(set(re.findall(r"\*\*(%s-\d+)\*\*" % p, req))) for p in ("FR", "NFR", "DOC")}
    all_ids = set(sum(ids.values(), []))
    tcs = sorted(set(re.findall(r"TC-\d+", req.split("## 6.")[1].split("## 7.")[0])))
    inv = read(INVENTORY)
    inv_ids = set(re.findall(r"\b(F-\d\d|SF-\d\d\.\d+|FE-\d\d\.\d+|FE-\d\d)\b", inv))
    cover, tc_head, tc_named, problems, spec_ids = {}, {}, {}, [], []
    files = sorted(glob.glob(os.path.join(SPECS, "*.md")))
    for path in files:
        text, name = read(path), os.path.basename(path)
        sid = spec_id(text)
        spec_ids.append(sid)
        for sec in SECTIONS:
            if sec not in text:
                problems.append("%s: falta %s" % (name, sec))
        scan = re.sub(r"## Architectural Attributes.*?## Success Criteria", "## Success Criteria", text, flags=re.S)
        scan = re.sub(r"`[A-Z][A-Z0-9_]{3,}`", "", scan)  # nombres de parámetros y constantes de enumeración
        for pat in BANNED:
            m = re.search(pat, scan, re.I)
            if m:
                problems.append("%s: tecnología o ruta prohibida (%s)" % (name, m.group(0)))
        for pat in PLACEHOLDERS:
            if re.search(pat, text):
                problems.append("%s: placeholder (%s)" % (name, pat))
        if not re.search(r"^- \*\*FR-", text, re.M):
            problems.append("%s: sin requisitos FR-XXX" % name)
        if re.search(r"\bBR-\d|\bREQ-F", text):
            problems.append("%s: usa BR-/REQ- como requisito" % name)
        for block in re.findall(r"Campos principales:\n((?:  - .*\n?)+)", text):
            for line in block.rstrip().split("\n"):
                if not re.match(r"  - `[^`]+`: .+", line):
                    problems.append("%s: campo de entidad mal formado: %s" % (name, line))
        # escenarios: Given/When/Then, valores concretos, TC nombrados
        n_sc = len(re.findall(r"\*\*Scenario\*\*", text))
        sc = scenarios(text)
        if n_sc != len(sc) or n_sc == 0:
            problems.append("%s: hay %d escenarios y %d con Given/When/Then completos" % (name, n_sc, len(sc)))
        if not any(CONCRETE.search(re.sub(r"TC-\d+", "", " ".join(s))) for s in sc):
            problems.append("%s: ningún escenario usa valores concretos del caso base o de su variante TC" % name)
        for s in sc:
            for tc in re.findall(r"TC-\d+", s[0]):
                full = " ".join(s)
                if tc in TC_KEYWORDS and not re.search(TC_KEYWORDS[tc], full, re.I):
                    problems.append("%s: el escenario «%s» etiqueta %s pero no usa su dato característico" % (name, s[0][:60], tc))
                else:
                    tc_named.setdefault(tc, set()).add(sid)
        # FR-VIS en front
        if sid.startswith("FE-"):
            for v in ("FR-VIS-001", "FR-VIS-002", "FR-VIS-003"):
                if not re.search(r"^- \*\*%s\*\*:" % v, text, re.M):
                    problems.append("%s: falta %s" % (name, v))
        # IDs citados existen
        for cid in set(re.findall(r"\b((?:FR|NFR|DOC)-\d+)\b", text)):
            if cid not in all_ids:
                problems.append("%s: cita %s, que no existe en REQUERIMIENTOS_V1" % (name, cid))
        for tid in set(re.findall(r"\b(TC-\d+)\b", text)):
            if tid not in tcs:
                problems.append("%s: cita %s, que no existe en REQUERIMIENTOS_V1" % (name, tid))
        # unicidad
        for label, items in (("escenario", [s[0] for s in sc]), ("escenario (Given/When/Then)", [s[1:] for s in sc]),
                             ("borde", re.findall(r"^- \[(?:MUST-IMPLEMENT|DEFERRED)\] (.*)$", text, re.M)),
                             ("requisito", re.findall(r"^- \*\*((?:FR|NFR|DOC)-[\w-]+)\*\*:", text, re.M)),
                             ("criterio de éxito", re.findall(r"^- \*\*SC-\d+\*\*: (.*)$", text, re.M)),
                             ("entidad", re.findall(r"^- \*\*([^*]+)\*\*: .* Campos principales:$", text, re.M))):
            for d in dup(items):
                problems.append("%s: %s duplicado: %s" % (name, label, str(d)[:90]))
        prev = None
        for line in text.split("\n"):
            if line.strip() and line == prev and not line.strip().startswith(("```", "---", "|", "- **Given", "   - **")):
                problems.append("%s: línea consecutiva repetida: %s" % (name, line[:80]))
            prev = line
        body = text.split("## Requirements")[1].split("### Key Entities")[0]
        for rid in re.findall(r"^- \*\*((?:FR|NFR|DOC)-\d+)\*\*:", body, re.M):
            cover.setdefault(rid, []).append(sid)
        for tc in re.findall(r"TC-\d+", text.split("## Reglas")[0]):
            tc_head.setdefault(tc, set()).add(sid)
    # parámetros de configuración (EXTERNAL_CONTRACTS §2.4): cada uno se cubre por nombre en F-12 o en sus subflujos
    ec = read(os.path.join(ROOT, "sdd", "reports", "EXTERNAL_CONTRACTS.md"))
    sec = ec.split("### 2.4 Configuraci")[1].split("## 3.")[0]
    params = sorted(set(re.findall(r"^\| `([A-Z][A-Z0-9_]+)`", sec, re.M)))
    f12 = ""
    for path in files:
        t = read(path)
        if spec_id(t) == "F-12" or spec_id(t).startswith("SF-12."):
            f12 += t
    for prm in params:
        if prm not in f12:
            problems.append("configuración: el parámetro %s no se cubre por nombre en F-12 ni en SF-12.x" % prm)
    # inventario
    for i in sorted(inv_ids - set(spec_ids)):
        problems.append("inventario: %s no tiene spec" % i)
    for i in sorted(set(spec_ids) - inv_ids):
        if not i.startswith("X-"):
            problems.append("spec %s no figura en el inventario de flujos" % i)
    for d in dup(spec_ids):
        problems.append("spec duplicado: %s" % d)
    # RFC: filas duplicadas por tabla
    rfc = read(RFC)
    table, tname = [], None
    for line in rfc.split("\n") + [""]:
        if line.startswith("|"):
            table.append(line)
        else:
            for d in dup([r for r in table if not re.match(r"^\|[-| ]+\|$", r)]):
                problems.append("RFC: fila de tabla duplicada: %s" % d[:90])
            table = []
    missing = {p: [i for i in ids[p] if i not in cover] for p in ids}
    missing_tc = [t for t in tcs if t not in tc_head]
    unnamed_tc = [t for t in tcs if t not in tc_named]
    print("specs revisados:", len(files))
    for p in ids:
        print("%s: %d requisitos, sin cubrir: %s" % (p, len(ids[p]), missing[p] or "ninguno"))
    print("TC: %d casos; sin spec en cabecera: %s; sin escenario que lo nombre: %s" % (len(tcs), missing_tc or "ninguno", unnamed_tc or "ninguno"))
    print("problemas:", len(problems))
    for item in problems:
        print(" -", item)
    if "--write-report" in sys.argv:
        write_report(ids, cover, tcs, tc_head, tc_named, len(files))
    ok = not (any(missing.values()) or missing_tc or unnamed_tc or problems)
    print("RESULTADO:", "OK" if ok else "FALLA")
    return 0 if ok else 1


def order(spec_ids):
    def key(s):
        m = re.match(r"([A-Z]+)-(\d+)(?:\.(\d+))?", s)
        return (m.group(1), int(m.group(2)), int(m.group(3) or 0))
    return sorted(set(spec_ids), key=key)


def write_report(ids, cover, tcs, tc_head, tc_named, n):
    out = ["# Cobertura de requisitos por spec funcional (A2)", "",
           "**Paso SDD:** A2 · **Fuente:** `docs/REQUERIMIENTOS_V1.md` · **Specs:** `sdd/specs/functional/` (%d archivos) · "
           "**Generado por:** `python -I sdd/scripts/check_specs.py --write-report`." % n, "",
           "Resultado del chequeo: **%d FR, %d NFR y %d DOC, todos cubiertos por al menos un spec; %d TC, todos listados en la cabecera de un spec y nombrados por al menos un escenario.** "
           "La numeración de FR tiene huecos (hay %d identificadores entre FR-001 y FR-124; FR-073 y FR-104 pasaron a DOC-012 y DOC-013; ver A2_OPEN_QUESTIONS.md)." % (
               len(ids["FR"]), len(ids["NFR"]), len(ids["DOC"]), len(tcs), len(ids["FR"])), "",
           "Lectura: «Primer spec (orden)» es el primero de la lista según el orden de los flujos (F-01, SF-01.1, …); **no** indica cuál es el spec principal del requisito. "
           "«Todos los specs» lista cada spec que lo declara. Los IDs son los del FLOW_INVENTORY (F-xx, SF-xx.x, FE-xx, FE-xx.x); X-01 y X-02 son specs de apoyo "
           "para los requisitos transversales y los entregables DOC.", ""]
    for title, prefix in (("Requisitos funcionales (FR)", "FR"), ("Requisitos no funcionales (NFR)", "NFR"), ("Documentación (DOC)", "DOC")):
        out += ["## " + title, "", "| Requisito | Primer spec (orden) | Todos los specs |", "|---|---|---|"]
        for rid in ids[prefix]:
            specs = order(cover[rid])
            out.append("| %s | %s | %s |" % (rid, specs[0], ", ".join(specs)))
        out.append("")
    out += ["## Casos de prueba (TC)", "", "| TC | Specs que lo listan en la cabecera | Specs con un escenario que lo nombra |", "|---|---|---|"]
    for tc in tcs:
        out.append("| %s | %s | %s |" % (tc, ", ".join(order(tc_head[tc])), ", ".join(order(tc_named[tc])) if tc in tc_named else "ninguno"))
    out.append("")
    with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
