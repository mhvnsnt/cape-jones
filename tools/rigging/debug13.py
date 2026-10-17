"""Inspect forearm_def_L in warped rig."""
import bpy, json
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
J = json.load(open('/tmp/cj_joints.json'))
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
bpy.context.view_layer.update()
for n in ['forearm_def_L', 'elbow_str_L', 'forearm_toon_L', 'elbow_toon_L', 'hand_str_L']:
    pb = arm.pose.bones.get(n)
    rb = arm.data.bones.get(n)
    print(f"{n}: rest=({rb.head_local.x:.3f},{rb.head_local.y:.3f},{rb.head_local.z:.3f}) pose=({pb.head.x:.3f},{pb.head.y:.3f},{pb.head.z:.3f})")
    for c in pb.constraints:
        print(f"    {c.type} -> {getattr(c,'subtarget','')} mute={c.mute}")
print('want elbow:', J['elbow_L'])
