#!/usr/bin/env python3
"""Stage 2: render the montage. Locked camera, one dance loop, world changes."""
import numpy as np, subprocess, os, json, math, random
from PIL import Image, ImageDraw
import importlib.util
spec = importlib.util.spec_from_file_location('bd', os.path.join(os.path.dirname(__file__), 'build_dance.py'))
bd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd)

ROOT = bd.ROOT
W, H, FPS = 1920, 1080, 24
OUTDIR = os.path.expanduser('~/workspace/your_files/cape-jones-dance-proof')
random.seed(11)

# ---------------- backgrounds (flat SGC2C-style plates) ----------------
def vgrad(size, top, bot):
    t = np.linspace(0, 1, size[1])[:, None, None]
    top = np.array(top, float)[None, None, :]; bot = np.array(bot, float)[None, None, :]
    arr = (top * (1 - t) + bot * t).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, size[0], axis=1))

def blobs(d, ybase, n, rmin, rmax, color, xspan=(0, W)):
    for _ in range(n):
        x = random.uniform(*xspan); r = random.uniform(rmin, rmax)
        d.ellipse([x - r, ybase - r * 0.7, x + r, ybase + r * 0.7], fill=color)

def bg_yard():
    im = vgrad((W, H), (110, 190, 245), (215, 245, 255)); d = ImageDraw.Draw(im)
    d.ellipse([1620, 60, 1780, 220], fill=(255, 236, 150))          # sun
    d.rectangle([0, 790, W, H], fill=(86, 168, 92))                  # ground
    for i in range(6):                                               # mow stripes
        if i % 2 == 0: d.rectangle([i * 340, 790, i * 340 + 170, H], fill=(96, 180, 102))
    blobs(d, 800, 26, 40, 95, (52, 128, 66))                         # tree line
    d.rectangle([0, 782, W, 800], fill=(46, 110, 58))
    for x in range(20, W, 64):                                       # picket fence
        d.rectangle([x, 742, x + 26, 838], fill=(238, 238, 232))
        d.polygon([(x, 742), (x + 13, 724), (x + 26, 742)], fill=(238, 238, 232))
    d.rectangle([0, 792, W, 806], fill=(220, 220, 214))
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    blobs(fd, 1120, 7, 90, 170, (24, 74, 34, 255), xspan=(-80, 420))
    blobs(fd, 1120, 7, 90, 170, (24, 74, 34, 255), xspan=(1500, 2000))
    for x in range(30, W, 90):                                       # grass tufts
        fd.polygon([(x, 1080), (x + 9, 1030), (x + 18, 1080)], fill=(30, 92, 40, 255))
    return im, fg

def bg_mesa():
    im = vgrad((W, H), (125, 205, 250), (240, 250, 255)); d = ImageDraw.Draw(im)
    d.ellipse([120, 70, 260, 210], fill=(255, 240, 160))
    d.rectangle([0, 800, W, H], fill=(224, 176, 115))
    d.polygon([(0, 800), (0, 560), (420, 560), (520, 660), (700, 660), (700, 800)], fill=(198, 108, 72))
    d.polygon([(0, 800), (0, 640), (430, 640), (520, 700), (700, 700), (700, 800)], fill=(172, 88, 54))
    d.polygon([(W, 800), (W, 600), (1560, 600), (1460, 690), (1300, 690), (1300, 800)], fill=(204, 116, 78))
    d.polygon([(W, 800), (W, 680), (1570, 680), (1470, 730), (1300, 730), (1300, 800)], fill=(178, 94, 58))
    for cx in (880, 1740):                                           # cacti
        d.rectangle([cx, 690, cx + 26, 810], fill=(46, 122, 62))
        d.rectangle([cx - 34, 724, cx, 748], fill=(46, 122, 62)); d.rectangle([cx - 34, 700, cx - 10, 748], fill=(46, 122, 62))
        d.rectangle([cx + 26, 736, cx + 58, 760], fill=(46, 122, 62)); d.rectangle([cx + 34, 706, cx + 58, 760], fill=(46, 122, 62))
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    fd.polygon([(0, 1080), (0, 980), (180, 940), (340, 1010), (380, 1080)], fill=(120, 66, 40, 255))
    fd.polygon([(W, 1080), (W, 960), (1760, 930), (1600, 1000), (1560, 1080)], fill=(128, 70, 42, 255))
    fd.ellipse([260, 1020, 420, 1090], fill=(146, 84, 48, 255)); fd.ellipse([1560, 1030, 1700, 1095], fill=(146, 84, 48, 255))
    return im, fg

