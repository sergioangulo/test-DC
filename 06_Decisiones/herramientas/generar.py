# -*- coding: utf-8 -*-
"""
Genera, a partir de decisiones_data.py y de los documentos del proyecto:
  - ../decisiones.json
  - ../DECISIONES_CATALOGO.md
  - ../FORMULARIO_DECISIONES.html
y valida que cada ID citado (REQ, GAP, AMB, DAT, SRC, POL) exista de verdad.

Uso:  python generar.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from decisiones_data import DEC, GRUPOS, POLREF  # noqa: E402

VERSION = "1.0"


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


def cells(line):
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return parts


def strip_md(s):
    return re.sub(r"[*`]", "", s).strip()


req_md = read("03_Requerimientos", "REQUERIMIENTOS.md")
dic = {"req": {}, "gap": {}, "amb": {}, "dat": {}, "src": {}, "pol": {}}

for line in req_md.splitlines():
    m = re.match(r"^\| \*\*(REQ-([A-Z])-\d+)\*\*", line)
    if m:
        c = cells(line)
        rid, fam = m.group(1), m.group(2)
        if fam == "C" and len(c) >= 5:
            dic["req"][rid] = "Contrato de %s%s — %s" % (strip_md(c[1]), strip_md(c[2]), strip_md(c[4]))
        elif fam == "E" and len(c) >= 2:
            dic["req"][rid] = strip_md(c[1])
        else:
            dic["req"][rid] = strip_md(c[1])
        continue
    m = re.match(r"^\| \*\*(GAP-\d+)\*\*", line)
    if m:
        dic["gap"][m.group(1)] = strip_md(cells(line)[1])
        continue
    m = re.match(r"^\| \*\*(AMB-\d+)\*\*", line)
    if m:
        dic["amb"][m.group(1)] = strip_md(cells(line)[1])

dat_md = read("04_Analisis_de_Datos", "00_LEEME_Analisis_de_Datos.md")
for line in dat_md.splitlines():
    m = re.match(r"^\| `(DAT-\d+)` \| (\S+) \| (.+?) \| `", line)
    if m:
        dic["dat"][m.group(1)] = "[%s] %s" % (m.group(2), strip_md(m.group(3)))

src_md = read("01_Fuente_y_Trazabilidad", "01_Indice_de_fuente_SRC.md")
for line in src_md.splitlines():
    m = re.match(r"^\| \*{0,2}(SRC-\d\d-\d\d)\*{0,2} \| (.+?) \| (.+) \|$", line)
    if m:
        t = m.group(3).strip()
        dic["src"][m.group(1)] = (t[:200] + "…") if len(t) > 200 else t

for k, (arch, res) in POLREF.items():
    dic["pol"][k] = res

# Normalizar claves de "gap"/"req"/"dat"/"src"/"amb"/"pol" en las decisiones para los chips
problemas = []
pol_texts = ""
polroot = os.path.join(ROOT, "05_Politicas_Externas")
for fn in os.listdir(polroot):
    if fn.endswith(".md"):
        with open(os.path.join(polroot, fn), encoding="utf-8") as f:
            pol_texts += f.read()

for d in DEC:
    z = d["traz"]
    for kind in ("req", "gap", "amb", "dat", "src"):
        for i in z[kind]:
            if i not in dic[kind]:
                problemas.append("%s: %s %s no existe" % (d["id"], kind.upper(), i))
    for i in z["pol"]:
        if i not in POLREF:
            problemas.append("%s: POL %s no está en POLREF" % (d["id"], i))
        if not re.search(re.escape(i) + r"\b", pol_texts) and not i.startswith(("MATRIZ", "CRUCE", "LEEME")):
            problemas.append("%s: %s no aparece en 05_Politicas_Externas/*.md" % (d["id"], i))
    for r in d["referencias"]:
        e = r["etiqueta"]
        if e.startswith("POL-") and not re.search(re.escape(e) + r"\b", pol_texts):
            problemas.append("%s: referencia %s no aparece en 05_Politicas_Externas/*.md" % (d["id"], e))
        if not os.path.exists(os.path.join(ROOT, r["archivo"])):
            problemas.append("%s: archivo %s no existe" % (d["id"], r["archivo"]))
    ids = {o["id"] for o in d["opciones"]}
    for x in d["rec"]:
        if x not in ids:
            problemas.append("%s: recomendación %s no es una opción" % (d["id"], x))
    if d["tipo"] == "EXTERNA" and not d["referencias"]:
        problemas.append("%s: EXTERNA sin referencias" % d["id"])

if problemas:
    print("PROBLEMAS DE VALIDACIÓN:")
    for p in problemas:
        print(" -", p)
else:
    print("Validación OK: todas las referencias existen.")

data = {"version": VERSION, "grupos": GRUPOS, "decisiones": DEC, "dic": {k: dic[k] for k in ("req", "gap", "amb", "dat", "src", "pol")}}

with open(os.path.join(OUT, "decisiones.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

# ───────────── Catálogo legible ─────────────
Dsorted = sorted(DEC, key=lambda d: (d["grupo"], d["orden"]))
L = []
L.append("# 06 · Catálogo de decisiones")
L.append("")
L.append("> **Es la versión legible del formulario** (`FORMULARIO_DECISIONES.html`). Las decisiones **EXTERNAS** usan información que no está en el PDF y requieren tu **revisión estricta**. Ninguna está tomada: lo que ves como *recomendación* es solo mi propuesta razonada.")
L.append("> Total: **%d decisiones** (%d externas, %d internas)." % (len(DEC), sum(1 for d in DEC if d["tipo"] == "EXTERNA"), sum(1 for d in DEC if d["tipo"] != "EXTERNA")))
L.append("")
L.append("## Índice")
L.append("")
L.append("| ID | Grupo | Decisión | Tipo | Recomendación |")
L.append("|---|---|---|---|---|")
for d in Dsorted:
    L.append("| %s | %s | %s | %s | %s |" % (d["id"], d["grupo"], d["titulo"], "**EXTERNA**" if d["tipo"] == "EXTERNA" else "Interna", ", ".join(d["rec"])))
L.append("")
g = None
for d in Dsorted:
    if d["grupo"] != g:
        g = d["grupo"]
        L.append("---")
        L.append("")
        L.append("## " + GRUPOS[g])
        L.append("")
    L.append("### %s · %s%s" % (d["id"], d["titulo"], "  —  EXTERNA (revisión estricta)" if d["tipo"] == "EXTERNA" else ""))
    L.append("")
    L.append("**Pregunta:** " + d["pregunta"])
    L.append("")
    L.append("**Contexto:** " + d["contexto"])
    L.append("")
    T = []
    for k in ("src", "req", "amb", "gap", "dat", "pol"):
        if d["traz"][k]:
            T.append("%s: %s" % (k.upper(), ", ".join("`%s`" % i for i in d["traz"][k])))
    if T:
        L.append("**Trazabilidad:** " + " · ".join(T))
        L.append("")
    if d["referencias"]:
        L.append("**Información externa para tu revisión:**")
        L.append("")
        for r in d["referencias"]:
            L.append("- `%s` → `%s` — %s" % (r["etiqueta"], r["archivo"], r["resumen"]))
        L.append("")
    L.append("**Opciones:**")
    L.append("")
    for o in d["opciones"]:
        star = " ★ *recomendada*" if o["id"] in d["rec"] else ""
        ext = " · *usa información externa*" if o["externas"] else ""
        L.append("- **%s) %s**%s%s — %s" % (o["id"], o["titulo"], star, ext, o["detalle"]))
        L.append("  - A favor: %s" % o["pros"])
        L.append("  - En contra: %s" % o["contras"])
    L.append("")
    L.append("**Recomendación:** %s — %s" % (", ".join(d["rec"]), d["razon"]))
    L.append("")
    L.append("**Efecto en los requerimientos:** " + d["efecto"])
    L.append("")
with open(os.path.join(OUT, "DECISIONES_CATALOGO.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

# ───────────── Formulario HTML ─────────────
with open(os.path.join(HERE, "plantilla_formulario.html"), encoding="utf-8") as f:
    tpl = f.read()
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = tpl.replace("__DATA_JSON__", payload)
with open(os.path.join(OUT, "FORMULARIO_DECISIONES.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Generados: decisiones.json, DECISIONES_CATALOGO.md, FORMULARIO_DECISIONES.html (%d decisiones)" % len(DEC))
