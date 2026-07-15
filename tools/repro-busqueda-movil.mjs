// Verifica la busqueda en movil (390x844): sin solape del header y resultados a la vista.
// REPRO_URL=http://localhost:8891/index.html para local; por defecto el sitio vivo.
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const URL = process.env.REPRO_URL || 'https://essencialuxxe.com';
const csp = [], errores = [];
const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
page.on('console', m => {
  if (m.text().includes('Content Security Policy')) csp.push(m.text());
  if (m.type() === 'error') errores.push(m.text());
});
page.on('pageerror', e => errores.push(String(e)));

await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForSelector('#catGrid .pc');

await page.screenshot({ path: 'tools/cap-mov-1-header.png' });

// tocar el buscador y escribir
await page.click('#navSearch');
await page.waitForTimeout(400);
await page.screenshot({ path: 'tools/cap-mov-2-focus.png' });
await page.fill('#navSearch', 'dior');
await page.waitForTimeout(500);
await page.screenshot({ path: 'tools/cap-mov-3-escrito.png' });

// ¿el campo se monta encima de la marca?
const solape = await page.evaluate(() => {
  const a = document.querySelector('.brand'), i = document.getElementById('navSearch');
  if (!a || !i) return null;
  const ra = a.getBoundingClientRect(), ri = i.getBoundingClientRect();
  const x = Math.max(0, Math.min(ra.right, ri.right) - Math.max(ra.left, ri.left));
  const y = Math.max(0, Math.min(ra.bottom, ri.bottom) - Math.max(ra.top, ri.top));
  return Math.round(x * y);
});

// esperar el auto-scroll y ver si los resultados quedaron a la vista
await page.waitForTimeout(1400);
await page.screenshot({ path: 'tools/cap-mov-4-resultados.png' });
const vista = await page.evaluate(() => {
  const meta = document.getElementById('catCount');
  const card = document.querySelector('#catGrid .pc');
  const vis = e => { if (!e) return false; const r = e.getBoundingClientRect(); return r.top < window.innerHeight && r.bottom > 0; };
  return { contador: vis(meta), contadorTxt: meta ? meta.textContent : null, primeraTarjeta: vis(card), scrollY: Math.round(window.scrollY) };
});

// al limpiar, la marca vuelve
await page.fill('#navSearch', '');
await page.evaluate(() => document.getElementById('navSearch').blur());
await page.waitForTimeout(400);
const marcaVuelve = await page.evaluate(() => {
  const bt = document.querySelector('.brand .bt');
  return bt && getComputedStyle(bt).display !== 'none';
});
await page.screenshot({ path: 'tools/cap-mov-5-limpio.png' });

console.log('solape marca/buscador (px2):', solape);
console.log('tras buscar:', JSON.stringify(vista));
console.log('marca vuelve al limpiar:', marcaVuelve);
console.log('Errores JS:', errores.length, errores.slice(0, 3));
console.log('Violaciones CSP:', csp.length, csp.slice(0, 2));
await b.close();
const ok = solape === 0 && vista.contador && vista.primeraTarjeta && marcaVuelve && !errores.length && !csp.length;
console.log('RESULTADO:', ok ? 'TODO OK' : 'REVISAR');
