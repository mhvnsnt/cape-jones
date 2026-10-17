import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
vg_names = [v.name for v in mesh.vertex_groups]
for bn in ["finger_pinky_1_R","finger_pinky_2_R","finger_pinky_3_R"]:
    gid = vg_names.index(bn)
    cnt_any = sum(1 for v in me.vertices for g in v.groups if g.group==gid)
    print(f"{bn}: any_weight={cnt_any}")
# what groups DO the verts near the R pinky have?
import numpy as np
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
n = len(ev.vertices)
co = np.empty(n*3); ev.vertices.foreach_get("co", co); P = co.reshape(n,3)
pb = rig.pose.bones["finger_pinky_2_R"]
c = (np.array(pb.head)+np.array(pb.tail))/2
d = np.linalg.norm(P-c, axis=1)
idx = np.where(d<0.015)[0]
print(f"verts within 15mm of pinky_2_R center: {len(idx)}")
from collections import Counter
gc = Counter()
for i in idx[:50]:
    v = me.vertices[int(i)]
    for g in v.groups:
        if g.weight >= 0.1:
            gc[vg_names[g.group]] += 1
print("dominant groups:", gc.most_common(8))
