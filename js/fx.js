/* ============================================================
   FX · CAPA 3D  —  motion orquestada, prioridad móvil
   Cero librerías. Todo con guardas de equipo y viewport.
   ============================================================ */
(function(){
  var mqReduce = matchMedia('(prefers-reduced-motion:reduce)');
  var reduce   = mqReduce.matches;
  var fine     = matchMedia('(pointer:fine)').matches && innerWidth >= 768;
  var lowEnd   = (navigator.deviceMemory && navigator.deviceMemory <= 4) ||
                 (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4);
  var root = document.documentElement;
  if (fine && !reduce) root.classList.add('fx-fine');
  var rAF = window.requestAnimationFrame || function(f){return setTimeout(f,16)};

  /* ---------- 1 · parallax 3D del frasco (mouse) ---------- */
  if (fine && !reduce){
    var hero = document.querySelector('.hero');
    var photo = document.querySelector('.hero-photo');
    if (hero && photo){
      var pend=false, lpx=0, lpy=0;
      hero.addEventListener('pointermove', function(e){
        var r = hero.getBoundingClientRect();
        lpx = ((e.clientX - r.left)/r.width  - .5)*2;   // -1..1
        lpy = ((e.clientY - r.top )/r.height - .5)*2;
        if(!pend){ pend=true; rAF(function(){
          photo.style.setProperty('--px', lpx.toFixed(3));
          photo.style.setProperty('--py', lpy.toFixed(3));
          pend=false;
        }); }
      });
      hero.addEventListener('pointerleave', function(){
        photo.style.setProperty('--px',0); photo.style.setProperty('--py',0);
      });
    }
  }

  /* ---------- 2 · tilt 3D + spotlight (delegado, tarjetas dinámicas) ---------- */
  if (fine && !reduce){
    var SEL = '.pc,.fcard,.sku';
    var cur = null, tpend=false, lx=0, ly=0, lrect=null, ltag=null;
    function amp(el){ return el.classList.contains('fcard') ? 4 : 6; }
    document.addEventListener('pointermove', function(e){
      var el = e.target.closest(SEL);
      if (el !== cur){
        if (cur){ cur.classList.remove('tilt');
          cur.style.removeProperty('--rx'); cur.style.removeProperty('--ry');
          cur.style.removeProperty('--mx'); cur.style.removeProperty('--my'); }
        cur = el;
        if (cur) cur.classList.add('tilt');
      }
      if (!cur) return;
      lrect = cur.getBoundingClientRect(); ltag = cur;
      lx = e.clientX; ly = e.clientY;
      if(!tpend){ tpend=true; rAF(function(){
        if(!ltag) { tpend=false; return; }
        var r = lrect;
        var dx = (lx - r.left)/r.width  - .5;   // -.5..5
        var dy = (ly - r.top )/r.height - .5;
        var a = amp(ltag);
        ltag.style.setProperty('--ry', (dx*a).toFixed(2)+'deg');
        ltag.style.setProperty('--rx', (-dy*a).toFixed(2)+'deg');
        ltag.style.setProperty('--mx', (((lx-r.left)/r.width)*100).toFixed(1)+'%');
        ltag.style.setProperty('--my', (((ly-r.top)/r.height)*100).toFixed(1)+'%');
        tpend=false;
      }); }
    }, {passive:true});
    document.addEventListener('pointerleave', function(){
      if (cur){ cur.classList.remove('tilt');
        cur.style.removeProperty('--rx'); cur.style.removeProperty('--ry');
        cur.style.removeProperty('--mx'); cur.style.removeProperty('--my'); cur=null; }
    });
  }

  /* ---------- 3 · entrada escalonada del catálogo ---------- */
  if (!reduce){
    var catGrid = document.getElementById('catGrid');
    if (catGrid){
      var obs = new MutationObserver(function(muts){
        muts.forEach(function(m){
          var i = 0;
          m.addedNodes.forEach(function(n){
            if (n.nodeType!==1 || !n.classList || !n.classList.contains('pc')) return;
            var d = (i%8)*45; i++;
            n.style.opacity = '0';
            n.style.transform = 'translateY(16px)';
            n.style.transition = 'opacity .55s cubic-bezier(.2,.7,.2,1) '+d+'ms, transform .55s cubic-bezier(.2,.7,.2,1) '+d+'ms';
            rAF(function(){ rAF(function(){
              n.style.opacity=''; n.style.transform='';
            }); });
            n.addEventListener('transitionend', function clr(){
              n.style.transition=''; n.removeEventListener('transitionend', clr);
            });
          });
        });
      });
      obs.observe(catGrid, {childList:true});
    }
  }

  /* ---------- 4 · cursor magnético (CTA dorado) ---------- */
  if (fine && !reduce){
    document.querySelectorAll('.hero-actions .btn--gold, .nav-r .btn--gold').forEach(function(btn){
      btn.classList.add('fx-magnet');
      btn.addEventListener('pointermove', function(e){
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width/2)*.28;
        var y = (e.clientY - r.top - r.height/2)*.4;
        btn.style.transform = 'translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)';
      });
      btn.addEventListener('pointerleave', function(){ btn.style.transform=''; });
    });
  }

  /* ---------- 5 · esporas vivas en #ritual (canvas) ---------- */
  if (!reduce){
    var ritual = document.getElementById('ritual');
    if (ritual && !ritual.querySelector('.fx-spores')){
      var cv = document.createElement('canvas');
      cv.className = 'fx-spores'; cv.setAttribute('aria-hidden','true');
      ritual.insertBefore(cv, ritual.firstChild);
      var ctx = cv.getContext('2d');
      var DPR = Math.min(devicePixelRatio||1, 2);
      var W=0, H=0, parts=[], running=false, raf=0;
      var N = lowEnd ? 10 : (fine ? 30 : 16);
      function size(){
        var r = ritual.getBoundingClientRect();
        W = r.width; H = r.height;
        cv.width = W*DPR; cv.height = H*DPR;
        cv.style.width=W+'px'; cv.style.height=H+'px';
        ctx.setTransform(DPR,0,0,DPR,0,0);
      }
      function mk(){
        return { x:Math.random()*W, y:Math.random()*H,
          r:Math.random()*1.8+0.6, vx:(Math.random()-.5)*0.25,
          vy:-(Math.random()*0.4+0.15), a:Math.random()*0.5+0.18,
          tw:Math.random()*Math.PI*2, gold:Math.random()<0.35 };
      }
      function init(){ parts=[]; for(var i=0;i<N;i++){ var p=mk(); p.y=Math.random()*H; parts.push(p);} }
      function frame(){
        if(!running) return;
        ctx.clearRect(0,0,W,H);
        for(var i=0;i<parts.length;i++){
          var p=parts[i];
          p.x+=p.vx; p.y+=p.vy; p.tw+=0.03;
          if(p.y< -8){ p.y=H+8; p.x=Math.random()*W; }
          if(p.x< -8) p.x=W+8; if(p.x>W+8) p.x=-8;
          var fl = p.a*(0.6+0.4*Math.sin(p.tw));
          ctx.beginPath();
          ctx.fillStyle = p.gold ? 'rgba(216,189,126,'+fl.toFixed(3)+')'
                                 : 'rgba(176,196,160,'+fl.toFixed(3)+')';
          ctx.arc(p.x,p.y,p.r,0,6.283);
          ctx.fill();
        }
        raf = rAF(frame);
      }
      function start(){ if(running) return; running=true; raf=rAF(frame); }
      function stop(){ running=false; if(raf) cancelAnimationFrame(raf); }
      size(); init();
      var vis = new IntersectionObserver(function(es){
        es.forEach(function(e){ e.isIntersecting && !document.hidden ? start() : stop(); });
      },{threshold:0.05});
      vis.observe(ritual);
      document.addEventListener('visibilitychange', function(){
        document.hidden ? stop() : (isOnScreen() && start());
      });
      function isOnScreen(){ var r=ritual.getBoundingClientRect(); return r.bottom>0 && r.top<innerHeight; }
      var rz; addEventListener('resize', function(){ clearTimeout(rz); rz=setTimeout(function(){ size(); init(); }, 200); });
    }
  }
})();
