#!/usr/bin/env python3
"""ARM-FRONT-SNAP FIX 20261101 — re-render successor-pose-dialects with snap ON.
Source: rig-chains-20261031/build_chains.py DIAL_KEYS, exact angles/head/holds.
Fix: per frame, sense_from_angles(cfg) — forearm vs Torso_Chest at 1100x1500,
snap = overlap > 1000px. Snapped side's WHOLE chain (upper+forearm+fist+cap)
is rendered after torso, before neck/head (chest snap: torso < arm < head),
using anatomy-fix-bundle figure2(). Original top keys are kept as face_top
(rendered after head, as originally). Non-snapped sides are unchanged.
Knee-feet: NO bundle exception here — feet follow original cfg, no mirror.
Original successor video and placeholder videos are untouched.
"""
import os, sys, math, json, csv, subprocess
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/rig-chains-20261031"))
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/anatomy-fix-bundle-20261101"))
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/arm-front-snap-auto-20261101"))
import build_chains as bc
from build_anatomy_fix import figure2, render2
from arm_front_snap_sensor import sense_from_angles
import numpy as np

R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(R, "arm-snap-last3-fix-20261101")
FR = os.path.join(OUT, "frames-snapped")
os.makedirs(FR, exist_ok=True)

def bottom_orig(cfg, head, top):
    vf = bc.video_frame(bc.render(cfg, head, top, 0, 0))
    a = np.asarray(vf.convert("RGB")).astype(int)
    sil = (np.abs(a - 128).sum(axis=2) > 40)
    ys, _ = np.where(sil)
    return int(ys.max())

keys = bc.DIAL_KEYS
# ground compensation, exactly as build_chains: dy from original render
for k in keys:
    target_h = k.get("target_h", -k["dy"] // 2)
    b0 = bottom_orig(k["cfg"], k["head"], k["top"])
    k["dy"] = 2 * ((652 - target_h) - b0)
    k["height_video_px"] = target_h

frames, meta = [], []
def add(cfg, head, face_top, dx, dy, note, frm, to, t, e, height=None):
    snap = sense_from_angles(cfg)
    chest = tuple(s for s in ("L", "R") if snap[s][0] and s not in face_top)
    frames.append(bc.video_frame(render2(cfg, head, chest, face_top, (), dx, dy)))
    meta.append({"frame": len(frames) - 1, "kind": note, "from": frm, "to": to,
                 "t": round(t, 2), "eased": round(e, 2), "dx_rig": dx, "dy_rig": dy,
                 "height_video_px": height if height is not None else -dy // 2,
                 "snap_L_px": snap["L"][1], "snap_R_px": snap["R"][1],
                 "snap_L": bool(snap["L"][0]), "snap_R": bool(snap["R"][0]),
                 "chest_top": ",".join(chest), "face_top": ",".join(face_top),
                 "arm_upper_L": cfg["arm_upper"]["L"], "arm_upper_R": cfg["arm_upper"]["R"],
                 "arm_lower_L": cfg["arm_lower"]["L"], "arm_lower_R": cfg["arm_lower"]["R"]})

def transition(a, b, n_inb=5):
    deltas = {s: abs(b["cfg"]["arm_upper"][s] - a["cfg"]["arm_upper"][s]) for s in ("L", "R")}
    big = max(deltas, key=deltas.get)
    for j in range(1, n_inb + 1):
        t = j / (n_inb + 1); e = bc.ease(t); cfg = bc.lerp_cfg(a["cfg"], b["cfg"], e)
        head = a["head"] + (b["head"] - a["head"]) * e
        face = tuple(sorted(set(a["top"]) | set(b["top"])))
        dx = int(a["dx"] + (b["dx"] - a["dx"]) * e); dy = int(a["dy"] + (b["dy"] - a["dy"]) * e); tag = "inbetween"
        if j == 3:
            cfg["arm_upper"][big] += 10 if b["cfg"]["arm_upper"][big] >= a["cfg"]["arm_upper"][big] else -10
            tag = "BREAKDOWN arc +10deg largest-moving arm upper"
        if j == 5:
            cfg["arm_lower"][big] += 8 if b["cfg"]["arm_lower"][big] >= a["cfg"]["arm_lower"][big] else -8
            tag = "BREAKDOWN follow-through +8deg that arm lower"
        h = a.get("height_video_px", 0) + (b.get("height_video_px", 0) - a.get("height_video_px", 0)) * e
        add(cfg, head, face, dx, dy, tag, a["name"], b["name"], t, e, height=int(round(h)))

def hold(k, note="KEY hold"):
    for _ in range(k["hold"]):
        add(k["cfg"], k["head"], k["top"], k["dx"], k["dy"], note, k["name"], k["name"], 0, 0, height=k.get("height_video_px", 0))

hold(keys[0])
for i in range(len(keys) - 1):
    transition(keys[i], keys[i + 1]); hold(keys[i + 1])
# overshoot arms only + settle + return, as build_chains
prev, last = keys[-2], keys[-1]
over = {g: dict(last["cfg"][g]) for g in last["cfg"]}
for g in ("arm_upper", "arm_lower"):
    for s in ("L", "R"):
        over[g][s] = prev["cfg"][g][s] + (last["cfg"][g][s] - prev["cfg"][g][s]) * 1.05
add(over, last["head"], last["top"], last["dx"], last["dy"], "OVERSHOOT 5% beyond key", prev["name"], last["name"], 1.05, 1.05, height=last.get("height_video_px", 0))
add(last["cfg"], last["head"], last["top"], last["dx"], last["dy"], "SETTLE back to key", last["name"], last["name"], 1.0, 1.0, height=last.get("height_video_px", 0))
transition(last, keys[0]); hold(keys[0])

with open(os.path.join(OUT, "successor-snapped-frames.txt"), "w") as fh:
    for i, f in enumerate(frames):
        f.save(os.path.join(FR, f"snapped-{i:03d}.jpg"), quality=92)
        fh.write(f"file '{FR}/snapped-{i:03d}.jpg'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", "24",
                "-i", os.path.join(OUT, "successor-snapped-frames.txt"), "-vf", "scale=1100:750",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                os.path.join(OUT, "successor-pose-dialects-ARM-SNAP-FIXED-20261101.mp4")], check=True)
with open(os.path.join(OUT, "successor-snapped-xsheet-20261101.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(meta[0].keys())); w.writeheader(); w.writerows(meta)
print("snapped successor", len(frames), f"{len(frames)/24:.2f}s",
      "snap_frames", sum(1 for m in meta if m["snap_L"] or m["snap_R"]))
for name in ("JoJo 02 fashion twist", "Stand 02 user figure only (stand figure omitted, labelled)", "JoJo 03 menacing lean"):
    rows = [m for m in meta if m["from"] == name and m["kind"] == "KEY hold"]
    if rows:
        print(name, "key frames", [r["frame"] for r in rows], "snap_L", rows[0]["snap_L"], rows[0]["snap_L_px"],
              "snap_R", rows[0]["snap_R"], rows[0]["snap_R_px"], "chest_top", rows[0]["chest_top"])
