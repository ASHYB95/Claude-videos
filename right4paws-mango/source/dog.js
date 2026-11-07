// Mango: a ginger Indie dog. One ear up, one flopped, question-mark tail, white chest blaze, red collar.
// mango(C, o): o = { x, y, s, flip, pose: 'lie'|'stand'|'sit', head: {view:'side'|'front', r, dx, dy}, expr, look:[x,y],
//   tail (wag angle, rad), colour (0..1 fill progress), lineDraw (0..1), seed, earPerk (0..1), eyeDraw }
import { line, fill, dab, ellipse, handCircle, xf, smooth } from './crayon.js';
import { part, tube, curve } from './rig.js';
import { PAL } from './pal.js';
import { clamp, lerp } from './lib.js';
const K = PAL.crayon;
const LW = 7;

export function mango(C, o) {
  const k = o.flip ? -1 : 1, s = o.s ?? 1, sd = o.seed ?? 500;
  const T = pts => xf(pts, { x: o.x, y: o.y, s, sx: k });
  const col = o.colour ?? 1, ld = o.lineDraw ?? 1;
  const LO = (n, w = LW) => ({ w, seed: sd + n, col: K.ink, draw: ld });
  const FO = (c, n, ex = {}) => col > 0 ? { col: c, p: 0.85, gap: 9, w: 11, draw: col, seed: sd + n, ang: 0.7, over: 5, ...ex } : null;
  const G = (n) => FO(K.ginger, n);
  const pose = o.pose || 'stand';
  const H = o.head || {};
  const tail = o.tail ?? 0;

  const tailTube = (base, a, flipT = 1) => {
    const raw = [[0, 0], [-40 * flipT, -45], [-52 * flipT, -110], [-28 * flipT, -152], [6 * flipT, -146]];
    const c = Math.cos(a), sn = Math.sin(a);
    const pts = curve(raw.map(([x, y]) => [base[0] + x * c - y * sn, base[1] + x * sn + y * c]), 4);
    return tube(pts, 36, 18);
  };

  if (pose === 'stand') {
    // far legs, tail, body, near legs, neck, head
    const legF = [[150, -220], [162, -110], [168, -10]], legB = [[-140, -220], [-152, -112], [-160, -10]];
    part(C, T(tube(legF, 46, 40)), G(1), LO(1));
    part(C, T(tube(legB, 50, 40)), G(2), LO(2));
    part(C, T(tailTube([-195, -262], -0.25 + tail)), G(3), LO(3));
    part(C, T(ellipse(0, -232, 215, 98, 40)), G(4), LO(4));
    part(C, T(smooth([[178, -262], [212, -236], [206, -190], [182, -180], [170, -220]], 5)), null, null);   // chest blaze: paper left white
    const nf = [[118, -210], [124, -112], [120, -10]], nb = [[-168, -212], [-180, -118], [-172, -10]];
    part(C, T(tube(nf, 48, 42)), G(5), LO(5));
    part(C, T(tube(nb, 54, 42)), G(6), LO(6));
    paw(C, T, 128, -6, sd + 7, col, ld); paw(C, T, -166, -6, sd + 8, col, ld);
    const hp = [248 + (H.dx ?? 0), -400 + (H.dy ?? 0)];
    const ne = [hp[0] - 22, hp[1] + 30], nm = [lerp(150, ne[0], 0.55) + 10, lerp(-250, ne[1], 0.55) - 10];
    part(C, T(tube(curve([[150, -250], nm, ne], 4), 104, 92)), G(9), LO(9));
    const cA = [lerp(150, ne[0], 0.72), lerp(-250, ne[1], 0.72)];
    const dx = ne[0] - 150, dy = ne[1] + 250, dl = Math.hypot(dx, dy);
    collarSide(C, T, [[cA[0] + dy / dl * 46, cA[1] - dx / dl * 46], [cA[0] - dy / dl * 46, cA[1] + dx / dl * 46]], sd + 10, col, ld);
    headSide(C, o, T, hp, H.r ?? 0, sd + 20, col, ld);
  } else if (pose === 'lie') {
    part(C, T(tailTube([-235, -70], -1.15 + tail * 0.4, 1)), G(1), LO(1));
    part(C, T(ellipse(-20, -96, 232, 86, 40)), G(2), LO(2));
    part(C, T(ellipse(-128, -104, 98, 82, 32)), G(3), LO(3));
    part(C, T(ellipse(-50, -20, 62, 20, 20)), G(4), LO(4));
    part(C, T(tube([[130, -78], [240, -44], [338, -28]], 50, 40)), G(5), LO(5));
    part(C, T(tube([[110, -62], [230, -22], [332, -10]], 50, 40)), G(6), LO(6));
    part(C, T(smooth([[150, -120], [196, -110], [196, -70], [150, -60]], 5)), null, null);
    collarSide(C, T, [[200, -170], [236, -100]], sd + 10, col, ld);
    const hp = [300 + (H.dx ?? 0), -128 + (H.dy ?? 0)];
    if (H.view === 'side') headSide(C, o, T, hp, H.r ?? 0.12, sd + 20, col, ld);
    else headFront(C, o, T, hp, H.r ?? 0, sd + 20, col, ld);
  } else if (pose === 'sit') {
    part(C, T(tailTube([110, -60], 0.55 + tail, -1)), G(1), LO(1));
    part(C, T(ellipse(-104, -78, 88, 78, 30)), G(2), LO(2));
    part(C, T(ellipse(104, -78, 88, 78, 30)), G(3), LO(3));
    part(C, T(ellipse(-150, -14, 48, 18, 18)), G(4), LO(4));
    part(C, T(ellipse(150, -14, 48, 18, 18)), G(5), LO(5));
    part(C, T(ellipse(0, -226, 128, 176, 40)), G(6), LO(6));
    part(C, T(smooth([[0, -360], [52, -300], [46, -170], [0, -128], [-46, -170], [-52, -300]], 5)), null, null);
    part(C, T(tube([[-46, -200], [-50, -96], [-52, -16]], 48, 44)), G(7), LO(7));
    part(C, T(tube([[46, -200], [50, -96], [52, -16]], 48, 44)), G(8), LO(8));
    paw(C, T, -54, -8, sd + 9, col, ld); paw(C, T, 54, -8, sd + 11, col, ld);
    const hp = [0 + (H.dx ?? 0), -440 + (H.dy ?? 0)];
    collarFront(C, T, [0, -372], sd + 12, col, ld);
    if (H.view === 'side') headSide(C, o, T, hp, H.r ?? 0, sd + 20, col, ld);
    else headFront(C, o, T, hp, H.r ?? 0, sd + 20, col, ld);
  }
}

