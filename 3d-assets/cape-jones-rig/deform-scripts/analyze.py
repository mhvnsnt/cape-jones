"""Analyze deformation: defect zones + corrective shape-key deltas.
Input: /tmp/deform_npz/{rest,elbowL,elbowR,jaw,headL}.npz + faces.npz
Output: /tmp/deform_npz/correctives.npz with per-key (indices, delta_rest)
"""
import numpy as np
from scipy.spatial import cKDTree

NPZ = "/tmp/deform_npz"
rest_d = np.load(f"{NPZ}/rest.npz")
R = rest_d["rest"]
n = len(R)
print("verts:", n, flush=True)

faces = np.load(f"{NPZ}/faces.npz")
tris, quads = faces["tris"], faces["quads"]
print("tris:", len(tris), "quads:", len(quads), flush=True)

# ---------- adjacency (CSR-ish via bincount) ----------
e0 = np.concatenate([tris[:, 0], tris[:, 1], tris[:, 2],
                     quads[:, 0], quads[:, 1], quads[:, 2], quads[:, 3]])
e1 = np.concatenate([tris[:, 1], tris[:, 2], tris[:, 0],
                     quads[:, 1], quads[:, 2], quads[:, 3], quads[:, 0]])
src = np.concatenate([e0, e1])
dst = np.concatenate([e1, e0])
deg = np.bincount(src, minlength=n).astype(np.float32)
print("edges built", flush=True)

def laplacian_smooth(P, mask, iters=6, factor=0.5):
    P = P.copy()
    midx = np.where(mask)[0]
    for _ in range(iters):
        # sum of neighbor positions
        s = np.zeros_like(P)
        np.add.at(s, src, P[dst])
        avg = s / np.maximum(deg[:, None], 1)
        P[midx] += factor * (avg[midx] - P[midx])
    return P

def quat_to_mat(q):
    w, x, y, z = q
    return np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w)],
        [2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w)],
        [2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)],
    ], dtype=np.float64)

def slerp(q0, q1, t):
    # q0,q1 shape (4,), t shape (m,) -> (m,4)
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
        a = np.sin((1 - t) * th) / s
        b = np.sin(t * th) / s
        out = q0[None, :] * a[:, None] + q1[None, :] * b[:, None]
    out /= np.linalg.norm(out, axis=1, keepdims=True)
    return out

def blend_rot_mats(qa, qb, wa, wb):
    t = wb / np.maximum(wa + wb, 1e-9)
    qs = slerp(qa, qb, t)
    mats = np.empty((len(qs), 3, 3))
    for i, q in enumerate(qs):
        mats[i] = quat_to_mat(q)
    return mats

def spike_report(P, name, mask):
    D = P - R
    # spatial hash residual
    cell = 0.004
    key = np.floor(R / cell).astype(np.int64)
    ukey, inv = np.unique(key, axis=0, return_inverse=True)
    cnt = np.bincount(inv, minlength=len(ukey))
    s = np.zeros((len(ukey), 3))
    np.add.at(s, inv, D)
    mean = s / np.maximum(cnt[:, None], 1)
    resid = np.linalg.norm(D - mean[inv], axis=1)
    m = mask
    if m.sum() == 0:
        print(f"[{name}] empty mask", flush=True)
        return
    vals = resid[m]
    print(f"[{name}] region verts={m.sum()} max_resid={vals.max()*1000:.2f}mm "
          f"p99={np.percentile(vals,99)*1000:.2f}mm p95={np.percentile(vals,95)*1000:.2f}mm "
          f"max_disp={np.linalg.norm(D[m],axis=1).max()*1000:.1f}mm", flush=True)
    return resid

def build_corrective(pose_name, mask, bone_pair, push_mm=0.0, smooth_iters=8):
    d = np.load(f"{NPZ}/{pose_name}.npz")
    P = d["posed"].astype(np.float64)
    Np = d["posed_normal"].astype(np.float64)
    resid = spike_report(P, pose_name, mask)
    S = laplacian_smooth(P, mask, iters=smooth_iters, factor=0.5)
    delta_posed = S - P
    if push_mm:
        delta_posed[mask] += Np[mask] * (push_mm / 1000.0)
    # map to rest space via inverse blended bone rotation
    (ba, bb) = bone_pair
    wa = rest_d[f"w_{ba}"].astype(np.float64)
    wb = rest_d[f"w_{bb}"].astype(np.float64)
    qa = d[f"q_{ba}"].astype(np.float64)
    qb = d[f"q_{bb}"].astype(np.float64)
    midx = np.where(mask)[0]
    Rm = blend_rot_mats(qa, qb, wa[midx], wb[midx])
    delta_rest = np.einsum('mij,mj->mi', Rm.transpose(0, 2, 1), delta_posed[midx])
    mag = np.linalg.norm(delta_rest, axis=1)
    print(f"  corrective {pose_name}: max_delta={mag.max()*1000:.2f}mm mean={mag.mean()*1000:.3f}mm", flush=True)
    return midx, delta_rest.astype(np.float32), resid

