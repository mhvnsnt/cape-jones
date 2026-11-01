"""Render all clip keyframes with joint-locked v6 rig (supersedes v5 render_clips.py)."""
import json, pathlib
src = pathlib.Path("/home/hatch/workspace/cape-jones-rig/joint_locked_rig_v6.py").read_text()
src = src.split('build("joint-apose-v6')[0]
ns = {}; exec(src, ns); build = ns["build"]
OUT = pathlib.Path("/home/hatch/workspace/cape-jones-rig/clips")
for clipname in ["jump", "punch", "dance", "flex", "flying", "walk"]:
    d = json.loads((OUT / f"{clipname}-clip.json").read_text())
    dest = OUT / clipname; dest.mkdir(exist_ok=True); ns["OUT"] = str(dest)
    for kf in d["keyframes"]:
        if "arm1_upper" in kf:
            cfg = {"arm_upper": {"L": kf["arm1_upper"], "R": kf["arm2_upper"]},
                   "arm_lower": {"L": kf["arm1_lower"], "R": kf["arm2_lower"]},
                   "leg_upper": {"L": kf["leg1_upper"], "R": kf["leg2_upper"]},
                   "leg_lower": {"L": kf["leg1_lower"], "R": kf["leg2_lower"]}}
            pose = kf["pose"]
        else:
            cfg = {"arm_upper": kf["arm_upper"], "arm_lower": kf["arm_lower"],
                   "leg_upper": kf["leg_upper"], "leg_lower": kf["leg_lower"]}
            pose = kf["name"]
        whole = clipname == "flying" and pose == "diving-arms-up"
        # jump takeoff also uses whole arms in v6 poses
        if clipname == "jump" and pose == "takeoff-arms-whole-up":
            whole = True
        build(f"{clipname}-{kf['frame']:02d}-{pose}.png", cfg, arms_whole=whole)
print("v6 clip frames rendered")
