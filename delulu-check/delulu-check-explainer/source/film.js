// Delulu Check — "Your chat already knows". Living Screencast, 1080×1920, 30 s.
// The phone UI is redrawn as HTML each frame (screen-local coords, 836×1636); camera = CSS transform on #world.
import { clamp, lerp, seg, eo, eio, ei, back, hash, track } from './lib.js';
export const DUR = 30;
const SX = 122, SY = 118;            // screen origin in world coords
const W = 836, H = 1636;
const pr = seg;

// —— narration (t = start; d from TTS)
export const LINES = [
  { id: 'v1', t: 0.4, d: 2.33, text: 'Three days of silence. Then… a meme.' },
  { id: 'v2', t: 4.2, d: 1.68, text: 'Upload the chat to Delulu Check.' },
  { id: 'v3', t: 7.4, d: 1.706, text: 'It reads every single message…' },
  { id: 'v4', t: 11.6, d: 1.675, text: '…and tells you where you actually stand.' },
  { id: 'v5', t: 15.4, d: 1.946, text: 'Ask Doctor Delulu what to do next.' },
  { id: 'v6', t: 19.6, d: 2.563, text: 'Then let the keyboard write the reply. In any app.' },
  { id: 'v7', t: 25.4, d: 3.17, text: 'Your friends are too nice to tell you. Your chat already did.' },
];
export const SUBS = LINES.map((L, i) => { const nx = LINES[i + 1]; return { t0: L.t - 0.1, t1: Math.min(Math.max(L.t + 1.8, L.t + L.d + 0.6), nx ? nx.t - 0.1 : DUR), text: L.text }; });

// —— key times
const T = { meme: 1.5, type0: 2.9, sheet: 4.0, tapDC: 5.0, whip: [5.25, 5.65], upload: [5.7, 7.0], born: 7.0, read: [7.4, 10.9], hush: [10.9, 11.45],
  report: 11.45, count: [11.9, 13.0], quote: 13.6, doctor: 15.3, ask: 16.6, rep1: 17.5, rep2: 18.4, kbd: 19.5, god: 20.1, cook: [20.3, 21.5], sugg: 21.5,
  chill: 22.5, pick: 23.5, send: 24.3, end: 25.0, line2: 26.8, logo: 27.6, cta: 28.0, click: 28.4 };

// —— camera [cx, cy, zoom]
const cam = track([
  [0, [540, 1020, 1.35]], [1.4, [560, 1060, 1.32]], [3.6, [540, 960, 1.0]], [5.25, [540, 960, 1.0]], [5.65, [540, 960, 1.0]],
  [7.2, [540, 820, 1.18]], [10.9, [540, 860, 1.18]], [11.45, [540, 960, 1.0]], [11.9, [540, 960, 1.0]], [12.6, [540, 1150, 1.55]], [13.4, [540, 1150, 1.55]],
  [14.2, [540, 800, 1.3]], [15.3, [540, 800, 1.3]], [15.5, [540, 960, 1.0]], [16.4, [540, 1060, 1.12]], [19.2, [540, 1180, 1.12]], [19.5, [540, 960, 1.0]],
  [21.4, [540, 1260, 1.18]], [23.0, [540, 1300, 1.18]], [23.8, [540, 1000, 1.28]], [24.4, [540, 1000, 1.28]], [25.0, [540, 960, 1.0]], [25.2, [540, 900, 1.12]],
  [26.8, [540, 960, 1.0]], [30, [540, 960, 1.0]],
]);

// —— events for the mixer
export const EV = [];
const ev = (t, type, o = {}) => EV.push({ t: +t.toFixed(3), type, ...o });
LINES.forEach(L => ev(L.t, 'voice', { id: L.id }));
ev(0, 'room'); ev(T.meme, 'pop'); for (let i = 0; i < 8; i++) ev(T.type0 + i * 0.09, 'key', { soft: 1 }); ev(T.type0 + 0.9, 'delete', { dur: 0.5 });
ev(T.sheet, 'swish'); ev(T.tapDC, 'tap'); ev(T.whip[0], 'whoosh');
for (let i = 0; i < 10; i++) ev(T.upload[0] + i * 0.13, 'tick');
ev(T.born, 'spawn'); for (let t = T.read[0]; t < T.read[1]; t += 0.25) ev(t, 'step8');
ev(T.read[0], 'whirr', { dur: T.read[1] - T.read[0] });
ev(T.hush[0], 'riser', { dur: 0.55 }); for (let i = 0; i < 12; i++) ev(T.count[0] + i * 0.09, 'mtick'); ev(T.count[1], 'ding'); ev(T.quote, 'slap');
ev(T.doctor, 'swish'); ev(T.ask, 'send'); ev(T.rep1, 'recv'); ev(T.rep2, 'recv'); ev(T.rep1 + 0.1, 'sit8');
ev(T.kbd, 'swish'); ev(T.god, 'tap'); ev(T.cook[0], 'shimmer', { dur: 1.2 }); ev(T.sugg, 'recv');
ev(T.chill, 'tap'); ev(T.chill + 0.15, 'shimmer', { dur: 0.5 }); ev(T.pick, 'tap'); for (let i = 0; i < 6; i++) ev(T.pick + 0.1 + i * 0.05, 'key', { soft: 1 });
ev(T.send, 'tap'); ev(T.send + 0.05, 'send'); ev(T.send + 0.1, 'jump8');
ev(T.end, 'swish'); ev(T.click, 'tap'); ev(T.click + 0.02, 'jump8'); ev(28.0, 'hit');
[['intro', 0], ['drop', 4.0], ['hush', 10.9], ['back', 11.45], ['fill', 19.0], ['break', 25.0], ['hit', 28.0]].forEach(([id, t]) => ev(t, 'cue', { id }));

