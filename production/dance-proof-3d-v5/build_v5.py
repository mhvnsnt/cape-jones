"""Cape Jones 3D dance v5 - STAGE A: build the NEW STANDING RIG.

Opens the repo base rig READ-ONLY and saves a NEW file (standing rig).
The sitting rig / sitting pose library are never written (owner rule
2026-11-02). This rig's default is STANDING.

Fixes applied to the copy:
 1. Preserve Volume (dual-quaternion) ON for body + cape armature
    modifiers (bake-off winning recipe; the v3 scene had it OFF and v4
    inherited OFF).
 2. Twist bones for upperarm/forearm/thigh (bake-off step 4): deform-only
    children taking 50% of the parent bone's axial twist via COPY_ROTATION
    (LOCAL, Y-only, influence 0.5); distal-half weights split 50/50 onto
    the twist bone. Kills candy-wrapper collapse in biceps/forearm/thigh.
 3. Shoulder/deltoid weight repair (the owner's named defect; bake-off
    defect zone 1: right-shoulder pinch/collapse, solver asymmetry):
    across the shoulder joint, the chest+clavicle share and the upperarm
    share are re-blended by a smooth falloff along the upperarm axis -
    torso-side verts gain partial upperarm influence and arm-side verts
    keep partial torso influence, so the seam is a gradient, not a wall.
    Same construction both sides (asymmetry removed by construction).
 4. Ankle transition tighten (bake-off defect zone 2): shin/foot weights
    re-blended in a narrow band across the ankle joint.
 5. Influences capped at 4 + totals renormalized (repo standard).
 6. Report JSON: per-group vertex counts + total weights, L/R, before
    and after - the repair is measured, not claimed.

Run: blender -b --python build_v5.py -- <base.blend> <out.blend> <report.json>
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BASE, OUT, REPORT = argv[0], argv[1], argv[2]

if os.path.abspath(bpy.data.filepath) != os.path.abspath(BASE):
    bpy.ops.wm.open_mainfile(filepath=BASE)
rig = bpy.data.objects["CapeJones_Rig"]
body = None
for ob in bpy.data.objects:
    if ob.type == "MESH" and len(ob.data.vertices) > 100000:
        body = ob
        break
assert rig and body, "rig/body not found"
print("[v5] base:", BASE, "| rig bones:", len(rig.data.bones),
      "| body:", body.name, len(body.data.vertices), flush=True)

for pb in rig.pose.bones:
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0)
    pb.scale = (1, 1, 1)
bpy.context.view_layer.update()

B = {b.name: (Vector(b.head_local), Vector(b.tail_local)) for b in rig.data.bones}

def group_stats(obj):
    cnt, tot = {}, {}
    for g in obj.vertex_groups:
        cnt[g.name], tot[g.name] = 0, 0.0
    name_of = {g.index: g.name for g in obj.vertex_groups}
    for v in obj.data.vertices:
        for g in v.groups:
            if g.weight > 0.01:
                cnt[name_of[g.group]] += 1
                tot[name_of[g.group]] += g.weight
    return {"count_gt01": cnt, "total_weight": {k: round(x, 1) for k, x in tot.items()}}

report = {"base": BASE, "body": body.name, "verts": len(body.data.vertices),
          "before": group_stats(body)}

# ---------------------------------------------------------------- 1. PV on
for ob in bpy.data.objects:
    if ob.type != "MESH":
        continue
    for md in ob.modifiers:
        if md.type == "ARMATURE" and md.object == rig:
            md.use_deform_preserve_volume = True
print("[v5] preserve volume ON", flush=True)

# ------------------------------------------------------- 2. twist bones
def add_twist(parent_name, twist_name, target_name):
    """Bake-off add_twist_bones() construction, adapted to this rig's
    two-layer system: the twist bone is a deform child of the limb bone
    (so it inherits the limb's FK/IK-driven motion) spanning the bone's
    middle-to-distal half, plus a COPY_ROTATION (LOCAL, Y-only, 0.5)
    from the NEXT deform bone down - it absorbs half the downstream
    twist so the segment doesn't candy-wrapper."""
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    eb = rig.data.edit_bones
    p = eb[parent_name]
    h, t = Vector(p.head), Vector(p.tail)
    nb = eb.new(twist_name)
    nb.head, nb.tail = h + (t - h) * 0.5, t
    nb.parent = p
    nb.use_deform = True
    nb.use_connect = False
    nb.align_roll(p.vector)
    bpy.ops.object.mode_set(mode="POSE")
    pb = rig.pose.bones[twist_name]
    c = pb.constraints.new("COPY_ROTATION")
    c.target = rig
    c.subtarget = target_name
    c.use_x = c.use_z = False
    c.use_y = True
    c.mix_mode = "REPLACE"
    c.target_space = c.owner_space = "LOCAL"
    c.influence = 0.5
    bpy.ops.object.mode_set(mode="OBJECT")

TWISTS = []
for side in ("L", "R"):
    for parent, tw, tgt in ((f"upperarm_{side}", f"upperarm_twist_{side}", f"forearm_{side}"),
                            (f"forearm_{side}", f"forearm_twist_{side}", f"hand_{side}"),
                            (f"thigh_{side}", f"thigh_twist_{side}", f"shin_{side}")):
        if parent in rig.data.bones and tw not in rig.data.bones:
            add_twist(parent, tw, tgt)
            TWISTS.append((parent, tw))
print("[v5] twist bones:", TWISTS, flush=True)

me = body.data
n = len(me.vertices)

def split_weights(parent, twist):
    if twist not in body.vertex_groups:
        body.vertex_groups.new(name=twist)
    h, t = B[parent]
    axis = t - h
    L2 = axis.length_squared
    vg_p, vg_t = body.vertex_groups[parent], body.vertex_groups[twist]
    moved = 0
    for v in me.vertices:
        w = 0.0
        for g in v.groups:
            if g.group == vg_p.index:
                w = g.weight
                break
        if w <= 0.01:
            continue
        tt = (Vector(v.co) - h).dot(axis) / L2
        if tt > 0.5:
            share = w * 0.5 * min(1.0, (tt - 0.5) * 2.0)
            if share > 0.01:
                vg_p.add([v.index], w - share, "REPLACE")
                vg_t.add([v.index], share, "REPLACE")
                moved += 1
    print(f"[v5] twist split {parent}: {moved} verts", flush=True)

for parent, tw in TWISTS:
    split_weights(parent, tw)

# ------------------------------------------- 3+4. falloff zone re-blending
coords = np.empty(n * 3, dtype=np.float64)
me.vertices.foreach_get("co", coords)
coords = coords.reshape(n, 3)
name_of = {g.index: g.name for g in body.vertex_groups}

def get_weights(names):
    W = {nm: np.zeros(n) for nm in names}
    for v in me.vertices:
        for g in v.groups:
            nm = name_of[g.group]
            if nm in W:
                W[nm][v.index] = g.weight
    return W

def set_weights(W, OLD=None):
    for nm, arr in W.items():
        vg = body.vertex_groups[nm]
        idxs = np.nonzero(arr > 0.005)[0]
        for i in idxs:
            vg.add([int(i)], float(arr[i]), "REPLACE")
        if OLD is not None and nm in OLD:
            rem = np.nonzero((OLD[nm] > 0.005) & (arr <= 0.005))[0]
            if len(rem):
                vg.remove([int(i) for i in rem])

def sstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)

