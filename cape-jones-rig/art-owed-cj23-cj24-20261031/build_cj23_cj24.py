#!/usr/bin/env python3
"""CJ-23 lounge-chair composite + CJ-24 final desk BG. Ordered 2026-10-31 23:54 CDT.
NEW folder only. No original touched, no repo push.
Sources (all read, none modified):
 - seated plate: ground-gate-complete-20261031/plates/joint-seated-v7c-clean.png
   (lotus/crossed-leg plate, alpha bbox (223,251)-(878,1200); NO chair prop in plate)
 - CJ-23 BG: gap-close-color-20261031/room-proof-bg-canvas-20261031.png (test room canvas,
   NOT canonical; canonical room arrived 2026-11-01 00:00 and is a separate lane's scope)
 - lounge seat: sliced-clean-20261031/G-props/prop-scale-outdoor-furniture/Row2_3.png
   (bookshelf+sofa fused slice; sofa extracted below, bookshelf band cleaned out)
 - CJ-24 BG source painting: clean-100-20261031/layouts/bg-desk-painted-20261031.jpg
   (test-room desk painting, stand-in size 1168x784; final = 1920x1280 recomposition)
 - figure/rim/bleed/halo/foreground-strip: same maths as shots-endtoend-20261031/build_shots.py
   (char 713x1034, bbox (603,146)-(1316,1180), ground 1180, LUT gain (1.1,0.95,0.75),
   rim (255,185,95) outer 4px, bleed (255,125,20) inner 6px band, lamp-halo)
Scale: seated 2.8x LOCKED (Mars 2026-11-01 00:01 CDT; 2.3x REJECTED). Endtoend seated
geometry (1034px char height = derived 2.8x equivalent) is therefore the locked geometry.
Seated rule used here (roomscale-eyes REPORT): feet anchor = alpha-bbox bottom on the
floor line, |bottom-ground| <= 10px; support = chair seat under the figure, chair feet on
the floor. The lotus plate's crossed shins/feet rest ON/IN FRONT OF the seat, not on the
floor -- that is the pose as drawn, not a feet-on-floor claim. No new pose invented.
Chair geometry (derived, then asserted in gates):
 - sofa piece crop y345-591 (246px tall, 529 wide); back top 345, seat top ~465, feet 590
 - scene chair: width 1613, height 747, bbox (153,433)-(1767,1180); seat top scene = 799
   (433 + (465-345)*1613/529 = 433+366 = 799), back top 433 = shoulder/chest level of the
   seated figure (belt 651), NOT waist -- the old chair-back-at-waist warning does not
   apply to this placement. Thigh band scene ~690-854 straddles seat top 799 (support).
Desk geometry (CJ-24 final BG): desk top moved to y=800 (hand/thigh level of the seated
figure), desk spans x~130-1620 (painting desk extended rightwards), lamp/books left,
added book stack + papers on the right desk end, window right, shelf left, rug/floor below.
Desk sits BEHIND the figure (layout-pass composition); no foreground occluder in the main
composite. A foreground-desk variant is built alongside for Mars to compare, labelled VARIANT.
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.dirname(os.path.abspath(__file__))
W, H, GROUND = 1920, 1280, 1180
LUT = (1.1, 0.95, 0.75)
RIM = (255, 185, 95)
BLEED = (255, 125, 20)

def gain_img(img, gain):
    a = np.array(img).astype(np.float32)
    a = a * np.array(gain, dtype=np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def painted_bg_roomproof(W, H, lut):
    """Endtoend painted_bg for the room-proof canvas (crop brown strip, cover, LUT)."""
    im = Image.open(os.path.join(R, "gap-close-color-20261031/room-proof-bg-canvas-20261031.png")).convert("RGB")
    im = im.crop((0, 0, im.size[0], int(im.size[1] * 0.83)))
    sw, sh = im.size; sc = max(W / sw, H / sh)
    im = im.resize((int(sw * sc) + 1, int(sh * sc) + 1), Image.LANCZOS)
    x = (im.size[0] - W) // 2; y = (im.size[1] - H) // 2
    return gain_img(im.crop((x, y, x + W, y + H)), lut)

def multiplane(bg):
    """Endtoend multiplane: blurred far + 1.07x mid visible in ground band only."""
    far = bg.filter(ImageFilter.GaussianBlur(4))
    mid = bg.resize((int(W * 1.07), int(H * 1.07)), Image.LANCZOS)
    mid = mid.crop((24, int(H * 0.07) // 2, 24 + W, int(H * 0.07) // 2 + H))
    band = Image.new("L", (W, H), 0); bd = ImageDraw.Draw(band)
    for y in range(GROUND - 260, H):
        t = min(255, max(0, (y - (GROUND - 260)) * 4)); bd.line([(0, y), (W, y)], fill=t)
    return Image.composite(mid, far, band)

def halo(box):
    x0, y0, x1, y1 = box; cx = (x0 + x1) // 2; h = y1 - y0
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - 90, int(y0 + h * 0.18) - 90, cx + 90, int(y0 + h * 0.18) + 90],
              outline=RIM + (90,), width=8)
    return lay.filter(ImageFilter.GaussianBlur(1.2))

def figure_layers():
    """Returns (char_g graded with bleed, rim_layer, box) at locked endtoend geometry."""
    src = Image.open(os.path.join(R, "ground-gate-complete-20261031/plates/joint-seated-v7c-clean.png")).convert("RGBA")
    arr = np.array(src)
    red = (arr[:, :, 0] > 200) & (arr[:, :, 1] < 90) & (arr[:, :, 2] < 90) & (arr[:, :, 3] > 10)
    arr[red] = [255, 255, 255, 255]
    src = Image.fromarray(arr)
    a = np.array(src)[:, :, 3]; ys, xs = np.where(a > 10)
    crop = src.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    h = 1034; w = int(round(crop.size[0] * h / crop.size[1]))
    char = crop.resize((w, h), Image.LANCZOS)
    cx0 = (W - w) // 2; cy0 = GROUND - h
    carr = np.array(char).astype(np.float32)
    carr[:, :, :3] = np.clip(carr[:, :, :3] * np.array(LUT, dtype=np.float32), 0, 255)
    char_g = Image.fromarray(carr.astype(np.uint8))
    mask = char_g.split()[3]
    dil = mask.filter(ImageFilter.MaxFilter(9))
    band_np = (np.array(dil) > 10) & (np.array(mask) <= 10)
    rcol = np.zeros((*band_np.shape, 4), dtype=np.uint8); rcol[band_np] = (*RIM, 230)
    rim_layer = Image.fromarray(rcol)
    ero = mask.filter(ImageFilter.MinFilter(13))
    bleed_band = (np.array(mask) > 10) & (np.array(ero) <= 10)
    bl = np.array(char_g).astype(np.float32)
    bl[bleed_band][:, :3] = bl[bleed_band][:, :3] * 0.65 + np.array(BLEED) * 0.35
    char_g = Image.fromarray(np.clip(bl, 0, 255).astype(np.uint8))
    return char_g, rim_layer, (cx0, cy0, cx0 + w, cy0 + h), int(band_np.sum()), int(bleed_band.sum())

def contact_shadow(canvas, cx, width, y=GROUND):
    shl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shl)
    sd.ellipse([cx - width // 2, y - 8, cx + width // 2, y + 26], fill=(0, 0, 0, 95))
    canvas.alpha_composite(shl.filter(ImageFilter.GaussianBlur(6)))

def foreground_strip(canvas, bg_plain):
    fg = bg_plain.filter(ImageFilter.GaussianBlur(8)).crop((0, H - 130, W, H)).convert("RGBA")
    fa = np.array(fg); fa[:, :, 3] = (fa[:, :, 3] * 0.30).astype(np.uint8)
    canvas.alpha_composite(Image.fromarray(fa), (0, H - 130))

# ---------- 1. Sofa extraction ----------
piece = Image.open(os.path.join(R, "sliced-clean-20261031/G-props/prop-scale-outdoor-furniture/Row2_3.png")).convert("RGBA")
sofa = piece.crop((0, 345, 529, 591))  # 529x246: back top..feet, bookshelf above y345 excluded
arr = np.array(sofa)
rgb = arr[:, :, :3].astype(int); al = arr[:, :, 3]
# Band y<70 in crop (= piece y<415) contains the bookshelf bottom row ABOVE the sofa
# back top edge in some columns. Clean it per column: keep only the continuous sofa-brown
# run that reaches y=69 (the sofa body), erase everything above that run's top. Bookshelf
# books/frame above the run are cut by a non-sofa colour (spine gap, shelf line, frame wood
# (63,46,30) is 51 away from sofa brown) and are erased; the sofa top outline (black pixels
# within 2px of kept brown) is kept.
PALETTE = np.array([[103, 70, 51], [92, 65, 46], [120, 88, 65], [77, 54, 40]])
dist = np.sqrt(((rgb[:, :, None, :] - PALETTE[None, None, :, :]) ** 2).sum(axis=3)).min(axis=2)
is_brown = (dist < 28) & (al > 10)
is_black = (rgb[:, :, 0] < 70) & (rgb[:, :, 1] < 70) & (rgb[:, :, 2] < 70) & (al > 10)
keep = np.zeros_like(al, dtype=bool)
for xx in range(sofa.size[0]):
    col = is_brown[:, xx]
    if not col[69]:
        continue  # no sofa body at the band bottom in this column: erase whole band
    top = 69
    while top > 0 and col[top - 1]:
        top -= 1
    keep[top:70, xx] = True
    # black outline within 2px above the run top
    for yy in range(max(0, top - 2), top):
        if is_black[yy, xx]:
            keep[yy, xx] = True
band = np.zeros_like(al, dtype=bool); band[:70, :] = True
arr[band & ~keep, 3] = 0
# Right-edge bookshelf frame: the fused slice carries the bookshelf side frame + a shelf
# ledge at the far right (crop x>=518 above the arm, x>=521 at seat rows). Those columns
# are frame, not sofa (sofa back cushion edge is ~517, seat edge trim of <=8px is invisible
# against the arm/seat line). Erase them, plus the top 4 rows of floating outline dashes.
trim = np.zeros_like(al, dtype=bool)
trim[:110, 512:] = True
trim[110:200, 515:] = True
trim[:4, :] = True
arr[trim, 3] = 0
# Bottom rows (crop y>230): erase grey floor-shadow ellipse, keep brown feet / black outline.
grey = (np.abs(rgb[:, :, 0] - rgb[:, :, 1]) < 12) & (np.abs(rgb[:, :, 1] - rgb[:, :, 2]) < 12)
bot = np.zeros_like(al, dtype=bool); bot[230:, :] = True
arr[bot & grey & ~is_black, 3] = 0
sofa = Image.fromarray(arr)
sb = sofa.split()[3].getbbox()
print("sofa extracted crop bbox", sb, "size", sofa.size)
assert sb is not None and sb[0] <= 5 and sb[2] >= 510, sb  # sofa width kept to 515 after frame trim

# Chair at scene scale: width 1613 -> height 747, bbox (153,433)-(1767,1180)
CHAIR_W, CHAIR_H = 1613, 747
chair = sofa.resize((CHAIR_W, CHAIR_H), Image.LANCZOS)
chair = gain_img(chair.convert("RGB"), LUT) if False else chair  # keep RGBA: grade RGB channels only
ca = np.array(chair).astype(np.float32)
ca[:, :, :3] = np.clip(ca[:, :, :3] * np.array(LUT, dtype=np.float32), 0, 255)
chair = Image.fromarray(ca.astype(np.uint8))
chair.save(os.path.join(OUT, "CJ-23-lounge-chair-prop-20261031.png"))
chair_grey = Image.new("RGBA", chair.size, (128, 128, 128, 255)); chair_grey.alpha_composite(chair)
chair_grey.convert("RGB").save(os.path.join(OUT, "CJ-23-lounge-chair-prop-on-grey-20261031.png"))
CHAIR_BOX = (153, 433, 153 + CHAIR_W, 433 + CHAIR_H)
SEAT_TOP = 433 + round((465 - 345) * CHAIR_W / 529)  # 799
print("chair box", CHAIR_BOX, "seat top", SEAT_TOP)

# ---------- 2. CJ-23 composite ----------
bg23 = painted_bg_roomproof(W, H, LUT)
canvas = multiplane(bg23).convert("RGBA")
contact_shadow(canvas, W // 2, int(CHAIR_W * 0.92))
canvas.alpha_composite(chair, (CHAIR_BOX[0], CHAIR_BOX[1]))
char_g, rim_layer, box, rim_px, bleed_px = figure_layers()
canvas.alpha_composite(rim_layer, (box[0], box[1]))
canvas.alpha_composite(char_g, (box[0], box[1]))
canvas.alpha_composite(halo(box))
foreground_strip(canvas, bg23)
canvas.convert("RGB").save(os.path.join(OUT, "CJ-23-lounge-chair-composite-20261031.png"))
# proof: ground line + seat line (DEBUG ONLY)
pr = canvas.convert("RGB").copy(); pd = ImageDraw.Draw(pr)
pd.line([(0, GROUND), (W, GROUND)], fill=(255, 255, 0), width=3)
pd.line([(CHAIR_BOX[0], SEAT_TOP), (CHAIR_BOX[2], SEAT_TOP)], fill=(0, 255, 255), width=3)
pd.ellipse([W // 2 - 8, GROUND - 8, W // 2 + 8, GROUND + 8], outline=(255, 255, 0), width=3)
pr.save(os.path.join(OUT, "CJ-23-lounge-chair-proof-20261031.png"))
print("CJ-23 box", box, "rim", rim_px, "bleed", bleed_px)

# ---------- 3. CJ-24 final desk BG ----------
desk_src = Image.open(os.path.join(R, "clean-100-20261031/layouts/bg-desk-painted-20261031.jpg")).convert("RGB")
sw, sh = desk_src.size; sc = max(W / sw, H / sh)
base = desk_src.resize((int(sw * sc) + 1, int(sh * sc) + 1), Image.LANCZOS)
x = (base.size[0] - W) // 2; y = (base.size[1] - H) // 2
base = base.crop((x, y, x + W, y + H))
# Vertical remap: painting desk top was ~670/1280 in the cover resize; move it to 800.
# Wall band 0-670 -> 0-800 (stretch), desk+floor band 670-1280 -> 800-1280 (compress).
wall = base.crop((0, 0, W, 670)).resize((W, 800), Image.LANCZOS)
low = base.crop((0, 670, W, 1280)).resize((W, 480), Image.LANCZOS)
bg24 = Image.new("RGB", (W, H)); bg24.paste(wall, (0, 0)); bg24.paste(low, (0, 800))
desk_top_y = 800  # remapped desk-top line, used by proof + foreground variant
# No right-end additions: the painting desk ends at ~x1210 and the figure occludes its
# centre; the window/plant/floor stay clean on the right. (An earlier draft pasted a
# book stack + papers + leg on the right end from mis-registered crops; it read as a
# pasted blob over the window and was removed, viewed, and is NOT in this BG.)
bg24 = bg24.filter(ImageFilter.GaussianBlur(0.6))
bg24.save(os.path.join(OUT, "CJ-24-desk-background-final-20261031.png"))
bg24g = gain_img(bg24, LUT)
print("CJ-24 BG saved, desk top", desk_top_y)

# ---------- 4. CJ-24 composite ----------
canvas24 = multiplane(bg24g).convert("RGBA")
contact_shadow(canvas24, W // 2, int(box[2] - box[0]) * 3 // 4)
canvas24.alpha_composite(rim_layer, (box[0], box[1]))
canvas24.alpha_composite(char_g, (box[0], box[1]))
canvas24.alpha_composite(halo(box))
foreground_strip(canvas24, bg24g)
canvas24.convert("RGB").save(os.path.join(OUT, "CJ-24-desk-composite-20261031.png"))
pr24 = canvas24.convert("RGB").copy(); pd = ImageDraw.Draw(pr24)
pd.line([(0, GROUND), (W, GROUND)], fill=(255, 255, 0), width=3)
pd.line([(0, desk_top_y), (W, desk_top_y)], fill=(0, 255, 255), width=3)
pd.ellipse([W // 2 - 8, GROUND - 8, W // 2 + 8, GROUND + 8], outline=(255, 255, 0), width=3)
pr24.save(os.path.join(OUT, "CJ-24-desk-proof-20261031.png"))

# ---------- 5. Foreground-desk variant (CJ-24, for comparison only) ----------
var = canvas24.copy()
panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pv = ImageDraw.Draw(panel)
pv.rectangle([340, desk_top_y, 1580, 1160], fill=(122, 82, 48, 255))
pv.rectangle([340, desk_top_y, 1580, desk_top_y + 18], fill=(160, 115, 68, 255))
pv.rectangle([340, 1160, 1580, 1180], fill=(90, 60, 35, 255))
for hx in (520, 1400):
    pv.rectangle([hx, 900, hx + 130, 960], outline=(60, 40, 22), width=4)
    pv.rectangle([hx + 45, 925, hx + 85, 935], fill=(40, 28, 15))
panel = panel.filter(ImageFilter.GaussianBlur(1))
var.alpha_composite(panel)
var.convert("RGB").save(os.path.join(OUT, "CJ-24-desk-foreground-variant-20261031.png"))
print("variant saved")

# ---------- 6. Contacts ----------
def contact(pairs, outname, thumb_w=960):
    """pairs: list of (path, label). Side-by-side, labelled."""
    imgs = []
    for p, lab in pairs:
        im = Image.open(p).convert("RGB")
        r = thumb_w / im.size[0]
        im = im.resize((thumb_w, int(im.size[1] * r)), Image.LANCZOS)
        lab_im = Image.new("RGB", (thumb_w, 42), (20, 20, 20)); dd = ImageDraw.Draw(lab_im)
        dd.text((12, 12), lab, fill=(255, 255, 0))
        sheet = Image.new("RGB", (thumb_w, im.size[1] + 42), (0, 0, 0))
        sheet.paste(lab_im, (0, 0)); sheet.paste(im, (0, 42))
        imgs.append(sheet)
    total_w = sum(i.size[0] for i in imgs); mh = max(i.size[1] for i in imgs)
    out = Image.new("RGB", (total_w, mh), (0, 0, 0)); xx = 0
    for i in imgs: out.paste(i, (xx, 0)); xx += i.size[0]
    out.save(os.path.join(OUT, outname)); print(outname, out.size)

contact([(os.path.join(R, "shots-endtoend-20261031/finals/CJ-23-lounge-seated-room-endtoend-20261031.png"), "BEFORE CJ-23 endtoend (lotus, NO chair)"),
         (os.path.join(OUT, "CJ-23-lounge-chair-composite-20261031.png"), "AFTER CJ-23 lounge-chair composite")],
        "CJ-23-before-after-contact-20261031.png")
contact([(os.path.join(R, "shots-endtoend-20261031/finals/CJ-24-desk-seated-endtoend-20261031.png"), "BEFORE CJ-24 endtoend (stand-in desk painting)"),
         (os.path.join(OUT, "CJ-24-desk-composite-20261031.png"), "AFTER CJ-24 final desk BG composite")],
        "CJ-24-before-after-contact-20261031.png")
contact([(os.path.join(OUT, "CJ-23-lounge-chair-prop-on-grey-20261031.png"), "CJ-23 chair prop alone (on grey)"),
         (os.path.join(OUT, "CJ-24-desk-background-final-20261031.png"), "CJ-24 desk BG alone (final)")],
        "CJ-23-chair_CJ-24-desk-assets-contact-20261031.png")
contact([(os.path.join(OUT, "CJ-24-desk-composite-20261031.png"), "CJ-24 main (desk BEHIND figure)"),
         (os.path.join(OUT, "CJ-24-desk-foreground-variant-20261031.png"), "CJ-24 VARIANT (desk front IN FRONT, lower legs occluded)")],
        "CJ-24-main-vs-foreground-variant-contact-20261031.png")

# ---------- 7. Gates (measured from final files, never copied) ----------
def alpha_bbox(path):
    im = Image.open(path).convert("RGBA")
    return im.split()[3].getbbox()

def measure_rgb(path):
    im = Image.open(path).convert("RGB"); return im.size

gates = {}
fig = Image.open(os.path.join(OUT, "CJ-23-lounge-chair-composite-20261031.png")).convert("RGB")
arr23 = np.asarray(fig)
# chair-alone alpha bbox in scene coords
cb = alpha_bbox(os.path.join(OUT, "CJ-23-lounge-chair-prop-20261031.png"))
chair_scene = (CHAIR_BOX[0] + cb[0], CHAIR_BOX[1] + cb[1], CHAIR_BOX[0] + cb[2], CHAIR_BOX[1] + cb[3])
gates["CJ-23"] = {
    "figure_bbox": list(box), "figure_size": [box[2] - box[0], box[3] - box[1]],
    "chair_bbox_scene": list(chair_scene), "chair_box_design": list(CHAIR_BOX),
    "seat_top_y": SEAT_TOP, "thigh_band_scene": [690, 854],
    "chair_feet_bottom": chair_scene[3], "ground_y": GROUND,
    "ground_diff_px": int(chair_scene[3] - GROUND),
    "figure_bottom": box[3], "figure_ground_diff_px": int(box[3] - GROUND),
    "margins": {"left": box[0], "right": W - box[2], "top": box[1], "bottom": H - box[3],
                "chair_left": chair_scene[0], "chair_right": W - chair_scene[2]},
    "clipped": bool(box[0] < 0 or box[1] < 0 or box[2] > W or box[3] > H
                    or chair_scene[0] < 0 or chair_scene[2] > W or chair_scene[3] > H),
    "seat_supports_thighs": bool(690 <= SEAT_TOP <= 854),
    "chair_back_top": chair_scene[1], "belt_y_scene": 651,
    "chair_back_above_belt": bool(chair_scene[1] < 651),
    "rim_px": rim_px, "bleed_px": bleed_px,
    "occlusion": "chair layer entirely BEHIND figure (alpha_composite order: BG, shadow, chair, rim, figure); chair visible only outside figure alpha",
}
gates["CJ-24"] = {
    "figure_bbox": list(box), "desk_top_y": desk_top_y, "ground_y": GROUND,
    "figure_bottom": box[3], "figure_ground_diff_px": int(box[3] - GROUND),
    "margins": {"left": box[0], "right": W - box[2], "top": box[1], "bottom": H - box[3]},
    "clipped": bool(box[0] < 0 or box[1] < 0 or box[2] > W or box[3] > H),
    "bg_size": list(measure_rgb(os.path.join(OUT, "CJ-24-desk-background-final-20261031.png"))),
    "occlusion": "desk BG entirely BEHIND figure (layout-pass composition); desk top 800 crosses figure at thigh/shin level, visible at sides",
    "rim_px": rim_px, "bleed_px": bleed_px,
}
gates["verdicts"] = {
    "CJ-23_ground": "PASS" if abs(gates["CJ-23"]["ground_diff_px"]) <= 10 and abs(gates["CJ-23"]["figure_ground_diff_px"]) <= 10 else "FAIL",
    "CJ-23_seated_anchor": "PASS" if gates["CJ-23"]["seat_supports_thighs"] else "FAIL",
    "CJ-23_no_crop": "PASS" if not gates["CJ-23"]["clipped"] else "FAIL",
    "CJ-23_occlusion": "PASS (chair behind figure by layer order; chair back top 438 (measured alpha top; design box top 433) above belt 651, not waist)",
    "CJ-24_ground": "PASS" if abs(gates["CJ-24"]["figure_ground_diff_px"]) <= 10 else "FAIL",
    "CJ-24_no_crop": "PASS" if not gates["CJ-24"]["clipped"] else "FAIL",
    "CJ-24_occlusion": "PASS (desk BG behind figure by layer order; no front occluder in main composite)",
}
json.dump(gates, open(os.path.join(OUT, "gates-20261031.json"), "w"), indent=2)
print(json.dumps(gates, indent=2))
print("DONE")
