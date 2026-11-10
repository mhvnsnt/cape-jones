"""V6: V5 cape-fix base + cape collar offset ONLY: down 20px, left 10px.
Collar/top zone (canvas y<=450) gets full offset + full torso motion.
Seated bottom zone (canvas y>=950) gets 0 offset, pinned.
Middle 450-950: smoothstep gradient between the two.
Whole cape layer warped, no crop, no erase, all rows/cols preserved,
mapping monotonic in y (max total dy 35 * max |w'| ~0.003 = 0.105 < 1).
All other pieces/motion identical to V5 builder."""
from PIL import Image
import json, os, math
import numpy as np
ROOT="/home/hatch/workspace/cape-jones-rig"
OUT=f"{ROOT}/rig-34-locked-neck-v6-cape-collar-20261101"
P34=f"{ROOT}/sitting-rig-34-20261101/pieces"
PV7=f"{ROOT}/cut-limbs-v7c"
DEFS=[
 ("upperArmL", f"{P34}/upper_arm_L_socket.png", (125,237), (0.5,0)),
 ("thighR", f"{P34}/thigh_bent_R.png", (218,299), (0.5,0)),
 ("thighL", f"{P34}/thigh_bent_L.png", (230,267), (0.5,0)),
 ("forearmL", f"{ROOT}/rig-34-disassembled-wired-20261101/pieces/forearm_no_fist_L.png", (145,275), (0.39,0.11)),
 ("pelvis", f"{P34}/pelvis_belt.png", (218,181), (0.5,0.5)),
 ("kneeL", f"{P34}/knee_ball_spare.png", (74,94), (0.5,0.5)),
 ("elbowCapL", f"{PV7}/Arm_Front_Cap.png", (63,63), (0.5,0.5)),
 ("shinL", f"{P34}/shin_boot_L.png", (244,410), (0.5,0)),
 ("shinR", f"{P34}/shin_boot_mid.png", (256,415), (0.5,0)),
 ("kneeR", f"{P34}/knee_ball_spare.png", (74,94), (0.5,0.5)),
 ("torso", f"{P34}/torso.png", (291,315), (0.5,0)),
 ("upperArmR", f"{P34}/upper_arm_R.png", (112,256), (0.5,0)),
 ("forearmR", f"{ROOT}/rig-34-disassembled-wired-20261101/pieces/forearm_no_fist_R.png", (150,274), (0.63,0.11)),
 ("elbowCapR", f"{PV7}/Arm_Back_Cap.png", (63,63), (0.5,0.5)),
 ("neck", f"{ROOT}/sliced/Neck.png", (137,87), (0.5,0.5)),
 ("head", f"{P34}/head_cowl.png", (130,196), (0.5,0.5)),
 ("handL", f"{P34}/hand_spare_L.png", (117,170), (0.5,0.5)),
 ("handR", f"{P34}/hand_spare_L.png", (117,170), (0.5,0.5)),
]
SAVED={
 "upperArmL":(490,390,5),"thighR":(590,750,6),"thighL":(400,710,2),
 "forearmL":(455,580,-15),"pelvis":(565,650,0),"kneeL":(380,885,0),"elbowCapL":(465,580,0),
 "shinL":(225,945,0),"shinR":(395,985,-10),"kneeR":(560,950,0),"torso":(550,370,0),
 "head":(635,195,0),"upperArmR":(805,420,15),"forearmR":(685,650,45),"elbowCapR":(775,610,0),
 "handL":(530,740,-46),"handR":(565,755,70),
}
NECK_XY=(632,339,0)
TORSO_GROUP={"torso","upperArmL","upperArmR","forearmL","forearmR","elbowCapL","elbowCapR","handL","handR"}
W,H=1400,1600
CAPE_SRC=f"{P34}/cape_back.png"; CAPE_SIZE=(514,900); CAPE_PIVOT=(0.5,0.5); CAPE_XY=(360,330)
COLLAR_DX=-10; COLLAR_DY=20

