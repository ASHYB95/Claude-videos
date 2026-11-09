// Props: the Ultimate Diet pack (the product, always brand red), steel bowl + flakes, scale, jug, fork, wall clock.
import { shape, ink, ellipse, spline, rrect, rect, text, star, sparkle, rays, rng, TAU, lerp, path } from './toon.js';
import { C } from './pal.js';

let LOGO = null;
export function setLogo(img) { LOGO = img; }
// the brand paw, recoloured (white on the red plate)
function paw(ctx, x, y, h, col = C.white) {
  if (!LOGO) { star(ctx, x, y, h / 2, { fill: col, off: [0, 0] }); return; }
  const w = h * LOGO.width / LOGO.height;
  const c = paw.cache || (paw.cache = {});
  if (!c[col]) {
    const cv = new OffscreenCanvas(LOGO.width, LOGO.height), g = cv.getContext('2d');
    g.drawImage(LOGO, 0, 0); g.globalCompositeOperation = 'source-in'; g.fillStyle = col; g.fillRect(0, 0, cv.width, cv.height); c[col] = cv;
  }
  ctx.drawImage(c[col], x - w / 2, y - h / 2, w, h);
}
export { paw };

// ---------- the pack (3/4 view). Origin: bottom centre of the front face. ----------
export function drawPack(ctx, x, y, o = {}) {
  const { s = 1, rot = 0, open = 0 } = o;
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
  const W = 230, H = 310, D = 62, Dy = 34;
  // side (red) and top
  shape(ctx, [[W / 2, -H], [W / 2 + D, -H - Dy], [W / 2 + D, -Dy], [W / 2, 0]], { fill: C.red, line: 4, seed: 601, grain: 0.3, shade: [{ pts: [[W / 2, -H * 0.45], [W / 2 + D, -H * 0.45 - Dy], [W / 2 + D, -Dy], [W / 2, 0]], color: C.redD, alpha: 0.6 }] });
  if (open > 0) {
    // open flap: a lid hinged at the back edge
    shape(ctx, [[-W / 2, -H], [-W / 2 + D, -H - Dy], [W / 2 + D, -H - Dy], [W / 2, -H]], { fill: C.flakeD, line: 4, seed: 602, grain: 0.3 });
    shape(ctx, [[-W / 2 + D, -H - Dy], [-W / 2 + D - 10, -H - Dy - 120 * open], [W / 2 + D - 10, -H - Dy - 120 * open], [W / 2 + D, -H - Dy]], { fill: C.card, line: 4, seed: 603, grain: 0.25 });
  } else {
    shape(ctx, [[-W / 2, -H], [-W / 2 + D, -H - Dy], [W / 2 + D, -H - Dy], [W / 2, -H]], { fill: C.paperD, line: 4, seed: 602, grain: 0.25 });
  }
  // front face
  shape(ctx, rect(-W / 2, -H, W, H), { fill: C.card, line: 4.2, seed: 604, grain: 0.25 });
  // logo plate (red) top-left
  shape(ctx, rrect(-W / 2 + 10, -H + 10, 104, 92, 10), { fill: C.red, line: 0, seed: 605, grain: 0.2 });
  text(ctx, 'RIGHT', -W / 2 + 18, -H + 42, { font: '800 21px Jost', fill: C.white });
  text(ctx, '4PAWS', -W / 2 + 18, -H + 64, { font: '800 21px Jost', fill: C.white });
  paw(ctx, -W / 2 + 96, -H + 40, 26, C.white);
  text(ctx, 'Raw Made Right', -W / 2 + 62, -H + 88, { font: '700 13px Oleo', fill: C.white, align: 'center' });
  // ULTIMATE DIET
  text(ctx, 'ULTIMATE', -W / 2 + 122, -H + 46, { font: '27px Slab', fill: C.red, maxW: 100 });
  text(ctx, 'DIET', -W / 2 + 122, -H + 82, { font: '34px Slab', fill: C.red, maxW: 100 });
  // the pack's dog: a round badge with a golden dog head
  shape(ctx, ellipse(10, -100, 74, 74, 40), { fill: C.mustardL, line: 3.4, seed: 606, grain: 0.25 });
  ctx.save(); ctx.beginPath(); ctx.arc(10 + 6, -100 + 4, 74, 0, TAU); ctx.clip();
  // a golden dog: long hanging ears, lighter muzzle
  shape(ctx, ellipse(-28, -96, 15, 40, 16, 0, TAU, 0.18), { fill: C.ginger, line: 3, seed: 608, grain: 0.2 });
  shape(ctx, ellipse(48, -96, 15, 40, 16, 0, TAU, -0.18), { fill: C.ginger, line: 3, seed: 609, grain: 0.2 });
  shape(ctx, spline([[-14, -48], [-22, -110], [0, -146], [20, -146], [42, -110], [34, -48], [10, -36]], true, 8), { fill: C.gingerL, line: 3.2, seed: 607, grain: 0.25 });
  shape(ctx, ellipse(10, -68, 22, 18, 16), { fill: C.card, line: 2.6, seed: 613, grain: 0.1 });
  shape(ctx, ellipse(10, -78, 9, 7, 12), { fill: C.ink, line: 0, seed: 610, grain: 0, off: [0, 0] });
  shape(ctx, ellipse(-2, -106, 4, 5.5, 10), { fill: C.ink, line: 0, seed: 611, grain: 0, off: [0, 0] });
  shape(ctx, ellipse(22, -106, 4, 5.5, 10), { fill: C.ink, line: 0, seed: 612, grain: 0, off: [0, 0] });
  ink(ctx, [[2, -62], [10, -58], [18, -62]], 2.4, { seed: 614 });
  ctx.restore();
  // a little red ribbon: Medium & Maxi Adult
  shape(ctx, rrect(-W / 2 + 10, -30, W - 20, 22, 6), { fill: C.red, line: 0, seed: 613, grain: 0.15 });
  text(ctx, 'MEDIUM & MAXI · ADULT', 0, -14, { font: '600 13px Jost', fill: C.white, align: 'center', track: 2 });
  ctx.restore();
}

