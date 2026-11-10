#!/usr/bin/env python3
"""Device prop v2 — hand-fit, industry-standard prop sheet + final shot.
Original vector art in Cape Jones palette. No third-party logo/art copied.
GBA dimensions as METHOD reference only: 144.5 x 82 x 24.5 mm, screen 61.2 x 40.8 mm.
Scale interpretation (Mars 2026-10-31: 'scaled down like times 50, maybe'):
  ~50% of v1 size / hand-fit, NOT 1/50 (which would be invisible). Mars confirms.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.expanduser("~/workspace/cape-jones-rig/device-prop-v2-20261031")
os.makedirs(OUT, exist_ok=True)

BG = (237, 234, 224)
INK = (20, 20, 20)
PURPLE = (90, 39, 114)
PURPLE_DK = (60, 25, 80)
WHITE = (245, 245, 248)
BLACK = (30, 30, 34)
SKIN = (239, 175, 131)
GREEN = (120, 220, 130)
RED = (200, 40, 50)

def font(sz, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()

def rrect(d, box, rad, fill, outline=INK, w=4):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=w)

def device(d, x, y, w, h, screen_label=True):
    """Draw the handheld at (x,y,w,h). Returns screen box."""
    rrect(d, [x, y, x + w, y + h], 28, PURPLE, w=5)
    rrect(d, [x + 10, y + 10, x + w - 10, y + h - 10], 20, WHITE, w=3)
    sw, sh = int(w * 0.52), int(h * 0.44)
    sx, sy = x + int(w * 0.30), y + int(h * 0.14)
    rrect(d, [sx, sy, sx + sw, sy + sh], 10, BLACK, w=4)
    d.rectangle([sx + 6, sy + 6, sx + sw - 6, sy + sh - 6], fill=(140, 230, 150))
    # mini-game: sun + figure + care dots
    d.ellipse([sx + 14, sy + 10, sx + 38, sy + 34], fill=(250, 200, 40))
    d.polygon([(sx + sw - 50, sy + sh - 28), (sx + sw - 30, sy + sh - 28), (sx + sw - 40, sy + sh - 52)], fill=PURPLE)
    d.ellipse([sx + sw - 46, sy + sh - 62, sx + sw - 34, sy + sh - 50], fill=SKIN)
    for i, c in enumerate([(240, 110, 140), (250, 200, 40), (150, 180, 255)]):
        cx = sx + 22 + i * 30
        d.ellipse([cx, sy + sh - 16, cx + 16, sy + sh], fill=c)
    # D-pad
    dx, dy, s = x + int(w * 0.08), y + int(h * 0.60), int(w * 0.11)
    d.rectangle([dx + s // 3, dy, dx + 2 * s // 3, dy + s], fill=BLACK)
    d.rectangle([dx, dy + s // 3, dx + s, dy + 2 * s // 3], fill=BLACK)
    # A/B
    r = int(w * 0.045)
    for i, lab in enumerate("AB"):
        cx = x + int(w * 0.84) + i * int(w * 0.075)
        cy = y + int(h * 0.68)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=INK, width=3)
        d.text((cx, cy), lab, font=font(16), fill=(255, 255, 255), anchor="mm")
    # SELECT / START — labels BELOW buttons, never overlapping speaker
    for i, lab in enumerate(["SELECT", "START"]):
        bx = x + int(w * 0.38) + i * int(w * 0.16)
        by = y + int(h * 0.72)
        rrect(d, [bx, by, bx + int(w * 0.11), by + int(h * 0.07)], 8, BLACK, w=2)
        if h >= 200:
            d.text((bx + int(w * 0.055), by + int(h * 0.07) + 16), lab, font=font(13), fill=INK, anchor="ma")
    # speaker dots, clear of START label
    for i in range(4):
        d.ellipse([x + int(w * 0.70) + i * 7, y + int(h * 0.78), x + int(w * 0.70) + i * 7 + 4, y + int(h * 0.78) + 4], fill=INK)
    return (sx, sy, sw, sh)

def hand(d, x, y, w, h, flip=False):
    """Schematic hand (mitt + thumb), skin tone, for scale/grip diagrams only."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=SKIN, outline=INK, width=3)
    # fingers hint
    for i in range(3):
        d.line([x + 18 + i * 22, y + 8, x + 18 + i * 22, y + 34], fill=(200, 130, 95), width=3)
    # thumb
    if not flip:
        d.ellipse([x + w - 30, y + h - 50, x + w + 22, y + h - 8], fill=SKIN, outline=INK, width=3)
    else:
        d.ellipse([x - 22, y + h - 50, x + 30, y + h - 8], fill=SKIN, outline=INK, width=3)