// —————————————————— drawing helpers (HTML strings)
const st = o => Object.entries(o).map(([k, v]) => `${k.replace(/[A-Z]/g, m => '-' + m.toLowerCase())}:${typeof v === 'number' && !/opacity|z-index|font-weight|line-height|flex/.test(k.replace(/[A-Z]/g, m => '-' + m.toLowerCase())) ? v + 'px' : v}`).join(';');
const box = (x, y, w, h, s = {}, inner = '') => `<div class="abs" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${st(s)}">${inner}</div>`;
const txt = (x, y, w, s, inner) => `<div class="abs" style="left:${x}px;top:${y}px;width:${w}px;${st(s)}">${inner}</div>`;
export function logo(size, id = 'g') {
  return `<svg width="${size}" height="${size * 0.84}" viewBox="0 0 120 100"><defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff3fb4"/><stop offset=".55" stop-color="#b44cf0"/><stop offset="1" stop-color="#6a5cf5"/></linearGradient></defs>
  <path d="M6 8 H38 C66 8 78 28 78 50 C78 72 66 92 38 92 H6 L18 50 Z" fill="url(#${id})"/>
  <path d="M116 18 C104 8 92 6 84 8 C70 12 62 30 62 50 C62 70 70 88 84 92 C92 94 104 92 116 82 L100 66 C96 72 90 74 86 72 C80 68 78 60 78 50 C78 40 80 32 86 28 C90 26 96 28 100 34 Z" fill="url(#${id})"/>
  <path d="M40 74 C20 60 18 46 26 40 C33 35 40 40 42 45 C44 40 51 35 58 40 C66 46 62 60 40 74 Z" fill="#2a0f2e" stroke="#ff7ad0" stroke-width="2.5"/>
  <path d="M30 50 L50 44 M30 56 L52 50 M34 62 L50 56" stroke="#ff3fb4" stroke-width="2" stroke-linecap="round"/></svg>`;
}
// Delu: 12×11 pixel sprite
const SPR = ['..MM....MM..', '.MMMM..MMMM.', 'MMMMMMMMMMMM', 'MMWWMMMMWWMM', 'MMWKMMMMWKMM', 'MMMMMMMMMMMM', '.MMMMPPMMMM.', '..MMMMMMMM..', '...MMMMMM...', '....MMMM....', '...F....F...'];
const ROWC = ['#ff3fb4', '#ff3fb4', '#f040c0', '#e042cc', '#d044d6', '#c046e0', '#b048e6', '#a04aec', '#904cf0', '#804ef2', '#3a1a5a'];
function delu(x, y, p, o = {}) {   // x,y = bottom-centre (world); p = pixel size
  const sq = o.sq ?? 1, flip = o.flip, look = o.look ?? 0, blink = o.blink, happy = o.happy;
  let h = ''; const w = 12 * p, hh = 11 * p * sq, x0 = Math.round((x - w / 2) * 2) / 2, y0 = Math.round((y - hh) * 2) / 2;
  SPR.forEach((row, r) => [...row].forEach((c, k) => {
    if (c === '.') return; const kk = flip ? 11 - k : k; let col = ROWC[r];
    if (c === 'W') col = blink ? ROWC[r] : '#fff';
    if (c === 'K') { col = blink ? '#3a1a5a' : '#1a0b22'; }
    if (c === 'W' && happy) col = '#1a0b22';
    if (c === 'K' && happy) col = ROWC[r];
    if (c === 'P') col = '#ffb3e0';
    if (c === 'F') col = '#3a1a5a';
    let dx = 0; if ((c === 'K') && look) dx = look > 0 ? (flip ? -1 : 1) * 0 : 0;
    const kx = (c === 'K' && look) ? kk + (look > 0 ? 0 : -1) * 0 : kk;
    h += `<div class="px" style="left:${x0 + kx * p + dx}px;top:${y0 + r * p * sq}px;width:${p + 0.6}px;height:${p * sq + 0.6}px;background:${col}"></div>`;
  }));
  if (o.arms) { const ay = y0 + 6 * p * sq; h += `<div class="px" style="left:${x0 - p}px;top:${ay - p * 2}px;width:${p}px;height:${p * 2}px;background:#c046e0"></div><div class="px" style="left:${x0 + 12 * p}px;top:${ay - p * 2}px;width:${p}px;height:${p * 2}px;background:#c046e0"></div>`; }
  return h;
}
function sparks(x, y, k, n, col = '#ffc928', r0 = 30, r1 = 120, p = 8) {
  let h = ''; for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2 + 0.3, r = lerp(r0, r1, eo(k)); h += `<div class="px" style="left:${x + Math.cos(a) * r}px;top:${y + Math.sin(a) * r * 0.8}px;width:${p}px;height:${p}px;background:${i % 2 ? col : '#ff3fb4'};opacity:${1 - k}"></div>`; } return h;
}
const cursorSvg = (x, y, sc, z) => `<svg class="abs" style="left:${x - 4}px;top:${y - 2}px;transform:scale(${sc / z});transform-origin:4px 2px;filter:drop-shadow(0 4px 6px rgba(0,0,0,.45))" width="46" height="60" viewBox="0 0 46 60"><path d="M4 2 L4 46 L15 36 L23 56 L31 52 L23 33 L39 33 Z" fill="#fff" stroke="#111" stroke-width="3" stroke-linejoin="round"/></svg>`;

