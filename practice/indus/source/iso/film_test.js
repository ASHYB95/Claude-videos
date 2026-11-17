// Style test · Isometric Picture Book · Mohenjo-daro. Two shots: ?shot=1 (the street at dawn, drains) and ?shot=3 (a house, lid off).
import { C, W, H, iso, tri, mix, hex, css, TAU, clamp, lerp, seg, ss, eo, eio, hash, onPlane, fillPoly, rect, phraseLayout, floorType, drawPerson, subtitle } from './kit.js';
export const DUR = 8;
const B = { brick: '#B8683F', brickLt: '#D49268', mud: '#E3CDAA', mudD: '#D6BC94', street: '#E6D3B2', lane: '#DCC7A3', water: '#5E9C98', waterD: '#3E7C7A', ink: '#2A2420', accent: '#D0573A', reed: '#7E8F5A', palm: '#5F7A4A', cloth: ['#C9A24A', '#8FA7B8', '#9C8AA6', '#E2D3B0', '#B8714A'] };
const BRICK = tri(B.brick, .2, .22), BRICKL = tri(B.brickLt, .2, .2), MUD = tri(B.mud, .14, .16);

// ———— the city: one main street along x, houses on both sides, side lanes, a covered drain, the river to the east
const HOUSES = [];
for (let i = -5; i <= 4; i++) {
  const x0 = i * 11 + 1;
  HOUSES.push({ x: x0, y: -15, w: 9, d: 11, h: 5.2 + (hash(i) * 2 | 0) * 1.4, side: 'far', seed: i });    // far side of the street
  HOUSES.push({ x: x0, y: 4.2, w: 9, d: 10, h: 1.1, side: 'near', seed: i + 40 });                          // near side: cut low (cut-away)
}
function house(hs, t, o = {}) {
  const { x, y, w, d, h } = hs;
  // walls: four boxes with a courtyard (open centre)
  const th = .6, col = hs.side === 'near' ? BRICKL : BRICK, hn = o.cut ? 1.3 : h;   // cut-away: the near walls (+y, +x) drop low
  iso.box(x, y, 0, w, th, h, col); iso.box(x, y + d - th, 0, w, th, hn, col);
  iso.box(x, y + th, 0, th, d - 2 * th, h, col); iso.box(x + w - th, y + th, 0, th, d - 2 * th, hn, col);
  if (o.cut) { iso.box(x + 1.5, y + d - th, hn, 1.1, th, .0001, col); }
  if (o.lid === undefined && hs.side === 'far') {
    iso.box(x, y, h, w, d, .35, tri('#C98760', .25, .2));                      // flat roof (mud over brick)
    iso.box(x + w * .62, y + d * .2, h + .35, 1.8, 1.8, 1.0, tri('#C98760', .25, .2));   // a roof room / stair head
  }
  // little high windows on the street face (+y side for far houses)
  if (hs.side === 'far' && !o.cut) for (let k = 0; k < 3; k++) iso.box(x + 1.4 + k * 2.6, y + d - .02, h * .62, .7, .05, .55, tri('#4A2E22', .1, .1), { bias: .02 });
  // the floor of the near houses (seen inside, from above)
  if (hs.side === 'near') { iso.flat(rect(x + th, x + w - th, y + th, y + d - th), .02, B.mudD); iso.box(x + 1.2, y + 1.4, 0, 1.4, 1.4, .25, tri('#9E5A36', .2, .2)); }
}
function well(x, y) {
  iso.cyl(x, y, 0, .9, .9, BRICK);
  iso.flat([[x - .55, y - .55], [x + .55, y - .55], [x + .55, y + .55], [x - .55, y + .55]].map(([a, b]) => [a, b]), .92, '#2B3B3A', { layer: 1, depth: x + y + 1.9 });
}
function streetAndDrain(t, lifted) {
  iso.flat(rect(-70, 60, -3.4, 4.2), 0, B.street);
  for (let x = -60; x < 60; x += 11) iso.flat(rect(x + 9.6, x + 11.4, -16, -3.4), 0, B.lane);   // side lanes
  // brick kerbs
  iso.box(-70, -3.6, 0, 130, .25, .12, BRICK, { cull: false });
  // the covered drain at y≈3.2: a channel with brick slabs; some slabs lifted to show the water
  iso.flat(rect(-70, 60, 2.7, 3.7), .005, '#8E4E30');
  for (let i = 0; i < 70; i++) {
    const x = -70 + i * 1.86, L = lifted(i);
    if (L > 0) {
      iso.flat(rect(x + .05, x + 1.8, 2.82, 3.58), .01, B.waterD);
      const ph = t * 1.2 + i; iso.flat(rect(x + .2 + (ph % 1) * .6, x + .9 + (ph % 1) * .6, 3.0, 3.1), .015, '#9CC8C2', { a: .8 });
      // the lifted slab: hinged on its far edge (y=2.75), tilted up by L
      const a = L * 1.15, cy = 2.75, s = [[x, cy, .12], [x + 1.8, cy, .12], [x + 1.8, cy + .9 * Math.cos(a), .12 + .9 * Math.sin(a)], [x, cy + .9 * Math.cos(a), .12 + .9 * Math.sin(a)]];
      iso.add(x + cy + .6, () => { iso.face3(s, tri('#A9603C', .25, .2), { both: true }); }, 1);
    } else iso.box(x + .03, 2.75, 0, 1.8, .9, .12, tri('#A9603C', .22, .22));
  }
}
function river(t) {
  iso.flat(rect(60, 140, -60, 60), 0, B.water);
  for (let k = 0; k < 14; k++) { const yy = -40 + k * 7, ph = (t * .6 + k * .37) % 1; iso.flat(rect(64 + ph * 30, 70 + ph * 30, yy, yy + .25), .01, '#86BDB6', { a: .7 }); }
  iso.flat(rect(58, 62, -60, 60), .005, '#C9B48E');   // bank
  // a reed-boat with a square sail
  const bx = 78 + Math.sin(t * .3) * 2, by = -6;
  iso.box(bx, by, .05, 7, 1.6, .5, tri('#9C7A4E', .2, .2));
  iso.box(bx + 3.3, by + .7, .55, .18, .18, 4.4, tri('#5A4430', .1, .1));
  iso.add(bx + by + 5, () => iso.face3([[bx + 3.4, by + .2, 1.3], [bx + 3.4, by + 1.5, 1.3], [bx + 3.4, by + 1.5, 4.8], [bx + 3.4, by + .2, 4.8]], tri('#EADCC0', .1, .15), { both: true }), 1);
}
const PEOPLE = [
  { x0: 14, y: 1.8, v: 1.2, top: B.cloth[2], legs: '#6A5444', pot: true, skirt: '#E2D3B0' }, { x0: 26, y: -2.0, v: 1.1, top: B.cloth[4], legs: '#5A4A3A' }, { x0: 40, y: 1.2, v: 1.3, top: B.cloth[1], legs: '#6A5444', pot: true, skirt: '#C9A24A' },
  { x0: -30, y: -1.2, v: 1.3, top: B.cloth[0], legs: '#7A5A40', pot: true, skirt: '#E2D3B0' }, { x0: -24, y: 1.0, v: 1.2, top: B.cloth[1], legs: '#6A5444' },
  { x0: -12, y: -.4, v: 1.4, top: B.cloth[3], legs: '#5A4A3A', pot: true, skirt: '#C9A24A' }, { x0: 2, y: 1.4, v: 1.25, top: B.cloth[2], legs: '#6A5444' },
  { x0: 10, y: -1.6, v: 1.35, top: B.cloth[4], legs: '#5A4A3A', pot: true, skirt: '#8FA7B8' }, { x0: 18, y: .3, v: 1.3, top: B.cloth[0], legs: '#6A5444' },
];
function people(t) {
  for (const p of PEOPLE) {
    const x = p.x0 + p.v * t, ph = x / .7 * Math.PI;
    iso.bill(x, p.y, 0, g => {
      drawPerson(g, { h: 1.7, top: p.top, legs: p.legs, skirt: p.skirt, hairLong: !!p.skirt }, { walking: true, phase: ph });
      if (p.pot) { const bob = Math.abs(Math.cos(ph)) * .02; g.beginPath(); g.ellipse(0, -1.78 - bob, .16, .14, 0, 0, TAU); g.fillStyle = '#B5603A'; g.fill(); g.beginPath(); g.ellipse(.05, -1.78 - bob, .1, .13, 0, 0, TAU); g.fillStyle = '#8E4A2C'; g.fill(); }
    }, { r: 2 });
  }
}
// a few trees (date palms, neem) in courtyards and along the river bank
function palm(x, y, h = 6) {
  iso.cyl(x, y, 0, .22, h, tri('#8A6A48', .2, .2));
  iso.bill(x, y, h, g => { for (let k = 0; k < 7; k++) { const a = k / 7 * TAU; g.save(); g.rotate(a); g.beginPath(); g.ellipse(1.1, 0, 1.3, .28, 0, 0, TAU); g.fillStyle = k % 2 ? '#6E8A50' : '#5F7A4A'; g.fill(); g.restore(); } }, { r: 3 });
}