def proj_tt(head, tail):
    h = np.array(head); t = np.array(tail); axis = t - h
    L2 = float(axis @ axis)
    tt = ((coords - h) @ axis) / L2
    closest = h + np.clip(tt, 0, 1)[:, None] * axis
    dist = np.linalg.norm(coords - closest, axis=1)
    return tt, dist

zone_counts = {}
# --- shoulder: segment = upperarm (shoulder joint -> elbow).
# total = chest + clavicle + upperarm(+twist excluded, proximal zone).
# s = sstep((tt + 0.45) / 0.95): at tt=-0.45 (torso side) s=0 (all torso),
# at tt=0.5 (mid-upperarm) s=1 (all arm). Torso share keeps chest:clavicle
# ratio. Applied to verts within radius 1.1x upperarm length of the segment
# whose total > 0.01.
for side in ("L", "R"):
    ua = f"upperarm_{side}"; cl = f"clavicle_{side}"
    names = ["chest", cl, ua]
    W = get_weights(names)
    total = W["chest"] + W[cl] + W[ua]
    h, t = B[ua]
    seg = (t - h).length
    tt, dist = proj_tt(h, t)
    zone = (dist < seg * 1.1) & (total > 0.01)
    s = sstep((tt + 0.45) / 0.95)
    torso = W["chest"] + W[cl]
    ratio = np.where(torso > 1e-6, W["chest"] / np.maximum(torso, 1e-6), 0.5)
    new = {"chest": total * (1 - s) * ratio,
           cl: total * (1 - s) * (1 - ratio),
           ua: total * s}
    OLD = {nm: W[nm].copy() for nm in names}
    for nm in names:
        W[nm][zone] = new[nm][zone]
    set_weights({nm: W[nm] for nm in names}, OLD)
    zone_counts[f"shoulder_{side}"] = int(zone.sum())
    print(f"[v5] shoulder reblend {side}: {int(zone.sum())} verts", flush=True)

