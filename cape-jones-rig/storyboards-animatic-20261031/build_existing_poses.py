"""Existing-pose transparent renders for storyboard panels (labels=False).
Configs from clips/*.json keyframes; CJ-03 impact = extend geometry held 12f;
CJ-05 across-down re-rendered from the EDL description (R forearm diagonal down
across belly, fist lower centre) because the source variant file is labelled.
CJ-16/CJ-19 keyed from their existing clean files (exact-128 background only,
verified no interior holes on red test)."""
from PIL import Image
import os, math, json, numpy as np
RIG="/home/hatch/workspace/cape-jones-rig"; BASE=os.path.join(RIG,"sliced"); CUT=os.path.join(RIG,"cut-limbs-v7c")
OUT=os.path.join(RIG,"storyboards-animatic-20261031/poses"); SCALE=0.95
SHOULDER={"L":(430,445),"R":(670,445)}; HIP={"L":(470,740),"R":(615,740)}
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}; LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.paste(im,(int(cx-im.size[0]/2),int(top)),im)
def rot_vec(v, a):
    a=math.radians(a); x,y=v; return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(name, cfg):
    c=Image.new("RGBA",(1100,1500),(0,0,0,0))
    def limb(path, joint, angle, anchor):
        im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
        layer=Image.new("RGBA",(1100,1500),(0,0,0,0)); layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
        c.alpha_composite(layer.rotate(angle, center=joint, expand=False))
    def cap_at(path, joint):
        im=load(path); c.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
    paste_at(c, load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
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
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),550,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),550,370)
    paste_at(c, load(os.path.join(BASE,"Torso_Chest.png")),550,400); paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),550,670)
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        limb(os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),550,360); paste_at(c, load(os.path.join(BASE,"Head_Front.png")),550,250)
    bbox=c.getchannel("A").getbbox(); x0=max(0,bbox[0]-20); y0=max(0,bbox[1]-20); x1=min(1100,bbox[2]+20); y1=min(1500,bbox[3]+20)
    out=c.crop((x0,y0,x1,y1)); out.save(os.path.join(OUT,name)); print(name, out.size, bbox)
def C(auL,alL,auR,alR,luL,llL,luR,llR): return {"arm_upper":{"L":auL,"R":auR},"arm_lower":{"L":alL,"R":alR},"leg_upper":{"L":luL,"R":luR},"leg_lower":{"L":llL,"R":llR}}
APOSE=C(-20,-20,20,20,-10,10,10,-10)
build("CJ-03-punch-impact-locked-pose-20261031.png", C(-90,-90,20,160,-15,15,15,-15))
build("CJ-05-punch-across-down-pose-20261031.png", C(-90,-90,15,-70,-15,15,15,-15))
build("CJ-06-walk-street-contact-pose-20261031.png", C(-25,-25,15,15,-25,5,20,-20))
build("CJ-07-walk-town-passing-pose-20261031.png", C(-20,-20,20,20,0,0,0,0))
build("CJ-08-walk-alley-night-pose-20261031.png", C(-15,-15,25,25,20,-20,-25,5))
build("CJ-09-dance-a-pose-20261031.png", C(-150,-150,20,20,-20,20,10,-10))
build("CJ-10-dance-b-pose-20261031.png", C(-20,-20,150,150,10,-10,-20,20))
build("CJ-12-flying-hover-pose-20261031.png", C(-20,-20,20,20,-5,5,5,-5))
build("CJ-13-flying-soar-pose-20261031.png", C(-90,-90,90,90,-5,5,5,-5))
build("CJ-14-flying-dive-pose-20261031.png", C(-150,-150,150,150,-5,5,5,-5))
build("CJ-21-jump-crouch-takeoff-pose-20261031.png", C(-20,-20,20,20,-25,30,25,-30))
build("CJ-22-jump-tuck-landing-pose-20261031.png", C(-150,-150,150,150,-20,45,20,-45))
build("CJ-23-lounge-seated-room-pose-20261031.png", C(-20,-20,20,20,-60,80,60,-80))
build("CJ-24-desk-seated-pose-20261031.png", C(-20,-20,20,20,-60,80,60,-80))
build("CJ-25-room-standing-device-pose-20261031.png", APOSE)
build("CJ-28-rooftop-sunset-pose-20261031.png", APOSE)
build("CJ-29-rooftop-night-city-pose-20261031.png", APOSE)
build("CJ-30-alley-neon-dual-light-pose-20261031.png", APOSE)
# Keyed existing clean poses (exact-128 only)
for name, src in [("CJ-16-flex-anticipation-pose-20261031.png","reposes-v7c-clean/flex-anticipation-before-tighten-v7c-clean.png"),
                  ("CJ-19-fighting-curl-pose-20261031.png","reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")]:
    im=Image.open(os.path.join(RIG,src)).convert("RGBA"); a=np.array(im)
    m=(a[:,:,0]==128)&(a[:,:,1]==128)&(a[:,:,2]==128); a[m,3]=0
    out=Image.fromarray(a); bbox=out.getchannel("A").getbbox()
    x0=max(0,bbox[0]-20); y0=max(0,bbox[1]-20); x1=min(1100,bbox[2]+20); y1=min(1500,bbox[3]+20)
    out=out.crop((x0,y0,x1,y1)); out.save(os.path.join(OUT,name)); print(name, out.size, "keyed", bbox)
