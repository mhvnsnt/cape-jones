"""Lane 3: 3D distance from each R finger bone head to nearest evaluated vert."""
import bpy
import numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
bpy.context.view_layer.update()
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
n = len(ev.vertices)
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
P = co.reshape(n, 3)

for pb in sorted(rig.pose.bones, key=lambda b: b.name):
    if not (pb.name.startswith("finger_") and pb.name.endswith("_R")):
        continue
    h = np.array(pb.head)
    d = np.linalg.norm(P - h, axis=1)
    i = int(np.argmin(d))
    print(f"{pb.name}: head={np.round(h,3)} nearest_eval_vert_d={d[i]:.4f} vert_pos={np.round(P[i],3)}")
