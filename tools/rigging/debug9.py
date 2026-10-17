"""In OFF mode, does moving a guide move the deform bones?"""
import bpy
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
# ensure OFF
arm.data['reproportion'] = 0
for pb in arm.pose.bones:
    for C in pb.constraints:
        if 'REPROP' in C.name:
            C.mute = True
        elif 'NOREP' in C.name:
            C.mute = False
bpy.context.view_layer.update()

g = arm.pose.bones['hand_str_L']
d = arm.pose.bones['hand_def_L']
print('BEFORE: guide head', tuple(round(v,3) for v in g.head), 'def head', tuple(round(v,3) for v in d.head))
# move guide +0.1 in x via location
g.location.x += 0.1
bpy.context.view_layer.update()
print('AFTER +0.1x: guide head', tuple(round(v,3) for v in g.head), 'def head', tuple(round(v,3) for v in d.head))
