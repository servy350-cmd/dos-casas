# -*- coding: utf-8 -*-
"""
Auditoría de seguridad del sitio estático DOS CASAS.
Escanea el proyecto en busca de:
  - Secretos / claves / tokens filtrados
  - Enlaces externos sin rel="noopener" (tabnabbing)
  - Recursos externos cargados por http:// (mixed content)
  - Dominios de terceros (para construir el CSP)
  - Patrones de JS peligrosos (eval, innerHTML con datos externos, document.write)
Salida: reporte por consola + tools/security-report.json
"""
import io
import json
import os
import re

ROOT = r"C:\Users\usuario\dos-casas"
SKIP_DIRS = {".git", "node_modules", "tools"}
TEXT_EXT = {".html", ".js", ".css", ".json", ".md", ".txt", ".bat"}

hallazgos = {"alto": [], "medio": [], "bajo": [], "info": []}
dominios = set()

def add(nivel, regla, archivo, detalle):
    hallazgos[nivel].append({"regla": regla, "archivo": archivo, "detalle": detalle})

# Patrones de secretos (evitando falsos positivos obvios)
SECRET_PATTERNS = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Token tipo JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("Clave privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Bearer/secret asignado", re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd|authorization)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
    ("Stripe key", re.compile(r"sk_live_[0-9A-Za-z]{20,}")),
]

files = []
for base, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for n in names:
        p = os.path.join(base, n)
        if os.path.splitext(n)[1].lower() in TEXT_EXT:
            files.append(p)

for p in files:
    rel = os.path.relpath(p, ROOT)
    try:
        txt = io.open(p, encoding="utf-8").read()
    except Exception:
        continue

    # 1) Secretos
    for nombre, pat in SECRET_PATTERNS:
        for m in pat.finditer(txt):
            # el catálogo de perfumes son datos públicos; ignorar coincidencias dentro de URLs de imagenes cdn
            frag = txt[max(0, m.start()-40):m.start()]
            if "cdn.shopify" in frag or "?v=" in m.group(0):
                continue
            add("alto", "Posible secreto: " + nombre, rel, m.group(0)[:60])

    # 2) Dominios externos
    for m in re.finditer(r"https?://([a-z0-9.\-]+)", txt, re.I):
        dominios.add(m.group(1).lower())

    # 3) Mixed content (http:// en HTML/CSS)
    if rel.endswith((".html", ".css")):
        for m in re.finditer(r"(?<!:)http://[a-z0-9.\-]+", txt, re.I):
            if "localhost" not in m.group(0) and "127.0.0.1" not in m.group(0):
                add("medio", "Recurso por HTTP (mixed content)", rel, m.group(0)[:70])

    # 4) Enlaces externos sin noopener
    if rel.endswith(".html"):
        for m in re.finditer(r"<a\b[^>]*target=[\"']_blank[\"'][^>]*>", txt, re.I):
            tag = m.group(0)
            if "rel=" not in tag.lower() or "noopener" not in tag.lower():
                add("medio", "target=_blank sin rel=noopener (tabnabbing)", rel, tag[:80])

    # 5) JS peligroso
    if rel.endswith((".html", ".js")):
        for regla, pat in [
            ("eval()", re.compile(r"\beval\s*\(")),
            ("document.write", re.compile(r"document\.write\s*\(")),
            ("new Function()", re.compile(r"\bnew\s+Function\s*\(")),
            ("innerHTML con concatenación", re.compile(r"innerHTML\s*[+]?=\s*[^;]*\+")),
        ]:
            for m in pat.finditer(txt):
                add("bajo", "Patrón JS a revisar: " + regla, rel, txt[m.start():m.start()+70].replace("\n", " "))

# Dominios de terceros (excluye el propio y localhost)
externos = sorted(d for d in dominios if "localhost" not in d and not d.startswith("127."))
for d in externos:
    add("info", "Dominio de tercero (incluir en CSP)", "-", d)

print("=" * 60)
print("AUDITORÍA DE SEGURIDAD — DOS CASAS")
print("=" * 60)
print(f"Archivos escaneados: {len(files)}")
for nivel in ("alto", "medio", "bajo", "info"):
    items = hallazgos[nivel]
    print(f"\n[{nivel.upper()}] {len(items)} hallazgo(s)")
    for h in items:
        print(f"  · {h['regla']} — {h['archivo']}: {h['detalle']}")

json.dump(hallazgos, io.open(os.path.join(ROOT, "tools", "security-report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\nReporte guardado en tools/security-report.json")
print("Dominios externos detectados:", externos)
