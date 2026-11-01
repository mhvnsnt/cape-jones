"""Clean punch plates CJ-01..CJ-05, 2026-10-31. Art/assets owed batch, ordered 2026-10-31 23:54 CDT.

Method (standing, not invented):
- Rig: joint_locked_rig_v7c, labels=False ONLY (LABELS-ARE-DEBUG-ONLY rule:
  red numbered ARM/LEG circles are debug, never part of a shot; white
  elbow/knee joint balls ARE character joints and stay).
- Rig builder copy: clean-100-20261031/exposure-clips/rig-v7c-clean100.py
  (same anchors/scale/piece order as joint_locked_rig_v7c.py, output path +
  OutFixed selectable). Punch uses ORIGINAL lowers, never OutFixed:
  punch is not the fighting pose (clean-100 note: -110/-70/-90 are below
  the 120 threshold; -110 is the Mars-locked punch frame; 160-current =
  punch-09). OutFixed applies only to the fighting pose.
- Poses: punch-clip.json keyframes for CJ-01/02/04; punch_base from
  clean-100 build-clean100.py for CJ-03/05 (L -90/-90, R 20, legs -15/15,
  15/-15; R lower -110 locked for CJ-03, -70 across-down for CJ-05).
- Transparency: transparent-plates-sweep convert() method verbatim
  (bg = median of 4 corners, mask distance > 30, closing 3x3 x2 + hole
  fill, components >= 800, 1px feather + fringe decontamination,
  original canvas 1100x1500 kept, no crop, interior never recoloured).
- No original touched, no repo push. Outputs only in this folder.
- Control (NOT plates): v7 rig with its label block stripped, same
  punch-clip configs, to isolate the v7->v7c geometry delta for
  CJ-01/02/04 from the label-removal delta. Controls live in
  control-v7b-stripped-NOT-plates/ and are never used as shot plates.
"""
import os, sys, json, hashlib, importlib.util
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "art-owed-punch-plates-20261031")
PLATES = os.path.join(OUT, "plates-clean")
CTRL = os.path.join(OUT, "control-v7b-stripped-NOT-plates")
os.makedirs(PLATES, exist_ok=True); os.makedirs(CTRL, exist_ok=True)

spec = importlib.util.spec_from_file_location(
    "rigv7c", os.path.join(RIG, "clean-100-20261031/exposure-clips/rig-v7c-clean100.py"))
rig = importlib.util.module_from_spec(spec); spec.loader.exec_module(rig)

SHOTS = [
    # shot, slug, cfg, labelled source plate (transparent sweep), labelled source RGB
    ("CJ-01", "punch-windup",
     {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -120, "R": 160},
      "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}},
     "transparent-plates-sweep-20261031/plates/clips-v7__punch__punch-01-windup-v7.png",
     "clips-v7/punch/punch-01-windup-v7.png"),
    ("CJ-02", "punch-extend-snap",
     {"arm_upper": {"L": -90, "R": 20}, "arm_lower": {"L": -90, "R": 160},
      "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": 15, "R": -15}},
     "transparent-plates-sweep-20261031/plates/clips-v7__punch__punch-07-extend-snap-v7.png",
     "clips-v7/punch/punch-07-extend-snap-v7.png"),
    ("CJ-03", "punch-impact-locked",
     {"arm_upper": {"L": -90, "R": 20}, "arm_lower": {"L": -90, "R": -110},
      "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": 15, "R": -15}},
     "transparent-plates-sweep-20261031/plates/clips-v7c__punch-impact-locked-v7c.png",
     "clips-v7c/punch-impact-locked-v7c.png"),
    ("CJ-04", "punch-recover",
     {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
      "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}},
     "transparent-plates-sweep-20261031/plates/clips-v7__punch__punch-21-recover-v7.png",
     "clips-v7/punch/punch-21-recover-v7.png"),
    ("CJ-05", "punch-across-down-placement",
     {"arm_upper": {"L": -90, "R": 20}, "arm_lower": {"L": -90, "R": -70},
      "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": 15, "R": -15}},
     "transparent-plates-sweep-20261031/plates/clips-v7c__punch-arm2-variants__punch-impact-a2l-minus70-across-down-v7c.png",
     "clips-v7c/punch-arm2-variants/punch-impact-a2l-minus70-across-down-v7c.png"),
]

def sha12(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]

def redcount_rgb(arr):
    a = arr.astype(int)
    return int(((a[:, :, 0] > 200) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)).sum())

def redcount_rgba(path):
    a = np.array(Image.open(path).convert("RGBA")).astype(int)
    return int(((a[:, :, 0] > 200) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90) & (a[:, :, 3] > 10)).sum())

