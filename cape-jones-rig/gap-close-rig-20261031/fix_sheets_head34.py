"""Fixes from own-eyes viewing:
- 3/4 v3 far eye: the first build squeezed the wrong zone (x6-26) and left a
  double-eye smudge; the real far eye in the warped head is x17-31. v3b clears
  x15-33 and pastes the squeezed eye there.
- Sheets used PIL's tiny bitmap font, so titles/labels looked merged. v2 sheets
  use DejaVuSans TTF with short labels.
- Bone-chain diagram: hem joints were chained B3->B4->B5 (a line across the hem
  and a floating centre dot). v2 fans B2 -> each hem joint, and B5 sits on the hem.
Originals kept as drafts; v2/v3b files are the deliverables.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

OUT = "/home/hatch/workspace/cape-jones-rig/gap-close-rig-20261031"
RIG = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(RIG, "sliced")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
COWL = (92, 40, 115, 255)

def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)

# --- 3/4 head v3b
head = Image.open(os.path.join(BASE, "Head_Front.png")).convert("RGBA")
W0, H0 = head.size
left = head.crop((0, 0, 59, H0)).resize((41, H0), Image.LANCZOS)
right = head.crop((59, 0, W0, H0)).resize((58, H0), Image.LANCZOS)
out = Image.new("RGBA", (100, H0), (0, 0, 0, 0))
out.paste(left, (0, 0), left); out.paste(right, (41, 0), right)
eye = out.crop((15, 66, 33, 86))
eye_s = eye.resize((14, 20), Image.LANCZOS)
d = ImageDraw.Draw(out); d.rectangle((15, 66, 33, 86), fill=COWL)
out.paste(eye_s, (17, 66), eye_s)
arr = np.array(out).astype(np.int16)
strip = (np.arange(100)[None, :] >= 38) & (np.arange(100)[None, :] <= 41)
rows = (np.arange(H0)[:, None] >= 65) & (np.arange(H0)[:, None] <= 95)
zone = strip & rows
for ch in range(3):
    arr[:, :, ch] = np.where(zone & (arr[:, :, 3] > 10), (arr[:, :, ch]*0.65).astype(np.int16), arr[:, :, ch])
out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
out.save(os.path.join(OUT, "gap-close-head-34-v3b-kitbash-20261031.png"))
print("head34 v3b saved", out.size)
# v3b sheet with TTF text
s = Image.new("RGBA", (1000, 430), (128, 128, 128, 255)); d = ImageDraw.Draw(s)
d.text((12, 10), "3/4 HEAD v3b - DERIVED KITBASH, NOT a true hand-drawn 3/4", fill=(255, 255, 0, 255), font=font(20, True))
big = out.resize((200, 344), Image.LANCZOS); s.paste(big, (40, 55), big)
ref = out.resize((200, 344), Image.LANCZOS); s.paste(ref, (300, 55), ref)
d.line([(300+82, 55), (300+82, 399)], fill=(255, 0, 0, 255), width=2)
d.line([(300, 55+150), (500, 55+150)], fill=(255, 0, 0, 255), width=2)
notes = ["Far side (image-left) 0.70x", "Near side 0.97x; far eye x0.80", "Bridge-occlusion strip x38-41",
         "Clean piece (left) has NO lines.", "BLOCKER for a true 3/4: needs a",
         "hand-drawn master; warps cannot", "redraw linework. This kitbash",
         "is the working replacement."]
for i, t in enumerate(notes):
    d.text((560, 80+i*30), t, fill=(255, 255, 255, 255), font=font(17))
s.save(os.path.join(OUT, "gap-close-head-34-v3b-sheet-20261031.png"))
print("head34 v3b sheet saved")

# --- catalogue v2 with short labels + TTF
short = [("gap-close-neck-01-base-20261031.png", "neck 01 base"),
         ("gap-close-neck-02-short-20261031.png", "neck 02 short"),
         ("gap-close-neck-03-long-20261031.png", "neck 03 long"),
         ("gap-close-neck-04-tilt-left-20261031.png", "neck 04 tilt L"),
         ("gap-close-neck-05-tilt-right-long-20261031.png", "neck 05 tilt R long"),
         ("gap-close-head-blank-20261031.png", "head blank"),
         ("gap-close-head-blank-normal-eyes-20261031.png", "head + normal eyes"),
         ("gap-close-head-blank-comedic-eyes-20261031.png", "head + comedic eyes"),
         ("gap-close-head-blank-angry-20261031.png", "head + angry"),
         ("gap-close-head-furious-faceangry-normaleyes-20261031.png", "head furious"),
         ("gap-close-foot-left-20261031.png", "foot left"),
         ("gap-close-foot-right-20261031.png", "foot right"),
         ("gap-close-gauntlet-arm1-20261031.png", "gauntlet arm1"),
         ("gap-close-gauntlet-arm2-20261031.png", "gauntlet arm2")]
cols, cw, ch = 4, 300, 230
rows = (len(short)+cols-1)//cols
s = Image.new("RGBA", (cols*cw, rows*(ch+36)+56), (128, 128, 128, 255)); d = ImageDraw.Draw(s)
d.text((12, 10), "GAP-CLOSE MISSING PIECES - catalogue (labels on sheet only, never on pieces)", fill=(255, 255, 0, 255), font=font(19, True))
for i, (f, lab) in enumerate(short):
    r, cc = divmod(i, cols); x, y = cc*cw, 56+r*(ch+36)
    im = Image.open(os.path.join(OUT, f)).convert("RGBA"); im.thumbnail((cw-16, ch-16), Image.LANCZOS)
    s.paste(im, (x+(cw-im.size[0])//2, y+(ch-im.size[1])//2), im)
    d.text((x+8, y+ch+6), lab, fill=(255, 255, 0, 255), font=font(16))
s.save(os.path.join(OUT, "gap-close-missing-pieces-catalogue-v2-20261031.png"))
print("catalogue v2 saved", s.size)

# --- bone-chain diagram v2 (fan, not chain, at the hem)
cape_full = Image.open(os.path.join(BASE, "Cape_Back_Main.png")).convert("RGBA")
diag = Image.new("RGBA", (1100, 1000), (128, 128, 128, 255))
cape_d = cape_full.resize((490, 833), Image.LANCZOS); diag.paste(cape_d, (60, 90), cape_d)
d = ImageDraw.Draw(diag)
d.text((12, 10), "CAPE BONE-CHAIN - diagram (labels on sheet only). Lag 1-2 frames.", fill=(255, 255, 0, 255), font=font(19, True))
hub = (305, 620)
for name, (x, y) in [("B0 neck", (305, 130)), ("B1 mid-back", (305, 380)), ("B2 mid-cape", hub),
                     ("B3 hem-L", (110, 880)), ("B4 hem-R", (500, 880)), ("B5 hem-C", (305, 885))]:
    pass
d.line([(305, 130), (305, 380)], fill=(255, 0, 0, 255), width=4)
d.line([(305, 380), hub], fill=(255, 0, 0, 255), width=4)
for hx, hy in [(110, 880), (500, 880), (305, 885)]:
    d.line([hub, (hx, hy)], fill=(255, 0, 0, 255), width=4)
for name, (x, y) in [("B0 neck", (305, 130)), ("B1 mid-back", (305, 380)), ("B2 mid-cape", hub),
                     ("B3 hem-L", (110, 880)), ("B4 hem-R", (500, 880)), ("B5 hem-C", (305, 885))]:
    d.ellipse((x-18, y-18, x+18, y+18), fill=(255, 0, 0, 255), outline=(255, 255, 255, 255), width=3)
    d.text((x+24, y-10), name, fill=(255, 255, 255, 255), font=font(16))
notes = ["Chain: neck -> mid-back -> mid-cape", "-> hem fan: L / C / R.",
         "Follow-through: each bone lags the", "one above it by 1-2 frames; hem",
         "moves last and farthest.",
         "Cape is a SEPARATE prop-rig layer:", "body file + cape file + composite",
         "are delivered separately. Cape is", "NOT baked into the body."]
for i, t in enumerate(notes):
    d.text((620, 150+i*30), t, fill=(255, 255, 255, 255), font=font(17))
diag.save(os.path.join(OUT, "gap-close-cape-bone-chain-diagram-v2-20261031.png"))
print("bone-chain v2 saved")