// ———— shot 1: the street at dawn
function shot1(g, t) {
  const u = t / DUR;
  iso.cam = { x: lerp(26, 33, u), y: lerp(-2, -4, u), z: 0, k: lerp(18, 20, ss(u)) };
  g.fillStyle = B.street; g.fillRect(0, 0, W, H);
  river(t);
  streetAndDrain(t, i => (i === 50 || i === 51 || i === 56) ? eo(seg(t, 1.0 + (i - 50) * .25, 2.2 + (i - 50) * .25)) : 0);
  for (const hs of HOUSES) house(hs, t);
  well(20.5, -1.8); palm(56, 10); palm(57, -8, 7); palm(29.5, 7.5, 5.5); palm(18, 8, 6);
  people(t);
  iso.flush();
  // floor type on the street: "2600 BCE"
  const P = { x: 31, y: 1.9, z: .02, t0: 1.4, t1: 99, step: .1, scale: .82, lines: [[['2600', 'na'], [' BCE', 'n']]] };
  floorType(g, t, P, phraseLayout(P));
  // dawn wash (warm, low) + the subtitle bar
  g.fillStyle = 'rgba(255,214,150,.10)'; g.fillRect(0, 0, W, H);
  subtitle(g, t, [{ t0: .3, t1: 99, text: 'Four and a half thousand years ago, a city on the Indus had drains under every street.' }]);
}

