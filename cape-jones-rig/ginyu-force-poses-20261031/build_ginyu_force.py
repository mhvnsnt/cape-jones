"""Whole Ginyu Force pose study — Cape Jones poses from member pose dialects.
ONLY Cape's own v7c rig pieces. No show character shipped, no art copied, no
dialogue, no logo, no character names in any generation prompt (none used).
Method: v7c ball-centre pivots (joint_locked_rig_v7c.py), with a TOP-ARM layer:
any arm that is raised across the face or above the cowl is drawn as a whole
chain (upper + lower + cap) AFTER head/cowl, per the face/cowl snap extension
to ARM-FRONT-SNAP-RULE.md. Chest-only crossing arms use the normal order
(upper behind torso, lower in front of torso, head above arm).
Knee-feet: knees-out -> toes-out, knees-in -> toes-in, checked per pose.
Canvas 1100x1500 transparent per pose.
"""
from PIL import Image, ImageDraw
import os, math
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT="/home/hatch/workspace/cape-jones-rig/ginyu-force-poses-20261031"
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
def figure(c, cx, cfg, head_angle=0, top_arms=()):
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
        if side in top_arms: continue
        ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,_,_=ARM_PIECES[side]; sh=shoulders[side]
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),cx,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),cx,370)
    paste_at(c, load(os.path.join(BASE,"Torso_Chest.png")),cx,400); paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),cx,670)
    for side in ("L","R"):
        if side in top_arms: continue
        _,low,cap=ARM_PIECES[side]; ball,_=ARM[side]
        limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),cx,360)
    head=load(os.path.join(BASE,"Head_Front.png"))
    if head_angle: head=head.rotate(head_angle, expand=True)
    c.alpha_composite(head,(int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    # TOP arms: whole chain after head/cowl, so a raised arm is never buried
    for side in ("L","R"):
        if side not in top_arms: continue
        ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,low,cap=ARM_PIECES[side]; sh=shoulders[side]
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT,low), elbow, cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbow)
    return c
def save_single(name,cfg,head=0,top=()):
    c=Image.new("RGBA",(1100,1500),(0,0,0,0)); figure(c,550,cfg,head,top); c.save(os.path.join(OUT,name)); print(name, "top=",top)

# cfg shorthand: au, al, lu, ll dicts L/R
def C(au,al,lu,ll): return {"arm_upper":{"L":au[0],"R":au[1]},"arm_lower":{"L":al[0],"R":al[1]},"leg_upper":{"L":lu[0],"R":lu[1]},"leg_lower":{"L":ll[0],"R":ll[1]}}

