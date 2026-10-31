"""Knee-feet fix rebuild of the improved dance.
Same rig/config as dance-improved-20261031/build_dance.py, except:
frames 15-55 (segments stride-B->groove, groove, kick) use FootIn lower
pieces (whole-piece horizontal mirror, new knee anchor) for BOTH legs,
so toes point INWARD where knees point inward. Frames 1-13 and 56-109
keep original lowers (knees outward, toes outward = matching).
Foot swap happens on keyframes 15 and 56 (drawing substitution, like
the gauntlet swap) — noted, not hidden.
"""
from PIL import Image, ImageDraw
import os, math, shutil
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
FLEX="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c-flex-out"
FIX="/home/hatch/workspace/cape-jones-rig/dance-kneefeet-fix-20261031"
OUT=os.path.join(FIX,"frames"); PIECES=os.path.join(FIX,"pieces")
SCALE=0.95
SHOULDER={"L":(430,445),"R":(670,445)}; HIP={"L":(470,740),"R":(615,740)}
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
FOOTIN={"L":("Leg_Front_Lower_FootIn.png",59),"R":("Leg_Back_Lower_FootIn.png",127)}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
FLEX_PIECES={"L":"Arm_Front_Lower_FlexOut.png","R":"Arm_Back_Lower_FlexOut.png"}
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.paste(im,(int(cx-im.size[0]/2),int(top)),im)
def limb(c, path, joint, angle, anchor):
    im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
    layer=Image.new("RGBA",(1100,1500),(0,0,0,0)); layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
    layer=layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im=load(path); c.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
