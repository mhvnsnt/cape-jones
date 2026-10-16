#!/usr/bin/env python3
"""
led_controller.py — Cape Jones in-house LED lighting system.

The concept: Cape Jones has RGB LED strip lights in his house (like real
ones). He hits a button on the controller and the room lighting changes.
This script applies animated LED lighting presets to video.

Each preset uses ffmpeg filters with time (t) expressions for smooth,
real LED-strip behavior:
  - hue=h='...' — hue rotation over time (smooth color cycling)
  - eq=brightness='...'/saturation='...' — pulsing, breathing, strobing

Real LED strip modes this mirrors:
  - FADE: smooth color transitions (chill-blue, sunset-cycle, rainbow)
  - JUMP: abrupt color changes (party-strobe)
  - PULSE/BREATHE: brightness oscillation (purple-pulse, ember-glow)
  - STATIC: solid color (reference looks in grades.py)

Usage:
  led_controller.py input.mp4 output.mp4 --preset chill-blue
  led_controller.py input.mp4 output.mp4 --preset sunset-cycle --speed 2.0
  led_controller.py --list

The --speed multiplier: 1.0 = default, 2.0 = twice as fast, 0.5 = half speed.
"""

import argparse
import subprocess
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grades import get_grade


def _cycle_filter(base_grade, hue_expr, sat_expr=None, bright_expr=None, extra=""):
    """Build a filter chain: base grade + time-varying adjustments."""
    parts = [base_grade] if base_grade else []
    hue_parts = [f"h={hue_expr}"]
    if sat_expr:
        hue_parts.append(f"s={sat_expr}")
    parts.append("hue=" + ":".join(hue_parts))
    eq_parts = []
    if bright_expr:
        eq_parts.append(f"brightness={bright_expr}")
    if eq_parts:
        parts.append("eq=" + ":".join(eq_parts))
    if extra:
        parts.append(extra)
    return ",".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# LED PRESETS
# Each: (display_name, description, builder_function)
# Builder takes speed multiplier, returns ffmpeg filter chain.
# ---------------------------------------------------------------------------

def _preset_chill_blue(speed=1.0):
    # Slow fade between deep blue and cyan. Relaxing, thinking scenes.
    # Period: 24s at 1.0x
    period = 24.0 / speed
    hue_expr = f"200+25*sin(2*PI*t/{period})"
    return _cycle_filter(
        get_grade("led-chill-blue"),
        hue_expr,
        bright_expr=f"0.005*sin(2*PI*t/{period})",
    )


def _preset_purple_pulse(speed=1.0):
    # Deep violet breathing — brightness pulses like a heartbeat.
    # Period: 8s at 1.0x. Cape Jones's signature room mode.
    period = 8.0 / speed
    hue_expr = f"275+10*sin(2*PI*t/{period})"
    return _cycle_filter(
        get_grade("led-deep-purple"),
        hue_expr,
        bright_expr=f"0.03*sin(2*PI*t/{period})",
    )


def _preset_sunset_cycle(speed=1.0):
    # Cycles through the full sunset: orange -> pink -> purple -> blue.
    # Period: 30s at 1.0x. Slow, cinematic.
    period = 30.0 / speed
    hue_expr = f"15+60*sin(2*PI*t/{period})"
    return _cycle_filter(
        get_grade("led-sunset"),
        hue_expr,
        sat_expr="1.4+0.2*sin(2*PI*t/%f)" % period,
    )


def _preset_party_strobe(speed=1.0):
    # Rapid color jumps — NOT smooth. Hard cuts between colors like a
    # real strobe/JUMP mode. Period: 2s at 1.0x (fast!).
    # Uses step function via floor() for abrupt changes.
    period = 2.0 / speed
    # floor creates discrete jumps: 0,1,2,3 -> mapped to hue offsets
    hue_expr = (
        f"0+90*floor(mod(t,{period})/({period}/4))"
    )
    return _cycle_filter(
        get_grade("led-party"),
        hue_expr,
        bright_expr=f"0.04*pow(sin(2*PI*t/{period*0.5}),2)",
    )


def _preset_ghost_mode(speed=1.0):
    # Slow eerie teal-green drift. Ghost cave ambience.
    # Period: 40s at 1.0x. Barely perceptible movement.
    period = 40.0 / speed
    hue_expr = f"165+20*sin(2*PI*t/{period})"
    return _cycle_filter(
        get_grade("led-ghost-teal"),
        hue_expr,
        bright_expr=f"-0.01+0.015*sin(2*PI*t/{period})",
    )


