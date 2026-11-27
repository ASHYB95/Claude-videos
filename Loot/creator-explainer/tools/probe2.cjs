const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, '../index.html')); await p.waitForTimeout(800);
  const r = await p.evaluate(() => {
    const tl = window.__timelines.main; const q = s => { const e = document.querySelector(s); const cs = getComputedStyle(e); return [cs.opacity, cs.visibility, e.style.transform].join(' | '); };
    const o = {};
    tl.seek(60.25); tl.seek(10.5); o.after_end_10_5 = q('#v_signup0');
    tl.seek(0); for (let t = 0; t <= 11; t += 1 / 30) tl.seek(t); o.sequential_11 = q('#v_signup0');
    tl.progress(0); tl.pause(); tl.totalTime(11); o.totalTime = q('#v_signup0');
    return o;
  });
  console.log(r); await b.close();
})();
