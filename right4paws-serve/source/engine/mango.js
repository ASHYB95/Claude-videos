// Mango: a ginger Indie (Indian Pariah) dog, drawn as a 1950s geometric cartoon.
// Held body (limited animation): only eyes, brows, ears, mouth and tail move.
// Local units: floor at y = 0, ear tip near y = -640. dir = 1 faces right.
import { shape, ink, ellipse, spline, xform, rrect, TAU, reg, move } from './toon.js';
import { C } from './pal.js';

// o: { s, dir, blink 0..1, look [dx,dy], tail (radians of wag), mouth: 'smile'|'open'|'lick'|'grin', ear 0..1 (perk), brow -1..1 }
export function drawMango(ctx, x, y, o = {}) {
  const { s = 1, dir = 1, blink = 0, look = [0, 0], tail = 0, mouth = 'smile', ear = 0, brow = 0, collar = true } = o;
  const T = pts => pts.map(([px, py]) => [x + px * s * dir, y + py * s]);
  const E = (cx, cy, rx, ry, n = 32, rot = 0) => T(ellipse(cx, cy, rx, ry, n, 0, TAU, rot));
  const S = (pts, n = 8) => T(spline(pts, true, n));
  const lw = 4.2;

  // tail (question-mark curl), pivots at its base
  {
    const base = [-120, -70], c = Math.cos(tail), si = Math.sin(tail);
    const raw = [[-120, -70], [-190, -105], [-232, -185], [-222, -262], [-178, -292], [-142, -268], [-152, -232]];
    const rot = raw.map(([px, py]) => { const dx = px - base[0], dy = py - base[1]; return [base[0] + c * dx - si * dy, base[1] + si * dx + c * dy]; });
    const P = T(spline(rot, false, 8));
    ink(ctx, P, 34 * s, { seed: 501, taper: true, wob: 0.1 });
    const off = reg(502, 1);
    ink(ctx, move(P, off[0] * 0.6, off[1] * 0.6), 24 * s, { seed: 503, taper: true, wob: 0.06, color: C.ginger });
  }
  // body: sitting pear
  const body = [[-150, 0], [-178, -70], [-162, -170], [-112, -252], [-52, -330], [-2, -382], [40, -404], [86, -388], [106, -300], [98, -180], [92, -90], [82, 0]];
  shape(ctx, S(body), { fill: C.ginger, line: lw, seed: 510, grain: 0.32, shade: [{ pts: E(-150, -120, 80, 140), color: C.gingerD }] });
  // chest blaze
  shape(ctx, S([[30, -350], [86, -336], [102, -262], [90, -165], [60, -112], [34, -170], [20, -280]]), { fill: C.white, line: 0, seed: 511, grain: 0.15 });
  // haunch + back paw
  shape(ctx, E(-74, -84, 104, 86, 40, -0.25), { fill: C.ginger, line: lw, seed: 512, grain: 0.3, shade: [{ pts: E(-120, -40, 90, 50), color: C.gingerD, alpha: 0.85 }] });
  shape(ctx, E(-6, -12, 56, 17), { fill: C.white, line: lw, seed: 513, grain: 0.15 });
  // front legs (far one darker), white socks
  [[38, C.gingerD, 514], [92, C.ginger, 516]].forEach(([lx, col, sd]) => {
    shape(ctx, T(rrect(lx - 19, -246, 38, 232, 18)), { fill: col, line: lw, seed: sd, grain: 0.3, shade: [{ pts: T(rrect(lx - 22, -70, 44, 70, 10)), color: C.white }] });
    shape(ctx, E(lx + 12, -12, 33, 15), { fill: C.white, line: lw, seed: sd + 1, grain: 0.15 });
  });
  // collar + tag
  if (collar) {
    const band = T(spline([[-22, -348], [40, -324], [102, -344]], false, 8));
    ink(ctx, band, 26 * s, { seed: 520, taper: false, wob: 0.05 });
    const off = reg(521, 1);
    ink(ctx, move(band, off[0] * 0.5, off[1] * 0.5), 17 * s, { seed: 521, taper: false, wob: 0.03, color: C.teal });
    shape(ctx, E(42, -300, 15, 15, 20), { fill: C.mustard, line: 3, seed: 522, grain: 0.2 });
  }
  // ears (behind the skull): far one flopped, near one up (perks with `ear`)
  shape(ctx, S([[-44, -492], [-92, -566], [-128, -548], [-122, -494], [-74, -466]]), { fill: C.gingerD, line: lw, seed: 530, grain: 0.3 });
  const tipY = -640 - ear * 16;
  shape(ctx, S([[-22, -500], [-48, -590], [-30, tipY], [6, -598], [42, -512]]), { fill: C.ginger, line: lw, seed: 531, grain: 0.3,
    shade: [{ pts: S([[-10, -510], [-30, -585], [-24, tipY + 34], [0, -592], [24, -520]]), color: C.pink, alpha: 0.9 }] });
  // head: skull + snout in one outline (the muzzle is part of the head line)
  const head = [[-78, -440], [-58, -500], [0, -526], [62, -506], [98, -472], [152, -458], [192, -444], [204, -414], [184, -392], [122, -380], [70, -364], [10, -360], [-50, -380], [-82, -410]];
  shape(ctx, S(head), { fill: C.ginger, line: lw, seed: 540, grain: 0.3,
    shade: [{ pts: S([[96, -470], [152, -458], [192, -444], [204, -414], [184, -392], [122, -380], [84, -386], [86, -440]]), color: C.gingerL }] });
  // nose
  shape(ctx, E(194, -440, 17, 13, 20), { fill: C.ink, line: 0, seed: 541, grain: 0, off: [0, 0] });
  // mouth
  if (mouth === 'open' || mouth === 'lick') {
    shape(ctx, S([[186, -404], [160, -378], [120, -372], [104, -392], [140, -396]]), { fill: C.ink, line: 3, seed: 542, grain: 0 });
    shape(ctx, S([[160, -386], [150, -352], [132, -350], [124, -378]]), { fill: C.pink, line: 3, seed: 543, grain: 0.1 });
  } else {
    ink(ctx, T(spline([[188, -402], [150, -392], [116, -394], [104, -406]], false, 6)), 3.6, { seed: 544 });
    if (mouth === 'grin') ink(ctx, T([[104, -406], [98, -416]]), 3.4, { seed: 545 });
  }
  // eyes (near + far), brows
  const ey = -458, eyes = [[86, ey, 1], [36, ey - 4, 0.82]];
  for (const [ex, eyy, k] of eyes) {
    if (blink > 0.5) ink(ctx, T([[ex - 10 * k, eyy], [ex + 10 * k, eyy + 2]]), 3.6, { seed: 546 });
    else shape(ctx, E(ex + look[0], eyy + look[1], 8 * k, 12 * k, 16), { fill: C.ink, line: 0, seed: 547, grain: 0, off: [0, 0] });
    ink(ctx, T([[ex - 14 * k, eyy - 26 - brow * 4], [ex + 12 * k, eyy - 24 + brow * 6]]), 3.4, { seed: 548 });
  }
}
