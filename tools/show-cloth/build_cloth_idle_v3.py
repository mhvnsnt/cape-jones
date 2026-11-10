#!/usr/bin/env python3
"""Idle cloth setup v3 — THE FIX for v2's body penetration.

Root cause of v2 (1,286 overlap pairs vs body at frame 48): the cape
object was UNPARENTED, so its cloth pins were fixed in WORLD space while
the body moved under them during the idle. A mantle pinned in world
space on a moving character MUST penetrate.

Fix: parent the cape object to the chest BONE (world matrix preserved at
frame 0), so pins ride the torso and the free part drapes relative to a
moving body. Plus a neck capsule collider for the neck/head boundary.
Proxy sim (decimate 0.05, quality 5) as proven by the v2 bake completing.
"""
import bpy, math, numpy as np
from mathutils import Matrix

SRC = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_slim.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_v3.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
cape = bpy.data.objects["CapeJones_Cape"]

# ---- 1. parent cape to chest bone, preserving world transform at frame 0 ----
sc.frame_set(0)
bpy.context.view_layer.update()
mw = cape.matrix_world.copy()
cape.parent = rig
cape.parent_type = "BONE"
cape.parent_bone = "chest"
cape.matrix_world = mw
bpy.context.view_layer.update()
mw2 = cape.matrix_world
print("cape world preserved:", [round(v, 4) for v in mw2.translation],
      "expected:", [round(v, 4) for v in mw.translation], flush=True)
assert (mw2.translation - mw.translation).length < 0.001, "parenting moved the cape!"

# ---- 2. neck capsule collider ----
def make_capsule(bone_name, radius, sides=12):
    b = rig.data.bones[bone_name]
    h = np.array([b.head_local.x, b.head_local.y, b.head_local.z])
    t = np.array([b.tail_local.x, b.tail_local.y, b.tail_local.z])
    axis = t - h
    axis = axis / np.linalg.norm(axis)
    ref = np.array([1.0, 0.0, 0.0]) if abs(axis[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u = np.cross(axis, ref); u /= np.linalg.norm(u)
    wv = np.cross(axis, u)
    vs, fs = [], []
    for center in (h, t):
        for s in range(sides):
            a = 2 * math.pi * s / sides
            p = center + radius * (math.cos(a) * u + math.sin(a) * wv)
            vs.append(tuple(p))
    for s in range(sides):
        s2 = (s + 1) % sides
        fs.append((s, s2, sides + s2, sides + s))
    vs.append(tuple(h - axis * 0.01)); vs.append(tuple(t + axis * 0.01))
    hc, tc = len(vs) - 2, len(vs) - 1
    for s in range(sides):
        s2 = (s + 1) % sides
        fs.append((hc, s2, s))
        fs.append((tc, sides + s, sides + s2))
    m = bpy.data.meshes.new(bone_name + "_Capsule")
    m.from_pydata(vs, [], fs)
    m.update()
    ob = bpy.data.objects.new(bone_name + "_Collider", m)
    sc.collection.objects.link(ob)
    vg2 = ob.vertex_groups.new(name=bone_name)
    vg2.add(list(range(len(vs))), 1.0, "REPLACE")
    ob.modifiers.new("Armature", "ARMATURE").object = rig
    cc2 = ob.modifiers.new("Collision", "COLLISION")
    cc2.settings.thickness_outer = 0.012
    cc2.settings.thickness_inner = 0.004
    ob.hide_render = True
    return ob

make_capsule("neck_1", 0.06)
print("neck capsule collider set", flush=True)

# ---- 3. proxy decimate + cloth (pin group already on mesh from setup) ----
for m in list(cape.modifiers):
    if m.type == "CLOTH":
        cape.modifiers.remove(m)
dec = cape.modifiers.new("Decimate", "DECIMATE")
dec.ratio = 0.05
cloth = cape.modifiers.new("Cloth", "CLOTH")
cs = cloth.settings
cs.quality = 5
cs.mass = 0.35
cs.tension_stiffness = 15.0
cs.compression_stiffness = 15.0
cs.shear_stiffness = 8.0
cs.bending_stiffness = 0.8
cs.tension_damping = 5.0
cs.compression_damping = 5.0
cs.shear_damping = 5.0
cs.bending_damping = 0.5
cs.air_damping = 1.0
cs.vertex_group_mass = "cape_pin"
try:
    cs.pin_stiffness = 1.0
except Exception:
    pass
col = cloth.collision_settings
col.use_collision = True
col.collision_quality = 3
col.distance_min = 0.010
col.use_self_collision = True
col.self_distance_min = 0.006
pc = cloth.point_cache
pc.frame_start, pc.frame_end = 0, 96
pc.use_disk_cache = True
sc.frame_start, sc.frame_end = 0, 96
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED V3", OUT, flush=True)
