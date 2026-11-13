# Build storyboard.jpg from real rendered frames:  python3 -I art/storyboard.py <snapshot_dir>
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
d = sys.argv[1]
BEATS = [
    ('0:00', 'JO', "So I'm class rep this year…"),
    ('0:03', 'JO', "…which apparently means I'm doing the teacher gift."),
    ('0:05', 'JO', "I pop a message in the class WhatsApp. Five quid each for Miss Clarke."),
    ('0:09', 'DAD / MUM / MUM 2', "Can I give it you Friday? · Is it five or ten? · Ooh, we've already got her something!"),
    ('0:15', 'JO', "Eleven thumbs-up. Zero fivers."),
    ('0:18', 'JO', "Three weeks of 'just a gentle reminder'."),
    ('0:21', 'JO', "A sandwich bag of coins at the gate."),
    ('0:24', 'JO', "And I'm still forty quid short… so guess who's topping it up."),
    ('0:27', 'JO  (yellow tear)', "Next year? One Collection Pot, one link… and I'm putting the kettle on."),
    ('0:31', 'VO', "Collection Pot. Easy to sort. Impossible to forget."),
]
frames = sorted(glob.glob(os.path.join(d, 'frame-*.png')))[:len(BEATS)]
FW, FH, PAD, CAP = 400, 711, 28, 190
cols = 5; rows = (len(frames) + cols - 1) // cols
W = cols * FW + (cols + 1) * PAD; H = 150 + rows * (FH + CAP + PAD) + PAD
sheet = Image.new('RGB', (W, H), (255, 252, 248))
dr = ImageDraw.Draw(sheet)
F = '/usr/share/fonts/opentype/inter/'
title = ImageFont.truetype(F + 'Inter-Bold.otf', 52); sub = ImageFont.truetype(F + 'Inter-Medium.otf', 26)
tc = ImageFont.truetype(F + 'Inter-Bold.otf', 24); body = ImageFont.truetype(F + 'Inter-Regular.otf', 22)
INK, GOLD = (47, 47, 50), (249, 185, 16)
dr.text((PAD, 34), 'Class Rep · Collection Pot · storyboard', font=title, fill=INK)
dr.text((PAD, 100), '9:16 · ~35 s · real frames from the animated build (timings approximate until the voice is recorded)', font=sub, fill=(110, 110, 115))
def wrap(t, f, w):
    out, line = [], ''
    for word in t.split():
        test = (line + ' ' + word).strip()
        if dr.textlength(test, font=f) > w and line: out.append(line); line = word
        else: line = test
    return out + [line]
for k, fp in enumerate(frames):
    r, c = divmod(k, cols)
    x = PAD + c * (FW + PAD); y = 150 + r * (FH + CAP + PAD)
    im = Image.open(fp).convert('RGB').resize((FW, FH), Image.LANCZOS)
    sheet.paste(im, (x, y)); dr.rectangle([x - 1, y - 1, x + FW, y + FH], outline=(220, 214, 204))
    t, who, line = BEATS[k]
    dr.rounded_rectangle([x, y + FH + 14, x + 80, y + FH + 48], 17, fill=GOLD)
    dr.text((x + 14, y + FH + 18), t, font=tc, fill=INK)
    dr.text((x + 94, y + FH + 18), who, font=tc, fill=INK)
    for i, l in enumerate(wrap('“' + line + '”', body, FW)[:4]):
        dr.text((x, y + FH + 60 + i * 30), l, font=body, fill=INK)
sheet.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'storyboard.jpg'), quality=88)
print(W, H)
