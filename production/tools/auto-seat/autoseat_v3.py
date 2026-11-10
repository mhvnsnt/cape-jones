"""AUTO-SEAT v3 — fix: solve ROOT for full 3D pelvis-head target (not X/Y + pelvis DLOC).

v2 bug: root placed X/Y only, pelvis DLOC didn't move the butt. v3: single
linear solve puts the pelvis head at (SEAT_C.x, SEAT_C.y, PELVIS_Z) where
PELVIS_Z = BUTT_Z + (pelvis_head_z - butt_z) measured in the solved pose.
The whole body moves rigidly via root; pose is preserved.
"""
import bpy, math, os, time
from mathutils import Matrix, Quaternion, Vector

WORKTREE = "/home/hatch/workspace/wt-autoseat"
FBX = os.path.join(WORKTREE, "production/tools/auto-seat/113_15.fbx")
OUT_BLEND = os.path.join(WORKTREE, "production/tools/auto-seat/proof_sitting.blend")
PROOF_DIR = os.path.join(WORKTREE, "production/tools/auto-seat/proofs")
os.makedirs(PROOF_DIR, exist_ok=True)

SRC_F0, SRC_F1 = 70, 150
DST_F0 = 1
TARGET_HEIGHT = 0.925
COMPRESSION = 0.020
ROOTQ = Quaternion((0, 0, 1), math.radians(-90.0))
STAMP = time.strftime("%Y%m%d_%H%M%S")

scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
assert rig and len(rig.data.bones) == 94
for b in rig.pose.bones:
    b.rotation_mode = 'QUATERNION'
if rig.animation_data:
    rig.animation_data.action = None
print("rig ready", flush=True)

# ---- measure chair
deps = bpy.context.evaluated_depsgraph_get()
def raycast(obj, origin, direction):
    o = obj.evaluated_get(deps)
    o.to_mesh()
    mw = o.matrix_world
    mi = mw.inverted()
    hit, loc, nor, idx = o.ray_cast(mi @ origin, (mi.to_3x3() @ direction).normalized())
    o.to_mesh_clear()
    return (mw @ loc) if hit else None

base = bpy.data.objects.get("recliner_base")
back = bpy.data.objects.get("recliner_backrest")
floor_o = bpy.data.objects.get("Floor")
seat_hits = []
for ix in range(7):
    for iy in range(7):
        h = raycast(base, Vector((2.92 + ix*0.06, 1.90 + iy*0.06, 1.5)), Vector((0,0,-1)))
        if h and 0.15 < h.z < 0.35:
            seat_hits.append(h.z)
