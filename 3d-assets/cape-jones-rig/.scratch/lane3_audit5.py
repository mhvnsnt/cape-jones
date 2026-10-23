"""Lane 3 audit part 5: run on w5r_clean.blend — normalization, pruned?, finger coverage (tight radius)."""
import bpy, sys, numpy as np
from collections import Counter

BLEND = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.open_mainfile(filepath=BLEND)

rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)
vg_names = [vg.name for vg in mesh.vertex_groups]

print("FILE:", BLEND)
thr = 0.01
hist = Counter(); maxsum = 0.0; minsum = 1e9
for v in me.vertices:
    s = 0.0; c = 0
    for g in v.groups:
        if g.weight >= thr:
            c += 1; s += g.weight
    hist[c] += 1
    maxsum = max(maxsum, s); minsum = min(minsum, s)
print(f"THR=0.01 hist={dict(sorted(hist.items()))} maxsum={maxsum:.3f} minsum={minsum:.4f}")
over4 = sum(c * k for k, c in hist.items() if k > 4)
print("verts with >4 groups @0.01:", over4)

# finger bone constraints (are finger bones directly posable?)
fb = rig.pose.bones["finger_index_1_L"]
print("finger_index_1_L constraints:", [(c.type, c.mute) for c in fb.constraints])
print("finger_index_1_L drivers:", len(rig.animation_data.drivers) if rig.animation_data else 0)

# tight-radius coverage: verts within 4mm of bone segment, own-group weight>=0.01
deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
w = co.reshape(n, 3)

def seg_dist(p, a, b):
    ab = b - a
    t = np.clip(((p - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1)

print("== finger bone coverage (verts within 4mm of segment, own-group w>=0.01) ==")
for pb in sorted(rig.pose.bones, key=lambda b: b.name):
    if not pb.name.startswith("finger_"):
        continue
    a = np.array(pb.head, dtype=np.float64); b = np.array(pb.tail, dtype=np.float64)
    d = seg_dist(w, a, b)
    near = np.where(d < 0.004)[0]
    gid = vg_names.index(pb.name) if pb.name in vg_names else -1
    own = 0
    for i in near:
        v = me.vertices[int(i)]
        for g in v.groups:
            if g.group == gid and g.weight >= 0.01:
                own += 1; break
    flag = "OK " if own > 10 else ("WEAK" if own > 0 else "DEAD")
    print(f"{flag} {pb.name}: near={len(near)} own_w={own}")