def paste_piece(canvas, src, size, pivot, rot, xy, flip=False):
    ox,oy=pivot; x,y=xy
    im=Image.open(src).convert("RGBA").resize(size, Image.LANCZOS)
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    tmp=Image.new("RGBA",(size[0]*3,size[1]*3),(0,0,0,0)); tmp.alpha_composite(im,(size[0],size[1]))
    px,py=size[0]+ox*size[0], size[1]+oy*size[1]
    rot_im=tmp.rotate(-rot, resample=Image.BICUBIC, center=(px,py))
    paste_x=int(round(x+ox*size[0]-px)); paste_y=int(round(y+oy*size[1]-py))
    canvas.alpha_composite(rot_im,(paste_x,paste_y))
    return rot_im, paste_x, paste_y

def cape_layer_base():
    c=Image.new("RGBA",(W,H),(0,0,0,0)); paste_piece(c, CAPE_SRC, CAPE_SIZE, CAPE_PIVOT, 0, CAPE_XY)
    return c

def weight(ys):
    u=np.clip((ys-450)/500.0, 0, 1); return 1-(u*u*(3-2*u))

def warp_cape_v5(base, dy):
    """V5 only, vertical: for comparison measurements."""
    if dy==0: return base
    a=np.array(base).astype(np.float32)
    ys=np.arange(H, dtype=np.float32); w=weight(ys); shift=dy*w
    src_y=ys-shift
    y0=np.clip(np.floor(src_y).astype(int),0,H-1); y1=np.clip(y0+1,0,H-1); frac=(src_y-y0)[:,None,None]
    out=a[y0]*(1-frac)+a[y1]*frac
    return Image.fromarray(out.astype(np.uint8), "RGBA")

def warp_cape_v6(base, torso_dy):
    """V6: shift_y = torso_dy*w + 20*w, shift_x = -10*w, bilinear 2D."""
    a=np.array(base).astype(np.float32)
    ys=np.arange(H, dtype=np.float32); w=weight(ys)
    shift_y=(torso_dy+COLLAR_DY)*w
    shift_x=COLLAR_DX*w  # -10*w
    src_y=(ys-shift_y)[:,None] * np.ones((1,W), dtype=np.float32)
    src_x=np.ones((H,1), dtype=np.float32) * (np.arange(W, dtype=np.float32)[None,:]-shift_x[:,None])
    y0=np.clip(np.floor(src_y).astype(int),0,H-1); y1=np.clip(y0+1,0,H-1); fy=(src_y-y0)[:,:,None]
    x0=np.clip(np.floor(src_x).astype(int),0,W-1); x1=np.clip(x0+1,0,W-1); fx=(src_x-x0)[:,:,None]
    out=(a[y0,x0]*(1-fx)*(1-fy) + a[y0,x1]*fx*(1-fy) + a[y1,x0]*(1-fx)*fy + a[y1,x1]*fx*fy)
    return Image.fromarray(out.astype(np.uint8), "RGBA")

def cape_stats(layer):
    a=np.array(layer)[:,:,3]
    ys,xs=np.where(a>10)
    def centroid(rows, cols=None):
        sub=a[rows]
        yy,xx=np.where(sub>10)
        if len(yy)==0: return None
        return [round(float(xx.mean()),2), round(float(yy.mean()+rows.start),2)]
    return {"top":int(ys.min()),"bottom":int(ys.max()),"left":int(xs.min()),"right":int(xs.max()),
            "collar_centroid_xy_rows_lt450":centroid(slice(0,450)),
            "collar_centroid_xy_rows_lt550":centroid(slice(0,550)),
            "bottom_centroid_xy_rows_gt1100":centroid(slice(1100,1600))}

BASE_CAPE=cape_layer_base()
V5_POSE_CAPE=warp_cape_v5(BASE_CAPE, 0)
V6_POSE_CAPE=warp_cape_v6(BASE_CAPE, 0)
print("V5 cape pose", cape_stats(V5_POSE_CAPE))
print("V6 cape pose", cape_stats(V6_POSE_CAPE))

def render(dy=None, head_rot_extra=0, forearm_swing=0):
    dy=dy or {}
    torso_dy=dy.get("torso",0)
    warped=warp_cape_v6(BASE_CAPE, torso_dy)
    canvas=Image.new("RGBA",(W,H),(0,0,0,0)); canvas.alpha_composite(warped)
    bboxes={"cape_warped": cape_stats(warped)}
    for pid,src,size,pivot in DEFS:
        if pid=="neck":
            x,y,rot=NECK_XY; y=y+dy.get("neck",0)
        else:
            x,y,rot=SAVED[pid]; y=y+dy.get(pid,0)
            if pid=="head": rot=rot+head_rot_extra
            if pid=="forearmL": rot=rot-forearm_swing
            if pid=="forearmR": rot=rot+forearm_swing
        rot_im,px,py=paste_piece(canvas,src,size,pivot,rot,(x,y),flip=(pid=="handR"))
        single=Image.new("RGBA",(W,H),(0,0,0,0)); single.alpha_composite(rot_im,(px,py)); bboxes[pid]=single.getbbox()
    return canvas,bboxes

