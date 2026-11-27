const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + path.resolve(__dirname, '../index.html'));
  await p.waitForTimeout(800);
  const r = await p.evaluate(() => {
    const tl = window.__timelines.main; const out = { dur: tl.duration() };
    const q = s => { const e = document.querySelector(s); const cs = getComputedStyle(e); return [cs.opacity, cs.visibility, e.style.transform, cs.clipPath].join(' | '); };
    for (const t of [3.6, 6.9, 11.5, 13.8]) { tl.seek(t); out[t] = { slash: q('#hookSlash'), bslash: q('#bSlash'), signup0: q('#v_signup0'), hobbies: q('#v_hobbies'), k1: q('#k1'), k2: q('#k2') }; }
    return out;
  });
  console.log(JSON.stringify(r, null, 1)); console.log('errors', errs);
  await b.close();
})();
