// The Mound of the Dead — Isometric Picture Book, 1920×1080, 30 fps, 45.5 s.
// One world at one scale: the lower town of Mohenjo-daro (a grid of blocks, a main street with a covered drain),
// the citadel mound to the west (Great Bath, granary), the Indus to the east. The camera travels; nothing cuts.
import { C, W, H, iso, tri, mix, hex, css, TAU, clamp, lerp, seg, ss, eo, eio, hash, onPlane, fillPoly, rect, phraseLayout, floorType, drawPerson } from './kit.js';
export const DUR = 45.5;
const B = { brick: '#B8683F', brickLt: '#D49268', roof: '#C98760', street: '#E6D3B2', lane: '#DCC7A3', water: '#5E9C98', waterD: '#3E7C7A', sand: '#E8D2A6', sandD: '#D9BE8C', sandL: '#F1E2C2', ink: '#2A2420', accent: '#D0573A',
  cloth: ['#C9A24A', '#8FA7B8', '#9C8AA6', '#E2D3B0', '#B8714A'] };
const BRICK = tri(B.brick, .2, .22), BRICKL = tri(B.brickLt, .2, .2), ROOF = tri(B.roof, .25, .2);

// ———— narration (am_michael) and subtitle cues
export const LINES = [
  { id: 'v1', t: 0.6, d: 7.748, cues: ['Four and a half thousand years ago, while Egypt built its pyramids,', 'a city on the Indus had drains under every street.'] },
  { id: 'v2', t: 8.8, d: 5.969, cues: ['This is Mohenjo-daro.', 'With Harappa, it was the heart of the Indus Valley Civilisation.'] },
  { id: 'v3', t: 15.2, d: 6.511, cues: ['Streets ran in a grid.', 'Bricks were baked to the same proportions.', 'Most homes had their own bathroom.'] },
  { id: 'v4', t: 22.2, d: 4.924, cues: ['Merchants stamped their goods with seals,', 'in a script no one can read, to this day.'] },
  { id: 'v5', t: 27.6, d: 6.503, cues: ['Around 1900 BCE, the rivers shifted,', 'the monsoon weakened, and the cities emptied.'] },
  { id: 'v6', t: 34.6, d: 7.462, cues: ['Four thousand years later, archaeologists dug into a mound called Mohenjo-daro.', 'The Mound of the Dead.'] },
];
export const SUBS = [];
LINES.forEach((L, i) => {
  const tot = L.cues.reduce((a, c) => a + c.length, 0), nx = LINES[i + 1], end = Math.min(L.t + L.d + .6, nx ? nx.t - .1 : DUR);
  let t0 = L.t - .1; L.cues.forEach((c, k) => { const t1 = k === L.cues.length - 1 ? end : t0 + L.d * c.length / tot + .1; SUBS.push({ t0, t1, text: c }); t0 = t1; });
});
const CUE = i => SUBS[i].t0 + .1;
const T = { lift: 1.0, ad: 1.6, wide: [8.6, 11.2], name: 9.6, grid: CUE(4), brick: CUE(5), home: CUE(6), market: 22.0, stamp: 22.6, glyph: CUE(8), decline: 27.6, yr: 28.0, bury: [34.6, 36.4], y1922: 36.6, dig: [37.2, 40.0], title: 40.4 };

// ———— camera keys [t, x, y, z, k]
const KEYS = [[0, 26, -2, 0, 18], [8.4, 33, -4, 0, 20], [11.2, -74, 12, 0, 9.6], [15.0, -70, 10, 0, 9.4], [16.6, -32, -2, 0, 9.2], [17.6, 3.4, -.6, 0, 90], [19.4, 3.5, -.5, 0, 86],
  [20.4, 3.6, -7.2, 1.4, 52], [22.0, 3.4, -7.6, 1.6, 50], [22.8, -29, 0, 0, 44], [27.4, -30, 0, 0, 46], [29.6, -8, 2, 0, 10.6], [34.4, -10, 2, 0, 10.2], [36.6, -5, -8, 0, 21], [40.2, -5, -8, 0, 22], [42.4, 1, -3, 0, 15.2], [DUR, 1.5, -3.4, 0, 15.6]];
function camAt(t) {
  let i = 0; while (i < KEYS.length - 2 && t >= KEYS[i + 1][0]) i++;
  const a = KEYS[i], b = KEYS[i + 1], u = eio(seg(t, a[0], b[0]));
  return { x: lerp(a[1], b[1], u), y: lerp(a[2], b[2], u), z: lerp(a[3], b[3], u), k: Math.exp(lerp(Math.log(a[4]), Math.log(b[4]), u)) };
}

