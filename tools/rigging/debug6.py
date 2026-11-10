"""Why doesn't hand_ik_mstr_L follow wrist_str_L?"""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
bpy.context.view_layer.update()
ws = arm.pose.bones['wrist_str_L']
hm = arm.pose.bones['hand_ik_mstr_L']
print('wrist_str_L matrix head:', tuple(round(v, 3) for v in ws.head))
print('wrist_str_L matrix_basis translation:', tuple(round(v, 3) for v in ws.matrix_basis.col[3][:3]))
print('hand_ik_mstr_L head:', tuple(round(v, 3) for v in hm.head))
for c in hm.constraints:
    print(f'  {c.type}: mute={c.mute} inf={round(c.influence,3)} enabled={c.enabled}')
    if c.type == 'COPY_TRANSFORMS':
        print('    target:', c.target.name, 'subtarget:', c.subtarget, 'mix:', c.mix_mode)
# drivers affecting hand_ik_mstr_L?
for d in arm.animation_data.drivers:
    if 'hand_ik_mstr_L' in d.data_path:
        print('DRV:', d.data_path)
