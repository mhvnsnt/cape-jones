#!/usr/bin/env python3
"""Mandatory landscape scale gate, 2026-10-31.
This gate exists because the old gate FAILED to catch the revert:
the old check_room_scale.py only checked figure height / FRAME height
(0.607) and feet-on-rug in the master. The reverted landscape PASSED
that kind of check by construction (655/1080 = 0.607) while shrinking
the figure 510px in scene terms. A % -of-frame number is therefore
NOT a pass criterion here, and this gate prints that warning on
every run.

NEW LOCK, for a 1920x1080 landscape delivery:
  FAIL (exit 2, loud) if ANY of:
    - final figure height < 1000px
    - figure-to-chair height ratio < 1.42 (2.5x lock ratio, tol 0.005)
    - figure not whole (head < 0 or feet > 1080)
  PASS (exit 0) only if all three hold.
Seated scale (2.3x) is a separate gate, not this one.
Chair height is the furniture anchor: chair-back top ~700 to chair
feet ~1518 in scene = 818px. Ratio = figure height / chair height.
Usage:
  python3 check_scale_gate.py --figure-height 1010 --ratio 1.423 --label "2.5x lock"
  python3 check_scale_gate.py --measurements measurements-20261031.json --version 2.5x_lock
  python3 check_scale_gate.py --figure-height 655 --ratio 1.193 --label "reverted"
"""
import argparse, json, sys

MIN_HEIGHT = 1000
MIN_RATIO = 1.42

def judge(height, ratio, whole, label):
    fails = []
    if height < MIN_HEIGHT:
        fails.append(f"figure height {height}px < locked minimum {MIN_HEIGHT}px")
    if ratio < MIN_RATIO - 0.005:
        fails.append(f"figure-to-chair ratio {ratio} < locked minimum {MIN_RATIO}")
    if not whole:
        fails.append("figure not whole in frame")
    print("WARNING: % -of-frame height alone is NEVER a scale pass. "
          "This gate checks absolute height + furniture ratio + whole figure.")
    if fails:
        print(f"SCALE GATE FAIL — {label} — DO NOT SHIP")
        for f in fails:
            print(f"  - {f}")
        return 2
    print(f"SCALE GATE PASS — {label} — height {height}px, ratio {ratio}, whole={whole}")
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--figure-height", type=int)
    ap.add_argument("--ratio", type=float)
    ap.add_argument("--label", default="delivery")
    ap.add_argument("--whole", type=int, default=1)
    ap.add_argument("--measurements")
    ap.add_argument("--version")
    a = ap.parse_args()
    if a.measurements:
        meta = json.load(open(a.measurements))
        v = meta["versions"][a.version]
        return judge(v["final_figure_height"], v["figure_to_chair_ratio"],
                     v["whole"], f"{a.version} {v['file']}")
    return judge(a.figure_height, a.ratio, bool(a.whole), a.label)

if __name__ == "__main__":
    sys.exit(main())
