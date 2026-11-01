"""Face/cowl snap fix: render ONLY the flagged arm chain in its original pose
position and composite it on top of the original pose. No angle changes, no
redraw, no other arm touched. Original files untouched."""
import os, math
from PIL import Image, ImageDraw
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
SRC="/home/hatch/workspace/cape-jones-rig/pose-dialects-20261031"
OUT="/home/hatch/workspace/cape-jones-rig/pose-dialects-fix-face-cowl-20261031"
SCALE=0.95
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((max(1,int(im.size[0]*scale)), max(1,int(im.size[1]*scale))), Image.LANCZOS)
def limb_layer(path, joint, angle, anchor):
    im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
    layer=Image.new("RGBA",(1100,1500),(0,0,0,0)); layer.alpha_composite(im,(int(joint[0]-ax),int(joint[1]-ay)))
    return layer.rotate(angle, center=joint, expand=False)
def cap_layer(path, joint):
    im=load(path); layer=Image.new("RGBA",(1100,1500),(0,0,0,0)); layer.alpha_composite(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2))); return layer
def rot_vec(v,a):
    r=math.radians(a); x,y=v; return (x*math.cos(r)+y*math.sin(r), -x*math.sin(r)+y*math.cos(r))
def chain_layer(cfg, side, cx=550):
    shoulders={"L":(cx-120,445),"R":(cx+120,445)}
    ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,low,cap=ARM_PIECES[side]; sh=shoulders[side]
    chain=Image.new("RGBA",(1100,1500),(0,0,0,0))
    chain.alpha_composite(limb_layer(os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor))
    elbow=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    chain.alpha_composite(limb_layer(os.path.join(CUT,low), elbow, cfg["arm_lower"][side], (ball[0],0)))
    chain.alpha_composite(cap_layer(os.path.join(CUT,cap), elbow))
    return chain
def fix(src_name, cfg, side, out_name):
    orig=Image.open(os.path.join(SRC,src_name)).convert("RGBA")
    fixed=orig.copy(); fixed.alpha_composite(chain_layer(cfg,side))
    fixed.save(os.path.join(OUT,out_name)); print(out_name, fixed.size)
    # diff count vs original (pixels changed)
    import numpy as np
    a=np.array(orig); b=np.array(fixed); print("  changed px:", int((np.any(a!=b,axis=2)).sum()))

fix("jojo-03-menacing-lean-hand-face-20261031.png",
    {"arm_upper":{"L":-25,"R":-88},"arm_lower":{"L":35,"R":145}}, "R",
    "jojo-03-menacing-lean-hand-face-FACE-SNAP-20261031.png")
fix("ginyu-01-rollcall-chest-out-20261031.png",
    {"arm_upper":{"L":-160,"R":20},"arm_lower":{"L":-20,"R":95}}, "L",
    "ginyu-01-rollcall-chest-out-COWL-SNAP-20261031.png")

# before/after contact: grey bg, labelled in sheet only (not in pose files)
def on_grey(p):
    im=Image.open(p).convert("RGBA"); bg=Image.new("RGBA",im.size,(128,128,128,255)); bg.alpha_composite(im); return bg
pairs=[
 ("jojo-03 ORIGINAL", os.path.join(SRC,"jojo-03-menacing-lean-hand-face-20261031.png"),
  "jojo-03 FACE-SNAP FIXED", os.path.join(OUT,"jojo-03-menacing-lean-hand-face-FACE-SNAP-20261031.png")),
 ("ginyu-01 ORIGINAL", os.path.join(SRC,"ginyu-01-rollcall-chest-out-20261031.png"),
  "ginyu-01 COWL-SNAP FIXED", os.path.join(OUT,"ginyu-01-rollcall-chest-out-COWL-SNAP-20261031.png")),
]
sheet=Image.new("RGB",(1100,1600),(128,128,128)); d=ImageDraw.Draw(sheet)
y=0
for i,(la,pa,lb,pb) in enumerate(pairs):
    a=on_grey(pa).resize((275,375),Image.LANCZOS); b=on_grey(pb).resize((275,375),Image.LANCZOS)
    d.text((10,y+5),la,fill=(0,0,0)); d.text((300,y+5),lb,fill=(0,0,0))
    sheet.paste(a,(0,y+25)); sheet.paste(b,(285,y+25))
    # zoom crops of the zone, 2x
    if i==0: box=(380,180,780,580)   # face zone jojo03
    else: box=(250,180,650,580)      # cowl/bicep zone ginyu01
    for j,p in enumerate((pa,pb)):
        crop=on_grey(p).crop(box).resize((400,400),Image.LANCZOS)
        sheet.paste(crop,(575+j*410,y+25))
    d.text((575,y+5),"ZOOM: original (left) vs fixed (right)",fill=(0,0,0))
    y+=800
sheet.save(os.path.join(OUT,"before-after-face-cowl-snap-20261031.png")); print("contact done")