// ———— the city plan
const COLS = [-64, -34, -4, 26], ROWS = [-45, -15, 15, 45];
const HOUSES = [];
COLS.forEach(cx => ROWS.forEach(cy => [-11, 1].forEach(x0 => [-11, 1].forEach(y0 => {
  const id = HOUSES.length, s = hash(id * 1.7 + 3);
  HOUSES.push({ id, x: cx + x0, y: cy + y0, w: 10, d: 10, h: 4.4 + (s * 3 | 0) * 1.2, near: cy === 15 && y0 === -11, far: cy === -15 && y0 === 1 });
}))));
const HERO = HOUSES.find(h => h.x === -3 && h.y === -14);
const STREETS_X = [-79, -49, -19, 11, 41], STREETS_Y = [-30, 0, 30];
const PEOPLE = [];
for (let i = 0; i < 18; i++) PEOPLE.push({ x0: -80 + hash(i * 3.3) * 140, y: -2.6 + hash(i * 7.1) * 4.6, v: (hash(i) < .5 ? 1 : -1) * (1 + hash(i * 2) * .5), top: B.cloth[i % 5], legs: ['#7A5A40', '#6A5444', '#5A4A3A'][i % 3], pot: i % 3 === 0, skirt: i % 3 === 0 ? B.cloth[(i + 2) % 5] : null });