# --- ankle: segment = shin head -> foot tail; blend band tt in [0.72, 1.0]
# total = shin + foot; w_foot = total * sstep((tt - 0.72) / 0.28).
for side in ("L", "R"):
    sh, ft = f"shin_{side}", f"foot_{side}"
    W = get_weights([sh, ft])
    total = W[sh] + W[ft]
    h = B[sh][0]; t = B[ft][1]
    tt, dist = proj_tt(h, t)
    seg = float(np.linalg.norm(np.array(t) - np.array(h)))
    zone = (dist < seg * 0.5) & (total > 0.01) & (tt > 0.6) & (tt < 1.1)
    s = sstep((tt - 0.72) / 0.28)
    newf = total * s
    news = total * (1 - s)
    OLD = {nm: W[nm].copy() for nm in (sh, ft)}
    W[ft][zone] = newf[zone]
    W[sh][zone] = news[zone]
    set_weights(W, OLD)
    zone_counts[f"ankle_{side}"] = int(zone.sum())
    print(f"[v5] ankle reblend {side}: {int(zone.sum())} verts", flush=True)
report["zones_reblended"] = zone_counts

# ---------------------- 5. hand/finger/toe weight completion
# Measured on the base: hand_L total weight = 111 verts, most finger
# groups = 0.0, toe_L/R = exactly 0.0. The SHD bake-off ran on a 20-bone
# test skeleton; on the full rig the extremities were never weighted -
# hands/fingers ride the forearm rigidly and toes do not exist as skin.
# Completion: distance-falloff skinning over the hand/toe bone segments
# (the classic distance-weighted extremity pass), pool-conserving so
# nothing else moves. Candidates are verts already carrying pool weight
# inside the extremity region; shares come from squared-exponential
# distance to each bone segment.
def seg_dist(P, h, t):
    h = np.array(h); t = np.array(t); axis = t - h
    L2 = float(axis @ axis)
    tt = np.clip(((P - h) @ axis) / max(L2, 1e-12), 0, 1)
    closest = h + tt[:, None] * axis
    return np.linalg.norm(P - closest, axis=1), tt