function paw(C, T, x, y, sd, col, ld) {
  part(C, T(ellipse(x + 6, y - 6, 34, 16, 18)), col > 0 ? { col: K.ginger2, p: 0.8, gap: 7, w: 9, draw: col, seed: sd } : null, { w: 6, seed: sd, col: K.ink, draw: ld });
}
function collarSide(C, T, [a, b], sd, col, ld) {
  const poly = tube([a, b], 26, 26);
  part(C, T(poly), col > 0 ? { col: K.red, p: 1, gap: 6, w: 9, draw: col, seed: sd } : null, { w: 5, seed: sd, col: K.ink, draw: ld });
  const tg = [(a[0] + b[0]) / 2 + 6, (a[1] + b[1]) / 2 + 22];
  part(C, T(handCircle(tg[0], tg[1], 13, sd, 0, 18)), col > 0 ? { col: K.yolk, p: 0.9, gap: 4, w: 6, draw: col, seed: sd + 1, over: 1 } : null, { w: 4, seed: sd + 1, col: K.ink, draw: ld });
}
function collarFront(C, T, [x, y], sd, col, ld) {
  const pts = []; for (let i = 0; i <= 16; i++) { const a = Math.PI * (0.12 + 0.76 * i / 16); pts.push([x - Math.cos(a) * 92, y + Math.sin(a) * 26 - 10]); }
  part(C, T(tube(pts, 26, 26)), col > 0 ? { col: K.red, p: 1, gap: 6, w: 9, draw: col, seed: sd } : null, { w: 5, seed: sd, col: K.ink, draw: ld });
  part(C, T(handCircle(x, y + 38, 14, sd, 0, 18)), col > 0 ? { col: K.yolk, p: 0.9, gap: 4, w: 6, draw: col, seed: sd + 1, over: 1 } : null, { w: 4, seed: sd + 1, col: K.ink, draw: ld });
}

