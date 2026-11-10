"""Dump rest/posed positions + needed group weights + bone delta quats to npz.
Usage: blender -b file.blend --python dump_pose.py -- out.npz POSE_SPEC
POSE_SPEC: bone,axis,deg;bone,axis,deg  (axis as x,y,z)
"""
import bpy, math, os, sys
import numpy as np
from mathutils import Quaternion, Vector

args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
spec = args[1] if len(args) > 1 else ""

scn = bpy.context.scene
rig = bpy.data.objects['CapeJones_Rig']
body = bpy.data.objects['CapeJones_Body']
root = rig.pose.bones['root']
for prop in ['ik_arm_L', 'ik_arm_R', 'ik_leg_L', 'ik_leg_R']:
    if prop in root:
        root[prop] = 0.0
for pb in rig.pose.bones:
    pb.rotation_mode = 'XYZ'
    pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0)
    pb.scale = (1, 1, 1)

for item in spec.split(";"):
    if not item.strip():
        continue
    bname, axis, deg = item.split(",")
    ax = tuple(float(v) for v in axis.split(":"))
    pb = rig.pose.bones[bname]
    q_rest = pb.bone.matrix_local.to_quaternion()
    q_delta = Quaternion(Vector(ax), math.radians(float(deg)))
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = q_rest.inverted() @ q_delta @ q_rest

bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
deps.update()
eval_body = deps.objects.get('CapeJones_Body')
mesh = eval_body.to_mesh()
n = len(mesh.vertices)
posed = np.empty(n * 3, dtype=np.float32)
posed_n = np.empty(n * 3, dtype=np.float32)
mesh.vertices.foreach_get("co", posed)
mesh.vertices.foreach_get("normal", posed_n)
eval_body.to_mesh_clear()

rest = np.empty(n * 3, dtype=np.float32)
body.data.vertices.foreach_get("co", rest)

data = {
    "rest": rest.reshape(-1, 3),
    "posed": posed.reshape(-1, 3),
    "posed_normal": posed_n.reshape(-1, 3),
}
# needed group weights
want = ["upperarm_L", "forearm_L", "upperarm_R", "forearm_R",
        "jaw", "head", "neck_1", "neck_2", "hand_L", "hand_R", "chest"]
vg = body.vertex_groups
idx_of = {gname: vg[gname].index for gname in want if gname in vg}
inv = {idx: gname for gname, idx in idx_of.items()}
warr = {gname: np.zeros(n, dtype=np.float32) for gname in idx_of}
for v in body.data.vertices:
    i = v.index
    for g in v.groups:
        gname = inv.get(g.group)
        if gname is not None:
            warr[gname][i] = g.weight
for gname, w in warr.items():
    data["w_" + gname] = w
    print(f"group {gname}: nonzero={(w>0).sum()}", flush=True)

# bone delta quats (rest->posed, armature space) for key bones
for bname in ["upperarm_L", "forearm_L", "upperarm_R", "forearm_R",
              "jaw", "head", "neck_1", "neck_2", "chest"]:
    pb = rig.pose.bones.get(bname)
    if pb:
        q_rest = pb.bone.matrix_local.to_quaternion()
        q_posed = pb.matrix.to_quaternion()
        qd = q_rest.inverted() @ q_posed
        data["q_" + bname] = np.array([qd.w, qd.x, qd.y, qd.z], dtype=np.float32)

np.savez_compressed(out, **data)
print("SAVED", out, n, "verts", flush=True)
