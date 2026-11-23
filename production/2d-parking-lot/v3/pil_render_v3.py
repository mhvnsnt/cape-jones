#!/usr/bin/env python3
"""Render Rig Jones 2 (V3) puppet frames with PIL, from a v3 transforms
dump (Blender-computed bone math; PIL rasterises).
- Plane parts: same proven rules as rig/pil_render.py — rotate by
  rec["rot"] AS-IS (never negated), z-sorted paste, ortho screen map.
- Cape: ONE continuous mesh, warped per cell. Each grid cell is
  perspective-mapped from its source rect in Cape_Back_Main.png onto
  its deformed screen quad (numpy 8-point solve). Draw order: ground
  shadow (z -0.05) -> cape mesh (z 0.001) -> body planes by z.
- Self-check: at rest the warp must reproduce the unwarped cape
  exactly (run with --check-rest: compares the f1 warped cape against
  a plain whole-texture paste and reports mean/max pixel diff).
Usage: python3 v3-swap-system/pil_render_v3.py <transforms.json> <outdir>
       [f_start f_end] [--check-rest]
Output: <outdir>/f%04d.png (RGBA, transparent, 1280x720).
"""
import json
import os
import sys

import numpy as np
from PIL import Image

V3 = "/home/hatch/workspace/_cape-jones-parking-lot-2d/v3-swap-system"
WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"

transforms_path, OUT = sys.argv[1], sys.argv[2]
args = sys.argv[3:]
check_rest = "--check-rest" in args
args = [a for a in args if not a.startswith("--")]
start = int(args[0]) if len(args) > 0 else 1
end = int(args[1]) if len(args) > 1 else None

spec = json.load(open(transforms_path))
if end is None:
    end = spec["frames"]
os.makedirs(OUT, exist_ok=True)

# Load part art once. V3 image paths are //art/... relative to the
# v3-swap-system dir (the .blend lives there).
art = {}
for p in spec["parts"]:
    rel = p["image"].lstrip("/")
    path = os.path.join(V3, rel[2:] if rel.startswith("//") else rel)
    art[p["name"]] = Image.open(path).convert("RGBA")

# Image-swap textures (hand/mouth variants), loaded lazily by filename
# from the art dir and cached. The per-frame record's "tex" names the
# active image; the plane's base image is only a fallback.
_tex_cache = {}


def tex_image(fname):
    if fname not in _tex_cache:
        _tex_cache[fname] = Image.open(
            os.path.join(V3, "art", fname)).convert("RGBA")
    return _tex_cache[fname]

cape_spec = spec["cape"]
cape_tex = Image.open(os.path.join(V3, "art", "Cape_Back_Main.png")).convert("RGBA")
CW, CH = cape_tex.size
COLS, ROWS = cape_spec["cols"], cape_spec["rows"]

parts = sorted(spec["parts"], key=lambda p: p["z"])
cams = {c["frame"]: c for c in spec["cameras"]}
CAPE_Z = 0.001


