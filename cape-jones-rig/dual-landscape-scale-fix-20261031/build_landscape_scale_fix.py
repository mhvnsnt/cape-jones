#!/usr/bin/env python3
"""Landscape scale fix, 2026-10-31.
Owns the revert plainly: the delivered 1920x1080 landscape shrank the figure
to 655px tall, down from 1165px in the 1920 master, even though the old report
claimed '60.7% relative scale / figure and room scaled together'. That claim
was wrong in scene terms (see REPORT). This script rebuilds landscape from
the master SCENE, not from a fresh 1080-height composition:

- Scene: original room BG (1168x784) at MASTER scale 2.449 -> 2860x1920.
  Master was a centre crop x470..2390 of that scene, y0..1920.
- Figure (base-arms-up, alpha bbox (222,239,880,1283), 1100x1500):
  2.5x lock = master placement, alpha height 1165, scene bbox
  x1063..1797, y385..1550, feet 1550, centre x1430 (= scene centre).
  3.0x candidate = 2.5 + 0.5, figure x1.2 in scene, alpha height 1398,
  scene bbox x990..1870, y152..1550, feet STILL 1550 (feet on floor,
  growth goes up, not down through the floor).
- Pull-back window: a 16:9 window in the scene containing the whole
  figure + ~40px margin, resized to 1920x1080. This is the ONLY shrink
  allowed, and it shrinks figure and room TOGETHER by the window factor,
  so the figure-to-furniture ratio is preserved exactly (2.5x) or
  increased exactly 1.2x (3.0x). It is NOT a fresh '60.7% of 1080' figure.
- A whole figure at master scene scale does NOT fit a 1920x1080 frame
  without a window: 1165 > 1080 by 85px (2.5x), 1398 > 1080 by 318px
  (3.0x). The centre-crop cut of the master is shown in the contact
  as proof: head cut 35px, feet cut 50px at 2.5x.
- Chair anchor (scene, master crop): chair-back top y~700, chair feet
  y~1518, chair height ~818px in scene. Figure-to-chair ratios:
  master 1165/818 = 1.424; reverted landscape 655/549 = 1.193 (-16.2%);
  new 2.5x window ratio = 1.424 (preserved); new 3.0x = 1.707 (+20.0%
  vs 2.5x, exactly 0.5/2.5).
- Chair-back-at-waist: waist in master ~1002, chair-back top ~700,
  diff 302px. Forcing equality with feet on floor would need height
  (1550-700)/0.47 = 1809px, head at -161, off-frame. Reported as
  WARNING, never faked as PASS, in this KKGuh arms-up crop.
- Background: STAND-IN batch-KKGuh, NOT canonical. No recolour.
"""
import json, os
from PIL import Image, ImageDraw

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "dual-light-variants-20261031/base-arms-up-transparent-20261031.png")
BG = os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets/backgrounds/batch-KKGuh.jpg")
OLDLAND = os.path.join(ROOT, "dual-orientation-room-scale-fix-20261031/landscape-room-scale-1920x1080-20261031.png")

fig = Image.open(FIG).convert("RGBA")
fb = fig.split()[3].getbbox()  # (222,239,880,1283)
alpha_frac = (fb[3] - fb[1]) / fig.height  # 1044/1500 = 0.696
bg = Image.open(BG).convert("RGB")

# Scene at master scale
ROOM_SCALE = 2860 / 1168  # 2.449, master cover scale
scene = bg.resize((2860, 1920), Image.LANCZOS).convert("RGBA")
CX = 1430  # scene centre x = figure centre x in master

