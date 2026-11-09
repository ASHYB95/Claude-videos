// Film palette: warm paper, warm ink, soft atomic-age complements.
// The product (pack, logo plate) is always and only brand red; the accent is turquoise.
export const C = {
  paper: '#F3E7D3', paperD: '#E4D3B6', card: '#FBEFE4',
  ink: '#2A211C', inkSoft: '#4A3F38',
  red: '#D9282E', redD: '#A81E24', redL: '#EC6A6E',
  teal: '#3F9C99', tealD: '#2B7472', tealL: '#8ACBC6',
  blue: '#A9C9D3', blueD: '#7FA7B5', blueL: '#CFE1E6',
  mustard: '#E2B24E', mustardD: '#C4923A', mustardL: '#F0CF86',
  sage: '#AEBB75', sageD: '#8D9A57', sageL: '#CDD5A3',
  ginger: '#D8812E', gingerD: '#B5651F', gingerL: '#F0B26C',
  white: '#FBEFE4', pink: '#E99A8E', pinkD: '#C9766B',
  flake: '#8C5A3A', flakeL: '#B07A4E', flakeD: '#5E3820', soft: '#74432A',
  steel: '#BFC4C6', steelD: '#8E959B', steelL: '#E8EAE6',
  skin: '#C98E63', skinD: '#A9724B',
};
const hx = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
export const mix = (a, b, k) => { const A = hx(a), B = hx(b); return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, '0')).join(''); };
export const tint = (c, k) => mix(c, '#FFFFFF', k), shade = (c, k) => mix(c, '#2A211C', k);
