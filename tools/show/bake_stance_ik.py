"""Direction-based stance bake (cape-jones repo version).
Re-bakes ep1_cape_stance.glb from gunjack t3_stance_b.json (wh-anim/1).

Why this exists: bake_cape_t3.py's orientation retarget lands the stance
arms wrong (repo clip played L upper 17-31deg from down, R upper
130-144deg) while the source guard has both arms raised. The orientation
map alone does not fix it (a segment-correct orientation map was tested:
L upper went to rest ~80deg, R upper stayed ~106-117deg). Root cause:
orientation retarget fails where T3 and Cape bone rolls differ — a bone
can twist about its own axis without moving its segment, so matching
orientations does not match segment directions.

Method: torso/legs/clavicle/hand keep the orientation bake (which already
matches source tilt/roll); ARMS are solved from source segment
DIRECTIONS via motion-chain FK (Root->Hips->Spine->Chest->Shoulder->
Arm->ForeArm->Hand; joints: Arm = shoulder joint, ForeArm = elbow,
Hand = wrist). Each arm bone's world orientation = shortest-arc rotation
from its rest world direction to the desired direction, composed onto
its rest orientation (minimal twist change). Verified by measurement:
output matches source FK to ~1deg on sampled frames (see SOURCES.md
stance re-bake note).

Usage: blender -b --python bake_stance_ik.py -- <outdir>
Paths follow bake_cape_t3.py conventions (local wh-repo checkout +
scratch show GLB).
"""
import bpy, json, sys
from mathutils import Quaternion, Vector

OUTDIR = sys.argv[sys.argv.index("--") + 1]
import os
os.makedirs(OUTDIR, exist_ok=True)

GUN = "/home/hatch/workspace/wh-repo/game/assets/anim/t3/gunjack/"
TJ = json.load(open(GUN + "t3_stance_b.json"))
SK = json.load(open(GUN + "skeleton.json"))
REST = {j["name"]: Vector(j["rest"]) for j in SK["joints"]}
PARENTS = {"Root": None, "Hips": "Root", "Spine": "Hips", "Chest": "Spine",
    "Neck": "Chest", "Head": "Neck",
    "LeftShoulder": "Chest", "LeftArm": "LeftShoulder", "LeftForeArm": "LeftArm", "LeftHand": "LeftForeArm",
    "RightShoulder": "Chest", "RightArm": "RightShoulder", "RightForeArm": "RightArm", "RightHand": "RightForeArm",
    "LeftUpLeg": "Hips", "LeftLeg": "LeftUpLeg", "LeftFoot": "LeftLeg", "LeftToeBase": "LeftFoot",
    "RightUpLeg": "Hips", "RightLeg": "RightUpLeg", "RightFoot": "RightLeg", "RightToeBase": "RightFoot"}
OMAP = {
 "Hips": ["pelvis"],
 "Spine": ["spine_1", "spine_2"],
 "Chest": ["spine_3", "spine_4", "chest"],
 "Neck": ["neck_1", "neck_2"],
 "Head": ["head"],
 "LeftUpLeg": ["thigh_L"], "LeftLeg": ["shin_L"], "LeftFoot": ["foot_L"], "LeftToeBase": ["toe_L"],
 "RightUpLeg": ["thigh_R"], "RightLeg": ["shin_R"], "RightFoot": ["foot_R"], "RightToeBase": ["toe_R"],
}
QG = Quaternion((0.7071067811865476, 0.7071067811865476, 0.0, 0.0))  # Rx(+90), wxyz
SCALE = 0.409 / 1.00022
ROOT_REST = Vector((0.0, 1.00022, 0.0))

def q_xyzw(v):
    q = Quaternion((v[3], v[0], v[1], v[2])); q.normalize()
    return -q if q.w < 0 else q

def shortest_arc(a, b):
    a = a.normalized(); b = b.normalized()
    d = a.dot(b)
    if d > 0.999999:
        return Quaternion((1.0, 0.0, 0.0, 0.0))
    if d < -0.999999:
        axis = Vector((1.0, 0.0, 0.0)) if abs(a.x) < 0.9 else Vector((0.0, 1.0, 0.0))
        axis = (axis - a * axis.dot(a)).normalized()
        return Quaternion((0.0, axis.x, axis.y, axis.z))
    c = a.cross(b)
    q = Quaternion((1.0 + d, c.x, c.y, c.z)); q.normalize()
    return q

