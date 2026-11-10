"""Debug: why doesn't FK posing deform the mesh?"""
import bpy, math
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_cape_sep.blend')
arm = bpy.data.objects['CapeJones_Rig']
char = bpy.data.objects['CapeJones_Body']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

# check FK bone and deform bone
fk = arm.pose.bones['upperarm_fk_L']
df = arm.pose.bones['upperarm_L']
print('FK bone:', fk.name, 'rotmode:', fk.rotation_mode)
print('Deform constraints:', [(c.name, c.type, round(c.influence,2)) for c in df.constraints])
# check the driver
for c in df.constraints:
    if c.name == 'FK':
        print('FK influence:', c.influence)
        if c.animation_data and c.animation_data.drivers:
            for d in c.animation_data.drivers:
                print('  driver:', d.data_path, d.driver.expression if hasattr(d.driver,'expression') else d.driver.type)
# try rotating FK
fk.rotation_mode = 'XYZ'
fk.rotation_euler = (0, math.radians(-80), 0)
bpy.context.view_layer.update()
print('FK head after:', tuple(round(v,3) for v in fk.head))
print('FK tail after:', tuple(round(v,3) for v in fk.tail))
print('Deform head after:', tuple(round(v,3) for v in df.head))
print('Deform tail after:', tuple(round(v,3) for v in df.tail))
# check if deform moved
