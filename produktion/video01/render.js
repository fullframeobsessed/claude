// node render.js <dir>  -> rendert alle *.svg in <dir> zu *.png (1920x1080)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg')).sort()) {
    await p.setContent(`<html><body style="margin:0">${fs.readFileSync(path.join(dir, f), 'utf8')}</body></html>`);
    await p.locator('svg').first().screenshot({ path: path.join(dir, f.replace('.svg', '.png')) });
  }
  await b.close();
})();
