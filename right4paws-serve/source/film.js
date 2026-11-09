// Right4Paws — How to Serve Ultimate Diet. 1080×1920, 24 fps, ♩ = 120 (beat 0.5 s, bar 2 s). Brand colours.
import { setClock, shape, ink, plane, ellipse, rrect, rect, text, fit, measure, star, sparkle, rays, dashed, arrow,
  paperFinish, clamp, lerp, seg, ss, eo, eio, back, twos, rng, TAU } from './engine/toon.js';
import { C, tint, shade } from './engine/pal.js';
import { drawMango, mangoHeadPt } from './engine/mango.js';
import { drawHand, arm } from './engine/hands.js';
import { drawPack, drawBowl, flakeStream, drawScale, drawDial, drawJug, drawFork, steam, drawClock, drawMug, checker, halftone,
  drawLogoTab, drawLogoWhite } from './engine/props.js';

export const W = 1080, H = 1920, BEAT = 0.5;
export const SECTIONS = [
  { k: 'hook', t0: 0, t1: 4 }, { k: 'title', t0: 4, t1: 8 }, { k: 's1', t0: 8, t1: 16 }, { k: 's2', t0: 16, t1: 22 },
  { k: 's3', t0: 22, t1: 30 }, { k: 'quiet', t0: 30, t1: 32 }, { k: 'pay', t0: 32, t1: 34 }, { k: 'tip', t0: 34, t1: 36 }, { k: 'end', t0: 36, t1: 42 },
];
export const DUR = 42;
export const CUES = [
  { t0: 0.4, t1: 1.9, text: 'This is Mango.' },
  { t0: 2.0, t1: 3.9, text: 'And this… is dinner.' },
  { t0: 4.4, t1: 7.6, text: 'Here’s how to serve it, in three easy steps.' },
  { t0: 8.4, t1: 11.2, text: 'Step one. Weigh your dog.' },
  { t0: 11.6, t1: 15.6, text: 'Thirty kilos? Around 350 grams a day.' },
  { t0: 16.4, t1: 18.4, text: 'Step two. Measure it out.' },
  { t0: 18.6, t1: 21.6, text: 'One cup holds about 100 grams.' },
  { t0: 22.4, t1: 24.4, text: 'Step three. Serve it your way.' },
  { t0: 24.6, t1: 26.2, text: 'Dry, straight from the pack.' },
  { t0: 26.4, t1: 28.4, text: 'Sprinkle on warm water, for extra flavour and aroma.' },
  { t0: 28.6, t1: 29.9, text: 'Or mash it.' },
  { t0: 33.0, t1: 36.6, text: 'Pro tip: it’s more nutrient-dense than kibble, so you’ll feed less.' },
  { t0: 37.0, t1: 40.0, text: 'Right4Paws Ultimate Diet. Raw, made right.' },
];

const pop = (t, t0, d = 0.28) => back(seg(t, t0, t0 + d), 1.9);
const bg = (ctx, col) => { ctx.fillStyle = col; ctx.fillRect(-200, -200, W + 400, H + 400); };
const blinkAt = (t, every = 3.1, ph = 0) => ((t + ph) % every) < 0.12 ? 1 : 0;

