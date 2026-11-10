"""Before/after proof, REFERENCE ONLY — alignment lines are drawn on proof copies,
never baked into the clean pieces."""
from PIL import Image, ImageDraw
import os
BASE = os.path.expanduser('~/workspace/cape-jones-rig/')
def panel(path, label, colour, axis_x_frac, fist_x_frac):
    im = Image.open(path).convert('RGBA')
    # scale to height 300, on checker-ish dark bg
    s = 300 / im.height
    im = im.resize((int(im.width*s), 300), Image.LANCZOS)
    bg = Image.new('RGBA', (im.width, 340), (30, 30, 30, 255))
    bg.alpha_composite(im, (0, 20))
    d = ImageDraw.Draw(bg)
    ax = int(axis_x_frac * im.width); fx = int(fist_x_frac * im.width)
    d.line([(ax, 20), (ax, 320)], fill=colour, width=3)
    d.ellipse([fx-7, 260, fx+7, 274], outline=colour, width=3)
    d.text((5, 325), label, fill=(255, 255, 255, 255))
    return bg
# axis fractions: use measured medians / widths
# v2 Arm2: forearm median 173.5/249=0.697, fist 180/249=0.723 (QC bands; manual kink -26px at extrapolated axis)
# original Back: forearm 109.8/158=0.695, fist 103.5/158=0.655
# v3: forearm 175.5/249=0.705, fist 174/249=0.699
p1 = panel(BASE+'forearm-head34-v2-20261031/forearm-v2-arm2-back-20261031.png', 'BAD v2: 23deg shear, kink', (255,0,0,255), 0.697, 0.723)
p2 = panel(BASE+'cut-limbs-v7c/Arm_Back_Lower.png', 'REF v7c: 4deg', (0,200,0,255), 0.695, 0.655)
p3 = panel(BASE+'forearm-arm2-aligned-20261031/forearm-v3-arm2-back-aligned-20261031.png', 'FIXED v3: 5.6deg, PASS', (0,200,0,255), 0.705, 0.699)
W = p1.width + p2.width + p3.width + 20
out = Image.new('RGBA', (W, 340), (20, 20, 20, 255))
out.alpha_composite(p1, (0, 0)); out.alpha_composite(p2, (p1.width+10, 0)); out.alpha_composite(p3, (p1.width+p2.width+20, 0))
out.save(BASE+'forearm-arm2-aligned-20261031/proof-arm2-alignment-before-after-20261031.png')
print(f"saved proof {out.size}")
