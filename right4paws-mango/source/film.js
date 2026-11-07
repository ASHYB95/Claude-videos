// Mango's Mealtime: two picture-book pages, one camera that never cuts (glides over page 1, a page turn, glides over page 2)
import { layer, clear, line, fill, dab, text, handCircle, ellipse, smooth, CAM, BOIL, W, H, sx, sy } from './crayon.js';
import { group, clearGroup, part, curve } from './rig.js';
import { mango } from './dog.js';
import { bowl, pellets, flakes, pack, ingredient, ING, heart, zigs, paw, clock, sun, crayonStick } from './props.js';
import { PAL } from './pal.js';
import { clamp, lerp, hash, track, ss, eio, eo, ei, back, mulberry } from './lib.js';
const K = PAL.crayon;
const pr = (t, a, b) => clamp((t - a) / (b - a));
export const DUR = 41;
const BEAT = 0.5, BAR = 1.5;   // ♩ = 120, 3/4
const TURN = [20.4, 21.9];

// —— narration (t = speech start; d filled in after TTS)
export const LINES = [
  { id: 'v1', t: 0.6, d: 3.513, text: 'Right. Confession time. I used to be a terribly fussy eater.' },
  { id: 'v2', t: 5.2, d: 3.346, text: 'Same brown pellets. Every. Single. Day.' },
  { id: 'v3', t: 10.4, d: 2.193, text: 'Then one morning… something new turned up.' },
  { id: 'v4', t: 14.4, d: 4.01, text: 'Real chicken. Fresh eggs. Veggies, berries… even sardines!' },
  { id: 'v5', t: 20.4, d: 2.641, text: 'Now I wake up thinking about breakfast.' },
  { id: 'v6', t: 23.6, d: 2.692, text: 'I sit by my bowl. I wait. Very nicely.' },
  { id: 'v7', t: 29.6, d: 2.071, text: 'Best. Bit. Of my day.' },
  { id: 'v8', t: 34.0, d: 2.928, text: 'Right4Paws Ultimate Diet. Raw, made right.' },
];
// subtitles: long lines split into two cues; ≥ 1.8 s and ≥ speech + 0.6 s
function cues() {
  const out = [];
  LINES.forEach((L, i) => {
    const nx = LINES[i + 1]; const end = Math.min(Math.max(L.t + 1.8, L.t + L.d + 0.6), nx ? nx.t - 0.15 : DUR);
    const parts = L.text.length > 34 ? splitLine(L.text) : [L.text];
    out.push({ t0: L.t - 0.1, t1: end, text: parts });
  });
  return out;
}
function splitLine(s) { const w = s.split(' '); let best = 1, bd = 1e9; for (let i = 1; i < w.length; i++) { const a = w.slice(0, i).join(' ').length, b = w.slice(i).join(' ').length; if (Math.abs(a - b) < bd) { bd = Math.abs(a - b); best = i; } } return [w.slice(0, best).join(' '), w.slice(best).join(' ')]; }
export const SUBS = cues().map(c => ({ t0: c.t0, t1: c.t1, text: c.text.join(' ') }));
const CUES = cues();

// —— page 1 layout (world units)
const M1 = { x: 600, y: 1800 };               // Mango lying
const PB = { x: 1330, y: 1770 };              // pellet bowl rim
const BX = { x: 740, y: 1250, w: 300, h: 420 }; // pack, bottom-front-left
const BOXT = 10.25, BOXL = 10.6;              // drop start, landing
const ING_T = ING.map((_, i) => 14.5 + 0.5 * i);
const ING_AT = [[260, 1380], [1480, 1340], [250, 2180], [700, 2260], [1130, 2230], [1530, 2120]];
const ING_S = [1.6, 1.5, 1.5, 1.5, 1.5, 1.4];

// —— page 2 layout
const M2 = { x: 720, y: 2060, s: 1.05 };
const RB = { x: 1290, y: 1990, w: 175 };
const CLK = { x: 330, y: 1130, R: 120 };
const SUN = { x: 1380, y: 520, R: 118 };
const POUR = 28.5, EAT = [29.3, 31.0];
const BANDS = [
  { y0: 2290, y1: 2770, t0: 34.3, t1: 35.9, dir: 1, seed: 1 },
  { y0: 2700, y1: 3340, t0: 35.7, t1: 37.3, dir: -1, seed: 2 },
];

