import bpy
import numpy as np
from collections import Counter, defaultdict

body = bpy.data.objects["CapeJones_Body"]
mesh = body.data
nv = len(mesh.vertices)

# ---- union-find over edges ----
ne = len(mesh.edges)
earr = np.empty(ne * 2, dtype=np.int64)
mesh.edges.foreach_get("vertices", earr)
earr = earr.reshape(ne, 2)
parent = np.arange(nv, dtype=np.int64)

def find(x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root

for a, b in earr:
    ra, rb = find(int(a)), find(int(b))
    if ra != rb:
        parent[ra] = rb
labels = np.array([find(i) for i in range(nv)], dtype=np.int64)
uniq, comp_id = np.unique(labels, return_inverse=True)
nc = len(uniq)
print(f"components: {nc}")
sizes = np.bincount(comp_id)

co = np.empty(nv * 3, dtype=np.float64)
mesh.vertices.foreach_get("co", co)
co = co.reshape(nv, 3)
cent = np.zeros((nc, 3))
np.add.at(cent, comp_id, co)
cent /= sizes[:, None]
bmin = np.full((nc, 3), 1e9)
bmax = np.full((nc, 3), -1e9)
np.minimum.at(bmin, comp_id, co)
np.maximum.at(bmax, comp_id, co)

# ---- dominant bone per component (sampled: every vert, cheap max) ----
gname = {g.index: g.name for g in body.vertex_groups}
comp_bones = defaultdict(Counter)
for v in mesh.vertices:
    if v.groups:
        g = max(v.groups, key=lambda gg: gg.weight)
        comp_bones[comp_id[v.index]][gname[g.group]] += 1

# ---- rig bone positions in body-local space (facing reference) ----
rig = bpy.data.objects["CapeJones_Rig"]
M = np.array(body.matrix_world.inverted() @ rig.matrix_world)
def bonepos(name):
    b = rig.data.bones[name]
    h = np.array([b.head_local.x, b.head_local.y, b.head_local.z, 1.0])
    return (M @ h)[:3]
for bn in ("root", "pelvis", "chest", "neck_1", "head"):
    print(f"bone {bn} local pos: {bonepos(bn).round(3)}")
print(f"body bbox local: min={co.min(axis=0).round(3)} max={co.max(axis=0).round(3)}")

# ---- texture sampling per component ----
mat = mesh.materials[0]
img = None
for nd in mat.node_tree.nodes:
    if nd.type == 'TEX_IMAGE' and nd.image:
        img = nd.image
        break
print("texture:", img.name if img else None, img.size[:] if img else None)
uv_layer = mesh.uv_layers.active
nloops = len(mesh.loops)
luv = np.empty(nloops * 2, dtype=np.float64)
uv_layer.data.foreach_get("uv", luv)
luv = luv.reshape(nloops, 2)
lvi = np.empty(nloops, dtype=np.int64)
mesh.loops.foreach_get("vertex_index", lvi)
uv = np.zeros((nv, 2))
uniq_v, first_idx = np.unique(lvi, return_index=True)
uv[uniq_v] = luv[first_idx]
small = img.copy()
small.scale(256, 256)
px = np.empty(256 * 256 * 4, dtype=np.float32)
small.pixels.foreach_get(px)
px = px.reshape(256, 256, 4)
def sample_color(cid):
    idx = np.nonzero(comp_id == cid)[0]
    if len(idx) > 40:
        idx = idx[:: max(1, len(idx) // 40)]
    u = np.clip((uv[idx, 0] * 255).astype(int), 0, 255)
    v = np.clip((uv[idx, 1] * 255).astype(int), 0, 255)
    cols = px[v, u, :3]
    return cols.mean(axis=0)

order = np.argsort(-sizes)
print("\nTop 40 components by size:")
for cid in order[:40]:
    db = comp_bones[int(cid)].most_common(2)
    col = sample_color(int(cid))
    print(f"  comp {cid}: size={sizes[cid]} cent={cent[cid].round(3)} bboxY=[{bmin[cid][1]:.3f},{bmax[cid][1]:.3f}] bboxZ=[{bmin[cid][2]:.3f},{bmax[cid][2]:.3f}] bones={db} texRGB={col.round(3)}")
print("DONE")
