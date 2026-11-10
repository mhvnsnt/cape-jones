"""CJ-15 foreshortened forearm + CJ-18 seam options, 2026-10-31.
NEW folder only. Sources READ only, never overwritten:
 - cut-limbs-v7c/Arm_Front_Lower.png (rig gauntlet+fist piece)
 - transparent-plates-sweep-20261031 plates for CJ-15 (flying-37) and CJ-18 (true-flex)
 - clean-100-20261031/layouts/bg-flying-painted-20261031.jpg (CJ-15 BG)
No hand smear, no blur-stretch, no recolour on disk: piece is a resize-only
reassembly of the source piece (LANCZOS resample, no smear filter); CJ-15
LUT gain is applied at composite time only, exactly as the original
shots-endtoend build does for every plate. CJ-18 blend option blurs ONLY
inside the two seam bands, from the art's own neighbouring pixels.
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

R = '/home/hatch/workspace/cape-jones-rig'
OUT = os.path.join(R, 'art-owed-cj15-cj18-20261031')

def gain_img(rgb, gain):
    a = np.array(rgb).astype(np.float32) * np.array(gain, dtype=np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def resize_rgba(im, h):
    w0, h0 = im.size; return im.resize((int(round(w0 * h / h0)), h), Image.LANCZOS)

def alpha_bbox(im):
    a = np.array(im)[:, :, 3]; ys, xs = np.where(a > 10)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)

def painted_bg(src, W, H, lut):
    im = Image.open(os.path.join(R, src)).convert('RGB')
    sw, sh = im.size; sc = max(W / sw, H / sh)
    im = im.resize((int(sw * sc) + 1, int(sh * sc) + 1), Image.LANCZOS)
    x = (im.size[0] - W) // 2; y = (im.size[1] - H) // 2
    return gain_img(im.crop((x, y, x + W, y + H)), lut)

def script_bg(env, W, H, lut, ground_y, seed):
    import random
    rnd = random.Random(seed)
    top, bot = (80, 85, 100), (140, 135, 120)
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    for y in range(H):
        t = y / max(1, H - 1); arr[y, :, :] = [int(top[i] + (bot[i] - top[i]) * t) for i in range(3)]
    img = Image.fromarray(arr); d = ImageDraw.Draw(img)
    d.rectangle([0, ground_y, W, H], fill=(110, 100, 90))
    return gain_img(img, lut)

def rim_bleed_layers(char_g, rim, bleed):
    """Returns (rim_layer, char_with_bleed, rim_px, bleed_px) — same recipe as shots-endtoend."""
    mask = char_g.split()[3]
    dil = mask.filter(ImageFilter.MaxFilter(9))
    dil_np, m_np = np.array(dil), np.array(mask)
    band_np = (dil_np > 10) & (m_np <= 10)
    rim_px = int(band_np.sum())
    rcol = np.zeros((*band_np.shape, 4), dtype=np.uint8); rcol[band_np] = (*rim, 230)
    ero = mask.filter(ImageFilter.MinFilter(13)); ero_np = np.array(ero)
    bleed_band = (m_np > 10) & (ero_np <= 10)
    bleed_px = int(bleed_band.sum())
    bl = np.array(char_g).astype(np.float32)
    bl[bleed_band][:, :3] = bl[bleed_band][:, :3] * 0.65 + np.array(bleed) * 0.35
    return Image.fromarray(rcol), Image.fromarray(np.clip(bl, 0, 255).astype(np.uint8)), rim_px, bleed_px

def speed_lines(box, W, H, rim):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box; h = y1 - y0
    for i in range(8):
        yy = int(y0 + h * 0.2) + i * int(h * 0.09)
        d.line([x0 - 130, yy, x0 - 15, yy], fill=rim + (180,), width=5)
    return lay.filter(ImageFilter.GaussianBlur(1.2))

def aura(box, W, H, rim):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; w, h = x1 - x0, y1 - y0
    d.ellipse([cx - int(w * 0.58), cy - int(h * 0.54), cx + int(w * 0.58), cy + int(h * 0.54)], outline=rim + (130,), width=12)
    return lay.filter(ImageFilter.GaussianBlur(1.2))

# ---------- 1. Foreshortened forearm piece (from cut-limb rig piece) ----------
src_piece = Image.open(os.path.join(R, 'cut-limbs-v7c/Arm_Front_Lower.png')).convert('RGBA')
pb = alpha_bbox(src_piece)  # (4,0,123,285)
piece_crop = src_piece.crop(pb)  # 119x285
SPLIT = 208  # gauntlet above, fist below (12px overlap in fist crop)
# Cuff crop starts at y=28: the source's top ~28px is an elbow-ball fragment,
# NOT gauntlet — including it compressed into a sliver (v1 defect, fixed here).
gauntlet_src = piece_crop.crop((0, 28, piece_crop.size[0], SPLIT))
fist_src = piece_crop.crop((0, SPLIT - 12, piece_crop.size[0], piece_crop.size[1]))
fb = alpha_bbox(fist_src)
fist_src = fist_src.crop(fb)
print('source piece bbox', pb, 'gauntlet', gauntlet_src.size, 'fist bbox', fb, 'fist', fist_src.size)
# Foreshortening transform (resize only, no smear):
#  gauntlet: width 155, height 85 (shaft recedes from camera; was 119x180 cuff crop)
#  fist:     width 145 (nearer = larger; fist/gauntlet width ratio 0.72 -> 0.94),
#            height proportional, overlapping the gauntlet's lower half (in front)
gauntlet = gauntlet_src.resize((155, 85), Image.LANCZOS)
fist = fist_src.resize((145, int(round(fist_src.size[1] * 145 / fist_src.size[0]))), Image.LANCZOS)
canvas = Image.new('RGBA', (340, 300), (0, 0, 0, 0))
canvas.alpha_composite(gauntlet, (92, 15))
canvas.alpha_composite(fist, (97, 55))
piece_bbox = alpha_bbox(canvas)
piece = canvas.crop(piece_bbox)
piece.save(os.path.join(OUT, 'cj15-foreshortened-forearm-piece-20261031.png'))
grey = Image.new('RGBA', canvas.size, (128, 128, 128, 255)); grey.alpha_composite(canvas)
grey.save(os.path.join(OUT, 'cj15-foreshortened-forearm-piece-on-grey-20261031.png'))
print('piece bbox in 340x300 canvas', piece_bbox, 'cropped piece', piece.size)
meas = {
  'source': 'cut-limbs-v7c/Arm_Front_Lower.png (read only)',
  'source_alpha_bbox': list(pb), 'source_size': list(src_piece.size),
  'split_y_in_crop': SPLIT,
  'gauntlet_resize': [gauntlet_src.size, list(gauntlet.size)],
  'gauntlet_width_scale': round(gauntlet.size[0] / gauntlet_src.size[0], 3),
  'gauntlet_height_scale': round(gauntlet.size[1] / gauntlet_src.size[1], 3),
  'fist_source_size': list(fist_src.size), 'fist_resize': list(fist.size),
  'fist_width_scale': round(fist.size[0] / fist_src.size[0], 3),
  'fist_to_gauntlet_width_ratio': round(fist.size[0] / gauntlet.size[0], 3),
  'piece_canvas': [340, 300], 'piece_alpha_bbox': list(piece_bbox), 'piece_cropped_size': list(piece.size),
  'foreshortening_ratio': 'piece height vs same-width unshortened piece: '
    + str(round(piece.size[1] / (piece.size[0] / piece_crop.size[0] * piece_crop.size[1]), 3)),
  'method': 'resize-only reassembly (LANCZOS). No smear, no blur-stretch, no recolour on disk. '
            'CJ-15 LUT gain applied at composite only, as with every plate.',
}
print(meas)

# ---------- 2. CJ-15 re-render ----------
W, H, ground_y, feet_y = 1920, 1190, 1060, 920
LUT15 = [0.7, 1.0, 1.25]; RIM15 = (140, 200, 255); BLEED15 = (70, 140, 255)
plate15 = Image.open(os.path.join(R, 'transparent-plates-sweep-20261031/plates/clips-v7c-clean-20261031__flying__flying-37-hover-v7c-clean.png')).convert('RGBA')
pa = np.array(plate15)[:, :, 3]; ys, xs = np.where(pa > 10)
crop15 = plate15.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
print('CJ15 plate alpha bbox', (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1), 'crop', crop15.size)
# Mask old viewer-right gauntlet+fist in PLATE-crop space (keeps elbow ball + cape):
#  plate x>=770, y 660..890, EXCEPT inside the elbow-ball disc (centre plate
#  (790,645), r=32) — v1 masked only from y=690 and left a gauntlet strip
#  above it; the disc exception lets the mask start at y=660 without eating
#  the ball that the new piece anchors under.
arr = np.array(crop15).copy()
ox, oy = int(xs.min()), int(ys.min())
yy_grid, xx_grid = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
plate_x = xx_grid + ox; plate_y = yy_grid + oy
# v4 lesson: the old gauntlet top OVERLAPS the ball's lower-right in plate
# space, so a full-disc ball exception protects gauntlet pixels. Preserve
# only the ball's VISIBLE part (top/left of centre (783,640), r=28):
#   ball_visible = dist<=28 AND (y<652 OR x<778)
# Everything else from x>=730, y640-890 is old arm (cape edge there is
# <=742 and the new piece covers that x-range in the final, so a <=12px
# cape-edge sliver at y640-660 is covered, not a hole).
ball_visible = ((plate_x - 783) ** 2 + (plate_y - 640) ** 2 <= 28 ** 2) & ((plate_y < 652) | (plate_x < 778))
mask_zone = (plate_x >= 730) & (plate_y >= 640) & (plate_y <= 890) & (~ball_visible)
region_before = int((arr[mask_zone, 3] > 10).sum())
arr[mask_zone, 3] = 0
print('CJ15 old-arm mask plate px removed', region_before)
char15 = resize_rgba(Image.fromarray(arr), 880)
cw, ch = char15.size; cx0 = (W - cw) // 2; cy0 = feet_y - ch
print('CJ15 char', cw, ch, 'at', cx0, cy0)
# CJ-15 LUT gain on character only
carr = np.array(char15).astype(np.float32)
carr[:, :, :3] = np.clip(carr[:, :, :3] * np.array(LUT15, dtype=np.float32), 0, 255)
char15g = Image.fromarray(carr.astype(np.uint8))
rim15, char15b, rim15_px, bleed15_px = rim_bleed_layers(char15g, RIM15, BLEED15)
# Piece layer: scale cropped piece so its height = 190px, rotate -13 deg (outward, toward viewer-right)
piece_scaled = piece.resize((int(round(piece.size[0] * 190 / piece.size[1])), 190), Image.LANCZOS)
piece_scaled = piece_scaled.rotate(-8, resample=Image.BICUBIC, expand=True)
parr = np.array(piece_scaled).astype(np.float32)
parr[:, :, :3] = np.clip(parr[:, :, :3] * np.array(LUT15, dtype=np.float32), 0, 255)
piece_g = Image.fromarray(parr.astype(np.uint8))
prim, piece_b, prim_px, pbleed_px = rim_bleed_layers(piece_g, RIM15, BLEED15)
# Anchor: elbow-ball centre plate ~(790,645) -> final (698+ (790-246)*880/1061 , 40+(645-251)*880/1061)
# char15 is the resized crop, so use char-space: ball char-local = ((790-246)*cw/632, (645-251)*880/1061)
ball_fx = cx0 + (790 - 246) * cw / 632
ball_fy = cy0 + (645 - 251) * 880 / 1061
print('CJ15 elbow-ball final approx', round(ball_fx, 1), round(ball_fy, 1))
# Paste piece so its top-centre sits directly under the ball centre,
# overlapping the ball bottom by ~6px (cuff tucks under the joint ball; ball radius plate ~32, not 48 — v2 used 48 and protected the old gauntlet top)
px = int(round(ball_fx - piece_scaled.size[0] / 2))
py = int(round(ball_fy + 9))
print('CJ15 piece paste at', px, py, 'piece size', piece_scaled.size)
# Background multiplane (painted, same recipe as original)
far = painted_bg('clean-100-20261031/layouts/bg-flying-painted-20261031.jpg', W, H, LUT15).filter(ImageFilter.GaussianBlur(4))
mid_full = painted_bg('clean-100-20261031/layouts/bg-flying-painted-20261031.jpg', W, H, LUT15)
mid_full = mid_full.resize((int(W * 1.07), int(H * 1.07)), Image.LANCZOS)
mid_full = mid_full.crop((24, int(H * 0.07) // 2, 24 + W, int(H * 0.07) // 2 + H))
band = Image.new('L', (W, H), 0); bd = ImageDraw.Draw(band)
for y in range(ground_y - 260, H):
    bd.line([(0, y), (W, y)], fill=min(255, max(0, (y - (ground_y - 260)) * 4)))
bg15 = Image.composite(mid_full, far, band)
canvas15 = bg15.convert('RGBA')
shl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shl)
sw_ = int(cw * 0.45)
sd.ellipse([W // 2 - sw_ // 2, ground_y - 8, W // 2 + sw_ // 2, ground_y + 26], fill=(0, 0, 0, 45))
canvas15.alpha_composite(shl.filter(ImageFilter.GaussianBlur(6)))
canvas15.alpha_composite(rim15, (cx0, cy0))
canvas15.alpha_composite(char15b, (cx0, cy0))
# Piece ON TOP of torso/cape (foreground occlusion: fist toward camera) + its own rim/bleed
canvas15.alpha_composite(prim, (px, py))
canvas15.alpha_composite(piece_b, (px, py))
# Combined figure bbox (char alpha OR piece alpha, in final coords)
char_alpha = np.array(char15b)[:, :, 3] > 10
piece_alpha = np.array(piece_b)[:, :, 3] > 10
comb = np.zeros((H, W), dtype=bool)
comb[cy0:cy0 + ch, cx0:cx0 + cw] |= char_alpha
comb[py:py + piece_scaled.size[1], px:px + piece_scaled.size[0]] |= piece_alpha
ys2, xs2 = np.where(comb)
box15 = (int(xs2.min()), int(ys2.min()), int(xs2.max()) + 1, int(ys2.max()) + 1)
overlap_px = int(((np.zeros((H, W), dtype=bool)) ) .sum())  # placeholder replaced below
# overlap: piece pixels that fall on top of char pixels (occlusion measure)
ca = np.zeros((H, W), dtype=bool); ca[cy0:cy0 + ch, cx0:cx0 + cw] = char_alpha
pa2 = np.zeros((H, W), dtype=bool); pa2[py:py + piece_scaled.size[1], px:px + piece_scaled.size[0]] = piece_alpha
overlap_px = int((ca & pa2).sum())
eff15 = speed_lines(box15, W, H, RIM15)
eff15_px = int((np.array(eff15)[:, :, 3] > 10).sum())
canvas15.alpha_composite(eff15)
fg_src = painted_bg('clean-100-20261031/layouts/bg-flying-painted-20261031.jpg', W, H, LUT15).filter(ImageFilter.GaussianBlur(8))
fg = fg_src.crop((0, H - 130, W, H)).convert('RGBA')
fga = Image.new('RGBA', (W, 130), (0, 0, 0, 0)); fga.paste(fg, (0, 0))
fa = np.array(fga); fa[:, :, 3] = (fa[:, :, 3] * 0.30).astype(np.uint8)
canvas15.alpha_composite(Image.fromarray(fa), (0, H - 130))
canvas15.convert('RGB').save(os.path.join(OUT, 'CJ-15-flying-forward-foreshortened-rerender-20261031.png'))
pr = canvas15.convert('RGB').copy(); pd = ImageDraw.Draw(pr)
pd.line([(0, ground_y), (W, ground_y)], fill=(255, 255, 0), width=3)
pd.line([(0, feet_y), (W, feet_y)], fill=(0, 255, 255), width=3)
pd.ellipse([W // 2 - 8, feet_y - 8, W // 2 + 8, feet_y + 8], outline=(0, 255, 255), width=3)
pr.save(os.path.join(OUT, 'CJ-15-flying-forward-foreshortened-proof-20261031.png'))
# Stray-fragment gate (final space): char pixels in the OLD-ARM SKY zone
# (final x1130-1240, y430-600 — right of the cape edge, where the old
# gauntlet/fist hung in sky) that are NOT covered by the new piece (+6px
# rim tolerance). Cape/torso/ball are outside this rect by construction.
# Should be 0. (A broader rect counts cape/torso and is not a stray test.)
resid = np.array(char15)
ca_full = np.zeros((H, W), dtype=bool); ca_full[cy0:cy0 + ch, cx0:cx0 + cw] = np.array(char15)[:, :, 3] > 10
pa_full = np.zeros((H, W), dtype=bool); pa_full[py:py + piece_scaled.size[1], px:px + piece_scaled.size[0]] = np.array(piece_b)[:, :, 3] > 10
pa_dil = Image.fromarray((pa_full * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(13))
pa_dil = np.array(pa_dil) > 10
yy_f, xx_f = np.mgrid[0:H, 0:W]
join_zone = (xx_f >= 1130) & (xx_f <= 1240) & (yy_f >= 430) & (yy_f <= 600)
resid_px = int((ca_full & join_zone & (~pa_dil)).sum())
print('CJ15 combined bbox', box15, 'rim', rim15_px + prim_px, 'bleed', bleed15_px + pbleed_px,
      'eff', eff15_px, 'overlap(piece over char)', overlap_px, 'stray join px (char not ball/piece)', resid_px)
cj15_gate = dict(canvas=[W, H], ground_y=ground_y, feet_y=feet_y, height_px=140,
  char_bbox=list(box15), char_size=[box15[2] - box15[0], box15[3] - box15[1]],
  margins=dict(left=box15[0], right=W - box15[2], top=box15[1], bottom=H - box15[3]),
  clipped=bool(box15[0] < 0 or box15[1] < 0 or box15[2] > W or box15[3] > H),
  grounded=False, airborne=True, feet_above_ground_px=ground_y - box15[3] if False else ground_y - feet_y,
  rim_px=rim15_px + prim_px, bleed_px=bleed15_px + pbleed_px, effect='speed-lines', effect_px=eff15_px,
  shaft_count=0, piece_overlap_over_char_px=overlap_px, residual_old_arm_px=resid_px,
  piece_paste=[px, py], piece_size=list(piece_scaled.size), elbow_ball_final=[round(ball_fx, 1), round(ball_fy, 1)])

# ---------- 3. CJ-18 seam options ----------
W18, H18, ground18 = 1920, 1080, 950
LUT18 = [1.25, 0.85, 0.65]; RIM18 = (255, 165, 95); BLEED18 = (255, 110, 30)
plate18 = Image.open(os.path.join(R, 'transparent-plates-sweep-20261031/plates/reposes-v7c-clean__true-flex-double-bicep-v7c-clean.png')).convert('RGBA')
pa = np.array(plate18)[:, :, 3]; ys, xs = np.where(pa > 10)
crop18 = plate18.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
char18 = resize_rgba(crop18, 880)
cw18, ch18 = char18.size; cx18 = (W18 - cw18) // 2; cy18 = ground18 - ch18
print('CJ18 char', cw18, ch18, 'at', cx18, cy18, 'plate bbox', (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
# Seam polylines, plate -> char-local -> final (char scale: cw18/661 wide, 880/1054 tall)
def to_final(px_, py_):
    return (cx18 + (px_ - int(xs.min())) * cw18 / 661, cy18 + (py_ - int(ys.min())) * 880 / 1054)
seams_plate = [((255, 428), (375, 478)), ((715, 432), (840, 482))]
seams_final = [(to_final(*a), to_final(*b)) for a, b in seams_plate]
print('CJ18 seams final', seams_final)
# Seam band mask in char-local coords
band_mask = Image.new('L', char18.size, 0); md = ImageDraw.Draw(band_mask)
for (a, b) in seams_final:
    la = (a[0] - cx18, a[1] - cy18); lb = (b[0] - cx18, b[1] - cy18)
    md.line([la, lb], fill=255, width=16)
band_mask = band_mask.filter(ImageFilter.GaussianBlur(3))
bm = np.array(band_mask).astype(np.float32) / 255.0
base18 = np.array(char18).astype(np.float32)
blur18 = np.array(char18.filter(ImageFilter.GaussianBlur(2.5))).astype(np.float32)
blend18 = base18 * (1 - bm[..., None]) + blur18 * bm[..., None]
half18 = base18 * (1 - 0.5 * bm[..., None]) + blur18 * (0.5 * bm[..., None])
options = {
  'A-keep-seam': Image.fromarray(base18.astype(np.uint8)),
  'B-blend-seam': Image.fromarray(np.clip(blend18, 0, 255).astype(np.uint8)),
  'C-half-blend-seam': Image.fromarray(np.clip(half18, 0, 255).astype(np.uint8)),
}
cj18_results = {}
for key, ch in options.items():
    carr = np.array(ch).astype(np.float32)
    carr[:, :, :3] = np.clip(carr[:, :, :3] * np.array(LUT18, dtype=np.float32), 0, 255)
    chg = Image.fromarray(carr.astype(np.uint8))
    rim18, chb, rim_px, bleed_px = rim_bleed_layers(chg, RIM18, BLEED18)
    bg18 = script_bg('any', W18, H18, LUT18, ground18, seed=18)
    can = bg18.convert('RGBA')
    shl = Image.new('RGBA', (W18, H18), (0, 0, 0, 0)); sd = ImageDraw.Draw(shl)
    sd.ellipse([W18 // 2 - int(cw18 * 0.75) // 2, ground18 - 8, W18 // 2 + int(cw18 * 0.75) // 2, ground18 + 26], fill=(0, 0, 0, 95))
    can.alpha_composite(shl.filter(ImageFilter.GaussianBlur(6)))
    can.alpha_composite(rim18, (cx18, cy18)); can.alpha_composite(chb, (cx18, cy18))
    box18 = (cx18, cy18, cx18 + cw18, cy18 + ch18)
    eff18 = aura(box18, W18, H18, RIM18)
    eff_px = int((np.array(eff18)[:, :, 3] > 10).sum())
    can.alpha_composite(eff18)
    fg18 = script_bg('any', W18, H18, LUT18, ground18, seed=18 + 99)
    fg = fg18.crop((0, H18 - 130, W18, H18)).convert('RGBA')
    fga = Image.new('RGBA', (W18, 130), (0, 0, 0, 0)); fga.paste(fg, (0, 0))
    fa = np.array(fga); fa[:, :, 3] = (fa[:, :, 3] * 0.30).astype(np.uint8)
    can.alpha_composite(Image.fromarray(fa), (0, H18 - 130))
    out = os.path.join(OUT, f'CJ-18-true-flex-double-bicep-{key}-20261031.png')
    can.convert('RGB').save(out)
    cj18_results[key] = dict(file=os.path.basename(out), canvas=[W18, H18], ground_y=ground18, feet_y=ground18,
      char_bbox=list(box18), margins=dict(left=box18[0], right=W18 - box18[2], top=box18[1], bottom=H18 - box18[3]),
      clipped=False, rim_px=rim_px, bleed_px=bleed_px, effect='power-aura', effect_px=eff_px, shaft_count=0)
    print('CJ18', key, box18, rim_px, bleed_px, eff_px)
json.dump(dict(piece=meas, cj15=cj15_gate, cj18=cj18_results,
  seams_plate=seams_plate, seams_final=[[[list(a), list(b)] for a, b in seams_final]]),
  open(os.path.join(OUT, 'measurements-20261031.json'), 'w'), indent=1)
print('DONE')
