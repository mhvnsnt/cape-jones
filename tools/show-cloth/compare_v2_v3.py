#!/usr/bin/env python3
"""Compare evaluated proxy cape verts at frame 48 between v2 and v3 bakes.
If identical, bone parenting had no effect on the sim."""
import bpy, numpy as np

def cape_verts(path, frame):
    bpy.ops.wm.open_mainfile(filepath=path)
    sc = bpy.context.scene
    cape = bpy.data.objects["CapeJones_Cape"]
    print(path.split("/")[-1], "parent:", cape.parent.name if cape.parent else None,
          "bone:", cape.parent_bone, flush=True)
    sc.frame_set(frame)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(deps)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    mw = np.array(ev.matrix_world, dtype=np.float64)
    world = (np.concatenate([arr.reshape(-1, 3), np.ones((len(me.vertices), 1))], axis=1) @ mw.T)[:, :3]
    ev.to_mesh_clear()
    return world

v2 = cape_verts("/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_proxy_baked.blend", 48)
v3 = cape_verts("/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_v3_baked.blend", 48)
print("vert counts:", len(v2), len(v3))
n = min(len(v2), len(v3))
diff = np.abs(v2[:n] - v3[:n]).max(axis=1)
print(f"max vert delta v2->v3 at frame 48: {diff.max() * 1000:.2f}mm")
print(f"mean vert delta: {diff.mean() * 1000:.2f}mm")
print(f"verts moved >10mm: {(diff > 0.010).sum()} / {n}")
