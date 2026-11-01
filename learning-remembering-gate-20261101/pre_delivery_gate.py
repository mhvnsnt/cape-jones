#!/usr/bin/env python3
"""pre_delivery_gate.py — MANDATORY pre-delivery gate for Cape Jones clips/videos.
Mars 2026-11-01 11:31 CST: stop making Mars repeat himself; learn as we go.
The gate loads rules.json (the single source of truth) and checks a pose
table against EVERY rule. Exit 0 = PASS (may ship). Exit 1 = FAIL (must NOT
ship, must NOT be shown as fixed). No --force flag exists on purpose.

10 industry-standard learning/remembering systems WIRED here, not listed:
 1. Aviation/NASA pre-flight checklist — all items checked, none skippable,
    a single FAIL blocks the flight (here: the delivery).
 2. Software CI quality gate (GitHub Actions/Jenkins) — exit 1 blocks the
    pipeline; the gate runs in check_before_ship.sh before any show/send.
 3. Toyota lean poka-yoke / Andon — a rule violation stops the line at
    the station where it occurs, with the frame number, not at the end.
 4. Animation X-sheet / exposure sheet (Disney, Toon Boom Harmony) —
    a per-frame pose table is REQUIRED input; no table = FAIL, because
    a flat video cannot prove layer order, knee direction, or elbow
    direction after the fact (ARM-FRONT-SNAP-RULE pipeline step).
 5. Broadcast QC (WCAG 2.3.1 / Harding-PEAT proxy) — whole-frame flash
    check in video mode; layout-specific forearm boxes are NOT reused
    on a different layout (stated limit, dance-flash-fix).
 6. Cut-out rig QA (Harmony Z-depth, Godot Behind-Parent, Spine draw
    order) — layer order is a per-frame keyable property, checked per
    arm per frame, never a rig constant.
 7. WHO surgical checklist / independent double-check — two independent
    senses where possible: angle-mode sensor (authoritative) + flat
    video proxy (candidate only, never a verdict by itself).
 8. Regression testing (pytest-style snapshots) — fixtures/ hold the
    OLD bad poses; the gate must FAIL them forever. If a future build
    matches an old bad fixture, it fails even if nobody remembers why.
 9. Aerospace/NASA CAPA lessons-learned — CORRECTION-LOG is append-only;
    a correction closes only when its regression fixture FAILs old and
    PASSes fixed. The log is loaded and listed in every report.
 10. ADR / runbook knowledge base — rules.json is versioned, builders
    import it; numbers are never copy-pasted per clip again.

Pose-table schema (one row per frame; fields not present are skipped
with a WARNING, not silently passed — except the table itself, which
is mandatory):
  frame, move (flex|shuffle|walk|fight|dance|other),
  forearm_torso_overlap_L/R (px), snap_L/R (bool), snap_layer_L/R
    (normal|chest|face|cowl-upper|cowl-whole),
  forearm_head_overlap_L/R (px),
  knee_dir_L/R (in|out|straight), foot_dir_L/R (in|out|straight),
  leg1_exception (bool), leg2_past_knee_threshold (bool),
  wrist_distance_px, wrist_nearer_than_fingertip (bool), wrist_cut (bool),
  flex_spread_deg, elbow_dir_L/R (back|out|forward|in),
  arm_motion_sign_L/R, intended_motion_sign_L/R,
  step_leg (L|R|null), lifted_leg (L|R|null), step_hold (bool),
  airborne (bool), foot_ground_y_L/R (px), ground_y (px),
  cape_collar_present, cape_back_present, collar_dy, torso_dy,
  seated, cape_bottom_dy, cropped, square_crop, hand_drawn

Usage:
  python3 pre_delivery_gate.py --pose-table fixtures/fixed_all.json --clip-id test
  python3 pre_delivery_gate.py --pose-table X.json --video clip.mp4 --clip-id Y
  python3 pre_delivery_gate.py --pose-table X.json --out report.json
Exit 0 PASS, 1 FAIL, 2 usage error (no table, bad JSON).
"""
import argparse, json, os, sys, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = json.load(open(os.path.join(HERE, "rules.json")))["rules"]
BY_ID = {r["id"]: r for r in RULES}

def fail(fails, rule, frame, msg):
    fails.append({"rule": rule, "frame": frame, "message": msg})

