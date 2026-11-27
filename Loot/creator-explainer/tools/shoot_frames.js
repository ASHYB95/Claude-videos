// Renders each <section class="frame"> of storyboard/frames.html to storyboard/fN.jpg
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(__dirname, '../storyboard/frames.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const ids = await p.$$eval('section.frame', s => s.map(x => x.id));
  for (const id of ids) {
    await (await p.$('#' + id)).screenshot({ path: path.resolve(__dirname, `../storyboard/${id}.jpg`), type: 'jpeg', quality: 88 });
  }
  await b.close(); console.log(ids.join(' '));
})();
