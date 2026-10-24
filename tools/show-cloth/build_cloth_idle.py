#!/usr/bin/env python3
"""Build the idle cloth setup (Scene A: cape-vs-body). v2 — primitive colliders.

Opens cloth_idle_base.blend (show GLB + idle action), places the standalone
cape on the shoulders, adds cape_pin + cloth (stage2 pattern), builds
fitted primitive colliders skinned to the rig (back shell + upper-arm
capsules) + floor collision. NO body duplication (OOM-killed the VM twice
in the sitting saga). Saves cloth_idle_setup.blend WITHOUT baking.
"""
import bpy, math, numpy as np

SRC = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_base.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_setup.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)

sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["CapeJones_Body"]
cape = bpy.data.objects["CapeJones_Cape"]

# ---- 1. place cape on shoulders (measured 2026-10-24) ----
cape.location = (0.01, 0.04, 0.377)
print("cape placed at", tuple(cape.location), flush=True)

# ---- 2. pin group: local-z ramp, full pin across the top band ----
if "cape_pin" in cape.vertex_groups:
    cape.vertex_groups.remove(cape.vertex_groups["cape_pin"])
vg = cape.vertex_groups.new(name="cape_pin")
co = np.empty(len(cape.data.vertices) * 3, dtype=np.float64)
cape.data.vertices.foreach_get("co", co)
co = co.reshape(-1, 3)
w = np.clip((co[:, 2] - 0.36) / 0.04, 0.0, 1.0)
for i in np.nonzero(w > 0)[0]:
    vg.add([int(i)], float(w[i]), "REPLACE")
print(f"pin verts>0: {int((w > 0).sum())}, full pin: {int((w >= 0.999).sum())}", flush=True)

# ---- 3. cloth (stage2 settings, quality 10 for VM bake time) ----
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
pc.frame_start, pc.frame_end = 0, 96
pc.use_disk_cache = True
print("cloth set", flush=True)

# ---- 4. back shell: measured back profile (rest frame), skinned to rig ----
sc.frame_set(0)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(deps)
me = ev.to_mesh()
bco = np.empty(len(me.vertices) * 3, dtype=np.float64)
me.vertices.foreach_get("co", bco)
bco = bco.reshape(-1, 3)
mw = np.array(ev.matrix_world, dtype=np.float64)
hom = np.concatenate([bco, np.ones((len(bco), 1))], axis=1)
world = (hom @ mw.T)[:, :3]
ev.to_mesh_clear()

# profile: p99 y of back verts (y>0) per z band, 0.05..0.85
zs = np.linspace(0.05, 0.85, 17)
prof = []
for i in range(len(zs) - 1):
    sel = world[(world[:, 2] >= zs[i]) & (world[:, 2] < zs[i + 1]) & (world[:, 1] > 0)]
    y = float(np.percentile(sel[:, 1], 99)) if len(sel) else 0.10
    prof.append(((zs[i] + zs[i + 1]) / 2, y))
print("back profile (z, y_p99):", [(round(z, 2), round(y, 3)) for z, y in prof], flush=True)

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
bpy.context.scene.collection.objects.link(shell)
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

# ---- 5. upper-arm capsules (mantle edges brush the arms during idle) ----
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
    bpy.context.scene.collection.objects.link(ob)
    vg2 = ob.vertex_groups.new(name=bone_name)
    vg2.add(list(range(len(vs))), 1.0, "REPLACE")
    ob.modifiers.new("Armature", "ARMATURE").object = rig
    cc2 = ob.modifiers.new("Collision", "COLLISION")
    cc2.settings.thickness_outer = 0.012
    cc2.settings.thickness_inner = 0.004
    ob.hide_render = True
    return ob

make_capsule("upperarm_L", 0.055)
make_capsule("upperarm_R", 0.055)
print("upper-arm capsule colliders set", flush=True)

# ---- 6. floor collision ----
bpy.ops.mesh.primitive_plane_add(size=4.0, location=(0, 0, 0))
floor = bpy.context.view_layer.objects.active
floor.name = "Floor_Collision"
fc = floor.modifiers.new("Collision", "COLLISION")
fc.settings.thickness_outer = 0.010
floor.hide_render = True

sc.frame_start, sc.frame_end = 0, 96
sc.frame_set(0)
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
