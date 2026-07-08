(function(){
  var lb=document.getElementById('lightbox'),lbImg=document.getElementById('lbImg');
  if(!lb) return;
  function open(src){ lbImg.src=src; lb.hidden=false; requestAnimationFrame(function(){lb.classList.add('show');}); }
  function close(){ lb.classList.remove('show'); setTimeout(function(){lb.hidden=true;lbImg.src='';},300); }
  document.querySelectorAll('[data-zoom]').forEach(function(b){
    b.addEventListener('click',function(){ var im=b.querySelector('img'); if(im) open(im.src); });
  });
  document.getElementById('lbX').addEventListener('click',close);
  lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!lb.hidden) close(); });
})();