// —— cameras [t, [cx, cy, scale]]
const cam1 = track([
  [0, [968, 1660, 4.2]], [1.3, [968, 1660, 4.2]], [4.4, [800, 1720, 1.08]], [5.4, [960, 1720, 1.0]], [9.9, [1000, 1720, 1.0]],
  [11.2, [900, 1420, 0.72]], [14.3, [900, 1400, 0.72]], [16.2, [880, 1640, 0.64]], [18.6, [880, 1800, 0.6]], [21.9, [880, 1800, 0.6]],
]);
const cam2 = track([
  [20.4, [900, 720, 0.82]], [22.6, [900, 720, 0.82]], [24.2, [880, 1680, 0.82]], [27.8, [930, 1780, 0.9]], [28.8, [1000, 1860, 1.0]],
  [30.9, [1000, 1860, 1.0]], [31.8, [760, 1640, 1.55]], [33.6, [770, 1650, 1.6]], [35.0, [900, 2050, 0.8]], [37.0, [900, 1660, 0.58]], [41, [900, 1660, 0.58]],
]);

// —— events for the mixer
export const EV = [];
const ev = (t, type, o = {}) => EV.push({ t: +t.toFixed(3), type, ...o });
LINES.forEach(L => ev(L.t, 'voice', { id: L.id }));
ev(0, 'room'); ev(0.05, 'scribble', { dur: 1.2, pan: 0.1 }); ev(1.4, 'crayonoff');
[[1.0, 0.8], [1.8, 0.9], [2.6, 0.8]].forEach(([t, d]) => ev(t, 'scratch', { dur: d, pan: -0.1 }));
ev(3.2, 'sigh'); ev(4.6, 'scratch', { dur: 0.9, pan: 0.5 }); ev(5.2, 'pellets', { pan: 0.5 });
ev(6.0, 'sniff', { pan: 0.3 }); ev(6.5, 'sniff', { pan: 0.3 }); ev(7.0, 'hmph'); ev(7.05, 'jingle');
ev(BOXT, 'whoosh', { dur: 0.35 }); ev(BOXL, 'thump'); ev(10.75, 'jingle'); ev(10.8, 'scribble', { dur: 1.2, pan: 0 });
ev(14.0, 'flaps');
ING_T.forEach((t, i) => { ev(t, 'pop', { i }); ev(t + 0.5, 'plop', { i, pan: (ING_AT[i][0] - 900) / 900 }); ev(t + 0.5, 'glock', { i }); ev(t + 0.55, 'scribble', { dur: 0.4, pan: (ING_AT[i][0] - 900) / 900 }); });
ev(15.2, 'scribble', { dur: 3.2, pan: -0.1 });
ev(16.6, 'jingle'); [17.0, 17.5, 18.0, 18.5, 19.0, 19.5].forEach(t => ev(t, 'tail'));
ev(TURN[0], 'page', { dur: TURN[1] - TURN[0] }); ev(22.0, 'birds'); ev(22.3, 'ding');
for (let t = 24.0; t < 28.5; t += 0.5) ev(t, 'tick');
ev(27.0, 'silence', { dur: 1.5 }); ev(27.7, 'whine');
ev(POUR, 'pour', { dur: 0.8 });
for (let t = EAT[0]; t < EAT[1]; t += 0.33) ev(t, 'munch');
ev(31.1, 'snort'); [31.5, 32.0, 32.5, 33.0].forEach(t => ev(t, 'sparkle'));
BANDS.forEach(b => ev(b.t0, 'brush', { dur: b.t1 - b.t0, dir: b.dir }));
ev(37.3, 'write', { dur: 1.7 }); ev(39.0, 'musicbox');
[['A', 0], ['B', 10.5], ['C', 22.5], ['S', 27.0], ['D', 28.5], ['E', 34.5]].forEach(([id, t]) => ev(t, 'cue', { id }));

// —— layers
const BG = group(), PK = group(), IN = group(), DG = group(), WAX = group(), WASH = layer(), FX = layer(), TOP = group(), SUBK = layer(), SUBT = layer();
const OBJ = document.createElement('canvas'); OBJ.width = W; OBJ.height = H;
const mk = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; return { c, g: c.getContext('2d') }; };
const P1 = mk(), P2 = mk(), OUT = mk();
const glc = () => document.getElementById('gl');
const snap = P => { P.g.setTransform(1, 0, 0, 1, 0, 0); P.g.clearRect(0, 0, W, H); P.g.drawImage(glc(), 0, 0); };

