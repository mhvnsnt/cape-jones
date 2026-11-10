#!/usr/bin/env python3
"""
retro_fx.py — VHS / CRT / retro video effects for Cape Jones (trippy vibe).

All ffmpeg-based, CPU only. Chainable with the rest of post-pipeline.

Effects:
  --vhs         Tracking distortion + chromatic aberration + noise + soft blur
  --crt         Scanlines + screen curvature vignette + phosphor glow
  --chromatic   RGB channel shift (aberration) only
  --noise       Animated film grain only
  --scanlines   Scanline overlay only

Examples:
  python3 retro_fx.py --vhs input.mp4 -o output.mp4
  python3 retro_fx.py --crt --scanlines input.mp4 -o output.mp4 --intensity 0.7
"""
import argparse, subprocess, sys


def build_filter(args):
    parts = []
    it = args.intensity

    if args.chromatic or args.vhs:
        # RGB shift: shift red/blue channels horizontally
        shift = int(3 * it) or 2
        parts.append(
            f"split[a][b];[a]crop=iw-{shift*2}:ih:{shift}:0,setsar=1[r];"
            f"[b]crop=iw-{shift*2}:ih:0:0,setsar=1[c]"
            # recombine below via mergeplanes is complex; use rgbashift instead
        )
        parts = []  # reset — use simpler rgbashift
        parts.append(f"rgbashift=rh={shift}:rv=0:bh=-{shift}:bv=0")

    if args.noise or args.vhs:
        amt = 8 * it
        parts.append(f"noise=alls={amt:.0f}:allf=t")

    if args.scanlines or args.crt:
        # scanlines via drawgrid
        parts.append("drawgrid=w=iw:h=3:t=3:c=black@0.25")

    if args.crt:
        # vignette for CRT curvature feel + slight saturation pop
        parts.append("vignette=PI/4.2")
        parts.append("eq=saturation=1.15:contrast=1.05")

    if args.vhs:
        # soft blur + slight contrast crush + tracking wobble
        parts.append("gblur=sigma=0.6")
        parts.append("eq=contrast=1.08:brightness=-0.02")
        # horizontal tracking jitter
        parts.append(
            "crop=iw-8:ih:x='4+3*sin(2*PI*t*0.7)+2*sin(2*PI*t*13.7)':y=0,"
            "scale=iw+8:ih"
        )

    return ",".join(parts)


def main():
    ap = argparse.ArgumentParser(description="VHS/CRT retro effects")
    ap.add_argument("input", help="Input video")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--vhs", action="store_true")
    ap.add_argument("--crt", action="store_true")
    ap.add_argument("--chromatic", action="store_true")
    ap.add_argument("--noise", action="store_true")
    ap.add_argument("--scanlines", action="store_true")
    ap.add_argument("--intensity", type=float, default=1.0,
                    help="Effect strength 0.1-2.0 (default 1.0)")
    args = ap.parse_args()

    if not any([args.vhs, args.crt, args.chromatic, args.noise, args.scanlines]):
        sys.exit("Pick at least one effect: --vhs --crt --chromatic --noise --scanlines")

    vf = build_filter(args)
    print(f"filter: {vf}")
    cmd = ["ffmpeg", "-y", "-i", args.input,
           "-vf", vf, "-c:v", "libx264", "-preset", "medium",
           "-crf", "18", "-c:a", "copy", args.output]
    subprocess.run(cmd, check=True)
    print(f"retro fx -> {args.output}")


if __name__ == "__main__":
    main()
