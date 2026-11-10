# Functional TV — integration guide

Lane 3 of the living-room scene wave (owner directive 2026-10-17 ~20:51 CDT:
"His TV and stuff needs to turn on and be able to have stuff on the screen").

This folder is applied to `3d-assets/living_room.blend` by the **integration
lane**. The `.blend` itself is deliberately NOT modified in this lane's commit.

## What this delivers

- **Power control** — custom property `tv_power` (0.0–1.0) on the `crt_tv`
  object. `0` = off (dark glass screen), `1` = on (emissive screen content).
  Animatable / keyframable like any property.
- **Screen content** — `frames/tv_show_0001.png` … `tv_show_0048.png`
  (320×240, 48 frames @ 12 fps = 4 s loop, ~2.6 MB total). 100% original:
  static burst → color bars resolving in ("CJ-TV" bug) → animated original
  short (caped silhouette gliding over a dusk city skyline) → "CAPE JONES /
  TONIGHT" title card. Loops cyclically. No copyrighted material.
- **Light contribution** — a `TV_Glow` point light (cool white, energy driven
  by `tv_power`, no shadows) sits just in front of the screen so the TV throws
  spill on the stand/floor when on. Ownership: **this lane owns the TV screen
  and TV_Glow**; the lighting lane owns the room lights. If the lighting lane
  rebalances, TV_Glow's driver expression (`p * 14.0`) is the single knob.

## How to apply (integration lane)

```bash
blender -b 3d-assets/living_room.blend \
    --python 3d-assets/living-room/tv/tv_setup.py
```

The script is idempotent — re-running rebuilds the `tvScreenMat` node tree,
reloads the image sequence, and reuses/creates `TV_Glow`. It expects
`crt_tv`, `crt_screen`, and `tvScreenMat` (all present in the canon scene).

Toggle power, then render — that's it:

```python
bpy.data.objects["crt_tv"]["tv_power"] = 1.0  # on   (0.0 = off)
```

The `cj_tv_apply_power` frame-change handler installed by the script reads
`tv_power` fresh at every frame change and switches the screen material +
glow light, so headless renders always honor the switch. Keyframing
`tv_power` works too (standard animation workflow).

Blender 4.0 headless quirk (verified 2026-10-17, don't "simplify" this away):
drivers installed on the screen mix and glow light evaluate in the viewport
depsgraph but do NOT propagate into `bpy.ops.render.render()` here — neither
`update_tag()` after writing the property nor keyframing changes that. The
handler is the mechanism that makes renders work; the drivers remain for
live interactive use. Frame-change handlers don't persist in the `.blend`,
so re-run `tv_setup.py` in any fresh session before headless renders
(it's idempotent, takes seconds).

## Staging note for the integration lane (sight-line finding)

Measured on origin/main: the chair sits at (2.653, 2.312, 0) at 270° yaw,
facing the TV dead-on — but the TV *screen* faces -Y (into the room from the
back wall), so from the chair the screen is ~90° off-axis (edge-on). The
power/glow rig works from any angle, but screen *content* is only readable
from the -Y side of the room (front/sofa area). If the owner wants content
readable from the chair, the TV needs a yaw tweak or the chair needs
re-staging — that's a staging decision for the integration/sitting lanes,
not this one (no furniture was moved here).

## Canon notes

- Zero color changes to the room. The screen's OFF state is near-black glass;
  the ON content is new screen material, not room colorway. Title-card accent
  uses the room's violet `#731AE5` as a deliberate tie-in.
- Mug untouched, chair/TV placement untouched, no geometry changes at all —
  this lane only touches the screen material, one custom property, and one new
  light.

## Verification (this lane)

Rendered headless, Cycles CPU, 960×540 @ 64 samples (canon settings):

- `renders/tv-off.png` — `tv_power = 0` from the chair viewpoint: dark glass
  screen, no glow.
- `renders/tv-on.png` — `tv_power = 1` (frame 30) from the chair viewpoint:
  TV_Glow spill visible on the stand; screen edge-on from here (see staging
  note above).
- `renders/tv-content.png` — `tv_power = 1` (frame 30) from a screen-readable
  3/4 viewpoint: the animated show (caped silhouette over the dusk skyline)
  readable on the screen.

All three verified by eye before the PR. The power switch was validated
headless through the full matrix: drivers alone (invalid in renders here),
`update_tag()` after property writes (viewport-only), keyframed property
(renders ignore it) — the frame-change handler is the verified-working
mechanism and is what the committed renders used.