// —————————————————— screens (screen-local coords)
const statusBar = (dark) => `${txt(70, 40, 120, { font: '600 30px Inter', color: dark ? '#fff' : '#111' }, '9:41')}${txt(640, 40, 140, { font: '600 26px Inter', color: dark ? '#fff' : '#111', textAlign: 'right' }, '▮▮▮ ◔ ▬')}`;
const bubble = (x, y, w, text, o = {}) => {
  const out = o.out; const bg = o.bg || (out ? '#d9fdd3' : '#fff');
  return box(x, y, w, o.h ?? 'auto', { background: bg, borderRadius: out ? '26px 26px 6px 26px' : '26px 26px 26px 6px', padding: '18px 24px', font: `400 ${o.fs ?? 34}px Inter`, lineHeight: 1.3, color: o.col || '#111', boxShadow: '0 2px 2px rgba(0,0,0,.08)', opacity: o.op ?? 1, transform: o.tf || 'none', transformOrigin: out ? '100% 100%' : '0 100%' }, text + (o.time ? `<span style="float:right;font-size:22px;color:#667;margin:14px 0 0 16px">${o.time}</span>` : ''));
};
function chatHeader(sub) {
  return box(0, 0, W, 210, { background: '#f6f5f3', borderBottom: '1px solid #ddd' }, statusBar(false) +
    txt(36, 128, 40, { font: '600 44px Inter', color: '#1c8a7a' }, '‹') +
    box(86, 106, 84, 84, { borderRadius: '50%', background: 'linear-gradient(135deg,#ffb36b,#ff6f91)', font: '600 40px Inter', color: '#fff', textAlign: 'center', lineHeight: '84px' }, 'A') +
    txt(190, 110, 400, { font: '600 40px Inter', color: '#111' }, 'Aarav') + txt(190, 158, 500, { font: '400 26px Inter', color: '#667' }, sub));
}
function memeCard(x, y, sc, op) {
  return box(x, y, 560, 520, { background: '#fff', borderRadius: '26px 26px 26px 6px', padding: '14px', boxShadow: '0 2px 2px rgba(0,0,0,.08)', transform: `scale(${sc})`, transformOrigin: '0 100%', opacity: op },
    box(14, 14, 532, 420, { background: 'linear-gradient(180deg,#2b3a55,#1b2233)', borderRadius: '18px', overflow: 'hidden' },
      txt(0, 26, 532, { font: '400 46px Anton', color: '#fff', textAlign: 'center', textShadow: '0 0 6px #000,0 0 2px #000', letterSpacing: '1px' }, 'ME AFTER 3 DAYS OF SILENCE') +
      txt(0, 120, 532, { fontSize: '170px', textAlign: 'center', lineHeight: 1 }, '😎') +
      txt(0, 330, 532, { font: '400 46px Anton', color: '#fff', textAlign: 'center', textShadow: '0 0 6px #000' }, '*SENDS MEME*')) +
    txt(380, 470, 160, { font: '400 22px Inter', color: '#667', textAlign: 'right' }, '9:14 pm'));
}
function chatScreen(t, o = {}) {
  let h = box(0, 0, W, H, { background: '#efe7dc' });
  const yo = o.yo || 0;
  h += box(330, 250 + yo, 176, 46, { background: '#fff', borderRadius: '12px', font: '600 22px Inter', color: '#667', textAlign: 'center', lineHeight: '46px' }, 'MONDAY');
  h += bubble(300, 320 + yo, 500, 'had so much fun tonight!! 🥹', { out: true, time: '11:52 pm <span style="color:#3aa0ff">✓✓</span>' });
  h += bubble(360, 450 + yo, 440, 'text me when u get home?', { out: true, time: '11:53 pm <span style="color:#3aa0ff">✓✓</span>' });
  h += box(268, 600 + yo, 300, 50, { background: '#fff2c4', borderRadius: '12px', font: '600 24px JBM', color: '#8a6a00', textAlign: 'center', lineHeight: '50px', letterSpacing: '2px' }, '3 DAYS LATER');
  const mk = o.memeK ?? 1;
  if (mk > 0) h += memeCard(36, 690 + yo, back(clamp(mk), 1.6) * 0.98 + 0.02, clamp(mk * 3));
  if (o.sent) { const k = o.sent; h += bubble(250, 580 + (1 - eo(k)) * 130, 550, o.sentText, { out: true, time: '9:31 pm ✓', op: clamp(k * 3) }); }
  h += chatHeader(o.sub || 'last seen 3 days ago');
  // input bar
  const iy = o.inputY ?? 1530;
  h += box(0, iy - 26, W, H - iy + 26, { background: '#f6f5f3' });
  h += box(26, iy, 670, 84, { background: '#fff', borderRadius: '42px', font: '400 32px Inter', color: o.typed ? '#111' : '#999', padding: '22px 30px 0 84px', overflow: 'hidden', whiteSpace: 'nowrap' },
    txt(26, 18, 50, { fontSize: '38px' }, '🙂') + (o.typed || 'Message') + (o.caret && Math.floor(t * 2.5) % 2 ? '<span style="color:#1c8a7a">|</span>' : ''));
  h += box(712, iy, 84, 84, { borderRadius: '50%', background: '#1c8a7a', color: '#fff', font: '600 38px Inter', textAlign: 'center', lineHeight: '84px' }, o.typed ? '➤' : '🎙');
  return h;
}
function shareSheet(k, hi) {
  const y = lerp(H, 820, eo(k));
  const apps = [['Messages', '#34c759', '💬'], ['Mail', '#3b82f6', '✉️'], ['Drive', '#f4b400', '▲'], ['Delulu Check', null, '']];
  let h = box(0, 0, W, H, { background: `rgba(0,0,0,${0.35 * k})` });
  h += box(0, y, W, H - 820 + 40, { background: '#f2f2f6', borderRadius: '40px 40px 0 0' },
    box(368, 18, 100, 10, { background: '#ccc', borderRadius: '5px' }) +
    txt(50, 60, 700, { font: '600 40px Inter', color: '#111' }, 'Export chat') +
    txt(50, 118, 700, { font: '400 28px Inter', color: '#667' }, 'Aarav · 412 messages · without media') +
    apps.map(([n, c, ic], i) => { const x = 50 + i * 190, isD = !c;
      return box(x, 210, 150, 150, { borderRadius: '36px', background: isD ? '#0b0a10' : c, textAlign: 'center', lineHeight: '150px', fontSize: '64px', color: '#fff', boxShadow: isD && hi ? `0 0 0 ${6 * hi}px #c02ee0,0 0 40px rgba(192,46,224,${hi})` : 'none', transform: `scale(${isD && hi ? 1 + 0.06 * Math.sin(hi * 3.14) : 1})` },
        isD ? `<div style="padding-top:28px">${logo(100, 'gs')}</div>` : ic) + txt(x - 20, 375, 190, { font: '400 24px Inter', color: '#333', textAlign: 'center' }, n); }).join(''));
  return h;
}
const SNIPS = ['wyd', 'lol ok', 'my phone died', 'can we talk later', 'you know how…', 'i never said that', 'ok goodnight', 'why do you always…', 'work has been crazy', 'haha same', 'u up?', 'we should hang soon', 'sorry was busy', '😂😂', 'k', 'miss u', 'idk', 'whatever you want', 'brb', 'lmk'];
export const ROWH = 104;
function appScreen(t) {
  let h = box(0, 0, W, H, { background: 'radial-gradient(900px 700px at 50% 0%,#2a0f2e,#0b0a10 70%)' }) + statusBar(true);
  h += box(40, 104, 70, 60, {}, logo(70, 'ga')) + txt(124, 110, 500, { font: '700 42px &quot;Inter Tight&quot;', color: '#fff', letterSpacing: '-1px' }, 'Delulu Check');
  h += txt(40, 210, 760, { font: '500 28px JBM', color: '#a8a3b8', letterSpacing: '6px' }, '<span style="color:#8a5cf5;font-size:40px">01</span>&nbsp;&nbsp;THE REPORT');
  const up = pr(t, T.upload[0], T.upload[1]), rd = t >= T.born;
  const cardY = rd ? lerp(290, 270, eo(pr(t, T.born, T.born + 0.4))) : 290, cardH = rd ? lerp(250, 150, eo(pr(t, T.born, T.born + 0.4))) : 250;
  h += box(40, cardY, 756, cardH, { background: '#15131c', border: '1px solid #2c2838', borderRadius: '30px' },
    (rd ? '' : box(34, 34, 110, 92, {}, `<div style="opacity:${1 - pr(t, T.born - 0.15, T.born)}">${logo(110, 'gu')}</div>`)) +
    txt(rd ? 34 : 170, rd ? 26 : 40, 540, { font: '600 34px Inter', color: '#fff' }, 'Aarav.txt') +
    txt(rd ? 34 : 170, rd ? 72 : 88, 560, { font: '400 26px Inter', color: '#a8a3b8' }, rd ? 'Reading every message' + '.'.repeat(1 + Math.floor(t * 3) % 3) : (up < 1 ? `Uploading… ${Math.round(up * 100)}%` : 'Uploaded ✓')) +
    (rd ? '' : box(34, 170, 688, 18, { background: '#2a2636', borderRadius: '9px', overflow: 'hidden' }, box(0, 0, 688 * up, 18, { background: 'linear-gradient(90deg,#c02ee0,#7a4cf0,#3b63f0)', borderRadius: '9px' }))));
  if (rd) {
    const n = Math.round(lerp(0, 412, eio(pr(t, T.read[0], T.read[1] - 0.3))));
    h += txt(40, 450, 760, { font: '400 54px Bebas', color: '#ff2e88', letterSpacing: '2px', textShadow: '0 0 18px rgba(255,46,136,.6)' }, `${n} MESSAGES ANALYZED`);
    if (t > T.read[0] && t < T.read[1]) h += box(620, 456, 150, 50, { background: 'rgba(255,201,40,.15)', border: '2px solid #ffc928', borderRadius: '25px', font: '600 26px JBM', color: '#ffc928', textAlign: 'center', lineHeight: '46px', opacity: Math.floor(t * 4) % 2 ? 1 : 0.55 }, '▶▶ 8×');
    // message rows scrolling (time-lapse)
    const scroll = Math.max(0, t - T.read[0]) * 300;
    let rows = '';
    for (let i = 0; i < 40; i++) {
      const y = 560 + i * ROWH - scroll; if (y < 520 || y > H) continue;
      const out = hash(i * 3.7) > 0.5, s = SNIPS[i % SNIPS.length], w = 160 + s.length * 17;
      rows += box(out ? W - 40 - w : 40, y, w, 76, { background: out ? 'linear-gradient(90deg,#c02ee0,#7a4cf0 55%,#3b63f0)' : '#1c1a24', borderRadius: '24px', font: '400 30px Inter', color: '#fff', padding: '18px 26px', opacity: clamp((y - 520) / 120) * (y < 700 ? 0.55 : 1) }, s);
    }
    h += rows;
  }
  // hush: dim
  if (t > T.hush[0]) h += box(0, 0, W, H, { background: `rgba(0,0,0,${0.55 * pr(t, T.hush[0], T.hush[1])})` });
  return h;
}
function reportScreen(t) {
  let h = box(0, 0, W, H, { background: '#000' }) + statusBar(true);
  const a = k => `opacity:${clamp(k)};transform:translateY(${(1 - eo(clamp(k))) * 30}px)`;
  h += `<div class="abs" style="left:318px;top:120px;${a(pr(t, T.report, T.report + 0.3))}">${logo(200, 'gr')}</div>`;
  h += txt(0, 300, W, { font: 'italic 400 104px Anton', textAlign: 'center', letterSpacing: '-1px' }, `<span class="gtext" style="display:inline-block;transform:skewX(-8deg)">VIBE CHECK</span>`);
  h += txt(0, 446, W, { font: '400 50px Bebas', color: '#ff2e88', textAlign: 'center', letterSpacing: '2px' }, '412 MESSAGES ANALYZED');
  h += txt(0, 510, W, { font: '400 40px Bebas', color: '#b44cf0', textAlign: 'center', letterSpacing: '5px', textShadow: '0 0 14px rgba(180,76,240,.8)' }, 'WEEK 9 OF AN UNDEFINED SITUATIONSHIP.');
  // interest level card
  const n = Math.round(62 * eo(pr(t, T.count[0], T.count[1])));
  const ic = pr(t, T.report + 0.2, T.report + 0.6);
  h += `<div class="abs" style="left:40px;top:${640}px;width:756px;height:520px;border-radius:40px;background:radial-gradient(500px 300px at 50% 50%,#3a0a2a,#14060f);${a(ic)}">` +
    box(218, 40, 320, 84, { border: '4px solid #ff2e88', borderRadius: '42px', font: '400 40px Bebas', color: '#fff', textAlign: 'center', lineHeight: '78px', letterSpacing: '3px', boxShadow: '0 0 20px rgba(255,46,136,.5)', background: '#000' }, 'INTEREST LEVEL') +
    txt(0, 140, 756, { font: '400 230px Bebas', color: 'transparent', WebkitTextStroke: '6px #ff2e88', textAlign: 'center', lineHeight: 1, textShadow: `0 0 ${30 + (t > T.count[1] ? 20 * Math.max(0, 1 - (t - T.count[1]) * 2) : 0)}px rgba(255,46,136,.8)` }, String(n)) +
    box(96, 386, 564, 24, { background: '#2a1a24', borderRadius: '12px', overflow: 'hidden' }, box(0, 0, 564 * n / 100, 24, { background: 'linear-gradient(90deg,#d0104a,#c02ee0,#9a3cf0)', borderRadius: '12px' })) +
    txt(0, 440, 756, { font: '400 48px Bebas', color: '#ff2e88', textAlign: 'center', letterSpacing: '8px', opacity: pr(t, T.count[1], T.count[1] + 0.3) }, 'LUKEWARM AFFECTION') + '</div>';
  // quote card
  const qk = pr(t, T.quote, T.quote + 0.35);
  h += `<div class="abs" style="left:40px;top:1190px;width:756px;height:250px;border-radius:40px;background:linear-gradient(135deg,#2a1240,#1a0f2e);opacity:${clamp(qk * 2)};transform:scale(${lerp(1.25, 1, eo(qk))});transform-origin:50% 50%">` +
    txt(50, 50, 656, { font: 'italic 400 54px Anton', color: '#fff', textAlign: 'center', lineHeight: 1.15, transform: 'skewX(-6deg)' }, '“THEY WANT THE FEELING, NOT THE RESPONSIBILITY.”') + '</div>';
  // spotlight vignette during the freeze
  const sp = pr(t, 12.0, 12.6) * (1 - pr(t, 13.4, 14.0));
  if (sp > 0) h += box(0, 0, W, H, { background: `radial-gradient(520px 420px at 50% 52%,transparent 60%,rgba(0,0,0,${0.75 * sp}) 100%)` });
  return h;
}
function doctorScreen(t) {
  let h = box(0, 0, W, H, { background: '#0e0d12' }) + statusBar(true);
  h += txt(40, 120, 760, { font: '500 28px JBM', color: '#a8a3b8', letterSpacing: '6px' }, '<span style="color:#8a5cf5;font-size:40px">03</span>&nbsp;&nbsp;DOCTOR DELULU');
  const ub = (y, s, k) => box(W - 40 - Math.min(620, 120 + s.length * 17), y + (1 - eo(clamp(k))) * 40, Math.min(620, 120 + s.length * 17), 'auto', { background: 'linear-gradient(90deg,#c02ee0,#7a4cf0 55%,#3b63f0)', borderRadius: '34px', padding: '24px 34px', font: '400 34px Inter', color: '#fff', lineHeight: 1.3, opacity: clamp(k * 3) }, s);
  const db = (y, s, k) => box(40, y + (1 - eo(clamp(k))) * 40, 72, 60, { opacity: clamp(k * 3) }, logo(64, 'gd' + y)) + box(124, y + (1 - eo(clamp(k))) * 40 - 20, 600, 'auto', { background: '#1a1922', border: '1px solid #2c2838', borderRadius: '34px', padding: '24px 34px', font: '400 34px Inter', color: '#fff', lineHeight: 1.3, opacity: clamp(k * 3) }, s);
  const sc = lerp(0, 240, eio(pr(t, 17.2, 18.8)));
  h += `<div class="abs" style="left:0;top:${-sc}px;width:${W}px;height:${H + 400}px">`;
  h += txt(40, 190, 760, { font: '800 74px &quot;Inter Tight&quot;', color: '#fff', letterSpacing: '-3px', lineHeight: 1, opacity: 1 - pr(t, 17.2, 18.2) }, 'Doctor Delulu<br>read everything.<br>Now ask anything.');
  h += ub(470, 'He went quiet for 3 days and then sent a meme. What do I do?', 1);
  h += db(700, 'A meme after three days is a check-in. Don’t answer it like an apology.', pr(t, T.doctor + 0.2, T.doctor + 0.5));
  h += ub(940, 'So I ignore him?', pr(t, T.ask, T.ask + 0.3));
  h += db(1110, 'Reply when you have something to say, not when he tugs the line.', pr(t, T.rep1, T.rep1 + 0.3));
  h += db(1350, 'Next time he reappears, let him make the plan.', pr(t, T.rep2, T.rep2 + 0.3));
  h += '</div>';
  h += box(30, 1500, 776, 96, { background: '#17161d', border: '1px solid #2c2838', borderRadius: '48px', font: '400 32px Inter', color: '#6f6a80', padding: '28px 40px' }, 'Ask Doctor Delulu anything…');
  return h;
}
const SUGG1 = ['Took you long enough 😅 what did you have in mind?', 'A meme after 3 days? Bold. Free Saturday — your plan 😌', 'lol hi stranger. If you wanna hang, make it a plan, not a meme.'];
const SUGG2 = ['Haha hey stranger 🙂 free Saturday if you want to make a plan', 'Ha, hi. Busy week. What’s the plan?', 'lol good meme. Saturday works if you’re asking.'];
function keyboardScreen(t) {
  const pick = t >= T.pick + 0.05, sent = pr(t, T.send, T.send + 0.45);
  const typed = pick && t < T.send ? SUGG2[0].slice(0, Math.round(SUGG2[0].length * pr(t, T.pick + 0.05, T.pick + 0.45))) : '';
  let h = chatScreen(t, { sub: 'online', yo: -520 - 170 * eo(sent), memeK: 1, inputY: 760, typed, caret: pick && t < T.send, sent, sentText: SUGG2[0] });
  // keyboard panel
  const ky = lerp(H, 870, eo(pr(t, T.kbd, T.kbd + 0.45)));
  const chip = (x, w, label, on, col) => box(x, 20, w, 70, { borderRadius: '35px', background: on ? 'linear-gradient(90deg,#c02ee0,#7a4cf0 55%,#3b63f0)' : '#fff', border: on ? 'none' : `2px solid ${col}55`, font: '400 34px Bebas', letterSpacing: '1px', color: on ? '#fff' : col, textAlign: 'center', lineHeight: on ? '70px' : '66px', boxShadow: on ? '0 6px 20px rgba(122,76,240,.45)' : 'none' }, label);
  const god = t >= T.god;
  let k = box(0, 0, W, 112, { background: '#ecebf0', borderBottom: '1px solid #ddd' },
    box(18, 22, 74, 66, {}, logo(70, 'gk')) + chip(104, 196, '✦ GOD MODE', god, '#7a4cf0') + chip(314, 180, '✍ COMPOSE', false, '#a03cc0') + chip(508, 150, '⚡ REPLY', false, '#2a9a7a') + chip(672, 190, '🔮 PSYCHIC', false, '#c03cb0'));
  k += box(0, 112, W, 800, { background: '#f2f1f5' });
  const cook = t >= T.cook[0] && t < T.sugg;
  if (cook) {
    const pu = 1 + 0.05 * Math.sin(t * 8);
    k += box(338, 250, 160, 160, { borderRadius: '50%', background: '#fff', boxShadow: `0 0 ${50 * pu}px rgba(192,46,224,.5)`, transform: `scale(${pu})`, paddingTop: '30px', paddingLeft: '22px' }, logo(116, 'gc'));
    k += txt(0, 450, W, { font: 'italic 400 40px Kalam, Inter', color: '#555', textAlign: 'center', fontFamily: 'Inter', fontStyle: 'italic' }, 'cooking your messages' + '.'.repeat(1 + Math.floor(t * 3) % 3));
  }
  if (t >= T.sugg) {
    const S = t >= T.chill + 0.2 ? SUGG2 : SUGG1, sh = t >= T.chill && t < T.chill + 0.4 ? 0.4 : 1;
    k += txt(30, 150, 400, { font: '400 30px Bebas', color: '#7a4cf0', letterSpacing: '2px' }, '✦ GOD MODE');
    S.forEach((s, i) => { const kk = pr(t, T.sugg + i * 0.12, T.sugg + i * 0.12 + 0.3);
      const sel = pick && i === 0;
      k += box(26, 200 + i * 150, 784, 130, { background: '#fff', borderRadius: '26px', border: sel ? '3px solid #c02ee0' : '1px solid #e2e0ea', padding: '20px 70px 0 28px', font: '400 31px Inter', color: '#222', lineHeight: 1.3, opacity: clamp(kk * 3) * sh, transform: `translateY(${(1 - eo(kk)) * 30}px)`, boxShadow: sel ? '0 0 20px rgba(192,46,224,.3)' : 'none' }, s + `<span style="position:absolute;right:26px;top:36px;color:#c02ee0;font-size:36px">↑</span>`); });
  }
  const tones = [['😂 FUNNY', 168], ['😏 FLIRTY', 168], ['💀 SAVAGE', 176], ['🥰 SWEET', 158], ['🌊 CHILL', 150]];
  let tx = 20;
  tones.forEach(([l, w]) => { const on = l.includes('CHILL') && t >= T.chill; k += box(tx, 680, w - 10, 66, { borderRadius: '33px', background: on ? '#e4f3ff' : '#fff', border: on ? '3px solid #3b8ef0' : '1px solid #ddd', font: '400 30px Bebas', color: '#333', textAlign: 'center', lineHeight: on ? '60px' : '64px' }, l); tx += w; });
  h += box(0, ky, W, H - 870, {}, k);
  return h;
}
function endScreen(t) {
  let h = box(0, 0, W, H, { background: 'radial-gradient(900px 800px at 50% 30%,#2a0f2e,#0b0a10 70%)' }) + statusBar(true);
  const a = k => `opacity:${clamp(k * 2)};transform:translateY(${(1 - eo(clamp(k))) * 40}px)`;
  h += `<div class="abs" style="left:56px;top:300px;width:740px;font:800 104px 'Inter Tight';letter-spacing:-5px;line-height:.98;color:#fff;${a(pr(t, T.end + 0.3, T.end + 0.8))}">Your friends are too nice to tell you.</div>`;
  h += `<div class="abs" style="left:56px;top:${300 + 412}px;width:740px;font:800 104px 'Inter Tight';letter-spacing:-5px;line-height:.98;color:#7d7590;${a(pr(t, T.line2, T.line2 + 0.5))}">Your chat already did.</div>`;
  const lk = pr(t, T.logo, T.logo + 0.4);
  h += `<div class="abs" style="left:56px;top:1080px;${a(lk)}">${logo(120, 'ge')}</div>` + txt(196, 1100, 600, { font: '700 64px &quot;Inter Tight&quot;', color: '#fff', letterSpacing: '-2px', opacity: clamp(lk * 2) }, 'Delulu Check');
  const ck = pr(t, T.cta, T.cta + 0.35), press = t > T.click && t < T.click + 0.2 ? 0.95 : 1;
  h += box(56, 1270, 724, 136, { borderRadius: '68px', background: 'linear-gradient(90deg,#c02ee0,#7a4cf0 55%,#3b63f0)', font: '400 66px Bebas', color: '#fff', letterSpacing: '4px', textAlign: 'center', lineHeight: '136px', boxShadow: `0 10px ${40 + (t > T.click ? 30 : 0)}px rgba(192,46,224,.55)`, opacity: clamp(ck * 2), transform: `scale(${lerp(0.9, 1, eo(ck)) * press})` }, 'GET THE APP &nbsp;→');
  h += txt(56, 1440, 740, { font: '500 26px JBM', color: '#a8a3b8', letterSpacing: '3px', opacity: pr(t, 28.6, 29.0), lineHeight: 1.6 }, '<span style="color:#22c58a">●</span> 50,000+ PEOPLE · FREE PREVIEW<br>&nbsp;&nbsp;&nbsp;ON YOUR FIRST CHAT');
  return h;
}

