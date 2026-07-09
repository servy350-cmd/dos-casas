# -*- coding: utf-8 -*-
"""Descarga todas las fotos del catalogo de perfumes (CDN de Shopify de
Perfumes Imperial) a assets/img/perfumes/ y reescribe js/main.js para que
PRODUCTS apunte a las copias locales.

Uso:  python tools/descargar-imagenes.py
Idempotente: si la foto ya existe en disco no la vuelve a bajar.
"""
import io
import json
import os
import re
import sys
import unicodedata
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "js", "main.js")
DEST = os.path.join(ROOT, "assets", "img", "perfumes")
WIDTH = 900  # ancho pedido al CDN (tarjeta + lightbox se ven nitidos)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

os.makedirs(DEST, exist_ok=True)

src = io.open(MAIN, encoding="utf-8").read()
m = re.search(r"const PRODUCTS=(\[.*?\]);", src, re.S)
if not m:
    sys.exit("No encontre const PRODUCTS=[...] en js/main.js")
products = json.loads(m.group(1))
print(f"{len(products)} productos en el catalogo")


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t or "producto"


def nombre_archivo(p, usados):
    base = slug((p.get("u") or "").rstrip("/").split("/")[-1] or p.get("n", ""))
    ext = os.path.splitext((p["i"].split("?")[0]))[1].lower() or ".webp"
    if ext not in (".webp", ".jpg", ".jpeg", ".png", ".gif", ".avif"):
        ext = ".webp"
    nombre, k = base + ext, 2
    while nombre in usados:
        nombre, k = f"{base}-{k}{ext}", k + 1
    usados.add(nombre)
    return nombre


def bajar(url, destino):
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        return "ya estaba"
    sep = "&" if "?" in url else "?"
    for intento_url in (f"{url}{sep}width={WIDTH}", url):
        try:
            req = urllib.request.Request(intento_url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                datos = r.read()
            if not datos:
                continue
            with open(destino, "wb") as f:
                f.write(datos)
            return "ok"
        except Exception as e:  # noqa: BLE001 - reintenta sin width y reporta
            ultimo = e
    return f"ERROR {ultimo}"


# --- plan de descarga (cachea URLs repetidas) ---
usados, por_url, tareas = set(), {}, []
con_foto = [p for p in products if p.get("i", "").startswith("http")]
for p in con_foto:
    url = p["i"]
    if url in por_url:
        continue
    por_url[url] = nombre_archivo(p, usados)
    tareas.append(url)
print(f"{len(con_foto)} productos con foto, {len(tareas)} URLs unicas")

errores = []
with ThreadPoolExecutor(max_workers=12) as ex:
    futs = {ex.submit(bajar, u, os.path.join(DEST, por_url[u])): u for u in tareas}
    hechos = 0
    for fut in as_completed(futs):
        u = futs[fut]
        estado = fut.result()
        hechos += 1
        if estado.startswith("ERROR"):
            errores.append((u, estado))
        if hechos % 100 == 0:
            print(f"  {hechos}/{len(tareas)} descargadas...")

print(f"Descarga terminada: {len(tareas) - len(errores)} bien, {len(errores)} errores")
for u, e in errores:
    print(f"  FALLO {u} -> {e}")

if errores:
    sys.exit("Hay errores de descarga: NO se reescribe main.js. Corre de nuevo el script.")

# --- reescribir main.js con rutas locales ---
for p in con_foto:
    p["i"] = "assets/img/perfumes/" + por_url[p["i"]]
nuevo = json.dumps(products, ensure_ascii=False, separators=(",", ":"))
src = src[: m.start(1)] + nuevo + src[m.end(1):]
io.open(MAIN, "w", encoding="utf-8", newline="\n").write(src)

total = sum(
    os.path.getsize(os.path.join(DEST, f)) for f in os.listdir(DEST)
) / 1024 / 1024
print(f"main.js actualizado. {len(os.listdir(DEST))} fotos locales, {total:.1f} MB en assets/img/perfumes/")
