"""Rebuild the coming-forward walk with snap layering applied.
Frozen builders are NOT edited: this is a new builder in a new folder
that calls snap_figure.figure() with a per-frame, per-side snap table
produced by gate_walk_snap.py's table (walk_snap_table.json).
Everything else is copied from the original walk, not changed:
same keys, same SEG=10 interpolation, same scales 0.70->1.60, same
1600x1800 canvas, same grey background + ground band, same
feet-on-GROUND_Y=1500 anchor (bbox bottom == ground line), same
24 fps GIF/MP4. The ONLY change is layer order per side per frame.
Usage: python3 build_walk_layer_fix.py   (requires walk_snap_table.json
in this folder; the gate must PASS on applied=fixed before this runs
-- see gate_walk_snap.py, run it first and check exit 0.)
"""
import os, sys, math, json, subprocess, importlib.util
from PIL import Image, ImageDraw
import numpy as np
RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "coming-forward-walk-layer-fix-20261031")
W, H = 1600, 1800
GROUND_Y = 1500
GREY = (128, 128, 128)
HERO_H = 700
spec = importlib.util.spec_from_file_location("snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

def alpha_bbox(im):
    a = np.array(im.split()[3])
    rows = np.where(a.max(axis=1) > 10)[0]; cols = np.where(a.max(axis=0) > 10)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())
def anchor_layer(fig, scale, squash_x=1.0):
    bx0, by0, bx1, by1 = alpha_bbox(fig); fig_h = by1 - by0 + 1
    plate_scale = (HERO_H * scale) / fig_h
    nw = max(1, int(fig.size[0] * plate_scale * squash_x)); nh = max(1, int(fig.size[1] * plate_scale))
    scaled = fig.resize((nw, nh), Image.LANCZOS)
    sx0, sy0, sx1, sy1 = alpha_bbox(scaled)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx = W // 2 - (sx0 + sx1) // 2; top = GROUND_Y - sy1
    layer.alpha_composite(scaled, (cx, top))
    lx0, ly0, lx1, ly1 = alpha_bbox(layer)
    return layer, {"feet_y": ly1, "bbox": [lx0, ly0, lx1, ly1],
                   "touches_edge": (lx0 <= 0 or ly0 <= 0 or lx1 >= W - 1 or ly1 >= H - 1),
                   "margin": min(lx0, ly0, W - 1 - lx1, H - 1 - ly1)}
def background(scale):
    bg = Image.new("RGB", (W, H), GREY); d = ImageDraw.Draw(bg)
    d.rectangle([0, GROUND_Y, W, H], fill=(96, 96, 96))
    d.line([(0, GROUND_Y), (W, GROUND_Y)], fill=(255, 255, 255), width=3)
    drift = int((scale - 1.0) * 0.3 * 400)
    for i, bx in enumerate([150, 450, 1050, 1350]):
        bw = 120 + 40 * (i % 2); x = bx - drift if bx < W // 2 else bx + drift
        d.rectangle([x, GROUND_Y - 180, x + bw, GROUND_Y], fill=(150, 150, 150))
    return bg
def compose(layer, scale):
    return Image.alpha_composite(background(scale).convert("RGBA"), layer).convert("RGB")
def smooth(t): return t * t * (3 - 2 * t)
def interp_cfg(a, b, t):
    return {k: {s: a[k][s] + (b[k][s] - a[k][s]) * smooth(t) for s in ("L", "R")} for k in a}

