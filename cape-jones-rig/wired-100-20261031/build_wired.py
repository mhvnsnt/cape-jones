#!/usr/bin/env python3
"""Wired-100 driver: PIL + FFmpeg + masks + XFL builder + sliced-clean use.
All outputs are NEW dated files in wired-100-20261031/, never overwriting
a version Mars has seen. Run from the rig root.
"""
import json, os, subprocess, sys
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "wired-100-20261031")
os.makedirs(OUT, exist_ok=True)
LOG = []

def log(msg):
    LOG.append(msg); print(msg)

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        log(f"CMD FAILED {cmd[:3]}: {r.stderr[-500:]}")
    return r

# --- 1. FFmpeg lut3d: approved neutral LUT on the fighting pose ---
pose = os.path.join(RIG, "reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")
lut = os.path.join(RIG, "showcase/lut-neutral.cube")
lut_out = os.path.join(OUT, "wired-ffmpeg-lut3d-fighting-20261031.png")
if os.path.exists(lut):
    r = run(["ffmpeg", "-y", "-i", pose, "-vf", f"lut3d={lut}", lut_out])
    log(f"FFmpeg lut3d: {lut_out} exists={os.path.exists(lut_out)} size={os.path.getsize(lut_out) if os.path.exists(lut_out) else 0}")
else:
    log(f"FFmpeg lut3d SKIPPED: LUT not found at {lut}")

# --- 2. Clean walk clips -> real MP4 via FFmpeg ---
walk_dir = os.path.join(RIG, "clips-v7c-clean-20261031/walk")
walk_mp4 = os.path.join(OUT, "wired-walk-clean-clips-20261031.mp4")
frames = sorted(os.listdir(walk_dir)) if os.path.isdir(walk_dir) else []
log(f"walk clean frames: {frames}")
if frames:
    # concat in sorted order, 24fps, 2 loops (8 frames)
    lst = os.path.join(OUT, "walk-concat.txt")
    with open(lst, "w") as f:
        for _ in range(2):
            for fn in frames:
                f.write(f"file '{os.path.join(walk_dir, fn)}'\n")
    r = run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-r", "24", "-i", lst,
             "-vf", "scale=550:750", "-pix_fmt", "yuv420p", walk_mp4])
    log(f"walk MP4: {walk_mp4} exists={os.path.exists(walk_mp4)} size={os.path.getsize(walk_mp4) if os.path.exists(walk_mp4) else 0}")

