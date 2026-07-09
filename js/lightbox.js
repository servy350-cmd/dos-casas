(function(){
  var lb=document.getElementById('lightbox'),lbImg=document.getElementById('lbImg');
  if(!lb) return;
  function open(src){ lbImg.src=src; lb.hidden=false; requestAnimationFrame(function(){lb.classList.add('show');}); }
  function close(){ lb.classList.remove('show'); setTimeout(function(){lb.hidden=true;lbImg.src='';},300); }
  function zoomDe(el){ var b=el&&el.closest?el.closest('[data-zoom]'):null; if(!b) return false; var im=b.querySelector('img'); if(im&&im.src) open(im.src); return true; }
  document.addEventListener('click',function(e){ zoomDe(e.target); });
  document.addEventListener('keydown',function(e){ if((e.key==='Enter'||e.key===' ')&&e.target&&e.target.matches&&e.target.matches('[data-zoom]')){ if(zoomDe(e.target)) e.preventDefault(); } });
  document.getElementById('lbX').addEventListener('click',close);
  lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!lb.hidden) close(); });
})();
