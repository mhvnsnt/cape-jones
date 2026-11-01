#!/usr/bin/env python3
"""Regenerate B xsheet from rig-angle sequence + sensor only.
Rendering already done by build_b_snap.py; this reproduces its meta
(frame order, holds, transitions, breakdowns, overshoot) without
re-rendering, so a CSV writer bug does not force a full re-render."""
import os, sys, csv
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/rig-chains-20261031"))
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/arm-front-snap-auto-20261101"))
import build_chains as bc
from arm_front_snap_sensor import sense_from_angles

def gen(keys, n_inb):
    frames = []
    def hold(k):
        for _ in range(k["hold"]):
            frames.append((dict(k["cfg"]), k["name"], "KEY hold", k["name"], k["name"]))
    def transition(a, b):
        deltas = {s: abs(b["cfg"]["arm_upper"][s] - a["cfg"]["arm_upper"][s]) for s in ("L", "R")}
        big = max(deltas, key=deltas.get)
        for j in range(1, n_inb + 1):
            t = j / (n_inb + 1); e = bc.ease(t); cfg = bc.lerp_cfg(a["cfg"], b["cfg"], e)
            tag = "inbetween"
            if j == 3:
                cfg["arm_upper"][big] += 10 if b["cfg"]["arm_upper"][big] >= a["cfg"]["arm_upper"][big] else -10
                tag = "BREAKDOWN arc +10deg largest-moving arm upper"
            if j == 5:
                cfg["arm_lower"][big] += 8 if b["cfg"]["arm_lower"][big] >= a["cfg"]["arm_lower"][big] else -8
                tag = "BREAKDOWN follow-through +8deg that arm lower"
            frames.append((cfg, f"{a['name']}->{b['name']}", tag, a["name"], b["name"]))
    hold(keys[0])
    for i in range(len(keys) - 1):
        transition(keys[i], keys[i + 1]); hold(keys[i + 1])
    cycle = keys[-1]["name"] == keys[0]["name"] and len(keys) > 1
    if not cycle:
        prev, last = keys[-2], keys[-1]
        over = {g: dict(last["cfg"][g]) for g in last["cfg"]}
        for g in ("arm_upper", "arm_lower"):
            for s in ("L", "R"):
                over[g][s] = prev["cfg"][g][s] + (last["cfg"][g][s] - prev["cfg"][g][s]) * 1.05
        frames.append((over, "OVERSHOOT", "OVERSHOOT 5% beyond key", prev["name"], last["name"]))
        frames.append((dict(last["cfg"]), "SETTLE", "SETTLE back to key", last["name"], last["name"]))
        transition(last, keys[0]); hold(keys[0])
    out = []
    for i, (cfg, frm, tag, f, t) in enumerate(frames):
        s = sense_from_angles(cfg)
        chest = tuple(x for x in ("L", "R") if s[x][0])
        out.append({"frame": i, "kind": tag, "from": f, "to": t, "snap_L": bool(s["L"][0]), "snap_R": bool(s["R"][0]),
                    "snap_L_px": s["L"][1], "snap_R_px": s["R"][1], "chest_top": ",".join(chest), "face_top": "",
                    "arm_upper_L": cfg["arm_upper"]["L"], "arm_upper_R": cfg["arm_upper"]["R"],
                    "arm_lower_L": cfg["arm_lower"]["L"], "arm_lower_R": cfg["arm_lower"]["R"]})
    return out

punch = gen(bc.PUNCH_KEYS, 7)
walk = gen(bc.WALK_KEYS, 5)
print("punch", len(punch), "snap", sum(1 for m in punch if m["snap_L"] or m["snap_R"]))
print("walk", len(walk), "snap", sum(1 for m in walk if m["snap_L"] or m["snap_R"]))
assert len(punch) == 75 and len(walk) == 67
rows = []
for i in range(24):
    rows.append({"output_frame": i, "output_time_s": round(i / 24, 4), "segment": "stand", "segment_frame": 0,
                 "kind": "frozen stand, first move frame", "from": "apose", "to": "apose",
                 "snap_L": False, "snap_R": False, "snap_L_px": 0, "snap_R_px": 0, "chest_top": "", "face_top": "",
                 "arm_upper_L": 0, "arm_upper_R": 0, "arm_lower_L": 0, "arm_lower_R": 0})
for seg, meta in (("punch", punch[:74]), ("walk", walk[:66])):
    for m in meta:
        rows.append({"output_frame": 24 + len([r for r in rows if r["segment"] in ("punch", "walk")]),
                     "output_time_s": 0, "segment": seg, "segment_frame": m["frame"], "kind": m["kind"],
                     "from": m["from"], "to": m["to"], "snap_L": m["snap_L"], "snap_R": m["snap_R"],
                     "snap_L_px": m["snap_L_px"], "snap_R_px": m["snap_R_px"], "chest_top": m["chest_top"],
                     "face_top": m["face_top"], "arm_upper_L": m["arm_upper_L"], "arm_upper_R": m["arm_upper_R"],
                     "arm_lower_L": m["arm_lower_L"], "arm_lower_R": m["arm_lower_R"]})
for r in rows: r["output_time_s"] = round(r["output_frame"] / 24, 4)
out = os.path.expanduser("~/workspace/cape-jones-rig/preset-b-arm-snap-20261101/B-ARM-SNAP-XSHEET-20261101.csv")
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("rows", len(rows), "snap output", sum(1 for r in rows if r["snap_L"] or r["snap_R"]),
      "punch seg snap", sum(1 for r in rows if r["segment"] == "punch" and (r["snap_L"] or r["snap_R"])),
      "walk seg snap", sum(1 for r in rows if r["segment"] == "walk" and (r["snap_L"] or r["snap_R"])))
