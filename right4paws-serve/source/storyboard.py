"""Storyboard sheet: python storyboard.py out.jpg frames_dir  (frames t_<time>.jpg rendered by core/render/still.mjs)"""
import sys, textwrap
from PIL import Image, ImageDraw, ImageFont
out, d = sys.argv[1], sys.argv[2]
F = lambda w, s: ImageFont.truetype('fonts/Jost.ttf', s) if w == 'j' else ImageFont.truetype('fonts/AlfaSlabOne-Regular.ttf', s)
SHOTS = [
  ('0.3',  '1', '0:00–0:04', 'Medium, low angle · slow push', 'Mango drops his empty bowl (clang). The pack thumps down beside it.', '“This is Mango. And this… is dinner.”'),
  ('7.2',  '2', '0:04–0:08', 'Full card · wipe up', 'Red title card: HOW TO SERVE · Ultimate Diet. Medallions 1 · 2 · 3 stamp on the beat.', '“Here’s how to serve it, in three easy steps.”'),
  ('13.6', '3', '0:08–0:16', 'Medium + call-out · iris through medallion 1', 'Mango hops on the scale. Needle swings… silence… settles on 30 kg (ding).', '“Step one. Weigh your dog. Thirty kilos? Around 350 grams a day.”'),
  ('19.9', '4', '0:16–0:22', 'Insert on hands · side wipe', 'A hand scoops a cup from the open pack; a finger flicks it level. Call-out: 250 ml ≈ 100 g.', '“Step two. Measure it out. One cup holds about 100 grams.”'),
  ('27.4', '5', '0:22–0:30', 'Split frame ×3 (signature)', 'Three panels light up on the beat: dry from the pack · warm water + steam · mashed with a fork.', '“Step three. Serve it your way. Dry… sprinkle on warm water… or mash it.”'),
  ('31.0', '6', '0:30–0:32', 'Medium close · dead still', 'Total silence. Mango waits perfectly still as the bowl comes down… clink.', '(silence)'),
  ('32.9', '7', '0:32–0:34', 'Medium · slow push', 'Mango dives in. CRUNCH! Tail going like a metronome.', '(crunch, music back up a step)'),
  ('35.4', '8', '0:34–0:36', 'Card · side wipe', 'Pro tip card: kibble bowl vs Right4Paws bowl, arrow, “25–30% less per bowl”.', '“Pro tip: it’s more nutrient-dense than kibble, so you’ll feed less.”'),
  ('40.6', '9', '0:36–0:42', 'Wide · wipe up · dead still 3 s', 'The brand’s own cover: logo tab, ULTIMATE DIET, pack + Mango on the checker floor, right4paws.com.', '“Right4Paws Ultimate Diet. Raw, made right.”'),
]
cols, fw, fh, cap, pad = 3, 400, 711, 210, 28
rows = (len(SHOTS) + cols - 1) // cols
top = 170
Wd, Hd = pad + cols * (fw + pad), top + rows * (fh + cap + pad) + pad
S = Image.new('RGB', (Wd, Hd), (255, 237, 223)); g = ImageDraw.Draw(S)
RED, INK, SOFT = (203, 17, 43), (31, 26, 25), (74, 64, 60)
g.rectangle([0, 0, Wd, 130], fill=RED)
g.text((pad, 26), 'Right4Paws · How to Serve Ultimate Diet', font=F('s', 42), fill=(255, 248, 242))
g.text((pad, 84), 'Storyboard · Mid-century Cartoon in brand colours · 9:16 · ~42 s · cool-jazz combo + 1950s classroom narrator', font=F('j', 24), fill=(255, 248, 242))
for k, (t, n, tc, frame, what, line) in enumerate(SHOTS):
    x, y = pad + (k % cols) * (fw + pad), top + (k // cols) * (fh + cap + pad)
    im = Image.open(f'{d}/t_{t}.jpg').convert('RGB').resize((fw, fh), Image.LANCZOS)
    S.paste(im, (x, y)); g.rectangle([x - 1, y - 1, x + fw, y + fh], outline=INK, width=3)
    g.ellipse([x + 10, y + 10, x + 58, y + 58], fill=RED, outline=INK, width=2); g.text((x + 34, y + 34), n, font=F('s', 28), fill=(255, 248, 242), anchor='mm')
    cy = y + fh + 10
    g.text((x, cy), f'{tc}  ·  {frame}', font=F('j', 19), fill=RED); cy += 30
    for l in textwrap.wrap(what, 42): g.text((x, cy), l, font=F('j', 19), fill=INK); cy += 24
    cy += 4
    for l in textwrap.wrap(line, 40): g.text((x, cy), l, font=ImageFont.truetype('fonts/Jost.ttf', 19), fill=SOFT); cy += 24
S.save(out, quality=90); print(out, S.size)
