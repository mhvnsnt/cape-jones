import bpy, math
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/scene_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
# rest state: no action
sc.frame_set(1); bpy.context.view_layer.update()
def snap(tag):
    out = {}
    for n in ("DEF-spine","DEF-spine.001","DEF-spine.002","DEF-spine.003","DEF-spine.004","DEF-spine.005","DEF-spine.006"):
        pb = RPB[n]
        out[n] = tuple(round(x,3) for x in (rig.matrix_world @ pb.head))
    for n in ("hips","torso","chest","neck","head"):
        pb = RPB[n]
        m = rig.matrix_world @ pb.matrix
        out[n+"@"] = tuple(round(x,3) for x in m.to_translation())
        out[n+"Q"] = round(math.degrees(m.to_quaternion().angle),1)
    print(tag, out)
snap("REST")
rig.animation_data.action = bpy.data.actions["DanceV4Loop"]
for f in (5, 25):
    sc.frame_set(f); bpy.context.view_layer.update()
    snap(f"F{f}")
