# Repaint Chip's pupils to match the brand reference (ref/chip-eyes-reference.jpg): large, glossy, slightly
# tilted black ovals with an upper-left highlight, sitting inside the white face. Erases the old pupils by
# inpainting, then draws the new ones (supersampled), clipped to the white face so they never touch the black head.
# Usage: python3 -I fix_eyes.py in.png out.png [--center 0.5] [--scale 1.0]
#   --center: how far to move each pupil toward the middle of its eye area (0 = keep, 1 = fully centred)
import cv2, numpy as np, sys
a = sys.argv[1:]
def opt(name, default):
    if name in a: i = a.index(name); v = float(a[i + 1]); del a[i:i + 2]; return v
    return default
center = opt('--center', 0.0); gscale = opt('--scale', 1.0)
src, dst = a[0], a[1]
img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
rgb, alpha = img[..., :3].copy(), img[..., 3]
H, W = alpha.shape
hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
head = np.zeros((H, W), bool); head[:int(H * 0.62)] = True
white = (hsv[..., 2] > 175) & (hsv[..., 1] < 70) & (alpha > 200) & head
white = cv2.morphologyEx(white.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
# the face: largest white region (eye lobes + cheeks); fill its holes to get the area the pupils live in
n, lab, st, cen = cv2.connectedComponentsWithStats(white)
face_id = 1 + int(np.argmax(st[1:, 4])); face = (lab == face_id).astype(np.uint8)
cnts, _ = cv2.findContours(face, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
face_filled = np.zeros_like(face); cv2.drawContours(face_filled, cnts, -1, 1, -1)
dark = (hsv[..., 2] < 120).astype(np.uint8)
holes = face_filled & (1 - face) & dark
n, lab, st, cen = cv2.connectedComponentsWithStats(holes)
pupils = []
for k in range(1, n):
    area = st[k, 4]
    if area < 0.00025 * H * W: continue
    comp = (lab == k).astype(np.uint8)
    c2, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    per = cv2.arcLength(max(c2, key=cv2.contourArea), True)
    circ = 4 * np.pi * area / max(per * per, 1)
    if circ < 0.55: continue            # closed/winking eye or beak line: leave it alone
    pupils.append((area, k, comp))
pupils = sorted(pupils, reverse=True)[:2]
if not pupils: print(dst, 'no pupils found'); cv2.imwrite(dst, img); sys.exit()
fx0, fy0, fw, fh = cv2.boundingRect(face_filled)
mid = fx0 + fw / 2
out = rgb.copy()
erase = np.zeros((H, W), np.uint8)
for _, k, comp in pupils:
    c2, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(comp); cv2.drawContours(filled, c2, -1, 1, -1)
    erase |= cv2.dilate(filled, np.ones((5, 5), np.uint8), iterations=2)
out = cv2.inpaint(out, erase * 255, 7, cv2.INPAINT_TELEA)
allowed = cv2.erode(face_filled, np.ones((5, 5), np.uint8), iterations=1)
SS = 4
layer = np.zeros((H * SS, W * SS, 4), np.float32)
for _, k, comp in pupils:
    ys, xs = np.where(comp > 0); cx, cy = xs.mean(), ys.mean()
    r = np.sqrt(len(xs) / np.pi)
    side = -1 if cx < mid else 1
    if center > 0:   # pull toward the centre of this eye's white area (per side of the face)
        sidem = face_filled.copy(); sidem[:, :int(mid)] = 0 if side > 0 else sidem[:, :int(mid)]
        if side < 0: sidem[:, int(mid):] = 0
        sy, sx = np.where(sidem[:int(cy + 3 * r)] > 0)
        if len(sx): cx = cx + (sx.mean() - cx) * center
    pw, ph = 2 * r * 1.2 * gscale, 2 * r * 1.42 * gscale
    cy = cy + 0.12 * r
    ang = 10 * side
    C = (int(cx * SS), int(cy * SS)); ax = (int(pw / 2 * SS), int(ph / 2 * SS))
    pm = np.zeros((H * SS, W * SS), np.uint8); cv2.ellipse(pm, C, ax, ang, 0, 360, 255, -1)
    # glossy black: slightly lifted rim at the bottom
    base = np.zeros((H * SS, W * SS, 3), np.float32); base[:] = (30, 28, 28)
    yy = np.linspace(0, 1, H * SS)[:, None]
    m = pm.astype(np.float32) / 255
    for ch in range(3): layer[..., ch] = layer[..., ch] * (1 - m) + base[..., ch] * m
    layer[..., 3] = np.maximum(layer[..., 3], m)
    # highlight
    hx, hy = cx - 0.2 * pw, cy - 0.24 * ph
    hl = np.zeros((H * SS, W * SS), np.uint8)
    cv2.circle(hl, (int(hx * SS), int(hy * SS)), int(0.13 * pw * SS), 255, -1)
    hm = (hl.astype(np.float32) / 255) * m
    for ch in range(3): layer[..., ch] = layer[..., ch] * (1 - hm) + 252 * hm
small = cv2.resize(layer, (W, H), interpolation=cv2.INTER_AREA)
small = cv2.GaussianBlur(small, (0, 0), 0.6)
la = small[..., 3:4] * allowed[..., None]
res = (out.astype(np.float32) * (1 - la) + small[..., :3] * la).clip(0, 255).astype(np.uint8)
cv2.imwrite(dst, np.dstack([res, alpha])); print(dst, 'pupils replaced:', len(pupils))
