"""Trace hand/head/thigh driver chains."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

def show(n):
    pb = arm.pose.bones.get(n)
    if not pb:
        print(n, 'MISSING'); return
    print(f"{n}: head=({pb.head.x:.3f},{pb.head.y:.3f},{pb.head.z:.3f}) parent={pb.parent.name if pb.parent else None}")

for n in ['hand_str_L', 'hand_fk_L', 'hand_def_mstr_L', 'hand_def_L',
          'head_str', 'head_fk', 'head_def_mstr',
          'pelvis_str', 'pelvis_str_L', 'pelvis_toon_L', 'thigh_toon_L', 'thigh_def_L']:
    show(n)
print('--- constraints on hand_def_mstr_L, hand_fk_L, pelvis_toon_L ---')
for n in ['hand_def_mstr_L', 'hand_fk_L', 'pelvis_toon_L', 'thigh_toon_L']:
    pb = arm.pose.bones.get(n)
    for c in pb.constraints:
        tgt = ''
        if c.type == 'ARMATURE':
            tgt = [t.subtarget for t in c.targets]
        elif hasattr(c, 'subtarget'):
            tgt = getattr(c, 'subtarget', '')
        print(f"  {n}.{c.type} -> {tgt}")