// ———— drawing
function house(hs, t, o = {}) {
  const { x, y, w, d } = hs, h = hs.h * (o.sink ?? 1);
  if (h < .05) return;
  const th = .6, col = BRICK, hn = o.cut ? Math.min(1.3, h) : h;
  const hf = o.cut && !o.keepBack ? hn : h;   // a cut house drops all its walls (a near house would hide the street)
  iso.box(x, y, 0, w, th, hf, col); iso.box(x, y + d - th, 0, w, th, hn, col);
  iso.box(x, y + th, 0, th, d - 2 * th, hf, col); iso.box(x + w - th, y + th, 0, th, d - 2 * th, hn, col);
  if (!o.cut && !o.noRoof) { iso.box(x, y, h, w, d, .35, ROOF); if (hash(hs.id) < .5) iso.box(x + w * .62, y + d * .2, h + .35, 1.8, 1.8, 1.0, ROOF); }
  if (!o.cut && hs.far) for (let k = 0; k < 3; k++) iso.box(x + 1.4 + k * 2.6, y + d - .02, h * .62, .7, .05, .55, tri('#4A2E22', .1, .1), { bias: .02 });
  if (o.cut) { iso.flat(rect(x + th, x + w - th, y + th, y + d - th), .02, '#D9C29C'); iso.box(x + 1.2, y + 1.4, 0, 1.4, 1.4, .25, tri('#9E5A36', .2, .2)); }
}
function well(x, y, s = 1) { iso.cyl(x, y, 0, .9 * s, .9, BRICK); iso.flat([[x - .55, y - .55], [x + .55, y - .55], [x + .55, y + .55], [x - .55, y + .55]], .92, '#2B3B3A', { layer: 1, depth: x + y + 1.9 }); }
function ground() {
  iso.flat(rect(-170, 64, -75, 75), 0, B.lane, { depth: -1e6 });
  for (const sx of STREETS_X) iso.flat(rect(sx - 4, sx + 4, -62, 62), .002, B.street, { depth: -9e5 });
  for (const sy of STREETS_Y) iso.flat(rect(-94, 62, sy - 4, sy + 4), .003, B.street, { depth: -8e5 });
  iso.flat(rect(-100, -94, -62, 62), .002, B.street, { depth: -9e5 });
}
function drain(t, lifted) {
  iso.flat(rect(-94, 58, 2.6, 3.6), .005, '#8E4E30');
  for (let i = 0; i < 82; i++) {
    const x = -94 + i * 1.86, L = lifted(i);
    if (L > 0) {
      iso.flat(rect(x + .05, x + 1.8, 2.72, 3.48), .01, B.waterD);
      const ph = (t * 1.2 + i) % 1; iso.flat(rect(x + .2 + ph * .6, x + .9 + ph * .6, 2.95, 3.05), .015, '#9CC8C2', { a: .8 });
      const a = L * 1.15, cy = 2.65, s = [[x, cy, .12], [x + 1.8, cy, .12], [x + 1.8, cy + .9 * Math.cos(a), .12 + .9 * Math.sin(a)], [x, cy + .9 * Math.cos(a), .12 + .9 * Math.sin(a)]];
      iso.add(x + cy + .6, () => iso.face3(s, tri('#A9603C', .25, .2), { both: true }), 1);
    } else iso.box(x + .03, 2.65, 0, 1.8, .9, .12, tri('#A9603C', .22, .22));
  }
}
function river(t, recede = 0) {
  const x0 = 62 + recede * 40, wdt = 80 * (1 - recede * .6);
  iso.flat(rect(58, x0 + 2, -80, 80), .001, '#C9B48E', { depth: -7e5 });
  if (recede > 0) iso.flat(rect(62, x0, -80, 80), .002, B.sandD, { depth: -6.9e5 });
  iso.flat(rect(x0, x0 + wdt, -80, 80), .003, B.water, { depth: -6.8e5 });
  for (let k = 0; k < 16; k++) { const yy = -60 + k * 8, ph = (t * .6 + k * .37) % 1; iso.flat(rect(x0 + 4 + ph * 30, x0 + 10 + ph * 30, yy, yy + .25), .01, '#86BDB6', { a: .7 * (1 - recede) }); }
  if (recede < .5) { const bx = 78 + Math.sin(t * .3) * 2, by = -8;
    iso.box(bx, by, .05, 7, 1.6, .5, tri('#9C7A4E', .2, .2)); iso.box(bx + 3.3, by + .7, .55, .18, .18, 4.4, tri('#5A4430', .1, .1));
    iso.add(bx + by + 5, () => iso.face3([[bx + 3.4, by + .2, 1.3], [bx + 3.4, by + 1.5, 1.3], [bx + 3.4, by + 1.5, 4.8], [bx + 3.4, by + .2, 4.8]], tri('#EADCC0', .1, .15), { both: true }), 1); }
}
function citadel(t, sink = 1) {
  const z = 7 * sink;
  if (z < .1) return;
  iso.box(-148, -34, 0, 48, 52, z, tri('#C08A5C', .22, .2), { cull: false });
  if (sink < .98) return;
  const bx = -132, by = -14;   // the Great Bath: a sunken pool with steps, ringed by rooms
  iso.flat(rect(bx - 3, bx + 15, by - 3, by + 10), z + .02, '#D9B48A');
  iso.flat(rect(bx, bx + 12, by, by + 7), z + .03, B.waterD); iso.flat(rect(bx + .6, bx + 11.4, by + .6, by + 6.4), z + .04, B.water);
  const ph = (t * .4) % 1; iso.flat(rect(bx + 1 + ph * 8, bx + 3 + ph * 8, by + 3, by + 3.15), z + .05, '#9CC8C2', { a: .8 });
  for (let k = 0; k < 6; k++) iso.box(bx - 4 + k * 3.4, by - 6, z, 2.6, 1.2, 2.4, BRICK);
  for (let k = 0; k < 6; k++) iso.box(bx - 4 + k * 3.4, by + 11, z, 2.6, 1.2, 1.6, BRICKL);
  for (let a = 0; a < 3; a++) for (let b2 = 0; b2 < 4; b2++) iso.box(-145 + a * 4.2, 6 + b2 * 2.6, z, 3.6, 2, 1.8, BRICK);   // the granary
  iso.box(-112, -30, z, 8, 8, 3.2, BRICK); iso.box(-112, 8, z, 9, 7, 2.8, BRICK);
  for (let k = 0; k < 3; k++) person(bx + 2 + k * 3, by - 1.6, z, { top: B.cloth[k + 1], legs: '#6A5444' }, { walking: true, phase: t * 4 + k });
}
function palm(x, y, h = 6) {
  iso.cyl(x, y, 0, .22, h, tri('#8A6A48', .2, .2));
  iso.bill(x, y, h, g => { const sw = Math.sin(performance.now ? 0 : 0); for (let k = 0; k < 7; k++) { g.save(); g.rotate(k / 7 * TAU); g.beginPath(); g.ellipse(1.1, 0, 1.3, .28, 0, 0, TAU); g.fillStyle = k % 2 ? '#6E8A50' : '#5F7A4A'; g.fill(); g.restore(); } }, { r: 3 });
}
function person(x, y, z, p, s = {}) {
  iso.bill(x, y, z, g => {
    drawPerson(g, { h: p.h || 1.7, top: p.top, legs: p.legs, skirt: p.skirt, hairLong: !!p.skirt }, s);
    const bob = s.walking ? Math.abs(Math.cos(s.phase)) * .02 : 0;
    if (p.pot) { g.beginPath(); g.ellipse(0, -1.78 - bob, .16, .14, 0, 0, TAU); g.fillStyle = '#B5603A'; g.fill(); g.beginPath(); g.ellipse(.05, -1.78 - bob, .1, .13, 0, 0, TAU); g.fillStyle = '#8E4A2C'; g.fill(); }
    if (p.hat) { g.fillStyle = '#ECE3CE'; g.beginPath(); g.ellipse(0, -1.62, .21, .055, 0, 0, TAU); g.fill(); g.beginPath(); g.ellipse(0, -1.64, .12, .1, 0, Math.PI, TAU); g.fill(); }
    if (p.tool) { const dg = (s.dig || 0) * .25; g.strokeStyle = '#5A4430'; g.lineWidth = .05; g.beginPath(); g.moveTo(.18, -1.05 + dg); g.lineTo(.42, -.08 + dg * .4); g.stroke(); g.fillStyle = '#6A6A62'; g.fillRect(.36, -.14 + dg * .4, .14, .12); }
    if (p.basket) { g.beginPath(); g.ellipse(-.22, -.95, .18, .1, 0, 0, TAU); g.fillStyle = '#B79A62'; g.fill(); }
  }, { r: 2 });
}
function walkers(t, leave) {
  for (const p of PEOPLE) {
    let x = p.x0 + p.v * t; x = ((x + 95) % 155 + 155) % 155 - 95; let dir = Math.sign(p.v);
    if (t > T.brick - .6 && t < T.home + 1.2 && Math.abs(x - 3) < 10) continue;
    if (leave) { x = x + 26 * ss(seg(t, T.decline, T.decline + 6)) + Math.max(0, t - T.decline) * 1.4; dir = 1; if (x > 66) continue; }
    person(x, p.y, 0, p, { walking: true, phase: x / .7 * Math.PI * dir });
  }
}
// floor glyphs: invented Indus-like signs, painted on the floor (metres)
const GLYPHS = [
  g => { g.moveTo(0, 0); g.lineTo(0, -1); g.moveTo(-.3, -.2); g.lineTo(.3, -.2); g.moveTo(-.3, -.5); g.lineTo(.3, -.5); g.moveTo(-.3, -.8); g.lineTo(.3, -.8); },
  g => { g.ellipse(0, -.5, .35, .5, 0, 0, TAU); g.moveTo(-.35, -.5); g.lineTo(.35, -.5); },
  g => { g.moveTo(-.4, -.5); g.quadraticCurveTo(0, -1.1, .4, -.5); g.quadraticCurveTo(0, .1, -.4, -.5); g.moveTo(.4, -.5); g.lineTo(.6, -.25); g.moveTo(.4, -.5); g.lineTo(.6, -.75); },
  g => { g.moveTo(-.3, 0); g.lineTo(-.3, -1); g.moveTo(0, 0); g.lineTo(0, -1); g.moveTo(.3, 0); g.lineTo(.3, -1); },
  g => { g.moveTo(-.35, 0); g.lineTo(0, -1); g.lineTo(.35, 0); g.moveTo(-.2, -.4); g.lineTo(.2, -.4); },
  g => { g.moveTo(.45, -.5); g.arc(0, -.5, .45, 0, TAU); g.moveTo(-.45, -.5); g.lineTo(.45, -.5); g.moveTo(0, -.95); g.lineTo(0, -.05); },
];
function glyphRow(g, t, x, y, t0, scale = 1) {
  GLYPHS.forEach((fn, i) => {
    const tc = t0 + i * .16, a = eo(seg(t, tc, tc + .3)); if (a <= 0) return;
    const sc = lerp(1.22, 1, eo(seg(t, tc, tc + .34))) * scale, fade = 1 - ss(seg(t, T.decline - .3, T.decline));
    onPlane(g, x + (i / 3 | 0) * 1.65 * scale, y - (i % 3) * 1.35 * scale, .02, 'xy', g2 => { g2.globalAlpha = a * fade; g2.scale(sc, sc); g2.beginPath(); fn(g2); g2.strokeStyle = css(mix(C.ghost, B.ink, ss(seg(t, tc + .1, tc + .5)))); g2.lineWidth = .1; g2.lineCap = 'round'; g2.lineJoin = 'round'; g2.stroke(); });
  });
}
const PH = {};
function phrase(g, t, key, P) { if (!PH[key]) PH[key] = phraseLayout(P); floorType(g, t, P, PH[key]); }

