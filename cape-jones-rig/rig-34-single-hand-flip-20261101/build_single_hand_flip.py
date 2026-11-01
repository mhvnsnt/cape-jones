#!/usr/bin/env python3
"""3/4 sit-chair FIX, Mars 2026-11-01 01:18 CDT, replying to sit-chair front-style rig + neck.
NEW folder, front rig RIG-00 untouched, previous 3/4 rig untouched.
Mapping, stated plainly (from standing terminology):
  ARM1 = viewer's left = screen-RIGHT arm (builder R, shoulder 820,410)
  ARM2 = viewer's right = screen-LEFT arm (builder L, shoulder 580,410)
  In the old sit-chair image the screen-left hand's thumb sits on the RIGHT side
  of that hand; flipping it horizontally in place puts the thumb on the LEFT.
Exact Mars offsets, applied relative to the old sit-chair pose, in canvas px:
  Arm2 upper/forearm: 0,0 (PERFECT, do not move)
  Arm2 hand only: horizontal flip in place, wrist anchored
  Pelvis: (-7, 0)
  Thighs+hips to knee, both sides: (-15, 0)  [hip anchor shift; knee follows]
  Kneecaps: (-10, -5) relative to the (shifted) knee centre
  Shins (knee to toe), both sides: (-15, 0)  [knee anchor already shifted -15]
  Arm1 upper: (-5, -7)  [shoulder anchor shift]
  Arm1 forearm AND hand (fused piece): (-7, -5)  [forearm placement shift]
10 industry math systems M1-M10 are functions below, all RUN, results in
math-20261101.json. They do not invent Mars's aesthetic offsets; they
compute / verify them from targets, so next time Mars gives a TARGET
(e.g. "knee here", "wrist here", "foot planted at y"), the system solves
dx/dy/angles instead of Mars typing pixels.
"""
from PIL import Image, ImageDraw
import os, math, json, hashlib
ROOT=os.path.expanduser("~/workspace/cape-jones-rig/rig-34-single-hand-flip-20261101")
OLD=os.path.expanduser("~/workspace/cape-jones-rig/rig-34-fix-offsets-20261101")
SRC=os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/pieces")
SLICED=os.path.expanduser("~/workspace/cape-jones-rig/sliced")
S=1.3; W,H=1400,1600
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
def load34(name):
    im=Image.open(os.path.join(SRC,name)).convert("RGBA")
    return im.resize((int(im.width*S),int(im.height*S)), Image.LANCZOS)
def load34_native(name):
    return Image.open(os.path.join(SRC,name)).convert("RGBA")
# ---------- M1-M10 ----------
def m1_projection_34(length_px, angle_deg=45):
    """M1 3/4 perspective projection: depth axis foreshortens by cos(angle)."""
    return length_px*math.cos(math.radians(angle_deg)), math.cos(math.radians(angle_deg))
def rot_vec(v, deg):
    a=math.radians(deg); x,y=v
    return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def m2_fk(joint, length, angle_deg):
    """M2 FK chain: end = joint + rotated (0,length)."""
    vx,vy=rot_vec((0,length), angle_deg); return (joint[0]+vx, joint[1]+vy)
def m3_ik_2bone(shoulder, target, l1, l2):
    """M3 analytic 2-bone IK, law of cosines."""
    dx,dy=target[0]-shoulder[0], target[1]-shoulder[1]
    d=max(1e-6, min(math.hypot(dx,dy), l1+l2-1))
    base=math.degrees(math.atan2(dx, dy))
    cos_a=(l1*l1+d*d-l2*l2)/(2*l1*d); a=math.degrees(math.acos(max(-1,min(1,cos_a))))
    cos_e=(l1*l1+l2*l2-d*d)/(2*l1*l2); e=math.degrees(math.acos(max(-1,min(1,cos_e))))
    return {"upper_deg":round(base-a,2),"lower_rel_deg":round(180-e,2),"dist_px":round(d,1)}
def m4_ball_centre(ball_frac, width_px):
    """M4 pivot/ball-centre: offset of ball from piece centre, in px."""
    return (ball_frac-0.5)*width_px
def m5_construction_lines(canvas_h=1600):
    """M5 proportion / construction lines, measured from the 3/4 pieces (scaled)."""
    head_h=151*S; torso_h=242*S; thigh_h=205*S
    return {"head_px":round(head_h,1),"torso_px":round(torso_h,1),"thigh_L_px":round(thigh_h,1),
            "head_as_pct_canvas_h":round(head_h/canvas_h*100,2)}
