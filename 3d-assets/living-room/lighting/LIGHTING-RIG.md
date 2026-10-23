# Lighting + Volumetrics Rig — Living Room (Lane 4)

Owner directive 2026-10-17 ~20:51 CDT: "The lights need to be able to change
color... actual god rays and ray casting."

**Canon is locked.** All locked values live in `../SCENE-CANON.md` and are NOT
changed by this rig. The rig ADDS drivable controls around them.

## Locked defaults (untouched)

| Light | Type | Color | Energy | Location |
|---|---|---|---|---|
| RoomLight | POINT | violet (0.45,0.10,0.90) ≈ #731AE5 | 300 | (0,0,2.4) |
| Sun | SUN | white | 1.5 | (2,-4,5) |
| HallLight | POINT | warm (1.0,0.914,0.588) | 60 | (-2.6,4.4,2.2) |
| LED strips | emission | #731AE5 | 4.0 | — |
| World | — | (0.051) dark | — | — |
| Render | Cycles | 960×540 @50% (480×270), 24 samples | — | — |

## The rig

`apply_lighting_rig.py` (run by the integration lane on the OPEN blend —
never hand-edit, never commit a re-saved `living_room.blend` from it):

```
blender -b 3d-assets/living_room.blend \
    --python 3d-assets/living-room/lighting/apply_lighting_rig.py
```

**Additive only.** It creates:

1. **`LED_RemoteRig`** — a control Empty with drivable custom properties:
   - `preset` (0..3): 0 = DEFAULT violet #731AE5 (canon),
     1 = RED, 2 = BLUE, 3 = BROKEN_STREETLIGHT purple (parking-lot gag)
     — the colors match the LED remote button materials per SHOW-BIBLE.md §8.
   - `environment` (0..1): 0 = ROOM (rim = LED color), 1 = SPACE (rim = cyan).
   - `vol_density` (0..0.2): room volume scatter density; 0 disables god rays.
   - `rim_energy` (0..500): RimLight energy.
2. **Drivers** (plain scripted expressions, no addons):
   - `RoomLight.color` and LEDStripMat emission color ← `preset`.
   - `RimLight.color` ← cyan when `environment==1` (SPACE), else LED preset color.
   - `VolumeMat_Room` Principled Volume density ← `vol_density`.
   - `RimLight.energy` ← `rim_energy`.
3. **Volumetric spots** (all additive new objects):
   - `VolumeBox_Room`: room-sized box (x ±3.5, y ±3, z 0..3) with
     Principled Volume, density 0.015 default, anisotropy 0.7. Camera stays
     outside it. Subtle scatter so shafts read on camera.
     **CRITICAL:** the box faces MUST wind outward. An earlier revision had
     inverted normals; Cycles then treats the interior as exterior and the
     volume silently does not scatter — a 400W beam in 0.05 density renders
     pitch black. If your god rays are invisible, check face winding first.
   - `LampCone_Floor` / `LampCone_Table`: warm SPOTs under the floor-lamp and
     table-lamp shades (from the real lamp positions).
   - `WindowShaft`: cool SPOT just inside the window plane at (3.30, 1.50, 2.00)
     → toward (-1.20, -0.20, 0.0) → the visible god-ray shaft. Position is
     INSIDE the room volume (wall inner face ≈ x=3.45); an earlier revision at
     x=3.80 sat outside the room and the wall self-shadowed the beam.
   - `RimLight`: env-driven rim/fill SPOT on the recliner subject zone
     ((2.60, 3.40, 2.60) → (3.14, 1.20, 0.50)).

The script self-verifies on every apply: preset 1 evaluates to RED **through
the driver alone** (no direct color writes in the check), and preset 0
evaluates back to the exact canon violet (tolerance 1e-4). If either fails it
asserts and the lane knows immediately.

Headless note (Blender 4.0): assigning an ID property does NOT tag the
depsgraph, so every script calls `rig.update_tag()` + `frame_set()` before
reading driven values. That one-line omission silently leaves stale driver
values — all three scripts carry the fix.

