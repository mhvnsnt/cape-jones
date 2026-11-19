import bpy, math
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/scene_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
act = bpy.data.actions["DanceV4Loop"]
if not rig.animation_data: rig.animation_data_create()
rig.animation_data.action = act
def wp(n):
    pb = RPB[n]
    return rig.matrix_world @ pb.head, rig.matrix_world @ pb.tail
for f in (5, 25, 49):
    sc.frame_set(f); bpy.context.view_layer.update()
    print("FRAME", f)
    for n in ("DEF-foot.L", "DEF-toe.L", "DEF-foot.R", "DEF-hand.L", "DEF-hand.R", "DEF-spine", "DEF-spine.006"):
        h, t = wp(n)
        print("  ", n, "head", tuple(round(x,3) for x in h), "tail", tuple(round(x,3) for x in t))
    for n in ("hand_ik.L", "hand_ik.R", "foot_ik.L", "hips", "chest", "torso"):
        pb = RPB[n]
        p = (rig.matrix_world @ pb.matrix).to_translation()
        print("   ctrl", n, tuple(round(x,3) for x in p))
    # facing from toes
    hl, tl = wp("DEF-foot.L"); hr, tr = wp("DEF-foot.R")
    facing = ((tl - hl) + (tr - hr)) * 0.5
    print("   facing toe dir:", tuple(round(x,3) for x in facing.normalized()))
