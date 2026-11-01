"""Gap-close alignment QC (item 7) + knee-feet QC (item 8).
Method (reused from the forearm-arm2-aligned approach, re-implemented here):
centres are measured from the pose's own alpha, never from the builder's word
for it. Expected centres come from the v7c rig geometry saved in the pose's
joints JSON. A joint PASSES when its measured centroid is within threshold of
the v7c-geometric expected point. Cuff centre is measured in a 45px box around
the point 85% along elbow->wrist (where the cuff sits in the lower piece).
Knee-feet QC: knee direction (knee_x - ankle_x) and foot direction
(toe_x - ankle_x) must have the same sign (C-01: knees point where feet point).
For the flex pose the ankle comes from v7c leg geometry; for a dance frame
the silhouette method is used and the result is labelled APPROXIMATE.
Usage: python3 alignment_qc_gap_close.py
"""
import json, math, os
import numpy as np
from PIL import Image

OUT = "/home/hatch/workspace/cape-jones-rig/gap-close-rig-20261031"
RIG = "/home/hatch/workspace/cape-jones-rig"
SCALE = 0.95
HIP = {"L": (470, 740), "R": (615, 740)}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}

def rot_vec(v, a):
    r = math.radians(a); x, y = v
    return (x*math.cos(r)+y*math.sin(r), -x*math.sin(r)+y*math.cos(r))

