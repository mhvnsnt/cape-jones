"""LANE 1 CAPE REBUILD — Step 2 (v2): cloth sim + bake, LOW-MEMORY.
Replaces the 910k-vert decimate (OOM-killed) with a procedural back-shell
collider built from measured body-surface data (800 verts).
- BackShell: curved panel behind torso, Armature-weighted (chest/spine_2/spine_1),
  + Collision. Follows the idle breathing.
- Floor plane + Collision.
- Cape: Armature (top->chest/spine_2) then Cloth (pin='cape_pin', self-collision).
- Bake 1-48 -> cape_jones_rigged_w5r_idle_cape.blend"""
import bpy, os

FINAL = os.path.join(os.getcwd(), 'cape_jones_rigged_w5r_idle_cape.blend')
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, 48

rig = bpy.data.objects['CapeJones_Rig']
cape = bpy.data.objects['CapeJones_Cape']
print(f"cape verts: {len(cape.data.vertices)}", flush=True)

# measured body back surface (idle pose, 2026-10-17)
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

# ---- 1. procedural back-shell collider ----
NZ, NX = 40, 20
verts, faces = [], []
for r in range(NZ):
    z = 0.05 + r / (NZ - 1) * 0.80  # 0.05 .. 0.85
    for c in range(NX):
        x = -0.26 + c / (NX - 1) * 0.52
        # 1cm inside surface at center, curving back 2.5cm at edges
        y = back_y(z) - 0.010 - 0.025 * (x / 0.22) ** 2
        verts.append((x, y, z))
for r in range(NZ - 1):
    for c in range(NX - 1):
        a = r * NX + c; b = a + 1; d = a + NX; e = d + 1
        faces.append((a, d, e, b))
mesh = bpy.data.meshes.new('BackShell_Mesh')
mesh.from_pydata(verts, [], faces)
mesh.update()
shell = bpy.data.objects.new('BackShell_Collider', mesh)
sc.collection.objects.link(shell)
# procedural armature weights so it breathes with the body
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
arm = shell.modifiers.new('Armature', 'ARMATURE')
arm.object = rig
coll = shell.modifiers.new('Collision', 'COLLISION')
coll.settings.thickness_outer = 0.012
coll.settings.thickness_inner = 0.004
coll.settings.cloth_friction = 8.0
shell.hide_viewport = True
shell.hide_render = True
print(f"shell built: {len(verts)} verts", flush=True)

# ---- 2. floor ----
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
floor = bpy.context.view_layer.objects.active
floor.name = 'Floor_Collision'
floor.modifiers.new('Collision', 'COLLISION').settings.thickness_outer = 0.01
floor.hide_viewport = True
floor.hide_render = True

# ---- 3. cape armature weights (top follows chest) ----
if 'cape_pin' not in [vg.name for vg in cape.vertex_groups]:
    print("ERROR: cape_pin group missing", flush=True)
    raise SystemExit(1)
vg_chest = cape.vertex_groups.new(name='chest')
vg_spine = cape.vertex_groups.new(name='spine_2')
for i, v in enumerate(cape.data.vertices):
    z = v.co.z
    if z > 0.70:
        vg_chest.add([i], 1.0, 'REPLACE')
    elif z > 0.58:
        t = (z - 0.58) / 0.12
        vg_chest.add([i], t, 'REPLACE')
        vg_spine.add([i], 1.0 - t, 'REPLACE')
arm2 = cape.modifiers.new('Armature', 'ARMATURE')
arm2.object = rig
arm2.use_deform_preserve_volume = True

# ---- 4. cloth ----
cloth = cape.modifiers.new('Cloth', 'CLOTH')
cs = cloth.settings
cs.quality = 8
cs.mass = 0.3
cs.tension_stiffness = 15.0
cs.compression_stiffness = 15.0
cs.shear_stiffness = 5.0
cs.bending_stiffness = 1.0
cs.tension_damping = 5.0
cs.compression_damping = 5.0
cs.shear_damping = 5.0
cs.bending_damping = 0.5
cs.vertex_group_mass = 'cape_pin'
# (self-collision lives on collision_settings, set below)
cc = cloth.collision_settings
cc.collision_quality = 4
cc.distance_min = 0.004
cc.use_collision = True
cc.use_self_collision = True
cc.self_distance_min = 0.004
print("cloth configured", flush=True)

# ---- 5. bake ----
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = cape
cape.select_set(True)
print("BAKE START (frames 1-48)", flush=True)
bpy.ops.ptcache.bake(bake=True)
print("BAKE DONE", flush=True)

bpy.ops.wm.save_as_mainfile(filepath=FINAL)
print(f"SAVED {FINAL}", flush=True)
