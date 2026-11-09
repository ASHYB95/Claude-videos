// Four-finger cartoon glove hands and sleeves entering from the frame edge (no full presenter: the hand is the step).
import { ellipse, xform, path, move, reg, ink, spline, TAU } from './toon.js';
import { C } from './pal.js';

// kind: 'open' | 'flat' | 'point' | 'grip'. Fingers point along angle a. k = scale.
export function drawHand(ctx, x, y, a, kind = 'open', side = 1, k = 1, skin = C.skin) {
  const parts = [], seps = [];
  const E = (cx, cy, rx, ry, rot = 0) => parts.push(ellipse(cx, cy, rx, ry, 18, 0, TAU, rot));
  E(12, 0, 15, 13.5);
  if (kind === 'open') {
    [-0.62, 0, 0.62].forEach(r => E(12 + Math.cos(r) * 25, Math.sin(r) * 25, 12, 5, r));
    E(4, -15 * side, 10, 5, -1.35 * side);
  } else if (kind === 'flat') {
    [-10, 0, 10].forEach((dy, i) => E(34 + (i === 1 ? 3 : 0), dy, 13, 4.8));
    E(10, -15 * side, 9, 5, -0.9 * side);
    seps.push([[24, -5], [40, -5]], [[24, 5], [40, 5]]);
  } else if (kind === 'point') {
    E(38, -5 * side, 19, 4.8); E(25, 5 * side, 7, 6); E(20, 11 * side, 6, 5.5); E(8, -14 * side, 8.5, 5, -1.0 * side);
  } else { E(26, -8, 6.5, 6.5); E(28, 1, 6.5, 6.5); E(25, 10, 6, 6); E(12, -14 * side, 9, 5.5, -0.4 * side); seps.push([[22, -3.5], [30, -3.5]], [[22, 5.5], [29, 5.5]]); }
  const P = parts.map(p => xform(p, x, y, a, k));
  const lw = 6 * Math.min(k, 1.35);
  ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = lw; ctx.lineJoin = 'round';
  for (const p of P) { path(ctx, p); ctx.stroke(); }
  const o = reg(77, 0.6); ctx.fillStyle = skin;
  for (const p of P) { path(ctx, move(p, o[0] * 0.5, o[1] * 0.5)); ctx.fill(); }
  ctx.lineWidth = 2.6 * Math.min(k, 1.35); ctx.lineCap = 'round';
  for (const s2 of seps) { const q = xform(s2, x, y, a, k); ctx.beginPath(); ctx.moveTo(...q[0]); ctx.lineTo(...q[1]); ctx.stroke(); }
  ctx.restore();
}

// a sleeve (thick ink ribbon + turquoise ribbon on top) from off-frame to the wrist, then the hand
export function arm(ctx, pts, kind, o = {}) {
  const { k = 2, side = 1, seed = 60, col = C.teal, colD = C.tealD, w = 22 * k } = o;
  const P = spline(pts, false, 8);
  ink(ctx, P, w + 10, { seed, taper: false, wob: 0.06 });
  const off = reg(seed, 1);
  ink(ctx, move(P, off[0] * 0.6, off[1] * 0.6), w, { seed: seed + 1, taper: false, wob: 0.04, color: col });
  const n = P.length, e = P[n - 1], d = P[Math.max(0, n - 4)], a = Math.atan2(e[1] - d[1], e[0] - d[0]);
  // cuff stripe
  const cx = e[0] - Math.cos(a) * 10 * k, cy = e[1] - Math.sin(a) * 10 * k, r = (w + 10) / 2;
  ink(ctx, [[cx + Math.cos(a + 1.57) * r, cy + Math.sin(a + 1.57) * r], [cx - Math.cos(a + 1.57) * r, cy - Math.sin(a + 1.57) * r]], 3.4, { seed: seed + 2, taper: false, color: colD });
  drawHand(ctx, e[0], e[1], o.handA ?? a, kind, side, k);
  return { x: e[0], y: e[1], a };
}
