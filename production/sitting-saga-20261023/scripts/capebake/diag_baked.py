"""Diagnose baked cape: per-frame out-of-bounds census + culprit components."""
import bpy
import numpy as np
from collections import Counter

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/capebake-work/scene_capebaked.blend")
sc = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
cloth = [m for m in cape.modifiers if m.type == 'CLOTH'][0]
print("is_baked:", cloth.point_cache.is_baked, "cape verts:", len(cape.data.vertices))

cape_idx = np.load("/home/hatch/workspace/capebake-work/cape_verts.npz")["cape_idx"]
comp_id = np.load("/home/hatch/workspace/capebake-work/comp_id.npz")["comp_id"]
HAVE_MAP = len(cape_idx) == len(cape.data.vertices)
print("comp mapping available:", HAVE_MAP)
CENTER = np.array([2.9, 2.05, 0.45])

def stats(f):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    ev.to_mesh_clear()
    return arr.reshape(-1, 3)

first_bad = None
for f in range(1, 82):
    P = stats(f)
    out = (P[:, 2] < -0.02) | (np.linalg.norm(P - CENTER, axis=1) > 1.6)
    n_out = int(out.sum())
    if f % 10 == 1 or (n_out > 0 and first_bad is None) or f in (40, 81):
        print(f"frame {f}: out={n_out} maxdist={np.linalg.norm(P - CENTER, axis=1).max():.2f} zmin={P[:,2].min():.3f}", flush=True)
    if n_out > 0 and first_bad is None:
        first_bad = f
        if HAVE_MAP:
            idx = np.nonzero(out)[0]
            comps = Counter(comp_id[cape_idx[idx]].tolist())
            print(f"  FIRST BAD frame {f}: {n_out} verts, components: {comps.most_common(8)}", flush=True)
        print(f"  bad vert world sample: {P[idx[:5]].round(3).tolist()}", flush=True)

P = stats(81)
out = (P[:, 2] < -0.02) | (np.linalg.norm(P - CENTER, axis=1) > 1.6)
print(f"frame 81 FINAL: out={int(out.sum())}")
print("DIAG DONE")
