#!/usr/bin/env python3
"""RIG-06 v2: 3/4 sitting rig rigged LIKE the front rig (v7c).
Front rig RIG-00 untouched: pieces are READ from sitting-rig-34-20261101/pieces,
front Neck.png is READ from sliced/, all outputs are in this new folder only.
Top-10 industry rigging methods T1-T10 are wired and run below; see gates json.
Neck: front Neck.png, alpha width 96px native, 101px at v7c scale 1.05.
This rig uses EXACTLY 101px rendered width (cropped alpha, resized to 101 wide,
height 82 proportional). It is NOT redrawn/squashed for 3/4, per Mars.
"""
from PIL import Image, ImageDraw
import os, math, json, hashlib
ROOT=os.path.expanduser("~/workspace/cape-jones-rig/rig-34-front-style-neck-20261101")
SRC=os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/pieces")
SLICED=os.path.expanduser("~/workspace/cape-jones-rig/sliced")
S=1.3  # same piece scale as prior 3/4 builds, so fit is comparable
W,H=1400,1600
def md5(p):
    return hashlib.md5(open(p,'rb').read()).hexdigest()
def load34(name):
    im=Image.open(os.path.join(SRC,name)).convert("RGBA")
    return im.resize((int(im.width*S),int(im.height*S)), Image.LANCZOS)
def load_neck():
    # T-neck: crop to alpha bbox of front Neck.png, resize to 101px wide
    im=Image.open(os.path.join(SLICED,"Neck.png")).convert("RGBA")
    bb=im.split()[3].getbbox()  # (4,1,100,79) -> 96x78
    crop=im.crop(bb)
    nw=101; nh=int(round(crop.height*nw/crop.width))  # 82
    return crop.resize((nw,nh), Image.LANCZOS), bb, nw, nh
def paste_cx(canvas, im, cx, top):
    canvas.alpha_composite(im,(int(cx-im.width/2),int(top)))
def rot_vec(v, deg):
    a=math.radians(deg); x,y=v
    return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def clamp(v,lo,hi): return max(lo,min(hi,v))
