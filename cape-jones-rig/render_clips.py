"""Render clip keyframes with joint-locked v5 rig. Imports v5 builder functions
by exec'ing only the function definitions (top-level builds are skipped)."""
import json, pathlib, sys
src = pathlib.Path("/home/hatch/workspace/cape-jones-rig/joint_locked_rig_v5.py").read_text()
# Cut off at first top-level build() call
src = src.split('build("joint-apose-v5')[0]
ns = {}
exec(src, ns)
build = ns["build"]
OUT = pathlib.Path("/home/hatch/workspace/cape-jones-rig/clips")
for clipname in ["punch", "dance", "flex", "flying"]:
    d = json.loads((OUT / f"{clipname}-clip.json").read_text())
    for kf in d["keyframes"]:
        cfg = {"arm_upper": {"L": kf["arm1_upper"], "R": kf["arm2_upper"]},
               "arm_lower": {"L": kf["arm1_lower"], "R": kf["arm2_lower"]},
               "leg_upper": {"L": kf["leg1_upper"], "R": kf["leg2_upper"]},
               "leg_lower": {"L": kf["leg1_lower"], "R": kf["leg2_lower"]}}
        whole = clipname == "flying" and kf["pose"] == "diving-arms-up"
        # build() saves to reposes/ by name; override by temporarily changing OUT in ns
        ns["OUT"] = str(OUT / clipname)
        pathlib.Path(OUT / clipname).mkdir(exist_ok=True)
        build(f"{clipname}-{kf['frame']:02d}-{kf['pose']}.png", cfg, arms_whole=whole)
print("clip frames rendered")