## Headless preset setter

`set_led_preset.py` — authoritative setter for render automation:

```
blender -b rigged.blend --python set_led_preset.py -- <preset 0..3> [env 0..1] [out.blend]
```

Writes `rig["preset"]`/`rig["environment"]` AND the driven colors directly
(RoomLight, LEDStripMat emission, RimLight). Deterministic in background mode
— does not rely on drivers for headless renders. The drivers agree for
interactive use.

## Proof renderer

`render_proof.py` — renders IN MEMORY ONLY, never re-saves the blend:

```
blender -b rigged.blend --python render_proof.py -- <preset> <camera> <out.png> [samples] [env] [vol_density]
```

Sets Cycles, 960×540@50%, OpenImageDenoise, **volume_bounces = 0**
(single-scatter god rays: fast and they read on camera). Canon = 24 samples.
Optional 6th arg overrides `vol_density` for this render only.

## Render-time guidance (volumetrics are the cost)

| Target | Volume bounces | Samples | Density | Notes |
|---|---|---|---|---|
| Canon proof (CPU) | 0 | 24 | 0.015 | exact canon look; shafts subtle but present |
| Cleaner CPU preview | 0 | 64 | 0.015–0.03 | denoise on |
| Colab GPU shot | 1–2 | 96–128 | 0.015–0.03 | GPU handles this at 960×540@50% in ~1–2 min |
| Cinematic | 2 | 256 | 0.03 | night-before-render territory |

Rules of thumb:
- Keep `vol_density` ≤ 0.03 unless the gag needs haze. Higher = noise, not beauty.
- Anisotropy 0.7 forwards-scatters the shafts toward camera. Lower (0.0) =
  softer room glow; higher = visible directional shafts.
- `volume_bounces = 0` kills multi-scatter noise; god rays are dominated by
  single scatter. Raise to 1–2 only for wide shots where bounces matter.
- Denoise is mandatory at 24–64 samples (OpenImageDenoise on CPU, OptiX on GPU).
- The volume box is finite — nothing leaks into the world outside the room,
  so the dark-world look (0.051) stays intact.
- Ray casting is real: all three volumetric spots use shadows (`use_shadow =
  True`), so furniture blocks the shafts — rays read as geometry-driven beams.

## Rim behavior (canon)

Blaster/LED colors drive rim + environment (SHOW-BIBLE.md §8):
- SPACE scenes → rim is **cyan** (remote BtnMat_5 #00FFFF) regardless of preset.
- LED/room scenes → rim follows the active preset color.
Default = violet; the rim rig only adds the driver.

## Verification renders (own eyes, CPU)

`renders/`: `proof-violet.png` (preset 0, MainCam, 24 samples — canon),
`proof-red.png` (preset 1, MainCam — gag color), `proof-godrays.png`
(GodRayCam side-on to the window shaft, density 0.04, 64 samples,
volume_bounces=2 — the shaft reads as a real volumetric beam),
`proof-cyan-rim.png` (preset 0 + environment=1, MainCam — rim driver verified
numerically to evaluate cyan (0,1,1); the rim spot itself targets the
recliner zone, off the MainCam axis, so the visual difference is subtle).
`proof-shaft.png` is a superseded early angle; `proof-godrays.png` is the
keeper.

**Debugging note (earned the hard way):** when a volumetric spot appears dark,
check the CAMERA FRAMING first, not the light. The rig's spots were verified
working (fresh-spot control renders emit correctly; save/reload preserves
them). The beam is narrow (38°) and hits a specific floor zone — a camera
aimed at an empty wall corner sees nothing even at 2000W. Frame the beam's
actual path (window → floor target) side-on. Also: dim ambient for shaft
legibility — god rays need darkness, same as on a real set.
Integration lane: apply the rig, set preset/env per the remote gag in the
scene script, animate `LED_RemoteRig` custom props — the drivers do the rest.
