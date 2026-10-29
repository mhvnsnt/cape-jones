#!/usr/bin/env python3
"""Stage 2 v2: painted plates + composite render.

Plates are PAINTED HERE (labelled honestly): the repo search found real
production plates only in mystery-coast-ghosted's Scooby-Doo SDMI pack -
16 viewed, all establishing/interior compositions for another show's
locations, none a character-scale outside stage. So the yard / mesa /
evening plates are painted with texture, shading and layered depth:
far / mid / near / foreground, per cape-jones docs/environments/
MIXED-MEDIA-GUIDE.md layering.

Outputs:
- video_only_1080.mp4  (native-res cutout composite = labelled fallback)
- vace_in/sec{i}.mp4   (832x480 section composites, VACE driving video)
- vace_in/sec{i}_mask.mp4 (white = redraw the character, dilated)
- vace_in/ref.png      (the sheet figure on neutral grey, VACE reference)
- contact sheet (7 states)
Grades and section structure are v1's, unchanged.
"""
import numpy as np, subprocess, os, json, math
from PIL import Image, ImageDraw, ImageFilter
import cv2, importlib.util

spec = importlib.util.spec_from_file_location('bd2', os.path.join(os.path.dirname(__file__), 'build_dance_v2.py'))
bd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd)

ROOT = bd.ROOT
W, H, FPS = 1920, 1080, 24
VW, VH = 832, 480                      # VACE working size (accel-kernel class)
OUTDIR = os.path.expanduser('~/workspace/your_files/cape-jones-dance-proof')
VACEIN = f'{ROOT}/vace_in'; os.makedirs(VACEIN, exist_ok=True)
rng = np.random.default_rng(20261029)

# ---------------- texture helpers ----------------
def noise_field(w, h, cell, seed):
    r = np.random.default_rng(seed)
    gh, gw = max(2, h // cell + 2), max(2, w // cell + 2)
    g = r.random((gh, gw)).astype(np.float32)
    f = cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
    return (f - f.mean()) / (f.std() + 1e-6)

def add_texture(img, coarse=5.0, fine=2.5, seed=1, mask=None):
    a = np.asarray(img).astype(np.float32)
    n = noise_field(a.shape[1], a.shape[0], 90, seed) * coarse + noise_field(a.shape[1], a.shape[0], 9, seed + 7) * fine
    if mask is not None:
        n = n * mask
    a += n[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def vgrad(w, h, top, bot):
    t = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(top, float)[None, None, :] * (1 - t) + np.array(bot, float)[None, None, :] * t)
    return Image.fromarray(np.repeat(arr, w, axis=1).astype(np.uint8))

def soft_layer(w, h, draw_fn, blur=8):
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay))
    return lay.filter(ImageFilter.GaussianBlur(blur))

def blobs_on(d, ybase, n, rmin, rmax, color, xspan=(0, W), seed=3):
    r = np.random.default_rng(seed)
    for _ in range(n):
        x = r.uniform(*xspan); rad = r.uniform(rmin, rmax)
        d.ellipse([x - rad, ybase - rad * 0.72, x + rad, ybase + rad * 0.72], fill=color)

def speckle(img, n, y0, y1, colors, seed=5, rmax=3.0):
    r = np.random.default_rng(seed)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y = r.uniform(0, img.size[0]), r.uniform(y0, y1); rad = r.uniform(0.8, rmax)
        col = colors[int(r.integers(0, len(colors)))]
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=tuple(col) + (int(r.uniform(60, 150)),))
    img.alpha_composite(lay) if img.mode == 'RGBA' else None
    return Image.alpha_composite(img.convert('RGBA'), lay).convert('RGB') if img.mode != 'RGBA' else img

def contact_shadow(img, cx=960, cy=1006, rx=300, ry=30, alpha=95):
    lay = soft_layer(img.size[0], img.size[1],
                     lambda d: d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(10, 20, 12, alpha)), blur=14)
    return Image.alpha_composite(img.convert('RGBA'), lay).convert('RGB')

