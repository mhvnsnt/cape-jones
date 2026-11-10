#!/usr/bin/env python3
"""Build the sitting cloth setup (Scene B: cape-vs-chair).

Copies living_room.blend (NEVER overwrites it), places the standalone cape
on the seated figure's shoulders (measured from the posed bones + back
surface), adds cape_pin + cloth (stage2 pattern), back-shell + thigh
colliders skinned to the rig, and REAL chair + floor collision.
Saves sit_cloth_setup.blend WITHOUT baking (bake is a separate step).

Seated figure faces -X (chair canon); back-out direction is +X. The
capelet's authored thin axis (+Y) maps to +X via Rz(-90deg).
"""
import bpy, math, numpy as np
from mathutils import Vector

SRC = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_setup.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)

sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["CapeJones_Body"]
cape = bpy.data.objects["CapeJones_Cape"]
chair = bpy.data.objects["loungeChairRelax(Clone)"]
print("rig action:", rig.animation_data.action.name if rig.animation_data and rig.animation_data.action else None, flush=True)

# ---- 1. measure seated neck + back surface at shoulder height ----
sc.frame_set(1)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
neck = rig.matrix_world @ rig.pose.bones["neck_1"].head
print("seated neck_1 head:", [round(v, 3) for v in neck], flush=True)
ev = body.evaluated_get(deps)
me = ev.to_mesh()
bco = np.empty(len(me.vertices) * 3, dtype=np.float64)
me.vertices.foreach_get("co", bco)
bco = bco.reshape(-1, 3)
mw = np.array(ev.matrix_world, dtype=np.float64)
world = (np.concatenate([bco, np.ones((len(bco), 1))], axis=1) @ mw.T)[:, :3]
ev.to_mesh_clear()
# back = +X side; shoulder-height band around neck z
band = world[(np.abs(world[:, 2] - neck.z) < 0.06)]
back_x = float(np.percentile(band[:, 0], 95)) if len(band) else 3.35
print(f"seated back surface x_p95 at neck height: {back_x:.3f}", flush=True)

# ---- 2. rotate capelet Rz(-90) + translate onto seated shoulders ----
# CRITICAL: room-blend cape uses QUATERNION rotation_mode, under which
# rotation_euler is ignored (v1 sit bake placed an unrotated plank behind
# the wall). Force XYZ first so the rotation actually applies.
cape.rotation_mode = "XYZ"
cape.rotation_euler = (0, 0, -math.pi / 2)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
evc = cape.evaluated_get(deps)
mec = evc.to_mesh()
cco = np.empty(len(mec.vertices) * 3, dtype=np.float64)
mec.vertices.foreach_get("co", cco)
cco = cco.reshape(-1, 3)
mw = np.array(evc.matrix_world, dtype=np.float64)
cworld = (np.concatenate([cco, np.ones((len(cco), 1))], axis=1) @ mw.T)[:, :3]
evc.to_mesh_clear()
# top band = top 5cm of cape z (rotation preserves z)
top = cworld[cworld[:, 2] > cworld[:, 2].max() - 0.05]
top_center = top.mean(axis=0)
slab_min_x = cworld[:, 0].min()
print(f"cape top center after rotation: {top_center.round(3)}, slab min x: {slab_min_x:.3f}", flush=True)
# target: top center z -> neck z; slab inner face -> back surface + 12mm
dx = (back_x + 0.012) - slab_min_x
dy = 2.067 - top_center[1]
dz = neck.z - top_center[2]
cape.location = (dx, dy, dz)
print(f"cape location set: {(round(dx, 3), round(dy, 3), round(dz, 3))}", flush=True)
# verify orientation: post-rotation mantle must be THIN in x (back-out)
# and WIDE in y (shoulder width), NOT the reverse
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
evv = cape.evaluated_get(deps)
mev = evv.to_mesh()
vvo = np.empty(len(mev.vertices) * 3, dtype=np.float64)
mev.vertices.foreach_get("co", vvo)
vvo = vvo.reshape(-1, 3)
mww = np.array(evv.matrix_world, dtype=np.float64)
wvo = (np.concatenate([vvo, np.ones((len(vvo), 1))], axis=1) @ mww.T)[:, :3]
evv.to_mesh_clear()
print(f"cape world bbox x [{wvo[:, 0].min():.3f}, {wvo[:, 0].max():.3f}] "
      f"y [{wvo[:, 1].min():.3f}, {wvo[:, 1].max():.3f}] "
      f"z [{wvo[:, 2].min():.3f}, {wvo[:, 2].max():.3f}]", flush=True)
assert (wvo[:, 0].max() - wvo[:, 0].min()) < 0.10, "mantle not thin in x — rotation failed!"
assert (wvo[:, 1].max() - wvo[:, 1].min()) > 0.30, "mantle not wide in y — rotation failed!"

# ---- 3. pin group (local-z ramp, same as idle) ----
if "cape_pin" in cape.vertex_groups:
    cape.vertex_groups.remove(cape.vertex_groups["cape_pin"])
