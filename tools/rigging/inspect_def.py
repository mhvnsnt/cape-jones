"""Inspect deform bone drivers."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_raw.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
for n in ['thigh_def_L', 'forearm_def_L', 'spine_1_def', 'head_def_mstr', 'hand_def_L', 'shin_def_L']:
    pb = arm.pose.bones.get(n)
    if not pb:
        print(n, 'MISSING'); continue
    print('===', n, 'parent=', pb.parent.name if pb.parent else None)
    for c in pb.constraints:
        tgt = ''
        if hasattr(c, 'target') and c.target:
            tgt = f"{c.target.name}.{getattr(c, 'subtarget', '')}"
        elif c.type == 'ARMATURE':
            tgt = str([t.subtarget for t in c.targets])
        print(f"   {c.type} -> {tgt} inf={round(c.influence, 2)}")