# ---------------- YARD (day) ----------------
def bg_yard():
    im = vgrad(W, H, (96, 175, 240), (208, 240, 255)); d = ImageDraw.Draw(im, 'RGBA')
    # sun + glow
    glow = soft_layer(W, H, lambda dd: dd.ellipse([1560, 0, 1860, 300], fill=(255, 244, 190, 110)), blur=60)
    im = Image.alpha_composite(im.convert('RGBA'), glow).convert('RGB'); d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse([1630, 55, 1795, 220], fill=(255, 238, 158))
    # clouds: shaded puffs
    for (cx, cy, s) in [(300, 120, 1.0), (760, 80, 0.7), (1180, 150, 0.85), (150, 240, 0.55)]:
        for dx, dy, r in [(-90, 10, 55), (-30, -18, 75), (45, -8, 65), (105, 14, 48)]:
            d.ellipse([cx + dx * s - r * s, cy + dy * s + 14 * s, cx + dx * s + r * s, cy + dy * s + 40 * s], fill=(176, 205, 232, 120))
        for dx, dy, r in [(-90, 0, 55), (-30, -28, 75), (45, -18, 65), (105, 4, 48)]:
            d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s * 0.62, cx + dx * s + r * s, cy + dy * s + r * s * 0.62], fill=(255, 255, 255, 235))
    # far tree line (two depths)
    blobs_on(d, 782, 30, 55, 120, (88, 156, 92, 255), seed=21)
    blobs_on(d, 796, 34, 45, 100, (58, 128, 68, 255), seed=22)
    blobs_on(d, 760, 22, 30, 60, (110, 178, 104, 160), seed=23)
    d.rectangle([0, 780, W, 806], fill=(50, 116, 60))
    im = add_texture(im, 3.5, 2.0, seed=31, mask=(np.indices((H, W))[0] > 700).astype(np.float32))
    d = ImageDraw.Draw(im, 'RGBA')
    # lawn
    lawn = vgrad(W, 274, (96, 178, 98), (66, 142, 76)); im.paste(lawn, (0, 806)); d = ImageDraw.Draw(im, 'RGBA')
    for i in range(6):  # soft mow stripes
        if i % 2 == 0:
            stripe = soft_layer(W, H, lambda dd, i=i: dd.rectangle([i * 340, 800, i * 340 + 170, H], fill=(255, 255, 220, 16)), blur=18)
            im = Image.alpha_composite(im.convert('RGBA'), stripe).convert('RGB'); d = ImageDraw.Draw(im, 'RGBA')
    im = add_texture(im, 4.0, 2.5, seed=33, mask=(np.indices((H, W))[0] > 800).astype(np.float32))
    d = ImageDraw.Draw(im, 'RGBA')
    # picket fence with per-picket shading + cast shadow
    shad = soft_layer(W, H, lambda dd: dd.rectangle([0, 838, W, 862], fill=(20, 60, 26, 70)), blur=7)
    im = Image.alpha_composite(im.convert('RGBA'), shad).convert('RGB'); d = ImageDraw.Draw(im, 'RGBA')
    for x in range(16, W, 64):
        d.polygon([(x, 742), (x + 13, 722), (x + 26, 742)], fill=(242, 242, 236))
        d.rectangle([x, 742, x + 26, 840], fill=(240, 240, 234))
        d.rectangle([x + 19, 742, x + 26, 840], fill=(206, 206, 198))
        d.rectangle([x, 742, x + 4, 840], fill=(252, 252, 248))
    d.rectangle([0, 770, W, 782], fill=(232, 232, 226)); d.rectangle([0, 812, W, 824], fill=(226, 226, 220))
    d.rectangle([0, 770, W, 774], fill=(250, 250, 246))
    # grass detail: patches + blades
    for _ in range(14):
        x, y = rng.uniform(0, W), rng.uniform(850, 1060); r = rng.uniform(30, 90)
        d.ellipse([x - r, y - r * 0.3, x + r, y + r * 0.3], fill=(52, 118, 58, 36))
    for _ in range(700):
        x, y = rng.uniform(0, W), rng.uniform(880, 1078); ln = rng.uniform(6, 16)
        col = (40, 104, 48, 170) if rng.random() < 0.6 else (128, 198, 120, 150)
        d.line([x, y, x + rng.uniform(-3, 3), y - ln], fill=col, width=2)
    im = contact_shadow(im)
    # foreground: shaded foliage corners
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    blobs_on(fd, 1130, 8, 95, 175, (22, 66, 32, 255), xspan=(-90, 430), seed=41)
    blobs_on(fd, 1130, 8, 95, 175, (22, 66, 32, 255), xspan=(1490, 2010), seed=42)
    blobs_on(fd, 1080, 6, 60, 110, (40, 96, 46, 200), xspan=(-60, 380), seed=43)
    blobs_on(fd, 1080, 6, 60, 110, (40, 96, 46, 200), xspan=(1540, 1990), seed=44)
    fg = add_texture(fg, 5.0, 2.0, seed=45)
    return im, fg

