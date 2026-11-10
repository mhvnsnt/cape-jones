"""Knee-feet CORRECTION rebuild (Mars, 2026-10-31 16:58 CDT).
CORRECTION to dance-kneefeet-fix-20261031: that fix used a BLOCK range
FootIn ON for frames 15-55. That was wrong in both directions.
Mars's rule is BIDIRECTIONAL:
  knees OUTWARD -> feet OUTWARD (original lowers)
  knees INWARD  -> feet INWARD  (FootIn mirrored lowers)
Per-frame rule used here, NO block range:
  FootIn = True  iff  leg_upper L > 0 AND leg_upper R < 0
  (both thighs angled toward the midline = both kneecaps inward)
  otherwise False (original lowers, feet outward/straight).
This is the thigh-angle sign, not knee-x vs hip-x: at rest the thigh
piece already sits slightly inboard of the hip, so x-offset alone
misreads straight legs as inward. The angle sign is the kneecap
direction Mars is judging by eye.
Segment endpoints are the same rig/config as fix_dance.py; only the
footin decision changes, per rendered frame.
"""
import os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/dance-kneefeet-fix-20261031"))
# Import builder pieces by exec-ing fix_dance up to the segment loop is messy;
# instead duplicate the builder here with the per-frame rule (self-contained).
from PIL import Image, ImageDraw
import math
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
FLEX="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c-flex-out"
FIX="/home/hatch/workspace/cape-jones-rig/dance-arm-snap-20261031"
# ARM-FRONT-SNAP: see ARM-FRONT-SNAP-RULE.md. Snap = whole arm chain
# (upper + lower + elbow cap) moved above torso/pecs, ONLY on frames
# where that side's forearm alpha overlaps the torso alpha by >1000 px
# at 1100x1500 (measured gate; out-to-side frames measure 0-268 px,
# crossed frames measure 1500-9000 px). Upper arm is the piece that
# was being eaten: it was drawn BEFORE the torso while the forearm
# was drawn AFTER it, so a crossed arm read as detached at the pec line.
OUT=os.path.join(FIX,"frames"); PIECES="/home/hatch/workspace/cape-jones-rig/dance-kneefeet-fix-correction-20261031/pieces"
SCALE=0.95
SHOULDER={"L":(430,445),"R":(670,445)}; HIP={"L":(470,740),"R":(615,740)}
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
FOOTIN={"L":("Leg_Front_Lower_FootIn.png",59),"R":("Leg_Back_Lower_FootIn.png",127)}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
FLEX_PIECES={"L":"Arm_Front_Lower_FlexOut.png","R":"Arm_Back_Lower_FlexOut.png"}
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
def _limb_layer(path, joint, angle, anchor, scale=SCALE):
    im=load(path); ax,ay=anchor[0]*scale,anchor[1]*scale
    layer=Image.new("RGBA",(1100,1500),(0,0,0,0)); layer.paste(im,(int(joint[0]-ax),int(joint[1]-ay)),im)
    return layer.rotate(angle, center=joint, expand=False)
import numpy as np
_TORSO_MASK=None
def _torso_alpha():
    global _TORSO_MASK
    if _TORSO_MASK is None:
        t=load(os.path.join(BASE,"Torso_Chest.png"))
        m=Image.new("RGBA",(1100,1500),(0,0,0,0)); m.paste(t,(int(550-t.size[0]/2),400),t)
        _TORSO_MASK=(np.array(m.split()[3])>0)
    return _TORSO_MASK
def snap_for(cfg, elbows):
    """Per-side snap decision, measured not guessed: render that side's
    forearm alone, count alpha overlap with the torso alpha mask."""
    ta=_torso_alpha(); out={}
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        path = os.path.join(FLEX, FLEX_PIECES[side]) if cfg.get("flexout",{}).get(side) else os.path.join(CUT,low)
        lay=_limb_layer(path, elbows[side], cfg["arm_lower"][side], (ball[0],0))
        ov=int(((np.array(lay.split()[3])>0)&ta).sum())
        out[side]=(ov>1000, ov)
    return out
