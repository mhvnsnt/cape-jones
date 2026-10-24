import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

print("=== MEASURE: gaps / overlap / lift ===", flush=True)
OUT_TXT = []
rig = bpy.data.objects.get("CapeJones_Rig")
rrig = bpy.data.objects.get("recliner_rig")
scene = bpy.context.scene
body = bpy.data.objects.get("CapeJones_Body")
pad = bpy.data.objects['recliner_footrest_pad']
link = bpy.data.objects['recliner_footrest_link']
scene.frame_set(40)

def eval_update():
    rrig.update_tag(refresh={'DATA'})
    rig.update_tag(refresh={'DATA'})
    bpy.context.view_layer.update()

# shin-dominant vert mask from base mesh groups
shin_gis = {body.vertex_groups[n].index for n in ('shin_L', 'shin_R')}
foot_gis = {body.vertex_groups[n].index for n in ('foot_L', 'foot_R', 'toe_L', 'toe_R')}
nv = len(body.data.vertices)
shin_mask = np.zeros(nv, dtype=bool)
for v in body.data.vertices:
    if v.groups:
        g = max(v.groups, key=lambda gg: gg.weight)
        if g.group in shin_gis:
            shin_mask[v.index] = True
print(f"shin-dominant verts: {int(shin_mask.sum())}", flush=True)

def world_verts(obj, dg):
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    arr = arr.reshape(-1, 3)
    M = np.array(ev.matrix_world)
    out = (M[:3, :3] @ arr.T).T + M[:3, 3]
    ev.to_mesh_clear()
    return out

results = {}
for rec in (0.0, 0.25, 0.5, 0.75, 1.0):
    rrig['recline'] = rec
    eval_update()
    eval_update()  # settle multi-level driver/constraint chains
    dg = bpy.context.evaluated_depsgraph_get()
    body_bvh = BVHTree.FromObject(body, dg)
    pad_bvh = BVHTree.FromObject(pad, dg)
    link_bvh = BVHTree.FromObject(link, dg)
    bw = world_verts(body, dg)
    pw = world_verts(pad, dg)
    # (a) pad verts -> body surface
    d_a = min(body_bvh.find_nearest(p)[3] for p in pw)
    # (b) shin verts (region-filtered) -> pad surface
    sv = bw[shin_mask]
    region = sv[(sv[:, 2] < 0.36) & (sv[:, 0] > 2.55) & (sv[:, 0] < 3.15)]
    d_b = min(pad_bvh.find_nearest(p)[3] for p in region[::3])
    d_link = min(link_bvh.find_nearest(p)[3] for p in region[::3])
    # overlap (interpenetration) pad/link vs body
    ov_pad = len(pad_bvh.overlap(body_bvh))
    ov_link = len(link_bvh.overlap(body_bvh))
    # foot lift: evaluated foot bone head z + lowest foot-region vert z
    evr = rig.evaluated_get(dg)
    fz = {s: (evr.matrix_world @ evr.pose.bones[f"foot_{s}"].head).z for s in ("L", "R")}
    gap = min(d_a, d_b)
    results[rec] = (gap, d_a, d_b, d_link, ov_pad, ov_link, fz)
    print(f"recline={rec}: pad-shin gap={gap*1000:.1f}mm (pad->body {d_a*1000:.1f}, shin->pad {d_b*1000:.1f}, shin->link {d_link*1000:.1f}) "
          f"overlap pad/body={ov_pad} link/body={ov_link} foot_z L={fz['L']:.3f} R={fz['R']:.3f}", flush=True)

z0 = results[0.0][6]
for rec in (0.25, 0.5, 0.75, 1.0):
    fz = results[rec][6]
    print(f"lift at {rec}: L {(fz['L']-z0['L'])*1000:.1f}mm R {(fz['R']-z0['R'])*1000:.1f}mm", flush=True)
rrig['recline'] = 0.0
eval_update()
print("=== MEASURE DONE ===", flush=True)
