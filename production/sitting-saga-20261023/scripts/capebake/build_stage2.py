"""Stage 2: open stage1_welded.blend, add cape_pin + cloth, collision proxy,
chair/floor collision. Save bake_scene.blend (upload-ready)."""
import bpy
import numpy as np

SRC = "/home/hatch/workspace/capebake-work/stage1_welded.blend"
OUT = "/home/hatch/workspace/capebake-work/bake_scene2.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
body = bpy.data.objects["CapeJones_Body"]
cape = bpy.data.objects["CapeJones_Cape"]
print(f"stage2: body {len(body.data.vertices)} cape {len(cape.data.vertices)}", flush=True)

# ---------- pin group: neckline/shoulder band (bind space z ramp 0.68->0.78) ----------
cmesh = cape.data
pin = cmesh.vertices  # local coords == body local coords (same transform)
if "cape_pin" in cape.vertex_groups:
    cape.vertex_groups.remove(cape.vertex_groups["cape_pin"])
vg = cape.vertex_groups.new(name="cape_pin")
cco = np.empty(len(pin) * 3, dtype=np.float64)
pin.foreach_get("co", cco)
cco = cco.reshape(-1, 3)
w = np.clip((cco[:, 2] - 0.68) / 0.10, 0.0, 1.0)
# only the back panel band (y > -0.02) can pin; front drips stay free (cape has none in front, safety)
w[cco[:, 1] < -0.02] = 0.0
for i in np.nonzero(w > 0)[0]:
    vg.add([int(i)], float(w[i]), 'REPLACE')
print(f"pin verts>0: {int((w>0).sum())}, full pin: {int((w>=0.999).sum())}", flush=True)

# ---------- cloth modifier ----------
cloth = cape.modifiers.new("Cloth", 'CLOTH')
cs = cloth.settings
cs.quality = 12
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
pc.frame_start, pc.frame_end = 1, 81
pc.use_disk_cache = False
print("cloth set", flush=True)

# ---------- collision colliders (light procedural, repo cape_sim_bake pattern) ----------
# NOTE: duplicating the 627k body for a decimate proxy OOM-killed this VM twice.
# Use fitted primitive colliders instead: back shell + thigh capsules + real chair/floor.
import math
rig = bpy.data.objects["CapeJones_Rig"]

BACK = [(0.10, 0.052), (0.15, 0.101), (0.20, 0.101), (0.25, 0.101), (0.30, 0.102),
        (0.35, 0.102), (0.40, 0.101), (0.45, 0.100), (0.50, 0.097), (0.60, 0.089),
        (0.70, 0.089), (0.75, 0.080), (0.80, 0.064), (0.85, 0.050)]
def back_y(z):
    if z <= BACK[0][0]:
        return BACK[0][1]
    for (z0, y0), (z1, y1) in zip(BACK, BACK[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return y0 + t * (y1 - y0)
    return BACK[-1][1]

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
shell_mesh = bpy.data.meshes.new('BackShell_Mesh')
shell_mesh.from_pydata(verts, [], faces)
shell_mesh.update()
shell = bpy.data.objects.new('BackShell_Collider', shell_mesh)
bpy.context.scene.collection.objects.link(shell)
for vgname in ['chest', 'spine_2', 'spine_1', 'pelvis']:
    shell.vertex_groups.new(name=vgname)
for i, (x, y, z) in enumerate(verts):
    if z > 0.62:
        shell.vertex_groups['chest'].add([i], 1.0, 'REPLACE')
    elif z > 0.48:
        t = (z - 0.48) / 0.14
        shell.vertex_groups['chest'].add([i], t, 'REPLACE')
        shell.vertex_groups['spine_2'].add([i], 1.0 - t, 'REPLACE')
    elif z > 0.38:
        t = (z - 0.38) / 0.10
        shell.vertex_groups['spine_2'].add([i], t, 'REPLACE')
        shell.vertex_groups['spine_1'].add([i], 1.0 - t, 'REPLACE')
    else:
        shell.vertex_groups['pelvis'].add([i], 1.0, 'REPLACE')
shell.modifiers.new('Armature', 'ARMATURE').object = rig
scoll = shell.modifiers.new('Collision', 'COLLISION')
scoll.settings.thickness_outer = 0.015
scoll.settings.thickness_inner = 0.005
shell.hide_render = True
print("back shell collider set", flush=True)

# thigh capsules along the thigh bones
def make_capsule(bone_name, radius=0.072, sides=12):
    b = rig.data.bones[bone_name]
    h = np.array([b.head_local.x, b.head_local.y, b.head_local.z])
    t = np.array([b.tail_local.x, b.tail_local.y, b.tail_local.z])
    axis = t - h
    axis = axis / np.linalg.norm(axis)
    ref = np.array([1.0, 0.0, 0.0]) if abs(axis[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u = np.cross(axis, ref); u /= np.linalg.norm(u)
    w = np.cross(axis, u)
    vs, fs = [], []
    for center in (h, t):
        for s in range(sides):
            a = 2 * math.pi * s / sides
            p = center + radius * (math.cos(a) * u + math.sin(a) * w)
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
    m = bpy.data.meshes.new(bone_name + '_Capsule')
    m.from_pydata(vs, [], fs)
    m.update()
    ob = bpy.data.objects.new(bone_name + '_Collider', m)
    bpy.context.scene.collection.objects.link(ob)
    vg = ob.vertex_groups.new(name=bone_name)
    vg.add(list(range(len(vs))), 1.0, 'REPLACE')
    ob.modifiers.new('Armature', 'ARMATURE').object = rig
    cc = ob.modifiers.new('Collision', 'COLLISION')
    cc.settings.thickness_outer = 0.012
    cc.settings.thickness_inner = 0.004
    ob.hide_render = True
    return ob

make_capsule('thigh_L')
make_capsule('thigh_R')
print("thigh capsule colliders set", flush=True)

# ---------- chair + floor collision ----------
chair = bpy.data.objects.get("loungeChairRelax(Clone)")
cc = chair.modifiers.new("Collision", 'COLLISION')
cc.settings.thickness_outer = 0.012
cc.settings.thickness_inner = 0.004
floor = bpy.data.objects.get("Floor")
fc = floor.modifiers.new("Collision", 'COLLISION')
fc.settings.thickness_outer = 0.010
print("colliders set", flush=True)

sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, 81
sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT}", flush=True)
print("BUILD DONE", flush=True)
