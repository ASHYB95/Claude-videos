const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  const ctx = await b.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 2 });
  await ctx.route(/googletagmanager|google-analytics|doubleclick|hotjar|facebook/, r => r.fulfill({ status: 200, contentType: 'application/javascript', body: '' }));
  await ctx.route(/collectionpot\.com\/_next\/static\/chunks\//, async r => {
    try {
      const body = execFileSync('curl', ['-sS', '-g', '--fail', r.request().url()], { maxBuffer: 1 << 26 });
      await r.fulfill({ status: 200, contentType: 'application/javascript', body });
    } catch (e) { await r.continue(); }
  });
  const p = await ctx.newPage();
  let n = 0;
  const snap = async (tag) => {
    await p.waitForTimeout(1200);
    n += 1;
    await p.screenshot({ path: (process.env.OUT || '.') + '/flow_' +String(n).padStart(2, '0') + '_' + tag + '.png' });
    console.log(n, tag, p.url());
  };
  const texts = async () => (await p.$$eval('button, a, h1, h2, h3, label, p', e => e.map(x => x.innerText.trim()).filter(Boolean))).slice(0, 40).join(' | ');
  await p.goto('https://app.collectionpot.com/create-a-pot', { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await snap('occasion');
  const info = await p.evaluate(() => {
    const els = [...document.querySelectorAll('button, label, [role=button], div, span')].filter(e => e.innerText && e.innerText.trim() === 'Leaver' && e.getBoundingClientRect().y > 250 && e.getBoundingClientRect().width > 0);
    const el = els.sort((a, b) => a.innerText.length - b.innerText.length)[0];
    if (!el) return 'none';
    const t = el.closest('button,label,[role=button]') || el; t.scrollIntoView({ block: 'center' });
    const r = t.getBoundingClientRect(); return [t.tagName, r.x + r.width / 2, r.y + r.height / 2];
  });
  console.log('leaver target', info);
  if (info !== 'none') await p.mouse.click(info[1], info[2]);
  await snap('leaver_selected');
  for (let step = 0; step < 6; step++) {
    const next = p.getByRole('button', { name: /next|continue/i });
    if (!(await next.count())) break;
    console.log('TEXT:', (await texts()).slice(0, 600));
    const pick = await p.evaluate(() => {
      const want = [/^chipping in money is optional$/i, /^someone else$/i, /^send to someone else$/i, /^for someone else$/i, /^skip$/i];
      const all = [...document.querySelectorAll('button, label, [role=button], [role=radio], div, span')].filter(e => { const r = e.getBoundingClientRect(); return r.y > 120 && r.width > 0 && r.y < 900; });
      for (const w of want) {
        const el = all.filter(e => w.test((e.innerText || '').replace(/​/g, '').trim())).sort((a, b) => a.innerText.length - b.innerText.length)[0];
        if (el) { const t = el.closest('button,label,[role=button],[role=radio]') || el; const r = t.getBoundingClientRect(); return [w.source, r.x + r.width / 2, r.y + r.height / 2]; }
      }
      return null;
    });
    if (pick) { console.log('pick', pick[0]); await p.mouse.click(pick[1], pick[2]); await p.waitForTimeout(500); }
    for (const inp of await p.$$('input[type=text]:visible, input:not([type]):visible, textarea:visible')) {
      const v = await inp.inputValue();
      if (!v) await inp.fill('Sarah').catch(() => {});
    }
    await snap('step' + step + '_filled');
    await p.evaluate(() => { const bt = [...document.querySelectorAll('button')].find(e => /^(next|continue)$/i.test(e.innerText.trim()) && !e.disabled); if (bt) bt.click(); });
    await snap('step' + step + '_after');
    if (/signup|register|login|account/i.test(p.url())) { console.log('reached account step, stopping'); break; }
  }
  console.log('FINAL TEXT:', (await texts()).slice(0, 600));
  await b.close();
})();
