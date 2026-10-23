"""Cross-section joint detector for Cape Jones (T-pose, faces -Y, up +Z, L=+X, feet z=0).
Reads /tmp/cj_verts.npy, writes /tmp/cj_joints.json. Pure numpy.
"""
import numpy as np, json

V = np.load('/tmp/cj_verts.npy').astype(np.float64)
print('verts', V.shape)

# ---------- slice + cluster ----------
def slice_clusters(zc, dz=0.002, cell=0.006, min_n=25, x=None, y=None, z=None):
    pts = V[np.abs(V[:, 2] - zc) < dz]
    if x is not None:
        pts = pts[(pts[:, 0] >= x[0]) & (pts[:, 0] <= x[1])]
    if y is not None:
        pts = pts[(pts[:, 1] >= y[0]) & (pts[:, 1] <= y[1])]
    if len(pts) < min_n:
        return []
    ci = np.floor(pts[:, :2] / cell).astype(np.int64)
    cells = {}
    for i, c in enumerate(map(tuple, ci)):
        cells.setdefault(c, []).append(i)
    # union-find over 8-neighborhood
    parent = {c: c for c in cells}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for c in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (c[0] + dx, c[1] + dy)
                if n in cells:
                    ra, rb = find(c), find(n)
                    if ra != rb:
                        parent[ra] = rb
    groups = {}
    for c, idxs in cells.items():
        groups.setdefault(find(c), []).extend(idxs)
    out = []
    for idxs in groups.values():
        if len(idxs) >= min_n:
            p = pts[idxs]
            cen = p[:, :2].mean(axis=0)
            r = np.percentile(np.linalg.norm(p[:, :2] - cen, axis=1), 90)
            out.append({'c': cen, 'r': float(r), 'n': len(idxs),
                        'z': zc, 'x': float(cen[0]), 'y': float(cen[1])})
    return out

def profile(z0, z1, dz=0.004):
    zs = np.arange(z0, z1, dz)
    rows = []
    for zc in zs:
        cl = slice_clusters(zc)
        rows.append((zc, cl))
    return rows

def argmin_smooth(vals, zs, win=3):
    v = np.array(vals, dtype=float)
    k = np.ones(win) / win
    vs = np.convolve(v, k, mode='same')
    return zs[int(np.argmin(vs))]

def argmax_smooth(vals, zs, win=3):
    v = np.array(vals, dtype=float)
    k = np.ones(win) / win
    vs = np.convolve(v, k, mode='same')
    return zs[int(np.argmax(vs))]

J = {}
prof = profile(0.0, 0.925)

def clusters_at(zc):
    for z, cl in prof:
        if abs(z - zc) < 0.0021:
            return cl
    return []

# ---------- legs ----------
leg_prof = []  # (z, xL, rL, xR, rR)
for z, cl in prof:
    if z > 0.52 or z < 0.01:
        continue
    legs = [c for c in cl if abs(c['y']) < 0.09 and abs(c['x']) < 0.20 and abs(c['x']) > 0.015]
    if len(legs) == 2:
        legs.sort(key=lambda c: c['x'])
        R, L = legs[0], legs[1]  # x<0 is R, x>0 is L
        leg_prof.append((z, L['x'], L['r'], R['x'], R['r'], L['y'], R['y']))
leg_prof = np.array(leg_prof)
# crotch: highest z with 2 leg clusters
crotch_z = leg_prof[:, 0].max()
J['crotch_z'] = float(crotch_z)
J['hip_z'] = float(crotch_z + 0.035)
row = leg_prof[np.argmax(leg_prof[:, 0])]
J['hip_L'] = [float(row[1]), float(row[5]), J['hip_z']]
J['hip_R'] = [float(row[3]), float(row[6]), J['hip_z']]
# knee: between thigh bulge and calf bulge, radius minimum
for side, (xi, ri, yi) in {'L': (1, 2, 5), 'R': (3, 4, 6)}.items():
    zs = leg_prof[:, 0]; r = leg_prof[:, ri]
    thigh = (zs > 0.30) & (zs < 0.46)
    calf = (zs > 0.06) & (zs < 0.22)
    zt = zs[thigh][np.argmax(r[thigh])]; zc = zs[calf][np.argmax(r[calf])]
    band = (zs >= zc) & (zs <= zt)
    zk = zs[band][np.argmin(r[band])]
    i = np.argmin(np.abs(zs - zk))
    J[f'knee_{side}'] = [float(leg_prof[i, xi]), float(leg_prof[i, yi]), float(zk)]
    # ankle: min radius low
    low = zs < 0.10
    za = zs[low][np.argmin(r[low])]
    i = np.argmin(np.abs(zs - za))
    J[f'ankle_{side}'] = [float(leg_prof[i, xi]), float(leg_prof[i, yi]), float(za)]
print('crotch', crotch_z, 'hip', J['hip_z'], 'knee_L', J['knee_L'], 'ankle_L', J['ankle_L'])

