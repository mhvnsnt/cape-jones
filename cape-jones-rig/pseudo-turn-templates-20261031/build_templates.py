"""Pseudo-turn template pack. Parameters, not hard-coded one-offs.
Source method (original): snap.figure angle interpolation, width squash
sine 1.0->0.62->1.0, head tilt to -10, arm layer flip at t>=0.5.
All frames are RGBA transparent masters; GIF/MP4 are view copies on a
neutral grey canvas sized as the UNION of all frames in that template,
so no frame is ever clipped (no crop window)."""
import os, sys, math, json, subprocess, tempfile
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/face-cowl-snap-wire100-20261031")
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import importlib.util
spec = importlib.util.spec_from_file_location("snap", "/home/hatch/workspace/cape-jones-rig/face-cowl-snap-wire100-20261031/snap_figure.py")
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

OUT = "/home/hatch/workspace/cape-jones-rig/pseudo-turn-templates-20261031"
GREY = (128, 128, 128, 255)
APOSE = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": 0, "R": 0}, "leg_upper": {"L": 0, "R": 0}, "leg_lower": {"L": 0, "R": 0}}
TURNED = {"arm_upper": {"L": -40, "R": 60}, "arm_lower": {"L": 90, "R": -110}, "leg_upper": {"L": -15, "R": 20}, "leg_lower": {"L": 10, "R": -10}}
def interp(a, b, t):
    return {k: {s: a[k][s] + (b[k][s] - a[k][s]) * t for s in ("L", "R")} for k in a}
def smooth(t):  # smoothstep slow-in/out
    return t * t * (3 - 2 * t)

_FIG_CACHE = {}
def base_fig(angles, head_angle=0, snap_cfg=None):
    """snap.figure returns 1100x1500; trim to alpha bbox (transparent padding
    only, computed from the figure itself -- never a fixed crop window).
    Identical angle/head/snap keys reuse one build (cheat-a reuses pseudo)."""
    key = (json.dumps(angles, sort_keys=True), head_angle, json.dumps(snap_cfg or {}, sort_keys=True))
    if key not in _FIG_CACHE:
        fig = snap.figure(550, angles, head_angle=head_angle, snap=snap_cfg or {})
        _FIG_CACHE[key] = fig.crop(fig.getchannel("A").getbbox())
    return _FIG_CACHE[key].copy()

BASE = base_fig(APOSE)
BASE_BBOX = BASE.size
print("base cropped figure:", BASE.size)

def transform(fig, sx, sy, darken=1.0, mirror=False):
    f = fig.copy()
    if mirror:
        f = f.transpose(Image.FLIP_LEFT_RIGHT)
    w, h = f.size
    f = f.resize((max(2, int(w * sx)), max(2, int(h * sy))), Image.LANCZOS)
    if darken != 1.0:
        r, g, b, a = f.split()
        f = Image.merge("RGBA", (r.point(lambda v: int(v * darken)), g.point(lambda v: int(v * darken)),
                                  b.point(lambda v: int(v * darken)), a))
    return f

def bend_warp(fig, amt):
    """Lattice/plastic-equivalent: horizontal shift varying with height."""
    w, h = fig.size
    out = Image.new("RGBA", (w + abs(amt) * 2, h), (0, 0, 0, 0))
    for y in range(0, h, 2):
        shift = int(amt * math.sin(math.pi * y / max(1, h)))
        out.alpha_composite(fig.crop((0, y, w, y + 2)), (abs(amt) + shift, y))
    return out

def outline_of(fig, hard=(180, 245, 255, 255), soft=(0, 200, 255, 153)):
    """Light outline from the UNSQUASHED silhouette: hard ring + one soft halo.
    Frozen at full width on purpose for INVISIBLE-POWER: the outline must
    survive the body squashing to zero, or it would vanish with it."""
    a = fig.getchannel("A")
    hard_ring = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(13)), a)
    soft_halo = a.filter(ImageFilter.MaxFilter(29)).filter(ImageFilter.GaussianBlur(6))
    soft_halo = ImageChops.subtract(soft_halo, a)
    out = Image.new("RGBA", fig.size, (0, 0, 0, 0))
    for mask, col in ((soft_halo, soft), (hard_ring, hard)):
        layer = Image.new("RGBA", fig.size, col)
        layer.putalpha(mask)
        out.alpha_composite(layer)
    return out

OUTLINE = outline_of(BASE)

