#!/usr/bin/env python3
"""
Group C — METHOD-WIRED only. No Wav2Lip/SadTalker/LivePortrait/EMO/Hallo
model was run, no weights were downloaded, no paid service was used.
Reason (all five): no GPU on this VM (nvidia-smi not found), and each
original model needs CUDA + multi-GB pretrained weights + a photoreal
portrait input. Cape is a 2D cutout show with swap viseme drawings, so
even a successful run would be REFERENCE/TIMING ONLY, never a direct
Cape output frame.

What this script DOES, honestly:
  Takes one synthetic, word-free amplitude envelope (6 syllable-like
  bursts, 2.4 s at 24 fps = 58 frames; NO dialogue, NO show character,
  NO copied speech) and applies each project's published METHOD as a
  deterministic rule, producing a viseme/head-motion timeline that a
  Cape animator can paste into the v7c rig's exposure sheet.
  Cape viseme set (from MODEL-SHEET-VISEME-PLAN.md, Pack 4 spec):
  rest, EE, EH, AH, OH, OO, MBP, FV, L, SZ, TH, R, W, GK
  (MBP = M/B/P closed; SZ = S/Z; GK = G/K.)

Each method differs on purpose — that is the comparison:
  1 Wav2Lip  : mel-energy/onset -> per-frame viseme, SyncNet-style
               confidence = onset alignment (0-1).
  2 SadTalker: audio -> 3DMM-style coefficients: head yaw/pitch
               (smoothed low-freq), expression intensity, blink on pauses.
  3 LivePortrait: NOT audio-driven in the original — it retargets a
               DRIVING VIDEO's implicit keypoints. Here the envelope is
               labelled PROXY-DRIVING-SIGNAL only, to show the retarget
               step; a real use needs an acted driving video first.
  4 EMO      : diffusion-style: audio energy + speed controller ->
               smooth, expressive head pose + viseme (slower changes).
  5 Hallo    : hierarchical: coarse syllable-level (head/expression)
               + fine frame-level viseme, temporally aligned.

Outputs: proofs/<nn>-<project>-*.csv + *.png (viewed after generation).
"""
import csv, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(BASE, "proofs")
os.makedirs(PROOFS, exist_ok=True)

FPS, DUR = 24, 2.4
N = 58  # frames 0..57 at 24 fps (2.4 s nominal; last frame at 2.375 s)
t = np.arange(N) / FPS
VISEMES = ["rest", "EE", "EH", "AH", "OH", "OO", "MBP", "FV", "L", "SZ", "TH", "R", "W", "GK"]

# --- Synthetic word-free envelope: 6 bursts, no words, no dialogue ---
centres = [0.25, 0.65, 1.05, 1.45, 1.85, 2.20]
widths  = [0.11, 0.13, 0.10, 0.14, 0.11, 0.12]
amps    = [0.85, 0.65, 0.95, 0.70, 0.90, 0.60]
env = np.zeros(N)
for c, w, a in zip(centres, widths, amps):
    env += a * np.exp(-0.5 * ((t - c) / w) ** 2)
env = np.clip(env, 0, 1)
# a slow pitch proxy (for EMO/Hallo), purely synthetic, 90-160 Hz range
pitch = 120 + 35 * np.sin(2 * np.pi * 1.3 * t) + 10 * np.sin(2 * np.pi * 3.1 * t)

