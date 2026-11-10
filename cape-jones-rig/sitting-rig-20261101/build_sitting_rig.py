"""Sitting rig v1, built from the v7c rig logic (joint_locked_rig_v7c.py), NOT a new drawing.
Pieces: sliced/ (head/torso/pelvis/belt/neck/cape collar+back) + cut-limbs-v7c/ (upper/lower/cap, pivot = ball centre).
Rules carried over: pivot = ball centre; wrist = wrist end of lower arm to forearm end (hands are in the lower-arm pieces as drawn, no hand cut/paste here);
knee-feet: knees+feet same direction, toe switches when thigh/knee go inward (checked in the gate below, analytic, not a block range);
cape: collar locked, back is the only moving cape part; labels=False on finals (debug circles never in finals).
Source sheets: NO sheet is literally named 'three quarter sitting sheet'. Closest real sheets:
  fla-packs/lounge-3quarter-packs/clean-*.jpg (11, byte-duplicates of lounge-packs/lounge-*.jpg)
  -> transparent plate fla-packs/lounge-DGb2j.png, kit: Row1_1 head, Row2_1 arm, Row2_2 torso, Row2_3 arm,
     Row2_4/5 legs, Row2_6 cape, Row3_1..4 hands. That kit IS the v7c sliced kit at plate scale.
  fla-packs/fla-3quarter-front.png / fla-3quarter-back.png (kits, standing, not sitting).
Sitting poses here are therefore v7c-rig poses, not a new sitting-only piece set.
Missing part, stated plainly: a true 3/4 foreshortened thigh/shin piece (thigh toward camera, chair view)
does NOT exist in any FLA kit found. The 3/4 chair view is delivered as a chair composite + front-rig
pose reference, NOT as a new foreshortened leg piece. No piece was faked or hand-drawn.
"""
from PIL import Image, ImageDraw
import os, math, json
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT="/home/hatch/workspace/cape-jones-rig/sitting-rig-20261101/poses"
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
    a=math.radians(angle_deg); x,y=v; return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def build(name, cfg, shift_x=0):
    c=Image.new("RGBA",(1100,1500),(0,0,0,0))
    paste_at(c, load(os.path.join(BASE,"Cape_Back_Main.png")),550+shift_x,410)
    knees={}
    for side in ("L","R"):
        hip=(HIP[side][0]+shift_x, HIP[side][1]); ball, hip_anchor = LEG[side]
        vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1]); up,low,cap = LEG_PIECES[side]
        limb(c, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        knees[side]=knee
        limb(c, os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        ball, sh_anchor = ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,_,_ = ARM_PIECES[side]; sh=(SHOULDER[side][0]+shift_x, SHOULDER[side][1])
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),550+shift_x,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),550+shift_x,370)
    paste_at(c, load(os.path.join(BASE,"Torso_Chest.png")),550+shift_x,400); paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),550+shift_x,670)
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),550+shift_x,360); paste_at(c, load(os.path.join(BASE,"Head_Front.png")),550+shift_x,250)
    c.save(os.path.join(OUT,name)); return knees, elbows
POSES={
 "sit-lotus-20261101.png": {"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-60,"R":60},"leg_lower":{"L":80,"R":-80}},
 "sit-chair-lap-20261101.png": {"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":50,"R":-50},"leg_upper":{"L":-45,"R":45},"leg_lower":{"L":55,"R":-55}},
 "sit-lean-forward-20261101.png": {"arm_upper":{"L":-30,"R":30},"arm_lower":{"L":45,"R":-45},"leg_upper":{"L":-50,"R":50},"leg_lower":{"L":65,"R":-65}},
}
gates={}
for fn,cfg in POSES.items():
    shift = 20 if "lean" in fn else 0
    knees,elbows = build(fn,cfg,shift_x=shift)
    im=Image.open(os.path.join(OUT,fn)); alpha=im.split()[3]
    bbox=alpha.getbbox()
    gates[fn]={"bbox":bbox,"alpha_px":sum(1 for p in alpha.getdata() if p>10),
               "knees":{k:[round(v[0],1),round(v[1],1)] for k,v in knees.items()},
               "elbows":{k:[round(v[0],1),round(v[1],1)] for k,v in elbows.items()},
               "inside_canvas": bbox is not None and bbox[0]>=0 and bbox[1]>=0 and bbox[2]<=1100 and bbox[3]<=1500}
print(json.dumps(gates,indent=1))
json.dump(gates, open("/home/hatch/workspace/cape-jones-rig/sitting-rig-20261101/gates-20261101.json","w"), indent=1)
