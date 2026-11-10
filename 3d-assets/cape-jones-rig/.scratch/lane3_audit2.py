"""Lane 3 audit part 2 (numpy-fast): thresholded weights + spatial sampling."""
import bpy, numpy as np
from collections import Counter

rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)
vg_names = [vg.name for vg in mesh.vertex_groups]

# thresholded histogram + sums (single pass)
for thr in (0.01, 0.1):
    hist = Counter(); maxsum = 0.0; minsum = 1e9; maxw = 0.0
    for v in me.vertices:
        s = 0.0; c = 0
        for g in v.groups:
            if g.weight >= thr:
                c += 1; s += g.weight
                if g.weight > maxw: maxw = g.weight
        hist[c] += 1
        if s > maxsum: maxsum = s
        if s < minsum: minsum = s
    print(f"THR={thr}: hist={dict(sorted(hist.items()))} maxsum={maxsum:.3f} minsum={minsum:.4f} maxw={maxw:.4f}")

# world coords via numpy
co = np.empty(n * 3, dtype=np.float64)
me.vertices.foreach_get("co", co)
co = co.reshape(n, 3)
mw = np.array(mesh.matrix_world, dtype=np.float64)
w = (mw @ np.vstack([co.T, np.ones(n)]))[:3].T

def bone_world(name):
    b = rig.pose.bones[name]
    v = rig.matrix_world @ b.head
    return np.array(v, dtype=np.float64)

for side in ("L", "R"):
    print(f"hand_{side} head world =", bone_world(f"hand_{side}"))
print("X range of world verts:", w[:, 0].min(), w[:, 0].max())

# nearest verts to each hand bone
for side in ("L", "R"):
    c = bone_world(f"hand_{side}")
    d = np.linalg.norm(w - c, axis=1)
    idx = np.argpartition(d, 8)[:8]
    idx = idx[np.argsort(d[idx])]
    print(f"--- verts near hand_{side} (dist, x, groups>=0.01) ---")
    for i in idx:
        v = me.vertices[i]
        gs = [(vg_names[g.group], round(g.weight, 3)) for g in v.groups if g.weight >= 0.01]
        print(f"  d={d[i]:.4f} x={w[i,0]:.3f} n={len(gs)} {gs[:6]}")

# L-hand finger check: any finger-group weight on verts with x<0 near left hand?
cL = bone_world("hand_L")
dL = np.linalg.norm(w - cL, axis=1)
maskL = dL < 0.15
finger_ids = {i for i, g in enumerate(vg_names) if g.startswith("finger_")}
cntL = cntR = 0
for i in np.where(maskL)[0]:
    v = me.vertices[i]
    for g in v.groups:
        if g.group in finger_ids and g.weight >= 0.01:
            if vg_names[g.group].endswith("_L"): cntL += 1
            else: cntR += 1
print("L-hand region verts w/ _L finger weights>=0.01:", cntL, " w/ _R finger weights:", cntR)
