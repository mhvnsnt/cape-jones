"""AUTO-SEAT v2 — measurement-driven contact solver (simplified, robust).

v1 hung on per-frame mesh evals. v2: solve contacts ONCE on the middle seated
frame, apply corrections + mocap to all frames. No per-frame mesh evaluation.

Root cause of all prior failures (measured, not guessed):
  seat surface z=0.230 (raycast), NOT 0.370 (bounding box). All prior lanes
  floated him 10-14cm above the real seat.

Method (all numbers measured at runtime):
  1. MEASURE chair: seat top, backrest plane, floor (raycasts).
  2. RETARGET mocap (CMU 113_15) with proven world-space math.
  3. SOLVE on middle frame:
     - butt->seat: linear solve via calibration matrix (rigid for pelvis verts)
     - back->backrest: pitch solve
     - feet->floor: analytic two-bone IK
  4. APPLY solved corrections to all frames + mocap motion. Keyframe. Render.
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

# ---- mocap import
bpy.ops.import_scene.fbx(filepath=FBX)
src = next(o for o in bpy.data.objects if o.type=='ARMATURE' and o != rig)
src_act = src.animation_data.action
src.animation_data.action = None
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
SRC_REST = {b.name: (src.matrix_world @ b.matrix_local).to_3x3().to_quaternion() for b in src.data.bones}
ankle = min((src.matrix_world @ b.head_local).z for b in src.data.bones if 'Foot' in b.name)
headb = src.data.bones['head']
SRC_H = (src.matrix_world @ headb.head_local).z + headb.length - ankle
print(f"SRC_H={SRC_H:.2f}", flush=True)
TGT_RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion() for b in rig.data.bones}
M_REL = {}
for b in rig.data.bones:
    M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion() if b.parent is None else \
        (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()

M = [
 ("hip",    [("pelvis", 1.0)]),
 ("abdomen",[("spine_fk_1", 0.5), ("spine_fk_2", 0.5)]),
 ("chest",  [("spine_fk_3", 0.34), ("spine_fk_4", 0.33), ("chest_fk", 0.33)]),
 ("neck",   [("neck_1", 0.5), ("neck_2", 0.5)]),
 ("head",   [("head", 1.0)]),
 ("lCollar",[("clavicle_L", 1.0)]), ("rCollar",[("clavicle_R", 1.0)]),
 ("lShldr", [("upperarm_fk_L", 1.0)]), ("rShldr",[("upperarm_fk_R", 1.0)]),
 ("lForeArm",[("forearm_fk_L", 1.0)]), ("rForeArm",[("forearm_fk_R", 1.0)]),
 ("lHand",  [("hand_fk_L", 1.0)]), ("rHand",[("hand_fk_R", 1.0)]),
 ("lThigh", [("thigh_fk_L", 1.0)]), ("rThigh",[("thigh_fk_R", 1.0)]),
 ("lShin",  [("shin_fk_L", 1.0)]), ("rShin",[("shin_fk_R", 1.0)]),
 ("lFoot",  [("foot_fk_L", 1.0)]), ("rFoot",[("foot_fk_R", 1.0)]),
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
act = bpy.data.actions.new("autoseat_v2")
if not rig.animation_data: rig.animation_data_create()
rig.animation_data.action = act

def eval_now():
    bpy.context.view_layer.update()
    return bpy.context.evaluated_depsgraph_get()

# calibration matrices
def calibrate(bone):
    bone.location=Vector((0,0,0)); bpy.context.view_layer.update()
    r0=(rig.matrix_world @ bone.head).copy(); cols=[]
    for i in range(3):
        e=Vector((0,0,0)); e[i]=1.0; bone.location=e; bpy.context.view_layer.update()
        cols.append((rig.matrix_world @ bone.head).copy()-r0)
    A=Matrix((cols[0],cols[1],cols[2])).transposed()
    bone.location=Vector((0,0,0)); bpy.context.view_layer.update()
    return A
A_root=calibrate(root); A_pelv=calibrate(pb)
print(f"calib det: {A_root.determinant():.3f} {A_pelv.determinant():.3f}", flush=True)
for _ in range(3):
    p=(rig.matrix_world @ pb.head).copy()
    err=Vector((SEAT_C.x-p.x, SEAT_C.y-p.y, 0))
    if err.length<0.001: break
    root.location += A_root.inverted() @ err; bpy.context.view_layer.update()
ROOT_LOC=root.location.copy()
print(f"root placed", flush=True)

# proxy for fast contact measurement
body=bpy.data.objects.get("CapeJones_Body")
bpy.context.view_layer.objects.active=body; body.select_set(True)
bpy.ops.object.duplicate()
proxy=bpy.context.view_layer.objects.active; proxy.name="BodyProxy"
proxy.hide_viewport=True; proxy.hide_render=True
dec=proxy.modifiers.new("DECIMATE",'DECIMATE'); dec.ratio=0.04
bpy.context.view_layer.objects.active=proxy
bpy.ops.object.modifier_apply(modifier=dec.name)
body.select_set(False); proxy.select_set(False)
print(f"proxy: {len(proxy.data.vertices)} verts", flush=True)
pelv_gi=proxy.vertex_groups["pelvis"].index
BUTT_IDX=[v.index for v in proxy.data.vertices for g in v.groups if g.group==pelv_gi and g.weight>0.6]
BACK_GNS=[gn for gn in ("spine_1","spine_2","spine_3","spine_4","chest") if gn in proxy.vertex_groups]
BACK_GIS={proxy.vertex_groups[gn].index for gn in BACK_GNS}

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
    root.location=ROOT_LOC; pb.location=Vector((0,0,0))
    return Wdes

# ---- SOLVE on middle frame
MID=(SRC_F1-SRC_F0)//2
src.animation_data.action=src_act
Wdes=pose_frame(MID)
px=(rig.matrix_world@pb.head).x
# butt
bz=m_butt()
DLOC=Vector((0,0,0))
if bz is not None:
    DLOC=A_pelv.inverted()@Vector((0,0,(BUTT_Z-bz)))
    pb.location+=DLOC
print(f"solve: butt_z={bz:.4f} dloc_z applied", flush=True)
# back
BACKQ={}
gap=m_back(px)
if gap is not None and gap>0.015:
    ang=math.radians(min(gap*120.0,10.0)); dq=Quaternion((0,1,0),-ang)
    for bn in ('pelvis','spine_fk_1','spine_fk_2'):
        qpb=rig.pose.bones[bn]; par=qpb.parent
        Wpar=W_ROOT if (par and par.name=='root') else (Wdes[par.name] if (par and par.name in Wdes) else TGT_RESTW['root'])
        Wold=Wdes.get(bn,TGT_RESTW[bn])
        qn=(Wpar@M_REL[bn]).inverted()@(dq@Wold)
        qpb.rotation_quaternion=qn; BACKQ[bn]=qn
print(f"solve: back gap={gap}", flush=True)
# legs: analytic two-bone IK (armature eval only — proxy mesh skipped by using rig directly)
bpy.context.view_layer.update()
d=eval_now(); rr=rig.evaluated_get(d); mw=rig.matrix_world
thigh_len=rig.data.bones['thigh_fk_L'].length; shin_len=rig.data.bones['shin_fk_L'].length
LEGQ={}
for side in ('L','R'):
    ts=f"_{side}"
    H=(mw@rr.pose.bones[f'thigh_fk{ts}'].head).copy()
    T=Vector((H.x-0.13, H.y+(0.075 if side=='L' else -0.075), FLOOR_Z+0.035))
    a,b=thigh_len,shin_len
    dl=max(min((T-H).length,a+b-1e-4),abs(a-b)+1e-4)
    x=(a*a-b*b+dl*dl)/(2*dl); h=math.sqrt(max(a*a-x*x,1e-8))
    axis=(T-H).normalized()
    fwd=Vector((-1,0,0)); bend=(fwd-fwd.dot(axis)*axis).normalized()
    K=H+axis*x+bend*h
    td=(K-H).normalized(); sd=(T-K).normalized()
    tr=(TGT_RESTW[f'thigh_fk{ts}']@Vector((0,1,0))).normalized()
    sr=(TGT_RESTW[f'shin_fk{ts}']@Vector((0,1,0))).normalized()
    Wt=(tr.rotation_difference(td))@TGT_RESTW[f'thigh_fk{ts}']
    Ws_=(sr.rotation_difference(sd))@TGT_RESTW[f'shin_fk{ts}']
    Wpt=(mw@rr.pose.bones['pelvis'].matrix).to_3x3().to_quaternion()
    qt=(Wpt@M_REL[f'thigh_fk{ts}']).inverted()@Wt
    qs=(Wt@M_REL[f'shin_fk{ts}']).inverted()@Ws_
    rig.pose.bones[f'thigh_fk{ts}'].rotation_quaternion=qt
    rig.pose.bones[f'shin_fk{ts}'].rotation_quaternion=qs
    LEGQ[f'thigh_fk{ts}']=qt; LEGQ[f'shin_fk{ts}']=qs
print("solve: legs IK done", flush=True)
# verify butt after all solves
bz2=m_butt()
print(f"verify: butt_z={bz2:.4f} target={BUTT_Z:.4f}", flush=True)

# ---- APPLY to all frames: mocap + solved corrections
src.animation_data.action=src_act
n=SRC_F1-SRC_F0+1
for i in range(n):
    df=DST_F0+i
    pose_frame(i)
    pb.location+=DLOC
    for bn,q in BACKQ.items(): rig.pose.bones[bn].rotation_quaternion=q
    for bn,q in LEGQ.items(): rig.pose.bones[bn].rotation_quaternion=q
    for b in rig.pose.bones:
        if b.name in [t for _,tl in M for t,_ in tl] or b.name=='pelvis':
            b.keyframe_insert(data_path="rotation_quaternion",frame=df)
    pb.keyframe_insert(data_path="location",frame=df)
    root.location=ROOT_LOC
    root.keyframe_insert(data_path="location",frame=df)
    root.keyframe_insert(data_path="rotation_quaternion",frame=df)
    if i%20==0: print(f"  baked {i+1}/{n}",flush=True)
src.animation_data.action=None

cape=bpy.data.objects.get("CapeJones_Cape")
if cape: cape.hide_viewport=True; cape.hide_render=True
proxy.hide_viewport=True; proxy.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED",OUT_BLEND,flush=True)

# ---- render proofs
scn.render.engine='CYCLES'; scn.cycles.samples=24
scn.render.resolution_x=960; scn.render.resolution_y=540; scn.render.resolution_percentage=100
scn.frame_set(DST_F0+MID); bpy.context.view_layer.update()
cam=scn.camera
def look_at(eye,target):
    d=Vector(target)-Vector(eye); cam.location=eye
    cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update()
cc=(3.06,2.067,0.45)
look_at((1.4,2.067,0.9),cc)
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_front_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("front rendered",flush=True)
look_at((1.7,1.2,1.1),cc)
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_threeq_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("threeq rendered",flush=True)
print("DONE",flush=True)
