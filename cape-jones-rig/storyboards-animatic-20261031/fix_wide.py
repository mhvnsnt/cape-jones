import sys
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/storyboards-animatic-20261031")
# Standalone wide build (copy of geometry, W=1400, CX=700)
from PIL import Image
import os, math
RIG="/home/hatch/workspace/cape-jones-rig"; BASE=os.path.join(RIG,"sliced"); CUT=os.path.join(RIG,"cut-limbs-v7c")
OUT=os.path.join(RIG,"storyboards-animatic-20261031/poses"); SCALE=0.95; W=1400; CX=700
SHOULDER={"L":(580,445),"R":(820,445)}; HIP={"L":(620,740),"R":(765,740)}
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}; LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.paste(im,(int(cx-im.size[0]/2),int(top)),im)
def rot_vec(v, a):
    a=math.radians(a); x,y=v; return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(name, cfg):
    c=Image.new("RGBA",(W,1500),(0,0,0,0))
    def limb(path, joint, angle, anchor):
        im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
        layer=Image.new("RGBA",(W,1500),(0,0,0,0)); layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
        c.alpha_composite(layer.rotate(angle, center=joint, expand=False))
    def cap_at(path, joint):
        im=load(path); c.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
    paste_at(c, load(os.path.join(BASE,"Cape_Back_Main.png")),CX,410)
    for side in ("L","R"):
        hip=HIP[side]; ball, ha = LEG[side]; vec=(ball[0]-ha[0], ball[1]-ha[1]); up,low,cap = LEG_PIECES[side]
        limb(os.path.join(CUT,up), hip, cfg["leg_upper"][side], ha)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        limb(os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0)); cap_at(os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        ball, sa = ARM[side]; vec=(ball[0]-sa[0], ball[1]-sa[1]); up,_,_ = ARM_PIECES[side]; sh=SHOULDER[side]
        limb(os.path.join(CUT,up), sh, cfg["arm_upper"][side], sa)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),CX,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),CX,370)
    paste_at(c, load(os.path.join(BASE,"Torso_Chest.png")),CX,400); paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),CX,670)
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        limb(os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),CX,360); paste_at(c, load(os.path.join(BASE,"Head_Front.png")),CX,250)
    bbox=c.getchannel("A").getbbox(); x0=max(0,bbox[0]-20); y0=max(0,bbox[1]-20); x1=min(W,bbox[2]+20); y1=min(1500,bbox[3]+20)
    out=c.crop((x0,y0,x1,y1)); out.save(os.path.join(OUT,name)); print(name, out.size, bbox, "clipped" if bbox[0]==0 or bbox[2]==W else "OK")
def C(auL,alL,auR,alR,luL,llL,luR,llR): return {"arm_upper":{"L":auL,"R":auR},"arm_lower":{"L":alL,"R":alR},"leg_upper":{"L":luL,"R":luR},"leg_lower":{"L":llL,"R":llR}}
build("CJ-03-punch-impact-locked-pose-20261031-v2.png", C(-90,-90,20,160,-15,15,15,-15))
build("CJ-05-punch-across-down-pose-20261031-v2.png", C(-90,-90,15,-70,-15,15,15,-15))
build("CJ-13-flying-soar-pose-20261031-v2.png", C(-90,-90,90,90,-5,5,5,-5))
