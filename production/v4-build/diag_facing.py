import bpy, math
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_anim.bvh(filepath="/home/hatch/workspace/_cj_v4_assets/bvh/61_03.bvh", target="ARMATURE", global_scale=1.0, frame_start=0, use_fps_scale=False, update_scene_fps=False, update_scene_duration=False)
src = next(o for o in bpy.data.objects if o.type == "ARMATURE")
sc = bpy.context.scene
SPB = src.pose.bones
def wp(n, f):
    sc.frame_set(f); bpy.context.view_layer.update()
    return (src.matrix_world @ SPB[n].matrix).to_translation()
for f in (1010, 1070, 1130, 1190, 1250, 1310, 1370, 1430, 1485):
    ank = wp("LeftFoot", f); toe = wp("LeftToeBase", f)
    ank2 = wp("RightFoot", f); toe2 = wp("RightToeBase", f)
    d = ((toe - ank) + (toe2 - ank2)) * 0.5
    yaw = math.degrees(math.atan2(d.x, -d.y))
    hips = wp("Hips", f)
    print(f, "facing yaw deg (0=-Y front):", round(yaw, 1), "hips", tuple(round(x,1) for x in hips))