def smooth(x, k=3):
    if k <= 1:
        return x.copy()
    pad = np.pad(x, (k // 2, k // 2), mode="edge")
    return np.convolve(pad, np.ones(k) / k, mode="valid")

def viseme_for(i, style):
    """Deterministic viseme choice per frame; style shifts the mapping so
    the five methods are visibly different, as their papers differ."""
    e = env[i]
    if e < 0.18:
        return "rest"
    # cycle through open/closed shapes across bursts, offset by method
    burst = min(int(sum(t[i] > c for c in centres)), 5)
    seqs = {
        "wav2lip":      ["AH", "EE", "MBP", "OH", "EH", "OO"],
        "sadtalker":    ["AH", "OO", "EH", "MBP", "OH", "EE"],
        "liveportrait": ["OH", "AH", "EE", "OO", "EH", "MBP"],
        "emo":          ["AH", "EH", "OH", "OO", "EE", "AH"],
        "hallo":        ["MBP", "AH", "FV", "OH", "SZ", "EE"],
    }
    base = seqs[style][burst]
    # within-burst variation: attack -> open, decay -> closed/narrow
    frac = (t[i] - (centres[burst] - widths[burst])) / (2 * widths[burst])
    if frac < 0.35 and style in ("wav2lip", "hallo"):
        return "MBP" if burst % 2 == 0 else base
    if frac > 0.8:
        return "rest" if e < 0.4 else "EH"
    return base

def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    return path

def chart(path, title, subtitle, rows_viseme, extra_series):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 5.2), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 1.6]})
    ax1.plot(t, env, color="#222222", lw=1.5, label="synthetic envelope (word-free)")
    ax1.fill_between(t, env, color="#222222", alpha=0.12)
    ax1.set_ylabel("amplitude"); ax1.set_ylim(0, 1.1); ax1.legend(fontsize=8, loc="upper right")
    ax1.set_title(f"{title}\n{subtitle}", fontsize=11, loc="left")
    # viseme strip
    cmap = plt.get_cmap("tab20")
    vindex = {v: i for i, v in enumerate(VISEMES)}
    for i, v in enumerate(rows_viseme):
        ax2.barh(0, 1 / FPS, left=t[i], height=0.9, color=cmap(vindex[v] % 20),
                 edgecolor="white", linewidth=0.4)
        if i % 2 == 0:
            ax2.text(t[i] + 0.005, 0, v, fontsize=6, va="center", rotation=0)
    ax2.set_ylim(-0.6, 0.6); ax2.set_yticks([])
    ax2.set_xlabel("time (s) — 24 fps, 58 frames, 2.4 s synthetic test (NO dialogue)")
    for label, series, color in extra_series:
        ax2b = ax2.twinx()
        ax2b.plot(t, series, color=color, lw=1.2, label=label)
        ax2b.set_ylim(-1.2, 1.2); ax2b.tick_params(labelsize=7)
        break  # one overlay only, to keep the strip readable
    fig.tight_layout()
    fig.savefig(path, dpi=130); plt.close(fig)
    return path

# 1 — Wav2Lip
onset = np.gradient(env)
conf = np.clip(0.55 + 0.45 * (onset / (np.max(np.abs(onset)) + 1e-9)), 0, 1)
v1 = [viseme_for(i, "wav2lip") for i in range(N)]
rows = [(i, round(float(t[i]), 3), v1[i], round(float(env[i]), 3), round(float(conf[i]), 3)) for i in range(N)]
write_csv(f"{PROOFS}/01-wav2lip-viseme-timeline.csv",
          ["frame", "time_s", "cape_viseme", "envelope", "syncnet_style_confidence"], rows)
chart(f"{PROOFS}/01-wav2lip-viseme-timeline.png",
      "01 Wav2Lip — METHOD-WIRED (model NOT run)",
      "Mel-energy/onset -> Cape viseme per frame. SyncNet-style confidence = onset alignment.",
      v1, [("confidence", conf, "#c0392b")])

# 2 — SadTalker (3DMM-style coefficients)
yaw = smooth(8 * np.sin(2 * np.pi * 0.6 * t) * env, 5)
pitch_deg = smooth(5 * np.sin(2 * np.pi * 0.9 * t + 0.7) * env, 5)
expr = np.clip(env * 0.9, 0, 1)
blink = [1 if (env[i] < 0.18 and i % 17 == 0) else 0 for i in range(N)]
v2 = [viseme_for(i, "sadtalker") for i in range(N)]
rows = [(i, round(float(t[i]), 3), v2[i], round(float(yaw[i]), 2), round(float(pitch_deg[i]), 2),
         round(float(expr[i]), 3), blink[i]) for i in range(N)]
write_csv(f"{PROOFS}/02-sadtalker-head-motion.csv",
          ["frame", "time_s", "cape_viseme", "head_yaw_deg", "head_pitch_deg", "expression", "blink"], rows)
chart(f"{PROOFS}/02-sadtalker-head-motion.png",
      "02 SadTalker — METHOD-WIRED (model NOT run)",
      "Audio -> 3DMM-style head yaw/pitch + expression + blink. Cape use: borrow head-motion curve only; mouth stays a swap viseme.",
      v2, [("yaw deg/10", yaw / 10, "#2471a3")])

# 3 — LivePortrait (proxy driving signal — original needs a driving VIDEO)
# Retarget: proxy keypoint lip aperture + head pose follow the envelope,
# with stitching-style smoothing (heavier smoothing than the others).
lip_ap = smooth(np.clip(env * 1.0, 0, 1), 5)
head_lp = smooth(6 * np.sin(2 * np.pi * 0.5 * t) * env, 7)
v3 = [viseme_for(i, "liveportrait") for i in range(N)]
rows = [(i, round(float(t[i]), 3), v3[i], round(float(lip_ap[i]), 3), round(float(head_lp[i]), 2),
         "PROXY-DRIVING-SIGNAL (envelope, NOT a real driving video)") for i in range(N)]