# ---------------- MESA ----------------
def strata(d, x0, x1, ytop, ybot, base, dark, light, seed):
    r = np.random.default_rng(seed)
    d.polygon([(x0, ybot), (x0, ytop + 40), (x0 + 60, ytop), (x1 - 60, ytop), (x1, ytop + 40), (x1, ybot)], fill=base)
    y = ytop + 26
    while y < ybot - 10:
        hh = r.uniform(10, 26)
        d.rectangle([x0 + 4, y, x1 - 4, y + hh * 0.45], fill=dark if r.random() < 0.6 else light)
        y += hh
    # shadow facet on the right third + sunlit top edge
    d.polygon([(x1 - (x1 - x0) * 0.30, ytop + 12), (x1, ytop + 40), (x1, ybot), (x1 - (x1 - x0) * 0.22, ybot)], fill=dark)
    d.line([x0 + 60, ytop, x1 - 60, ytop], fill=light, width=5)

def bg_mesa():
    im = vgrad(W, H, (110, 196, 246), (228, 248, 255)); d = ImageDraw.Draw(im, 'RGBA')
    glow = soft_layer(W, H, lambda dd: dd.ellipse([60, 10, 330, 280], fill=(255, 246, 196, 100)), blur=55)
    im = Image.alpha_composite(im.convert('RGBA'), glow).convert('RGB'); d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse([115, 65, 255, 205], fill=(255, 242, 168))
    for (cx, cy, s) in [(560, 110, 0.8), (1330, 90, 1.0), (1720, 190, 0.6)]:
        for dx, dy, r in [(-70, 0, 48), (0, -16, 62), (70, 6, 42)]:
            d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s * 0.6, cx + dx * s + r * s, cy + dy * s + r * s * 0.6], fill=(255, 255, 255, 215))
    # far range (hazy) then mid mesas
    far = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(far)
    strata(fd, -40, 700, 600, 806, (214, 164, 128, 235), (198, 142, 106, 235), (230, 188, 152, 235), 51)
    strata(fd, 1180, 1980, 580, 806, (210, 158, 122, 235), (192, 136, 100, 235), (226, 182, 146, 235), 52)
    far = far.filter(ImageFilter.GaussianBlur(1.6)); im = Image.alpha_composite(im.convert('RGBA'), far).convert('RGB')
    d = ImageDraw.Draw(im, 'RGBA')
    strata(d, -60, 560, 545, 812, (196, 106, 70), (168, 84, 50), (222, 140, 96), 53)
    strata(d, 1420, 1990, 520, 812, (200, 112, 74), (172, 88, 52), (226, 146, 100), 54)
    im = add_texture(im, 4.5, 2.0, seed=55, mask=(np.indices((H, W))[0] > 500).astype(np.float32))
    # desert floor
    floor = vgrad(W, 268, (233, 192, 130), (206, 156, 96)); im.paste(floor, (0, 812)); d = ImageDraw.Draw(im, 'RGBA')
    im = add_texture(im, 5.0, 3.0, seed=56, mask=(np.indices((H, W))[0] > 812).astype(np.float32))
    im = speckle(im, 900, 830, 1075, [(150, 104, 62), (120, 80, 46), (248, 220, 170)], seed=57)
    d = ImageDraw.Draw(im, 'RGBA')
    def cactus(x, y, s):
        sh = soft_layer(W, H, lambda dd: dd.ellipse([x - 46 * s, y + 96 * s, x + 90 * s, y + 116 * s], fill=(90, 60, 30, 90)), blur=8)
        nonlocal_im = Image.alpha_composite(im.convert('RGBA'), sh).convert('RGB')
        dd = ImageDraw.Draw(nonlocal_im, 'RGBA')
        g, gd, gl = (44, 120, 62), (30, 92, 46), (86, 168, 96)
        dd.rounded_rectangle([x, y, x + 30 * s, y + 105 * s], 14 * s, fill=g)
        dd.rounded_rectangle([x + 19 * s, y, x + 30 * s, y + 105 * s], 10 * s, fill=gd)
        dd.line([x + 6 * s, y + 8 * s, x + 6 * s, y + 98 * s], fill=gl, width=max(2, int(3 * s)))
        dd.rounded_rectangle([x - 34 * s, y + 30 * s, x - 8 * s, y + 58 * s], 10 * s, fill=g)
        dd.rounded_rectangle([x - 34 * s, y + 8 * s, x - 20 * s, y + 40 * s], 9 * s, fill=g)
        dd.rounded_rectangle([x + 32 * s, y + 42 * s, x + 58 * s, y + 66 * s], 10 * s, fill=gd)
        dd.rounded_rectangle([x + 44 * s, y + 18 * s, x + 58 * s, y + 50 * s], 9 * s, fill=gd)
        return nonlocal_im
    im = cactus(872, 700, 1.0); im = cactus(1732, 688, 1.15); d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(16):  # scrub tufts
        x, y = rng.uniform(40, W - 40), rng.uniform(850, 1050); s = rng.uniform(0.6, 1.3)
        for k in range(7):
            dx = rng.uniform(-16, 16) * s
            d.line([x, y, x + dx, y - rng.uniform(12, 26) * s], fill=(96, 108, 58, 220), width=3)
    im = contact_shadow(im)
    # foreground rocks with facets
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    def rock(cx, cy, s, seed):
        r = np.random.default_rng(seed)
        pts = [(cx + r.uniform(-90, 90) * s, cy + r.uniform(-14, 10) * s) for _ in range(7)]
        pts = sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        fd.polygon(pts, fill=(150, 92, 58, 255))
        fd.polygon([pts[0], pts[1], pts[2], (cx, cy)], fill=(178, 116, 76, 255))
        fd.polygon([pts[3], pts[4], pts[5], (cx, cy)], fill=(118, 70, 42, 255))
    rock(150, 1052, 1.15, 61); rock(380, 1070, 0.8, 62); rock(1790, 1058, 1.05, 63); rock(1560, 1074, 0.7, 64)
    fg = add_texture(fg, 5.0, 2.5, seed=65)
    return im, fg

