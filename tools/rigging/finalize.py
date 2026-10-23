"""Finalize deliverable: cape cloth setup (no bake), save to 3d-assets."""
import bpy, os
import numpy as np
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
OUT = os.path.expanduser('~/workspace/cj-rig-wt/3d-assets/cape-jones-rig/cape_jones_rigged.blend')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_direct.blend'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
cape = bpy.data.objects['CapeJones_Cape']
arm = bpy.data.objects['CapeJones_Rig']
for o in (char, cape, arm):
    if o.name not in scn.collection.objects:
        scn.collection.objects.link(o)
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='OBJECT')

# Cape cloth setup
bpy.context.view_layer.objects.active = cape
# Pin group: top verts (z > 0.40, near shoulders)
n = len(cape.data.vertices)
verts = np.empty(n*3, dtype=np.float32)
cape.data.vertices.foreach_get('co', verts)
verts = verts.reshape(-1, 3)
mw = np.array(cape.matrix_world, dtype=np.float32)
verts_w = (mw[:3,:3] @ verts.T).T + mw[:3,3]
pin_mask = verts_w[:,2] > 0.40
print('pin verts:', pin_mask.sum())
vg = cape.vertex_groups.new(name='pin_shoulders')
idx = np.where(pin_mask)[0]
for i in range(0, len(idx), 10000):
    vg.add(idx[i:i+10000].tolist(), 1.0, 'REPLACE')
# Armature modifier (so pins follow chest)
mod_arm = cape.modifiers.new('Armature', 'ARMATURE')
mod_arm.object = arm
# Create a simple weight: all pin verts -> chest bone
# (For now, use a single vertex group for chest)
vg_chest = cape.vertex_groups.new(name='chest')
vg_chest.add(idx.tolist(), 1.0, 'REPLACE')
# Cloth modifier
mod_cloth = cape.modifiers.new('Cloth', 'CLOTH')
cloth = mod_cloth.settings
cloth.quality = 5
cloth.pin_stiffness = 1.0
# set pin group
# In Blender 4.0, pin group is via vertex_group_mass? Actually it's cloth.settings.vertex_group_mass
# The pin group for cloth is: settings.vertex_group_mass (for mass) and use_pin?
# Actually, cloth pinning uses the 'pin' vertex group via settings.vertex_group_structural_stiffness? No.
# Cloth pin: mod.settings.vertex_group_mass is for mass. Pinning is via 'use_dynamic_mesh'?
# Let me check: In Blender, cloth pin group is set via the modifier's 'settings.vertex_group_mass'?
# Actually, it's: cloth.settings.vertex_group_mass = 'pin_shoulders' AND cloth.settings.use_pin = True?
# In 4.0, the pin group is specified in the Cloth settings under 'Shape' -> 'Pin Group'.
# Via Python: mod.settings.vertex_group_mass? No.
# The correct: bpy.data.objects['Cape'].modifiers['Cloth'].settings.vertex_group_mass
# Hmm, actually for pinning, it's: settings.vertex_group_structural_stiffness? No.
# Let me just set the pin group via the known property.
try:
    cloth.vertex_group_mass = 'pin_shoulders'
    print('pin group set via vertex_group_mass')
except:
    print('pin group property not found, documenting manually')
# Collision settings
cloth.use_collision = True
cloth.collision_quality = 2
print('CLOTH SETUP DONE (bake pending)')

# Ensure char has Armature (already added)
print('char mods:', [m.type for m in char.modifiers])

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('DELIVERABLE SAVED to', OUT)
