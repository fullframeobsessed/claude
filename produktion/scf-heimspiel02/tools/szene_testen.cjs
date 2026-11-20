// Einzelne Szene im Browser prüfen: node tools/szene_testen.cjs <szene> <sekunde>  (braucht gsap.min.js unter /tmp/claude-0/)
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const comp = process.argv[2], t = parseFloat(process.argv[3]);
  const src = fs.readFileSync(`compositions/${comp}.html`, 'utf8');
  const inner = src.replace(/^[\s\S]*?<template>/, '').replace(/<\/template>[\s\S]*$/, '');
  const html = `<!doctype html><html><head><script src="file:///tmp/claude-0/gsap.min.js"></script>
  <style>*{margin:0;padding:0;box-sizing:border-box} body{width:1080px;height:1920px;background:#300;position:relative;overflow:hidden}</style></head>
  <body><script>window.__timelines={};</script>${inner.replace(/<script>/, '<script>try{').replace(/<\/script>/, '}catch(e){document.title="ERR "+e.message}</script>')}
  <script>const tl=window.__timelines["${comp}"]; if(tl){tl.seek(${t}); document.title=(document.title||"ok")+" dur="+tl.duration().toFixed(2);}</script></body></html>`;
  fs.writeFileSync(process.cwd() + '/_h.html', html);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('pageerror', e.message));
  await p.goto('file://' + process.cwd() + '/_h.html'); await p.waitForTimeout(500);
  console.log(await p.title());
  const st = await p.evaluate(() => [...document.querySelectorAll('#root > div > div[id]')].slice(0, 6).map(e => e.id + ' op=' + getComputedStyle(e).opacity + ' tf=' + getComputedStyle(e).transform.slice(0, 60)));
  console.log(st.join('\n'));
  await p.screenshot({ path: '/tmp/claude-0/h_' + comp + '.png' }); await b.close();
})();
