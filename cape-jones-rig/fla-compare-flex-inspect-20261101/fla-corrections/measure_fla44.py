"""Second-pass measurement cross-check for the 44 remaining FLA batch-60 pieces.
Reads ONLY the source pieces under sliced-clean-20261031/D-xray-angle-ref/.
Writes measurements JSON in this folder. No original touched, no PNG output.
Colour rules (opaque pixels only):
  black: R+G+B < 150
  purple: B > R+30 and 60<R<200 and G<110 and B>120  (cowl / emblem purple family)
  white/light: R+G+B > 600
  mid: everything else (skin/shading/grey)
"""
import json, os
from PIL import Image

ROOT = "/home/hatch/workspace/cape-jones-rig/sliced-clean-20261031/D-xray-angle-ref"
OUT = "/home/hatch/workspace/cape-jones-rig/fla-compare-flex-inspect-20261101/fla-corrections"

# piece_id -> (draft_label, draft_tier) from build-still-20261101 agent-eye draft.
# Tier: CLEAN = full label certain at agent-eye level; SHAPE-ONLY = shape certain,
# side/subtype/view TBD; NEEDS-MARS = ambiguous/MIXED, no label guessed.
DRAFT = {
 "fla-front/Row1_17.png": ("capejones_leg_foot_front", "SHAPE-ONLY"),
 "fla-front/Row1_18.png": ("capejones_leg_front", "SHAPE-ONLY"),
 "fla-front/Row1_19.png": ("capejones_torso_chest_front", "CLEAN"),
 "fla-front/Row1_2.png": ("capejones_gauntlet_front", "SHAPE-ONLY"),
 "fla-front/Row1_20.png": ("capejones_belt_front", "CLEAN"),
 "fla-front/Row1_21.png": ("capejones_head_front", "CLEAN"),
 "fla-front/Row1_22.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-front/Row1_23.png": ("capejones_leg_front", "SHAPE-ONLY"),
 "fla-front/Row1_31.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-front/Row1_32.png": ("capejones_cape_main_front", "SHAPE-ONLY"),
 "fla-front/Row1_33.png": (None, "NEEDS-MARS"),
 "fla-front/Row1_4.png": ("capejones_leg_foot_front", "SHAPE-ONLY"),
 "fla-front/Row1_5.png": ("capejones_hand_front", "SHAPE-ONLY"),
 "fla-front/Row1_6.png": ("capejones_gauntlet_front", "SHAPE-ONLY"),
 "fla-front/Row1_7.png": ("capejones_leg_foot_front", "SHAPE-ONLY"),
 "fla-front/Row1_8.png": (None, "NEEDS-MARS"),
 "fla-front/Row1_9.png": ("capejones_torso_chest_front", "CLEAN"),
 "fla-back/Row1_1.png": ("capejones_gauntlet", "SHAPE-ONLY"),
 "fla-back/Row1_10.png": (None, "NEEDS-MARS"),
 "fla-back/Row1_11.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-back/Row1_12.png": ("capejones_pelvis", "CLEAN"),
 "fla-back/Row1_13.png": ("capejones_gauntlet", "SHAPE-ONLY"),
 "fla-back/Row1_14.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-back/Row1_15.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-back/Row1_16.png": ("capejones_torso_back", "CLEAN"),
 "fla-back/Row1_17.png": ("capejones_belt", "CLEAN"),
 "fla-back/Row1_18.png": (None, "NEEDS-MARS"),
 "fla-back/Row1_19.png": ("capejones_cowl", "SHAPE-ONLY"),
 "fla-back/Row1_2.png": ("capejones_hand", "SHAPE-ONLY"),
 "fla-back/Row1_20.png": (None, "NEEDS-MARS"),
 "fla-back/Row1_21.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-back/Row1_22.png": (None, "NEEDS-MARS"),
 "fla-back/Row1_23.png": ("capejones_gauntlet", "SHAPE-ONLY"),
 "fla-back/Row1_24.png": (None, "NEEDS-MARS"),
 "fla-back/Row1_25.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-back/Row1_26.png": (None, "NEEDS-MARS"),
 "fla-back/Row1_27.png": ("capejones_gauntlet", "SHAPE-ONLY"),
 "fla-back/Row1_28.png": ("capejones_gauntlet", "SHAPE-ONLY"),
 "fla-back/Row1_29.png": ("capejones_ball_joint_or_circular_eye_front", "CLEAN"),
 "fla-back/Row1_3.png": (None, "NEEDS-MARS"),
 "fla-back/Row1_30.png": ("capejones_cape_main", "SHAPE-ONLY"),
 "fla-back/Row1_4.png": ("capejones_hand", "SHAPE-ONLY"),
 "fla-back/Row1_5.png": ("capejones_hand", "SHAPE-ONLY"),
 "fla-back/Row1_6.png": ("capejones_torso_chest", "CLEAN"),
}

