"""verify_repair.py — confirm the seam-averaging repair on the POSED mesh.

For the averaging repair (no topology change), boundary-edge COUNT does not
drop. The correct metric is seam SEPARATION: coincident seam verts must stay
coincident after deformation. This script measures, for each seam vert, the
distance to its nearest neighbor in the posed mesh. If the max separation is
under the weld threshold, the seams are shut (invisible).

Also verifies CorrectiveSmooth is alive (non-zero output delta).

Headless:
    xvfb-run -a env -u PYTHONPATH <blender> -b <repaired.blend> \
        --python verify_repair.py -- <body_object> <seam_npy> <out_json>

Writes <out_json> with the verdict (repaired_ok bool).
"""
import bpy
import numpy as np
import json
import sys
from mathutils.kdtree import KDTree


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    body_name, seam_npy, out_json = argv[0], argv[1], argv[2]
    threshold = float(argv[3]) if len(argv) > 3 else 0.02

    body = bpy.data.objects.get(body_name)
    if body is None:
        raise SystemExit(f"object '{body_name}' not found")
    seam = np.load(seam_npy).astype(np.int32)

    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    bev = body.evaluated_get(dg)
    pm = bev.to_mesh()
    n = len(pm.vertices)
    pco = np.empty(n * 3, dtype=np.float32)
    pm.vertices.foreach_get("co", pco)
    pco = pco.reshape(-1, 3)

    # seam separation in the POSED mesh
    kd = KDTree(len(seam))
    for i, vi in enumerate(seam):
        kd.insert(pco[int(vi)], int(i))
    kd.balance()
    seps = []
    step = max(1, len(seam) // 20000)  # sample up to 20k for speed
    for i in range(0, len(seam), step):
        vi = int(seam[i])
        hits = kd.find_n(pco[vi], 2)
        if len(hits) > 1:
            seps.append(hits[1][2])
    seps = np.array(seps, dtype=np.float64)
    bev.to_mesh_clear()

    max_sep = float(seps.max()) if len(seps) else 0.0
    p99_sep = float(np.percentile(seps, 99)) if len(seps) else 0.0
    frac_open = float((seps > threshold).mean()) if len(seps) else 0.0

    # CorrectiveSmooth alive?
    cs = next((m for m in body.modifiers if m.type == 'CORRECTIVE_SMOOTH'), None)
    cs_working = None
    if cs is not None:
        def evalc():
            d = bpy.context.evaluated_depsgraph_get()
            p = body.evaluated_get(d).to_mesh()
            nn = len(p.vertices)
            cc = np.empty(nn * 3, dtype=np.float32)
            p.vertices.foreach_get("co", cc)
            body.evaluated_get(d).to_mesh_clear()
            return cc
        bpy.context.view_layer.update()
        on = evalc()
        cs.show_viewport = False
        cs.show_render = False
        bpy.context.view_layer.update()
        off = evalc()
        cs.show_viewport = True
        cs.show_render = True
        cs_working = bool(np.abs(on - off).max() > 1e-6)

    report = {
        "body": body_name,
        "modifiers": [(m.type, m.name) for m in body.modifiers],
        "seam_verts": int(len(seam)),
        "threshold": threshold,
        "posed_max_seam_separation": round(max_sep, 5),
        "posed_p99_seam_separation": round(p99_sep, 5),
        "posed_frac_seams_open": round(frac_open, 5),
        "corrective_smooth_working": cs_working,
        "repaired_ok": bool(max_sep <= threshold and (cs_working is not False)),
    }
    with open(out_json, "w") as f:
        json.dump(report, f, indent=1)
    print("VERIFY: " + json.dumps(report, indent=1), flush=True)


if __name__ == "__main__":
    main()
