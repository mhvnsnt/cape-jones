#!/usr/bin/env python3
"""Preset B arm-front-snap fix, Mars 2026-11-01 14:42 CST.
B = Foster's punch/walk structure, clean version:
  stand (1s, first frame of move) + move
  move = chain-punch re-cut frames 0-73 (74f) + chain-walk frames 0-65 (66f) = 140f
  total clean = 24 + 140 = 164f, 6.833333s, 1100x750, 24fps.
Flat-video re-layering CANNOT fix eaten arms (hidden pixels are gone), so
both chains are re-rendered from rig angles with the arm-front-snap sensor
ON, exactly as the A/C successor snap fix did:
  per frame, sense_from_angles(cfg) forearm-vs-Torso_Chest at 1100x1500,
  snap = overlap > 1000px; snapped side's WHOLE chain (upper+forearm+fist+cap)
  rendered after torso, before neck/head (torso < arm < head), via
  anatomy-fix-bundle figure2/render2. Face-top keys: none in punch/walk,
  so chest_top = snap sides. No foot mirror (universal knee-feet rule;
  the anatomy bundle's leg1-exception is NOT reused here). No other
  pose, timing, background, or sound change.
Ground compensation and frame generation replicate build_chains.build()
exactly: hold counts, 7 inbetween (punch) / 5 inbetween (walk),
breakdown +10deg upper at j=3, +8deg lower at j=5, punch overshoot 5%
arms-only + settle + return to apose, walk cycle (ends on contact A)
so no overshoot/return. Silhouette bottom is measured with render2
(layer order does not change the silhouette union, so dy matches the
original chains to within the render path).
"""
import os, sys, csv, json, subprocess
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/rig-chains-20261031"))
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/anatomy-fix-bundle-20261101"))
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/arm-front-snap-auto-20261101"))
import build_chains as bc
from build_anatomy_fix import render2
from arm_front_snap_sensor import sense_from_angles
import numpy as np

R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(R, "preset-b-arm-snap-20261101")
FR = os.path.join(OUT, "frames"); os.makedirs(FR, exist_ok=True)

def bottom_render2(cfg, head, chest_top, face_top):
    vf = bc.video_frame(render2(cfg, head, chest_top, face_top, (), 0, 0))
    a = np.asarray(vf.convert("RGB")).astype(int)
    sil = (np.abs(a - 128).sum(axis=2) > 40)
    ys, _ = np.where(sil)
    return int(ys.max())

