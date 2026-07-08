(function(){
  var track=document.getElementById('skuTrack'); if(!track) return;
  var wrap=track.closest('.sku-carousel');
  var prev=wrap.querySelector('.car-prev'), next=wrap.querySelector('.car-next');
  function step(){ var c=track.querySelector('.sku2'); return c? c.offsetWidth+18 : 260; }
  function upd(){
    var over = track.scrollWidth - track.clientWidth > 4;
    if(!over){ if(prev)prev.style.display='none'; if(next)next.style.display='none'; track.style.justifyContent='center'; return; }
    track.style.justifyContent='flex-start';
    if(prev){ prev.style.display='flex'; prev.style.opacity = track.scrollLeft>4?'1':'.3'; }
    if(next){ next.style.display='flex'; next.style.opacity = (track.scrollLeft < track.scrollWidth-track.clientWidth-4)?'1':'.3'; }
  }
  if(prev) prev.addEventListener('click',function(){ track.scrollBy({left:-step(),behavior:'smooth'}); });
  if(next) next.addEventListener('click',function(){ track.scrollBy({left:step(),behavior:'smooth'}); });
  track.addEventListener('scroll',upd,{passive:true});
  window.addEventListener('resize',upd);
  setTimeout(upd,60);
})();
