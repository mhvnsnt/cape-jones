"""JoJo DREAM variation sheet — palette replacement (v3 method).
Base plate: rig-apose-v7c-clean-transparent.png (clean, labels=False plate).
Method: nearest-base-colour classification, new = shifted + (pixel - base), clamped.
Black outline NEVER reassigned. V3 doc untouched; see addendum file.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = "/home/hatch/workspace/cape-jones-rig/jojo-shift-variation-20261031"
PLATE = "/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png"

BASE = {
    "cowl": (90, 39, 114),
    "skin": (239, 175, 131),
    "suit": (255, 255, 255),
    "suit_shadow": (178, 186, 199),
    "cape": (23, 21, 26),
    "outline": (0, 0, 0),
}
# DREAM (v3): cowl turquoise, skin pink-tinted, eye ice
# Mars 16:35 refinement: cape = FULL colour (not dark tint, not pure black);
# suit = white in A, changed in B. Cape held constant across A/B to isolate suit choice.
VAR_A = {
    "cowl": (40, 200, 210), "skin": (255, 200, 180), "suit": (255, 255, 255),
    "suit_shadow": (178, 186, 199), "cape": (255, 60, 180), "outline": (0, 0, 0),
    "eye": (220, 250, 255),
}
VAR_B = {
    "cowl": (40, 200, 210), "skin": (255, 200, 180), "suit": (255, 205, 90),
    "suit_shadow": (200, 150, 70), "cape": (255, 60, 180), "outline": (0, 0, 0),
    "eye": (220, 250, 255),
}

def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def recolor(img, mapping):
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            # nearest base colour
            best, bestd = None, 1e9
            for name, bc in BASE.items():
                d = dist((r, g, b), bc)
                if d < bestd:
                    best, bestd = name, d
            if best is None or bestd > 110:
                continue  # belt, boots, etc.: leave untouched
            sc = mapping[best]
            nr = max(0, min(255, sc[0] + (r - BASE[best][0])))
            ng = max(0, min(255, sc[1] + (g - BASE[best][1])))
            nb = max(0, min(255, sc[2] + (b - BASE[best][2])))
            px[x, y] = (nr, ng, nb, a)
    return img

plate = Image.open(PLATE)
base_img = plate.copy()
a_img = recolor(plate, VAR_A)
b_img = recolor(plate, VAR_B)

# Sheet: 3 panels on grey-128 control background, labels + swatches
PW = 380  # panel width
PH = 520  # plate height scaled
GAP = 30
TOP = 90
SW = 120
sheet_w = GAP + 3 * (PW + GAP)
sheet_h = TOP + PH + SW + 40
sheet = Image.new("RGB", (sheet_w, sheet_h), (128, 128, 128))
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except Exception:
    font = small = tiny = ImageFont.load_default()

panels = [
    ("C — BASE (canon)", base_img, [("Cowl", (90,39,114)), ("Cape", (23,21,26)), ("Suit", (255,255,255))]),
    ("A — DREAM: cape FULL colour, suit WHITE", a_img, [("Cowl", (40,200,210)), ("Cape", (255,60,180)), ("Suit", (255,255,255))]),
    ("B — DREAM: cape FULL colour, suit CHANGED", b_img, [("Cowl", (40,200,210)), ("Cape", (255,60,180)), ("Suit", (255,205,90))]),
]
d.text((GAP, 15), "JoJo DREAM variation — cape full colour, suit white OR changed (Mars 2026-10-31 16:35 CDT)", fill=(255,255,255), font=small)
d.text((GAP, 42), "Helm/cowl turquoise in both shifts. Cape = full magenta-pink, NOT black, NOT dark tint. Suit: white in A, gold in B.", fill=(255,255,255), font=tiny)
d.text((GAP, 62), "Creator-feel rule: choice is per beat, what looks cool — recorded in shot spec, not a formula.", fill=(255,255,255), font=tiny)

for i, (label, img, swatches) in enumerate(panels):
    x0 = GAP + i * (PW + GAP)
    # scale plate to PW x PH preserving aspect (plate 1100x1500)
    thumb = img.copy()
    thumb.thumbnail((PW, PH), Image.LANCZOS)
    # paste centred on white-ish panel? Use transparent over grey: paste with mask
    bg = Image.new("RGBA", (PW, PH), (128, 128, 128, 255))
    bg.alpha_composite(thumb, ((PW - thumb.width)//2, (PH - thumb.height)//2))
    sheet.paste(bg.convert("RGB"), (x0, TOP))
    d.text((x0, TOP + PH + 8), label, fill=(255,255,255), font=small)
    sx = x0
    for name, col in swatches:
        d.rectangle([sx, TOP + PH + 38, sx + 34, TOP + PH + 68], fill=col, outline=(0,0,0))
        d.text((sx, TOP + PH + 72), f"{name} {col}", fill=(255,255,255), font=tiny)
        sx += 130

out = os.path.join(OUT, "jojo-dream-variation-cape-full-suit-white-or-changed-20261031.png")
sheet.save(out)
print("saved", out, sheet.size)
# also save individual variant panels for reuse
for name, img in [("base", base_img), ("dream-a-cape-full-suit-white", a_img), ("dream-b-cape-full-suit-gold", b_img)]:
    p = os.path.join(OUT, f"jojo-dream-{name}-20261031.png")
    img.save(p)
    print("saved", p, img.size)
