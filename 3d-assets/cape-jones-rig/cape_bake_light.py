"""LANE 1 — bake cloth in the LIGHT file (no 910k body).
Creates shell + floor, cloth on cape, MANUAL shape-key bake 1-48.
Saves cape_sim_light_baked.blend."""
import bpy, os

BAKED = os.path.join(os.getcwd(), 'cape_sim_light_baked.blend')
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, 48

rig = bpy.data.objects['CapeJones_Rig']
cape = bpy.data.objects['CapeJones_Cape']

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

# shell collider
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
mesh = bpy.data.meshes.new('BackShell_Mesh')
mesh.from_pydata(verts, [], faces); mesh.update()
shell = bpy.data.objects.new('BackShell_Collider', mesh)
sc.collection.objects.link(shell)
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
coll = shell.modifiers.new('Collision', 'COLLISION')
coll.settings.thickness_outer = 0.012
shell.hide_viewport = True; shell.hide_render = True

# floor
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
floor = bpy.context.view_layer.objects.active
floor.name = 'Floor_Collision'
floor.modifiers.new('Collision', 'COLLISION').settings.thickness_outer = 0.01
floor.hide_viewport = True; floor.hide_render = True

# cape armature + cloth
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
cape.modifiers.new('Armature', 'ARMATURE').object = rig
cloth = cape.modifiers.new('Cloth', 'CLOTH')
cs = cloth.settings
cs.quality = 8; cs.mass = 0.3
cs.tension_stiffness = 15.0; cs.compression_stiffness = 15.0
cs.shear_stiffness = 5.0; cs.bending_stiffness = 1.0
cs.tension_damping = 5.0; cs.compression_damping = 5.0
cs.shear_damping = 5.0; cs.bending_damping = 0.5
cs.vertex_group_mass = 'cape_pin'
cc = cloth.collision_settings
cc.collision_quality = 4; cc.distance_min = 0.004
cc.use_collision = True
cc.use_self_collision = True; cc.self_distance_min = 0.004
print("cloth configured", flush=True)

# MANUAL shape-key bake (ptcache unreliable headless)
if not cape.data.shape_keys:
    cape.shape_key_add(name='Basis')
dg = bpy.context.evaluated_depsgraph_get()
for f in range(sc.frame_start, sc.frame_end + 1):
    sc.frame_set(f)
    dg.update()
    eval_ob = dg.objects.get(cape.name)
    eval_me = eval_ob.to_mesh()
    sk = cape.shape_key_add(name=f'frame_{f:03d}')
    for i, v in enumerate(eval_me.vertices):
        sk.data[i].co = v.co
    eval_ob.to_mesh_clear()
    sk.value = 0.0
    sk.keyframe_insert('value', frame=f - 1)
    sk.value = 1.0
    sk.keyframe_insert('value', frame=f)
    sk.value = 0.0
    sk.keyframe_insert('value', frame=f + 1)
    if f % 12 == 1:
        print(f"captured frame {f}", flush=True)
cape.modifiers['Cloth'].show_viewport = False
cape.modifiers['Cloth'].show_render = False
print("SHAPE-KEY BAKE DONE", flush=True)
bpy.ops.wm.save_as_mainfile(filepath=BAKED)
print(f"SAVED {BAKED}", flush=True)
