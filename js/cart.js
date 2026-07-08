(function(){
  function escH(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
  function waNum(){ return (typeof WA!=='undefined' && WA) ? WA : '573001234567'; }
  var KEY='dc_cart_v1', CART=[];
  try{ CART=JSON.parse(localStorage.getItem(KEY)||'[]')||[]; }catch(e){ CART=[]; }
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(CART)); }catch(e){} }
  function fmt(n){ return '$'+(n||0).toLocaleString('es-CO'); }
  var badge=document.getElementById('cartBadge'), body=document.getElementById('cartBody'),
      totalEl=document.getElementById('cartTotal'), sendEl=document.getElementById('cartSend'),
      drawer=document.getElementById('cartDrawer'), overlay=document.getElementById('cartOverlay'),
      toast=document.getElementById('cartToast');
  function count(){ return CART.reduce(function(s,it){return s+it.qty;},0); }
  function total(){ return CART.reduce(function(s,it){return s+it.price*it.qty;},0); }
  function renderBadge(){
    var c=count();
    if(badge){ badge.textContent=c; badge.hidden=(c===0);
      if(c>0){ badge.classList.remove('bump'); void badge.offsetWidth; badge.classList.add('bump'); } }
  }
  function buildMsg(){
    var lines=CART.map(function(it,i){
      var det=[it.m,it.env].filter(Boolean).join(', ');
      return (i+1)+'. '+it.n+(det?' ('+det+')':'')+' x'+it.qty+' - '+fmt(it.price*it.qty);
    });
    return 'Hola 🌿 Quiero hacer este pedido en DOS CASAS:\n\n'+lines.join('\n')+'\n\nTotal: '+fmt(total())+'\n\n¿Me confirman disponibilidad y envío?';
  }
  function render(){
    if(!body) return;
    if(!CART.length){
      body.innerHTML='<p class="cart-empty">Aún no has agregado nada.<br>Explora los perfumes y la medicina natural.</p>';
      sendEl.classList.add('disabled'); sendEl.removeAttribute('href');
    } else {
      body.innerHTML=CART.map(function(it,i){
        var meta=[it.m,it.env].filter(Boolean).join(' · ');
        return '<div class="cart-item"><div class="ci-main">'
          +'<div class="ci-name">'+escH(it.n)+'</div>'
          +(meta?'<div class="ci-meta">'+escH(meta)+'</div>':'')
          +'<div class="ci-row"><span class="ci-qty"><button data-dec="'+i+'" aria-label="Quitar uno">&minus;</button><span>'+it.qty+'</span><button data-inc="'+i+'" aria-label="Agregar uno">+</button></span>'
          +'<span class="ci-price">'+fmt(it.price*it.qty)+'</span></div>'
          +'<button class="ci-del" data-del="'+i+'">Quitar</button>'
          +'</div></div>';
      }).join('');
      sendEl.classList.remove('disabled');
      sendEl.setAttribute('href','https://wa.me/'+waNum()+'?text='+encodeURIComponent(buildMsg()));
    }
    totalEl.textContent=fmt(total());
    renderBadge();
  }
  var tmr;
  function showToast(){ if(!toast)return; toast.classList.add('show'); clearTimeout(tmr); tmr=setTimeout(function(){toast.classList.remove('show');},1600); }
  function add(item){
    var ex=CART.filter(function(x){return x.id===item.id;})[0];
    if(ex){ ex.qty++; } else { item.qty=1; CART.push(item); }
    save(); render(); showToast();
  }
  function openCart(){ overlay.hidden=false; requestAnimationFrame(function(){overlay.classList.add('show');drawer.classList.add('open');}); drawer.setAttribute('aria-hidden','false'); }
  function closeCart(){ overlay.classList.remove('show'); drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); setTimeout(function(){overlay.hidden=true;},340); }
  var cartBtn=document.getElementById('cartBtn');
  if(cartBtn) cartBtn.addEventListener('click',openCart);
  var cl=document.getElementById('cartClose'); if(cl) cl.addEventListener('click',closeCart);
  if(overlay) overlay.addEventListener('click',closeCart);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeCart(); });
  // delegacion global: botones Agregar
  document.addEventListener('click',function(e){
    var b=e.target.closest('[data-add]'); if(!b) return;
    e.preventDefault();
    var n=b.getAttribute('data-n')||'', m=b.getAttribute('data-m')||'';
    var env=b.getAttribute('data-env')||'', price=parseInt(b.getAttribute('data-price')||'0',10)||0;
    if(b.hasAttribute('data-hasv')){
      var pc=b.closest('.pc'); var s=pc&&pc.querySelector('.env-sel'); var vs=[];
      try{ vs=JSON.parse(pc.getAttribute('data-v')||'[]'); }catch(err){}
      var idx=s?parseInt(s.value,10):0; var v=vs[idx]||vs[0];
      if(v){ env=v.t; price=v.p; }
    }
    add({ id:n+'|'+env, n:n, m:m, env:env, price:price });
  });
  // qty / quitar dentro del drawer
  if(body) body.addEventListener('click',function(e){
    var t=e.target.closest('button'); if(!t) return;
    var inc=t.getAttribute('data-inc'), dec=t.getAttribute('data-dec'), del=t.getAttribute('data-del');
    if(inc!=null){ CART[+inc].qty++; }
    else if(dec!=null){ CART[+dec].qty--; if(CART[+dec].qty<1) CART.splice(+dec,1); }
    else if(del!=null){ CART.splice(+del,1); }
    else return;
    save(); render();
  });
  render();
})();
