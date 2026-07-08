# -*- coding: utf-8 -*-
"""Convierte la sección SETASOULS de carrusel a catálogo categorizado (misma vista que perfumes)."""
import io
import re

P = r"C:\Users\usuario\dos-casas\index.html"
html = io.open(P, encoding="utf-8").read()

PRODUCTOS = [
    # (zoom/ficha, cat, benefit, nombre, sci, fmt, precio, env, img)
    ("melena", "hongos", "Foco", "Melena de León", "Hericium erinaceus", "60 caps · 30g", 120000, "60 cápsulas", "melena.webp"),
    ("shiitake", "hongos", "Defensa", "Shiitake", "Lentinula edodes", "60 caps · 30g", 120000, "60 cápsulas", "shiitake.webp"),
    ("cordyceps", "hongos", "Energía", "Cordyceps", "Cordyceps militaris", "60 caps · 30g", 120000, "60 cápsulas", "cordyceps.webp"),
    ("reishi", "hongos", "Calma", "Reishi", "Ganoderma lucidum", "60 caps · 30g", 120000, "60 cápsulas", "reishi.webp"),
    ("oregano", "extractos", "Inmunidad", "Aceite de Orégano", "Origanum vulgare", "Gotero · 30ml", 60000, "gotero 30ml", "oregano.webp"),
    ("aceite-coco", "extractos", "Nutrición", "Aceite de Coco", "Cocos nucifera", "Frasco · 500ml", 80000, "frasco 500ml", "aceite-coco.webp"),
    ("hidratante", "cuidado", "Piel", "Hidratante Anti-envejecimiento", "Retinol · Ganoderma · Colágeno", "Tarro · 90g", 140000, "tarro 90g", "hidratante.webp"),
    ("crema-dental", "cuidado", "Sonrisa", "Crema Dental", "Cuidado oral natural", "Dispensador", 35000, "dispensador", "crema-dental.webp"),
    ("desodorante", "cuidado", "Frescura", "Desodorante Piedra de Alumbre", "Alumbre natural", "Roll-on", 40000, "roll-on", "desodorante-alumbre.webp"),
    ("jabon-ganoderma", "cuidado", "Piel", "Jabón Ganoderma", "Ganoderma lucidum", "Jabón artesanal", 35000, "jabón artesanal", "jabon-ganoderma.webp"),
    ("lips", "cuidado", "Labios", "Lips — Bálsamo Labial", "Bálsamo natural", "Barra", 30000, "barra", "lips.webp"),
]

def card(k, cat, ben, nombre, sci, fmt, precio, env, img):
    p = "${:,.0f}".format(precio).replace(",", ".")
    return (
        '<article class="pc reveal" data-cat="' + cat + '">'
        '<button class="pc-img pc-zoom" type="button" data-zoom="' + k + '" aria-label="Ampliar ' + nombre + '">'
        '<img loading="lazy" decoding="async" alt="' + nombre + ' — SETASOULS" src="assets/img/' + img + '">'
        '<span class="sku2-zoom">Ampliar ⤢</span></button>'
        '<div class="pc-b"><span class="brandtag">SETASOULS · ' + ben + '</span>'
        '<h3>' + nombre + '</h3><div class="sci">' + sci + '</div><div class="pc-spacer"></div>'
        '<div class="nat-fmt">' + fmt + '</div>'
        '<div class="price">' + p + '</div>'
        '<button class="ficha-btn" type="button" data-ficha="' + k + '">Ficha técnica</button>'
        '<button class="pedir-btn add-btn" type="button" data-add data-n="' + nombre + '" data-m="SETASOULS" data-env="' + env + '" data-price="' + str(precio) + '">Agregar al carrito <span>+</span></button>'
        '</div></article>'
    )

cards = "\n      ".join(card(*p) for p in PRODUCTOS)

nuevo = (
    '<div class="cat-controls reveal">\n'
    '      <div class="nat-tabs" id="natTabs">\n'
    '        <button class="chip active" data-val="">Todos</button>\n'
    '        <button class="chip" data-val="hongos">Hongos funcionales</button>\n'
    '        <button class="chip" data-val="extractos">Extractos y aceites</button>\n'
    '        <button class="chip" data-val="cuidado">Cosmética y cuidado</button>\n'
    '      </div>\n'
    '    </div>\n'
    '    <div class="cat-meta reveal"><span id="natCount">11 productos</span></div>\n'
    '    <div class="grid4" id="natGrid">\n'
    '      ' + cards + '\n'
    '    </div>'
)

patron = re.compile(r'<div class="sku-carousel">.*?car-next"[^>]*>›</button>\s*</div>', re.S)
html2, n = patron.subn(lambda m: nuevo, html, count=1)
assert n == 1, "no se encontró el carrusel"

# subtítulo de sección, como en perfumes
html2 = html2.replace(
    '<h2 class="h2 reveal">Hecha con hongos funcionales.</h2>\n    </div>',
    '<h2 class="h2 reveal">Hecha con hongos funcionales.</h2>\n      <p class="sec-sub reveal">Nuestra línea completa de bienestar natural. Filtrá por categoría.</p>\n    </div>',
    1,
)

# script del filtro antes de </body>
filtro = """<script>
(function(){
  var tabs=document.getElementById('natTabs'); if(!tabs) return;
  var grid=document.getElementById('natGrid'), count=document.getElementById('natCount');
  var cards=[].slice.call(grid.querySelectorAll('.pc'));
  function update(val){
    var n=0;
    cards.forEach(function(c){ var show=!val||c.getAttribute('data-cat')===val; c.style.display=show?'':'none'; if(show) n++; });
    count.textContent=n+' producto'+(n===1?'':'s');
  }
  tabs.addEventListener('click',function(e){
    var b=e.target.closest('.chip'); if(!b) return;
    tabs.querySelectorAll('.chip').forEach(function(c){ c.classList.remove('active'); });
    b.classList.add('active');
    update(b.getAttribute('data-val'));
  });
  update('');
})();
</script>
</body>"""
html2 = html2.replace("</body>", filtro, 1)

io.open(P, "w", encoding="utf-8").write(html2)
print("seccion reemplazada; tarjetas:", len(PRODUCTOS))
