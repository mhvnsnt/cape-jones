"""Rebuild the punch pose from scratch (no patching).
Lesson from the v4b patch attempt: erasing the old fist region also erased the
rotated forearm cuff, leaving a gap. This builder composites, in order:
legs, torso, L arm (native), R forearm part only (native fist discarded),
wrist cap masked to the forearm+fist union, then the scaled v4b fist seated
with overlap at the wrist. No double fist, no gap, no peek-through.
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math, json
import numpy as np

OUT = "/home/hatch/workspace/cape-jones-rig/gap-close-rig-20261031"
RIG = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}; HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_UP = {"L": "Arm_Front_Upper.png", "R": "Arm_Back_Upper.png"}
ARM_LOW = {"L": "Arm_Front_Lower.png", "R": "Arm_Back_Lower.png"}
ARM_CAP = {"L": "Arm_Front_Cap.png", "R": "Arm_Back_Cap.png"}
W2, DX = 1300, 100

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def load1(p): return Image.open(p).convert("RGBA")
def rot_vec(v, a):
    r = math.radians(a); x, y = v
    return (x*math.cos(r)+y*math.sin(r), -x*math.sin(r)+y*math.cos(r))

c = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
def pat(im, cx, top): c.paste(im, (int(cx-im.size[0]/2), int(top)), im)
def limb2(path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    return layer.rotate(angle, center=joint, expand=False)
def cap2(path, joint):
    im = load(path); c.paste(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)), im)

pat(load(os.path.join(BASE, "Cape_Back_Main.png")), 550+DX, 410)
knees = {}
for side in ("L", "R"):
    hip = (HIP[side][0]+DX, HIP[side][1]); ball, ha = LEG[side]
    vec = (ball[0]-ha[0], ball[1]-ha[1])
    c.alpha_composite(limb2(os.path.join(CUT, LEG_PIECES[side][0]), hip, {"L": -20, "R": 20}[side], ha))
    knee = (hip[0]+rot_vec(vec, {"L": -20, "R": 20}[side])[0]*SCALE, hip[1]+rot_vec(vec, {"L": -20, "R": 20}[side])[1]*SCALE)
    knees[side] = knee
    c.alpha_composite(limb2(os.path.join(CUT, LEG_PIECES[side][1]), knee, {"L": -20, "R": 20}[side], (ball[0], 0)))
    cap2(os.path.join(CUT, LEG_PIECES[side][2]), knee)
pat(load(os.path.join(BASE, "Pelvis.png")), 550+DX, 680)
pat(load(os.path.join(BASE, "Cape_Collar.png")), 550+DX, 370)
pat(load(os.path.join(BASE, "Torso_Chest.png")), 550+DX, 400)
pat(load(os.path.join(BASE, "Belt_Overlay.png")), 550+DX, 670)
elbows, wrists = {}, {}
for side in ("L", "R"):
    ball, sh_a = ARM[side]; vec = (ball[0]-sh_a[0], ball[1]-sh_a[1])
    sh = (SHOULDER[side][0]+DX, SHOULDER[side][1])
    c.alpha_composite(limb2(os.path.join(CUT, ARM_UP[side]), sh, {"L": -45, "R": 90}[side], sh_a))
    elbows[side] = (sh[0]+rot_vec(vec, {"L": -45, "R": 90}[side])[0]*SCALE,
                    sh[1]+rot_vec(vec, {"L": -45, "R": 90}[side])[1]*SCALE)
c.alpha_composite(limb2(os.path.join(CUT, ARM_LOW["L"]), elbows["L"], -45, (ARM["L"][0][0], 0)))
cap2(os.path.join(CUT, ARM_CAP["L"]), elbows["L"])
# R forearm part only (split at y178; native fist discarded)
low_r = load1(os.path.join(CUT, ARM_LOW["R"]))
fa_ = np.array(low_r); fa_[178:, :, 3] = 0
fore_r = Image.fromarray(fa_).resize((int(low_r.size[0]*SCALE), int(low_r.size[1]*SCALE)), Image.LANCZOS)
layer = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
layer.paste(fore_r, (int(elbows["R"][0]-ARM["R"][0][0]*SCALE), int(elbows["R"][1])), fore_r)
fore_layer = layer.rotate(90, center=elbows["R"], expand=False)
c.alpha_composite(fore_layer)
cap2(os.path.join(CUT, ARM_CAP["R"]), elbows["R"])
wvec = (114-ARM["R"][0][0], 180)
wrists["R"] = (elbows["R"][0]+rot_vec(wvec, 90)[0]*SCALE, elbows["R"][1]+rot_vec(wvec, 90)[1]*SCALE)
wvec_l = (79-ARM["L"][0][0], 180)
wrists["L"] = (elbows["L"][0]+rot_vec(wvec_l, -45)[0]*SCALE, elbows["L"][1]+rot_vec(wvec_l, -45)[1]*SCALE)
# scaled v4b fist, seated with 12px overlap along the axis (axis ~ +x)
fist = load1(os.path.join(OUT, "gap-close-fist-v4b-knuckle-front-20261031.png"))
small = fist.resize((155, 164), Image.LANCZOS)
fist_rot = small.rotate(-90, expand=True)
ws = (160*155/320, 306*164/340)
w_rot = (small.size[1]-1-ws[1], ws[0])
seat = (wrists["R"][0]-12, wrists["R"][1])
flayer = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
flayer.paste(fist_rot, (int(seat[0]-w_rot[0]), int(seat[1]-w_rot[1])), fist_rot)
# wrist cap BEHIND fist, masked to forearm+fist union (dilated) — side arcs only
cap_im = load(os.path.join(CUT, ARM_CAP["R"]))
cap_layer = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
cap_layer.paste(cap_im, (int(wrists["R"][0]-cap_im.size[0]/2), int(wrists["R"][1]-cap_im.size[1]/2)), cap_im)
union = (np.array(fore_layer)[:, :, 3] > 0) | (np.array(flayer)[:, :, 3] > 0)
union_im = Image.fromarray((union.astype(np.uint8))*255).filter(ImageFilter.MaxFilter(7))
ca = np.array(cap_layer); ma = np.array(union_im)
ca[:, :, 3] = np.where(ma > 0, ca[:, :, 3], 0)
c.alpha_composite(Image.fromarray(ca))
c.alpha_composite(flayer)
pat(load(os.path.join(BASE, "Neck.png"), scale=1.05), 550+DX, 360)
pat(load(os.path.join(BASE, "Head_Front.png")), 550+DX, 250)
# gap check: rows around the wrist axis must be continuously opaque from elbow to fist end
a = np.array(c)[:, :, 3] > 10
yrow = int(round(wrists["R"][1]))
xs = np.where(a[yrow])[0]
# find interval containing the R arm (x > 800)
seg = [x for x in xs if x > 800]
gaps = [(seg[i], seg[i+1]) for i in range(len(seg)-1) if seg[i+1]-seg[i] > 5]
print("wrist row", yrow, "R-arm interval", (min(seg), max(seg)) if seg else None, "gaps>5px", gaps)
fa2 = np.array(flayer)[:, :, 3] > 10; ys2, xs2 = np.where(fa2)
joints = {"elbows": {k: [round(v[0], 1), round(v[1], 1)] for k, v in elbows.items()},
          "wrists": {k: [round(v[0], 1), round(v[1], 1)] for k, v in wrists.items()},
          "fist_R_centre": [round(float(xs2.mean()), 1), round(float(ys2.mean()), 1)],
          "fist_R_bbox": [int(xs2.min()), int(xs2.max()), int(ys2.min()), int(ys2.max())],
          "knees": {k: [round(v[0], 1), round(v[1], 1)] for k, v in knees.items()},
          "wrist_row_gaps": gaps}
c.save(os.path.join(OUT, "gap-close-punch-pose-v4c-20261031.png"))
json.dump(joints, open(os.path.join(OUT, "gap-close-punch-pose-v4c-joints-20261031.json"), "w"), indent=2)
print("saved punch v4c", joints)