def main():
    table_path = os.path.join(OUT, "walk_snap_table.json")
    if not os.path.exists(table_path):
        print(f"MISSING {table_path} -- run the measurement + gate steps first"); return 2
    rows = json.load(open(table_path))
    snap_by_frame = {}
    for r in rows:
        snap_by_frame.setdefault(r["frame"], {})[r["side"]] = r["applied_fixed"]
    # Gate must pass before building: call gate_walk_snap.py as a subprocess.
    gate = subprocess.run([sys.executable, os.path.join(OUT, "gate_walk_snap.py"),
                           "--table", table_path, "--applied", "fixed",
                           "--out", os.path.join(OUT, "gate_fixed.json")])
    if gate.returncode != 0:
        print("GATE FAILED on applied=fixed -- refusing to build"); return gate.returncode
    CONTACT_L = {"arm_upper": {"L": 20, "R": -20}, "arm_lower": {"L": -30, "R": 30}, "leg_upper": {"L": -28, "R": 22}, "leg_lower": {"L": 5, "R": 15}}
    PASSING = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": -10, "R": 10}, "leg_upper": {"L": 0, "R": 5}, "leg_lower": {"L": 15, "R": 5}}
    CONTACT_R = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30}, "leg_upper": {"L": 22, "R": -28}, "leg_lower": {"L": 15, "R": 5}}
    walk_keys = [(CONTACT_L, 0.70, "CONTACT-L"), (PASSING, 0.95, "PASSING"), (CONTACT_R, 1.20, "CONTACT-R"), (PASSING, 1.40, "PASSING"), (CONTACT_L, 1.60, "CONTACT-L")]
    frames, meas, phases = [], [], []
    SEG = 10
    for ki in range(len(walk_keys) - 1):
        cfg_a, s_a, lab_a = walk_keys[ki]; cfg_b, s_b, lab_b = walk_keys[ki + 1]
        for i in range(SEG):
            t = i / SEG; cfg = interp_cfg(cfg_a, cfg_b, t); s = s_a + (s_b - s_a) * smooth(t)
            fi = len(frames)
            snapd = {side: v for side, v in snap_by_frame.get(fi, {}).items() if v != "none"}
            fig = snap.figure(550, cfg, snap=snapd)
            layer, m = anchor_layer(fig, s)
            frames.append(compose(layer, s)); phases.append(lab_a if i == 0 else "INBETWEEN")
            m.update({"frame": fi, "scale": round(s, 4), "phase": phases[-1], "snap": snapd}); meas.append(m)
            layer.save(os.path.join(OUT, "frames-transparent", f"f{fi:03d}.png")) if False else None
    fig = snap.figure(550, CONTACT_L, snap={s: v for s, v in snap_by_frame.get(40, {}).items() if v != "none"})
    for _ in range(4):
        fi = len(frames); layer, m = anchor_layer(fig, 1.60)
        frames.append(compose(layer, 1.60)); phases.append("CONTACT-L-HOLD")
        m.update({"frame": fi, "scale": 1.60, "phase": "CONTACT-L-HOLD", "snap": snap_by_frame.get(40, {})}); meas.append(m)
    os.makedirs(os.path.join(OUT, "frames-fixed"), exist_ok=True)
    for i, f in enumerate(frames): f.save(os.path.join(OUT, "frames-fixed", f"f{i:03d}.jpg"), quality=92)
    gif = os.path.join(OUT, "coming-forward-walk-LAYER-FIXED-20261031.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=int(1000/24), loop=0)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(frames): f.save(os.path.join(td, f"f{i:03d}.jpg"), quality=92)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(td, "f%03d.jpg"),
                        "-vf", f"scale={W}:{H},format=yuv420p", "-c:v", "libx264",
                        os.path.join(OUT, "coming-forward-walk-LAYER-FIXED-20261031.mp4")], check=True)
    feet = [m["feet_y"] for m in meas]
    report = {"frames": len(frames), "fps": 24, "feet_y_min": min(feet), "feet_y_max": max(feet),
              "feet_y_spread_px": max(feet)-min(feet), "touches_edge_frames": [m["frame"] for m in meas if m["touches_edge"]],
              "min_margin_px": min(m["margin"] for m in meas),
              "PASS": (max(feet)-min(feet) <= 1) and not any(m["touches_edge"] for m in meas),
              "measurements": meas}
    json.dump(report, open(os.path.join(OUT, "fixed_walk_measurements.json"), "w"), indent=2)
    print("BUILT", len(frames), "frames, feet spread", max(feet)-min(feet), "PASS", report["PASS"])
    return 0
if __name__ == "__main__":
    sys.exit(main())
