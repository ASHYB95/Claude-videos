# Patterns (lifted from `SM explainer/index.html` — copy that file as the starting template)

## Layer order (DOM order = paint order)
```
paperL      newsprint ground (assets/paper.jpg = newsprint duotoned with --contrast 0.75)
S* scenes   full-screen collage scenes, each with its own .bgp ground   ← UNDER the camera
tearL       brand-colour torn-paper wipe                                ← under the camera, so the PiP stays put
camL        #cam > #camclip > #camin > <video> + #ring                  ← NOT timed itself (only <video> has data-start)
P*/F*       overlays on the face (credentials, stamps, headlines)       ← ABOVE the camera
capL        captions
grainL      grain (opacity .08, multiply, steps() jitter)
<audio>     audio/mix.wav (video is muted)
```
Start each collage scene at its tear's midpoint (tearAt(T) covers T-.4 → T+.4) or it hides the previous scene early.

## Camera modes (full screen ↔ PiP circle ↔ taped photo)
`#cam` is 22 px larger than the frame on every side (left/top −22, 1124×1964) so its paper border + torn edge sit
off-screen at full size and show only in photo mode. `#camclip` carries a circle clip-path centred on the speaker
(video space (540,880) = head + shoulders). For PiP centre (cx,cy), screen radius r and scale s, with transform-origin 50% 50%:
`x = cx − 540`, `y = cy − 960 + 80·s`, `clip r_local = r / s`. Reference: cx 240, cy 1310, r 185, s .28 → x −300, y 372, r_local 661.
Full screen: s 1, clip r 1200 (covers every corner from (540,880)).
```js
const CS = {
  face:  { cam: { scale: 1,   x: 0,    y: 0,   rotation: 0,    backgroundColor: 'rgba(243,240,232,0)', boxShadow: '0px 0px 0px 0px rgba(34,32,36,0)' }, r: 1200, ring: 0 },
  pip:   { cam: { scale: .28, x: -300, y: 372, rotation: 0,    backgroundColor: 'rgba(243,240,232,0)', boxShadow: '0px 0px 0px 0px rgba(34,32,36,0)' }, r: 661,  ring: 1 },
  photo: { cam: { scale: .56, x: 0,    y: 290, rotation: -2.5, backgroundColor: 'rgba(243,240,232,1)', boxShadow: '14px 22px 0px 0px rgba(34,32,36,.25)' }, r: 1200, ring: 0 },
  gone:  { cam: { scale: 0,   x: -300, y: 372, rotation: 0,    backgroundColor: 'rgba(243,240,232,0)', boxShadow: '0px 0px 0px 0px rgba(34,32,36,0)' }, r: 661,  ring: 0 },
};
tl.set('#camclip', { clipPath: 'circle(1200px at 540px 880px)' }, 0); tl.set('#cam', CS.face.cam, 0);
let prevMode = 'face';
const camTo = (mode, t, d = .62) => {
  const m = CS[mode], from = prevMode; prevMode = mode;
  if (from === 'pip') tl.to('#ring', { opacity: 0, scale: 1.25, duration: .16, ease: 'power2.in' }, t);
  if (mode === 'gone') { tl.to('#ring', { opacity: 0, scale: 0, duration: .4, ease: 'back.in(2)' }, t); tl.to('#cam', { scale: 0, duration: .4, ease: 'back.in(2)' }, t); return; }
  tl.to('#cam', { ...m.cam, duration: d, ease: 'expo.inOut' }, t);
  tl.to('#camclip', { clipPath: `circle(${m.r}px at 540px 880px)`, duration: d, ease: 'expo.inOut' }, t);
  if (m.ring) tl.fromTo('#ring', { opacity: 0, scale: 1.35 }, { opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)', immediateRender: false }, t + d - .2);
};
// [time, mode] — start each switch ~0.25 s before the line boundary. End: face → pip → gone over the end card.
const MODES = [[3.78, 'pip'], [7.82, 'face'], [10.4, 'photo'], [13.0, 'pip'], /* … */ [84.3, 'pip'], [85.35, 'gone']];
MODES.forEach(([t, m]) => camTo(m, t));
const modeAt = t => { let m = 'face'; for (const [mt, mm] of MODES) if (t >= mt + .3) m = mm; return m; };
// punch-ins on jump cuts (CUTS from data.js) only while full screen; never inside the circle
CUTS.forEach((t, k) => tl.set('#camin', { scale: modeAt(t) === 'face' && k % 2 ? 1.12 : 1.0 }, t));
MODES.forEach(([t, m]) => { if (m !== 'face') tl.set('#camin', { scale: 1.0 }, t + .62); });
```
Ring CSS: `#ring{left:cx−197;top:cy−197;width:394px;height:394px;border-radius:50%;border:12px solid paper;box-shadow:0 0 0 7px brand,9px 14px 0 7px rgba(34,32,36,.25)}`.