# ---------- feet ----------
for side, sx in {'L': 1, 'R': -1}.items():
    ax = J[f'ankle_{side}'][0]
    m = (V[:, 2] < J[f'ankle_{side}'][2] + 0.02) & (np.abs(V[:, 0] - ax) < 0.07)
    f = V[m]
    J[f'toe_{side}'] = [float(ax), float(f[:, 1].min()), float(f[:, 2].min() + 0.012)]
    J[f'heel_{side}'] = [float(ax), float(f[:, 1].max()), float(f[:, 2].min() + 0.012)]
    J[f'sole_{side}'] = [float(ax), float((f[:, 1].min() + f[:, 1].max()) / 2), float(f[:, 2].min())]
print('toe_L', J['toe_L'], 'sole', J['sole_L'][2])

# ---------- torso ----------
def torso_width(zc):
    cl = clusters_at(zc)
    big = [c for c in cl if abs(c['x']) < 0.16 and abs(c['y']) < 0.16]
    if not big:
        return 0, 0
    b = max(big, key=lambda c: c['n'])
    return b['r'] * 2, b['x'], b['y']

zs_t = np.arange(0.46, 0.62, 0.004)
widths = [torso_width(z)[0] for z in zs_t]
# torso is a near-straight column (width varies <1mm); waist is placed at the
# anatomical midpoint between hip and chest rather than a noisy argmin
J['waist_z'] = 0.56
zs_c = np.arange(0.60, 0.74, 0.004)
widths_c = [torso_width(z)[0] for z in zs_c]
J['chest_z'] = float(argmax_smooth(widths_c, zs_c))
# shoulder: z where arm inner edge meets torso edge; joint just outside torso
J['shoulder_z'] = 0.745
zc = J['shoulder_z']
tm = (np.abs(V[:, 2] - zc) < 0.004) & (np.abs(V[:, 1]) < 0.10) & (np.abs(V[:, 0]) < 0.24)
torso_hw = float(np.percentile(np.abs(V[tm][:, 0]), 92))
am = (np.abs(V[:, 2] - zc) < 0.004) & (np.abs(V[:, 1]) < 0.10) & (np.abs(V[:, 0]) > torso_hw)
for side, s in {'L': 1, 'R': -1}.items():
    sm = am & (np.sign(V[:, 0]) == s)
    p = V[sm]
    J[f'shoulder_{side}'] = [float(s * (torso_hw + 0.018)), float(np.median(p[:, 1])), float(zc)]
print('waist', J['waist_z'], 'chest', J['chest_z'], 'shoulder', J['shoulder_L'], 'hw', round(torso_hw, 3))

# ---------- neck / head ----------
J['neck_z'] = 0.80
nm = (V[:, 2] > 0.815) & (np.abs(V[:, 0]) < 0.10) & (V[:, 1] > -0.16) & (V[:, 1] < 0.06)
head = V[nm]
hc = head.mean(axis=0)
J['head_center'] = [float(hc[0]), float(hc[1]), float(hc[2])]
J['head_top'] = [float(hc[0]), float(hc[1]), float(head[:, 2].max())]
J['chin_z'] = float(J['neck_z'] + 0.03)
J['face_y'] = float(head[:, 1].min())  # facing -Y: face at min y
J['neck_base'] = [0.0, -0.01, float(J['neck_z'] - 0.01)]
print('neck', J['neck_z'], 'head_c', J['head_center'], 'top', J['head_top'][2], 'face_y', J['face_y'])

# ---------- arms (T-pose along X) ----------
def arm_profile(side):
    s = 1 if side == 'L' else -1
    xs = np.arange(0.10, 0.55, 0.006) * s
    rows = []
    for xc in xs:
        m = (np.abs(V[:, 0] - xc) < 0.007) & (V[:, 2] > J['shoulder_z'] - 0.12) & (V[:, 2] < J['shoulder_z'] + 0.08) & (np.abs(V[:, 1]) < 0.10)
        p = V[m]
        if len(p) < 30:
            continue
        # cluster in YZ to drop torso bleed
        c = np.array([p[:, 1].mean(), p[:, 2].mean()])
        r = np.percentile(np.linalg.norm(p[:, 1:3] - c, axis=1), 90)
        rows.append((abs(xc), float(c[0]), float(c[1]), float(r), len(p)))
    return rows

