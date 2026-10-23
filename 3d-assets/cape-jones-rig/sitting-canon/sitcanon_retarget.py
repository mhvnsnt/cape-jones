"""SITTING FIX — FULL CANON SCENE PASS.
Loads scene_wave2.blend (full living room + 94-bone rig + wave2 correctives),
clears the stale pose_sit_normal action, retargets CMU 113_15 mocap,
places him by MEASUREMENT (butt on seat, back to wall), solves contact.

Seat: center (2.990, 2.067), top z=0.370. Backrest at x=3.283 -> faces -X.
Armrest z=0.590.
"""
import bpy, math
from mathutils import Matrix, Quaternion, Vector

FBX = "/home/hatch/workspace/wt-sitcanon/3d-assets/animation/mocap-sit/113_15.fbx"
SRC_F0, SRC_F1 = 70, 150
DST_F0 = 1
OUT_BLEND = "/home/hatch/workspace/sitcanon-work/scene_sit.blend"

SEAT_XY = Vector((2.990, 2.067))
SEAT_TOP_Z = 0.370
ROOTQ = Quaternion((0, 0, 1), math.radians(90.0))  # rig -Y -> world -X (faces room)

rig = bpy.data.objects.get("CapeJones_Rig")
assert rig and len(rig.data.bones) == 94, "need 94-bone rig"
for b in rig.pose.bones:
    b.rotation_mode = 'QUATERNION'
    b.location = (0, 0, 0)
if rig.animation_data:
    rig.animation_data.action = None
print("cleared rig action (pose_sit_normal gone)", flush=True)
bpy.context.view_layer.update()

# hide heavy meshes during retarget (depsgraph speed)
for _o in (bpy.data.objects.get("CapeJones_Body"), bpy.data.objects.get("CapeJones_Cape")):
    if _o:
        _o.hide_viewport = True
        _o.hide_render = False
print("body+cape hidden for retarget speed", flush=True)

bpy.ops.import_scene.fbx(filepath=FBX)
src = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o != rig)
src_act = src.animation_data.action
print("source:", src.name, int(src_act.frame_range[1]), "frames", flush=True)

scn = bpy.context.scene
ad = src.animation_data
ad.action = None
bpy.context.view_layer.update()
SRC_REST = {b.name: (src.matrix_world @ b.matrix_local).to_3x3().to_quaternion()
            for b in src.data.bones}
SRC_REST_LOC = {b.name: (src.matrix_world @ b.matrix_local).to_translation()
                for b in src.data.bones}
ankle = min((src.matrix_world @ b.head_local).z for b in src.data.bones if 'Foot' in b.name)
headb = src.data.bones['head']
SRC_H = (src.matrix_world @ headb.head_local).z + headb.length - ankle
MOTION_SCALE = 0.925 / SRC_H
print(f"SRC_H={SRC_H:.2f} MOTION_SCALE={MOTION_SCALE:.4f}", flush=True)
TGT_RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion()
             for b in rig.data.bones}
