#!/usr/bin/env python3
# blender_proof.py — Pinocchio auto-rig proof on the Cape Jones model.
#
# Usage (headless):
#   blender -b --python blender_proof.py -- <mesh.obj> <skeleton.json> <weights.bin> <outdir>
#
# Builds a Blender armature from the Pinocchio skeleton, binds the mesh with
# the Pinocchio skinning weights (vertex groups), applies a test pose
# (elbows + knees + shoulders), and renders proof images.
#
# Bone mapping: Blender bone head == Pinocchio joint position (the pivot the
# Pinocchio transforms rotate about). Bone j tail = first child joint pos,
# or head + (head - parent) * 0.15 for leaf joints.

import bpy, json, math, os, struct, sys

argv = sys.argv[sys.argv.index("--") + 1:]
mesh_path, skel_path, wbin_path, outdir = [os.path.abspath(a) for a in argv[:4]]
os.makedirs(outdir, exist_ok=True)

# Delete the default Cube/Light/Camera FIRST: the 2m default Cube SWALLOWS
# the 0.9m character (this caused every "blank" render in this lane).
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
assert len(bpy.context.scene.objects) == 0, "default objects would hide the character"

# ---------- load rig data ----------
# The skeleton JSON is in OBJ space (Y-up, as Blender wrote it). Blender
# 4.0.2's OBJ importer does NO axis conversion, so below we bake a +90deg X
# rotation into the mesh data; JSON joint (x,y,z) then maps to (x,-z,y).
skel = json.load(open(skel_path))
joints = skel["joints"]
for jt in joints:
    x, y, z = jt["pos"]
    jt["pos"] = [x, -z, y]
nj = len(joints)
with open(wbin_path, "rb") as f:
    nv, nj2 = struct.unpack("ii", f.read(8))
    assert nj2 == nj, f"joint count mismatch {nj2} vs {nj}"
    import array
    w = array.array("f")
    w.fromfile(f, nv * nj)

# ---------- import mesh ----------
before = set(bpy.context.scene.objects)
bpy.ops.wm.obj_import(filepath=mesh_path)
new = [o for o in bpy.context.scene.objects if o not in before and o.type == "MESH"]
assert new, "OBJ import produced no mesh object"
mesh_obj = new[0]
mesh_obj.name = "CJ_Pinocchio"
# Blender 4.0.2's OBJ importer DOES Y-up -> Z-up conversion, via the OBJECT's
# rotation matrix (matrix_world = R_x(+90); vertex data stays in file frame).
# That puts the mesh Z-up in world space, exactly matching the armature frame
# below (JSON joint (x,y,z) -> (x,-z,y), character faces -Y).
# DO NOT bake any extra rotation into the mesh data: a +90deg X data bake
# DOUBLE-applies the conversion and flips the mesh head-down while the bones
# stay head-up -- every pose then mangles (this was the "blob" bug).
# Object rotation stays as the importer set it; the armature modifier
# resolves object transforms correctly, and vertex groups are index-based.
from mathutils import Matrix
bpy.context.view_layer.update()
print(f"[proof] mesh object rotation: {[round(v,3) for v in mesh_obj.rotation_euler]} (importer Y-up->Z-up, kept)")
print(f"[proof] mesh verts: {len(mesh_obj.data.vertices)} (weights file: {nv})")
assert len(mesh_obj.data.vertices) == nv, "vertex count mismatch between mesh and weights!"

# ---------- build armature ----------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object
arm.name = "CJ_Pinocchio_Rig"
eb = arm.data.edit_bones
root = eb[0]
ebones = {}
children = {}
for j, jt in enumerate(joints):
    children.setdefault(jt["parent"], []).append(j)

for j, jt in enumerate(joints):
    p = jt["pos"]
    b = eb.new(jt["name"]) if j else root
    if j:
        b.name = jt["name"]
    b.head = (p[0], p[1], p[2])
    kids = children.get(j, [])
    par = jt["parent"]
    if kids:
        kp = joints[kids[0]]["pos"]
        b.tail = (kp[0], kp[1], kp[2])
    elif par is not None and par >= 0:
        pp = joints[par]["pos"]
        d = (p[0] - pp[0], p[1] - pp[1], p[2] - pp[2])
        L = math.sqrt(sum(x * x for x in d)) or 1.0
        b.tail = (p[0] + d[0] / L * 0.05, p[1] + d[1] / L * 0.05, p[2] + d[2] / L * 0.05)
    else:
        b.tail = (p[0], p[1] - 0.05, p[2])
    if par is not None and par >= 0:
        b.parent = ebones[par]
    ebones[j] = b

bpy.ops.object.mode_set(mode="OBJECT")

# ---------- vertex groups from weights ----------
mesh_obj.select_set(True)
bpy.context.view_layer.objects.active = mesh_obj
for j, jt in enumerate(joints):
    mesh_obj.vertex_groups.new(name=jt["name"])
