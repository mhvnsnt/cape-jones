"""Debug: did guides move? did toon bones follow?"""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
for n in ['pelvis_str_L', 'thigh_toon_L', 'thigh_def_L', 'master_torso_str', 'spine_1_toon']:
    pb = arm.pose.bones.get(n)
    rb = arm.data.bones.get(n)
    print(f"{n}: pose_head=({pb.head.x:.3f},{pb.head.y:.3f},{pb.head.z:.3f}) rest_head=({rb.head_local.x:.3f},{rb.head_local.y:.3f},{rb.head_local.z:.3f})")
print('reproportion =', arm.data.get('reproportion'))
# check a driver: is it using the property?
for d in arm.animation_data.drivers[:3]:
    print('drv:', d.data_path, '<-', d.driver.variables[0].targets[0].data_path if d.driver.variables else None)
