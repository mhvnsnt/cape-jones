#!/usr/bin/env python3
"""Painterly procedural backgrounds (code-painted, NOT AI-generated) for the two
locations left after the 4-image media-generation cap in this batch:
  - neutral plaza (CJ-16..20, spec family 'any' — no specific location named)
  - lounge room, warm interior (CJ-23, CJ-25, CJ-27, storyboard stand-ins)
Technique: layered vertical gradients + blurred colour blobs + thousands of
semi-transparent brush strokes + paper grain, so the result reads painted,
not flat charcoal / flat vector. No character, no text, no logos, no labels
are drawn into either painting; centre foreground is kept clear for the
character plate. Original art only.
"""
import random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

random.seed(20261031)
OUT = "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/masters"


def vgrad(w, h, top, bottom):
    t = np.linspace(0, 1, h)[:, None]
    arr = np.zeros((h, w, 3), dtype=np.float64)
    for i in range(3):
        arr[:, :, i] = top[i] * (1 - t) + bottom[i] * t
    return Image.fromarray(arr.astype(np.uint8))


def blobs(img, items, blur=40):
    """items: (cx, cy, rx, ry, colour, alpha) soft ellipses on their own layer."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for cx, cy, rx, ry, col, a in items:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col + (a,))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(layer)
    return img


def strokes(img, n, palette, region, length=(8, 60), width=(2, 9), alpha=(18, 70)):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = region
    for _ in range(n):
        x = random.randint(x0, x1)
        y = random.randint(y0, y1)
        ang = random.uniform(-0.5, 0.5) + (random.choice([0, 1.57]) if random.random() < 0.2 else 0)
        ln = random.randint(*length)
        import math
        x2, y2 = x + ln * math.cos(ang), y + ln * math.sin(ang)
        col = random.choice(palette)
        d.line([x, y, x2, y2], fill=col + (random.randint(*alpha),), width=random.randint(*width))
    layer = layer.filter(ImageFilter.GaussianBlur(0.7))
    img.alpha_composite(layer)
    return img


def grain(img, amount=10):
    arr = np.array(img.convert("RGB")).astype(np.int16)
    noise = np.random.randint(-amount, amount + 1, arr.shape[:2])[..., None]
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def vignette(img, strength=0.18):
    w, h = img.size
    y, x = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt(((x - cx) / (w / 2)) ** 2 + ((y - cy) / (h / 2)) ** 2)
    factor = 1 - strength * np.clip(dist - 0.55, 0, 1) ** 2
    arr = (np.array(img.convert("RGB")).astype(np.float64) * factor[..., None]).astype(np.uint8)
    return Image.fromarray(arr)


# ---------------- neutral plaza (1920x1080) ----------------
def plaza():
    W, H = 1920, 1080
    img = vgrad(W, H, (255, 196, 110), (122, 84, 150)).convert("RGBA")
    # sky wash + sun glow (front-right, warm gold, matches CJ-16..20 rim family)
    img = blobs(img, [
        (1400, 260, 420, 300, (255, 222, 150), 150),
        (1500, 300, 180, 140, (255, 244, 200), 200),
        (300, 180, 500, 220, (150, 110, 190), 90),
        (1700, 120, 420, 200, (200, 140, 190), 80),
        (960, 420, 900, 260, (240, 180, 120), 70),
    ], blur=60)
    d = ImageDraw.Draw(img)
    # distant low skyline silhouettes, kept below the sky band, edges clear of centre
    for x, bw, bh, col in [(0, 150, 190, (88, 62, 110)), (160, 110, 150, (104, 74, 122)),
                            (300, 130, 210, (80, 56, 104)), (1450, 140, 180, (96, 68, 118)),
                            (1600, 120, 230, (76, 54, 100)), (1760, 160, 160, (104, 76, 124))]:
        d.rectangle([x, 590 - bh, x + bw, 600], fill=col + (255,))
    # tree canopies at the sides only — centre stays open
    for cx, cy, r in [(180, 480, 150), (330, 520, 110), (1680, 470, 150), (1800, 530, 100)]:
        for dx, dy, rr, col in [(0, 0, r, (96, 110, 74)), (-r // 2, 30, r // 2, (120, 130, 84)),
                                (r // 2, 40, r // 2, (84, 96, 64))]:
            d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=col + (235,))
    # ground: warm paved plaza, perspective converging to centre horizon
    ground = vgrad(W, H - 590, (196, 150, 110), (112, 82, 104))
    img.paste(ground, (0, 590))
    d = ImageDraw.Draw(img)
    for i in range(-8, 9):  # paving joints converging to centre
        d.line([960 + i * 130, 590, 960 + i * 300, 1080], fill=(70, 52, 74, 90), width=3)
    for y in range(620, 1080, 55):  # paving courses, widening toward camera
        d.line([0, y, W, y], fill=(70, 52, 74, 70), width=2)
    # warm sun pool on the ground, centre kept as open standing ground
    img = blobs(img, [(1000, 900, 560, 180, (255, 210, 130), 70),
                      (1400, 700, 380, 110, (255, 190, 110), 55)], blur=70)
    img = strokes(img, 9000, [(255, 210, 140), (150, 110, 170), (120, 90, 140),
                              (240, 180, 120), (100, 80, 120)], (0, 0, W, 590))
    img = strokes(img, 7000, [(200, 160, 120), (140, 110, 110), (255, 205, 130),
                              (90, 66, 96)], (0, 590, W, H))
    img = vignette(grain(img.convert("RGB")), 0.15)
    img.save(f"{OUT}/bg-plaza-neutral-painted-code-20261031.png")
    print("plaza", img.size)


# ---------------- lounge room, warm interior (1920x1280) ----------------
def room():
    W, H = 1920, 1280
    wall_h = 780  # back wall above, wooden floor below; feet line (1180) is on floor
    img = vgrad(W, wall_h, (214, 186, 150), (168, 138, 108)).convert("RGBA")
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wall = vgrad(W, wall_h, (216, 190, 152), (172, 140, 110)).convert("RGBA")
    img.paste(wall, (0, 0))
    floor = vgrad(W, H - wall_h, (150, 104, 66), (96, 64, 42))
    img.paste(floor, (0, wall_h))
    d = ImageDraw.Draw(img)
    # wainscot line + skirting
    d.rectangle([0, wall_h - 14, W, wall_h], fill=(120, 92, 66, 255))
    # window, right of centre (hills view), not behind the character's centre
    wx, wy, ww, wh = 1320, 170, 420, 430
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(88, 62, 48, 255))
    d.rectangle([wx + 16, wy + 16, wx + ww - 16, wy + wh - 16], fill=(150, 190, 205, 255))
    d.polygon([(wx + 16, wy + 300), (wx + ww - 16, wy + 280), (wx + ww - 16, wy + wh - 16),
               (wx + 16, wy + wh - 16)], fill=(120, 150, 96, 255))
    d.rectangle([wx + ww // 2 - 6, wy + 16, wx + ww // 2 + 6, wy + wh - 16], fill=(88, 62, 48, 255))
    d.rectangle([wx + 16, wy + wh // 2 - 6, wx + ww - 16, wy + wh // 2 + 6], fill=(88, 62, 48, 255))
    # bookshelf, left side only
    bx, by, bw, bh = 130, 200, 380, 480
    d.rectangle([bx, by, bx + bw, by + bh], fill=(96, 64, 40, 255))
    for row in range(4):
        y = by + 20 + row * 115
        d.rectangle([bx + 14, y + 90, bx + bw - 14, y + 100], fill=(70, 46, 28, 255))
        for i in range(7):
            x = bx + 22 + i * 48
            col = random.choice([(150, 60, 50), (60, 90, 120), (120, 100, 60), (80, 110, 70), (140, 110, 70)])
            d.rectangle([x, y, x + 34, y + 88], fill=col + (255,))
    # armchair silhouette, far left, back at waist height of a standing figure scale
    d.rounded_rectangle([90, 560, 330, 760], radius=30, fill=(96, 120, 84, 255))
    d.rounded_rectangle([70, 520, 350, 600], radius=30, fill=(110, 134, 96, 255))
    # floor planks converging gently + patterned rug centre-foreground (under feet, not a prop)
    for i in range(-6, 7):
        d.line([960 + i * 150, wall_h, 960 + i * 320, H], fill=(70, 46, 30, 80), width=3)
    d.ellipse([560, 950, 1360, 1210], fill=(150, 90, 80, 255))
    d.ellipse([620, 985, 1300, 1175], fill=(178, 120, 100, 255))
    d.ellipse([700, 1020, 1220, 1140], fill=(150, 90, 80, 255))
    # warm lamp glow, front-left (matches room rim: warm amber 255,180,80)
    img = blobs(img, [(330, 420, 260, 300, (255, 190, 100), 110),
                      (1530, 380, 220, 200, (255, 220, 160), 70),
                      (960, 1080, 500, 130, (255, 200, 120), 45)], blur=80)
    img = strokes(img, 7000, [(230, 200, 160), (170, 140, 110), (120, 95, 70)],
                  (0, 0, W, wall_h))
    img = strokes(img, 6000, [(170, 120, 80), (110, 76, 50), (200, 150, 100)],
                  (0, wall_h, W, H))
    img = vignette(grain(img.convert("RGB")), 0.16)
    img.save(f"{OUT}/bg-room-lounge-painted-code-20261031.png")
    print("room", img.size)


if __name__ == "__main__":
    plaza()
    room()