def _preset_ocean_calm(speed=1.0):
    # Slow blue-teal waves, like water reflections on walls.
    # Period: 20s at 1.0x.
    period = 20.0 / speed
    hue_expr = f"190+30*sin(2*PI*t/{period})"
    return _cycle_filter(
        get_grade("led-chill-blue"),
        hue_expr,
        sat_expr="1.3+0.15*sin(2*PI*t/%f+1.5)" % period,
    )


def _preset_ember_glow(speed=1.0):
    # Warm red-orange flicker like a fireplace.
    # Irregular flicker via layered sine waves.
    p1 = 3.0 / speed
    p2 = 7.0 / speed
    hue_expr = f"15+8*sin(2*PI*t/{p1})+5*sin(2*PI*t/{p2})"
    bright_expr = (
        f"0.02*sin(2*PI*t/{p1})+0.015*sin(2*PI*t/{p2}+2)"
    )
    return _cycle_filter(
        get_grade("led-ember"),
        hue_expr,
        bright_expr=bright_expr,
    )


def _preset_rainbow_smooth(speed=1.0):
    # Full spectrum slow cycle. The "demo mode" of LED strips.
    # Period: 36s at 1.0x.
    period = 36.0 / speed
    hue_expr = f"180+180*sin(2*PI*t/{period})"
    return _cycle_filter(
        get_grade("led-party"),
        hue_expr,
        sat_expr="1.5",
    )


PRESETS = {
    "chill-blue": (
        "Chill Blue Fade",
        "Slow fade between deep blue and cyan. Relaxing, thinking scenes. "
        "The cup-lift thinker moment.",
        _preset_chill_blue,
    ),
    "purple-pulse": (
        "Deep Purple Pulse",
        "Violet breathing like a heartbeat. Cape Jones's signature room mode. "
        "Default when he's just vibing.",
        _preset_purple_pulse,
    ),
    "sunset-cycle": (
        "Sunset Cycle",
        "Orange to pink to purple to blue. Slow, cinematic. "
        "Evening wind-down scenes.",
        _preset_sunset_cycle,
    ),
    "party-strobe": (
        "Party Strobe",
        "Rapid hard color jumps. NOT smooth — real JUMP mode. "
        "Use sparingly (Baked Jones scenes).",
        _preset_party_strobe,
    ),
    "ghost-mode": (
        "Ghost Mode",
        "Slow eerie teal-green drift. Barely perceptible. "
        "Ghost cave, spooky scenes, Nosferatu vibing.",
        _preset_ghost_mode,
    ),
    "ocean-calm": (
        "Ocean Calm",
        "Blue-teal waves like water reflections. Beach house feel. "
        "Daytime chilling.",
        _preset_ocean_calm,
    ),
    "ember-glow": (
        "Ember Glow",
        "Fireplace flicker — warm red-orange with irregular movement. "
        "Cozy night scenes.",
        _preset_ember_glow,
    ),
    "rainbow-smooth": (
        "Rainbow Smooth",
        "Full spectrum slow cycle. LED strip demo mode. "
        "Party scenes, montages.",
        _preset_rainbow_smooth,
    ),
}


def get_preset_filter(name, speed=1.0):
    if name not in PRESETS:
        raise ValueError(f"Unknown preset '{name}'. Use --list.")
    return PRESETS[name][2](speed=speed)


def main():
    ap = argparse.ArgumentParser(
        description="Cape Jones LED lighting controller")
    ap.add_argument("input", nargs="?", help="Input video")
    ap.add_argument("output", nargs="?", help="Output video")
    ap.add_argument("--preset", default="purple-pulse",
                    help="LED preset name (see --list)")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="Speed multiplier (default: 1.0)")
    ap.add_argument("--list", action="store_true",
                    help="List all presets and exit")
    ap.add_argument("--crf", type=int, default=18,
                    help="Output quality CRF (default: 18)")
    args = ap.parse_args()

    if args.list:
        print("Cape Jones LED Controller — Presets:\n")
        for key, (name, desc, _) in PRESETS.items():
            print(f"  {key:16s} {name}")
            print(f"  {'':16s} {desc}\n")
        return

    if not args.input or not args.output:
        print("Need input and output. Use --list to see presets.",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    filt = get_preset_filter(args.preset, speed=args.speed)
    name = PRESETS[args.preset][0]
    print(f"LED preset: {name} (speed {args.speed}x)")

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", args.input,
        "-vf", filt,
        "-c:v", "libx264", "-crf", str(args.crf),
        "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        args.output,
    ]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("ffmpeg failed", file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(args.output) / (1024 * 1024)
    print(f"Done: {args.output} ({size:.1f} MB)")


if __name__ == "__main__":
    main()
