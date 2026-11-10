#!/usr/bin/env python3
"""
Energy Blast Effect — for Cape Jones wrist blasters.

Generates animated energy blast overlays: force beam, stun rings, freezing ray.
Composites onto existing video or generates standalone overlay.

Blast types:
  - beam: sustained force beam from wrist position
  - rings: expanding stun rings
  - freeze: ice-blue freezing ray with particles
  - burst: radial energy burst/overlap

Usage:
    # Generate standalone blast overlay (transparent → use as overlay)
    python3 energy_blast.py --type beam --duration 2.0 --output blast.mp4

    # Composite onto existing video
    python3 energy_blast.py --type beam --duration 2.0 \\
        --base input.mp4 --x 540 --y 960 --angle 0 \\
        --output output.mp4

Colors follow Cape Jones canon:
  - Core: pure white (#FFFFFF)
  - Corona: bright yellow/cyan (Color Dodge feel)
"""

import argparse
import cv2
import numpy as np
import subprocess
import os
import math
import random


def make_beam_frame(w, h, t, duration, angle_deg=0):
    """Generate a single beam frame. Beam fires from left-center outward."""
    frame = np.zeros((h, w, 4), dtype=np.uint8)  # BGRA

    # Beam progress: grows then sustains then fades
    grow = min(1.0, t / 0.3)
    fade = 1.0 if t < duration - 0.3 else max(0, (duration - t) / 0.3)
    intensity = grow * fade

    if intensity <= 0:
        return frame

    cx, cy = w // 4, h // 2  # Origin (wrist position relative)
    beam_len = int(w * 0.7 * grow)
    # Flicker
    flicker = 0.85 + 0.15 * math.sin(t * 50) * math.sin(t * 37)

    # Core beam (white)
    core_w = int(12 + 4 * math.sin(t * 40))
    for x in range(beam_len):
        alpha = int(255 * intensity * flicker * (1 - x / beam_len * 0.3))
        cv2.line(frame, (cx, cy - core_w // 2), (cx + x, cy - core_w // 2),
                 (255, 255, 255, alpha), 1)
        cv2.line(frame, (cx, cy + core_w // 2), (cx + x, cy + core_w // 2),
                 (255, 255, 255, alpha), 1)
    # Fill core
    cv2.rectangle(frame, (cx, cy - core_w // 2), (cx + beam_len, cy + core_w // 2),
                  (255, 255, 255, int(200 * intensity * flicker)), -1)

    # Corona (cyan glow around beam)
    corona_w = core_w * 3
    for x in range(0, beam_len, 3):
        alpha = int(120 * intensity * flicker * (1 - x / beam_len * 0.5))
        cv2.line(frame, (cx, cy - corona_w // 2), (cx + x, cy - corona_w // 2),
                 (255, 255, 0, alpha), 2)  # Cyan in BGRA
        cv2.line(frame, (cx, cy + corona_w // 2), (cx + x, cy + corona_w // 2),
                 (255, 255, 0, alpha), 2)
    cv2.rectangle(frame, (cx, cy - corona_w // 2), (cx + beam_len, cy + corona_w // 2),
                  (255, 255, 0, int(60 * intensity * flicker)), -1)

    # Muzzle flash (bright white-yellow burst at origin)
    flash_r = int(30 + 15 * math.sin(t * 60))
    cv2.circle(frame, (cx, cy), flash_r,
               (255, 255, 255, int(255 * intensity)), -1)
    cv2.circle(frame, (cx, cy), flash_r + 15,
               (0, 255, 255, int(150 * intensity)), -1)  # Yellow halo

    # Sparks
    for _ in range(8):
        sx = cx + random.randint(0, beam_len // 2)
        sy = cy + random.randint(-corona_w, corona_w)
        sr = random.randint(2, 5)
        cv2.circle(frame, (sx, sy), sr,
                   (255, 255, 255, int(200 * intensity)), -1)

    # Rotate if angle specified
    if angle_deg != 0:
        M = cv2.getRotationMatrix2D((cx, cy), angle_deg, 1.0)
        frame = cv2.warpAffine(frame, M, (w, h))

    return frame


def make_rings_frame(w, h, t, duration, cx=None, cy=None):
    """Expanding stun rings."""
    frame = np.zeros((h, w, 4), dtype=np.uint8)
    cx = cx or w // 2
    cy = cy or h // 2

    n_rings = 3
    for i in range(n_rings):
        phase = (t / duration * n_rings - i / n_rings) % 1.0
        radius = int(phase * min(w, h) * 0.4)
        alpha = int(255 * (1 - phase) * 0.9)
        if radius > 2 and alpha > 0:
            # White core ring
            cv2.circle(frame, (cx, cy), radius, (255, 255, 255, alpha), 4)
            # Cyan outer glow
            cv2.circle(frame, (cx, cy), radius, (255, 255, 0, alpha // 2), 10)

    return frame


def make_freeze_frame(w, h, t, duration):
    """Ice-blue freezing ray with particles."""
    frame = make_beam_frame(w, h, t, duration)
    # Tint blue
    b, g, r, a = cv2.split(frame)
    # Shift toward ice blue: boost blue, reduce red
    b = np.clip(b.astype(int) * 1.2, 0, 255).astype(np.uint8)
    r = np.clip(r.astype(int) * 0.7, 0, 255).astype(np.uint8)
    frame = cv2.merge([b, g, r, a])

    # Ice crystals (small crosses)
    for _ in range(12):
        ix = random.randint(0, w - 1)
        iy = random.randint(0, h - 1)
        s = random.randint(3, 8)
        alpha = random.randint(100, 200)
        cv2.line(frame, (ix - s, iy), (ix + s, iy), (255, 255, 255, alpha), 1)
        cv2.line(frame, (ix, iy - s), (ix, iy + s), (255, 255, 255, alpha), 1)

    return frame


def make_burst_frame(w, h, t, duration, cx=None, cy=None):
    """Radial energy burst."""
    frame = np.zeros((h, w, 4), dtype=np.uint8)
    cx = cx or w // 2
    cy = cy or h // 2

    # Expand then fade
    progress = t / duration
    max_r = int(min(w, h) * 0.45 * min(1.0, progress * 3))
    alpha = int(255 * (1 - progress))

    if max_r > 0 and alpha > 0:
        # White core
        cv2.circle(frame, (cx, cy), max_r, (255, 255, 255, alpha), -1)
        # Yellow mid
        cv2.circle(frame, (cx, cy), int(max_r * 1.3),
                   (0, 255, 255, alpha // 2), -1)
        # Cyan outer
        cv2.circle(frame, (cx, cy), int(max_r * 1.6),
                   (255, 255, 0, alpha // 3), -1)

    # Rays
    n_rays = 12
    for i in range(n_rays):
        ang = (2 * math.pi * i / n_rays) + t * 2
        x2 = int(cx + math.cos(ang) * max_r * 1.8)
        y2 = int(cy + math.sin(ang) * max_r * 1.8)
        cv2.line(frame, (cx, cy), (x2, y2),
                 (255, 255, 255, alpha // 2), 3)

    return frame


def composite_onto_base(blast_frame, base_frame, x, y):
    """Composite blast BGRA onto base BGR at position (x, y = blast origin)."""
    bh, bw = blast_frame.shape[:2]
    hh, ww = base_frame.shape[:2]

    # Blast origin should be at (x, y) — blast frames have origin at w//4, h//2
    ox = x - bw // 4
    oy = y - bh // 2

    # Clip to base bounds
    x1 = max(0, ox)
    y1 = max(0, oy)
    x2 = min(ww, ox + bw)
    y2 = min(hh, oy + bh)
    if x2 <= x1 or y2 <= y1:
        return base_frame

    bx1, by1 = x1 - ox, y1 - oy
    bx2, by2 = bx1 + (x2 - x1), by1 + (y2 - y1)

    blast_roi = blast_frame[by1:by2, bx1:bx2]
    base_roi = base_frame[y1:y2, x1:x2].astype(np.float32)

    alpha = blast_roi[:, :, 3:4].astype(np.float32) / 255.0
    blast_bgr = blast_roi[:, :, :3].astype(np.float32)

    # Screen blend for energy feel (brighter)
    blended = 255 - (255 - base_roi) * (255 - blast_bgr) / 255
    # Mix by alpha
    result_roi = blended * alpha + base_roi * (1 - alpha)

    output = base_frame.copy()
    output[y1:y2, x1:x2] = np.clip(result_roi, 0, 255).astype(np.uint8)
    return output


def main():
    ap = argparse.ArgumentParser(description="Cape Jones energy blast effects")
    ap.add_argument("--type", default="beam",
                    choices=["beam", "rings", "freeze", "burst"])
    ap.add_argument("--duration", type=float, default=2.0)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--output", required=True)
    ap.add_argument("--base", default=None,
                    help="Base video to composite onto")
    ap.add_argument("--x", type=int, default=None,
                    help="Blast origin X on base video")
    ap.add_argument("--y", type=int, default=None,
                    help="Blast origin Y on base video")
    ap.add_argument("--angle", type=float, default=0,
                    help="Beam angle in degrees")
    args = ap.parse_args()

    random.seed(42)  # Reproducible sparks

    generators = {
        "beam": lambda w, h, t, d: make_beam_frame(w, h, t, d, args.angle),
        "rings": make_rings_frame,
        "freeze": make_freeze_frame,
        "burst": make_burst_frame,
    }
    gen = generators[args.type]
    n_frames = int(args.duration * args.fps)

    # Load base video if compositing
    base_frames = None
    if args.base:
        cap = cv2.VideoCapture(args.base)
        base_frames = []
        while True:
            ret, f = cap.read()
            if not ret:
                break
            base_frames.append(f)
        cap.release()
        # Loop or trim to match
        while len(base_frames) < n_frames:
            base_frames.extend(base_frames)
        base_frames = base_frames[:n_frames]
        args.width = base_frames[0].shape[1]
        args.height = base_frames[0].shape[0]
        if args.x is None:
            args.x = args.width // 2
        if args.y is None:
            args.y = args.height // 2

    work_dir = os.path.expanduser("~/workspace/tmp/energy_blast_frames")
    os.makedirs(work_dir, exist_ok=True)

    print(f"Rendering {n_frames} {args.type} frames...", flush=True)
    for i in range(n_frames):
        t = i / args.fps
        blast = gen(args.width, args.height, t, args.duration)

        if base_frames is not None:
            frame = composite_onto_base(blast, base_frames[i], args.x, args.y)
        else:
            # Standalone: convert BGRA to BGR on black
            b, g, r, a = cv2.split(blast)
            alpha = a.astype(np.float32) / 255
            frame = np.zeros((args.height, args.width, 3), dtype=np.uint8)
            for c, ch in enumerate([b, g, r]):
                frame[:, :, c] = (ch.astype(np.float32) * alpha).astype(np.uint8)

        cv2.imwrite(f"{work_dir}/f{i:05d}.png", frame)

    cmd = ["ffmpeg", "-y", "-v", "error",
           "-framerate", str(args.fps), "-i", f"{work_dir}/f%05d.png",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", args.output]
    subprocess.run(cmd, check=True)

    import shutil
    shutil.rmtree(work_dir)
    print(f"Done: {args.output}")


if __name__ == "__main__":
    main()