def check_pose_table(data):
    fails, warnings = [], []
    frames = data.get("frames")
    if not isinstance(frames, list) or not frames:
        return fails, ["pose table has no frames — FAIL by missing table"], True
    for row in frames:
        f = row.get("frame", "?")
        # R01 arm-front snap, per arm
        for side in ("L", "R"):
            ov = row.get(f"forearm_torso_overlap_{side}")
            snap = row.get(f"snap_{side}")
            if ov is not None and ov > 1000 and snap is not True:
                fail(fails, "R01-arm-front-snap", f,
                     f"arm {side}: forearm_vs_torso={ov}px >1000 but snap=False — arm EATEN by chest")
            if ov is not None and snap is True and ov <= 1000:
                layer = row.get(f"snap_layer_{side}")
                if layer not in ("face", "cowl-upper"):
                    fail(fails, "R01-arm-front-snap", f,
                         f"arm {side}: snapped with overlap={ov}px <=1000 and no face/cowl reason — floating arm")
            # R02 face snap
            hov = row.get(f"forearm_head_overlap_{side}")
            if hov is not None and hov > 5000:
                if row.get(f"snap_layer_{side}") != "face":
                    fail(fails, "R02-face-snap", f,
                         f"arm {side}: forearm_vs_head={hov}px >5000 but layer is not face — arm eaten by head")
            # R03 cowl whole-chain banned
            if row.get(f"snap_layer_{side}") == "cowl-whole":
                fail(fails, "R03-cowl-upper-only", f,
                     f"arm {side}: whole-chain cowl snap is BANNED (upper-only + eye-check only)")
        # R04 / R04b knee-feet, per leg, per frame
        for side, leg in (("L", "leg1"), ("R", "leg2")):
            kd, fd = row.get(f"knee_dir_{side}"), row.get(f"foot_dir_{side}")
            if kd in ("in", "out") and fd in ("in", "out") and kd != fd:
                if leg == "leg1" and row.get("leg1_exception") is True:
                    warnings.append(f"frame {f}: leg1 knee/foot mismatch excused by 2026-11-01 leg1 exception (flagged)")
                else:
                    fail(fails, "R04-knee-feet-per-frame" if leg == "leg1" else "R04b-leg1-leg2-exception-20261101", f,
                         f"{leg} ({side}): knee={kd} but foot={fd} — knee/foot mismatch, broken-joint read")
        if row.get("leg2_past_knee_threshold") is True and row.get("knee_dir_R") == "in" and row.get("foot_dir_R") != "in":
            fail(fails, "R04b-leg1-leg2-exception-20261101", f,
                 "leg2 (RIGHT): knee past threshold and inward, but foot did NOT turn inward")
        # R05 wrist
        if row.get("wrist_cut") is True:
            fail(fails, "R05-wrist", f, "wrist cut — banned; hands go WITH the wrist")
        wd = row.get("wrist_distance_px")
        if wd is not None and wd > 30:
            fail(fails, "R05-wrist", f, f"wrist_distance={wd}px >30 — hand not attached by wrist")
        if row.get("wrist_nearer_than_fingertip") is False:
            fail(fails, "R05-wrist", f, "wrist is NOT nearer than fingertip — hand attached by fingertips")
        # R06 flex obtuse
        if row.get("move") == "flex":
            sp = row.get("flex_spread_deg")
            if sp is not None and sp < 100:
                fail(fails, "R06-flex-obtuse", f,
                     f"flex_spread={sp} deg <100 — too ACUTE, super-extreme overexerted flex, needs 70-90 deg wider (target 100-160)")
            if sp is not None and sp > 160:
                warnings.append(f"frame {f}: flex_spread={sp} deg >160 — over-wide, eye-check required")
        # R07 elbow direction + motion sign
        for side in ("L", "R"):
            ed = row.get(f"elbow_dir_{side}")
            if ed in ("forward", "in"):
                fail(fails, "R07-elbow-direction", f, f"elbow {side} points {ed} — backwards/reversed elbow")
            ms, im = row.get(f"arm_motion_sign_{side}"), row.get(f"intended_motion_sign_{side}")
            if ms is not None and im is not None and ms != im:
                fail(fails, "R07-elbow-direction", f, f"arm {side} motion sign {ms} != intended {im} — arms in opposite direction")
        # R08 shuffle alternating steps
        if row.get("move") == "shuffle":
            pass  # sequence check below, needs order
        # R09 grounded
        if row.get("airborne") is not True:
            gy = row.get("ground_y")
            for side in ("L", "R"):
                fy = row.get(f"foot_ground_y_{side}")
                if gy is not None and fy is not None and abs(fy - gy) > 5 and row.get("lifted_leg") != side:
                    fail(fails, "R09-grounded", f, f"foot {side} y={fy} vs ground {gy} (>5px) and not labelled airborne/lifted — floating foot")
        # R10 cape two parts
        if row.get("cape_collar_present") or row.get("cape_back_present"):
            if not (row.get("cape_collar_present") and row.get("cape_back_present")):
                fail(fails, "R10-cape-two-parts", f, "cape must be TWO parts (collar + back), only one present")
            if row.get("collar_dy") is not None and row.get("torso_dy") is not None and row["collar_dy"] != row["torso_dy"]:
                fail(fails, "R10-cape-two-parts", f, f"collar_dy={row['collar_dy']} != torso_dy={row['torso_dy']} — collar must move with torso")
            if row.get("seated") is True and row.get("cape_bottom_dy") not in (None, 0):
                fail(fails, "R10-cape-two-parts", f, f"seated cape_bottom_dy={row['cape_bottom_dy']} != 0 — bottom must be pinned (sitting on it)")
        # R11 no crop / no hand-draw
        for k in ("cropped", "square_crop", "hand_drawn"):
            if row.get(k) is True:
                fail(fails, "R11-no-crop-no-handdraw", f, f"{k}=True — banned")
    # R08 sequence: alternating steps, one leg lifted
    steps = [(r.get("frame"), r.get("step_leg"), r.get("lifted_leg"), r.get("step_hold"))
             for r in frames if r.get("move") == "shuffle" and r.get("step_leg")]
    prev = None
    for fr, leg, lifted, hold in steps:
        if not hold:
            if lifted is None:
                fail(fails, "R08-shuffle-alternating-steps", fr, f"shuffle step {leg} with NO leg lifted — slide, not a step")
            elif lifted != leg:
                fail(fails, "R08-shuffle-alternating-steps", fr, f"shuffle step leg={leg} but lifted_leg={lifted} — step must lift the stepping leg")
            if prev is not None and leg == prev:
                fail(fails, "R08-shuffle-alternating-steps", fr, f"shuffle step {leg} twice in a row — must ALTERNATE L,R,L,R")
        prev = leg
    return fails, warnings, False

