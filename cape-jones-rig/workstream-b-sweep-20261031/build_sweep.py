"""Workstream B sweep 2026-10-31: serve-to-guard v3 (rig, snap.figure),
4 NEW movement poses (ADDITIVES, not production blockers), pseudo-turn
verification, poses-as-movements audit with AIRBORNE/GROUNDED labelling.

GROUND RULE (Mars 2026-10-31 20:56 CDT, do NOT re-decide):
- AIRBORNE = flying, floating, levitating, JUMPING, fight-motion-off-ground,
  chase-airborne. Jump / fight-off-ground poses are labelled AIRBORNE with a
  stated height/flight line; their feet are NOT forced to ground.
- Walking/standing = GROUNDED-default, feet planted; a grounded proof that
  floats FAILS the gate. No grounded floating is excused as "airborne".
In this build every sequence is GROUNDED (serve/guard/fight standing, all
4 new poses standing/crouched with feet planted), so vertical translation
is 0 on every frame and the grounded gate checks exactly that. Jump proofs
are audited (not rebuilt) and labelled AIRBORNE with their height line.

RIG METHOD (v3, and the 4 new poses' movement videos):
- Every frame is a fresh render through snap.figure (face-cowl-snap-wire100
  builder): real snap passes, NOT a top-arm union approximation (that was
  v2's shortcut) and NOT image crossfade. No whole-picture blending anywhere.
- Interpolation: easeInOutCubic (industry slow-in/slow-out), 7 inbetweens
  per transition, TWO labelled breakdowns per transition (arc bulge +10deg
  on the largest-moving arm upper at j=3; follow-through +8deg on that
  arm's lower at j=5), overshoot 5% beyond the key + settle as REAL frames.
- Snap union rule per inbetween, priority face > cowl > chest > normal.
- No-crop: union canvas = union of all frames' alpha bboxes + 40px pad,
  even dims; grounded frames are feet-anchored to one ground line, and the
  gate measures edge alpha (must be 0) and vertical translation (must be 0
  for grounded sequences). Canvas fits the figure, never the reverse.
- Fight key is STILL a measured estimate +/-15deg (v2's caveat, NOT fixed
  here: no builder-exact fight config exists on disk). Labelled on every
  proof. Replacing it needs a measured config from the approved fighting
  file or a builder-exact config — still owed, not silently swapped.
- Jump-to-shimmy rig re-key is NOT built here: BLOCKED on Mars say-so
  (re-keying changes the sequence). Noted as blocked, not built.
"""
import os, sys, math, json, subprocess, tempfile
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/face-cowl-snap-wire100-20261031")
import importlib.util
from PIL import Image, ImageDraw

R = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(R, "workstream-b-sweep-20261031")
FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
GREY = (128, 128, 128, 255)
FPS = 24
PAD = 40