// —— head, side view (facing +x). Local origin = skull centre
function headSide(C, o, T0, hp, r, sd, col, ld) {
  const T = pts => T0(xf(pts, { x: hp[0], y: hp[1], r }));
  const ex = o.expr || 'meh', perk = o.earPerk ?? 0.5;
  const LO = (n, w = LW) => ({ w, seed: sd + n, col: K.ink, draw: ld });
  const FO = (c, n, ex2 = {}) => col > 0 ? { col: c, p: 0.85, gap: 8, w: 10, draw: col, seed: sd + n, ang: 0.4, over: 4, ...ex2 } : null;
  // far ear (up, pricked); droops when bored
  const up = lerp(0.6, 0, perk);
  part(C, T(xf([[-50, -48], [-30, -178], [8, -60]], { r: -up, ox: -20, oy: -55 })), FO(K.ginger, 1), LO(1));
  part(C, T(ellipse(0, 0, 90, 80, 36)), FO(K.ginger, 2), LO(2));
  part(C, T(smooth([[36, -34], [118, -30], [156, 0], [146, 42], [92, 54], [36, 46]], 5)), FO(K.ginger2, 3), LO(3));
  // nose
  part(C, T(ellipse(154, -6, 17, 14, 16)), { col: K.ink, p: 1, gap: 4, w: 6, seed: sd + 4, over: 1, draw: clamp(ld * 2 - 0.6) }, LO(4, 5));
  // mouth / tongue
  if (ex === 'happy' || ex === 'excited' || ex === 'chomp') {
    line(C.l, T(curve([[140, 36], [110, 58], [74, 52]])), LO(5, 5));
    if (ex !== 'chomp') part(C, T(smooth([[96, 50], [124, 54], [126, 92], [106, 104], [92, 84]], 5)), { col: K.pink, p: 0.9, gap: 5, w: 8, seed: sd + 6 }, LO(6, 5));
  } else line(C.l, T(curve([[140, 38], [112, 50], [80, 46]])), LO(5, 5));
  // eye
  eyeS(C, T, 32, -22, ex, sd + 7, o);
  if (col > 0) dab(C.f, ...T([[42, 18]])[0], 12 * (o.s ?? 1), { col: K.pink, p: 0.55, seed: sd + 8 });
  // near ear: floppy, hangs at the back of the skull (lifts when excited)
  const flap = (ex === 'excited' ? -0.5 : 0) + (o.earFlap ?? 0);
  part(C, T(xf([[-34, -58], [-98, -36], [-92, 30], [-42, -6]], { r: flap, ox: -34, oy: -40 })), FO(K.ginger, 9), LO(9));
}
function eyeS(C, T, x, y, ex, sd, o) {
  const LO = (n, w) => ({ w, seed: sd + n, col: K.ink });
  if (ex === 'happy' || ex === 'chomp') { line(C.l, T(curve([[x - 16, y + 4], [x, y - 12], [x + 16, y + 4]])), LO(0, 6)); return; }
  const [lx, ly] = o.look || [0, 0];
  const ex2 = ex === 'excited' ? 1.25 : 1;
  const c = T([[x + lx * 5, y + ly * 5]])[0];
  dab(C.f, c[0], c[1], 10 * ex2 * (o.s ?? 1), { col: K.ink, p: 1, seed: sd + 1, gap: 3, w: 5 });
  const cl = T([[x + lx * 5 + 3, y + ly * 5 - 4]])[0];
  dab(C.f, cl[0], cl[1], 3.2 * (o.s ?? 1), { col: K.white, p: 1, seed: sd + 2, gap: 2, w: 3 });
  if (ex === 'meh' || ex === 'bored' || ex === 'sniff') line(C.l, T([[x - 16, y - 4], [x + 15, y - 7]]), LO(3, 6));   // heavy lid
}

