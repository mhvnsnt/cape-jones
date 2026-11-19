"""Scan pulled CMU BVH clips for the best FRONT-FACING loop window.
Uses bvh_analyze.py's parser + FK. Facing yaw in Blender terms:
yaw = atan2(f.x, f.z) over file-space toe-ankle vector f (calibration:
61_03 frame 1250 -> about -86 deg, frame 1070 -> about +168 deg).
Window = 476 source frames (96 out @ step 5). Score rewards elbow/knee/
shoulder joint-angle travel and penalizes |yaw| deviation from front and
root travel (in-one-spot). Also reports seam distance like the first pass.
"""
import math, os, sys
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("ba", "/home/hatch/workspace/_cj_v4_assets/bvh_analyze.py")
ba = importlib.util.module_from_spec(spec)
import types
# prevent ba's __main__ from running
ba.__name__ = "ba"
spec.loader.exec_module(ba)

BVH_DIR = "/home/hatch/workspace/_cj_v4_assets/bvh"
WIN = 476
STEP = 5

def facing_yaw(pos):
    d = np.zeros(3)
    for a, t in (("LeftFoot", "LeftToeBase"), ("RightFoot", "RightToeBase")):
        d += pos[t] - pos[a]
    return math.degrees(math.atan2(d[0], d[2]))

def scan(path):
    joints, root, data, ftime = ba.parse_bvh(path)
    n = data.shape[0]
    idx = {j["name"]: ji for ji, j in enumerate(joints)}
    # per-frame positions for the joints we need (every 5th frame is enough)
    frames = list(range(0, n, STEP))
    P = {}
    yaw = {}
    for f in frames:
        pos = ba.fk_positions(joints, data, f)
        P[f] = pos
        yaw[f] = facing_yaw(pos)
    def ang_at(f, a, b, c):
        return ba.ang(P[f][b], P[f][a], P[f][c])
    best = []
    starts = list(range(0, n - WIN, STEP))
    for s in starts:
        e = s + WIN
        fs = [f for f in frames if s <= f < e]
        if len(fs) < 90:
            continue
        yaws = np.array([yaw[f] for f in fs])
        med_yaw = float(np.median(yaws))
        front_frac = float((np.abs(yaws) < 40).mean())
        if front_frac < 0.55:
            continue
        def rng(a, b, c):
            v = [ang_at(f, a, b, c) for f in fs]
            return max(v) - min(v)
        act = (rng("LeftArm", "LeftForeArm", "LeftHand") + rng("RightArm", "RightForeArm", "RightHand")
               + rng("LeftUpLeg", "LeftLeg", "LeftFoot") + rng("RightUpLeg", "RightLeg", "RightFoot")
               + rng("LeftArm", "LeftShoulder", "LeftHand") if "LeftShoulder" in idx else 0)
        hips = np.array([P[f]["Hips"] for f in fs])
        spread = float(hips[:, 0].max() - hips[:, 0].min() + hips[:, 2].max() - hips[:, 2].min())
        # seam: pose distance between window ends (joint pos L2 over key joints)
        keys = ["Hips", "LeftHand", "RightHand", "LeftFoot", "RightFoot", "Head"]
        seam = float(np.mean([np.linalg.norm(P[fs[0]][k2] - P[fs[-1]][k2]) for k2 in keys]))
        score = act - spread * 1.5 - seam * 2.0
        best.append((score, s, med_yaw, front_frac, act, spread, seam))
    best.sort(reverse=True)
    return best[:3], n

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "calib":
        joints, root, data, ftime = ba.parse_bvh(os.path.join(BVH_DIR, "61_03.bvh"))
        for f in (1070, 1250):
            pos = ba.fk_positions(joints, data, f)
            print("frame", f, "yaw", round(facing_yaw(pos), 1))
        sys.exit(0)
    for fn in sorted(os.listdir(BVH_DIR)):
        if not fn.endswith(".bvh"):
            continue
        try:
            top, n = scan(os.path.join(BVH_DIR, fn))
        except Exception as e:
            print(fn, "ERROR", e)
            continue
        print(f"== {fn} frames={n}")
        for score, s, my, ff, act, spread, seam in top:
            print(f"   start={s} score={score:.0f} med_yaw={my:.0f} front_frac={ff:.2f} activity={act:.0f} root_spread={spread:.1f} seam={seam:.2f}")
