"""Pass 2: dump full component table + adjacency of dark rejects to the v1 cape selection."""
import bpy
import numpy as np
import json
from collections import Counter, defaultdict

SRC = "/home/hatch/workspace/sitcanon-work/scene_anim_placed3.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
body = bpy.data.objects["CapeJones_Body"]
mesh = body.data
nv = len(mesh.vertices)

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
cent = np.zeros((nc, 3)); np.add.at(cent, comp_id, co); cent /= sizes[:, None]
bmax = np.full((nc, 3), -1e9); np.maximum.at(bmax, comp_id, co)
bmin = np.full((nc, 3), 1e9); np.minimum.at(bmin, comp_id, co)

gname = {g.index: g.name for g in body.vertex_groups}
comp_bones = defaultdict(Counter)
for v in mesh.vertices:
    if v.groups:
        g = max(v.groups, key=lambda gg: gg.weight)
        comp_bones[comp_id[v.index]][gname[g.group]] += 1

mat = mesh.materials[0]
img = None
for nd in mat.node_tree.nodes:
    if nd.type == 'TEX_IMAGE' and nd.image:
        img = nd.image; break
uv_layer = mesh.uv_layers.active
nloops = len(mesh.loops)
luv = np.empty(nloops * 2, dtype=np.float64); uv_layer.data.foreach_get("uv", luv); luv = luv.reshape(nloops, 2)
lvi = np.empty(nloops, dtype=np.int64); mesh.loops.foreach_get("vertex_index", lvi)
vuv = np.zeros((nv, 2)); uvv, fi = np.unique(lvi, return_index=True); vuv[uvv] = luv[fi]
small = img.copy(); small.scale(1024, 1024)
px = np.empty(1024 * 1024 * 4, dtype=np.float32); small.pixels.foreach_get(px); px = px.reshape(1024, 1024, 4)
rng = np.random.default_rng(7)
comp_rgb = np.zeros((nc, 3)); comp_darkfrac = np.zeros(nc)
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

# v1 selection
v1 = []
for cid in range(nc):
    dark = comp_rgb[cid].max() < 0.15 and comp_darkfrac[cid] >= 0.65
    back = cent[cid][1] > 0.025
    torso_span = bmax[cid][2] > 0.20 and bmin[cid][2] < 0.85
    bottom_corner = cent[cid][1] > 0.040 and bmax[cid][2] <= 0.20
    if dark and sizes[cid] >= 200 and ((back and torso_span) or bottom_corner):
        v1.append(cid)
v1set = set(v1)
cape_pts = co[np.isin(comp_id, v1)]
cape_sample = cape_pts[rng.choice(len(cape_pts), min(30000, len(cape_pts)), replace=False)]

table = []
for cid in range(nc):
    e = {"cid": int(cid), "size": int(sizes[cid]), "cent": cent[cid].round(4).tolist(),
         "bmin": bmin[cid].round(4).tolist(), "bmax": bmax[cid].round(4).tolist(),
         "medRGB": comp_rgb[cid].round(4).tolist(), "darkfrac": round(float(comp_darkfrac[cid]), 3),
         "bones": comp_bones[cid].most_common(2), "v1": cid in v1set}
    # adjacency for dark non-v1 comps
    if cid not in v1set and comp_rgb[cid].max() < 0.20 and sizes[cid] >= 50:
        idx = np.nonzero(comp_id == cid)[0]
        if len(idx) > 300:
            idx = rng.choice(idx, 300, replace=False)
        P = co[idx]
        d = np.sqrt(((P[:, None, :] - cape_sample[None, :, :]) ** 2).sum(axis=2)).min()
        e["dist_to_cape"] = round(float(d), 4)
    table.append(e)

with open("/home/hatch/workspace/capebake-work/comps.json", "w") as fh:
    json.dump(table, fh)
np.savez("/home/hatch/workspace/capebake-work/comp_id.npz", comp_id=comp_id)
print(f"table dumped: {nc} comps, v1={len(v1)} comps")
print("DARK REJECTS (not in v1):")
for e in table:
    if not e["v1"] and e["medRGB"] and max(e["medRGB"]) < 0.20 and e["size"] >= 50:
        print(f"  comp {e['cid']}: size={e['size']} cent={e['cent']} zrange=[{e['bmin'][2]},{e['bmax'][2]}] yrange=[{e['bmin'][1]},{e['bmax'][1]}] medRGB={e['medRGB']} darkfrac={e['darkfrac']} bones={e['bones']} dist_to_cape={e.get('dist_to_cape')}")
print("PASS2 DONE")
