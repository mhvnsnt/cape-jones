"""Bind cage->armature, character->cage (mesh deform), corrective smooth.
Loads .rig_tmp/cj_weighted.blend."""
import bpy, os
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_weighted.blend'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
cage = bpy.data.objects['BlenRigMdefCage']
arm = bpy.data.objects['CapeJones_Rig']

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
# ensure cage is linked to scene
if cage.name not in scn.collection.objects:
    scn.collection.objects.link(cage)
if char.name not in scn.collection.objects:
    scn.collection.objects.link(char)
if arm.name not in scn.collection.objects:
    scn.collection.objects.link(arm)
bpy.context.view_layer.update()

# cage -> armature
bpy.context.view_layer.objects.active = cage
cage.select_set(True)
mod = cage.modifiers.new('Armature', 'ARMATURE')
mod.object = arm
# dual quaternion for volume preservation
mod.use_deform_preserve_volume = True
bpy.context.view_layer.update()
print('CAGE BOUND TO ARMATURE')

# character -> cage (mesh deform)
bpy.context.view_layer.objects.active = char
char.select_set(True)
# ensure cage is visible for binding
cage.hide_viewport = False
cage.hide_render = False
mod2 = char.modifiers.new('MeshDeform', 'MESH_DEFORM')
mod2.object = cage
mod2.precision = 5
# bind (this can take a while for 991k verts)
print('BINDING MESH DEFORM (991k verts, may take a few minutes)...')
bpy.ops.object.meshdeform_bind(modifier='MeshDeform')
print('MESH DEFORM BOUND')

# corrective smooth (masked to problem zones via vertex group)
# create a vertex group for problem zones (elbows, knees, shoulders, hips)
# for now, apply to all with low factor; mask can be refined
mod3 = char.modifiers.new('CorrectiveSmooth', 'CORRECTIVE_SMOOTH')
mod3.factor = 0.5
mod3.iterations = 3
mod3.use_only_smooth = False
print('CORRECTIVE SMOOTH ADDED')

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_bound.blend'))
print('BOUND SAVED')
