// Right4Paws brand palette (pack, logo tab, feeding guide and right4paws.com):
// brand red (logo tab / pack), cream, off-white, near-black, warm light grey. The red/white checker and halftone
// dots come from the brand's feeding guide. Natural colours stay natural: Mango's ginger fur, the brown flakes, steel.
export const C = {
  red: '#CB112B', redD: '#9C0D21', redL: '#EE8F93', redT: '#FBE1DB',
  paper: '#FFEDDF', paperD: '#F2D9C5', card: '#FFF8F2', white: '#FFF8F2',
  ink: '#1F1A19', inkSoft: '#4A403C',
  grey: '#ECE6E1', greyD: '#D3CBC4', greyDD: '#AFA59D',
  ginger: '#D8812E', gingerD: '#B5651F', gingerL: '#F0B26C', pink: '#E99A8E',
  flake: '#8C5A3A', flakeL: '#B07A4E', flakeD: '#5E3820', soft: '#74432A', kibble: '#9A7652', kibbleD: '#6F5236',
  steel: '#BFC4C6', steelD: '#8E959B', steelL: '#F2F3F0',
  skin: '#C98E63', skinD: '#A9724B',
};
const hx = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
export const mix = (a, b, k) => { const A = hx(a), B = hx(b); return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, '0')).join(''); };
export const tint = (c, k) => mix(c, '#FFFFFF', k), shade = (c, k) => mix(c, '#1F1A19', k);