def bg_evening():
    im = vgrad((W, H), (38, 58, 110), (110, 124, 168)); d = ImageDraw.Draw(im)
    for _ in range(140):
        x, y = random.uniform(0, W), random.uniform(0, 520); r = random.uniform(1, 2.6)
        d.ellipse([x, y, x + r, y + r], fill=(235, 240, 255))
    d.ellipse([1500, 70, 1650, 220], fill=(240, 240, 220))          # moon
    d.ellipse([1460, 55, 1620, 205], fill=(38, 58, 110))
    d.rectangle([0, 800, W, H], fill=(30, 62, 40))
    blobs(d, 806, 26, 42, 100, (14, 34, 22))
    d.rectangle([0, 786, W, 806], fill=(10, 26, 16))
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    blobs(fd, 1120, 8, 95, 180, (6, 16, 10, 255), xspan=(-80, 430))
    blobs(fd, 1120, 8, 95, 180, (6, 16, 10, 255), xspan=(1490, 2000))
    return im, fg

# ---------------- grades (lighting states) ----------------
# name -> (rgb multiply, tint color, tint strength, brightness)
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
    if k > 0:
        a = a * (1 - k) + np.array(tint, np.float32) * k
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def apply_grade_rgba(img, name):
    """Grade only the RGB of an RGBA layer (the grade is linear, so grading
    each layer then compositing == compositing then grading)."""
    r, g, b, a = img.split()
    rgb = apply_grade(Image.merge('RGB', (r, g, b)), name)
    rgb.putalpha(a)
    return rgb

# ---------------- sections: (bg, grade, flipped) ----------------
SECTIONS = [
    ('yard',    'day',     False),
    ('yard',    'magenta', False),
    ('mesa',    'cyan',    False),
    ('mesa',    'green',   False),
    ('evening', 'dusk',    True),
    ('evening', 'night',   True),
    ('yard',    'day',     True),
]
SEC_FRAMES = 72                      # 3 s each, 21 s total
TOTAL = SEC_FRAMES * len(SECTIONS)

def main():
    fig = Image.open(f'{ROOT}/parts/figure_rgba.png')
    layers, piv = bd.segment(fig)
    drawings, drawings_flip = [], []
    for spec_d in bd.DANCE:
        d = bd.build_drawing(layers, piv, spec_d)
        drawings.append(d)
        drawings_flip.append(d.transpose(Image.FLIP_LEFT_RIGHT))
    # scale to stage: figure height 900 px, feet planted at y=1018
    def stage(d):
        r = 900 / d.size[1]
        return d.resize((int(d.size[0] * r), 900), Image.LANCZOS)
    drawings = [stage(d) for d in drawings]
    drawings_flip = [stage(d) for d in drawings_flip]
    bgs = {'yard': bg_yard(), 'mesa': bg_mesa(), 'evening': bg_evening()}
    # Pre-grade every layer per section (grade is linear -> distributes over
    # alpha compositing), so the frame loop is just two pastes.
    graded_bg, graded_fg, graded_d = {}, {}, {}
    for bgname, grade, flipped in SECTIONS:
        if (bgname, grade) not in graded_bg:
            bg, fg = bgs[bgname]
            graded_bg[(bgname, grade)] = apply_grade(bg, grade)
            graded_fg[(bgname, grade)] = apply_grade_rgba(fg, grade)
        key = (grade, flipped)
        if key not in graded_d:
            src = drawings_flip if flipped else drawings
            graded_d[key] = [apply_grade_rgba(d, grade) for d in src]

    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
        '-i', '-', '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17',
        '-preset', 'veryfast',
        f'{ROOT}/video_only.mp4'], stdin=subprocess.PIPE)
    sheet_frames = []
    for f in range(TOTAL):
        sec = f // SEC_FRAMES
        bgname, grade, flipped = SECTIONS[sec]
        frame = graded_bg[(bgname, grade)].copy()
        d = graded_d[(grade, flipped)][(f // 3) % 4]
        frame.paste(d, (960 - d.size[0] // 2, 1018 - 900), d)
        fg = graded_fg[(bgname, grade)]
        frame.paste(fg, (0, 0), fg)
        ff.stdin.write(frame.tobytes())
        if f % SEC_FRAMES == SEC_FRAMES // 2:
            sheet_frames.append(frame.resize((640, 360), Image.LANCZOS))
    ff.stdin.close(); ff.wait()
    sheet = Image.new('RGB', (640 * 4, 360 * 2), (20, 20, 20))
    for i, sf in enumerate(sheet_frames):
        sheet.paste(sf, ((i % 4) * 640, (i // 4) * 360))
    sheet.save(f'{OUTDIR}/cj-dance-proof-2d-sheet.png')
    print('video_only done, sheet saved', len(sheet_frames))

if __name__ == '__main__':
    main()