// —— which screen
function screenAt(t) {
  if (t < T.whip[0] + 0.2) { let h = chatScreen(t, { memeK: pr(t, T.meme, T.meme + 0.35), typed: t > T.type0 && t < T.type0 + 1.5 ? typedHook(t) : '', caret: t > T.type0 && t < T.type0 + 1.5 }); if (t > T.sheet) h += shareSheet(pr(t, T.sheet, T.sheet + 0.4), pr(t, T.tapDC, T.tapDC + 0.4)); return h; }
  if (t < T.report) return appScreen(t);
  if (t < T.doctor) return reportScreen(t);
  if (t < T.kbd) return doctorScreen(t);
  if (t < T.end) return keyboardScreen(t);
  return endScreen(t);
}
function typedHook(t) { const s = 'omg hiii did u', u = t - T.type0; if (u < 0.75) return s.slice(0, Math.round(s.length * u / 0.75)); return s.slice(0, Math.max(0, Math.round(s.length * (1 - (u - 0.9) / 0.5)))); }
// screen transitions: whip (horizontal slide + blur), and short slides between chapters
function transition(t) {
  const cuts = [[T.whip[0], T.whip[1], 'whip'], [T.report - 0.25, T.report + 0.2, 'up'], [T.doctor - 0.2, T.doctor + 0.2, 'up'], [T.kbd - 0.2, T.kbd + 0.2, 'up'], [T.end - 0.2, T.end + 0.25, 'up']];
  for (const [a, b, k] of cuts) if (t >= a && t < b) { const u = eio(pr(t, a, b)), m = (a + b) / 2; return { k, u, a, b, m }; }
  return null;
}

