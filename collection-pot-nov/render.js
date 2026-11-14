// Render every <section class="slide"> in an HTML file to PNGs (1080×1350).
// Usage: node render.js c1-awkward-reminder.html out/c1/c1
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [file, prefix] = process.argv.slice(2);
  fs.mkdirSync(path.dirname(prefix), { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(file));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const slides = await p.$$('section.slide');
  for (let i = 0; i < slides.length; i++) {
    const out = prefix + '-' + String(i + 1).padStart(2, '0') + '.png';
    await slides[i].screenshot({ path: out });
    console.log(out);
  }
  await b.close();
})();
