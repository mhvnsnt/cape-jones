"""Snap gate — mandatory pre-delivery step for every new pose/clip/shot.
Usage:
  python3 check_pose_snap.py --name jojo-03 --upperL -25 --lowerL 35 \
      --upperR -88 --lowerR 145 --head 8 --applied face --out audit.csv
  python3 check_pose_snap.py --name ginyu-03 --upperL -130 --lowerL -60 \
      --upperR 130 --lowerR 60 --head 10 --applied cowl-upper --eye-check \
      "bicep notch at collar, both sides, viewed" --out audit.csv

Decisions (from ARM-FRONT-SNAP-RULE.md, FACE/COWL extension):
  FACE-SNAP  lower_vs_head > 5000            -> whole chain above head
  COWL-CAND  elbow above shoulder > 50 px AND upper_vs_collar > 1000
             -> UPPER ONLY above collar, and ONLY with --eye-check
  CHEST-SNAP lower_vs_torso > 1000, face not crossed -> whole chain
             above torso, below head — WARNING ONLY, not a FAIL by
             itself: lower_vs_torso alone does NOT prove the upper arm
             is eaten (stand-02 user, v7c-flex: forearms in front, uppers
             at the sides, not eaten). A chest snap FAILs only if the
             eye-check says the upper IS eaten and it was not applied.
  NO SNAP    otherwise
Priority: FACE > COWL > CHEST. Exit 0 = PASS (applied matches decision,
or a cowl candidate has a recorded eye-check). Exit 1 = FAIL: a face
snap the gate requires has not been applied, a cowl candidate has no
eye-check, a banned cowl-whole was applied, or a snap was applied with
no gate reason (arm over the face for no reason is a FAIL, see JoJo 02 L).
--applied is PER SIDE: --applied "L:none,R:face" (a single word applies
to both sides only when both sides share it).
A flat PNG cannot prove layer order after the fact — that is why this
gate runs from the pose ANGLES BEFORE rendering, and the builder must
use its decision. Do not edit joint_locked_rig_v7c.py or build_poses.py
to force this in: those builders are frozen for approved poses; this
script is the mandatory step that sits in front of them.
"""
import argparse, csv, importlib.util, io, contextlib, os, sys
GATE = "/home/hatch/workspace/cape-jones-rig/pose-dialects-fix-face-cowl-20261031/check_face_cowl_snap.py"

def run_gate(ul, ll, ur, lr, ha):
    spec = importlib.util.spec_from_file_location("gate", GATE)
    gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        gate.check({"arm_upper": {"L": ul, "R": ur}, "arm_lower": {"L": ll, "R": lr}}, ha)
    return buf.getvalue().strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--upperL", type=float, required=True); ap.add_argument("--lowerL", type=float, required=True)
    ap.add_argument("--upperR", type=float, required=True); ap.add_argument("--lowerR", type=float, required=True)
    ap.add_argument("--head", type=float, default=0)
    ap.add_argument("--applied", default="none",
                    help='per side, e.g. "L:none,R:face" or a single word for both sides')
    ap.add_argument("--eye-check", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    out = run_gate(a.upperL, a.lowerL, a.upperR, a.lowerR, a.head)
    print(out)
    # Parse decisions per side from gate output lines "L: <numbers> -> DECISION"
    decisions = {}
    for line in out.splitlines():
        side, rest = line.split(":", 1)
        decisions[side.strip()] = rest.split("->", 1)[1].strip() if "->" in rest else rest.strip()
    # --applied per side
    applied = {}
    for part in a.applied.split(","):
        if ":" in part:
            s, v = part.split(":", 1); applied[s.strip()] = v.strip()
        else:
            applied = {"L": part.strip(), "R": part.strip()}
    fails, warns = [], []
    for side, rest in decisions.items():
        ap_side = applied.get(side, "none")
        if rest.startswith("FACE-SNAP") and ap_side != "face":
            fails.append(f"{side} needs FACE-SNAP, applied={ap_side}")
        if rest.startswith("COWL-CANDIDATE") and ap_side not in ("cowl-upper",) and not a.eye_check:
            fails.append(f"{side} is COWL-CANDIDATE with no eye-check recorded")
        if rest.startswith("COWL-CANDIDATE") and ap_side == "cowl-whole":
            fails.append(f"{side} cowl-whole is BANNED (see JoJo 02 L: it covers the face); use cowl-upper")
        if rest.startswith("CHEST-SNAP"):
            if "upper eaten" in a.eye_check and ap_side not in ("chest", "face"):
                fails.append(f"{side} eye-check says upper eaten, chest snap not applied")
            else:
                warns.append(f"{side} CHEST-SNAP gate fires (lower_vs_torso>1000) — eye-check decides; not a FAIL alone")
        if rest.startswith("NO SNAP") and ap_side in ("face",):
            fails.append(f"{side} has face snap with NO SNAP gate reason")
    if warns:
        print("WARNINGS:")
        for w in warns:
            print(" -", w)
    if a.out:
        new = not os.path.exists(a.out)
        with open(a.out, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["pose", "side", "gate_output", "applied", "eye_check", "result"])
            for side, rest in decisions.items():
                w.writerow([a.name, side, rest, a.applied, a.eye_check, "FAIL" if fails else "PASS"])
    if fails:
        print("FAIL:")
        for f in fails:
            print(" -", f)
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
