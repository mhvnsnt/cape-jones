"""Wave-2 numeric deform audit: analyze /tmp/deform2/ dumps.
Flags: Laplacian-motion residual spikes, hinge collapse bands, cross-bone weight bleed.
Emits: text report + (if flagged) wave2_correctives.npz with (idx, delta_rest) per key,
weight smooth arrays, and mask counts. No hand edits anywhere.
"""
import numpy as np
import os
from scipy.spatial import cKDTree

NPZ = "/home/hatch/workspace/cj-deform-audit/3d-assets/cape-jones-rig/deform-wave2/scratch"
rest_d = np.load(f"{NPZ}/rest.npz")
R = rest_d["rest"].astype(np.float64)
n = len(R)
print("verts:", n, flush=True)

faces = np.load(f"{NPZ}/faces.npz")
tris = np.asarray(faces["tris"]).reshape(-1, 3)
quads = np.asarray(faces["quads"]).reshape(-1, 4)

edges = [tris[:, 0], tris[:, 1], tris[:, 2]]
if len(quads):
    edges += [quads[:, 0], quads[:, 1], quads[:, 2], quads[:, 3]]
e0 = np.concatenate(edges)
edges2 = [tris[:, 1], tris[:, 2], tris[:, 0]]
if len(quads):
    edges2 += [quads[:, 1], quads[:, 2], quads[:, 3], quads[:, 0]]
e1 = np.concatenate(edges2)
src = np.concatenate([e0, e1])
dst = np.concatenate([e1, e0])
deg = np.bincount(src, minlength=n).astype(np.float32)
print("edges built", flush=True)

def laplacian_smooth(P, mask, iters=6, factor=0.5):
    P = P.copy()
    midx = np.where(mask)[0]
    for _ in range(iters):
        s = np.zeros_like(P)
        np.add.at(s, src, P[dst])
        avg = s / np.maximum(deg[:, None], 1)
        P[midx] += factor * (avg[midx] - P[midx])
    return P

def residual(P):
    D = P - R
    cell = 0.004
    key = np.floor(R / cell).astype(np.int64)
    ukey, inv = np.unique(key, axis=0, return_inverse=True)
    cnt = np.bincount(inv, minlength=len(ukey))
    s = np.zeros((len(ukey), 3))
    np.add.at(s, inv, D)
    mean = s / np.maximum(cnt[:, None], 1)
    return np.linalg.norm(D - mean[inv], axis=1)

def quat_to_mat(q):
    w, x, y, z = q
    return np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w)],
        [2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w)],
        [2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)],
    ], dtype=np.float64)

def slerp(q0, q1, t):
    dot = np.dot(q0, q1)
    if dot < 0:
        q1 = -q1
        dot = -dot
    dot = np.clip(dot, -1, 1)
    if dot > 0.9995:
        out = q0[None, :] * (1 - t[:, None]) + q1[None, :] * t[:, None]
    else:
        th = np.arccos(dot)
        s = np.sin(th)
        out = q0[None, :] * (np.sin((1 - t) * th) / s)[:, None] + q1[None, :] * (np.sin(t * th) / s)[:, None]
    out /= np.linalg.norm(out, axis=1, keepdims=True)
    return out

def blend_rot_mats(qa, qb, wa, wb):
    t = wb / np.maximum(wa + wb, 1e-9)
    qs = slerp(qa, qb, t)
    mats = np.empty((len(qs), 3, 3))
    for i, q in enumerate(qs):
        mats[i] = quat_to_mat(q)
    return mats

def smooth_weights(w, mask, iters=3, factor=0.5):
    w = w.astype(np.float64).copy()
    midx = np.where(mask)[0]
    for _ in range(iters):
        s = np.zeros_like(w)
        np.add.at(s, src, w[dst])
        avg = s / np.maximum(deg, 1)
        w[midx] += factor * (avg[midx] - w[midx])
    return w.astype(np.float32)

def dilate(mask, iters=2):
    m = mask.copy()
    for _ in range(iters):
        touched = np.zeros(n, dtype=bool)
        np.logical_or.at(touched, src, m[dst])
        m = m | touched
    return m

W = {k[2:]: rest_d[k] for k in rest_d.files if k.startswith("w_")}