// ---------- steel bowl (side view) with an optional mound of food ----------
// food: null | 'dry' | 'soft' | 'mash';  fill 0..1 mound height
export function drawBowl(ctx, cx, rimY, o = {}) {
  const { rx = 150, food = null, fill = 1, seed = 640 } = o;
  const ry = rx * 0.22, h = rx * 0.62, bx = rx * 0.72;
  // inside of the bowl (back)
  shape(ctx, ellipse(cx, rimY, rx, ry, 48), { fill: C.steelD, line: 4, seed, grain: 0.2 });
  if (food && fill > 0) drawFood(ctx, cx, rimY, rx * 0.9, rx * 0.52 * fill, food, seed + 1);
  // outside front: the lower half of the rim ellipse, sides, base
  const front = [];
  for (let i = 0; i <= 24; i++) { const a = Math.PI * i / 24; front.push([cx + Math.cos(a) * rx, rimY + Math.sin(a) * ry]); }
  const body = [[cx + rx, rimY], [cx + bx, rimY + h], ...ellipse(cx, rimY + h, bx, ry * 0.7, 20, 0, Math.PI).reverse().map(([a, b]) => [a, b]).reverse(), [cx - bx, rimY + h], [cx - rx, rimY], ...front.reverse()];
  shape(ctx, body, { fill: C.steel, line: 4.2, seed: seed + 2, grain: 0.22,
    shade: [{ pts: [[cx + rx * 0.35, rimY], [cx + rx, rimY], [cx + bx, rimY + h + 20], [cx + bx * 0.25, rimY + h + 20]], color: C.steelD, alpha: 0.55 }] });
  // rim highlight
  ink(ctx, ellipse(cx, rimY + 4, rx * 0.86, ry * 0.7, 30, Math.PI * 0.15, Math.PI * 0.55), 4, { color: C.steelL, seed: seed + 3 });
}
// a mound of flakes: dry = crisp flakes; soft = darker, glossy; mash = smooth with fork grooves
export function drawFood(ctx, cx, rimY, w, mh, kind, seed = 650) {
  const R = rng(seed);
  const mound = [];
  for (let i = 0; i <= 28; i++) {
    const u = i / 28, a = Math.PI * (1 - u), bump = kind === 'mash' ? 0.02 : 0.08;
    mound.push([cx + Math.cos(a) * w, rimY - Math.sin(a) * mh * (1 + (R() - 0.5) * bump * 2) + 6]);
  }
  mound.push([cx + w, rimY + 10], [cx - w, rimY + 10]);
  const base = kind === 'soft' ? C.soft : C.flake;
  shape(ctx, mound, { fill: base, line: 3.6, seed: seed + 1, grain: 0.4 });
  ctx.save(); path(ctx, mound); ctx.clip();
  if (kind === 'mash') {
    for (let k = 0; k < 5; k++) { const y0 = rimY - mh * (0.2 + k * 0.15); ink(ctx, [[cx - w * 0.6, y0 + 6], [cx - w * 0.2, y0], [cx + w * 0.3, y0 + 4], [cx + w * 0.65, y0 - 2]], 2.4, { color: C.flakeD, seed: seed + 10 + k, breaks: 0.35 }); }
  } else {
    const n = 46;
    for (let i = 0; i < n; i++) {
      const fx = cx + (R() - 0.5) * 2 * w, fy = rimY - R() * mh * 1.05, r = 9 + R() * 12, a = R() * TAU;
      const pts = []; const m = 5 + Math.floor(R() * 2);
      for (let j = 0; j < m; j++) { const aa = a + j * TAU / m, rr = r * (0.55 + R() * 0.5); pts.push([fx + Math.cos(aa) * rr * 1.4, fy + Math.sin(aa) * rr * 0.6]); }
      const col = R() < 0.5 ? (kind === 'soft' ? C.flake : C.flakeL) : C.flakeD;
      shape(ctx, pts, { fill: col, line: R() < 0.35 ? 1.8 : 0, seed: seed + 20 + i, grain: 0.2, breaks: 0.4 });
    }
    if (kind === 'soft') for (let i = 0; i < 7; i++) sparkle(ctx, cx + (R() - 0.5) * w * 1.4, rimY - R() * mh * 0.9, 9 + R() * 6, { fill: C.card, alpha: 0.85 });
  }
  ctx.restore();
}
// falling flakes between two points (u = time phase)
export function flakeStream(ctx, from, to, u, n = 16, seed = 700) {
  const R = rng(seed);
  for (let i = 0; i < n; i++) {
    const k = ((u * 1.6 + i / n) % 1), wob = (R() - 0.5) * 40;
    const x = lerp(from[0], to[0], k) + wob * k, y = lerp(from[1], to[1], k * k * 0.6 + k * 0.4);
    const r = 7 + R() * 7, a = R() * TAU + u * 6;
    const pts = []; for (let j = 0; j < 5; j++) { const aa = a + j * TAU / 5; pts.push([x + Math.cos(aa) * r * 1.3, y + Math.sin(aa) * r * 0.7]); }
    shape(ctx, pts, { fill: R() < 0.5 ? C.flakeL : C.flake, line: 1.6, seed: seed + i, grain: 0.1, breaks: 0.4 });
  }
}

