"""Verify FK->deform chain works."""
import bpy, math
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_cape_sep.blend')
arm = bpy.data.objects['CapeJones_Rig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
fk = arm.pose.bones['upperarm_fk_L']
df = arm.pose.bones['upperarm_L']
# set FK to XYZ and rotate
fk.rotation_mode = 'XYZ'
fk.rotation_euler = (0, math.radians(-80), 0)
bpy.context.view_layer.update()
# get world position of tail via matrix
fk_tail = fk.matrix @ Vector((0, fk.bone.length, 0))
df_tail = df.matrix @ Vector((0, df.bone.length, 0))
print('FK tail world:', tuple(round(v,3) for v in fk_tail))
print('Deform tail world:', tuple(round(v,3) for v in df_tail))
# they should match (COPY_TRANSFORMS)
dist = (fk_tail - df_tail).length
print('dist:', round(dist, 4), 'OK' if dist < 0.01 else 'FAIL')
