"""Inspect guide bones: locks, constraints, drivers."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_raw.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
guides = ['master_torso_str', 'pelvis_str', 'pelvis_str_L', 'knee_str_L', 'ankle_str_L',
          'shoulder_str_L', 'elbow_str_L', 'wrist_str_L', 'hand_str_L', 'clavi_str_L',
          'spine_ctrl_1_str', 'neck_ctrl_1_str', 'head_str', 'face_mstr_str', 'foot_str_L',
          'fing_ind_str_1_L', 'fing_thumb_str_1_L', 'elbow_pole_str_L', 'knee_pole_str_L',
          'toe_str_1_L', 'sole_str_L']
for n in guides:
    pb = arm.pose.bones.get(n)
    if not pb:
        print(n, 'MISSING')
        continue
    cons = [c.type for c in pb.constraints]
    print(f"{n}: cons={cons} lock_loc={tuple(pb.lock_location)} lock_rot={tuple(pb.lock_rotation)} lock_scale={tuple(pb.lock_scale)} rotmode={pb.rotation_mode}")
print('reproportion:', arm.data.get('reprojection', arm.data.get('reproportion')))
drv = arm.animation_data.drivers if arm.animation_data else []
print('armature drivers:', len(drv))
for d in drv[:10]:
    print('  drv:', d.data_path)