W = {k: rest_d[k] for k in rest_d.files if k.startswith("w_")}

# ---------- region masks ----------
# elbow L inner: blend of upperarm_L/forearm_L, front (-Y) of elbow center
elb_c = np.array([0.43, -0.04, 0.72])
blendL = np.minimum(W["w_upperarm_L"], W["w_forearm_L"])
mask_elbL = (blendL > 0.06) & (R[:, 1] < -0.015) & (np.linalg.norm(R - elb_c, axis=1) < 0.16)
blendR = np.minimum(W["w_upperarm_R"], W["w_forearm_R"])
elb_cR = np.array([-0.43, -0.04, 0.72])
mask_elbR = (blendR > 0.06) & (R[:, 1] < -0.015) & (np.linalg.norm(R - elb_cR, axis=1) < 0.16)
# jaw: jaw-weighted verts in face zone
mask_jaw = (W["w_jaw"] > 0.10) & (R[:, 2] > 0.74) & (np.abs(R[:, 0]) < 0.14) & (R[:, 1] < 0.0)
# neck/head blend
mask_neck = (np.minimum(W["w_neck_2"], W["w_head"]) > 0.06) & (R[:, 2] > 0.76) & (R[:, 2] < 0.88)

# ---------- weight distribution audit ----------
print("--- jaw weight audit by z-band ---", flush=True)
wj = W["w_jaw"]
for zlo, zhi in [(0.74, 0.80), (0.80, 0.84), (0.84, 0.88), (0.88, 0.93)]:
    m = (wj > 0.01) & (R[:, 2] >= zlo) & (R[:, 2] < zhi)
    print(f"  z {zlo}-{zhi}: verts={(m).sum()} mean_w={wj[m].mean() if m.sum() else 0:.3f} max_w={wj[m].max() if m.sum() else 0:.3f}", flush=True)
print("--- neck/head weight audit ---", flush=True)
for gname in ["w_neck_1", "w_neck_2", "w_head"]:
    w = W[gname]
    print(f"  {gname}: nonzero={(w>0.01).sum()} mean={w[w>0.01].mean():.3f}", flush=True)

# ---------- hinge weight smoothing (elbow blend zones) ----------
def smooth_weights(w, mask, iters=3, factor=0.5):
    w = w.astype(np.float64).copy()
    midx = np.where(mask)[0]
    for _ in range(iters):
        s = np.zeros_like(w)
        np.add.at(s, src, w[dst])
        avg = s / np.maximum(deg, 1)
        w[midx] += factor * (avg[midx] - w[midx])
    return w.astype(np.float32)

# dilate masks slightly for smooth falloff of the weight edit
def dilate(mask, iters=2):
    m = mask.copy()
    for _ in range(iters):
        touched = np.zeros(n, dtype=bool)
        np.logical_or.at(touched, src, m[dst])
        m = m | touched
    return m

out = {}
for key, pose, mask, pair, push in [
    ("corr_elbow_L", "elbowL", mask_elbL, ("upperarm_L", "forearm_L"), 1.2),
    ("corr_elbow_R", "elbowR", mask_elbR, ("upperarm_R", "forearm_R"), 1.2),
    ("corr_jaw_open", "jaw", mask_jaw, ("head", "jaw"), 0.6),
    ("corr_neck_head", "headL", mask_neck, ("neck_2", "head"), 0.4),
]:
    midx, delta, resid = build_corrective(pose, mask, pair, push_mm=push)
    out[key + "_idx"] = midx.astype(np.int32)
    out[key + "_delta"] = delta
    out[key + "_maskcount"] = np.array([mask.sum()])

np.savez_compressed(f"{NPZ}/correctives.npz", **out)

# smooth hinge weights and save
for side, mask, ga, gb in [("L", mask_elbL, "w_upperarm_L", "w_forearm_L"),
                           ("R", mask_elbR, "w_upperarm_R", "w_forearm_R")]:
    dm = dilate(mask, 2)
    for gname in (ga, gb):
        ws = smooth_weights(W[gname], dm)
        chg = np.abs(ws - W[gname])
        idx = np.where(chg > 1e-4)[0]
        out2key = f"smooth_{gname[2:]}"
        out[out2key + "_idx"] = idx.astype(np.int32)
        out[out2key + "_val"] = ws[idx]
        print(f"  weight smooth {gname}: {len(idx)} verts changed, max_dw={chg.max():.3f}", flush=True)

np.savez_compressed(f"{NPZ}/correctives.npz", **out)
print("SAVED correctives.npz", flush=True)
