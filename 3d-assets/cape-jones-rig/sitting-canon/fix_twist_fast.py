"""Fix over-rotated quaternions via fcurves (fast, no frame_set)."""
import bpy, re
from mathutils import Quaternion

rig = bpy.data.objects.get('CapeJones_Rig')
act = rig.animation_data.action

# group fcurves by bone
bones = {}
for fc in act.fcurves:
    if 'rotation_quaternion' not in fc.data_path:
        continue
    m = re.search(r'pose\.bones\["([^"]+)"\]', fc.data_path)
    if not m:
        continue
    bn = m.group(1)
    bones.setdefault(bn, {})[fc.array_index] = fc

fixed_bones = 0
for bn, comps in bones.items():
    if len(comps) != 4:
        continue
    fcs = [comps[i] for i in range(4)]
    nkeys = len(fcs[0].keyframe_points)
    fixed_keys = 0
    for ki in range(nkeys):
        w = fcs[0].keyframe_points[ki].co[1]
        x = fcs[1].keyframe_points[ki].co[1]
        y = fcs[2].keyframe_points[ki].co[1]
        z = fcs[3].keyframe_points[ki].co[1]
        q = Quaternion((w, x, y, z))
        if q.angle > 3.14159:
            # flip to shorter equivalent
            for ci, fc in enumerate(fcs):
                kp = fc.keyframe_points[ki]
                kp.co[1] = -kp.co[1]
                kp.handle_left[1] = -kp.handle_left[1]
                kp.handle_right[1] = -kp.handle_right[1]
            fixed_keys += 1
    if fixed_keys:
        fixed_bones += 1
        print(f"  {bn}: {fixed_keys} keys flipped", flush=True)
        for fc in fcs:
            fc.update()

bpy.ops.wm.save_as_mainfile(filepath='/home/hatch/workspace/sitcanon-work/scene_sit.blend')
print(f"FIXED {fixed_bones} bones, saved", flush=True)
