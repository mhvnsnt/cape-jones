"""LANE 1 CAPE REBUILD — Step 2: cloth sim setup + bake.
- Body proxy: decimated duplicate (8k) + Armature + Collision
- Floor plane + Collision
- Cape: Armature (procedural top weights to chest/spine_2) then Cloth
  (pin='cape_pin', self-collision ON)
- Bake 1-48, save FINAL as cape_jones_rigged_w5r_idle_cape.blend
Run: blender -b <STEP1> --python cape_sim_bake.py"""
import bpy, os

STEP1 = os.path.join(os.getcwd(), 'cape_jones_rigged_w5r_idle_cape_STEP1.blend')
FINAL = os.path.join(os.getcwd(), 'cape_jones_rigged_w5r_idle_cape.blend')
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, 48

rig = bpy.data.objects['CapeJones_Rig']
body = bpy.data.objects['CapeJones_Body']
cape = bpy.data.objects['CapeJones_Cape']
print(f"cape verts: {len(cape.data.vertices)}", flush=True)

# ---- 1. body collision proxy (decimated, keeps Armature) ----
bpy.ops.object.select_all(action='DESELECT')
proxy = body.copy()
proxy.data = body.data.copy()
proxy.name = 'Body_Collision_Proxy'
sc.collection.objects.link(proxy)
bpy.context.view_layer.objects.active = proxy
# keep only Armature modifier; drop CorrectiveSmooth for speed
for m in list(proxy.modifiers):
    if m.type != 'ARMATURE':
        proxy.modifiers.remove(m)
dec = proxy.modifiers.new('Decimate', 'DECIMATE')
dec.ratio = 0.01
dec.use_collapse_triangulate = True
bpy.ops.object.modifier_apply(modifier=dec.name)
print(f"proxy verts: {len(proxy.data.vertices)}", flush=True)
# move Armature to top (already is), add Collision
coll = proxy.modifiers.new('Collision', 'COLLISION')
coll.settings.thickness_outer = 0.012
coll.settings.thickness_inner = 0.004
coll.settings.cloth_friction = 8.0
proxy.hide_viewport = True
proxy.hide_render = True

# ---- 2. floor collider ----
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
floor = bpy.context.view_layer.objects.active
floor.name = 'Floor_Collision'
fcoll = floor.modifiers.new('Collision', 'COLLISION')
fcoll.settings.thickness_outer = 0.01
floor.hide_viewport = True
floor.hide_render = True

# ---- 3. cape: procedural armature weights for the top ----
# (so the pinned shoulders follow the breathing chest)
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
arm = cape.modifiers.new('Armature', 'ARMATURE')
arm.object = rig
arm.use_deform_preserve_volume = True

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
cs.use_sewing_springs = False
# pin at shoulders
cs.vertex_group_mass = 'cape_pin'
# self collision
cs.use_self_collision = True
cs.self_collision_distance = 0.004
cs.collision_quality = 4
# aerodynamics: light air drag so it settles, slight turbulence off
cs.effector_weights.gravity = 1.0
cs.time_scale = 1.0

# cloth collision with proxy/floor
cc = cloth.collision_settings
cc.collision_quality = 4
cc.distance_min = 0.004
cc.use_collision = True
cc.use_self_collision = True
cc.self_collision_distance = 0.004

print("cloth configured; pin=cape_pin, self-collision ON", flush=True)

# ---- 5. bake ----
# speed: mute body's CorrectiveSmooth during bake (cosmetic only)
body_cs = body.modifiers.get('CorrectiveSmooth')
was_on = None
if body_cs:
    was_on = body_cs.show_viewport
    body_cs.show_viewport = False
    body_cs.show_render = False

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = cape
cape.select_set(True)
print("BAKE START (frames 1-48)", flush=True)
bpy.ops.ptcache.bake(bake=True)
print("BAKE DONE", flush=True)

if body_cs and was_on:
    body_cs.show_viewport = True
    body_cs.show_render = True

bpy.ops.wm.save_as_mainfile(filepath=FINAL)
print(f"SAVED {FINAL}", flush=True)
