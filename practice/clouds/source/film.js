// How a Cloud Is Made — Mid-century Cartoon, 1080×1920, 48.5 s, music grid 120 BPM (bar = 2 s, beat = 0.5 s).
// World = a tall column of air: ground/lake at the bottom (y≈3720), cloud at the top (y≈800). 1 km = 1200 units.
// Motion policy: drawings change on twos (12 fps); camera, wipes, irises, drifting décor and rays at 24 fps; something always moves.
import { PAL, setClock, shape, ink, plane, text, fit, measure, star, sparkle, rays, dashed, arrow, spline, ellipse, rrect, rect, move, xform,
  clamp, lerp, seg, ss, eo, eio, back, twos, hash, TAU, paperFinish, boomerang, kidney } from './engine/toon.js';
import { drawOwner, armJoints, toScreen } from './engine/chars.js';
export const W = 1080, H = 1920, DUR = 48.5;
Object.assign(PAL, { paper: '#F6EFE2', paperD: '#E9DDC6', ink: '#2E2622', white: '#FFFAF3', pink: '#F4B7B0' });
const C = {
  sky: '#BCD9EA', skyHook: '#C6E0EE', mint: '#B8E3CF', mintD: '#8FCBB2', butter: '#F6DC8A', butterD: '#E8C35E', peach: '#F7C6A8', peachD: '#EBA582',
  peri: '#B9C2EF', periD: '#949FDB', lilac: '#C9B2E6', cloud: '#FFFAF3', cloudD: '#DFE6EE', sand: '#EFE2C8', sandD: '#E2CFA9', drop: '#CFE6F5', dropD: '#A9CFEA',
  g1: '#D6EFE3', g2: '#FBE3D4', g3: '#DCDFF7', g4: '#CFE4F0', g5: '#E6DDF3',
};
const pr = seg, BEAT = 0.5;
const KM = 1200, GROUND = 3720, SUNP = [190, 2740];
const beatPh = t => (t / BEAT) % 1;                 // 0..1 within the beat
const bob = (t, a = 1) => Math.sin(twos(t) / BEAT * Math.PI) * a;   // on twos, one swing per beat

// —— narration
export const LINES = [
  { id: 'v1', t: 0.8, d: 3.968, text: 'Ever wondered how a cloud is made? It takes just four steps.' },
  { id: 'v2', t: 6.4, d: 4.304, text: 'Step one. The sun warms water in seas, lakes and puddles.' },
  { id: 'v3', t: 12.4, d: 5.619, text: 'Step two. Some of it turns into invisible water vapour, and rises with the warm air.' },
  { id: 'v4', t: 20.4, d: 6.559, text: 'Step three. As the air climbs, it spreads out and cools. Nearly ten degrees for every kilometre.' },
  { id: 'v5', t: 28.3, d: 7.432, text: 'Step four. Cool air can’t hold as much vapour. It clings to specks of dust and salt, and becomes tiny droplets.' },
  { id: 'v6', t: 36.4, d: 3.889, text: 'Billions of droplets, side by side. That’s a cloud.' },
  { id: 'v7', t: 42.4, d: 3.568, text: 'And when the droplets grow too heavy… they fall as rain.' },
];
function cues() {
  const out = [];
  LINES.forEach((L, i) => {
    const nx = LINES[i + 1], end = Math.min(Math.max(L.t + 1.8, L.t + L.d + 0.6), nx ? nx.t - 0.15 : DUR);
    const parts = L.text.length > 64 ? L.text.split(/(?<=[.?:])\s+/) : [L.text];
    if (parts.length === 1) { out.push({ t0: L.t - 0.1, t1: end, text: L.text }); return; }
    const tot = parts.reduce((a, p) => a + p.length, 0); let t0 = L.t - 0.1;
    parts.forEach((p, k) => { const t1 = k === parts.length - 1 ? end : t0 + (L.d * p.length / tot) + 0.15; out.push({ t0, t1, text: p }); t0 = t1; });
  });
  return out;
}
export const SUBS = cues();

// —— sections (boundaries on downbeats)
const S = { hook: [0, 6.0], s1: [6.0, 12.0], s2: [12.0, 20.0], s3: [20.0, 28.0], s4: [28.0, 36.0], pay: [36.0, 42.0], tip: [42.0, DUR] };
const STAMP = { s1: 5.5, s2: 11.5, s3: 19.5, s4: 27.5 };
const T = { title: 0.5, tilt: [2.9, 5.2], sunPoint: 6.7, call1: 8.5, tag1: 9.0, vap: 12.6, tag2a: 14.5, tag2b: 16.5,
  ruler: [20.4, 21.4], bubble: [21.5, 26.8], tag3: 24.0, call4: 28.5, specks: 30.5, cling: [32.0, 33.4], hush: [33.5, 34.0], drops: 34.0, puff: [34.7, 35.8], tag4: 34.6,
  form: [36.1, 37.9], pop: 38.0, meds: [38.5, 39.0, 39.5, 40.0], swell: [42.8, 44.2], fall: [44.2, 45.0], umb: 45.0, irisOut: [46.5, 47.6] };

// —— events
export const EV = [];
const ev = (t, type, o = {}) => EV.push({ t: +t.toFixed(3), type, ...o });
LINES.forEach(L => ev(L.t, 'voice', { id: L.id }));
ev(0, 'room'); ev(0.25, 'sparkle'); ev(T.title, 'stamp'); 'HOWACLOUDISMADE'.split('').forEach((_, i) => ev(T.title + 0.25 + i * 0.045, 'letter', { i }));
ev(T.tilt[0], 'swish', { dur: 2.3 }); ev(1.2, 'birds', { dur: 3 });
Object.entries(STAMP).forEach(([k, t], i) => { ev(t, 'stamp'); ev(t + 0.05, 'iris'); ev(t + 0.5, 'chord', { i }); });
ev(T.sunPoint, 'shimmer', { dur: 1.2 }); ev(6.2, 'lap', { dur: 5.6 }); ev(T.call1, 'pop'); ev(T.tag1, 'pop'); ev(8.0, 'birds', { dur: 3 });
for (let k = 0; k < 6; k++) ev(7.0 + k * 0.8, 'ripple', { k });
ev(T.vap, 'slide', { dur: 2.4 }); ev(13.5, 'swish', { dur: 0.5 }); ev(T.tag2a, 'pop'); ev(T.tag2b, 'pop'); ev(14.0, 'swish', { dur: 4.4 });
ev(T.ruler[0], 'scratch', { dur: 1.0 }); [0, 1, 2].forEach(k => ev(bubbleTimeAtKm(k), 'tick', { k })); ev(T.bubble[0], 'swell', { dur: 5.3 }); ev(T.tag3, 'pop');
ev(T.call4, 'pop'); ev(T.specks, 'pop'); ev(T.cling[0], 'drift', { dur: 1.4 }); ev(T.hush[0], 'silence', { dur: T.hush[1] - T.hush[0] });
for (let i = 0; i < 6; i++) ev(T.drops + i * 0.11, 'plink', { i }); ev(T.puff[0] + 0.7, 'fwump'); ev(T.tag4, 'pop');
ev(T.form[0], 'swirl', { dur: 1.8 }); ev(T.pop, 'boing'); ev(T.pop, 'confetti'); T.meds.forEach((t, i) => { ev(t, 'stamp'); ev(t, 'chord', { i }); }); ev(40.2, 'birds', { dur: 1.8 });
ev(42.0, 'wipe'); ev(T.swell[0], 'stretch', { dur: 1.4 }); ev(T.fall[0], 'drip'); ev(T.fall[0] + 0.25, 'rain', { dur: 3.0 }); ev(T.umb, 'umbrella'); ev(T.irisOut[0], 'iris');
for (let i = 0; i < 10; i++) ev(T.fall[0] + 0.8 + i * 0.22, 'splash', { i });
[['intro', 0], ['s1', 6.0], ['s2', 12.0], ['s3', 20.0], ['s4', 28.0], ['hush', 33.5], ['back', 34.0], ['pay', 36.0], ['tip', 42.0], ['end', 46.5]].forEach(([id, t]) => ev(t, 'cue', { id }));
function bubbleTimeAtKm(k) { const y = GROUND - k * KM - 120; return T.bubble[0] + (T.bubble[1] - T.bubble[0]) * invEio(invBub(y)); }
function invEio(v) { let lo = 0, hi = 1; for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; if (eio(m) < v) lo = m; else hi = m; } return (lo + hi) / 2; }

