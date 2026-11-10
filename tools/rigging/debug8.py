"""Compare default rig deform positions in ON vs OFF reproportion."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_raw.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

def set_repro(on):
    arm.data['reproportion'] = 1 if on else 0
    for pb in arm.pose.bones:
        for C in pb.constraints:
            if 'REPROP' in C.name:
                C.mute = not on
            elif 'NOREP' in C.name:
                C.mute = on
    bpy.context.view_layer.update()

for mode in [True, False]:
    set_repro(mode)
    print(f'--- reproportion {"ON" if mode else "OFF"} (default rig) ---')
    for n in ['thigh_def_L', 'hand_def_L', 'head_def_mstr']:
        pb = arm.pose.bones[n]
        print(f'  {n}: head=({pb.head.x:.3f},{pb.head.y:.3f},{pb.head.z:.3f})')
