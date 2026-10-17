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
# Blender 4.0.2's OBJ importer does NO Y-up -> Z-up conversion (unlike the
# glTF importer), so the mesh arrives Y-up. Bake a +90deg X rotation into the
# MESH DATA (keeps vertex order -> weights still align by index) to make it
# Z-up; then JSON joint (x,y,z) maps to Blender (x,-z,y) (already applied
# above), and the character faces -Y. Object rotation stays identity so the
# armature modifier sees matching spaces.
from mathutils import Matrix
mesh_obj.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
mesh_obj.data.update()
# The OBJ carries custom split normals; the data transform leaves them stale
# (wrong shading). Clear so Blender recomputes them.
bpy.context.view_layer.objects.active = mesh_obj
mesh_obj.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.customdata_custom_splitnormals_clear()
bpy.ops.object.mode_set(mode="OBJECT")
mesh_obj.select_set(False)
bpy.context.view_layer.update()
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

# elbows/knees bend, shoulders lift sideways, head turns
# (Blender space: Z-up, character faces -Y)
rot("lelbow", "X", -70); rot("relbow", "X", -70)
rot("lknee", "X", 55);   rot("rknee", "X", 55)
rot("lshoulder", "Y", 25); rot("rshoulder", "Y", -25)
rot("head", "Z", 18)
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

# camera: frame the 0.925m character (Z-up; faces -Y). Aim with track-quat
# (guaranteed) and keep world +Z as up so the character is upright in frame.
from mathutils import Vector
def aim_cam(loc, target=(0, 0, 0.05)):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.active_object
    d = Vector(target) - Vector(loc)
    c.rotation_euler = d.to_track_quat("-Z", "Z").to_euler()
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

# side view
cam.location = (1.7, 0, 0.25)
cam.rotation_euler = (Vector((0, 0, 0.05)) - Vector(cam.location)).to_track_quat("-Z", "Z").to_euler()
render(os.path.join(outdir, "pinocchio_pose_side.png"))

# rest pose for comparison
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for b in pb: b.rotation_euler = (0, 0, 0)
bpy.ops.object.mode_set(mode="OBJECT")
cam.location = (0, -1.7, 0.25)
cam.rotation_euler = (Vector((0, 0, 0.05)) - Vector(cam.location)).to_track_quat("-Z", "Z").to_euler()
render(os.path.join(outdir, "pinocchio_rest_front.png"))
print("[proof] ALL DONE")
