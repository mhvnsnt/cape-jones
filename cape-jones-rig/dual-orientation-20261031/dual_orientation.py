"""Dual-orientation delivery for Cape Jones (YouTube + TikTok).
Method: OPEN-GATE / PROTECTED-MASTER (2D analogue of camera open-gate):
  master = 1920x1920 square. Landscape = centre 1920x1080 crop.
  Portrait = centre 1080x1920 crop. Intersection = central 1080x1080
  protected square. Subject fitted inside that square => whole in BOTH.
Safe zones (see spec doc for sources): portrait organic union =
  left 97, right 238, top 288, bottom 438 on 1080x1920; ads bottom = 672.
Landscape: action-safe 5%, title-safe 10% (broadcast convention).
"""
from PIL import Image, ImageDraw, ImageFilter
import json, os
ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "dual-orientation-20261031")
FIG = os.path.join(ROOT, "dual-light-variants-20261031/base-arms-up-transparent-20261031.png")
BG  = os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets/backgrounds/batch-KKGuh.jpg")

def cover(bg, size):
    im = bg.copy(); im.thumbnail(size, Image.LANCZOS)
    # cover: resize so both dims >= target, then centre crop
    r = max(size[0]/im.width, size[1]/im.height)
    im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x = (im.width-size[0])//2; y = (im.height-size[1])//2
    return im.crop((x, y, x+size[0], y+size[1]))

def alpha_bbox(im):
    a = im.split()[3]
    return a.getbbox()

