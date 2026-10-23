"""Test: with reproportion=1, do FK/toon bones follow guides?"""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
arm.data['reproportion'] = 1
bpy.context.view_layer.update()
for n in ['hand_fk_L', 'hand_ik_pivot_L', 'hand_toon_L', 'hand_def_mstr_L',
          'head_fk', 'neck_3_fk', 'pelvis_toon_L', 'thigh_toon_L',
          'forearm_fk_L', 'upperarm_fk_L' if 'upperarm_fk_L' in arm.pose.bones else 'arm_fk_L']:
    pb = arm.pose.bones.get(n)
    if pb:
        print(f"{n}: head=({pb.head.x:.3f},{pb.head.y:.3f},{pb.head.z:.3f})")
# what drives hand_ik_pivot_L?
pb = arm.pose.bones.get('hand_ik_pivot_L')
for c in pb.constraints:
    tgt = [t.subtarget for t in c.targets] if c.type == 'ARMATURE' else getattr(c, 'subtarget', '')
    print('hand_ik_pivot_L.', c.type, '->', tgt, 'inf=', round(c.influence, 3))
arm.data['reproportion'] = 0