# --- 3. Audio loudness measurement (owed: 0/5 cues measured) ---
wav = os.path.join(RIG, "showcase/audio/cape-jones-audio-cues-demo.wav")
loud = os.path.join(OUT, "wired-audio-loudnorm-20261031.json")
if os.path.exists(wav):
    r = run(["ffmpeg", "-i", wav, "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    # loudnorm JSON is on stderr after [Parsed_loudnorm...]
    txt = r.stderr
    j = txt[txt.find("{"):txt.rfind("}") + 1] if "{" in txt else "{}"
    try:
        data = json.loads(j)
    except Exception:
        data = {"raw_tail": txt[-400:]}
    json.dump(data, open(loud, "w"), indent=2)
    log(f"audio loudnorm measured: {data}")
else:
    log(f"audio SKIPPED: {wav} missing")

# --- 4. Shot-spec CJ-01 end-to-end through PIL Level 2 v2 ---
punch = os.path.join(RIG, "clips-v7c/punch-impact-locked-v7c.png")
cj_outdir = os.path.join(OUT, "wired-shot-cj01-punch-level2")
if os.path.exists(punch):
    r = run([sys.executable, os.path.join(RIG, "apply_lighting_level2_v2.py"), punch, cj_outdir])
    log(f"CJ-01 Level2: outdir={cj_outdir} files={sorted(os.listdir(cj_outdir)) if os.path.isdir(cj_outdir) else 'NONE'} rc={r.returncode} {r.stderr[-300:]}")
else:
    log(f"CJ-01 SKIPPED: punch file missing")

# --- 5. Blender masks (full-size, 1100x1500): shadow ellipse+pads, line light, fade ---
plate = Image.open(pose).convert("RGBA")
W, H = plate.size
alpha = np.array(plate.split()[3]) > 10
ys, xs = np.where(alpha)
xmin, xmax, ymin, ymax = xs.min(), xs.max(), ys.min(), ys.max()
log(f"fighting bbox x {xmin}-{xmax} y {ymin}-{ymax}")
# shadow mask: ellipse under feet + two pads at foot bottoms (bottom-most alpha per half)
shadow = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(shadow)
cx, cy, rx, ry = (xmin + xmax) // 2, ymax + 30, (xmax - xmin) // 2 + 40, 55
d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
mid = (xmin + xmax) // 2
for half in [(xmin, mid), (mid, xmax)]:
    col = alpha[:, half[0]:half[1]]
    rows = np.where(col.any(axis=1))[0]
    if len(rows):
        fy = rows.max()
        fx = int(np.where(col[fy])[0].mean()) + half[0] if col[fy].any() else (half[0] + half[1]) // 2
        d.ellipse([fx - 70, fy - 10, fx + 70, fy + 35], fill=255)
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
shadow.save(os.path.join(OUT, "wired-blender-shadow-ellipse-pads-mask-20261031.png"))
# line-light mask: internal edge band (dilated alpha minus eroded alpha, inner 12px)
a_img = plate.split()[3]
dil = a_img.filter(ImageFilter.MaxFilter(13))
ero = a_img.filter(ImageFilter.MinFilter(25))
line = Image.new("L", (W, H), 0)
la = np.array(dil, dtype=int) - np.array(ero, dtype=int)
line_arr = np.clip(la, 0, 255).astype(np.uint8)
# keep only inside silhouette
line_arr = np.where(alpha, line_arr, 0).astype(np.uint8)
Image.fromarray(line_arr).filter(ImageFilter.GaussianBlur(2)).save(os.path.join(OUT, "wired-blender-linellight-mask-20261031.png"))
# fade mask: lit side left 255 -> right 76 (1.0 -> 0.3), horizontal gradient
grad = np.tile(np.linspace(255, 76, W, dtype=np.uint8), (H, 1))
Image.fromarray(grad).save(os.path.join(OUT, "wired-blender-fade-mask-20261031.png"))
log("Blender masks written: shadow ellipse+pads, line light, fade")

# --- 6. Sliced-clean USE: a real layout shot from a sliced-clean full figure ---
# B-model sheets are 1 piece each (full figures). Use one as a plate in a
# new layout shot (room-style ground, seated scale rule NOT applied here).
bdir = os.path.join(RIG, "sliced-clean-20261031/B-model/model-sheet-front-set2")
log(f"B-model dir: {bdir} exists={os.path.isdir(bdir)}")
if os.path.isdir(bdir):
    pieces = []
    for root, _, files in os.walk(bdir):
        for fn in files:
            if fn.lower().endswith(".png"):
                pieces.append(os.path.join(root, fn))
    log(f"B-model pieces: {pieces[:5]} count={len(pieces)}")
    if pieces:
        fig = Image.open(pieces[0]).convert("RGBA")
        # composite on grey-128 control + ground line, 1168x784 layout canvas
        canvas = Image.new("RGBA", (1168, 784), (128, 128, 128, 255))
        fig_s = fig.copy(); fig_s.thumbnail((400, 700))
        canvas.alpha_composite(fig_s, ((1168 - fig_s.size[0]) // 2, 784 - fig_s.size[1] - 20))
        canvas.convert("RGB").save(os.path.join(OUT, "wired-sliced-clean-layout-20261031.jpg"), quality=92)
        log(f"sliced-clean layout shot written from {pieces[0]}")

# --- 7. JSFL logic -> runnable XFL builder (Animate run still blocked) ---
clip_path = os.path.join(RIG, "clips/punch-clip.json")
xfl_dir = os.path.join(OUT, "wired-xfl-punch-20261031")
os.makedirs(os.path.join(xfl_dir, "LIBRARY"), exist_ok=True)
layers = ["Head_Front", "Torso_Chest", "Pelvis", "Arm_Front_Upper", "Arm_Front_Lower",
          "Arm_Back_Upper", "Arm_Back_Lower", "Leg_Front_Upper", "Leg_Front_Lower",
          "Leg_Back_Upper", "Leg_Back_Lower", "Cape_Back_Main", "Cape_Collar", "Neck", "Belt"]
clip = {}
if os.path.exists(clip_path):
    try:
        clip = json.load(open(clip_path))
    except Exception as e:
        log(f"punch clip parse failed: {e}")
keyframes = clip.get("keyframes", []) if isinstance(clip, dict) else []
log(f"punch clip keyframes: {len(keyframes)} clip keys: {list(clip.keys())[:8] if isinstance(clip, dict) else 'n/a'}")
# DOMDocument: one timeline, one layer per limb, keyframes at clip frames,
# rotation = 90 - clipAngle (the JSFL conversion, documented in the .jsfl)
tl_layers = ""
for li, lname in enumerate(layers):
    frames_xml = ""
    for kf in keyframes:
        fnum = kf.get("frame", 1)
        # map layer to a clip angle key if present, else 0
        keymap = {"Arm_Front_Upper": "arm1_upper", "Arm_Front_Lower": "arm1_lower",
                  "Arm_Back_Upper": "arm2_upper", "Arm_Back_Lower": "arm2_lower",
                  "Leg_Front_Upper": "leg1_upper", "Leg_Front_Lower": "leg1_lower",
                  "Leg_Back_Upper": "leg2_upper", "Leg_Back_Lower": "leg2_lower"}
        ang = kf.get(keymap.get(lname, ""), 0) if keymap.get(lname) else 0
        rot = 90 - float(ang or 0)
        frames_xml += f'<DOMFrame index="{int(fnum)-1}" duration="6"><elements><DOMSymbolInstance rotation="{rot}"/></elements></DOMFrame>'
    if not frames_xml:
        frames_xml = '<DOMFrame index="0" duration="24"><elements><DOMSymbolInstance rotation="0"/></elements></DOMFrame>'
    tl_layers += f'<DOMLayer name="{lname}" color="#FF0000" current="0" isSelected="0"><frames>{frames_xml}</frames></DOMLayer>'
dom = f'''<?xml version="1.0" encoding="UTF-8"?>
<DOMDocument xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://ns.adobe.com/xfl/2008/" width="1100" height="1500" frameRate="24" backgroundColor="#808080" currentTimeline="1">
<timelines><DOMTimeline name="CapeJonesPunch_WiredFromJSFL"><layers>{tl_layers}</layers></DOMTimeline></timelines>
<symbols></symbols>
</DOMDocument>'''
open(os.path.join(xfl_dir, "DOMDocument.xml"), "w").write(dom)
# verify by re-parsing
import xml.etree.ElementTree as ET
ns = {"x": "http://ns.adobe.com/xfl/2008/"}
tree = ET.parse(os.path.join(xfl_dir, "DOMDocument.xml"))
found_layers = tree.getroot().findall(".//x:DOMLayer", ns)
found_frames = tree.getroot().findall(".//x:DOMFrame", ns)
log(f"XFL verified: layers={len(found_layers)} frames={len(found_frames)} (JSFL logic, Animate run still blocked)")

json.dump(LOG, open(os.path.join(OUT, "wired-driver-log-20261031.json"), "w"), indent=2)
print("DRIVER DONE")
