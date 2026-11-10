"""Stage 1A: identify cape verts, save indices to cape_verts.npz. No big .blend save."""
import bpy
import numpy as np
from collections import defaultdict

SRC = "/home/hatch/workspace/sitcanon-work/scene_anim_placed3.blend"
NPZ = "/home/hatch/workspace/capebake-work/cape_verts.npz"

bpy.ops.wm.open_mainfile(filepath=SRC)
body = bpy.data.objects["CapeJones_Body"]
mesh = body.data
nv = len(mesh.vertices)
print(f"body verts {nv}", flush=True)

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
sizes = np.bincount(comp_id)
co = np.empty(nv * 3, dtype=np.float64)
mesh.vertices.foreach_get("co", co)
co = co.reshape(nv, 3)
cent = np.zeros((nc, 3))
np.add.at(cent, comp_id, co)
cent /= sizes[:, None]
bmax = np.full((nc, 3), -1e9)
np.maximum.at(bmax, comp_id, co)
bmin = np.full((nc, 3), 1e9)
np.minimum.at(bmin, comp_id, co)
print(f"components: {nc}", flush=True)

mat = mesh.materials[0]
img = None
for nd in mat.node_tree.nodes:
    if nd.type == 'TEX_IMAGE' and nd.image:
        img = nd.image
        break
uv_layer = mesh.uv_layers.active
nloops = len(mesh.loops)
luv = np.empty(nloops * 2, dtype=np.float64)
uv_layer.data.foreach_get("uv", luv)
luv = luv.reshape(nloops, 2)
lvi = np.empty(nloops, dtype=np.int64)
mesh.loops.foreach_get("vertex_index", lvi)
vuv = np.zeros((nv, 2))
uniq_v, first_idx = np.unique(lvi, return_index=True)
vuv[uniq_v] = luv[first_idx]
small = img.copy()
small.scale(1024, 1024)
px = np.empty(1024 * 1024 * 4, dtype=np.float32)
small.pixels.foreach_get(px)
px = px.reshape(1024, 1024, 4)
rng = np.random.default_rng(7)
comp_rgb = np.zeros((nc, 3))
comp_darkfrac = np.zeros(nc)
for cid in range(nc):
    idx = np.nonzero(comp_id == cid)[0]
    if len(idx) > 60:
        idx = rng.choice(idx, 60, replace=False)
    u = np.clip((vuv[idx, 0] * 1023).astype(int), 0, 1023)
    v = np.clip((vuv[idx, 1] * 1023).astype(int), 0, 1023)
    cols = px[v, u, :3]
    comp_rgb[cid] = np.median(cols, axis=0)
    comp_darkfrac[cid] = float((cols.max(axis=1) < 0.10).mean())
bpy.data.images.remove(small)

cape_comps = []
for cid in range(nc):
    dark = comp_rgb[cid].max() < 0.15 and comp_darkfrac[cid] >= 0.65
    back = cent[cid][1] > 0.025
    torso_span = bmax[cid][2] > 0.20 and bmin[cid][2] < 0.85
    bottom_corner = cent[cid][1] > 0.040 and bmax[cid][2] <= 0.20
    big_enough = sizes[cid] >= 200
    if dark and big_enough and ((back and torso_span) or bottom_corner):
        cape_comps.append(cid)

# ---- pass 2 additions: dark fragments touching the v1 cape layer ----
v1set = set(cape_comps)
cape_pts = co[np.isin(comp_id, list(v1set))]
cape_sample = cape_pts[rng.choice(len(cape_pts), min(30000, len(cape_pts)), replace=False)]
added = []
for cid in range(nc):
    if cid in v1set or sizes[cid] < 50 or comp_rgb[cid].max() >= 0.115:
        continue
    idx = np.nonzero(comp_id == cid)[0]
    if len(idx) > 300:
        idx = rng.choice(idx, 300, replace=False)
    P = co[idx]
    d = np.sqrt(((P[:, None, :] - cape_sample[None, :, :]) ** 2).sum(axis=2)).min()
    if d <= 0.005:
        added.append(cid)
for extra in (191,):  # front collar ring piece (dist measured across the neck; ring partners 99/190/223 already in)
    if extra not in v1set and extra not in added:
        added.append(extra)
print(f"pass2 additions: {len(added)} comps -> {int(sizes[added].sum()) if added else 0} verts: {added}", flush=True)
cape_comps = cape_comps + added
cape_idx = np.nonzero(np.isin(comp_id, cape_comps))[0].astype(np.int64)
print(f"cape components FINAL: {len(cape_comps)} -> {len(cape_idx)} verts", flush=True)
assert 200000 < len(cape_idx) < 320000
np.savez(NPZ, cape_idx=cape_idx, cape_comps=np.array(cape_comps))
print(f"SAVED {NPZ}", flush=True)
print("STAGE1A DONE", flush=True)
