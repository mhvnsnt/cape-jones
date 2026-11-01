#!/usr/bin/env python3
"""Group B method-wired pose-angle tool (NOT a detector).

Honest labelling, read this first:
- No detector ran to produce these keypoints. Each keypoint set below was
  placed MANUALLY by eye from a viewed Cape pose image (the joint circles
  in the v7c cutout art make shoulder/elbow/wrist/hip/knee/ankle visible).
- What this script DOES do, for real, on real Cape frames: take a keypoint
  set, compute joint angles with vector maths, run knee-feet + balance
  checks, and draw the skeleton ONLY on a new copy (overlay layer).
  Originals in pose-dialects-20261031/ are never opened for writing.
- If a real detector (MediaPipe / OpenPose / DWPose) is later run, its
  output JSON can replace the "keypoints" dict below with no other change:
  the angle maths and the Cape-rig mapping are detector-agnostic.
  That is the "method-wired" claim, and nothing more.

Angles: interior angle at the middle joint, degrees, 180 = straight limb.
Knee-feet check: |knee_x - ankle_x| in image-width fractions, and foot
turnout = angle of ankle->toe from straight-down.
Balance (Cascadeur-method analogue): centre of mass approximated as the
hip midpoint; support interval = [min ankle x, max ankle x]; the pose is
"inside support" if COM x falls inside that interval (single-frame, 2D,
no depth — a proxy, not AutoPhysics).
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.expanduser("~/workspace/cape-jones-rig/pose-dialects-20261031")
OUT = os.path.dirname(os.path.abspath(__file__)) + "/proofs"
os.makedirs(OUT, exist_ok=True)

# keypoints: (x, y) fractions of image size. L/R = image-left / image-right.
# Source images are 1100x1500; fractions keep the tool resolution-free.
POSES = {
    "jojo-01": {
        "file": "jojo-01-contrapposto-s-curve-20261031.png",
        "kp": {"nose": (.54, .235), "shoulder_L": (.36, .325), "shoulder_R": (.66, .325),
               "elbow_L": (.24, .36), "elbow_R": (.735, .43),
               "wrist_L": (.31, .235), "wrist_R": (.625, .525),
               "hip_L": (.42, .535), "hip_R": (.585, .535),
               "knee_L": (.29, .645), "knee_R": (.715, .645),
               "ankle_L": (.335, .84), "ankle_R": (.675, .84),
               "toe_L": (.30, .875), "toe_R": (.70, .875)}},
    "jojo-02": {
        "file": "jojo-02-fashion-twist-point-20261031.png",
        "kp": {"nose": (.53, .235), "shoulder_L": (.36, .325), "shoulder_R": (.64, .325),
               "elbow_L": (.22, .27), "elbow_R": (.755, .365),
               "wrist_L": (.20, .255), "wrist_R": (.545, .345),
               "hip_L": (.42, .535), "hip_R": (.585, .535),
               "knee_L": (.335, .655), "knee_R": (.685, .635),
               "ankle_L": (.33, .87), "ankle_R": (.65, .84),
               "toe_L": (.30, .905), "toe_R": (.68, .875)}},
    "ginyu-02": {
        "file": "ginyu-02-squat-elbows-out-goofy-20261031.png",
        "kp": {"nose": (.50, .235), "shoulder_L": (.37, .325), "shoulder_R": (.63, .325),
               "elbow_L": (.225, .35), "elbow_R": (.775, .35),
               "wrist_L": (.27, .21), "wrist_R": (.73, .21),
               "hip_L": (.42, .535), "hip_R": (.58, .535),
               "knee_L": (.24, .62), "knee_R": (.76, .62),
               "ankle_L": (.36, .82), "ankle_R": (.64, .82),
               "toe_L": (.34, .86), "toe_R": (.66, .86)}},
    "ginyu-03": {
        "file": "ginyu-03-dance-shimmy-hips-out-20261031.png",
        "kp": {"nose": (.50, .235), "shoulder_L": (.36, .325), "shoulder_R": (.64, .325),
               "elbow_L": (.245, .26), "elbow_R": (.755, .26),
               "wrist_L": (.11, .345), "wrist_R": (.89, .345),
               "hip_L": (.42, .535), "hip_R": (.585, .535),
               "knee_L": (.295, .66), "knee_R": (.705, .64),
               "ankle_L": (.355, .855), "ankle_R": (.645, .84),
               "toe_L": (.345, .89), "toe_R": (.665, .875)}},
}

EDGES = [("nose", "shoulder_L"), ("nose", "shoulder_R"),
         ("shoulder_L", "shoulder_R"), ("shoulder_L", "elbow_L"),
         ("elbow_L", "wrist_L"), ("shoulder_R", "elbow_R"),
         ("elbow_R", "wrist_R"), ("shoulder_L", "hip_L"),
         ("shoulder_R", "hip_R"), ("hip_L", "hip_R"),
         ("hip_L", "knee_L"), ("knee_L", "ankle_L"), ("ankle_L", "toe_L"),
         ("hip_R", "knee_R"), ("knee_R", "ankle_R"), ("ankle_R", "toe_R")]

def angle(a, b, c):
    """Interior angle at b, degrees."""
    v1 = (a[0]-b[0], a[1]-b[1]); v2 = (c[0]-b[0], c[1]-b[1])
    d = math.hypot(*v1) * math.hypot(*v2)
    if d == 0: return 0.0
    cosv = max(-1.0, min(1.0, (v1[0]*v2[0]+v1[1]*v2[1]) / d))
    return round(math.degrees(math.acos(cosv)), 1)

def analyse(name):
    kp = POSES[name]["kp"]
    r = {}
    for side in ("L", "R"):
        r[f"elbow_{side}"] = angle(kp[f"shoulder_{side}"], kp[f"elbow_{side}"], kp[f"wrist_{side}"])
        r[f"knee_{side}"] = angle(kp[f"hip_{side}"], kp[f"knee_{side}"], kp[f"ankle_{side}"])
        r[f"shoulder_{side}"] = angle(kp[f"hip_{side}"], kp[f"shoulder_{side}"], kp[f"elbow_{side}"])
        r[f"hip_{side}"] = angle(kp[f"shoulder_{side}"], kp[f"hip_{side}"], kp[f"knee_{side}"])
        # foot turnout: ankle->toe vs straight down (0,1)
        dx = kp[f"toe_{side}"][0]-kp[f"ankle_{side}"][0]
        dy = kp[f"toe_{side}"][1]-kp[f"ankle_{side}"][1]
        r[f"foot_turnout_{side}"] = round(math.degrees(math.atan2(abs(dx), abs(dy))), 1)
        r[f"knee_ankle_offset_{side}"] = round(abs(kp[f"knee_{side}"][0]-kp[f"ankle_{side}"][0]), 3)
    com_x = (kp["hip_L"][0]+kp["hip_R"][0]) / 2
    lo, hi = min(kp["ankle_L"][0], kp["ankle_R"][0]), max(kp["ankle_L"][0], kp["ankle_R"][0])
    r["com_x"] = round(com_x, 3)
    r["support_span"] = [round(lo, 3), round(hi, 3)]
    r["com_inside_support"] = bool(lo <= com_x <= hi)
    r["com_margin_to_edge"] = round(min(abs(com_x-lo), abs(com_x-hi)), 3)
    return r

def draw_overlay(pose_name, title, footer, out_name, extra=None):
    src = os.path.join(BASE, POSES[pose_name]["file"])
    img = Image.open(src).convert("RGBA")
    W, H = img.size
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    kp = POSES[pose_name]["kp"]
    px = {k: (v[0]*W, v[1]*H) for k, v in kp.items()}
    for a, b in EDGES:
        d.line([px[a], px[b]], fill=(0, 255, 255, 255), width=6)
    for k, (x, y) in px.items():
        d.ellipse([x-13, y-13, x+13, y+13], fill=(255, 220, 0, 255), outline=(0, 0, 0, 255), width=3)
    r = analyse(pose_name)
    # header banner (overlay only — base art untouched underneath)
    d.rectangle([0, 0, W, 92], fill=(0, 0, 0, 200))
    d.text((20, 14), title, fill=(255, 255, 0, 255))
    d.text((20, 52), "METHOD-WIRED: keypoints placed by eye, NOT detector output. Overlay only.", fill=(255, 255, 255, 255))
    lines = [f"elbow L {r['elbow_L']}  R {r['elbow_R']}   knee L {r['knee_L']}  R {r['knee_R']}",
             f"shoulder L {r['shoulder_L']}  R {r['shoulder_R']}   hip L {r['hip_L']}  R {r['hip_R']}",
             f"foot turnout L {r['foot_turnout_L']}deg  R {r['foot_turnout_R']}deg   knee-ankle offset L {r['knee_ankle_offset_L']}  R {r['knee_ankle_offset_R']}",
             f"COM x {r['com_x']}  support {r['support_span']}  inside={r['com_inside_support']}  margin {r['com_margin_to_edge']}"]
    if extra: lines += extra
    y = H + 8  # readout lives on the added strip, never over the feet
    # (drawn on ov at y>=H: ov is H tall, so draw readout on canvas instead — see below)
    pass  # readout drawn on the strip below, after compositing
    comp = Image.alpha_composite(img, ov)
    canvas = Image.new("RGBA", (W, H+210), (0, 0, 0, 255))
    canvas.paste(comp, (0, 0))
    dc = ImageDraw.Draw(canvas)
    dc.rectangle([0, H, W, H+210], fill=(0, 0, 0, 255))
    yy = H + 10
    for ln in lines:
        dc.text((20, yy), ln, fill=(255, 255, 255, 255)); yy += 30
    dc.text((20, H+174), footer, fill=(255, 255, 0, 255))
    out = canvas.convert("RGB")
    path = os.path.join(OUT, out_name)
    out.save(path)
    return path, r

if __name__ == "__main__":
    report = {}
    proofs = [
        ("jojo-01", "1 MEDIAPIPE-POSE (BlazePose 33-pt schema, body subset shown)",
         "Cape rig: shoulder/elbow/wrist + hip/knee/ankle -> Arm_Front/Back, Leg_Front/Back",
         "proof-01-mediapipe-jojo01-overlay-20261031.png", None),
        ("ginyu-02", "2 OPENPOSE (BODY_25 schema, body+foot subset shown)",
         "Cape rig: foot toe/heel points check squat feet; multi-person N/A (1 figure)",
         "proof-02-openpose-ginyu02-squat-overlay-20261031.png", None),
        ("jojo-02", "3 DWPOSE (whole-body 133-pt schema, body subset shown)",
         "Cape rig: twist pose — hand/face detail is DWPose's edge; body angles here",
         "proof-03-dwpose-jojo02-twist-overlay-20261031.png", None),
        ("ginyu-02", "4 CASCADEUR-METHOD (AutoPhysics analogue: COM vs support)",
         "Balance verdict below is a 2D proxy, NOT Cascadeur AutoPhysics output",
         "proof-04-cascadeur-method-ginyu02-balance-20261031.png",
         ["BALANCE (2D proxy): COM inside support = stable squat; knees wide, feet planted."]),
        ("ginyu-03", "5 PLASK (primary) / MOVEAI (compared) — retarget map",
         "Retarget: video-mocap joints -> Cape rig joints (table in GROUP-B.md)",
         "proof-05-plask-moveai-ginyu03-dance-retarget-20261031.png",
         ["RETARGET: wrist->fist, elbow->arm joint, shoulder->torso, hip->pelvis, knee->leg joint, ankle->boot."]),
    ]
    for pose, title, footer, fname, extra in proofs:
        path, r = draw_overlay(pose, title, footer, fname, extra)
        report[fname] = {"pose": pose, "source": POSES[pose]["file"], "angles": r}
        print(fname, r)
    # contact sheet of the 5 proofs, scaled down
    import glob as _g
    thumbs = []
    for _, _, _, fname, _ in proofs:
        im0=Image.open(os.path.join(OUT, fname)); thumbs.append(im0.resize((440, int(440*im0.size[1]/im0.size[0]))))
    sheet = Image.new("RGB", (440*5, thumbs[0].size[1]), (20, 20, 20))
    for i, t in enumerate(thumbs): sheet.paste(t, (440*i, 0))
    sheet.save(os.path.join(OUT, "proofs-contact-20261031.png"))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pose-angles-20261031.json"), "w") as f:
        json.dump(report, f, indent=2)
    print("contact + json written")
