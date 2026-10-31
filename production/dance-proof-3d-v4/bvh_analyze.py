"""BVH loop analyzer: FK-sample CMU BVH files, score 96-frame (24fps) windows
for loopability (seam distance, root drift) and full-body articulation ranges.
Usage: python3 bvh_analyze.py file.bvh [file2.bvh ...]
"""
import sys, math
import numpy as np

def parse_bvh(path):
    text = open(path).read().split()
    toks = iter(range(len(text)))
    raw = text
    idx = [0]
    def nxt():
        t = raw[idx[0]]; idx[0] += 1; return t
    joints = []  # dict name,parent,offset,channels[]
    stack = []
    root = None
    def parse_joint(parent):
        name = nxt()
        j = {"name": name, "parent": parent, "offset": np.zeros(3), "channels": [], "chan_idx": 0, "children": []}
        joints.append(j)
        assert nxt() == "{"
        while True:
            t = nxt()
            if t == "OFFSET":
                j["offset"] = np.array([float(nxt()), float(nxt()), float(nxt())])
            elif t == "CHANNELS":
                n = int(nxt())
                j["channels"] = [nxt() for _ in range(n)]
            elif t == "JOINT":
                parse_joint(j)
            elif t == "End":
                assert nxt() == "Site"
                assert nxt() == "{"
                while nxt() != "}":
                    pass
                # consume offset line tokens were skipped above except braces/offsets numbers
            elif t == "}":
                break
        return j
    assert nxt() == "HIERARCHY"
    assert nxt() == "ROOT"
    root = parse_joint(None)
    assert nxt() == "MOTION"
    assert nxt() == "Frames:"
    nframes = int(nxt())
    assert nxt() == "Frame"
    assert nxt() == "Time:"
    ftime = float(nxt())
    total_ch = sum(len(j["channels"]) for j in joints)
    c = 0
    for j in joints:
        j["chan_idx"] = c; c += len(j["channels"])
    data = np.array([float(x) for x in raw[idx[0]:]], dtype=np.float64)
    data = data[: nframes * total_ch].reshape(nframes, total_ch)
    return joints, root, data, ftime