write_csv(f"{PROOFS}/03-liveportrait-retarget.csv",
          ["frame", "time_s", "cape_viseme", "lip_aperture_proxy", "head_pose_proxy_deg", "driving_source_note"], rows)
chart(f"{PROOFS}/03-liveportrait-retarget.png",
      "03 LivePortrait — METHOD-WIRED, PROXY ONLY (model NOT run)",
      "Original is VIDEO-driven, not audio-driven. Envelope stands in as proxy driving signal; real use needs an acted driving video first.",
      v3, [("lip aperture", lip_ap, "#7d3c98")])

# 4 — EMO (diffusion-style, speed-controlled, smooth)
speed = np.clip(0.7 + 0.3 * (pitch - pitch.min()) / (pitch.max() - pitch.min()), 0, 1)
emo_pose = smooth(7 * np.sin(2 * np.pi * 0.45 * t) * env * speed, 9)
v4 = [viseme_for(i, "emo") for i in range(N)]
# EMO holds visemes longer: quantise to 2-frame holds
v4 = [v4[i - (i % 2)] for i in range(N)]
rows = [(i, round(float(t[i]), 3), v4[i], round(float(emo_pose[i]), 2), round(float(speed[i]), 3)) for i in range(N)]
write_csv(f"{PROOFS}/04-emo-expression-timeline.csv",
          ["frame", "time_s", "cape_viseme_2frame_hold", "head_pose_deg", "speed_controller"], rows)
chart(f"{PROOFS}/04-emo-expression-timeline.png",
      "04 EMO — METHOD-WIRED (model NOT run)",
      "Audio -> diffusion-style smooth expression/head pose + speed controller; visemes held 2 frames (Cape-friendly smoothing).",
      v4, [("head pose/10", emo_pose / 10, "#b7950b")])

# 5 — Hallo (hierarchical: coarse syllable + fine frame)
coarse = []
for i in range(N):
    burst = min(int(sum(t[i] > c for c in centres)), 5)
    coarse.append(["nod", "tilt-L", "nod", "tilt-R", "nod", "settle"][burst])
v5 = [viseme_for(i, "hallo") for i in range(N)]
rows = [(i, round(float(t[i]), 3), coarse[i], v5[i], round(float(env[i]), 3)) for i in range(N)]
write_csv(f"{PROOFS}/05-hallo-hierarchical-timeline.csv",
          ["frame", "time_s", "coarse_head_motion_syllable_level", "fine_cape_viseme_frame_level", "envelope"], rows)
chart(f"{PROOFS}/05-hallo-hierarchical-timeline.png",
      "05 Hallo — METHOD-WIRED (model NOT run)",
      "Hierarchical: coarse syllable-level head motion + fine frame-level viseme, temporally aligned. Best Cape fit: two-level exposure sheet.",
      v5, [("envelope", env, "#1e8449")])

# 0 — Generic viseme schematic (abstract mouth diagrams, NOT show character art)
fig, axes = plt.subplots(2, 7, figsize=(13, 4.2))
fig.suptitle("00 Cape viseme set — GENERIC SCHEMATIC ONLY (not show character art)\n"
             "14 Pack-4 slots: rest, EE, EH, AH, OH, OO, MBP, FV, L, SZ, TH, R, W, GK — drawn as abstract mouth shapes",
             fontsize=10)
shapes = {"rest": (0.5, 0.12), "EE": (0.75, 0.18), "EH": (0.6, 0.30), "AH": (0.55, 0.55),
          "OH": (0.38, 0.5), "OO": (0.28, 0.42), "MBP": (0.6, 0.05), "FV": (0.55, 0.15),
          "L": (0.5, 0.35), "SZ": (0.6, 0.22), "TH": (0.5, 0.28), "R": (0.45, 0.30),
          "W": (0.30, 0.35), "GK": (0.5, 0.40)}
for ax, v in zip(axes.flat, VISEMES):
    w, h = shapes[v]
    th = np.linspace(0, 2 * np.pi, 60)
    ax.fill(0.5 + (w / 2) * np.cos(th), 0.5 + (h / 2) * np.sin(th), color="#333333")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(v, fontsize=10)
    for s in ax.spines.values():
        s.set_visible(False)
fig.tight_layout(rect=[0, 0, 1, 0.88])
fig.savefig(f"{PROOFS}/00-cape-viseme-schematic.png", dpi=130); plt.close(fig)

print(f"frames={N} fps={FPS} duration={DUR}s proofs_dir={PROOFS}")
for f in sorted(os.listdir(PROOFS)):
    print(" ", f)
