// Prueba el modal de ficha rediseÃ±ado (foto | info) y saca capturas.
// Requiere tools/serve-secure.py en :8891.
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const csp = [], errores = [];
const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 1280, height: 900 } });
page.on('console', m => {
  if (m.text().includes('Content Security Policy')) csp.push(m.text());
  if (m.type() === 'error') errores.push(m.text());
});
page.on('pageerror', e => errores.push(String(e)));

await page.goto('http://localhost:8891/index.html', { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForSelector('#catGrid .pc');

// 1) clic en la foto de un perfume -> modal con foto + tagline + resumen
await page.click('#catGrid .pc-img[data-fh]');
await page.waitForSelector('.fmodal.show', { timeout: 5000 });
const tag = await page.textContent('.fmodal .fm-tag').catch(() => null);
const res = await page.textContent('.fmodal .fm-res').catch(() => null);
const foto = await page.getAttribute('.fmodal .fm-photo img', 'src').catch(() => null);
console.log('PERFUME modal -> foto:', foto, '| tagline:', tag, '| resumen:', (res || '').slice(0, 90) + '...');
await page.waitForTimeout(450); await page.screenshot({ path: 'tools/cap-modal-perfume.png' });

// 2) clic en la foto del modal -> lightbox por encima
await page.click('.fmodal .fm-photo');
await page.waitForSelector('#lightbox.show', { timeout: 5000 });
const lbVisible = await page.isVisible('#lightbox img');
console.log('Lightbox sobre el modal:', lbVisible);
await page.waitForTimeout(450); await page.screenshot({ path: 'tools/cap-lightbox-sobre-modal.png' });
await page.keyboard.press('Escape'); // cierra lightbox
await page.waitForTimeout(400);
await page.keyboard.press('Escape'); // cierra modal
await page.waitForTimeout(400);

// 3) ficha SETASOULS desde la foto
await page.click('#natGrid [data-fh-nat]');
await page.waitForSelector('.fmodal.show', { timeout: 5000 });
const tagN = await page.textContent('.fmodal .fm-tag').catch(() => null);
const haceN = await page.textContent('.fmodal .fm-res').catch(() => null);
const filas = await page.$$eval('.fmodal .fm-row b', els => els.map(e => e.textContent));
console.log('HONGO modal -> frase:', tagN, '| hace:', (haceN || '').slice(0, 80) + '...', '| filas:', filas.join(', '));
await page.waitForTimeout(450); await page.screenshot({ path: 'tools/cap-modal-hongo.png' });
await page.keyboard.press('Escape');
await page.waitForTimeout(400);

// 4) boton "Ficha tÃ©cnica" sigue funcionando + un perfume sin piramide
await page.click('#catGrid .ficha-btn');
await page.waitForSelector('.fmodal.show', { timeout: 5000 });
console.log('Boton Ficha tecnica abre modal: si');
await page.keyboard.press('Escape');
await page.waitForTimeout(400);

// 5) mobile
await page.setViewportSize({ width: 390, height: 844 });
await page.click('#catGrid .pc-img[data-fh]');
await page.waitForSelector('.fmodal.show', { timeout: 5000 });
await page.waitForTimeout(450); await page.screenshot({ path: 'tools/cap-modal-mobile.png' });

console.log('Errores JS:', errores.length, errores.slice(0, 3));
console.log('Violaciones CSP:', csp.length, csp.slice(0, 2));
await b.close();
console.log('RESULTADO:', (!errores.length && !csp.length && tag && res && tagN) ? 'TODO OK' : 'REVISAR');

