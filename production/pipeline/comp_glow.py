#!/usr/bin/env python3
"""
comp_glow.py — 2D animation compositing effects (CPU-only, ffmpeg-based).

Applies studio-style compositing to 2D animation frames:
  --glow        : neon/energy glow (for blasts, eyes, LED effects)
  --light-wrap  : light wrap / bloom spill (character over bright backgrounds)
  --atmosphere  : depth haze / volumetric feel (backgrounds)
  --vignette    : subtle edge darkening for focus

These are the Natron/After Effects compositing staples, rebuilt as
scriptable ffmpeg filters so they run headless in the pipeline.

Usage:
  python3 comp_glow.py input.mp4 output.mp4 --glow 0.8
  python3 comp_glow.py input.mp4 output.mp4 --glow 0.8 --light-wrap 0.5 --atmosphere 0.3
  python3 comp_glow.py input.mp4 output.mp4 --preset energy-blast
  python3 comp_glow.py input.mp4 output.mp4 --list-presets

Presets:
  energy-blast  : heavy glow + light wrap (for gauntlet blasts)
  neon-sign     : medium glow (for signage, LED strips)
  dream         : atmosphere + soft glow + vignette (flashback/dream scenes)
  night-exterior: light wrap + vignette (purple streetlight scenes)
  subtle        : tiny glow + vignette (general polish pass)

All effects are additive-safe for the Cape Jones locked palette:
glow uses screen/add blending so white suit (#FFFFFF) stays blown out.
"""
import argparse
import subprocess
import sys
import shutil


def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        sys.exit("ERROR: ffmpeg not found in PATH")


def build_filter(args) -> str:
    """Build the ffmpeg -vf filter chain."""
    filters = []

    if args.preset:
        p = PRESETS.get(args.preset)
        if not p:
            sys.exit(f"ERROR: unknown preset '{args.preset}'. Use --list-presets.")
        # merge preset values into args
        for k, v in p.items():
            if getattr(args, k, 0) == 0:
                setattr(args, k, v)

    g = args.glow
    lw = args.light_wrap
    at = args.atmosphere
    vg = args.vignette

    if g > 0:
        # Bloom-style glow: blur a copy, screen-blend it back.
        # split -> [a][b]; [b] gblur -> screen with [a]
        # Strength scales blur sigma and mix.
        sigma = 8 + g * 20
        filters.append(
            f"split[a][b];[b]gblur=sigma={sigma:.1f}[blur];"
            f"[a][blur]blend=all_mode=screen:all_opacity={min(g,1.0):.2f}"
        )
    if lw > 0:
        # Light wrap: erode-blur the luma, add it back softly.
        # Approximates background light spilling onto character edges.
        filters.append(
            f"split[c][d];[d]gblur=sigma={4 + lw*10:.1f},"
            f"eq=brightness={lw*0.15:.2f}[wrap];"
            f"[c][wrap]blend=all_mode=addition:all_opacity={lw*0.5:.2f}"
        )
    if at > 0:
        # Atmosphere: lift blacks slightly + desaturate a touch for depth haze.
        filters.append(
            f"eq=brightness={at*0.06:.2f}:saturation={1.0 - at*0.15:.2f}"
        )
    if vg > 0:
        filters.append(f"vignette=PI/4*{vg:.2f}")

    return ",".join(filters)


PRESETS = {
    "energy-blast":  {"glow": 1.0, "light_wrap": 0.7, "atmosphere": 0.0, "vignette": 0.2},
    "neon-sign":     {"glow": 0.6, "light_wrap": 0.3, "atmosphere": 0.0, "vignette": 0.0},
    "dream":         {"glow": 0.4, "light_wrap": 0.0, "atmosphere": 0.5, "vignette": 0.5},
    "night-exterior":{"glow": 0.2, "light_wrap": 0.5, "atmosphere": 0.3, "vignette": 0.4},
    "subtle":        {"glow": 0.25, "light_wrap": 0.0, "atmosphere": 0.0, "vignette": 0.25},
}


def main():
    ap = argparse.ArgumentParser(description="2D compositing effects for animation")
    ap.add_argument("input", nargs="?", help="input video")
    ap.add_argument("output", nargs="?", help="output video")
    ap.add_argument("--glow", type=float, default=0.0, help="0.0-1.0 neon/bloom glow")
    ap.add_argument("--light-wrap", type=float, default=0.0, help="0.0-1.0 light spill")
    ap.add_argument("--atmosphere", type=float, default=0.0, help="0.0-1.0 depth haze")
    ap.add_argument("--vignette", type=float, default=0.0, help="0.0-1.0 edge vignette")
    ap.add_argument("--preset", default=None, help="preset name")
    ap.add_argument("--list-presets", action="store_true", help="list presets and exit")
    ap.add_argument("--crf", type=int, default=18, help="output quality (default 18)")
    ns = ap.parse_args()

    if ns.list_presets:
        for name, vals in PRESETS.items():
            print(f"  {name}: {vals}")
        return

    if not ns.input or not ns.output:
        ap.error("input and output required (unless --list-presets)")

    check_ffmpeg()
    vf = build_filter(ns)
    if not vf:
        sys.exit("ERROR: no effects selected (all values 0 and no preset)")

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", ns.input,
        "-vf", vf,
        "-c:v", "libx264", "-crf", str(ns.crf),
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        ns.output,
    ]
    print(f"filter: {vf}", file=sys.stderr)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(f"ERROR: ffmpeg failed (code {r.returncode})")
    print(f"wrote {ns.output}")


if __name__ == "__main__":
    main()
