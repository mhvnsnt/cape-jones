import bpy, math
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/scene_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
rig.animation_data.action = bpy.data.actions["DanceV4Loop"]
import numpy as np
prev = {}
for f in range(40, 58):
    sc.frame_set(f); bpy.context.view_layer.update()
    bad = []
    for n in ("DEF-upper_arm.L","DEF-forearm.L","DEF-hand.L","DEF-upper_arm.R","DEF-forearm.R","DEF-hand.R",
              "DEF-thigh.L","DEF-shin.L","DEF-foot.L","DEF-thigh.R","DEF-shin.R","DEF-foot.R",
              "DEF-spine.002","DEF-spine.003","DEF-cape.003","DEF-cape.005"):
        pb = RPB[n]
        h = rig.matrix_world @ pb.head
        if h.length > 2.0 or any(math.isnan(x) for x in h):
            bad.append((n, tuple(round(x,2) for x in h)))
        if n in prev:
            jump = (h - prev[n]).length
            if jump > 0.25:
                bad.append((n + " JUMP", round(jump, 2)))
        prev[n] = h
    print("f", f, "bad:", bad if bad else "-")
