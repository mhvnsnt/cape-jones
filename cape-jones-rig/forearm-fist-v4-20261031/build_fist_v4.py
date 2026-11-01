"""Build TRUE front-facing punching fist v4 (Mars correction 2026-10-31 16:41 CDT).
V3 file is palm/upward-facing, NOT front-facing. This is a new original vector
fist drawn in Cape Jones palette (white glove, black outline, grey shading):
- knuckles at TOP, facing the camera/viewer, 4 knuckle bumps in a row
- NO palm visible (palm is the opposite side; v3 showed palm/finger-pads side-on)
- thumb wrapped ACROSS the front of the fingers (diagonal band, lower front)
- wrist/cuff at the BOTTOM (attachment end) in standalone orientation
Supersampled PIL drawing, downscaled with LANCZOS. No copied show art.
"""
from PIL import Image, ImageDraw

SS = 4
W, H = 300 * SS, 340 * SS
WHITE = (255, 255, 255, 255)
GREY = (205, 212, 222, 255)
GREY2 = (178, 186, 199, 255)
BLACK = (0, 0, 0, 255)
OUT = 5 * SS  # outline width at supersample scale

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

def rr(box, r, fill, outline=None, width=OUT):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def ellipse(box, fill, outline=None, width=OUT):
    d.ellipse(box, fill=fill, outline=outline, width=width)

# --- fist body: back-of-hand mass, wider at knuckles, tapering to wrist ---
# main body
rr([62*SS, 62*SS, 238*SS, 268*SS], 42*SS, WHITE, BLACK)
# --- knuckles: 4 bumps across the TOP, facing camera ---
# index highest, middle next, ring, pinky slightly lower / smaller (never flat, never palm)
knuckles = [
    (72, 52, 122, 104),   # index
    (122, 46, 176, 102),  # middle (tallest)
    (176, 50, 226, 104),  # ring
    (226, 58, 262, 104),  # pinky (smaller, lower)
]
for (x0, y0, x1, y1) in knuckles:
    rr([x0*SS, y0*SS, x1*SS, y1*SS], 22*SS, WHITE, BLACK)
# knuckle highlight caps (small white-grey arcs on each knuckle face)
for (x0, y0, x1, y1) in knuckles:
    d.ellipse([ (x0+10)*SS, (y0+8)*SS, (x1-10)*SS, (y0+34)*SS ], fill=(235, 238, 244, 255))
# seams between knuckles: short vertical creases descending from knuckle gaps
for x in (122, 176, 226):
    d.line([(x*SS, 92*SS), (x*SS, 132*SS)], fill=BLACK, width=4*SS)
# finger-curl crease: one shallow arc below the knuckle row (fingers curled AWAY,
# not palm pads) -- shows the fist is clenched toward camera, not open palm
d.arc([80*SS, 120*SS, 250*SS, 210*SS], start=20, end=160, fill=BLACK, width=4*SS)
d.arc([95*SS, 150*SS, 235*SS, 225*SS], start=20, end=160, fill=(90, 95, 105, 255), width=3*SS)

# --- shading: cool grey on right + lower mass, clipped by body shape ---
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ds = ImageDraw.Draw(shade)
ds.polygon([(190*SS, 100*SS), (238*SS, 100*SS), (238*SS, 268*SS), (180*SS, 268*SS)], fill=(190, 198, 210, 130))
ds.ellipse([(150*SS, 200*SS), (250*SS, 280*SS)], fill=(190, 198, 210, 90))
# clip shade to fist body alpha: redraw body as mask
mask = Image.new("L", (W, H), 0)
dm = ImageDraw.Draw(mask)
dm.rounded_rectangle([62*SS, 62*SS, 238*SS, 268*SS], radius=42*SS, fill=255)
for (x0, y0, x1, y1) in knuckles:
    dm.rounded_rectangle([x0*SS, y0*SS, x1*SS, y1*SS], radius=22*SS, fill=255)