export function frame(comp, t) {
  if (t < TURN[0]) return page1(comp, t, cam1(t), { subs: true });
  if (t >= TURN[1]) return page2(comp, t, cam2(t), { subs: true });
  // page turn
  page1(comp, t, cam1(t), { subs: false, vig: 0 }); snap(P1);
  page2(comp, t, cam2(t), { subs: false, vig: 0 }); snap(P2);
  const u = eio(pr(t, TURN[0], TURN[1]));
  const g = OUT.g; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H);
  g.drawImage(P2.c, 0, 0);
  const f = W * (1 - u);                          // fold x
  const flap = (W - f) * (1 - 0.35 * Math.sin(u * Math.PI));   // the lifted part, foreshortened as it rises
  // page 1 still lying down on the left
  g.save(); g.beginPath(); g.rect(0, 0, f, H); g.clip(); g.drawImage(P1.c, 0, 0); g.restore();
  // shadow cast on page 2 beyond the fold
  const sg = g.createLinearGradient(f, 0, f + 90, 0); sg.addColorStop(0, 'rgba(60,30,20,0.28)'); sg.addColorStop(1, 'rgba(60,30,20,0)');
  g.fillStyle = sg; g.fillRect(f, 0, 90, H);
  // the back of the turning page, strip by strip (affine per strip)
  const n = 40;
  for (let i = 0; i < n; i++) {
    const a = i / n, b = (i + 1) / n;
    const xa = f - flap * a, xb = f - flap * b;
    const lift = Math.sin(u * Math.PI) * 60 * Math.sin(a * Math.PI * 0.5);
    g.save();
    g.beginPath(); g.moveTo(xa + 0.5, -lift); g.lineTo(xb - 0.5, -lift); g.lineTo(xb - 0.5, H + lift); g.lineTo(xa + 0.5, H + lift); g.closePath(); g.clip();
    const shade = 0.93 - 0.18 * (1 - a) * Math.sin(u * Math.PI);
    g.fillStyle = `rgb(${Math.round(251 * shade)},${Math.round(239 * shade)},${Math.round(228 * shade)})`; g.fillRect(0, -100, W, H + 200);
    g.globalAlpha = 0.06; g.translate(xa, 0); g.scale(-(xa - xb) / ((W - f) / n), 1); g.drawImage(P1.c, -(f + (W - f) * a), 0);
    g.restore();
  }
  g.strokeStyle = 'rgba(80,40,30,0.25)'; g.lineWidth = 2; g.beginPath(); g.moveTo(f - flap, 0); g.lineTo(f - flap, H); g.stroke();
  comp.paperCam(0, 0, 1); comp.begin(PAL.paper); comp.image(OUT.c);
  // subtitle stays on top through the turn
  clear(SUBK); clear(SUBT); subTo(SUBK, SUBT, t); comp.knock(SUBK.c); comp.crayon(SUBT.c);
  comp.finish({ vig: 0.12, emb: 0 });
}

function setCam(cam) { [CAM.x, CAM.y, CAM.s] = cam; }
function clearAll() { [WASH, FX, SUBK, SUBT].forEach(clear); [BG, PK, IN, DG, WAX, TOP].forEach(clearGroup); const g = OBJ.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H); }

