"""Lane 3 audit part 3: depsgraph-evaluated positions, verts near each FINGER bone."""
import bpy, numpy as np

rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
print("mesh matrix_world is identity-ish:", np.allclose(np.array(mesh.matrix_world), np.eye(4), atol=1e-6))
print("rig matrix_world is identity-ish:", np.allclose(np.array(rig.matrix_world), np.eye(4), atol=1e-6))

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data  # evaluated
n = len(ev.vertices)
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
w = co.reshape(n, 3)  # evaluated mesh already in world space (identity matrix_world)

vg_names = [vg.name for vg in mesh.vertex_groups]
finger_ids = {i for i, g in enumerate(vg_names) if g.startswith("finger_")}

print("== per finger bone: nearest verts' groups ==")
for pb in sorted(rig.pose.bones, key=lambda b: b.name):
    if not pb.name.startswith("finger_"):
        continue
    head = np.array(rig.matrix_world @ pb.head, dtype=np.float64)
    tail = np.array(rig.matrix_world @ pb.tail, dtype=np.float64)
    mid = (head + tail) / 2
    d = np.linalg.norm(w - mid, axis=1)
    idx = np.argpartition(d, 5)[:5]
    # any finger-group weight >= 0.01 among 50 nearest?
    idx50 = np.argpartition(d, 50)[:50]
    fw = {}
    for i in idx50:
        v = mesh.data.vertices[int(i)]
        for g in v.groups:
            if g.group in finger_ids and g.weight >= 0.01:
                fw[vg_names[g.group]] = fw.get(vg_names[g.group], 0) + 1
    dmin = d[idx].min()
    has = "OK " if fw else "NONE"
    print(f"{has} {pb.name}: nearest_vert_d={dmin:.4f} finger-w>=0.01 nearby={dict(sorted(fw.items()))}")