## Captions (data.js from scripts/captions.py)
```js
const CAP_HIDE = [[10.5, 13.25]];                // only where a headline says the same words
CAPS.forEach((c, i) => {
  if (hidden(c.t0)) return;
  const r = i % 2 ? 1.6 : -1.8;
  tl.fromTo(`#c${i}`, { opacity: 0, xPercent: -50, scale: .78, rotation: r - 4 }, { opacity: 1, xPercent: -50, scale: 1, rotation: r, duration: .16, ease: 'back.out(2.2)' }, c.t0);
  tl.set(`#c${i}`, { opacity: 0 }, Math.min(c.t1, ...CAP_HIDE.map(h => h[0]).filter(h => h > c.t0)));
  c.w.forEach((w, k) => {
    tl.set(`#c${i}w${k}`, { backgroundColor: BRAND, color: PAPER }, Math.max(c.t0, w[1] - .02));
    if (k < c.w.length - 1) tl.set(`#c${i}w${k}`, { backgroundColor: 'rgba(0,0,0,0)', color: INK }, c.w[k + 1][1] - .02);
  });
});
```
`.cap{left:50%;top:1590px;white-space:nowrap}` `.cap .in{background:paper;padding:18px 30px 16px;font:800 60px/1.05 Montserrat}` + `torn()`.

## Motion helpers
pop (back-ease in from below), slam (scale 1.9 → 1, power4.in, for stamps/counters), draw (SVG `pathLength="1"` +
dashoffset), hl (yellow highlighter = background-size 0 → 100%), scribble (clip-path inset reveal — also use it for
dotted lines, which can't be dash-drawn), push (slow scale on the scene ground), outUp (clear overlays before a
morph), tearAt(T, colour). Ink shapes: curve (arrow), loop (hand-drawn circle), cloud (thought bubble).
Counters: tween a proxy `{v}` with `onUpdate` writing `toLocaleString()`; then `tl.set(el, {textContent:'100,000s'})`.
Torn edges: percentage-based clip-path polygons (pixel ones clip late-loading images).

## Layout zones (1080×1920)
- Face mode: overlays in the sky y≈120–440 (above the head) and on the chest; head usually spans y≈470–1500.
- PiP mode: keep the bottom-left (x<450, y>1100) free for the circle; captions at y≈1540–1640; Instagram's right
  buttons x>960 (y 1050–1650) and bottom text y>1650 — nothing important there. Keep labels 40 px off the edges
  (`white-space:nowrap` labels overflow at the right edge — measure: Montserrat Black ≈ 0.62 em per char).

## Art prompts (Higgsfield nano_banana_pro, 2k)
Sheet: "Vintage newspaper collage clippings: four separate black-and-white halftone photographs printed on aged
newsprint, coarse halftone dots, high contrast, each cut out roughly along its outline with a thin white torn paper
edge, lying flat and well separated with generous empty space between them (not touching, not overlapping) on
crumpled old newspaper pages with faint illegible small print. The four items: …. Grayscale only. No readable text,
no letters, no logos."
People: "three separate … head-and-shoulders portrait photographs … modern urban [Indian] metro-city professionals
in contemporary western clothing: …". Crowd: "eight young modern urban [Indian] people from a big metro city in
contemporary city clothes: oversized t-shirts, denim jackets, hoodies, … looking up and slightly to the right".
Screens for live HTML: "… a hand holding a modern smartphone upright, screen facing the viewer, the screen painted
flat solid yellow #FEC42D" → duotone `--keep-yellow`, find the screen with cv2.minAreaRect on the yellow mask,
overlay an HTML div (scale everything by displayed_width / natural_width; portrait rect angle = cv angle + 90).

## Commands
```
npx --yes hyperframes@0.9.20 snapshot --at 3.6,6.5,10.75      # read the contact sheet before every render
npx --yes hyperframes@0.9.20 render --start 12.6 --end 31.7 --workers 2 --quiet -o renders/batchN.mp4
ffmpeg -i renders/batchN.mp4 -vf scale=540:960 -c:v libx264 -crf 24 -c:a aac -b:a 128k previews/0N-name.mp4
npx --yes hyperframes@0.9.20 render --workers 2 --quiet -o renders/full.mp4      # ~11 min for 87 s (motion blur on)
ffmpeg -i renders/full.mp4 -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 192k -movflags +faststart FINAL.mp4
```
Wait on a background render with `tail --pid=<pid> -f /dev/null` (foreground `sleep` is blocked).
