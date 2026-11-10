"""Trace hand_toon_L and pelvis_toon_L constraint chains."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

for n in ['hand_toon_L', 'pelvis_toon_L', 'head_toon' if 'head_toon' in arm.pose.bones else 'head_def_mstr']:
    pb = arm.pose.bones.get(n)
    if not pb:
        print(n, 'MISSING'); continue
    print(f'== {n} head=({pb.head.x:.3f},{pb.head.y:.3f},{pb.head.z:.3f})')
    for c in pb.constraints:
        tag = 'REPROP' if 'REPROP' in c.name else ('NOREP' if 'NOREP' in c.name else '--')
        tgt = getattr(c, 'subtarget', '')
        print(f'   [{tag}] {c.name} ({c.type}) -> {tgt} mute={c.mute}')
