"""Pose dialects: JoJo / Stand-user / Ginyu-style, built ONLY from Cape Jones v7c rig pieces.
Method: v7c ball-centre pivots (see joint_locked_rig_v7c.py). No new art drawn, no
show characters shipped. Stand figures are silhouettes of Cape's own rig pieces.
Knee-feet rule checked per pose: knees-out -> toes-out, knees-in -> toes-in.
Canvas 1100x1500 per single pose, 2200x1500 for paired Stand poses. Transparent bg.
"""
from PIL import Image
import os, math
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT="/home/hatch/workspace/cape-jones-rig/pose-dialects-20261031"
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
def figure(c, cx, cfg, head_angle=0, tint=None):
    # legs (cape behind legs as in v7c order)
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
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),cx,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),cx,370)
    paste_at(c, load(os.path.join(BASE,"Torso_Chest.png")),cx,400); paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),cx,670)
    for side in ("L","R"):
        _,low,cap=ARM_PIECES[side]; ball,_=ARM[side]
        limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),cx,360)
    head=load(os.path.join(BASE,"Head_Front.png"))
    if head_angle: head=head.rotate(head_angle, expand=True)
    c.alpha_composite(head,(int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    if tint:
        # silhouette: keep alpha, replace RGB
        px=c.load()
        # only tint this figure's region is hard on shared canvas; caller tints a separate layer instead
        pass
    return c
def figure_layer(w,h,cx,cfg,head_angle=0):
    layer=Image.new("RGBA",(w,h),(0,0,0,0)); figure(layer,cx,cfg,head_angle); return layer
def silhouette(layer, rgb, alpha_scale=0.92):
    out=Image.new("RGBA",layer.size,(0,0,0,0)); a=layer.split()[3].point(lambda v:int(v*alpha_scale))
    solid=Image.new("RGBA",layer.size,rgb+(255,)); out.paste(solid, (0,0), a); return out
def save_single(name,cfg,head=0):
    c=Image.new("RGBA",(1100,1500),(0,0,0,0)); figure(c,550,cfg,head); c.save(os.path.join(OUT,name)); print(name)
def save_pair(name,user_cfg,stand_cfg,user_head=0,stand_head=0,stand_cx=830,user_cx=650):
    c=Image.new("RGBA",(2200,1500),(0,0,0,0))
    stand=silhouette(figure_layer(2200,1500,stand_cx,stand_cfg,stand_head),(52,22,90))
    c.alpha_composite(stand); figure(c,user_cx,user_cfg,user_head); c.save(os.path.join(OUT,name)); print(name)

# --- JoJo-style: extreme contrapposto, hips vs shoulders torqued, hand choreography ---
save_single("jojo-01-contrapposto-s-curve-20261031.png",
 {"arm_upper":{"L":-75,"R":40},"arm_lower":{"L":125,"R":-45},"leg_upper":{"L":-38,"R":28},"leg_lower":{"L":22,"R":-18}}, head=12)
save_single("jojo-02-fashion-twist-point-20261031.png",
 {"arm_upper":{"L":-115,"R":65},"arm_lower":{"L":85,"R":-95},"leg_upper":{"L":-16,"R":32},"leg_lower":{"L":6,"R":-28}}, head=-10)
save_single("jojo-03-menacing-lean-hand-face-20261031.png",
 {"arm_upper":{"L":-25,"R":-88},"arm_lower":{"L":35,"R":145},"leg_upper":{"L":-42,"R":12},"leg_lower":{"L":32,"R":-6}}, head=8)
# --- Stand-user pairs: user + larger silhouette of his own rig behind, mirrored / towering ---
save_pair("stand-01-mirrored-pair-20261031.png",
 {"arm_upper":{"L":-60,"R":60},"arm_lower":{"L":130,"R":-130},"leg_upper":{"L":-25,"R":25},"leg_lower":{"L":12,"R":-12}},
 {"arm_upper":{"L":-60,"R":60},"arm_lower":{"L":130,"R":-130},"leg_upper":{"L":-25,"R":25},"leg_lower":{"L":12,"R":-12}}, user_head=0, stand_head=0)
save_pair("stand-02-towering-behind-20261031.png",
 {"arm_upper":{"L":-35,"R":35},"arm_lower":{"L":60,"R":-60},"leg_upper":{"L":-30,"R":30},"leg_lower":{"L":35,"R":-35}},
 {"arm_upper":{"L":-150,"R":150},"arm_lower":{"L":-40,"R":40},"leg_upper":{"L":-12,"R":12},"leg_lower":{"L":-8,"R":8}}, user_head=6, stand_head=-4)
# --- Ginyu-style funny / sentai roll-call: synchronized, chest-out, deliberately goofy ---
save_single("ginyu-01-rollcall-chest-out-20261031.png",
 {"arm_upper":{"L":-160,"R":20},"arm_lower":{"L":-20,"R":95},"leg_upper":{"L":-45,"R":20},"leg_lower":{"L":10,"R":-10}}, head=-6)
save_single("ginyu-02-squat-elbows-out-goofy-20261031.png",
 {"arm_upper":{"L":-70,"R":70},"arm_lower":{"L":140,"R":-140},"leg_upper":{"L":-45,"R":45},"leg_lower":{"L":40,"R":-40}}, head=0)
save_single("ginyu-03-dance-shimmy-hips-out-20261031.png",
 {"arm_upper":{"L":-130,"R":130},"arm_lower":{"L":-60,"R":60},"leg_upper":{"L":-20,"R":35},"leg_lower":{"L":30,"R":-20}}, head=10)

# contact sheets on grey-128 for viewing only
from PIL import ImageDraw
names=["jojo-01-contrapposto-s-curve-20261031.png","jojo-02-fashion-twist-point-20261031.png","jojo-03-menacing-lean-hand-face-20261031.png",
"stand-01-mirrored-pair-20261031.png","stand-02-towering-behind-20261031.png",
"ginyu-01-rollcall-chest-out-20261031.png","ginyu-02-squat-elbows-out-goofy-20261031.png","ginyu-03-dance-shimmy-hips-out-20261031.png"]
thumbs=[]
for n in names:
    im=Image.open(os.path.join(OUT,n)).convert("RGBA")
    bg=Image.new("RGBA",im.size,(128,128,128,255)); bg.alpha_composite(im); thumbs.append(bg.resize((275,375),Image.LANCZOS) if im.size[0]==1100 else bg.resize((550,375),Image.LANCZOS))
sheet=Image.new("RGB",(1100,1500),(128,128,128))
# layout: row1 3 singles, row2 2 pairs (wide), row3 3 singles
x=y=0
for i,t in enumerate(thumbs):
    if i<3: sheet.paste(t,(i*367,0))
    elif i<5: sheet.paste(t,((i-3)*550,375))
    else: sheet.paste(t,((i-5)*367,750))
sheet.save(os.path.join(OUT,"pose-dialects-contact-20261031.png")); print("contact done")