// ---------- a 1950s bathroom scale (3/4 view). Origin: front-left corner of the top face. ----------
export function drawScale(ctx, x, y, o = {}) {
  const { w = 440, d = 70, h = 64, kg = 0 } = o;
  shape(ctx, [[x, y], [x + 40, y - d], [x + w + 40, y - d], [x + w, y]], { fill: C.card, line: 4.2, seed: 660, grain: 0.25 });
  // rubber mat ribs
  for (let i = 1; i < 9; i++) { const u = i / 9; ink(ctx, [[x + 40 * 0.25 + w * u, y - d * 0.25], [x + 40 * 0.8 + w * u, y - d * 0.8]], 2.4, { color: C.paperD, seed: 661 + i }); }
  shape(ctx, rrect(x, y, w, h, 14), { fill: C.teal, line: 4.2, seed: 670, grain: 0.3, shade: [{ pts: rect(x, y + h * 0.6, w, h), color: C.tealD, alpha: 0.7 }] });
  // the dial window on the front
  const dx = x + w / 2, dy = y + h * 0.5;
  shape(ctx, ellipse(dx, dy, 52, 40, 32), { fill: C.card, line: 4, seed: 671, grain: 0.2 });
  ink(ctx, [[dx, dy + 30], [dx, dy - 26]], 3, { seed: 672, color: C.ink, alpha: 0.5 });
  text(ctx, String(Math.round(kg)), dx, dy + 14, { font: '30px Slab', fill: C.ink, align: 'center' });
  return { dial: [dx, dy] };
}
// the dial seen in the call-out (native scale): 0..60 kg, needle at kg
export function drawDial(ctx, kg, R = 150) {
  shape(ctx, ellipse(0, 0, R, R, 64), { fill: C.card, line: 4.5, seed: 680, grain: 0.15 });
  const ang = v => (-220 + v / 60 * 260) * Math.PI / 180;
  for (let v = 0; v <= 60; v += 2) {
    const a = ang(v), big = v % 10 === 0, r0 = R * (big ? 0.72 : 0.8);
    ink(ctx, [[Math.cos(a) * r0, Math.sin(a) * r0], [Math.cos(a) * R * 0.95, Math.sin(a) * R * 0.95]], big ? 4 : 2.2, { seed: 681 + v, taper: false });
    if (big) {
      const tr = R * 0.64;
      if (v === 30) shape(ctx, ellipse(Math.cos(a) * tr, Math.sin(a) * tr, 34, 30, 24), { fill: C.tealL, line: 3, seed: 690, grain: 0.1 });
      text(ctx, String(v), Math.cos(a) * tr, Math.sin(a) * tr + 11, { font: '30px Slab', fill: C.ink, align: 'center' });
    }
  }
  text(ctx, 'kg', 0, R * 0.5, { font: '600 26px Jost', fill: C.inkSoft, align: 'center' });
  const a = ang(kg);
  shape(ctx, [[Math.cos(a) * R * 0.44, Math.sin(a) * R * 0.44], [Math.cos(a + 1.57) * 9, Math.sin(a + 1.57) * 9], [Math.cos(a + Math.PI) * 26, Math.sin(a + Math.PI) * 26], [Math.cos(a - 1.57) * 9, Math.sin(a - 1.57) * 9]], { fill: C.ink, line: 0, seed: 691, grain: 0, off: [0, 0] });
  shape(ctx, ellipse(0, 0, 13, 13, 16), { fill: C.mustard, line: 3, seed: 692, grain: 0.1 });
}