def complete_extremity(side, pool_names, target_segs, wrist_bone, sigma, gate_lo, gate_len):
    """target_segs: list of (group_name, head, tail). wrist_bone: (h, t)
    defines the axial gate: blend ramps 0->1 from gate_lo to gate_lo+gate_len
    along the wrist axis."""
    W = get_weights(pool_names)
    pool = sum(W[nm] for nm in pool_names)
    wh, wt = wrist_bone
    axis = np.array(wt) - np.array(wh)
    axis_n = axis / max(np.linalg.norm(axis), 1e-12)
    rel = coords - np.array(wh)
    axial = rel @ axis_n
    radial = np.linalg.norm(rel - np.outer(axial, axis_n), axis=1)
    cand = np.nonzero((pool > 0.03) & (axial > gate_lo - 0.02) & (radial < 0.055))[0]
    if len(cand) == 0:
        return 0
    P = coords[cand]
    blend = sstep((axial[cand] - gate_lo) / gate_len)
    shares = []
    for gname, h, t in target_segs:
        d, _ = seg_dist(P, h, t)
        shares.append(np.exp(-((d / sigma) ** 2)))
    S = np.stack(shares, axis=1)
    S = S / np.maximum(S.sum(axis=1, keepdims=True), 1e-12)
    pool_c = pool[cand]
    # pool split: (1-blend) stays as-is; blend share redistributes 85% to
    # the target segments by distance share, 15% residual stays in the
    # pool. ORDER MATTERS: subtract from the pool FIRST, then add the
    # shares - adding first and subtracting second overwrites the adds
    # (that bug zeroed the whole pass on the first production run).
    out = {nm: W[nm].copy() for nm in pool_names}
    taken = pool_c * blend * 0.85
    for nm in pool_names:
        frac = np.where(pool_c > 1e-9, W[nm][cand] / np.maximum(pool_c, 1e-9), 0)
        out[nm][cand] = np.clip(W[nm][cand] - taken * frac, 0, None)
    for gi, (gname, h, t) in enumerate(target_segs):
        if gname not in out:
            out[gname] = np.zeros(n)
        add = pool_c * blend * 0.85 * S[:, gi]
        idx = cand[add > 0.005]
        out[gname][idx] += add[add > 0.005]
    set_weights(out, W)
    return int(len(cand))

