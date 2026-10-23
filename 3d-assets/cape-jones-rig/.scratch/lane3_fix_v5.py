"""Lane 3 FIX v5: chain-aware redistribution. For each finger chain, collect
verts near the chain and assign each to the segment where its projection
onto the chain polyline falls. Ensures every segment gets its share.
Only reassigns verts currently on finger bones or unassigned (keeps hand-bone verts)."""
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

chains = {}
for side in ("L", "R"):
    for f in ("index", "middle", "ring", "pinky"):
        chains[(f, side)] = [f"finger_{f}_{i}_{side}" for i in (1, 2, 3)]
    chains[("thumb", side)] = [f"finger_thumb_{i}_{side}" for i in (1, 2)]

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
P = co.reshape(n, 3)

finger_gids = {vg_names.index(bn) for ch in chains.values() for bn in ch}

def chain_points(bone_names):
    pts = []
    for bn in bone_names:
        pb = rig.pose.bones[bn]
        pts.append(np.array(pb.head))
    pb = rig.pose.bones[bone_names[-1]]
    pts.append(np.array(pb.tail))
    return pts  # len = segments+1

def project_to_chain(p, pts):
    """Return (seg_idx, dist) for point p onto polyline pts."""
    best_d = 1e9
    best_s = 0
    for s in range(len(pts) - 1):
        a, b = pts[s], pts[s + 1]
        ab = b - a
        denom = float(ab @ ab)
        if denom < 1e-12:
            d = float(np.linalg.norm(p - a))
        else:
            t = np.clip(float((p - a) @ ab) / denom, 0, 1)
            d = float(np.linalg.norm(p - (a + t * ab)))
        if d < best_d:
            best_d = d
            best_s = s
    return best_s, best_d

R = 0.015
total_reassigned = 0
for (f, side), bone_names in chains.items():
    pts = chain_points(bone_names)
    # candidate verts: within R of the chain polyline
    # (compute via segment distances)
    dmin = np.full(n, 1e9)
    for s in range(len(pts) - 1):
        a, b = pts[s], pts[s + 1]
        ab = b - a
        denom = float(ab @ ab)
        if denom < 1e-12:
            d = np.linalg.norm(P - a, axis=1)
        else:
            t = np.clip(((P - a) @ ab) / denom, 0, 1)
            d = np.linalg.norm(P - (a + t[:, None] * ab), axis=1)
        dmin = np.minimum(dmin, d)
    cand = np.nonzero(dmin <= R)[0]
    n_assigned = 0
    for vi in cand:
        v = me.vertices[int(vi)]
        # only touch verts that are on finger bones or have no strong hand-bone weight
        # (don't steal from hand bone if it's dominant)
        hand_w = 0.0
        fing_w = 0.0
        for g in v.groups:
            gn = vg_names[g.group]
            if gn in deform:
                if g.group in finger_gids:
                    fing_w = max(fing_w, g.weight)
                elif gn.startswith("hand_"):
                    hand_w = max(hand_w, g.weight)
        if hand_w >= 0.5 and fing_w < 0.5:
            continue  # firmly palm, leave it
        s, d = project_to_chain(P[vi], pts)
        target_bn = bone_names[min(s, len(bone_names) - 1)]
        target_gid = vg_names.index(target_bn)
        # check if already correctly assigned
        cur = None
        for g in v.groups:
            if vg_names[g.group] in deform and g.weight >= 0.5:
                cur = g.group
                break
        if cur == target_gid:
            continue
        for g in list(v.groups):
            if vg_names[g.group] in deform and g.group != target_gid:
                try: vg[g.group].remove([int(vi)])
                except RuntimeError: pass
        vg[target_gid].add([int(vi)], 1.0, 'REPLACE')
        n_assigned += 1
    total_reassigned += n_assigned
    print(f"chain {(f, side)}: {len(cand)} near, reassigned {n_assigned}", flush=True)

print(f"total reassigned: {total_reassigned} in {time.time()-t0:.0f}s", flush=True)
bpy.ops.wm.save_mainfile(filepath=BLEND)
print("SAVED", BLEND, flush=True)
