# -*- coding: utf-8 -*-
"""Reemplaza los 7 <script> inline de index.html por <script src>.
Extrae ritual-fall (base64 grande) verbatim; los demás ya fueron creados a mano."""
import io
import os

ROOT = r"C:\Users\usuario\dos-casas"
P = os.path.join(ROOT, "index.html")
html = io.open(P, encoding="utf-8").read()

# (marcador único dentro del bloque, archivo destino, ¿extraer contenido?)
BLOQUES = [
    ("FX · CAPA 3D", "js/fx.js", False),
    ("dc_cart_v1", "js/cart.js", False),
    ("getElementById('lightbox')", "js/lightbox.js", False),
    ("getElementById('skuTrack')", "js/carousel.js", False),
    ('getElementById("ritualFall")', "js/ritual-fall.js", True),
    ("/*heroVid*/", "js/hero-video.js", False),
    ("getElementById('natTabs')", "js/nat-grid.js", False),
]

for marcador, src, extraer in BLOQUES:
    idx = html.find(marcador)
    assert idx != -1, "no encontrado: " + marcador
    start = html.rfind("<script>", 0, idx)
    end = html.find("</script>", idx) + len("</script>")
    assert start != -1 and end > start, "bloque mal delimitado: " + marcador
    bloque = html[start:end]
    if extraer:
        inner = bloque[len("<script>"):-len("</script>")].strip("\n")
        dest = os.path.join(ROOT, src.replace("/", os.sep))
        io.open(dest, "w", encoding="utf-8").write(inner + "\n")
        print("extraído:", src, os.path.getsize(dest) // 1024, "KB")
    html = html[:start] + '<script src="' + src + '"></script>' + html[end:]
    print("reemplazado ->", src)

io.open(P, "w", encoding="utf-8").write(html)

# verificación: 0 <script> inline (solo <script src>)
import re
inline = re.findall(r"<script>(?!\s*</script>)", html)
print("\n<script> inline restantes:", len(inline))
print("index.html:", os.path.getsize(P) // 1024, "KB")
