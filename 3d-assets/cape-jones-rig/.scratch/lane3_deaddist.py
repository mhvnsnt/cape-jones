import bpy
import numpy as np
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
bpy.context.view_layer.update()
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
n = len(ev.vertices)
co = np.empty(n*3); ev.vertices.foreach_get("co", co); P = co.reshape(n,3)
dead = ["finger_index_1_L","finger_index_2_L","finger_index_3_L",
        "finger_middle_2_L","finger_middle_3_L",
        "finger_pinky_1_R","finger_pinky_2_R","finger_pinky_3_R",
        "finger_ring_2_R","finger_ring_3_R","finger_thumb_2_L","finger_thumb_2_R"]
for bn in dead:
    pb = rig.pose.bones[bn]
    h = np.array(pb.head); t = np.array(pb.tail)
    # distance to segment
    ab = t-h
    tt = np.clip(((P-h)@ab)/(ab@ab),0,1)
    d = np.linalg.norm(P-(h+tt[:,None]*ab),axis=1)
    print(f"{bn}: min_d_to_seg={d.min():.4f}")
