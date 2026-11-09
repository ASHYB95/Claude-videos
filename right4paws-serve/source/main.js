// Page contract: window.READY, window.render(t), window.DUR
import { textures } from './engine/toon.js';
import { setLogo } from './engine/props.js';
const cv = document.getElementById('c'), g = cv.getContext('2d');
await Promise.all(['700 80px Oleo', '400 80px Oleo', '80px Slab', '400 40px Jost', '500 40px Jost', '600 40px Jost', '800 40px Jost'].map(f => document.fonts.load(f)));
textures();
const load = async src => { const im = new Image(); im.src = src; await im.decode(); return im; };
const [mark, tab, white] = await Promise.all(['img/logomark.png', 'img/logo_tab.png', 'img/logo_white.png'].map(load));
setLogo(mark, { tab, white });
const film = await import('./film.js');
window.DUR = film.DUR;
window.render = async t => { g.setTransform(1, 0, 0, 1, 0, 0); film.renderFilm(g, t); };
window.READY = true;
