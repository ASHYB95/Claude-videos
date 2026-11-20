// Render every <section class="slide"> in carousel.html to a 1080×1350 PNG, plus a side-by-side overview.
// Usage: node render.js   → out/gta6-01.png … out/gta6-06.png, out/strip.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(__dirname, 'carousel.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(600);
  const slides = await p.$$('section.slide');
  const files = [];
  for (let i = 0; i < slides.length; i++) {
    const out = path.join(__dirname, 'out', 'gta6-' + String(i + 1).padStart(2, '0') + '.png');
    await slides[i].screenshot({ path: out });
    files.push(out);
    console.log(out);
  }
  await b.close();
  // overview strip (slides side by side)
  require('child_process').execFileSync('ffmpeg', ['-v', 'error', '-y', ...files.flatMap(f => ['-i', f]),
    '-filter_complex', `hstack=inputs=${files.length}`, path.join(__dirname, 'out', 'strip.png')]);
})();