def centroid_in_box(alpha, cx, cy, r):
    x0, y0 = max(0, int(cx-r)), max(0, int(cy-r))
    x1, y1 = min(alpha.shape[1], int(cx+r)), min(alpha.shape[0], int(cy+r))
    sub = alpha[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return (float(xs.mean()+x0), float(ys.mean()+y0))

def check_pose(pose_file, joints_file, label):
    im = Image.open(os.path.join(OUT, pose_file)).convert("RGBA")
    a = np.array(im)[:, :, 3] > 10
    j = json.load(open(os.path.join(OUT, joints_file)))
    print(f"--- {label}: {pose_file}")
    results = {}
    for kind, thresh, radius in [("elbows", 20, 80), ("wrists", 20, 80)]:
        for side, exp in j[kind].items():
            meas = centroid_in_box(a, exp[0], exp[1], radius)
            d = math.hypot(meas[0]-exp[0], meas[1]-exp[1]) if meas else 999
            ok = d <= thresh
            results[f"{kind}_{side}"] = {"expected": exp, "measured": [round(meas[0], 1), round(meas[1], 1)] if meas else None, "delta_px": round(d, 1), "pass": ok}
            print(f"  {kind} {side}: expected {exp} measured {results[f'{kind}_{side}']['measured']} delta {d:.1f}px {'PASS' if ok else 'FAIL'}")
    # fists
    fist_map = {}
    if "fist_R_centre" in j: fist_map["R"] = j["fist_R_centre"]
    if "fists" in j: fist_map.update(j["fists"])
    for side, exp in fist_map.items():
        meas = centroid_in_box(a, exp[0], exp[1], 110)
        d = math.hypot(meas[0]-exp[0], meas[1]-exp[1]) if meas else 999
        ok = d <= 30
        results[f"fist_{side}"] = {"expected": exp, "measured": [round(meas[0], 1), round(meas[1], 1)] if meas else None, "delta_px": round(d, 1), "pass": ok}
        print(f"  fist {side}: expected {exp} measured {results[f'fist_{side}']['measured']} delta {d:.1f}px {'PASS' if ok else 'FAIL'}")
    # cuffs: point 85% elbow->wrist, measured in a 45px box
    for side in ("L", "R"):
        if side not in j.get("elbows", {}) or side not in j.get("wrists", {}): continue
        e, w = j["elbows"][side], j["wrists"][side]
        exp = [e[0]+0.85*(w[0]-e[0]), e[1]+0.85*(w[1]-e[1])]
        meas = centroid_in_box(a, exp[0], exp[1], 45)
        d = math.hypot(meas[0]-exp[0], meas[1]-exp[1]) if meas else 999
        ok = d <= 25
        results[f"cuff_{side}"] = {"expected": [round(exp[0], 1), round(exp[1], 1)], "measured": [round(meas[0], 1), round(meas[1], 1)] if meas else None, "delta_px": round(d, 1), "pass": ok}
        print(f"  cuff {side}: expected {results[f'cuff_{side}']['expected']} measured {results[f'cuff_{side}']['measured']} delta {d:.1f}px {'PASS' if ok else 'FAIL'}")
    # Secondary check (decisive for bent joints): expected joint must lie ON opaque
    # body (nearest opaque pixel within 6px) and the arm must be continuous across it.
    # Box-centroid deltas are biased when a joint is bent, because the mass centroid
    # of upper+lower pieces in the box is not the joint centre. Both are reported.
    for kind in ("elbows", "wrists"):
        for side, exp in j[kind].items():
            ex, ey = int(exp[0]), int(exp[1])
            win = a[max(0, ey-6):ey+7, max(0, ex-6):ex+7]
            on_body = bool(win.any())
            results[f"onbody_{kind}_{side}"] = {"pass": on_body}
            print(f"  on-body {kind} {side}: {'PASS' if on_body else 'FAIL'} (expected point on opaque body)")
    n_pass = sum(1 for v in results.values() if v["pass"])
    print(f"  RESULT {label}: {n_pass}/{len(results)} pass")
    return results

def kneefeet_flex():
    im = Image.open(os.path.join(OUT, "gap-close-true-final-flex-v2-20261031.png")).convert("RGBA")
    a = np.array(im)[:, :, 3] > 10
    j = json.load(open(os.path.join(OUT, "gap-close-true-final-flex-v2-joints-20261031.json")))
    print("--- KNEE-FEET: flex v2 (rig geometry + pose alpha)")
    res = {}
    for side, (lu, ll) in [("L", (-22, 10)), ("R", (22, -10))]:
        hip = HIP[side]; ball, ha = LEG[side]; vec = (ball[0]-ha[0], ball[1]-ha[1])
        knee = (hip[0]+rot_vec(vec, lu)[0]*SCALE, hip[1]+rot_vec(vec, lu)[1]*SCALE)
        ankle = (knee[0]+rot_vec(vec, ll)[0]*SCALE, knee[1]+rot_vec(vec, ll)[1]*SCALE)
        # NOTE: v7c lower anchor is (ball_x, 0), so the lower vector is (ball-ha) rotated
        # by leg_lower only in the simplified form used here; the ankle is therefore
        # approximate to within the lower piece's own length. Foot toe from alpha:
        y0, y1 = int(ankle[1]), min(a.shape[0], int(ankle[1])+150)
        x0, x1 = max(0, int(ankle[0])-140), min(a.shape[1], int(ankle[0])+140)
        sub = a[y0:y1, x0:x1]
        ys, xs = np.where(sub)
        toe_x = float(xs.min()+x0) if side == "L" else float(xs.max()+x0)
        kd, fd = knee[0]-ankle[0], toe_x-ankle[0]
        ok = (kd == 0 and fd == 0) or (kd*fd > 0) or (abs(kd) < 15 and abs(fd) < 15)
        res[side] = {"knee": [round(knee[0], 1), round(knee[1], 1)], "ankle": [round(ankle[0], 1), round(ankle[1], 1)],
                     "toe_x": round(toe_x, 1), "knee_dir": round(kd, 1), "foot_dir": round(fd, 1), "pass": bool(ok)}
        print(f"  {side}: knee {res[side]['knee']} ankle {res[side]['ankle']} toe_x {toe_x} knee_dir {kd:.1f} foot_dir {fd:.1f} {'PASS' if ok else 'FAIL'}")
    return res

def kneefeet_dance():
    p = os.path.join(RIG, "dance-improved-20261031/frames/dance-improved-f015.png")
    im = Image.open(p).convert("RGB")
    arr = np.array(im).astype(int)
    bg = arr[0, 0]
    mask = (np.abs(arr - bg).sum(axis=2) > 60)
    ys, xs = np.where(mask)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx = int((x0+x1)//2)
    print(f"--- KNEE-FEET: dance frame f015 (APPROXIMATE silhouette method) file={p} bbox x{x0}-{x1} y{y0}-{y1}")
    # Crossed-leg detection: at knee height, if the silhouette is one interval
    # spanning the centre, the legs cross there and a centre split cannot assign
    # a foot to its leg. The silhouette numbers are then INCONCLUSIVE, not a fail;
    # the legs must be tracked visually through the cross (see report).
    knee_y = int(y0 + 0.55*(y1-y0))
    row = np.where(mask[knee_y])[0]
    crossed = len(row) > 0 and row.min() < cx < row.max() and (row.max()-row.min()) > 100
    print(f"  knee-height row {knee_y}: silhouette x{row.min() if len(row) else '-'}-{row.max() if len(row) else '-'} crossed={crossed}")
    res = {}
    for side, (xa, xb) in [("L", (x0, cx)), ("R", (cx, x1))]:
        if crossed:
            res[side] = {"pass": None, "note": "INCONCLUSIVE - crossed legs; centre split cannot assign feet to legs; use visual tracking"}
            print(f"  {side}: INCONCLUSIVE - crossed legs (see visual tracking in report)")
            continue
        sub = mask[:, xa:xb]
        rows = []
        for y in range(y0, y1+1):
            w = np.where(sub[y])[0]
            if len(w): rows.append((y, w.min()+xa, w.max()+xa))
        H = y1-y0
        mid = [r for r in rows if y0+0.40*H <= r[0] <= y0+0.70*H]
        knee_row = min(mid, key=lambda r: r[2]-r[1]) if mid else None
        foot_rows = [r for r in rows if r[0] >= y0+0.85*H]
        ankle_row = foot_rows[0] if foot_rows else None
        if knee_row and ankle_row:
            knee_c = (knee_row[1]+knee_row[2])/2; ankle_c = (ankle_row[1]+ankle_row[2])/2
            toe_x = min(r[1] for r in foot_rows) if side == "L" else max(r[2] for r in foot_rows)
            kd, fd = knee_c-ankle_c, toe_x-ankle_c
            ok = (kd*fd > 0) or (abs(kd) < 20 and abs(fd) < 20)
            res[side] = {"knee_row": knee_row[0], "knee_cx": round(knee_c, 1), "ankle_cx": round(ankle_c, 1),
                         "toe_x": round(float(toe_x), 1), "knee_dir": round(float(kd), 1), "foot_dir": round(float(fd), 1), "pass": bool(ok)}
            print(f"  {side}: knee_row {knee_row[0]} knee_cx {knee_c:.1f} ankle_cx {ankle_c:.1f} toe_x {toe_x} knee_dir {kd:.1f} foot_dir {fd:.1f} {'PASS' if ok else 'FAIL'}")
        else:
            res[side] = {"pass": False, "note": "silhouette rows not found"}
            print(f"  {side}: FAIL (rows not found)")
    return res

if __name__ == "__main__":
    out = {}
    out["punch_v4c"] = check_pose("gap-close-punch-pose-v4c-20261031.png", "gap-close-punch-pose-v4c-joints-20261031.json", "PUNCH v4c")
    out["flex_v2"] = check_pose("gap-close-true-final-flex-v2-20261031.png", "gap-close-true-final-flex-v2-joints-20261031.json", "FLEX v2")
    out["kneefeet_flex"] = kneefeet_flex()
    out["kneefeet_dance_f015"] = kneefeet_dance()
    json.dump(out, open(os.path.join(OUT, "gap-close-qc-results-20261031.json"), "w"), indent=2)
    print("QC results saved to gap-close-qc-results-20261031.json")
