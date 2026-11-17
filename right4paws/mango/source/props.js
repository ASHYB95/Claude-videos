// Props: pellet bowl, the Ultimate Diet pack, ingredients, red bowl + flakes, clock, sun, hearts, paw prints
import { line, fill, dab, text, ellipse, handCircle, xf, smooth, sx, sy, CAM } from './crayon.js';
import { part, tube, curve } from './rig.js';
import { PAL } from './pal.js';
import { clamp, lerp, hash, mulberry } from './lib.js';
const K = PAL.crayon;
const LO = (sd, w = 6, ex = {}) => ({ w, seed: sd, col: K.ink, ...ex });
const F = (col, sd, ex = {}) => ({ col, p: 0.88, gap: 8, w: 10, seed: sd, ang: 0.6, over: 4, ...ex });

// —— bowl (side view). x,y = rim centre; w = rim half-width
export function bowl(C, x, y, o = {}) {
  const w = o.w ?? 150, s = w / 150, sd = o.seed ?? 70, ld = o.draw ?? 1, red = o.red;
  const body = [[x - w, y], [x + w, y], [x + w * 0.78, y + 92 * s], [x - w * 0.78, y + 92 * s]];
  const fo = red && o.colour !== 0 ? F(K.red, sd, { draw: o.colour ?? 1, p: 0.95 }) : null;
  // contents behind the rim front
  if (o.fill) o.fill(C);
  part(C, smooth([...body], 3), fo, LO(sd + 1, 7, { draw: ld }));
  part(C, ellipse(x, y, w, 22 * s, 30), red && o.colour !== 0 ? F(K.red, sd + 2, { draw: o.colour ?? 1, p: 0.7, gap: 10 }) : null, LO(sd + 3, 6, { draw: ld }), { occ: false });
  if (o.label) text(C.l, o.label, sx(x), sy(y + 58 * s), { size: 34 * s * CAM.s, font: 'Fredoka', weight: 700, col: K.white, p: 0.95 * clamp(o.colour ?? 1), seed: sd + 9 });
}
// a mound of the old brown pellets sitting in the bowl
export function pellets(L, x, y, w, sd = 80, n = 26, k = 1) {
  const R = mulberry(sd);
  for (let i = 0; i < n; i++) {
    const u = R() * 2 - 1, h = (1 - u * u) * 46;
    const px = x + u * w * 0.86, py = y - R() * h + 6;
    dab(L.f, px, py, 11 * k, { col: K.brown, p: 0.95, seed: sd + i, gap: 4, w: 6 });
    line(L.l, handCircle(px, py, 11 * k, sd + i, 0.05, 14), { w: 3, seed: sd + i, col: K.ink, p: 0.7 });
  }
}
// Right4Paws flakes: a heap of jagged crumbly pieces
export function flakes(C, x, y, w, sd = 90, amt = 1) {
  const R = mulberry(sd), n = Math.floor(30 * amt);
  for (let i = 0; i < n; i++) {
    const u = R() * 2 - 1, h = (1 - u * u) * 70 * Math.min(1, amt * 1.3);
    const px = x + u * w * 0.85, py = y - R() * h + 4, r = 12 + R() * 9;
    const poly = []; for (let k = 0; k < 7; k++) { const a = k / 7 * 6.283 + R(); const rr = r * (0.6 + 0.6 * R()); poly.push([px + Math.cos(a) * rr, py + Math.sin(a) * rr * 0.7]); }
    fill(C.f, poly, { col: R() < 0.5 ? '#b7703f' : '#9c5a32', p: 0.95, gap: 4, w: 6, seed: sd + i, over: 1.5 });
    line(C.l, [...poly, poly[0]], { w: 3, seed: sd + i * 3, col: K.ink, p: 0.6 });
  }
}

