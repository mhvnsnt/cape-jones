#!/usr/bin/env python3
"""Dual-orientation ROOM-SCALE fix, 20261031.
Mars, 2026-10-31 19:42 CDT: dual-orientation proof showed him in the room
floating, way too small. Lock (2026-10-31 15:34 CDT, room ONLY):
2.5x, rig 950px tall, feet ON THE FLOOR, chair back at waist, seated 2.3x.
Background is the STAND-IN batch-KKGuh, NOT canonical. Do not call it canonical.
Do not recolour it toward a guessed canonical.

Measured translation (see ROOM-SCALE-RULE.md for the full table):
- Locked preview file layout-pass-room-scaled-25x-20261031.jpg is 1168x1060.
  Measured there: head (purple cowl) top y=268, feet (white) bottom y=911,
  figure alpha height = 643 preview px. 643/950 = 0.677 preview scale.
  Figure height / preview frame height = 643/1060 = 60.7%.
- Old dual proof: figure alpha height 709 in a 1920 master (36.9% of master),
  head 613, feet 1322, centred. Rug top in master ~1371, so old feet were
  49px ABOVE the rug, 196px above chair feet (~1518), i.e. floating.
- New room-scale master: alpha height = round(0.607*1920) = 1165,
  feet alpha y = 1550 (on the rug, 179px below rug top, 32px below chair
  feet - figure is slightly closer to camera than the chair, so slightly
  lower is correct perspective), head = 1550-1165 = 385.
- Protected square 420-1500 is only 1080 tall. 1165 > 1080 by 85px.
  Centre crops therefore CUT him: landscape centre crop (y420-1500) cuts
  head 35px (420-385) and feet 50px (1550-1500). Portrait centre crop
  (x420-1500, full height) keeps him whole vertically and horizontally.
  This script does NOT silently shrink him to fit. It shows the cut,
  then delivers the recommended method: PULL-BACK / TWO-FRAMING.
  Landscape and square are separate framings of the SAME room at the
  SAME relative scale (figure and room scaled together), not a
  figure-only shrink. Portrait is a centre crop from the master.
- Chair-back check: chair-back top in the KKGuh master is ~700 (visual
  estimate, bg y~286 x 2.449). Waist in the new master is head + 0.53*H
  = 385 + 618 = 1003. Difference = 303px. Forcing waist = chair-back
  with feet on the floor would need H = (1550-700)/0.47 = 1809px,
  head at -161, i.e. head off-frame. So chair-back-at-waist as a pixel
  equality does NOT hold in this KKGuh arms-up crop at any feet-on-floor
  scale. It is reported as a CONTRADICTION, not faked as a pass.
  The hard gate is therefore scale-ratio + feet-on-floor; chair-back
  is a WARNING that needs Mars's clarification for this crop
  (it may refer to the apose layout-pass composition, or to the
  chair armrest, not to this armchair back top in this crop).
  See ROOM-SCALE-RULE.md section 5.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "dual-light-variants-20261031/base-arms-up-transparent-20261031.png")
BG = os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets/backgrounds/batch-KKGuh.jpg")
OLD = os.path.join(ROOT, "dual-orientation-20261031")

def cover(bg, size):
    im = bg.copy()
    r = max(size[0]/im.width, size[1]/im.height)
    im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x = (im.width-size[0])//2; y = (im.height-size[1])//2
    return im.crop((x, y, x+size[0], y+size[1]))

def check_room_scale(alpha_h, feet_y, master_h=1920, tol_feet=60):
    """Hard gate: scale ratio + feet. Returns (ok, report dict)."""
    ratio = alpha_h / master_h
    target_ratio = 0.607  # locked preview proportion
    scale_ok = abs(ratio - target_ratio) <= 0.03
    # rug plane in master: rug top ~1371, chair feet ~1518; feet must be on rug
    feet_ok = 1371 <= feet_y <= 1700
    waist_y = None
    return scale_ok and feet_ok, {
        "alpha_height": alpha_h, "height_ratio": round(ratio, 4),
        "target_ratio": target_ratio, "scale_ok": scale_ok,
        "feet_y": feet_y, "feet_on_rug": feet_ok,
        "rug_top_master": 1371, "chair_feet_master": 1518,
        "chair_back_top_master_est": 700,
        "waist_y_est": None,  # filled by caller
        "chair_back_waist_diff_px": None,
        "chair_back_check": "WARNING - see report, not a pixel pass in this crop",
    }

fig = Image.open(FIG).convert("RGBA")
fb = fig.split()[3].getbbox()  # (222,239,880,1283)
bg = Image.open(BG).convert("RGB")
master = cover(bg, (1920, 1920)).convert("RGBA")

# --- new room-scale placement ---
H = 1165
FEET = 1550
HEAD = FEET - H
# whole-source resize height fh so alpha height = H: alpha fraction = (1283-239)/1500
fh = round(H / ((fb[3]-fb[1]) / fig.height))
fw = round(fig.width * fh / fig.height)
fig_s = fig.resize((fw, fh), Image.LANCZOS)
# placement: alpha bottom = placement_y + fb[3]*fh/fig.height = FEET
py = FEET - round(fb[3]*fh/fig.height)
# alpha centre x = 960
px = 960 - (round(fb[0]*fw/fig.width) + round((fb[2]-fb[0])*fw/fig.width)//2)
master.alpha_composite(fig_s, (px, py))
fx0 = px + round(fb[0]*fw/fig.width); fy0 = py + round(fb[1]*fh/fig.height)
fx1 = px + round(fb[2]*fw/fig.width); fy1 = py + round(fb[3]*fh/fig.height)
print(f"new master figure bbox {(fx0,fy0,fx1,fy1)} height {fy1-fy0} feet {fy1} head {fy0}")
assert (fx1-fx0, fy1-fy0) != (0,0)
ok, rep = check_room_scale(fy1-fy0, fy1)
waist = fy0 + round(0.53*(fy1-fy0))
rep["waist_y_est"] = waist
rep["chair_back_waist_diff_px"] = waist - 700
rep["hard_gate_scale_and_feet_pass"] = ok
print("GATE", rep)
if not ok:
    print("ROOM-SCALE GATE FAILED - scale or feet out of tolerance", file=sys.stderr)
    sys.exit(2)

master_rgb = master.convert("RGB")
master_rgb.save(f"{OUT}/master-room-scale-1920x1920-20261031.png")

# --- centre-crop consequence (proof only, NOT a delivery) ---
land_centre = master_rgb.crop((0, 420, 1920, 1500))
land_centre.save(f"{OUT}/landscape-centre-crop-CUT-20261031.png")
# annotate cut
ann = land_centre.copy(); d = ImageDraw.Draw(ann)
d.rectangle([0,0,1920,35], fill=(255,0,0))
d.text((20,8), "CUT: head 35px above this crop top (head master 385, crop starts 420)", fill=(255,255,255))
d.rectangle([0,1045,1920,1080], fill=(255,0,0))
d.text((20,1053), "CUT: feet 50px below this crop bottom (feet master 1550, crop ends 1500)", fill=(255,255,255))
ann.save(f"{OUT}/landscape-centre-crop-CUT-annotated-20261031.png")

# --- portrait: centre crop from master, whole ---
port = master_rgb.crop((420, 0, 1500, 1920))
port.save(f"{OUT}/portrait-room-scale-1080x1920-20261031.png")
fig_port = (fx0-420, fy0, fx1-420, fy1)
print("portrait figure", fig_port, "whole", 0 <= fig_port[0] and fig_port[1] >= 0 and fig_port[2] <= 1080 and fig_port[3] <= 1920)

# --- landscape: pull-back / two-framing, same relative scale ---
# Dedicated 1920x1080 landscape composition: BG cover to 1920x1080, figure
# height = 60.7% of 1080 = 655, feet on floor in that framing.
land_bg = cover(bg, (1920, 1080)).convert("RGBA")
LH = 655
# In this cover, bg scale = 1920/1168=1.644, resized 1920x1289, crop y=(1289-1080)//2=104.
# Rug top bg 560*1.644-104=817, chair feet bg 625*1.644-104=924. Feet = 924.
LFEET = 924; LHEAD = LFEET - LH
lfh = round(LH / ((fb[3]-fb[1]) / fig.height))
lfw = round(fig.width * lfh / fig.height)
fig_l = fig.resize((lfw, lfh), Image.LANCZOS)
lpy = LFEET - round(fb[3]*lfh/fig.height)
lpx = 960 - (round(fb[0]*lfw/fig.width) + round((fb[2]-fb[0])*lfw/fig.width)//2)
land_bg.alpha_composite(fig_l, (lpx, lpy))
lfx0 = lpx + round(fb[0]*lfw/fig.width); lfy0 = lpy + round(fb[1]*lfh/fig.height)
lfx1 = lpx + round(fb[2]*lfw/fig.width); lfy1 = lpy + round(fb[3]*lfh/fig.height)
print(f"landscape pull-back figure {(lfx0,lfy0,lfx1,lfy1)} height {lfy1-lfy0} feet {lfy1}")
land_bg.convert("RGB").save(f"{OUT}/landscape-room-scale-1920x1080-20261031.png")

# --- square pull-back: master window 1165 tall, resized to 1080 (not centre crop) ---
# Window: x 960-1035= -75..1935 -> clamp: use full master width window? Square window
# must be 1165x1165 to keep aspect: x 960-582=378..1543, y 385..1550.
sq_win = master_rgb.crop((378, 385, 1543, 1550)).resize((1080, 1080), Image.LANCZOS)
sq_win.save(f"{OUT}/square-pullback-1080x1080-20261031.png")
print("square pull-back window (378,385,1543,1550) -> 1080x1080, figure whole by construction")

# --- blurred pillarbox alternative, from new landscape ---
blur = cover(land_bg.convert("RGB"), (1080, 1920)).filter(ImageFilter.GaussianBlur(25))
fg = land_bg.convert("RGB").resize((1080, 608), Image.LANCZOS)
pf = blur.copy(); pf.paste(fg, (0, (1920-608)//2))
pf.save(f"{OUT}/portrait-blurfill-room-scale-20261031.png")

# --- safe overlays (proof only) ---
def overlay_port(im, figb):
    o = im.copy(); d = ImageDraw.Draw(o, "RGBA")
    d.rectangle([97,288,842,1482], outline=(0,255,0), width=6)
    d.rectangle(figb, outline=(0,200,255), width=4)
    d.line([(0, figb[3]), (1080, figb[3])], fill=(255,0,255), width=3)
    return o
def overlay_land(im, figb):
    o = im.copy(); d = ImageDraw.Draw(o, "RGBA")
    d.rectangle([192,108,1728,972], outline=(0,255,0), width=4)
    d.rectangle([96,54,1824,1026], outline=(255,0,0), width=4)
    d.rectangle(figb, outline=(0,200,255), width=4)
    d.line([(0, figb[3]), (1920, figb[3])], fill=(255,0,255), width=3)
    return o
overlay_port(port, fig_port).save(f"{OUT}/portrait-room-scale-safe-overlay-20261031.png")
overlay_land(land_bg.convert("RGB"), (lfx0,lfy0,lfx1,lfy1)).save(f"{OUT}/landscape-room-scale-safe-overlay-20261031.png")

# --- master diagram with room-scale figure + floor line ---
diag = master_rgb.copy(); d = ImageDraw.Draw(diag, "RGBA")
d.rectangle([0,420,1920,1500], outline=(0,200,255), width=8)
d.rectangle([420,0,1500,1920], outline=(255,200,0), width=8)
d.rectangle([420,420,1500,1500], outline=(0,255,0), width=8)
d.rectangle((fx0,fy0,fx1,fy1), outline=(255,0,255), width=6)
d.line([(0,1371),(1920,1371)], fill=(255,165,0), width=4)  # rug top
d.line([(0,1550),(1920,1550)], fill=(255,0,255), width=4)  # feet line
diag.save(f"{OUT}/master-room-scale-diagram-20261031.png")

# --- before/after contact: old vs new, landscape + portrait ---
old_land = Image.open(f"{OLD}/landscape-1920x1080-clean-20261031.png")
old_port = Image.open(f"{OLD}/portrait-1080x1920-clean-20261031.png")
def scaled(im, w): return im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
from PIL import ImageDraw as _D
sheet = Image.new("RGB", (1920, 1080+1080+40), (128,128,128))
# top row: old landscape (960) + new landscape (960) side by side, scaled to 960 wide each
top = Image.new("RGB", (1920, 540), (128,128,128))
top.paste(scaled(old_land, 960), (0,0)); top.paste(scaled(land_bg.convert("RGB"), 960), (960,0))
sheet.paste(top, (0,0))
# bottom: old portrait + new portrait, scaled to 480 wide each, centred
bot = Image.new("RGB", (1920, 540), (128,128,128))
bot.paste(scaled(old_port, 270), (480,0)); bot.paste(scaled(port, 270), (960,0))
# labels
dd = _D.Draw(sheet)
dd.text((10,545), "TOP: OLD landscape (floating, 709px) left | NEW landscape pull-back (room scale, 655px in 1080 frame = same relative scale) right", fill=(255,255,0))
dd.text((10,1090), "BOTTOM: OLD portrait left | NEW portrait centre-crop from room-scale master right - see full contact for labels", fill=(255,255,0))
sheet.save(f"{OUT}/before-after-contact-20261031.png")

meta = {
  "room_background": "STAND-IN batch-KKGuh, NOT canonical",
  "lock": "2.5x standing, rig 950px, feet on floor, seated 2.3x",
  "locked_preview_measured": {"file": "showcase/layout-pass-room-scaled-25x-20261031.jpg", "size": [1168,1060], "head_top_y": 268, "feet_bottom_y": 911, "figure_height_preview_px": 643, "preview_scale_vs_950": 0.677, "height_ratio": 0.607},
  "old_dual": {"figure_height_master": 709, "head_master": 613, "feet_master": 1322, "feet_vs_rug_top_1371": -49, "feet_vs_chair_feet_1518": -196, "verdict": "FLOATING, too small"},
  "new_master": {"figure_bbox": [fx0,fy0,fx1,fy1], "height": fy1-fy0, "head": fy0, "feet": fy1, "waist_est": waist, "chair_back_top_est": 700, "waist_minus_chair_back": waist-700, "chair_back_check": "WARNING - contradiction, see report"},
  "protected_square": [420,420,1500,1500],
  "centre_crop_consequence": {"landscape_head_cut_px": 35, "landscape_feet_cut_px": 50, "portrait_whole": True, "square_centre_crop_whole": False},
  "recommended": "PULL-BACK / TWO-FRAMING: portrait = centre crop from room-scale master (whole); landscape = dedicated 1920x1080 framing at same relative scale (figure 655px in 1080 frame, feet 924); square = pull-back resize of 1165x1165 master window (not centre crop)",
  "new_landscape": {"figure_bbox": [lfx0,lfy0,lfx1,lfy1], "height": lfy1-lfy0, "feet": lfy1},
  "new_portrait": {"figure_bbox": list(fig_port), "whole": True},
  "gate": rep,
}
json.dump(meta, open(f"{OUT}/measurements-20261031.json","w"), indent=2)
print(json.dumps(meta, indent=2))