vg = mesh_obj.vertex_groups
for i in range(nv):
    row = [(joints[j]["name"], w[i * nj + j]) for j in range(nj) if w[i * nj + j] > 1e-4]
    for name, wt in row:
        vg[name].add([i], wt, "REPLACE")
print("[proof] vertex groups assigned")

# ---------- armature modifier ----------
mod = mesh_obj.modifiers.new("PinocchioSkin", "ARMATURE")
mod.object = arm

# ---------- pose test ----------
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
pb = arm.pose.bones
def rot(name, axis, deg):
    b = pb.get(name)
    if b:
        b.rotation_mode = "XYZ"
        e = list(b.rotation_euler)
        e["XYZ".index(axis)] = math.radians(deg)
        b.rotation_euler = e

# elbows/knees bend, head turns -- MODEST angles only.
# (Blender space: Z-up, character faces -Y)
# Bone local axes are MEASURED (edit-bone matrix_local), not guessed:
#  - elbow bones: local Z ~= up -> bend forearms forward with Z
#    (mirrored signs: left +45, right -45). Verified clean at 90.
#  - knee bones: local X ~= left-right axis -> shins swing back with X.
#  - head bone: local Y ~= up (along head) -> turn with Y.
# Kept modest on purpose: Pinocchio's PDE weights are very smooth/diffuse
# and web on big combined poses (bake-off W8 MIXED-FAIL) -- this proof
# demonstrates clean articulation, not extreme motion.
# (The old axes -- shoulder Y = twist about the arm's own long axis,
# head Z = tilt -- folded the rig into a blob; shoulders are omitted
# from this proof until their raise axis is verified empirically.)
rot("lelbow", "Z", 45);    rot("relbow", "Z", -45)
rot("lknee", "X", 30);     rot("rknee", "X", 30)
rot("head", "Y", 10)
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.update()

# ---------- lighting (repo canon) + camera ----------
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.render.resolution_x, scene.render.resolution_y = 960, 960
scene.render.resolution_percentage = 100
scene.cycles.samples = 32
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.01, 0.02, 1)

def area_light(name, loc, energy, color=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.active_object
    l.name = name
    l.data.energy = energy
    l.data.color = color
    l.data.size = 2.0
    return l
area_light("RoomLight", (2.5, -2.5, 3.0), 300, (0.45, 0.10, 0.90))  # violet key
area_light("Fill", (-2.5, -1.5, 2.0), 60, (1.0, 0.85, 0.70))        # warm fill
sun = bpy.data.lights.new("Sun", "SUN"); sun.energy = 1.5
so = bpy.data.objects.new("Sun", sun); scene.collection.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(30))

# camera: frame the 0.925m character (Z-up; faces -Y). Aim with an explicit
# look-at basis (guaranteed correct up vector). NOTE: Vector.to_track_quat
# was tried first but rolls the camera 90deg for the side view
# (measured: up=[0,1,0] instead of +Z), so we build the basis manually.
from mathutils import Vector, Matrix
def aim_cam(loc, target=(0, 0, 0.05)):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.active_object
    fwd = (Vector(target) - Vector(loc)).normalized()
    right = fwd.cross(Vector((0, 0, 1))).normalized()
    up = right.cross(fwd).normalized()
    # camera looks down -Z: matrix columns = [right, up, -fwd]
    m = Matrix((right, up, -fwd)).transposed().to_4x4()
    m.translation = Vector(loc)
    c.matrix_world = m
    return c
cam = aim_cam((0, -1.7, 0.25))
scene.camera = cam
# show the armature through the mesh so the proof image displays bone placement
arm.display_type = "WIRE"
arm.show_in_front = True

def render(path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"[proof] rendered {path}")

render(os.path.join(outdir, "pinocchio_pose_front.png"))

# side view (rebuild basis manually; do not use to_track_quat -- see note above)
from mathutils import Vector as _V, Matrix as _M
_loc = (1.7, 0, 0.25)
_fwd = (_V((0, 0, 0.05)) - _V(_loc)).normalized()
_right = _fwd.cross(_V((0, 0, 1))).normalized()
_up = _right.cross(_fwd).normalized()
_m = _M((_right, _up, -_fwd)).transposed().to_4x4()
_m.translation = _V(_loc)
cam.matrix_world = _m
render(os.path.join(outdir, "pinocchio_pose_side.png"))

# rest pose for comparison
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for b in pb: b.rotation_euler = (0, 0, 0)
bpy.ops.object.mode_set(mode="OBJECT")
cam.location = (0, -1.7, 0.25)
_loc = (0, -1.7, 0.25)
_fwd = (_V((0, 0, 0.05)) - _V(_loc)).normalized()
_right = _fwd.cross(_V((0, 0, 1))).normalized()
_up = _right.cross(_fwd).normalized()
_m = _M((_right, _up, -_fwd)).transposed().to_4x4()
_m.translation = _V(_loc)
cam.matrix_world = _m
render(os.path.join(outdir, "pinocchio_rest_front.png"))
print("[proof] ALL DONE")