// —— the Ultimate Diet pack (child perspective: front + slanted side). x,y = bottom-front-left; w,h front size
export function pack(C, x, y, o = {}) {
  const w = o.w ?? 300, h = o.h ?? 420, d = w * 0.28, sd = o.seed ?? 200, col = o.colour ?? 1, ld = o.draw ?? 1;
  const k = w / 300;
  const front = [[x, y], [x + w, y], [x + w, y - h], [x, y - h]];
  const side = [[x + w, y], [x + w + d, y - d * 0.7], [x + w + d, y - h - d * 0.7], [x + w, y - h]];
  const top = [[x, y - h], [x + w, y - h], [x + w + d, y - h - d * 0.7], [x + d, y - h - d * 0.7]];
  part(C, side, col > 0 ? F(K.red, sd, { draw: col, p: 1, ang: -0.9 }) : null, LO(sd + 1, 7, { draw: ld }));
  part(C, top, col > 0 ? F(K.red, sd + 2, { draw: col, p: 0.8, ang: 0.2 }) : null, LO(sd + 3, 7, { draw: ld }));
  part(C, front, col > 0 ? F(K.cream, sd + 4, { draw: col, p: 0.6, gap: 12 }) : null, LO(sd + 5, 7, { draw: ld }));
  // red logo block, top-left
  const lb = [[x + 14 * k, y - h + 14 * k], [x + 140 * k, y - h + 14 * k], [x + 140 * k, y - h + 116 * k], [x + 14 * k, y - h + 116 * k]];
  if (col > 0) fill(C.f, lb, F(K.red, sd + 6, { draw: col, p: 1, gap: 6, w: 9, over: 1.5 }));
  const tc = clamp((col - 0.5) * 2);
  if (tc > 0) {
    text(C.l, 'RIGHT', sx(x + 77 * k), sy(y - h + 52 * k), { size: 30 * k * CAM.s, font: 'Fredoka', weight: 700, col: K.white, p: tc, seed: sd + 7 });
    text(C.l, '4PAWS', sx(x + 77 * k), sy(y - h + 82 * k), { size: 30 * k * CAM.s, font: 'Fredoka', weight: 700, col: K.white, p: tc, seed: sd + 8 });
    text(C.l, 'Raw Made Right', sx(x + 77 * k), sy(y - h + 106 * k), { size: 15 * k * CAM.s, font: 'Kalam', weight: 700, col: K.white, p: tc, seed: sd + 9 });
    text(C.l, 'ULTIMATE', sx(x + 222 * k), sy(y - h + 58 * k), { size: 29 * k * CAM.s, font: 'Fredoka', weight: 700, col: K.red, p: tc, seed: sd + 10 });
    text(C.l, 'DIET', sx(x + 222 * k), sy(y - h + 100 * k), { size: 44 * k * CAM.s, font: 'Fredoka', weight: 700, col: K.red, p: tc, seed: sd + 11 });
    text(C.l, '85.7%', sx(x + 66 * k), sy(y - h + 170 * k), { size: 30 * k * CAM.s, font: 'Fredoka', weight: 700, col: K.red, p: tc, seed: sd + 12 });
  }
  // a golden dog face on the pack
  const fx = x + 190 * k, fy = y - 150 * k, fr = 70 * k;
  part(C, xf([[-60, -40], [-80, 40], [-40, 10]], { x: fx, y: fy, s: k }), col > 0 ? F('#d99a3a', sd + 13, { draw: col }) : null, LO(sd + 14, 5, { draw: ld }));
  part(C, xf([[60, -40], [80, 40], [40, 10]], { x: fx, y: fy, s: k }), col > 0 ? F('#d99a3a', sd + 15, { draw: col }) : null, LO(sd + 16, 5, { draw: ld }));
  part(C, handCircle(fx, fy, fr, sd + 17, 0.04), col > 0 ? F('#e9b25a', sd + 18, { draw: col }) : null, LO(sd + 19, 5, { draw: ld }));
  dab(C.f, fx - 24 * k, fy - 10 * k, 7 * k, { col: K.ink, p: 1, seed: sd + 20, gap: 3, w: 4 });
  dab(C.f, fx + 24 * k, fy - 10 * k, 7 * k, { col: K.ink, p: 1, seed: sd + 21, gap: 3, w: 4 });
  dab(C.f, fx, fy + 14 * k, 10 * k, { col: K.ink, p: 1, seed: sd + 22, gap: 3, w: 4 });
  if (col > 0.3) dab(C.f, fx, fy + 38 * k, 11 * k, { col: K.pink, p: 0.9, seed: sd + 23, gap: 3, w: 5 });
  // lid flaps when open (0..1)
  if (o.open > 0) {
    const a = o.open;
    const fl = [[x, y - h], [x + w, y - h], [x + w - 10, y - h - 130 * k * a], [x + 10, y - h - 150 * k * a]];
    part(C, fl, col > 0 ? F(K.red, sd + 24, { draw: col, p: 0.95 }) : null, LO(sd + 25, 6, { draw: ld }));
  }
}

