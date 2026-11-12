# -*- coding: utf-8 -*-
"""Construye informe.html, incrusta anexos, renderiza PDF (2 pasadas para TOC)."""
import base64
import html as htmllib
import re
import sys
from pathlib import Path

BASE = Path(r"C:\Development\parcial_EnviaYa\EnviaYa_Parcial3\informe")
REPO = Path(r"C:\Development\parcial_EnviaYa\EnviaYa_Parcial3")

# ---------- 1. concat parts ----------
parts = []
for i in range(1, 11):
    parts.append((BASE / f"part{i}.html").read_text(encoding="utf-8"))
doc = "".join(parts)

env_src = (REPO / "envios.py").read_text(encoding="utf-8")
cl_src = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
doc = doc.replace("@@ANEXO_A@@", htmllib.escape(env_src))
doc = doc.replace("@@ANEXO_B@@", htmllib.escape(cl_src))

# inyectar marcadores invisibles unicos en los h1 con id (para localizar paginas sin ambiguedad)
def inject_marker(m):
    hid = m.group(1)
    return m.group(0).replace("</h1>", f'<span style="font-size:1px; color:#ffffff;">§MARK_{hid}§</span></h1>')
doc = re.sub(r'<h1 id="([A-Za-z0-9_]+)".*?</h1>', inject_marker, doc, flags=re.S)
(BASE / "informe.html").write_text(doc, encoding="utf-8")
print("informe.html:", len(doc), "chars")

# ---------- 2. header/footer templates ----------
def data_uri(p):
    return "data:image/png;base64," + base64.b64encode(Path(p).read_bytes()).decode()

logo = data_uri(BASE / "assets" / "image1.png")
orn = data_uri(BASE / "assets" / "image3.png")

header_tmpl = f"""<div style="width:100%; position:relative; height:100%; font-family:'Times New Roman'; font-size:8px; color:#647484;">
<img src="{logo}" style="position:absolute; left:0.82in; top:1px; height:0.34in;">
<div style="position:absolute; right:0.82in; top:0.09in; font-weight:bold; white-space:nowrap;">UNIVERSIDAD DE LA GUAJIRA&nbsp;&nbsp;|&nbsp;&nbsp;INGENIERÍA DE SISTEMAS&nbsp;&nbsp;|&nbsp;&nbsp;INGENIERÍA DE SOFTWARE I</div>
</div>"""

footer_tmpl = f"""<div style="width:100%; position:relative; height:100%; font-family:'Times New Roman'; font-size:8px; color:#647484;">
<div style="position:absolute; left:0; right:0; text-align:center; top:0.09in;">Informe Parcial 3 — EnvíaYa&nbsp;&nbsp;•&nbsp;&nbsp;<span class="pageNumber"></span> de <span class="totalPages"></span></div>
<img src="{orn}" style="position:absolute; right:0.82in; top:0.02in; height:0.34in;">
</div>"""

page_args = dict(
    format="Letter",
    print_background=True,
    display_header_footer=True,
    header_template=header_tmpl,
    footer_template=footer_tmpl,
    margin={"top": "0.72in", "bottom": "0.72in", "left": "0.82in", "right": "0.82in"},
)

from playwright.sync_api import sync_playwright

def render(out_name):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto(BASE.joinpath("informe.html").as_uri(), wait_until="networkidle")
        page.pdf(path=str(BASE / out_name), **page_args)
        browser.close()

render("informe_pass1.pdf")

# ---------- 3. find anchor pages ----------
import pymupdf
anchors = {k: "§MARK_%s§" % k for k in [
    "misparametros", "sec1", "sec2", "sec3", "sec4", "sec5", "sec6", "sec7",
    "sec8", "conclusiones", "referencias", "anexoA", "anexoB",
]}
pdf = pymupdf.open(str(BASE / "informe_pass1.pdf"))
found = {}
for i, page in enumerate(pdf, start=1):
    text = page.get_text()
    for key, needle in anchors.items():
        if key not in found and needle in text:
            found[key] = i
missing = set(anchors) - set(found)
print("páginas:", {k: found[k] for k in sorted(found, key=found.get)})
print("faltantes:", missing or "ninguno")

# ---------- 4. patch TOC and re-render ----------
html = (BASE / "informe.html").read_text(encoding="utf-8")
for key, page_no in found.items():
    html = re.sub(
        r'(<span class="pg" data-ref="%s">)[^<]*(</span>)' % re.escape(key),
        r"\g<1>%d\g<2>" % page_no,
        html,
    )
(BASE / "informe.html").write_text(html, encoding="utf-8")
render("Informe_Parcial3_EnviaYa.pdf")

pdf = pymupdf.open(str(BASE / "Informe_Parcial3_EnviaYa.pdf"))
print("PDF final:", pdf.page_count, "páginas")