vg = cape.vertex_groups.new(name="cape_pin")
lco = np.empty(len(cape.data.vertices) * 3, dtype=np.float64)
cape.data.vertices.foreach_get("co", lco)
lco = lco.reshape(-1, 3)
w = np.clip((lco[:, 2] - 0.36) / 0.04, 0.0, 1.0)
for i in np.nonzero(w > 0)[0]:
    vg.add([int(i)], float(w[i]), "REPLACE")
print(f"pin verts>0: {int((w > 0).sum())}, full pin: {int((w >= 0.999).sum())}", flush=True)

# ---- 4. cloth (stage2 settings) ----
cloth = cape.modifiers.new("Cloth", "CLOTH")
cs = cloth.settings
cs.quality = 10
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
pc.frame_start, pc.frame_end = 1, 60
pc.use_disk_cache = True
print("cloth set", flush=True)

# ---- 5. back shell in BIND space (temporarily clear action, measure, restore) ----
saved_action = rig.animation_data.action if rig.animation_data else None
if rig.animation_data:
    rig.animation_data.action = None
sc.frame_set(1)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(deps)
me = ev.to_mesh()
bco = np.empty(len(me.vertices) * 3, dtype=np.float64)
me.vertices.foreach_get("co", bco)
bco = bco.reshape(-1, 3)
mw = np.array(ev.matrix_world, dtype=np.float64)
bworld = (np.concatenate([bco, np.ones((len(bco), 1))], axis=1) @ mw.T)[:, :3]
ev.to_mesh_clear()
# bind pose: figure at origin facing -Y, back = +Y side
zs = np.linspace(0.05, 0.85, 17)
prof = []
for i in range(len(zs) - 1):
    sel = bworld[(bworld[:, 2] >= zs[i]) & (bworld[:, 2] < zs[i + 1]) & (bworld[:, 1] > 0)]
    y = float(np.percentile(sel[:, 1], 99)) if len(sel) else 0.10
    prof.append(((zs[i] + zs[i + 1]) / 2, y))
print("bind back profile:", [(round(z, 2), round(y, 3)) for z, y in prof], flush=True)
if rig.animation_data:
    rig.animation_data.action = saved_action
sc.frame_set(1)
bpy.context.view_layer.update()

def back_y(z):
    if z <= prof[0][0]:
        return prof[0][1]
    for (z0, y0), (z1, y1) in zip(prof, prof[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return y0 + t * (y1 - y0)
    return prof[-1][1]

NZ, NX = 40, 20
verts, faces = [], []
for r in range(NZ):
    z = 0.05 + r / (NZ - 1) * 0.80
    for c in range(NX):
        x = -0.26 + c / (NX - 1) * 0.52
        y = back_y(z) - 0.010 - 0.025 * (x / 0.22) ** 2
        verts.append((x, y, z))
for r in range(NZ - 1):
    for c in range(NX - 1):
        a = r * NX + c; b = a + 1; d = a + NX; e = d + 1
        faces.append((a, d, e, b))
shell_mesh = bpy.data.meshes.new("BackShell_Mesh")
shell_mesh.from_pydata(verts, [], faces)
shell_mesh.update()
shell = bpy.data.objects.new("BackShell_Collider", shell_mesh)
sc.collection.objects.link(shell)
for vgname in ["chest", "spine_2", "spine_1", "pelvis"]:
    shell.vertex_groups.new(name=vgname)
for i, (x, y, z) in enumerate(verts):
    if z > 0.62:
        shell.vertex_groups["chest"].add([i], 1.0, "REPLACE")
    elif z > 0.48:
        t = (z - 0.48) / 0.14
        shell.vertex_groups["chest"].add([i], t, "REPLACE")
        shell.vertex_groups["spine_2"].add([i], 1.0 - t, "REPLACE")
    elif z > 0.38:
        t = (z - 0.38) / 0.10
        shell.vertex_groups["spine_2"].add([i], t, "REPLACE")
        shell.vertex_groups["spine_1"].add([i], 1.0 - t, "REPLACE")
    else:
        shell.vertex_groups["pelvis"].add([i], 1.0, "REPLACE")
shell.modifiers.new("Armature", "ARMATURE").object = rig
scoll = shell.modifiers.new("Collision", "COLLISION")
scoll.settings.thickness_outer = 0.015
scoll.settings.thickness_inner = 0.005
shell.hide_render = True
print("back shell collider set", flush=True)

# ---- 6. thigh capsules (mantle may swing toward legs when settling) ----
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
        fs.append((s, s2, sides + s2, sides + s2))
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

for bn in ("thigh_L", "thigh_R"):
    if bn in rig.data.bones:
        make_capsule(bn, 0.072)
print("thigh capsule colliders set", flush=True)

# ---- 7. REAL chair + floor collision ----
cc = chair.modifiers.new("Collision", "COLLISION")
cc.settings.thickness_outer = 0.012
cc.settings.thickness_inner = 0.004
floor = bpy.data.objects.get("Floor")
if floor:
    fc = floor.modifiers.new("Collision", "COLLISION")
    fc.settings.thickness_outer = 0.010
    print("floor collision set", flush=True)
else:
    print("NOTE: no Floor object in room blend; chair + shell only", flush=True)
print("chair collision set", flush=True)

sc.frame_start, sc.frame_end = 1, 60
sc.frame_set(1)
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
