"""CJ-15 v3: L arm omitted from body build, replaced by ONE scaled foreground
lower arm (cut piece, no added fist) anchored at L shoulder, fist landing
centre-front. No extra arm, no double fist. v1/v2 kept."""
from PIL import Image
import os, math
RIG="/home/hatch/workspace/cape-jones-rig"
BASE=os.path.join(RIG,"sliced"); CUT=os.path.join(RIG,"cut-limbs-v7c")
OUT=os.path.join(RIG,"storyboards-animatic-20261031/poses")
SCALE=0.95; CX=550; W=1100
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def rot_vec(v, a):
    a=math.radians(a); x,y=v; return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
SHOULDER={"L":(430,445),"R":(670,445)}; HIP={"L":(470,740),"R":(615,740)}
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
cfg={"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-5,"R":5},"leg_lower":{"L":5,"R":-5}}
canvas=Image.new("RGBA",(W,1500),(0,0,0,0))
def paste_at(im, cx, top): canvas.paste(im,(int(cx-im.size[0]/2),int(top)),im)
def limb(path, joint, angle, anchor, scale=SCALE):
    im=load(path, scale=scale); ax,ay=anchor[0]*scale,anchor[1]*scale
    layer=Image.new("RGBA",(W,1500),(0,0,0,0)); layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
    canvas.alpha_composite(layer.rotate(angle, center=joint, expand=False))
def cap_at(path, joint):
    im=load(path); canvas.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
paste_at(load(os.path.join(BASE,"Cape_Back_Main.png")),CX,410)
for side in ("L","R"):
    hip=HIP[side]; ball, hip_anchor = LEG[side]; vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1]); up,low,cap = LEG_PIECES[side]
    limb(os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
    knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
    limb(os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0)); cap_at(os.path.join(CUT,cap), knee)
# R arm only (L arm replaced by foreground arm below)
side="R"; ball, sh_anchor = ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,_,_ = ARM_PIECES[side]; sh=SHOULDER[side]
limb(os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
elbow=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
paste_at(load(os.path.join(BASE,"Pelvis.png")),CX,680); paste_at(load(os.path.join(BASE,"Cape_Collar.png")),CX,370)
paste_at(load(os.path.join(BASE,"Torso_Chest.png")),CX,400); paste_at(load(os.path.join(BASE,"Belt_Overlay.png")),CX,670)
_,low,cap = ARM_PIECES[side]; limb(os.path.join(CUT,low), elbow, cfg["arm_lower"][side], (ball[0],0)); cap_at(os.path.join(CUT,cap), elbow)
paste_at(load(os.path.join(BASE,"Neck.png"),scale=1.05),CX,360); paste_at(load(os.path.join(BASE,"Head_Front.png")),CX,250)
# Foreground L arm: front lower piece, 1.7x, anchored at L shoulder, rotated so its
# fist (piece end) lands centre-front over chest. One arm, one fist.
limb(os.path.join(CUT,"Arm_Front_Lower.png"), SHOULDER["L"], -55, (60,0), scale=SCALE*1.7)
bbox=canvas.getchannel("A").getbbox()
x0=max(0,bbox[0]-20); y0=max(0,bbox[1]-20); x1=min(W,bbox[2]+20); y1=min(1500,bbox[3]+20)
out=canvas.crop((x0,y0,x1,y1)); out.save(os.path.join(OUT,"CJ-15-flying-forward-foreshortened-pose-20261031-v3.png"))
print("CJ-15 v3", out.size, bbox)