// ————————————————————————— page 1
function mangoP1(t) {
  const o = { x: M1.x, y: M1.y, s: 1, pose: 'lie', head: { view: 'side', r: 0.12 }, expr: 'meh', earPerk: 0, colour: 0, seed: 500, lineDraw: pr(t, 0.4, 3.0), tail: 0 };
  if (t > 3.2 && t < 3.9) o.head.dy = 6 * Math.sin(pr(t, 3.2, 3.9) * Math.PI);           // sigh
  if (t >= 6.0 && t < 7.0) { o.expr = 'sniff'; o.head.dx = 26; o.head.dy = -6; o.head.r = 0.02; o.earPerk = 0.3; }
  if (t >= 7.0 && t < 8.3) { o.head = { view: 'front', r: -0.32, dx: -30, dy: -30 }; o.expr = 'bored'; o.look = [-1, -0.6]; o.earPerk = 0.1; }
  if (t >= 8.3 && t < 10.62) { o.head = { view: 'side', r: 0.16, dx: -8, dy: 4 }; o.expr = 'meh'; o.earPerk = 0; }
  if (t >= 10.62 && t < 16.6) { o.head = { view: 'front', r: -0.06, dx: -20, dy: -46 }; o.expr = t > 14.5 ? 'excited' : 'wait'; o.look = t < 14.6 ? [0.2, -1] : [lerp(-1, 1, (Math.sin(t * 3) + 1) / 2), -0.6]; o.earPerk = 1; o.tail = 0.4 * Math.sin(t * 9) * pr(t, 14.6, 15.2); }
  if (t >= 15.2) o.colour = pr(t, 15.2, 18.4);
  if (t >= 16.6) {   // up on his feet, tail going
    const hop = t < 16.9 ? Math.sin(pr(t, 16.6, 16.9) * Math.PI) * 50 : 0;
    Object.assign(o, { pose: 'stand', x: M1.x + 40, y: M1.y + 10 - hop, head: { r: -0.1 + 0.05 * Math.sin(t * 6) }, expr: 'excited', earPerk: 1, tail: 0.32 * Math.sin(t * 14) });
    if (t > 18.6) o.expr = 'happy';
  }
  return o;
}
function page1(comp, t, cam, { subs = true, vig = 0.28 } = {}) {
  setCam(cam); clearAll();
  BOIL.amp = 1;
  // pellet bowl (outline + the dull brown pellets)
  const bd = pr(t, 4.5, 5.4);
  if (bd > 0) bowl(PK, PB.x, PB.y, { w: 150, draw: bd, seed: 70, fill: C => { const n = Math.floor(26 * pr(t, 5.1, 5.6)); if (n) pellets(C, PB.x, PB.y, 150, 80, n); } });
  // the pack drops in, then gets coloured
  if (t >= BOXT) {
    const u = pr(t, BOXT, BOXL); const dy = -1500 * (1 - ei(u));
    const sq = t > BOXL ? Math.exp(-(t - BOXL) * 9) * Math.sin((t - BOXL) * 30) * 0.06 : 0;
    const col = pr(t, 10.8, 12.0);
    pack(PK, BX.x - BX.w * sq / 2, BX.y + dy, { w: BX.w * (1 + sq), h: BX.h * (1 - sq), colour: col, open: eo(pr(t, 14.0, 14.4)), seed: 200 });
    if (t > BOXL && t < BOXL + 0.5) { const k = pr(t, BOXL, BOXL + 0.5); [[-1, 0], [1, 0]].forEach(([d], i) => zigs(FX, [[BX.x + (d < 0 ? -30 : BX.w + 110), BX.y - 20], [BX.x + (d < 0 ? -90 : BX.w + 170), BX.y - 60 - 30 * k]], 900 + i, 1 - k)); }
  }
  // ingredients: pop out of the box, arc down, land and colour in
  ING.forEach((kind, i) => {
    const t0 = ING_T[i]; if (t < t0) return;
    const u = pr(t, t0, t0 + 0.5); const q = Math.floor(u * 12) / 12;   // stepped at 12 fps like the drawing
    const [ax, ay] = [BX.x + BX.w / 2 + 40, BX.y - BX.h - 60], [bx, by] = ING_AT[i];
    const x = lerp(ax, bx, q), y = lerp(ay, by, q) - 520 * Math.sin(q * Math.PI);
    const land = t > t0 + 0.5 ? Math.exp(-(t - t0 - 0.5) * 8) * Math.sin((t - t0 - 0.5) * 26) * 0.1 : 0;
    ingredient(IN, kind, x, y, { s: ING_S[i] * (1 + land), r: (1 - q) * (i % 2 ? 2 : -2) + 0.15 * Math.sin(i * 3), seed: 300 + i * 50, colour: pr(t, t0 + 0.45, t0 + 0.85) });
    if (t > t0 + 0.5 && t < t0 + 1.3) sparkle(FX, bx, by - 90, 700 + i, pr(t, t0 + 0.5, t0 + 1.3));
  });
  // Mango
  const mo = mangoP1(t); mango(DG, mo);
  // "hmph" puff, and "!" when the box lands
  if (t > 7.0 && t < 8.0) puff(FX, M1.x + 210, M1.y - 250, pr(t, 7.0, 8.0), 950);
  if (t > BOXL + 0.1 && t < 12.2) bang(FX, M1.x + 260, M1.y - 420, pr(t, BOXL + 0.1, BOXL + 0.3), 960);
  // opening crayon tip
  if (t < 2.3) {
    const g = OBJ.getContext('2d'); const e = [M1.x + (300 + 32) * 1, M1.y - 128 - 22 + 4];
    const k = pr(t, 1.3, 2.3);
    const tx = sx(e[0]) + 60 * Math.cos(t * 9) * (1 - k) + 900 * ei(k), ty = sy(e[1]) + 40 * Math.sin(t * 9) * (1 - k) - 1400 * ei(k);
    crayonStick(g, tx, ty, -0.9, 900, K.ink);
  }
  if (subs) subTo(SUBK, SUBT, t);
  comp.paperCam(CAM.x * 0.6, CAM.y * 0.6, CAM.s / 0.6);
  comp.begin(PAL.paper);
  const go = [hash(BOIL.step) * 300, hash(BOIL.step + 7) * 300];
  comp.group(BG, { goff: [0, 0] });
  comp.group(PK, { goff: go }); comp.group(IN, { goff: go }); comp.group(DG, { goff: go });
  comp.crayon(FX.c, { goff: go });
  if (t < 2.3) comp.image(OBJ);
  comp.knock(SUBK.c); comp.crayon(SUBT.c);
  comp.finish({ vig });
}

