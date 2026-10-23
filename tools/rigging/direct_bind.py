"""Transfer cage weights to character, use direct Armature (bypass cage deform)."""
import bpy, os
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_clean.blend'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
cage = bpy.data.objects['BlenRigMdefCage']
arm = bpy.data.objects['CapeJones_Rig']
for o in (char, cage, arm):
    if o.name not in scn.collection.objects:
        scn.collection.objects.link(o)
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

# Remove MeshDeform and CorrectiveSmooth from char (we'll use direct Armature)
bpy.context.view_layer.objects.active = char
for m in list(char.modifiers):
    mtype = m.type
    if mtype in ('MESH_DEFORM', 'CORRECTIVE_SMOOTH'):
        char.modifiers.remove(m)
        print('removed', mtype)
# Transfer weights from cage to char via Data Transfer
# Select cage then char
cage.select_set(True)
char.select_set(True)
bpy.context.view_layer.objects.active = char
# Use data transfer operator
bpy.ops.object.data_transfer(
    data_type='VGROUP_WEIGHTS',
    use_create_data=True,
    vert_mapping='POLYINTERP_NEAREST',
    layers_select_src='ALL',
    layers_select_dst='NAME',
    mix_mode='REPLACE'
)
print('WEIGHTS TRANSFERRED')
# Add Armature modifier
mod = char.modifiers.new('Armature', 'ARMATURE')
mod.object = arm
mod.use_deform_preserve_volume = True
print('ARMATURE ADDED')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_direct.blend'))
print('DIRECT SAVED')
