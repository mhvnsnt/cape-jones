# Living Room Scene — Integration (scene wave assembly)

**Lane:** `scene/integration-20261017` | **Date:** 2026-10-18
**Owner directive:** 2026-10-17 ~20:51 CDT — "Living room becomes fully functional"
**Assembled from (all merged on origin/main):** PR #123 (recliner), #129 (TV),
#132 (lighting), #131 (sit targets), #126 (research).

## Assembly order (code: `integrate_scene.py`, one headless session)

1. **Recliner (PR #123).** LINKED the `Recliner` collection from
   `living-room/recliner/recliner_rigged.blend` — armature lands at canon
   placement (2.653, 2.312, 0), rot Z 270°, verified in-script. Closed state
   default (`recline` = 0). The static `loungeChairRelax(Clone)` mesh is KEPT
   in the file but hidden (viewport + render) — the rigged recliner IS the
   chair now. Library path rewritten repo-relative
   (`//living-room/recliner/recliner_rigged.blend`) so the committed blend is
   portable. The temporary `CapeJones_ScaleCheck` standing figure was removed
   (its job — the 0.925 m scale check — is done; the real rigged character is
   seated now).
2. **TV console yaw (staging decision, see below)** — then `tv/tv_setup.py`,
   TV power **ON** (hero look). `TV_Glow` repositioned along the yawed screen
   normal (tv_setup hardcodes the pre-yaw position). Screen sequence path
   rewritten repo-relative (`//living-room/tv/frames/tv_show_0001.png`).
   Saved state: mix factor = 1.0 (emission), glow = 14.0 — the committed blend
   renders TV-ON even in a session where the handler wasn't re-run.
   **Frame-1 save:** the linked recliner carries the `ReclinerOpen` action
   (frames 1–24, `recline` 0→1), so the blend is saved at **frame 1** for the
   closed default (`recline` = 0 — verified at save). The TV image sequence is
   offset (`image_user.frame_offset = 47`) so frame 1 shows the "CAPE JONES /
   TONIGHT" title card instead of the static burst.
3. **Lighting (PR #132).** `lighting/apply_lighting_rig.py` (self-verifying:
   preset 1 → RED through the driver alone, preset 0 → canon violet 1e-4),
   then `set_led_preset.py -- 0` for a deterministic headless state. Locked
   defaults untouched (RoomLight 300 / violet, Sun 1.5, HallLight 60, LED 4.0).
4. **Sitting (PR #131).** `sit-targets/place_sitter.py -- pose_sit_normal`.
   All 5 of its gates PASS (ankle 0.064, pelvis 0.409, soles 0.000, zero
   body-vs-chair overlap). Own extra gate: BVH body vs the LINKED recliner
   (closed) = 0 overlapping face pairs. Character scale 0.925 locked —
   armature object transform untouched (loc 0, scale 1).
5. **Research (PR #126).** Consulted `docs/research/SCENE-FULLSTACK.md`: the
   applicable pieces (god-ray volume kit, LED 3D presets, CRT stack) were
   already wired by the lighting/TV lanes; nothing further to apply at
   assembly time. The pulled studio tools (Light Editor, Render Manager,
   Extra Lights) remain available under `tools/` for look-dev.

All 20 in-script checks passed; the blend was saved once, at the end.

**Post-assembly correction (`fixup_frame1.py`, same lane, 2026-10-18):** the
first save sat at frame 48, where the linked `ReclinerOpen` action (frames
1–24) holds `recline` at 1.0 — violating the closed default. The fixup
re-ran `tv_setup.py`, re-applied the repo-relative paths + yawed glow
position (tv_setup resets both to its hardcoded defaults), set
`image_user.frame_offset = 47`, and re-saved at **frame 1** (`recline` = 0
verified at save, TV still ON). `integrate_scene.py` now contains the
corrected logic end-to-end; the fixup script is kept for provenance.

## The TV-yaw staging decision

**Finding:** the TV lane measured the screen facing −Y — from the chair the
screen was ~90° off-axis (edge-on). The CHAIR's placement is canon-locked and
cannot move.

**Decision:** yaw the TV console (a prop — placement not locked) by **84.53°**
about Z around pivot (−0.9, 2.45, 0), aiming the screen normal at the seated
viewer's face zone (3.10, 2.067, 1.05). Measured result: **0.60° off-axis**
(dead-on). The 15 cm shift off the back wall was REQUIRED: at full yaw the
cabinet's back edge would otherwise sit 8.6 cm inside the wall (inner face
y = 2.925); after the shift the console's y-max is 2.779 (6.4 cm clear, no
clipping). The yaw lives on a `TVConsole_Yaw` empty, so the angle stays
tweakable. POV render from the sitter's eyes confirms the title card reads
cleanly.

## Canon locks honored

- Colorway: zero changes (no material touched except the TV screen's own
  `tvScreenMat`, which the TV lane owns).
- Character scale 0.925 m: armature object transform untouched.
- Mug: untouched (`okayest_hero_mug` still in place).
- Locked lighting defaults: unchanged (verified RoomLight energy/color).
- Chair placement: fixed at (2.653, 2.312, 0) — the linked armature carries
  the exact source transform.

## How to re-run the setup in a FRESH session (renders)

Frame-change handlers do **not** persist in .blend files, and Blender 4.0
headless ignores scripted drivers at render time — so before any headless
render, re-run (idempotent, seconds):

```bash
blender -b 3d-assets/living_room.blend --python 3d-assets/living-room/tv/tv_setup.py \
    --python-expr "
import bpy
tv = bpy.data.objects['crt_tv']
tv['tv_power'] = 1.0          # 0.0 = off
tv.update_tag()               # REQUIRED: ID-prop writes don't tag the depsgraph;
                              # without this the TV_Glow driver re-evaluates stale (p=0)
                              # and wipes the handler's value (verified 2026-10-18)
mat = bpy.data.materials['tvScreenMat']
tex = next(n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE')
tex.image_user.frame_offset = 47  # title card on frame 1 (tv_setup rebuilds the node tree)
bpy.context.scene.frame_set(1)    # frame 1 = recliner closed + TV title card
"
```

Then render. The committed blend already has TV-ON baked as stored values
(mix = 1.0, glow = 14.0), so it renders correctly even without the re-run —
but toggling power headless REQUIRES the handler.

LED gag presets headless (deterministic, no driver reliance):

```bash
blender -b 3d-assets/living_room.blend --python 3d-assets/living-room/lighting/set_led_preset.py -- <0..3> [env 0|1]
```

0 = canon violet, 1 = RED, 2 = BLUE, 3 = broken-streetlight purple.

## Verification (own eyes, Cycles CPU 960×540)

- `renders/integration_hero.png` — him seated on the recliner watching TV
  (TV ON, "CAPE JONES / TONIGHT" title card readable), canon violet look.
- `renders/integration_pov.png` — sight-line from the sitter's eyes: screen
  dead-on, content readable (the yaw decision, proven).
- `renders/integration_open.png` — recliner fully open with him seated
  (posed via direct bone writes on an appended copy — 4.0 headless ignores
  the `recline` drivers at render; BVH body-vs-open-recliner reported).
- `renders/integration_red.png` — lighting gag, preset 1 (RED).
- `renders/integration_godray.png` — WindowShaft god rays, vol 0.03.

Zero clipping, no floating, feet flat on the floor in all shots.

## KNOWN OPEN ITEM (do not attempt in this lane)

True legs-up-on-footrest sitting needs the pose lane to articulate the thighs
~70° at the hips — no root translation can fake it (sit lane's finding, this
lane confirms). Flagged, not faked.

## Gotchas found while integrating (for the next lanes)

1. `obj.parent = empty; obj.matrix_parent_inverse = empty.matrix_world.inverted()
   @ obj.matrix_world` DOUBLE-APPLIES the child local matrix (Blender 4.0).
   Use `bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)`.
2. Setting `tv['tv_power']` then `frame_set()` without `tv.update_tag()` lets
   the TV_Glow driver re-evaluate stale (p=0) and overwrite the handler's
   14.0 with 0.0. Always `update_tag()` after ID-prop writes (lighting lane
   knew this; the TV setup path needed it too).
3. `cabinetTelevision(Clone)` mesh has no vertices — bbox checks must use
   `bound_box` over the whole console group.