def build_fix(zname, z, mask, d, P, Np):
    S = laplacian_smooth(P, mask, iters=8, factor=0.5)
    delta_posed = S - P
    delta_posed[mask] += Np[mask] * (z["push"] / 1000.0)
    ba, bb = z["pair"]
    wa = rest_d["w_" + ba].astype(np.float64)
    wb = rest_d["w_" + bb].astype(np.float64)
    qa = d["q_" + ba].astype(np.float64)
    qb = d["q_" + bb].astype(np.float64)
    midx = np.where(mask)[0]
    Rm = blend_rot_mats(qa, qb, wa[midx], wb[midx])
    delta_rest = np.einsum('mij,mj->mi', Rm.transpose(0, 2, 1), delta_posed[midx]).astype(np.float32)
    mag = np.linalg.norm(delta_rest, axis=1)
    print(f"    corrective corr_{zname}: {len(midx)} verts max_delta={mag.max()*1000:.2f}mm "
          f"mean={mag.mean()*1000:.3f}mm", flush=True)
    return midx.astype(np.int32), delta_rest

def blend(g1, g2):
    return np.minimum(W[g1], W[g2])

def ball(c, r):
    return np.linalg.norm(R - np.array(c), axis=1) < r

# ---------- region masks + hinge pairs ----------
ZONES = {
    "shoulderL": dict(c=(0.243, -0.031, 0.745), r=0.15, blend=("clavicle_L", "upperarm_L"),
                      pose="shoulderL_side", pair=("clavicle_L", "upperarm_L"), push=1.0),
    "shoulderR": dict(c=(-0.243, -0.031, 0.745), r=0.15, blend=("clavicle_R", "upperarm_R"),
                      pose="shoulderR_side", pair=("clavicle_R", "upperarm_R"), push=1.0),
    "hipL": dict(c=(0.057, -0.041, 0.439), r=0.15, blend=("pelvis", "thigh_L"),
                 pose="hipL_flex", pair=("pelvis", "thigh_L"), push=1.0),
    "hipR": dict(c=(-0.057, -0.041, 0.439), r=0.15, blend=("pelvis", "thigh_R"),
                 pose="hipR_flex", pair=("pelvis", "thigh_R"), push=1.0),
    "kneeL": dict(c=(0.065, -0.037, 0.28), r=0.13, blend=("thigh_L", "shin_L"),
                  pose="kneeL", pair=("thigh_L", "shin_L"), push=1.2),
    "kneeR": dict(c=(-0.065, -0.037, 0.28), r=0.13, blend=("thigh_R", "shin_R"),
                  pose="kneeR", pair=("thigh_R", "shin_R"), push=1.2),
    "wristL": dict(c=(0.484, -0.044, 0.718), r=0.08, blend=("forearm_L", "hand_L"),
                   pose="wristL_bend", pair=("forearm_L", "hand_L"), push=0.6),
    "wristR": dict(c=(-0.484, -0.044, 0.718), r=0.08, blend=("forearm_R", "hand_R"),
                   pose="wristR_bend", pair=("forearm_R", "hand_R"), push=0.6),
    "ankleL": dict(c=(0.074, -0.022, 0.064), r=0.09, blend=("shin_L", "foot_L"),
                   pose="ankleL", pair=("shin_L", "foot_L"), push=0.6),
    "ankleR": dict(c=(-0.074, -0.022, 0.064), r=0.09, blend=("shin_R", "foot_R"),
                   pose="ankleR", pair=("shin_R", "foot_R"), push=0.6),
}
SPINE = dict(pose="spine_fwd", pair=("pelvis", "spine_1"), push=0.8)

out = {}
FLAGGED = []

