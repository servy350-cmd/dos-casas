# -*- coding: utf-8 -*-
"""
Extrae los assets base64 embebidos de gold-member.html a archivos reales
y reemplaza cada data URI por su ruta relativa.

Uso:  python tools/extract-assets.py
Genera: index.html + assets/video/* + assets/img/*
"""
import base64
import hashlib
import io
import os
import re

SRC = r"C:\Users\usuario\Downloads\gold-member.html"
OUT_DIR = r"C:\Users\usuario\dos-casas"
INLINE_MAX_BYTES = 5 * 1024  # imágenes < 5KB quedan inline

EXT = {
    "video/mp4": ".mp4",
    "image/webp": ".webp",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
}

# Nombre descriptivo por posición del data URI en el HTML original
# (posiciones detectadas en el escaneo previo; se validan por hash/dedupe)
NAMES_BY_POS = {
    36560: "logo",              # logo del header (se repite en footer y JS)
    63837: "hero-poster",       # poster del video del hero
    302011: "hero",             # video de fondo del hero
    2392023: "perfume-float",   # imagen flotante grande de la casa de perfumes
    2575567: "mushroom-float-1",
    2607743: "mushroom-float-2",
    2639415: "mushroom-float-3",
    2677051: "mushroom-float-4",
    2718304: "mushroom-float-5",
    2750724: "melena",
    2795934: "shiitake",
    2842997: "cordyceps",
    2898012: "reishi",
    2986360: "bottle",
    3435686: "mushroom-fall-1",
    3531923: "mushroom-fall-2",
    3539982: "mushroom-fall-3",
    3548961: "mushroom-fall-4",
}

html = io.open(SRC, encoding="utf-8").read()

pattern = re.compile(r"data:([\w/+.-]+);base64,([A-Za-z0-9+/=]+)")

by_hash = {}   # sha1 -> ruta relativa asignada
report = []
auto_idx = 0


def target_path(mime, name):
    ext = EXT.get(mime, ".bin")
    sub = "video" if mime.startswith("video/") else "img"
    return f"assets/{sub}/{name}{ext}"


def replace(m):
    global auto_idx
    mime, b64 = m.group(1), m.group(2)
    data = base64.b64decode(b64)
    if len(data) < INLINE_MAX_BYTES:
        return m.group(0)  # queda inline
    h = hashlib.sha1(data).hexdigest()
    if h not in by_hash:
        name = NAMES_BY_POS.get(m.start())
        if name is None:
            auto_idx += 1
            name = f"asset-{auto_idx}"
        rel = target_path(mime, name)
        abspath = os.path.join(OUT_DIR, rel.replace("/", os.sep))
        with open(abspath, "wb") as f:
            f.write(data)
        by_hash[h] = rel
        report.append((rel, len(data)))
    return by_hash[h]


new_html = pattern.sub(replace, html)

out_file = os.path.join(OUT_DIR, "index.html")
io.open(out_file, "w", encoding="utf-8").write(new_html)

print("Assets extraídos:")
for rel, size in sorted(report, key=lambda r: -r[1]):
    print(f"  {rel:40s} {size/1024:8.1f} KB")
print(f"\nindex.html: {os.path.getsize(out_file)/1024:.1f} KB (antes: {os.path.getsize(SRC)/1024:.1f} KB)")

# Verificación: no deben quedar data URIs pesados
heavy = [m for m in pattern.finditer(new_html) if len(m.group(2)) * 3 / 4 >= INLINE_MAX_BYTES]
print(f"Data URIs pesados restantes: {len(heavy)}")
