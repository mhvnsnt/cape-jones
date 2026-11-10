"""Build the 4 NEW movement poses ONLY (ADDITIVES), one at a time, releasing
frames between poses. Reuses build_sweep.py's header (builder, keys,
build_sequence) by exec'ing everything before 'results = {}'.
Usage: python3 build_new_poses.py 0 1  (pose indices)  or no args = all 4.
Writes only inside workstream-b-sweep-20261031/. No Mars-seen file touched.
All 4 poses GROUNDED (feet planted, y-translation 0, gated in build_sequence).
"""
import os, sys, json, gc
src = open("/home/hatch/workspace/cape-jones-rig/workstream-b-sweep-20261031/build_sweep.py").read()
g = {"__name__": "build_new_poses"}
exec(src.split("\nresults = {}")[0], g)
C = g["C"]; build_sequence = g["build_sequence"]; save_video = g["save_video"]
contact = g["contact"]; write_xsheet = g["write_xsheet"]; render_key = g["render_key"]
OUT, FR, GREY = g["OUT"], g["FR"], g["GREY"]
from PIL import Image, ImageDraw

NEW = [
    ("nmp-01-hero-land-crouch", "HERO-LAND CROUCH (grounded landing, feet planted)",
     C((30, -70), (20, 60), (-35, 60), (20, -40)), 8, {"L": "chest"},
     "L fist down-forward over torso (chest pass), R arm swept back, deep asymmetric crouch. Not jump-land (arms-up) and not gul-01 compact crouch (both hands out)."),
    ("nmp-02-sky-point-salute", "SKY-POINT SALUTE (grounded standing)",
     C((-170, 60), (10, 120), (-15, 25), (10, -10)), -12, {},
     "L arm straight up pointing at the sky, R hand on hip, head tilted up to the pointing hand. Not jei-03 side-point (sideways) and not cap-01 entrance."),
    ("nmp-03-prowl-step", "PROWL STEP (grounded low crouch, moving forward)",
     C((-90, 40), (30, 90), (-70, 30), (70, -20)), 6, {"L": "chest"},
     "Asymmetric prowl: L arm reaching forward low over torso, R arm back, deep step-crouch. Not gul-02 focus (symmetric hands out) and not bur-01 dash (upright lean)."),
    ("nmp-04-overhead-smash-windup", "OVERHEAD SMASH WINDUP (grounded braced)",
     C((-170, 170), (20, -20), (-45, 45), (30, -30)), 6, {},
     "Both arms overhead and slightly inward (clasped-smash windup), legs braced wide, head forward-down. Not cap-02 spread (arms sideways) and not flex (arms bent at sides)."),
]
idxs = [int(a) for a in sys.argv[1:]] or list(range(4))
results = {}
if os.path.exists(os.path.join(OUT, "new-poses-20261031.json")):
    results = json.load(open(os.path.join(OUT, "new-poses-20261031.json")))
for ii in idxs:
    slug, title, cfg, head, sn, why = NEW[ii]
    key = {"name": title, "cfg": cfg, "head": head, "snap": sn}
    trim2, view2, rows2, (uw2, uh2), edge2 = build_sequence(slug, [key])
    save_video(slug + "-movement-20261031", view2)
    cp2 = contact(slug + "-movement-20261031", view2,
                  {0: "apose KEY", len(view2) // 2: "POSE KEY", len(view2) - 1: "apose KEY"})
    xs2 = write_xsheet(slug + "-movement-20261031", rows2)
    d2 = os.path.join(FR, slug); os.makedirs(d2, exist_ok=True)
    still = render_key(key)
    bb = still.getchannel("A").getbbox(); still_t = still.crop(bb)
    still_t.save(os.path.join(OUT, slug + "-key-still-20261031.png"))
    grey = Image.alpha_composite(Image.new("RGBA", still_t.size, GREY), still_t).convert("RGB")
    grey.save(os.path.join(OUT, slug + "-key-still-grey-20261031.png"))
    for i, (f, label, _) in enumerate(trim2):
        f.save(os.path.join(d2, f"f{i:03d}.png"))
    results[slug] = {"title": title, "frames": len(view2), "fps": 24, "seconds": round(len(view2) / 24, 2),
        "canvas": [uw2, uh2], "edge_alpha_px": edge2, "grounded_y_translation_all_zero": True,
        "method": "RIG-ANGLE snap.figure, easeInOutCubic, 7 inbetweens/transition, 2 breakdowns/transition, overshoot+settle real frames",
        "angles": cfg, "head": head, "snap": sn, "distinct_from": why,
        "classification": "ADDITIVE / EXTRA — not a production blocker",
        "approval": "0/1", "contact": os.path.basename(cp2), "xsheet": os.path.basename(xs2)}
    print(slug, results[slug]["frames"], "frames", flush=True)
    del trim2, view2, rows2, still, still_t, grey
    gc.collect()
# combined contact of the 4 key stills (only when all 4 exist)
if all(os.path.exists(os.path.join(OUT, NEW[i][0] + "-key-still-grey-20261031.png")) for i in range(4)):
    stills = [Image.open(os.path.join(OUT, NEW[i][0] + "-key-still-grey-20261031.png")).convert("RGB") for i in range(4)]
    tw = 360; th = int(360 * stills[0].size[1] / stills[0].size[0])
    sheet = Image.new("RGB", (tw * 4, th + 28), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
    for j, im in enumerate(stills):
        sheet.paste(im.resize((tw, th)), (j * tw, 28))
        dr.text((j * tw + 6, 6), NEW[j][0], fill=(255, 255, 0))
    sheet.save(os.path.join(OUT, "new-movement-poses-4-contact-20261031.png"))
    print("combined new-poses contact saved")
json.dump(results, open(os.path.join(OUT, "new-poses-20261031.json"), "w"), indent=1)
print("NEW POSES DONE:", sorted(results.keys()))
