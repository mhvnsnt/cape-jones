#!/usr/bin/env python3
"""
fx-particles.py — DETERMINISTIC 2D cartoon FX generator.
Same seed => byte-identical frames, every run. No AI, no randomness leaks.

Renders particle-based cartoon effects as PNG sequences (RGBA) for compositing:
  fire      campfire / blast flame tongues
  smoke     cartoon smoke puffs (expanding, fading)
  sparkle   twinkle stars (magic, hits, transitions)
  speedlines horizontal anime speed streaks
  explosion radial burst + debris + smoke
  magic     rising sparkle column

Usage:
  fx-particles.py --effect smoke --frames 48 --seed 7 --size 1920x1080 --out fx/smoke/
"""
import argparse
import math
import os
import numpy as np
from PIL import Image, ImageDraw

PALETTES = {
    "fire":      [(255, 60, 10), (255, 140, 20), (255, 210, 80), (255, 240, 180)],
    "smoke":     [(90, 90, 95), (130, 130, 135), (170, 170, 175)],
    "sparkle":   [(255, 255, 220), (255, 240, 150), (255, 255, 255)],
    "speedlines": [(255, 255, 255)],
    "explosion": [(255, 80, 10), (255, 160, 40), (120, 120, 125), (60, 60, 65)],
    "magic":     [(180, 220, 255), (255, 200, 255), (255, 255, 255)],
}

def _spawn(rng, effect, w, h):
    """Return a fresh particle dict for the given effect."""
    if effect == "fire":
        return dict(x=rng.uniform(w*0.35, w*0.65), y=h*0.95,
                    vx=rng.uniform(-8, 8), vy=rng.uniform(-260, -160),
                    life=rng.uniform(0.5, 1.1), age=0.0,
                    size=rng.uniform(14, 34), ci=int(rng.integers(0, 4)), kind="fire")
    if effect == "smoke":
        return dict(x=rng.uniform(w*0.35, w*0.65), y=h*0.9,
                    vx=rng.uniform(-14, 14), vy=rng.uniform(-120, -60),
                    life=rng.uniform(1.2, 2.4), age=0.0,
                    size=rng.uniform(26, 54), ci=int(rng.integers(0, 3)), kind="smoke")
    if effect == "sparkle":
        a = rng.uniform(0, 2*math.pi); r = rng.uniform(0, min(w, h)*0.3)
        return dict(x=w/2 + r*math.cos(a), y=h/2 + r*math.sin(a)*0.6,
                    vx=0, vy=0, life=rng.uniform(0.4, 0.9), age=0.0,
                    size=rng.uniform(6, 22), ci=int(rng.integers(0, 3)), kind="sparkle")
    if effect == "speedlines":
        return dict(x=rng.uniform(0, w), y=rng.uniform(0, h),
                    vx=rng.uniform(-1400, -900), vy=0,
                    life=rng.uniform(0.25, 0.5), age=0.0,
                    size=rng.uniform(2, 6), ci=0, kind="speedlines",
                    length=rng.uniform(120, 420))
    if effect == "explosion":
        a = rng.uniform(0, 2*math.pi); sp = rng.uniform(120, 700)
        kind = "debris" if rng.random() < 0.55 else "smoke"
        return dict(x=w/2, y=h/2, vx=sp*math.cos(a), vy=sp*math.sin(a),
                    life=rng.uniform(0.5, 1.6), age=0.0,
                    size=rng.uniform(8, 30), ci=int(rng.integers(0, 4)), kind=kind)
    # magic
    return dict(x=rng.uniform(w*0.3, w*0.7), y=rng.uniform(h*0.5, h),
                vx=rng.uniform(-20, 20), vy=rng.uniform(-200, -90),
                life=rng.uniform(0.8, 1.6), age=0.0,
                size=rng.uniform(5, 16), ci=int(rng.integers(0, 3)), kind="sparkle")

def _update(p, dt):
    p["age"] += dt
    if p["kind"] == "smoke":
        p["vx"] *= (1 - 0.6*dt); p["vy"] *= (1 - 0.4*dt)
    if p["kind"] == "debris":
        p["vy"] += 500*dt
    p["x"] += p["vx"]*dt; p["y"] += p["vy"]*dt

def _draw(draw, p, pal):
    t = p["age"]/p["life"]
    if t >= 1:
        return
    col = pal[p["ci"]]
    if p["kind"] == "fire":
        r = p["size"]*(1-t*0.75); a = int(255*(1-t))
        draw.ellipse([p["x"]-r, p["y"]-r*1.4, p["x"]+r, p["y"]+r*1.4],
                     fill=col+(a,))
    elif p["kind"] in ("smoke", "debris"):
        r = p["size"]*(0.6+t*1.4); a = int(200*(1-t))
        draw.ellipse([p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r], fill=col+(a,))
    elif p["kind"] == "sparkle":
        r = p["size"]*math.sin(math.pi*t); a = int(255*math.sin(math.pi*t))
        draw.line([p["x"]-r, p["y"], p["x"]+r, p["y"]], fill=col+(a,), width=2)
        draw.line([p["x"], p["y"]-r, p["x"], p["y"]+r], fill=col+(a,), width=2)
    elif p["kind"] == "speedlines":
        a = int(220*(1-t))
        draw.line([p["x"], p["y"], p["x"]+p["length"], p["y"]],
                  fill=col+(a,), width=int(p["size"]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--effect", default="smoke",
                    choices=list(PALETTES)+["debris"])
    ap.add_argument("--frames", type=int, default=48)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--out", default="fx_out")
    ap.add_argument("--rate", type=int, default=90,
                    help="particles spawned per second")
    args = ap.parse_args()

    w, h = (int(v) for v in args.size.lower().split("x"))
    dt = 1.0/args.fps
    rng = np.random.default_rng(args.seed)
    pal = PALETTES["explosion"] if args.effect == "debris" else PALETTES[args.effect]
    os.makedirs(args.out, exist_ok=True)

    particles, carry = [], 0.0
    for f in range(args.frames):
        carry += args.rate*dt
        while carry >= 1:
            particles.append(_spawn(rng, args.effect, w, h)); carry -= 1
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img, "RGBA")
        alive = []
        for p in particles:
            _update(p, dt)
            if p["age"] < p["life"]:
                _draw(draw, p, pal); alive.append(p)
        particles = alive
        img.save(os.path.join(args.out, f"fx_{f:04d}.png"))
    print(f"wrote {args.frames} frames to {args.out}/ (seed={args.seed})")

if __name__ == "__main__":
    main()
