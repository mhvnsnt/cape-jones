"""Lane 3 FIX v4: rigid finger repaint with 20mm capture radius + hand-bone
comparison (so palm stays with hand bone, fingers go to finger bones).

- candidate verts (evaluated space): within 20mm of any posed finger segment,
  or carrying any finger-group weight >= 0.005
- each candidate: d_finger (nearest finger seg) vs d_hand (hand bone seg).
  if d_finger < d_hand -> rigid 1.0 to nearest finger bone, strip others.
  else -> strip finger groups only, keep hand weights.
- stray finger weights (>20mm) stripped, vert renormalized.
- candidates: prune deform <0.01, keep top 4, renormalize.
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
assert len(finger_bones) == 28
segs = []
for bn in finger_bones:
    pb = rig.pose.bones[bn]
    segs.append((bn, np.array(pb.head, dtype=np.float64), np.array(pb.tail, dtype=np.float64)))
hand_segs = {}
for side in ("L", "R"):
    pb = rig.pose.bones[f"hand_{side}"]
    hand_segs[side] = (np.array(pb.head, dtype=np.float64), np.array(pb.tail, dtype=np.float64))

deps = bpy.context.evaluated_depsgraph_get()
ev = deps.objects.get(mesh.name).data
assert len(ev.vertices) == n
co = np.empty(n * 3, dtype=np.float64)
ev.vertices.foreach_get("co", co)
P = co.reshape(n, 3)

def seg_dist_batch(p, a, b):
    ab = b - a
    denom = float(ab @ ab)
    if denom < 1e-12:
        return np.linalg.norm(p - a, axis=1)
    t = np.clip(((p - a) @ ab) / denom, 0.0, 1.0)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1)

R = 0.020
dmin_f = np.full(n, 1e9)
nearest = np.full(n, -1, dtype=np.int64)
for si, (bn, a, b) in enumerate(segs):
    d = seg_dist_batch(P, a, b)
    better = d < dmin_f
    dmin_f[better] = d[better]
    nearest[better] = si
# hand bone distance per side (use nearest of the two)
dmin_h = np.full(n, 1e9)
for side in ("L", "R"):
    a, b = hand_segs[side]
    d = seg_dist_batch(P, a, b)
    dmin_h = np.minimum(dmin_h, d)
print(f"dist done {time.time()-t0:.0f}s; within 20mm of finger: {(dmin_f<=R).sum()}", flush=True)

finger_gids = {vg_names.index(bn) for bn in finger_bones}
has_finger_w = np.zeros(n, dtype=bool)
for v in me.vertices:
    for g in v.groups:
        if g.group in finger_gids and g.weight >= 0.005:
            has_finger_w[v.index] = True
            break

cand = (dmin_f <= R) | has_finger_w
cand_idx = np.nonzero(cand)[0]
print("candidates:", len(cand_idx), flush=True)

gid_of = {bn: vg_names.index(bn) for bn in finger_bones}
n_rigid = n_hand = n_stray = 0
for vi in cand_idx:
    v = me.vertices[int(vi)]
    if dmin_f[vi] <= R and dmin_f[vi] < dmin_h[vi]:
        target_gid = gid_of[finger_bones[int(nearest[vi])]]
        for g in list(v.groups):
            if vg_names[g.group] in deform and g.group != target_gid:
                try: vg[g.group].remove([int(vi)])
                except RuntimeError: pass
        vg[target_gid].add([int(vi)], 1.0, 'REPLACE')
        n_rigid += 1
    else:
        # palm/stray: strip finger groups, keep the rest
        for g in list(v.groups):
            if g.group in finger_gids:
                try: vg[g.group].remove([int(vi)])
                except RuntimeError: pass
        n_stray += 1
print(f"rigid finger: {n_rigid}, finger-stripped: {n_stray}", flush=True)

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
print(f"cleanup done in {time.time()-t0:.0f}s", flush=True)

bpy.ops.wm.save_mainfile(filepath=BLEND)
print("SAVED", BLEND, flush=True)
