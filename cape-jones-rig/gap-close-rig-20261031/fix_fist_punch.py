"""Fixes found on own-eyes viewing (2026-10-31):
- v4 fist: knuckle scallops too deep, thumb read as a detached diamond, left grey
  slab read as a separate panel. Redrawn as v4b: shallower knuckle bumps, thumb as
  a wide diagonal band across the front, shading clipped inside the silhouette.
- Punch pose: v4 fist was pasted at full 320px width and clipped at the canvas edge,
  and the wrist cap showed as a white block. v4b pose: fist scaled to 155px wide,
  wrist point computed by the exact CW-rotation point formula, cap masked to the
  forearm+fist union so only side arcs peek.
Originals are kept (superseded drafts), new files are v4b; nothing Mars has seen
is touched.
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math, json
import numpy as np

OUT = "/home/hatch/workspace/cape-jones-rig/gap-close-rig-20261031"
RIG = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")

# --- redrawn fist v4b
W, H = 320, 340
sil = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sil)
sd.rounded_rectangle((70, 100, 250, 295), radius=42, fill=255)
for cx in (102, 140, 178, 216):  # shallow bumps: only ~20px above the body top
    sd.ellipse((cx-26, 80, cx+26, 132), fill=255)
sd.rectangle((118, 280, 202, 330), fill=255)
outline = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(outline)
od.bitmap((0, 0), sil.filter(ImageFilter.MaxFilter(9)), fill=(0, 0, 0, 255))
fist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fist.alpha_composite(outline)
body = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(body)
bd.bitmap((0, 0), sil, fill=(255, 255, 255, 255))
fist.alpha_composite(body)
# shading clipped INSIDE the silhouette: soft grey on the lower-left edge only
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shd = ImageDraw.Draw(sh)
shd.ellipse((60, 180, 130, 300), fill=(190, 196, 205, 90))
sh_mask = Image.new("L", (W, H), 0); sh_mask.paste(sil, (0, 0))
sh.putalpha(Image.composite(sh.split()[3], Image.new("L", (W, H), 0), sh_mask))
fist.alpha_composite(sh)
d = ImageDraw.Draw(fist)
for cx in (102, 140, 178, 216):  # short faint seam ticks below the knuckles
    d.line([(cx-13, 138), (cx+13, 138)], fill=(150, 155, 165, 255), width=3)
# thumb: WIDE diagonal band wrapped across the front, right edge -> centre-left tip
d.polygon([(252, 160), (252, 205), (170, 232), (132, 224), (128, 196), (200, 172)],
          fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
d.line([(170, 232), (200, 172)], fill=(0, 0, 0, 255), width=2)  # thumb tip crease (inner edge)
for y in (250, 272):
    d.arc((100, y-16, 220, y+16), start=20, end=160, fill=(150, 155, 165, 255), width=3)
d.line([(118, 280), (202, 280)], fill=(0, 0, 0, 255), width=3)
fist.save(os.path.join(OUT, "gap-close-fist-v4b-knuckle-front-20261031.png"))
print("fist v4b saved", fist.size)

# --- punch pose v4b: rebuild by patching the v4 builder logic at smaller scale.
# Simplest robust route: re-run the punch build from build_gap_close.py but with the
# scaled fist. Importing that module would rebuild everything, so instead patch the
# existing punch PNG: erase the R fist region and paste the scaled, correctly seated fist.
# Erase region: x > 1010 (old fist + cap block), y 200-650 in the 1300-wide pose.
pose = Image.open(os.path.join(OUT, "gap-close-punch-pose-v4-20261031.png")).convert("RGBA")
joints = json.load(open(os.path.join(OUT, "gap-close-punch-pose-v4-joints-20261031.json")))
wx, wy = joints["wrists"]["R"]
arr = np.array(pose)
arr[200:650, 1010:, 3] = 0
pose = Image.fromarray(arr)
# forearm end: the native R forearm (from the v4 build) ends near the wrist; re-extend it
# by pasting the forearm's last 40px column band is unnecessary — the wrist cap + fist
# will cover the seam. Place the wrist cap, masked later by the fist overlap.
from PIL import Image as _I
cap = _I.open(os.path.join(CUT, "Arm_Back_Cap.png")).convert("RGBA")
cap = cap.resize((int(cap.size[0]*0.95), int(cap.size[1]*0.95)), _I.LANCZOS)
cap_layer = Image.new("RGBA", pose.size, (0, 0, 0, 0))
cap_layer.paste(cap, (int(wx-cap.size[0]/2), int(wy-cap.size[1]/2)), cap)
# scaled fist: 155 wide -> 155x164; CW rotate (-90): (x,y) -> (H-1-y, x)
small = fist.resize((155, 164), Image.LANCZOS)
fist_rot = small.rotate(-90, expand=True)
# wrist point in small image: cuff centre (160,306) scaled by 155/320, 164/340
ws = (160*155/320, 306*164/340)
w_rot = (small.size[1]-1-ws[1], ws[0])  # CW formula
print("small", small.size, "rot", fist_rot.size, "wrist scaled", ws, "wrist rotated", w_rot)
# seat 18px deep: wrist point sits 18px inside the forearm along the axis (axis ~ +x)
seat_x, seat_y = wx-18, wy
flayer = Image.new("RGBA", pose.size, (0, 0, 0, 0))
flayer.paste(fist_rot, (int(seat_x-w_rot[0]), int(seat_y-w_rot[1])), fist_rot)
# mask the cap to forearm+fist union (dilated) so only side arcs peek
union = (np.array(pose)[:, :, 3] > 0) | (np.array(flayer)[:, :, 3] > 0)
union_im = Image.fromarray((union.astype(np.uint8))*255).filter(ImageFilter.MaxFilter(7))
ca = np.array(cap_layer); ma = np.array(union_im)
ca[:, :, 3] = np.where(ma > 0, ca[:, :, 3], 0)
pose.alpha_composite(Image.fromarray(ca))
pose.alpha_composite(flayer)
pose.save(os.path.join(OUT, "gap-close-punch-pose-v4b-20261031.png"))
a = np.array(flayer)[:, :, 3] > 10; ys, xs = np.where(a)
print("v4b fist bbox in pose", xs.min(), xs.max(), ys.min(), ys.max(), "centre", round(float(xs.mean()), 1), round(float(ys.mean()), 1))
joints["fist_R_centre"] = [round(float(xs.mean()), 1), round(float(ys.mean()), 1)]
joints["wrists"]["R"] = [round(float(seat_x), 1), round(float(seat_y), 1)]
json.dump(joints, open(os.path.join(OUT, "gap-close-punch-pose-v4b-joints-20261031.json"), "w"), indent=2)
print("punch v4b saved")