# ---------------- EVENING YARD (dusk/night base) ----------------
def bg_evening():
    im = vgrad(W, H, (26, 42, 88), (96, 112, 158)); d = ImageDraw.Draw(im, 'RGBA')
    r = np.random.default_rng(71)
    for _ in range(220):
        x, y = r.uniform(0, W), r.uniform(0, 540); rad = r.uniform(0.7, 2.4)
        d.ellipse([x, y, x + rad, y + rad], fill=(235, 240, 255, int(r.uniform(90, 230))))
    glow = soft_layer(W, H, lambda dd: dd.ellipse([1420, 20, 1740, 340], fill=(220, 226, 255, 70)), blur=50)
    im = Image.alpha_composite(im.convert('RGBA'), glow).convert('RGB')
    # crescent: full moon, then a shifted copy of the sky itself pasted over
    # (a flat colour disc would show as a blob against the gradient)
    sky_only = im.copy()
    d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse([1505, 65, 1655, 215], fill=(238, 240, 224))
    occ = sky_only.crop((1466, 50, 1626, 200))
    omask = Image.new('L', (160, 150), 0)
    ImageDraw.Draw(omask).ellipse([0, 0, 160, 150], fill=255)
    im.paste(occ, (1466, 50), omask)
    d = ImageDraw.Draw(im, 'RGBA')
    blobs_on(d, 788, 30, 55, 120, (18, 40, 30, 255), seed=72)
    blobs_on(d, 800, 30, 45, 95, (10, 26, 20, 255), seed=73)
    d.rectangle([0, 782, W, 806], fill=(8, 22, 16))
    ground = vgrad(W, 274, (26, 58, 38), (16, 40, 26)); im.paste(ground, (0, 806)); d = ImageDraw.Draw(im, 'RGBA')
    im = add_texture(im, 3.5, 2.0, seed=74, mask=(np.indices((H, W))[0] > 780).astype(np.float32))
    d = ImageDraw.Draw(im, 'RGBA')
    for x in range(16, W, 64):  # fence as blue-grey silhouette w/ lit top edge
        d.polygon([(x, 742), (x + 13, 722), (x + 26, 742)], fill=(96, 110, 128))
        d.rectangle([x, 742, x + 26, 840], fill=(88, 102, 120))
        d.rectangle([x, 742, x + 26, 746], fill=(150, 166, 186))
    im = contact_shadow(im, alpha=130)
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    blobs_on(fd, 1130, 8, 95, 180, (6, 16, 11, 255), xspan=(-90, 430), seed=75)
    blobs_on(fd, 1130, 8, 95, 180, (6, 16, 11, 255), xspan=(1490, 2010), seed=76)
    return im, fg

