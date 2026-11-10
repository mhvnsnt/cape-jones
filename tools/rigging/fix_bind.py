"""Fix MeshDeform after cape separation: re-bind body, strip cape modifier."""
import bpy, os
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_cape_sep.blend'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
cape = bpy.data.objects['CapeJones_Cape']
cage = bpy.data.objects['BlenRigMdefCage']
for o in (char, cape, cage):
    if o.name not in scn.collection.objects:
        scn.collection.objects.link(o)
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

# cape: remove broken MeshDeform (will use cloth later)
bpy.context.view_layer.objects.active = cape
for m in list(cape.modifiers):
    if m.type == 'MESH_DEFORM':
        cape.modifiers.remove(m)
        print('removed MeshDeform from cape')
# cape keeps its modeled drape for now (no deform)

# body: remove broken MeshDeform, re-bind
bpy.context.view_layer.objects.active = char
for m in list(char.modifiers):
    if m.type == 'MESH_DEFORM':
        char.modifiers.remove(m)
        print('removed broken MeshDeform from body')
# re-add and bind
mod = char.modifiers.new('MeshDeform', 'MESH_DEFORM')
mod.object = cage
mod.precision = 5
print('RE-BINDING body MeshDeform (910k verts)...')
bpy.ops.object.meshdeform_bind(modifier='MeshDeform')
print('BODY RE-BOUND')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_cape_sep.blend'))
print('FIXED SAVED')
