#!/usr/bin/env python3
"""Group E proofs — METHOD-WIRED PROXIES ONLY.
No SAM 2 / Grounding DINO / MotionDiffuse / Animate Anyone weights ran here:
no GPU, no torch, headless VM (see GROUP-E.md). These are free PIL/numpy/ffmpeg
implementations of each method's *interface* on a synthetic flat-colour cutout
figure (NOT a Cape Jones character, NOT show art). Flat colours make exact-colour
masks equal connected components here; on real textured art the real models
would be required. No fake model scores are shown.
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.expanduser("~/workspace/cape-jones-rig/experimental-25-20261031/group-e-rig-labelling-editing/proofs")
os.makedirs(BASE, exist_ok=True)
W, H = 900, 600
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except Exception:
    FONT = ImageFont.load_default(); SMALL = FONT

# Synthetic cutout parts: name -> (colour, bbox, kind)
PARTS = {
    "head":   ((255, 200, 150), (395, 65, 505, 175), "ellipse"),
    "torso":  ((60, 120, 220),  (395, 180, 505, 380), "rect"),
    "arm_L":  ((80, 180, 100),  (300, 190, 390, 230), "rect"),
    "hand_L": ((255, 180, 80),  (265, 185, 305, 235), "ellipse"),
    "arm_R":  ((200, 80, 60),   (510, 190, 600, 230), "rect"),
    "hand_R": ((255, 180, 80),  (600, 185, 640, 235), "ellipse"),
    "leg_L":  ((90, 90, 140),   (410, 385, 445, 520), "rect"),
    "leg_R":  ((90, 90, 140),   (460, 385, 495, 520), "rect"),
    "foot_L": ((40, 40, 40),    (400, 520, 450, 545), "rect"),
    "foot_R": ((40, 40, 40),    (460, 520, 510, 545), "rect"),
}

def draw_figure(draw, arm_angle_L=0, arm_angle_R=0):
    """Draw flat-colour figure; arm angles rotate arm+hand around shoulder (deg)."""
    for name, (col, box, kind) in PARTS.items():
        if name in ("arm_L", "hand_L", "arm_R", "hand_R"):
            continue
        if kind == "ellipse": draw.ellipse(box, fill=col, outline=(0,0,0), width=2)
        else: draw.rectangle(box, fill=col, outline=(0,0,0), width=2)
    # arms as rotated rectangles via polygon
    def arm(cx, cy, length, angle_deg, col, is_left):
        a = math.radians(angle_deg + (180 if is_left else 0))
        # arm extends horizontally by default; rotate around shoulder
        dx, dy = math.cos(a)*length, math.sin(a)*length
        # thickness perpendicular
        px, py = -dy*0.18, dx*0.18
        pts = [(cx-px, cy-py), (cx+px, cy+py), (cx+dx+px, cy+dy+py), (cx+dx-px, cy+dy-py)]
        draw.polygon(pts, fill=col, outline=(0,0,0))
        hx, hy = cx+dx, cy+dy
        draw.ellipse([hx-22, hy-22, hx+22, hy+22], fill=(255,180,80), outline=(0,0,0), width=2)
    arm(395, 210, 100, arm_angle_L, (80,180,100), True)
    arm(505, 210, 100, arm_angle_R, (200,80,60), False)

def base_figure():
    im = Image.new("RGB", (W, H), (240, 240, 235))
    d = ImageDraw.Draw(im)
    draw_figure(d)
    return im

# ---- 01 SAM 2 proxy: prompt point in head -> exact-colour mask ----
fig = base_figure()
import numpy as np
arr = np.array(fig)
head_col = np.array([255, 200, 150])
mask = np.all(arr == head_col, axis=2)
print(f"SAM-proxy: head mask pixels={int(mask.sum())} (flat colour = connected component here)")
overlay = fig.copy()
ov = np.array(overlay).copy()
ov[mask] = (255, 0, 120)  # magenta mask overlay
out = Image.new("RGB", (W*2+20, H+50), (255,255,255))
out.paste(fig, (0, 50)); out.paste(Image.fromarray(ov), (W+20, 50))
d = ImageDraw.Draw(out)
d.text((10, 10), "01 SAM 2 PROXY — prompt point (450,120) in HEAD -> mask (magenta). NOT SAM 2 weights.", fill=(0,0,0), font=SMALL)
d.ellipse([445,115,455,125], fill=(255,0,0), outline=(0,0,0))
d.ellipse([W+20+445,115,W+20+455,125], fill=(255,0,0), outline=(0,0,0))
out.save(f"{BASE}/01-sam2-proxy_synthetic-cutout-20261031.png")

# ---- 02 Grounding DINO proxy: text prompts -> boxes from labelled geometry ----
gd = fig.copy(); d = ImageDraw.Draw(gd)
prompts = [("head", (395,65,505,175), (255,0,120)), ("hand", (265,185,305,235), (0,150,0)),
           ("hand", (600,185,640,235), (0,150,0)), ("torso", (395,180,505,380), (0,0,255))]
for label, box, col in prompts:
    d.rectangle(box, outline=col, width=4)
    d.text((box[0], max(0, box[1]-24)), label, fill=col, font=SMALL)
d.text((10, 10), "02 GROUNDING DINO PROXY — text prompts -> boxes. NO GDINO weights, NO scores.", fill=(0,0,0), font=SMALL)
gd.save(f"{BASE}/02-grounding-dino-proxy_boxes-20261031.png")
print(f"GDINO-proxy: boxes={len(prompts)}")

# ---- 03 MotionDiffuse proxy: text prompts -> parametric pose strip + joint CSV ----
poses = [
    ("a person stands still", 0, 0),
    ("a person raises left arm", -70, 0),
    ("a person punches with right arm", 0, -10),
    ("a person dances, both arms up", -120, -120),
    ("a person steps and swings arms", -40, 40),
    ("a person bows, arms down", 60, 60),
]
strip = Image.new("RGB", (W, 340), (255,255,255))
rows = []
for i, (prompt, al, ar) in enumerate(poses):
    cell = Image.new("RGB", (300, 300), (240,240,235))
    d = ImageDraw.Draw(cell)
    # scaled figure: draw simplified skeleton+cutout in cell coords
    d.ellipse([120,20,180,80], fill=(255,200,150), outline=(0,0,0), width=2)
    d.rectangle([120,85,180,190], fill=(60,120,220), outline=(0,0,0), width=2)
    def s_arm(cx, cy, length, ang, col, left):
        a = math.radians(ang + (180 if left else 0))
        dx, dy = math.cos(a)*length, math.sin(a)*length
        d.line([cx, cy, cx+dx, cy+dy], fill=col, width=10)
        d.ellipse([cx+dx-10, cy+dy-10, cx+dx+10, cy+dy+10], fill=(255,180,80), outline=(0,0,0))
    s_arm(120, 100, 60, al, (80,180,100), True)
    s_arm(180, 100, 60, ar, (200,80,60), False)
    d.line([135,190,135,260], fill=(90,90,140), width=10)
    d.line([165,190,165,260], fill=(90,90,140), width=10)
    strip.paste(cell, (i*150, 0)) if False else None
    # paste at 150px wide slots by resizing
    strip.paste(cell.resize((150,150)), (i*150, 30))
    d2 = ImageDraw.Draw(strip)
    d2.text((i*150+4, 185), prompt, fill=(0,0,0), font=SMALL)
    rows.append({"frame": i, "text_prompt": prompt, "arm_L_deg": al, "arm_R_deg": ar})
strip.save(f"{BASE}/03-motiondiffuse-proxy_keyframes-20261031.png")
with open(f"{BASE}/03-motiondiffuse-proxy_poses-20261031.csv", "w") as f:
    f.write("frame,text_prompt,arm_L_deg,arm_R_deg\n")
    for r in rows: f.write(f"{r['frame']},{r['text_prompt']},{r['arm_L_deg']},{r['arm_R_deg']}\n")
print(f"MotionDiffuse-proxy: poses={len(poses)}")

# ---- 04 Animate Anyone proxy: reference still + pose sequence -> frames + mp4 ----
frames_dir = f"{BASE}/frames-animate-anyone-proxy-20261031"
os.makedirs(frames_dir, exist_ok=True)
seq = [(0,0), (-40,0), (-80,-20), (-120,-60), (-120,-120), (-60,-60), (0,0), (0,-40), (-20,-80), (0,0), (-60,60), (0,0)]
for i, (al, ar) in enumerate(seq):
    im = Image.new("RGB", (W, H), (240,240,235))
    d = ImageDraw.Draw(im); draw_figure(d, al, ar)
    d.text((10,10), f"Animate Anyone PROXY frame {i} arm_L={al} arm_R={ar} — pose-driven cutout, NOT diffusion output", fill=(0,0,0), font=SMALL)
    im.save(f"{frames_dir}/frame-{i:02d}.png")
subprocess.run(["ffmpeg","-y","-v","error","-framerate","6","-i",f"{frames_dir}/frame-%02d.png",
                "-c:v","libx264","-pix_fmt","yuv420p",f"{BASE}/04-animate-anyone-proxy_pose-driven-20261031.mp4"], check=True)
# contact sheet
sheet = Image.new("RGB", (900, 600), (255,255,255))
for i in range(12):
    fr = Image.open(f"{frames_dir}/frame-{i:02d}.png").resize((225,150))
    sheet.paste(fr, ((i%4)*225, (i//4)*150))
sheet.save(f"{BASE}/04-animate-anyone-proxy_contact-sheet-20261031.png")
print(f"AnimateAnyone-proxy: frames={len(seq)}")

# ---- 05 Olive proxy: ffmpeg EDL edit — dance clip + fight clip, crossfade ----
# fight clip: punch poses only
fight_dir = f"{BASE}/frames-fight-proxy-20261031"; os.makedirs(fight_dir, exist_ok=True)
for i, (al, ar) in enumerate([(0,0),(0,-10),(0,-30),(0,0),(0,-40),(0,0)]):
    im = Image.new("RGB", (W, H), (240,240,235)); d = ImageDraw.Draw(im); draw_figure(d, al, ar)
    d.text((10,10), f"FIGHT proxy frame {i}", fill=(0,0,0), font=SMALL); im.save(f"{fight_dir}/frame-{i:02d}.png")
subprocess.run(["ffmpeg","-y","-v","error","-framerate","6","-i",f"{fight_dir}/frame-%02d.png",
                "-c:v","libx264","-pix_fmt","yuv420p",f"{BASE}/05-olive-proxy_fight-clip-20261031.mp4"], check=True)
# xfade dance(2s) + fight(1s), offset 1.5s, duration 0.5s
subprocess.run(["ffmpeg","-y","-v","error","-i",f"{BASE}/04-animate-anyone-proxy_pose-driven-20261031.mp4",
                "-i",f"{BASE}/05-olive-proxy_fight-clip-20261031.mp4","-filter_complex",
                "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=1.5[v]",
                "-map","[v]","-c:v","libx264","-pix_fmt","yuv420p",f"{BASE}/05-olive-proxy_edited-dance-fight-20261031.mp4"], check=True)
with open(f"{BASE}/05-olive-proxy_edl-20261031.txt","w") as f:
    f.write("OLIVE-METHOD EDL (ffmpeg implementation; Olive GUI did NOT run here — headless VM, alpha app)\n")
    f.write("001  dance  04-animate-anyone-proxy_pose-driven-20261031.mp4  00:00:00:00-00:00:02:00  CUT\n")
    f.write("002  fight  05-olive-proxy_fight-clip-20261031.mp4          00:00:00:00-00:00:01:00  XFADE 0.5s at 00:00:01:12\n")
    f.write("OUT  05-olive-proxy_edited-dance-fight-20261031.mp4\n")
meta = {"parts": len(PARTS), "gdino_boxes": len(prompts), "motion_poses": len(poses),
        "animate_frames": len(seq), "sam_head_mask_px": int(mask.sum())}
with open(f"{BASE}/proof-manifest-20261031.json","w") as f: json.dump(meta, f, indent=2)
print(json.dumps(meta, indent=2))