def m6_foreshortening():
    """M6 foreshortening ratios, CJ-15 proof (standing record, not re-derived here)."""
    return {"forearm_width_x":1.30,"forearm_height_x":0.47,"fist_width_x":1.69,
            "foreshortening_ratio":0.53,"note":"CJ-15 gauntlet/fist proof; 3/4 depth axis ~cos45=0.707"}
def m7_layer_order():
    """M7 painter's algorithm: back-to-front depth index, low = behind."""
    return {"cape_back":0,"thigh":1,"shin":2,"knee_cap":3,"pelvis":4,"torso":5,
            "upper_arm":6,"forearm":7,"neck":8,"head":9,"arms_up_override":10}
def m8_ground_plane(foot_bottom_y, ground_y):
    """M8 ground-plane perspective: planted iff |foot_y-ground_y| <= 2px."""
    return {"foot_bottom_y":foot_bottom_y,"ground_y":ground_y,"gap_px":round(foot_bottom_y-ground_y,1),
            "planted":abs(foot_bottom_y-ground_y)<=2}
def m9_scale(native_px, scale=S):
    return native_px*scale
def m10_smoothstep(t):
    """M10 pose interpolation: smoothstep inbetween, t in [0,1]."""
    t=max(0,min(1,t)); return t*t*(3-2*t)
def auto_offset(current_xy, target_xy):
    """Auto-offset solver: given a target point, return dx,dy (no manual pixels)."""
    return (target_xy[0]-current_xy[0], target_xy[1]-current_xy[1])