def complete_hand_fan(side):
    """Fan-axis collective finger skinning for the fused mitten.

    Why not per-segment distance shares (the first version): the sculpt's
    fingers are one fused mitten, and the base bake left full-weight
    finger-tip islands scattered at the wrist (finger_pinky_3_L = 1.0 on
    wrist verts). Distance shares over 18 competing segments reproduced
    the same patchwork - most chains ended at exactly 0.0 and the mitten
    could not curl (gate builds 5/6: fingers flat, one fin island flips
    alone). Production answer for a fused mitten: segment the fan by
    each finger's AXIS. Every distal vert's finger pool is split across
    the five finger chains by lateral softmax over the chain polylines,
    and along the owning chain by projection t with triangular joint
    kernels - smooth everywhere, no islands, and a synchronized curl
    (which is how the dance solve drives the fingers: master-coupled)
    bends the whole mitten as one.
    """
    hand = f"hand_{side}"
    fore = f"forearm_{side}"
    chains = {}
    for f in ("index", "middle", "ring", "pinky"):
        chains[f] = [f"finger_{f}_{i}_{side}" for i in (1, 2, 3)]
    chains["thumb"] = [f"finger_thumb_{i}_{side}" for i in (1, 2)]
    pool_names = [fore, hand] + [nm for c in chains.values() for nm in c]
    W = get_weights(pool_names)
    pool = sum(W[nm] for nm in pool_names)
    wh = np.array(B[hand][0])
    dwrist = np.linalg.norm(coords - wh, axis=1)
    cand = np.nonzero((pool > 0.03) & (dwrist > 0.006) & (dwrist < 0.09))[0]
    if len(cand) == 0:
        return 0
    P = coords[cand]
    g = sstep((dwrist[cand] - 0.010) / 0.018)
    finger_pool = pool[cand] * g * 0.85
    keep = 1.0 - g * 0.85
    out = {nm: W[nm].copy() for nm in pool_names}
    for nm in pool_names:
        out[nm][cand] = W[nm][cand] * keep
    lat = {}
    tmap = {}
    for f, chain in chains.items():
        pts = [np.array(B[chain[0]][0])] + [np.array(B[nm][1]) for nm in chain]
        dmin = np.full(len(cand), 1e9)
        tglob = np.zeros(len(cand))
        seglens = [float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1)]
        total = sum(seglens) or 1e-9
        acc = 0.0
        for i in range(len(pts) - 1):
            d, tt = seg_dist(P, pts[i], pts[i + 1])
            upd = d < dmin
            dmin = np.where(upd, d, dmin)
            tglob = np.where(upd, (acc + tt * seglens[i]) / total, tglob)
            acc += seglens[i]
        lat[f] = np.exp(-((dmin / 0.008) ** 2))
        tmap[f] = tglob
    L = np.stack([lat[f] for f in chains], axis=1)
    L = L / np.maximum(L.sum(axis=1, keepdims=True), 1e-12)
    for fi, (f, chain) in enumerate(chains.items()):
        tg = tmap[f]
        if len(chain) == 3:
            centers, width = (0.17, 0.5, 0.83), 0.52
        else:
            centers, width = (0.25, 0.75), 0.7
        K = np.stack([np.clip(1.0 - np.abs(tg - c) / width, 0, None) for c in centers], axis=1)
        K = K / np.maximum(K.sum(axis=1, keepdims=True), 1e-12)
        for si, nm in enumerate(chain):
            add = finger_pool * L[:, fi] * K[:, si]
            idx = cand[add > 0.003]
            out[nm][idx] += add[add > 0.003]
    set_weights(out, W)
    return int(len(cand))

comp_counts = {}
for side in ("L", "R"):
    hand = f"hand_{side}"
    c = complete_hand_fan(side)
    comp_counts[f"hand_{side}"] = c
    print(f"[v5] hand completion {side}: {c} verts", flush=True)
    ft, toe = f"foot_{side}", f"toe_{side}"
    segs = [(ft, B[ft][0], B[ft][1]), (toe, B[toe][0], B[toe][1])]
    c = complete_extremity(side, [ft, toe], segs, B[ft], sigma=0.012, gate_lo=0.028, gate_len=0.03)
    comp_counts[f"toe_{side}"] = c
    print(f"[v5] toe completion {side}: {c} verts", flush=True)
report["extremity_completion"] = comp_counts

# ---------------------- 5b. hand weight-field smoothing
# Gate bisect (probe7/9 + trial build): the distance-share completion
# alone TEARS the wrist - segment-distance shares form Voronoi-hard
# borders across the fused mitten, and adjacent verts on different
# finger bones shear apart under the hand/forearm pivot difference.
# Production skinning pipelines smooth the weight fields over the mesh
# after assignment (Dem Bones' smoothness term, Blender/Maya smooth
# weights). Apply Laplacian smoothing to the hand+finger fields in the
# hand region, preserving each vert's hand-region weight sum (forearm
# share untouched, so the cuff keeps one frame).
def build_edges():
    pv = np.empty(len(me.polygons) * 4, dtype=np.int64)
    me.polygons.foreach_get("vertices", pv)
    pv = pv.reshape(-1, 4)
    ea = np.concatenate([pv[:, 0], pv[:, 1], pv[:, 2], pv[:, 3]])
    eb = np.concatenate([pv[:, 1], pv[:, 2], pv[:, 3], pv[:, 0]])
    ok = ea != eb
    ea, eb = ea[ok], eb[ok]
    key = np.minimum(ea, eb) * np.int64(n) + np.maximum(ea, eb)
    uk = np.unique(key)
    return uk // n, uk % n

