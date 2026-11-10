"""Lane 3 audit 7: deform vs non-deform groups. Is the junk non-deform?"""
import bpy, sys
import numpy as np
from collections import Counter

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
vg_names = [vg.name for vg in mesh.vertex_groups]
deform = set(b.name for b in rig.data.bones if b.use_deform)
print("total vertex groups:", len(vg_names))
print("deform bones:", len(deform))
nondef = [g for g in vg_names if g not in deform]
print("NON-DEFORM GROUPS:", len(nondef))
print("sample non-deform:", nondef[:20])

# stats over DEFORM groups only
hist = Counter(); maxsum = 0.0; minsum = 1e9
for v in me.vertices:
    s = 0.0; c = 0
    for g in v.groups:
        if vg_names[g.group] in deform and g.weight >= 0.01:
            c += 1; s += g.weight
    hist[c] += 1
    maxsum = max(maxsum, s); minsum = min(minsum, s)
print("DEFORM-ONLY THR=0.01 hist:", dict(sorted(hist.items())), "maxsum:", round(maxsum,3), "minsum:", round(minsum,4))
over4 = sum(k*c for k, c in hist.items() if k > 4)
print("deform verts >4 groups @0.01:", over4)

# raw deform-only (any weight)
hist0 = Counter(); maxsum0 = 0.0
for v in me.vertices:
    s = 0.0; c = 0
    for g in v.groups:
        if vg_names[g.group] in deform:
            c += 1; s += g.weight
    hist0[c] += 1
    maxsum0 = max(maxsum0, s)
print("DEFORM-ONLY RAW hist:", dict(sorted(hist0.items())), "maxsum:", round(maxsum0,3))