// —— mascot
function deluAt(t) {
  const S = (x, y) => [SX + x, SY + y];
  if (t >= T.born && t < T.report) {
    const k = pr(t, T.born, T.born + 0.35);
    if (t < T.read[0]) { const y = 270 - 120 * Math.sin(k * Math.PI); return { p: S(120, y), sq: t > T.born + 0.33 ? 0.85 : 1.1, burst: pr(t, T.born, T.born + 0.5) }; }
    // runs along the scrolling rows, hopping row to row
    const u = t - T.read[0], hop = Math.floor(u / 0.5), ph = (u % 0.5) / 0.5;
    const x = 140 + ((hop % 4) * 170) + ph * 170 * (hop % 8 < 4 ? 1 : -1) * 0.5;
    return { p: S(Math.min(760, Math.max(80, x)), 760 - Math.sin(ph * Math.PI) * 80), flip: hop % 8 >= 4, sq: ph > 0.92 ? 0.85 : 1, look: 1 };
  }
  if (t >= T.report && t < T.doctor) { // on top of the interest card, cheering when it hits 62
    const k = pr(t, T.report + 0.3, T.report + 0.8); if (k <= 0) return null;
    const cheer = t > T.count[1] && t < T.count[1] + 1.2, hop = cheer ? Math.abs(Math.sin((t - T.count[1]) * 9)) * 50 : 0;
    return { p: S(520, 680 - hop - (1 - eo(k)) * 300), arms: cheer, happy: cheer, sq: 1 };
  }
  if (t >= T.doctor && t < T.kbd) { const k = pr(t, T.rep1, T.rep1 + 0.4); if (k <= 0) return null; const sc = lerp(0, 240, eio(pr(t, 17.2, 18.8)));
    return { p: S(220, 1090 - sc - (1 - eo(k)) * 200), sq: t < T.rep1 + 0.5 && t > T.rep1 + 0.38 ? 0.8 : 1, look: -1 }; }
  if (t >= T.kbd && t < T.end) {
    if (t < T.send) { const k = pr(t, T.sugg, T.sugg + 0.4); if (k <= 0) return null; return { p: S(754, 760 - (1 - eo(k)) * 160), sq: 1, look: -1 }; }
    const k = pr(t, T.send, T.send + 0.45); return { p: S(700, 580 + (1 - eo(k)) * 130 - Math.sin(k * Math.PI) * 60), sq: 1, happy: true };
  }
  if (t >= T.end) { const k = pr(t, T.click - 0.25, T.click + 0.1); if (k <= 0) return null; const y = lerp(800, 1270, eo(k));
    return { p: S(640, t < T.click + 0.1 ? y : 1270 - Math.abs(Math.sin((t - T.click) * 7)) * 40 * Math.max(0, 1 - (t - T.click))), happy: t > T.click, arms: t > T.click, sq: t > T.click + 0.08 && t < T.click + 0.18 ? 0.8 : 1 }; }
  return null;
}
// —— cursor keyframes (screen-local): [t, x, y, click]
const CUR = [[3.6, 900, 1500, 0], [4.6, 640, 1150, 0], [T.tapDC, 640, 1150, 1], [5.4, 700, 1300, 0],
  [19.5, 760, 1400, 0], [T.god - 0.05, 200, 925, 0], [T.god, 200, 925, 1], [T.chill - 0.4, 760, 1580, 0], [T.chill, 760, 1580, 1], [T.pick - 0.3, 420, 1140, 0], [T.pick, 420, 1140, 1],
  [T.send - 0.3, 754, 800, 0], [T.send, 754, 800, 1], [24.8, 780, 900, 0], [27.9, 640, 1500, 0], [T.click, 420, 1338, 1], [30, 430, 1360, 0]];
