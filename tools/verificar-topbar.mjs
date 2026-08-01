// Verifica la barra de beneficios (topbar) integrada al sitio: render, no-solape con el nav, scroll, CSP.
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const URL = process.env.REPRO_URL || 'http://localhost:8891/index.html';
const b = await chromium.launch();
let fallos = 0;
const ok = (nombre, cond) => { console.log((cond ? 'OK ' : 'FALLO ') + nombre); if (!cond) fallos++; };

for (const [nombre, vp] of [['desktop-1440', { width: 1440, height: 900 }], ['movil-390', { width: 390, height: 844 }]]) {
  const page = await b.newPage({ viewport: vp });
  const csp = [];
  page.on('console', m => { if (m.type() === 'error') csp.push(m.text()); });
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });

  const arriba = await page.evaluate(() => {
    const tb = document.querySelector('.topbar');
    const nav = document.getElementById('nav');
    const items = [...document.querySelectorAll('.topbar-item')];
    return {
      topbar: tb && tb.getBoundingClientRect().height,
      items: items.length,
      iconos: items.every(i => i.querySelector('svg')),
      textos: items.map(i => getComputedStyle(i.querySelector('span')).display),
      navTop: nav.getBoundingClientRect().top,
      solape: nav.getBoundingClientRect().top < tb.getBoundingClientRect().bottom - 1,
    };
  });

  await page.screenshot({ path: `C:/Users/usuario/dos-casas/tools/cap-topbar-${nombre}-arriba.png` });
  await page.evaluate(() => window.scrollTo(0, 600));
  await page.waitForTimeout(600);
  const abajo = await page.evaluate(() => {
    const nav = document.getElementById('nav');
    return { scrolled: nav.classList.contains('scrolled'), navTop: Math.round(nav.getBoundingClientRect().top) };
  });
  await page.screenshot({ path: `C:/Users/usuario/dos-casas/tools/cap-topbar-${nombre}-scroll.png` });

  console.log(`\n=== ${nombre} ===`);
  ok('topbar visible de 40px', Math.round(arriba.topbar) === 40);
  ok('3 beneficios con icono', arriba.items === 3 && arriba.iconos);
  ok('nav arranca debajo de la topbar (sin solape)', Math.round(arriba.navTop) === 40 && !arriba.solape);
  if (nombre.startsWith('movil')) ok('solo iconos en movil', arriba.textos.every(d => d === 'none'));
  else ok('textos visibles en desktop', arriba.textos.every(d => d !== 'none'));
  ok('con scroll: nav fijo arriba (top 0)', abajo.scrolled && abajo.navTop === 0);
  ok('0 errores de consola/CSP', csp.length === 0);
  if (csp.length) console.log('  errores:', csp);
  await page.close();
}

await b.close();
console.log('\nRESULTADO FINAL:', fallos === 0 ? 'TODO OK' : `${fallos} FALLOS`);
process.exit(fallos === 0 ? 0 : 1);
