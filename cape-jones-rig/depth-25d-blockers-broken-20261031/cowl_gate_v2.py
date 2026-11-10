"""EXPERIMENTAL cowl-gate v2 second signal.
Idea: render the SAME pose twice with snap_figure — normal vs cowl-upper —
and measure the pixel change inside the collar band (y 370..520, both
shoulder zones x 350..500 and 600..750). A true collar notch changes many
band pixels when the bicep is lifted over the collar; a normal shoulder
attachment changes few, because the bicep already sits beside/over the
collar edge rather than being cut by it.
Baseline = apose (no snap needed). Signal = band_diff / baseline_diff.
This is a SECOND signal, not a replacement: eye-check remains the final
vote where the signal is near the threshold. Threshold is set from the
measured cases below, not guessed in advance.
"""
import os, sys, importlib.util
import numpy as np
from PIL import Image
RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "depth-25d-blockers-broken-20261031")
spec = importlib.util.spec_from_file_location("snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

def band_diff(cfg, head=0):
    n = np.array(snap.figure(550, cfg, head_angle=head).convert("RGBA"))
    c = np.array(snap.figure(550, cfg, head_angle=head, snap={"L": "cowl", "R": "cowl"}).convert("RGBA"))
    diff = (np.abs(n.astype(int) - c.astype(int)).sum(axis=2) > 30)
    band = np.zeros_like(diff); band[370:520, 350:500] = True; band[370:520, 600:750] = True
    return int((diff & band).sum())

APOSE = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": 0, "R": 0}, "leg_upper": {"L": 0, "R": 0}, "leg_lower": {"L": 0, "R": 0}}
CASES = {
    "apose_baseline": (APOSE, 0, "no snap needed"),
    "jojo02_false_positive": ({"arm_upper": {"L": -115, "R": 65}, "arm_lower": {"L": 85, "R": -95}, "leg_upper": {"L": -16, "R": 32}, "leg_lower": {"L": 6, "R": -28}}, -10, "eye-check: fist beside head, not a cut bicep"),
    "ginyu03_true_notch": ({"arm_upper": {"L": -130, "R": 130}, "arm_lower": {"L": -60, "R": 60}, "leg_upper": {"L": -20, "R": 35}, "leg_lower": {"L": 30, "R": -20}}, 10, "eye-check: bicep notched by collar both sides"),
    "v7c_jump_true_notch": ({"arm_upper": {"L": -150, "R": 150}, "arm_lower": {"L": -40, "R": 40}, "leg_upper": {"L": -12, "R": 12}, "leg_lower": {"L": -8, "R": 8}}, 0, "eye-check: bicep notched by collar both sides"),
    "ginyu01_true_notch": ({"arm_upper": {"L": -160, "R": 20}, "arm_lower": {"L": -20, "R": 95}, "leg_upper": {"L": -45, "R": 20}, "leg_lower": {"L": 10, "R": -10}}, -6, "eye-check: L bicep cut by collar"),
    "jojo03_face": ({"arm_upper": {"L": -25, "R": -88}, "arm_lower": {"L": 35, "R": 145}, "leg_upper": {"L": -42, "R": 12}, "leg_lower": {"L": 32, "R": -6}}, 8, "face snap, not a cowl case (control)"),
}
rows = []
base = None
for name, (cfg, head, note) in CASES.items():
    d = band_diff(cfg, head)
    if base is None:
        base = max(d, 1)
    rows.append((name, d, round(d / base, 2), note))
    print(name, d, round(d / base, 2), note)
with open(os.path.join(OUT, "cowl_gate_v2_results-20261031.csv"), "w") as f:
    f.write("case,band_diff_px,ratio_vs_apose_baseline,eye_check_note\n")
    for name, d, r, note in rows:
        f.write(f"{name},{d},{r},{note}\n")
print("baseline", base)
