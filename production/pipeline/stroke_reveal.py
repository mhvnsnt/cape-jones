#!/usr/bin/env python3
"""
Stroke Reveal Effect — neon write-on animation for Cape Jones.

Takes a final drawing (transparent PNG) + stroke order, animates a mask
revealing it stroke-by-stroke with neon glow. For the scary face/mask gag
and chalkboard write effects.

Usage:
    python3 stroke_reveal.py final_drawing.png output.mp4 \
        --strokes strokes.json --duration 3.0 --glow-color cyan \
        --fps 24 --width 1080 --height 1920

strokes.json format:
    [
        {"path": [[x1,y1],[x2,y2],...], "start": 0.0, "end": 0.5},
        {"path": [[x1,y1],...], "start": 0.5, "end": 1.0},
        ...
    ]
    Times are in seconds. Each stroke reveals along its path.

If --strokes not provided, reveals the whole image with a left-to-right
wipe (simple fallback).

The neon glow: draws the revealed portion, applies Gaussian blur for glow,
composites blurred copy underneath at high brightness.
"""

import argparse
import json
import cv2
import numpy as np
import subprocess
import os
import sys
import math


GLOW_COLORS = {
    "cyan": (255, 255, 0),      # BGR for OpenCV
    "magenta": (255, 0, 255),
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "red": (0, 0, 255),
    "white": (255, 255, 255),
    "purple": (255, 0, 128),
    "orange": (0, 165, 255),
}


def load_drawing(path):
    """Load PNG with alpha channel."""
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Cannot load {path}")
    if img.shape[2] == 3:
        # No alpha — add opaque alpha
        alpha = np.ones(img.shape[:2], dtype=np.uint8) * 255
        img = np.dstack([img, alpha])
    return img


def point_on_path(path, t):
    """Get point at parameter t (0-1) along a polyline path."""
    if len(path) < 2:
        return path[0] if path else (0, 0)
    # Compute cumulative distances
    total = 0
    dists = [0]
    for i in range(1, len(path)):
        d = math.hypot(path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])
        total += d
        dists.append(total)
    if total == 0:
        return path[0]
    target = t * total
    for i in range(1, len(path)):
        if dists[i] >= target:
            # Interpolate
            seg_len = dists[i] - dists[i-1]
            if seg_len == 0:
                return path[i]
            frac = (target - dists[i-1]) / seg_len
            x = path[i-1][0] + frac * (path[i][0] - path[i-1][0])
            y = path[i-1][1] + frac * (path[i][1] - path[i-1][1])
            return (x, y)
    return path[-1]


def build_reveal_mask(shape, strokes, current_time, brush_radius=8):
    """Build binary mask of revealed area at current_time."""
    h, w = shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    for stroke in strokes:
        path = stroke["path"]
        start = stroke.get("start", 0)
        end = stroke.get("end", 1)
        if current_time < start:
            continue
        if current_time >= end:
            # Fully revealed — draw entire path
            t = 1.0
        else:
            t = (current_time - start) / (end - start)
        # Draw path up to parameter t
        n_points = max(2, int(len(path) * t) + 1)
        partial = path[:n_points]
        if t < 1.0 and n_points < len(path):
            partial = partial + [point_on_path(path, t)]
        pts = np.array(partial, dtype=np.int32)
        if len(pts) >= 2:
            cv2.polylines(mask, [pts], False, 255, brush_radius * 2,
                          lineType=cv2.LINE_AA)
    return mask


def apply_neon_glow(revealed_bgr, mask, glow_color_bgr, glow_radius=15):
    """Apply neon glow to revealed portion."""
    # Masked color layer
    mask_3ch = cv2.merge([mask, mask, mask])
    colored = np.zeros_like(revealed_bgr)
    colored[:] = glow_color_bgr
    # Where mask is on AND original has content, apply glow color tint
    # Actually: keep original colors, add glow around edges
    glow_mask = cv2.GaussianBlur(mask, (glow_radius * 2 + 1, glow_radius * 2 + 1), 0)
    glow_mask_3ch = cv2.merge([glow_mask, glow_mask, glow_mask]).astype(np.float32) / 255.0

    glow_layer = np.zeros_like(revealed_bgr, dtype=np.float32)
    glow_layer[:] = np.array(glow_color_bgr, dtype=np.float32)

    # Composite: original + glow
    result = revealed_bgr.astype(np.float32)
    result = result + glow_layer * glow_mask_3ch * 0.8
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result


