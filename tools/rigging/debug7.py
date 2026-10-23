"""Check REPROP/NOREP constraint names on deform + control bones."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

for n in ['thigh_def_L', 'hand_def_L', 'hand_fk_L', 'thigh_toon_L', 'forearm_def_L']:
    pb = arm.pose.bones[n]
    print(f'== {n}')
    for c in pb.constraints:
        tag = 'REPROP' if 'REPROP' in c.name else ('NOREP' if 'NOREP' in c.name else '--')
        tgt = getattr(c, 'subtarget', '')
        print(f'   [{tag}] {c.name} ({c.type}) -> {tgt} mute={c.mute}')