EA, EB = build_edges()
deg = np.zeros(n)
np.add.at(deg, EA, 1)
np.add.at(deg, EB, 1)
deg = np.maximum(deg, 1)

for side in ("L", "R"):
    hand = f"hand_{side}"
    fields = [hand] + [f"finger_{f}_{i}_{side}" for f in ("index", "middle", "ring", "pinky") for i in (1, 2, 3)] \
        + [f"finger_thumb_{i}_{side}" for i in (1, 2)]
    W = get_weights(fields)
    OLD = {nm: W[nm].copy() for nm in fields}
    tot0 = sum(W[nm] for nm in fields)
    wh, wt = B[hand]
    axis = np.array(wt) - np.array(wh)
    axis_n = axis / max(np.linalg.norm(axis), 1e-12)
    rel = coords - np.array(wh)
    axial = rel @ axis_n
    radial = np.linalg.norm(rel - np.outer(axial, axis_n), axis=1)
    region = np.nonzero((axial > -0.03) & (radial < 0.075) & (tot0 > 0.01))[0]
    if len(region) == 0:
        continue
    in_region = np.zeros(n, dtype=bool)
    in_region[region] = True
    for nm in fields:
        arr = W[nm]
        for _ in range(10):
            acc = np.zeros(n)
            np.add.at(acc, EA, arr[EB])
            np.add.at(acc, EB, arr[EA])
            avg = acc / deg
            new = arr.copy()
            new[region] = 0.5 * arr[region] + 0.5 * avg[region]
            arr = new
        W[nm] = arr
    tot1 = sum(W[nm] for nm in fields)
    scale = np.where(tot1 > 1e-9, tot0 / np.maximum(tot1, 1e-9), 0.0)
    for nm in fields:
        W[nm] = W[nm] * scale
    set_weights(W, OLD)
    print(f"[v5] hand smoothing {side}: {len(region)} verts", flush=True)
    report[f"hand_smoothed_{side}"] = int(len(region))

# ---------------------- 5c. wrist band cleanup
# Gate bisect verdict (probe7/9/10 + base-file gate run): the wrist tear
# exists IDENTICALLY in the untouched base rig. Cause: the SHD bake
# scattered finger-bone weight into the wrist zone (finger_pinky_2_L
# alone holds 663 weight units at the wrist crease; hand_L itself only
# 111 of 8,788 zone verts) - under a hard elbow bend the hand frame and
# forearm frame shear those islands apart. Standard production wrist
# skinning is a clean TWO-BONE blend: inside the wrist band, all finger
# weight is redistributed to hand/forearm by a smooth axial falloff.
# Distal of the band the (smoothed) finger weights stay - fingers curl.
for side in ("L", "R"):
    hand = f"hand_{side}"
    fore = f"forearm_{side}"
    fingers = [f"finger_{f}_{i}_{side}" for f in ("index", "middle", "ring", "pinky") for i in (1, 2, 3)] \
        + [f"finger_thumb_{i}_{side}" for i in (1, 2)]
    FW = get_weights(fingers + [hand, fore])
    wh, wt = B[hand]
    # Band = EUCLIDEAN distance from the wrist point. (First version used
    # projection on the hand bone's axis; the hand bone is a ~1 cm stub,
    # so the projection put most of the mitten inside the band and the
    # cleanup stripped the fingers' own weights - gate build 5: fingers
    # stayed flat, one fin of verts stood alone. Distance is the honest
    # measure: palm heel is within ~2 cm of the wrist, fingers are not.)
    dwrist = np.linalg.norm(coords - np.array(wh), axis=1)
    ftot = sum(FW[nm] for nm in fingers)
    # Crease guard only (completion v2 leaves no confetti to clean; the
    # wide first version ate the proximal finger weights). Inside
    # 1.4 cm of the wrist point, finger weight folds into the two-bone
    # forearm/hand blend; beyond it the fan-axis weights stand.
    cand = np.nonzero((dwrist < 0.014) & (ftot > 0.001))[0]
    if len(cand):
        tt = np.clip((dwrist[cand] - 0.004) / 0.010, 0.0, 1.0)
        blend = tt * tt * (3 - 2 * tt)
        F = ftot[cand]
        NEW = {hand: FW[hand].copy(), fore: FW[fore].copy()}
        OLDw = {hand: FW[hand], fore: FW[fore]}
        NEW[hand][cand] += F * blend
        NEW[fore][cand] += F * (1.0 - blend)
        for nm in fingers:
            arr = FW[nm].copy()
            OLDw[nm] = FW[nm]
            arr[cand] = 0.0
            NEW[nm] = arr
        set_weights(NEW, OLDw)
    print(f"[v5] wrist band cleanup {side}: {len(cand)} verts", flush=True)
    report[f"wrist_band_{side}"] = int(len(cand))

