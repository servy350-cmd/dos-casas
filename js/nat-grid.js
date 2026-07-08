(function(){
  var tabs=document.getElementById('natTabs'); if(!tabs) return;
  var grid=document.getElementById('natGrid'), count=document.getElementById('natCount'), more=document.getElementById('natMore');
  var cards=[].slice.call(grid.querySelectorAll('.pc'));
  var INITIAL=4, STEP=8, val='', shown=INITIAL;
  function render(){
    var f=cards.filter(function(c){ return !val||c.getAttribute('data-cat')===val; });
    cards.forEach(function(c){ c.style.display='none'; });
    f.slice(0,shown).forEach(function(c){ c.style.display=''; });
    count.textContent=f.length+' producto'+(f.length===1?'':'s');
    more.hidden = shown>=f.length;
  }
  tabs.addEventListener('click',function(e){
    var b=e.target.closest('.chip'); if(!b) return;
    tabs.querySelectorAll('.chip').forEach(function(c){ c.classList.remove('active'); });
    b.classList.add('active');
    val=b.getAttribute('data-val'); shown=INITIAL; render();
  });
  more.addEventListener('click',function(){ shown+=STEP; render(); });
  render();
})();