def convert_transparent(src, dst):
    """Verbatim from transparent-plates-sweep-20261031/convert_plates.py."""
    im = Image.open(src).convert("RGB")
    arr = np.array(im).astype(float)
    corners = np.concatenate([arr[:5, :5].reshape(-1, 3), arr[:5, -5:].reshape(-1, 3),
                              arr[-5:, :5].reshape(-1, 3), arr[-5:, -5:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((arr - bg) ** 2).sum(axis=2))
    mask = dist > 30
    mask = ndimage.binary_closing(mask, structure=np.ones((3, 3)), iterations=2)
    mask = ndimage.binary_fill_holes(mask)
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    keep = np.zeros_like(mask)
    for i in range(1, n + 1):
        if (lab == i).sum() >= 800:
            keep |= (lab == i)
    alpha = (keep * 255).astype(float)
    alpha = ndimage.gaussian_filter(alpha, 0.8)
    alpha_u8 = np.clip(alpha, 0, 255).astype(np.uint8)
    rgb = arr.copy()
    a = np.clip(alpha / 255.0, 0.01, 1.0)[..., None]
    rgb = np.clip((arr - bg * (1 - a)) / a, 0, 255)
    rgb[keep] = arr[keep]
    rgba = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
    rgba[:, :, :3] = rgb.astype(np.uint8)
    rgba[:, :, 3] = alpha_u8
    Image.fromarray(rgba, "RGBA").save(dst)
    ys, xs = np.where(alpha_u8 > 10)
    return {"bg": bg.tolist(), "size": list(im.size),
            "alpha_px": int((alpha_u8 > 10).sum()),
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}

def label_mask():
    m = Image.new("L", (1100, 1500), 0); d = ImageDraw.Draw(m)
    for (x, y) in [(340, 430), (760, 430), (400, 820), (700, 820)]:
        d.ellipse((x - 32, y - 32, x + 32, y + 32), fill=1)
    for (x, y) in [(300, 470), (720, 470), (360, 860), (660, 860)]:
        d.rectangle((x - 5, y - 5, x + 70, y + 20), fill=1)
    return np.array(m) > 0

LM = label_mask()
manifest = []

# --- v7b-stripped controls: v7b build functions only, label block removed ---
# (clips-v7 punch files were built with the v7b rig: v7b-stripped matches the
#  labelled source outside the label mask exactly, 0 px, for CJ-01/02/04.)
v7bsrc = open(os.path.join(RIG, "joint_locked_rig_v7b.py")).read()
v7bsrc = v7bsrc.split('build("joint-apose-v7')[0]
# remove the unconditional label block (from ImageDraw import to the save line's label calls)
lines = v7bsrc.splitlines(True)
cut_start = next(i for i, l in enumerate(lines) if "from PIL import ImageDraw" in l)
cut_end = next(i for i, l in enumerate(lines) if "canvas.convert" in l)
v7bsrc = "".join(lines[:cut_start] + lines[cut_end:])
ns = {"__name__": "v7stripped"}
exec(v7bsrc, ns)
v7bbuild = ns["build"]

for sid, slug, cfg, src_plate, src_rgb in SHOTS:
    rgb_name = f"{sid}-{slug}-clean-rig-rgb-20261031.png"
    plate_name = f"{sid}-{slug}-clean-plate-20261031.png"
    rgb_path = os.path.join(PLATES, rgb_name)
    plate_path = os.path.join(PLATES, plate_name)
    rig.build(rgb_path, cfg, labels=False, outfixed=False)
    rgb_arr = np.array(Image.open(rgb_path).convert("RGB"))
    assert redcount_rgb(rgb_arr) == 0, f"{sid} rig render still has red px"
    conv = convert_transparent(rgb_path, plate_path)
    assert redcount_rgba(plate_path) == 0, f"{sid} clean plate still has red px"
    # compare clean RGB vs labelled RGB source
    src_arr = np.array(Image.open(os.path.join(RIG, src_rgb)).convert("RGB")).astype(int)
    diff = np.any(src_arr != rgb_arr.astype(int), axis=2)
    # old transparent plate red count + old final workaround note
    old_plate_arr = np.array(Image.open(os.path.join(RIG, src_plate)).convert("RGBA"))
    old_red = int(((old_plate_arr[:, :, 0] > 200) & (old_plate_arr[:, :, 1] < 90)
                   & (old_plate_arr[:, :, 2] < 90) & (old_plate_arr[:, :, 3] > 10)).sum())
    # v7b control
    ctrl_path = os.path.join(CTRL, f"{sid}-{slug}-v7b-stripped-control-20261031.png")
    ns["OUT"] = CTRL
    v7bbuild(f"{sid}-{slug}-v7b-stripped-control-20261031.png", cfg)
    ctrl_arr = np.array(Image.open(ctrl_path).convert("RGB")).astype(int)
    ctrl_diff = np.any(src_arr != ctrl_arr, axis=2)
    rec = {
        "shot": sid, "slug": slug, "cfg": cfg,
        "clean_rig_rgb": f"plates-clean/{rgb_name}", "clean_plate": f"plates-clean/{plate_name}",
        "labelled_source_rgb": src_rgb, "labelled_source_plate": src_plate,
        "clean_rgb_red_px": 0, "clean_plate_red_px": 0,
        "old_plate_red_px": old_red,
        "rgb_size": list(Image.open(rgb_path).size),
        "plate_size": conv["size"], "plate_alpha_px": conv["alpha_px"], "plate_bbox": conv["bbox"],
        "plate_sha12": sha12(plate_path), "rgb_sha12": sha12(rgb_path),
        "diff_vs_labelled_rgb_all": int(diff.sum()),
        "diff_vs_labelled_rgb_outside_label_mask": int((diff & ~LM).sum()),
        "diff_vs_labelled_rgb_inside_label_mask": int((diff & LM).sum()),
        "v7b_control_vs_labelled_outside_label_mask": int((ctrl_diff & ~LM).sum()),
        "v7b_control_file": f"control-v7b-stripped-NOT-plates/{os.path.basename(ctrl_path)}",
        "method": "joint_locked_rig_v7c labels=False, original lowers; transparent convert (sweep method)",
    }
    manifest.append(rec)
    print(sid, "old_red", old_red, "plate_alpha", conv["alpha_px"], "bbox", conv["bbox"],
          "diff_outside_labels", rec["diff_vs_labelled_rgb_outside_label_mask"],
          "v7ctrl_outside", rec["v7b_control_vs_labelled_outside_label_mask"])

json.dump({"batch": "art-owed-punch-plates-20261031", "plates": manifest},
          open(os.path.join(OUT, "clean-plates-manifest-20261031.json"), "w"), indent=1)
print("DONE plates", len(manifest))
