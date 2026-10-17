"""Lane 3 FIX v6: chain-projection with DEAD-BONE PRIORITY.
Dead bones (0 verts) claim their verts first; non-dead chains skip claimed verts.
Prevents thumb stealing pinky's verts."""
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

# identify dead bones
dead_bones = set()
for ch in chains.values():
    for bn in ch:
        gid = vg_names.index(bn)
        cnt = 0
        for v in me.vertices:
            for g in v.groups:
                if g.group == gid and g.weight >= 0.5:
                    cnt += 1
                    break
            if cnt > 0:
                break
        if cnt == 0:
            dead_bones.add(bn)
print(f"dead bones: {sorted(dead_bones)}", flush=True)

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
P = co.reshape(n, 3)

finger_gids = {vg_names.index(bn) for ch in chains.values() for bn in ch}

def chain_points(bone_names):
    pts = [np.array(rig.pose.bones[bn].head) for bn in bone_names]
    pts.append(np.array(rig.pose.bones[bone_names[-1]].tail))
    return pts

def project_to_chain(p, pts):
    best_d, best_s = 1e9, 0
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
            best_d, best_s = d, s
    return best_s, best_d

R = 0.020
claimed = np.zeros(n, dtype=bool)

# order: chains with dead bones first
def chain_priority(item):
    (f, side), bones = item
    return (0 if any(b in dead_bones for b in bones) else 1, f, side)

total = 0
for (f, side), bone_names in sorted(chains.items(), key=chain_priority):
    pts = chain_points(bone_names)
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
    cand = np.nonzero((dmin <= R) & (~claimed))[0]
    n_a = 0
    for vi in cand:
        v = me.vertices[int(vi)]
        hand_w = max([g.weight for g in v.groups
                      if vg_names[g.group] in deform and vg_names[g.group].startswith("hand_")] + [0.0])
        fing_w = max([g.weight for g in v.groups
                      if g.group in finger_gids] + [0.0])
        if hand_w >= 0.5 and fing_w < 0.5:
            continue
        s, d = project_to_chain(P[vi], pts)
        target_bn = bone_names[min(s, len(bone_names) - 1)]
        target_gid = vg_names.index(target_bn)
        cur = next((g.group for g in v.groups
                    if vg_names[g.group] in deform and g.weight >= 0.5), None)
        if cur == target_gid:
            claimed[vi] = True
            continue
        for g in list(v.groups):
            if vg_names[g.group] in deform and g.group != target_gid:
                try: vg[g.group].remove([int(vi)])
                except RuntimeError: pass
        vg[target_gid].add([int(vi)], 1.0, 'REPLACE')
        claimed[vi] = True
        n_a += 1
    total += n_a
    print(f"chain {(f, side)}: {len(cand)} cand, assigned {n_a}", flush=True)

print(f"total assigned: {total} in {time.time()-t0:.0f}s", flush=True)
bpy.ops.wm.save_mainfile(filepath=BLEND)
print("SAVED", BLEND, flush=True)
