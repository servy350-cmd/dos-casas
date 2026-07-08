# -*- coding: utf-8 -*-
"""
Genera js/fichas.js:
- window.FICHAS: pirámide olfativa real de cada perfume (parseada de las
  descripciones publicadas por el proveedor perfumesimperial.com.co)
- window.FICHAS_NATURAL: fichas de los productos SETASOULS
- modal "Ficha técnica" (se abre con los botones .ficha-btn)
"""
import io
import json
import re

BASE = r"C:\Users\usuario\dos-casas"

fichas = json.load(open(BASE + r"\tools\fichas-parseadas.json", encoding="utf-8"))
js = io.open(BASE + r"\js\main.js", encoding="utf-8").read()
prods = json.loads(re.search(r"const PRODUCTS=(\[.*?\]);", js, re.S).group(1))

def limpia_nota(n):
    n = re.sub(r"\s*\([^)]*\)", "", n).strip().lstrip(":").strip().rstrip(".").strip()
    if not n or len(n) > 45:
        return None
    if re.match(r"^(con |que |dando |dejando |aportando |creando |ideal |perfecto )", n, re.I):
        return None
    return n[0].upper() + n[1:]

handles_landing = {(p.get("u") or "").rstrip("/").split("/")[-1] for p in prods}
out = {}
for h, f in fichas.items():
    if h not in handles_landing:
        continue
    g = {"fam": f["fam"].strip().rstrip(".")}
    for k in ("sal", "cor", "fon"):
        g[k] = [x for x in (limpia_nota(n) for n in f[k]) if x]
    if g["fam"] or g["sal"] or g["cor"] or g["fon"]:
        out[h] = g

print("fichas de perfume incluidas:", len(out), "de", len(handles_landing), "en la landing")

NATURAL = {
    "melena": {
        "nombre": "Melena de León", "cat": "Suplemento dietario · Hongo funcional",
        "especie": "Hericium erinaceus", "activos": "Hericenonas y erinacinas",
        "present": "60 cápsulas · 30g", "precio": "$120.000",
        "uso": "Usado tradicionalmente en la medicina oriental para acompañar la claridad mental, la memoria y la concentración.",
        "nota": "Suplemento dietario. Este producto no es un medicamento y no sustituye una alimentación equilibrada.",
    },
    "shiitake": {
        "nombre": "Shiitake", "cat": "Suplemento dietario · Hongo funcional",
        "especie": "Lentinula edodes", "activos": "Polisacáridos (lentinano)",
        "present": "60 cápsulas · 30g", "precio": "$120.000",
        "uso": "Hongo culinario y funcional valorado tradicionalmente como acompañante de las defensas y la vitalidad.",
        "nota": "Suplemento dietario. Este producto no es un medicamento y no sustituye una alimentación equilibrada.",
    },
    "cordyceps": {
        "nombre": "Cordyceps", "cat": "Suplemento dietario · Hongo funcional",
        "especie": "Cordyceps militaris", "activos": "Cordicepina y adenosina",
        "present": "60 cápsulas · 30g", "precio": "$120.000",
        "uso": "Usado tradicionalmente para acompañar la energía y la resistencia física.",
        "nota": "Suplemento dietario. Este producto no es un medicamento y no sustituye una alimentación equilibrada.",
    },
    "reishi": {
        "nombre": "Reishi", "cat": "Suplemento dietario · Hongo funcional",
        "especie": "Ganoderma lucidum", "activos": "Triterpenos y betaglucanos",
        "present": "60 cápsulas · 30g", "precio": "$120.000",
        "uso": "Conocido como el “hongo de la calma”; usado tradicionalmente para acompañar el descanso y el equilibrio.",
        "nota": "Suplemento dietario. Este producto no es un medicamento y no sustituye una alimentación equilibrada.",
    },
    "oregano": {
        "nombre": "Aceite de Orégano", "cat": "Extracto herbal",
        "especie": "Origanum vulgare", "activos": "Carvacrol y timol",
        "present": "Gotero · 30ml", "precio": "$60.000",
        "uso": "Extracto concentrado usado tradicionalmente como apoyo del sistema inmune.",
        "nota": "Este producto no es un medicamento y no sustituye una alimentación equilibrada.",
    },
    "hidratante": {
        "nombre": "Hidratante Anti-envejecimiento", "cat": "Cosmética natural",
        "activos": "Retinol 20% · Niacinamida 20% · Sérum 20% · Rosa mosqueta 15% · Ganoderma 15% · Colágeno 5% · Vitamina C 5%",
        "present": "Tarro · 90g", "precio": "$140.000",
        "uso": "Uso tópico facial: desmancha, tensura, levanta y suaviza la piel.",
    },
    "crema-dental": {
        "nombre": "Crema Dental", "cat": "Cuidado oral natural",
        "present": "Frasco con dispensador", "precio": "$35.000",
        "uso": "Higiene dental diaria con ingredientes de origen natural.",
    },
    "desodorante": {
        "nombre": "Desodorante Piedra de Alumbre", "cat": "Cuidado personal natural",
        "especie": "Piedra de alumbre (mineral natural)",
        "present": "Roll-on", "precio": "$40.000",
        "uso": "Desodorante mineral de origen natural para uso diario.",
    },
    "aceite-coco": {
        "nombre": "Aceite de Coco", "cat": "Aceite natural",
        "especie": "Cocos nucifera",
        "present": "Frasco · 500ml", "precio": "$80.000",
        "uso": "Multiusos: cocina, hidratación de piel y cabello.",
    },
    "jabon-ganoderma": {
        "nombre": "Jabón Ganoderma", "cat": "Jabón artesanal",
        "especie": "Elaborado con Ganoderma lucidum",
        "present": "Unidad artesanal", "precio": "$35.000",
        "uso": "Limpieza corporal diaria; elaboración artesanal.",
    },
    "lips": {
        "nombre": "Lips — Bálsamo Labial", "cat": "Cuidado labial",
        "present": "Barra", "precio": "$30.000",
        "uso": "Bálsamo natural para hidratar y proteger los labios.",
    },
}

