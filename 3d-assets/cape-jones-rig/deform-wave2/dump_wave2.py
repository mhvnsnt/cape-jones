"""Wave-2 deform audit: dump rest + full-range pose positions to /tmp/deform2/.
Usage: blender -b cape_jones_rigged_w5r_clean.blend --python dump_wave2.py
Sweeps: shoulders fwd/side, hips, knees, wrists, ankles, spine bend/twist (L+R).
"""
import bpy, math, os, sys
import numpy as np
from mathutils import Quaternion, Vector

OUT = "/home/hatch/workspace/cj-deform-audit/3d-assets/cape-jones-rig/deform-wave2/scratch"
os.makedirs(OUT, exist_ok=True)

rig = bpy.data.objects['CapeJones_Rig']
body = bpy.data.objects['CapeJones_Body']

def reset_pose():
    for pb in rig.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
        pb.scale = (1, 1, 1)
    root = rig.pose.bones['root']
    for prop in ['ik_arm_L', 'ik_arm_R', 'ik_leg_L', 'ik_leg_R']:
        if prop in root:
            root[prop] = 0.0

def set_world_rot(pb_name, axis, deg):
    pb = rig.pose.bones[pb_name]
    q_rest = pb.bone.matrix_local.to_quaternion()
    q_delta = Quaternion(Vector(axis), math.radians(deg))
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = q_rest.inverted() @ q_delta @ q_rest

# joint sweep specs: name -> list of (fk_bone, world_axis, deg)
SPECS = {
    "shoulderL_fwd":  [("upperarm_fk_L", (0, 0, 1), -90)],
    "shoulderR_fwd":  [("upperarm_fk_R", (0, 0, 1),  90)],
    "shoulderL_side": [("upperarm_fk_L", (0, 1, 0), -80)],
    "shoulderR_side": [("upperarm_fk_R", (0, 1, 0),  80)],
    "hipL_flex":      [("thigh_fk_L", (1, 0, 0),  90)],
    "hipR_flex":      [("thigh_fk_R", (1, 0, 0),  90)],
    "kneeL":          [("shin_fk_L", (1, 0, 0), -120)],
    "kneeR":          [("shin_fk_R", (1, 0, 0), -120)],
    "wristL_bend":    [("hand_fk_L", (0, 0, 1), -60)],
    "wristR_bend":    [("hand_fk_R", (0, 0, 1),  60)],
    "wristL_side":    [("hand_fk_L", (1, 0, 0), -35)],
    "ankleL":         [("foot_fk_L", (1, 0, 0),  30)],
    "ankleR":         [("foot_fk_R", (1, 0, 0),  30)],
    "spine_fwd":      [("spine_1", (1, 0, 0),  35)],
    "spine_twist":    [("spine_1", (0, 0, 1),  35)],
}

DEFORM_BONES = ["clavicle_L", "clavicle_R", "upperarm_L", "upperarm_R",
                "forearm_L", "forearm_R", "hand_L", "hand_R", "chest",
                "spine_1", "spine_2", "pelvis", "thigh_L", "thigh_R",
                "shin_L", "shin_R", "foot_L", "foot_R", "toe_L", "toe_R",
                "neck_1", "neck_2", "head", "jaw"]

def snapshot(pose_name):
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
    data = {"posed": posed.reshape(-1, 3), "posed_normal": posed_n.reshape(-1, 3)}
    # bone delta quats (rest -> posed) for all deform bones
    for bname in DEFORM_BONES:
        pb = rig.pose.bones.get(bname)
        if pb:
            qr = pb.bone.matrix_local.to_quaternion()
            qp = pb.matrix.to_quaternion()
            qd = qr.inverted() @ qp
            data["q_" + bname] = np.array([qd.w, qd.x, qd.y, qd.z], dtype=np.float32)
    np.savez_compressed(os.path.join(OUT, pose_name + ".npz"), **data)
    print(f"SAVED {pose_name}: {n} verts", flush=True)

# ---- rest ----
reset_pose()
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
deps.update()
n = len(body.data.vertices)
rest = np.empty(n * 3, dtype=np.float32)
body.data.vertices.foreach_get("co", rest)
rest = rest.reshape(-1, 3)

data = {"rest": rest}
vg = body.vertex_groups
idx_of = {g: vg[g].index for g in DEFORM_BONES if g in vg}
inv = {i: g for g, i in idx_of.items()}
warr = {g: np.zeros(n, dtype=np.float32) for g in idx_of}
for v in body.data.vertices:
    i = v.index
    for g in v.groups:
        gn = inv.get(g.group)
        if gn:
            warr[gn][i] = g.weight
for g, w in warr.items():
    data["w_" + g] = w
np.savez_compressed(os.path.join(OUT, "rest.npz"), **data)
print(f"SAVED rest: {n} verts, {len(warr)} groups", flush=True)

# ---- faces (tris+quads) for adjacency ----
mesh0 = body.data
ploop = np.empty(len(mesh0.polygons) * 3, dtype=np.int32)
# simpler: loop tris/quads
tris, quads = [], []
for p in mesh0.polygons:
    vs = list(p.vertices)
    if len(vs) == 3:
        tris.append(vs)
    elif len(vs) == 4:
        quads.append(vs)
np.savez_compressed(os.path.join(OUT, "faces.npz"),
                    tris=np.array(tris, dtype=np.int64),
                    quads=np.array(quads, dtype=np.int64))
print(f"SAVED faces: {len(tris)} tris {len(quads)} quads", flush=True)

# ---- poses ----
for name, spec in SPECS.items():
    reset_pose()
    for bname, axis, deg in spec:
        set_world_rot(bname, axis, deg)
    snapshot(name)

print("ALL DONE", flush=True)