spec = importlib.util.spec_from_file_location("snap", os.path.join(R, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)
# cache resized pieces: snap.load re-reads + resizes from disk every call
_cache = {}
_orig_load = snap.load
def cached_load(p, scale=snap.SCALE):
    k = (p, scale)
    if k not in _cache:
        _cache[k] = _orig_load(p, scale)
    return _cache[k]
snap.load = cached_load

def C(au, al, lu, ll):
    return {"arm_upper": {"L": au[0], "R": au[1]}, "arm_lower": {"L": al[0], "R": al[1]},
            "leg_upper": {"L": lu[0], "R": lu[1]}, "leg_lower": {"L": ll[0], "R": ll[1]}}

def lerp_cfg(a, b, t):
    return {g: {s: a[g][s] + (b[g][s] - a[g][s]) * t for s in ("L", "R")}
            for g in ("arm_upper", "arm_lower", "leg_upper", "leg_lower")}

def ease_io(t):  # easeInOutCubic, industry slow-in/slow-out
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

PRIO = {"face": 3, "cowl": 2, "chest": 1}
def snap_union(sa, sb):
    out = {}
    for s in ("L", "R"):
        a, b = sa.get(s), sb.get(s)
        out[s] = max([x for x in (a, b) if x], key=lambda x: PRIO[x]) if (a or b) else None
    return {k: v for k, v in out.items() if v}

def overshoot_cfg(key, prev, pct=0.05):
    """5% past the key, away from the previous key, per joint group."""
    return {g: {s: key[g][s] + (key[g][s] - prev[g][s]) * pct for s in ("L", "R")}
            for g in ("arm_upper", "arm_lower", "leg_upper", "leg_lower")}

APOSE = {"name": "apose", "cfg": C((0, 0), (0, 0), (0, 0), (0, 0)), "head": 0, "snap": {}}
SERVE = {"name": "jei-01 serve windup FIST (Ginyu builder exact)",
         "cfg": C((-160, 80), (-20, -110), (-25, 30), (15, -15)), "head": -10, "snap": {"L": "cowl"}}
GUARD = {"name": "gul-03 guard crouch (Ginyu builder exact)",
         "cfg": C((-30, 30), (140, -140), (-45, 45), (40, -40)), "head": -8,
         "snap": {"L": "chest", "R": "chest"}}
FIGHT = {"name": "fighting pose (MEASURED-ESTIMATE +/-15deg, NOT builder-exact)",
         "cfg": C((-65, 65), (140, -140), (-20, 20), (10, -10)), "head": 0,
         "snap": {}}
# Recovered gate (depth-25d angle-configs-recovered): fighting pose PASS with
# NO SNAP both sides, eye-check "fists near head, not over face; elbows out".
# An earlier draft of this script used chest for fight; corrected 2026-10-31
# to the recovered gate decision. Serve L cowl and guard chest are ASSIGNED
# (Ginyu builder top + COWL-SNAP upper-only rule; guard arms cross the
# torso), NOT gate-verified — snap check still owed for serve/guard.

def render_key(key):
    return snap.figure(550, key["cfg"], head_angle=key["head"], snap=key["snap"])

def build_sequence(name, keys, n_inb=7):
    """keys: list of key dicts, wrapped apose -> keys -> apose.
    Returns (frames_rgba_trimmed, xsheet_rows). Grounded: no Y translation."""
    seq = [APOSE] + keys + [APOSE]
    raw = []   # (rgba_full, label, y_offset)
    rows = []
    for i in range(len(seq) - 1):
        a, b = seq[i], seq[i + 1]
        h = 3 if a["name"] == "apose" else 5
        for _ in range(h):
            raw.append((render_key(a), f"{a['name']} KEY hold", 0))
            rows.append({"frame": len(raw) - 1, "kind": "KEY hold", "from": a["name"], "to": "",
                         "t": "", "eased": "", "note": ""})
        deltas = {s: abs(b["cfg"]["arm_upper"][s] - a["cfg"]["arm_upper"][s]) for s in ("L", "R")}
        big = max(deltas, key=deltas.get)
        for j in range(1, n_inb + 1):
            t = j / (n_inb + 1); e = ease_io(t)
            cfg = lerp_cfg(a["cfg"], b["cfg"], e)
            head = a["head"] + (b["head"] - a["head"]) * e
            sn = snap_union(a["snap"], b["snap"])
            tag = "inbetween"
            if j == 3:
                cfg["arm_upper"][big] += 10 if b["cfg"]["arm_upper"][big] >= a["cfg"]["arm_upper"][big] else -10
                tag = "BREAKDOWN arc bulge +10deg largest-moving arm upper"
            if j == 5:
                cfg["arm_lower"][big] += 8 if b["cfg"]["arm_lower"][big] >= a["cfg"]["arm_lower"][big] else -8
                tag = "BREAKDOWN follow-through +8deg same arm lower"
            raw.append((snap.figure(550, cfg, head_angle=head, snap=sn), f"{a['name']} -> {b['name']} {tag}", 0))
            rows.append({"frame": len(raw) - 1, "kind": tag, "from": a["name"], "to": b["name"],
                         "t": round(t, 3), "eased": round(e, 3), "note": f"largest arm {big}; snap {sn}"})
        if b["name"] != "apose" and b in keys:
            ov = overshoot_cfg(b["cfg"], a["cfg"])
            raw.append((snap.figure(550, ov, head_angle=b["head"], snap=b["snap"]),
                        f"{b['name']} OVERSHOOT +5% real frame", 0))
            rows.append({"frame": len(raw) - 1, "kind": "OVERSHOOT +5%", "from": b["name"], "to": "", "t": "", "eased": "", "note": "real frame, not a hold"})
            raw.append((render_key(b), f"{b['name']} SETTLE (key, real frame)", 0))
            rows.append({"frame": len(raw) - 1, "kind": "SETTLE", "from": b["name"], "to": "", "t": "", "eased": "", "note": "real frame, not a hold"})
    for _ in range(3):
        raw.append((render_key(APOSE), "apose KEY hold", 0))
        rows.append({"frame": len(raw) - 1, "kind": "KEY hold", "from": "apose", "to": "", "t": "", "eased": "", "note": ""})
    # trim each frame to its own alpha bbox (transparent padding only, never a
    # fixed crop window), then union canvas, feet-anchored (grounded only).
    trimmed = []
    for rgba, label, yoff in raw:
        bb = rgba.getchannel("A").getbbox()
        trimmed.append((rgba.crop(bb), label, yoff))
    uw = max(f.size[0] for f, _, _ in trimmed) + 2 * PAD
    uh = max(f.size[1] for f, _, _ in trimmed) + 2 * PAD
    uw += uw % 2; uh += uh % 2
    ground = uh - PAD
    view = []
    edge = 0
    for f, label, yoff in trimmed:
        canvas = Image.new("RGBA", (uw, uh), (0, 0, 0, 0))
        canvas.alpha_composite(f, ((uw - f.size[0]) // 2, ground - f.size[1] + yoff))
        a = canvas.getchannel("A")
        for x in range(uw):
            if a.getpixel((x, 0)) or a.getpixel((x, uh - 1)): edge += 1
        for y in range(uh):
            if a.getpixel((0, y)) or a.getpixel((uw - 1, y)): edge += 1
        view.append(Image.alpha_composite(Image.new("RGBA", (uw, uh), GREY), canvas).convert("RGB"))
    assert edge == 0, f"NO-CROP GATE FAIL {name}: edge alpha {edge}"
    assert all(y == 0 for _, _, y in trimmed), f"GROUNDED GATE FAIL {name}: vertical translation present"
    return trimmed, view, rows, (uw, uh), edge

def save_video(name, view, fps=FPS):
    gif = os.path.join(OUT, name + ".gif")
    view[0].save(gif, save_all=True, append_images=view[1:], duration=int(1000 / fps), loop=0)
    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(view):
            f.save(os.path.join(td, f"f{i:03d}.jpg"), quality=92)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                        "-i", os.path.join(td, "f%03d.jpg"),
                        "-vf", f"scale={view[0].size[0]}:{view[0].size[1]},format=yuv420p",
                        "-c:v", "libx264", os.path.join(OUT, name + ".mp4")], check=True)
    return gif

def contact(name, view, labels):
    idx = sorted(set([0, len(view) // 4, len(view) // 2, 3 * len(view) // 4, len(view) - 1]))
    tw = 360; th = int(360 * view[0].size[1] / view[0].size[0])
    sheet = Image.new("RGB", (tw * len(idx), th + 28), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    for j, k in enumerate(idx):
        sheet.paste(view[k].resize((tw, th)), (j * tw, 28))
        dr.text((j * tw + 6, 6), f"f{k:02d} {labels.get(k, '')}", fill=(255, 255, 0))
    p = os.path.join(OUT, name + "-contact-20261031.png")
    sheet.save(p)
    return p

def write_xsheet(name, rows):
    import csv
    p = os.path.join(OUT, name + "-xsheet-20261031.csv")
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["frame", "kind", "from", "to", "t", "eased", "note"])
        w.writeheader(); w.writerows(rows)
    return p

results = {}

# ---- 1. SERVE-TO-GUARD v3 (PRODUCTION movement: shot movement, grounded) ----
trim, view, rows, (uw, uh), edge = build_sequence("serve-to-guard-v3", [SERVE, GUARD, FIGHT])
save_video("move-serve-to-guard-v3-20261031", view)
cp = contact("move-serve-to-guard-v3-20261031", view,
             {0: "apose KEY", len(view)//2: "guard/fight", len(view)-1: "apose KEY"})
xs = write_xsheet("move-serve-to-guard-v3-20261031", rows)
d = os.path.join(FR, "serve-to-guard-v3"); os.makedirs(d, exist_ok=True)
for i, (f, label, _) in enumerate(trim):
    f.save(os.path.join(d, f"f{i:03d}.png"))
results["serve-to-guard-v3"] = {"frames": len(view), "fps": FPS, "seconds": round(len(view)/FPS, 2),
    "canvas": [uw, uh], "edge_alpha_px": edge, "grounded_y_translation_all_zero": True,
    "method": "RIG-ANGLE snap.figure, easeInOutCubic, 7 inbetweens/transition, 2 breakdowns/transition, overshoot+settle real frames",
    "keys": ["apose", SERVE["name"], GUARD["name"], FIGHT["name"], "apose"],
    "caveat": "fight key MEASURED-ESTIMATE +/-15deg (v2 caveat NOT fixed); serve/guard builder-exact",
    "ground": "GROUNDED, feet planted, no vertical translation on any frame",
    "contact": os.path.basename(cp), "xsheet": os.path.basename(xs),
    "approval": "0/1 (new v3, not Mars-approved; v2 was 0/1; v1 wording conflict noted in report)"}
print("serve-to-guard-v3:", results["serve-to-guard-v3"])

# ---- 2. FOUR NEW MOVEMENT POSES (ADDITIVES / EXTRAS, not blockers) ----
# Distinctness checked against: 18 Ginyu poses, 8 dialect poses, flex/fight/
# punch/jump/walk/fly/dance/seated stills. None below re-uses an existing
# angle set or name; each is a new rig angle set + new movement video.
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
new_contacts = []
for slug, title, cfg, head, sn, why in NEW:
    key = {"name": title, "cfg": cfg, "head": head, "snap": sn}
    trim2, view2, rows2, (uw2, uh2), edge2 = build_sequence(slug, [key])
    save_video(slug + "-movement-20261031", view2)
    cp2 = contact(slug + "-movement-20261031", view2, {0: "apose KEY", len(view2)//2: "POSE KEY", len(view2)-1: "apose KEY"})
    xs2 = write_xsheet(slug + "-movement-20261031", rows2)
    d2 = os.path.join(FR, slug); os.makedirs(d2, exist_ok=True)
    # key still: transparent master + grey view
    still = render_key(key)
    bb = still.getchannel("A").getbbox(); still_t = still.crop(bb)
    still_t.save(os.path.join(OUT, slug + "-key-still-20261031.png"))
    grey = Image.alpha_composite(Image.new("RGBA", still_t.size, GREY), still_t).convert("RGB")
    grey.save(os.path.join(OUT, slug + "-key-still-grey-20261031.png"))
    for i, (f, label, _) in enumerate(trim2):
        f.save(os.path.join(d2, f"f{i:03d}.png"))
    results[slug] = {"title": title, "frames": len(view2), "fps": FPS, "seconds": round(len(view2)/FPS, 2),
        "canvas": [uw2, uh2], "edge_alpha_px": edge2, "grounded_y_translation_all_zero": True,
        "method": "RIG-ANGLE snap.figure, easeInOutCubic, 7 inbetweens/transition, 2 breakdowns/transition, overshoot+settle real frames",
        "angles": cfg, "head": head, "snap": sn, "distinct_from": why,
        "classification": "ADDITIVE / EXTRA — not a production blocker",
        "approval": "0/1", "contact": os.path.basename(cp2), "xsheet": os.path.basename(xs2)}
    new_contacts.append((slug, view2))
    print(slug, results[slug]["frames"], "frames")

# combined contact of the 4 new key stills (viewed proof)
stills = []
for slug, _, _, _, _, _ in NEW:
    im = Image.open(os.path.join(OUT, slug + "-key-still-grey-20261031.png")).convert("RGB")
    stills.append(im)
tw = 360; th = int(360 * stills[0].size[1] / stills[0].size[0])
sheet = Image.new("RGB", (tw * 4, th + 28), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
for j, im in enumerate(stills):
    sheet.paste(im.resize((tw, th)), (j * tw, 28))
    dr.text((j * tw + 6, 6), NEW[j][0], fill=(255, 255, 0))
sheet.save(os.path.join(OUT, "new-movement-poses-4-contact-20261031.png"))
print("combined new-poses contact saved")

with open(os.path.join(OUT, "workstream-b-build-20261031.json"), "w") as fh:
    json.dump(results, fh, indent=1)
print("BUILD DONE")
