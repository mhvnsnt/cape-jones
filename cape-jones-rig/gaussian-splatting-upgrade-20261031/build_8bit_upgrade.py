#!/usr/bin/env python3
"""Gaussian Splatting upgrade builder — 8-bit Cape Jones.

Tool name stays: Gaussian Splatting. Builder: build_8bit_upgrade.py
(source plate rig-apose-v7c-clean-transparent.png, base art untouched).

Usage:
  python3 build_8bit_upgrade.py --preset 8bit --version V1   # reproduce V1 exactly
  python3 build_8bit_upgrade.py --preset 8bit --version V2   # dense splat
  python3 build_8bit_upgrade.py --preset 8bit --version V3   # pixel-grid box dots
  python3 build_8bit_upgrade.py --preset 8bit --version all  # V1+V2+V3 + methods
  python3 build_8bit_upgrade.py --preset 8bit --methods       # 10 method fronts only

V1 parameters (from 8-BIT-CAPE-JONES-PRESET-20261031.md, reproduced, not changed):
  stride 8, sigma 3.2, opacity 0.85, focal 900, Gaussian kernel, full plate colour.
V2 (DENSE): stride 4, sigma 2.4, opacity 0.85, focal 900, Gaussian kernel.
V3 (PIXEL-GRID): stride 6, box kernel 6x6, opacity 1.0 per dot, focal 900,
  colours snapped to a 16-colour palette extracted from the plate itself
  (PIL median-cut quantize, no invented colours).

Depth in all versions: SYNTHETIC bulge proxy (distance transform, max 81.9px
toward camera). NOT a true multi-view reconstruction, NOT a scanned back.
Turn views are depth-bulge rotations; a true back needs Mars's FLA back pieces.
No GPU, no torch, no CUDA on this VM: vendor CUDA implementations (gsplat,
splatfacto) are mappings, never claimed as runs. The 10 methods below are CPU
implementations/proxies of those methods' cores, labelled as such in the report.
"""
import argparse, json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "gaussian-splatting-upgrade-20261031")
SRC = os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")
GREY = (128, 128, 128, 255)

VERSIONS = {
    "V1": dict(stride=8, sigma=3.2, opacity=0.85, kernel="gauss", palette=None,
               sub=".", label="V1 preset (reproduction)"),
    "V2": dict(stride=4, sigma=2.4, opacity=0.85, kernel="gauss", palette=None,
               sub="8BIT-V2", label="V2 DENSE"),
    "V3": dict(stride=6, sigma=3.0, opacity=1.0, kernel="box", palette=16,
               sub="8BIT-V3", label="V3 PIXEL-GRID"),
}
ANGLES = [-40, -25, -10, 0, 10, 25, 40, 25, 10]


def load_plate():
    img = Image.open(SRC).convert("RGBA")
    return img, np.asarray(img).astype(np.float32)


def sample(arr, stride, palette_n=None):
    alpha = arr[..., 3] / 255.0
    rgb = arr[..., :3]
    ys, xs = np.where(alpha[::stride, ::stride] > 0.5)
    xs = xs * stride; ys = ys * stride
    edt = distance_transform_edt(alpha > 0.5)
    depth = edt[ys, xs]
    cols = rgb[ys, xs].copy()
    if palette_n:
        # 16-colour palette from the plate itself (median-cut, PIL quantize)
        pal_img = Image.open(SRC).convert("RGB").quantize(colors=palette_n)
        pal = np.asarray(pal_img.getpalette()[:palette_n * 3], dtype=np.float32).reshape(-1, 3)
        d = ((cols[:, None, :] - pal[None, :, :]) ** 2).sum(axis=2)
        cols = pal[np.argmin(d, axis=1)]
    return xs, ys, depth, cols, float(edt.max())