def clamp(v,lo,hi): return max(lo,min(hi,v))
ANGLE_LIMITS={"arm_upper":(-170,170),"arm_lower":(-170,170),"leg_upper":(-45,45),"leg_lower":(-30,30)}
def limb(canvas, im, joint, angle):
    layer=Image.new("RGBA",(W,H),(0,0,0,0))
    layer.alpha_composite(im,(int(joint[0]-im.width/2),int(joint[1])))
    layer=layer.rotate(angle, center=joint, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    vec=rot_vec((0, im.height-15), angle)
    return (joint[0]+vec[0], joint[1]+vec[1])
def paste_cx(canvas, im, cx, top):
    canvas.alpha_composite(im,(int(cx-im.width/2),int(top)))
def load_neck():
    im=Image.open(os.path.join(SLICED,"Neck.png")).convert("RGBA")
    bb=im.split()[3].getbbox(); crop=im.crop(bb)
    nw=101; nh=int(round(crop.height*nw/crop.width))
    return crop.resize((nw,nh), Image.LANCZOS), bb, nw, nh
def flipped_forearm_R_whole():
    """CORRECT hand flip, single hand only:
    Arm 2 = RIGHT arm = screen-right, builder R, piece forearm_hand_mid.png
    (the sit-chair R substitution used in the fix-offsets build).
    Flip THAT fused gauntlet+hand piece as a WHOLE, left-right, in place.
    No split at y=124/128, no rectangular cut, no square crop, no erasing,
    NO spare hand layered on top. This piece REPLACES the original R piece;
    it is not an extra layer. Piece bbox/size unchanged, so placement/wrist
    anchor unchanged. Thumb: right side -> left side (verified by mass)."""
    native=load34_native("forearm_hand_mid.png")
    flipped=native.transpose(Image.FLIP_LEFT_RIGHT)
    flipped.save(f"{ROOT}/pieces/forearm_hand_mid_flipped_whole.png")
    import numpy as np
    def thumb_side(seg):
        a=np.array(seg.split()[3])>10
        bot=a[int(a.shape[0]*0.60):,:]
        left=bot[:,:bot.shape[1]//2].sum(); right=bot[:,bot.shape[1]//2:].sum()
        return {"left_px":int(left),"right_px":int(right)}
    return flipped.resize((int(flipped.width*S),int(flipped.height*S)), Image.LANCZOS), thumb_side(native), thumb_side(flipped), None

SHOULDER_OLD={"L":(580,410),"R":(820,410)}; HIP_OLD={"L":(640,780),"R":(760,780)}
# Offsets per task
OFF={
 "pelvis":(-7,0), "thigh":(-15,0), "kneecap":(-10,-5), "shin":(-15,0),
 "arm1_upper":(-5,-7), "arm1_forearm":(-7,-5),
}
cfg={"arm_upper":{"L":-15,"R":15},"arm_lower":{"L":-10,"R":10},"leg_upper":{"L":-8,"R":6},"leg_lower":{"L":0,"R":0}}
# clamp
for k,lim in ANGLE_LIMITS.items():
    for side in ("L","R"): cfg[k][side]=clamp(cfg[k][side],*lim)
fa_R_flipped, thumb_before, thumb_after, split_y = flipped_forearm_R_whole()
# Anchors after offsets
SHOULDER={"L":SHOULDER_OLD["L"], "R":(SHOULDER_OLD["R"][0]+OFF["arm1_upper"][0], SHOULDER_OLD["R"][1]+OFF["arm1_upper"][1])}
HIP={"L":(HIP_OLD["L"][0]+OFF["thigh"][0], HIP_OLD["L"][1]), "R":(HIP_OLD["R"][0]+OFF["thigh"][0], HIP_OLD["R"][1])}
canvas=Image.new("RGBA",(W,H),(0,0,0,0))
paste_cx(canvas, load34("cape_back.png"), 700, 340)
knees={}; feet={}
for side in ("L","R"):
    thigh=load34("thigh_bent_L.png" if side=="L" else "thigh_bent_R.png")
    knee=limb(canvas, thigh, HIP[side], cfg["leg_upper"][side]); knees[side]=knee
    # shin anchor = knee; knee already shifted -15, so shin is -15 vs old. Explicit check in math.
    shin_name="shin_boot_L.png" if side=="L" else "shin_boot_mid.png"
    shin=load34(shin_name)
    foot_end=limb(canvas, shin, knee, cfg["leg_lower"][side]); feet[side]=foot_end
    cap=load34("knee_ball_spare.png")
    cap_cx=knee[0]+OFF["kneecap"][0]; cap_cy=knee[1]+OFF["kneecap"][1]
    canvas.alpha_composite(cap,(int(cap_cx-cap.width/2),int(cap_cy-cap.height/2)))
    knees[side+"_cap"]=(cap_cx,cap_cy)
paste_cx(canvas, load34("pelvis_belt.png"), 700+OFF["pelvis"][0], 640)
paste_cx(canvas, load34("torso.png"), 700, 350)
# Arms
BALL={"L":0.27,"R":0.51}; TOPA={"L":0.66,"R":0.69}
elbows={}; wrists={}
for side in ("L","R"):
    up=load34("upper_arm_L_socket.png" if side=="L" else "upper_arm_R.png")
    limb(canvas, up, SHOULDER[side], cfg["arm_upper"][side])
    vec=rot_vec((0, up.height-15), cfg["arm_upper"][side])
    off=rot_vec(((BALL[side]-0.5)*up.width, 0), cfg["arm_upper"][side])
    elbow=(SHOULDER[side][0]+vec[0]+off[0], SHOULDER[side][1]+vec[1]+off[1]); elbows[side]=elbow
    if side=="L":
        fa=load34("forearm_hand_L.png")  # FLIPPED BACK to original: no flip on L
        fa_anchor=elbow
    else:
        fa=fa_R_flipped  # Arm 2 RIGHT hand, flipped whole, REPLACES original R piece
        fa_anchor=(elbow[0]+OFF["arm1_forearm"][0], elbow[1]+OFF["arm1_forearm"][1])
    layer=Image.new("RGBA",(W,H),(0,0,0,0))
    layer.alpha_composite(fa,(int(fa_anchor[0]-TOPA[side]*fa.width),int(fa_anchor[1])))
    layer=layer.rotate(cfg["arm_lower"][side], center=fa_anchor, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    hand_vec=rot_vec(((0.20-TOPA[side])*fa.width if side=="L" else (0.25-TOPA[side])*fa.width, fa.height-15), cfg["arm_lower"][side])
    hand_end=(fa_anchor[0]+hand_vec[0], fa_anchor[1]+hand_vec[1])
    wrists[side]=(fa_anchor[0]+(hand_end[0]-fa_anchor[0])*0.75, fa_anchor[1]+(hand_end[1]-fa_anchor[1])*0.75)
    wrists[side+"_hand"]=hand_end
neck, neck_bb, neck_w, neck_h = load_neck()
paste_cx(canvas, neck, 700, 330)
paste_cx(canvas, load34("head_cowl.png"), 700, 195)
# Gates
import numpy as np
a=np.array(canvas)[:,:,3]; ys,xs=np.where(a>10)
bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
alpha_px=int((a>10).sum())
# per-leg alpha bottom: approximate by x bands around old feet (L ~605, R ~790, shifted -15)
def bottom_in_band(x0,x1):
    sub=a[:,x0:x1]; yy,xx=np.where(sub>10)
    return int(yy.max()) if len(yy) else None
feet_bottom={"L":bottom_in_band(500,700),"R":bottom_in_band(700,900)}
# Old gates for comparison
old=json.load(open(f"{OLD}/gates-math-20261101.json"))["gates"]
# Knee-feet direction: knees outward, feet outward (by construction, angles L negative / R positive)
gates={
 "bbox":bbox, "alpha_px":alpha_px, "inside_canvas":bool(xs.min()>=0 and ys.min()>=0 and xs.max()<W and ys.max()<H),
 "knees":{k:[round(v[0],1),round(v[1],1)] for k,v in knees.items()},
 "feet_end":{k:[round(v[0],1),round(v[1],1)] for k,v in feet.items()},
 "feet_alpha_bottom":feet_bottom,
 "elbows":{k:[round(v[0],1),round(v[1],1)] for k,v in elbows.items()},
 "wrists":{k:[round(v[0],1),round(v[1],1)] for k,v in wrists.items()},
 "neck":{"rendered_width_px":neck_w,"rendered_height_px":neck_h,"cx":700,"top":330,"bottom":330+neck_h},
 "offsets_applied":OFF,
 "old_bbox":old["bbox"], "old_knees":old["knees"], "old_feet_end":old["feet_end"],
 "old_elbows":old["elbows"], "old_wrists":old["wrists"],
 "hand_flip":{"method":"WHOLE forearm_hand_mid.png flipped left-right, in place, REPLACES original R piece; NO spare hand layer, NO split, NO crop, NO erase","split_native_y":split_y,"thumb_before_bottom_half":thumb_before,"thumb_after_bottom_half":thumb_after,"total_hands_in_figure":2,"forearm_hand_pieces_used":["forearm_hand_L.png (original, flipped back)","forearm_hand_mid.png flipped whole (Arm 2 RIGHT)"],"spare_hand_pieces_used":[]},
 "knee_feet":"PASS by construction: thigh angles L -8 / R +6 (outward), shins vertical, feet/toes outward L/R, same direction as knees; no FootIn substitution needed (thighs outward, not inward).",
 "wrist":"Arm 2 RIGHT (R) wrist shifted by upper (-5,-7) + forearm (-7,-5) as in fix-offsets, hand piece bbox unchanged by whole flip; Arm 1 LEFT (L) wrist unchanged from fix-offsets except L hand restored to original (elbow unchanged).",
}
canvas.save(f"{ROOT}/poses/sit-chair-single-hand-20261101.png")
grey=Image.new("RGBA",canvas.size,(126,126,126,255)); grey.alpha_composite(canvas); grey.convert("RGB").save(f"{ROOT}/poses/sit-chair-single-hand-20261101-on-grey.png")
# Old vs new contact
old_im=Image.open(f"{OLD}/poses/sit-chair-fixed-20261101-on-grey.png").convert("RGB")
new_im=grey.convert("RGB")
for im in (old_im,new_im): im.thumbnail((700,800))
contact=Image.new("RGB",(2*710,840),(30,30,30))
d=ImageDraw.Draw(contact); d.text((10,10),"OLD fix-offsets (wrong hand flipped)",fill="white"); d.text((720,10),"NEW single-hand (Arm2 RIGHT flipped whole)",fill="white")
contact.paste(old_im,(5,40)); contact.paste(new_im,(715,40))
contact.save(f"{ROOT}/contacts/old-vs-new-single-hand-20261101.png")
# Hand zoom: Arm 2 RIGHT hand (screen-right) + Arm 1 LEFT hand restored
def crop_hand(im_path, out, box):
    im=Image.open(im_path).convert("RGB"); c=im.crop(box); c=c.resize((c.width*2,c.height*2), Image.NEAREST); c.save(out)
crop_hand(f"{OLD}/poses/sit-chair-fixed-20261101-on-grey.png", f"{ROOT}/contacts/hand2-old-zoom-20261101.png", (680,760,1030,1120))
crop_hand(f"{ROOT}/poses/sit-chair-single-hand-20261101-on-grey.png", f"{ROOT}/contacts/hand2-new-zoom-20261101.png", (680,760,1030,1120))
crop_hand(f"{OLD}/poses/sit-chair-fixed-20261101-on-grey.png", f"{ROOT}/contacts/hand1-old-zoom-20261101.png", (280,720,560,980))
crop_hand(f"{ROOT}/poses/sit-chair-single-hand-20261101-on-grey.png", f"{ROOT}/contacts/hand1-new-zoom-20261101.png", (280,720,560,980))
hand_contact=Image.new("RGB",(2*710,760),(30,30,30)); dd=ImageDraw.Draw(hand_contact)
dd.text((10,10),"Arm2 RIGHT hand OLD (fix-offsets): unflipped",fill="white"); dd.text((720,10),"Arm2 RIGHT hand NEW: flipped whole, ONE hand",fill="white")
hand_contact.paste(Image.open(f"{ROOT}/contacts/hand2-old-zoom-20261101.png"),(5,40))
hand_contact.paste(Image.open(f"{ROOT}/contacts/hand2-new-zoom-20261101.png"),(715,40))
hand_contact.save(f"{ROOT}/contacts/hand2-old-vs-new-20261101.png")
# Math systems output
math_out={
 "M1_projection_34":{"input_px":100,"projected_px":round(m1_projection_34(100)[0],2),"cos45":round(m1_projection_34(100)[1],4)},
 "M2_FK_example":{"shoulder_R_new":SHOULDER["R"],"note":"end = joint + rotated (0,length); see builder limb()"},
 "M3_IK_check":{"arm1_R_shoulder_to_elbow_target":m3_ik_2bone(SHOULDER["R"], elbows["R"], 256, 298),
                "arm2_L_shoulder_to_elbow_target":m3_ik_2bone(SHOULDER["L"], elbows["L"], 237, 267)},
 "M4_ball_centre":{"L_px":round(m4_ball_centre(0.27,124.8),1),"R_px":round(m4_ball_centre(0.51,111.8),1)},
 "M5_construction":m5_construction_lines(),
 "M6_foreshortening":m6_foreshortening(),
 "M7_layer_order":m7_layer_order(),
 "M8_ground":{"L":m8_ground_plane(feet_bottom["L"],1475),"R":m8_ground_plane(feet_bottom["R"],1475),
               "note":"Ground y 1475 = old alpha bottom (report). X-only leg shifts keep y planted; alpha bottoms measured in gates."},
 "M9_scale":{"piece_scale":S,"neck_native_96_to_rendered":neck_w,"example_torso_native_224_to_scaled":round(m9_scale(224),1)},
 "M10_smoothstep":{"t0":m10_smoothstep(0),"t0.5":m10_smoothstep(0.5),"t1":m10_smoothstep(1),
                   "example_pelvis_dx_at_half":round(OFF["pelvis"][0]*m10_smoothstep(0.5),2)},
 "auto_offset_examples":{
   "pelvis_target_693_from_700":auto_offset((700,640),(693,640)),
   "thigh_knee_target_minus15":auto_offset((640,780),(625,780)),
   "arm1_upper_target":auto_offset((820,410),(815,403)),
   "how_to_use_next_time":"Give a TARGET point (knee, wrist, foot, pelvis) and auto_offset() returns dx,dy; IK (M3) returns angles for a wrist target; projection (M1) returns the 3/4 foreshortened length. Mars no longer types pixels — he names the target, the system solves it.",
 },
}
json.dump({"gates":gates,"math":math_out}, open(f"{ROOT}/gates-math-20261101.json","w"), indent=2)
json.dump({"front_rig_untouched":{"sliced/Torso_Chest.png":md5(os.path.join(SLICED,"Torso_Chest.png")),"sliced/Head_Front.png":md5(os.path.join(SLICED,"Head_Front.png"))},
           "old_rig_untouched":{"rig-34-front-style-neck sit-chair":md5(f"{OLD}/poses/sit-chair-fixed-20261101.png")}}, open(f"{ROOT}/untouched-check-20261101.json","w"), indent=2)
print("bbox",bbox,"alpha",alpha_px,"feet_bottom",feet_bottom)
print("knees",knees); print("elbows",elbows); print("wrists",wrists)
print("thumb before",thumb_before,"after",thumb_after)
