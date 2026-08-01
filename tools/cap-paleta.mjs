// Captura secciones clave para revisar la paleta negro/dorado/blanco (sin verdes).
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const URL = process.env.REPRO_URL || 'http://localhost:8891/index.html';
const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errores = [];
page.on('console', m => { if (m.type() === 'error') errores.push(m.text()); });
await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });

for (const [nombre, sel] of [['features', '#features'], ['ritual', '#ritual'], ['footer', 'footer']]) {
  await page.locator(sel).scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);
  await page.screenshot({ path: `C:/Users/usuario/dos-casas/tools/cap-paleta-${nombre}.png` });
}

// abrir el carrito para ver overlay y drawer
await page.evaluate(() => window.scrollTo(0, 0));
await page.click('#cartBtn');
await page.waitForTimeout(700);
await page.screenshot({ path: 'C:/Users/usuario/dos-casas/tools/cap-paleta-carrito.png' });

console.log('errores de consola:', errores.length, errores.slice(0, 5));
await b.close();