seat_hits.sort()
SEAT_Z = seat_hits[len(seat_hits)//2]
SEAT_C = Vector((3.05, 2.067, SEAT_Z))
br = [raycast(back, Vector((2.90, 2.067, z)), Vector((1,0,0))) for z in (0.40,0.45,0.50,0.55,0.60)]
br = [h for h in br if h]
BACK_X = sum(h.x for h in br)/len(br)
fh = raycast(floor_o, Vector((3.0, 2.067, 1.0)), Vector((0,0,-1)))
FLOOR_Z = fh.z if fh else 0.0
BUTT_Z = SEAT_Z - COMPRESSION
print(f"SEAT_Z={SEAT_Z:.4f} BACK_X={BACK_X:.4f} FLOOR_Z={FLOOR_Z:.4f} BUTT_Z={BUTT_Z:.4f}", flush=True)
# NOTE: loungeChairRelax(Clone) stays render-hidden (canon scene state);
# the recliner_* parts are the measured/rendered chair. Do not unhide.
pass

# ---- mocap import (same proven math)
bpy.ops.import_scene.fbx(filepath=FBX)
src = next(o for o in bpy.data.objects if o.type=='ARMATURE' and o != rig)
src_act = src.animation_data.action
src.animation_data.action = None
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
SRC_REST = {b.name: (src.matrix_world @ b.matrix).to_3x3().to_quaternion() for b in src.pose.bones}
TGT_RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion() for b in rig.data.bones}
M_REL = {}
for b in rig.data.bones:
    M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion() if b.parent is None else \
        (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()

M = [
 ("hip",    [("pelvis", 1.0)]),
 ("abdomen",[("spine_1", 0.5), ("spine_2", 0.5)]),
 ("chest",  [("spine_3", 0.34), ("spine_4", 0.33), ("chest", 0.33)]),
 ("neck",   [("neck_1", 0.5), ("neck_2", 0.5)]),
 ("head",   [("head", 1.0)]),
 ("lCollar",[("clavicle_L", 1.0)]), ("rCollar",[("clavicle_R", 1.0)]),
 ("lShldr", [("upperarm_L", 1.0)]), ("rShldr",[("upperarm_R", 1.0)]),
 ("lForeArm",[("forearm_L", 1.0)]), ("rForeArm",[("forearm_R", 1.0)]),
 ("lHand",  [("hand_L", 1.0)]), ("rHand",[("hand_R", 1.0)]),
 ("lThigh", [("thigh_L", 1.0)]), ("rThigh",[("thigh_R", 1.0)]),
 ("lShin",  [("shin_L", 1.0)]), ("rShin",[("shin_R", 1.0)]),
 ("lFoot",  [("foot_L", 1.0)]), ("rFoot",[("foot_R", 1.0)]),
]
for sside, tside in (("l","_L"),("r","_R")):
    for sseg,fname,n in [("Thumb1","thumb",1),("Thumb2","thumb",2),("Index1","index",1),
                         ("Index2","index",2),("Mid1","middle",1),("Mid2","middle",2),
                         ("Ring1","ring",1),("Ring2","ring",2),("Pinky1","pinky",1),("Pinky2","pinky",2)]:
        sn=f"{sside}{sseg}"
        if fname=="thumb": M.append((sn,[(f"finger_thumb_{n}{tside}",1.0)]))
        elif n==1: M.append((sn,[(f"finger_{fname}_1{tside}",1.0)]))
        else: M.append((sn,[(f"finger_{fname}_2{tside}",0.6),(f"finger_{fname}_3{tside}",0.4)]))
def scaled(q,w): return q if w==1.0 else Quaternion(q.axis, q.angle*w)

root = rig.pose.bones['root']; pb = rig.pose.bones['pelvis']
root.rotation_mode='QUATERNION'; root.rotation_quaternion=ROOTQ
W_ROOT = TGT_RESTW['root'] @ ROOTQ
act = bpy.data.actions.new("autoseat_v3")
if not rig.animation_data: rig.animation_data_create()
rig.animation_data.action = act

def eval_now():
    bpy.context.view_layer.update()
    return bpy.context.evaluated_depsgraph_get()

# proxy for contact measurement (created BEFORE calibration — calibrate on verts)
body=bpy.data.objects.get("CapeJones_Body")
bpy.context.view_layer.objects.active=body; body.select_set(True)
bpy.ops.object.duplicate()
proxy=bpy.context.view_layer.objects.active; proxy.name="BodyProxy"
proxy.hide_viewport=True; proxy.hide_render=True
dec=proxy.modifiers.new("DECIMATE",'DECIMATE'); dec.ratio=0.04
bpy.context.view_layer.objects.active=proxy
bpy.ops.object.modifier_apply(modifier=dec.name)
body.select_set(False); proxy.select_set(False)
pelv_gi=proxy.vertex_groups["pelvis"].index
BUTT_IDX=[v.index for v in proxy.data.vertices for g in v.groups if g.group==pelv_gi and g.weight>0.6]
BACK_GNS=[gn for gn in ("spine_1","spine_2","spine_3","spine_4","chest") if gn in proxy.vertex_groups]
BACK_GIS={proxy.vertex_groups[gn].index for gn in BACK_GNS}
print(f"proxy: {len(proxy.data.vertices)} verts, {len(BUTT_IDX)} butt verts", flush=True)

# calibrate root.location -> MEAN BUTT VERTEX world (rigid for pelvis verts;
# bone head is 22cm off from the surface, so calibrate on the verts directly)
def mean_butt():
    d=eval_now(); pm=proxy.evaluated_get(d); mesh=pm.to_mesh(); mw=pm.matrix_world
    pts=[mw@mesh.vertices[i].co for i in BUTT_IDX if mesh.vertices[i].co.z<0.41]
    pm.to_mesh_clear()
    s=Vector((0,0,0))
    for p in pts: s+=p
    return s/len(pts)
# (calibration removed — using analytic root_world_R() in the solve instead)

def m_butt():
    d=eval_now(); pm=proxy.evaluated_get(d); mesh=pm.to_mesh(); mw=pm.matrix_world
    zs=[(mw@mesh.vertices[i].co).z for i in BUTT_IDX if mesh.vertices[i].co.z<0.41]
    pm.to_mesh_clear(); return min(zs) if zs else None
def m_back(px):
    d=eval_now(); pm=proxy.evaluated_get(d); mesh=pm.to_mesh(); mw=pm.matrix_world
    xs=[]
    for v in mesh.vertices:
        if sum(g.weight for g in v.groups if g.group in BACK_GIS)>0.5:
            wx=(mw@v.co).x
            if wx>px+0.02: xs.append(wx)
    pm.to_mesh_clear(); return BACK_X-max(xs) if xs else None

def pose_frame(i, Wdes_out=None):
    scn.frame_set(SRC_F0+i); bpy.context.view_layer.update()
    Ws={b.name:(src.matrix_world@b.matrix).to_3x3().to_quaternion() for b in src.pose.bones}
    Wdes={}
    for sname,targets in M:
        D=SRC_REST[sname].inverted()@Ws[sname]
        if sname in ('neck','head'): D=scaled(D,0.5)
        for tname,w in targets: Wdes[tname]=TGT_RESTW[tname]@scaled(D,w)
    for sname,targets in M:
        for tname,w in targets:
            qpb=rig.pose.bones[tname]; par=qpb.parent
            Wpar=Quaternion() if par is None else (W_ROOT if par.name=='root' else (Wdes[par.name] if par.name in Wdes else TGT_RESTW[par.name]))
            qpb.rotation_quaternion=(Wpar@M_REL[tname]).inverted()@Wdes[tname]
    root.rotation_quaternion=ROOTQ
    if Wdes_out is not None: Wdes_out.update(Wdes)
    return Wdes

# ---- SOLVE on middle frame
MID=(SRC_F1-SRC_F0)//2
src.animation_data.action=src_act
Wdes=pose_frame(MID)
root.location=Vector((0,0,0)); pb.location=Vector((0,0,0))
bpy.context.view_layer.update()

# Analytic pelvis placement: pelvis.location (bone-local) -> world via pelvis world rotation.
# The pelvis has use_deform=True, so moving it moves the mesh. (Root has use_deform=False.)
def pelvis_world_R():
    return (rig.matrix_world @ rig.pose.bones['pelvis'].matrix).to_3x3()
def place_pelvis(world_delta):
    R = pelvis_world_R()
    pb.location += R.inverted() @ world_delta
    bpy.context.view_layer.update()

# measure butt (min and mean) in the raw posed position
bz0=m_butt()
mb0=mean_butt()
print(f"raw: butt_min_z={bz0:.4f} butt_mean=({mb0.x:.3f},{mb0.y:.3f},{mb0.z:.3f})", flush=True)
# mean target: seat XZ + height that puts MIN at BUTT_Z
MEAN_Z_TGT = BUTT_Z + (mb0.z - bz0)
mean_tgt = Vector((SEAT_C.x, SEAT_C.y, MEAN_Z_TGT))
print(f"mean target: ({mean_tgt.x:.3f},{mean_tgt.y:.3f},{mean_tgt.z:.3f})", flush=True)
# iterate (2 passes; R is stable for pure translations)
for _ in range(3):
    m=mean_butt()
    err=mean_tgt-m
    if err.length<0.0005: break
    place_pelvis(err)
ROOT_LOC=root.location.copy()
PELVIS_LOC=pb.location.copy()
mb_final=mean_butt()
bz_final=m_butt()
print(f"solved: butt_mean=({mb_final.x:.3f},{mb_final.y:.3f},{mb_final.z:.3f}) butt_min_z={bz_final:.4f} target={BUTT_Z:.4f}", flush=True)

# back solve (pitch to close gap)
px=mb_final.x
BACKQ={}
gap=m_back(px)
if gap is not None and gap>0.015:
    ang=math.radians(min(gap*120.0,10.0)); dq=Quaternion((0,1,0),-ang)
    for bn in ('pelvis','spine_1','spine_2'):
        qpb=rig.pose.bones[bn]; par=qpb.parent
        Wpar=W_ROOT if (par and par.name=='root') else (Wdes[par.name] if (par and par.name in Wdes) else TGT_RESTW['root'])
        Wold=Wdes.get(bn,TGT_RESTW[bn])
        qn=(Wpar@M_REL[bn]).inverted()@(dq@Wold)
        qpb.rotation_quaternion=qn; BACKQ[bn]=qn
print(f"back gap={gap}", flush=True)

# legs: analytic two-bone IK
bpy.context.view_layer.update()
d=eval_now(); rr=rig.evaluated_get(d); mw=rig.matrix_world
thigh_len=rig.data.bones['thigh_L'].length; shin_len=rig.data.bones['shin_L'].length
LEGQ={}
for side in ('L','R'):
    ts=f"_{side}"
    H=(mw@rr.pose.bones[f'thigh{ts}'].head).copy()
    T=Vector((H.x-0.13, H.y+(0.075 if side=='L' else -0.075), FLOOR_Z+0.035))
    a,b=thigh_len,shin_len
    dl=max(min((T-H).length,a+b-1e-4),abs(a-b)+1e-4)
    x=(a*a-b*b+dl*dl)/(2*dl); h=math.sqrt(max(a*a-x*x,1e-8))
    axis=(T-H).normalized()
    fwd=Vector((-1,0,0)); bend=(fwd-fwd.dot(axis)*axis).normalized()
    K=H+axis*x+bend*h
    td=(K-H).normalized(); sd=(T-K).normalized()
    tr=(TGT_RESTW[f'thigh{ts}']@Vector((0,1,0))).normalized()
    sr=(TGT_RESTW[f'shin{ts}']@Vector((0,1,0))).normalized()
    Wt=(tr.rotation_difference(td))@TGT_RESTW[f'thigh{ts}']
    Ws_=(sr.rotation_difference(sd))@TGT_RESTW[f'shin{ts}']
    Wpt=(mw@rr.pose.bones['pelvis'].matrix).to_3x3().to_quaternion()
    qt=(Wpt@M_REL[f'thigh{ts}']).inverted()@Wt
    qs=(Wt@M_REL[f'shin{ts}']).inverted()@Ws_
    rig.pose.bones[f'thigh{ts}'].rotation_quaternion=qt
    rig.pose.bones[f'shin{ts}'].rotation_quaternion=qs
    LEGQ[f'thigh{ts}']=qt; LEGQ[f'shin{ts}']=qs
print("legs IK done", flush=True)
bz_verify=m_butt()
print(f"FINAL verify: butt_z={bz_verify:.4f} target={BUTT_Z:.4f}", flush=True)

# ---- APPLY to all frames
src.animation_data.action=src_act
n=SRC_F1-SRC_F0+1
for i in range(n):
    df=DST_F0+i
    pose_frame(i)
    root.location=ROOT_LOC
    pb.location=PELVIS_LOC
    for bn,q in BACKQ.items(): rig.pose.bones[bn].rotation_quaternion=q
    for bn,q in LEGQ.items(): rig.pose.bones[bn].rotation_quaternion=q
    for b in rig.pose.bones:
        b.keyframe_insert(data_path="rotation_quaternion",frame=df)
    root.keyframe_insert(data_path="location",frame=df)
    pb.keyframe_insert(data_path="location",frame=df)
    if i%20==0: print(f"  baked {i+1}/{n}",flush=True)
src.animation_data.action=None

cape=bpy.data.objects.get("CapeJones_Cape")
if cape: cape.hide_viewport=True; cape.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED",OUT_BLEND,flush=True)

# ---- render proofs (Cycles)
scn.render.engine='CYCLES'; scn.cycles.samples=24
scn.render.resolution_x=960; scn.render.resolution_y=540; scn.render.resolution_percentage=100
scn.frame_set(DST_F0+MID); bpy.context.view_layer.update()
cam=scn.camera
def look_at(eye,target):
    d=Vector(target)-Vector(eye); cam.location=eye
    cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update()
# front: from -X looking at chair (chair faces -X, sitter faces -X into room)
look_at((1.35,2.067,0.85),(3.05,2.067,0.45))
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_front_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("front rendered",flush=True)
# three-quarter
look_at((1.75,1.15,1.15),(3.05,2.067,0.45))
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_threeq_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("threeq rendered",flush=True)
print("DONE",flush=True)