// —— camera [cx, cy, z] + drift + punch-ins on every stamp
function camBase(t) {
  if (t < S.hook[1]) {
    if (t < T.tilt[0]) return [540, 900, lerp(1.0, 1.06, ss(t / T.tilt[0]))];
    const u = eio(pr(t, T.tilt[0], T.tilt[1])); return [540, lerp(900, 3260, u), lerp(1.06, 1.0, u)];
  }
  if (t < S.s1[1]) return [540, 3260, lerp(1.0, 1.06, ss(pr(t, 6.0, 12.0)))];
  if (t < S.s2[1]) { const u = eio(pr(t, 14.0, 18.5)); return [540, lerp(3240, 2620, u), lerp(1.0, 0.96, u)]; }
  if (t < S.s3[1]) { const u = eio(pr(t, T.bubble[0], T.bubble[1])); return [560, Math.min(3240, bubY(u) + 300), 0.8]; }
  if (t < S.s4[1]) return [540, 1300, lerp(1.0, 1.04, pr(t, 28, 36))];
  if (t < S.pay[1]) { const u = eio(pr(t, 36.0, 37.6)); return [540, lerp(1300, 1060, u), lerp(1.0, 0.92, u)]; }
  return [540, 960, 1.0];
}
const PUNCH = [T.title, ...Object.values(STAMP), T.drops, T.pop, ...T.meds, T.umb];
function camAt(t) {
  const [x, y, z] = camBase(t); let p = 0;
  for (const s of PUNCH) if (t >= s && t < s + 0.5) p = Math.max(p, Math.exp(-(t - s) * 9) * 0.035);
  return [x + Math.sin(t * 0.53) * 7, y + Math.cos(t * 0.41) * 7, z * (1 + p)];
}
const w2s = (x, y, c) => [W / 2 + (x - c[0]) * c[2], H / 2 + (y - c[1]) * c[2]];
function camT(ctx, c) { ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.translate(W / 2, H / 2); ctx.scale(c[2], c[2]); ctx.translate(-c[0], -c[1]); }
const pop = (t, t0, d = 0.28) => back(seg(t, t0, t0 + d), 1.9);

