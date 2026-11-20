// Render the continuous 6480×1350 strip in carousel.html into six 1080×1350 Instagram slides.
// Usage: node render.js            → out/gta6-01.png … out/gta6-06.png and out/strip.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 6480, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(__dirname, 'carousel.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(600);
  await p.screenshot({ path: path.join(__dirname, 'out', 'strip.png'), clip: { x: 0, y: 0, width: 6480, height: 1350 } });
  for (let i = 0; i < 6; i++) {
    const out = path.join(__dirname, 'out', 'gta6-' + String(i + 1).padStart(2, '0') + '.png');
    await p.screenshot({ path: out, clip: { x: i * 1080, y: 0, width: 1080, height: 1350 } });
    console.log(out);
  }
  await b.close();
})();
