import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_enable(module='rigify')
bpy.ops.object.armature_human_metarig_add()
meta = bpy.context.active_object
bpy.ops.object.mode_set(mode='EDIT')
eb = meta.data.edit_bones
spine3 = eb['spine.003']
prev = spine3
for i, (h, t) in enumerate([((0,0.10,0.75),(0,0.11,0.62)),((0,0.11,0.62),(0,0.115,0.49)),((0,0.115,0.49),(0,0.12,0.36)),((0,0.12,0.36),(0,0.12,0.23)),((0,0.12,0.23),(0,0.115,0.10))]):
    b = eb.new(f'cape.{i+1:03d}')
    b.head, b.tail = h, t
    b.parent = prev if i else spine3
    b.use_connect = i > 0
    prev = b
bpy.ops.object.mode_set(mode='POSE')
pb = meta.pose.bones['cape.001']
print('HAS rigify_type attr:', hasattr(pb, 'rigify_type'))
pb.rigify_type = 'limbs.spline_tentacle'
print('SET OK', pb.rigify_type)
try:
    print('GENERATE', bpy.ops.pose.rigify_generate())
except Exception as e:
    print('GENERATE_FAIL', repr(e))
rig = bpy.data.objects.get('rig')
if rig:
    cape = [b.name for b in rig.data.bones if 'cape' in b.name]
    print('CAPE BONES', cape)
    for pb in rig.pose.bones:
        if 'cape' in pb.name and pb.constraints:
            print('CONSTRAINTS', pb.name, [(c.type, c.name) for c in pb.constraints])
    print('OBJECTS', [o.name for o in bpy.data.objects])
