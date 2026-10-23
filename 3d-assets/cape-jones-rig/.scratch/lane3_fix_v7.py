"""Lane 3 FIX v7: thumb-priority assignment. Thumb chains get first pick
of verts within 12mm, assigned to nearest thumb segment."""
import bpy, time
import numpy as np

t0 = time.time()
BLEND = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend"
bpy.ops.wm.open_mainfile(filepath=BLEND)
bpy.context.view_layer.update()

rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)
vg = mesh.vertex_groups
vg_names = [g.name for g in vg]
deform = set(b.name for b in rig.data.bones if b.use_deform)

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
P = co.reshape(n, 3)

def seg_dist(p, a, b):
    ab = b - a
    t = np.clip(((p - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1)

R = 0.012
for side in ("L", "R"):
    # thumb chain segments
    segs = []
    for bn in (f"finger_thumb_1_{side}", f"finger_thumb_2_{side}"):
        pb = rig.pose.bones[bn]
        segs.append((bn, np.array(pb.head), np.array(pb.tail)))
    # verts within R of either segment
    dmin = np.full(n, 1e9)
    nearest = np.full(n, -1)
    for si, (bn, a, b) in enumerate(segs):
        d = seg_dist(P, a, b)
        m = d < dmin
        dmin[m] = d[m]
        nearest[m] = si
    cand = np.nonzero(dmin <= R)[0]
    print(f"thumb {side}: {len(cand)} verts within 12mm", flush=True)
    n_a = 0
    for vi in cand:
        v = me.vertices[int(vi)]
        # skip if firmly on hand bone (>=0.5) and not on finger
        hw = max([g.weight for g in v.groups if vg_names[g.group] in deform and vg_names[g.group].startswith("hand_")] + [0.0])
        if hw >= 0.5:
            # check if already on a finger bone
            fw = max([g.weight for g in v.groups if vg_names[g.group].startswith("finger_")] + [0.0])
            if fw < 0.5:
                continue
        bn = segs[int(nearest[vi])][0]
        gid = vg_names.index(bn)
        for g in list(v.groups):
            if vg_names[g.group] in deform and g.group != gid:
                try: vg[g.group].remove([int(vi)])
                except RuntimeError: pass
        vg[gid].add([int(vi)], 1.0, 'REPLACE')
        n_a += 1
    print(f"thumb {side}: assigned {n_a}", flush=True)

print(f"done in {time.time()-t0:.0f}s", flush=True)
bpy.ops.wm.save_mainfile(filepath=BLEND)
print("SAVED", BLEND, flush=True)
