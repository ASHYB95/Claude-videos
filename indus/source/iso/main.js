const Q = new URLSearchParams(location.search);
const g = document.getElementById('c').getContext('2d');
await Promise.all(['500 40px Newsreader', '600 40px Newsreader', '700 40px Newsreader'].map(f => document.fonts.load(f)));
const F = await import(Q.get('test') ? './film_test.js' : './film.js');
window.DUR = F.DUR; window.EV = F.EV || []; window.SUBS = F.SUBS || [];
window.render = t => { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; F.render(g, t, Q); };
window.READY = true;
