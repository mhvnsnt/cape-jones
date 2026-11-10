#!/usr/bin/env python3
"""V2 code-painted plaza + lounge room. V1 was viewed and rejected by this lane:
flat circles/rectangles + scratch-static texture, not painterly enough next to
the four media-generated paintings. V2 changes: large soft cloud/wash blobs
instead of scratch strokes as the main texture, blurred foliage clusters,
lit-window skylines, drop shadows, light shafts, longer low-alpha strokes,
and a final soft blur + light grain. Still code-painted (PIL) — labelled as
such in the manifest/report, never claimed as media-generated. No character,
no text, no logos; centre foreground kept clear."""
import random, math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

random.seed(777)
OUT = "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/masters"


def vgrad(w, h, top, bottom):
    t = np.linspace(0, 1, h)[:, None]
    arr = np.zeros((h, w, 3), dtype=np.float64)
    for i in range(3):
        arr[:, :, i] = top[i] * (1 - t) + bottom[i] * t
    return Image.fromarray(arr.astype(np.uint8))


def blobs(img, items, blur=50):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for cx, cy, rx, ry, col, a in items:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col + (a,))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))
    return img


def wash(img, n, palette, region, rmin=60, rmax=260, amin=12, amax=45, blur=45):
    x0, y0, x1, y1 = region
    items = []
    for _ in range(n):
        items.append((random.randint(x0, x1), random.randint(y0, y1),
                      random.randint(rmin, rmax), random.randint(rmin // 2, rmax // 2),
                      random.choice(palette), random.randint(amin, amax)))
    return blobs(img, items, blur=blur)


def soft_strokes(img, n, palette, region):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = region
    for _ in range(n):
        x, y = random.randint(x0, x1), random.randint(y0, y1)
        ang = random.uniform(-0.4, 0.4)
        ln = random.randint(30, 140)
        d.line([x, y, x + ln * math.cos(ang), y + ln * math.sin(ang)],
               fill=random.choice(palette) + (random.randint(8, 30),),
               width=random.randint(3, 10))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.6)))
    return img


def finish(img, blur=0.8, grain_amt=6):
    img = img.convert("RGB").filter(ImageFilter.GaussianBlur(blur))
    arr = np.array(img).astype(np.int16)
    noise = np.random.randint(-grain_amt, grain_amt + 1, arr.shape[:2])[..., None]
    return Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))


def plaza():
    W, H = 1920, 1080
    horizon = 600
    img = vgrad(W, horizon, (255, 198, 112), (150, 108, 168)).convert("RGBA")
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sky = vgrad(W, horizon, (255, 198, 112), (150, 108, 168)).convert("RGBA")
    img.paste(sky, (0, 0))
    # sun glow upper-right + cloud washes
    img = blobs(img, [(1420, 240, 380, 260, (255, 228, 160), 160),
                      (1500, 280, 150, 110, (255, 246, 210), 200)], blur=70)
    img = wash(img, 46, [(255, 220, 170), (200, 150, 200), (240, 190, 140), (170, 130, 190)],
               (0, 0, W, horizon), rmin=90, rmax=300, blur=55)
    d = ImageDraw.Draw(img)
    # skyline: varied heights, warm lit windows, haze at its base — centre low
    xs = 0
    while xs < W:
        bw = random.randint(90, 190)
        bh = random.randint(90, 260) if not (650 < xs < 1270) else random.randint(60, 120)
        col = random.choice([(94, 66, 116), (110, 80, 128), (82, 58, 106)])
        d.rectangle([xs, horizon - bh, xs + bw, horizon], fill=col + (255,))
        for _ in range(bw // 14):
            wx = xs + random.randint(8, max(9, bw - 14))
            wy = horizon - bh + random.randint(10, max(11, bh - 20))
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 7, wy + 9], fill=(255, 205, 110, 230))
        xs += bw + random.randint(4, 30)
    img = blobs(img, [(960, horizon - 20, 900, 90, (240, 180, 130), 60)], blur=40)
    # ground
    ground = vgrad(W, H - horizon, (206, 160, 118), (118, 88, 108)).convert("RGBA")
    img.paste(ground, (0, horizon))
    d = ImageDraw.Draw(img)
    for i in range(-9, 10):
        d.line([960 + i * 120, horizon, 960 + i * 310, H], fill=(74, 56, 78, 60), width=3)
    for y in range(horizon + 30, H, 48):
        d.line([0, y, W, y], fill=(74, 56, 78, 45), width=2)
    # trees: blurred foliage clusters + trunks, sides only
    for tx, ty, s in [(200, 470, 1.0), (380, 520, 0.7), (1700, 460, 1.0), (1540, 520, 0.7)]:
        d.rectangle([tx - 10, ty + 60, tx + 10, horizon], fill=(70, 52, 40, 255))
        items = []
        for _ in range(16):
            items.append((tx + random.randint(-110, 110) * s, ty + random.randint(-80, 60),
                          random.randint(40, 90), random.randint(30, 70),
                          random.choice([(96, 118, 74), (120, 134, 84), (80, 100, 62)]), 200))
        img = blobs(img, items, blur=22)
        d = ImageDraw.Draw(img)
    img = blobs(img, [(1020, 920, 560, 170, (255, 212, 132), 65),
                      (1420, horizon + 60, 360, 90, (255, 196, 110), 50)], blur=70)
    img = soft_strokes(img, 2600, [(255, 214, 150), (160, 120, 175), (120, 92, 140)],
                       (0, 0, W, H))
    img = finish(img)
    img.save(f"{OUT}/bg-plaza-neutral-painted-code-20261031.png")
    print("plaza v2", img.size)


