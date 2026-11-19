import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/rig_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
def chain(name):
    out, b = [], rig.data.bones.get(name)
    while b:
        out.append(b.name); b = b.parent
    return " <- ".join(out)
for n in ("neck", "head", "ORG-spine.004", "MCH-spine.004", "DEF-spine.004"):
    if n in rig.data.bones:
        print(n, "parents:", chain(n))
        pb = RPB[n]
        print("   cons:", [(c.type, getattr(c, 'subtarget', '')) for c in pb.constraints])
def show(tag):
    bpy.context.view_layer.update()
    print(tag, "DEF-spine.004 head:", tuple(round(x,3) for x in (rig.matrix_world @ RPB["DEF-spine.004"].head)),
          "DEF-spine.003 len:", round(((rig.matrix_world @ RPB["DEF-spine.003"].tail) - (rig.matrix_world @ RPB["DEF-spine.003"].head)).length, 3))
sc.frame_set(1); show("REST      ")
RPB["torso"].location = (0, 0, -0.2); show("TORSO z-0.2")
RPB["torso"].location = (0, 0, 0)
RPB["chest"].location = (0, 0, -0.2); show("CHEST z-0.2")
RPB["chest"].location = (0, 0, 0)
RPB["hips"].location = (0, 0, -0.2); show("HIPS  z-0.2")
