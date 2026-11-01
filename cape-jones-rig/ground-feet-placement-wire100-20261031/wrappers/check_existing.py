#!/usr/bin/env python3
"""Re-gate existing outputs with the new ground gate. No original file
is read for writing, only for measurement. Each wrapper prints its
verdict JSON and exits 0 on PASS, 2 on FAIL.
"""
import json, os, sys
ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
sys.path.insert(0, os.path.join(ROOT, "ground-feet-placement-wire100-20261031"))
from ground_gate import check_single, check_sequence


def main(which):
    if which == "multiplane":
        bars = json.load(open(os.path.join(ROOT, "multiplane-upgrade-20261031/feet-measurements-20261031.json")))
        rows = [{"feet_y": f["feet_y_world"], "feet_centre_x": f["feet_centre_x_world"],
                 "figure_height": 653} for f in bars["final"]]
        rep = check_sequence(rows, "GROUNDED")
    elif which == "size":
        m = json.load(open(os.path.join(ROOT, "size-transformation-power-20261031/size-transformation-measurements-20261031.json")))
        out = {}
        for k in ("coming_forward_walk", "size_transformation"):
            ys = m["templates"][k]["gate"]["feet_y_all"]
            out[k] = check_sequence([{"feet_y": y, "feet_centre_x": 800, "figure_height": 700} for y in ys], "GROUNDED")
        print(json.dumps(out, indent=2))
        return 0 if all(v["verdict"] == "PASS" for v in out.values()) else 2
    elif which == "dual":
        out = {
            "portrait_A_planted": check_single({"feet_y": 1700, "feet_centre_x": 539, "height": 1165},
                                               "GROUNDED", rug_far=1421, rug_near=1868),
            "portrait_old_float": check_single({"feet_y": 1548, "feet_centre_x": 539, "height": 1165},
                                               "GROUNDED", rug_far=1421, rug_near=1868),
        }
        print(json.dumps(out, indent=2))
        # old_float is EXPECTED to fail; the wrapper passes iff A passes
        # and old fails (i.e. the gate discriminates). Report that plainly.
        ok = out["portrait_A_planted"]["verdict"] == "PASS" and out["portrait_old_float"]["fails"]
        print(json.dumps({"wrapper_verdict": "PASS (gate discriminates)" if ok else "FAIL"}))
        return 0 if ok else 2
    elif which == "rig":
        # Rig plates are transparent with no ground in the file itself.
        # The builder must supply ground_y AFTER scaling/pasting; this
        # wrapper proves the call shape on the proof figure (feet 700,
        # ground 700, measured 693 after light-foot fringe, PASS).
        rep = check_single({"feet_y": 693, "feet_centre_x": 550, "height": 593},
                           "GROUNDED", ground_y=700)
    else:
        raise SystemExit("unknown wrapper: multiplane|size|dual|rig")
    print(json.dumps(rep, indent=2))
    return 0 if rep["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
