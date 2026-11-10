import bpy
import numpy as np

print("=== MEASURE4: numpy vertex distances + bone clearance ===", flush=True)
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
    arr = np.empty(len(me.vertices) * 3, dtype=np.float32)
    me.vertices.foreach_get("co", arr)
    arr = arr.reshape(-1, 3)
    M = np.array(ev.matrix_world, dtype=np.float64)
    out = (M[:3, :3] @ arr.T).T + M[:3, 3]
    ev.to_mesh_clear()
    return out.astype(np.float32)

def min_dist(A, B):
    # min over rows of A of distance to set B (B small)
    best = 1e9
    for a in A:
        d = np.linalg.norm(B - a, axis=1).min()
        if d < best:
            best = d
    return float(best)

def seg_point_dist(P, A, B):
    AB = B - A
    L2 = float(AB @ AB)
    t = np.clip(((P - A) @ AB) / L2, 0.0, 1.0)
    proj = A + t[:, None] * AB[None, :]
    return np.linalg.norm(P - proj, axis=1)

results = {}
for rec in (0.0, 0.25, 0.5, 0.75, 1.0):
    rrig['recline'] = rec
    eval_update(); eval_update()
    dg = bpy.context.evaluated_depsgraph_get()
    bw = ev_world(body, dg)
    pw = ev_world(pad, dg)
    lw = ev_world(link, dg)
    padset = np.vstack([pw, lw])
    d_pad_body = min_dist(padset, bw)
    sv = bw[shin_mask]
    region = sv[(sv[:, 2] < 0.36) & (sv[:, 0] > 2.55) & (sv[:, 0] < 3.15)]
    d_shin_pad = min_dist(region[::2], padset)
    # bone clearance: pad verts to shin bone segments (world), minus shin radius 0.032
    evr = rig.evaluated_get(dg)
    clear = 1e9
    for s in ("L", "R"):
        knee = np.array(evr.matrix_world @ evr.pose.bones[f"shin_{s}"].head)
        ankle = np.array(evr.matrix_world @ evr.pose.bones[f"foot_{s}"].head)
        dseg = seg_point_dist(padset, knee, ankle).min()
        clear = min(clear, float(dseg) - 0.032)
    fz = {s: float((evr.matrix_world @ evr.pose.bones[f"foot_{s}"].head).z) for s in ("L", "R")}
    gap = min(d_pad_body, d_shin_pad)
    results[rec] = (gap, d_pad_body, d_shin_pad, clear, fz)
    print(f"recline={rec}: gap={gap*1000:.1f}mm (pad->body {d_pad_body*1000:.1f}, shin->pad {d_shin_pad*1000:.1f}) "
          f"bone_clearance={clear*1000:.1f}mm foot_z L={fz['L']:.3f} R={fz['R']:.3f}", flush=True)

z0 = results[0.0][4]
for rec in (0.25, 0.5, 0.75, 1.0):
    fz = results[rec][4]
    print(f"lift at {rec}: L {(fz['L']-z0['L'])*1000:.1f}mm R {(fz['R']-z0['R'])*1000:.1f}mm", flush=True)
rrig['recline'] = 0.0
eval_update()
print("=== MEASURE4 DONE ===", flush=True)
