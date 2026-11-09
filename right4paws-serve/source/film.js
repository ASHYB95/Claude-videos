// Right4Paws — How to Serve Ultimate Diet. 1080×1920, 24 fps, ♩ = 120 (beat 0.5 s, bar 2 s).
import { setClock, shape, ink, plane, ellipse, rrect, rect, text, fit, measure, star, sparkle, rays, dashed, kidney, boomerang,
  paperFinish, clamp, lerp, seg, ss, eo, back, twos, TAU } from './engine/toon.js';
import { C, tint, shade } from './engine/pal.js';
import { drawMango } from './engine/mango.js';
import { drawHand, arm } from './engine/hands.js';
import { drawPack, drawBowl, flakeStream, drawScale, drawDial, drawJug, drawFork, steam, drawClock } from './engine/props.js';

export const W = 1080, H = 1920, BEAT = 0.5;
export const SECTIONS = [
  { k: 'hook', t0: 0, t1: 4 }, { k: 'title', t0: 4, t1: 8 }, { k: 's1', t0: 8, t1: 16 }, { k: 's2', t0: 16, t1: 22 },
  { k: 's3', t0: 22, t1: 30 }, { k: 'quiet', t0: 30, t1: 32 }, { k: 'pay', t0: 32, t1: 36 }, { k: 'end', t0: 36, t1: 42 },
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
const bg = (ctx, col) => { ctx.fillStyle = col; ctx.fillRect(0, 0, W, H); };

// ---------------------------------------------------------------- shared furniture
function caption(ctx, t) {
  const cue = CUES.find(c => t >= c.t0 && t < c.t1); if (!cue) return;
  const a = Math.min(ss(seg(t, cue.t0, cue.t0 + 0.16)), 1 - ss(seg(t, cue.t1 - 0.16, cue.t1)));
  const f = fit(ctx, cue.text, '500 {px}px Jost', 44, 820, 2, 36);
  const lw = Math.max(...f.lines.map(l => measure(ctx, l, f.font)));
  const w = lw + 140, h = 46 + f.lines.length * f.px * 1.18, x = W / 2 - w / 2, y = 1640 - h;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, (1 - a) * 10);
  shape(ctx, rrect(x, y, w, h, 14), { fill: C.card, line: 3.4, seed: 901, grain: 0.15, breaks: 0.08, off: [5, 5] });
  star(ctx, x + 34, y + h / 2, 15, { n: 8, inner: 0.4, fill: C.teal, off: [0, 0], rot: t * 0.8 });
  star(ctx, x + w - 34, y + h / 2, 15, { n: 8, inner: 0.4, fill: C.teal, off: [0, 0], rot: -t * 0.8 });
  f.lines.forEach((l, i) => text(ctx, l, W / 2, y + 23 + f.px * 0.9 + i * f.px * 1.18, { font: f.font, fill: C.ink, align: 'center' }));
  ctx.restore();
}
function stepHeader(ctx, t, t0, num, label) {
  const k = eo(seg(twos(t), t0 + 0.05, t0 + 0.4)); if (k <= 0) return;
  ctx.save(); ctx.translate(-(1 - k) * 700, 0);
  shape(ctx, ellipse(112, 222, 56, 56, 40), { fill: C.ink, line: 0, seed: 700, grain: 0.1, off: [0, 0] });
  text(ctx, String(num), 112, 246, { font: '66px Slab', fill: C.card, align: 'center' });
  text(ctx, `STEP ${num} OF 3`, 192, 194, { font: '600 24px Jost', fill: C.ink, track: 6 });
  const f = fit(ctx, label, '{px}px Slab', 64, 820, 1, 40);
  text(ctx, f.lines[0], 190, 264, { font: f.font, fill: C.ink, plate: C.card, off: [4, 4] });
  ctx.restore();
}
function tag(ctx, t, t0, str, x, y, o = {}) {
  const k = pop(t, t0); if (k <= 0) return;
  const f = fit(ctx, str, '600 {px}px Jost', o.px || 38, o.maxW || 560, 2, 26);
  const w = Math.max(...f.lines.map(l => measure(ctx, l, f.font))) + 100, h = 32 + f.lines.length * f.px * 1.2;
  const X = o.align === 'right' ? x - w : o.align === 'center' ? x - w / 2 : x;
  ctx.save(); ctx.translate(X + w / 2, y + h / 2); ctx.scale(k, k); ctx.translate(-(X + w / 2), -(y + h / 2));
  shape(ctx, rrect(X, y, w, h, 14), { fill: C.card, line: 3.6, seed: 710, grain: 0.15, off: [6, 5] });
  star(ctx, X + 40, y + h / 2, 18, { n: 8, inner: 0.42, fill: C.teal, off: [0, 0], rot: t * 0.6 });
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
function room(ctx, wall, floorY, seed = 0) {
  bg(ctx, wall);
  plane(ctx, rect(0, floorY, W, H - floorY), shade(wall, 0.16));
  ink(ctx, [[-20, floorY], [W + 20, floorY]], 4, { breaks: 0.22, seed: 40 + seed, taper: false });
}

// ---------------------------------------------------------------- STEP 1: weigh your dog
function sceneWeigh(ctx, t, s) {
  const u = t - s.t0, floorY = 1290;
  room(ctx, C.blue, floorY, 1);
  // atomic wall ornaments + the sunburst clock
  drawClock(ctx, 820, 470, 62, t);
  [[180, 420, 22], [660, 330, 16], [950, 760, 20], [130, 820, 14]].forEach(([x, y, r], i) => sparkle(ctx, x, y, r, { fill: C.card, rot: i * 0.4, alpha: 0.9 }));
  shape(ctx, kidney(400, 1390, 360, 0.04).map(([x, y]) => [x, 1390 + (y - 1390) * 0.3]), { fill: C.mustardL, line: 0, seed: 801, grain: 0.3 });
  // the scale and Mango on it (hop at beat 2 of the section: anticipation 9.6, land 10.0)
  const jump = u < 2 ? 0 : u < 2.25 ? -ss(seg(u, 2, 2.25)) * 90 : u < 2.5 ? -90 + ss(seg(u, 2.25, 2.5)) * 90 : 0;
  const kg = u < 2.5 ? 0 : u < 4 ? 30 + Math.sin((u - 2.5) * 9) * 14 * (1 - seg(u, 2.5, 4)) : 30;
  const sc = drawScale(ctx, 160, 1250, { w: 450, kg });
  drawMango(ctx, 360, 1232 + jump, { s: 1.06, dir: 1, tail: Math.sin(twos(t) * 9) * 0.12, mouth: u > 5 ? 'grin' : 'smile', ear: u > 5 ? 1 : 0, brow: 0.2,
    blink: (u % 3.1) < 0.12 ? 1 : 0 });
  // the call-out on the dial, then the tag
  callout(ctx, t, s.t0 + 4.8, 800, 1030, 165, g => drawDial(g, kg, 132), C.blueL, [sc.dial[0] + 60, sc.dial[1] - 10]);
  tag(ctx, t, s.t0 + 5.0, '30 kg dog ≈ 350 g a day', 1040, 1350, { align: 'right', px: 36 });
  stepHeader(ctx, t, s.t0, 1, 'Weigh your dog');
}

// ---------------------------------------------------------------- STEP 3: serve it your way (split frame)
const BANDS = [
  { y: 340, col: C.blue, label: 'DRY', sub: 'straight from the pack', food: 'dry', on: 24.6 },
  { y: 720, col: C.mustard, label: 'SOFT', sub: 'sprinkle warm water', food: 'soft', on: 26.4 },
  { y: 1100, col: C.sage, label: 'MASHED', sub: 'mash it with a fork', food: 'mash', on: 28.6 },
];
function sceneServe(ctx, t, s) {
  bg(ctx, C.paper);
  const BH = 380, X0 = 40, BW = W - 80;
  BANDS.forEach((b, i) => {
    const slide = eo(seg(twos(t), s.t0 + i * 0.25, s.t0 + 0.5 + i * 0.25));
    if (slide <= 0) return;
    const active = t >= b.on, done = t >= b.on + 1.2;
    ctx.save(); ctx.translate((1 - slide) * (i % 2 ? W : -W), 0);
    ctx.beginPath(); ctx.rect(X0, b.y, BW, BH); ctx.save(); ctx.clip();
    shape(ctx, rect(X0, b.y, BW, BH), { fill: active ? b.col : tint(b.col, 0.45), line: 0, seed: 820 + i, grain: 0.3, off: [0, 0] });
    plane(ctx, rect(X0, b.y + BH * 0.74, BW, BH * 0.26), shade(active ? b.col : tint(b.col, 0.45), 0.14));
    // label (left)
    const la = active ? 1 : 0.45;
    text(ctx, b.label, 84, b.y + 118, { font: '74px Slab', fill: C.ink, plate: C.card, off: [5, 5], alpha: la });
    text(ctx, b.sub.toUpperCase(), 88, b.y + 166, { font: '600 22px Jost', fill: C.ink, track: 3, alpha: la });
    // the bowl (right of centre)
    const bx = 690, rimY = b.y + 238, u = clamp((t - b.on) / 1.2);
    const fill = b.food === 'dry' ? (active ? u : 0) : 1;
    drawBowl(ctx, bx, rimY, { rx: 140, food: b.food === 'dry' ? 'dry' : (active ? b.food : 'dry'), fill: b.food === 'dry' ? fill : 1, seed: 640 + i * 40 });
    if (b.food === 'dry' && active && !done) {
      drawPack(ctx, 862, b.y + 74, { s: 0.46, rot: -2.1, open: 1 });
      arm(ctx, [[W + 60, b.y + 190], [1010, b.y + 150], [930, b.y + 112]], 'grip', { k: 1.7, side: 1, seed: 870 });
      flakeStream(ctx, [736, b.y + 150], [bx - 10, rimY - 40], t, 14, 900);
    } else if (b.food === 'dry') {
      drawPack(ctx, 440, b.y + 340, { s: 0.44, rot: 0, open: 0 });
    }
    if (b.food === 'soft' && active) {
      steam(ctx, bx, rimY - 70, t, 3, 120);
      if (!done) {
        arm(ctx, [[W + 60, b.y + 40], [980, b.y + 60], [900, b.y + 96]], 'grip', { k: 1.7, side: -1, seed: 830 });
        drawJug(ctx, 850, b.y + 150, -0.75, 0.72);
        for (let d = 0; d < 7; d++) {
          const ph = ((t * 1.8 + d / 7) % 1), x = 735 - ph * 40 + (d % 2) * 10, y = b.y + 128 + ph * 70;
          shape(ctx, [[x, y - 14], [x + 6, y - 2], [x + 5, y + 5], [x, y + 8], [x - 5, y + 5], [x - 6, y - 2]], { fill: C.blueL, line: 2.4, seed: 840 + d, grain: 0, alpha: 1 - ph * 0.3 });
        }
      }
    }
    if (b.food === 'mash' && active) {
      const press = Math.abs(Math.sin(twos(t) * Math.PI * 2)) * 18;
      drawFork(ctx, bx + 30, rimY - 70 + press, 0.5, 0.9);
      arm(ctx, [[W + 60, b.y + 60], [1010, b.y + 90], [890 + press * 0.3, b.y + 118 + press]], 'grip', { k: 1.7, side: -1, seed: 850 });
    }
    if (active) [[bx - 190, rimY - 120], [bx + 170, rimY - 150]].forEach(([x, y], j) => sparkle(ctx, x, y, 18 + j * 4, { fill: C.card, rot: t * 0.5 + j }));
    ctx.restore();
    ink(ctx, rect(X0, b.y, BW, BH), 4.2, { closed: true, seed: 860 + i, breaks: 0.12 });
    ctx.restore();
  });
  stepHeader(ctx, t, s.t0, 3, 'Serve it your way');
}

// ---------------------------------------------------------------- placeholder for scenes still to draw
function scenePending(ctx, t, s) {
  bg(ctx, C.paper);
  text(ctx, s.k.toUpperCase(), W / 2, H / 2, { font: '60px Slab', fill: C.inkSoft, align: 'center' });
}

const SCENES = { s1: sceneWeigh, s3: sceneServe };
export function renderFilm(ctx, t) {
  setClock(t);
  const s = SECTIONS.find(x => t >= x.t0 && t < x.t1) || SECTIONS[SECTIONS.length - 1];
  (SCENES[s.k] || scenePending)(ctx, t, s);
  caption(ctx, t);
  paperFinish(ctx, W, H, 0.85);
}
