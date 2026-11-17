# Storyboard sheet from real HyperFrames snapshots.
# Usage (from the project folder):
#   npx hyperframes snapshot --at 4.9,11.9,17.9,21.1,28.9,35.2,42.7,47.2,50.3,57.0,62.3
#   python3 -I art/storyboard.py <snapshot-dir> storyboard.jpg
import sys, glob, textwrap
from PIL import Image, ImageDraw, ImageFont

snap, out = sys.argv[1], sys.argv[2]
ROWS = [
    ("0:00", "Narrator", "This is Siddhartha. 2,500 years ago, he was born a prince in the Himalayan foothills."),
    ("0:05", "Narrator", "His father wanted him to be king, so he kept him in the palace, away from anything sad."),
    ("0:12", "Narrator", "At 29, he finally stepped outside. He saw an old man. A sick man. A dead body."),
    ("0:18", "Channa", "This happens to everyone, my prince. Even you."),
    ("0:21", "Narrator", "That night, he left it all, even his wife and newborn son, to find out why we suffer, and how to stop."),
    ("0:29", "Narrator", "For six years he barely ate, hoping it would bring answers. It almost killed him."),
    ("0:35", "Narrator", "Then a woman named Sujata brought him rice and milk. He ate, and realised: starving wasn't the answer either."),
    ("0:43", "Narrator", "So he sat under a tree at Bodh Gaya, and made a promise."),
    ("0:47", "Siddhartha", "I will not get up until I understand."),
    ("0:50", "Narrator", "By sunrise, he understood. We suffer because we always want more. Let go of that, and suffering ends."),
    ("0:57", "Narrator", "From that day, people called him the Buddha: the one who woke up."),
]
frames = sorted(glob.glob(f"{snap}/frame-*.png"))
assert len(frames) == len(ROWS), (len(frames), len(ROWS))

FW, FH, M, CAP, COLS = 405, 720, 30, 220, 4
HEAD = 170
rows = (len(ROWS) + 1 + COLS - 1) // COLS
W = COLS * FW + (COLS + 1) * M
H = HEAD + rows * (FH + CAP + M) + M
ink, paper, yel = (47, 47, 50), (255, 252, 248), (249, 185, 16)
im = Image.new("RGB", (W, H), paper); d = ImageDraw.Draw(im)
F = "/usr/share/fonts/truetype/dejavu/"
ft = ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", 64)
fs = ImageFont.truetype(F + "DejaVuSans.ttf", 26)
fb = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 24)
fl = ImageFont.truetype(F + "DejaVuSans.ttf", 22)
d.text((M, 40), "The Prince Who Walked Away", font=ft, fill=ink)
d.text((M, 120), "Storyboard · 9:16 · ~62 s · real frames from index.html (timings before voice-over)", font=fs, fill=ink)
for k, (f, (t, who, line)) in enumerate(zip(frames, ROWS)):
    r, c = divmod(k, COLS)
    x = M + c * (FW + M); y = HEAD + r * (FH + CAP + M)
    fr = Image.open(f).convert("RGB").resize((FW, FH), Image.LANCZOS)
    im.paste(fr, (x, y)); d.rectangle([x - 1, y - 1, x + FW, y + FH], outline=ink, width=2)
    tag = f"{k + 1}  ·  {t}  ·  {who}"
    tw = d.textlength(tag, font=fb)
    d.rectangle([x, y + FH + 12, x + tw + 20, y + FH + 48], fill=yel)
    d.text((x + 10, y + FH + 16), tag, font=fb, fill=ink)
    for i, ln in enumerate(textwrap.wrap(f"“{line}”", 31)[:5]):
        d.text((x, y + FH + 60 + i * 30), ln, font=fl, fill=ink)
# legend cell
k = len(ROWS); r, c = divmod(k, COLS); x = M + c * (FW + M); y = HEAD + r * (FH + CAP + M)
d.rectangle([x, y, x + FW, y + FH], outline=ink, width=2)
legend = ["Look: newspaper collage,", "halftone cut-outs duotoned", "charcoal → cream,", "one gold/saffron accent", "(earrings, bowl, robe, sun).", "",
          "Turn: gold paper tear", "into sunrise (frame 10).", "", "Voices: George (narrator),", "Channa + Siddhartha", "(one line each).", "",
          "Art: Higgsfield", "(Nano Banana Pro),", "cut out on Higgsfield."]
for i, ln in enumerate(legend):
    d.text((x + 24, y + 30 + i * 36), ln, font=fs, fill=ink)
im.save(out, quality=88); print(out, im.size)
