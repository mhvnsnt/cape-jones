import bpy
import numpy as np
from collections import Counter

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend")
body = bpy.data.objects.get("CapeJones_Body")
mesh = body.data
print("materials:", [(i, m.name if m else None) for i, m in enumerate(mesh.materials)])
mi = np.empty(len(mesh.polygons), dtype=np.int32)
mesh.polygons.foreach_get("material_index", mi)
print("faces per material:", Counter(mi.tolist()))
# verts touched per material (verts whose ALL faces are that material)
nv = len(mesh.vertices)
face_verts = np.empty(len(mesh.polygons) * 3, dtype=np.int64)
mesh.polygons.foreach_get("vertices", face_verts)
face_verts = face_verts.reshape(-1, 3)
for m in sorted(set(mi.tolist())):
    sel = mi == m
    vs = np.unique(face_verts[sel])
    print(f"material {m}: faces {int(sel.sum())}, verts touched {len(vs)}")
print("total verts:", nv)
print("DIAG3 DONE")