def main():
    ap = argparse.ArgumentParser(description="Neon stroke-reveal write-on effect")
    ap.add_argument("input", help="Final drawing PNG (transparent background)")
    ap.add_argument("output", help="Output MP4")
    ap.add_argument("--strokes", default=None, help="JSON file with stroke order")
    ap.add_argument("--duration", type=float, default=3.0, help="Total duration in seconds")
    ap.add_argument("--glow-color", default="cyan", choices=list(GLOW_COLORS.keys()))
    ap.add_argument("--glow-radius", type=int, default=15)
    ap.add_argument("--brush-radius", type=int, default=8)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--hold", type=float, default=1.0,
                    help="Seconds to hold final frame")
    args = ap.parse_args()

    drawing = load_drawing(args.input)
    dh, dw = drawing.shape[:2]

    # Scale drawing to fit if needed (keep aspect)
    scale = min(args.width / dw, args.height / dh)
    if scale < 1.0:
        new_w, new_h = int(dw * scale), int(dh * scale)
        drawing = cv2.resize(drawing, (new_w, new_h), interpolation=cv2.INTER_AREA)
        dh, dw = drawing.shape[:2]

    # Center on canvas
    canvas_h, canvas_w = args.height, args.width
    ox, oy = (canvas_w - dw) // 2, (canvas_h - dh) // 2

    # Load strokes or create default wipe
    if args.strokes and os.path.exists(args.strokes):
        with open(args.strokes) as f:
            raw_strokes = json.load(f)
        # Offset paths by drawing position
        strokes = []
        for s in raw_strokes:
            path = [[p[0] + ox, p[1] + oy] for p in s["path"]]
            strokes.append({"path": path, "start": s.get("start", 0),
                            "end": s.get("end", args.duration)})
    else:
        # Default: left-to-right wipe across the drawing
        strokes = [{
            "path": [[ox, oy + dh // 2], [ox + dw, oy + dh // 2]],
            "start": 0, "end": args.duration,
        }]
        print("No strokes file — using left-to-right wipe fallback", file=sys.stderr)

    glow_bgr = GLOW_COLORS[args.glow_color]
    n_frames = int(args.duration * args.fps)
    hold_frames = int(args.hold * args.fps)

    # Place drawing on canvas
    canvas_drawing = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)
    canvas_drawing[oy:oy+dh, ox:ox+dw] = drawing
    drawing_bgr = canvas_drawing[:, :, :3]
    drawing_alpha = canvas_drawing[:, :, 3]

    work_dir = os.path.expanduser("~/workspace/tmp/stroke_reveal_frames")
    os.makedirs(work_dir, exist_ok=True)

    print(f"Rendering {n_frames + hold_frames} frames...", file=sys.stderr)
    for i in range(n_frames + hold_frames):
        if i < n_frames:
            t = i / args.fps
        else:
            t = args.duration  # Hold: fully revealed

        mask = build_reveal_mask((canvas_h, canvas_w), strokes, t,
                                 args.brush_radius)
        # Only reveal where drawing has content
        mask = cv2.bitwise_and(mask, drawing_alpha)

        # Base: black background
        frame = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

        # Revealed drawing
        mask_3ch = cv2.merge([mask, mask, mask])
        revealed = cv2.bitwise_and(drawing_bgr, mask_3ch)

        # Neon glow
        frame = apply_neon_glow(revealed, mask, glow_bgr, args.glow_radius)

        cv2.imwrite(f"{work_dir}/f{i:05d}.png", frame)
        if i % 24 == 0:
            print(f"  frame {i}/{n_frames + hold_frames}", file=sys.stderr)

    # Encode
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-framerate", str(args.fps), "-i", f"{work_dir}/f%05d.png",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", args.output,
    ]
    subprocess.run(cmd, check=True)

    # Cleanup
    import shutil
    shutil.rmtree(work_dir)

    print(f"Done: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
