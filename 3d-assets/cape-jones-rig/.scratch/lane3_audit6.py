"""Lane 3 audit part 6: coverage using POSED bone positions (correct for any current pose)."""
import bpy, sys, numpy as np

BLEND = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.open_mainfile(filepath=BLEND)
bpy.context.view_layer.update()

rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)
vg_names = [vg.name for vg in mesh.vertex_groups]
vg_index = {g: i for i, g in enumerate(vg_names)}

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
w = co.reshape(n, 3)

def seg_dist(p, a, b):
    ab = b - a
    denom = (ab @ ab)
    if denom < 1e-12:
        return np.linalg.norm(p - a, axis=1)
    t = np.clip(((p - a) @ ab) / denom, 0, 1)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1)

print("FILE:", BLEND.split("/")[-1])
for pb in sorted(rig.pose.bones, key=lambda b: b.name):
    if not pb.name.startswith("finger_"):
        continue
    # posed head/tail in world
    m = np.array(rig.matrix_world @ pb.matrix, dtype=np.float64)
    a = m[:3, 3]
    # posed tail: matrix @ rest tail-local offset
    hl = np.array(pb.head, dtype=np.float64); tl = np.array(pb.tail, dtype=np.float64)
    b = (np.array(rig.matrix_world @ pb.matrix, dtype=np.float64) @ np.append(tl - hl, 1.0))[:3] + 0  # approx
    # better: tail world = head world + rotated (tail-head)
    R = m[:3, :3]
    bb = a + R @ (tl - hl)
    d = seg_dist(w, a, bb)
    near = np.where(d < 0.004)[0]
    gid = vg_index.get(pb.name, -1)
    own = 0
    for i in near:
        v = me.vertices[int(i)]
        for g in v.groups:
            if g.group == gid and g.weight >= 0.01:
                own += 1; break
    flag = "OK  " if own > 10 else ("WEAK" if own > 0 else "DEAD")
    print(f"{flag} {pb.name}: near={len(near)} own_w={own} posed_head={[round(v,3) for v in a]}")
