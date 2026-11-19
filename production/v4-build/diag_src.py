import bpy
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_anim.bvh(filepath="/home/hatch/workspace/_cj_v4_assets/bvh/61_03.bvh", target="ARMATURE", global_scale=1.0, frame_start=0, use_fps_scale=False, update_scene_fps=False, update_scene_duration=False)
src = next(o for o in bpy.data.objects if o.type == "ARMATURE")
sc = bpy.context.scene
for f in (0, 1, 2, 1010, 1250):
    sc.frame_set(f); bpy.context.view_layer.update()
    print("FRAME", f)
    for n in ("Hips", "Head", "LeftHand", "RightHand", "LeftFoot", "RightFoot", "LeftArm", "RightArm"):
        pb = src.pose.bones[n]
        p = (src.matrix_world @ pb.matrix).to_translation()
        print("  ", n, tuple(round(x, 2) for x in p))
    print("   obj rot", tuple(round(x, 3) for x in src.rotation_euler), "scale", tuple(src.scale))