fig = Image.open(FIG).convert("RGBA")
print("figure source", fig.size, "alpha bbox", alpha_bbox(fig))
bg = Image.open(BG).convert("RGB")
master = cover(bg, (1920,1920)).convert("RGBA")
# place figure: height 1020 inside protected square (1080), centred on master centre
fh = 1020; fw = round(fig.width*fh/fig.height)
fig_s = fig.resize((fw, fh), Image.LANCZOS)
master.alpha_composite(fig_s, ((1920-fw)//2, (1920-fh)//2))
print("figure placed", fw, fh, "at", (1920-fw)//2, (1920-fh)//2)
# measured subject bbox in master coords
mb = alpha_bbox(master)
print("master alpha bbox (figure, bg opaque? bg is opaque so use fig bbox instead)")
# figure bbox in master = placement box trimmed by fig alpha bbox
fb = alpha_bbox(fig); fx0 = (1920-fw)//2 + round(fb[0]*fw/fig.width); fy0 = (1920-fh)//2 + round(fb[1]*fh/fig.height)
fx1 = (1920-fw)//2 + round(fb[2]*fw/fig.width); fy1 = (1920-fh)//2 + round(fb[3]*fh/fig.height)
print("figure bbox in master", (fx0,fy0,fx1,fy1))
master_rgb = master.convert("RGB")
master_rgb.save(f"{OUT}/master-1920x1920-20261031.png")

# crops
land = master_rgb.crop((0,420,1920,1500))          # 1920x1080
port = master_rgb.crop((420,0,1500,1920))          # 1080x1920
sq   = master_rgb.crop((420,420,1500,1500))        # 1080x1080
land.save(f"{OUT}/landscape-1920x1080-clean-20261031.png")
port.save(f"{OUT}/portrait-1080x1920-clean-20261031.png")
sq.save(f"{OUT}/square-1080x1080-clean-20261031.png")

# figure bbox in each crop
def in_crop(b, ox, oy): return (b[0]-ox, b[1]-oy, b[2]-ox, b[3]-oy)
fig_land = in_crop((fx0,fy0,fx1,fy1), 0, 420)
fig_port = in_crop((fx0,fy0,fx1,fy1), 420, 0)
fig_sq   = in_crop((fx0,fy0,fx1,fy1), 420, 420)
print("figure in landscape", fig_land, "whole?", fig_land[0]>=0 and fig_land[1]>=0 and fig_land[2]<=1920 and fig_land[3]<=1080)
print("figure in portrait", fig_port, "whole?", fig_port[0]>=0 and fig_port[1]>=0 and fig_port[2]<=1080 and fig_port[3]<=1920)

# --- safe-area overlays (proof only, NOT in clean exports) ---
def overlay_portrait(im):
    o = im.copy(); d = ImageDraw.Draw(o, "RGBA")
    # UI dead zones, shaded
    d.rectangle([0,0,1080,288], fill=(255,0,0,70))      # top
    d.rectangle([0,1482,1080,1920], fill=(255,0,0,70))  # bottom organic
    d.rectangle([0,1248,1080,1482], fill=(255,165,0,60))# ads extra bottom 672 total
    d.rectangle([842,0,1080,1920], fill=(255,0,0,70))   # right
    d.rectangle([0,0,97,1920], fill=(255,0,0,70))       # left
    # organic safe box green, ads box amber dashed
    d.rectangle([97,288,842,1482], outline=(0,255,0), width=6)
    d.rectangle([97,288,842,1248], outline=(255,165,0), width=4)
    d.rectangle(fig_port, outline=(0,200,255), width=4)
    return o
def overlay_landscape(im):
    o = im.copy(); d = ImageDraw.Draw(o, "RGBA")
    d.rectangle([96,54,1824,1026], outline=(255,0,0), width=4)    # action safe 5%
    d.rectangle([192,108,1728,972], outline=(0,255,0), width=4)   # title safe 10%
    d.rectangle(fig_land, outline=(0,200,255), width=4)
    return o

overlay_portrait(port).save(f"{OUT}/portrait-1080x1920-safe-overlay-20261031.png")
overlay_landscape(land).save(f"{OUT}/landscape-1920x1080-safe-overlay-20261031.png")

# --- method B: blurred pillarbox fill from landscape (no crop loss, smaller subject) ---
blur = land.filter(ImageFilter.GaussianBlur(30)).resize((1080,1920))
# cover-crop blur to portrait
blur = cover(land, (1080,1920)).filter(ImageFilter.GaussianBlur(25))
fg = land.resize((1080,608), Image.LANCZOS)
pf = blur.copy(); pf.paste(fg, (0,(1920-608)//2))
pf.save(f"{OUT}/portrait-blurfill-from-landscape-20261031.png")

# --- method C (BAD, shown as warning): blind 9:16 centre crop from landscape ---
bad = land.crop(((1920-607)//2,0,(1920-607)//2+607,1080)).resize((1080,1920), Image.LANCZOS)
bad.save(f"{OUT}/portrait-blind-crop-WARNING-cuts-arms-20261031.png")
# how much of figure is cut in blind crop?
bx0 = fig_land[0]-((1920-607)//2); bx1 = fig_land[2]-((1920-607)//2)
print("blind crop figure x-range in 607-wide crop:", bx0, bx1, "cut left px:", max(0,-bx0), "cut right px:", max(0,bx1-607))

# --- master diagram: master with both crop windows + protected square ---
diag = master_rgb.copy(); d = ImageDraw.Draw(diag, "RGBA")
d.rectangle([0,420,1920,1500], outline=(0,200,255), width=8)   # landscape
d.rectangle([420,0,1500,1920], outline=(255,200,0), width=8)  # portrait
d.rectangle([420,420,1500,1500], outline=(0,255,0), width=8)  # protected
d.rectangle((fx0,fy0,fx1,fy1), outline=(255,0,255), width=6)
diag.save(f"{OUT}/master-diagram-crops-and-protected-20261031.png")

# --- contact sheet: master diagram + landscape + portrait ---
sheet = Image.new("RGB", (1920, 1920+1080+1920), (128,128,128))
# scale diagram to 960 wide for sheet? keep simple: stack scaled versions
def scaled(im, w):
    return im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
parts = [scaled(diag, 960), scaled(land, 960), scaled(port, 540)]
y=0; sheet2 = Image.new("RGB", (960, sum(p.height for p in parts)), (128,128,128))
for p in parts: sheet2.paste(p,(0,y)); y+=p.height
sheet2.save(f"{OUT}/dual-orientation-contact-20261031.png")
print("sheet", sheet2.size)

meta = {
 "master": "1920x1920 square open-gate master",
 "protected_square": [420,420,1500,1500],
 "landscape_crop": [0,420,1920,1500],
 "portrait_crop": [420,0,1500,1920],
 "figure_bbox_master": [fx0,fy0,fx1,fy1],
 "figure_bbox_landscape": list(fig_land),
 "figure_bbox_portrait": list(fig_port),
 "figure_whole_in_landscape": bool(fig_land[0]>=0 and fig_land[1]>=0 and fig_land[2]<=1920 and fig_land[3]<=1080),
 "figure_whole_in_portrait": bool(fig_port[0]>=0 and fig_port[1]>=0 and fig_port[2]<=1080 and fig_port[3]<=1920),
 "portrait_safe_organic": {"left":97,"right":238,"top":288,"bottom":438,"box":[97,288,842,1482]},
 "portrait_safe_ads_bottom": 672,
 "blind_crop_figure_cut": {"left_px": max(0,-bx0), "right_px": max(0,bx1-607)},
}
json.dump(meta, open(f"{OUT}/dual-orientation-measurements-20261031.json","w"), indent=2)
print(json.dumps(meta, indent=2))