def persp_coeffs(dst, src):
    """Coefficients mapping destination points -> source points.
    dst/src: 4 (x, y) pairs in order NW, NE, SE, SW. Solves the
    8-point perspective system (PIL PERSPECTIVE wants output->input)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        b.append(v)
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def render_cape(canvas, verts, cam):
    """Warp the cape texture through the dumped grid vertices."""
    ppu = 1280.0 / cam["ortho"]

    def scr(rx, ry):
        return (640 + (rx - cam["x"]) * ppu, 360 - (ry - cam["y"]) * ppu)

    for r in range(ROWS):
        for c in range(COLS):
            quad_rig = [verts[f"{c},{r}"], verts[f"{c + 1},{r}"],
                        verts[f"{c + 1},{r + 1}"], verts[f"{c},{r + 1}"]]
            quad = [scr(x, y) for x, y in quad_rig]
            xs = [q[0] for q in quad]
            ys = [q[1] for q in quad]
            bx0, by0 = int(min(xs)) - 1, int(min(ys)) - 1
            bx1, by1 = int(max(xs)) + 2, int(max(ys)) + 2
            if bx1 - bx0 < 2 or by1 - by0 < 2:
                continue
            # Source rect for this cell (row 0 = top of texture).
            su0, su1 = c * CW / COLS, (c + 1) * CW / COLS
            sv0, sv1 = r * CH / ROWS, (r + 1) * CH / ROWS
            src = [(su0, sv0), (su1, sv0), (su1, sv1), (su0, sv1)]
            # Destination corners in cell-canvas coords, same order.
            dst = [(q[0] - bx0, q[1] - by0) for q in quad]
            try:
                coeffs = persp_coeffs(dst, src)
            except np.linalg.LinAlgError:
                continue
            cell = cape_tex.transform((bx1 - bx0, by1 - by0),
                                      Image.PERSPECTIVE, coeffs,
                                      resample=Image.BICUBIC)
            canvas.paste(cell, (bx0, by0), cell)


def render_plane(canvas, p, rec, cam):
    # Image-swap slot: the per-frame "tex" is the active variant image
    # on the same plane. Otherwise the part's fixed image.
    im = tex_image(rec["tex"]) if rec.get("tex") else art[p["name"]]
    ppu = 1280.0 / cam["ortho"]
    sw = max(1, round(p["w"] * ppu))
    sh = max(1, round(p["h"] * ppu))
    im2 = im.resize((sw, sh), Image.LANCZOS)
    # VERIFIED rule from the fixed2 lane: rotate by rec["rot"] as-is,
    # never negated (negating mirrors every plane's rotation).
    if abs(rec["rot"]) > 0.01:
        im2 = im2.rotate(rec["rot"], resample=Image.BICUBIC, expand=True)
    cx = 640 + (rec["x"] - cam["x"]) * ppu
    cy = 360 - (rec["y"] - cam["y"]) * ppu
    canvas.paste(im2, (round(cx - im2.width / 2),
                       round(cy - im2.height / 2)), im2)


for f in range(start, end + 1):
    cam = cams[f]
    canvas = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    # Ground shadow first, then the one-piece cape, then body planes.
    for p in parts:
        if p["z"] >= CAPE_Z:
            break
        rec = p["frames"][f - 1]
        if not rec["hide"]:
            render_plane(canvas, p, rec, cam)
    render_cape(canvas, cape_spec["frames"][f - 1]["verts"], cam)
    for p in parts:
        if p["z"] < CAPE_Z:
            continue
        rec = p["frames"][f - 1]
        if not rec["hide"]:
            render_plane(canvas, p, rec, cam)
    canvas.save(f"{OUT}/f{f:04d}.png")
    if f % 30 == 0 or f == end:
        print(f"pil v3 frame {f} done")

if check_rest:
    # Rest-frame self-check: warped f1 cape vs plain whole-texture paste.
    cam = cams[1]
    ppu = 1280.0 / cam["ortho"]
    plain = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    tex = cape_tex.resize((round(cape_spec["w"] * ppu),
                           round(cape_spec["h"] * ppu)), Image.LANCZOS)
    cx = 640 + (0 - cam["x"]) * ppu
    cy = 360 - ((cape_spec["top"] - cape_spec["h"] / 2) - cam["y"]) * ppu
    plain.paste(tex, (round(cx - tex.width / 2),
                      round(cy - tex.height / 2)), tex)
    warped = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    render_cape(warped, cape_spec["frames"][0]["verts"], cam)
    import numpy as np
    a = np.asarray(plain).astype(int)
    b = np.asarray(warped).astype(int)
    diff = np.abs(a - b)
    print(f"REST CHECK f1 cape warp vs plain: mean abs diff "
          f"{diff.mean():.2f}, max {diff.max()}, "
          f"px>10: {(diff.max(axis=2) > 10).sum()}")
print("PIL V3 frames:", start, "->", end)