def grey(canvas):
    bg=Image.new("RGBA",(W,H),(126,126,126,255)); bg.alpha_composite(canvas); return bg.convert("RGB")
def smoothstep(u):
    u=max(0.0,min(1.0,u)); return u*u*(3-2*u)
def lean_t(f):
    if f<24: return 0.0
    if f<60: return smoothstep((f-24)/36.0)
    if f<72: return 1.0
    return 1.0-smoothstep((f-72)/24.0)

pose,bboxes=render()
pose.save(f"{OUT}/poses/default-sitting-pose-locked-neck-v6-cape-collar-20261101.png")
grey(pose).save(f"{OUT}/poses/default-sitting-pose-locked-neck-v6-cape-collar-20261101-on-grey.png")
pa=np.array(pose); ys,xs=np.where(pa[:,:,3]>0); fig_bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
print("FIG BBOX",fig_bbox)

os.makedirs("/tmp/capev6/idle",exist_ok=True); os.makedirs("/tmp/capev6/lean",exist_ok=True)
idle_checks={}
for f in range(48):
    bob=int(round(3*math.sin(2*math.pi*f/48))); tilt=int(round(2*math.sin(2*math.pi*f/48)))
    dy={p:bob for p in TORSO_GROUP}; dy["neck"]=bob; dy["head"]=bob
    c,bb=render(dy=dy, head_rot_extra=tilt); grey(c).save(f"/tmp/capev6/idle/frame-{f:03d}.png")
    if f in (0,12,24,36): idle_checks[f]={"bob":bob,"torso_top":bb["torso"][1],"cape":bb["cape_warped"]}
lean_checks={}
for f in range(96):
    t=lean_t(f); bob=int(round(3*math.sin(2*math.pi*f/48.0))); bob_lean=int(round(bob*(1-0.5*t)))
    head_tilt=round(1.5*math.sin(2*math.pi*f/48.0),2)
    dy={p:(14*t+bob_lean) for p in TORSO_GROUP}; dy["neck"]=18*t+bob_lean; dy["head"]=24*t+bob_lean
    c,bb=render(dy=dy, head_rot_extra=head_tilt, forearm_swing=5*t); grey(c).save(f"/tmp/capev6/lean/frame-{f:03d}.png")
    if f in (0,24,42,65,71,95): lean_checks[f]={"t":round(t,4),"torso_dy":dy["torso"],"torso_top":bb["torso"][1],"cape":bb["cape_warped"],"shinR":list(bb["shinR"])}
print("IDLE",json.dumps(idle_checks,indent=2)); print("LEAN",json.dumps(lean_checks,indent=2))
manifest={"canvas":[W,H],"figure_bbox":fig_bbox,
 "neck_v4":{"size":[127,82],"centre_x":700,"top":340,"bottom_excl":422,"unchanged":True},
 "collar_offset":{"dx":-10,"dy":20,"applied_to":"collar/top zone y<=450 full, gradient 450-950, bottom y>=950 pinned 0"},
 "cape_v5_pose":cape_stats(V5_POSE_CAPE),
 "cape_v6_pose":cape_stats(V6_POSE_CAPE),
 "idle_checks":idle_checks,"lean_checks":lean_checks,
 "legs_static_lean": lean_checks[0]["shinR"]==lean_checks[65]["shinR"],
 "approval":"0/1 separately: V6 pose, V6 idle, V6 lean. Do NOT delete V4 or V5 yet - deletion only after Mars shows V6 approval in chat.",
 "version":"V6","status":"V6 PENDING APPROVAL - V4 and V5 remain, do NOT delete yet."}
json.dump(manifest, open(f"{OUT}/MANIFEST-CAPE-COLLAR-V6-20261101.json","w"), indent=2)
print(json.dumps(manifest,indent=2))
