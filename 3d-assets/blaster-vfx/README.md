# Blaster VFX — 3D build

Canon: `docs/blaster/BLASTER-VFX-SPEC.md` (built off sheets 03 + 04, palette locked 2026-10-17).

## What this is

A procedural, headless-buildable blaster FX system for Cape Jones's gauntlet blasters:
- `CJ_BlasterFX` geometry-node group — charge rings, energy beam (white core + amber shell), zigzag beam tip, burst flash, sparks, all driven by `Charge` / `Fire` / `Seed` / `BeamLength` inputs.
- Canon materials: `CJ_FX_Core` (#FFFFFF), `CJ_FX_Glow` (#FFB300), `CJ_FX_Arc` (cyan).
- `blaster_fx.blend` — the built file: FX object + `CJ_BlasterDriver` empty (custom props `charge`, `fire`, `recoil`) + proof scene (dark void, motivated cyan rim rig, blast-color rim takeover, amber cast light).
- `proof/` — rendered proof frames (`blaster_charge_proof.png`, `blaster_fire_proof.png`). The owner signs off with his own eyes.

## Palette

`blaster_palette.json` is the single source of truth for blaster colors (wardrobe recolor system). Edit it, rebuild, done. Locked values come from the owner 2026-10-17 ~10:24 CDT — don't invent colors.

## Rebuild

```bash
cd 3d-assets/blaster-vfx
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python build_blasterfx.py -- ./blaster_fx.blend
# proof renders only (no rebuild):
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b ./blaster_fx.blend --python proof_renders.py
```

Blender 4.0.2 notes: no torus primitive (rings are curve-circle → curve-to-mesh), no GN texture nodes (jitter is per-vertex Random Value), Distribute Points in Volume needs Mesh-to-Volume. The script handles all of this.

## Using it in a shot

1. Link/append `CJ_BlasterFX` (the object) and `CJ_BlasterDriver` (the empty) into the shot file.
2. Parent the FX object to the rig's `blaster_*` bone (Bone parent — the rig file itself is NOT edited; rig lane owns it).
3. Keyframe `charge` / `fire` / `recoil` on the driver empty per the state machine in the spec (§3): charge 24–36f, hold 12f, fire 3f snap, recoil 12f, settle 12f. Comedy timing: build it too long, hold the beat, BANG.
4. The `fire` prop also crossfades the scene's rim rig to the blaster color (blaster lighting concept, 2026-10-17 ~10:36) — wire the shot's rim lights the same way in real scenes.

## Scout pull-ins (lane 4, 2026-10-17 — landed)

- **FXType socket** (`fx_type` prop): 0=energy_beam, 1=gauntlet_bolt (stretched burst),
  2=wave_pulse (expanding torus), 3=arc_chain (rings + sparks). Implements the palette's
  `type_personalities`; parts gate per-type, existing beam look untouched.
- **Per-scene tint** (`tint_r/g/b` props → `CJ_Tint` attribute → `CJ_FX_GlowTint` material):
  recolors glow/rings/sparks/pulse per scene; **core stays #FFFFFF** (canon).
- **CJ_BlastLightRig** collection: blast point light + cyan rim + blast rim (fire-crossfade).
  Append the collection + `CJ_BlasterDriver` into the shot; the blast light becomes the
  scene lighting while firing (rim + spill), per the 2026-10-17 lighting concept.
- **Impact flash + ring** at the beam terminus (sheet 04).
- Open-source technique studied: `laishi/GeometryNodesByTutorials` Ch.31 lightning (MIT) —
  studied only, nothing copied; our arcs were already per-vertex jitter (4.0 has no GN textures).
