"""Procedural weights directly on character (vectorized, chunked)."""
import bpy, json, os
import numpy as np
from mathutils import Vector

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_clean.blend'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
arm = bpy.data.objects['CapeJones_Rig']
for o in (char, arm):
    if o.name not in scn.collection.objects:
        scn.collection.objects.link(o)
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='OBJECT')

# deform bones
deform_bones = [b.name for b in arm.data.bones if b.use_deform]
print('bones:', len(deform_bones))
# bone head/tail world
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
bpy.context.view_layer.update()
segs_a = []
segs_b = []
for bn in deform_bones:
    pb = arm.pose.bones[bn]
    segs_a.append(Vector(pb.head))
    segs_b.append(Vector(pb.tail))
bpy.ops.object.mode_set(mode='OBJECT')
segs_a = np.array(segs_a)  # (B,3)
segs_b = np.array(segs_b)
n_bones = len(deform_bones)

# char verts world
n_verts = len(char.data.vertices)
print('verts:', n_verts)
verts = np.empty(n_verts*3, dtype=np.float32)
char.data.vertices.foreach_get('co', verts)
verts = verts.reshape(-1, 3)
mw = np.array(char.matrix_world, dtype=np.float32)
verts_w = (mw[:3,:3] @ verts.T).T + mw[:3,3]
print('verts loaded')

# locked bones get rigid weights
LOCKED = {'hand_L', 'hand_R', 'foot_L', 'foot_R', 'head', 'chest'}
locked_idx = set(i for i, n in enumerate(deform_bones) if n in LOCKED)

# process in chunks, compute top-4 weights
# store as dict bone_idx -> list of (vert_idx, weight)
from collections import defaultdict
vg_data = defaultdict(list)
chunk = 20000
ab = segs_b - segs_a  # (B,3)
ab_len2 = np.sum(ab*ab, axis=1) + 1e-12  # (B,)
for s in range(0, n_verts, chunk):
    e = min(s+chunk, n_verts)
    pts = verts_w[s:e]  # (C,3)
    C = e - s
    # dist to each segment: (C,B)
    # t = dot(p-a, ab) / |ab|^2
    ap = pts[:, None, :] - segs_a[None, :, :]  # (C,B,3) - memory heavy!
    # To save memory, loop over bones in inner loop but vectorize over verts
    # Actually (C=20k, B=72, 3) = 4.3M floats = 17MB, okay
    t = np.sum(ap * ab[None, :, :], axis=2) / ab_len2[None, :]  # (C,B)
    t = np.clip(t, 0, 1)
    closest = segs_a[None, :, :] + t[:, :, None] * ab[None, :, :]  # (C,B,3)
    dist = np.linalg.norm(pts[:, None, :] - closest, axis=2)  # (C,B)
    # weights
    w = 1.0 / (dist**2 + 1e-6)  # (C,B)
    # top 4 per vert
    top_idx = np.argsort(-w, axis=1)[:, :4]  # (C,4)
    top_w = np.take_along_axis(w, top_idx, axis=1)  # (C,4)
    # locked: if best is locked, use only it
    for ci in range(C):
        vi = s + ci
        bi = top_idx[ci, 0]
        if bi in locked_idx:
            vg_data[bi].append((vi, 1.0))
        else:
            ws = top_w[ci]
            ws = ws / (ws.sum() + 1e-12)
            for k in range(4):
                vg_data[top_idx[ci, k]].append((vi, float(ws[k])))
    if s % 100000 == 0:
        print(f'  chunk {s}/{n_verts}', flush=True)

print('creating vertex groups...')
for bi, bn in enumerate(deform_bones):
    if bi not in vg_data:
        continue
    vg = char.vertex_groups.new(name=bn)
    data = vg_data[bi]
    # add in batches
    for i in range(0, len(data), 5000):
        batch = data[i:i+5000]
        idxs = [d[0] for d in batch]
        ws = [d[1] for d in batch]
        # vg.add takes single weight, need loop (slow) OR use foreach?
        # Blender 4.0 doesn't have efficient batch add; do loop but it's okay
        for vi, w in zip(idxs, ws):
            if w > 1e-4:
                vg.add([vi], w, 'REPLACE')
    if bi % 20 == 0:
        print(f'  vg {bi}/{n_bones}', flush=True)

print('WEIGHTS DONE')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_direct.blend'))
print('SAVED')