def js_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

codigo = """/* Fichas técnicas — datos olfativos reales del proveedor + fichas SETASOULS */
window.FICHAS=%s;
window.FICHAS_NATURAL=%s;
(function(){
  var modal=null;
  function ensure(){
    if(modal) return modal;
    var d=document.createElement('div');
    d.innerHTML='<div class="fmodal" hidden><div class="fmodal-panel"><button class="fmodal-x" aria-label="Cerrar">&times;</button><div class="fmodal-c"></div></div></div>';
    modal=d.firstElementChild;
    document.body.appendChild(modal);
    modal.addEventListener('click',function(e){ if(e.target===modal) close(); });
    modal.querySelector('.fmodal-x').addEventListener('click',close);
    document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!modal.hidden) close(); });
    return modal;
  }
  function open(html){ var m=ensure(); m.querySelector('.fmodal-c').innerHTML=html; m.hidden=false; requestAnimationFrame(function(){ m.classList.add('show'); }); }
  function close(){ modal.classList.remove('show'); setTimeout(function(){ modal.hidden=true; },300); }
  function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }
  function row(k,v){ return v?'<div class="fm-row"><b>'+k+'</b><span>'+esc(v)+'</span></div>':''; }
  function pyr(f){
    if(!f||!((f.sal&&f.sal.length)||(f.cor&&f.cor.length)||(f.fon&&f.fon.length))) return '';
    function col(t,a){ return '<div class="fm-col"><h4>'+t+'</h4><p>'+(a&&a.length?a.map(esc).join(', '):'&mdash;')+'</p></div>'; }
    return '<div class="fm-pyr">'+col('Salida',f.sal)+col('Corazón',f.cor)+col('Fondo',f.fon)+'</div>';
  }
  function abrirPerfume(h){
    var lista=(typeof PRODUCTS!=='undefined')?PRODUCTS:[];
    var p=null;
    for(var i=0;i<lista.length;i++){ if((lista[i].u||'').split('/').pop()===h){ p=lista[i]; break; } }
    if(!p) return;
    var f=window.FICHAS[h];
    var pres=(p.v&&p.v.length)?p.v.map(function(v){ return v.t+' — $'+v.p.toLocaleString('es-CO'); }).join(' · '):(p.p?'$'+p.p.toLocaleString('es-CO'):'');
    open('<span class="eyebrow bare">Ficha técnica</span><h3>'+esc(p.n)+'</h3><div class="fm-sub">'+esc([p.m,p.t].filter(Boolean).join(' · '))+'</div>'
      +'<div class="fm-rows">'
      +row('Género',(p.g&&p.g!=='—')?p.g:'')
      +row('Ocasión',p.o)
      +row('Familia olfativa',f&&f.fam)
      +row('Presentaciones',pres)
      +'</div>'
      +(f?pyr(f):'<p class="fm-note">El proveedor no publica la pirámide olfativa de esta referencia.</p>'));
  }
  function abrirNatural(k){
    var f=window.FICHAS_NATURAL[k]; if(!f) return;
    open('<span class="eyebrow bare">Ficha técnica</span><h3>'+esc(f.nombre)+'</h3><div class="fm-sub">'+esc(f.cat)+'</div>'
      +'<div class="fm-rows">'
      +row('Especie / Base',f.especie)
      +row('Activos',f.activos)
      +row('Presentación',f.present)
      +row('Precio',f.precio)
      +row('Uso',f.uso)
      +'</div>'
      +(f.nota?'<p class="fm-note">'+esc(f.nota)+'</p>':''));
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest('.ficha-btn'); if(!b) return;
    e.preventDefault();
    if(b.getAttribute('data-h')) abrirPerfume(b.getAttribute('data-h'));
    else if(b.getAttribute('data-ficha')) abrirNatural(b.getAttribute('data-ficha'));
  });
})();
""" % (js_json(out), js_json(NATURAL))

io.open(BASE + r"\js\fichas.js", "w", encoding="utf-8").write(codigo)
import os
print("js/fichas.js:", os.path.getsize(BASE + r"\js\fichas.js") // 1024, "KB")
