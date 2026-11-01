"""Face/cowl snap check — per arm, per pose. Usage:
  python3 check_face_cowl_snap.py <arm_upper_L> <arm_lower_L> <arm_upper_R> <arm_lower_R> <head_angle>
Angles are the v7c pose angles (see build_poses.py). Prints per-side overlaps
and a decision. FACE is numeric; COWL is a candidate flag (see rule doc —
collar overlap alone also occurs at a normal shoulder attachment, so a
cowl snap always needs the eye-check, never an automatic reorder).
"""
import os, math, sys
from PIL import Image
import numpy as np
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
SCALE = 0.95
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.LANCZOS)

def paste_at(c, im, cx, top):
    c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))

def limb_layer(path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - ax), int(joint[1] - ay)))
    return layer.rotate(angle, center=joint, expand=False)

def rot_vec(v, a):
    r = math.radians(a); x, y = v
    return (x * math.cos(r) + y * math.sin(r), -x * math.sin(r) + y * math.cos(r))

def mask(piece, cx, top, scale=SCALE, ha=0):
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    if piece == "Head_Front.png":
        h = load(os.path.join(BASE, piece))
        if ha: h = h.rotate(ha, expand=True)
        layer.alpha_composite(h, (int(cx - h.size[0] / 2), int(331 - h.size[1] / 2)))
    else:
        paste_at(layer, load(os.path.join(BASE, piece), scale=scale), cx, top)
    return np.array(layer.split()[3]) > 10

def check(cfg, ha):
    head = mask("Head_Front.png", 550, 0, ha=ha)
    collar = mask("Cape_Collar.png", 550, 370)
    torso = mask("Torso_Chest.png", 550, 400)
    for side in ("L", "R"):
        shoulders = {"L": (430, 445), "R": (670, 445)}
        ball, sh_anchor = ARM[side]
        vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
        up, low, _ = ARM_PIECES[side]; sh = shoulders[side]
        upL = limb_layer(os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * SCALE,
                 sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1] * SCALE)
        lowL = limb_layer(os.path.join(CUT, low), elbow, cfg["arm_lower"][side], (ball[0], 0))
        def ov(layer, m):
            return int(((np.array(layer.split()[3]) > 10) & m).sum())
        lh, uc, lt = ov(lowL, head), ov(upL, collar), ov(lowL, torso)
        dy = elbow[1] - sh[1]
        if lh > 5000:
            decision = "FACE-SNAP: whole chain above head (torso < head < arm)"
        elif dy < -50 and uc > 1000:
            decision = "COWL-CANDIDATE: raised arm + collar overlap — EYE-CHECK bicep interruption before snapping"
        elif lt > 1000:
            decision = "CHEST-SNAP: whole chain above torso, below head (torso < arm < head)"
        else:
            decision = "NO SNAP"
        print(f"{side}: lower_vs_head={lh} upper_vs_collar={uc} lower_vs_torso={lt} elbow_dy={dy:.0f} -> {decision}")

if __name__ == "__main__":
    # args: upperL lowerL upperR lowerR head_angle
    a = [float(x) for x in sys.argv[1:5]]; ha = float(sys.argv[5]) if len(sys.argv) > 5 else 0
    cfg = {"arm_upper": {"L": a[0], "R": a[2]}, "arm_lower": {"L": a[1], "R": a[3]}}
    check(cfg, ha)