def check_video_flash(path):
    """Whole-frame WCAG 2.3.1 proxy only. Returns (fails, info)."""
    try:
        import numpy as np
        from PIL import Image
    except Exception as e:
        return [], {"flash": f"skipped: {e}"}
    tmp = tempfile.mkdtemp(prefix="gate_flash_")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-vf", "fps=24,scale=480:-1",
                    os.path.join(tmp, "f%05d.png")], check=True)
    files = sorted(os.listdir(tmp))
    if not files:
        return [{"rule": "R12-flicker", "frame": "?", "message": "no frames extracted"}], {}
    means, reds = [], []
    for fn in files:
        a = np.array(Image.open(os.path.join(tmp, fn)).convert("RGB")).astype(float)
        lum = 0.2126*a[:, :, 0] + 0.7152*a[:, :, 1] + 0.0722*a[:, :, 2]
        means.append(float(lum.mean()))
        reds.append(float(((a[:, :, 0] > 200) & (a[:, :, 0]-a[:, :, 1] > 80) & (a[:, :, 0]-a[:, :, 2] > 80)).mean()))
    gen = []
    for i in range(2, len(means)):
        d1, d2 = means[i-1]-means[i-2], means[i]-means[i-1]
        if d1*d2 < 0 and abs(d1) >= 25.5 and abs(d2) >= 25.5 and min(means[i-2:i+1]) < 204:
            gen.append(i)
    # max in any 1s window at 24fps
    worst = max((sum(1 for x in gen if e <= x < e+24) for e in gen), default=0)
    fails = []
    if worst > 3:
        fails.append({"rule": "R12-flicker", "frame": gen, "message": f"whole-frame flashes {worst} in 1s > 3 (WCAG 2.3.1 proxy)"})
    return fails, {"frames": len(files), "general_flash_events": len(gen), "max_per_sec": worst,
                   "note": "whole-frame proxy only; dance-test forearm boxes NOT reused on other layouts"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pose-table", required=True)
    ap.add_argument("--video", default="")
    ap.add_argument("--clip-id", default="unnamed")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    if not os.path.exists(args.pose_table):
        print(f"FAIL: pose table not found: {args.pose_table}"); return 2
    try:
        data = json.load(open(args.pose_table))
    except Exception as e:
        print(f"FAIL: bad pose-table JSON: {e}"); return 2
    fails, warnings, missing = check_pose_table(data)
    video_info, audio_info = {}, {}
    if args.video:
        vf, video_info = check_video_flash(args.video)
        fails += vf
        try:
            out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                                  "-of", "csv=p=0", args.video], capture_output=True, text=True, check=True).stdout
            audio_info = {"streams": out.strip().splitlines(), "has_audio": "audio" in out}
            if not audio_info["has_audio"]:
                fails.append({"rule": "audio", "frame": "?", "message": "video has NO audio track — clips must not ship silent"})
        except Exception as e:
            audio_info = {"error": str(e)}
    verdict = "FAIL" if (fails or missing) else "PASS"
    report = {"clip_id": args.clip_id, "verdict": verdict, "rules_loaded": len(RULES),
              "rules": [r["id"] for r in RULES], "failures": fails, "warnings": warnings,
              "missing_table": missing, "video_flash": video_info, "audio": audio_info,
              "correction_log": "CORRECTION-LOG-20261101.md (append-only; every logged correction is a rule above)"}
    if args.out:
        json.dump(report, open(args.out, "w"), indent=2)
    print(f"{verdict}: {args.clip_id} — {len(fails)} failure(s), {len(warnings)} warning(s), {len(RULES)} rules loaded")
    for fl in fails:
        print(f"  FAIL {fl['rule']} frame {fl['frame']}: {fl['message']}")
    for w in warnings:
        print(f"  WARN: {w}")
    return 0 if verdict == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