def build(cfg):
    canvas=Image.new("RGBA",(1100,1500),(0,0,0,0))
    paste_at(canvas, load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
    for side in ("L","R"):
        hip=HIP[side]; ball, hip_anchor = LEG[side]
        vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up,low,cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        if cfg.get("footin"):
            fpath, fball = FOOTIN[side]
            limb(canvas, os.path.join(PIECES,fpath), knee, cfg["leg_lower"][side], (fball,0))
        else:
            limb(canvas, os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0))
        cap_at(canvas, os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        ball, sh_anchor = ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        up,_,_ = ARM_PIECES[side]; sh=SHOULDER[side]
        limb(canvas, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    # SNAP DECISION (measured, before torso is pasted): the original order
    # draws upper arms BEFORE the torso, so a crossed arm's upper segment
    # is hidden behind the chest while its forearm (drawn after) is not.
    # Snap sides are re-drawn whole, above the torso, in the post-torso pass.
    snap=snap_for(cfg, elbows)
    # NOTE: upper arms were just drawn for both sides; for snap sides we
    # must undo that by rebuilding without them. Cheapest correct route:
    # rebuild the canvas from scratch when any snap is on (rare frames).
    if any(v[0] for v in snap.values()):
        canvas=Image.new("RGBA",(1100,1500),(0,0,0,0))
        paste_at(canvas, load(os.path.join(BASE,"Cape_Back_Main.png")),550,410)
        for side in ("L","R"):
            hip=HIP[side]; ball, hip_anchor = LEG[side]
            vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
            up,low,cap = LEG_PIECES[side]
            limb(canvas, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
            knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
            if cfg.get("footin"):
                fpath, fball = FOOTIN[side]
                limb(canvas, os.path.join(PIECES,fpath), knee, cfg["leg_lower"][side], (fball,0))
            else:
                limb(canvas, os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0))
            cap_at(canvas, os.path.join(CUT,cap), knee)
        for side in ("L","R"):
            if snap[side][0]: continue
            ball, sh_anchor = ARM[side]; up,_,_ = ARM_PIECES[side]; sh=SHOULDER[side]
            limb(canvas, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
    paste_at(canvas, load(os.path.join(BASE,"Pelvis.png")),550,680); paste_at(canvas, load(os.path.join(BASE,"Cape_Collar.png")),550,370)
    paste_at(canvas, load(os.path.join(BASE,"Torso_Chest.png")),550,400); paste_at(canvas, load(os.path.join(BASE,"Belt_Overlay.png")),550,670)
    for side in ("L","R"):
        _,low,cap = ARM_PIECES[side]; ball,_ = ARM[side]
        path = os.path.join(FLEX, FLEX_PIECES[side]) if cfg.get("flexout",{}).get(side) else os.path.join(CUT,low)
        if snap[side][0]:
            up,_,_ = ARM_PIECES[side]; ball2, sh_anchor = ARM[side]; sh=SHOULDER[side]
            limb(canvas, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        limb(canvas, path, elbows[side], cfg["arm_lower"][side], (ball[0],0))
        cap_at(canvas, os.path.join(CUT,cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE,"Neck.png"),scale=1.05),550,360); paste_at(canvas, load(os.path.join(BASE,"Head_Front.png")),550,250)
    out=Image.new("RGBA",(1100,1500),(0,0,0,0))
    out.alpha_composite(canvas,(int(cfg.get("dx",0)),int(cfg.get("bounce",0))))
    return out, snap
def lerp(a,b,t): return a+(b-a)*t
def interp_pose(pa,pb,t):
    cfg={"arm_upper":{},"arm_lower":{},"leg_upper":{},"leg_lower":{},"flexout":{},"bounce":0,"dx":0}
    for k in ("arm_upper","arm_lower","leg_upper","leg_lower"):
        for s in ("L","R"): cfg[k][s]=lerp(pa[k][s],pb[k][s],t)
    cfg["bounce"]=lerp(pa.get("bounce",0),pb.get("bounce",0),t); cfg["dx"]=lerp(pa.get("dx",0),pb.get("dx",0),t)
    cfg["flexout"]=pb.get("flexout",{}) if t>0.5 else pa.get("flexout",{})
    return cfg
P_STRIDE_A={"arm_upper":{"L":-35,"R":35},"arm_lower":{"L":-30,"R":30},"leg_upper":{"L":-25,"R":25},"leg_lower":{"L":20,"R":-20},"bounce":0,"dx":-20}
P_STRIDE_B={"arm_upper":{"L":35,"R":-35},"arm_lower":{"L":30,"R":-30},"leg_upper":{"L":25,"R":-25},"leg_lower":{"L":-20,"R":20},"bounce":-6,"dx":20}
P_GROOVE_A={"arm_upper":{"L":-60,"R":60},"arm_lower":{"L":-50,"R":50},"leg_upper":{"L":-15,"R":15},"leg_lower":{"L":30,"R":-30},"bounce":-14,"dx":0}
P_GROOVE_B={"arm_upper":{"L":-70,"R":70},"arm_lower":{"L":-40,"R":40},"leg_upper":{"L":15,"R":-15},"leg_lower":{"L":-30,"R":30},"bounce":-8,"dx":0}
P_KICK={"arm_upper":{"L":-45,"R":90},"arm_lower":{"L":-45,"R":90},"leg_upper":{"L":-50,"R":20},"leg_lower":{"L":30,"R":-25},"bounce":-4,"dx":10}
P_SPLIT={"arm_upper":{"L":-70,"R":70},"arm_lower":{"L":150,"R":-150},"leg_upper":{"L":-35,"R":35},"leg_lower":{"L":40,"R":-40},"bounce":-18,"dx":0,"flexout":{"L":True,"R":True}}
P_TWIST={"arm_upper":{"L":-90,"R":20},"arm_lower":{"L":120,"R":-60},"leg_upper":{"L":-20,"R":30},"leg_lower":{"L":30,"R":-20},"bounce":-10,"dx":-15,"flexout":{"L":True}}
P_ARMSUP={"arm_upper":{"L":-70,"R":70},"arm_lower":{"L":150,"R":-150},"leg_upper":{"L":-15,"R":15},"leg_lower":{"L":20,"R":-20},"bounce":-12,"dx":0,"flexout":{"L":True,"R":True}}
P_REST={"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":-10,"R":10},"bounce":0,"dx":0}
segments=[
 (1,15,P_STRIDE_A,P_STRIDE_B,2),
 (15,28,P_STRIDE_B,P_GROOVE_A,2),
 (28,42,P_GROOVE_A,P_GROOVE_B,2),
 (42,56,P_GROOVE_B,P_KICK,1),
 (56,69,P_KICK,P_SPLIT,2),
 (69,83,P_SPLIT,P_TWIST,2),
 (83,97,P_TWIST,P_ARMSUP,2),
 (97,110,P_ARMSUP,P_REST,2),
]
# Old v1 block decision for comparison
OLD_SEG_FOOTIN=[False,True,True,True,False,False,False,False]
frames={}; audit=[]
for si,(a,b,pa,pb,step) in enumerate(segments):
    n=max(1,(b-a)//step)
    for i in range(n+1):
        f=a+i*step
        if f>110 or f in frames: continue
        cfg=interp_pose(pa,pb,i/n if n else 0)
        # PER-FRAME bidirectional rule
        footin = cfg["leg_upper"]["L"]>0 and cfg["leg_upper"]["R"]<0
        cfg["footin"]=footin; frames[f]=cfg
        old=OLD_SEG_FOOTIN[si]
        knee = "INWARD" if footin else "OUTWARD"
        audit.append((f, round(cfg["leg_upper"]["L"],1), round(cfg["leg_upper"]["R"],1), knee, old, footin, old!=footin))
snap_audit=[]
for f in sorted(frames):
    _out=os.path.join(OUT,f"dance-arm-snap-f{f:03d}.png")
    if os.path.exists(_out):
        print(f"skip existing f{f:03d}"); continue
    im, snap = build(frames[f])
    snap_audit.append((f, snap["L"][0], snap["L"][1], snap["R"][0], snap["R"][1]))
    if 69<=f<=82:
        r,g,bl,al=im.split()
        r=r.point(lambda v: min(255,int(v*1.20))); g=g.point(lambda v: int(v*0.70)); bl=bl.point(lambda v: min(255,int(v*1.30)))
        im=Image.merge("RGBA",(r,g,bl,al))
    if f in (42,56,69,83):
        d=ImageDraw.Draw(im)
        for (x,y) in [(300,300),(800,300),(550,150)]:
            d.polygon([(x,y-22),(x+7,y-7),(x+22,y),(x+7,y+7),(x,y+22),(x-7,y+7),(x-22,y),(x-7,y-7)],fill=(255,220,80,220))
    im.save(_out)
print(f"frames rendered: {len(frames)}")
print("FootIn (corrected, per-frame):", sorted(f for f,c in frames.items() if c['footin']))
print("Changed vs v1 block:")
for row in audit:
    if row[6]: print(f"  f{row[0]:03d} Lupper={row[1]:+.1f} Rupper={row[2]:+.1f} knee={row[3]} oldFootIn={row[4]} newFootIn={row[5]}")
with open(os.path.join(FIX,"per-frame-audit-20261031.csv"),"w") as fh:
    fh.write("frame,leg_upper_L,leg_upper_R,knee_direction,old_v1_footin,new_footin,changed\n")
    for row in audit: fh.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}\n")

with open(os.path.join(FIX,"arm-snap-audit-20261031.csv"),"w") as fh:
    fh.write("frame,snap_L,overlap_L_px,snap_R,overlap_R_px\n")
    for f, sl, ol, sr, orr in snap_audit: fh.write(f"{f},{sl},{ol},{sr},{orr}\n")
print("SNAP frames (either side):", sorted(f for f,sl,ol,sr,orr in snap_audit if sl or sr))
print("SNAP L frames:", sorted(f for f,sl,ol,sr,orr in snap_audit if sl))
print("SNAP R frames:", sorted(f for f,sl,ol,sr,orr in snap_audit if sr))
print("Total side-snaps:", sum((1 if sl else 0)+(1 if sr else 0) for f,sl,ol,sr,orr in snap_audit))