// ———— shot 3: one house, the roof lifts off; courtyard, well, bathing platform, drain to the street
function shot3(g, t) {
  const u = t / DUR, open = eio(seg(t, .6, 2.4)), rise = eio(seg(t, .6, 3.2));
  const hs = { x: 1, y: -15, w: 9, d: 11, h: 6.0, side: 'far' };
  iso.cam = { x: lerp(3.6, 3.2, u), y: lerp(-7.0, -7.6, u), z: lerp(1, 1.6, rise), k: lerp(60, 55, rise) };
  g.fillStyle = B.street; g.fillRect(0, 0, W, H);
  streetAndDrain(t, i => (i === 37) ? 1 : 0);
  for (const h of HOUSES) if (h.side !== 'far' || (h.x !== 1 && h.x !== 12)) house(h, t); house({ x: 12, y: -15, w: 9, d: 11, h: 1.3, side: 'near' }, t);
  // this house: walls, rooms, courtyard, well, bathing platform, drain chute
  const { x, y, w, d, h } = hs;
  iso.flat(rect(x, x + w, y, y + d), .01, '#D9C29C');
  house({ ...hs }, t, { lid: true, cut: open > .5 });
  iso.box(x + 3.8, y + .6, 0, .35, 3.6, 2.6, BRICKL); iso.box(x + .6, y + 4.2, 0, 3.2, .35, 2.6, BRICKL);   // inner room walls
  for (let k = 0; k < 6; k++) iso.box(x + w - 2.6, y + 1.0 + k * .45, 0, 1.8, .45, .35 + k * .42, BRICKL);   // stair
  well(x + 2.2, y + 2.4);
  // bathing platform: a raised square of fine brick with a slope to a corner outlet
  const bx = x + 5.2, by = y + 6.6;
  iso.box(bx, by, 0, 2.6, 2.6, .25, tri('#C27A52', .25, .2));
  for (let a = 0; a < 5; a++) for (let b2 = 0; b2 < 5; b2++) iso.flat(rect(bx + .1 + a * .5, bx + .5 + a * .5, by + .1 + b2 * .5, by + .3 + b2 * .5), .26, (a + b2) % 2 ? '#B56C46' : '#C9845B', { layer: 1, depth: bx + by + 3 });
  // the drain chute from the platform corner, through the wall, out to the street drain (accent: the path of the water)
  const prog = seg(t, 2.6, 4.2);
  const path = [[bx + 2.5, by + 2.5, .27], [bx + 2.5, y + d - .3, .2], [bx + 2.5, y + d + .5, .1], [bx + 2.5, 2.9, .05]];
  iso.add(1e4, () => {
    const pts = path.map(p => iso.P(...p));
    g.save(); g.strokeStyle = B.accent; g.lineWidth = 9; g.lineCap = 'round'; g.lineJoin = 'round'; g.setLineDash([22, 14]); g.lineDashOffset = -t * 60;
    let L = 0; const d2 = []; for (let i = 1; i < pts.length; i++) { const l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); d2.push(l); L += l; }
    let rem = L * prog; g.beginPath(); g.moveTo(...pts[0]); for (let i = 1; i < pts.length && rem > 0; i++) { const f = Math.min(1, rem / d2[i - 1]); g.lineTo(lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f)); rem -= d2[i - 1]; }
    g.stroke(); g.restore();
  }, 2);
  // a woman pouring water on the platform
  iso.bill(bx + 1.2, by + 1.0, .25, gg => { drawPerson(gg, { h: 1.65, top: B.cloth[1], legs: '#6A5444', skirt: '#E2D3B0', hairLong: true }, {}); gg.beginPath(); gg.ellipse(.22, -1.15, .15, .13, 0, 0, TAU); gg.fillStyle = '#B5603A'; gg.fill(); if (t > 2.4) { gg.strokeStyle = '#9CC8C2'; gg.lineWidth = .05; gg.beginPath(); gg.moveTo(.3, -1.1); gg.quadraticCurveTo(.45, -.8, .4, -.2); gg.stroke(); } }, { r: 2 });
  // the roof lid: hinged on the far edge (y = hs.y), it flips up and over, paper side up, then glides away
  if (open < 1 || t < 3.0) {
    const a = open * Math.PI * .92, gx = (seg(t, 2.4, 3.2)) * -14;
    const P2 = (px, py) => { const dy = py - y; return [px + gx, y - dy * Math.cos(a) * -1 * -1 + 0, h + .35 + dy * Math.sin(a)]; };
    const corners = [[x, y], [x + w, y], [x + w, y + d], [x, y + d]].map(([px, py]) => { const dy = py - y; return [px + gx, y + dy * Math.cos(a), h + .35 + dy * Math.sin(a)]; });
    iso.add(x + y + h + 20, () => iso.face3(corners, Math.cos(a) > 0 ? tri('#C98760', .25, .2) : tri('#F1E8D8', .05, .1), { both: true }), 1);
  }
  // a brick stack on the street + "1 : 2 : 4"
  for (let k = 0; k < 3; k++) for (let j = 0; j < 2; j++) iso.box(x + w + 1.0 + j * .3, -2.6 + k * .62, 0, .28, .56, .14 + 0, BRICK, { bias: k });
  iso.box(x + w + 1.0, -2.6, .14, .28, 1.24, .14, BRICK); iso.box(x + w + 1.3, -2.6, .14, .28, 1.24, .14, BRICK);
  iso.flush();
  const P = { x: x + w - 2.6, y: -.6, z: .02, t0: 3.4, t1: 99, step: .12, scale: .8, lines: [[['1', 'na'], [' : 2 : 4', 'n']]] };
  floorType(g, t, P, phraseLayout(P));
  g.fillStyle = 'rgba(255,214,150,.08)'; g.fillRect(0, 0, W, H);
  subtitle(g, t, [{ t0: .3, t1: 99, text: 'Most homes had their own bathroom, connected to covered drains.' }]);
}
export function render(g, t, Q) {
  iso.g = g;
  if ((Q.get('shot') || '1') === '3') shot3(g, t); else shot1(g, t);
}
