"""Cape Jones dance v4 - joint-checklist measurements on the solved loop.
Opens scene_v4.blend, activates the DanceV4Loop action directly, samples
DEF-bone world geometry across the 96-frame loop, writes measurements.json.
"""
import bpy, math, os, json, time
import numpy as np
from mathutils import Vector

WORK = "/home/hatch/workspace/_cj_v4_build"
LOOP = 96
bpy.ops.wm.open_mainfile(filepath=os.path.join(WORK, "scene_v4.blend"))
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
act = bpy.data.actions["DanceV4Loop"]
if not rig.animation_data:
    rig.animation_data_create()
rig.animation_data.action = act

def bpos(name):
    pb = RPB[name]
    return rig.matrix_world @ pb.head, rig.matrix_world @ pb.tail
def bang(a, b, c):
    v1, v2 = a - b, c - b
    if v1.length < 1e-9 or v2.length < 1e-9:
        return 0.0
    return math.degrees(v1.angle(v2))
def qrange(name, samples):
    # scale-immune: swing of the bone's direction vector (DEF matrices carry
    # IK-stretch scale, which poisons quaternion extraction)
    dirs = []
    for f in samples:
        sc.frame_set(f); bpy.context.view_layer.update()
        h, t = bpos(name)
        dirs.append((t - h).normalized())
    mx = 0.0
    for i in range(len(dirs)):
        for j in range(i + 1, len(dirs)):
            mx = max(mx, math.degrees(dirs[i].angle(dirs[j])))
    return mx

M = {}
samples = list(range(1, LOOP + 1, 2))
series = {k: [] for k in ("elbowL", "elbowR", "kneeL", "kneeR", "ankleL", "ankleR",
                          "finger", "armdirL", "armdirR", "pelvis", "footL", "footR", "capetip")}
for f in samples:
    sc.frame_set(f); bpy.context.view_layer.update()
    S = lambda n: bpos(n)[0]
    series["elbowL"].append(bang(S("DEF-upper_arm.L"), S("DEF-forearm.L"), S("DEF-hand.L")))
    series["elbowR"].append(bang(S("DEF-upper_arm.R"), S("DEF-forearm.R"), S("DEF-hand.R")))
    series["kneeL"].append(bang(S("DEF-thigh.L"), S("DEF-shin.L"), S("DEF-foot.L")))
    series["kneeR"].append(bang(S("DEF-thigh.R"), S("DEF-shin.R"), S("DEF-foot.R")))
    series["ankleL"].append(bang(S("DEF-shin.L"), S("DEF-foot.L"), S("DEF-toe.L")))
    series["ankleR"].append(bang(S("DEF-shin.R"), S("DEF-foot.R"), S("DEF-toe.R")))
    series["finger"].append(bang(S("DEF-f_middle.01.L"), S("DEF-f_middle.02.L"), S("DEF-f_middle.03.L")))
    for nm, key_ in (("DEF-upper_arm.L", "armdirL"), ("DEF-upper_arm.R", "armdirR")):
        h, t = bpos(nm)
        d = t - h
        s = max(-1.0, min(1.0, d.z / max(d.length, 1e-9)))
        series[key_].append(math.degrees(math.asin(s)))
    series["pelvis"].append(S("DEF-spine"))
    series["footL"].append(S("DEF-foot.L")); series["footR"].append(S("DEF-foot.R"))
    series["capetip"].append(bpos("DEF-cape.005")[1])
for k in ("elbowL", "elbowR", "kneeL", "kneeR", "ankleL", "ankleR", "finger"):
    v = series[k]
    M[k] = {"min": round(min(v), 1), "max": round(max(v), 1), "range": round(max(v) - min(v), 1)}
for k in ("armdirL", "armdirR"):
    v = series[k]
    M[k] = {"min_deg_from_horizontal": round(min(v), 1), "max_deg_from_horizontal": round(max(v), 1),
            "pct_frames_below_horizontal_15deg": round(100.0 * sum(1 for x in v if x < -15) / len(v), 1)}
M["spine_bend_quat_range_deg"] = round(qrange("DEF-spine.002", samples), 1)
M["chest_quat_range_deg"] = round(qrange("DEF-spine.003", samples), 1)
M["neck_quat_range_deg"] = round(qrange("DEF-spine.005", samples), 1)
M["head_quat_range_deg"] = round(qrange("DEF-spine.006", samples), 1)
M["wrist_quat_range_deg_L"] = round(qrange("DEF-hand.L", samples), 1)
M["wrist_quat_range_deg_R"] = round(qrange("DEF-hand.R", samples), 1)
pv = np.array([list(v) for v in series["pelvis"]])
M["pelvis_travel_m"] = {"x": round(float(pv[:, 0].max() - pv[:, 0].min()), 3),
                        "z_bounce": round(float(pv[:, 2].max() - pv[:, 2].min()), 3)}
for k in ("footL", "footR"):
    a = np.array([list(v) for v in series[k]])
    M[k + "_travel_m"] = {"x": round(float(a[:, 0].max() - a[:, 0].min()), 3),
                          "z_lift": round(float(a[:, 2].max() - a[:, 2].min()), 3)}
ct = np.array([list(v) for v in series["capetip"]])
M["cape_tip_travel_m"] = {ax: round(float(ct[:, i].max() - ct[:, i].min()), 3) for i, ax in enumerate("xyz")}
with open(os.path.join(WORK, "measurements.json"), "w") as fh:
    json.dump(M, fh, indent=1)
print("MEASUREMENTS", json.dumps(M))
print("MEASURE_DONE")
