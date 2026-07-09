// Verifica que el catalogo funciona 100% local:
// - ninguna peticion sale a cdn.shopify.com / perfumesimperial.com.co
// - las fotos de las tarjetas cargan (naturalWidth > 0) y son locales
// - clic en la foto abre el lightbox (no navega fuera)
// - 0 violaciones CSP
// Requiere tools/serve-secure.py corriendo en :8891.
// Correr:  node tools/verificar-fotos-locales.mjs   (usa el playwright de la cache de npx)
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const URL = 'http://localhost:8891/index.html';
const externas = [], csp = [];

const b = await chromium.launch();
const page = await b.newPage();
page.on('request', r => {
  const u = r.url();
  if (u.includes('cdn.shopify.com') || u.includes('perfumesimperial')) externas.push(u);
});
page.on('console', m => { if (m.text().includes('Content Security Policy')) csp.push(m.text()); });

await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForSelector('#catGrid .pc');

const fotos = await page.$$eval('#catGrid .pc-img img',
  els => els.map(e => ({ src: e.getAttribute('src'), ok: e.complete && e.naturalWidth > 0 })));
const malas = fotos.filter(f => !f.ok);
const noLocales = fotos.filter(f => !(f.src || '').startsWith('assets/img/perfumes/'));
console.log(`Tarjetas visibles: ${fotos.length} | rotas: ${malas.length} | no locales: ${noLocales.length}`);
[...malas, ...noLocales].slice(0, 5).forEach(f => console.log('  ', JSON.stringify(f)));

const urlAntes = page.url();
await page.click('#catGrid .pc-img[data-zoom]');
await page.waitForSelector('#lightbox.show', { timeout: 5000 });
const lbSrc = await page.getAttribute('#lbImg', 'src');
console.log(`Lightbox abre: si | imagen: ${lbSrc.split('/').pop()} | navego fuera: ${page.url() !== urlAntes}`);
await page.keyboard.press('Escape');

// cargar mas productos (10 tandas de "Ver mas") y re-chequear
for (let i = 0; i < 10; i++) {
  const btn = await page.$('#catMore');
  if (!btn || !(await btn.isVisible())) break;
  await btn.click();
  await page.waitForTimeout(400);
}
await page.waitForTimeout(2500);
const fotos2 = await page.$$eval('#catGrid .pc-img img',
  els => els.map(e => e.complete && e.naturalWidth > 0));
console.log(`Tras 'Ver mas' x10: ${fotos2.length} tarjetas, rotas: ${fotos2.filter(x => !x).length}`);

console.log(`Peticiones externas a Imperial/Shopify: ${externas.length}`);
externas.slice(0, 5).forEach(u => console.log('  ', u));
console.log(`Violaciones CSP: ${csp.length}`);
csp.slice(0, 5).forEach(c => console.log('  ', c));
await b.close();

const ok = !externas.length && !csp.length && !malas.length && !noLocales.length;
console.log('RESULTADO:', ok ? 'TODO OK' : 'REVISAR');
process.exit(ok ? 0 : 1);