bpy.context.scene.render.fps = 30
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/scratch/cj-3d/cape-jones-show.glb")
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'CapeJones_Rig')
for b in rig.pose.bones:
    b.rotation_mode = 'QUATERNION'
for n in ("CapeJones_Body", "CapeJones_Cape"):
    o = bpy.data.objects.get(n)
    if o:
        o.hide_viewport = True; o.hide_render = True
RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion() for b in rig.data.bones}
M_REL = {}
for b in rig.data.bones:
    M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion() if b.parent is None else (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()

n = len(TJ["root_t"])
act = bpy.data.actions.new("ep1_cape_stance")
if not rig.animation_data:
    rig.animation_data_create()
rig.animation_data.action = act

for i in range(n):
    W = {}
    for bn in TJ["bones"]:
        q = q_xyzw(TJ["rot_xyzw"][bn][i]); p = PARENTS[bn]
        W[bn] = (W[p] @ q) if (p and p in W) else q
    rt = Vector(TJ["root_t"][i])
    pos = {"Root": rt, "Chest": rt}
    for j, p in [("LeftShoulder", "Chest"), ("LeftArm", "LeftShoulder"), ("LeftForeArm", "LeftArm"), ("LeftHand", "LeftForeArm"),
                 ("RightShoulder", "Chest"), ("RightArm", "RightShoulder"), ("RightForeArm", "RightArm"), ("RightHand", "RightForeArm")]:
        off = REST[j] - REST[p]
        pos[j] = pos[p] + (W[p] @ off)
    des = {}
    for side, ch in (("L", "Left"), ("R", "Right")):
        sh = pos[f"{ch}Arm"]; el = pos[f"{ch}ForeArm"]; wr = pos[f"{ch}Hand"]
        des[f"upperarm_{side}"] = (QG @ (el - sh)).normalized()
        des[f"forearm_{side}"] = (QG @ (wr - el)).normalized()
    Wdes = {}
    for s, targets in OMAP.items():
        if s not in W:
            continue
        qw = QG @ W[s] @ QG.inverted()
        for t in targets:
            Wdes[t] = qw @ RESTW[t]
    for side, ch in (("L", "Left"), ("R", "Right")):
        qw_sh = QG @ W[f"{ch}Shoulder"] @ QG.inverted()
        Wdes[f"clavicle_{side}"] = qw_sh @ RESTW[f"clavicle_{side}"]
        qw_hand = QG @ W[f"{ch}Hand"] @ QG.inverted()
        Wdes[f"hand_{side}"] = qw_hand @ RESTW[f"hand_{side}"]
    for side in ("L", "R"):
        for bone in (f"upperarm_{side}", f"forearm_{side}"):
            rdir = RESTW[bone] @ Vector((0.0, 1.0, 0.0))
            arc = shortest_arc(rdir, des[bone])
            Wdes[bone] = arc @ RESTW[bone]
    order = ["pelvis", "spine_1", "spine_2", "spine_3", "spine_4", "chest",
             "neck_1", "neck_2", "head",
             "clavicle_L", "upperarm_L", "forearm_L", "hand_L",
             "clavicle_R", "upperarm_R", "forearm_R", "hand_R",
             "thigh_L", "shin_L", "foot_L", "toe_L",
             "thigh_R", "shin_R", "foot_R", "toe_R"]
    for t in order:
        if t not in Wdes:
            continue
        pb = rig.pose.bones[t]; par = pb.parent
        Wpar = Quaternion() if par is None else (Wdes[par.name] if par.name in Wdes else RESTW[par.name])
        pb.rotation_quaternion = (Wpar @ M_REL[t]).inverted() @ Wdes[t]
        pb.keyframe_insert(data_path="rotation_quaternion", frame=i)
    d = rt - ROOT_REST
    moved = Vector((d.x, -d.z, d.y)) * SCALE
    pb = rig.pose.bones["pelvis"]
    pb.location = Vector((moved.x, moved.z, -moved.y))
    pb.keyframe_insert(data_path="location", frame=i)

print(f"BAKED ep1_cape_stance (IK): {n} frames")
bpy.ops.object.select_all(action="DESELECT")
rig.select_set(True); bpy.context.view_layer.objects.active = rig
out = os.path.join(OUTDIR, "ep1_cape_stance.glb")
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_selection=True,
    export_animations=True, export_frame_range=True, export_anim_single_armature=True,
    export_skins=True, export_morph=False, export_cameras=False, export_lights=False)
print("EXPORTED", out, os.path.getsize(out), "bytes")
print("IK BAKE DONE")
