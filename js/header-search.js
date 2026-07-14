/* Buscador del header: espeja la búsqueda en el buscador del catálogo (#catSearch)
   y lleva al visitante a la sección de perfumes para ver los resultados. */
(function(){
  var inp=document.getElementById('navSearch'); if(!inp) return;
  var cat=document.getElementById('catSearch');
  var sec=document.getElementById('perfumes');
  function sync(){
    if(!cat) return;
    cat.value=inp.value;
    cat.dispatchEvent(new Event('input',{bubbles:true}));
  }
  function verResultados(){
    if(!sec) return;
    var r=sec.getBoundingClientRect();
    /* solo desplaza si el catálogo no está a la vista */
    if(r.top>window.innerHeight*.55||r.bottom<120) sec.scrollIntoView({behavior:'smooth'});
  }
  var tmr;
  inp.addEventListener('input',function(){
    clearTimeout(tmr);
    tmr=setTimeout(function(){sync();if(inp.value.trim())verResultados();},220);
  });
  inp.addEventListener('keydown',function(e){
    if(e.key==='Enter'){e.preventDefault();clearTimeout(tmr);sync();verResultados();}
  });
  /* la X nativa del input type=search también limpia el catálogo */
  inp.addEventListener('search',sync);
})();
