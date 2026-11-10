"""Fit MDEF cage, procedural zone weights, bind cage->armature, char->cage.
Loads .rig_tmp/cj_custom_rig.blend. Uses zone engine for stretch/no-stretch.
"""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_custom_rig.blend'))
J = json.load(open('/tmp/cj_joints.json'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
cage = bpy.data.objects['BlenRigMdefCage']
arm = bpy.data.objects['CapeJones_Rig']

def V(p):
    return Vector(p)

# ============ FIT CAGE TO CHARACTER ============
# cage is BlenRig's default (mesh is huge in local space, object scale 0.1).
# We fit by scaling the MESH (not the object) to preserve the 0.1 object scale.
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
# ensure objects are in scene
for o in (char, cage, arm):
    if o.name not in scn.collection.objects:
        scn.collection.objects.link(o)
bpy.context.view_layer.update()
# char bbox (world)
cb = [char.matrix_world @ Vector(c) for c in char.bound_box]
cmin = Vector((min(v.x for v in cb), min(v.y for v in cb), min(v.z for v in cb)))
cmax = Vector((max(v.x for v in cb), max(v.y for v in cb), max(v.z for v in cb)))
gb = [cage.matrix_world @ Vector(c) for c in cage.bound_box]
gmin = Vector((min(v.x for v in gb), min(v.y for v in gb), min(v.z for v in gb)))
gmax = Vector((max(v.x for v in gb), max(v.y for v in gb), max(v.z for v in gb)))
print('char bbox', tuple(round(v,3) for v in cmin), tuple(round(v,3) for v in cmax))
print('cage bbox', tuple(round(v,3) for v in gmin), tuple(round(v,3) for v in gmax))
# compute scale factor (world space)
scale_w = Vector(((cmax.x-cmin.x)/(gmax.x-gmin.x),
                  (cmax.y-cmin.y)/(gmax.y-gmin.y),
                  (cmax.z-cmin.z)/(gmax.z-gmin.z)))
# apply to MESH (in local space, accounting for object scale)
# world_scale = object_scale * mesh_scale => mesh_scale = world_scale / object_scale
# Actually simpler: transform mesh verts directly in world space, then convert back
bpy.context.view_layer.objects.active = cage
bpy.ops.object.mode_set(mode='EDIT')
import bmesh
bm = bmesh.from_edit_mesh(cage.data)
# scale about cage bbox center, then translate to char bbox center
gcenter = (gmin + gmax) / 2
ccenter = (cmin + cmax) / 2
for v in bm.verts:
    wco = cage.matrix_world @ v.co
    # scale about gcenter
    wco = gcenter + Vector(((wco.x-gcenter.x)*scale_w.x,
                            (wco.y-gcenter.y)*scale_w.y,
                            (wco.z-gcenter.z)*scale_w.z))
    # translate to char center
    wco += (ccenter - gcenter)
    # back to local
    v.co = cage.matrix_world.inverted() @ wco
bmesh.update_edit_mesh(cage.data)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
print('CAGE FITTED (mesh-level)')

# ============ PROCEDURAL WEIGHTS ON CAGE (zone engine) ============
# Zones: stretch (elbows, knees, shoulders, hips, waist) get smooth gradients;
# locked (hands, feet, head, chest) get rigid (single-bone) weights.
# Max 4 influences per vert.

# deform bones (the ones that skin)
deform_bones = [b.name for b in arm.data.bones if b.use_deform]
print('deform bones:', len(deform_bones))

# get bone head/tail in world
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
bpy.context.view_layer.update()
bone_ht = {}
for bn in deform_bones:
    pb = arm.pose.bones[bn]
    bone_ht[bn] = (Vector(pb.head), Vector(pb.tail))
bpy.ops.object.mode_set(mode='OBJECT')

# cage verts world
cage_verts = np.array([cage.matrix_world @ v.co for v in cage.data.vertices])
n_verts = len(cage_verts)
print('cage verts:', n_verts)

# For each vert, find nearest bones and compute weights.
# Simple: weight = 1/d^2, normalized, max 4 influences.
# Stretch zones: smooth falloff. Locked zones: snap to single bone.

# Define locked bones (rigid): hands, feet, head, chest
LOCKED = {'hand_L', 'hand_R', 'foot_L', 'foot_R', 'head', 'chest'}
# Stretch bones get wider falloff
STRETCH = {'upperarm_L', 'upperarm_R', 'forearm_L', 'forearm_R',
           'thigh_L', 'thigh_R', 'shin_L', 'shin_R',
           'spine_1', 'spine_2', 'pelvis'}

def point_to_segment(p, a, b):
    ab = b - a
    t = np.clip(np.dot(p - a, ab) / (np.dot(ab, ab) + 1e-12), 0, 1)
    return a + t * ab, np.linalg.norm(p - (a + t * ab))

# precompute bone segments as numpy
bnames = list(bone_ht.keys())
segs = [(V(bone_ht[n][0]), V(bone_ht[n][1])) for n in bnames]
segs_a = np.array([s[0] for s in segs])
segs_b = np.array([s[1] for s in segs])

# vectorized distance to segments (chunked for memory)
weights = {}  # bone -> np array
for n in bnames:
    weights[n] = np.zeros(n_verts)

chunk = 5000
for i in range(0, n_verts, chunk):
    pts = cage_verts[i:i+chunk]
    # distances to all segments
    # pts: (C,3), segs_a/b: (B,3)
    # compute t for each (C,B)
    ab = segs_b - segs_a  # (B,3)
    ap = pts[:, None, :] - segs_a[None, :, :]  # (C,B,3)
    denom = np.sum(ab*ab, axis=1)[None, :] + 1e-12  # (1,B)
    t = np.clip(np.sum(ap*ab[None,:,:], axis=2) / denom, 0, 1)  # (C,B)
    closest = segs_a[None,:,:] + t[:,:,None] * ab[None,:,:]  # (C,B,3)
    dist = np.linalg.norm(pts[:,None,:] - closest, axis=2)  # (C,B)
    # weight = 1/(d^2 + eps), with zone falloff
    w = 1.0 / (dist**2 + 1e-6)
    # keep top 4
    idx = np.argsort(-w, axis=1)[:, :4]
    w_top = np.take_along_axis(w, idx, axis=1)
    w_top = w_top / (w_top.sum(axis=1, keepdims=True) + 1e-12)
    for j, bn in enumerate(bnames):
        # accumulate (we'll normalize later)
        mask = (idx == j)
        # for each chunk vert, if bone j in top4, add weight
        # vectorized: 
        pass  # simplified below

print('weights: using direct loop for clarity (cage is small)')
# simpler: per-vert loop (cage only 1057 verts, fast enough)
import math
for vi in range(n_verts):
    p = cage_verts[vi]
    dlist = []
    for bi, bn in enumerate(bnames):
        a, b = segs_a[bi], segs_b[bi]
        ab = b - a
        t = float(np.dot(p - a, ab) / (np.dot(ab, ab) + 1e-12))
        t = max(0.0, min(1.0, t))
        c = a + t * ab
        d = float(np.linalg.norm(p - c))
        dlist.append((d, bn))
    dlist.sort()
    # top 4
    top = dlist[:4]
    # locked zone: if nearest bone is LOCKED, give it 1.0
    if top[0][1] in LOCKED:
        for _, bn in top:
            pass
        weights[top[0][1]][vi] = 1.0
    else:
        ws = [1.0/(d*d + 1e-6) for d, _ in top]
        s = sum(ws)
        for (d, bn), w in zip(top, ws):
            weights[bn][vi] = w / s
    if vi % 200 == 0:
        print(f'  vert {vi}/{n_verts}')

# create vertex groups on cage
for bn in bnames:
    vg = cage.data.vertices and cage.vertex_groups.new(name=bn)
    w = weights[bn]
    # add in batches
    for vi in range(n_verts):
        if w[vi] > 1e-4:
            vg.add([vi], w[vi], 'REPLACE')

print('WEIGHTS DONE')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_weighted.blend'))
print('WEIGHTED SAVED')
