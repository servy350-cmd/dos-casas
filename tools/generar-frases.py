# -*- coding: utf-8 -*-
"""Genera para cada perfume una frase identitaria (t) y un resumen de aroma (r)
a partir de su piramide olfativa, y enriquece las fichas SETASOULS con
que-hace (hace), beneficios fisicos (fisico), frase energetica (frase) y foto (img).

Reescribe window.FICHAS y window.FICHAS_NATURAL dentro de js/fichas.js.
Correr DESPUES de tools/generar-fichas.py si se regeneran las piramides.

Uso:  python tools/generar-frases.py
"""
import io
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHAS_JS = os.path.join(ROOT, "js", "fichas.js")
MAIN_JS = os.path.join(ROOT, "js", "main.js")


def plano(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


# ---------- temas olfativos ----------
TEMAS = {
    "citrico": ["bergamota", "limon", "mandarina", "naranja", "toronja", "pomelo",
                "yuzu", "citrico", "lima", "petit grain", "citron"],
    "frutal": ["manzana", "pera", "pina", "durazno", "melocoton", "ciruela", "frambuesa",
               "fresa", "lichi", "grosella", "zarzamora", "cereza", "albaricoque",
               "granada", "melon", "sandia", "fruta", "mango", "maracuya", "uva", "kiwi"],
    "dulce": ["vainilla", "caramelo", "praline", "miel", "chocolate", "cacao", "azucar",
              "malvavisco", "tonka", "almendra", "pistacho", "cafe", "leche", "crema",
              "gourmand", "regaliz", "turron", "galleta"],
    "floral": ["jazmin", "azahar", "tuberosa", "gardenia", "ylang", "lirio", "magnolia",
               "flor", "nardo", "madreselva", "azucena", "rosa", "violeta", "peonia",
               "iris", "geranio", "jacinto", "mimosa", "heliotropo", "orquidea",
               "fresia", "loto", "ciclamen", "clavel", "neroli"],
    "especiado": ["pimienta", "cardamomo", "canela", "azafran", "clavo", "jengibre",
                  "nuez moscada", "especia", "comino", "anis", "cilantro"],
    "amaderado": ["cedro", "sandalo", "vetiver", "madera", "caoba", "guayaco",
                  "palo santo", "cachemira", "abeto", "pino", "cipres", "roble", "bambu"],
    "oscuro": ["oud", "agarwood", "incienso", "mirra", "resina", "benjui", "labdano",
               "opoponaco", "cuero", "gamuza", "tabaco", "alquitran", "civeta"],
    "ambar": ["ambar", "amberwood", "ambargris"],
    "fresco": ["marina", "acuatic", "agua", "brisa", "ozono", "menta", "romero",
               "salvia", "te verde", "cesped", "verde", "albahaca", "eucalipto",
               "lavanda", "tomillo", "artemisa", "hierba", "sal "],
    "almizcle": ["almizcle", "musk"],
}
ADJ = {
    "citrico": "luminoso", "frutal": "jugoso", "dulce": "envolvente",
    "floral": "elegante", "especiado": "especiado", "amaderado": "amaderado",
    "oscuro": "profundo", "ambar": "cálido", "fresco": "fresco", "almizcle": "sensual",
}
FRASES = {
    "citrico": ["Luz cítrica que despierta la piel.",
                "Frescura que abre puertas.",
                "El primer rayo de sol, embotellado.",
                "Energía limpia para empezar cualquier historia."],
    "frutal": ["Jugoso, vibrante, imposible de ignorar.",
               "Fruta madura con carácter propio.",
               "Dulzura fresca que contagia alegría.",
               "Un mordisco de color en la piel."],
    "dulce": ["Dulzura que se vuelve presencia.",
              "El postre que se lleva puesto.",
              "Azúcar con intención, estela con memoria.",
              "Calidez dulce que abraza sin pedir permiso."],
    "floral": ["Un jardín entero en la piel.",
               "Flores con voz propia.",
               "Elegancia que florece con las horas.",
               "Pétalos que se vuelven recuerdo."],
    "especiado": ["Especias que cuentan historias.",
                  "Calor que se queda en la memoria.",
                  "Carácter especiado, presencia magnética.",
                  "Fuego lento que envuelve."],
    "amaderado": ["Madera noble, carácter firme.",
                  "Raíces profundas, presencia serena.",
                  "La elegancia de lo esencial.",
                  "Solidez que se percibe sin alzar la voz."],
    "oscuro": ["Intensidad que no pide permiso.",
               "Elegancia oscura, estela infinita.",
               "Profundo, magnético, inolvidable.",
               "El misterio también se lleva puesto."],
    "ambar": ["Calidez que envuelve como un atardecer.",
              "Ámbar que se funde con la piel.",
              "Sensualidad cálida, huella duradera.",
              "Un abrazo que permanece."],
    "fresco": ["Brisa limpia, piel serena.",
               "Frescura que acompaña todo el día.",
               "El aire libre, hecho perfume.",
               "Claridad que se respira."],
    "almizcle": ["Cercanía que seduce.",
                 "Segunda piel, primera impresión.",
                 "Suavidad que invita a quedarse."],
}
FRASES_ARABE = ["La firma árabe: intensidad que deja huella.",
                "Concentración alta, estela que habla por ti.",
                "Oriente en la piel, presencia absoluta."]
FRASES_GENERICAS = ["Carácter propio, presencia que se recuerda.",
                    "Un clásico que no necesita presentación.",
                    "Estilo que se lleva sin esfuerzo."]


def temas_de(f):
    puntos = {}
    for nivel, peso in (("sal", 1.0), ("cor", 1.2), ("fon", 1.3)):
        for nota in f.get(nivel) or []:
            n = plano(nota)
            for tema, claves in TEMAS.items():
                if any(k in n for k in claves):
                    puntos[tema] = puntos.get(tema, 0) + peso
    return [t for t, _ in sorted(puntos.items(), key=lambda x: -x[1])]


def pick(pool, handle):
    return pool[sum(ord(c) for c in handle) % len(pool)]


def lista(notas, n=3):
    ns = [x.strip().lower() for x in (notas or [])[:n] if x.strip()]
    if not ns:
        return ""
    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " y " + ns[-1]


def ocasion(p):
    o = plano(p.get("o") or "")
    if "dia" in o and "noche" in o:
        return "todo momento"
    if "noche" in o or "citas" in o or "fiestas" in o:
        return "la noche"
    if "dia" in o:
        return "el día"
    return "cualquier ocasión"


def resumen(p, f, handle):
    sal, cor, fon = lista(f.get("sal")), lista(f.get("cor")), lista(f.get("fon"))
    tt = temas_de(f)
    adjs = [ADJ[t] for t in tt[:2]]
    caracter = " y ".join(dict.fromkeys(adjs)) if adjs else "con carácter propio"
    cierre = f"Un aroma {caracter} para {ocasion(p)}."
    if sal and cor and fon:
        cuerpo = pick([
            f"Abre con {sal}; el corazón revela {cor} y el fondo reposa en {fon}.",
            f"La salida de {sal} florece en un corazón de {cor}, sobre un fondo de {fon}.",
            f"Arranca con {sal}, se desarrolla en {cor} y deja una estela de {fon}.",
        ], handle)
    elif sal and fon:
        cuerpo = f"Abre con {sal} y se asienta en un fondo de {fon}."
    elif sal and cor:
        cuerpo = f"Abre con {sal} y florece en un corazón de {cor}."
    elif sal:
        cuerpo = f"Sus notas de {sal} marcan el carácter desde el primer momento."
    else:
        return ""
    return f"{cuerpo} {cierre}"


def resumen_generico(p):
    tipo = (p.get("t") or "perfume").lower()
    marca = p.get("m") or ""
    de = f" de {marca}" if marca else ""
    return (f"Una creación {tipo}{de} para {ocasion(p)}. El proveedor no publica su "
            "pirámide olfativa: escríbenos por WhatsApp y te contamos cómo huele.")


def tagline(p, f, handle):
    tt = temas_de(f) if f else []
    g = plano(p.get("g") or "")
    if len(tt) > 1 and tt[0] == "floral" and "hombre" in g and "mujer" not in g:
        tt = tt[1:]
    if tt:
        return pick(FRASES[tt[0]], handle)
    if "arabe" in plano(p.get("t") or ""):
        return pick(FRASES_ARABE, handle)
    return pick(FRASES_GENERICAS, handle)


# ---------- fichas SETASOULS enriquecidas ----------
NATURAL_EXTRA = {
    "melena": {
        "img": "assets/img/melena.webp",
        "hace": "El hongo del enfoque: usado tradicionalmente en la medicina oriental para acompañar la claridad mental, la memoria y la concentración en días de alta demanda.",
        "fisico": "Acompaña el enfoque sostenido, la memoria de trabajo y el bienestar del sistema nervioso.",
        "frase": "Mente despierta, ideas en orden: claridad que se siente en el cuerpo.",
    },
    "shiitake": {
        "img": "assets/img/shiitake.webp",
        "hace": "Clásico de la tradición oriental, valorado como acompañante de las defensas y de la vitalidad diaria.",
        "fisico": "Acompaña el sistema inmune, la energía estable y el bienestar general.",
        "frase": "Defensas firmes y energía pareja para sostener tu día.",
    },
    "cordyceps": {
        "img": "assets/img/cordyceps.webp",
        "hace": "El hongo del rendimiento: usado tradicionalmente para acompañar la energía, la resistencia física y la respiración durante el esfuerzo.",
        "fisico": "Acompaña la resistencia en el entrenamiento, la oxigenación y la recuperación.",
        "frase": "Combustible natural: más aire, más aguante, más presencia.",
    },
    "reishi": {
        "img": "assets/img/reishi.webp",
        "hace": "El «hongo de la calma»: usado tradicionalmente para acompañar el descanso profundo y el equilibrio del cuerpo.",
        "fisico": "Acompaña el sueño reparador, la relajación y el equilibrio del sistema inmune.",
        "frase": "Calma que restaura: descanso profundo, cuerpo en equilibrio.",
    },
    "oregano": {
        "img": "assets/img/oregano.webp",
        "hace": "Extracto concentrado de orégano, usado tradicionalmente como apoyo del sistema inmune y aliado en épocas de cambio.",
        "fisico": "Acompaña las defensas naturales y el confort respiratorio y digestivo.",
        "frase": "Gotas concentradas de protección natural.",
    },
    "hidratante": {
        "img": "assets/img/hidratante.webp",
        "hace": "Tratamiento facial todo-en-uno con activos de alta concentración: desmancha, tensura, levanta y suaviza la piel.",
        "fisico": "Piel más firme, pareja y luminosa con el uso constante.",
        "frase": "Tu piel, con la energía de quien duerme bien.",
    },
    "crema-dental": {
        "img": "assets/img/crema-dental.webp",
        "hace": "Higiene dental diaria con ingredientes de origen natural, sin agresivos innecesarios.",
        "fisico": "Limpieza profunda, encías cuidadas y aliento fresco.",
        "frase": "Sonrisa limpia, naturaleza intacta.",
    },
    "desodorante": {
        "img": "assets/img/desodorante-alumbre.webp",
        "hace": "Desodorante mineral de piedra de alumbre: neutraliza el olor respetando la transpiración natural de la piel.",
        "fisico": "Protección duradera sin fragancias sintéticas ni residuos.",
        "frase": "Frescura mineral que respeta tu piel.",
    },
    "aceite-coco": {
        "img": "assets/img/aceite-coco.webp",
        "hace": "Aceite de coco multiusos: cocina consciente e hidratación profunda de piel y cabello.",
        "fisico": "Nutre la piel, repara el cabello y aporta energía limpia en la cocina.",
        "frase": "Un solo frasco, mil cuidados.",
    },
    "jabon-ganoderma": {
        "img": "assets/img/jabon-ganoderma.webp",
        "hace": "Jabón artesanal elaborado con Ganoderma lucidum (reishi) para la limpieza diaria del cuerpo.",
        "fisico": "Limpia con suavidad y cuida la piel, también la sensible.",
        "frase": "El ritual del reishi, hecho espuma.",
    },
    "lips": {
        "img": "assets/img/lips.webp",
        "hace": "Bálsamo natural que hidrata y protege los labios expuestos al sol, el viento y el frío.",
        "fisico": "Labios suaves, nutridos y protegidos todo el día.",
        "frase": "Protección suave que se nota al sonreír.",
    },
}

# ---------- ejecutar ----------
src_main = io.open(MAIN_JS, encoding="utf-8").read()
prods = json.loads(re.search(r"const PRODUCTS=(\[.*?\]);", src_main, re.S).group(1))

src = io.open(FICHAS_JS, encoding="utf-8").read()
m_f = re.search(r"window\.FICHAS=(\{.*?\});\n", src, re.S)
m_n = re.search(r"window\.FICHAS_NATURAL=(\{.*?\});\n", src, re.S)
fichas = json.loads(m_f.group(1))
natural = json.loads(m_n.group(1))

con_notas, sin_notas = 0, 0
for p in prods:
    h = (p.get("u") or "").rstrip("/").split("/")[-1]
    if not h:
        continue
    f = fichas.get(h)
    if f is None:
        f = fichas[h] = {"fam": "", "sal": [], "cor": [], "fon": []}
    r = resumen(p, f, h)
    if r:
        con_notas += 1
    else:
        r = resumen_generico(p)
        sin_notas += 1
    f["t"] = tagline(p, f, h)
    f["r"] = r

for k, extra in NATURAL_EXTRA.items():
    if k not in natural:
        sys.exit(f"clave SETASOULS desconocida: {k}")
    natural[k].update(extra)

dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
src = src[:m_f.start(1)] + dump(fichas) + src[m_f.end(1):]
m_n = re.search(r"window\.FICHAS_NATURAL=(\{.*?\});\n", src, re.S)
src = src[:m_n.start(1)] + dump(natural) + src[m_n.end(1):]
io.open(FICHAS_JS, "w", encoding="utf-8", newline="\n").write(src)

print(f"Perfumes: {con_notas} con resumen real, {sin_notas} genericos, total fichas {len(fichas)}")
print(f"SETASOULS: {len(NATURAL_EXTRA)} fichas enriquecidas")
ej = fichas[(prods[0]['u']).split('/')[-1]]
print("Ejemplo:", prods[0]["n"], "->", ej["t"], "|", ej["r"])