// —— ingredients (local origin centre, scale s, rotation r)
export const ING = ['chicken', 'egg', 'carrot', 'berries', 'sardine', 'pumpkin'];
export function ingredient(C, kind, x, y, o = {}) {
  const s = o.s ?? 1, r = o.r ?? 0, sd = o.seed ?? 300, col = o.colour ?? 1;
  const T = pts => xf(pts, { x, y, s, r });
  const FO = (c, n, ex = {}) => col > 0 ? F(c, sd + n, { draw: col, ...ex }) : null;
  if (kind === 'chicken') {
    part(C, T(tube([[-70, 30], [-30, 10]], 26, 26)), FO(K.cream, 1), LO(sd + 2));
    part(C, T(handCircle(-78, 22, 16, sd)), FO(K.cream, 3), LO(sd + 4));
    part(C, T(handCircle(-70, 46, 16, sd + 1)), FO(K.cream, 5), LO(sd + 6));
    part(C, T(smooth([[-34, 6], [10, -46], [70, -40], [84, 10], [40, 46], [-20, 36]], 5)), FO(K.tan, 7, { cross: true }), LO(sd + 8, 7));
  } else if (kind === 'egg') {
    part(C, T(ellipse(0, 0, 48, 62, 30)), FO(K.cream, 1, { p: 0.7 }), LO(sd + 2, 7));
    part(C, T(ellipse(78, 26, 44, 56, 30, 0, Math.PI * 2, 0.4)), FO(K.cream, 3, { p: 0.7 }), LO(sd + 4, 7));
  } else if (kind === 'carrot') {
    part(C, T([[-22, -60], [22, -60], [4, 80], [-4, 80]]), FO(K.orange, 1, { p: 0.95 }), LO(sd + 2, 7));
    for (let i = -1; i <= 1; i++) part(C, T(smooth([[i * 8, -58], [i * 22 - 6, -110], [i * 22 + 8, -112]], 4)), FO(K.green, 3 + i), LO(sd + 6 + i, 5));
    line(C.l, T([[-14, -20], [0, -18]]), LO(sd + 9, 4)); line(C.l, T([[-8, 20], [6, 22]]), LO(sd + 10, 4));
  } else if (kind === 'berries') {
    [[0, 0], [44, 10], [20, 40], [-36, 24], [-14, -36], [30, -30]].forEach(([bx, by], i) => {
      part(C, T(handCircle(bx, by, 26, sd + i * 3)), FO(K.blue, 10 + i, { p: 0.95, gap: 6 }), LO(sd + 20 + i, 5));
      line(C.l, T([[bx - 6, by - 14], [bx, by - 10], [bx + 6, by - 15]]), LO(sd + 30 + i, 3));
    });
    part(C, T(smooth([[-10, -60], [30, -90], [70, -70], [30, -56]], 4)), FO(K.green, 40), LO(sd + 41, 5));
  } else if (kind === 'sardine') {
    part(C, T([[60, 0], [120, -40], [112, 0], [120, 40]]), FO(K.grey, 1), LO(sd + 2, 6));
    part(C, T(smooth([[-100, 0], [-50, -40], [40, -34], [80, 0], [40, 34], [-50, 36]], 5)), FO(K.grey, 3, { cross: true, crossP: 0.4 }), LO(sd + 4, 7));
    dab(C.f, ...T([[-62, -8]])[0], 8 * s, { col: K.ink, p: 1, seed: sd + 5, gap: 3, w: 4 });
    line(C.l, T(curve([[-40, -30], [-32, 0], [-40, 30]])), LO(sd + 6, 4));
  } else if (kind === 'pumpkin') {
    for (const [i, dx] of [[0, -44], [1, 44], [2, 0]]) part(C, T(ellipse(dx, 0, 56, 58, 30)), FO(K.orange, 1 + i, { p: 0.9 }), LO(sd + 5 + i, 6));
    part(C, T(smooth([[-6, -56], [-2, -86], [16, -92], [8, -56]], 4)), FO(K.green, 9), LO(sd + 10, 5));
  }
}

