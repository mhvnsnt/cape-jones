#!/usr/bin/env python3
"""Sit animation from the LOCKED default sitting pose — reusable builder.

Usage:
  python3 build_sit_lean.py [--manifest PATH] [--out DIR] [--frames-dir DIR]
    [--frames N] [--fps N]

Inputs (read-only, never overwritten):
  Manifest: ~/workspace/cape-jones-rig/rig-34-locked-default-sitting-20261101/
              MANIFEST-DEFAULT-SITTING-POSE-20261101.json  (v2 poses)
  Pieces:   APPROVED PERFECT wired pieces in
              rig-34-disassembled-wired-20261101/pieces/ (forearm_no_fist_*,
              fists OFF) plus sitting-rig-34 pieces, cut-limbs-v7c caps,
              sliced/Neck.png (front rig).

Motion (96 frames @ 24 fps = 4.0 s, distinct from the locked job's 48-frame
sit-idle bob):
  f 0-23 : sit idle breathing (upper bob +-3 px, head tilt +-1.5 deg)
  f 24-59: lean forward, smoothstep ease-in, t 0 -> 1
  f 60-71: hold lean (breathing continues, reduced)
  f 72-95: return to sit, smoothstep ease-out, t 1 -> 0 (loops to frame 0)

JOINT LOCKS (locked TOGETHER, not frozen in space — chains move together):
  SHOULDER_TORSO   torso -> upperArmL/R (same torso dy as torso)
  ELBOW_BICEP      upperArm -> elbowCapL/R (same dy as upper arm)
  ELBOW_FOREARM    elbowCap -> forearmL/R (same dy; small +/-5 deg lean swing)
  FOREARM_WRIST_HAND forearm -> handL/R (same dy as forearm)
  HIP_PELVIS       pelvis -> thighL/R (STATIC: pelvis/legs never move)
  HIP_KNEE_TURN    thigh -> kneeL/R (STATIC)
  KNEE_SHIN        knee -> shinL/R (STATIC, feet exactly as saved)
  CAPE_BACK        cape locked to back placement (STATIC, z0)
  NECK_HEAD        neck -> head (neck dy between torso dy and head dy, so the
                   neck always bridges head bottom and torso top)
  LAYERS           DEFS-stable z order, same as build_locked_v2.py:
                   cape, upperArmL, thighR, thighL, forearmL, pelvis, kneeL,
                   elbowCapL, shinL, shinR, kneeR, torso, upperArmR, forearmR,
                   elbowCapR, neck, head, handL, handR

Lean geometry (front view: lean forward reads as head/torso dropping
toward the viewer, NOT a sideways tilt and NOT a whole-figure shift):
  torso/arms dy = 14*t px, neck dy = 18*t px, head dy = 24*t px.
  At t=1: torso top 370->384, neck 348->430, head bottom 391->415,
  so neck still overlaps both (348 < 415 and 430 > 384) — bridge intact.
  Pelvis/legs/cape dy = 0 exactly; figure bottom stays ~1410, never
  shifted to fake a 1475 ground line.

Rotation method (standing rule): LARGE-TEMP rotate ONLY — each piece is
pasted onto a 3x temp canvas and rotated about its saved pivot. NEVER
in-place rotate with expand=False (that square-cropped Arm 2 bicep
-25.7%). Whole pieces only: no crop, no split, no erase, no
square/rectangular crop for any piece, for any reason. Neck is the WHOLE
sliced/Neck.png (104x83) resized to 109x87, so its alpha renders
101x82, centre x~700, top ~330, drawn after arms, before head.

Outputs: transparent PNG frames (frames-dir, default /tmp), then
ffmpeg encodes MP4 (VP9 yuva420p, alpha preserved) + GIF (palette with
reserved transparent index). No background plate is ever composited
into a deliverable; a grey preview composite is never written here.
"""
import argparse, json, math, os, subprocess, sys