function cursorAt(t) {
  if (t < CUR[0][0] - 0.3 || (t > 5.5 && t < 19.5) || (t > 24.9 && t < 27.6)) return null;
  let i = 0; while (i < CUR.length - 1 && t > CUR[i + 1][0]) i++;
  const a = CUR[i], b = CUR[Math.min(i + 1, CUR.length - 1)];
  const u = b[0] > a[0] ? eio(clamp((t - a[0]) / (b[0] - a[0]))) : 1;
  let x = lerp(a[1], b[1], u), y = lerp(a[2], b[2], u);
  let ring = 0, sc = 1; for (const c of CUR) if (c[3] && t >= c[0] && t < c[0] + 0.4) { ring = (t - c[0]) / 0.4; sc = t < c[0] + 0.12 ? 0.85 : 1; }
  return { x: SX + x, y: SY + y, ring, sc };
}

// —— render one frame into #world / #hud
export function render(t, world, hud) {
  const [cx, cy, z] = cam(t);
  world.style.transform = `translate(540px,960px) scale(${z}) translate(${-cx}px,${-cy}px)`;
  const tr = transition(t);
  let scr = screenAt(t), tf = '', filt = '';
  if (tr) {
    if (tr.k === 'whip') { const before = t < tr.m; tf = `translateX(${before ? -tr.u * 836 * 2 * 0.5 : (1 - tr.u) * 836}px)`; filt = `blur(${Math.sin(tr.u * Math.PI) * 26}px)`; }
    else { const before = t < tr.m; tf = `translateY(${before ? -tr.u * 140 : (1 - tr.u) * 140}px)`; filt = `blur(${Math.sin(tr.u * Math.PI) * 14}px)`; }
  }
  let h = `<div class="phone"><div class="screen"><div class="abs" style="left:0;top:0;width:${W}px;height:${H}px;transform:${tf || 'none'};filter:${filt || 'none'}">${scr}</div><div class="island"></div></div></div>`;
  // mascot + fx (world coords)
  const D = deluAt(t);
  if (D && !D.hide) {
    const [x, y] = D.p; h += delu(x, y, 9, { flip: D.flip, sq: D.sq, happy: D.happy, arms: D.arms, blink: Math.floor(t * 10) % 37 === 0 });
    if (D.burst > 0 && D.burst < 1) h += sparks(SX + 120 + 40, SY + 330, D.burst, 12, '#ffc928', 20, 140, 10);
  }
  if (t > T.count[1] && t < T.count[1] + 0.7) h += sparks(540, SY + 640 + 270, pr(t, T.count[1], T.count[1] + 0.7), 14, '#ffc928', 120, 380, 12);
  if (t > T.click && t < T.click + 0.6) h += sparks(SX + 418, SY + 1338, pr(t, T.click, T.click + 0.6), 12, '#ffc928', 60, 260, 12);
  const cu = cursorAt(t);
  if (cu) { if (cu.ring > 0) h += `<div class="abs" style="left:${cu.x - 34 * cu.ring - 6}px;top:${cu.y - 34 * cu.ring - 6}px;width:${68 * cu.ring + 12}px;height:${68 * cu.ring + 12}px;border-radius:50%;border:${4 / z}px solid rgba(255,255,255,${(1 - cu.ring) * 0.9})"></div>`; h += cursorSvg(cu.x, cu.y, cu.sc, 1); }
  world.innerHTML = h;
  // HUD: caption pill (v7 is on screen as the title, so no pill)
  const S = SUBS.find(s => t >= s.t0 && t < s.t1 && !s.text.startsWith('Your friends'));
  let hh = '';
  if (S) { const k = pr(t, S.t0, S.t0 + 0.2), out = pr(t, S.t1 - 0.15, S.t1);
    hh += `<div class="abs" style="left:60px;width:960px;top:1790px;text-align:center;opacity:${k * (1 - out)}"><span style="display:inline-block;padding:18px 34px;border-radius:40px;background:rgba(20,14,28,.62);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.12);font:600 42px Inter;color:#fff;letter-spacing:-.5px;line-height:1.25">${S.text}</span></div>`; }
  hud.innerHTML = hh;
}
export const TEXTS = t => [];
