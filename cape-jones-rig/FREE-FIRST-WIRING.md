# Free-first wiring — Mars, 2026-10-31 14:47 CDT

Standing order, in Mars's sense: wire everything up in the freest way possible.
Anything that is not free, reverse-engineer the METHOD and rebuild it free —
methods, systems, timing, passes, node order — never a proprietary character,
logo, asset, or copied code. That is the same line as the standing forbidden
list: characters/names/logos/cries/literal dialogue/town names straight from
another game are out; structure, order, windows, inputs, values, data shapes,
mechanics, and tools are in.

## Free stack actually wired here (not a shopping list)

- Blender 5.2.3 LTS — production compositor, verified `blender --version`.
  Node builder: blender-compositor-stack.py. Blender 4.5.3 on disk is NOT
  the production standard and is not used for production passes.
- FFmpeg — `lut3d` for every .cube in this project (30 base + 24 spectrum +
  16 spectrum v2), delivery encode, -14 LUFS audio target.
- PIL / Python — apply_compositor.py (layer stack, same order as the Blender
  tree), slice_clean.py (clean cuts, component-based, no hand rectangles),
  joint_locked_rig_v7c.py (ball-centre pivots, round-masked caps, no square crops).
- OpenColorIO — bundled with Blender 5.2.3; ACES input/output transform is
  still NOT wired in PIL (stated in WIRED-COMPOSITOR-STATUS.md) — that gap
  is owed, not claimed.
- Free compositing equivalents reverse-engineered from public behaviour:
  Nuke-style pass/AOV compositing -> separate pass PNGs + Plus/Multiply
  merges in PIL and in the Blender tree (see apply_lighting_levels.py);
  DaVinci Resolve grading order -> colour management, primary, secondary,
  look LUT, output transform, in that order in LIGHTING-LEVELS-0-5.md;
  Toon Boom / OpenToonz-style cleanup -> stray-pixel, hole, and line-weight
  metrics in cleanup v2 (owed as a full pass, not claimed done here).

## What "reverse engineer" does NOT mean here

- No downloaded commercial game, ROM, or full proprietary asset in any repo.
- No proprietary character or logo generated or pasted into a shot.
- No paid tool is claimed as installed, and no paid run happens without
  Mars's approval for that specific run (standing GPU rule).

## Counts for this wiring batch

- Pass-based lighting script: apply_lighting_levels.py, levels 0–5, colored +
  non-colored, passes written out separately (shadow, rim, bleed, volume,
  emission, finishing) so each can be tuned without re-rendering.
- LUT totals after this batch: base approved 30/30, spectrum approved 6/24,
  spectrum v2 expanded 16/16 files, approved 0/16. Total .cube files 70.
  Approved total: 36/70 = 51%.