// —— shapes
export function cloudPts(cx, cy, s, circles = CLOUD, sx = 1, sy = 1) {
  const out = [], N = 140;
  for (let i = 0; i < N; i++) {
    const a = i / N * TAU, dx = Math.cos(a), dy = Math.sin(a); let best = 0;
    for (const [x, y, r] of circles) { const b = dx * x + dy * y, c2 = x * x + y * y - r * r, disc = b * b - c2; if (disc < 0) continue; best = Math.max(best, b + Math.sqrt(disc)); }
    let px = dx * best, py = dy * best; if (py > 70) py = 70 + (py - 70) * 0.15;
    out.push([cx + px * s * sx, cy + py * s * sy]);
  }
  return out;
}
const CLOUD = [[-250, 20, 120], [-110, -60, 170], [70, -100, 190], [230, -20, 140], [330, 40, 90], [-340, 50, 80], [0, 40, 150]];
const PUFF = [[-60, 10, 60], [0, -30, 80], [70, 0, 60], [10, 20, 60]];
function drawCloud(ctx, cx, cy, s, o = {}) {
  const t = o.t ?? 0, br = o.breathe ?? 1;
  const sx = (o.sx ?? 1) * (1 + 0.018 * br * Math.sin(twos(t) * 2.4)), sy = (o.sy ?? 1) * (1 - 0.018 * br * Math.sin(twos(t) * 2.4));
  const P = cloudPts(cx, cy, s, CLOUD, sx, sy);
  shape(ctx, P, { fill: o.fill || C.cloud, line: 4.5, seed: o.seed ?? 210, grain: 0.18, breaks: 0.16,
    shade: [{ pts: rect(cx - 600 * s, cy + 18 * s * sy, 1200 * s, 220 * s), color: o.shadeC || C.cloudD, alpha: 0.9 }] });
  if (o.face) {
    const blink = (twos(t) % 3.1) < 0.12, look = o.look || 0, ex = 6 * look * s;
    const eye = (x0) => blink || o.happy ? ink(ctx, [[x0 - 20 * s, cy - 14 * s], [x0, cy - (o.happy ? 26 : 14) * s], [x0 + 20 * s, cy - 14 * s]], 4.5, { seed: 220 + (x0 > cx ? 1 : 0) })
      : (shape(ctx, ellipse(x0 + ex, cy - 16 * s, 9 * s, 13 * s, 14), { fill: PAL.ink, line: 0, grain: 0, off: [0, 0] }), shape(ctx, ellipse(x0 + ex + 3 * s, cy - 21 * s, 3 * s, 3.5 * s, 8), { fill: PAL.white, line: 0, grain: 0, off: [0, 0] }));
    eye(cx - 50 * s); eye(cx + 50 * s);
    if (o.mouth === 'o') shape(ctx, ellipse(cx, cy + 26 * s, 12 * s, 15 * s, 14), { fill: '#E08C8C', line: 3.5, seed: 225, grain: 0 });
    else ink(ctx, spline([[cx - 26 * s, cy + 20 * s], [cx, cy + 36 * s], [cx + 26 * s, cy + 20 * s]], false, 6), 4.5, { seed: 222 });
    shape(ctx, ellipse(cx - 95 * s, cy + 18 * s, 18 * s, 11 * s, 14), { fill: C.peach, line: 0, grain: 0, seed: 223 });
    shape(ctx, ellipse(cx + 95 * s, cy + 18 * s, 18 * s, 11 * s, 14), { fill: C.peach, line: 0, grain: 0, seed: 224 });
  }
}
function drawSun(ctx, x, y, R, t, k = 1) {
  y += bob(t, 6);
  rays(ctx, x, y, 28, R * (2.5 + 0.15 * Math.sin(t * 2.2)), C.butter, { rot: t * 0.14, alpha: 0.45 * k, r0: R * 1.15 });
  rays(ctx, x, y, 14, R * 1.75, C.butterD, { rot: -t * 0.2, alpha: 0.35 * k, r0: R * 1.1 });
  shape(ctx, ellipse(x, y, R, R, 56), { fill: C.butter, line: 4.5, seed: 240, grain: 0.25, shade: [{ pts: rect(x + R * 0.25, y - R, R, 2 * R), color: C.butterD, alpha: 0.6 }] });
  const wink = (twos(t) % 2.7) < 0.14;
  ink(ctx, [[x - 34, y - 6], [x - 20, y - 16], [x - 6, y - 6]], 4, { seed: 241 });
  ink(ctx, wink ? [[x + 10, y - 10], [x + 38, y - 10]] : [[x + 10, y - 6], [x + 24, y - 16], [x + 38, y - 6]], 4, { seed: 242 });
  ink(ctx, spline([[x - 24, y + 22], [x + 2, y + 38], [x + 28, y + 22]], false, 6), 4, { seed: 243 });
  shape(ctx, ellipse(x - 48, y + 16, 12, 8, 12), { fill: C.peachD, line: 0, grain: 0, seed: 244, alpha: 0.7 });
  shape(ctx, ellipse(x + 50, y + 16, 12, 8, 12), { fill: C.peachD, line: 0, grain: 0, seed: 245, alpha: 0.7 });
}
const LAKE = spline([[430, GROUND + 70], [700, GROUND + 40], [1000, GROUND + 60], [1180, GROUND + 140], [1100, GROUND + 260], [760, GROUND + 290], [470, GROUND + 230], [380, GROUND + 140]], true, 8);
function ground(ctx, t) {
  plane(ctx, rect(-2000, GROUND, 5080, 2000), C.sand);
  plane(ctx, rect(-2000, GROUND + 260, 5080, 2000), C.sandD);
  ink(ctx, [[-200, GROUND], [1300, GROUND]], 4, { breaks: 0.3, seed: 250, taper: false });
  // reeds and pebbles sway on twos
  for (let i = 0; i < 5; i++) { const x = 400 + i * 22, sw = bob(t + i * 0.2, 6); ink(ctx, spline([[x, GROUND + 90], [x + sw * 0.5, GROUND + 30], [x + sw, GROUND - 30 - i * 8]], false, 5), 4, { seed: 255 + i, color: '#6E9C76' }); }
  shape(ctx, LAKE, { fill: C.mint, line: 4.5, seed: 251, grain: 0.25, shade: [{ pts: rect(380, GROUND + 190, 900, 200), color: C.mintD, alpha: 0.8 }] });
}
function lakeLife(ctx, t) {
  for (let i = 0; i < 4; i++) { const y = GROUND + 110 + i * 38, ph = twos(t) * 2 + i;
    const pts = []; for (let x = 520 + i * 30; x < 1040 - i * 40; x += 12) pts.push([x, y + Math.sin(x * 0.05 + ph) * 5]);
    ink(ctx, pts, 3, { seed: 260 + i, breaks: 0.35, color: '#5E9C88' }); }
  for (let k = 0; k < 7; k++) {          // ripple rings
    const t0 = 0.6 + k * 0.8 + hash(k) * 0.4, u = ((t - t0) % 5.6 + 5.6) % 5.6 / 1.4; if (u > 1 || t < t0) continue;
    const x = 560 + hash(k, 2) * 480, y = GROUND + 120 + hash(k, 3) * 120;
    ink(ctx, ellipse(x, y, 20 + 70 * eo(u), 6 + 18 * eo(u), 32), 3.5, { closed: true, seed: 270 + k, color: '#5E9C88', alpha: 1 - u, breaks: 0.3 });
  }
  for (let k = 0; k < 5; k++) { const ph = (twos(t) * 0.9 + k * 0.37) % 1; if (ph > 0.35) continue; sparkle(ctx, 560 + hash(k, 7) * 460, GROUND + 100 + hash(k, 8) * 140, 22 * Math.sin(ph / 0.35 * Math.PI), { fill: PAL.white }); }
}
function heatSquiggles(ctx, t, k) {
  if (k <= 0) return;
  for (let i = 0; i < 6; i++) { const x = 560 + i * 90, ph = ((t * 0.7 + i * 0.23) % 1), y0 = GROUND + 60 - ph * 260;
    const pts = []; for (let j = 0; j < 8; j++) pts.push([x + Math.sin(j * 1.3 + twos(t) * 6 + i) * 12, y0 - j * 18]);
    ink(ctx, pts, 5, { seed: 280 + i, color: C.butterD, alpha: k * Math.sin(ph * Math.PI) }); }
}
function ruler(ctx, t, u) {
  if (u <= 0) return;
  const x = 970, y0 = GROUND, y1 = GROUND - 2.25 * KM, yy = lerp(y0, y1, eo(u));
  shape(ctx, rrect(x - 34, yy, 68, y0 - yy, 10), { fill: PAL.paper, line: 4, seed: 270, grain: 0.15 });
  for (let k = 0; k <= 4; k++) { const y = y0 - k * KM / 2; if (y < yy + 10) break;
    ink(ctx, [[x - 34, y], [x + (k % 2 ? -6 : 10), y]], k % 2 ? 3 : 5, { seed: 271 + k, taper: false });
    if (k % 2 === 0) { const tk = bubbleTimeAtKm(k / 2), pk = t > tk ? back(pr(t, tk, tk + 0.3), 2.2) : 1, flash = t > tk && t < tk + 0.6;
      ctx.save(); ctx.translate(x - 50, y + 4); ctx.scale(pk, pk);
      if (flash) star(ctx, -60, -8, 70 * (1 - pr(t, tk, tk + 0.6)) + 30, { n: 12, inner: 0.55, fill: C.butter, off: [0, 0], rot: t });
      text(ctx, `${k / 2} km`, 0, 12, { font: '600 46px Jost', fill: PAL.ink, align: 'right', plate: C.peri, off: [3, 3] }); ctx.restore(); } }
}
function bubY(u) { return lerp(GROUND - 120, GROUND - 2.0 * KM - 160, u); }
function invBub(y) { return clamp((GROUND - 120 - y) / (2.0 * KM + 40)); }
function bubAt(t) { const u = eio(pr(t, T.bubble[0], T.bubble[1])); return { u, x: 480 + Math.sin(u * 5) * 30, y: bubY(u), r: lerp(110, 250, u) }; }
function drawBubble(ctx, t) {
  const { u, x, y, r } = bubAt(t);
  const v = (bubAt(t + 0.05).y - y) / 0.05;   // vertical speed
  const wob = Math.sin(twos(t) * 9) * 0.05, sq = clamp(-v / 2000, 0, 0.12);
  // speed lines under it while it climbs
  if (-v > 120) for (let i = 0; i < 5; i++) { const lx = x - r * 0.6 + i * r * 0.3, ph = (twos(t) * 3 + i * 0.3) % 1; ink(ctx, [[lx, y + r + 30 + ph * 60], [lx, y + r + 110 + ph * 60]], 6, { seed: 295 + i, color: C.periD, alpha: 0.8 * (1 - ph) }); }
  shape(ctx, ellipse(x, y, r * (1 + wob - sq * 0.5), r * 0.92 * (1 - wob + sq), 48), { fill: C.peach, line: 4.5, seed: 280, grain: 0.2, alpha: 0.9 });
  for (let i = 0; i < 12; i++) { const a = i * 2.4 + twos(t) * 1.6, rr = r * (0.2 + 0.55 * hash(i)); shape(ctx, ellipse(x + Math.cos(a) * rr, y + Math.sin(a) * rr, 10, 10, 10), { fill: PAL.white, line: 0, grain: 0, seed: 290 + i }); }
  // face: puffing out its cheeks as it expands
  ink(ctx, [[x - 40, y - 20], [x - 26, y - 30], [x - 12, y - 20]], 4, { seed: 300 }); ink(ctx, [[x + 12, y - 20], [x + 26, y - 30], [x + 40, y - 20]], 4, { seed: 301 });
  shape(ctx, ellipse(x, y + 14, 10, 12 + 4 * Math.sin(twos(t) * 6), 12), { fill: '#E08C8C', line: 3, seed: 302, grain: 0 });
  if (u > 0.04 && u < 0.98) [-1, 1].forEach(d => arrow(ctx, [x + d * (r + 20), y], [x + d * (r + 100), y], { u: 1, bob: beatPh(t), bend: 0, w: 6, head: 28, fill: C.peach, seed: 303 + d }));
  const km = (GROUND - 120 - y) / KM, temp = Math.round(20 - 9.8 * km);
  const tx = x - r - 120, ty = y - 30, shake = t - Math.max(...[0, 1, 2].map(bubbleTimeAtKm).filter(z => z <= t), -9) < 0.3 ? Math.sin(t * 80) * 6 : 0;
  ctx.save(); ctx.translate(shake, 0);
  shape(ctx, rrect(tx - 18, ty - 110, 36, 160, 18), { fill: PAL.white, line: 4, seed: 310, grain: 0 });
  const merc = clamp((temp + 15) / 40);
  shape(ctx, rrect(tx - 8, ty + 30 - 120 * merc, 16, 120 * merc + 10, 8), { fill: C.periD, line: 0, seed: 311, grain: 0, off: [0, 0] });
  shape(ctx, ellipse(tx, ty + 62, 26, 26, 24), { fill: C.periD, line: 4, seed: 312, grain: 0 });
  text(ctx, `${temp} °C`, tx, ty - 130, { font: '600 56px Jost', fill: PAL.ink, align: 'center', plate: C.peri, off: [3, 3] });
  ctx.restore();
  if (temp <= 1) for (let i = 0; i < 4; i++) sparkle(ctx, x + Math.cos(i * 1.6 + t) * (r + 40), y + Math.sin(i * 1.6 + t) * (r + 30), 16 + 8 * Math.sin(t * 6 + i), { fill: PAL.white });
  return { x, y, r };
}

// —— presenter (held body; hands on twos with one in-between; bobs on the beat)
function armAt(t, keys) {
  const tt = twos(t); let i = 0; while (i < keys.length - 1 && tt >= keys[i + 1][0]) i++;
  const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
  const u = b[0] > a[0] ? eo(clamp((tt - b[0] + 0.17) / 0.17)) : 0;
  const o = back(clamp((tt - a[0]) / 0.25), 2.4);   // overshoot then settle after each key
  const settle = i > 0 ? (o - 1) * 0.25 : 0;
  return { a1: lerp(a[1], b[1], u) + settle, a2: lerp(a[2], b[2], u) + settle * 1.3, hand: u > 0.5 ? b[3] : a[3] };
}
const ARMF = [[0, 1.3, 1.52, 'open'], [1.6, 0.2, -1.2, 'open'], [2.3, 0.2, -0.9, 'open'], [3.0, 0.2, -1.2, 'open'], [3.6, -1.35, -1.5, 'point'], [6.6, -1.45, -1.6, 'point'], [8.3, 0.35, 0.45, 'point'], [10.6, 0.6, 0.2, 'open'],
  [12.2, 1.3, 1.52, 'open'], [13.4, 0.1, 0.0, 'grip'], [15.4, -0.6, -0.8, 'grip'], [17.3, -1.2, -1.35, 'grip'], [19.4, 1.3, 1.52, 'open']];