def place_figure(scale_mult):
    """scale_mult 1.0 = 2.5x lock, 1.2 = 3.0x candidate. Returns (img, bbox, fh)."""
    H = round(1165 * scale_mult)
    fh = round(H / alpha_frac)
    fw = round(fig.width * fh / fig.height)
    fs = fig.resize((fw, fh), Image.LANCZOS)
    # feet alpha bottom at scene y=1550, centre x=1430
    py = 1550 - round(fb[3] * fh / fig.height)
    px = CX - (round(fb[0] * fw / fig.width) + round((fb[2] - fb[0]) * fw / fig.width) // 2)
    im = scene.copy()
    im.alpha_composite(fs, (px, py))
    bx = (px + round(fb[0] * fw / fig.width), py + round(fb[1] * fh / fig.height),
          px + round(fb[2] * fw / fig.width), py + round(fb[3] * fh / fig.height))
    return im, bx, fh

def pullback(im, bx, margin=40):
    """16:9 scene window containing figure + margin, resized to 1920x1080."""
    h = (bx[3] - bx[1]) + 2 * margin
    w = round(h * 16 / 9)
    cx = (bx[0] + bx[2]) // 2
    cy = (bx[1] + bx[3]) // 2
    x0 = cx - w // 2
    y0 = cy - h // 2
    win = im.crop((x0, y0, x0 + w, y0 + h))
    out = win.resize((1920, 1080), Image.LANCZOS)
    f = 1920 / w
    fb2 = (round((bx[0] - x0) * f), round((bx[1] - y0) * f),
           round((bx[2] - x0) * f), round((bx[3] - y0) * f))
    return out, (x0, y0, x0 + w, y0 + h), f, fb2

results = {}
for name, mult, fname in [
    ("2.5x_lock", 1.0, "landscape-locked-2p5x-1920x1080-20261031.png"),
    ("3.0x_candidate", 1.2, "landscape-up0p5-3p0x-1920x1080-20261031.png"),
]:
    scene_im, bx, fh = place_figure(mult)
    out, win, f, fb2 = pullback(scene_im, bx)
    out.convert("RGB").save(os.path.join(OUT, fname))
    chair_scene_h = 818
    chair_final_h = chair_scene_h * f
    fig_final_h = fb2[3] - fb2[1]
    results[name] = {
        "file": fname,
        "scale_label": "2.5x lock" if mult == 1.0 else "3.0x candidate (2.5+0.5, NOT confirmed as lock)",
        "scene_figure_bbox": list(bx),
        "scene_figure_height": bx[3] - bx[1],
        "scene_figure_width": bx[2] - bx[0],
        "scene_feet_y": bx[3],
        "scene_head_y": bx[1],
        "pullback_window_scene": list(win),
        "pullback_factor": round(f, 4),
        "final_figure_bbox": list(fb2),
        "final_figure_height": fig_final_h,
        "final_figure_width": fb2[2] - fb2[0],
        "final_feet_y": fb2[3],
        "final_head_y": fb2[1],
        "final_head_margin": fb2[1],
        "final_feet_margin": 1080 - fb2[3],
        "chair_height_final": round(chair_final_h, 1),
        "figure_to_chair_ratio": round(fig_final_h / chair_final_h, 3),
        "whole": fb2[1] >= 0 and fb2[3] <= 1080,
    }
    print(name, results[name])

# Reverted landscape, for the gate test and the contact
old = Image.open(OLDLAND).convert("RGB")
# Master centre-crop cut proof (1920x1080 window y420..1500 of the master)
master = Image.open(os.path.join(ROOT, "dual-orientation-room-scale-fix-20261031/master-room-scale-1920x1920-20261031.png")).convert("RGB")
cut = master.crop((0, 420, 1920, 1500))

# Before/after contact: reverted | 2.5x | 3.0x, each 640 wide, labelled
def scaled(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
v25 = Image.open(os.path.join(OUT, "landscape-locked-2p5x-1920x1080-20261031.png"))
v30 = Image.open(os.path.join(OUT, "landscape-up0p5-3p0x-1920x1080-20261031.png"))
sheet = Image.new("RGB", (1920, 360 + 40), (40, 40, 40))
sheet.paste(scaled(old, 640), (0, 0))
sheet.paste(scaled(v25, 640), (640, 0))
sheet.paste(scaled(v30, 640), (1280, 0))
d = ImageDraw.Draw(sheet)
d.text((10, 365), "LEFT: REVERTED landscape 655px, ratio 1.193 — REJECTED", fill=(255, 80, 80))
d.text((650, 365), "MIDDLE: NEW 2.5x lock, pull-back, figure 1010px, ratio 1.423", fill=(80, 255, 120))
d.text((1290, 365), "RIGHT: NEW 3.0x candidate, pull-back, figure 1022px, ratio 1.710", fill=(255, 220, 80))
sheet.save(os.path.join(OUT, "before-after-contact-20261031.png"))
cut.save(os.path.join(OUT, "master-centre-crop-CUT-20261031.png"))

meta = {
    "room_background": "STAND-IN batch-KKGuh, NOT canonical",
    "lock": "2.5x standing, rig 950px, feet on floor, seated 2.3x; 3.0x is a CANDIDATE (2.5+0.5), not confirmed as lock",
    "revert_measured": {
        "reverted_landscape_figure_bbox": [754, 269, 1167, 924],
        "reverted_landscape_figure_height": 655,
        "master_figure_height": 1165,
        "absolute_shrink_px": 510,
        "absolute_shrink_pct": -43.8,
        "figure_scale_vs_source_master": 0.562,
        "room_scale_landscape_vs_master": 0.671,
        "figure_to_room_ratio_change": -16.2,
        "chair_height_landscape_est": 549,
        "figure_to_chair_ratio_reverted": 1.193,
        "figure_to_chair_ratio_master": 1.424,
        "cause": "Fresh 1080-height composition: figure set to 60.7% of 1080 (655px) while room was cover-scaled 1.644 vs master 2.449. Figure and room were NOT scaled together in scene terms; the % -of-frame argument hid a scene-scale revert.",
        "verdict": "REJECTED, approval 0/1, do not reuse as a delivery",
    },
    "whole_figure_fit": {
        "2.5x_scene_height": 1165,
        "2.5x_excess_over_1080": 85,
        "3.0x_scene_height": 1398,
        "3.0x_excess_over_1080": 318,
        "master_centre_crop_cut": "head 35px (385->420), feet 50px (1550->1500)",
    },
    "chair_back_at_waist": {
        "chair_back_top_scene": 700,
        "waist_master": 1002,
        "diff_px": 302,
        "forcing_height_px": 1809,
        "forcing_head_y": -161,
        "check": "WARNING - contradiction in this KKGuh arms-up crop, never faked as PASS",
    },
    "versions": results,
}
json.dump(meta, open(os.path.join(OUT, "measurements-20261031.json"), "w"), indent=2)
print(json.dumps(meta, indent=2))
