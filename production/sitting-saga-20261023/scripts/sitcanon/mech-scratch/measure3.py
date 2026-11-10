import bpy
import numpy as np
import gc
from mathutils import Vector
from mathutils.bvhtree import BVHTree

print("=== MEASURE3: BVH gaps + signed penetration ===", flush=True)
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

shin_gis = {body.vertex_groups[n].index for n in ('shin_L', 'shin_R')}
nv = len(body.data.vertices)
shin_mask = np.zeros(nv, dtype=bool)
for v in body.data.vertices:
    if v.groups:
        g = max(v.groups, key=lambda gg: gg.weight)
        if g.group in shin_gis:
            shin_mask[v.index] = True

def ev_world(obj, dg):
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    arr = arr.reshape(-1, 3)
    M = np.array(ev.matrix_world)
    out = (M[:3, :3] @ arr.T).T + M[:3, 3]
    ev.to_mesh_clear()
    return out, M

results = {}
for rec in (0.0, 0.25, 0.5, 0.75, 1.0):
    rrig['recline'] = rec
    eval_update(); eval_update()
    dg = bpy.context.evaluated_depsgraph_get()
    body_bvh = BVHTree.FromObject(body, dg)   # local frame
    pad_bvh = BVHTree.FromObject(pad, dg)     # local frame
    link_bvh = BVHTree.FromObject(link, dg)   # local frame
    bw, body_M = ev_world(body, dg)
    pw, pad_M = ev_world(pad, dg)
    lw, link_M = ev_world(link, dg)
    body_Minv = np.linalg.inv(body_M)
    pad_Minv = np.linalg.inv(pad_M)
    link_Minv = np.linalg.inv(link_M)

    def xform(pts, Minv):
        return (Minv[:3, :3] @ pts.T).T + Minv[:3, 3]

    # pad+link verts -> body surface, with signed penetration check
    q = xform(np.vstack([pw, lw]), body_Minv)
    d_a = 1e9
    min_signed = 1e9
    for p in q:
        loc, nrm, idx, dist = body_bvh.find_nearest(Vector(p))
        if dist < d_a:
            d_a = dist
        s = float(np.dot(np.array(p) - np.array(loc), np.array(nrm)))
        if s < min_signed:
            min_signed = s
    # shin verts -> pad / link surfaces
    sv = bw[shin_mask]
    region = sv[(sv[:, 2] < 0.36) & (sv[:, 0] > 2.55) & (sv[:, 0] < 3.15)][::3]
    rp = xform(region, pad_Minv)
    rl = xform(region, link_Minv)
    d_b = min(pad_bvh.find_nearest(Vector(p))[3] for p in rp)
    d_l = min(link_bvh.find_nearest(Vector(p))[3] for p in rl)
    evr = rig.evaluated_get(dg)
    fz = {s: (evr.matrix_world @ evr.pose.bones[f"foot_{s}"].head).z for s in ("L", "R")}
    gap = min(d_a, d_b, d_l)
    results[rec] = (gap, d_a, d_b, d_l, min_signed, fz)
    print(f"recline={rec}: gap={gap*1000:.1f}mm (pad->body {d_a*1000:.1f}, shin->pad {d_b*1000:.1f}, shin->link {d_l*1000:.1f}) "
          f"min_signed_pad={min_signed*1000:.1f}mm foot_z L={fz['L']:.3f} R={fz['R']:.3f}", flush=True)
    del body_bvh, pad_bvh, link_bvh, bw, pw, lw
    gc.collect()

z0 = results[0.0][5]
for rec in (0.25, 0.5, 0.75, 1.0):
    fz = results[rec][5]
    print(f"lift at {rec}: L {(fz['L']-z0['L'])*1000:.1f}mm R {(fz['R']-z0['R'])*1000:.1f}mm", flush=True)
rrig['recline'] = 0.0
eval_update()
print("=== MEASURE3 DONE ===", flush=True)