const ARMB = [[0, 1.86, 1.7, 'open'], [9.2, 1.0, 0.2, 'open'], [10.6, 2.3, 2.8, 'open'], [12.2, 1.86, 1.7, 'open']];
function presenter(ctx, t, x, y, s, extra = {}) {
  const f = armAt(t, extra.armF || ARMF), b = armAt(t, extra.armB || ARMB);
  const blink = [2.1, 7.4, 10.3, 15.8, 18.6, 43.6, 46.0].some(bt => t > bt && t < bt + 0.12) ? 1 : 0;
  const hop = extra.hop ? Math.abs(Math.sin(twos(t) / BEAT * Math.PI)) * extra.hop : 0;
  const pose = { x, y: y - hop + bob(t, 2.5), s, dir: 1, view: 'q', face: extra.face || (t > 8.3 && t < 11.5 ? 'happy' : t > 1.5 && t < 3.4 ? 'happy' : 'neutral'), armF: { a1: f.a1, a2: f.a2 }, armB: { a1: b.a1, a2: b.a2 }, handF: f.hand, handB: b.hand, blink, look: extra.look || [3, -4] };
  drawOwner(ctx, pose, t);
  if (extra.pointer !== false && t > 12.8 && t < 19.6) {
    const J = armJoints(pose, 'F'), hp = toScreen(pose, J.ha), a = J.a2;
    const tip = [hp[0] + Math.cos(a) * 300 * s, hp[1] + Math.sin(a) * 300 * s];
    ink(ctx, [hp, tip], 7, { seed: 330, taper: false, color: '#8A6A4A' }); shape(ctx, ellipse(tip[0], tip[1], 10, 10, 12), { fill: C.lilac, line: 3, seed: 331, grain: 0 });
    for (let i = 0; i < 3; i++) { const ph = (twos(t) * 2 + i / 3) % 1; sparkle(ctx, tip[0] + Math.cos(i * 2.1) * 30 * ph, tip[1] - 40 * ph, 14 * (1 - ph), { fill: C.butter }); }
    return tip;
  }
  return null;
}

// —— vapour wisps (dotted peach paths rising from the lake) + rising arrows
function wisps(ctx, t, top = 2350) {
  const k = pr(t, T.vap, T.vap + 4.5); if (k <= 0) return;
  for (let i = 0; i < 6; i++) {
    const x0 = 560 + i * 85, pts = []; for (let y = GROUND + 120; y > top; y -= 30) pts.push([x0 + Math.sin(y * 0.012 + i * 1.7 + t * 1.2) * 28 + (GROUND - y) * 0.03 * (i - 2.5), y]);
    dashed(ctx, pts, 6, 16, 18, -t * 70 - i * 9, C.peachD, clamp(k * 1.2 - i * 0.05));
    for (let j = 0; j < 5; j++) { const v = ((t - T.vap) * 0.14 + j * 0.2 + i * 0.07) % 1; if (v > k) continue; const n = Math.floor(v * (pts.length - 1)); const p = pts[n];
      const wob = 1 + 0.2 * Math.sin(twos(t) * 8 + j); shape(ctx, ellipse(p[0], p[1], 12 * wob, 12 / wob, 12), { fill: C.peach, line: 3, seed: 340 + i * 5 + j, grain: 0 }); }
  }
  for (let i = 0; i < 4; i++) { const ph = ((t - T.vap) * 0.35 + i * 0.25) % 1; if (t < T.vap + 1) break; const x = 470 + i * 170, y = GROUND - 100 - ph * 1100;
    arrow(ctx, [x, y + 90], [x, y - 40], { u: 1, bob: beatPh(t), bend: 0.15, w: 6, head: 30, fill: C.peach, seed: 360 + i }); }
}

// —— background: parallax cloudlets, mid-century shapes, twinkles (screen space), birds
function background(ctx, t, c, tint) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const py = c ? c[1] * c[2] : 0;
  for (let i = 0; i < 7; i++) {           // boomerangs / kidneys, slow spin, far layer
    const x = ((hash(i, 11) * 1300 + t * (8 + 6 * hash(i))) % 1300) - 110, y = ((hash(i, 12) * 2400 - py * 0.12) % 2400 + 2400) % 2400 - 240;
    const P = (i % 2 ? boomerang : kidney)(x, y, 70 + 40 * hash(i, 13), t * 0.15 + i);
    shape(ctx, P, { fill: tint, line: 0, grain: 0.1, off: [0, 0], alpha: 0.55 });
  }
  for (let i = 0; i < 6; i++) {           // cloudlets, mid layer
    const sp = 18 + 22 * hash(i, 21), x = ((hash(i, 22) * 1500 + t * sp) % 1500) - 210, y = ((hash(i, 23) * 2600 - py * 0.35) % 2600 + 2600) % 2600 - 300;
    shape(ctx, cloudPts(x, y, 0.22 + 0.12 * hash(i, 24), PUFF), { fill: PAL.white, line: 3, seed: 380 + i, grain: 0.1, alpha: 0.85, breaks: 0.3 });
  }
  for (let i = 0; i < 16; i++) {          // twinkles
    const x = hash(i, 31) * W, y = ((hash(i, 32) * 2200 - py * 0.2) % 2200 + 2200) % 2200 - 140, ph = (twos(t) * (0.6 + hash(i, 33)) + hash(i, 34)) % 1;
    sparkle(ctx, x, y, 8 + 18 * Math.sin(ph * Math.PI), { fill: PAL.white, alpha: 0.85, rot: ph * 0.6 });
  }
}
function birds(ctx, t, t0, dur, y0, dir = 1) {
  const u = pr(t, t0, t0 + dur); if (u <= 0 || u >= 1) return;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  for (let i = 0; i < 3; i++) {
    const x = dir > 0 ? lerp(-120, W + 120, u) - i * 90 : lerp(W + 120, -120, u) + i * 90, y = y0 + i * 40 + Math.sin(u * 8 + i) * 18;
    const flap = Math.floor(twos(t) * 8 + i) % 2 ? 22 : -8;
    ink(ctx, [[x - 34, y - flap], [x, y + 6], [x + 34, y - flap]], 5, { seed: 390 + i, taper: true });
  }
}

