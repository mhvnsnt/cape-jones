# Recliner mechanism — working leg rest for the sitting scene (2026-10-23)

Recorded from the lane's completion report; release `recliner-mech-20261023`
(blend + 3 proof renders) verified present on GitHub 2026-10-23.

## Source

- `scene_recliner_mech.blend` — copy of placed3; the original placed3 is
  untouched (sha re-verified after the copy).
- Release: https://github.com/mhvnsnt/cape-jones/releases/tag/recliner-mech-20261023
  - `scene_recliner_mech.blend` (164,790,998 B)
  - `mech_r0_v1.png`, `mech_r50_v1.png`, `mech_r100_v1.png` (proof renders)

## Build

- Repo `recliner_rigged` parts appended: the same 308-vert chair split into
  base / backrest / shank / pad / armrests / legs.
- Canonical retraction applied to the rigged parts (66 verts; closed bbox
  exactly x 2.858..3.328).

## Rig

- ONE driver: `recliner_rig["recline"]`, 0..1.
  - backrest -26 degrees, shank -50 degrees, pad counter-rotates level.
- Leg coupling per the PR #166 pattern: FootPadTarget empties on the pad
  bone + ReclinerFollow constraints + IK blend drivers; coupling curve
  `clamp((recline-0.1)/0.55)` — a linear ramp clipped the shin at 0.5.

## Measurements (frame 40)

- pad-to-shin gap 0.4-1.7mm at all steps 0->1 (near-contact, never negative)
- shin bone clearance positive everywhere
- foot lift at recline 1 = +137/+134mm

## Proof

Renders `mech_r0` / `mech_r50` / `mech_r100` in
`~/workspace/your_files/recliner-mech/` — viewed by the lane AND by the
lane owner: closed = canonical shot; full = back tipped, feet up on the pad.

## Gotcha

Headless Blender 4.0.2 drivers go stale unless
`update_tag(refresh={'DATA'})` is called before `view_layer.update()`.
