#!/usr/bin/env python3
"""Clean mouth pipeline, v1 — 2026-10-31.
Stages, in order, no hand-tool step anywhere:
 1. COLOUR DECONTAMINATION: keep only mouth colours (dark <90, orange
    tongue, white teeth); drop JPEG fringe. Alpha threshold >=128 on
    resize, so semi-transparent fringe never darkens skin.
 2. COMPONENT SELECTION (garbage matte): keep only the mouth-body
    component(s) named by the caller; drop face/jaw/cheek components.
 3. VECTOR LINE FIT (thin-line mouths only): extract per-column
    centreline from ORIGINAL fragments only, fit a smoothing cubic
    spline (scipy UnivariateSpline), convert sampled spline points to
    cubic Bezier segments (Catmull-Rom -> Bezier), write a real .svg,
    rasterise at 8x supersample and downscale with LANCZOS. No pixel
    bridge, no straight hand-drawn stroke, no PIL vector mouth invented:
    the curve is fitted to measured original centreline points.
 4. PLACEMENT: alpha-bbox centre anchor, single target (231.5, 504.5),
    placed sizes from the approved PAH GO set (MBP 178x23, AH 196x67,
    GK 188x30) or the v2 fitted size x0.75 rule for new packs.
 5. GATES (gate_mouth.py): continuity (no missing dark columns inside
    the span for thin lines), mouth-only components, fringe count,
    placement centre, no-crop. Exit 0 PASS / 1 FAIL.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw
from scipy.interpolate import UnivariateSpline

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "mouth-packs-clean-pipeline-20261031")
SS = 8  # supersample factor for vector rasterisation

def dark_mask(arr):
    rgb = arr[:, :, :3].astype(int)
    return (arr[:, :, 3] > 50) & (rgb[:, :, 0] < 90) & (rgb[:, :, 1] < 90) & (rgb[:, :, 2] < 90)

def centreline(mask):
    """Per-column median y + thickness, for columns with dark pixels."""
    xs, ys, th = [], [], []
    for x in range(mask.shape[1]):
        col = np.where(mask[:, x])[0]
        if len(col):
            xs.append(x); ys.append(float(np.median(col))); th.append(len(col))
    return np.array(xs, float), np.array(ys, float), np.array(th, float)

def catmull_rom_to_bezier(pts):
    """pts: list of (x,y). Returns list of cubic segments (p0,c1,c2,p3)."""
    segs = []
    p = [(float(x), float(y)) for x, y in pts]
    for i in range(len(p) - 1):
        p0 = p[i - 1] if i > 0 else p[i]
        p1 = p[i]; p2 = p[i + 1]
        p3 = p[i + 2] if i + 2 < len(p) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        segs.append((p1, c1, c2, p2))
    return segs

def cubic(p0, c1, c2, p3, t):
    mt = 1 - t
    return (mt**3*p0[0] + 3*mt*mt*t*c1[0] + 3*mt*t*t*c2[0] + t**3*p3[0],
            mt**3*p0[1] + 3*mt*mt*t*c1[1] + 3*mt*t*t*c2[1] + t**3*p3[1])

def vector_line_patch(mask, size, stroke, name, smoothing):
    """Fit spline to centreline, write SVG + supersampled raster.
    Returns (raster Image, svg text, stats)."""
    xs, ys, th = centreline(mask)
    # Smoothing spline: s chosen so the fitted curve follows the wavy
    # original (residual < 1px median) without copying pixel steps.
    spl = UnivariateSpline(xs, ys, k=3, s=smoothing)
    x_new = np.arange(xs.min(), xs.max() + 1, 1.0)
    y_new = spl(x_new)
    # Sample every 4 columns for the SVG path (enough for a smooth curve,
    # few enough that the path is a real vector, not a polyline dump).
    sample_idx = list(range(0, len(x_new), 4))
    if sample_idx[-1] != len(x_new) - 1:
        sample_idx.append(len(x_new) - 1)
    pts = [(float(x_new[i]), float(y_new[i])) for i in sample_idx]
    # Scale to placed size: mask is source scale; caller passes size.
    sx = size[0] / mask.shape[1]; sy = size[1] / mask.shape[0]
    pts = [(x * sx, y * sy) for x, y in pts]
    segs = catmull_rom_to_bezier(pts)
    # SVG path
    d = f"M {pts[0][0]:.2f} {pts[0][1]:.2f} "
    for (p1, c1, c2, p2) in segs:
        d += f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:.2f} {p2[1]:.2f} "
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" '
           f'viewBox="0 0 {size[0]} {size[1]}">\n'
           f'  <path d="{d.strip()}" fill="none" stroke="black" stroke-width="{stroke}" '
           f'stroke-linecap="round" stroke-linejoin="round"/>\n</svg>\n')
    # Rasterise at 8x: dense Bezier sampling, then LANCZOS downscale.
    W, H = size[0] * SS, size[1] * SS
    hi = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(hi)
    for (p1, c1, c2, p2) in segs:
        prev = None
        for i in range(41):
            pt = cubic(p1, c1, c2, p2, i / 40.0)
            pt = (pt[0] * SS, pt[1] * SS)
            if prev is not None:
                dr.line([prev, pt], fill=(0, 0, 0, 255), width=int(stroke * SS))
            prev = pt
    raster = hi.resize(size, Image.LANCZOS)
    # Threshold alpha >=128 so the raster is a clean binary line, no fringe.
    ra = np.array(raster)
    ra[:, :, 3] = np.where(ra[:, :, 3] >= 128, 255, 0)
    raster = Image.fromarray(ra)
    resid = np.abs(spl(xs) - ys)
    stats = {"name": name, "placed_size": list(size), "stroke_px": stroke,
             "source_columns": [int(xs.min()), int(xs.max())],
             "median_residual_px": round(float(np.median(resid)), 3),
             "max_residual_px": round(float(np.max(resid)), 3),
             "median_thickness_source_px": round(float(np.median(th)), 2),
             "svg_segments": len(segs), "svg_path_points": len(pts)}
    return raster, svg, stats

def gate_thin_line(patch, name):
    """Continuity + step check on the rasterised line."""
    a = np.array(patch.convert("RGBA"))
    dark = (a[:, :, 0] < 90) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90) & (a[:, :, 3] > 50)
    cols = [x for x in range(dark.shape[1]) if dark[:, x].any()]
    missing = [x for x in range(cols[0], cols[-1] + 1) if x not in cols]
    med = []
    for x in cols:
        med.append(float(np.median(np.where(dark[:, x])[0])))
    steps = [abs(med[i+1] - med[i]) for i in range(len(med) - 1)]
    return {"name": name, "dark_columns": [cols[0], cols[-1]], "missing_columns_inside": missing,
            "max_adjacent_centre_step_px": round(max(steps), 2) if steps else 0,
            "pass": len(missing) == 0}
