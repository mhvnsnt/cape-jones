"""Clean cage modifiers: keep only Armature->CapeJones_Rig."""
import bpy, os
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_cape_sep.blend'))
scn = bpy.context.scene
cage = bpy.data.objects['BlenRigMdefCage']
arm = bpy.data.objects['CapeJones_Rig']
if cage.name not in scn.collection.objects:
    scn.collection.objects.link(cage)
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.objects.active = cage
print('before:', [(m.name, m.type, m.object.name if hasattr(m,'object') and m.object else None) for m in cage.modifiers])
# remove all except the Armature->CapeJones_Rig
for m in list(cage.modifiers):
    keep = (m.type == 'ARMATURE' and hasattr(m, 'object') and m.object and m.object.name == 'CapeJones_Rig')
    if not keep:
        print('removing:', m.name, m.type)
        cage.modifiers.remove(m)
print('after:', [(m.name, m.type) for m in cage.modifiers])
# ensure the kept one has preserve volume
for m in cage.modifiers:
    if m.type == 'ARMATURE':
        m.use_deform_preserve_volume = True
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_cape_sep.blend'))
print('CAGE CLEANED')
