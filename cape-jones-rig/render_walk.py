import json, pathlib
src = pathlib.Path("/home/hatch/workspace/cape-jones-rig/joint_locked_rig_v6.py").read_text()
src = src.split('build("joint-apose-v6')[0]
ns = {}; exec(src, ns); build = ns["build"]
OUT = pathlib.Path("/home/hatch/workspace/cape-jones-rig/clips/walk"); OUT.mkdir(exist_ok=True)
ns["OUT"] = str(OUT)
d = json.loads(pathlib.Path("/home/hatch/workspace/cape-jones-rig/clips/walk-clip.json").read_text())
for kf in d["keyframes"]:
    cfg = {"arm_upper": {"L": kf["arm1_upper"], "R": kf["arm2_upper"]},
           "arm_lower": {"L": kf["arm1_lower"], "R": kf["arm2_lower"]},
           "leg_upper": {"L": kf["leg1_upper"], "R": kf["leg2_upper"]},
           "leg_lower": {"L": kf["leg1_lower"], "R": kf["leg2_lower"]}}
    build(f"walk-{kf['frame']:02d}-{kf['pose']}.png", cfg)
print("walk frames rendered")