// ---------------------------------------------------------------- shared furniture
function caption(ctx, t) {
  const cue = CUES.find(c => t >= c.t0 && t < c.t1); if (!cue) return;
  const a = Math.min(ss(seg(t, cue.t0, cue.t0 + 0.16)), 1 - ss(seg(t, cue.t1 - 0.16, cue.t1)));
  const f = fit(ctx, cue.text, '500 {px}px Jost', 44, 820, 2, 36);
  const lw = Math.max(...f.lines.map(l => measure(ctx, l, f.font)));
  const w = lw + 140, h = 46 + f.lines.length * f.px * 1.18, x = W / 2 - w / 2, y = 1640 - h;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, (1 - a) * 10);
  shape(ctx, rrect(x, y, w, h, 14), { fill: C.card, line: 3.4, seed: 901, grain: 0.15, breaks: 0.08, off: [5, 5] });
  star(ctx, x + 34, y + h / 2, 15, { n: 8, inner: 0.4, fill: C.red, off: [0, 0], rot: t * 0.8 });
  star(ctx, x + w - 34, y + h / 2, 15, { n: 8, inner: 0.4, fill: C.red, off: [0, 0], rot: -t * 0.8 });
  f.lines.forEach((l, i) => text(ctx, l, W / 2, y + 23 + f.px * 0.9 + i * f.px * 1.18, { font: f.font, fill: C.ink, align: 'center' }));
  ctx.restore();
}
// step header; on a red page it flips to cream
function stepHeader(ctx, t, t0, num, label, onRed = false) {
  const k = eo(seg(twos(t), t0 + 0.05, t0 + 0.4)); if (k <= 0) return;
  const fg = onRed ? C.card : C.ink, disc = onRed ? C.card : C.red, numc = onRed ? C.red : C.card;
  ctx.save(); ctx.translate(-(1 - k) * 700, 0);
  shape(ctx, ellipse(112, 222, 56, 56, 40), { fill: disc, line: 3.4, seed: 700, grain: 0.1 });
  text(ctx, String(num), 112, 246, { font: '66px Slab', fill: numc, align: 'center' });
  text(ctx, `STEP ${num} OF 3`, 192, 194, { font: '600 24px Jost', fill: fg, track: 6 });
  const f = fit(ctx, label, '{px}px Slab', 64, 840, 1, 40);
  text(ctx, f.lines[0], 190, 264, { font: f.font, fill: fg, plate: onRed ? C.ink : C.redT, off: [4, 4] });
  ctx.restore();
}
function tag(ctx, t, t0, str, x, y, o = {}) {
  const k = pop(t, t0); if (k <= 0) return;
  const f = fit(ctx, str, '600 {px}px Jost', o.px || 38, o.maxW || 600, 2, 26);
  const w = Math.max(...f.lines.map(l => measure(ctx, l, f.font))) + 100, h = 32 + f.lines.length * f.px * 1.2;
  const X = o.align === 'right' ? x - w : o.align === 'center' ? x - w / 2 : x;
  ctx.save(); ctx.translate(X + w / 2, y + h / 2); ctx.scale(k, k); ctx.translate(-(X + w / 2), -(y + h / 2));
  shape(ctx, rrect(X, y, w, h, 14), { fill: C.card, line: 3.6, seed: 710, grain: 0.15, off: [6, 5] });
  star(ctx, X + 40, y + h / 2, 18, { n: 8, inner: 0.42, fill: C.red, off: [0, 0], rot: t * 0.6 });
  f.lines.forEach((l, i) => text(ctx, l, X + 70, y + 16 + f.px * 0.92 + i * f.px * 1.2, { font: f.font, fill: C.ink }));
  ctx.restore();
}
function callout(ctx, t, t0, cx, cy, r, inner, bgc, leader) {
  const k = back(seg(t, t0, t0 + 0.32), 1.5); if (k <= 0) return;
  const R = r * k;
  if (leader) {
    const a = Math.atan2(leader[1] - cy, leader[0] - cx);
    dashed(ctx, [[cx + Math.cos(a) * (R + 14), cy + Math.sin(a) * (R + 14)], leader], 4, 14, 10, -t * 40, C.ink, clamp(k));
    shape(ctx, ellipse(leader[0], leader[1], 9, 9, 12), { fill: C.ink, line: 0, off: [0, 0], grain: 0 });
  }
  shape(ctx, ellipse(cx, cy, R + 16, R + 16, 72), { fill: C.card, line: 4.5, seed: 720, grain: 0.15, breaks: 0.05 });
  ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.clip();
  ctx.fillStyle = bgc; ctx.fillRect(cx - R, cy - R, 2 * R, 2 * R);
  ctx.translate(cx, cy); ctx.scale(k, k); inner(ctx); ctx.restore();
  ink(ctx, ellipse(cx, cy, R, R, 72), 4, { closed: true, seed: 721, breaks: 0.1 });
}
function medallion(ctx, t, tStamp, x, y, i, r = 78) {
  const k = pop(t, tStamp, 0.24); if (k <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(k, k); ctx.rotate((1 - k) * 0.4);
  star(ctx, 0, 0, r * 1.22, { n: 16, inner: 0.84, fill: C.card, off: [0, 0], rot: i * 0.2 });
  shape(ctx, ellipse(0, 0, r, r, 64), { fill: C.redT, line: 5, seed: 730 + i, grain: 0.3 });
  text(ctx, String(i + 1), 0, r * 0.38, { font: `${Math.round(r * 1.1)}px Slab`, fill: C.ink, plate: C.red, off: [5, 5], align: 'center' });
  ctx.restore();
}
const dust = (ctx, x, y, u, n = 5) => { if (u <= 0 || u >= 1) return; for (let i = 0; i < n; i++) { const a = Math.PI + (i + 0.5) * Math.PI / n; shape(ctx, ellipse(x + Math.cos(a) * (60 + u * 90), y - 10 + Math.sin(a) * 30 * u, 16 * (1 - u), 11 * (1 - u), 12), { fill: C.card, line: 2.4, seed: 940 + i, grain: 0 }); } };
const impact = (ctx, x, y, u) => { if (u <= 0 || u >= 1) return; for (let i = 0; i < 6; i++) { const a = -Math.PI + (i + 0.5) * Math.PI / 6, r0 = 40 + u * 50; ink(ctx, [[x + Math.cos(a) * r0, y + Math.sin(a) * r0 * 0.5], [x + Math.cos(a) * (r0 + 40), y + Math.sin(a) * (r0 + 40) * 0.5]], 5, { seed: 950 + i, alpha: 1 - u }); } };

// ---------------------------------------------------------------- 0–4 HOOK: Mango drops his empty bowl; the pack thumps down
const HK = { mx: 520, my: 1340, ms: 1.12, FY: 1450 };
function sceneHook(ctx, t) {
  const u = t, z = lerp(1, 1.05, ss(u / 4));
  ctx.save(); ctx.translate(540, 1150); ctx.scale(z, z); ctx.translate(-540, -1150);
  bg(ctx, C.paper);
  halftone(ctx, 1010, 260, 40, 430, C.greyD, 0.5);
  checker(ctx, 1290, W, H + 200);
  [[150, 420, 24], [420, 300, 16], [880, 760, 20]].forEach(([x, y, r], i) => sparkle(ctx, x, y, r, { fill: C.red, rot: i * 0.4, alpha: 0.85 }));
  const hold = u < 0.5, landed = u >= 2.0;
  const mo = { s: HK.ms, dir: -1, head: hold ? 0.22 : lerp(0.22, 0, ss(seg(u, 0.5, 0.8))), mouth: hold ? 'open' : 'grin',
    tail: Math.sin(twos(t) * (landed ? 15 : 8)) * 0.14, ear: landed ? 1 : 0, look: u > 1.75 ? [8, -6] : [0, 0], blink: blinkAt(t, 2.9, 1.0), brow: landed ? 0.6 : 0 };
  drawMango(ctx, HK.mx, HK.my, mo);
  // the bowl: in his mouth, dropped at 0.5, lands at 0.75 (clang), little bounce
  const rx = 118, restRim = HK.FY - 92, restX = 250;
  if (hold) {
    const m = mangoHeadPt(HK.mx, HK.my, mo, [150, -384]);
    ctx.save(); ctx.translate(m[0], m[1]); ctx.rotate(0.42); drawBowl(ctx, -rx * 0.92, 18, { rx, seed: 640 }); ctx.restore();
  } else {
    const m = mangoHeadPt(HK.mx, HK.my, { ...mo, head: 0.22 }, [150, -384]);
    const k = ss(seg(u, 0.5, 0.75)), b = u > 0.75 ? Math.sin(seg(u, 0.75, 1.0) * Math.PI) * 22 : 0;
    const x = lerp(m[0] - rx * 0.92 * Math.cos(0.42), restX, k), y = lerp(m[1] + 40, restRim, k * k) - b;
    ctx.save(); ctx.translate(x, y); ctx.rotate(lerp(0.42, 0, k)); drawBowl(ctx, 0, 0, { rx, seed: 640 }); ctx.restore();
    impact(ctx, restX, restRim + 80, seg(u, 0.75, 1.05));
  }
  // the pack falls 1.7–2.0 and lands on the beat (thump), squash + dust
  if (u >= 1.7) {
    const pk = Math.pow(seg(u, 1.7, 2.0), 2), sq = landed ? Math.sin(seg(u, 2.0, 2.25) * Math.PI) * 0.08 : 0;
    ctx.save(); ctx.translate(845, lerp(-120, HK.FY + 10, pk)); ctx.scale(1 + sq, 1 - sq); drawPack(ctx, 0, 0, { s: 0.95 }); ctx.restore();
    dust(ctx, 845, HK.FY + 10, seg(u, 2.0, 2.4));
  }
  ctx.restore();
}

// ---------------------------------------------------------------- 4–8 TITLE: red card, the pack on a starburst, ① ② ③ stamp on
const MED = [[300, 1420], [540, 1420], [780, 1420]];
function sceneTitle(ctx, t) {
  bg(ctx, C.red);
  rays(ctx, 540, 1060, 30, 1700, C.card, { rot: t * 0.05, alpha: 0.12 });
  const kw = ss(seg(t, 4.3, 4.9));
  ctx.save(); ctx.beginPath(); ctx.rect(0, 300, 270 + 560 * kw, 200); ctx.clip();
  text(ctx, 'Let’s learn', 540, 440, { font: '700 110px Oleo', fill: C.card, plate: C.redD, off: [5, 5], align: 'center' });
  ctx.restore();
  const k1 = pop(t, 4.6);
  if (k1 > 0) { ctx.save(); ctx.translate(540, 560); ctx.scale(k1, k1); text(ctx, 'HOW TO SERVE', 0, 40, { font: '104px Slab', fill: C.card, plate: C.ink, off: [6, 6], align: 'center', maxW: 960 }); ctx.restore(); }
  const k2 = pop(t, 5.0);
  if (k2 > 0) {
    ctx.save(); ctx.translate(540, 690); ctx.scale(k2, k2);
    shape(ctx, rrect(-270, -52, 540, 96, 48), { fill: C.card, line: 4, seed: 760, grain: 0.15 });
    text(ctx, 'Ultimate Diet', 0, 20, { font: '60px Slab', fill: C.red, align: 'center' });
    ctx.restore();
  }
  const k3 = pop(t, 4.8, 0.35);
  if (k3 > 0) {
    ctx.save(); ctx.translate(540, 1050); ctx.scale(k3, k3);
    star(ctx, 0, 0, 300, { n: 18, inner: 0.84, fill: C.card, rot: t * 0.1 });
    ink(ctx, ellipse(0, 0, 250, 250, 60), 3, { closed: true, seed: 761, breaks: 0.4 });
    ctx.restore();
    const b = back(seg(t, 5.0, 5.35), 2.2);
    if (b > 0) drawPack(ctx, 525, 1235 - (1 - b) * 60, { s: 1.12 * b });
  }
  MED.forEach(([x, y], i) => medallion(ctx, t, 6.0 + i * 0.5, x, y, i));
}

// ---------------------------------------------------------------- 8–16 STEP 1: weigh your dog
function sceneWeigh(ctx, t) {
  const u = t - 8;
  bg(ctx, C.grey);
  halftone(ctx, 70, 560, 30, 380, C.greyD, 0.7);
  checker(ctx, 1290, W, H);
  drawClock(ctx, 820, 470, 62, t);
  [[180, 420, 22], [660, 330, 16], [950, 760, 20]].forEach(([x, y, r], i) => sparkle(ctx, x, y, r, { fill: C.red, rot: i * 0.4, alpha: 0.85 }));
  // the needle: swings on landing (10.0), creeps in the silence, settles on 30 at 13.0 (ding)
  const kg = u < 2 ? 0 : u < 3.8 ? 30 + Math.sin((u - 2) * 9) * 16 * (1 - seg(u, 2, 3.8)) - 3 * seg(u, 2, 3.8) : u < 5 ? lerp(27, 30, ss(seg(u, 3.8, 5))) : 30;
  const sc = drawScale(ctx, 110, 1250, { w: 450, kg });
  // Mango: sits right, hops at 9.75–10.0 onto the scale, turns mid-air
  let mx = 840, my = 1370, dir = -1, sq = 0;
  if (u >= 1.5 && u < 1.75) sq = ss(seg(u, 1.5, 1.75));
  if (u >= 1.75 && u < 2.0) { const k = seg(u, 1.75, 2.0); mx = lerp(840, 335, k); my = lerp(1370, 1232, k) - Math.sin(k * Math.PI) * 200; dir = k < 0.5 ? -1 : 1; sq = -0.4; }
  if (u >= 2.0) { mx = 335; my = 1232; dir = 1; sq = Math.max(0, 1 - seg(u, 2.0, 2.25) * 1) * (u < 2.25 ? 1 : 0); }
  drawMango(ctx, mx, my, { s: 1.06, dir, squash: sq, tail: Math.sin(twos(t) * (u > 5 ? 14 : 8)) * 0.12, mouth: u > 5 ? 'grin' : 'smile', ear: u > 5 ? 1 : 0,
    brow: u > 3.8 && u < 5 ? -0.4 : 0.2, look: u > 2.4 && u < 5 ? [4, 6] : [0, 0], blink: blinkAt(t, 3.1) });
  callout(ctx, t, 10.4, 800, 1030, 165, g => drawDial(g, kg, 132), C.redT, [sc.dial[0] + 60, sc.dial[1] - 10]);
  if (u >= 5 && u < 5.5) star(ctx, 800, 900, 40 + seg(u, 5, 5.5) * 30, { n: 8, inner: 0.35, fill: C.red, alpha: 1 - seg(u, 5, 5.5), off: [0, 0] });
  tag(ctx, t, 13.0, '30 kg dog ≈ 350 g a day', 1040, 1350, { align: 'right', px: 36 });
  stepHeader(ctx, t, 8, 1, 'Weigh your dog');
}

// ---------------------------------------------------------------- 16–22 STEP 2: measure it out
function sceneMeasure(ctx, t) {
  const u = t - 16;
  bg(ctx, C.paper);
  halftone(ctx, 1000, 640, 30, 420, C.greyD, 0.55);
  // the counter: red top, grey front
  plane(ctx, rect(0, 1330, W, H - 1330), C.greyD);
  shape(ctx, rect(-20, 1290, W + 40, 44), { fill: C.red, line: 4, seed: 801, grain: 0.25 });
  // pack, open
  drawPack(ctx, 300, 1300, { s: 1.3, open: 1 });
  // mug path: in (16.4–17.0), dip (17.0–17.5), lift heaped (17.5–18.1), level (19.0–19.3)
  let mx, my, heap = 0, rot = 0;
  if (u < 0.4) { mx = 1300; my = 760; }
  else if (u < 1.0) { const k = eio(seg(u, 0.4, 1.0)); mx = lerp(1300, 330, k); my = 760; rot = -0.1 * k; }
  else if (u < 1.5) { const k = ss(seg(u, 1.0, 1.5)); mx = 330; my = lerp(760, 1010, Math.sin(k * Math.PI)); rot = -0.1; heap = k > 0.5 ? 1 : 0; }
  else if (u < 2.1) { const k = eio(seg(u, 1.5, 2.1)); mx = lerp(330, 640, k); my = lerp(760, 900, k); rot = lerp(-0.1, 0, k); heap = 1; }
  else { mx = 640; my = 900; heap = u < 3.0 ? 1 : lerp(1, 0.32, ss(seg(u, 3.0, 3.3))); }
  ctx.save();
  if (u >= 1.0 && u < 1.5) { ctx.beginPath(); ctx.rect(0, 0, W, 905); ctx.clip(); }
  if (u >= 0.4) {
    arm(ctx, [[W + 80, my - 60], [mx + 260, my - 70], [mx + 150, my - 100]], 'grip', { k: 1.8, side: -1, seed: 830, handA: Math.PI + 0.1 });
    drawMug(ctx, mx, my, { s: 1.0, rot, heap, seed: 780 });
  }
  ctx.restore();
  // the level flick: a pointing finger sweeps across the rim, flakes fly
  if (u >= 2.8 && u < 3.6) {
    const k = eio(seg(u, 2.9, 3.3)), fx = lerp(mx - 160, mx + 120, k);
    arm(ctx, [[-120, my - 420], [fx - 200, my - 330], [fx - 60, my - 205]], 'point', { k: 1.6, side: 1, seed: 860, handA: 0.15 });
    const R = rng(99);
    for (let i = 0; i < 7; i++) { const f = seg(u, 3.05, 3.6); if (f <= 0 || f >= 1) continue; const x = mx + 80 + f * (120 + R() * 140), y = my - 220 - Math.sin(f * Math.PI) * (60 + R() * 60) + f * f * 160;
      shape(ctx, [[x - 9, y], [x, y - 5], [x + 10, y + 1], [x + 1, y + 6]], { fill: C.flakeL, line: 1.6, seed: 870 + i, grain: 0 }); }
  }
  callout(ctx, t, 19.3, 290, 600, 170, g => {
    shape(g, rrect(-92, -128, 184, 150, 12), { fill: C.red, line: 4, seed: 880, grain: 0.2 });
    text(g, '250', 0, -48, { font: '72px Slab', fill: C.card, align: 'center' });
    text(g, 'ml', 0, 4, { font: '700 34px Jost', fill: C.card, align: 'center' });
    text(g, '≈ 100 g', 0, 108, { font: '62px Slab', fill: C.ink, plate: C.card, off: [4, 4], align: 'center' });
  }, C.redT, [mx - 30, my - 110]);
  tag(ctx, t, 19.6, '1 cup (250 ml) ≈ 100 g of flakes', 540, 1380, { align: 'center', px: 36 });
  stepHeader(ctx, t, 16, 2, 'Measure it out');
}

// ---------------------------------------------------------------- 22–30 STEP 3: serve it your way (split frame)
const BANDS = [
  { y: 340, col: C.paper, label: 'DRY', sub: 'straight from the pack', food: 'dry', on: 24.6 },
  { y: 720, col: C.redT, label: 'SOFT', sub: 'sprinkle warm water', food: 'soft', on: 26.4 },
  { y: 1100, col: C.grey, label: 'MASHED', sub: 'mash it with a fork', food: 'mash', on: 28.6 },
];
function sceneServe(ctx, t) {
  bg(ctx, C.red);
  rays(ctx, 540, 960, 30, 1500, C.card, { rot: t * 0.04, alpha: 0.08 });
  const BH = 380, X0 = 40, BW = W - 80, s0 = 22;
  BANDS.forEach((b, i) => {
    const slide = eo(seg(twos(t), s0 + 0.35 + i * 0.25, s0 + 0.85 + i * 0.25));
    if (slide <= 0) return;
    const active = t >= b.on, done = t >= b.on + 1.2;
    ctx.save(); ctx.translate((1 - slide) * (i % 2 ? W : -W), 0);
    ctx.save(); ctx.beginPath(); ctx.rect(X0, b.y, BW, BH); ctx.clip();
    shape(ctx, rect(X0, b.y, BW, BH), { fill: b.col, line: 0, seed: 820 + i, grain: 0.3, off: [0, 0] });
    plane(ctx, rect(X0, b.y + BH * 0.74, BW, BH * 0.26), shade(b.col, 0.1));
    const la = active ? 1 : 0.4;
    text(ctx, b.label, 84, b.y + 118, { font: '74px Slab', fill: C.red, plate: C.ink, off: [5, 5], alpha: la });
    text(ctx, b.sub.toUpperCase(), 88, b.y + 166, { font: '600 22px Jost', fill: C.ink, track: 3, alpha: la });
    const bx = 690, rimY = b.y + 238, u = clamp((t - b.on) / 1.2);
    drawBowl(ctx, bx, rimY, { rx: 140, food: b.food === 'dry' ? 'dry' : (active ? b.food : 'dry'), fill: b.food === 'dry' ? (active ? u : 0) : 1, seed: 640 + i * 40 });
    if (b.food === 'dry' && active && !done) {
      drawPack(ctx, 862, b.y + 74, { s: 0.46, rot: -2.1, open: 1 });
      arm(ctx, [[W + 60, b.y + 190], [1010, b.y + 150], [930, b.y + 112]], 'grip', { k: 1.7, side: 1, seed: 870 });
      flakeStream(ctx, [736, b.y + 150], [bx - 10, rimY - 40], t, 14, 900);
    } else if (b.food === 'dry') drawPack(ctx, 440, b.y + 340, { s: 0.44 });
    if (b.food === 'soft' && active) {
      steam(ctx, bx, rimY - 70, t, 3, 120, C.red);
      if (!done) {
        arm(ctx, [[W + 60, b.y + 40], [980, b.y + 60], [900, b.y + 96]], 'grip', { k: 1.7, side: -1, seed: 830 });
        drawJug(ctx, 850, b.y + 150, -0.75, 0.72);
        for (let d = 0; d < 7; d++) {
          const ph = ((t * 1.8 + d / 7) % 1), x = 735 - ph * 40 + (d % 2) * 10, y = b.y + 128 + ph * 70;
          shape(ctx, [[x, y - 14], [x + 6, y - 2], [x + 5, y + 5], [x, y + 8], [x - 5, y + 5], [x - 6, y - 2]], { fill: '#CFE3EA', line: 2.4, seed: 840 + d, grain: 0, alpha: 1 - ph * 0.3 });
        }
      }
    }
    if (b.food === 'mash' && active) {
      const press = Math.abs(Math.sin(twos(t) * Math.PI * 2)) * 18;
      drawFork(ctx, bx + 30, rimY - 70 + press, 0.5, 0.9);
      arm(ctx, [[W + 60, b.y + 60], [1010, b.y + 90], [890 + press * 0.3, b.y + 118 + press]], 'grip', { k: 1.7, side: -1, seed: 850 });
    }
    if (active) [[bx - 190, rimY - 120], [bx + 170, rimY - 150]].forEach(([x, y], j) => sparkle(ctx, x, y, 18 + j * 4, { fill: C.red, rot: t * 0.5 + j }));
    ctx.restore();
    ink(ctx, rect(X0, b.y, BW, BH), 4.2, { closed: true, seed: 860 + i, breaks: 0.12 });
    ctx.restore();
  });
  stepHeader(ctx, t, 22, 3, 'Serve it your way', true);
}

// ---------------------------------------------------------------- 30–34 the wait (silence), the clink, the dive
const QM = { x: 300, y: 1420, s: 1.3 };
function bowlSpot() { const p = mangoHeadPt(QM.x, QM.y, { s: QM.s, dir: 1, eat: 1 }, [196, -410]); return { cx: p[0] + 70, rimY: p[1] + 30 }; }
function sceneQuiet(ctx, t) {
  const u = t - 30, B = bowlSpot();
  bg(ctx, C.paper);
  halftone(ctx, 980, 420, 30, 400, C.greyD, 0.5);
  checker(ctx, 1240, W, H);
  // Mango: dead still, eyes on the bowl (on twos)
  const by = u < 1.6 ? lerp(620, B.rimY, ss(seg(twos(t), 30.0, 31.6))) : B.rimY;
  drawMango(ctx, QM.x, QM.y, { s: QM.s, dir: 1, ear: 1, look: [6, lerp(-6, 6, seg(by, 620, B.rimY))], mouth: 'smile', brow: 0.4 });
  drawBowl(ctx, B.cx, by, { rx: 150, food: 'mash', fill: 1, seed: 720 });
  if (u < 1.9) { const k = seg(u, 1.6, 1.9); arm(ctx, [[W + 80, by - 520 - k * 300], [B.cx + 250, by - 170 - k * 260], [B.cx + 162, by - 6 - k * 200]], 'grip', { k: 1.8, side: -1, seed: 890, handA: Math.PI - 0.35 }); }
  impact(ctx, B.cx, B.rimY + 110, seg(u, 1.6, 1.95));
}
function scenePay(ctx, t) {
  const u = t - 32, B = bowlSpot(), z = lerp(1, 1.04, ss(u / 2));
  ctx.save(); ctx.translate(540, 1250); ctx.scale(z, z); ctx.translate(-540, -1250);
  bg(ctx, C.paper);
  halftone(ctx, 980, 420, 30, 400, C.greyD, 0.5);
  checker(ctx, 1240, W, H + 100);
  const eat = u < 0.25 ? ss(seg(u, 0, 0.25)) : 0.92 + Math.sin(twos(t) * 18) * 0.08;
  drawMango(ctx, QM.x, QM.y, { s: QM.s, dir: 1, eat, ear: 1, tail: Math.sin(twos(t) * 16) * 0.2, blink: 1, mouth: 'smile' });
  drawBowl(ctx, B.cx, B.rimY, { rx: 150, food: 'mash', fill: lerp(1, 0.2, seg(u, 0.3, 1.9)), seed: 720 });
  [[0.4, 860, 820], [1.2, 260, 760]].forEach(([at, x, y], i) => {
    const k = pop(t, 32 + at, 0.2); if (k <= 0 || u > at + 0.7) return;
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(i ? -0.12 : 0.1);
    star(ctx, 0, 0, 130, { n: 14, inner: 0.7, fill: C.card, line: 4 });
    text(ctx, 'CRUNCH!', 0, 16, { font: '48px Slab', fill: C.red, plate: C.ink, off: [3, 3], align: 'center' });
    ctx.restore();
  });
  ctx.restore();
}

// ---------------------------------------------------------------- 34–36 PRO TIP: feed less
function sceneTip(ctx, t) {
  bg(ctx, C.red);
  halftone(ctx, 540, 960, 200, 900, C.card, 0.08);
  const kw = ss(seg(t, 34.25, 34.7));
  ctx.save(); ctx.beginPath(); ctx.rect(0, 280, 330 + 440 * kw, 160); ctx.clip();
  text(ctx, 'Pro tip', 540, 400, { font: '700 104px Oleo', fill: C.card, plate: C.redD, off: [5, 5], align: 'center' });
  ctx.restore();
  const k = pop(t, 34.3, 0.32); if (k <= 0) return;
  ctx.save(); ctx.translate(540, 900); ctx.scale(k, k); ctx.translate(-540, -900);
  shape(ctx, rrect(70, 470, 940, 860, 34), { fill: C.card, line: 4.5, seed: 960, grain: 0.15 });
  text(ctx, 'Feed less', 540, 600, { font: '76px Slab', fill: C.ink, plate: C.redT, off: [5, 5], align: 'center' });
  text(ctx, 'MORE NUTRIENT-DENSE THAN KIBBLE', 540, 660, { font: '600 26px Jost', fill: C.inkSoft, align: 'center', track: 3 });
  drawBowl(ctx, 300, 1010, { rx: 150, food: 'kibble', fill: 1.15, seed: 970 });
  drawBowl(ctx, 780, 1010, { rx: 150, food: 'dry', fill: 0.75, seed: 975 });
  text(ctx, 'KIBBLE', 300, 1180, { font: '600 28px Jost', fill: C.ink, align: 'center', track: 4 });
  text(ctx, 'RIGHT4PAWS', 780, 1180, { font: '600 28px Jost', fill: C.red, align: 'center', track: 4 });
  arrow(ctx, [380, 860], [700, 900], { u: ss(seg(t, 34.6, 35.0)), bend: -0.35, fill: C.red, w: 6, head: 32, bob: (t * 2) % 1 });
  ctx.restore();
  const kp = pop(t, 34.9);
  if (kp > 0) { ctx.save(); ctx.translate(540, 1255); ctx.scale(kp, kp);
    shape(ctx, rrect(-250, -46, 500, 92, 46), { fill: C.red, line: 4, seed: 980, grain: 0.15 });
    text(ctx, '25–30% less per bowl', 0, 14, { font: '600 40px Jost', fill: C.card, align: 'center' }); ctx.restore(); }
}

// ---------------------------------------------------------------- 36–42 END CARD: the brand's own cover (logo tab, checker floor)
function sceneEnd(ctx, t) {
  const tt = Math.min(t, 39);
  bg(ctx, C.card);
  halftone(ctx, 540, 1080, 120, 700, C.greyD, 0.45);
  checker(ctx, 1180, W, H, { vpY: 300 });
  const kd = back(seg(t, 36.3, 36.75), 1.6);
  drawLogoTab(ctx, 540, -560 * (1 - kd), 470);
  const kt = pop(t, 36.8);
  if (kt > 0) { ctx.save(); ctx.translate(540, 640); ctx.scale(kt, kt);
    text(ctx, 'ULTIMATE DIET', 0, 0, { font: '84px Slab', fill: C.red, plate: C.ink, off: [5, 5], align: 'center', maxW: 960 });
    text(ctx, 'MEDIUM & MAXI · ADULT', 0, 56, { font: '600 28px Jost', fill: C.ink, align: 'center', track: 5 });
    ctx.restore(); }
  const kp = back(seg(t, 37.0, 37.35), 2.0);
  if (kp > 0) drawPack(ctx, 430, 1330, { s: 1.22 * kp });
  drawMango(ctx, 830, 1390, { s: 0.78, dir: -1, mouth: 'grin', ear: 1, tail: tt < 39 ? Math.sin(twos(t) * 10) * 0.12 : 0, blink: t > 39.4 && t < 39.8 ? 1 : 0, brow: 0.5 });
  const ku = pop(t, 37.6);
  if (ku > 0) { ctx.save(); ctx.translate(540, 1470); ctx.scale(ku, ku);
    shape(ctx, rrect(-230, -40, 460, 80, 40), { fill: C.red, line: 4, seed: 990, grain: 0.15 });
    text(ctx, 'right4paws.com', 0, 13, { font: '600 40px Jost', fill: C.card, align: 'center' }); ctx.restore(); }
}

// ---------------------------------------------------------------- transitions + frame
function wipeUp(ctx, t, t0, d, A, B, edge = C.card) {
  const e = eio(seg(t, t0, t0 + d)), y = H * (1 - e);
  A(ctx, t); ctx.save(); ctx.beginPath(); ctx.rect(0, y, W, H - y); ctx.clip(); B(ctx, Math.max(t, t0 + 0.01)); ctx.restore();
  if (e < 1) shape(ctx, rect(-20, y - 22, W + 40, 44), { fill: edge, line: 4, seed: 995, grain: 0.2 });
}
function wipeSide(ctx, t, t0, d, A, B, edge = C.card) {
  const e = eio(seg(t, t0, t0 + d)), x = W * e;
  A(ctx, t); ctx.save(); ctx.beginPath(); ctx.rect(0, 0, x, H); ctx.clip(); B(ctx, Math.max(t, t0 + 0.01)); ctx.restore();
  if (e < 1) shape(ctx, rect(x - 22, -20, 44, H + 40), { fill: edge, line: 4, seed: 996, grain: 0.2 });
}
function iris(ctx, t, t0, d, cx, cy, A, B) {
  const r = lerp(70, 2300, eio(seg(t, t0, t0 + d)));
  A(ctx, t); ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU); ctx.clip(); B(ctx, t0 + d + 0.01); ctx.restore();
  ink(ctx, ellipse(cx, cy, r, r, 90), 6, { closed: true, seed: 997, breaks: 0.08 });
}
export function renderFilm(ctx, t) {
  setClock(t);
  if (t < 4.0) sceneHook(ctx, t);
  else if (t < 4.4) wipeUp(ctx, t, 4.0, 0.4, sceneHook, sceneTitle, C.card);
  else if (t < 7.5) sceneTitle(ctx, t);
  else if (t < 8.0) iris(ctx, t, 7.5, 0.5, MED[0][0], MED[0][1], sceneTitle, sceneWeigh);
  else if (t < 16.0) sceneWeigh(ctx, t);
  else if (t < 16.35) wipeSide(ctx, t, 16.0, 0.35, sceneWeigh, sceneMeasure, C.red);
  else if (t < 22.0) sceneMeasure(ctx, t);
  else if (t < 22.35) wipeSide(ctx, t, 22.0, 0.35, sceneMeasure, sceneServe, C.card);
  else if (t < 30.0) sceneServe(ctx, t);
  else if (t < 32.0) sceneQuiet(ctx, t);
  else if (t < 34.0) scenePay(ctx, t);
  else if (t < 34.35) wipeSide(ctx, t, 34.0, 0.35, scenePay, sceneTip, C.card);
  else if (t < 36.0) sceneTip(ctx, t);
  else if (t < 36.4) wipeUp(ctx, t, 36.0, 0.4, sceneTip, sceneEnd, C.red);
  else sceneEnd(ctx, t);
  caption(ctx, t);
  paperFinish(ctx, W, H, 0.85);
}
