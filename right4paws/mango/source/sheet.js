import { layer, clear, text, CAM, BOIL } from './crayon.js';
import { group, clearGroup } from './rig.js';
import { mango } from './dog.js';
import { PAL } from './pal.js';
const D = group(), TX = layer();
export function sheet(comp, t, Q) {
  CAM.x = 540; CAM.y = 960; CAM.s = 1;
  clearGroup(D); clear(TX);
  const sc = 0.62;
  mango(D, { x: 300, y: 470, s: sc, pose: 'lie', head: { view: 'side' }, expr: 'meh', earPerk: 0, colour: 0, seed: 1 });
  mango(D, { x: 760, y: 470, s: sc, pose: 'lie', head: { view: 'front', r: -0.15 }, expr: 'bored', earPerk: 0.1, colour: 1, seed: 2 });
  mango(D, { x: 280, y: 1000, s: sc, pose: 'stand', head: {}, expr: 'excited', earPerk: 1, tail: 0.3, colour: 1, seed: 3 });
  mango(D, { x: 780, y: 1000, s: sc, pose: 'sit', head: { view: 'front' }, expr: 'wait', look: [-1, -0.6], earPerk: 0.9, colour: 1, seed: 4 });
  mango(D, { x: 280, y: 1560, s: sc, pose: 'stand', head: { dx: 40, dy: 210, r: 0.75 }, expr: 'chomp', earPerk: 0.8, tail: -0.2, colour: 1, seed: 5 });
  mango(D, { x: 780, y: 1560, s: sc, pose: 'sit', head: { view: 'front', r: 0.12 }, expr: 'happy', earPerk: 1, tail: 0.4, colour: 1, seed: 6 });
  text(TX, 'Mango · model sheet', 540, 1860, { size: 56, col: PAL.crayon.ink });
  comp.paperCam(540, 960, 1); comp.begin(PAL.paper);
  comp.group(D); comp.crayon(TX.c); comp.finish({ vig: 0.2 });
}