def device_mini(d, x, y, w, h):
    """Simplified device for tiny grip/gag panels: no care dots, no SELECT labels."""
    rrect(d, [x, y, x + w, y + h], 12, PURPLE, w=3)
    rrect(d, [x + 5, y + 5, x + w - 5, y + h - 5], 9, WHITE, w=2)
    sw, sh = int(w * 0.52), int(h * 0.44)
    sx, sy = x + int(w * 0.30), y + int(h * 0.12)
    rrect(d, [sx, sy, sx + sw, sy + sh], 5, BLACK, w=2)
    d.rectangle([sx + 3, sy + 3, sx + sw - 3, sy + sh - 3], fill=(140, 230, 150))
    dx, dy, s = x + int(w * 0.08), y + int(h * 0.58), int(w * 0.11)
    d.rectangle([dx + s // 3, dy, dx + 2 * s // 3, dy + s], fill=BLACK)
    d.rectangle([dx, dy + s // 3, dx + s, dy + 2 * s // 3], fill=BLACK)
    r = max(5, int(w * 0.04))
    for i, lab in enumerate("AB"):
        cx = x + int(w * 0.84) + i * int(w * 0.07)
        cy = y + int(h * 0.66)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=INK, width=2)
        d.text((cx, cy), lab, font=font(11), fill=(255, 255, 255), anchor="mm")

# ---------------- V2 PROP SHEET ----------------
W, H = 1800, 1350
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.text((40, 24), "MOCHIICHAO HANDHELD — PROP SHEET v2  (original art, Cape Jones palette)", font=font(30), fill=INK)
d.text((40, 62), "Hand-fit scale  •  GBA + Tamagotchi mix  •  no third-party logo  •  separate prop rig, never baked into the body", font=font(20), fill=(70, 70, 70))
d.text((40, 92), "SCALE FIX: v1 was ~295 px wide in the room shot vs a ~260 px seated figure — too big.  v2 = ~50% of v1 (≈148 px in that shot).",
       font=font(20), fill=(150, 30, 30))
d.text((40, 118), "Mars to confirm exact scale: 'times 50, maybe' read as about half / hand-fit, NOT 1/50 (invisible).  Real GBA ref: 144.5 x 82 x 24.5 mm, screen 61.2 x 40.8 mm.",
       font=font(20), fill=(70, 70, 70))

# Row 1: FRONT / BACK / SIDE
d.text((40, 160), "FRONT — detail view", font=font(22), fill=INK)
device(d, 40, 190, 700, 380)
d.text((40, 590), "Screen toward camera. Thumbs on D-pad + A/B. Care row: heart / food / sleep.", font=font(18), fill=(70, 70, 70))

d.text((800, 160), "BACK — detail view", font=font(22), fill=INK)
rrect(d, [800, 190, 1180, 570], 36, BLACK, w=5)
rrect(d, [910, 280, 1070, 400], 12, PURPLE, w=3)
d.text((990, 340), "CARTRIDGE", font=font(20), fill=(255, 255, 255), anchor="mm")
d.text((800, 590), "Cartridge slot. Never seen in normal shots.", font=font(18), fill=(70, 70, 70))

d.text((1240, 160), "SIDE — thickness", font=font(22), fill=INK)
rrect(d, [1300, 190, 1360, 570], 20, PURPLE, w=5)
d.rectangle([1300, 300, 1360, 460], fill=WHITE)
d.text((1330, 590), "24.5 mm thick\n(vs 82 mm tall)", font=font(18), fill=(70, 70, 70), anchor="ma")
# dimension arrow for side
d.line([1400, 190, 1400, 570], fill=INK, width=2)
d.text((1420, 380), "82 mm", font=font(18), fill=INK, anchor="lm")

# Row 2: HAND-SCALE + EXPLODED
d.text((40, 640), "HAND-SCALE — true proportion (this is the size check)", font=font(22), fill=INK)
d.rectangle([40, 670, 880, 950], outline=(160, 160, 160), width=2, fill=(255, 255, 255))
hand(d, 90, 760, 120, 130)
hand(d, 670, 760, 120, 130, flip=True)
device(d, 210, 770, 420, 150)
d.text((460, 935), "Device ≈ two-hand span. Thumbs reach D-pad + A/B without stretching.", font=font(18), fill=(70, 70, 70), anchor="ma")
d.text((460, 700), "144.5 mm wide  •  hand-fit  •  NOT lap-filling", font=font(20), fill=INK, anchor="ma")

d.text((920, 640), "EXPLODED — parts, numbered, no overlaps", font=font(22), fill=INK)
d.rectangle([920, 670, 1760, 950], outline=(160, 160, 160), width=2, fill=(255, 255, 255))
parts = ["1  Screen (garden dance mini-game)", "2  Shell — white / purple rim", "3  D-pad (left thumb)",
         "4  A / B buttons (right thumb)", "5  SELECT / START", "6  Cartridge (back)"]
for i, t in enumerate(parts):
    y = 700 + i * 40
    d.ellipse([950, y, 978, y + 28], fill=PURPLE)
    d.text((964, y + 14), str(i + 1), font=font(16), fill=(255, 255, 255), anchor="mm")
    d.text((990, y + 14), t, font=font(19), fill=INK, anchor="lm")
d.text((920, 965), "Each part is a separate prop-rig piece. Grip poses are prop-rig diagrams, not body pieces.", font=font(18), fill=(70, 70, 70))

# Row 3: GRIP + POCKET GAG (small device, correct size)
d.text((40, 990), "GRIP — one-hand / two-hand / lap (prop rig only)", font=font(22), fill=INK)
for i, lab in enumerate(["1-hand", "2-hand grip*", "Lap (hands at sides)"]):
    x = 40 + i * 290
    d.rectangle([x, 1020, x + 270, 1150], outline=(160, 160, 160), width=2, fill=(255, 255, 255))
    device_mini(d, x + 55, 1045, 160, 62)
    d.text((x + 135, 1130), lab, font=font(17), fill=INK, anchor="ma")
d.text((40, 1165), "* True two-hand grip needs a new arm pose (still owed).", font=font(17), fill=(70, 70, 70))
d.text((40, 1190), "Grip diagram = prop-rig target, not a body pose.", font=font(17), fill=(70, 70, 70))

d.text((950, 990), "POCKET GAG — small device, never a pocket drawn", font=font(22), fill=INK)
for i, lab in enumerate(["1. Hand to hip", "2. Device appears", "3. Hand back — gone"]):
    x = 950 + i * 270
    d.rectangle([x, 1020, x + 250, 1150], outline=(160, 160, 160), width=2, fill=(220, 220, 230))
    d.polygon([(x + 60, 1035), (x + 190, 1035), (x + 175, 1140), (x + 75, 1140)], fill=PURPLE)
    d.ellipse([x + 110, 1070, x + 140, 1100], fill=SKIN)
    if i == 1:
        device_mini(d, x + 150, 1085, 70, 32)
    d.text((x + 125, 1130), lab, font=font(17), fill=INK, anchor="ma") if False else None
    # labels below panel to avoid overlap with art
d.text((950, 1165), "Gag: ALWAYS in his pocket, NO visible pockets.", font=font(17), fill=(70, 70, 70))
d.text((950, 1190), "Glow/beep announces it — never a pocket drawn.", font=font(17), fill=(70, 70, 70))
d.text((950, 1215), "Full labels: see PROP-DESIGN-METHOD-V2.", font=font(17), fill=(70, 70, 70))

img.save(f"{OUT}/device-prop-sheet-v2-20261031.png")
print("sheet saved", img.size)

# ---------------- FINAL SHOT V2 (re-composite proof) ----------------
room = Image.open(os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets/backgrounds/batch-KKGuh.jpg")).convert("RGB")
v1 = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/mochiichao-combine-build-20261031/device-in-final-shot-room-20261031.png")).convert("RGB")
# Start from v1, erase old device by pasting clean room over its bbox, then
# restore the seated figure area above the device from v1 (same source, so it matches),
# then paste a 50%-scaled device at the same lap centre.
out = v1.copy()
room_crop = room.crop((680, 630, 990, 775))
# Replace ONLY device-like pixels in the old device box with clean room pixels,
# keeping figure/rug pixels that were never part of the device.
for yy in range(630, 775):
    for xx in range(680, 990):
        r, g, b = v1.getpixel((xx, yy))
        is_purple = abs(r - 90) < 45 and abs(g - 39) < 45 and abs(b - 114) < 45
        is_face = 238 <= r <= 250 and 238 <= g <= 250 and 242 <= b <= 252
        is_green = g > 180 and r < 180 and b < 180
        is_red = r > 170 and g < 80 and b < 80
        is_black_btn = r < 60 and g < 60 and b < 60
        if is_purple or is_face or is_green or is_red or is_black_btn:
            out.putpixel((xx, yy), room_crop.getpixel((xx - 680, yy - 630)))
# figure legs/torso above device top are already in v1 outside the erased box; nothing else needed.
# Clear the lower strip (y720-775) outright: figure legs end above ~710, so this
# strip is only old-device ghost fragments + rug. This removes the last ghost outline.
out.paste(room.crop((680, 720, 990, 775)), (680, 720))
# Draw a FRESH hand-fit device (no v1 crop fragments) and paste it at the lap centre.
# 148x65 = 50% of the v1 device (295x130), same centre as v1.
dev_img = Image.new("RGBA", (300, 130), (0, 0, 0, 0))
dd = ImageDraw.Draw(dev_img)
device(dd, 0, 0, 300, 130)
dev_small = dev_img.resize((148, 65), Image.LANCZOS)
cx, cy = (690 + 985) // 2, (640 + 770) // 2
# Clear the thin old-device top edge to the right of the new device (figure is left of x911 here).
out.paste(room.crop((911, 630, 990, 673)), (911, 630))
out.paste(dev_small, (cx - 74, cy - 32), dev_small)
out.save(f"{OUT}/device-in-final-shot-v2-20261031.png")
print("final shot saved", out.size, "v1 device 295x130 -> v2 148x65, centre", (cx, cy))