def rot_vec(v, angle_deg):
    a=math.radians(angle_deg); x,y=v
    return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(cfg):
    canvas=Image.new("RGBA",(1100,1500),(0,0,0,0))
    paste_at(canvas, load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
    for side in ("L","R"):
        hip=HIP[side]; ball, hip_anchor = LEG[side]
        vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up,low,cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        if cfg.get("footin"):
            fpath, fball = FOOTIN[side]
            limb(canvas, os.path.join(PIECES,fpath), knee, cfg["leg_lower"][side], (fball,0))
        else:
            limb(canvas, os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0))
        cap_at(canvas, os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        ball, sh_anchor = ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        up,_,_ = ARM_PIECES[side]; sh=SHOULDER[side]
        limb(canvas, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(canvas, load(os.path.join(BASE,"Pelvis.png")),550,680); paste_at(canvas, load(os.path.join(BASE,"Cape_Collar.png")),550,370)
    paste_at(canvas, load(os.path.join(BASE,"Torso_Chest.png")),550,400); paste_at(canvas, load(os.path.join(BASE,"Belt_Overlay.png")),550,670)
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        path = os.path.join(FLEX, FLEX_PIECES[side]) if cfg.get("flexout",{}).get(side) else os.path.join(CUT,low)
        limb(canvas, path, elbows[side], cfg["arm_lower"][side], (ball[0],0))
        cap_at(canvas, os.path.join(CUT,cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE,"Neck.png"),scale=1.05),550,360); paste_at(canvas, load(os.path.join(BASE,"Head_Front.png")),550,250)
    out=Image.new("RGBA",(1100,1500),(0,0,0,0))
    out.alpha_composite(canvas,(int(cfg.get("dx",0)),int(cfg.get("bounce",0))))
    return out
def lerp(a,b,t): return a+(b-a)*t
def interp_pose(pa,pb,t):
    cfg={"arm_upper":{},"arm_lower":{},"leg_upper":{},"leg_lower":{},"flexout":{},"bounce":0,"dx":0}
    for k in ("arm_upper","arm_lower","leg_upper","leg_lower"):
        for s in ("L","R"): cfg[k][s]=lerp(pa[k][s],pb[k][s],t)
    cfg["bounce"]=lerp(pa.get("bounce",0),pb.get("bounce",0),t); cfg["dx"]=lerp(pa.get("dx",0),pb.get("dx",0),t)
    cfg["flexout"]=pb.get("flexout",{}) if t>0.5 else pa.get("flexout",{})
    return cfg
P_STRIDE_A={"arm_upper":{"L":-35,"R":35},"arm_lower":{"L":-30,"R":30},"leg_upper":{"L":-25,"R":25},"leg_lower":{"L":20,"R":-20},"bounce":0,"dx":-20}
P_STRIDE_B={"arm_upper":{"L":35,"R":-35},"arm_lower":{"L":30,"R":-30},"leg_upper":{"L":25,"R":-25},"leg_lower":{"L":-20,"R":20},"bounce":-6,"dx":20}
P_GROOVE_A={"arm_upper":{"L":-60,"R":60},"arm_lower":{"L":-50,"R":50},"leg_upper":{"L":-15,"R":15},"leg_lower":{"L":30,"R":-30},"bounce":-14,"dx":0}
P_GROOVE_B={"arm_upper":{"L":-70,"R":70},"arm_lower":{"L":-40,"R":40},"leg_upper":{"L":15,"R":-15},"leg_lower":{"L":-30,"R":30},"bounce":-8,"dx":0}
P_KICK={"arm_upper":{"L":-45,"R":90},"arm_lower":{"L":-45,"R":90},"leg_upper":{"L":-50,"R":20},"leg_lower":{"L":30,"R":-25},"bounce":-4,"dx":10}
P_SPLIT={"arm_upper":{"L":-70,"R":70},"arm_lower":{"L":150,"R":-150},"leg_upper":{"L":-35,"R":35},"leg_lower":{"L":40,"R":-40},"bounce":-18,"dx":0,"flexout":{"L":True,"R":True}}
P_TWIST={"arm_upper":{"L":-90,"R":20},"arm_lower":{"L":120,"R":-60},"leg_upper":{"L":-20,"R":30},"leg_lower":{"L":30,"R":-20},"bounce":-10,"dx":-15,"flexout":{"L":True}}
P_ARMSUP={"arm_upper":{"L":-70,"R":70},"arm_lower":{"L":150,"R":-150},"leg_upper":{"L":-15,"R":15},"leg_lower":{"L":20,"R":-20},"bounce":-12,"dx":0,"flexout":{"L":True,"R":True}}
P_REST={"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10},"bounce":0,"dx":0}
segments=[
 (1,15,P_STRIDE_A,P_STRIDE_B,2,False),
 (15,28,P_STRIDE_B,P_GROOVE_A,2,True),
 (28,42,P_GROOVE_A,P_GROOVE_B,2,True),
 (42,56,P_GROOVE_B,P_KICK,1,True),
 (56,69,P_KICK,P_SPLIT,2,False),
 (69,83,P_SPLIT,P_TWIST,2,False),
 (83,97,P_TWIST,P_ARMSUP,2,False),
 (97,110,P_ARMSUP,P_REST,2,False),
]
frames={}
for (a,b,pa,pb,step,footin) in segments:
    n=max(1,(b-a)//step)
    for i in range(n+1):
        f=a+i*step
        if f>110: continue
        cfg=interp_pose(pa,pb,i/n if n else 0); cfg["footin"]=footin; frames[f]=cfg
for f in sorted(frames):
    im=build(frames[f])
    if 69<=f<=82:
        r,g,bl,al=im.split()
        r=r.point(lambda v: min(255,int(v*1.20))); g=g.point(lambda v: int(v*0.70)); bl=bl.point(lambda v: min(255,int(v*1.30)))
        im=Image.merge("RGBA",(r,g,bl,al))
    if f in (42,56,69,83):
        d=ImageDraw.Draw(im)
        for (x,y) in [(300,300),(800,300),(550,150)]:
            d.polygon([(x,y-22),(x+7,y-7),(x+22,y),(x+7,y+7),(x,y+22),(x-7,y+7),(x-22,y),(x-7,y-7)],fill=(255,220,80,220))
    im.save(os.path.join(OUT,f"dance-kneefeet-f{f:03d}.png"))
print(f"frames rendered: {len(frames)} footin frames: {sorted(f for f,c in frames.items() if c['footin'])}")