for side in ['L', 'R']:
    rows = arm_profile(side)
    xa = np.array([r[0] for r in rows]); ra = np.array([r[3] for r in rows])
    s = 1 if side == 'L' else -1
    # elbow: local min of r in [0.33, 0.42] (0.25 min is the armpit/deltoid blend)
    band = (xa > 0.33) & (xa < 0.42)
    xe = xa[band][np.argmin(ra[band])]
    # wrist: local min in [0.44, 0.49]
    band = (xa > 0.44) & (xa < 0.49)
    xw = xa[band][np.argmin(ra[band])]
    ie = np.argmin(np.abs(xa - xe)); iw = np.argmin(np.abs(xa - xw))
    J[f'elbow_{side}'] = [float(s * rows[ie][0]), float(rows[ie][1]), float(rows[ie][2])]
    J[f'wrist_{side}'] = [float(s * rows[iw][0]), float(rows[iw][1]), float(rows[iw][2])]
    # hand: beyond wrist (fixed mask: |x| beyond wrist on this side)
    hm = (s * V[:, 0] > rows[iw][0]) & (V[:, 2] > J['shoulder_z'] - 0.14) & (V[:, 2] < J['shoulder_z'] + 0.10) & (np.abs(V[:, 1]) < 0.12)
    h = V[hm]
    J[f'hand_{side}'] = [float(h[:, 0].mean()), float(h[:, 1].mean()), float(h[:, 2].mean())]
    tipx = float(h[:, 0].max() if s > 0 else h[:, 0].min())
    J[f'fingertip_{side}'] = [tipx, float(h[:, 1].mean()), float(h[:, 2].mean())]
    # fingers via PCA of the hand blob (fingers don't run along the arm axis here)
    hc0 = h.mean(axis=0)
    cov = np.cov((h - hc0).T)
    w, Vv = np.linalg.eigh(cov)
    fdir = Vv[:, np.argmax(w)]
    if np.dot(fdir, np.array([s, 0, 0])) < 0 and abs(fdir[0]) > abs(fdir[1]):
        fdir = -fdir
    # orient: fingers point away from wrist
    wpos = np.array(J[f'wrist_{side}'])
    if np.dot(fdir, hc0 - wpos) < 0:
        fdir = -fdir
    t = (h - hc0) @ fdir
    dtip = h[t >= np.percentile(t, 85)]; palm = h[t <= np.percentile(t, 30)]
    tip_c = dtip.mean(axis=0); palm_c = palm.mean(axis=0)
    J[f'finger_dir_{side}'] = [float(v) for v in fdir]
    J[f'palm_{side}'] = [float(v) for v in palm_c]
    J[f'finger_len_{side}'] = float((t.max() - t.min()) * 0.55)
    J[f'fingertip_{side}'] = [float(v) for v in tip_c]
    # thumb: front (-y) side of mid-hand
    mid = h[(t > np.percentile(t, 25)) & (t < np.percentile(t, 65))]
    th = mid[mid[:, 1] < np.percentile(mid[:, 1], 25)]
    J[f'thumb_{side}'] = [float(v) for v in th.mean(axis=0)] if len(th) > 20 else None
    # finger fan: hand cross-section at 60% hand length
    xb = rows[iw][0] + (abs(J[f'fingertip_{side}'][0]) - rows[iw][0]) * 0.55
    fm = (np.abs(np.abs(V[:, 0]) - xb) < 0.008) & (V[:, 2] > J['shoulder_z'] - 0.14) & (V[:, 2] < J['shoulder_z'] + 0.10) & (np.abs(V[:, 1]) < 0.12)
    fp = V[fm]
    J[f'hand_y_spread_{side}'] = float(fp[:, 1].max() - fp[:, 1].min())
    J[f'hand_z_spread_{side}'] = float(fp[:, 2].max() - fp[:, 2].min())
    print(side, 'elbow', J[f'elbow_{side}'], 'wrist', J[f'wrist_{side}'], 'hand', J[f'hand_{side}'], 'tip', J[f'fingertip_{side}'],
          'yspread', round(J[f'hand_y_spread_{side}'], 3), 'zspread', round(J[f'hand_z_spread_{side}'], 3))

# ---------- spine chain ----------
J['pelvis_c'] = [0.0, 0.0, J['hip_z']]
J['spine_base_z'] = float(J['hip_z'] + 0.02)
J['spine_top_z'] = float(J['chest_z'])
J['neck_base_z'] = float(J['neck_z'] - 0.01)

# ---------- cape ----------
cm = (V[:, 1] > 0.10) & (V[:, 2] < 0.84)
cape = V[cm]
zb = np.arange(0.02, 0.84, 0.02)
cprof = []
for zc in zb:
    m = np.abs(cape[:, 2] - zc) < 0.01
    if m.sum() > 50:
        cprof.append((zc, float(cape[m][:, 1].mean()), float(cape[m][:, 0].mean())))
J['cape_profile'] = [[round(z, 4), round(y, 4), round(x, 4)] for z, y, x in cprof]
J['cape_bottom_z'] = float(cape[:, 2].min())
J['cape_nverts'] = int(cm.sum())
print('cape verts', J['cape_nverts'], 'bottom', J['cape_bottom_z'], 'profile pts', len(cprof))

with open('/tmp/cj_joints.json', 'w') as f:
    json.dump(J, f, indent=1)
print('WROTE /tmp/cj_joints.json')