def finish(name, frames_rgba, fps=12, labels=None):
    """Union canvas, feet-anchored, no clipping. Saves transparent PNGs,
    GIF + MP4 view copies, and a contact sheet."""
    d = os.path.join(OUT, "frames", name); os.makedirs(d, exist_ok=True)
    pad = 24
    uw = max(f.size[0] for f in frames_rgba) + 2 * pad
    uh = max(f.size[1] for f in frames_rgba) + 2 * pad
    uw += uw % 2; uh += uh % 2  # libx264 requires even dimensions
    ground = uh - pad  # feet line
    view = []
    for i, f in enumerate(frames_rgba):
        # feet-anchored paste: bottom of figure sits on the ground line
        canvas = Image.new("RGBA", (uw, uh), (0, 0, 0, 0))
        canvas.alpha_composite(f, ((uw - f.size[0]) // 2, ground - f.size[1]))
        canvas.save(os.path.join(d, f"f{i:02d}.png"))
        view.append(Image.alpha_composite(Image.new("RGBA", (uw, uh), GREY), canvas).convert("RGB"))
    gif = os.path.join(OUT, name + ".gif")
    view[0].save(gif, save_all=True, append_images=view[1:], duration=int(1000 / fps), loop=0)
    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(view):
            f.save(os.path.join(td, f"f{i:03d}.jpg"), quality=92)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(td, "f%03d.jpg"),
                        "-vf", f"scale={uw}:{uh},format=yuv420p", "-c:v", "libx264", os.path.join(OUT, name + ".mp4")], check=True)
    # contact: first, 1/4, mid, 3/4, last, labelled
    idx = sorted(set([0, len(view) // 4, len(view) // 2, 3 * len(view) // 4, len(view) - 1]))
    tw, th = 360, int(360 * uh / uw)
    contact = Image.new("RGB", (tw * len(idx), th + 28), (20, 20, 20))
    dr = ImageDraw.Draw(contact)
    for j, k in enumerate(idx):
        contact.paste(view[k].resize((tw, th)), (j * tw, 28))
        dr.text((j * tw + 6, 6), f"f{k:02d}" + (f" {labels[k]}" if labels and labels.get(k) else ""), fill=(255, 255, 0))
    contact.save(os.path.join(OUT, name + "-contact-20261031.png"))
    # no-clip gate: no alpha on union-canvas edge, and unsquashed frame intact
    edge = 0
    for f in frames_rgba:
        c = Image.new("RGBA", (uw, uh), (0, 0, 0, 0))
        c.alpha_composite(f, ((uw - f.size[0]) // 2, ground - f.size[1]))
        a = c.getchannel("A")
        edge += sum(1 for x in range(uw) if a.getpixel((x, 0)) or a.getpixel((x, uh - 1)))
        edge += sum(1 for y in range(uh) if a.getpixel((0, y)) or a.getpixel((uw - 1, y)))
    print(name, len(frames_rgba), "frames", uw, "x", uh, "edge_alpha_px:", edge)
    assert edge == 0, f"CLIP GATE FAIL {name}"
    return {"name": name, "frames": len(frames_rgba), "fps": fps, "canvas": [uw, uh], "edge_alpha_px": edge}

results = {}
# 1. PSEUDO-TURN (base, parameterised, re-runnable on any pose)
fr = []
for i in range(13):
    t = i / 12; s = smooth(t)
    squash = 1.0 - 0.38 * math.sin(math.pi * t)
    cfg = {"L": "chest", "R": "normal"} if t < 0.5 else {"L": "normal", "R": "chest"}
    fr.append(transform(base_fig(interp(APOSE, TURNED, s), head_angle=int(-10 * s), snap_cfg=cfg), squash, 1.0))
results["pseudo-turn"] = finish("pseudo-turn", fr, labels={0: "front", 6: "mid squash .62 + flip", 12: "front again"})
# 2. STRETCH (power): taller, slightly narrower, volume-preserving feel
fr = []
for i in range(13):
    t = i / 12
    sy = 1.0 + 0.40 * math.sin(math.pi * t); sx = 1.0 - 0.10 * math.sin(math.pi * t)
    fr.append(transform(BASE, sx, sy))
results["stretch-power"] = finish("stretch-power", fr, labels={0: "normal", 6: "stretched 1.40x tall", 12: "normal"})
# 3. THIN (power): narrower than pseudo-turn midpoint, near-normal height
fr = []
for i in range(13):
    t = i / 12
    sx = 1.0 - 0.55 * math.sin(math.pi * t); sy = 1.0 + 0.05 * math.sin(math.pi * t)
    fr.append(transform(BASE, sx, sy))
results["thin-power"] = finish("thin-power", fr, labels={0: "normal", 6: "thin 0.45x wide", 12: "normal"})
# 4. INVISIBLE-POWER: body squashes to ~0, frozen light outline stays, then returns
fr = []
for i in range(17):
    if i < 8:      # squash out
        sx = 1.0 - 0.98 * smooth(i / 7); body = transform(BASE, sx, 1.0)
        # outline fades in as body fades out (cross of the two, outline frozen full-width)
        op = int(255 * smooth(i / 7))
        o = OUTLINE.copy(); o.putalpha(o.getchannel("A").point(lambda v: v * op // 255))
        comp = Image.new("RGBA", BASE.size, (0, 0, 0, 0)); comp.alpha_composite(body, ((BASE.size[0] - body.size[0]) // 2, 0)); comp.alpha_composite(o, (0, 0))
        fr.append(comp)
    elif i < 12:   # invisible hold: outline only
        fr.append(OUTLINE.copy())
    else:          # return
        sx = 0.02 + 0.98 * smooth((i - 12) / 4); body = transform(BASE, sx, 1.0)
        op = int(255 * (1 - smooth((i - 12) / 4)))
        o = OUTLINE.copy(); o.putalpha(o.getchannel("A").point(lambda v: v * op // 255))
        comp = Image.new("RGBA", BASE.size, (0, 0, 0, 0)); comp.alpha_composite(body, ((BASE.size[0] - body.size[0]) // 2, 0)); comp.alpha_composite(o, (0, 0))
        fr.append(comp)
results["invisible-power"] = finish("invisible-power", fr, labels={0: "visible", 8: "OUTLINE ONLY", 11: "OUTLINE ONLY", 16: "visible"})
# 5. CHEAT-TURN-A: squash + layer flip + depth-by-scale + far-side dark at midpoint
fr = []
for i in range(13):
    t = i / 12; s = smooth(t); mid = math.sin(math.pi * t)
    squash = 1.0 - 0.38 * mid
    cfg = {"L": "chest", "R": "normal"} if t < 0.5 else {"L": "normal", "R": "chest"}
    fig = base_fig(interp(APOSE, TURNED, s), head_angle=int(-10 * s), snap_cfg=cfg)
    fig = transform(fig, squash * (1.0 - 0.20 * mid), 1.0 - 0.20 * mid, darken=1.0 - 0.25 * mid)
    fr.append(fig)
results["cheat-turn-a-depth-dark"] = finish("cheat-turn-a-depth-dark", fr, labels={0: "front", 6: "mid: squash+scale+dark", 12: "front"})
# 6. CHEAT-TURN-B: squash + bend warp (lattice/plastic-equivalent) + mirror at midpoint
fr = []
for i in range(13):
    t = i / 12; s = smooth(t); mid = math.sin(math.pi * t)
    squash = 1.0 - 0.38 * mid
    fig = base_fig(interp(APOSE, TURNED, s), head_angle=int(-10 * s))
    fig = bend_warp(transform(fig, squash, 1.0), int(30 * mid))
    if t >= 0.5:
        fig = fig.transpose(Image.FLIP_LEFT_RIGHT)
    fr.append(fig)
results["cheat-turn-b-bend-mirror"] = finish("cheat-turn-b-bend-mirror", fr, labels={0: "front", 6: "mid: bend+mirror", 12: "mirrored front"})
# 7. SHEET-ANIMATED turn attempt: rig keys from sheet pieces, in turn order.
# Keys are real snap angle sets (sheet pieces, no new art drawn). Midpoint is
# squash, NOT a side drawing: there is no true side torso/head piece.
KEYS = [APOSE, TURNED, {"arm_upper": {"L": 60, "R": -40}, "arm_lower": {"L": -110, "R": 90}, "leg_upper": {"L": 20, "R": -15}, "leg_lower": {"L": -10, "R": 10}}, APOSE]
fr = []
for ki in range(len(KEYS) - 1):
    for j in range(5):
        t = j / 5; s = smooth(t)
        squash = 1.0 - 0.38 * math.sin(math.pi * (ki + t) / 3)
        cfg = {"L": "chest", "R": "normal"} if (ki + t) < 1.5 else {"L": "normal", "R": "chest"}
        fr.append(transform(base_fig(interp(KEYS[ki], KEYS[ki + 1], s), head_angle=int(-10 * (ki + t) / 3), snap_cfg=cfg), squash, 1.0))
results["sheet-animated-turn-attempt"] = finish("sheet-animated-turn-attempt", fr, labels={0: "front key", 5: "turned key", 10: "mirrored key", 14: "front key"})
with open(os.path.join(OUT, "templates-20261031.json"), "w") as fh:
    json.dump({"base_figure_cropped_px": BASE_BBOX, "results": results,
               "note": "CHEAT and POWER templates are NOT true turns. No true side torso/head piece exists; true hand-drawn turn master still owed."}, fh, indent=2)
print(json.dumps(results, indent=2))