# ---------------- grades (v1, unchanged) ----------------
GRADES = {
    'day':     ((1.00, 1.00, 1.00), (0, 0, 0), 0.00, 1.00),
    'magenta': ((1.06, 0.60, 1.06), (255, 0, 160), 0.16, 1.00),
    'cyan':    ((0.58, 1.00, 1.10), (0, 200, 255), 0.14, 1.00),
    'green':   ((0.62, 1.06, 0.62), (40, 255, 90), 0.14, 1.00),
    'dusk':    ((1.10, 0.74, 0.48), (255, 130, 40), 0.12, 0.94),
    'night':   ((0.40, 0.50, 0.88), (30, 40, 140), 0.10, 0.92),
}
def apply_grade(frame_img, name):
    mult, tint, k, bright = GRADES[name]
    a = np.asarray(frame_img).astype(np.float32)
    a *= np.array(mult, np.float32) * bright
    if k > 0: a = a * (1 - k) + np.array(tint, np.float32) * k
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def apply_grade_rgba(img, name):
    r, g, b, a = img.split()
    rgb = apply_grade(Image.merge('RGB', (r, g, b)), name); rgb.putalpha(a)
    return rgb

SECTIONS = [('yard', 'day', False), ('yard', 'magenta', False), ('mesa', 'cyan', False),
            ('mesa', 'green', False), ('evening', 'dusk', True), ('evening', 'night', True),
            ('yard', 'day', True)]
SEC_FRAMES = 72
TOTAL = SEC_FRAMES * len(SECTIONS)

def pipe_to(path, w, h, extra, rate=FPS):
    return subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                             '-s', f'{w}x{h}', '-r', str(rate), '-i', '-', '-an', '-c:v', 'libx264',
                             '-pix_fmt', 'yuv420p'] + extra + [path], stdin=subprocess.PIPE)

