#!/usr/bin/env python3
"""Mandatory pre-delivery ground check, importable by any builder.

Usage in a builder (do NOT edit the original builder to paste this in
without also keeping its own gate — this module IS the gate):
    from gate_mandatory import pre_delivery_check
    pre_delivery_check({"mode": "GROUNDED", "ground_y": 700,
                        "feet_y": measured_feet_y, ...})
On FAIL it raises SystemExit(2) — fail loudly, do not ship.
On PASS it returns the verdict dict and, if log_path is given, appends
one JSON line to that log (append-only, never rewritten).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ground_gate import check_single, check_sequence


def pre_delivery_check(spec, log_path=None):
    if "frames" in spec:
        rep = check_sequence(spec["frames"], spec["mode"],
                             spec.get("tolerance_px", 10))
    else:
        rep = check_single(
            {"feet_y": spec["feet_y"], "feet_centre_x": spec.get("feet_centre_x"),
             "height": spec.get("figure_height")},
            spec["mode"], spec.get("ground_y"), spec.get("rug_far"),
            spec.get("rug_near"), spec.get("tolerance_px", 10),
            spec.get("height_px"), spec.get("flight_line"))
    rep["shot"] = spec.get("shot", "unnamed")
    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps(rep) + "\n")
    if rep["fails"]:
        raise SystemExit(2)
    return rep
