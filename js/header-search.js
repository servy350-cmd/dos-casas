/* Buscador del header: espeja la búsqueda en el buscador del catálogo (#catSearch)
   y lleva al visitante directo a los resultados. En móvil, mientras se busca,
   el header se compacta (clase .searching) para que el campo no tape la marca. */
(function(){
  var inp=document.getElementById('navSearch'); if(!inp) return;
  var cat=document.getElementById('catSearch');
  var sec=document.getElementById('perfumes');
  var hdr=document.querySelector('header.nav');
  function compact(){
    if(!hdr) return;
    if(document.activeElement===inp||inp.value.trim()) hdr.classList.add('searching');
    else hdr.classList.remove('searching');
  }
  function sync(){
    if(!cat) return;
    cat.value=inp.value;
    cat.dispatchEvent(new Event('input',{bubbles:true}));
  }
  function verResultados(){
    var meta=document.getElementById('catCount');
    var dest=(meta&&meta.parentElement)||sec; if(!dest) return;
    var r=dest.getBoundingClientRect();
    /* solo desplaza si los resultados no están a la vista */
    if(r.top>window.innerHeight*.5||r.bottom<120){
      var y=window.scrollY+r.top-76; /* aire para el header fijo */
      window.scrollTo({top:Math.max(y,0),behavior:'smooth'});
    }
  }
  var tmr;
  inp.addEventListener('focus',compact);
  inp.addEventListener('blur',compact);
  inp.addEventListener('input',function(){
    compact();
    clearTimeout(tmr);
    tmr=setTimeout(function(){sync();if(inp.value.trim())verResultados();},220);
  });
  inp.addEventListener('keydown',function(e){
    if(e.key==='Enter'){e.preventDefault();clearTimeout(tmr);sync();verResultados();}
  });
  /* la X nativa del input type=search también limpia el catálogo */
  inp.addEventListener('search',function(){sync();compact();});
})();