def room():
    W, H = 1920, 1280
    wall_h = 780
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.paste(vgrad(W, wall_h, (222, 196, 158), (178, 146, 114)).convert("RGBA"), (0, 0))
    img.paste(vgrad(W, H - wall_h, (156, 110, 70), (100, 66, 44)).convert("RGBA"), (0, wall_h))
    img = wash(img, 30, [(235, 210, 170), (190, 158, 122), (210, 180, 140)],
               (0, 0, W, wall_h), rmin=120, rmax=340, blur=60)
    d = ImageDraw.Draw(img)
    d.rectangle([0, wall_h - 12, W, wall_h], fill=(118, 90, 64, 255))
    # shadows first, then furniture (softened by final blur)
    d.rectangle([150, 700, 540, 730], fill=(60, 44, 30, 90))
    d.rectangle([1330, 630, 1770, 660], fill=(60, 44, 30, 90))
    # bookshelf, left, books of varied height/colour
    bx, by, bw = 140, 190, 380
    d.rectangle([bx, by, bx + bw, by + 490], fill=(98, 66, 42, 255))
    for row in range(4):
        y = by + 16 + row * 118
        d.rectangle([bx + 12, y + 96, bx + bw - 12, y + 106], fill=(72, 48, 30, 255))
        x = bx + 20
        while x < bx + bw - 40:
            wbook = random.randint(22, 40)
            hbook = random.randint(70, 94)
            col = random.choice([(152, 62, 52), (62, 92, 122), (122, 102, 62), (82, 112, 72), (142, 112, 72)])
            d.rectangle([x, y + 96 - hbook, x + wbook, y + 96], fill=col + (255,))
            x += wbook + random.randint(2, 8)
    # armchair, far left
    d.rounded_rectangle([80, 540, 340, 760], radius=34, fill=(104, 128, 90, 255))
    d.rounded_rectangle([60, 500, 360, 590], radius=34, fill=(118, 142, 102, 255))
    # window, right, with hills + soft daylight shaft onto the floor
    wx, wy, ww, wh = 1330, 170, 420, 430
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(88, 62, 48, 255))
    d.rectangle([wx + 16, wy + 16, wx + ww - 16, wy + wh - 16], fill=(152, 192, 206, 255))
    d.polygon([(wx + 16, wy + 300), (wx + ww - 16, wy + 280), (wx + ww - 16, wy + wh - 16),
               (wx + 16, wy + wh - 16)], fill=(122, 152, 98, 255))
    d.rectangle([wx + ww // 2 - 6, wy + 16, wx + ww // 2 + 6, wy + wh - 16], fill=(88, 62, 48, 255))
    d.rectangle([wx + 16, wy + wh // 2 - 6, wx + ww - 16, wy + wh // 2 + 6], fill=(88, 62, 48, 255))
    # floor planks: alternating tones + perspective joints
    for i in range(-6, 7):
        d.line([960 + i * 150, wall_h, 960 + i * 320, H], fill=(72, 48, 30, 55), width=3)
    # rug with soft shadow, centre foreground
    d.ellipse([540, 940, 1380, 1230], fill=(60, 40, 28, 70))
    d.ellipse([560, 950, 1360, 1210], fill=(152, 92, 82, 255))
    d.ellipse([620, 985, 1300, 1175], fill=(180, 122, 102, 255))
    d.ellipse([700, 1020, 1220, 1140], fill=(152, 92, 82, 255))
    img = blobs(img, [(330, 420, 280, 320, (255, 192, 102), 100),
                      (1540, 390, 220, 200, (255, 222, 162), 60),
                      (1500, 900, 420, 180, (255, 205, 130), 35)], blur=80)
    img = soft_strokes(img, 2200, [(236, 206, 166), (176, 144, 112), (200, 156, 104)],
                       (0, 0, W, H))
    img = finish(img)
    img.save(f"{OUT}/bg-room-lounge-painted-code-20261031.png")
    print("room v2", img.size)


if __name__ == "__main__":
    plaza()
    room()