// —— HUD
function subtitle(ctx, t) {
  const cue = SUBS.find(s => t >= s.t0 && t < s.t1); if (!cue) return;
  const a = Math.min(ss(seg(t, cue.t0, cue.t0 + 0.16)), 1 - ss(seg(t, cue.t1 - 0.16, cue.t1)));
  const f = fit(ctx, cue.text, '500 {px}px Jost', 44, 860, 2, 34);
  const lw = Math.max(...f.lines.map(l => measure(ctx, l, f.font))), w = lw + 130, h = 36 + f.lines.length * f.px * 1.22, x = W / 2 - w / 2, y = 1800 - h;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, (1 - a) * 14);
  shape(ctx, rrect(x, y, w, h, 16), { fill: PAL.paper, line: 3.4, seed: 901, grain: 0.15, breaks: 0.08, off: [5, 5] });
  star(ctx, x + 32, y + h / 2, 15, { n: 8, inner: 0.4, fill: C.lilac, off: [0, 0], rot: t * 1.2 });
  star(ctx, x + w - 32, y + h / 2, 15, { n: 8, inner: 0.4, fill: C.lilac, off: [0, 0], rot: -t * 1.2 });
  f.lines.forEach((l, i) => text(ctx, l, W / 2, y + 18 + f.px * 0.95 + i * f.px * 1.22, { font: f.font, fill: PAL.ink, align: 'center' }));
  ctx.restore();
}
const STEPCOL = [C.mint, C.peach, C.peri, C.drop];
function stepHeader(ctx, t, t0, label, num) {
  const k = eo(seg(twos(t), t0 + 0.05, t0 + 0.4)); if (k <= 0) return;
  ctx.save(); ctx.translate(-(1 - k) * 700, 0);
  const nk = pop(t, t0 + 0.3, 0.3), sb = 1 + 0.04 * Math.sin(twos(t) / BEAT * Math.PI * 2) * pr(t, t0 + 0.6, t0 + 0.8);
  ctx.save(); ctx.translate(116, 150); ctx.scale(nk * sb, nk * sb); ctx.rotate(Math.sin(t * 2) * 0.05);
  star(ctx, 0, 0, 82, { n: 14, inner: 0.82, fill: STEPCOL[num - 1], off: [0, 0], rot: t * 0.4 });
  shape(ctx, ellipse(0, 0, 60, 60, 40), { fill: PAL.ink, line: 0, seed: 700, grain: 0.1, off: [0, 0] });
  text(ctx, String(num), 0, 26, { font: '72px Slab', fill: PAL.paper, align: 'center' });
  ctx.restore();
  text(ctx, `STEP ${num} OF 4`, 214, 118, { font: '600 26px Jost', fill: PAL.ink, track: 7 });
  bounceText(ctx, label, 212, 194, t, t0 + 0.3, { font: '76px Slab', fill: PAL.ink, plate: STEPCOL[num - 1], off: [5, 5] });
  ctx.restore();
}
// per-letter drop-in with overshoot, then a gentle wave on the beat
function bounceText(ctx, str, x, y, t, t0, o) {
  ctx.save(); ctx.font = o.font; if (o.track) ctx.letterSpacing = o.track + 'px';
  const ws = [...str].map(ch => ctx.measureText(ch).width), tw = ws.reduce((a, b) => a + b, 0);
  let cx = o.align === 'center' ? x - tw / 2 : x; ctx.restore();
  [...str].forEach((ch, i) => {
    const k = back(pr(t, t0 + i * 0.045, t0 + i * 0.045 + 0.3), 2.2);
    if (k > 0 && ch !== ' ') { const wave = Math.sin(twos(t) * 5 - i * 0.6) * 4 * pr(t, t0 + 1, t0 + 1.4);
      ctx.save(); ctx.translate(cx + ws[i] / 2, y + (1 - k) * -60 + wave); ctx.scale(clamp(k, 0, 1.3), k);
      text(ctx, ch, 0, 0, { font: o.font, fill: o.fill, plate: o.plate, off: o.off, align: 'center' }); ctx.restore(); }
    cx += ws[i];
  });
}
function tag(ctx, t, t0, str, x, y, o = {}) {
  const k = pop(t, t0); if (k <= 0) return;
  const f = fit(ctx, str, '500 {px}px Jost', o.px || 42, o.maxW || 560, 2, 28);
  const w = Math.max(...f.lines.map(l => measure(ctx, l, f.font))) + 104, h = 34 + f.lines.length * f.px * 1.2;
  const X = o.align === 'right' ? x - w : o.align === 'center' ? x - w / 2 : x, fl = Math.sin(twos(t) * 2.2 + x * 0.01) * 6 * pr(t, t0 + 0.3, t0 + 0.6);
  ctx.save(); ctx.translate(X + w / 2, y + h / 2 + fl); ctx.scale(k, k); ctx.rotate(Math.sin(twos(t) * 1.7 + y) * 0.015); ctx.translate(-(X + w / 2), -(y + h / 2));
  shape(ctx, rrect(X, y, w, h, 16), { fill: PAL.paper, line: 3.8, seed: 710, grain: 0.15, off: [6, 5] });
  star(ctx, X + 40, y + h / 2, 18, { n: 8, inner: 0.42, fill: o.star || C.lilac, off: [0, 0], rot: t * 1.1 });
  f.lines.forEach((l, i) => text(ctx, l, X + 72, y + 17 + f.px * 0.92 + i * f.px * 1.2, { font: f.font, fill: PAL.ink }));
  ctx.restore();
}
function callout(ctx, t, t0, cx, cy, r, inner, bgc, leader) {
  const k = back(seg(t, t0, t0 + 0.34), 1.6); if (k <= 0) return;
  cy += Math.sin(twos(t) * 1.6) * 8 * pr(t, t0 + 0.4, t0 + 0.8);
  const R = r * k;
  if (leader) { const a = Math.atan2(leader[1] - cy, leader[0] - cx); dashed(ctx, [[cx + Math.cos(a) * (R + 16), cy + Math.sin(a) * (R + 16)], leader], 5, 16, 12, -t * 40, PAL.ink, clamp(k)); shape(ctx, ellipse(leader[0], leader[1], 10, 10, 12), { fill: PAL.ink, line: 0, off: [0, 0], grain: 0 }); }
  rays(ctx, cx, cy, 24, R + 70, PAL.white, { rot: t * 0.2, alpha: 0.35, r0: R + 10 });
  shape(ctx, ellipse(cx, cy, R + 18, R + 18, 72), { fill: PAL.paper, line: 5, seed: 720, grain: 0.15, breaks: 0.05 });
  ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.clip();
  ctx.fillStyle = bgc; ctx.fillRect(cx - R, cy - R, 2 * R, 2 * R);
  ctx.translate(cx, cy); ctx.scale(k, k); inner(ctx); ctx.restore();
  ink(ctx, ellipse(cx, cy, R, R, 72), 5, { closed: true, seed: 721, breaks: 0.1 });
}
function ring(ctx, x, y, t, t0, r0, r1, col = PAL.white, w = 8, dur = 0.5) {
  const u = pr(t, t0, t0 + dur); if (u <= 0 || u >= 1) return;
  ink(ctx, ellipse(x, y, lerp(r0, r1, eo(u)), lerp(r0, r1, eo(u)), 64), w * (1 - u) + 1, { closed: true, color: col, seed: 997, breaks: 0.2 });
}
function burst(ctx, x, y, t, t0, n = 14, rmax = 260, cols = [C.butter, C.lilac, C.mint, C.peach, PAL.white]) {
  const u = pr(t, t0, t0 + 0.9); if (u <= 0 || u >= 1) return;
  for (let i = 0; i < n; i++) { const a = i / n * TAU + hash(i) * 0.5, r = rmax * eo(u) * (0.6 + 0.4 * hash(i, 2)), g = 260 * u * u;
    const px = x + Math.cos(a) * r, py = y + Math.sin(a) * r + g * 0.4;
    if (i % 3 === 0) sparkle(ctx, px, py, 26 * (1 - u), { fill: cols[i % cols.length], rot: u * 4 });
    else star(ctx, px, py, 14 * (1 - u * 0.7), { n: 5, inner: 0.45, fill: cols[i % cols.length], off: [0, 0], rot: u * 6 + i }); }
}
const MEDICON = ['sun', 'rise', 'cool', 'drop'];
function medallion(ctx, i, x, y, r, k, withIcon = false, t = 0) {
  if (k <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(k, k); ctx.rotate((1 - clamp(k)) * 0.5);
  star(ctx, 0, 0, r * 1.2, { n: 16, inner: 0.84, fill: PAL.white, off: [0, 0], rot: i * 0.2 + t * 0.3 });
  shape(ctx, ellipse(0, 0, r, r, 64), { fill: STEPCOL[i], line: 5, seed: 730 + i, grain: 0.3 });
  if (!withIcon) text(ctx, String(i + 1), 0, r * 0.38, { font: `${Math.round(r * 1.1)}px Slab`, fill: PAL.ink, plate: PAL.white, off: [5, 5], align: 'center' });
  else {
    medIcon(ctx, MEDICON[i], r, t);
    shape(ctx, ellipse(-r * 0.74, -r * 0.74, r * 0.32, r * 0.32, 30), { fill: PAL.ink, line: 0, seed: 310 + i, grain: 0.1, off: [0, 0] });
    text(ctx, String(i + 1), -r * 0.74, -r * 0.74 + r * 0.15, { font: `${Math.round(r * 0.42)}px Slab`, fill: PAL.paper, align: 'center' });
  }
  ctx.restore();
}
function medIcon(ctx, kind, r, t) {
  const s = r / 100;
  if (kind === 'sun') { rays(ctx, 0, 0, 12, 60 * s, C.butterD, { r0: 34 * s, rot: t * 0.6 }); shape(ctx, ellipse(0, 0, 32 * s, 32 * s, 24), { fill: C.butter, line: 3.5, seed: 801, grain: 0 }); }
  if (kind === 'rise') { const b = Math.sin(twos(t) * 6) * 6 * s; for (let i = -1; i <= 1; i++) arrow(ctx, [i * 26 * s, 40 * s + b], [i * 26 * s, -42 * s + b], { u: 1, bend: 0.15 * i, w: 5, head: 22 * s, fill: C.peachD, seed: 802 + i }); }
  if (kind === 'cool') { const m = 0.5 + 0.3 * Math.sin(twos(t) * 3); shape(ctx, rrect(-12 * s, -50 * s, 24 * s, 80 * s, 12 * s), { fill: PAL.white, line: 3.5, seed: 805, grain: 0 }); shape(ctx, ellipse(0, 36 * s, 20 * s, 20 * s, 20), { fill: C.periD, line: 3.5, seed: 806, grain: 0 }); shape(ctx, rrect(-5 * s, (30 - 70 * m) * s, 10 * s, 70 * m * s + 6 * s, 5 * s), { fill: C.periD, line: 0, seed: 807, grain: 0, off: [0, 0] }); }
  if (kind === 'drop') { const sq = 1 + 0.06 * Math.sin(twos(t) * 7); ctx.save(); ctx.scale(sq, 1 / sq); shape(ctx, dropPts(0, 6 * s, 40 * s), { fill: C.dropD, line: 3.5, seed: 808, grain: 0 }); sparkle(ctx, -10 * s, -2 * s, 12 * s, { fill: PAL.white }); ctx.restore(); }
}
function dropPts(x, y, r) { const out = []; for (let i = 0; i <= 48; i++) { const a = i / 48 * TAU; out.push([x + r * 0.95 * Math.sin(a) * Math.sin(a / 2), y - r * 1.25 * Math.cos(a)]); } return out; }

// —— microscope call-out content for step 4 (native scale, centred on 0,0)
function microScene(ctx, t) {
  const specks = [[-150, -80, 'dust'], [120, -140, 'salt'], [-40, 110, 'dust'], [170, 90, 'salt'], [-190, 120, 'salt'], [40, -10, 'dust']];
  const sk = pr(t, T.specks, T.specks + 0.4), cl = eio(pr(t, T.cling[0], T.cling[1]));
  const pk = eio(pr(t, T.puff[0], T.puff[1]));
  if (pk > 0) {
    for (let i = 0; i < 70; i++) { const a = i * 2.39 + pk * 2.5, d0 = 260 + 60 * Math.sin(i), d1 = 40 + 90 * Math.sqrt(hash(i, 6));
      const r = lerp(d0, d1, pk); shape(ctx, ellipse(Math.cos(a) * r, Math.sin(a) * r * 0.7, 9, 9, 10), { fill: C.dropD, line: 2.5, seed: 460 + i, grain: 0, alpha: clamp(pk * 3) }); }
    if (pk > 0.85) { const k = back(pr(t, T.puff[1] - 0.2, T.puff[1] + 0.2), 1.8); drawCloud(ctx, 0, 0, 0.42 * k, { seed: 470, face: true, happy: true, t }); burst(ctx, 0, 0, t, T.puff[1] - 0.1, 12, 230); }
  }
  if (pk > 0.6) return;
  for (let i = 0; i < 30; i++) {
    const sp = specks[i % specks.length], ang = i * 2.39 + t * 0.8 * cl, rad = 34 + (i % 5) * 6;
    const jx = (hash(i, Math.floor(t * 12)) - 0.5) * 10, jy = (hash(i, Math.floor(t * 12) + 99) - 0.5) * 10;   // Brownian jiggle on twos
    const fx = Math.cos(i * 1.7 + t * 0.9) * 210 + Math.sin(i * 0.9) * 40, fy = Math.sin(i * 2.3 + t * 0.8) * 210;
    const tx = sp[0] + Math.cos(ang) * rad, ty = sp[1] + Math.sin(ang) * rad;
    const x = lerp(fx, tx, cl) + jx * (1 - cl * 0.7), y = lerp(fy, ty, cl) + jy * (1 - cl * 0.7);
    if (t < T.drops) shape(ctx, ellipse(x, y, 13, 13, 12), { fill: C.peach, line: 3, seed: 400 + i, grain: 0 });
  }
  specks.forEach(([x, y, kind], i) => {
    const k = back(clamp(sk * 1.6 - i * 0.1), 1.8); if (k <= 0) return;
    const dt0 = T.drops + i * 0.11, dk = pr(t, dt0, dt0 + 0.25);
    if (dk > 0) { const wob = 1 + 0.06 * Math.sin(twos(t) * 8 + i), r = lerp(14, 58, back(dk, 1.6));
      shape(ctx, ellipse(x, y, r * wob, r / wob, 36), { fill: C.dropD, line: 4, seed: 420 + i, grain: 0.15, shade: [{ pts: rect(x - r, y + r * 0.3, 2 * r, r), color: '#8DBBDC', alpha: 0.7 }] });
      sparkle(ctx, x - r * 0.35, y - r * 0.35, r * 0.4, { fill: PAL.white }); ring(ctx, x, y, t, dt0, 20, 110, PAL.white, 7, 0.45); }
    const rot = t * (i % 2 ? 1.2 : -1.0);
    if (kind === 'salt') shape(ctx, xform(rect(-14, -14, 28, 28), x, y, rot, k), { fill: PAL.white, line: 3.5, seed: 440 + i, grain: 0.1 });
    else shape(ctx, xform(spline([[-16, -6], [-4, -16], [14, -10], [16, 8], [0, 16], [-14, 10]], true, 3), x, y, rot, k), { fill: '#9C8F84', line: 3.5, seed: 450 + i, grain: 0.2 });
    if (t > T.specks + 0.3 && t < T.drops) text(ctx, kind, x, y + 54, { font: '600 30px Jost', fill: PAL.ink, align: 'center' });
  });
}

// —— scenes
function sky(ctx, col) { ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = col; ctx.fillRect(0, 0, W, H); }
function columnScene(ctx, t, skyCol, tint) {
  const c = camAt(t); sky(ctx, skyCol); background(ctx, t, c, tint); camT(ctx, c);
  if (t < S.hook[1]) drawCloud(ctx, 540, 800 + bob(t, 8), 1.0, { face: true, t, look: Math.sin(t * 1.3), happy: t > 3.4 });
  if (t < S.s3[0]) drawSun(ctx, SUNP[0], SUNP[1], 92, t);
  ruler(ctx, t, t >= S.s3[0] ? pr(t, T.ruler[0], T.ruler[1]) : 0);
  ground(ctx, t); lakeLife(ctx, t);
  if (t >= S.s1[0] - 0.5 && t < S.s2[1]) heatSquiggles(ctx, t, pr(t, 6.6, 7.4) * (1 - pr(t, 15, 17)));
  if (t >= S.s2[0] && t < S.s3[0]) wisps(ctx, t, 2350);
  let bub = null; if (t >= S.s3[0] && t < S.pay[0]) bub = drawBubble(ctx, t);
  const tip = presenter(ctx, t, 230, GROUND + 250, 1.12);
  return { c, tip, bub };
}
function hookScene(ctx, t) {
  const r = columnScene(ctx, t, C.skyHook, '#B2D4E6');
  birds(ctx, t, 1.0, 3.6, 300, 1);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const k = pop(t, T.title, 0.35), out = pr(t, 4.6, 4.9);
  if (k > 0 && out < 1) {
    ctx.save(); ctx.globalAlpha = 1 - out; ctx.translate(540, 1420 - out * 80); ctx.scale(k, k); ctx.rotate(Math.sin(twos(t) * 2) * 0.012);
    star(ctx, 0, 0, 400, { n: 18, inner: 0.86, fill: '#D9EAF3', off: [0, 0], rot: t * 0.15 });
    shape(ctx, rrect(-420, -150, 840, 300, 26), { fill: PAL.paper, line: 4, seed: 760, grain: 0.15, off: [7, 6] });
    star(ctx, -360, -100, 26, { n: 8, inner: 0.4, fill: C.lilac, off: [0, 0], rot: t * 2 });
    star(ctx, 360, 100, 26, { n: 8, inner: 0.4, fill: C.mint, off: [0, 0], rot: -t * 2 });
    ctx.restore();
    ctx.save(); ctx.globalAlpha = 1 - out; ctx.translate(0, -out * 80);
    bounceText(ctx, 'How a', 540, 1380, t, T.title + 0.25, { font: '700 92px Oleo', fill: PAL.ink, plate: C.lilac, off: [4, 4], align: 'center' });
    bounceText(ctx, 'CLOUD IS MADE', 540, 1500, t, T.title + 0.5, { font: '86px Slab', fill: PAL.ink, plate: C.sky, off: [5, 5], align: 'center' });
    ctx.restore();
  }
  const [mx, my] = w2s(SUNP[0], SUNP[1], r.c);
  medallion(ctx, 0, mx, my, 96, pop(t, STAMP.s1, 0.24), false, t); ring(ctx, mx, my, t, STAMP.s1, 100, 260);
}
function step1(ctx, t) {
  const r = columnScene(ctx, t, C.g1, '#C5E6D6');
  birds(ctx, t, 7.6, 3.4, 260, -1);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  stepHeader(ctx, t, S.s1[0], 'WARM', 1);
  callout(ctx, t, T.call1, 640, 760, 220, c2 => {
    c2.fillStyle = C.mint; c2.fillRect(-260, -40, 520, 300);
    for (let i = 0; i < 5; i++) { const pts = []; for (let x = -240; x < 240; x += 10) pts.push([x, -30 + i * 44 + Math.sin(x * 0.04 + twos(t) * 3 + i) * 7]); ink(c2, pts, 4, { seed: 500 + i, color: '#5E9C88', breaks: 0.2 }); }
    for (let i = 0; i < 5; i++) { const x = -180 + i * 90, ph = ((t * 0.9 + i * 0.27) % 1); ink(c2, spline([[x, -40 - ph * 40], [x + 12, -80 - ph * 40], [x - 10, -120 - ph * 40], [x + 6, -160 - ph * 40]], false, 6), 6, { seed: 510 + i, color: C.butterD, alpha: 1 - ph }); }
    for (let i = 0; i < 8; i++) { const a = i * 0.8, jx = (hash(i, Math.floor(t * 12)) - 0.5) * 14; shape(c2, ellipse(-200 + i * 56 + jx, 40 + (i % 3) * 50 + jx * 0.5, 9, 9, 10), { fill: PAL.white, line: 2.5, seed: 520 + i, grain: 0 }); }
    sparkle(c2, 120, -150, 30 + 8 * Math.sin(t * 6), { fill: C.butter, rot: t });
    // a tiny thermometer rising
    const m = pr(t, T.call1 + 0.3, T.call1 + 2.0); shape(c2, rrect(150, -120, 26, 120, 13), { fill: PAL.white, line: 3.5, seed: 530, grain: 0 }); shape(c2, rrect(156, -10 - 90 * m, 14, 90 * m + 12, 7), { fill: '#F2A08A', line: 0, seed: 531, grain: 0, off: [0, 0] }); shape(c2, ellipse(163, 10, 20, 20, 20), { fill: '#F2A08A', line: 3.5, seed: 532, grain: 0 });
  }, C.g1, w2s(760, GROUND + 140, r.c));
  tag(ctx, t, T.tag1, 'the sun warms the water', 540, 1040, { align: 'center', star: C.butter });
  if (t > T.sunPoint && t < T.sunPoint + 1.4) { const [sx, sy] = w2s(SUNP[0], SUNP[1], r.c), [lx, ly] = w2s(760, GROUND + 60, r.c); arrow(ctx, [sx + 120, sy + 90], [lx, ly - 80], { u: pr(t, T.sunPoint, T.sunPoint + 0.6), bob: beatPh(t), bend: 0.25, w: 7, head: 34, fill: C.butter, dashedShaft: true, seed: 540 }); }
  const [mx, my] = w2s(800, GROUND - 220, r.c);
  medallion(ctx, 1, mx, my, 96, pop(t, STAMP.s2, 0.24), false, t); ring(ctx, mx, my, t, STAMP.s2, 100, 260);
}
function step2(ctx, t) {
  const r = columnScene(ctx, t, C.g2, '#F6D4C0'); ctx.setTransform(1, 0, 0, 1, 0, 0);
  stepHeader(ctx, t, S.s2[0], 'RISE', 2);
  tag(ctx, t, T.tag2a, 'water vapour · invisible', 520, 520, { align: 'center', star: C.peach });
  tag(ctx, t, T.tag2b, 'warm air rises', 520, 680, { align: 'center', star: C.peach });
  medallion(ctx, 2, 540, 960, 104, pop(t, STAMP.s3, 0.24), false, t); ring(ctx, 540, 960, t, STAMP.s3, 110, 300);
}
function step3(ctx, t) {
  const r = columnScene(ctx, t, C.g3, '#CDD1F2'); ctx.setTransform(1, 0, 0, 1, 0, 0);
  stepHeader(ctx, t, S.s3[0], 'COOL', 3);
  tag(ctx, t, T.tag3, '≈ −10 °C for every km', 540, 1480, { align: 'center', star: C.peri });
  if (r.bub) { const [bx, by] = w2s(r.bub.x, r.bub.y, r.c); medallion(ctx, 3, bx, by, 100, pop(t, STAMP.s4, 0.24), false, t); ring(ctx, bx, by, t, STAMP.s4, 110, 300); }
}
function step4(ctx, t) {
  const r = columnScene(ctx, t, C.g4, '#BFDBEA'); ctx.setTransform(1, 0, 0, 1, 0, 0);
  stepHeader(ctx, t, S.s4[0], 'CONDENSE', 4);
  // the hush: everything dims for the beat before the droplets
  callout(ctx, t, T.call4, 540, 860, 330, c2 => microScene(c2, t), '#EAF3F8', r.bub ? w2s(r.bub.x, r.bub.y - 40, r.c) : null);
  tag(ctx, t, T.tag4, '1 droplet ≈ 0.02 mm', 540, 1270, { align: 'center', star: C.drop });
}
function payoff(ctx, t) {
  const c = camAt(t); sky(ctx, C.sky); background(ctx, t, c, '#AFCFE2'); camT(ctx, c);
  rays(ctx, 540, 800, 30, 1500, PAL.white, { rot: t * 0.08, alpha: 0.4 * pr(t, T.pop, T.pop + 0.5), r0: 120 });
  rays(ctx, 540, 800, 15, 900, C.butter, { rot: -t * 0.12, alpha: 0.25 * pr(t, T.pop, T.pop + 0.5), r0: 120 });
  const fk = eio(pr(t, T.form[0], T.form[1]));
  const P = cloudPts(540, 800, 0.92);
  if (t < T.pop + 0.15) for (let i = 0; i < 70; i++) {    // droplets spiral in
    const tgt = P[(i * 7) % P.length], ix = 540 + (tgt[0] - 540) * (0.3 + 0.7 * hash(i)), iy = 800 + (tgt[1] - 800) * (0.3 + 0.7 * hash(i, 2));
    const a0 = i * 2.39, R0 = 700 + 200 * hash(i, 4), a = a0 + (1 - fk) * 2.6, R = lerp(R0, 0, fk);
    const x = lerp(540 + Math.cos(a) * R, ix, fk * fk), y = lerp(1100 + Math.sin(a) * R * 0.8, iy, fk * fk);
    shape(ctx, ellipse(x, y, 14, 14, 12), { fill: C.dropD, line: 3, seed: 600 + i, grain: 0 });
  }
  const k = pop(t, T.pop, 0.45);
  if (k > 0) { const st = t < T.pop + 0.5 ? Math.sin(pr(t, T.pop, T.pop + 0.5) * Math.PI * 2) * 0.08 * (1 - pr(t, T.pop, T.pop + 0.5)) : 0;
    ctx.save(); ctx.translate(540, 800); ctx.scale(k, k); ctx.translate(-540, -800);
    drawCloud(ctx, 540, 800 + bob(t, 8), 1.0, { face: true, t, sx: 1 + st, sy: 1 - st, happy: t > T.pop + 0.6 && t < 40.5, look: Math.sin(t * 1.5) }); ctx.restore(); }
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  burst(ctx, ...w2s(540, 800, c), t, T.pop, 22, 520);
  birds(ctx, t, 40.0, 2.4, 260, 1);
  const labels = ['WARM', 'RISE', 'COOL', 'CONDENSE'];
  T.meds.forEach((tm, i) => { const x = 150 + i * 260, y = 1330 + (t > tm + 0.4 ? Math.sin(twos(t) / BEAT * Math.PI - i * 0.8) * 8 : 0);
    medallion(ctx, i, x, y, 92, pop(t, tm, 0.26), true, t); ring(ctx, x, y, t, tm, 96, 200);
    if (t > tm) bounceText(ctx, labels[i], x, y + 152, t, tm, { font: '40px Slab', fill: PAL.ink, plate: STEPCOL[i], off: [3, 3], align: 'center' }); });
}
function tipScene(ctx, t) {
  sky(ctx, C.g5); background(ctx, t, null, '#DCD0EE'); ctx.setTransform(1, 0, 0, 1, 0, 0);
  plane(ctx, rect(0, 1560, W, 400), C.sand); ink(ctx, [[0, 1560], [W, 1560]], 4, { breaks: 0.3, seed: 650, taper: false });
  // puddle grows
  const pk = pr(t, T.fall[0] + 0.6, T.fall[0] + 2.6); if (pk > 0) shape(ctx, ellipse(640, 1630, 260 * eo(pk), 40 * eo(pk), 40), { fill: C.drop, line: 4, seed: 655, grain: 0.2 });
  const sw = pr(t, T.swell[0], T.swell[1]), fl = pr(t, T.fall[0], T.fall[1]);
  const squeeze = Math.sin(sw * Math.PI) * 0.06 * (t < T.fall[0] ? 1 : 0);
  drawCloud(ctx, 560, 470 + bob(t, 6), 0.95, { face: true, shadeC: '#CFD6E6', t, sx: 1 + squeeze, sy: 1 - squeeze, mouth: t > T.swell[0] && t < T.fall[0] + 0.4 ? 'o' : null, look: 0.4 });
  if (t >= T.swell[0]) { const r = lerp(16, 46, eo(sw)), y = lerp(560, 1560, fl * fl), st = 1 + fl * 0.25;
    if (fl < 1) { ctx.save(); ctx.translate(620, y); ctx.scale(1 / st, st); shape(ctx, dropPts(0, 0, r), { fill: C.dropD, line: 4, seed: 660, grain: 0.1 }); sparkle(ctx, -10, -r * 0.2, r * 0.35, { fill: PAL.white }); ctx.restore(); } }
  // rain + splashes; drops bounce off the umbrella
  const uk = pop(t, T.umb, 0.3);
  if (t > T.fall[0] + 0.25) for (let i = 0; i < 30; i++) {
    const x = 220 + (i * 47) % 720, ph = ((t - T.fall[0]) * 1.5 + hash(i)) % 1;
    if (pr(t, T.fall[0] + 0.25, T.fall[0] + 1.2) < hash(i, 3)) continue;
    const yEnd = uk > 0.8 && x > 140 && x < 600 ? 1180 : 1560, y = lerp(580, yEnd, ph);
    shape(ctx, dropPts(x, y, 14), { fill: C.dropD, line: 3, seed: 670 + i, grain: 0 });
    if (ph > 0.9) { const sp = (ph - 0.9) / 0.1; for (let j = -1; j <= 1; j++) shape(ctx, ellipse(x + j * 26 * sp, yEnd - 10 - 30 * Math.sin(sp * Math.PI) * (j ? 1 : 1.4), 6, 6, 8), { fill: C.dropD, line: 2, seed: 700 + i + j, grain: 0 }); }
  }
  const armF = [[0, 1.3, 1.52, 'open'], [T.umb - 0.1, -1.1, -1.4, 'grip']];
  presenter(ctx, t, 330, 1760, 1.0, { armF, armB: [[0, 1.86, 1.7, 'open'], [T.umb + 0.4, 0.6, -0.4, 'open']], pointer: false, face: t > T.umb + 0.2 ? 'happy' : 'wow', look: [4, -10], hop: t > T.umb + 0.4 ? 10 : 0 });
  if (uk > 0) {
    const hx = 370, hy = 1760 - 560 - (t > T.umb + 0.4 ? Math.abs(Math.sin(twos(t) / BEAT * Math.PI)) * 10 : 0);
    ctx.save(); ctx.translate(hx, hy); ctx.scale(uk, uk); ctx.rotate(Math.sin(twos(t) * 3) * 0.04);
    const can = []; for (let i = 0; i <= 24; i++) { const a = Math.PI + i / 24 * Math.PI; can.push([Math.cos(a) * 230, Math.sin(a) * 140]); }
    for (let i = 4; i >= 0; i--) can.push([-230 + i * 115, (i % 2 ? 22 : 0)]);
    shape(ctx, can, { fill: C.peach, line: 4.5, seed: 680, grain: 0.25, shade: [{ pts: rect(0, -200, 260, 260), color: C.peachD, alpha: 0.5 }] });
    ink(ctx, [[0, -140], [0, 220]], 6, { seed: 681, taper: false }); ink(ctx, spline([[0, 220], [0, 250], [-30, 252], [-34, 230]], false, 5), 6, { seed: 682 });
    ctx.restore();
    ring(ctx, hx, hy - 60, t, T.umb, 120, 340, PAL.white, 8, 0.5);
  }
}

// —— frame
const mk = () => { const c = new OffscreenCanvas(W, H); return c.getContext('2d'); };
const A = mk(), Bc = mk();
function scene(ctx, t) {
  setClock(t);
  if (t < S.hook[1]) return hookScene(ctx, t);
  if (t < S.s1[1]) return step1(ctx, t);
  if (t < S.s2[1]) return step2(ctx, t);
  if (t < S.s3[1]) return step3(ctx, t);
  if (t < S.s4[1]) return step4(ctx, t);
  if (t < S.pay[1]) return payoff(ctx, t);
  return tipScene(ctx, t);
}
function irisCentre(key, t) {
  if (key === 's1') return w2s(SUNP[0], SUNP[1], camAt(t - 1e-3));
  if (key === 's2') return w2s(800, GROUND - 220, camAt(t - 1e-3));
  if (key === 's3') return [540, 960];
  if (key === 's4') { const b = bubAt(STAMP.s4); return w2s(b.x, b.y, camAt(STAMP.s4)); }
}
export function render(g, t) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  let done = false;
  for (const key of ['s1', 's2', 's3', 's4']) {
    const t0 = S[key][0], a = t0 - 0.45;
    if (t >= a && t < t0 + 0.05) {
      scene(A, Math.min(t, t0 - 0.001)); scene(Bc, Math.max(t, t0 + 0.001));
      g.drawImage(A.canvas, 0, 0);
      const [cx, cy] = irisCentre(key, t), rr = 104 * 1.2 + eio(pr(t, a, t0 + 0.05)) * 2300;
      g.save(); g.beginPath(); g.arc(cx, cy, rr, 0, TAU); g.clip(); g.drawImage(Bc.canvas, 0, 0); g.restore();
      ink(g, ellipse(cx, cy, rr, rr, 96), 7, { closed: true, seed: 990, breaks: 0.1 });
      ink(g, ellipse(cx, cy, rr + 22, rr + 22, 96), 4, { closed: true, seed: 991, breaks: 0.4, color: PAL.white });
      done = true; break;
    }
  }
  if (!done && t >= S.tip[0] - 0.05 && t < S.tip[0] + 0.45) {   // colour-block wipe, bottom-up, with a scalloped lilac edge
    scene(A, S.tip[0] - 0.06); scene(Bc, Math.max(t, S.tip[0] + 0.001));
    g.drawImage(A.canvas, 0, 0); const y = lerp(H + 60, -60, eio(pr(t, S.tip[0] - 0.05, S.tip[0] + 0.45)));
    g.save(); g.beginPath(); g.rect(0, y, W, H + 100); g.clip(); g.drawImage(Bc.canvas, 0, 0); g.restore();
    const sc = []; for (let x = -40; x <= W + 40; x += 20) sc.push([x, y - 18 - Math.abs(Math.sin(x / 60 * Math.PI)) * 26]);
    shape(g, [...sc, [W + 40, y + 6], [-40, y + 6]], { fill: C.lilac, line: 4, seed: 993, grain: 0.15 });
    done = true;
  }
  if (!done) scene(g, t);
  g.setTransform(1, 0, 0, 1, 0, 0);
  if (t >= T.irisOut[0]) {
    const rr = lerp(1500, 360, eio(pr(t, T.irisOut[0], T.irisOut[1])));
    g.save(); g.beginPath(); g.rect(0, 0, W, H); g.arc(560, 470, rr, 0, TAU, true); g.fillStyle = PAL.ink; g.fill('evenodd'); g.restore();
    ink(g, ellipse(560, 470, rr, rr, 96), 7, { closed: true, color: PAL.paper, seed: 995, breaks: 0.05 });
    if (t > T.irisOut[1] - 0.2) {
      bounceText(g, 'How a', 540, 1240, t, T.irisOut[1] - 0.2, { font: '700 100px Oleo', fill: PAL.paper, plate: C.lilac, off: [4, 4], align: 'center' });
      bounceText(g, 'CLOUD IS MADE', 540, 1370, t, T.irisOut[1], { font: '92px Slab', fill: PAL.paper, plate: C.sky, off: [5, 5], align: 'center' });
      for (let i = 0; i < 6; i++) { const ph = (twos(t) * 0.8 + i / 6) % 1; sparkle(g, 160 + i * 150, 1500 + Math.sin(i * 2) * 40, 22 * Math.sin(ph * Math.PI), { fill: [C.lilac, C.mint, C.peach, C.butter, C.sky, PAL.white][i] }); }
    }
  }
  subtitle(g, t);
  paperFinish(g, W, H, 1);
}
