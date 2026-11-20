# Give a Chip render the brand face from ref/chip-eyes-reference.jpg: white eye patches shaped like an
# upside-down Pot, oval pupils with a highlight, open beak. The old (round) face is painted out with the head
# black, then the reference face is fitted to the old face's bounding box and composited on top.
# Usage: python3 -I fix_face.py in.png out.png [--wink] [--blur 1.0] [--grow 1.0] [--dy 0]
import cv2, numpy as np, sys, os
a = sys.argv[1:]
def opt(name, default):
    if name in a: i = a.index(name); v = float(a[i + 1]); del a[i:i + 2]; return v
    return default
wink = '--wink' in a
if wink: a.remove('--wink')
blur = opt('--blur', 1.0); grow = opt('--grow', 1.0); dy = opt('--dy', 0.0)
src, dst = a[0], a[1]
here = os.path.dirname(os.path.abspath(__file__))

def masks(rgb, region):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    white = ((hsv[..., 2] > 175) & (hsv[..., 1] < 70) & region).astype(np.uint8)
    white = cv2.morphologyEx(white, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(white)
    big = 1 + int(np.argmax(st[1:, 4])); face = (lab == big).astype(np.uint8)
    # the two eye lobes may be separate components: add the next one if it's large and beside the first
    if n > 2:
        order = 1 + np.argsort(-st[1:, 4])
        if st[order[1], 4] > 0.4 * st[big, 4]: face |= (lab == order[1]).astype(np.uint8)
    cnts, _ = cv2.findContours(face, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(face); cv2.drawContours(filled, cnts, -1, 1, -1)
    beak = (((hsv[..., 0] < 32) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 110) & (hsv[..., 2] > 90) & region).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(beak)
    if n > 1:
        bb = 1 + int(np.argmax(st[1:, 4])); beak = (lab == bb).astype(np.uint8)
        beak = cv2.morphologyEx(beak, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        c2, _ = cv2.findContours(beak, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        beak = np.zeros_like(beak); cv2.drawContours(beak, c2, -1, 1, -1)
    return filled, beak

# --- reference face (RGBA) ---
ref = cv2.imread(os.path.join(here, '..', 'ref', 'chip-eyes-reference.jpg'))
rr = np.zeros(ref.shape[:2], bool); rr[560:1120, 40:700] = True
rf, rb = masks(ref, rr)
ref_face = cv2.dilate(rf | rb, np.ones((7, 7), np.uint8))            # bring the soft dark seam along
rx, ry, rw, rh = cv2.boundingRect(rf | rb)
ref_rgba = np.dstack([ref, (cv2.GaussianBlur(ref_face.astype(np.float32), (0, 0), 1.5) * 255).astype(np.uint8)])
if wink:   # close the right eye: paint its pupil with the eye white, then draw a happy closed-eye arc
    hsv = cv2.cvtColor(ref, cv2.COLOR_BGR2HSV)
    dark = (hsv[..., 2] < 110) & (rf > 0)
    right = np.zeros_like(dark); right[:, rx + rw // 2 + 40:] = True
    n, lab, st, cen = cv2.connectedComponentsWithStats((dark & right & rr).astype(np.uint8))
    k = 1 + int(np.argmax(st[1:, 4])); pm = cv2.dilate((lab == k).astype(np.uint8), np.ones((9, 9), np.uint8), iterations=2)
    body = ref_rgba[..., :3].copy()
    body = cv2.inpaint(body, pm * 255, 9, cv2.INPAINT_TELEA)
    cx, cy = cen[k]; w_ = st[k, 2] * 1.25
    cv2.ellipse(body, (int(cx), int(cy + w_ * 0.18)), (int(w_ * 0.62), int(w_ * 0.42)), 0, 200, 340, (34, 32, 32), int(w_ * 0.2), cv2.LINE_AA)
    ref_rgba[..., :3] = body

# --- target ---
img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
rgb, alpha = img[..., :3].copy(), img[..., 3]
H, W = alpha.shape
hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
solid = alpha > 200
# beak = the TOPMOST orange shape (feet and beanbag are lower down)
orange = ((((hsv[..., 0] < 32) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 110) & (hsv[..., 2] > 90)) & solid).astype(np.uint8)
orange = cv2.morphologyEx(orange, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(orange)
cands = [k for k in range(1, n) if st[k, 4] > 0.0015 * H * W]
k = min(cands, key=lambda k: st[k, 1])
bx, by, bw, bh = st[k, :4]
tb = cv2.morphologyEx((lab == k).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
c2, _ = cv2.findContours(tb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); tb = np.zeros_like(tb); cv2.drawContours(tb, c2, -1, 1, -1)
# face = white pixels around the beak, above the neck; erode to break any bridge to the belly, keep lobes beside/above the beak
white = ((hsv[..., 2] > 175) & (hsv[..., 1] < 70) & solid).astype(np.uint8)
white[int(by + bh * 1.15):] = 0
er = cv2.erode(white, np.ones((5, 5), np.uint8), iterations=2)
n, lab, st, _ = cv2.connectedComponentsWithStats(er)
keep = np.zeros_like(er)
for j in range(1, n):
    x, y, w, h, ar = st[j]
    if ar < 0.002 * H * W: continue
    if y < by and x < bx + bw * 3.5 and x + w > bx - bw * 2.5: keep |= (lab == j).astype(np.uint8)
face = keep
# grow back into the white, allowing a little further down than the detection cut so the old chin is fully removed
white2 = ((hsv[..., 2] > 150) & (hsv[..., 1] < 80) & solid).astype(np.uint8)
# find the bottom of the old face: scan down under the beak until the white gives way to the black neck band
V = hsv[..., 2]
c0, c1 = int(bx + bw * 0.35), int(bx + bw * 0.65)          # narrow band under the middle of the beak (the chin's lowest point)
cut, run, seen = int(by + bh * 0.8), 0, False      # skip the beak's own dark outline: wait until white is seen, then the black band
while cut < H - 1 and run < 3:
    m = V[cut, c0:c1].max()
    if m > 200: seen = True
    run = run + 1 if (seen and m < 70) else 0
    cut += 1
white2 = ((V > 90) & (hsv[..., 1] < 90) & solid).astype(np.uint8)   # include the soft anti-aliased edge
white2[cut + 2:] = 0
for _ in range(60): face = cv2.dilate(face, np.ones((3, 3), np.uint8)) & white2
c2, _ = cv2.findContours(face, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); tf = np.zeros_like(face); cv2.drawContours(tf, c2, -1, 1, -1)
old = cv2.dilate(tf | tb, np.ones((5, 5), np.uint8), iterations=5)
tx, ty, tw, th = cv2.boundingRect(tf)
# paint the old face out with the head black (inpaint from the surrounding head)
painted = cv2.inpaint(rgb, old * 255, 11, cv2.INPAINT_TELEA)
ring = (cv2.dilate(old, np.ones((15, 15), np.uint8)) > 0) & (old == 0) & solid
headblack = np.median(rgb[ring], axis=0)
inner = cv2.erode(old, np.ones((9, 9), np.uint8)) > 0
painted[inner] = (painted[inner] * 0.5 + headblack * 0.5).astype(np.uint8)
soft = np.minimum(1, cv2.GaussianBlur(cv2.dilate(old, np.ones((21, 21), np.uint8)).astype(np.float32), (0, 0), 4) * 1.05)[..., None]   # =1 over the old face, fades outside it
painted = (rgb.astype(np.float32) * (1 - soft) + painted.astype(np.float32) * soft).astype(np.uint8)
# fit the reference face: uniform scale by face width, centred on the old face, tops aligned
rfx, rfy, rfw, rfh = cv2.boundingRect(rf)
sc = tw / rfw * grow
M = np.float32([[sc, 0, tx + tw / 2 - (rfx + rfw / 2) * sc], [0, sc, ty + dy - rfy * sc]])
warp = cv2.warpAffine(ref_rgba, M, (W, H), flags=cv2.INTER_AREA if sc < 1 else cv2.INTER_CUBIC, borderValue=(0, 0, 0, 0))
if blur > 0: warp = cv2.GaussianBlur(warp, (0, 0), blur)
la = (warp[..., 3:4].astype(np.float32) / 255) * (cv2.erode(solid.astype(np.uint8), np.ones((7, 7), np.uint8))[..., None])
res = (painted.astype(np.float32) * (1 - la) + warp[..., :3].astype(np.float32) * la).clip(0, 255).astype(np.uint8)
sx = sy = sc
cv2.imwrite(dst, np.dstack([res, alpha])); print(dst, 'face box', (tx, ty, tw, th), 'scale', round(sx, 3), round(sy, 3))
