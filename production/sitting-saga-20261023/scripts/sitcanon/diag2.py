import bpy
import numpy as np
from collections import defaultdict, deque

def load_co(path, objname):
    bpy.ops.wm.open_mainfile(filepath=path)
    ob = bpy.data.objects.get(objname)
    arr = np.empty(len(ob.data.vertices) * 3)
    ob.data.vertices.foreach_get("co", arr)
    return [tuple(np.round(p, 5)) for p in arr.reshape(-1, 3)]

mech = load_co("/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend", "CapeJones_Body")
baked_body = load_co("/home/hatch/workspace/sitcanon-work/scene_capebaked.blend", "CapeJones_Body")
cape = load_co("/home/hatch/workspace/sitcanon-work/scene_capebaked.blend", "CapeJones_Cape")
print("counts: mech", len(mech), "baked_body", len(baked_body), "cape", len(cape))

# index queues for mech positions
queues = defaultdict(deque)
for i, p in enumerate(mech):
    queues[p].append(i)

matched = []
last = -1
in_order = 0
for p in baked_body:
    q = queues[p]
    # pop until an index > last (queues are in increasing order)
    while q and q[0] <= last:
        q.popleft()
    if q:
        idx = q.popleft()
        matched.append(idx)
        last = idx
        in_order += 1
    else:
        matched.append(-1)
print(f"baked body verts matched in-order into mech body: {in_order}/{len(baked_body)}")
matched_set = set(i for i in matched if i >= 0)
removed = [i for i in range(len(mech)) if i not in matched_set]
print("removed mech indices:", len(removed))

mech_set = set(mech)
cape_set = set(cape)
removed_set = set(mech[i] for i in removed)
print("cape unique positions:", len(cape_set), " of which in mech body set:", len(cape_set & mech_set),
      " in removed set:", len(cape_set & removed_set), " in kept set:", len(cape_set - removed_set))
print("removed unique positions:", len(removed_set), " of which in cape set:", len(removed_set & cape_set))
np.save("/tmp/removed_idx.npy", np.array(removed, dtype=np.int64))
print("DIAG2 DONE")
