#!/usr/bin/env python3
import os, json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "duplicates-upgrade-true-vs-near-20261031/contacts")
R = os.path.join(ROOT, "sliced-68-unsliced-20261031/sheets/fla-packs")
S = os.path.join(ROOT, "sliced-clean-20261031/F-fla-packs")
true_a = os.path.join(R, "clean-DGb2j/Row1_1.png")
true_b = os.path.join(R, "lounge-DGb2j/Row1_1.png")  # same MD5 as true_a
near_a = os.path.join(S, "dance-2e9kj/Row1_10.png")   # near, same pattern row, different detail
ref = true_a

def checker(w, h, cell=16):
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            if (x//cell + y//cell) % 2: d.rectangle([x, y, x+cell-1, y+cell-1], fill=(200, 200, 200))
    return img

def paste_fit(base, im, x, y, h):
    im = im.convert("RGBA")
    s = h / im.height
    im2 = im.resize((max(1, int(im.width*s)), h), Image.LANCZOS)
    base.alpha_composite(im2, (x, y))
    return im2.size

def diffmap(pa, pb, size=256):
    a = Image.open(pa).convert("RGBA").resize((size, size), Image.LANCZOS)
    b = Image.open(pb).convert("RGBA").resize((size, size), Image.LANCZOS)
    aa, bb = np.asarray(a, dtype=int), np.asarray(b, dtype=int)
    diff = np.abs(aa[:, :, :3] - bb[:, :, :3]).mean(axis=2)
    # red highlight where diff>30, grey otherwise
    out = np.zeros((size, size, 3), dtype=np.uint8)
    out[:, :, 0] = np.clip(diff*3, 0, 255).astype(np.uint8)
    out[:, :, 1] = (diff > 30) * 0
    out[:, :, 2] = (diff > 30) * 0
    # keep grey diff as green channel for visibility
    out[:, :, 1] = np.clip(diff, 0, 255).astype(np.uint8)
    return Image.fromarray(out), float(diff.mean()), float((diff > 30).mean())

# Contact 1: TRUE pair vs NEAR pair
W, H = 1200, 560
img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d = ImageDraw.Draw(img)
for x0, label in [(0, "TRUE PAIR - identical (same MD5)"), (600, "NEAR PAIR - same row/pattern, different detail")]:
    d.rectangle([x0, 0, x0+600, 40], fill=(30, 30, 30))
    d.text((x0+10, 10), label, fill=(255, 255, 255))
paste_fit(img, Image.open(true_a), 60, 60, 400)
paste_fit(img, Image.open(true_b), 320, 60, 400)
paste_fit(img, Image.open(ref), 660, 60, 400)
paste_fit(img, Image.open(near_a), 920, 60, 400)
d.text((10, 480), "Left: clean-DGb2j Row1_1  ==  lounge-DGb2j Row1_1 (byte-identical)", fill=(0, 0, 0))
d.text((610, 480), "Right: clean-DGb2j Row1_1  vs  dance-2e9kj Row1_10 (same outline, interior differs)", fill=(0, 0, 0))
img.convert("RGB").save(os.path.join(OUT, "true-vs-near-contact-20261031.png"))

# Contact 2: difference maps
dm_true, m_true, f_true = diffmap(true_a, true_b)
dm_near, m_near, f_near = diffmap(ref, near_a)
W2, H2 = 900, 420
img2 = Image.new("RGB", (W2, H2), (255, 255, 255))
d2 = ImageDraw.Draw(img2)
d2.rectangle([0, 0, 450, 40], fill=(30, 30, 30)); d2.text((10, 10), "TRUE diff map: black = 0 difference", fill=(255, 255, 255))
d2.rectangle([450, 0, 900, 40], fill=(30, 30, 30)); d2.text((460, 10), "NEAR diff map: red = detail differs", fill=(255, 255, 255))
img2.paste(dm_true.resize((400, 300), Image.LANCZOS), (25, 60))
img2.paste(dm_near.resize((400, 300), Image.LANCZOS), (475, 60))
d2.text((10, 375), f"TRUE mean abs diff {m_true:.2f}, pixels diff>30: {f_true*100:.2f}%", fill=(0, 0, 0))
d2.text((460, 375), f"NEAR mean abs diff {m_near:.2f}, pixels diff>30: {f_near*100:.2f}%", fill=(0, 0, 0))
img2.save(os.path.join(OUT, "difference-maps-contact-20261031.png"))
print("true diff", m_true, f_true)
print("near diff", m_near, f_near)
print("true_a exists", os.path.exists(true_a), "true_b", os.path.exists(true_b), "near", os.path.exists(near_a))