M_REL = {}
for b in rig.data.bones:
    if b.parent is None:
        M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion()
    else:
        M_REL[b.name] = (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()
ad.action = src_act
bpy.context.view_layer.update()

M = [
 ("hip",        [("pelvis", 1.0)]),
 ("abdomen",    [("spine_fk_1", 0.5), ("spine_fk_2", 0.5)]),
 ("chest",      [("spine_fk_3", 0.34), ("spine_fk_4", 0.33), ("chest_fk", 0.33)]),
 ("neck",       [("neck_1", 0.5), ("neck_2", 0.5)]),
 ("head",       [("head", 1.0)]),
 ("lCollar",    [("clavicle_L", 1.0)]), ("rCollar", [("clavicle_R", 1.0)]),
 ("lShldr",     [("upperarm_fk_L", 1.0)]), ("rShldr", [("upperarm_fk_R", 1.0)]),
 ("lForeArm",   [("forearm_fk_L", 1.0)]), ("rForeArm", [("forearm_fk_R", 1.0)]),
 ("lHand",      [("hand_fk_L", 1.0)]), ("rHand", [("hand_fk_R", 1.0)]),
 ("lThigh",     [("thigh_fk_L", 1.0)]), ("rThigh", [("thigh_fk_R", 1.0)]),
 ("lShin",      [("shin_fk_L", 1.0)]), ("rShin", [("shin_fk_R", 1.0)]),
 ("lFoot",      [("foot_fk_L", 1.0)]), ("rFoot", [("foot_fk_R", 1.0)]),
]
for sside, tside in (("l", "_L"), ("r", "_R")):
    for sseg, fname, n in [("Thumb1","thumb",1),("Thumb2","thumb",2),
                           ("Index1","index",1),("Index2","index",2),
                           ("Mid1","middle",1),("Mid2","middle",2),
                           ("Ring1","ring",1),("Ring2","ring",2),
                           ("Pinky1","pinky",1),("Pinky2","pinky",2)]:
        sn = f"{sside}{sseg}"
        if fname == "thumb":
            M.append((sn, [(f"finger_thumb_{n}{tside}", 1.0)]))
        elif n == 1:
            M.append((sn, [(f"finger_{fname}_1{tside}", 1.0)]))
        else:
            M.append((sn, [(f"finger_{fname}_2{tside}", 0.6),
                           (f"finger_{fname}_3{tside}", 0.4)]))
missing = [(s, t) for s, tl in M for t, w in tl
           if s not in src.data.bones or t not in rig.data.bones]
print("missing:", missing if missing else "none", flush=True)
assert not missing

def scaled(q, w):
    return q if w == 1.0 else Quaternion(q.axis, q.angle * w)

root = rig.pose.bones['root']
root.rotation_mode = 'QUATERNION'
W_ROOT = TGT_RESTW['root'] @ ROOTQ

act = bpy.data.actions.new("mocap_sit_canon")
if not rig.animation_data:
    rig.animation_data_create()
rig.animation_data.action = act

n = SRC_F1 - SRC_F0 + 1
pb = rig.pose.bones['pelvis']
for i in range(n):
    sf = SRC_F0 + i
    df = DST_F0 + i
    scn.frame_set(sf)
    bpy.context.view_layer.update()
    Ws = {b.name: (src.matrix_world @ b.matrix).to_3x3().to_quaternion()
          for b in src.pose.bones}
    Wdes = {}
    for (sname, targets) in M:
        D = SRC_REST[sname].inverted() @ Ws[sname]
        if sname in ('neck', 'head'):
            D = scaled(D, 0.5)
        for (tname, w) in targets:
            Wdes[tname] = TGT_RESTW[tname] @ scaled(D, w)
    for (sname, targets) in M:
        for (tname, w) in targets:
            qpb = rig.pose.bones[tname]
            par = qpb.parent
            if par is None:
                Wpar = Quaternion()
            elif par.name == 'root':
                Wpar = W_ROOT
            elif par.name in Wdes:
                Wpar = Wdes[par.name]
            else:
                Wpar = TGT_RESTW[par.name]
            qpb.rotation_quaternion = (Wpar @ M_REL[tname]).inverted() @ Wdes[tname]
            qpb.keyframe_insert(data_path="rotation_quaternion", frame=df)
    if i % 20 == 0:
        print(f"  retarget {i+1}/{n}", flush=True)

# root rotation -> face -X on all frames
for df in range(DST_F0, DST_F0 + n):
    root.rotation_quaternion = ROOTQ
    root.keyframe_insert(data_path="rotation_quaternion", frame=df)
print("retarget done", flush=True)

# ---- placement: calibrate root location axes numerically ----
def root_world():
    bpy.context.view_layer.update()
    return (rig.matrix_world @ root.matrix).to_translation().copy()

scn.frame_set(DST_F0 + n // 2)
root.location = Vector((0, 0, 0))
bpy.context.view_layer.update()
r0 = root_world()
Acols = []
for i in range(3):
    e = Vector((0, 0, 0)); e[i] = 1.0
    root.location = e
    bpy.context.view_layer.update()
    Acols.append(root_world() - r0)
Aroot = Matrix((Acols[0], Acols[1], Acols[2])).transposed()
target_root = Vector((SEAT_XY.x, SEAT_XY.y, 0.0))
root_loc = Aroot.inverted() @ (target_root - r0)
root.location = root_loc
bpy.context.view_layer.update()
print("root.loc:", tuple(round(v, 3) for v in root_loc),
      "-> world:", tuple(round(v, 3) for v in root_world()), flush=True)

# ---- pelvis: solve butt-mesh to seat ----
# calibrate pelvis location axes
def pelvis_bone_world():
    bpy.context.view_layer.update()
    return (rig.matrix_world @ pb.head).copy()

pb.location = Vector((0, 0, 0))
bpy.context.view_layer.update()
p0 = pelvis_bone_world()
Bcols = []
for i in range(3):
    e = Vector((0, 0, 0)); e[i] = 1.0
    pb.location = e
    bpy.context.view_layer.update()
    Bcols.append(pelvis_bone_world() - p0)
Bpel = Matrix((Bcols[0], Bcols[1], Bcols[2])).transposed()

body = bpy.data.objects.get('CapeJones_Body')
def butt_min_z():
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    bm = body.evaluated_get(deps)
    mesh = bm.to_mesh()
    gP = body.vertex_groups.get('pelvis').index
    gT = {body.vertex_groups.get(x).index for x in ('thigh_L', 'thigh_R') if body.vertex_groups.get(x)}
    zs = []
    for v in mesh.vertices:
        gs = {g.group for g in v.groups}
        if gP in gs or gs & gT:
            w = bm.matrix_world @ v.co
            # butt region: below pelvis bone, near seat
            if w.z < 0.6:
                zs.append(w.z)
    bm.to_mesh_clear()
    return min(zs) if zs else None

# iterate: set pelvis, measure butt, adjust
_body = bpy.data.objects.get("CapeJones_Body")
if _body:
    _body.hide_viewport = False
bpy.context.view_layer.update()

def butt_center_xy():
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    bm = body.evaluated_get(deps)
    mesh = bm.to_mesh()
    gP = body.vertex_groups.get('pelvis').index
    pts = []
    for v in mesh.vertices:
        if any(g.group == gP for g in v.groups):
            w = bm.matrix_world @ v.co
            if w.z < 0.5:
                pts.append(w)
    bm.to_mesh_clear()
    if not pts:
        return None
    return Vector((sum(p.x for p in pts)/len(pts), sum(p.y for p in pts)/len(pts), 0))

# solve butt XY to seat center by shifting root
pb.location = Vector((0, 0, 0))
for it in range(3):
    bc = butt_center_xy()
    if bc is None:
        break
    dx, dy = SEAT_XY.x - bc.x, SEAT_XY.y - bc.y
    print(f"  xy iter {it}: butt=({bc.x:.3f},{bc.y:.3f}) d=({dx:.3f},{dy:.3f})", flush=True)
    if abs(dx) < 0.005 and abs(dy) < 0.005:
        break
    delta_world = Vector((dx, dy, 0))
    root.location = root.location + Aroot.inverted() @ delta_world
    bpy.context.view_layer.update()
for it in range(3):
    bz = butt_min_z()
    print(f"  iter {it}: butt_min_z={bz:.4f} target={SEAT_TOP_Z}", flush=True)
    if bz is None:
        break
    dz = SEAT_TOP_Z - bz
    # move pelvis along its local z that affects world z: use Bpel inverse
    delta_world = Vector((0, 0, dz))
    pb.location = pb.location + Bpel.inverted() @ delta_world
    bpy.context.view_layer.update()

final_bz = butt_min_z()
print(f"FINAL butt_min_z={final_bz:.4f}", flush=True)

# bake root + pelvis to all frames
rl, pl = root.location.copy(), pb.location.copy()
for df in range(DST_F0, DST_F0 + n):
    root.location = rl
    root.keyframe_insert(data_path="location", frame=df)
    pb.location = pl
    pb.keyframe_insert(data_path="location", frame=df)

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND, flush=True)
