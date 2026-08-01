// Capturas del menu compactado: 1440 arriba, 1440 con scroll (header claro), 1024 arriba.
import { chromium } from 'file:///C:/Users/usuario/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const URL = process.env.REPRO_URL || 'http://localhost:8891/index.html';
const b = await chromium.launch();

for (const [nombre, w, scroll] of [['1440-arriba', 1440, 0], ['1440-scroll', 1440, 600], ['1024-arriba', 1024, 0], ['990-arriba', 990, 0]]) {
  const page = await b.newPage({ viewport: { width: w, height: 400 } });
  const errores = [];
  page.on('console', m => { if (m.type() === 'error') errores.push(m.text()); });
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
  if (scroll) { await page.evaluate(s => window.scrollTo(0, s), scroll); await page.waitForTimeout(600); }
  const m = await page.evaluate(() => {
    const r = [...document.querySelectorAll('.brand, nav.links, .nav-r')].map(e => e.getBoundingClientRect());
    const links = [...document.querySelectorAll('nav.links a')];
    return {
      solape: r[0].right > r[1].left || r[1].right > r[2].left,
      desborde: document.documentElement.scrollWidth > window.innerWidth,
      unaLinea: links.every(a => a.getBoundingClientRect().height < 30),
    };
  });
  console.log(`${nombre}: solape=${m.solape} desborde=${m.desborde} unaLinea=${m.unaLinea} erroresConsola=${errores.length}`);
  await page.screenshot({ path: `C:/Users/usuario/dos-casas/tools/cap-menu-${nombre}.png` });
  await page.close();
}
await b.close();
