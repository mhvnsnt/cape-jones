"""v7b: vector pivot at ball centre. See v7 docstring for ball centres.
Upper vector = ball - shoulder/hip anchor, rotated by PIL matrix:
  (x,y) -> (x*cos + y*sin, -x*sin + y*cos)  [matches PIL rotate: (0,1)->(sin,cos)]
Lower anchor = ball centre in lower piece (whole crop from ball centre): (ball_x, 0)
Cap drawn at joint after lower, circle-masked, rotation-invariant ball.
"""
from PIL import Image
import os, math
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7"; OUT="/home/hatch/workspace/cape-jones-rig/reposes-v7"
SCALE=0.95
SHOULDER={"L":(430,445),"R":(670,445)}; HIP={"L":(470,740),"R":(615,740)}
# ball centres, upper anchors, lower anchors
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
def rot_vec(v, angle_deg):
    a=math.radians(angle_deg); x,y=v
    return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(name, cfg, arms_whole=False):
    canvas=Image.new("RGBA",(1100,1500),(128,128,128,255))
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
    if arms_whole:
        for side in ("L","R"):
            limb(canvas, os.path.join(BASE, "Arm_Front.png" if side=="L" else "Arm_Back.png"), SHOULDER[side], cfg["arm_upper"][side], (76,30))
    else:
        for side in ("L","R"):
            ball, sh_anchor = ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
            up,_,_ = ARM_PIECES[side]; sh=SHOULDER[side]
            limb(canvas, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
            elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(canvas, load(os.path.join(BASE,"Pelvis.png")),550,680); paste_at(canvas, load(os.path.join(BASE,"Cape_Collar.png")),550,370)
    paste_at(canvas, load(os.path.join(BASE,"Torso_Chest.png")),550,400); paste_at(canvas, load(os.path.join(BASE,"Belt_Overlay.png")),550,670)
    if not arms_whole:
        for side in ("L","R"):
            _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
            limb(canvas, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0))
            cap_at(canvas, os.path.join(CUT,cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE,"Neck.png"),scale=1.05),550,360); paste_at(canvas, load(os.path.join(BASE,"Head_Front.png")),550,250)
    from PIL import ImageDraw; d=ImageDraw.Draw(canvas)
    def label(x,y,t):
        d.ellipse((x-28,y-28,x+28,y+28),fill=(255,0,0,255),outline=(255,255,255,255),width=3); d.text((x-7,y-10),t,fill=(255,255,255,255))
    label(340,430,"1"); d.text((300,470),"ARM 1",fill=(255,0,0,255)); label(760,430,"2"); d.text((720,470),"ARM 2",fill=(255,0,0,255))
    label(400,820,"1"); d.text((360,860),"LEG 1",fill=(255,0,0,255)); label(700,820,"2"); d.text((660,860),"LEG 2",fill=(255,0,0,255))
    canvas.convert("RGB").save(os.path.join(OUT,name)); print(name)
build("joint-apose-v7-20261031.png", {"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}})
build("joint-flex-v7-20261031.png", {"arm_upper":{"L":-25,"R":25},"arm_lower":{"L":160,"R":-160},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}})
build("joint-punch-v7-20261031.png", {"arm_upper":{"L":-45,"R":90},"arm_lower":{"L":-45,"R":90},"leg_upper":{"L":-20,"R":20},"leg_lower":{"L":-20,"R":20}})
build("joint-jump-v7-20261031.png", {"arm_upper":{"L":-150,"R":150},"arm_lower":{"L":-150,"R":150},"leg_upper":{"L":-20,"R":20},"leg_lower":{"L":45,"R":-45}}, arms_whole=True)
build("joint-dance-v7-20261031.png", {"arm_upper":{"L":-60,"R":60},"arm_lower":{"L":-60,"R":60},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}})
build("joint-seated-v7-20261031.png", {"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-60,"R":60},"leg_lower":{"L":80,"R":-80}})