// —— small doodles
export function heart(L, x, y, r, sd, p = 1, col = K.red) {
  const pts = []; for (let i = 0; i <= 40; i++) { const t = i / 40 * Math.PI * 2; pts.push([x + r * 0.06 * 16 * Math.pow(Math.sin(t), 3), y - r * 0.06 * (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t))]); }
  fill(L, pts, { col, p: 0.95 * p, gap: 5, w: 7, seed: sd, over: 2 });
  line(L, pts, { w: 5, seed: sd + 1, col: K.ink, p });
}
export function zigs(L, pts, sd, p = 1, draw = 1) { line(L, pts, { w: 5, seed: sd, col: K.ink, p, draw }); }
export function paw(L, x, y, r, sd, col = K.white, rot = 0) {
  const T = pts => xf(pts, { x, y, s: r / 30, r: rot });
  dab(L, ...T([[0, 10]])[0], r * 0.62, { col, p: 1, seed: sd, gap: 3, w: 5, sq: 0.85 });
  [[-22, -18], [-8, -30], [8, -30], [22, -18]].forEach(([a, b], i) => dab(L, ...T([[a, b]])[0], r * 0.24, { col, p: 1, seed: sd + i + 1, gap: 3, w: 4 }));
}
export function clock(C, x, y, R, t, sd = 600, colour = 1) {
  part(C, handCircle(x, y, R, sd, 0.06), colour > 0 ? F(K.yolk, sd + 1, { draw: colour, p: 0.6 }) : null, LO(sd + 2, 7));
  part(C, handCircle(x, y, R * 0.8, sd + 3, 0.03), colour > 0 ? F(K.white, sd + 4, { draw: colour, p: 0.9 }) : null, LO(sd + 5, 5), { occ: false });
  for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283; line(C.l, [[x + Math.cos(a) * R * 0.66, y + Math.sin(a) * R * 0.66], [x + Math.cos(a) * R * 0.74, y + Math.sin(a) * R * 0.74]], LO(sd + 10 + i, 4)); }
  const mA = -Math.PI / 2 + (o => o)(t), hA = -Math.PI / 2 + 4.2;
  line(C.l, [[x, y], [x + Math.cos(hA) * R * 0.4, y + Math.sin(hA) * R * 0.4]], LO(sd + 30, 7));
  line(C.l, [[x, y], [x + Math.cos(mA) * R * 0.62, y + Math.sin(mA) * R * 0.62]], LO(sd + 31, 5));
}
export function sun(C, x, y, R, t, sd = 640, draw = 1) {
  for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283 + 0.1 * Math.sin(t * 2); line(C.l, [[x + Math.cos(a) * R * 1.2, y + Math.sin(a) * R * 1.2], [x + Math.cos(a) * R * 1.55, y + Math.sin(a) * R * 1.55]], { w: 8, seed: sd + i, col: K.orange, p: 0.9, draw }); }
  part(C, handCircle(x, y, R, sd, 0.08), F(K.yolk, sd + 20, { draw, p: 0.9, cross: true }), LO(sd + 21, 7, { draw }));
  if (draw > 0.6) {
    line(C.l, curve([[x - R * 0.42, y - R * 0.1], [x - R * 0.3, y - R * 0.24], [x - R * 0.16, y - R * 0.1]]), LO(sd + 22, 5));
    line(C.l, curve([[x + R * 0.16, y - R * 0.1], [x + R * 0.3, y - R * 0.24], [x + R * 0.42, y - R * 0.1]]), LO(sd + 23, 5));
    line(C.l, curve([[x - R * 0.34, y + R * 0.2], [x, y + R * 0.46], [x + R * 0.34, y + R * 0.2]]), LO(sd + 24, 6));
    dab(C.f, x - R * 0.5, y + R * 0.18, R * 0.12, { col: K.orange, p: 0.6, seed: sd + 25 });
    dab(C.f, x + R * 0.5, y + R * 0.18, R * 0.12, { col: K.orange, p: 0.6, seed: sd + 26 });
  }
}
// a crayon stick (drawn flat into a 2D canvas, screen coords)
export function crayonStick(g, x, y, ang, len, col) {
  g.save(); g.translate(x, y); g.rotate(ang);
  g.fillStyle = col; g.beginPath(); g.moveTo(0, 0); g.lineTo(46, -20); g.lineTo(46, 20); g.closePath(); g.fill();
  g.fillRect(46, -21, len, 42);
  g.fillStyle = 'rgba(255,255,255,.12)'; g.fillRect(46, -21, len, 10);
  g.fillStyle = '#e0262b'; g.fillRect(110, -22, len - 100, 44);
  g.fillStyle = 'rgba(0,0,0,.12)'; g.fillRect(110, 10, len - 100, 12);
  g.strokeStyle = '#fbefe4'; g.lineWidth = 3; for (const xx of [140, len - 20]) { g.beginPath(); g.moveTo(xx, -22); g.lineTo(xx, 22); g.stroke(); }
  g.restore();
}
