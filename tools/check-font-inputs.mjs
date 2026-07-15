// Chequea que los campos de busqueda tengan >=16px en movil (evita el auto-zoom del teclado).
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const URL = process.env.REPRO_URL || 'https://essencialuxxe.com';
const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
const fs = await page.evaluate(() => ({
  nav: getComputedStyle(document.getElementById('navSearch')).fontSize,
  cat: getComputedStyle(document.getElementById('catSearch')).fontSize
}));
await b.close();
console.log('font-size navSearch:', fs.nav, '| catSearch:', fs.cat);
console.log('RESULTADO:', (parseFloat(fs.nav) >= 16 && parseFloat(fs.cat) >= 16) ? 'TODO OK' : 'REVISAR');
