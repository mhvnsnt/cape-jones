"""Find what drives the ik pivot points / mstr bones."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

def cons(n):
    pb = arm.pose.bones.get(n)
    if not pb:
        print(n, 'MISSING'); return
    print(f"== {n} head=({pb.head.x:.3f},{pb.head.y:.3f},{pb.head.z:.3f}) parent={pb.parent.name if pb.parent else None}")
    for c in pb.constraints:
        if c.type == 'ARMATURE':
            tgt = [(t.target.name if t.target else '?', t.subtarget) for t in c.targets]
        else:
            tgt = (c.target.name + '.' + getattr(c, 'subtarget', '') if getattr(c, 'target', None) else '')
        print(f"    {c.type} -> {tgt} inf={round(c.influence,3)}")

for n in ['hand_ik_pivot_point_L', 'hand_mstr_L', 'hand_ik_mstr_L',
          'elbow_str_L', 'arm_mstr_L', 'forearm_fk_mstr_L']:
    cons(n)
