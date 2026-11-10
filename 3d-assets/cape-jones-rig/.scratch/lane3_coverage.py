"""Lane 3 coverage check v2: segment = (pose.bones.head, pose.bones.tail) directly
(these ARE the posed/bind positions), vs depsgraph-evaluated mesh."""
import bpy, sys
import numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
bpy.context.view_layer.update()
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)
vg_names = [v.name for v in mesh.vertex_groups]

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
P = co.reshape(n, 3)

def seg_dist(p, a, b):
    ab = b - a
    t = np.clip(((p - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1)

print("== finger bone coverage (correct segments) ==")
all_ok = True
for pb in sorted(rig.pose.bones, key=lambda b: b.name):
    if not pb.name.startswith("finger_"):
        continue
    a = np.array(pb.head, dtype=np.float64)
    b = np.array(pb.tail, dtype=np.float64)
    d = seg_dist(P, a, b)
    near = np.where(d < 0.004)[0]
    gid = vg_names.index(pb.name)
    own = 0
    for i in near:
        v = me.vertices[int(i)]
        for g in v.groups:
            if g.group == gid and g.weight >= 0.01:
                own += 1
                break
    flag = "OK  " if own > 10 else ("WEAK" if own > 0 else "DEAD")
    if own <= 10:
        all_ok = False
    print(f"{flag} {pb.name}: near={len(near)} own_w>={0.01}={own}")
print("ALL OK" if all_ok else "STILL BROKEN")