def measure(path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    px = list(im.getdata())
    opaque = [(r, g, b) for (r, g, b, a) in px if a > 10]
    n = len(opaque)
    if n == 0:
        return {"w": w, "h": h, "opaque": 0}
    black = sum(1 for r, g, b in opaque if r + g + b < 150)
    purple = sum(1 for r, g, b in opaque if b > r + 10 and b >= 85 and g <= 90 and r <= 170)
    white = sum(1 for r, g, b in opaque if r + g + b > 600)
    xs = []; ys = []
    for i, (r, g, b, a) in enumerate(px):
        if a > 10:
            xs.append(i % w); ys.append(i // w)
    bw = max(xs) - min(xs) + 1; bh = max(ys) - min(ys) + 1
    return {"w": w, "h": h, "opaque": n, "bbox_w": bw, "bbox_h": bh,
            "fill": round(n / (bw * bh), 3) if bw * bh else 0,
            "aspect": round(bw / bh, 3) if bh else 0,
            "black_frac": round(black / n, 3), "purple_frac": round(purple / n, 3), "purple_px": purple,
            "white_frac": round(white / n, 3),
            "bbox": [min(xs), min(ys), max(xs), max(ys)]}

rows = []
for pid, (label, tier) in sorted(DRAFT.items()):
    p = os.path.join(ROOT, pid)
    m = measure(p)
    m["piece_id"] = pid; m["draft_label"] = label; m["draft_tier"] = tier
    # Plausibility flags (measurement vs draft family, never a new label guess)
    flags = []
    if m["opaque"] == 0:
        flags.append("BLANK")
    if label and "ball_joint" in label:
        if not (0.7 <= m.get("aspect", 0) <= 1.4):
            flags.append("BALL-NOT-SQUARE")
        if m.get("fill", 0) < 0.5:
            flags.append("BALL-LOW-FILL")
    if label and "torso_chest" in label:
        if m.get("purple_px", 0) < 100:
            flags.append("TORSO-LOW-PURPLE")
    if label and "cape_main" in label:
        if m.get("black_frac", 0) < 0.15:
            flags.append("CAPE-LOW-BLACK")
    if label and label.endswith("cowl"):
        if m.get("purple_frac", 0) < 0.30:
            flags.append("COWL-LOW-PURPLE")
    if label and "belt" in label:
        if m.get("aspect", 0) < 1.0:
            flags.append("BELT-NOT-WIDE")
    m["flags"] = flags
    rows.append(m)
    print(pid, label, tier, m["w"], "x", m["h"], "opaque", m["opaque"],
          "bbox", m["bbox_w"], "x", m["bbox_h"], "fill", m["fill"],
          "blk", m["black_frac"], "pur", m["purple_frac"], "wht", m["white_frac"], flags)

with open(os.path.join(OUT, "fla44-measurements-20261101.json"), "w") as f:
    json.dump({"count": len(rows), "pieces": rows}, f, indent=1)
print("TOTAL", len(rows), "CLEAN", sum(1 for r in rows if r["draft_tier"] == "CLEAN"),
      "SHAPE-ONLY", sum(1 for r in rows if r["draft_tier"] == "SHAPE-ONLY"),
      "NEEDS-MARS", sum(1 for r in rows if r["draft_tier"] == "NEEDS-MARS"),
      "FLAGGED", sum(1 for r in rows if r["flags"]))