# ---------------------- 6. cape panel unification
# Gate evidence (first v5 gate run): the sculpt's cape panels - welded
# into the body mesh, hanging at the back/sides - fringe into strips
# when the thighs bend: SHD painted their verts with alternating
# pelvis/thigh allegiance down the sheet, and a bend pulls the rows
# apart. A cape hangs from the torso; it must not be leg-weighted at
# all. Selector: the back-side panel slab (lateral of the legs, behind
# the center plane, below the shoulder blades) - leg skin does not
# reach there. Any leg-bone weight found in the slab moves to pelvis.
LEG_GROUPS = []
for s in ("L", "R"):
    LEG_GROUPS += [f"thigh_{s}", f"shin_{s}", f"foot_{s}", f"toe_{s}",
                   f"thigh_twist_{s}"]
W = get_weights(LEG_GROUPS + ["pelvis"])
leg_tot = sum(W[nm] for nm in LEG_GROUPS)
ax = np.abs(coords[:, 0])
slab = (ax > 0.155) & (ax < 0.36) & (coords[:, 1] > 0.005) & (coords[:, 1] < 0.14) \
    & (coords[:, 2] > 0.06) & (coords[:, 2] < 0.60) & (leg_tot > 0.02)
moved = np.nonzero(slab)[0]
if len(moved):
    OLD = {nm: W[nm].copy() for nm in LEG_GROUPS + ["pelvis"]}
    W["pelvis"][moved] += leg_tot[moved]
    for nm in LEG_GROUPS:
        W[nm][moved] = 0.0
    set_weights({nm: W[nm] for nm in LEG_GROUPS + ["pelvis"]}, OLD)
report["cape_panel_unified"] = int(len(moved))
print("[v5] cape panel unified verts:", int(len(moved)), flush=True)

# --------------------------------- cap influences at 4 + renormalize (body)
renorm = 0
for v in me.vertices:
    gs = [(g.weight, g.group) for g in v.groups if g.weight > 0.005]
    if not gs:
        continue
    gs.sort(reverse=True)
    keep = gs[:4]
    tot = sum(w for w, _ in keep)
    if tot <= 0:
        continue
    if len(gs) > 4 or abs(tot - 1.0) > 0.02:
        renorm += 1
        for w, gi in gs[4:]:
            body.vertex_groups[name_of[gi]].remove([v.index])
        for w, gi in keep:
            body.vertex_groups[name_of[gi]].add([v.index], w / tot, "REPLACE")
print("[v5] renormalized verts:", renorm, flush=True)
report["renormalized_verts"] = renorm
report["after"] = group_stats(body)
report["twist_bones"] = [t for _, t in TWISTS]

bpy.ops.wm.save_as_mainfile(filepath=OUT)
with open(REPORT, "w") as f:
    json.dump(report, f, indent=1)
print("[v5] SAVED", OUT, flush=True)
print("BUILD_V5_DONE")