def rotmat(axis, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    if axis == "X": return np.array([[1,0,0],[0,c,-s],[0,s,c]])
    if axis == "Y": return np.array([[c,0,s],[0,1,0],[-s,0,c]])
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def fk_positions(joints, data, frame):
    """Return dict name->world pos for one frame (BVH native units)."""
    pos = {}
    mats = {}
    for j in joints:
        vals = data[frame, j["chan_idx"]: j["chan_idx"] + len(j["channels"])]
        off = j["offset"].copy()
        R = np.eye(3)
        vi = 0
        for ch in j["channels"]:
            if ch == "Xposition": off[0] = vals[vi]
            elif ch == "Yposition": off[1] = vals[vi]
            elif ch == "Zposition": off[2] = vals[vi]
            elif ch in ("Xrotation","Yrotation","Zrotation"):
                R = R @ rotmat(ch[0], vals[vi])
            vi += 1
        if j["parent"] is None:
            world_t = off; world_R = R
        else:
            p = j["parent"]["name"]
            world_R = mats[p] @ R
            world_t = pos[p] + mats[p] @ off
        pos[j["name"]] = world_t; mats[j["name"]] = world_R
    return pos

def ang(p, a, b):
    """angle at p between a-p and b-p, degrees"""
    v1, v2 = a - p, b - p
    n = np.linalg.norm(v1) * np.linalg.norm(v2)
    if n == 0: return 0.0
    return math.degrees(math.acos(np.clip(np.dot(v1, v2) / n, -1, 1)))

def analyze(path):
    joints, root, data, ftime = parse_bvh(path)
    names = [j["name"] for j in joints]
    src_fps = 1.0 / ftime
    step = max(1, round(src_fps / 24.0))
    out_frames = list(range(0, len(data), step))
    P = []
    for f in out_frames:
        P.append(fk_positions(joints, data, f))
    def g(p, n): return p.get(n)
    H = None
    if "Head" in names and "LeftFoot" in names:
        H = float(np.median([P[i]["Head"][1] - min(P[i]["LeftFoot"][1], P[i]["RightFoot"][1]) for i in range(0, len(P), 25)]))
    print(f"\n== {path} joints={len(names)} srcfps={src_fps:.1f} outframes={len(P)} height~{H}")
    print("joints:", ", ".join(names))
    W = 96
    results = []
    for s in range(0, len(P) - W - 1):
        seg = P[s:s + W]
        hips = np.array([p["Hips"] for p in seg])
        drift = np.linalg.norm(hips[-1][:3:2] - hips[0][:3:2]) if hips.shape[1] == 3 else 0
        # BVH: Y up in file coords (positions are x,y,z with y vertical in CMU conversion? verify via head-hips)
        xz = np.stack([hips[:, 0], hips[:, 2]], axis=1)
        drift = np.linalg.norm(xz[-1] - xz[0])
        spread = np.linalg.norm(xz.max(axis=0) - xz.min(axis=0))
        seam = np.mean([np.linalg.norm(seg[-1][n] - seg[0][n]) for n in names if n in seg[0]])
        rng = {}
        for (jname, a, b) in [("elbowL","LeftArm","LeftHand"),("elbowR","RightArm","RightHand"),
                              ("kneeL","LeftLeg","LeftFoot"),("kneeR","RightLeg","RightFoot"),
                              ("shoulderL","LeftArm","LeftForeArm"),("shoulderR","RightArm","RightForeArm")]:
            if a in names and b in names:
                if jname.startswith("elbow"):
                    vals = [ang(p[jname.replace("elbow","Left" if jname=="elbowL" else "Right")+"ForeArm"] if False else seg[i][a.replace("Arm","ForeArm") if False else a], seg[i][a], seg[i][b]) for i in range(W)]
                rng[jname] = 0
        # joint angle ranges via positions: elbow angle at ForeArm between Arm and Hand
        def arange(joint, pa, pb):
            vals = [ang(seg[i][joint], seg[i][pa], seg[i][pb]) for i in range(W)]
            return max(vals) - min(vals)
        r = {}
        try:
            r["elbowL"] = arange("LeftForeArm", "LeftArm", "LeftHand")
            r["elbowR"] = arange("RightForeArm", "RightArm", "RightHand")
            r["kneeL"] = arange("LeftLeg", "LeftUpLeg", "LeftFoot")
            r["kneeR"] = arange("RightLeg", "RightUpLeg", "RightFoot")
            r["shoulderL"] = arange("LeftArm", "Spine1", "LeftForeArm")
            r["shoulderR"] = arange("RightArm", "Spine1", "RightForeArm")
            spine = [ang(seg[i]["Spine"], seg[i]["Hips"], seg[i]["Spine1"]) for i in range(W)]
            r["spine"] = max(spine) - min(spine)
            footL = np.array([p["LeftFoot"] for p in seg]); footR = np.array([p["RightFoot"] for p in seg])
            r["footstep"] = float(footL[:, 1].max() - footL[:, 1].min() + footR[:, 1].max() - footR[:, 1].min())
        except KeyError as e:
            print("missing joint", e); return
        score = sum(r.values())
        results.append((score, -seam, -spread, s, drift, spread, seam, r))
    results.sort(reverse=True)
    for score, _, _, s, drift, spread, seam, r in results[:5]:
        print(f" start_out={s} (src {s*step}) score={score:.0f} driftXZ={drift:.1f} spreadXZ={spread:.1f} seam={seam:.2f} ranges=" +
              " ".join(f"{k}={v:.0f}" for k, v in r.items()))

if __name__ == "__main__":
    for p in sys.argv[1:]:
        analyze(p)
