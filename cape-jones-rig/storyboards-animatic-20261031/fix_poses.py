"""Fixes, saved as v2 files, v1 drafts kept untouched.
CJ-02 v2: wider 1400 canvas so extended fist is not clipped (no-crop).
CJ-27 v2: angry eye strip scaled to face width 95 (was 113), shout mouth 58 wide.
CJ-15 v2: foreshortened foreground fist+forearm over hover body, scale-up = toward camera."""
from PIL import Image
import os, math
RIG="/home/hatch/workspace/cape-jones-rig"
BASE=os.path.join(RIG,"sliced"); CUT=os.path.join(RIG,"cut-limbs-v7c")
OUT=os.path.join(RIG,"storyboards-animatic-20261031/poses")
SCALE=0.95
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def rot_vec(v, a_deg):
    a=math.radians(a_deg); x,y=v; return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(cfg, W=1100, CX=550, head=None, fore=False):
    SHOULDER={"L":(CX-120,445),"R":(CX+120,445)}; HIP={"L":(CX-80,740),"R":(CX+65,740)}
    ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
    LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
    LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
    ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
    canvas=Image.new("RGBA",(W,1500),(0,0,0,0))
    def paste_at(im, cx, top): canvas.paste(im,(int(cx-im.size[0]/2),int(top)),im)
    def limb(path, joint, angle, anchor):
        im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
        layer=Image.new("RGBA",(W,1500),(0,0,0,0)); layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
        canvas.alpha_composite(layer.rotate(angle, center=joint, expand=False))
    def cap_at(path, joint):
        im=load(path); canvas.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
    paste_at(load(os.path.join(BASE,"Cape_Back_Main.png")),CX,410)
    for side in ("L","R"):
        hip=HIP[side]; ball, hip_anchor = LEG[side]
        vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1]); up,low,cap = LEG_PIECES[side]
        limb(os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        limb(os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0)); cap_at(os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        ball, sh_anchor = ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        up,_,_ = ARM_PIECES[side]; sh=SHOULDER[side]
        limb(os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(load(os.path.join(BASE,"Pelvis.png")),CX,680); paste_at(load(os.path.join(BASE,"Cape_Collar.png")),CX,370)
    paste_at(load(os.path.join(BASE,"Torso_Chest.png")),CX,400); paste_at(load(os.path.join(BASE,"Belt_Overlay.png")),CX,670)
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        limb(os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(os.path.join(CUT,cap), elbows[side])
    paste_at(load(os.path.join(BASE,"Neck.png"),scale=1.05),CX,360); paste_at(load(os.path.join(BASE,"Head_Front.png")),CX,250)
    if head=="shout_angry":
        eyes=Image.open(os.path.join(BASE,"Eyes_AngryStrip.png")).convert("RGBA").resize((95, int(84*95/213)), Image.LANCZOS)
        canvas.paste(eyes,(CX-95//2, 295), eyes)
        mouth=Image.open(os.path.join(BASE,"Mouth_Shout.png")).convert("RGBA").resize((58, int(80*58/89)), Image.LANCZOS)
        canvas.paste(mouth,(CX-29, 352), mouth)
    if fore:
        # Foreground foreshortened arm: large fist toward camera over chest, forearm behind it.
        # Pieces only, no recolour. Fist scaled 2.4x, forearm (front lower) 1.7x rotated to point at viewer.
        fore_im=load(os.path.join(CUT,"Arm_Front_Lower.png"), scale=SCALE*1.7)
        layer=Image.new("RGBA",(W,1500),(0,0,0,0)); layer.paste(fore_im,(int(CX-40-fore_im.size[0]/2), 560), fore_im)
        canvas.alpha_composite(layer.rotate(-35, center=(CX+30,640), expand=False))
        fist=Image.open(os.path.join(BASE,"Hand_1_Fist.png")).convert("RGBA")
        fist=fist.resize((int(fist.size[0]*SCALE*2.4), int(fist.size[1]*SCALE*2.4)), Image.LANCZOS)
        canvas.paste(fist,(CX+10, 520), fist)
    bbox=canvas.getchannel("A").getbbox(); assert bbox
    x0=max(0,bbox[0]-20); y0=max(0,bbox[1]-20); x1=min(W,bbox[2]+20); y1=min(1500,bbox[3]+20)
    return canvas.crop((x0,y0,x1,y1)), bbox

def save(name, img, bbox): img.save(os.path.join(OUT,name)); print(name, img.size, bbox)
img,b=build({"arm_upper":{"L":-90,"R":20},"arm_lower":{"L":-90,"R":160},"leg_upper":{"L":-15,"R":15},"leg_lower":{"L":15,"R":-15}}, W=1400, CX=700)
save("CJ-02-punch-extend-snap-pose-20261031-v2.png", img, b)
img,b=build({"arm_upper":{"L":-35,"R":35},"arm_lower":{"L":-35,"R":35},"leg_upper":{"L":-12,"R":12},"leg_lower":{"L":10,"R":-10}}, head="shout_angry")
save("CJ-27-dialogue-shout-angry-pose-20261031-v2.png", img, b)
img,b=build({"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-5,"R":5},"leg_lower":{"L":5,"R":-5}}, fore=True)
save("CJ-15-flying-forward-foreshortened-pose-20261031-v2.png", img, b)
