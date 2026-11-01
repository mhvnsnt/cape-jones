import sys, io, contextlib
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/pose-dialects-fix-face-cowl-20261031")
import importlib.util
spec = importlib.util.spec_from_file_location("gate", "/home/hatch/workspace/cape-jones-rig/pose-dialects-fix-face-cowl-20261031/check_face_cowl_snap.py")
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)

POSES = [
 # pose-dialects (name, upperL, lowerL, upperR, lowerR, head)
 ("jojo-01", -75,125, 40,-45, 12),
 ("jojo-02", -115,85, 65,-95, -10),
 ("jojo-03-ORIGINAL", -25,35, -88,145, 8),
 ("jojo-03-FIXED (chain on top, gate should still report need)", -25,35, -88,145, 8),
 ("stand-01-user", -60,130, 60,-130, 0),
 ("stand-01-shadow-figure", -60,130, 60,-130, 0),
 ("stand-02-user", -35,60, 35,-60, 6),
 ("stand-02-shadow-figure", -150,-40, 150,40, -4),
 ("ginyu-01-ORIGINAL", -160,-20, 20,95, -6),
 ("ginyu-01-FIXED (chain on top)", -160,-20, 20,95, -6),
 ("ginyu-02", -70,140, 70,-140, 0),
 ("ginyu-03", -130,-60, 130,60, 10),
 # v7c joint poses
 ("v7c-apose", -20,-20, 20,20, 0),
 ("v7c-flex", -25,160, 25,-160, 0),
 ("v7c-punch", -45,-45, 90,90, 0),
 ("v7c-jump-armsup", -150,-150, 150,150, 0),
 ("v7c-dance", -60,-60, 60,60, 0),
 ("v7c-seated", -20,-20, 20,20, 0),
 # flex variants
 ("true-final-flex-v2", -85,145, 85,-145, 0),
 ("flex-variant-70-135", -70,135, 70,-135, 0),
 ("arms-up-base", -70,150, 70,-150, 0),
 ("flex-split-armsup", -70,150, 70,-150, 0),
 # dance-arm-snap key poses
 ("dance-STRIDE_A", -35,-30, 35,30, 0),
 ("dance-STRIDE_B", 35,30, -35,-30, 0),
 ("dance-GROOVE_A", -60,-50, 60,50, 0),
 ("dance-GROOVE_B", -70,-40, 70,40, 0),
 ("dance-KICK", -45,-45, 90,90, 0),
 ("dance-SPLIT", -70,150, 70,-150, 0),
 ("dance-TWIST", -90,120, 20,-60, 0),
 ("dance-ARMSUP", -70,150, 70,-150, 0),
 ("dance-REST", -20,-20, 20,20, 0),
]
for name, ul, ll, ur, lr, ha in POSES:
    print(f"=== {name} ===")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        gate.check({"arm_upper":{"L":ul,"R":ur},"arm_lower":{"L":ll,"R":lr}}, ha)
    print(buf.getvalue().strip())
