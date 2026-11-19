import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/scene_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
rig.animation_data.action = bpy.data.actions["DanceV4Loop"]
for f in (1, 49):
    sc.frame_set(f); bpy.context.view_layer.update()
    print("f", f)
    for n in ("hips", "torso", "chest", "neck"):
        m = rig.matrix_world @ RPB[n].matrix
        print("   ", n, tuple(round(x, 3) for x in m.to_translation()))
    h3 = rig.matrix_world @ RPB["DEF-spine.003"].head; t3 = rig.matrix_world @ RPB["DEF-spine.003"].tail
    print("    DEF-spine.003 len", round((t3 - h3).length, 3), "DEF-spine.004 head", tuple(round(x,3) for x in (rig.matrix_world @ RPB["DEF-spine.004"].head)))
