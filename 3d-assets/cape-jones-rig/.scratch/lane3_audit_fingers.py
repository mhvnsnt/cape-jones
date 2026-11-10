"""Lane 3: audit finger bones + weights in cape_jones_rigged_w5r_idle.blend."""
import bpy, json, math

D = bpy.data

print("== ARMATURES ==")
for a in D.armatures:
    print("ARMATURE:", a.name, "bones:", len(a.bones))

print("== OBJECTS WITH ARMATURE MODIFIER ==")
for o in D.objects:
    for m in o.modifiers:
        if m.type == 'ARMATURE':
            print("DEFORM-MESH:", o.name, "via", m.object.name if m.object else "None",
                  "vert:", len(o.data.vertices))

rig = D.objects.get("CapeJones_Rig")
if not rig:
    rig = [o for o in D.objects if o.type == 'ARMATURE'][0]
print("RIG USED:", rig.name)

# FK control bones for fingers
fingers = sorted([b.name for b in rig.pose.bones if b.name.startswith("finger_")])
print("FINGER POSE BONES:", len(fingers))
for f in fingers:
    print("  ", f)

# Deform bones (actually used by armature modifier = bones with same name)
# Character mesh: find deformed object
mesh = None
for o in D.objects:
    for m in o.modifiers:
        if m.type == 'ARMATURE' and m.object == rig:
            mesh = o; break
print("MESH:", mesh.name if mesh else None)

if mesh:
    vg_names = [vg.name for vg in mesh.vertex_groups]
    finger_groups = [g for g in vg_names if g.startswith("finger_")]
    print("FINGER VERTEX GROUPS:", len(finger_groups), finger_groups)

    # stats: influences per vert, weight sums
    n = len(mesh.data.vertices)
    counts = []
    sums = []
    over4 = 0
    low_sum = 0
    finger_verts = {g: 0 for g in finger_groups}
    for v in mesh.data.vertices:
        c = len(v.groups)
        counts.append(c)
        if c > 4:
            over4 += 1
        s = sum(g.weight for g in v.groups)
        sums.append(s)
        if s < 0.999:
            low_sum += 1
        for g in v.groups:
            gn = mesh.vertex_groups[g.group].name
            if gn in finger_verts:
                finger_verts[gn] += 1
    import statistics
    print("VERTS:", n)
    print("MAX GROUPS/VERT:", max(counts), " MEAM:", round(statistics.mean(counts),2))
    print("VERTS WITH >4 GROUPS:", over4)
    print("VERTS WITH WEIGHT SUM < 0.999:", low_sum)
    print("MIN SUM:", round(min(sums),4), "MAX SUM:", round(max(sums),4))
    print("VERTS PER FINGER GROUP:")
    for g, c in finger_verts.items():
        print("   ", g, c)
    # histogram of group counts
    from collections import Counter
    print("GROUP-COUNT HISTOGRAM:", dict(Counter(counts)))

    # finger bone vs vertex group mismatch check
    deform_bones = [b.name for b in rig.data.bones if b.use_deform]
    finger_deform = [b for b in deform_bones if b.startswith("finger_")]
    print("DEFORM FINGER BONES:", len(finger_deform))
    missing_groups = [b for b in finger_deform if b not in vg_names]
    unused_groups = [g for g in finger_groups if g not in deform_bones]
    print("DEFORM BONES MISSING VERTEX GROUP:", missing_groups)
    print("FINGER GROUPS WITHOUT DEFORM BONE:", unused_groups)
