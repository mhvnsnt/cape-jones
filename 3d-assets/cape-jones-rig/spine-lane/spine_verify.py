"""SPINE LANE — mathematical verification of the rebuilt spine rig.
Run: blender -b cape_jones_rigged_w5r.blend --python spine_verify.py
Prints PASS/FAIL metrics; exits 0 only if all pass."""
import bpy, sys
import numpy as np
from mathutils import Vector

RIG = "CapeJones_Rig"
BODY = "CapeJones_Body"
TOL = {}
fails = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        fails.append(name)


def rig():
    return bpy.data.objects[RIG]


def body():
    return bpy.data.objects[BODY]


def reset(r):
    for pb in r.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.scale = (1, 1, 1)
    r.pose.bones["root"]["ik_spine"] = 0.0
    bpy.context.view_layer.update()


def eval_coords(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    eo = obj.evaluated_get(dg)
    em = eo.to_mesh()
    n = len(em.vertices)
    co = np.empty(n * 3, dtype=np.float64)
    em.vertices.foreach_get("co", co)
    eo.to_mesh_clear()
    return co.reshape(n, 3)


def rest_world(bn):
    return bpy.data.objects[RIG].data.bones[bn].matrix_local.copy()


def cum_rot_deg(bn):
    """Rest-relative cumulative rotation of a pose bone (degrees, XYZ)."""
    pb = rig().pose.bones[bn]
    M = rest_world(bn).inverted() @ pb.matrix
    return [float(np.degrees(v)) for v in M.to_euler("XYZ")]


def main():
    r = rig()
    b = body()

    # ---- 0. structural ----
    nbones = len(r.data.bones)
    check("bone_count_94", nbones == 94, f"got {nbones}")
    for bn, deform in [("spine_3", True), ("spine_4", True),
                       ("spine_fk_1", False), ("spine_fk_2", False),
                       ("spine_fk_3", False), ("spine_fk_4", False),
                       ("chest_fk", False), ("chest_ik", False),
                       ("spine_twist", False)]:
        pb = r.pose.bones.get(bn)
        ok = pb is not None and (r.data.bones[bn].use_deform == deform)
        check(f"bone_{bn}", ok)
    check("ik_spine_prop", "ik_spine" in r.pose.bones["root"])
    # deform constraints
    for dn, fk in [("spine_1", "spine_fk_1"), ("spine_2", "spine_fk_2"),
                   ("spine_3", "spine_fk_3"), ("spine_4", "spine_fk_4"),
                   ("chest", "chest_fk")]:
        pb = r.pose.bones[dn]
        kinds = {c.name: c.type for c in pb.constraints}
        ok = kinds.get("FK") == "COPY_ROTATION" and kinds.get("TWIST") == "COPY_ROTATION"
        fk_c = pb.constraints.get("FK")
        tw_c = pb.constraints.get("TWIST")
        ok = ok and fk_c.subtarget == fk and tw_c.subtarget == "spine_twist"
        ok = ok and fk_c.mix_mode == "REPLACE" and tw_c.mix_mode == "ADD"
        ok = ok and abs(fk_c.influence - 1.0) < 1e-6 and abs(tw_c.influence - 0.2) < 1e-6
        check(f"deform_constraints_{dn}", ok)
    ikc = r.pose.bones["chest_fk"].constraints.get("IK")
    ok = ikc is not None and ikc.type == "IK" and ikc.subtarget == "chest_ik" and ikc.chain_count == 5
    check("ik_on_chest_fk", ok)
    # driver lives on the rig object's animation data
    drv_found = False
    if r.animation_data:
        for d in r.animation_data.drivers:
            if 'chest_fk' in d.data_path and d.data_path.endswith('influence'):
                drv_found = True
    check("ik_driver", drv_found)

    # ---- 1. rest stability vs pre-build sample ----
    reset(r)
    co = eval_coords(b)
    s = np.load("/tmp/spine_rest_sample.npz")
    idx, co0 = s["idx"], s["co"]
    tight = (np.abs(co0[:, 0]) < 0.12) & (co0[:, 2] < 0.80)
    d = np.abs(co[idx[tight]] - co0[tight]).max()
    check("rest_stability", d < 1e-4, f"max drift {d:.2e} m")

    # ---- 2. FK forward bend: exact per-joint distribution (5 x 12deg = 60deg) ----
    reset(r)
    for i in range(1, 5):
        r.pose.bones[f"spine_fk_{i}"].rotation_euler = (0.21, 0, 0)
    r.pose.bones["chest_fk"].rotation_euler = (0.21, 0, 0)
    bpy.context.view_layer.update()
    angs = [cum_rot_deg(bn)[0] for bn in
            ["spine_1", "spine_2", "spine_3", "spine_4", "chest"]]
    exp = [12, 24, 36, 48, 60]
    ok = all(abs(a - e) < 1.5 for a, e in zip(angs, exp))
    check("bend_distributed", ok,
          "cumulative X-rot: " + ", ".join(f"{a:.1f}" for a in angs) + " (expect 12/24/36/48/60)")
    # surface smoothness: the OUTER back line (max-y vert per z-band) must
    # displace monotonically with height — a smooth arc, no kinks.
    # (A raw strip can't be used: verts at the same z but different depths
    # legitimately move different amounts under rotation.)
    co_b = eval_coords(b)
    m = (np.abs(co[:, 0]) < 0.03) & (co[:, 1] > 0.0) & (co[:, 2] > 0.52) & (co[:, 2] < 0.78)
    zz = co[:, 2][m]
    yy = co[:, 1][m]
    dd = np.linalg.norm(co_b[m] - co[m], axis=1)
    bands = np.arange(0.52, 0.78, 0.005)
    line_z, line_d = [], []
    for b0 in bands:
        sel = (zz >= b0) & (zz < b0 + 0.005)
        if sel.sum() == 0:
            continue
        j = np.argmax(yy[sel])
        idx = np.where(sel)[0][j]
        line_z.append(zz[idx]); line_d.append(dd[idx])
    line_z = np.array(line_z); line_d = np.array(line_d)
    o = np.argsort(line_z); line_z = line_z[o]; line_d = line_d[o]
    dips = -np.diff(line_d)
    maxdip = float(dips.max()) if len(dips) else 0.0
    # Spearman rank correlation z vs disp
    rz = np.argsort(np.argsort(line_z)).astype(float)
    rd = np.argsort(np.argsort(line_d)).astype(float)
    spear = np.corrcoef(rz, rd)[0, 1]
    check("bend_smooth", spear > 0.99 and maxdip < 0.02,
          f"outer-line Spearman={spear:.3f}, max local dip {maxdip*1000:.1f}mm, top disp {line_d[-5:].mean():.3f}m")

    # ---- 3. twist distribution (45deg master -> ~9deg per joint) ----
    reset(r)
    r.pose.bones["spine_twist"].rotation_euler = (0, np.radians(45), 0)
    bpy.context.view_layer.update()
    angs = [cum_rot_deg(bn)[1] for bn in
            ["spine_1", "spine_2", "spine_3", "spine_4", "chest"]]
    exp = [9, 18, 27, 36, 45]
    ok = all(abs(a - e) < 2.0 for a, e in zip(angs, exp))
    check("twist_distributed", ok,
          "cumulative Y-rot: " + ", ".join(f"{a:.1f}" for a in angs) + " (expect ~9/18/27/36/45)")
    # candy-wrapper: waist ring radius preserved under 45deg twist
    co_t = eval_coords(b)
    ring = (np.abs(co[:, 2] - 0.60) < 0.01)
    ax = np.array([0.0, -0.003])
    r0 = np.linalg.norm(co[ring][:, :2] - ax, axis=1)
    r1 = np.linalg.norm(co_t[ring][:, :2] - ax, axis=1)
    ratio = (r1 / np.maximum(r0, 1e-9)).min()
    check("no_candy_wrapper", ratio > 0.93, f"min radius ratio {ratio:.3f}")

    # ---- 4. IK mode: reachable target (chain reach is 0.25m) ----
    # chest_ik points +Z: local (0,-0.06,+0.10) == world (0,-0.10,-0.06)
    reset(r)
    r.pose.bones["root"]["ik_spine"] = 1.0
    r.pose.bones["chest_ik"].location = (0, -0.06, 0.10)
    r.pose.bones["chest_fk"].rotation_euler = (0.25, 0, 0)
    bpy.context.view_layer.update()
    # tip tracks the target
    tip = (r.pose.bones["chest_fk"].matrix.translation)
    tgt = (r.pose.bones["chest_ik"].matrix.translation)
    err = (tip - tgt).length
    check("ik_tip_tracks", err < 0.02, f"tip-target error {err*1000:.1f}mm")
    # pelvis bone stays put
    pelv_move = (r.pose.bones["pelvis"].matrix.translation -
                 rest_world("pelvis").translation).length
    check("ik_pelvis_stable", pelv_move < 0.002, f"pelvis moved {pelv_move*1000:.2f}mm")
    # spine articulated, not rigid: waist participates (stiffness-tuned),
    # no joint cranked past 40deg local
    cum = [cum_rot_deg(bn)[0] for bn in ["spine_1", "spine_2", "spine_3", "spine_4"]]
    loc = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, 4)]
    ok = all(a > 2.0 for a in cum) and all(a < 40.0 for a in loc)
    check("ik_distributed", ok,
          "spine cumulative X-rot: " + ", ".join(f"{a:.1f}" for a in cum) +
          " (locals: " + ", ".join(f"{a:.1f}" for a in loc) + ")")
    # surface: chest-top moves a lot; hip verts near the waist pivot follow
    # through a few cm (soft tissue), pelvis bone itself is rock-stable
    co_ik = eval_coords(b)
    moved = np.linalg.norm(co_ik - co, axis=1)
    chest_m = (co[:, 2] > 0.74) & (np.abs(co[:, 0]) < 0.12)
    hip_m = (co[:, 2] > 0.42) & (co[:, 2] < 0.47) & (np.abs(co[:, 0]) < 0.10)
    ok = moved[chest_m].max() > 0.08 and moved[hip_m].max() < 0.06
    check("ik_bend", ok, f"chest-top max move {moved[chest_m].max():.3f}m, hip max move {moved[hip_m].max():.4f}m")

    # ---- 5. weight sanity ----
    mesh = b.data
    vg_idx = {g.index: g.name for g in b.vertex_groups}
    # remapped verts = members of the new spine_3/spine_4 groups -> must be <=4
    # (repo standard); global max must not regress past the pre-lane level (8)
    i3 = b.vertex_groups["spine_3"].index
    i4 = b.vertex_groups["spine_4"].index
    cand = np.where((co[:, 2] > 0.45) & (co[:, 2] < 0.80) & (np.abs(co[:, 0]) < 0.14))[0]
    sel = cand[::max(1, len(cand) // 2000)]
    maxdev, maxinf, maxinf_remapped = 0.0, 0, 0
    for i in sel:
        v = mesh.vertices[int(i)]
        groups = [(g.group, g.weight) for g in v.groups]
        tot = sum(w for _, w in groups)
        maxdev = max(maxdev, abs(tot - 1.0))
        maxinf = max(maxinf, len(groups))
        gidx = {gi for gi, _ in groups}
        if i3 in gidx or i4 in gidx:
            maxinf_remapped = max(maxinf_remapped, len(groups))
    check("weights_normalized", maxdev < 1e-4, f"max |sum-1| {maxdev:.2e} over {len(sel)} verts")
    check("weights_remapped_max4", maxinf_remapped <= 4, f"remapped max influences {maxinf_remapped}")
    check("weights_no_regression", maxinf <= 8, f"global max influences {maxinf} (pre-lane: 8)")

    reset(r)
    print("RESULT:", "ALL PASS" if not fails else f"FAILURES: {fails}")
    sys.exit(1 if fails else 0)


main()
