import bpy
import numpy as np

def cape_mask_counts(body):
    gi = body.vertex_groups.find("cape_mask")
    if gi < 0:
        return None
    c = {">0": 0, ">0.5": 0, ">=0.99": 0}
    for v in body.data.vertices:
        for g in v.groups:
            if g.group == gi:
                if g.weight > 0: c[">0"] += 1
                if g.weight > 0.5: c[">0.5"] += 1
                if g.weight >= 0.99: c[">=0.99"] += 1
    return c

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend")
body = bpy.data.objects.get("CapeJones_Body")
print("MECH objects with 'cape' in name:", [o.name for o in bpy.data.objects if 'cape' in o.name.lower()])
print("MECH body verts:", len(body.data.vertices))
print("MECH body cape_mask counts:", cape_mask_counts(body))
mech_co = np.empty(len(body.data.vertices) * 3)
body.data.vertices.foreach_get("co", mech_co)
mech_co = mech_co.reshape(-1, 3)
gi = body.vertex_groups.find("cape_mask")
mask = np.zeros(len(body.data.vertices), dtype=bool)
for v in body.data.vertices:
    for g in v.groups:
        if g.group == gi and g.weight > 0:
            mask[v.index] = True
kept = mech_co[~mask]
print("MECH body minus cape_mask verts:", len(kept))
np.save("/tmp/mech_kept.npy", kept)

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_capebaked.blend")
body2 = bpy.data.objects.get("CapeJones_Body")
cape = bpy.data.objects.get("CapeJones_Cape")
print("BAKED body verts:", len(body2.data.vertices))
print("BAKED body cape_mask counts:", cape_mask_counts(body2))
print("BAKED cape verts:", len(cape.data.vertices) if cape else None)
for m in cape.modifiers:
    print("  cape modifier:", m.type, "object:", getattr(m, 'object', None).name if getattr(m, 'object', None) else None,
          "baked:", m.point_cache.is_baked if m.type == 'CLOTH' else '-')
print("BAKED cape matrix_world:", [tuple(round(x, 3) for x in row) for row in cape.matrix_world])
print("BAKED cape vertex groups:", [g.name for g in cape.vertex_groups])
b2 = np.empty(len(body2.data.vertices) * 3)
body2.data.vertices.foreach_get("co", b2)
b2 = b2.reshape(-1, 3)
# set-equality check between mech-kept positions and baked body positions
def keyset(A):
    return set(map(tuple, np.round(A, 5)))
ks_kept = keyset(kept)
ks_b2 = keyset(b2)
print("position sets: mech-kept", len(ks_kept), " baked-body", len(ks_b2), " intersection", len(ks_kept & ks_b2))
print("DIAG DONE")
