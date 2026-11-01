"""Flex test sheet: joint-cut upper/lower arms, elbow ball pivot.
Own code, Cape Jones pieces only. No Toon Boom code.
Upper/lower from cut-limbs-v7 (standard joint cut, ball centre pivot).
"""
import os, math
from PIL import Image
BASE="/home/hatch/workspace/cape-jones-rig/sliced"
CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7"
OUT="/home/hatch/workspace/cape-jones-rig/wire-up-cannot-do-20261101/renders"
os.makedirs(OUT, exist_ok=True)
SCALE=0.95
SHOULDER={"L":(430,445),"R":(670,445)}
HIP={"L":(470,740),"R":(615,740)}
ARM_UPPER_LEN=192*SCALE
LEG_UPPER_LEN=274*SCALE
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png",(77,40),(77,14)),
            "R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png",(84,40),(84,14))}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),
            "R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
def load(p,scale=SCALE):
    im=Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0]*scale),int(im.size[1]*scale)),Image.LANCZOS)
def paste_at(c,im,cx,top):
    c.paste(im,(int(cx-im.size[0]/2),int(top)),im)
def limb(c,piece,joint,angle,anchor):
    im=load(piece); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
    layer=Image.new("RGBA",(1100,1500),(0,0,0,0))
    layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
    layer=layer.rotate(angle,center=joint,expand=False)
    c.alpha_composite(layer)
def cap_at(c,cap,joint):
    im=load(cap); c.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
def end_joint(joint,length,angle):
    a=math.radians(angle); return (joint[0]+length*math.sin(a),joint[1]+length*math.cos(a))
def build(name,up,low,leg_up={"L":-10,"R":10},leg_low={"L":-10,"R":10}):
    c=Image.new("RGBA",(1100,1500),(200,200,195,255))
    paste_at(c,load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
    for side in ("L","R"):
        hip=HIP[side]; upn,lown,capn,hipa,kneea=LEG_PIECES[side]
        limb(c,os.path.join(CUT,upn),hip,leg_up[side],hipa)
        knee=end_joint(hip,LEG_UPPER_LEN,leg_up[side])
        limb(c,os.path.join(CUT,lown),knee,leg_low[side],kneea)
        cap_at(c,os.path.join(CUT,capn),knee)
    elbows={}
    for side in ("L","R"):
        upn,_,capn=ARM_PIECES[side]; sh=SHOULDER[side]
        limb(c,os.path.join(CUT,upn),sh,up[side],(76,30))
        elbows[side]=end_joint(sh,ARM_UPPER_LEN,up[side])
    paste_at(c,load(os.path.join(BASE,"Pelvis.png")),550,680)
    paste_at(c,load(os.path.join(BASE,"Cape_Collar.png")),550,370)
    paste_at(c,load(os.path.join(BASE,"Torso_Chest.png")),550,400)
    paste_at(c,load(os.path.join(BASE,"Belt_Overlay.png")),550,670)
    for side in ("L","R"):
        _,lown,capn=ARM_PIECES[side]
        limb(c,os.path.join(CUT,lown),elbows[side],low[side],(76,-30))
        cap_at(c,os.path.join(CUT,capn),elbows[side])
    paste_at(c,load(os.path.join(BASE,"Neck.png"),scale=1.05),550,360)
    paste_at(c,load(os.path.join(BASE,"Head_Front.png")),550,250)
    c.convert("RGB").save(os.path.join(OUT,name))
    print(name, "elbows", {k:(round(v[0]),round(v[1])) for k,v in elbows.items()})
    return elbows

# Variants: upper up-out, lower bent toward head in different amounts
build("flex-test-A-upper120-lower120.png",{"L":-120,"R":120},{"L":-120,"R":120})
build("flex-test-B-upper120-lower160.png",{"L":-120,"R":120},{"L":-160,"R":160})
build("flex-test-C-upper140-lower160.png",{"L":-140,"R":140},{"L":-160,"R":160})
build("flex-test-D-upper70-lower160.png",{"L":-70,"R":70},{"L":-160,"R":160})
build("flex-test-E-upper140-lower100.png",{"L":-140,"R":140},{"L":-100,"R":100})
