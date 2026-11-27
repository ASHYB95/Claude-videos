const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2080, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(__dirname, '../storyboard/sheet.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: path.resolve(__dirname, '../storyboard/storyboard.jpg'), fullPage: true, type: 'jpeg', quality: 86 });
  await b.close();
})();