img.paste(Image.alpha_composite(img, shade), (0, 0), mask)
d = ImageDraw.Draw(img)
# re-outline body after shading (shade paste softens edges)
d.rounded_rectangle([62*SS, 62*SS, 238*SS, 268*SS], radius=42*SS, outline=BLACK, width=OUT)
for (x0, y0, x1, y1) in knuckles:
    d.rounded_rectangle([x0*SS, y0*SS, x1*SS, y1*SS], radius=22*SS, outline=BLACK, width=OUT)

# --- thumb: wrapped ACROSS the FRONT of the fingers, diagonal band ---
# thumb runs from lower-left front, diagonally up-right across the finger mass,
# tip ending mid-right. This is the front wrap, not a side thumb.
thumb = [(70, 196), (120, 172), (210, 196), (238, 224), (200, 250), (110, 240)]
d.polygon([(x*SS, y*SS) for x, y in thumb], fill=WHITE, outline=BLACK, width=OUT)
# thumb tip cap + thumbnail crease
d.ellipse([(196*SS, 196*SS), (238*SS, 232*SS)], fill=(235, 238, 244, 255))
d.line([(196*SS, 206*SS), (222*SS, 214*SS)], fill=BLACK, width=3*SS)
# thumb base crease
d.arc([70*SS, 180*SS, 140*SS, 245*SS], start=280, end=60, fill=BLACK, width=4*SS)

# --- wrist / gauntlet cuff at bottom (attachment end) ---
rr([92*SS, 258*SS, 212*SS, 312*SS], 14*SS, WHITE, BLACK)
d.line([(92*SS, 282*SS), (212*SS, 282*SS)], fill=BLACK, width=4*SS)
d.line([(100*SS, 258*SS), (100*SS, 312*SS)], fill=(150, 158, 170, 255), width=2*SS)

# downscale
out = img.resize((300, 340), Image.LANCZOS)
# fringe clean: drop near-transparent edge pixels
px = out.load()
for y in range(340):
    for x in range(300):
        r, g, b, a = px[x, y]
        if a < 40:
            px[x, y] = (0, 0, 0, 0)
out.save("/home/hatch/workspace/cape-jones-rig/forearm-fist-v4-20261031/fist-front-facing-punch-v4-20261031.png")
print("saved", out.size)

# ---- seated forearm: v3 standard-clean forearm, fist replaced ----
import os
base_p = "/home/hatch/workspace/cape-jones-rig/forearm-fist-v3-20261031/forearm-v3-arm2-standard-clean-20261031.png"
base = Image.open(base_p).convert("RGBA")
# keep forearm + wrist above y=108, erase everything below (old fist)
canvas = Image.new("RGBA", (320, 340), (0, 0, 0, 0))
crop = base.crop((0, 0, base.size[0], 108))
canvas.paste(crop, (35, 0), crop)
# wrist cap BEHIND fist: white disc with black outline, centred on wrist
cap_layer = Image.new("RGBA", (320, 340), (0, 0, 0, 0))
dc = ImageDraw.Draw(cap_layer)
cx, cy, r = 35 + 175, 102, 42
dc.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=BLACK, width=6)
canvas = Image.alpha_composite(canvas, cap_layer)
# seated fist = standalone rotated 180 deg: knuckles go to strike edge (bottom),
# still facing camera (in-plane rotation preserves facing), thumb ends LEFT (Arm2)
seated = out.rotate(180)
# seat: fist top (its wrist, after rotation) overlaps wrist cap by ~28px
canvas.paste(seated, (35 + 175 - 150, 102 - 28), seated)
# re-draw cap side arcs? cap is behind fist by construction (pasted before fist),
# so only arcs outside fist silhouette peek -- correct v7c language, no ring on face.
canvas.save("/home/hatch/workspace/cape-jones-rig/forearm-fist-v4-20261031/forearm-v4-arm2-front-punch-fist-20261031.png")
print("seated saved", canvas.size)