// ———— the brick demo: real bricks laid up as one big brick, 0.6 × 1.2 × 2.4 m (1 : 2 : 4)
const BS = { x: 1.0, y: -2.7, L: 2.4, Wd: 1.2, Hh: .6 };
function brickStack(t) {
  const { x, y, L, Wd, Hh } = BS, rise = eo(seg(t, T.brick - .2, T.brick + .5));
  iso.box(x, y, 0, L, Wd, Hh * rise, BRICK, { decal: I => {
    const g = I.g; g.save(); g.strokeStyle = 'rgba(90,45,28,.35)'; g.lineWidth = 1;
    for (let k = 1; k < 8 * rise; k++) { const z = k * .075; g.beginPath(); g.moveTo(...I.P(x, y + Wd, z)); g.lineTo(...I.P(x + L, y + Wd, z)); g.lineTo(...I.P(x + L, y, z)); g.stroke();
      for (let j = 0; j < 9; j++) { const xx = x + (j + (k % 2) * .5) * .28; if (xx < x + L) { g.beginPath(); g.moveTo(...I.P(xx, y + Wd, z)); g.lineTo(...I.P(xx, y + Wd, z - .075)); g.stroke(); } } }
    g.restore(); } });
  const e = [[[x, y + Wd, 0], [x, y + Wd, Hh]], [[x + L, y, 0], [x + L, y + Wd, 0]], [[x, y + Wd, 0], [x + L, y + Wd, 0]]];
  e.forEach((s3, i) => { const p = eo(seg(t, T.brick + .5 + i * .35, T.brick + .9 + i * .35)); if (p <= 0) return;
    const fade = 1 - ss(seg(t, T.home + .2, T.home + .6));
    iso.add(2e5 + i, () => { const g = iso.g, a = iso.P(...s3[0]), c = iso.P(lerp(s3[0][0], s3[1][0], p), lerp(s3[0][1], s3[1][1], p), lerp(s3[0][2], s3[1][2], p));
      g.save(); g.globalAlpha = fade; g.strokeStyle = B.accent; g.lineWidth = 7; g.lineCap = 'round'; g.beginPath(); g.moveTo(...a); g.lineTo(...c); g.stroke(); g.restore(); }, 2); });
}