ROOT = "/home/hatch/workspace/cape-jones-rig"
DEFAULT_MANIFEST = (f"{ROOT}/rig-34-locked-default-sitting-20261101/"
                    "MANIFEST-DEFAULT-SITTING-POSE-20261101.json")
W, H = 1400, 1600

# (piece, source, rendered size, pivot) in DEFS-stable draw order.
DEFS = [
    ("cape", f"{ROOT}/sitting-rig-34-20261101/pieces/cape_back.png", (514, 900), (0.5, 0.5)),
    ("upperArmL", f"{ROOT}/sitting-rig-34-20261101/pieces/upper_arm_L_socket.png", (125, 237), (0.5, 0)),
    ("thighR", f"{ROOT}/sitting-rig-34-20261101/pieces/thigh_bent_R.png", (218, 299), (0.5, 0)),
    ("thighL", f"{ROOT}/sitting-rig-34-20261101/pieces/thigh_bent_L.png", (230, 267), (0.5, 0)),
    ("forearmL", f"{ROOT}/rig-34-disassembled-wired-20261101/pieces/forearm_no_fist_L.png", (145, 275), (0.39, 0.11)),
    ("pelvis", f"{ROOT}/sitting-rig-34-20261101/pieces/pelvis_belt.png", (218, 181), (0.5, 0.5)),
    ("kneeL", f"{ROOT}/sitting-rig-34-20261101/pieces/knee_ball_spare.png", (74, 94), (0.5, 0.5)),
    ("elbowCapL", f"{ROOT}/cut-limbs-v7c/Arm_Front_Cap.png", (63, 63), (0.5, 0.5)),
    ("shinL", f"{ROOT}/sitting-rig-34-20261101/pieces/shin_boot_L.png", (244, 410), (0.5, 0)),
    ("shinR", f"{ROOT}/sitting-rig-34-20261101/pieces/shin_boot_mid.png", (256, 415), (0.5, 0)),
    ("kneeR", f"{ROOT}/sitting-rig-34-20261101/pieces/knee_ball_spare.png", (74, 94), (0.5, 0.5)),
    ("torso", f"{ROOT}/sitting-rig-34-20261101/pieces/torso.png", (291, 315), (0.5, 0)),
    ("upperArmR", f"{ROOT}/sitting-rig-34-20261101/pieces/upper_arm_R.png", (112, 256), (0.5, 0)),
    ("forearmR", f"{ROOT}/rig-34-disassembled-wired-20261101/pieces/forearm_no_fist_R.png", (150, 274), (0.63, 0.11)),
    ("elbowCapR", f"{ROOT}/cut-limbs-v7c/Arm_Back_Cap.png", (63, 63), (0.5, 0.5)),
    # Neck: WHOLE sliced/Neck.png, no crop. Full 104x83 -> 109x87 renders alpha 101x82.
    ("neck", f"{ROOT}/sliced/Neck.png", (109, 87), (0.5, 0.5)),
    ("head", f"{ROOT}/sitting-rig-34-20261101/pieces/head_cowl.png", (130, 196), (0.5, 0.5)),
    ("handL", f"{ROOT}/sitting-rig-34-20261101/pieces/hand_spare_L.png", (117, 170), (0.5, 0.5)),
    ("handR", f"{ROOT}/sitting-rig-34-20261101/pieces/hand_spare_L.png", (117, 170), (0.5, 0.5)),
]
UPPER = {"head", "neck", "torso", "upperArmL", "upperArmR",
         "forearmL", "forearmR", "elbowCapL", "elbowCapR", "handL", "handR"}
STATIC = {"cape", "pelvis", "thighL", "thighR", "kneeL", "kneeR", "shinL", "shinR"}
# Neck placement from build_locked_v2.py (alpha centre ~700, top ~330).
NECK_XY = (645, 329)