def main():
    fig = Image.open(f'{bd.V1PARTS}/figure_rgba.png')
    layers, piv = bd.segment(fig)
    def stage(d):
        r = 900 / d.size[1]
        return d.resize((int(d.size[0] * r), 900), Image.LANCZOS)
    cache = {}
    def drawing(flipped, f):
        key = (flipped, f % bd.LOOP)
        if key not in cache:
            d = bd.build_drawing(layers, piv, bd.sample_spec(f))
            if flipped: d = d.transpose(Image.FLIP_LEFT_RIGHT)
            cache[key] = stage(d)
        return cache[key]
    # VACE reference: the sheet figure on neutral grey
    refc = Image.new('RGBA', fig.size, (128, 128, 128, 255)); refc.alpha_composite(fig)
    refc.convert('RGB').save(f'{VACEIN}/ref.png')
    bgs = {'yard': bg_yard(), 'mesa': bg_mesa(), 'evening': bg_evening()}
    graded_bg, graded_fg = {}, {}
    for bgname, grade, flipped in SECTIONS:
        if (bgname, grade) not in graded_bg:
            bg, fg = bgs[bgname]
            graded_bg[(bgname, grade)] = apply_grade(bg, grade)
            graded_fg[(bgname, grade)] = apply_grade_rgba(fg, grade)
    ff = pipe_to(f'{ROOT}/video_only_1080.mp4', W, H, ['-crf', '17', '-preset', 'veryfast'])
    vace_ff, vace_mf = [], []
    for s in range(len(SECTIONS)):
        vace_ff.append(pipe_to(f'{VACEIN}/sec{s}.mp4', VW, VH, ['-crf', '10', '-preset', 'veryfast'], rate=16))
        vace_mf.append(pipe_to(f'{VACEIN}/sec{s}_mask.mp4', VW, VH, ['-crf', '6', '-preset', 'veryfast'], rate=16))
    sheet_frames = []
    for f in range(TOTAL):
        sec = f // SEC_FRAMES
        bgname, grade, flipped = SECTIONS[sec]
        frame = graded_bg[(bgname, grade)].copy()
        d = apply_grade_rgba(drawing(flipped, f), grade)
        frame.paste(d, (960 - d.size[0] // 2, 1018 - 900), d)
        fg = graded_fg[(bgname, grade)]
        frame.paste(fg, (0, 0), fg)
        ff.stdin.write(frame.tobytes())
        if f % SEC_FRAMES == SEC_FRAMES // 2: sheet_frames.append(frame.resize((640, 360), Image.LANCZOS))
        # VACE inputs: 49 frames per section at 16fps == f in [sec*72, sec*72+49)
        lf = f - sec * SEC_FRAMES
        if lf < 49:
            small = frame.resize((VW, VH), Image.LANCZOS)
            vace_ff[sec].stdin.write(small.tobytes())
            a = np.asarray(d.getchannel('A'))
            m = cv2.dilate((a > 8).astype(np.uint8) * 255, np.ones((21, 21), np.uint8))
            mask_full = np.zeros((H, W), np.uint8)
            mask_full[1018 - 900:1018, 960 - d.size[0] // 2:960 - d.size[0] // 2 + d.size[0]] = m[:900, :]
            mask_img = Image.fromarray(mask_full).resize((VW, VH), Image.BILINEAR).convert('RGB')
            vace_mf[sec].stdin.write(mask_img.tobytes())
    ff.stdin.close(); ff.wait()
    for p in vace_ff + vace_mf:
        p.stdin.close(); p.wait()
    sheet = Image.new('RGB', (640 * 4, 360 * 2), (20, 20, 20))
    for i, sf in enumerate(sheet_frames): sheet.paste(sf, ((i % 4) * 640, (i // 4) * 360))
    sheet.save(f'{ROOT}/sheet_cutout.png')
    print('render done: video_only_1080.mp4, vace_in/, sheet_cutout.png')

if __name__ == '__main__':
    main()
