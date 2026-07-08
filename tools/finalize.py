# -*- coding: utf-8 -*-
"""
Pasos finales sobre index.html:
1. Extrae el <style> principal a css/style.css
2. Extrae el <script> principal (con el catálogo PRODUCTS) a js/main.js
3. Conecta el número real de WhatsApp
4. Agrega loading="lazy" a las imágenes fuera del hero
"""
import io
import os
import re

OUT_DIR = r"C:\Users\usuario\dos-casas"
WA_REAL = "573001234567"

path = os.path.join(OUT_DIR, "index.html")
html = io.open(path, encoding="utf-8").read()

# --- 1. CSS ---
m = re.search(r"<style[^>]*>(.*?)</style>", html, re.S)
css = m.group(1)
assert "assets/" not in css, "el CSS referencia assets extraídos; revisar rutas relativas"
io.open(os.path.join(OUT_DIR, "css", "style.css"), "w", encoding="utf-8").write(css)
html = html[:m.start()] + '<link rel="stylesheet" href="css/style.css">' + html[m.end():]
print("css/style.css:", len(css), "chars")

# --- 2. JS principal (el primer <script>, el que define WA y PRODUCTS) ---
m = re.search(r"<script>(.*?)</script>", html, re.S)
js = m.group(1)
assert "const WA=" in js and "PRODUCTS" in js, "el primer script no es el principal"
html = html[:m.start()] + '<script src="js/main.js"></script>' + html[m.end():]

# --- 3. WhatsApp (en main.js y en cualquier fallback que quede en el HTML) ---
n_js = js.count("57XXXXXXXXXX")
js = js.replace("57XXXXXXXXXX", WA_REAL)
n_html = html.count("57XXXXXXXXXX")
html = html.replace("57XXXXXXXXXX", WA_REAL)
io.open(os.path.join(OUT_DIR, "js", "main.js"), "w", encoding="utf-8").write(js)
print("js/main.js:", len(js), "chars | WA reemplazado:", n_js, "en JS,", n_html, "en HTML")

# --- 4. loading="lazy" en imágenes fuera del hero ---
# el único <img> antes del hero es el logo del header (brand-logo); el resto va lazy
count = 0
def add_lazy(m):
    global count
    tag = m.group(0)
    if "loading=" in tag or "brand-logo" in tag:
        return tag
    count += 1
    return tag[:-1] + ' loading="lazy">'

html = re.sub(r"<img\b[^>]*>", add_lazy, html)
print('loading="lazy" agregado a', count, "imágenes")

io.open(path, "w", encoding="utf-8").write(html)
print("index.html final:", os.path.getsize(path) / 1024, "KB")