def make_renderer(W, H, xs, ys, depth, cols, sigma, opacity, kernel, box_half=3):
    cx, cy = W / 2.0, H / 2.0
    FOCAL = 900.0
    x0 = xs.astype(np.float64) - cx
    y0 = ys.astype(np.float64) - cy
    z0 = depth.astype(np.float64) * 0.9

    def render(angle_deg, sig_mult=1.0, sigx_mult=1.0, sigy_mult=1.0,
               subset=None, time_t=None, scale=1.0, leg_shift=0.0):
        th = math.radians(angle_deg)
        c, s = math.cos(th), math.sin(th)
        yy0 = y0
        if time_t is not None:  # 4D breathing proxy: gentle y pulse
            yy0 = y0 * (1.0 + 0.03 * math.sin(time_t * 2 * math.pi))
        xr = x0 * c + z0 * s
        zr = -x0 * s + z0 * c
        persp = FOCAL / (FOCAL + zr)
        sx = cx + xr * persp * scale
        sy = cy + yy0 * persp * scale
        if leg_shift:
            # stepping proxy only: lower-body Gaussians (y0 > 200, legs/feet)
            # shift alternately; upper body does not shift. NOT walk keys.
            sx = sx + np.where(y0 > 200, leg_shift * persp, 0.0)
        order = np.argsort(zr)
        if subset is not None:
            order = np.array([i for i in order if subset[i]])
        out_rgb = np.zeros((H, W, 3), dtype=np.float64)
        out_a = np.zeros((H, W), dtype=np.float64)
        for idx in order:
            px, py = sx[idx], sy[idx]
            sg = sigma * persp[idx] * sig_mult
            ix, iy = int(round(px)), int(round(py))
            if kernel == "box":
                half = box_half  # V3 stride 6 -> 6x6 dot; voxel -> 8x8 dot
                x1, x2 = max(0, ix - half), min(W, ix + half)
                y1, y2 = max(0, iy - half), min(H, iy + half)
                if x2 <= x1 or y2 <= y1:
                    continue
                a = np.full((y2 - y1, x2 - x1), opacity)
                a = a * (1.0 - out_a[y1:y2, x1:x2])
                out_rgb[y1:y2, x1:x2] += a[..., None] * cols[idx]
                out_a[y1:y2, x1:x2] += a
            else:
                sgx, sgy = sg * sigx_mult, sg * sigy_mult
                R = 4
                x1, x2 = max(0, ix - R), min(W, ix + R + 1)
                y1, y2 = max(0, iy - R), min(H, iy + R + 1)
                if x2 <= x1 or y2 <= y1:
                    continue
                gx = np.arange(x1, x2) - px
                gy = np.arange(y1, y2) - py
                gxx, gyy = np.meshgrid(gx, gy)
                w = np.exp(-(gxx ** 2 / (2 * sgx ** 2) + gyy ** 2 / (2 * sgy ** 2)))
                a = opacity * w
                a = a * (1.0 - out_a[y1:y2, x1:x2])
                out_rgb[y1:y2, x1:x2] += a[..., None] * cols[idx]
                out_a[y1:y2, x1:x2] += a
        final = np.zeros((H, W, 4), dtype=np.uint8)
        final[..., :3] = np.clip(out_rgb, 0, 255).astype(np.uint8)
        final[..., 3] = np.clip(out_a * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(final, "RGBA"), out_a
    return render


def on_grey(im):
    bg = Image.new("RGBA", im.size, GREY)
    bg.alpha_composite(im)
    return bg.convert("RGB")


def measure(front_a, plate_alpha):
    pa = plate_alpha > 0.5
    sa = front_a > 0.5
    inter = int((pa & sa).sum()); union = int((pa | sa).sum())
    return dict(plate_alpha_px=int(pa.sum()), splat_alpha_px=int(sa.sum()),
                iou_alpha=round(inter / union, 4) if union else 0)


def build_version(ver, img, arr):
    cfg = VERSIONS[ver]
    W, H = img.size
    xs, ys, depth, cols, dmax = sample(arr, cfg["stride"], cfg["palette"])
    render = make_renderer(W, H, xs, ys, depth, cols, cfg["sigma"], cfg["opacity"], cfg["kernel"])
    outdir = os.path.join(OUT, cfg["sub"]) if cfg["sub"] != "." else OUT
    os.makedirs(outdir, exist_ok=True)
    front, front_a = render(0)
    front.save(os.path.join(outdir, f"8bit-{ver}-front-20261031.png"))
    frames = []
    for ang in ANGLES:
        im, _ = render(ang)
        frames.append(on_grey(im))
    gif = os.path.join(outdir, f"8bit-{ver}-turn-sequence-20261031.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=150, loop=0)
    meas = measure(front_a, arr[..., 3] / 255.0)
    meas.update(version=ver, label=cfg["label"], gaussians=int(len(xs)),
                stride=cfg["stride"], sigma=cfg["sigma"], opacity=cfg["opacity"],
                kernel=cfg["kernel"], palette=cfg["palette"],
                depth_max_px=round(float(depth.max()), 1) if len(depth) else 0,
                frames=len(frames), angles=ANGLES)
    with open(os.path.join(outdir, f"8bit-{ver}-measurements-20261031.json"), "w") as f:
        json.dump(meas, f, indent=2)
    print(ver, meas)
    return meas, (xs, ys, depth, cols, render)


def build_v4(img, arr):
    """8BIT-V4 STEP-TO-CAMERA — SEPARATE labelled variant, NOT V1 relabelled.

    Mars reading (2026-10-31 20:19 CDT): V1 "almost looks like it is walking,
    taking steps towards the camera" — that is a READING of the depth-bulge
    rotation, NOT a true walk cycle, and V1 used no walk keys. This variant
    makes that reading explicit as a synthetic stepping proxy, and only here:
    scale grows toward the camera (0.85 -> 1.25 -> 0.85, loop-safe, peak
    frame kept off the canvas edge — an earlier 1.45 peak touched y=1499) and
    lower-body Gaussians shift alternately +/-18px per step. No walk keys,
    no rig pose, no planted feet — feet move with the growth, measured below.
    Motion explicitly differs from V1/V2/V3: turn is halved (-20..+20) because
    stepping/scale is the primary motion in this variant.
    """
    W, H = img.size
    outdir = os.path.join(OUT, "8BIT-V4")
    os.makedirs(outdir, exist_ok=True)
    xs, ys, depth, cols, _ = sample(arr, 8, None)
    render = make_renderer(W, H, xs, ys, depth, cols, 3.2, 0.85, "gauss")
    front, front_a = render(0)
    front.save(os.path.join(outdir, "8bit-V4-front-20261031.png"))
    angles = [-20, -10, 0, 10, 20, 10, 0, -10, -20]
    scales = [0.85, 0.95, 1.05, 1.15, 1.25, 1.15, 1.05, 0.95, 0.85]
    shifts = [18, -18, 18, -18, 18, -18, 18, -18, 18]
    frames, frame_meas = [], []
    for ang, sc, sh in zip(angles, scales, shifts):
        im, fa = render(ang, scale=sc, leg_shift=float(sh))
        frames.append(on_grey(im))
        yy, xx = np.where(fa > 0.5)
        frame_meas.append(dict(angle=ang, scale=sc, leg_shift_px=sh,
                               alpha_px=int(fa[fa > 0.5].size) if False else int((fa > 0.5).sum()),
                               bbox_x_min=int(xx.min()), bbox_x_max=int(xx.max()),
                               bbox_y_min=int(yy.min()), bbox_y_max=int(yy.max()),
                               width_px=int(xx.max() - xx.min() + 1),
                               height_px=int(yy.max() - yy.min() + 1)))
    gif = os.path.join(outdir, "8bit-V4-turn-sequence-20261031.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=150, loop=0)
    meas = measure(front_a, arr[..., 3] / 255.0)
    meas.update(version="V4", label="V4 STEP-TO-CAMERA (stepping proxy, NOT a walk cycle)",
                gaussians=int(len(xs)), stride=8, sigma=3.2, opacity=0.85,
                kernel="gauss", palette=None, depth_max_px=round(float(depth.max()), 1),
                frames=len(frames), angles=angles, scales=scales,
                leg_shifts_px=shifts, frame_measurements=frame_meas)
    with open(os.path.join(outdir, "8bit-V4-measurements-20261031.json"), "w") as f:
        json.dump(meas, f, indent=2)
    print("V4", meas)
    return meas


def build_methods(img, arr):
    """10 CPU method fronts, all on the V1 sampling (stride 8) unless noted."""
    W, H = img.size
    outdir = os.path.join(OUT, "methods")
    os.makedirs(outdir, exist_ok=True)
    xs, ys, depth, cols, dmax = sample(arr, 8, None)
    render = make_renderer(W, H, xs, ys, depth, cols, 3.2, 0.85, "gauss")
    # palette + dither variants need post-processing on the rendered front
    base_front, _ = render(0)
    plate_rgb = Image.open(SRC).convert("RGB")
    q16 = plate_rgb.quantize(colors=16)
    # per-Gaussian palette snap for I3-style front is done via a separate render
    _, _, _, cols_q, _ = sample(arr, 8, 16)
    render_q = make_renderer(W, H, xs, ys, depth, cols_q, 3.2, 0.85, "gauss")
    anchor = np.arange(len(xs)) % 3 == 0
    jitter_rng = np.random.default_rng(7)
    xs_j = np.clip(xs + jitter_rng.integers(-3, 4, size=len(xs)), 0, W - 1)
    ys_j = np.clip(ys + jitter_rng.integers(-3, 4, size=len(ys)), 0, H - 1)
    render_j = make_renderer(W, H, xs_j, ys_j, depth, cols, 3.2, 0.85, "gauss")
    specs = [
        ("I1-3dgs-core", "3DGS core (industry)", lambda: render(0)),
        ("I2-voxel", "Voxel grid 8px (industry)", None),  # special: box kernel render
        ("I3-palette16", "Palette quantize 16 (industry)", lambda: render_q(0)),
        ("I4-dither-fs", "Floyd-Steinberg dither 16 (industry)", None),  # post-process
        ("I5-mip", "Mip-Splatting filter (industry)", lambda: render(-20, sig_mult=1.6)),
        ("X1-2dgs", "2DGS surfels (experimental)", lambda: render(0, sigx_mult=1.6, sigy_mult=0.55)),
        ("X2-scaffold", "Scaffold-GS anchors (experimental)", lambda: render(0, subset=anchor, sig_mult=1.5)),
        ("X3-4dgs", "4DGS breathing t=0.25 (experimental)", lambda: render(0, time_t=0.25)),
        ("X4-jitter", "Jittered/blue-noise sampling (experimental)", lambda: render_j(0)),
        ("X5-depth-sigma", "Depth-scaled sigma (experimental)", None),  # special below
    ]
    results = {}
    for name, label, fn in specs:
        if name == "I2-voxel":
            rbox = make_renderer(W, H, xs, ys, depth, cols, 3.2, 1.0, "box", box_half=4)
            im, fa = rbox(0)
        elif name == "I4-dither-fs":
            # dither the V1 front to 16 colours with Floyd-Steinberg
            tmp = on_grey(base_front).quantize(colors=16, dither=Image.FLOYDSTEINBERG).convert("RGB")
            im = Image.new("RGBA", tmp.size); im.paste(tmp, (0, 0))
            fa = np.asarray(base_front)[..., 3] / 255.0
        elif name == "X5-depth-sigma":
            # sigma grows with bulge depth: near (deep) splats larger, edge splats smaller
            # implemented by rendering twice at two sigmas and compositing deep-first:
            # honest proxy, labelled as such in the report.
            im_lo, _ = render(0, sig_mult=0.7)
            im_hi, fa = render(0, sig_mult=1.4)
            im = Image.alpha_composite(im_lo, im_hi)
        else:
            im, fa = fn()
        p = os.path.join(outdir, f"method-{name}-front-20261031.png")
        on_grey(im).save(p)
        m = measure(fa, arr[..., 3] / 255.0)
        results[name] = dict(label=label, file=os.path.basename(p), **m)
        print(name, m)
    # contact sheet, 5x2
    tw, th = 440, 600
    sheet = Image.new("RGB", (tw * 5, th * 2 + 60), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for i, (name, label, _) in enumerate(specs):
        im = Image.open(os.path.join(outdir, f"method-{name}-front-20261031.png"))
        x, y = (i % 5) * tw, (i // 5) * (th + 30)
        sheet.paste(im, (x, y + 30)); d.text((x + 8, y + 6), f"{name} {label}", fill=(0, 0, 0))
    sheet.save(os.path.join(outdir, "methods-contact-20261031.png"))
    with open(os.path.join(outdir, "methods-measurements-20261031.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", default="8bit")
    ap.add_argument("--version", default="all", choices=["V1", "V2", "V3", "V4", "all"])
    ap.add_argument("--methods", action="store_true")
    args = ap.parse_args()
    if args.preset != "8bit":
        print("only --preset 8bit is supported by this builder", file=sys.stderr)
        sys.exit(2)
    img, arr = load_plate()
    W, H = img.size
    print(f"plate {W}x{H}")
    out = {}
    vers = ["V1", "V2", "V3"] if args.version == "all" else ([args.version] if args.version != "V4" else [])
    for v in vers:
        meas, _ = build_version(v, img, arr)
        out[v] = meas
    if args.version in ("V4", "all"):
        out["V4"] = build_v4(img, arr)
    if args.methods or args.version == "all":
        out["methods"] = build_methods(img, arr)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
