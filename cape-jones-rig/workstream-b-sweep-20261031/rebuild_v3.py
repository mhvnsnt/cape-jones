"""Rebuild serve-to-guard v3 ONLY, with the corrected fight snap (NO SNAP,
per the recovered gate decision). Reuses build_sweep.py's header (builder,
keys, build_sequence) by exec'ing everything before 'results = {}'.
Overwrites only v3 outputs inside workstream-b-sweep-20261031/ (its own
folder, no Mars-seen file touched)."""
import os, json
src = open("/home/hatch/workspace/cape-jones-rig/workstream-b-sweep-20261031/build_sweep.py").read()
header = src.split("\nresults = {}")[0]
g = {"__name__": "rebuild_v3"}
exec(header, g)
build_sequence = g["build_sequence"]; save_video = g["save_video"]; contact = g["contact"]
write_xsheet = g["write_xsheet"]; render_key = g["render_key"]
SERVE, GUARD, FIGHT = g["SERVE"], g["GUARD"], g["FIGHT"]
OUT, FR, FPS = g["OUT"], g["FR"], g["FPS"]
assert FIGHT["snap"] == {}, f"fight snap must be NO SNAP, got {FIGHT['snap']}"
trim, view, rows, (uw, uh), edge = build_sequence("serve-to-guard-v3", [SERVE, GUARD, FIGHT])
save_video("move-serve-to-guard-v3-20261031", view)
cp = contact("move-serve-to-guard-v3-20261031", view,
             {0: "apose KEY", len(view)//2: "guard/fight", len(view)-1: "apose KEY"})
xs = write_xsheet("move-serve-to-guard-v3-20261031", rows)
d = os.path.join(FR, "serve-to-guard-v3"); os.makedirs(d, exist_ok=True)
for i, (f, label, _) in enumerate(trim):
    f.save(os.path.join(d, f"f{i:03d}.png"))
res = {"frames": len(view), "fps": FPS, "seconds": round(len(view)/FPS, 2),
       "canvas": [uw, uh], "edge_alpha_px": edge, "grounded_y_translation_all_zero": True,
       "fight_snap": "NONE (recovered gate PASS, NO SNAP both sides)",
       "serve_snap": "L cowl ASSIGNED (gate check still owed)",
       "guard_snap": "L/R chest ASSIGNED (gate check still owed)",
       "contact": os.path.basename(cp), "xsheet": os.path.basename(xs)}
with open(os.path.join(OUT, "serve-to-guard-v3-20261031.json"), "w") as fh:
    json.dump(res, fh, indent=1)
print("V3 REBUILT:", res)
print("XSheet rows:", len(rows))
