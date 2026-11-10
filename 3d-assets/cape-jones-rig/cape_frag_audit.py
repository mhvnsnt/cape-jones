"""LANE 1 CAPE REBUILD — mesh-island audit of CapeJones_Cape.
Finds the 53 fragments: per-island vert count + world bbox + centroid.
Also dumps union bbox and modifier stack."""
import bpy
from mathutils import Vector
from collections import deque

ob = bpy.data.objects['CapeJones_Cape']
me = ob.data
print(f"Object: {ob.name}  verts={len(me.vertices)} faces={len(me.polygons)}")
print("Modifiers:")
for m in ob.modifiers:
    print(f"  {m.type}: {m.name}")
print(f"Parent: {ob.parent.name if ob.parent else None}  "
      f"parent_type={ob.parent_type}  parent_bone={ob.parent_bone if hasattr(ob,'parent_bone') else ''}")
print(f"location={tuple(round(v,4) for v in ob.location)} "
      f"rotation={tuple(round(v,4) for v in ob.rotation_euler)} scale={tuple(round(v,4) for v in ob.scale)}")
print(f"vertex groups: {[vg.name for vg in ob.vertex_groups]}")

# Build adjacency by edges -> connected components (islands)
n = len(me.vertices)
adj = [[] for _ in range(n)]
for e in me.edges:
    a, b = e.vertices
    adj[a].append(b)
    adj[b].append(a)
seen = [False] * n
islands = []
for i in range(n):
    if seen[i]:
        continue
    q = deque([i]); seen[i] = True; comp = []
    while q:
        v = q.popleft(); comp.append(v)
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True; q.append(w)
    islands.append(comp)

print(f"\nISLAND COUNT: {len(islands)}")
islands.sort(key=len, reverse=True)
allws = []
for idx, comp in enumerate(islands):
    ws = [ob.matrix_world @ me.vertices[v].co for v in comp]
    allws += ws
    xs = [c.x for c in ws]; ys = [c.y for c in ws]; zs = [c.z for c in ws]
    cx, cy, cz = sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)
    print(f"island {idx:2d}: verts={len(comp):6d} "
          f"x[{min(xs):.3f},{max(xs):.3f}] y[{min(ys):.3f},{max(ys):.3f}] z[{min(zs):.3f},{max(zs):.3f}] "
          f"centroid=({cx:.3f},{cy:.3f},{cz:.3f})")

ux = [c.x for c in allws]; uy = [c.y for c in allws]; uz = [c.z for c in allws]
print(f"\nUNION: x[{min(ux):.3f},{max(ux):.3f}] y[{min(uy):.3f},{max(uy):.3f}] z[{min(uz):.3f},{max(uz):.3f}]")

# sample: how many faces per island for the 3 largest
print("\nLargest-island face/edge stats:")
for idx, comp in enumerate(islands[:3]):
    vset = set(comp)
    f = sum(1 for p in me.polygons if all(v in vset for v in p.vertices))
    print(f"  island {idx}: {len(comp)} verts, {f} faces")
