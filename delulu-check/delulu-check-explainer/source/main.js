import * as F from './film.js';
await Promise.all(['400 40px Inter', '600 40px Inter', '700 40px "Inter Tight"', '800 40px "Inter Tight"', '40px Bebas', '500 40px JBM', '40px Anton'].map(f => document.fonts.load(f)));
await document.fonts.load('40px "Noto Color Emoji"').catch(() => {});
const world = document.getElementById('world'), hud = document.getElementById('hud');
window.DUR = F.DUR; window.EV = F.EV; window.SUBS = F.SUBS; window.TEXTS = F.TEXTS;
window.render = t => F.render(t, world, hud);
F.render(0, world, hud);
await new Promise(r => setTimeout(r, 300));
window.READY = true;
