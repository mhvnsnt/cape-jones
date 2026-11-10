#!/usr/bin/env python3
"""Mandatory room-scale gate for dual_orientation builds.
Usage: check_room_scale.py <figure_alpha_height_px> <feet_y_px> <master_height_px> [seated]
Hard FAIL (exit 2) if:
  - standing height ratio is not 0.607 +/- 0.03 of master height
    (seated: 0.607 * 2.3/2.5 = 0.558 +/- 0.03)
  - feet are not on the rug plane in the master (1371..1700)
Chair-back check is reported, NOT hard-failed, for the reason in
ROOM-SCALE-RULE.md section 5: in the KKGuh arms-up crop, chair-back top
(~700 master) cannot equal waist (~1003) at any feet-on-floor scale
(requiring H=1809, head off-frame). Faking that pass would be a lie.
A builder that reports chair-back as PASS in this crop is wrong.
Mars clarification is owed for what chair-back-at-waist means in this crop.
"""
import sys
def main():
    h, feet, master = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    seated = len(sys.argv) > 4 and sys.argv[4] == "seated"
    target = 0.558 if seated else 0.607
    ratio = h / master
    scale_ok = abs(ratio - target) <= 0.03
    feet_ok = 1371 <= feet <= 1700
    waist = None
    print(f"height {h} ratio {ratio:.4f} target {target} scale_ok={scale_ok}")
    print(f"feet_y {feet} rug 1371..1700 feet_ok={feet_ok}")
    print("chair_back: WARNING - see ROOM-SCALE-RULE.md s5, not a pixel pass in KKGuh crop")
    if not (scale_ok and feet_ok):
        print("ROOM-SCALE GATE FAILED"); return 2
    print("ROOM-SCALE GATE PASS (scale + feet; chair-back warning outstanding)")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
