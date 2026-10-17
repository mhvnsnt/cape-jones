import bpy
import numpy as np
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/led_test.blend")
bpy.context.view_layer.update()
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
vg_names = [v.name for v in mesh.vertex_groups]
def eval_pos():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = deps.objects.get(mesh.name).data
    co = np.empty(len(ev.vertices)*3); ev.vertices.foreach_get("co", co)
    return co.reshape(len(ev.vertices),3)
for bn in ["finger_thumb_1_R","finger_thumb_2_R"]:
    gid = vg_names.index(bn)
    idx = np.array([v.index for v in me.vertices for g in v.groups if g.group==gid and g.weight>=0.5])
    print(f"{bn}: {len(idx)} verts")
    if len(idx)==0: continue
    rig.animation_data.action = bpy.data.actions["led_press_R"]
    sc = bpy.context.scene
    sc.frame_set(1); bpy.context.view_layer.update(); P0 = eval_pos()
    sc.frame_set(12); bpy.context.view_layer.update(); P1 = eval_pos()
    move = np.linalg.norm(P1[idx]-P0[idx],axis=1)
    print(f"  f1->f12 mean move: {move.mean():.5f} max: {move.max():.5f}")
