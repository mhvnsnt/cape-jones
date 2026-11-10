"""Limits-broken builds. Reuses v7c ball-centre method from build_ginyu_force.py
(copied, not imported — the original runs its pose loop on import).
New: straight kick (knee ~straight), segment-twist torso (chest rotated +
shoulder line tilted, pelvis unrotated), hand substitution (pulled pieces
from sliced/, white-pixel-only erase of the old fist, no redrawn hand),
PIL effect layers on top of untouched poses (effects only, pose art intact).
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
ORIG="/home/hatch/workspace/cape-jones-rig/ginyu-force-poses-20261031"
OUT="/home/hatch/workspace/cape-jones-rig/ginyu-force-limits-broken-20261031"
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
def figure(c, cx, cfg, head_angle=0, top_arms=(), chest_rot=0, shoulder_tilt=0):
    paste_at(c, load(os.path.join(BASE,"Cape_Back_Main.png")),cx,410)
    hips={"L":(cx-80,740),"R":(cx+65,740)}
    shoulders={"L":(cx-120,445-shoulder_tilt),"R":(cx+120,445+shoulder_tilt)}
    for side in ("L","R"):
        hip=hips[side]; ball,hip_anchor=LEG[side]; vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up,low,cap=LEG_PIECES[side]
        limb(c, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        if side in top_arms: continue
        ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,_,_=ARM_PIECES[side]; sh=shoulders[side]
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),cx,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),cx,370)
    chest=load(os.path.join(BASE,"Torso_Chest.png"))
    if chest_rot: chest=chest.rotate(chest_rot, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(chest,(int(cx-chest.size[0]/2), int(400+ (load(os.path.join(BASE,"Torso_Chest.png")).size[1]-chest.size[1])/2)))
    paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),cx,670)
    for side in ("L","R"):
        if side in top_arms: continue
        _,low,cap=ARM_PIECES[side]; ball,_=ARM[side]
        limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),cx,360)
    head=load(os.path.join(BASE,"Head_Front.png"))
    if head_angle: head=head.rotate(head_angle, expand=True)
    c.alpha_composite(head,(int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    for side in ("L","R"):
        if side not in top_arms: continue
        ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,low,cap=ARM_PIECES[side]; sh=shoulders[side]
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT,low), elbow, cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbow)
    return c
def C(au,al,lu,ll): return {"arm_upper":{"L":au[0],"R":au[1]},"arm_lower":{"L":al[0],"R":al[1]},"leg_upper":{"L":lu[0],"R":lu[1]},"leg_lower":{"L":ll[0],"R":ll[1]}}
def save(name,cfg,head=0,top=(),chest_rot=0,tilt=0):
    c=Image.new("RGBA",(1100,1500),(0,0,0,0)); figure(c,550,cfg,head,top,chest_rot,tilt); c.save(os.path.join(OUT,name)); print(name); return c

# 1. KICK — Burter mach kick, knee straight: upper 65 / lower 60 (was 50 / -70, ~120 deg bend)
save("bur-03-mach-kick-extended-20261031.png", C((-60,100),(80,-40),(-20,65),(10,60)), 0, ())
# 2. TORSO SEGMENT-TWIST — chest rotated, shoulder line tilted, pelvis/belt unrotated
save("cap-01-twist-segment-20261031.png", C((-100,10),(30,90),(-40,35),(15,-15)), -8, ("L",), chest_rot=-8, tilt=14)
save("bur-01-twist-segment-20261031.png", C((-140,60),(-30,-90),(-55,15),(30,-5)), -6, (), chest_rot=8, tilt=-12)

def erase_white_circle(im, cx, cy, r):
    px=im.load()
    for y in range(max(0,int(cy-r)), min(im.size[1],int(cy+r))):
        for x in range(max(0,int(cx-r)), min(im.size[0],int(cx+r))):
            if (x-cx)**2+(y-cy)**2 <= r*r:
                R,G,B,A=px[x,y]
                if A>0 and R>180 and G>180 and B>180: px[x,y]=(0,0,0,0)
    return im
def hand_swap(pose_name, hand_file, centre, angle, erase_r, out_name):
    c=Image.open(os.path.join(OUT,pose_name)).convert("RGBA") if os.path.exists(os.path.join(OUT,pose_name)) else Image.open(os.path.join(ORIG,pose_name)).convert("RGBA")
    # For Jeice poses, rebuild fresh from original builder cfg so swap is on the approved base
    c=erase_white_circle(c, centre[0], centre[1], erase_r)
    hand=load(os.path.join(BASE,hand_file), scale=1.0)
    if angle: hand=hand.rotate(angle, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(hand,(int(centre[0]-hand.size[0]/2), int(centre[1]-hand.size[1]/2)))
    c.save(os.path.join(OUT,out_name)); print(out_name, "hand centre", centre, "angle", angle)

# Jeice serve: rebuild base first, then swap. Base cfg = original JEI-01
save("jei-01-base-for-swap-20261031.png", C((-160,80),(-20,-110),(-25,30),(15,-15)), -10, ("L",))
# fist end computed: elbow (382,268), fist ~(314,517). Open hand over it, rotated -20 to match forearm
hand_swap("jei-01-base-for-swap-20261031.png", "Hand_3_Open.png", (314,530), -20, 65, "jei-01-crusher-serve-open-palm-20261031.png")
# Jeice point: rebuild JEI-03 base, view first in v1 (no swap yet) — swap position computed below in step 2
save("jei-03-base-for-swap-20261031.png", C((-110,20),(40,100),(-35,25),(20,-20)), -12, ("L",))
print("done v1")
