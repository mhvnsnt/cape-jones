import bpy
import numpy as np
from collections import defaultdict, deque

MECH = "/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend"
BAKED = "/home/hatch/workspace/sitcanon-work/scene_capebaked.blend"
OUT = "/home/hatch/workspace/sitcanon-work/scene_final.blend"

def world_eval_bbox(ob, frame=40):
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", arr)
    arr = arr.reshape(-1, 3)
    M = np.array(ev.matrix_world)
    w = (M[:3, :3] @ arr.T).T + M[:3, 3]
    ev.to_mesh_clear()
    return w.min(axis=0), w.max(axis=0)

# ---- 1. source cape world bbox in its own file ----
bpy.ops.wm.open_mainfile(filepath=BAKED)
src_cape = bpy.data.objects.get("CapeJones_Cape")
src_min, src_max = world_eval_bbox(src_cape)
print("SRC cape world bbox f40: min", src_min.round(3), "max", src_max.round(3))
def pos_keys(ob):
    n = len(ob.data.vertices)
    arr = np.empty(n * 3, dtype=np.float64)
    ob.data.vertices.foreach_get("co", arr)
    g = np.round(arr.reshape(-1, 3) / 1e-5).astype(np.int64) + (1 << 20)
    return (g[:, 0] << 42) | (g[:, 1] << 21) | g[:, 2]

# ---- 1. source cape world bbox in its own file ----
bpy.ops.wm.open_mainfile(filepath=BAKED)
src_cape = bpy.data.objects.get("CapeJones_Cape")
src_min, src_max = world_eval_bbox(src_cape)
print("SRC cape world bbox f40: min", src_min.round(3), "max", src_max.round(3))
src_keys = pos_keys(bpy.data.objects["CapeJones_Body"])
print("src body keys:", len(src_keys))

# ---- 2. open mech, compute removed set by in-order alignment (int64 keys) ----
bpy.ops.wm.open_mainfile(filepath=MECH)
import gc
gc.collect()
body = bpy.data.objects.get("CapeJones_Body")
mech_keys = pos_keys(body)
order = np.argsort(mech_keys, kind='stable')
sorted_keys = mech_keys[order]
uniq, starts, counts = np.unique(sorted_keys, return_index=True, return_counts=True)
table = {int(k): (int(s), int(c)) for k, s, c in zip(uniq, starts, counts)}
ptr = {}
kept = set()
last = -1
for k in src_keys:
    ent = table.get(int(k))
    if ent is None:
        continue
    s, c = ent
    p = ptr.get(int(k), 0)
    while p < c and int(order[s + p]) <= last:
        p += 1
    if p < c:
        idx = int(order[s + p])
        kept.add(idx)
        last = idx
        p += 1
    ptr[int(k)] = p
removed = set(range(len(mech_keys))) - kept
print(f"alignment: kept {len(kept)}, removed {len(removed)} of {len(mech_keys)}")
assert len(kept) > 600000 and 200000 < len(removed) < 350000, "alignment implausible — aborting"
del mech_keys, src_keys, order, sorted_keys, uniq, table, ptr
gc.collect()

# ---- 3. delete removed verts from body (edit mode op handles shape keys/groups) ----
bpy.context.view_layer.objects.active = body
bpy.ops.object.mode_set(mode='EDIT')
import bmesh
bm = bmesh.from_edit_mesh(body.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    v.select = v.index in removed
bmesh.update_edit_mesh(body.data)
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')
print("body verts after cape cut:", len(body.data.vertices))

# ---- 4. append baked cape ----
before = set(bpy.data.objects.keys())
with bpy.data.libraries.load(BAKED, link=False) as (data_from, data_to):
    data_to.objects = ["CapeJones_Cape"]
new_objs = [o for o in bpy.data.objects if o.name not in before]
print("appended:", [(o.name, o.type) for o in new_objs])
cape = [o for o in new_objs if o.type == 'MESH'][0]
if cape.name not in bpy.context.scene.collection.objects:
    bpy.context.scene.collection.objects.link(cape)
# re-point armature modifier at local rig, drop appended rig clone if any
rig = bpy.data.objects.get("CapeJones_Rig")
for m in cape.modifiers:
    if m.type == 'ARMATURE':
        print("cape armature target was:", m.object.name if m.object else None)
        m.object = rig
cape.name = "CapeJones_Cape"
for o in new_objs:
    if o is not cape and o.type == 'ARMATURE':
        nm = o.name
        bpy.data.objects.remove(o, do_unlink=True)
        print("removed appended rig clone:", nm)

# ---- 5. verify ----
for m in cape.modifiers:
    if m.type == 'CLOTH':
        print("cape cloth baked:", m.point_cache.is_baked, "frames:", m.point_cache.frame_start, m.point_cache.frame_end)
new_min, new_max = world_eval_bbox(cape)
print("FINAL cape world bbox f40: min", new_min.round(3), "max", new_max.round(3))
print("bbox delta vs source: min", np.abs(new_min - src_min).round(4), "max", np.abs(new_max - src_max).round(4))
print("rig action:", rig.animation_data.action.name if rig.animation_data and rig.animation_data.action else None)
rr = bpy.data.objects.get("recliner_rig")
print("recline:", rr["recline"] if rr else "NO RECLINER RIG")
print("body verts final:", len(body.data.vertices))

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
