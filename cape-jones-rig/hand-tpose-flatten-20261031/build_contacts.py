"""Contacts for the combined hand fix. Labels are on the SHEET only,
never baked into the individual plates. Grey-128 viewing versions only;
individual files stay transparent."""
import os
from PIL import Image, ImageDraw
RIG = "/home/hatch/workspace/cape-jones-rig"
W = os.path.join(RIG, "wrist-attach-fix-20261031")
OUT = os.path.join(RIG, "hand-tpose-flatten-20261031")

def thumb(path, w):
    im = Image.open(path).convert("RGB")
    h = int(im.size[1] * w / im.size[0])
    return im.resize((w, h), Image.LANCZOS)

def sheet(tiles, cols, tile_w, label_h, path):
    # tiles: list of (image, label)
    rows = (len(tiles) + cols - 1) // cols
    tile_h = max(t.size[1] for t, _ in tiles) + label_h
    S = Image.new("RGB", (cols * tile_w + 20 * (cols + 1), rows * tile_h + 20), (40, 40, 40))
    d = ImageDraw.Draw(S)
    for i, (t, lab) in enumerate(tiles):
        r, c = divmod(i, cols)
        x = 20 + c * (tile_w + 20); y = 10 + r * tile_h
        S.paste(t, (x, y + label_h))
        d.text((x + 4, y + 4), lab, fill=(255, 255, 255))
    S.save(path); print(path, S.size)

# --- library contact: 7 rows x 3 cols ---
lib = [("1_fist", "library-1_fist-WRIST-FIXED-20261031.png"),
       ("2_fistback", "library-2_fistback-WRIST-FIXED-20261031.png"),
       ("3_open", "library-3_open-WRIST-FIXED-20261031.png"),
       ("4_point", "library-4_point-WRIST-FIXED-20261031.png"),
       ("5_point2", "library-5_point2-WRIST-FIXED-20261031.png"),
       ("6_relaxed", "library-6_relaxed-WRIST-FIXED-20261031.png"),
       ("7_grip", "library-7_grip-WRIST-FIXED-20261031.png")]
tiles = []
for tag, old in lib:
    tiles.append((thumb(os.path.join(W, old), 360), f"{tag} BEFORE groove-a FIXED both-up 1.7"))
    tiles.append((thumb(os.path.join(OUT, f"tpose-{tag}-OLD-PARAMS-20261031.png"), 360), f"{tag} T-POSE OLD-PARAMS both-up 1.7"))
    tiles.append((thumb(os.path.join(OUT, f"tpose-{tag}-FINAL-20261031.png"), 360), f"{tag} FINAL flattened +90/-90 Arm1-mirrored 1.275"))
sheet(tiles, 3, 360, 22, os.path.join(OUT, "library-before-after-contact-20261031.png"))

# --- dance contact: base-fist row + 9 before/after pairs ---
tiles = []
for g in ("groove-a", "groove-b", "groove-c"):
    tiles.append((thumb(os.path.join(W, f"dance-base-fist-{g}-WRIST-FIXED-20261031.png"), 300),
                  f"base-fist {g} CORRECT UNTOUCHED (not scaled)"))
# pad to 3-col row with a blank tile
tiles.append((Image.new("RGB", (300, 409), (40, 40, 40)), ""))
for vname in ("open", "point", "relaxed"):
    for g in ("groove-a", "groove-b", "groove-c"):
        b = thumb(os.path.join(W, f"dance-{vname}-{g}-WRIST-FIXED-20261031.png"), 210)
        a = thumb(os.path.join(OUT, f"dance-{vname}-{g}-FINAL-20261031.png"), 210)
        pair = Image.new("RGB", (420, max(b.size[1], a.size[1])), (40, 40, 40))
        pair.paste(b, (0, 0)); pair.paste(a, (210, 0))
        tiles.append((pair, f"{vname} {g} BEFORE 1.7 (left) vs FINAL 1.275 Arm1-mirrored (right)"))
# dance sheet uses mixed tile widths; rebuild manually
rows = 4
S = Image.new("RGB", (3 * 440 + 40, 4 * 460 + 40), (40, 40, 40)); d = ImageDraw.Draw(S)
# row 0: base-fist
for i in range(3):
    t, lab = tiles[i]; S.paste(t, (20 + i * 440, 30)); d.text((20 + i * 440, 10), lab, fill=(255, 255, 255))
for j in range(9):
    t, lab = tiles[4 + j]; r, c = divmod(j, 3)
    S.paste(t, (20 + c * 440, 460 * (r + 1) + 30)); d.text((20 + c * 440, 460 * (r + 1) + 10), lab, fill=(255, 255, 255))
S.save(os.path.join(OUT, "dance-before-after-contact-20261031.png")); print("dance contact", S.size)

# --- serve contact: 2x2 ---
tiles = [
    (thumb(os.path.join(W, "jei-01-serve-open-palm-WRIST-FIXED-20261031.png"), 400), "plain BEFORE overlay (wrist-fixed)"),
    (thumb(os.path.join(OUT, "jei-01-serve-open-palm-FINAL-20261031.png"), 400), "plain FINAL replacement, fist gone, Arm1 mirrored"),
    (thumb(os.path.join(W, "jei-01-serve-open-palm-ball-WRIST-FIXED-20261031.png"), 400), "ball BEFORE overlay"),
    (thumb(os.path.join(OUT, "jei-01-serve-open-palm-ball-FINAL-20261031.png"), 400), "ball FINAL over NEW palm centre (255,230,110)"),
]
sheet(tiles, 2, 400, 22, os.path.join(OUT, "serve-before-after-contact-20261031.png"))
print("CONTACTS DONE")
