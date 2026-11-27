"""Generates the LOOT brand graphics used in the film (deterministic).
brand/slash.svg  - the mint torn-paper slash (horizontal; rotate in CSS)
brand/bag.svg    - the flat mint money-bag icon
Run: python3 tools/gen_brand.py"""
import math, random, os
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rnd = random.Random(7)
MINT, PAPER = "#98FF98", "#FBFBF8"
L, H, T = 2000, 300, 70          # length, viewBox height, max half-thickness
c = H / 2

def profile(x):                  # thick in the middle, tapers to points
    s = math.sin(math.pi * x / L)
    return T * (s ** 0.9)

def edge(sign, extra):
    pts, wob = [], 0.0
    for i in range(0, L + 1, 6):
        wob = wob * 0.82 + rnd.uniform(-1, 1) * 2.2          # low-freq wobble
        jag = rnd.uniform(0, 1) ** 2 * 7                      # torn fibres
        t = profile(i)
        k = min(1, t / 12)
        pts.append((i, c + sign * (t + (wob + jag) * k + extra * k * (0.6 + rnd.uniform(0, .8)))))
    return pts

def poly(top, bot):
    p = top + bot[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in p) + "Z"

core = poly(edge(-1, 0), edge(1, 0))
rnd.seed(11)
fringe = poly(edge(-1, 9), edge(1, 9))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" preserveAspectRatio="none">
<path d="{fringe}" fill="#000" opacity=".10" transform="translate(4,9)"/>
<path d="{fringe}" fill="{PAPER}"/>
<path d="{core}" fill="{MINT}"/>
</svg>'''
open(os.path.join(here, "brand/slash.svg"), "w").write(svg)

bag = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 220">
<path d="M64 14 L88 34 L100 16 L112 34 L136 14 L126 60 L74 60 Z" fill="{MINT}"/>
<rect x="70" y="58" width="60" height="18" rx="8" fill="{MINT}"/>
<path d="M78 80 C30 100 14 168 34 196 C44 210 62 214 100 214 C138 214 156 210 166 196 C186 168 170 100 122 80 Z" fill="{MINT}"/>
<path d="M100 104 v94 M120 126 c-4-10-12-14-22-14 c-12 0-20 6-20 16 c0 22 44 12 44 36 c0 10-10 18-24 18 c-12 0-20-5-24-15" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round"/>
</svg>'''
open(os.path.join(here, "brand/bag.svg"), "w").write(bag)
print("ok")

# ---- torn wipe panels ----
def jag_line(n_pts, length, amp, seed):
    r = random.Random(seed); pts = []; wob = 0.0
    for i in range(n_pts + 1):
        wob = wob * 0.8 + r.uniform(-1, 1) * amp * 0.35
        pts.append((i * length / n_pts, wob + (r.uniform(0, 1) ** 2) * amp))
    return pts
def panel(color, W, Hh, edge_axis, name, fringe=10):
    # band of size W x Hh; torn on the two edges perpendicular to edge_axis ('x' = left/right torn)
    if edge_axis == 'x':
        L1 = jag_line(220, Hh, 12, 3); L2 = jag_line(220, Hh, 12, 5)
        left = [(40 + d, y) for y, d in L1]; right = [(W - 40 - d, y) for y, d in L2][::-1]
        lf = [(40 + d - fringe * (0.5 + random.Random(int(y)).random()), y) for y, d in L1]
        rf = [(W - 40 - d + fringe * (0.5 + random.Random(int(y) + 7).random()), y) for y, d in L2][::-1]
    else:
        L1 = jag_line(220, W, 12, 3); L2 = jag_line(220, W, 12, 5)
        left = [(x, 40 + d) for x, d in L1]; right = [(x, Hh - 40 - d) for x, d in L2][::-1]
        lf = [(x, 40 + d - fringe * (0.5 + random.Random(int(x)).random())) for x, d in L1]
        rf = [(x, Hh - 40 - d + fringe * (0.5 + random.Random(int(x) + 7).random())) for x, d in L2][::-1]
    P = lambda pts: "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" preserveAspectRatio="none">
<path d="{P(lf + rf)}" fill="{PAPER}"/><path d="{P(left + right)}" fill="{color}"/></svg>'''
    open(os.path.join(here, f"brand/{name}.svg"), "w").write(s)
panel(MINT, 1500, 2800, 'x', 'tear_mint')
panel("#7B7D9E", 1400, 2400, 'y', 'tear_slate', fringe=12)
print("panels ok")
