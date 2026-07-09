# -*- coding: utf-8 -*-
"""Genera favicon.ico (multi-tamaño) y favicon.png (180x180 Apple) desde el logo de la gota."""
from PIL import Image
import os

ROOT = r"C:\Users\usuario\dos-casas"
logo = Image.open(os.path.join(ROOT, "assets", "img", "logo.webp")).convert("RGBA")
print("logo original:", logo.size)

# recorte al contenido no transparente para que la gota llene el icono
bbox = logo.getbbox()
crop = logo.crop(bbox) if bbox else logo
w, h = crop.size
lado = max(w, h)
pad = int(lado * 0.12)
canvas = Image.new("RGBA", (lado + pad * 2, lado + pad * 2), (0, 0, 0, 0))
canvas.paste(crop, ((canvas.width - w) // 2, (canvas.height - h) // 2), crop)

BG = (22, 29, 23, 255)  # --forest-deep del sitio

# favicon.png 180x180 (Apple touch icon)
apple = Image.new("RGBA", (180, 180), BG)
ic = canvas.resize((156, 156), Image.LANCZOS)
apple.paste(ic, (12, 12), ic)
apple.convert("RGB").save(os.path.join(ROOT, "favicon.png"), "PNG")
print("favicon.png 180x180 OK")

# favicon.ico multi-tamaño
icob = Image.new("RGBA", (256, 256), BG)
ici = canvas.resize((224, 224), Image.LANCZOS)
icob.paste(ici, (16, 16), ici)
icob.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("favicon.ico OK:", os.path.getsize(os.path.join(ROOT, "favicon.ico")), "bytes")