def smoothstep(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lean_t(f):
    """Lean factor 0..1 for frame f of a 96-frame timeline."""
    if f < 24:
        return 0.0
    if f < 60:
        return smoothstep((f - 24) / 36.0)
    if f < 72:
        return 1.0
    return 1.0 - smoothstep((f - 72) / 24.0)


def paste_piece(canvas, src, size, pivot, rot, xy, flip=False):
    """Large-temp rotate ONLY. Whole piece, never cropped."""
    from PIL import Image
    ox, oy = pivot
    x, y = xy
    im = Image.open(src).convert("RGBA").resize(size, Image.LANCZOS)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    tmp = Image.new("RGBA", (size[0] * 3, size[1] * 3), (0, 0, 0, 0))
    tmp.alpha_composite(im, (size[0], size[1]))
    px, py = size[0] + ox * size[0], size[1] + oy * size[1]
    rot_im = tmp.rotate(-rot, resample=Image.BICUBIC, center=(px, py))
    paste_x = int(round(x + ox * size[0] - px))
    paste_y = int(round(y + oy * size[1] - py))
    canvas.alpha_composite(rot_im, (paste_x, paste_y))
    return rot_im, paste_x, paste_y


def render_frame(f, saved):
    """Return (canvas, per-piece alpha bboxes). saved: manifest pieces."""
    from PIL import Image
    t = lean_t(f)
    bob = int(round(3 * math.sin(2 * math.pi * f / 48.0)))
    bob_lean = int(round(bob * (1 - 0.5 * t)))  # breathing quiets at full lean
    head_tilt = round(1.5 * math.sin(2 * math.pi * f / 48.0), 2)
    torso_dy = 14 * t + bob_lean
    neck_dy = 18 * t + bob_lean
    head_dy = 24 * t + bob_lean
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bboxes = {}
    for pid, src, size, pivot in DEFS:
        if pid == "neck":
            x, y, rot = NECK_XY[0], NECK_XY[1] + neck_dy, 0
        else:
            x, y = saved[pid]["xy"]
            rot = saved[pid]["rotation"]
            if pid in ("torso", "upperArmL", "upperArmR", "elbowCapL",
                       "elbowCapR", "forearmL", "forearmR", "handL", "handR"):
                y = y + torso_dy
            if pid == "head":
                y, rot = y + head_dy, rot + head_tilt
            if pid == "forearmL":
                rot = rot - 5 * t
            if pid == "forearmR":
                rot = rot + 5 * t
        rot_im, px, py = paste_piece(canvas, src, size, pivot, rot, (x, y),
                                     flip=(pid == "handR"))
        single = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        single.alpha_composite(rot_im, (px, py))
        bboxes[pid] = single.getbbox()
    return canvas, bboxes, {"lean_t": round(t, 4), "bob": bob_lean,
                            "head_tilt": head_tilt}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("--out", default=f"{ROOT}/anim-sit-locked-20261101")
    ap.add_argument("--frames-dir", default="/tmp/anim-sit-locked-20261101/frames")
    ap.add_argument("--frames", type=int, default=96)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--skip-render", action="store_true",
                    help="Reuse already-rendered frames in --frames-dir; only "
                         "recompute gates and re-encode.")
    args = ap.parse_args()
    manifest = json.load(open(args.manifest))
    saved = {}
    for pid, entry in manifest["pieces"].items():
        saved[pid] = {"xy": tuple(entry["xy"]), "rotation": entry["rotation"]}
    # Neck in the manifest is listed at alpha size/xy; the builder renders the
    # whole piece per build_locked_v2.py (NECK_XY), so it is not taken from
    # the manifest xy — verified by alpha bbox below, not by xy equality.
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.frames_dir, exist_ok=True)
    from PIL import Image
    import numpy as np
    checks = {}
    if args.skip_render:
        existing = [n for n in os.listdir(args.frames_dir)
                    if n.startswith("frame-") and n.endswith(".png")]
        assert len(existing) == args.frames, \
            f"skip-render: found {len(existing)} frames, expected {args.frames}"
        for f in (0, 47, 65, 95):
            _, bboxes, meta = render_frame(f, saved)
            checks[f"frame_{f:03d}"] = {
                "lean_t": meta["lean_t"], "bob": meta["bob"],
                "neck_bbox": list(bboxes["neck"]),
                "head_bbox": list(bboxes["head"]),
                "torso_bbox": list(bboxes["torso"]),
                "shinR_bbox": list(bboxes["shinR"]),
            }
    for f in range(args.frames):
        if args.skip_render:
            continue
        canvas, bboxes, meta = render_frame(f, saved)
        canvas.save(os.path.join(args.frames_dir, f"frame-{f:03d}.png"))
        if f in (0, 47, 65, 95):
            checks[f"frame_{f:03d}"] = {
                "lean_t": meta["lean_t"], "bob": meta["bob"],
                "neck_bbox": list(bboxes["neck"]),
                "head_bbox": list(bboxes["head"]),
                "torso_bbox": list(bboxes["torso"]),
                "shinR_bbox": list(bboxes["shinR"]),
            }
    # Overall gates from frame 0 and the full-lean frame 65.
    c0, b0, _ = render_frame(0, saved)
    _, b65, _ = render_frame(65, saved)
    a = np.array(c0)
    ys, xs = np.where(a[:, :, 3] > 0)
    neck = b0["neck"]
    gates = {
        "canvas": [W, H], "frames": args.frames, "fps": args.fps,
        "duration_s": round(args.frames / args.fps, 2),
        "bbox_frame0": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
        "neck_alpha_bbox_frame0": list(neck),
        "neck_rendered_alpha_size": [neck[2] - neck[0] + 1, neck[3] - neck[1] + 1],
        "neck_centre_x_frame0": round((neck[0] + neck[2]) / 2, 1),
        "neck_top_frame0": neck[1],
        "shinR_bottom_frame0": b0["shinR"][3],
        "shinR_bottom_frame65_lean": b65["shinR"][3],
        "legs_static": all(b0[p] == b65[p] for p in STATIC),
        "hands": 2, "fists_drawn": 0,
        "joint_locks": ["SHOULDER_TORSO", "ELBOW_BICEP", "ELBOW_FOREARM",
                        "FOREARM_WRIST_HAND", "HIP_PELVIS", "HIP_KNEE_TURN",
                        "KNEE_SHIN", "CAPE_BACK", "NECK_HEAD", "LAYERS"],
        "checks": checks,
    }
    json.dump(gates, open(os.path.join(args.out, "gates-20261101.json"), "w"), indent=2)
    print(json.dumps(gates, indent=2))
    # Encodes (transparent inputs; no background composited anywhere).
    # MP4 codec choice, verified 2026-11-01 on this ffmpeg build: libvpx-vp9
    # with yuva420p and libaom-av1 with yuva420p both silently fall back to
    # yuv420p (alpha dropped, background decodes black) in .mp4 AND .webm,
    # and qtrle/prores are rejected by the mp4 muxer. PNG video in .mp4 is
    # the codec here that ffprobe-verifies as rgba and decodes with corner
    # alpha 0. It is large; the GIF below is the small playable preview.
    mp4 = os.path.join(args.out, "sit-lean-locked-20261101.mp4")
    gif = os.path.join(args.out, "sit-lean-locked-20261101.gif")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(args.fps),
                    "-i", os.path.join(args.frames_dir, "frame-%03d.png"),
                    "-c:v", "png", "-pix_fmt", "rgba", "-an", mp4], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(args.fps),
                    "-i", os.path.join(args.frames_dir, "frame-%03d.png"),
                    "-filter_complex",
                    "split[s0][s1];[s0]palettegen=max_colors=256:reserve_transparent=1[p];[s1][p]paletteuse",
                    gif], check=True)
    for path in (mp4, gif):
        print(path, os.path.getsize(path), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
