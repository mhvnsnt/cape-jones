import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/scene_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
rig.animation_data.action = bpy.data.actions["DanceV4Loop"]
CHAIN = ["DEF-spine", "DEF-spine.001", "DEF-spine.002", "DEF-spine.003", "DEF-spine.004", "DEF-spine.005", "DEF-spine.006"]
for f in (1, 25, 49, 73):
    sc.frame_set(f); bpy.context.view_layer.update()
    pts = [rig.matrix_world @ RPB[n].head for n in CHAIN]
    pts.append(rig.matrix_world @ RPB[CHAIN[-1]].tail)
    L = sum((pts[i + 1] - pts[i]).length for i in range(len(pts) - 1))
    segs = [round((pts[i + 1] - pts[i]).length, 3) for i in range(len(pts) - 1)]
    print("f", f, "spine chain len", round(L, 3), "segs", segs)