// ————————————————————————— page 2
function mangoP2(t) {
  const o = { x: M2.x, y: M2.y, s: M2.s, pose: 'sit', head: { view: 'front' }, expr: 'happy', earPerk: 1, colour: 1, seed: 510, tail: 0.25 * Math.sin(t * 10) };
  if (t < 23.6) { o.expr = 'wait'; o.look = [-0.6, -1]; o.head.r = -0.12; }
  else if (t < POUR + 0.1) {
    const b = Math.floor((t - 23.6) / BEAT);              // eyes flick: clock, bowl, on the beat
    o.expr = 'wait'; o.look = b % 2 ? [1, 0.5] : [-1, -0.8]; o.head.r = b % 2 ? 0.08 : -0.1;
    o.tail = 0.18 * Math.sin(t * lerp(10, 4, pr(t, 24, 27.5)));
    if (t > 27.0) { o.look = [1, 0.5]; o.head.r = 0.1; o.tail = 0; o.earPerk = 1; }
  } else if (t < EAT[0]) { o.expr = 'excited'; o.look = [1, 0.6]; o.head.r = 0.14; o.tail = 0.4 * Math.sin(t * 16); }
  else if (t < EAT[1]) {
    const ph = Math.floor((t - EAT[0]) / 0.33) % 2;      // two key drawings: head down / head up a little
    Object.assign(o, { pose: 'stand', x: 860, y: M2.y, head: { dx: 70, dy: ph ? 238 : 214, r: ph ? 0.85 : 0.7 }, expr: 'chomp', tail: 0.35 * Math.sin(t * 16) });
  } else { o.expr = 'happy'; o.head.r = 0.08 * Math.sin(t * 3); o.tail = 0.3 * Math.sin(t * 12); }
  return o;
}
function page2(comp, t, cam, { subs = true, vig = 0.28 } = {}) {
  setCam(cam); clearAll();
  BOIL.amp = t > 24.5 && t < POUR ? 0.5 : 1;          // the boil calms while he waits
  // sun + title
  sun(BG, SUN.x, SUN.y, SUN.R, t, 640, pr(t, 21.4, 22.6));
  text(BG.l, 'Every morning…', sx(640), sy(560), { size: 118 * CAM.s, font: 'Kalam', weight: 700, col: K.ink, reveal: pr(t, 22.2, 23.2), seed: 21, stroke: 1.5 });
  // clock (its minute hand creeps), wax message + paw prints (invisible until the wash)
  clock(BG, CLK.x, CLK.y, CLK.R, 2.0 + (t - 22) * 0.35, 600, 1);
  text(WAX.l, 'Raw Made Right', sx(900), sy(2580), { size: 168 * CAM.s, font: 'Kalam', weight: 700, col: '#fcf4ec', p: 0.9, seed: 33, boil: 0.2 });
  [[220, 2400, 0.4], [360, 2330, 0.2], [1560, 2380, -0.3], [1660, 2300, -0.5], [150, 3000, 0.3], [1650, 2900, -0.2]].forEach(([x, y, r], i) => paw(WAX.l, x, y, 34, 40 + i * 9, '#fcf4ec', r));
  // thought bubble: a bowl and a heart
  if (t > 21.9 && t < 24.0) {
    const k = pr(t, 22.0, 22.6), out = pr(t, 23.6, 24.0);
    const bx = M2.x + 330, by = M2.y - 800;
    [[M2.x + 140, M2.y - 560, 18], [M2.x + 200, M2.y - 640, 28]].forEach(([x, y, r], i) => line(FX, handCircle(x, y, r, 70 + i), { w: 5, seed: 70 + i, col: K.ink, draw: k, p: 1 - out }));
    line(FX, smooth([[bx - 190, by], [bx - 120, by - 120], [bx + 40, by - 150], [bx + 180, by - 70], [bx + 170, by + 70], [bx, by + 110], [bx - 160, by + 80]], 6), { w: 6, seed: 74, col: K.ink, draw: k, p: 1 - out });
    if (k > 0.5 && out < 1) { heart(FX, bx - 40, by - 20, 44, 76, 1 - out); fill(FX, [[bx + 30, by - 10], [bx + 140, by - 10], [bx + 120, by + 40], [bx + 50, by + 40]], { col: K.red, p: 0.9 * (1 - out), seed: 78, gap: 6, w: 8 }); }
  }
  // red bowl (+ flakes once poured)
  const amt = t < POUR ? 0 : t < EAT[1] ? pr(t, POUR, POUR + 0.7) * (1 - 0.6 * pr(t, EAT[0], EAT[1])) : 0.4;
  bowl(PK, RB.x, RB.y, { w: RB.w, red: true, seed: 90, label: 'MANGO', fill: C => { if (amt > 0) flakes(C, RB.x, RB.y, RB.w, 91, amt); } });
  if (t > POUR - 0.2 && t < POUR + 0.8) for (let i = 0; i < 9; i++) { const u = pr(t, POUR - 0.2 + i * 0.06, POUR + 0.3 + i * 0.06); if (u <= 0 || u >= 1) continue; const x = RB.x - 60 + i * 15, y = lerp(RB.y - 520, RB.y - 20, u * u); fill(FX, handCircle(x, y, 13, 50 + i, 0, 10), { col: '#b7703f', p: 0.95, gap: 4, w: 6, seed: 60 + i }); }
  // the pack, standing in the corner of the page (front cream stays readable after the wash)
  pack(TOP, 1230, 3240, { w: 260, h: 360, colour: 1, seed: 260 });
  // Mango
  mango(DG, mangoP2(t));
  if (t > EAT[0] && t < EAT[1]) for (let i = 0; i < 4; i++) { const u = ((t - EAT[0]) * 3 + i * 0.25) % 1; dab(FX, RB.x - 80 + i * 50, RB.y - 40 - 120 * Math.sin(u * Math.PI), 9, { col: '#b7703f', p: 0.9 * (1 - u), seed: 820 + i }); }
  if (t > EAT[1]) for (let i = 0; i < 4; i++) { const t0 = EAT[1] + 0.2 + i * 0.5; const u = pr(t, t0, t0 + 2.2); if (u <= 0 || u >= 1) continue; heart(FX, M2.x - 160 + i * 110 + 30 * Math.sin(u * 6 + i), M2.y - 600 - 360 * u, 34 + 8 * (i % 2), 840 + i, 1 - pr(u, 0.7, 1)); }
  if (t > 31.2 && t < 33.8) for (let i = 0; i < 3; i++) sparkle(FX, M2.x + [-240, 230, 260][i], M2.y - [560, 620, 360][i], 880 + i, ((t - 31.2) * 0.8 + i * 0.3) % 1);
  // tail thumps "thump" lines while waiting
  if (t > 24 && t < 27.0) { const ph = (t * 2) % 1; if (ph < 0.4) zigs(FX, [[M2.x + 300, M2.y - 30], [M2.x + 350, M2.y - 60]], 990, 1 - ph / 0.4); }
  // the wash
  if (t > BANDS[0].t0) { drawWash(WASH, t); const g = WASH.g; g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'destination-out'; g.drawImage(WAX.l.c, 0, 0); g.restore(); }
  // end lettering, white crayon over the red
  const e1 = pr(t, 37.3, 38.1), e2 = pr(t, 38.1, 39.0);
  if (e1 > 0) {
    text(TOP.l, 'RIGHT4PAWS', sx(560), sy(2950), { size: 120 * CAM.s, font: 'Fredoka', weight: 700, col: K.white, reveal: e1, seed: 51, p: 1, stroke: 2 * CAM.s });
    paw(TOP.l, 1040, 2895, 42, 52, K.white, 0.3);
    text(TOP.l, 'Ultimate Diet', sx(560), sy(3080), { size: 80 * CAM.s, font: 'Fredoka', weight: 600, col: K.white, reveal: e2, seed: 53, p: 1 });
    text(TOP.l, 'Medium & Maxi Adult', sx(560), sy(3170), { size: 56 * CAM.s, font: 'Fredoka', weight: 600, col: K.cream, reveal: e2, seed: 54, p: 1 });
  }
  if (subs) subTo(SUBK, SUBT, t);
  comp.paperCam(CAM.x * 0.6 + 4000, CAM.y * 0.6, CAM.s / 0.6);
  comp.begin(PAL.paper2);
  const go = [hash(BOIL.step) * 300, hash(BOIL.step + 7) * 300];
  comp.group(BG, { goff: [0, 0] });
  comp.group(PK, { goff: go });
  if (t > BANDS[0].t0) comp.wash(WASH.c, { color: PAL.wash, resist: 0.95 });
  comp.group(DG, { goff: go }); comp.group(TOP, { goff: go });
  comp.crayon(FX.c, { goff: go });
  comp.knock(SUBK.c); comp.crayon(SUBT.c);
  comp.finish({ vig });
}

