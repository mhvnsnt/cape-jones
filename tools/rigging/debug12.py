"""Inspect baked rest positions (pose bones only)."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
bpy.context.view_layer.update()
for n in ['hand_str_L', 'hand_def_L', 'hand_fk_L', 'hand_toon_L',
          'head_str', 'head_def_mstr', 'head_fk',
          'thigh_def_L', 'pelvis_str_L', 'pelvis_toon_L', 'forearm_def_L']:
    pb = arm.pose.bones.get(n)
    rb = arm.data.bones.get(n)
    if not pb:
        print(n, 'NO POSE BONE'); continue
    rh = tuple(round(v, 3) for v in rb.head_local) if rb else None
    ph = tuple(round(v, 3) for v in pb.head)
    print(f"{n}: rest={rh} pose={ph}")
print('reproportion =', arm.data.get('reproportion'))