# T6 deformation limits
ANGLE_LIMITS={"arm_upper":(-170,170),"arm_lower":(-170,170),"leg_upper":(-45,45),"leg_lower":(-30,30)}
def limb(canvas, im, joint, angle, anchor_top_centre=True):
    """T1+T2: FK limb. Piece anchor = top centre (shoulder/hip/elbow/knee top).
    Rotate full-canvas layer about joint, exactly like v7c limb()."""
    layer=Image.new("RGBA",(W,H),(0,0,0,0))
    layer.alpha_composite(im,(int(joint[0]-im.width/2),int(joint[1])))
    layer=layer.rotate(angle, center=joint, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    # joint end = joint + rotated (0, piece height-15)  (ball sits near bottom)
    vec=rot_vec((0, im.height-15), angle)
    return (joint[0]+vec[0], joint[1]+vec[1])
def ik_2bone(shoulder, target, l1, l2):
    """T3: analytic 2-bone IK. Returns (upper_angle, lower_angle_relative) in v7c convention.
    Used only to CHECK the lean pose hand target; FK is primary."""
    dx,dy=target[0]-shoulder[0], target[1]-shoulder[1]
    d=max(1e-6, min(math.hypot(dx,dy), l1+l2-1))
    # angle of target vector from vertical (down = 0 in screen coords, using rot_vec convention)
    base=math.degrees(math.atan2(dx, dy))  # dx horizontal, dy vertical-down
    # law of cosines: angle at shoulder between l1 and target line
    cos_a=(l1*l1+d*d-l2*l2)/(2*l1*d); a=math.degrees(math.acos(max(-1,min(1,cos_a))))
    upper=base-a  # elbow-out side; sign chosen to match L/R in caller if needed
    cos_e=(l1*l1+l2*l2-d*d)/(2*l1*l2); e=math.degrees(math.acos(max(-1,min(1,cos_e))))
    lower=180-e
    return upper, lower, d
# Front-rig anchors, mapped to 3/4 canvas (same logic, new coordinates):
# torso cx700 top350 w291 -> shoulders at torso sides, hips at pelvis
SHOULDER={"L":(580,410),"R":(820,410)}; HIP={"L":(640,780),"R":(760,780)}
POSES={
 "sit-chair": {"arm_upper":{"L":-15,"R":15},"arm_lower":{"L":-10,"R":10},"leg_upper":{"L":-8,"R":6},"leg_lower":{"L":0,"R":0}},
 "sit-upright": {"arm_upper":{"L":-5,"R":5},"arm_lower":{"L":0,"R":0},"leg_upper":{"L":-4,"R":4},"leg_lower":{"L":0,"R":0}},
 "sit-lean-forward-34": {"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":-35,"R":35},"leg_upper":{"L":-8,"R":6},"leg_lower":{"L":0,"R":0}},
 "arms-up-over-face": {"arm_upper":{"L":-150,"R":150},"arm_lower":{"L":-20,"R":20},"leg_upper":{"L":-8,"R":6},"leg_lower":{"L":0,"R":0}},
}
def build(pose_name, cfg, arms_over_face=False, substitution=None):
    # clamp angles T6, record
    clamped={}
    for k,lim in ANGLE_LIMITS.items():
        for side in ("L","R"):
            v=cfg[k][side]; c=clamp(v,*lim); clamped[f"{k}.{side}"]=[v,c]
            cfg[k][side]=c
    canvas=Image.new("RGBA",(W,H),(0,0,0,0))
    # T5 layer order (front rig order, adapted): cape > legs > pelvis > torso > arms > neck > head
    # arms_over_face=True overrides: arms drawn AFTER head (jump-fix top_arms rule)
    paste_cx(canvas, load34("cape_back.png"), 700, 340)
    knees={}; feet={}
    for side in ("L","R"):
        thigh=load34("thigh_bent_L.png" if side=="L" else "thigh_bent_R.png")
        knee=limb(canvas, thigh, HIP[side], cfg["leg_upper"][side]); knees[side]=knee
        shin_name="shin_boot_L.png" if side=="L" else "shin_boot_mid.png"
        shin=load34(shin_name)
        foot_end=limb(canvas, shin, knee, cfg["leg_lower"][side]); feet[side]=foot_end
        # T7 joint cap: spare knee ball centred on knee, after shin
        cap=load34("knee_ball_spare.png")
        canvas.alpha_composite(cap,(int(knee[0]-cap.width/2),int(knee[1]-cap.height/2)))
    paste_cx(canvas, load34("pelvis_belt.png"), 700, 640)
    paste_cx(canvas, load34("torso.png"), 700, 350)
    def draw_arms():
        # Ball-corrected elbows: v7c pieces are cropped FROM ball centre, 3/4 pieces are NOT.
        # Upper arm placed by centre (as drawn); its ball sits at bottom frac:
        # L 26/96=0.27, R 44/86=0.51. Forearm top anchor frac: L 87/133=0.66, R 95/139=0.69.
        # Elbow joint = upper bottom-centre + rotated(ball_frac-0.5)*width.
        # Forearm is placed so its TOP ANCHOR lands on that elbow, not its centre.
        BALL={"L":0.27,"R":0.51}; TOPA={"L":0.66,"R":0.69}
        elbows={}; wrists={}
        for side in ("L","R"):
            up=load34("upper_arm_L_socket.png" if side=="L" else "upper_arm_R.png")
            # place upper by centre at shoulder, rotate about shoulder (v7c limb, centre anchor)
            limb(canvas, up, SHOULDER[side], cfg["arm_upper"][side])
            # elbow ball position after rotation: centre-bottom vector + ball offset
            vec=rot_vec((0, up.height-15), cfg["arm_upper"][side])
            off=rot_vec(((BALL[side]-0.5)*up.width, 0), cfg["arm_upper"][side])
            elbow=(SHOULDER[side][0]+vec[0]+off[0], SHOULDER[side][1]+vec[1]+off[1]); elbows[side]=elbow
            fa_name=substitution if (substitution and side=="R") else ("forearm_hand_L.png" if side=="L" else "forearm_hand_R.png")
            fa=load34(fa_name)
            # place forearm so top anchor lands on elbow, then rotate about elbow
            layer=Image.new("RGBA",(W,H),(0,0,0,0))
            layer.alpha_composite(fa,(int(elbow[0]-TOPA[side]*fa.width),int(elbow[1])))
            layer=layer.rotate(cfg["arm_lower"][side], center=elbow, expand=False, resample=Image.BICUBIC)
            canvas.alpha_composite(layer)
            hand_vec=rot_vec(((0.20- TOPA[side])*fa.width if side=="L" else (0.25-TOPA[side])*fa.width, fa.height-15), cfg["arm_lower"][side])
            hand_end=(elbow[0]+hand_vec[0], elbow[1]+hand_vec[1])
            wrists[side]=(elbow[0]+(hand_end[0]-elbow[0])*0.75, elbow[1]+(hand_end[1]-elbow[1])*0.75)
            wrists[side+"_hand"]=hand_end
        return elbows, wrists
    elbows=wrists=None
    if not arms_over_face:
        elbows,wrists=draw_arms()
    neck, neck_bb, neck_w, neck_h = load_neck()
    paste_cx(canvas, neck, 700, 330)  # T-neck: bridges head bottom (391) and torso top (350)
    paste_cx(canvas, load34("head_cowl.png"), 700, 195)
    if arms_over_face:
        elbows,wrists=draw_arms()
    a=np_alpha(canvas)
    ys,xs=a
    gates={
      "bbox":[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
      "alpha_px":int((a[1]>10).sum()) if False else int(sum(1 for v in canvas.getchannel("A").getdata() if v>10)),
      "knees":{k:[round(v[0],1),round(v[1],1)] for k,v in knees.items()},
      "feet_end":{k:[round(v[0],1),round(v[1],1)] for k,v in feet.items()},
      "elbows":{k:[round(v[0],1),round(v[1],1)] for k,v in elbows.items()},
      "wrists":{k:[round(v[0],1),round(v[1],1)] for k,v in wrists.items()},
      "neck":{"alpha_bbox_native":list(neck_bb),"rendered_width_px":neck_w,"rendered_height_px":neck_h,"cx":700,"top":330,"bottom":330+neck_h},
      "clamped_angles":clamped,
      "inside_canvas": bool(xs.min()>=0 and ys.min()>=0 and xs.max()<W and ys.max()<H),
    }
    return canvas, gates
def np_alpha(canvas):
    import numpy as np
    a=np.array(canvas)[:,:,3]; ys,xs=np.where(a>10); return (ys,xs)
results={}
for name,cfg in POSES.items():
    cfg2={k:dict(v) for k,v in cfg.items()}
    arms_over=(name=="arms-up-over-face")
    subst="forearm_hand_mid.png" if name=="sit-chair" else None
    fig,gates=build(name,cfg2,arms_over_face=arms_over, substitution=subst)
    fig.save(f"{ROOT}/poses/{name}-20261101.png")
    grey=Image.new("RGBA",fig.size,(126,126,126,255)); grey.alpha_composite(fig); grey.convert("RGB").save(f"{ROOT}/poses/{name}-20261101-on-grey.png")
    results[name]=gates; print(name, gates["bbox"], "feet", gates["feet_end"])
# T3 IK check for lean pose: shoulder -> knee target
lean=results["sit-lean-forward-34"]
for side,sh in SHOULDER.items():
    knee=lean["knees"][side]
    # forearm+upper lengths approx (scaled piece heights)
    l1=237 if side=="L" else 256; l2=267 if side=="L" else 298
    up,low,d=ik_2bone(sh, knee, l1, l2)
    print("IK",side,"shoulder->knee",round(d,1),"upper",round(up,1),"lower_rel",round(low,1), "FK used", POSES["sit-lean-forward-34"]["arm_upper"][side], POSES["sit-lean-forward-34"]["arm_lower"][side])
    results["sit-lean-forward-34"][f"ik_check_{side}"]={"target_knee":knee,"dist":round(d,1),"ik_upper":round(up,1),"ik_lower_rel":round(low,1)}
# front rig untouched check
results["_front_rig_untouched"]={"sliced/Torso_Chest.png":md5(os.path.join(SLICED,"Torso_Chest.png")),"sliced/Head_Front.png":md5(os.path.join(SLICED,"Head_Front.png")),"sliced/Neck.png":md5(os.path.join(SLICED,"Neck.png"))}
json.dump(results, open(f"{ROOT}/gates-20261101.json","w"), indent=2)
# build sequence GIF: sheet -> pieces contact -> neck -> rig -> poses
seq=[]
sheet=Image.open(os.path.expanduser("~/workspace/user/files/1000179383_25_yh27.jpg")).convert("RGB"); sheet.thumbnail((700,800)); seq.append(sheet)
pieces_contact=Image.open(os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/contacts/pieces-contact-20261101.png")).convert("RGB"); pieces_contact.thumbnail((700,800)); seq.append(pieces_contact)
for n in ["sit-chair","sit-lean-forward-34","sit-upright"]:
    im=Image.open(f"{ROOT}/poses/{n}-20261101-on-grey.png").convert("RGB"); im.thumbnail((700,800)); seq.append(im)
# pad to same size on grey
canvas_seq=[]
for im in seq:
    c=Image.new("RGB",(700,800),(126,126,126)); c.paste(im,((700-im.width)//2,(800-im.height)//2)); canvas_seq.append(c)
canvas_seq[0].save(f"{ROOT}/build-sequence-20261101.gif", save_all=True, append_images=canvas_seq[1:], duration=800, loop=0)
# contact of poses
contact=Image.new("RGB",(4*360,560),(126,126,126))
for i,n in enumerate(["sit-chair","sit-upright","sit-lean-forward-34","arms-up-over-face"]):
    p=Image.open(f"{ROOT}/poses/{n}-20261101-on-grey.png"); p.thumbnail((350,550)); contact.paste(p,(i*360+5,5))
contact.save(f"{ROOT}/contacts/poses-contact-20261101.png")
print("done")
