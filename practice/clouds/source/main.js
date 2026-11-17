import { textures } from './engine/toon.js';
const g = document.getElementById('c').getContext('2d');
await Promise.all(['700 80px Oleo', '400 80px Oleo', '80px Slab', '400 40px Jost', '500 40px Jost', '600 40px Jost'].map(f => document.fonts.load(f)));
textures();
const F = await import('./film.js');
window.DUR = F.DUR; window.EV = F.EV; window.SUBS = F.SUBS;
window.render = t => F.render(g, t);
window.READY = true;
