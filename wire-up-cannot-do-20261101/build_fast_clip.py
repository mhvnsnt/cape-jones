"""48-frame 2D rig clip, joint-cut arms, arm-front-snap, true arms-up flex.
Own code, Cape Jones pieces only. No Toon Boom code, no wrist cut, no square crop.
Joint cut = elbow ball centre pivot, standard v7 cut (cut-limbs-v7), upper/lower
pieces are the original art split at the joint ball, cap circle-masked on the seam.
Knee-feet universal rule (Mars 2026-11-01 12:07): knees direction == toes
direction, both legs, per frame. Legs here are straight, toes as drawn, no turn.
Timeline @24fps, 48f = 2.0s:
 f1-8 rest, f9-20 arms out, f21-32 arms crossed chest (SNAP: whole arm chain
 above torso, below head), f33-48 arms-up flex (upper 120, lower 160,
 spread 120deg, fists upright above elbows).
"""
import os, math, time, json
from PIL import Image
BASE="/home/hatch/workspace/cape-jones-rig/sliced"
CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7"
OUT="/home/hatch/workspace/cape-jones-rig/wire-up-cannot-do-20261101/renders/pil48"
os.makedirs(OUT, exist_ok=True)
SCALE=0.95
SHOULDER={"L":(430,445),"R":(670,445)}
HIP={"L":(470,740),"R":(615,740)}
ARM_UPPER_LEN=192*SCALE; LEG_UPPER_LEN=274*SCALE
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png",(77,40),(77,14)),
            "R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png",(84,40),(84,14))}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),
            "R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
_CACHE={}
def load(p,scale=SCALE):
    if p not in _CACHE:
        im=Image.open(p).convert("RGBA")
        _CACHE[p]=im.resize((int(im.size[0]*scale),int(im.size[1]*scale)),Image.LANCZOS)
    return _CACHE[p]
def paste_at(c,im,cx,top):
    c.paste(im,(int(cx-im.size[0]/2),int(top)),im)
def limb(c,piece,joint,angle,anchor):
    # Fast: rotate a small layer around the joint anchor, not a full 1100x1500 canvas.
    im=load(piece); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
    w,h=im.size
    layer=Image.new("RGBA",(w*2,h*2),(0,0,0,0))
    layer.paste(im,(int(w-ax),int(h-ay)),im)
    layer=layer.rotate(angle,center=(w,h),expand=False)
    c.alpha_composite(layer,(int(joint[0]-w),int(joint[1]-h)))
def cap_at(c,cap,joint):
    im=load(cap); c.paste(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)),im)
def end_joint(joint,length,angle):
    a=math.radians(angle); return (joint[0]+length*math.sin(a),joint[1]+length*math.cos(a))
def lerp(a,b,t): return a+(b-a)*t
# keys: (frame, upperL, upperR, lowerL, lowerR, snap)
KEYS=[(1,-20,20,-20,20,False),(8,-20,20,-20,20,False),
      (20,-70,70,-70,70,False),
      (32,-20,20,90,-90,True),   # crossed-down: upper at sides, forearm horizontal across chest (PIL check: L +90 = east, R -90 = west), snap ON
      (48,-120,120,-160,160,False)]  # arms-up flex, spread 120
def pose_at(f):
    for i in range(len(KEYS)-1):
        f0, *v0 = KEYS[i]; f1, *v1 = KEYS[i+1]
        if f0 <= f <= f1:
            t=0 if f1==f0 else (f-f0)/(f1-f0)
            # smoothstep
            t=t*t*(3-2*t)
            vals=[lerp(a,b,t) for a,b in zip(v0[:4],v1[:4])]
            snap=v1[4] if t>=0.5 else v0[4]
            return vals, snap
    vals=list(KEYS[-1][1:5]); return vals, KEYS[-1][5]
def build_frame(f):
    (upL,upR,lowL,lowR), snap = pose_at(f)
    up={"L":upL,"R":upR}; low={"L":lowL,"R":lowR}
    c=Image.new("RGBA",(1100,1500),(200,200,195,255))
    paste_at(c,load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
    knees={}
    for side in ("L","R"):
        hip=HIP[side]; upn,lown,capn,hipa,kneea=LEG_PIECES[side]
        limb(c,os.path.join(CUT,upn),hip,-10 if side=="L" else 10,hipa)
        knee=end_joint(hip,LEG_UPPER_LEN,-10 if side=="L" else 10); knees[side]=knee
        limb(c,os.path.join(CUT,lown),knee,-10 if side=="L" else 10,kneea)
        cap_at(c,os.path.join(CUT,capn),knee)
    elbows={}
    def draw_arms():
        for side in ("L","R"):
            upn,_,capn=ARM_PIECES[side]; sh=SHOULDER[side]
            limb(c,os.path.join(CUT,upn),sh,up[side],(76,30))
            elbows[side]=end_joint(sh,ARM_UPPER_LEN,up[side])
        # forearms + caps are drawn by caller in snap order; here only uppers
    # Compute elbows first without drawing? draw uppers now, forearms after torso in both cases,
    # but for snap, uppers must ALSO be after torso. So: if snap, defer uppers.
    if snap:
        paste_at(c,load(os.path.join(BASE,"Pelvis.png")),550,680)
        paste_at(c,load(os.path.join(BASE,"Cape_Collar.png")),550,370)
        paste_at(c,load(os.path.join(BASE,"Torso_Chest.png")),550,400)
        paste_at(c,load(os.path.join(BASE,"Belt_Overlay.png")),550,670)
        for side in ("L","R"):
            upn,_,capn=ARM_PIECES[side]; sh=SHOULDER[side]
            limb(c,os.path.join(CUT,upn),sh,up[side],(76,30))
            elbows[side]=end_joint(sh,ARM_UPPER_LEN,up[side])
        for side in ("L","R"):
            _,lown,capn=ARM_PIECES[side]
            limb(c,os.path.join(CUT,lown),elbows[side],low[side],(76,-30))
            cap_at(c,os.path.join(CUT,capn),elbows[side])
    else:
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
    return c, {"frame":f,"upper":up,"lower":low,"snap":snap,"elbows":{k:(round(v[0]),round(v[1])) for k,v in elbows.items()}}
t0=time.time(); table=[]
for f in range(1,49):
    c,info=build_frame(f); table.append(info)
    c.convert("RGB").save(os.path.join(OUT,f"frame_{f:03d}.png"))
t1=time.time()
with open(os.path.join(OUT,"pose-table.json"),"w") as fh: json.dump({"fps":24,"frames":table,"render_s":round(t1-t0,2),"per_frame_s":round((t1-t0)/48,4)},fh,indent=1)
print(f"PIL48_DONE frames=48 total_s={t1-t0:.2f} per_frame_s={(t1-t0)/48:.4f}")