// —— head, front view. Local origin = face centre
export function headFront(C, o, T0, hp, r, sd, col, ld) {
  const T = pts => T0(xf(pts, { x: hp[0], y: hp[1], r }));
  const ex = o.expr || 'meh', perk = o.earPerk ?? 0.5;
  const LO = (n, w = LW) => ({ w, seed: sd + n, col: K.ink, draw: ld });
  const FO = (c, n, ex2 = {}) => col > 0 ? { col: c, p: 0.85, gap: 8, w: 10, draw: col, seed: sd + n, ang: 0.4, over: 4, ...ex2 } : null;
  const up = lerp(0.7, 0, perk);
  // left ear pricked, right ear flopped
  part(C, T(xf([[-82, -40], [-98, -190], [-22, -84]], { r: -up, ox: -60, oy: -60 })), FO(K.ginger, 1), LO(1));
  if (col > 0) fill(C.f, T(xf([[-74, -60], [-88, -160], [-40, -88]], { r: -up, ox: -60, oy: -60 })), { col: K.ginger2, p: 0.7, gap: 6, w: 8, draw: col, seed: sd + 2 });
  part(C, T(ellipse(0, 0, 100, 90, 40)), FO(K.ginger, 3), LO(3));
  const flap = (ex === 'excited' ? -0.45 : 0) + (o.earFlap ?? 0);
  part(C, T(xf([[34, -76], [118, -112], [140, -18], [92, -26], [70, -58]], { r: flap, ox: 50, oy: -70 })), FO(K.ginger, 4), LO(4));
  part(C, T(ellipse(0, 44, 56, 40, 30)), FO(K.ginger2, 5), LO(5));
  part(C, T(ellipse(0, 22, 22, 15, 18)), { col: K.ink, p: 1, gap: 4, w: 6, seed: sd + 6, over: 1 }, LO(6, 5));
  // mouth
  const happy = ex === 'happy' || ex === 'excited' || ex === 'chomp';
  if (happy) {
    line(C.l, T(curve([[-34, 50], [-16, 66], [0, 52], [16, 66], [34, 50]])), LO(7, 5));
    if (ex !== 'chomp') part(C, T(smooth([[-14, 62], [14, 62], [18, 102], [0, 114], [-18, 102]], 5)), { col: K.pink, p: 0.9, gap: 5, w: 8, seed: sd + 8 }, LO(8, 5));
  } else line(C.l, T(curve([[-24, 58], [0, 54], [24, 58]])), LO(7, 5));
  // eyes
  for (const [i, ex0] of [[0, -40], [1, 40]]) {
    if (ex === 'happy' || ex === 'chomp') { line(C.l, T(curve([[ex0 - 16, -6], [ex0, -22], [ex0 + 16, -6]])), LO(9 + i, 6)); continue; }
    const [lx, ly] = o.look || [0, 0], k = ex === 'excited' ? 1.3 : 1;
    const c = T([[ex0 + lx * 7, -12 + ly * 6]])[0];
    dab(C.f, c[0], c[1], 11 * k * (o.s ?? 1), { col: K.ink, p: 1, seed: sd + 11 + i, gap: 3, w: 5 });
    const cl = T([[ex0 + lx * 7 + 4, -16 + ly * 6]])[0];
    dab(C.f, cl[0], cl[1], 3.4 * (o.s ?? 1), { col: K.white, p: 1, seed: sd + 13 + i, gap: 2, w: 3 });
    if (ex === 'meh' || ex === 'bored') line(C.l, T([[ex0 - 18, -18], [ex0 + 18, -20]]), LO(15 + i, 6));
    if (ex === 'wait') line(C.l, T(curve([[ex0 - 16, -40], [ex0, -48], [ex0 + 16, -42]])), LO(17 + i, 5));   // raised brows: hopeful
  }
  if (col > 0) {
  dab(C.f, ...T([[-62, 28]])[0], 13 * (o.s ?? 1), { col: K.pink, p: 0.5, seed: sd + 20 });
  dab(C.f, ...T([[62, 28]])[0], 13 * (o.s ?? 1), { col: K.pink, p: 0.5, seed: sd + 21 });
  }
}
