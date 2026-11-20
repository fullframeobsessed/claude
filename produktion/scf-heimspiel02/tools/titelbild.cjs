// Titelbild rendern: node tools/titelbild.cjs  →  titelbild/titelbild_reel.png (1080x1920) + Vorschau der Raster-Ausschnitte
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.cwd() + '/titelbild/cover.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: 'titelbild/titelbild_reel.png' });
  await b.close();
})();
