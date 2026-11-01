"""Storyboard poses 9/9 pending, transparent v7c rig build, labels=False.
Copies joint_locked_rig_v7c geometry; canvas transparent (not grey) so panels
can composite without recolouring base art. No pixel recoloured: pieces pasted
as-is, rotations only. No-crop: pose canvas stays 1100x1500, trimmed only to
alpha bbox + margin at panel stage, never clipped inside the pose."""
from PIL import Image
import os, math, json
RIG="/home/hatch/workspace/cape-jones-rig"
BASE=os.path.join(RIG,"sliced"); CUT=os.path.join(RIG,"cut-limbs-v7c")
OUT=os.path.join(RIG,"storyboards-animatic-20261031/poses")
os.makedirs(OUT, exist_ok=True)
SCALE=0.95
SHOULDER={"L":(430,445),"R":(670,445)}; HIP={"L":(470,740),"R":(615,740)}
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
def load(p, scale=SCALE):
    im=Image.open(p).convert("RGBA"); return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.paste(im,(int(cx-im.size[0]/2),int(top)),im)
def limb(c, path, joint, angle, anchor):
    im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
    layer=Image.new("RGBA",(1100,1500),(0,0,0,0)); layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
    layer=layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im=load(path); c.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
def rot_vec(v, a_deg):
    a=math.radians(a_deg); x,y=v; return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(name, cfg, head="normal"):
    canvas=Image.new("RGBA",(1100,1500),(0,0,0,0))
    paste_at(canvas, load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
    for side in ("L","R"):
        hip=HIP[side]; ball, hip_anchor = LEG[side]
        vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up,low,cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
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
        limb(canvas, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0))
        cap_at(canvas, os.path.join(CUT,cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE,"Neck.png"),scale=1.05),550,360)
    paste_at(canvas, load(os.path.join(BASE,"Head_Front.png")),550,250)
    if head=="shout_angry":
        # Head_Front bbox in canvas: x 494-606, y 250-413 (113x163 at 0.95).
        # Overlay only: angry eye strip scaled to head width, shout mouth over neutral mouth. No base recoloured.
        eyes=Image.open(os.path.join(BASE,"Eyes_AngryStrip.png")).convert("RGBA")
        eyes=eyes.resize((113, int(84*113/213)), Image.LANCZOS)
        canvas.paste(eyes,(550-113//2, 292), eyes)
        mouth=Image.open(os.path.join(BASE,"Mouth_Shout.png")).convert("RGBA")
        mouth=mouth.resize((70, int(80*70/89)), Image.LANCZOS)
        canvas.paste(mouth,(550-35, 348), mouth)
    # trim to alpha bbox + 20px margin, never crop inside alpha
    bbox=canvas.getchannel("A").getbbox()
    assert bbox, name
    x0=max(0,bbox[0]-20); y0=max(0,bbox[1]-20); x1=min(1100,bbox[2]+20); y1=min(1500,bbox[3]+20)
    out=canvas.crop((x0,y0,x1,y1))
    out.save(os.path.join(OUT,name))
    print(name, out.size, "alpha_bbox", bbox)
    return out, bbox

POSES={
 "CJ-01-punch-windup-pose-20261031.png": ({"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-120,"R":160},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":10,"R":-10}}, "normal"),
 "CJ-02-punch-extend-snap-pose-20261031.png": ({"arm_upper":{"L":-90,"R":20},"arm_lower":{"L":-90,"R":160},"leg_upper":{"L":-15,"R":15},"leg_lower":{"L":15,"R":-15}}, "normal"),
 "CJ-04-punch-recover-pose-20261031.png": ({"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":10,"R":-10}}, "normal"),
 "CJ-11-dance-combined-finale-pose-20261031.png": ({"arm_upper":{"L":-150,"R":150},"arm_lower":{"L":-150,"R":150},"leg_upper":{"L":-20,"R":10},"leg_lower":{"L":20,"R":-10}}, "normal"),
 "CJ-15-flying-forward-foreshortened-pose-20261031.png": ({"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-5,"R":5},"leg_lower":{"L":5,"R":-5}}, "normal"),
 "CJ-17-arms-up-reference-pose-20261031.png": ({"arm_upper":{"L":-135,"R":135},"arm_lower":{"L":-135,"R":135},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":10,"R":-10}}, "normal"),
 "CJ-18-true-flex-double-bicep-pose-20261031.png": ({"arm_upper":{"L":-25,"R":25},"arm_lower":{"L":160,"R":-160},"leg_upper":{"L":-18,"R":18},"leg_lower":{"L":5,"R":-5}}, "normal"),
 "CJ-20-fighting-stance-arms-up-high-pose-20261031.png": ({"arm_upper":{"L":-150,"R":150},"arm_lower":{"L":-150,"R":150},"leg_upper":{"L":-30,"R":30},"leg_lower":{"L":10,"R":-10}}, "normal"),
 "CJ-27-dialogue-shout-angry-pose-20261031.png": ({"arm_upper":{"L":-35,"R":35},"arm_lower":{"L":-35,"R":35},"leg_upper":{"L":-12,"R":12},"leg_lower":{"L":10,"R":-10}}, "shout_angry"),
}
meta={}
for name,(cfg,head) in POSES.items():
    out,bbox=build(name,cfg,head); meta[name]={"size":out.size,"alpha_bbox_canvas":bbox,"cfg":cfg,"head":head}
json.dump(meta, open(os.path.join(OUT,"poses-20261031.json"),"w"), indent=1)
print("done", len(meta))
