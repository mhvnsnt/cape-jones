"""Effect versions: PIL effect layers composited OVER untouched original poses.
Pose pixels underneath are never recoloured; effect layer is separate and
labelled PIL (not Blender) in the doc. Colours tracked: input + sampled
on-screen at the effect centre (script prints them)."""
from PIL import Image, ImageDraw, ImageFilter
import os, math
ORIG="/home/hatch/workspace/cape-jones-rig/ginyu-force-poses-20261031"
LB="/home/hatch/workspace/cape-jones-rig/ginyu-force-limits-broken-20261031"
OUT=LB
def glow_layer(size, cx, cy, r, colour, peak=200):
    # radial glow: small radial image upscaled
    s=Image.new("RGBA",(r*2,r*2),(0,0,0,0)); d=ImageDraw.Draw(s)
    for i in range(20,0,-1):
        a=int(peak*i/20); d.ellipse([r-r*i/20, r-r*i/20, r+r*i/20, r+r*i/20], fill=colour+(a,))
    lay=Image.new("RGBA",size,(0,0,0,0)); lay.alpha_composite(s,(int(cx-r),int(cy-r))); return lay.filter(ImageFilter.GaussianBlur(6))
def base(name): return Image.open(os.path.join(ORIG,name)).convert("RGBA")
def save(im, fn): im.save(os.path.join(OUT,fn)); print(fn, "sample centre check below")
def sample(im, xy): print("  sample", xy, im.getpixel(xy))

# 1. RECOOME blast — REC-02 lean-back windup, beam from mouth up-right + orb
im=base("rec-02-eraser-windup-leanback-20261031.png"); lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
mouth=(545,375)
d.polygon([(mouth[0],mouth[1]-18),(mouth[0],mouth[1]+18),(880,180),(880,300)], fill=(255,120,40,150))
lay=lay.filter(ImageFilter.GaussianBlur(4))
im.alpha_composite(lay); im.alpha_composite(glow_layer(im.size, 880, 240, 110, (255,140,50), 220))
d2=ImageDraw.Draw(im); d2.ellipse([840,200,920,280], fill=(255,220,120,255), outline=(255,255,255,255), width=4)
save(im,"rec-02-eraser-blast-effect-20261031.png"); sample(im,(880,240))
# 2. BURTER hurricane — BUR-02 spin windup, swirl arcs around body centre
im=base("bur-02-hurricane-spin-windup-20261031.png"); lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
cx,cy=550,760
for r,a0,a1,w in [(260,0,120,14),(330,90,230,12),(400,180,320,10),(470,270,60,8)]:
    d.arc([cx-r,cy-r,cx+r,cy+r], a0, a1, fill=(160,220,255,200), width=w)
    d.arc([cx-r,cy-r,cx+r,cy+r], a0+180, a1+180, fill=(255,255,255,160), width=w//2)
lay=lay.filter(ImageFilter.GaussianBlur(3)); im.alpha_composite(lay)
save(im,"bur-02-hurricane-swirl-effect-20261031.png"); sample(im,(550,500))
# 3. JEICE ball — JEI-01 open-palm (limits-broken), orb above the open palm
im=Image.open(os.path.join(LB,"jei-01-crusher-serve-open-palm-20261031.png")).convert("RGBA")
im.alpha_composite(glow_layer(im.size, 314, 420, 120, (255,220,80), 220))
d=ImageDraw.Draw(im); d.ellipse([264,370,364,470], fill=(255,230,110,255), outline=(255,255,255,255), width=5)
for dx,dy in [(-70,-30),(70,-50),(-50,60),(80,40)]:
    d.ellipse([314+dx-8,420+dy-8,314+dx+8,420+dy+8], fill=(255,255,200,255))
save(im,"jei-01-crusher-ball-effect-20261031.png"); sample(im,(314,420))
# 4. GULDO time — GUL-02 focus, clock rings + ticks around the hands/centre
im=base("gul-02-time-freeze-focus-20261031.png"); lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
cx,cy=550,520
for r,w in [(140,6),(210,5),(280,4)]:
    d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(120,180,255,210), width=w)
for k in range(12):
    a=math.radians(k*30); x1=cx+260*math.cos(a); y1=cy+260*math.sin(a); x2=cx+280*math.cos(a); y2=cy+280*math.sin(a)
    d.line([x1,y1,x2,y2], fill=(200,230,255,230), width=5)
lay=lay.filter(ImageFilter.GaussianBlur(2)); im.alpha_composite(lay)
im.alpha_composite(glow_layer(im.size, 550, 520, 90, (120,180,255), 120))
save(im,"gul-02-time-freeze-effect-20261031.png"); sample(im,(550,520))
# 5. GINYU swap beam — CAP-02 spread, purple beam arc between the outstretched hands + orb
im=base("cap-02-body-change-spread-20261031.png"); lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
d.arc([200,80,900,520], 200, 340, fill=(170,90,255,220), width=22)
d.arc([200,80,900,520], 200, 340, fill=(230,200,255,160), width=8)
lay=lay.filter(ImageFilter.GaussianBlur(4)); im.alpha_composite(lay)
im.alpha_composite(glow_layer(im.size, 550, 200, 100, (170,90,255), 210))
d=ImageDraw.Draw(im); d.ellipse([510,160,590,240], fill=(220,180,255,255), outline=(255,255,255,255), width=4)
save(im,"cap-02-swap-beam-effect-20261031.png"); sample(im,(550,200))
print("effects done")
