// Verifica el componente header.html aislado: franjas, beneficios, logo, controles, badge, consola limpia.
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const FILE = 'file:///C:/Users/usuario/dos-casas/tools/header-preview/header.html';
const b = await chromium.launch();
let fallos = 0;
const ok = (nombre, cond) => { console.log((cond ? 'OK ' : 'FALLO ') + nombre); if (!cond) fallos++; };

for (const [nombre, vp] of [['desktop-1440', { width: 1440, height: 500 }], ['movil-390', { width: 390, height: 500 }]]) {
  const page = await b.newPage({ viewport: vp });
  const errores = [];
  page.on('console', m => { if (m.type() === 'error') errores.push(m.text()); });
  page.on('pageerror', e => errores.push(String(e)));
  await page.goto(FILE, { waitUntil: 'networkidle', timeout: 30000 });

  const r = await page.evaluate(() => {
    const vis = el => el && el.getClientRects().length > 0;
    const beneficios = [...document.querySelectorAll('.benefit')];
    const cart = document.querySelector('.cart-btn');
    return {
      barras: vis(document.querySelector('.benefits-bar')) && vis(document.querySelector('.main-bar')),
      beneficios: beneficios.length === 3 && beneficios.every(x => vis(x.querySelector('svg'))),
      textosMovil: beneficios.map(x => getComputedStyle(x.querySelector('span')).display),
      logo: vis(document.querySelector('.brand .drop')) && document.querySelector('.wordmark').textContent.replace(/\s/g, '') === 'ESSENCIALUXXE',
      controles: [...document.querySelectorAll('.icon-btn')].length === 3 && [...document.querySelectorAll('.icon-btn')].every(vis),
      badge: cart.dataset.count === '0' && getComputedStyle(cart, '::after').content.includes('attr') === false,
      arias: ['Buscar', 'Carrito', 'Menú'].every(a => document.querySelector(`[aria-label="${a}"]`)),
      alturaTop: document.querySelector('.benefits-bar').offsetHeight,
      alturaMain: document.querySelector('.main-bar').offsetHeight,
      fuente: getComputedStyle(document.querySelector('.wordmark')).fontFamily,
    };
  });

  console.log(`\n=== ${nombre} ===`);
  ok('dos franjas visibles', r.barras);
  ok('3 beneficios con icono', r.beneficios);
  ok('logo gota + wordmark ESSENCIA LUXXE', r.logo);
  ok('3 controles (lupa/carrito/menu)', r.controles);
  ok('badge carrito = 0', r.badge);
  ok('aria-labels Buscar/Carrito/Menu', r.arias);
  ok('altura franjas ~40/~68', Math.abs(r.alturaTop - 40) <= 2 && Math.abs(r.alturaMain - 68) <= 2);
  ok('fuente Cormorant en wordmark', /Cormorant/i.test(r.fuente));
  if (nombre.startsWith('movil')) ok('textos de beneficios ocultos en movil', r.textosMovil.every(d => d === 'none'));
  else ok('textos de beneficios visibles en desktop', r.textosMovil.every(d => d !== 'none'));
  ok('0 errores de consola', errores.length === 0);
  if (errores.length) console.log('  errores:', errores);

  await page.screenshot({ path: `C:/Users/usuario/dos-casas/tools/header-preview/cap-header-${nombre}.png` });
  await page.close();
}

await b.close();
console.log('\nRESULTADO FINAL:', fallos === 0 ? 'TODO OK' : `${fallos} FALLOS`);
process.exit(fallos === 0 ? 0 : 1);
