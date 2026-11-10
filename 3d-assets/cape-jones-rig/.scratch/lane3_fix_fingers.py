"""Lane 3 FIX v3: rigid per-segment finger weight repaint, done in EVALUATED
(posed/bind) space.

This rig's armature rest pose is degenerate (bones at origin); the effective
bind pose is the SAVED POSE. The Armature modifier carries stored verts to
the posed fingers via the rest->pose delta. Therefore weight assignment must
use depsgraph-evaluated vert positions + posed bone segments (pose.bones
head/tail), writing weights back to the same vert indices.

- candidate verts (evaluated space): within 8mm of any posed finger segment,
  or carrying any finger-group weight >= 0.005
- each candidate -> 1.0 to nearest finger segment bone, all other deform
  groups removed (rigid convention per RIG-DOCS)
- stray finger weights (>8mm from any segment) stripped, vert renormalized
- candidates: prune deform <0.01, keep top 4, renormalize
Saves cape_jones_rigged_w5r_idle.blend in place (branch worktree).
"""
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

finger_bones = sorted([pb.name for pb in rig.pose.bones if pb.name.startswith("finger_")])
assert len(finger_bones) == 28, len(finger_bones)
# posed (bind) segments
segs = []
for bn in finger_bones:
    pb = rig.pose.bones[bn]
    segs.append((bn, np.array(pb.head, dtype=np.float64), np.array(pb.tail, dtype=np.float64)))

# EVALUATED vert positions (bind/posed space)
deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
assert len(ev.vertices) == n, "topology mismatch!"
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
P = co.reshape(n, 3)
print(f"evaluated verts: {n}, bbox z {P[:,2].min():.3f}..{P[:,2].max():.3f}", flush=True)

def seg_dist_batch(p, a, b):
    ab = b - a
    denom = float(ab @ ab)
    if denom < 1e-12:
        return np.linalg.norm(p - a, axis=1)
    t = np.clip(((p - a) @ ab) / denom, 0.0, 1.0)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1)

dmin = np.full(n, 1e9)
nearest = np.full(n, -1, dtype=np.int64)
for si, (bn, a, b) in enumerate(segs):
    d = seg_dist_batch(P, a, b)
    better = d < dmin
    dmin[better] = d[better]
    nearest[better] = si
n_within8 = int((dmin <= 0.008).sum())
print(f"distances done in {time.time()-t0:.0f}s; evaluated verts within 8mm of a finger: {n_within8}", flush=True)

finger_gids = {vg_names.index(bn) for bn in finger_bones}
has_finger_w = np.zeros(n, dtype=bool)
for v in me.vertices:
    for g in v.groups:
        if g.group in finger_gids and g.weight >= 0.005:
            has_finger_w[v.index] = True
            break
print("verts with finger w>=0.005:", int(has_finger_w.sum()), flush=True)

cand = (dmin <= 0.008) | has_finger_w
cand_idx = np.nonzero(cand)[0]
print("candidate verts:", len(cand_idx), flush=True)

gid_of = {bn: vg_names.index(bn) for bn in finger_bones}
n_rigid = 0
n_stray = 0
for vi in cand_idx:
    v = me.vertices[int(vi)]
    if dmin[vi] <= 0.008:
        target_gid = gid_of[finger_bones[int(nearest[vi])]]
        for g in list(v.groups):
            if vg_names[g.group] in deform and g.group != target_gid:
                try: vg[g.group].remove([int(vi)])
                except RuntimeError: pass
        vg[target_gid].add([int(vi)], 1.0, 'REPLACE')
        n_rigid += 1
    else:
        for g in list(v.groups):
            if g.group in finger_gids:
                try: vg[g.group].remove([int(vi)])
                except RuntimeError: pass
        n_stray += 1
print(f"rigid assigned: {n_rigid}, strays stripped: {n_stray}", flush=True)

n_renorm = 0
for vi in cand_idx:
    v = me.vertices[int(vi)]
    ws = [(g.weight, g.group) for g in v.groups
          if vg_names[g.group] in deform and g.weight >= 0.01]
    if not ws:
        continue
    ws.sort(reverse=True)
    keep = {g for _, g in ws[:4]}
    for g in list(v.groups):
        if vg_names[g.group] in deform and g.group not in keep:
            try: vg[g.group].remove([int(vi)])
            except RuntimeError: pass
    v = me.vertices[int(vi)]
    tot = sum(g.weight for g in v.groups if vg_names[g.group] in deform)
    if tot > 1e-9:
        for g in v.groups:
            if vg_names[g.group] in deform:
                vg[g.group].add([int(vi)], g.weight / tot, 'REPLACE')
    n_renorm += 1
print(f"renormalized: {n_renorm} in {time.time()-t0:.0f}s", flush=True)

bpy.ops.wm.save_mainfile(filepath=BLEND)
print("SAVED", BLEND, flush=True)
