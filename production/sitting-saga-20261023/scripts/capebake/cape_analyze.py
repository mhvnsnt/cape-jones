import bpy
from collections import Counter, defaultdict

body = bpy.data.objects["CapeJones_Body"]
mesh = body.data
gi = body.vertex_groups["cape_mask"].index

buckets = Counter()
dom = Counter()
cape_verts = []
for v in mesh.vertices:
    w = 0.0
    for g in v.groups:
        if g.group == gi:
            w = g.weight
    if w == 0.0:
        buckets["zero"] += 1
    elif w < 0.5:
        buckets["0-0.5"] += 1
    elif w < 1.0:
        buckets["0.5-1"] += 1
    else:
        buckets["one"] += 1
    if w > 0.5:
        cape_verts.append(v.index)
        best, bw = None, -1
        for g in v.groups:
            if g.group != gi and g.weight > bw:
                bw, best = g.weight, body.vertex_groups[g.group].name
        dom[best] += 1

print("cape_mask buckets:", dict(buckets))
print("cape verts (w>0.5):", len(cape_verts))
print("their dominant bone groups:", dom.most_common(12))

# connected components among cape verts
cset = set(cape_verts)
adj = defaultdict(list)
for e in mesh.edges:
    a, b = e.vertices
    if a in cset and b in cset:
        adj[a].append(b)
        adj[b].append(a)
seen = set()
comps = []
for s in cape_verts:
    if s in seen:
        continue
    stack = [s]
    seen.add(s)
    comp = []
    while stack:
        x = stack.pop()
        comp.append(x)
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    comps.append(comp)
comps.sort(key=len, reverse=True)
print(f"components among cape verts: {len(comps)}")
for c in comps[:8]:
    xs = [mesh.vertices[i].co for i in c]
    import numpy as np
    P = np.array([[p.x, p.y, p.z] for p in xs])
    print(f"  comp size={len(c)} bbox min={P.min(axis=0).round(3)} max={P.max(axis=0).round(3)}")

# body world transform + a sample of cape vert positions in world space (frame 1 rest = object space here since armature not evaluated on raw co)
print("body matrix_world:", [round(x, 3) for row in body.matrix_world for x in row])
print("body location:", tuple(round(x, 3) for x in body.location), "scale:", tuple(round(x, 3) for x in body.scale))
# check shape keys mention
print("body shape keys:", [kb.name for kb in mesh.shape_keys.key_blocks] if mesh.shape_keys else None)
# material node check for cape_mask usage
mat = mesh.materials[0]
if mat and mat.use_nodes:
    for nd in mat.node_tree.nodes:
        print("  mat node:", nd.type, getattr(nd, 'attribute_name', '') if nd.type == 'ATTRIBUTE' else '')
print("DONE")