// ---------- jug (warm water) and fork ----------
export function drawJug(ctx, x, y, rot = 0, s = 1) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
  ink(ctx, spline([[54, -96], [96, -84], [100, -40], [58, -30]], false, 8), 9, { seed: 720, taper: false });
  shape(ctx, spline([[-50, -120], [52, -120], [60, -60], [56, 0], [-56, 0], [-60, -60]], true, 6).concat([]), { fill: C.card, line: 4.2, seed: 721, grain: 0.25,
    shade: [{ pts: rect(-70, -78, 140, 26), color: C.teal }] });
  shape(ctx, [[-50, -120], [-92, -136], [-84, -112], [-58, -100]], { fill: C.card, line: 4, seed: 722, grain: 0.2 });
  ctx.restore();
}
export function drawFork(ctx, x, y, rot = 0, s = 1) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
  shape(ctx, rrect(-10, -250, 20, 170, 10), { fill: C.steel, line: 4, seed: 730, grain: 0.15 });
  shape(ctx, spline([[-34, -84], [34, -84], [30, -40], [-30, -40]], true, 4), { fill: C.steel, line: 4, seed: 731, grain: 0.15 });
  for (let i = 0; i < 4; i++) { const tx = -27 + i * 18; shape(ctx, rrect(tx - 5, -44, 10, 54, 5), { fill: C.steel, line: 3.4, seed: 732 + i, grain: 0.1 }); }
  ctx.restore();
}
// steam / aroma curls rising (u = phase)
export function steam(ctx, x, y, u, n = 3, h = 140) {
  for (let i = 0; i < n; i++) {
    const ph = (u * 0.7 + i / n) % 1, x0 = x + (i - (n - 1) / 2) * 46;
    const pts = []; for (let j = 0; j <= 16; j++) { const v = j / 16; pts.push([x0 + Math.sin(v * 7 + u * 4 + i) * 14, y - v * h - ph * 30]); }
    ink(ctx, pts, 4.4, { color: C.card, seed: 740 + i, alpha: 0.9 * Math.sin(Math.PI * Math.min(1, ph + 0.15)) });
  }
}

// ---------- the 1950s sunburst wall clock ----------
export function drawClock(ctx, x, y, r, t = 0) {
  for (let i = 0; i < 12; i++) {
    const a = i * TAU / 12, r1 = r * (i % 3 === 0 ? 1.9 : 1.55);
    ink(ctx, [[x + Math.cos(a) * r * 1.05, y + Math.sin(a) * r * 1.05], [x + Math.cos(a) * r1, y + Math.sin(a) * r1]], i % 3 === 0 ? 6 : 4, { seed: 750 + i, taper: true });
    shape(ctx, ellipse(x + Math.cos(a) * r1, y + Math.sin(a) * r1, 9, 9, 12), { fill: C.mustard, line: 2.6, seed: 762 + i, grain: 0.1 });
  }
  shape(ctx, ellipse(x, y, r, r, 40), { fill: C.card, line: 4.2, seed: 775, grain: 0.2 });
  const hA = -Math.PI / 2 + 0.52 + t * 0.0001, mA = -Math.PI / 2 + t * 0.105;
  ink(ctx, [[x, y], [x + Math.cos(hA) * r * 0.5, y + Math.sin(hA) * r * 0.5]], 6, { seed: 776, taper: false });
  ink(ctx, [[x, y], [x + Math.cos(mA) * r * 0.78, y + Math.sin(mA) * r * 0.78]], 4, { seed: 777, taper: false });
  shape(ctx, ellipse(x, y, 7, 7, 10), { fill: C.teal, line: 0, seed: 778, grain: 0, off: [0, 0] });
}
