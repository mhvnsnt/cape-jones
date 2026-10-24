import bpy
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

print("=== MEASURE2: frame-consistent BVH gaps ===", flush=True)
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

def ev_world_verts(obj, dg):
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    arr = arr.reshape(-1, 3)
    M = np.array(ev.matrix_world)
    out = (M[:3, :3] @ arr.T).T + M[:3, 3]
    ev.to_mesh_clear()
    return out

def ev_local_verts(obj, dg):
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    ev.to_mesh_clear()
    return arr.reshape(-1, 3)

# --- frame probe (once, at recline 0) ---
rrig['recline'] = 0.0
eval_update(); eval_update()
dg = bpy.context.evaluated_depsgraph_get()
body_bvh = BVHTree.FromObject(body, dg)
bw = ev_world_verts(body, dg)
bl = ev_local_verts(body, dg)
pw = ev_world_verts(pad, dg)
pl = ev_local_verts(pad, dg)
probe_w = Vector(bw[0])
probe_l = Vector(bl[0])
d_w = body_bvh.find_nearest(probe_w)[3]
d_l = body_bvh.find_nearest(probe_l)[3]
body_frame = 'world' if d_w < d_l else 'local'
print(f"body BVH frame: {body_frame} (d_world={d_w:.4f} d_local={d_l:.4f})", flush=True)
pad_bvh0 = BVHTree.FromObject(pad, dg)
dp_w = pad_bvh0.find_nearest(Vector(pw[0]))[3]
dp_l = pad_bvh0.find_nearest(Vector(pl[0]))[3]
pad_frame = 'world' if dp_w < dp_l else 'local'
print(f"pad BVH frame: {pad_frame} (d_world={dp_w:.4f} d_local={dp_l:.4f})", flush=True)

body_M = np.array(body.evaluated_get(dg).matrix_world)
body_Minv = np.linalg.inv(body_M)

def to_body_frame(pts_world):
    if body_frame == 'world':
        return pts_world
    return (body_Minv[:3, :3] @ pts_world.T).T + body_Minv[:3, 3]

results = {}
for rec in (0.0, 0.25, 0.5, 0.75, 1.0):
    rrig['recline'] = rec
    eval_update(); eval_update()
    dg = bpy.context.evaluated_depsgraph_get()
    body_bvh = BVHTree.FromObject(body, dg)
    pad_bvh = BVHTree.FromObject(pad, dg)
    link_bvh = BVHTree.FromObject(link, dg)
    bw = ev_world_verts(body, dg)
    pw = ev_world_verts(pad, dg)
    lw = ev_world_verts(link, dg)
    pad_M = np.array(pad.evaluated_get(dg).matrix_world)
    pad_Minv = np.linalg.inv(pad_M)
    link_Minv = np.linalg.inv(np.array(link.evaluated_get(dg).matrix_world))

    # (a) pad+link verts -> body surface (query in body frame)
    q = to_body_frame(np.vstack([pw, lw]))
    d_a = min(body_bvh.find_nearest(Vector(p))[3] for p in q)
    # (b) shin verts -> pad/link surface (query in pad/link local-or-world frame)
    sv = bw[shin_mask]
    region = sv[(sv[:, 2] < 0.36) & (sv[:, 0] > 2.55) & (sv[:, 0] < 3.15)][::3]
    if pad_frame == 'world':
        rp = region
        rl = region
    else:
        rp = (pad_Minv[:3, :3] @ region.T).T + pad_Minv[:3, 3]
        rl = (link_Minv[:3, :3] @ region.T).T + link_Minv[:3, 3]
    d_b = min(pad_bvh.find_nearest(Vector(p))[3] for p in rp)
    d_l = min(link_bvh.find_nearest(Vector(p))[3] for p in rl)
    # overlap: pad tree rebuilt in body frame from pad polygons
    evp = pad.evaluated_get(dg)
    mep = evp.to_mesh()
    polys = []
    mep.calc_loop_triangles()
    tris = np.empty(len(mep.loop_triangles) * 3, dtype=np.int64)
    mep.loop_triangles.foreach_get("vertices", tris)
    tris = tris.reshape(-1, 3)
    pw_body = to_body_frame(pw)
    pad_tree_bf = BVHTree.FromPolygons([tuple(v) for v in pw_body], [tuple(t) for t in tris])
    ov = len(pad_tree_bf.overlap(body_bvh))
    evp.to_mesh_clear()
    evr = rig.evaluated_get(dg)
    fz = {s: (evr.matrix_world @ evr.pose.bones[f"foot_{s}"].head).z for s in ("L", "R")}
    gap = min(d_a, d_b, d_l)
    results[rec] = (gap, d_a, d_b, d_l, ov, fz)
    print(f"recline={rec}: gap={gap*1000:.1f}mm (pad->body {d_a*1000:.1f}, shin->pad {d_b*1000:.1f}, shin->link {d_l*1000:.1f}) overlap={ov} foot_z L={fz['L']:.3f} R={fz['R']:.3f}", flush=True)

z0 = results[0.0][5]
for rec in (0.25, 0.5, 0.75, 1.0):
    fz = results[rec][5]
    print(f"lift at {rec}: L {(fz['L']-z0['L'])*1000:.1f}mm R {(fz['R']-z0['R'])*1000:.1f}mm", flush=True)
rrig['recline'] = 0.0
eval_update()
print("=== MEASURE2 DONE ===", flush=True)
