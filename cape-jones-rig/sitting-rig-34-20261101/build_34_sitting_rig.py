"""Slice Mars 3/4 sitting sheet (clean-cut only) + assemble 3/4 sitting rig.
Source: ~/workspace/user/files/1000179383_25_yh27.jpg  md5 4dc11a3dc88b9bd0cba55bc156971ecb  1200x1648
Background: flat grey 126,126,126. Mask = max-channel distance >30, holes filled.
No rembg. No hand-drawn pieces. No piece invented.
"""
from PIL import Image
import numpy as np, json, os
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101")
SRC = os.path.expanduser("~/workspace/user/files/1000179383_25_yh27.jpg")
im = np.array(Image.open(SRC).convert("RGB")).astype(int)
dist = np.max(np.abs(im - 126), axis=2)
mask = dist > 30
lab, n = ndimage.label(mask)
objs = ndimage.find_objects(lab)

# component id -> name, by bbox, verified by eye
NAMES = {
    1: "head_cowl",
    5: "upper_arm_L_socket",
    10: "torso",
    14: "upper_arm_R",
    27: "upper_arm_spare",
    34: "forearm_hand_L",
    37: "forearm_hand_mid",
    40: "forearm_hand_R",
    41: "pelvis_belt",
    44: "cape_back",
    46: "hand_spare_L",
    52: "thigh_bent_L",
    58: "hand_spare_mid",
    59: "thigh_bent_R",
    60: "hand_spare_R",
    66: "piece_ambiguous_scoop_top",
    72: "shin_boot_L",
    73: "knee_ball_spare",
    74: "shin_boot_mid",
    75: "boot_spare",
    77: "shin_boot_R",
}
pieces = {}
for i, sl in enumerate(objs, 1):
    if i not in NAMES:
        continue
    area = int((lab[sl] == i).sum())
    if area < 200:
        continue
    y, x = sl
    comp = (lab[sl] == i)
    comp = ndimage.binary_fill_holes(comp)
    crop_rgb = Image.open(SRC).convert("RGBA").crop((x.start, y.start, x.stop, y.stop))
    alpha = (comp.astype(np.uint8)) * 255
    crop_rgb.putalpha(Image.fromarray(alpha))
    name = NAMES[i]
    crop_rgb.save(f"{ROOT}/pieces/{name}.png")
    pieces[name] = dict(component=i, area=area, bbox=[x.start, y.start, x.stop, y.stop],
                        w=x.stop - x.start, h=y.stop - y.start)
    print(name, area, x.start, y.start, x.stop, y.stop)

with open(f"{ROOT}/piece-inventory-20261101.json", "w") as f:
    json.dump({"source": "workspace/user/files/1000179383_25_yh27.jpg",
               "md5": "4dc11a3dc88b9bd0cba55bc156971ecb", "size": [1200, 1648],
               "background": [126, 126, 126], "method": "clean-cut, distance>30, holes filled, no rembg",
               "pieces": pieces}, f, indent=2)

# ---- assembly ----
def load(name):
    return Image.open(f"{ROOT}/pieces/{name}.png")

def paste(canvas, piece, cx, top, angle=0, scale=1.3):
    """paste piece so its centre-x = cx, top = top, rotated about its centre."""
    w, h = piece.size
    p = piece.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    if angle:
        p = p.rotate(angle, resample=Image.BICUBIC, expand=False)
    canvas.alpha_composite(p, (int(cx - p.width / 2), int(top)))
    return (int(cx - p.width / 2), int(top), p.width, p.height)

