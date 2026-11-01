#!/usr/bin/env python3
"""Arm alignment QC — fails any arm piece whose fist/cuff column is off-axis
vs its v7c reference. Industry rules wired in:
- Cutout rig joint alignment: elbow->wrist->fist must stay on ONE column.
- Anatomical forearm/wrist alignment: wrist at forearm midline; fist centre
  may sit off forearm centre by its natural thumb-side asymmetry, but that
  offset must MATCH the reference piece (turnaround consistency), not drift.
- Pose-driven substitution: a substituted fist/cuff must be re-centred on
  the same axis, never pasted at its source-image coordinates.
Usage:
  python3 check_arm_alignment.py --piece <png> --reference <png> [--tolerance-px 10] [--tolerance-deg 10]
Exit 0 = PASS, 1 = FAIL. Prints measurements as JSON + a plain verdict.
Bands are relative fractions so v7c lowers (288 tall) and foreshortened
pieces (215 tall) use the same rule: forearm = y 0.05-0.55, fist = y 0.60-0.98.
"""
import argparse, json, sys
import numpy as np
from PIL import Image

def measure(path):
    im = np.array(Image.open(path).convert('RGBA'))
    a = im[:, :, 3] > 10
    h = im.shape[0]
    def band(y0f, y1f):
        cs = []
        for y in range(int(h*y0f), int(h*y1f)):
            xx = np.where(a[y])[0]
            if len(xx):
                cs.append(((xx.min()+xx.max())/2, y))
        xs = np.array([c[0] for c in cs]); ys = np.array([c[1] for c in cs])
        m, b = np.polyfit(ys, xs, 1)
        return {"median_centre_px": round(float(np.median(xs)), 1),
                "axis_angle_deg": round(float(np.degrees(np.arctan(m))), 1)}
    f = band(0.05, 0.55); s = band(0.60, 0.98)
    return {"file": path, "size": [int(im.shape[1]), int(h)],
            "forearm": f, "fist": s,
            "fist_minus_forearm_px": round(s["median_centre_px"]-f["median_centre_px"], 1)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--piece', required=True); ap.add_argument('--reference', required=True)
    ap.add_argument('--tolerance-px', type=float, default=10.0)
    ap.add_argument('--tolerance-deg', type=float, default=10.0)
    args = ap.parse_args()
    p, r = measure(args.piece), measure(args.reference)
    d_off = p["fist_minus_forearm_px"] - r["fist_minus_forearm_px"]
    d_ang = p["forearm"]["axis_angle_deg"] - r["forearm"]["axis_angle_deg"]
    verdict = "PASS" if abs(d_off) <= args.tolerance_px and abs(d_ang) <= args.tolerance_deg else "FAIL"
    out = {"piece": p, "reference": r,
           "offset_delta_vs_reference_px": round(d_off, 1),
           "axis_angle_delta_vs_reference_deg": round(d_ang, 1),
           "tolerances": {"px": args.tolerance_px, "deg": args.tolerance_deg},
           "verdict": verdict}
    print(json.dumps(out, indent=2))
    print(f"{verdict}: offset delta {d_off:+.1f}px (tolerance {args.tolerance_px}px), "
          f"axis-angle delta {d_ang:+.1f}deg (tolerance {args.tolerance_deg}deg)")
    return 0 if verdict == "PASS" else 1

if __name__ == '__main__':
    sys.exit(main())
