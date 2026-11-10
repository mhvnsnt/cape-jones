"""Build bake-ready scene from placed3 (READ-ONLY source).
- Identify cape shells (components: dark texture, back side +Y, torso span)
- Separate them into CapeJones_Cape, add Armature->Cloth with cape_pin
- Body-minus-cape stays as render body; add decimated collision proxy + chair/floor collision
- Save to capebake-work/bake_scene.blend (checkpointed)
"""
import bpy
import numpy as np
from collections import Counter, defaultdict

SRC = "/home/hatch/workspace/sitcanon-work/scene_anim_placed3.blend"
OUT = "/home/hatch/workspace/capebake-work/stage1_separated.blend"

bpy.ops.wm.open_mainfile(filepath=SRC)
body = bpy.data.objects["CapeJones_Body"]
mesh = body.data
nv = len(mesh.vertices)
print(f"body verts {nv}", flush=True)

# ---------- components (union-find) ----------
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

# ---------- texture color per component ----------
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

# ---------- cape selection predicate ----------
cape_comps = []
for cid in range(nc):
    dark = comp_rgb[cid].max() < 0.15 and comp_darkfrac[cid] >= 0.65
    back = cent[cid][1] > 0.025
    torso_span = bmax[cid][2] > 0.20 and bmin[cid][2] < 0.85
    bottom_corner = cent[cid][1] > 0.040 and bmax[cid][2] <= 0.20
    big_enough = sizes[cid] >= 200
    if dark and big_enough and ((back and torso_span) or bottom_corner):
        cape_comps.append(cid)
cape_mask_arr = np.isin(comp_id, cape_comps)
print(f"cape components: {len(cape_comps)} -> {int(cape_mask_arr.sum())} verts", flush=True)
for cid in cape_comps:
    print(f"  cape comp {cid}: size={sizes[cid]} cent={cent[cid].round(3)} zrange=[{bmin[cid][2]:.2f},{bmax[cid][2]:.2f}] medRGB={comp_rgb[cid].round(3)} darkfrac={comp_darkfrac[cid]:.2f}", flush=True)
print("near-miss dark comps rejected by geometry gates:", flush=True)
for cid in range(nc):
    if comp_rgb[cid].max() < 0.15 and comp_darkfrac[cid] >= 0.65 and cid not in cape_comps and sizes[cid] >= 200:
        print(f"  nearmiss comp {cid}: size={sizes[cid]} cent={cent[cid].round(3)} zrange=[{bmin[cid][2]:.2f},{bmax[cid][2]:.2f}]", flush=True)
assert 150000 < int(cape_mask_arr.sum()) < 280000, "cape vert count out of expected range — ABORT before separation"

# ---------- separate cape verts into CapeJones_Cape ----------
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
for i in np.nonzero(cape_mask_arr)[0]:
    mesh.vertices[int(i)].select = True
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='SELECTED')
bpy.ops.object.mode_set(mode='OBJECT')
cape = None
for o in bpy.data.objects:
    if o.type == 'MESH' and o != body and o.data != mesh and len(o.data.vertices) == int(cape_mask_arr.sum()):
        cape = o
        break
assert cape, "separated cape object not found"
cape.name = "CapeJones_Cape"
print(f"cape object: {cape.name} verts={len(cape.data.vertices)} body now {len(body.data.vertices)}", flush=True)
# cape: strip shape keys + corrective smooth; keep Armature first
if cape.data.shape_keys:
    for kb in list(cape.data.shape_keys.key_blocks)[1:]:
        cape.shape_key_remove(kb)
    cape.shape_key_remove(cape.data.shape_keys.key_blocks[0])
for m in list(cape.modifiers):
    if m.type == 'CORRECTIVE_SMOOTH':
        cape.modifiers.remove(m)
print("cape modifiers:", [(m.name, m.type) for m in cape.modifiers], flush=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("CHECKPOINT saved after separation", flush=True)

# ---------- pin group: neckline/shoulder band (bind space z ramp 0.68->0.78) ----------
cmesh = cape.data
pin = cmesh.vertices  # local coords == body local coords (same transform)
if "cape_pin" in cape.vertex_groups:
    cape.vertex_groups.remove(cape.vertex_groups["cape_pin"])
vg = cape.vertex_groups.new(name="cape_pin")
cco = np.empty(len(pin) * 3, dtype=np.float64)
pin.foreach_get("co", cco)
cco = cco.reshape(-1, 3)
w = np.clip((cco[:, 2] - 0.68) / 0.10, 0.0, 1.0)
# only the back panel band (y > -0.02) can pin; front drips stay free (cape has none in front, safety)
w[cco[:, 1] < -0.02] = 0.0
for i in np.nonzero(w > 0)[0]:
    vg.add([int(i)], float(w[i]), 'REPLACE')
print(f"pin verts>0: {int((w>0).sum())}, full pin: {int((w>=0.999).sum())}", flush=True)

# ---------- cloth modifier ----------
cloth = cape.modifiers.new("Cloth", 'CLOTH')
cs = cloth.settings
cs.quality = 12
cs.mass = 0.35
cs.tension_stiffness = 15.0
cs.compression_stiffness = 15.0
cs.shear_stiffness = 8.0
cs.bending_stiffness = 0.8
cs.tension_damping = 5.0
cs.compression_damping = 5.0
cs.shear_damping = 5.0
cs.bending_damping = 0.5
cs.air_damping = 1.0
cs.vertex_group_mass = "cape_pin"
try:
    cs.pin_stiffness = 1.0
except Exception:
    pass
col = cloth.collision_settings
col.use_collision = True
col.collision_quality = 3
col.distance_min = 0.010
col.use_self_collision = True
col.self_distance_min = 0.006
pc = cloth.point_cache
pc.frame_start, pc.frame_end = 1, 81
pc.use_disk_cache = False
print("cloth set", flush=True)

# ---------- collision proxy from body ----------
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.duplicate()
proxy = bpy.context.view_layer.objects.active
proxy.name = "Body_CollisionProxy"
if proxy.data.shape_keys:
    for kb in list(proxy.data.shape_keys.key_blocks)[1:]:
        proxy.shape_key_remove(kb)
    proxy.shape_key_remove(proxy.data.shape_keys.key_blocks[0])
for m in list(proxy.modifiers):
    proxy.modifiers.remove(m)
dec = proxy.modifiers.new("Decimate", 'DECIMATE')
dec.decimate_type = 'COLLAPSE'
dec.ratio = 0.03
arm = proxy.modifiers.new("Armature", 'ARMATURE')
arm.object = bpy.data.objects["CapeJones_Rig"]
pcoll = proxy.modifiers.new("Collision", 'COLLISION')
pcoll.settings.thickness_outer = 0.015
pcoll.settings.thickness_inner = 0.005
try:
    pcoll.settings.cloth_friction = 8.0
except Exception:
    pass
proxy.hide_render = True
print(f"proxy base verts {len(proxy.data.vertices)} ratio {dec.ratio}", flush=True)

# ---------- chair + floor collision ----------
chair = bpy.data.objects.get("loungeChairRelax(Clone)")
cc = chair.modifiers.new("Collision", 'COLLISION')
cc.settings.thickness_outer = 0.012
cc.settings.thickness_inner = 0.004
floor = bpy.data.objects.get("Floor")
fc = floor.modifiers.new("Collision", 'COLLISION')
fc.settings.thickness_outer = 0.010
print("colliders set", flush=True)

sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, 81
sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT}", flush=True)
print("BUILD DONE", flush=True)