// —— watercolour bands (brand-red), a sweep with a wet leading edge
const X0 = -300, X1 = 2100;
function bandFront(b, t) { const u = clamp((t - b.t0) / (b.t1 - b.t0)); const e = u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; const v = 0.15 * u + 0.85 * e; return b.dir > 0 ? lerp(X0, X1, v) : lerp(X1, X0, v); }
function drawWash(LW, t) {
  const g = LW.g; g.save();
  g.setTransform(CAM.s, 0, 0, CAM.s, W / 2 - CAM.x * CAM.s, H / 2 - CAM.y * CAM.s);
  for (const b of BANDS) {
    if (t < b.t0) continue;
    const f = bandFront(b, t), moving = t < b.t1;
    const top = [], bot = [];
    for (let x = X0; x <= X1; x += 40) {
      top.push([x, b.y0 + 14 * (Math.sin(x * 0.006 + b.seed) + 0.6 * Math.sin(x * 0.017 + b.seed * 3)) - 60 * Math.sin((x - X0) / (X1 - X0) * Math.PI) * b.dir]);
      bot.push([x, b.y1 + 10 * Math.sin(x * 0.009 + b.seed * 2) + (b === BANDS[1] ? 400 : 0)]);
    }
    const frontX = y => f + b.dir * 70 * Math.sin(clamp((y - b.y0) / (b.y1 - b.y0)) * Math.PI) + 12 * Math.sin(y * 0.05);
    g.save(); g.beginPath();
    const ex = b.dir > 0 ? X0 - 60 : X1 + 60;
    g.moveTo(ex, b.y0 - 300); for (let y = b.y0 - 300; y <= b.y1 + 500; y += 20) g.lineTo(frontX(y), y); g.lineTo(ex, b.y1 + 500);
    g.closePath(); g.clip();
    const shape = new Path2D(); top.forEach(([x, y], i) => i ? shape.lineTo(x, y) : shape.moveTo(x, y)); for (let i = bot.length - 1; i >= 0; i--) shape.lineTo(bot[i][0], bot[i][1]); shape.closePath();
    g.fillStyle = '#000'; g.globalAlpha = 0.82; g.fill(shape);
    g.save(); g.clip(shape);
    const R = mulberry(b.seed * 97);
    for (let i = 0; i < 26; i++) {
      const yy = lerp(b.y0, b.y1, R()), wdt = 6 + R() * 30, dark = R() < 0.55;
      g.beginPath(); for (let x = X0; x <= X1; x += 60) { const y = yy + 14 * Math.sin(x * 0.002 + i) + 6 * Math.sin(x * 0.01 + i * 2); x === X0 ? g.moveTo(x, y) : g.lineTo(x, y); }
      g.lineWidth = dark ? wdt : wdt * 0.5; g.globalCompositeOperation = dark ? 'source-over' : 'destination-out'; g.globalAlpha = dark ? 0.12 + R() * 0.1 : 0.05 + R() * 0.07; g.strokeStyle = '#000'; g.stroke();
    }
    g.globalCompositeOperation = 'source-over';
    g.beginPath(); for (let y = b.y0 - 80; y <= b.y1 + 80; y += 16) { const x = frontX(y) - b.dir * 14; y === b.y0 - 80 ? g.moveTo(x, y) : g.lineTo(x, y); }
    g.lineWidth = moving ? 34 : 22; g.globalAlpha = moving ? 0.3 : 0.14; g.stroke();
    g.restore(); g.restore();
  }
  g.restore();
}