POSES=[
 # CAPTAIN — commanding, chest thrust, S-curve, centre of formation
 ("cap-01-grand-entrance-rollcall-20261031.png", C((-100,10),(30,90),(-40,35),(15,-15)), -8, ("L",)),
 ("cap-02-body-change-spread-20261031.png", C((-150,150),(-20,20),(-35,35),(20,-20)), 0, ("L","R")),
 ("cap-03-crossed-command-20261031.png", C((-20,20),(110,-110),(-20,20),(10,-10)), 6, ("L",)),
 # RECOOME — flamboyant power, wide, dance-trained, showboat
 ("rec-01-power-showboat-wide-20261031.png", C((-120,120),(-40,40),(-50,45),(25,-25)), 10, ("L","R")),
 ("rec-02-eraser-windup-leanback-20261031.png", C((-40,40),(60,-60),(-30,30),(35,-35)), -12, ()),
 ("rec-03-victory-taunt-hips-20261031.png", C((-30,30),(120,-120),(-45,20),(20,-10)), 12, ()),
 # BURTER — speed, lean, flowing, aerodynamic
 ("bur-01-speed-lean-dash-20261031.png", C((-140,60),(-30,-90),(-55,15),(30,-5)), -6, ()),
 ("bur-02-hurricane-spin-windup-20261031.png", C((-90,90),(0,0),(-35,35),(20,-20)), 8, ("L","R")),
 ("bur-03-mach-kick-stance-20261031.png", C((-60,100),(80,-40),(-20,50),(10,-70)), 0, ()),
 # JEICE — elegant/refined, elbows out, hand near face, serve
 ("jei-01-crusher-serve-windup-20261031.png", C((-160,80),(-20,-110),(-25,30),(15,-15)), -10, ("L",)),
 ("jei-02-elegant-elbows-out-20261031.png", C((-80,80),(130,-130),(-20,20),(10,-10)), 14, ()),
 ("jei-03-point-smirk-side-20261031.png", C((-110,20),(40,100),(-35,25),(20,-20)), -12, ("L",)),
 # GULDO — compact low, crouch, hands out, concentration
 ("gul-01-low-crouch-compact-20261031.png", C((-50,50),(90,-90),(-55,55),(55,-55)), 8, ()),
 ("gul-02-time-freeze-focus-20261031.png", C((-90,90),(30,-30),(-40,40),(30,-30)), 0, ()),
 ("gul-03-guard-crouch-startled-20261031.png", C((-30,30),(140,-140),(-45,45),(40,-40)), -8, ("L","R")),
 # BONYU — FORMER member, trait-derived only (she hates posing; no canonical pose
 # documented). These are pose-REFUSAL / neutral beats, labelled as such, not canon.
 ("bon-01-reluctant-rollcall-20261031.png", C((-10,10),(20,-20),(-15,15),(10,-10)), -14, ()),
 ("bon-02-walkoff-left-team-20261031.png", C((-30,30),(40,-40),(-40,20),(25,-10)), -10, ()),
 ("bon-03-training-neutral-20261031.png", C((-45,45),(70,-70),(-25,25),(15,-15)), 0, ()),
]
for name,cfg,head,top in POSES: save_single(name,cfg,head,top)

def thumb(path,w=275):
    im=Image.open(path).convert("RGBA"); bg=Image.new("RGBA",im.size,(128,128,128,255)); bg.alpha_composite(im)
    return bg.resize((w,375),Image.LANCZOS)
def sheet(names,cols,fn,label):
    rows=(len(names)+cols-1)//cols; s=Image.new("RGB",(cols*275,rows*375),(128,128,128)); d=ImageDraw.Draw(s)
    for i,n in enumerate(names):
        s.paste(thumb(os.path.join(OUT,n)),((i%cols)*275,(i//cols)*375))
    s.save(os.path.join(OUT,fn)); print(fn)
# per-member sheets (3 poses each)
for prefix in ("cap","rec","bur","jei","gul","bon"):
    ms=[n for n,_,_,_ in POSES if n.startswith(prefix)]
    sheet(ms,3,f"{prefix}-contact-20261031.png","")
# full force: 5 core members x3 = 15, then Bonyu 3 separately below
core=[n for n,_,_,_ in POSES if not n.startswith("bon")]
sheet(core,5,"full-force-contact-20261031.png","")
sheet([n for n,_,_,_ in POSES if n.startswith("bon")],3,"bonyu-contact-20261031.png","")
# roll-call sequence: canonical intro order Recoome, Burter, Jeice, Guldo, Ginyu;
# roll-call pose per member + final spread, then Bonyu walk-off coda (labelled former)
roll=["rec-01-power-showboat-wide-20261031.png","bur-02-hurricane-spin-windup-20261031.png",
"jei-02-elegant-elbows-out-20261031.png","gul-01-low-crouch-compact-20261031.png",
"cap-01-grand-entrance-rollcall-20261031.png","cap-02-body-change-spread-20261031.png"]
sheet(roll,6,"rollcall-contact-20261031.png","")
frames=[]
for n in roll:
    im=Image.open(os.path.join(OUT,n)).convert("RGBA"); bg=Image.new("RGBA",im.size,(128,128,128,255)); bg.alpha_composite(im)
    frames.append(bg.resize((275,375),Image.LANCZOS))
# GIF: announce hold (2 frames per pose) -> snap is the cut -> hold; loop the 6
gif_frames=[]
for f in frames: gif_frames += [f,f]
gif_frames[0].save(os.path.join(OUT,"rollcall-sequence-20261031.gif"), save_all=True, append_images=gif_frames[1:], duration=500, loop=0)
print("rollcall gif done")
