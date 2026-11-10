"""MOCAP SIT v2 — world-space retarget of CMU 113_15 ('sit in chair and get up')
onto the 94-bone Cape Jones rig, with contact solving (butt -> seat).

Correct retarget math:
  W_desired[t] = TGT_REST_WORLD[t] @ (SRC_REST_WORLD[s]^-1 @ SRC_WORLD[s](f))
  R_local[t]   = (W_parent_world @ M_local[t])^-1 @ W_desired[t]
where M_local[t] is the bone's rest local rotation. (v1 omitted M_local.)

Source faces -Y (verified from foot bone direction); rig faces -Y. No yaw fix needed.

Run: blender -b 3d-assets/living_room.blend --python mocap_retarget.py
Outputs: proof/sitting_mocap.blend
"""
import bpy, math
from mathutils import Matrix, Quaternion, Vector

FBX = "/home/hatch/workspace/mocap-sit/113_15.fbx"
SRC_F0, SRC_F1 = 70, 150
DST_F0 = 1
OUT_BLEND = "/home/hatch/workspace/wt-mocapsit/proof/sitting_mocap.blend"
BUTT_TARGET = Vector((3.120, 2.067, 0.368))
SEAT_Z = lambda x: 0.0486 * x + 0.2146
TARGET_HEIGHT = 0.925
ROOTQ = Quaternion((0, 0, 1), math.radians(-90.0))   # rig forward -Y -> world -X

rig = bpy.data.objects.get("CapeJones_Rig")
assert rig and len(rig.data.bones) == 94
for b in rig.pose.bones:
    b.rotation_mode = 'QUATERNION'
if rig.animation_data:
    rig.animation_data.action = None
print("cleared rig action")

bpy.ops.import_scene.fbx(filepath=FBX)
src = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o != rig)
src_act = src.animation_data.action
print("source:", src.name, int(src_act.frame_range[1]), "frames")

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
MOTION_SCALE = TARGET_HEIGHT / SRC_H
print(f"SRC_H={SRC_H:.2f} MOTION_SCALE={MOTION_SCALE:.4f}")
TGT_RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion()
             for b in rig.data.bones}
# parent-relative rest rotations (Blender composes: parent_world @ M_rel @ basis)
M_REL = {}
for b in rig.data.bones:
    if b.parent is None:
        M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion()
    else:
        M_REL[b.name] = (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()
PELVIS_HEAD_LOCAL = rig.data.bones['pelvis'].head_local.copy()
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
print("missing:", missing if missing else "none")
assert not missing

root = rig.pose.bones['root']
root.rotation_mode = 'QUATERNION'
root.rotation_quaternion = ROOTQ
W_ROOT = TGT_RESTW['root'] @ ROOTQ   # root world rotation (rig at origin)

# pelvis location: direct (head_world = root.loc + W_ROOT @ (HEAD_LOCAL + M_REL_rot @ L))
M_PELVIS_INV = M_REL['pelvis'].inverted()
act = bpy.data.actions.new("mocap_sit_113_15")
if not rig.animation_data:
    rig.animation_data_create()
rig.animation_data.action = act

body_pre = bpy.data.objects.get("CapeJones_Body")
cape_pre = bpy.data.objects.get("CapeJones_Cape")
for o in (body_pre, cape_pre):
    if o: o.hide_viewport = True

def scaled(q, w):
    return q if w == 1.0 else Quaternion(q.axis, q.angle * w)

n = SRC_F1 - SRC_F0 + 1
hip_rest_w = SRC_REST_LOC['hip']
pb = rig.pose.bones['pelvis']
PELVIS_SEAT_Z = 0.389
PELVIS_REST_Z = PELVIS_HEAD_LOCAL.z
_hip_sum = Vector((0,0,0))
for _f in range(SRC_F0, SRC_F1+1):
    scn.frame_set(_f); bpy.context.view_layer.update()
    _hip_sum += (src.matrix_world @ src.pose.bones['hip'].head)
HIP_MEAN = _hip_sum / n
print(f"HIP_MEAN z={HIP_MEAN.z:.2f} PELVIS_REST_Z={PELVIS_REST_Z:.3f}")
for i in range(n):
    sf = SRC_F0 + i
    df = DST_F0 + i
    scn.frame_set(sf)
    bpy.context.view_layer.update()
    Ws = {b.name: (src.matrix_world @ b.matrix).to_3x3().to_quaternion()
          for b in src.pose.bones}
    hip_w = (src.matrix_world @ src.pose.bones['hip'].head).copy()
    # desired world rotations
    Wdes = {}
    for (sname, targets) in M:
        D = SRC_REST[sname].inverted() @ Ws[sname]
        if sname in ('neck', 'head'):
            D = scaled(D, 0.5)
        for (tname, w) in targets:
            Wdes[tname] = TGT_RESTW[tname] @ scaled(D, w)
    # solve locals in hierarchy order (M is ordered parents-first)
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
                # undriven parent: use its rest world (shouldn't happen for our chains)
                Wpar = TGT_RESTW[par.name]
            qpb.rotation_quaternion = (Wpar @ M_REL[tname]).inverted() @ Wdes[tname]
            qpb.keyframe_insert(data_path="rotation_quaternion", frame=df)
    dloc = Vector((0, 0, PELVIS_SEAT_Z - PELVIS_REST_Z))
    pb.location = dloc
    pb.keyframe_insert(data_path="location", frame=df)
    if i % 20 == 0:
        print(f"  retarget {i+1}/{n}", flush=True)

for df in range(DST_F0, DST_F0 + n):
    root.keyframe_insert(data_path="rotation_quaternion", frame=df)
print("retarget done")

# ---- placement: pelvis-bone anchored (take-3 proved pelvis_z=0.389) ----
REF = DST_F0 + n // 2
# The mesh-based solve was aligning the wrong verts; anchor by the bone and verify by eye.
scn.frame_set(REF)
bpy.context.view_layer.update()
root.location = Vector((BUTT_TARGET.x, BUTT_TARGET.y, 0.0))
bpy.context.view_layer.update()
# report pelvis + feet for sanity
_pz = (rig.matrix_world @ rig.pose.bones['pelvis'].head).z
print(f"PELVIS_Z={_pz:.4f} (target ~0.389)")
loc = root.location.copy()
for df in range(DST_F0, DST_F0 + n):
    root.location = loc
    root.keyframe_insert(data_path="location", frame=df)
# feet check
body = bpy.data.objects.get('CapeJones_Body')
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
bm = body.evaluated_get(deps); mesh = bm.to_mesh()
gF = {body.vertex_groups.get(x).index for x in ('foot_L','foot_R') if body.vertex_groups.get(x)}
fz = [(bm.matrix_world @ v.co).z for v in mesh.vertices if any(g.group in gF for g in v.groups)]
bm.to_mesh_clear()
print(f"FEET: minz={min(fz):.4f} maxz={max(fz):.4f}" if fz else "FEET: no verts")

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND)