def build(pose):
    W, H = 1400, 1600
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # cape back first (behind), collar locked: no separate collar piece, torso carries it
    paste(canvas, load("cape_back"), 700, 340, angle=0, scale=1.4)
    paste(canvas, load("pelvis_belt"), 700, 660, scale=1.3)
    # thighs as drawn, small rotation only; knee balls end at bottom of thigh pieces
    if pose == "chair":
        paste(canvas, load("thigh_bent_L"), 600, 800, angle=-8, scale=1.3)
        paste(canvas, load("thigh_bent_R"), 800, 800, angle=6, scale=1.3)
    elif pose == "upright":
        paste(canvas, load("thigh_bent_L"), 620, 810, angle=-4, scale=1.3)
        paste(canvas, load("thigh_bent_R"), 780, 810, angle=4, scale=1.3)
    else:  # lean
        paste(canvas, load("thigh_bent_L"), 600, 800, angle=-8, scale=1.3)
        paste(canvas, load("thigh_bent_R"), 800, 800, angle=6, scale=1.3)
    # shins vertical, directly UNDER the thigh knee balls, feet planted at shared ground y=1420
    # left knee ~x550, right knee ~x760 (measured from v1 render); shin tops overlap knees
    for name, cx, top in [("shin_boot_L", 550, 1010), ("shin_boot_mid", 760, 1010)]:
        paste(canvas, load(name), cx, top, scale=1.3)
    paste(canvas, load("torso"), 700, 350, scale=1.3)
    # upper arms: shoulder at torso sides, elbow ball at bottom of each upper piece
    paste(canvas, load("upper_arm_L_socket"), 560, 390, angle=-8, scale=1.3)
    paste(canvas, load("upper_arm_R"), 840, 390, angle=8, scale=1.3)
    # forearms: gauntlet top at elbow ball, hand at bottom
    if pose == "chair":  # hands on thighs
        paste(canvas, load("forearm_hand_L"), 530, 600, angle=-15, scale=1.3)
        paste(canvas, load("forearm_hand_R"), 830, 600, angle=15, scale=1.3)
    elif pose == "upright":  # arms at sides
        paste(canvas, load("forearm_hand_L"), 520, 610, angle=-5, scale=1.3)
        paste(canvas, load("forearm_hand_R"), 860, 610, angle=5, scale=1.3)
    else:  # lean, hands to knees
        paste(canvas, load("forearm_hand_L"), 550, 620, angle=-25, scale=1.3)
        paste(canvas, load("forearm_hand_R"), 810, 620, angle=25, scale=1.3)
    # head last (in front of cape/torso top)
    paste(canvas, load("head_cowl"), 700, 195, scale=1.3)
    return canvas

for pose, label in [("chair", "sit-chair"), ("upright", "sit-upright"), ("lean", "sit-lean-forward-34")]:
    fig = build(pose)
    fig.save(f"{ROOT}/poses/{label}-20261101.png")
    grey = Image.new("RGBA", fig.size, (126, 126, 126, 255))
    grey.alpha_composite(fig)
    grey.convert("RGB").save(f"{ROOT}/poses/{label}-20261101-on-grey.png")
    # ground line check: alpha bbox
    a = np.array(fig)[:, :, 3]
    ys, xs = np.where(a > 10)
    print(label, "bbox", xs.min(), ys.min(), xs.max(), ys.max(), "alpha_px", int((a > 10).sum()))
    # foot bottoms: bottom rows per x-half
    for side, (x0, x1) in [("L", (0, 700)), ("R", (700, 1400))]:
        sub = a[:, x0:x1]
        yy, xx = np.where(sub > 10)
        print(" ", side, "bottom", int(yy.max()))

# contact sheet of pieces on grey
names = sorted(pieces)
cols = 5
cell = 260
rows = (len(names) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell, rows * cell), (126, 126, 126))
from PIL import ImageDraw
d = ImageDraw.Draw(sheet)
for idx, name in enumerate(names):
    p = load(name); p.thumbnail((240, 240))
    x, y = (idx % cols) * cell + 10, (idx // cols) * cell + 10
    sheet.paste(p, (x, y), p)
    d.text(((idx % cols) * cell + 10, (idx // cols) * cell + 225), name, fill=(255, 255, 255))
sheet.save(f"{ROOT}/contacts/pieces-contact-20261101.png")

# pose contact
contact = Image.new("RGB", (3 * 470, 560), (126, 126, 126))
for i, label in enumerate(["sit-chair", "sit-upright", "sit-lean-forward-34"]):
    p = Image.open(f"{ROOT}/poses/{label}-20261101-on-grey.png"); p.thumbnail((460, 550))
    contact.paste(p, (i * 470 + 5, 5))
contact.save(f"{ROOT}/contacts/poses-contact-20261101.png")
print("done")
