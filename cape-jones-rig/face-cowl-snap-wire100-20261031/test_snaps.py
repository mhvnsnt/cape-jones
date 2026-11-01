"""Render each gate-firing candidate in NORMAL v7c order and in SNAPPED order, diff them.
Snapped order: flagged arm chain (upper+lower+cap) drawn AFTER torso/collar/neck/head
for FACE/COWL, AFTER torso but BEFORE head for CHEST. Other arm stays normal.
"""
import os, math, sys
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/pose-dialects-20261031")
from PIL import Image
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT="/home/hatch/workspace/cape-jones-rig/face-cowl-snap-wire100-20261031"
SCALE=0.95
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((max(1,int(im.size[0]*scale)), max(1,int(im.size[1]*scale))), Image.LANCZOS)
def paste_at(c, im, cx, top): c.alpha_composite(im,(int(cx-im.size[0]/2),int(top)))
def limb(c, path, joint, angle, anchor):
    im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
    layer=Image.new("RGBA",c.size,(0,0,0,0)); layer.alpha_composite(im,(int(joint[0]-ax),int(joint[1]-ay)))
    layer=layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im=load(path); c.alpha_composite(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)))
def rot_vec(v, a):
    r=math.radians(a); x,y=v; return (x*math.cos(r)+y*math.sin(r), -x*math.sin(r)+y*math.cos(r))
def figure(cx, cfg, head=0, snap=None):
    """snap: dict side -> 'face'|'cowl'|'chest' ; snapped chain drawn in the snapped pass, not normal pass."""
    c=Image.new("RGBA",(1100,1500),(0,0,0,0))
    paste_at(c, load(os.path.join(BASE,"Cape_Back_Main.png")),cx,410)
    hips={"L":(cx-80,740),"R":(cx+65,740)}; shoulders={"L":(cx-120,445),"R":(cx+120,445)}
    for side in ("L","R"):
        hip=hips[side]; ball,hip_anchor=LEG[side]; vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up,low,cap=LEG_PIECES[side]
        limb(c, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,_,_=ARM_PIECES[side]; sh=shoulders[side]
        if snap and side in snap:
            elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
            continue
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),cx,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),cx,370)
    paste_at(c, load(os.path.join(BASE,"Torso_Chest.png")),cx,400); paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),cx,670)
    for side in ("L","R"):
        if snap and side in snap and snap[side] in ("face","cowl"): continue
        _,low,cap=ARM_PIECES[side]; ball,_=ARM[side]
        limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    # chest snaps: chain drawn here (above torso, below head) — in normal order upper was before torso,
    # so for chest we must draw the WHOLE chain here (upper too), not just lower.
    for side in ("L","R"):
        if snap and side in snap and snap[side]=="chest":
            up,low,cap=ARM_PIECES[side]; ball,sh_anchor=ARM[side]; sh=shoulders[side]
            limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
            limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),cx,360)
    head_im=load(os.path.join(BASE,"Head_Front.png"))
    if head: head_im=head_im.rotate(head, expand=True)
    c.alpha_composite(head_im,(int(cx-head_im.size[0]/2), int(331-head_im.size[1]/2)))
    # face/cowl snaps: whole chain on top of everything
    for side in ("L","R"):
        if snap and side in snap and snap[side] in ("face","cowl"):
            up,low,cap=ARM_PIECES[side]; ball,sh_anchor=ARM[side]; sh=shoulders[side]
            limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
            limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    return c

CANDS = [
 ("jojo-02", {"arm_upper":{"L":-115,"R":65},"arm_lower":{"L":85,"R":-95},"leg_upper":{"L":-16,"R":32},"leg_lower":{"L":6,"R":-28}}, -10, {"L":"cowl","R":"chest"}),
 ("stand-02-user", {"arm_upper":{"L":-35,"R":35},"arm_lower":{"L":60,"R":-60},"leg_upper":{"L":-30,"R":30},"leg_lower":{"L":35,"R":-35}}, 6, {"L":"chest","R":"chest"}),
 ("ginyu-03", {"arm_upper":{"L":-130,"R":130},"arm_lower":{"L":-60,"R":60},"leg_upper":{"L":-20,"R":35},"leg_lower":{"L":30,"R":-20}}, 10, {"L":"cowl","R":"cowl"}),
 ("v7c-flex", {"arm_upper":{"L":-25,"R":25},"arm_lower":{"L":160,"R":-160},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}}, 0, {"L":"chest","R":"chest"}),
 ("v7c-jump", {"arm_upper":{"L":-150,"R":150},"arm_lower":{"L":-150,"R":150},"leg_upper":{"L":-20,"R":20},"leg_lower":{"L":45,"R":-45}}, 0, {"L":"cowl","R":"cowl"}),
 ("dance-STRIDE_B", {"arm_upper":{"L":35,"R":-35},"arm_lower":{"L":30,"R":-30},"leg_upper":{"L":25,"R":-25},"leg_lower":{"L":-20,"R":20}}, 0, {"L":"chest","R":"chest"}),
 ("dance-TWIST", {"arm_upper":{"L":-90,"R":20},"arm_lower":{"L":120,"R":-60},"leg_upper":{"L":-20,"R":30},"leg_lower":{"L":30,"R":-20}}, 0, {"R":"chest"}),
]
import numpy as np
for name, cfg, head, snap in CANDS:
    n = figure(550, cfg, head, snap=None)
    s = figure(550, cfg, head, snap=snap)
    na = np.array(n.split()[3]); sa = np.array(s.split()[3])
    diff = int(((np.abs(na.astype(int)-sa.astype(int))>20)).sum())
    # also RGB diff where both opaque
    n.save(f"{OUT}/test-{name}-normal-20261031.png"); s.save(f"{OUT}/test-{name}-snapped-20261031.png")
    print(f"{name}: snap={snap} alpha-diff-px={diff}")
