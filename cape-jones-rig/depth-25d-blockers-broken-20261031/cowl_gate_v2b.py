"""EXPERIMENTAL cowl-gate v2b: does the collar SPLIT the bicep?
Draw the upper-arm piece alone at its pose position, draw the collar mask
alone, then count connected components of (upper MINUS collar).
- Continuous bicep (normal attachment): 1 component (the collar may overlap
  an edge, but does not cut through the limb).
- Notched bicep (collar cuts through): 2+ components, or a large bite:
  measured as (upper_area - upper_minus_collar_area) / upper_area AND
  component count.
This uses the same v7c joint math as trace_gp_frames.py. Pieces are drawn
with PIL (no Blender needed), scipy labels components.
"""
import os, math
import numpy as np
from PIL import Image
from scipy import ndimage
RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "depth-25d-blockers-broken-20261031")
BASE = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
SCALE = 0.95
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
ARM_PIECES = {"L": "Arm_Front_Upper.png", "R": "Arm_Back_Upper.png"}

def rot(v, a):
    r = math.radians(a); x, y = v
    return (x * math.cos(r) + y * math.sin(r), -x * math.sin(r) + y * math.cos(r))

def draw_piece(canvas, path, joint, angle, anchor, scale=SCALE):
    im = Image.open(path).convert("RGBA").resize((max(1, int(Image.open(path).size[0] * scale)), max(1, int(Image.open(path).size[1] * scale))), Image.LANCZOS)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - anchor[0] * scale), int(joint[1] - anchor[1] * scale)))
    layer = layer.rotate(angle, center=joint, expand=False)
    canvas.alpha_composite(layer)

def upper_mask(cfg, side, cx=550):
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    sh = (cx - 120, 445) if side == "L" else (cx + 120, 445)
    ball, sh_anchor = ARM[side]
    draw_piece(canvas, os.path.join(CUT, ARM_PIECES[side]), sh, cfg["arm_upper"][side], sh_anchor)
    return np.array(canvas)[:, :, 3] > 10

def collar_mask(cx=550):
    p = os.path.join(BASE, "Cape_Collar.png")
    im = Image.open(p).convert("RGBA")
    im = im.resize((max(1, int(im.size[0] * SCALE)), max(1, int(im.size[1] * SCALE))), Image.LANCZOS)
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    canvas.alpha_composite(im, (int(cx - im.size[0] / 2), 370))
    return np.array(canvas)[:, :, 3] > 10

COLLAR = collar_mask()
CASES = {
    "apose_L": ({"arm_upper": {"L": 0, "R": 0}}, "L", "no snap needed"),
    "apose_R": ({"arm_upper": {"L": 0, "R": 0}}, "R", "no snap needed"),
    "jojo02_L_false_positive": ({"arm_upper": {"L": -115, "R": 65}}, "L", "eye: fist beside head, not cut"),
    "ginyu03_L_true": ({"arm_upper": {"L": -130, "R": 130}}, "L", "eye: notched both sides"),
    "ginyu03_R_true": ({"arm_upper": {"L": -130, "R": 130}}, "R", "eye: notched both sides"),
    "jump_L_true": ({"arm_upper": {"L": -150, "R": 150}}, "L", "eye: notched both sides"),
    "ginyu01_L_true": ({"arm_upper": {"L": -160, "R": 20}}, "L", "eye: L bicep cut"),
    "ginyu01_R_normal": ({"arm_upper": {"L": -160, "R": 20}}, "R", "eye: R not raised/cut"),
}
rows = []
for name, (cfg, side, note) in CASES.items():
    up = upper_mask(cfg, side)
    rem = up & ~COLLAR
    lab, n = ndimage.label(rem)
    sizes = sorted([(lab == i).sum() for i in range(1, n + 1)], reverse=True) if n else [0]
    bite = 1 - rem.sum() / max(up.sum(), 1)
    rows.append((name, int(up.sum()), int(rem.sum()), n, sizes[:3], round(float(bite), 3), note))
    print(name, "upper", int(up.sum()), "remaining", int(rem.sum()), "components", n, "top sizes", sizes[:3], "bite", round(float(bite), 3), note)
with open(os.path.join(OUT, "cowl_gate_v2b_results-20261031.csv"), "w") as f:
    f.write("case,upper_px,remaining_px,components,top_component_sizes,bite_fraction,eye_check_note\n")
    for r in rows:
        f.write(f"{r[0]},{r[1]},{r[2]},{r[3]},\"{r[4]}\",{r[5]},{r[6]}\n")
