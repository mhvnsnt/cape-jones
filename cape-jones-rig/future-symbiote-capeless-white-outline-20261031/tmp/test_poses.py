import sys, os
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/future-symbiote-capeless-white-outline-20261031'))
# import builder logic by copying v7c functions
from PIL import Image
import math
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
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
def rot_vec(v, angle_deg):
    a=math.radians(angle_deg); x,y=v
    return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(cfg, cape=True, out="/tmp/test.png"):
    canvas=Image.new("RGBA",(1100,1500),(0,0,0,0))
    if cape: paste_at(canvas, load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
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
    paste_at(canvas, load(os.path.join(BASE,"Pelvis.png")),550,680)
    if cape: paste_at(canvas, load(os.path.join(BASE,"Cape_Collar.png")),550,370)
    paste_at(canvas, load(os.path.join(BASE,"Torso_Chest.png")),550,400); paste_at(canvas, load(os.path.join(BASE,"Belt_Overlay.png")),550,670)
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        limb(canvas, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0))
        cap_at(canvas, os.path.join(CUT,cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE,"Neck.png"),scale=1.05),550,360); paste_at(canvas, load(os.path.join(BASE,"Head_Front.png")),550,250)
    canvas.save(out); print(out, canvas.split()[-1].getbbox())
    return canvas

cfgs={
 "cross_L80_R-80": {"arm_upper":{"L":80,"R":-80},"arm_lower":{"L":80,"R":-80},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}},
 "cross_L60_R-60_low40": {"arm_upper":{"L":60,"R":-60},"arm_lower":{"L":40,"R":-40},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}},
 "cross_L120_R-120": {"arm_upper":{"L":120,"R":-120},"arm_lower":{"L":120,"R":-120},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}},
 "cross_L40_R-40_low120": {"arm_upper":{"L":40,"R":-40},"arm_lower":{"L":120,"R":-120},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10}},
}
from PIL import ImageDraw
for name,cfg in cfgs.items():
    build(cfg, cape=False, out=f"/home/hatch/workspace/cape-jones-rig/future-symbiote-capeless-white-outline-20261031/tmp/{name}.png")
# contact on grey
tiles=[]
for name in cfgs:
    im=Image.open(f"/home/hatch/workspace/cape-jones-rig/future-symbiote-capeless-white-outline-20261031/tmp/{name}.png")
    bg=Image.new("RGBA",(550,750),(128,128,128,255)); bg.alpha_composite(im.resize((275,375)))
    tiles.append((name,bg))
sheet=Image.new("RGBA",(1100,750),(0,0,0,255))
d=ImageDraw.Draw(sheet)
for i,(name,t) in enumerate(tiles):
    x=(i%4)*275; sheet.alpha_composite(t,(x,0)); d.text((x+4,380),name,fill=(255,255,0))
sheet.convert("RGB").save("/home/hatch/workspace/cape-jones-rig/future-symbiote-capeless-white-outline-20261031/tmp/test_poses_contact.png")
print("done")