// —— doodles
function sparkle(L, x, y, sd, u) {
  const a = Math.sin(clamp(u) * Math.PI), r = 18 + 26 * a;
  line(L, [[x - r, y], [x + r, y]], { w: 5, col: K.yolk, p: a, seed: sd, wob: 0.2 });
  line(L, [[x, y - r], [x, y + r]], { w: 5, col: K.yolk, p: a, seed: sd + 1, wob: 0.2 });
}
function puff(L, x, y, u, sd) {
  for (let i = 0; i < 3; i++) { const k = clamp(u * 1.4 - i * 0.15); if (k <= 0) continue; line(L, handCircle(x - 60 * k - i * 30, y - 20 * i - 30 * k, 16 + 10 * k, sd + i), { w: 4, seed: sd + i, col: K.ink, p: 1 - u }); }
}
function bang(L, x, y, u, sd) {
  line(L, [[x, y - 90], [x + 6, y - 20]], { w: 12, seed: sd, col: K.red, p: 1, draw: u });
  dab(L, x + 8, y + 10, 9, { col: K.red, p: u, seed: sd + 1 });
}
export function subTo(SUBK, SUBT, t) {
  const S = CUES.find(s => t >= s.t0 && t < s.t1); if (!S) return;
  const rv = pr(t, S.t0, S.t0 + 0.35);
  const g = SUBK.g; g.save(); g.font = '400 58px "Patrick Hand"'; const tw = Math.max(...S.text.map(s => g.measureText(s).width)); g.restore();
  const n = S.text.length, cx = W / 2, cy = 1660, hw = tw / 2 + 50, hh = 34 + 34 * n;
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#000'; g.beginPath();
  for (let i = 0; i <= 60; i++) { const a = i / 60 * Math.PI * 2; const px = Math.cos(a), py = Math.sin(a); const sq = Math.pow(Math.abs(px), 0.3) * Math.sign(px); const nn = 1 + 0.05 * Math.sin(a * 7 + 1.3) + 0.03 * Math.sin(a * 17); const X = cx + sq * hw * nn, Y = cy + py * hh * nn; i ? g.lineTo(X, Y) : g.moveTo(X, Y); }
  g.closePath(); g.fill(); g.restore();
  S.text.forEach((s, i) => text(SUBT, s, cx, cy + 20 + (i - (n - 1) / 2) * 66, { size: 58, col: K.ink, reveal: clamp(rv * n - i), seed: 11 + S.t0 * 3 + i, p: 1, stroke: 1.2 }));
}
// on-screen titles for readcheck (subtitles are checked from the .srt)
export function TEXTS(t) {
  const out = [];
  if (t >= TURN[1] && t < 24.4) out.push({ id: 'title', text: 'Every morning…', x0: 0, y0: 0, x1: W, y1: H / 2, pass: true });
  if (t > 38.1) out.push({ id: 'end', text: 'RIGHT4PAWS Ultimate Diet Medium & Maxi Adult', x0: 0, y0: H / 2, x1: W, y1: H });
  return out;
}