// floor phrases (shared by the picture and the sound events)
const t1b = () => T.home + .3;
const SPEC = {
  y2600: { x: 50, y: 7.5, z: .02, t0: T.ad, t1: T.wide[0] - .2, step: .1, scale: 1.7, lines: [[['2600', 'na'], [' BCE', 'n']]] },
  name: { x: -128, y: 66, z: .02, t0: T.name, t1: T.grid, step: .05, scale: 6.4, lines: [[['MOHENJO-DARO', 'e']], [['with Harappa · the Indus Valley Civilisation', 'en']]], dv: 1.25, indent: 0 },
  e1: { x: BS.x - .1, y: BS.y + BS.Wd + .5, z: .02, t0: T.brick + .5, t1: T.home + .3, scale: .36, lines: [[['1', 'n']]] },
  e2: { x: BS.x + BS.L + .9, y: BS.y + BS.Wd * .5 + .25, z: .02, t0: T.brick + .85, t1: T.home + .3, scale: .36, lines: [[['2', 'n']]] },
  e4: { x: BS.x + BS.L * .5 + .3, y: BS.y + BS.Wd + .95, z: .02, t0: T.brick + 1.2, t1: T.home + .3, scale: .36, lines: [[['4', 'n']]] },
  ratio: { x: BS.x + 5.2, y: 1.5, z: .02, t0: T.brick + 1.5, t1: T.home + .3, step: .07, scale: .6, lines: [[['1 : 2 : 4', 'n']], [['every brick, in every city', 'en']]], dv: 1.2, indent: 0 },
  q: { x: -27.6 + 2 * 1.65 * 1.25 + 1.2, y: .6, z: .02, t0: T.glyph + 1.1, t1: T.decline - .2, scale: 1.1, lines: [[['?', 'na']]] },
  y1900: { x: -6, y: 12, z: .02, t0: T.yr, t1: T.bury[0], step: .12, scale: 3.2, lines: [[['1900', 'na'], [' BCE', 'n']]] },
  y1922: { x: 9.5, y: 4, z: .03, t0: T.y1922, t1: T.title - .3, step: .12, scale: 2.6, lines: [[['1922', 'na']]] },
  title: { x: 16.5, y: 16, z: .03, t0: T.title, t1: 99, step: .07, scale: 2.9, lines: [[['MOHENJO-DARO', 'e']], [['the Mound of the Dead', 'en']]], dv: 1.25, indent: .2 },
};
// ———— frame
export function render(g, t) {
  iso.g = g; iso.cam = camAt(t);
  const decline = ss(seg(t, T.decline, T.decline + 5)), bury = ss(seg(t, T.bury[0], T.bury[1]));
  iso.desat = .7 * decline * (1 - .65 * ss(seg(t, T.dig[0], T.title + .5))); iso.keep = false;
  g.fillStyle = B.lane; g.fillRect(0, 0, W, H);
  ground();
  river(t, decline);
  const sink = 1 - bury;
  const cutNear = (t < T.wide[0] + .4) || (t > T.brick + .6 && t < 27.4);
  const heroOpen = eio(seg(t, T.home + .3, T.home + 1.6));
  if (t < T.bury[1]) {
    drain(t, i => (i === 63 || i === 64 || i === 69) ? eo(seg(t, T.lift + (i - 63) * .25, T.lift + 1.2 + (i - 63) * .25)) : 0);
    citadel(t, sink);
    for (const hs of HOUSES) { if (hs === HERO && t > T.home - .5 && t < 27) continue; house(hs, t, { sink, cut: cutNear && hs.near && sink > .99, noRoof: sink < .99 }); }
    if (sink > .9) { well(20.5, -1.8); well(-40, 1.5); palm(59, 32); palm(57, -12, 7); palm(29.5, 7.5, 5.5); palm(-90, 20, 6); palm(-97, -40, 7); }
  }
  if (t > T.home - .5 && t < 27) heroHouse(g, t, heroOpen);
  if (t > T.brick - .3 && t < T.home + 1.0) brickStack(t);
  if (t > 20 && t < 28) market(t);
  if (t < T.bury[0]) walkers(t, t > T.decline);
  if (decline > 0) { iso.alpha = .5 * decline; iso.flat(rect(-94, 62, -62, 62), .2, B.sand, { depth: -5e5 }); iso.alpha = 1; }
  if (t > T.bury[0]) mound(t, bury);
  iso.flush();
  iso.desat = 0;
  // ——— floor type
  if (t < T.wide[0] + .6) phrase(g, t, 'y2600', SPEC.y2600);
  if (t > T.name - .2 && t < T.grid + .4) phrase(g, t, 'name', SPEC.name);
  if (t > T.grid && t < T.brick + .6) gridLights(g, t);
  if (t > T.brick && t < T.home + .9) {
    phrase(g, t, 'e1', SPEC.e1);
    phrase(g, t, 'e2', SPEC.e2);
    phrase(g, t, 'e4', SPEC.e4);
    phrase(g, t, 'ratio', SPEC.ratio);
  }
  if (t > T.glyph - .2 && t < T.decline + .3) { glyphRow(g, t, -27.6, 2.4, T.glyph, 1.25); phrase(g, t, 'q', SPEC.q); }
  if (t > T.yr - .2 && t < T.bury[0] + .5) phrase(g, t, 'y1900', SPEC.y1900);
  if (t > T.y1922 - .2 && t < T.title) phrase(g, t, 'y1922', SPEC.y1922);
  if (t > T.title - .2) phrase(g, t, 'title', SPEC.title);
  subtitle(g, t);
}
function gridLights(g, t) {
  const p1 = eo(seg(t, T.grid, T.grid + 1.0)), p2 = eo(seg(t, T.grid + .6, T.grid + 1.6)), fade = 1 - ss(seg(t, T.brick + .2, T.brick + .6));
  g.save(); g.globalAlpha = fade; g.strokeStyle = B.accent; g.lineWidth = 5; g.lineCap = 'round';
  for (const sy of STREETS_Y) { g.beginPath(); g.moveTo(...iso.P(-94, sy, .05)); g.lineTo(...iso.P(lerp(-94, 60, p1), sy, .05)); g.stroke(); }
  for (const sx of STREETS_X) { g.beginPath(); g.moveTo(...iso.P(sx, -60, .05)); g.lineTo(...iso.P(sx, lerp(-60, 60, p2), .05)); g.stroke(); }
  g.restore();
}
function heroHouse(g, t, open) {
  const hs = HERO, { x, y, w, d } = hs, h = 6;
  iso.flat(rect(x, x + w, y, y + d), .01, '#D9C29C');
  house({ ...hs, h }, t, { cut: open > .5, noRoof: true, keepBack: true });
  iso.box(x + 3.8, y + .6, 0, .35, 3.6, 2.6, BRICKL); iso.box(x + .6, y + 4.2, 0, 3.2, .35, 2.6, BRICKL);
  for (let k = 0; k < 6; k++) iso.box(x + w - 2.6, y + 1.0 + k * .45, 0, 1.8, .45, .35 + k * .42, BRICKL);
  well(x + 2.0, y + 2.2, .9);
  const bx = x + 5.0, by = y + 6.4;
  iso.box(bx, by, 0, 2.6, 2.6, .25, tri('#C27A52', .25, .2));
  for (let a = 0; a < 5; a++) for (let b2 = 0; b2 < 5; b2++) iso.flat(rect(bx + .1 + a * .5, bx + .5 + a * .5, by + .1 + b2 * .5, by + .3 + b2 * .5), .26, (a + b2) % 2 ? '#B56C46' : '#C9845B', { layer: 1, depth: bx + by + 3 });
  const prog = seg(t, T.home + 1.6, T.home + 3.0), fade = 1 - ss(seg(t, 22.0, 22.5));
  const path = [[bx + 2.5, by + 2.5, .27], [bx + 2.5, y + d - .3, .2], [bx + 2.5, y + d + .5, .1], [bx + 2.5, 2.9, .05]];
  iso.add(1e4, () => {
    const pts = path.map(p => iso.P(...p)); g.save(); g.globalAlpha = fade; g.strokeStyle = B.accent; g.lineWidth = 8; g.lineCap = 'round'; g.lineJoin = 'round'; g.setLineDash([22, 14]); g.lineDashOffset = -t * 60;
    let L = 0; const d2 = []; for (let i = 1; i < pts.length; i++) { const l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); d2.push(l); L += l; }
    let rem = L * prog; g.beginPath(); g.moveTo(...pts[0]); for (let i = 1; i < pts.length && rem > 0; i++) { const f = Math.min(1, rem / d2[i - 1]); g.lineTo(lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f)); rem -= d2[i - 1]; }
    g.stroke(); g.restore(); }, 2);
  iso.bill(bx + 1.2, by + 1.0, .25, gg => { drawPerson(gg, { h: 1.65, top: B.cloth[1], legs: '#6A5444', skirt: '#E2D3B0', hairLong: true }, {}); gg.beginPath(); gg.ellipse(.24, -1.15, .15, .13, 0, 0, TAU); gg.fillStyle = '#B5603A'; gg.fill(); if (t > T.home + 1.2) { gg.strokeStyle = '#9CC8C2'; gg.lineWidth = .05; gg.beginPath(); gg.moveTo(.3, -1.1); gg.quadraticCurveTo(.45, -.8, .4, -.2); gg.stroke(); } }, { r: 2 });
  if (open < 1) {
    const a = open * Math.PI * .92;
    const corners = [[x, y], [x + w, y], [x + w, y + d], [x, y + d]].map(([px, py]) => { const dy = py - y; return [px, y + dy * Math.cos(a), h + .35 + dy * Math.sin(a)]; });
    iso.add(x + y + h + 20, () => iso.face3(corners, Math.cos(a) > 0 ? ROOF : tri('#F1E8D8', .05, .1), { both: true }), 1);
  }
}
function market(t) {
  const x0 = -36;
  for (let k = 0; k < 5; k++) { const bx = x0 + k * 2.2, by = -3.2; iso.box(bx, by, 0, 1.4, 1.0, .9, tri('#E3D2AE', .15, .18));
    const st = seg(t, T.stamp + k * .35, T.stamp + k * .35 + .2); if (st > 0) iso.box(bx + .5, by + 1.0, .25, .4, .02, .4 * Math.min(1, st * 1.2), tri(B.accent, .1, .1), { bias: .05 }); }
  for (let k = 0; k < 6; k++) iso.cyl(x0 + 11.5 + (k % 3) * .7, -3.0 + (k / 3 | 0) * .7, 0, .3, .6, tri('#B5603A', .2, .2));
  const cx = x0 - 8 + 3 * seg(t, 22, 27.6), cy = 1.0;
  iso.box(cx, cy, .5, 3.0, 1.6, .25, tri('#9C7A4E', .2, .2)); iso.box(cx + .3, cy + .2, .75, 2.4, 1.2, .7, tri('#E3D2AE', .15, .18));
  iso.cyl(cx + 1.4, cy - .05, 0, .5, .12, tri('#5A4430', .1, .1)); iso.cyl(cx + 1.4, cy + 1.65, 0, .5, .12, tri('#5A4430', .1, .1));
  iso.box(cx + 3.5, cy + .3, .5, 1.8, .9, .9, tri('#E9DFCB', .1, .2)); iso.box(cx + 5.0, cy + .45, .9, .6, .6, .6, tri('#E9DFCB', .1, .2));
  const k = Math.min(4, Math.floor(Math.max(0, t - T.stamp) / .35)), ph = ((t - T.stamp) / .35) % 1, dn = t > T.stamp && t < T.stamp + 1.8 ? Math.sin(ph * Math.PI) : 0;
  person(x0 + .7 + 2.2 * k, -1.6, 0, { top: B.cloth[0], legs: '#5A4A3A' }, { lift: .2 + .3 * dn, caseUp: false });
  person(x0 + 13, -1.6, 0, { top: B.cloth[2], legs: '#6A5444', skirt: B.cloth[3] }, {});
}
const DUNES = []; for (let i = 0; i < 46; i++) DUNES.push({ x: -90 + hash(i * 4.1) * 148, y: -58 + hash(i * 6.3) * 116, r: 3 + hash(i * 2.2) * 4, h: .7 + hash(i * 9.9) * 1.6 });
function mound(t, k) {
  iso.alpha = k; iso.flat(rect(-100, 62, -64, 64), .25, '#E6CF9E', { depth: -4e5 }); iso.alpha = 1;
  for (const d of DUNES) { if ((d.x > -28 && d.x < 10 && d.y > -18 && d.y < 10) || (d.x > 6 && d.x < 30 && d.y > -10 && d.y < 24)) continue; const h = d.h * k; if (h < .05) continue;
    const pts = []; for (let j = 0; j < 9; j++) { const a = j / 9 * TAU; pts.push([d.x + Math.cos(a) * d.r * (1 + .25 * Math.sin(j * 2.3 + d.x)), d.y + Math.sin(a) * d.r * .8]); }
    iso.prism(pts, 0, h, tri(hash(d.x) < .5 ? '#E2C996' : '#D9BE8C', .2, .16)); }
  if (k > .05) iso.prism([[-150, -36], [-98, -36], [-98, 20], [-150, 20]], 0, 7 * k, tri('#D9BE8C', .2, .18), { cull: false });
  if (t < T.dig[0]) return;
  // the dig: a cleared rectangle over the hero block, brick walls uncovered course by course, archaeologists at work
  const dk = seg(t, T.dig[0], T.dig[1]);
  iso.flat(rect(-16, 8, -15, 8), .3, '#F1E2C2', { depth: -3.9e5 });
  iso.flat(rect(-16, 8, -15, 8), .31, 'rgba(0,0,0,0)', { depth: -3.9e5 });
  const blocks = HOUSES.filter(h => h.x >= -15 && h.x <= 7 && h.y >= -14 && h.y <= 7);
  blocks.forEach((hs, i) => { const e = ss(seg(dk, i * .18, i * .18 + .35)); if (e <= 0) return; house({ ...hs, h: 1.6 * e }, t, { noRoof: true }); });
  const P = [{ top: '#D8CDB4', legs: '#6A5E4A', hat: true, tool: true }, { top: '#C9B99A', legs: '#5A4E3A', hat: true, basket: true }, { top: '#E2D8C2', legs: '#6A5E4A', hat: true, tool: true }, { top: '#CFC2A6', legs: '#5A4E3A', hat: true, basket: true }];
  const spots = [[-8.5, -2.5], [1.5, -2.3], [-4, -15.6], [6.5, -9]];
  P.forEach((p, i) => { const [px, py] = spots[i], walk = i % 2 ? Math.sin(t * .8 + i) * 1.5 : 0; person(px + walk, py, 0, p, { dig: Math.abs(Math.sin(t * 3 + i)), walking: i % 2 === 1, phase: t * 5 }); });
}
function subtitle(g, t) {
  for (const s of SUBS) {
    const a = ss(seg(t, s.t0, s.t0 + .2)) * (1 - ss(seg(t, s.t1 - .15, s.t1))); if (a <= 0) continue;
    g.save(); g.globalAlpha = a; g.font = '500 32px Newsreader'; const w = g.measureText(s.text).width;
    g.fillStyle = 'rgba(247,241,230,.9)'; g.beginPath(); g.roundRect(W / 2 - w / 2 - 22, 1008 - 30, w + 44, 52, 4); g.fill();
    g.fillStyle = C.ink; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(s.text, W / 2, 1005); g.restore();
  }
}
// ———— sound events (exported for the mixer)
export const EV = [];
{
  const ev = (t, type, o = {}) => EV.push({ t: +t.toFixed(3), type, ...o });
  LINES.forEach(L => ev(L.t, 'voice', { id: L.id }));
  ev(0, 'bed', { kind: 'river', dur: 28 }); ev(0, 'bed', { kind: 'birds', dur: 9 }); ev(0, 'bed', { kind: 'town', dur: 27.6 }); ev(27.6, 'bed', { kind: 'wind', dur: 17.9 });
  [0, 1, 2].forEach(k => ev(T.lift + k * .25, 'slab', { pan: .3 })); ev(T.lift + .3, 'trickle', { dur: 7 });
  for (const [key, P] of Object.entries(SPEC)) phraseLayout(P).forEach((c, i) => ev(c.tc, 'land', { key, i, accent: c.col === C.accent ? 1 : 0, big: c.size > 2 ? 1 : 0 }));
  ev(T.wide[0], 'rise', { dur: 2.6 });
  for (let k = 0; k < 8; k++) ev(T.grid + k * .2, 'trace', { k });
  ev(T.brick - .2, 'thunk'); [0, 1, 2].forEach(k => ev(T.brick + .5 + k * .35, 'edge', { k }));
  ev(T.home + .3, 'lid', { dur: 1.3 }); ev(T.home + 1.2, 'pour', { dur: 1.6 }); ev(T.home + 1.6, 'trickle', { dur: 2.4 });
  ev(22.0, 'cart', { dur: 5.6 }); for (let k = 0; k < 5; k++) ev(T.stamp + k * .35 + .1, 'stamp', { k });
  for (let k = 0; k < 6; k++) ev(T.glyph + k * .16, 'glyph', { k });
  ev(T.decline, 'fall', { dur: 3 }); ev(T.decline + .5, 'steps', { dur: 5 });
  ev(T.bury[0], 'sand', { dur: 2.2 });
  for (let k = 0; k < 9; k++) ev(T.dig[0] + k * .32, 'dig', { k });
  ev(T.title, 'reveal');
  [['dawn', 0], ['city', 8.6], ['grid', T.grid], ['home', T.home], ['market', 22.0], ['decline', T.decline], ['bury', T.bury[0]], ['title', T.title]].forEach(([id, t]) => ev(t, 'cue', { id }));
}
export function texts() { return []; }
