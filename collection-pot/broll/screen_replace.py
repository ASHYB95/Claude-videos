# Screen replacement for B-roll clip 2: track the phone's blank white screen per frame and
# composite a real Collection Pot screen into it (hand + dynamic island stay on top via the white mask).
import cv2, numpy as np, subprocess, sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, 'b2_fast.mp4'); ui_path = sys.argv[1]; out = os.path.join(here, 'b2_comp.mp4')
W, H, FPS = 1080, 1920, 30
ui = cv2.imread(ui_path)  # portrait phone screenshot
uh, uw = ui.shape[:2]
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '13', '-preset', 'slow', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
track = []; prev = None; i = 0
def order(pts):
    pts = pts[np.argsort(pts[:, 1])]; top = pts[:2][np.argsort(pts[:2, 0])]; bot = pts[2:][np.argsort(pts[2:, 0])]
    return np.array([top[0], top[1], bot[1], bot[0]], np.float32)  # tl tr br bl
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] > 225) & (hsv[..., 1] < 28)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    best = None
    for k in range(1, n):
        x, y, w, h, a = stats[k]
        if a < 6000: continue
        ar = h / max(w, 1)
        fill = a / (w * h)
        if prev is not None:
            px, py = prev
            d = np.hypot(x + w / 2 - px, y + h / 2 - py)
        else: d = 0
        score = a * fill - d * 50
        if 1.0 < ar < 3.2 and fill > 0.45 and (best is None or score > best[0]): best = (score, k)
    ok = False
    if best:
        k = best[1]
        blob = (lab == k).astype(np.uint8) * 255
        # fill holes (dynamic island) for geometry only
        cnts, _ = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(cnts, key=cv2.contourArea)
        hull = cv2.convexHull(c)
        rect = cv2.minAreaRect(hull)
        box = order(cv2.boxPoints(rect).astype(np.float32))
        # ensure portrait orientation (tl->tr is the short side)
        if np.linalg.norm(box[1] - box[0]) > np.linalg.norm(box[3] - box[0]): box = np.array([box[3], box[0], box[1], box[2]], np.float32)
        x, y, w, h, a = stats[k]
        geo = np.zeros_like(blob); cv2.drawContours(geo, [hull], -1, 255, -1)
        ok = a > 12000
    if ok:
        prev = (rect[0][0], rect[0][1])
        Hm = cv2.getPerspectiveTransform(np.array([[0, 0], [uw, 0], [uw, uh], [0, uh]], np.float32), box)
        warped = cv2.warpPerspective(ui, Hm, (W, H), flags=cv2.INTER_CUBIC)
        # alpha: the white pixels themselves (hand/thumb occlusion + island stay real), softened
        alpha = cv2.bitwise_and(blob, geo).astype(np.float32) / 255
        alpha = cv2.GaussianBlur(alpha, (5, 5), 0)[..., None]
        # match the screen's lighting: scale by local white level
        white = cv2.GaussianBlur(f.astype(np.float32), (61, 61), 0) / 250.0
        lit = np.clip(warped.astype(np.float32) * np.clip(white, 0.75, 1.05), 0, 255)
        f = (f * (1 - alpha) + lit * alpha).astype(np.uint8)
        track.append({'i': i, 'box': box.tolist()})
    else:
        track.append({'i': i, 'box': None})
    enc.stdin.write(f.tobytes()); i += 1
enc.stdin.close(); enc.wait()
json.dump(track, open(os.path.join(here, 'b2_track.json'), 'w'))
print('frames', i, 'tracked', sum(1 for t in track if t['box']))