def build_chain(name, keys, n_inb):
    # ground compensation, per key, using render2 silhouette bottom
    for k in keys:
        snap = sense_from_angles(k["cfg"])
        chest = tuple(s for s in ("L", "R") if snap[s][0] and s not in k["top"])
        target_h = k.get("target_h", -k["dy"] // 2)
        b0 = bottom_render2(k["cfg"], k["head"], chest, k["top"])
        k["dy"] = 2 * ((652 - target_h) - b0)
        k["height_video_px"] = target_h
    frames, meta = [], []
    def add(cfg, head, face_top, dx, dy, note, frm, to, t, e, height=None):
        snap = sense_from_angles(cfg)
        chest = tuple(s for s in ("L", "R") if snap[s][0] and s not in face_top)
        frames.append(bc.video_frame(render2(cfg, head, chest, face_top, (), dx, dy)))
        meta.append({"chain": name, "frame": len(frames) - 1, "kind": note, "from": frm, "to": to,
                     "t": round(t, 2), "eased": round(e, 2), "dx_rig": dx, "dy_rig": dy,
                     "height_video_px": height if height is not None else -dy // 2,
                     "snap_L": bool(snap["L"][0]), "snap_R": bool(snap["R"][0]),
                     "snap_L_px": snap["L"][1], "snap_R_px": snap["R"][1],
                     "chest_top": ",".join(chest), "face_top": ",".join(face_top),
                     "arm_upper_L": cfg["arm_upper"]["L"], "arm_upper_R": cfg["arm_upper"]["R"],
                     "arm_lower_L": cfg["arm_lower"]["L"], "arm_lower_R": cfg["arm_lower"]["R"],
                     "leg_upper_L": cfg["leg_upper"]["L"], "leg_upper_R": cfg["leg_upper"]["R"],
                     "leg_lower_L": cfg["leg_lower"]["L"], "leg_lower_R": cfg["leg_lower"]["R"]})
    def transition(a, b):
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
    cycle = keys[-1]["name"] == keys[0]["name"] and len(keys) > 1
    if not cycle:
        prev, last = keys[-2], keys[-1]
        over = {g: dict(last["cfg"][g]) for g in last["cfg"]}
        for g in ("arm_upper", "arm_lower"):
            for s in ("L", "R"):
                over[g][s] = prev["cfg"][g][s] + (last["cfg"][g][s] - prev["cfg"][g][s]) * 1.05
        add(over, last["head"], last["top"], last["dx"], last["dy"], "OVERSHOOT 5% beyond key", prev["name"], last["name"], 1.05, 1.05, height=last.get("height_video_px", 0))
        add(last["cfg"], last["head"], last["top"], last["dx"], last["dy"], "SETTLE back to key", last["name"], last["name"], 1.0, 1.0, height=last.get("height_video_px", 0))
        transition(last, keys[0]); hold(keys[0])
    return frames, meta

punch_frames, punch_meta = build_chain("punch", [dict(k, cfg={g: dict(k["cfg"][g]) for g in k["cfg"]}) for k in bc.PUNCH_KEYS], 7)
walk_frames, walk_meta = build_chain("walk", [dict(k, cfg={g: dict(k["cfg"][g]) for g in k["cfg"]}) for k in bc.WALK_KEYS], 5)
print(f"punch {len(punch_frames)} frames, snap {sum(1 for m in punch_meta if m['snap_L'] or m['snap_R'])}")
print(f"walk {len(walk_frames)} frames, snap {sum(1 for m in walk_meta if m['snap_L'] or m['snap_R'])}")
assert len(punch_frames) == 75 and len(walk_frames) == 67, (len(punch_frames), len(walk_frames))

# B move, exactly as the clean build: punch frames 0-73 + walk frames 0-65
move = punch_frames[:74] + walk_frames[:66]
move_meta = []
for i, m in enumerate(punch_meta[:74]):
    d = dict(m); d["segment"] = "punch"; d["segment_frame"] = m["frame"]; move_meta.append(d)
for i, m in enumerate(walk_meta[:66]):
    d = dict(m); d["segment"] = "walk"; d["segment_frame"] = m["frame"]; move_meta.append(d)
assert len(move) == 140

# clean build: 1s frozen stand (first move frame) + move, same wav, faststart
def save_frames(frames, prefix):
    paths = []
    for i, f in enumerate(frames):
        p = os.path.join(FR, f"{prefix}-{i:03d}.jpg"); f.save(p, quality=92); paths.append(p)
    return paths
stand_frame = move[0]
stand_paths = save_frames([stand_frame] * 24, "stand")
move_paths = save_frames(move, "move")
all_paths = stand_paths + move_paths
with open(os.path.join(OUT, "concat.txt"), "w") as fh:
    for p in all_paths: fh.write(f"file '{p}'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", "24",
                "-i", os.path.join(OUT, "concat.txt"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                os.path.join(OUT, "video-noaudio.mp4")], check=True)
WAV = os.path.join(R, "clean-shippable-animations-20261101", "B-FOSTERS-STRUCTURE-20261101.wav")
OUTMP4 = os.path.join(OUT, "B-FOSTERS-STRUCTURE-ARM-SNAP-FIXED-CLEAN-20261101.mp4")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(OUT, "video-noaudio.mp4"), "-i", WAV,
                "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest", "-movflags", "+faststart", OUTMP4], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", OUTMP4, "-vf",
                "fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse",
                OUTMP4.replace(".mp4", ".gif")], check=True)

# full clean-B xsheet: output frame = stand 0-23 (apose, no snap) + move
rows = []
for i in range(24):
    rows.append({"output_frame": i, "output_time_s": round(i / 24, 4), "segment": "stand", "segment_frame": 0,
                 "kind": "frozen stand, first move frame", "from": "apose", "to": "apose",
                 "snap_L": False, "snap_R": False, "snap_L_px": 0, "snap_R_px": 0, "chest_top": "", "face_top": "",
                 "arm_upper_L": 0, "arm_upper_R": 0, "arm_lower_L": 0, "arm_lower_R": 0})
for j, m in enumerate(move_meta):
    rows.append({"output_frame": 24 + j, "output_time_s": round((24 + j) / 24, 4), "segment": m["segment"],
                 "segment_frame": m["segment_frame"], "kind": m["kind"], "from": m["from"], "to": m["to"],
                 "snap_L": m["snap_L"], "snap_R": m["snap_R"], "snap_L_px": m["snap_L_px"], "snap_R_px": m["snap_R_px"],
                 "chest_top": m["chest_top"], "face_top": m["face_top"],
                 "arm_upper_L": m["arm_upper_L"], "arm_upper_R": m["arm_upper_R"],
                 "arm_lower_L": m["arm_lower_L"], "arm_lower_R": m["arm_lower_R"]})
with open(os.path.join(OUT, "B-ARM-SNAP-XSHEET-20261101.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"final {len(rows)} frames, snap output frames {sum(1 for r in rows if r['snap_L'] or r['snap_R'])}")
print(f"punch segment snap {sum(1 for r in rows if r['segment']=='punch' and (r['snap_L'] or r['snap_R']))}/74")
print(f"walk segment snap {sum(1 for r in rows if r['segment']=='walk' and (r['snap_L'] or r['snap_R']))}/66")
print("built", OUTMP4)