for zname, z in ZONES.items():
    m = (blend(*z["blend"]) > 0.06) & ball(z["c"], z["r"])
    d = np.load(f"{NPZ}/{z['pose']}.npz")
    P = d["posed"].astype(np.float64)
    Np = d["posed_normal"].astype(np.float64)
    D = P - R
    res = residual(P)
    rv = res[m] if m.sum() else np.array([0])
    dv = np.linalg.norm(D[m], axis=1) if m.sum() else np.array([0])
    # volume proxy: mean distance to mask centroid, rest vs posed
    if m.sum():
        cr = R[m].mean(0); cp = P[m].mean(0)
        vr = np.linalg.norm(R[m] - cr, axis=1).mean()
        vp = np.linalg.norm(P[m] - cp, axis=1).mean()
        vol = vp / max(vr, 1e-9)
    else:
        vol = 1.0
    print(f"[{zname}] pose={z['pose']} verts={m.sum()} "
          f"max_resid={rv.max()*1000:.2f}mm p99={np.percentile(rv,99)*1000:.2f}mm "
          f"max_disp={dv.max()*1000:.1f}mm vol_ratio={vol:.3f}", flush=True)
    flagged = False
    reason = []
    if rv.max() * 1000 > 20:
        flagged = True; reason.append(f"max_resid {rv.max()*1000:.1f}mm")
    if np.percentile(rv, 99) * 1000 > 2.5 and m.sum() > 200:
        flagged = True; reason.append(f"p99 {np.percentile(rv,99)*1000:.2f}mm broad")
    if vol < 0.82:
        flagged = True; reason.append(f"collapse vol_ratio {vol:.3f}")
    if flagged:
        FLAGGED.append((zname, reason))
        midx, delta_rest = build_fix(zname, z, m, d, P, Np)
        out[f"corr_{zname}_idx"] = midx
        out[f"corr_{zname}_delta"] = delta_rest
        for g in z["blend"]:
            dm = dilate(m, 2)
            ws = smooth_weights(W[g], dm)
            chg = np.abs(ws - W[g])
            idx = np.where(chg > 1e-4)[0]
            out[f"smooth_w2_{zname}_{g}_idx"] = idx.astype(np.int32)
            out[f"smooth_w2_{zname}_{g}_val"] = ws[idx]
            print(f"    smooth {zname}/{g}: {len(idx)} verts, max_dw={chg.max():.3f}", flush=True)

# ---------- spine (waist + torso: pelvis/spine_1 and spine_1/spine_2 blends) ----------
m_sp = (((blend("pelvis", "spine_1") > 0.06) | (blend("spine_1", "spine_2") > 0.06))
        & (R[:, 2] > 0.38) & (R[:, 2] < 0.72) & (np.abs(R[:, 0]) < 0.15))
for pose, zname in [("spine_fwd", "spine_fwd"), ("spine_twist", "spine_twist")]:
    d = np.load(f"{NPZ}/{pose}.npz")
    P = d["posed"].astype(np.float64)
    D = P - R
    res = residual(P)
    rv = res[m_sp]
    dv = np.linalg.norm(D[m_sp], axis=1)
    print(f"[spine] pose={pose} verts={m_sp.sum()} max_resid={rv.max()*1000:.2f}mm "
          f"p99={np.percentile(rv,99)*1000:.2f}mm max_disp={dv.max()*1000:.1f}mm", flush=True)
    if rv.max() * 1000 > 20 or (np.percentile(rv, 99) * 1000 > 2.5):
        FLAGGED.append((zname, ["residual"]))
        midx, delta_rest = build_fix(zname, SPINE, m_sp, d, P, d["posed_normal"].astype(np.float64))
        out[f"corr_{zname}_idx"] = midx
        out[f"corr_{zname}_delta"] = delta_rest

# ---------- weight-bleed audit ----------
def bleed(gname, zone_mask, thresh=0.15, label=""):
    w = W[gname]
    m = zone_mask & (w > thresh)
    print(f"BLEED {gname} {label}: {m.sum()} verts > {thresh}", flush=True)
    return m.sum()

print("--- bleed audit ---", flush=True)
bleed("thigh_L", (R[:, 2] < 0.20), 0.15, "shin zone z<0.20")
bleed("thigh_R", (R[:, 2] < 0.20), 0.15, "shin zone z<0.20")
bleed("shin_L", (R[:, 2] < 0.05) & (R[:, 1] < -0.05), 0.15, "toe zone")
bleed("forearm_L", (R[:, 0] > 0.52), 0.15, "hand beyond wrist x>0.52")
bleed("forearm_R", (R[:, 0] < -0.52), 0.15, "hand beyond wrist x<-0.52")
bleed("upperarm_L", (R[:, 0] > 0.42), 0.15, "forearm zone x>0.42")
bleed("pelvis", (R[:, 2] < 0.30), 0.40, "mid-thigh z<0.30 strong pelvis")
bleed("spine_1", (R[:, 2] < 0.40), 0.15, "below spine_1 head")

print("\n=== FLAGGED ZONES ===", flush=True)
for z, r in FLAGGED:
    print(" ", z, "->", "; ".join(r), flush=True)
if not FLAGGED:
    print("  none", flush=True)

if out:
    np.savez_compressed(os.path.join(NPZ, "wave2_correctives.npz"), **out)
    print("SAVED wave2_correctives.npz", flush=True)
