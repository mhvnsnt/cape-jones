# EFFECTS DESIGN V2 — effects that affect the world (Mars, 2026-10-31)

## Why V2 exists

Mars sent the effects design back, more than once: the old effects were
lacking. Flat coloured pieces of lines and circles do not count. Every
system below must, by design, do three things at once:

1. **AFFECT THE WORLD** — light, shadow, fog, or matter in the scene changes.
2. **CREATE LIGHTING** — the effect is itself a light source, or it bends,
   blocks, or scatters one.
3. **BRING SOMETHING TO THE ATMOSPHERE** — the air, the mood, the depth of
   the shot changes, not just a shape pasted on top.

Standing rules, unchanged: flat PIL VFX is DRAFT ONLY, never production.
Production VFX = Blender 5.2.3 LTS compositor + authored VFX, GPU run when
needed. Never recolour base art — light/shadow/bleed live on separate
layers. Rim follows the key/LUT hue family ±20°; the dual-light exception
applies only when BOTH sources are named in the shot spec. Labels are
debug only, never in finals.

Blender version notes found while building the V2 proof (2026-10-31):
Blender 5.2.3 changed the compositor API versus older tutorials. Sun Beams
is a **Glare type**, not a separate node. The Composite node is gone; the
Mix node is `ShaderNodeMix` (Factor = inputs[0], A_Color = inputs[6],
B_Color = inputs[7], Result_Color = outputs[2]). Glare nodes output ONLY
the glow pass — the original image must be added back with a Mix (ADD),
or a chained Glare stack goes black. Principled BSDF is
`ShaderNodeBsdfPrincipled`. Headless note: the compositor device must be
set to CPU on this VM (GPU device fails with EGL errors and the
compositor produces an empty result).

## The 12 systems

### 1. Volumetric god rays / light shafts
- **Industry method:** Principled Volume in a bounded cube + a Spot light
  (Blender Manual, Sun Beams / volumetrics practice: Volume Scatter with
  anisotropy 0.2–0.5 biases scattering along the beam; density in small
  increments; volume bounces 1–2).
- **Node setup (scene, not compositor):** Cube mesh, material = Volume
  Principled, Density 0.02, Anisotropy 0.5, Colour warm (1.0, 0.75, 0.45).
  Spot light, warm gold (1.0, 0.70, 0.32), energy 3000, angle 55°,
  blend 0.4, shadow on, aimed at the subject with a track quaternion.
  Compositor: Glare, Type = Sun Beams, source at the light's screen
  position, Strength 0.4, added back over the original.
- **World effect:** visible shafts in the air; the ground and the
  character inside a shaft get brighter; dust inside the shaft reads.
- **Shot-spec fields:** light_source, source_screen_x, source_screen_y,
  colour, density, anisotropy, ray_length, world_effect ("shaft pool on
  ground + character rim from shaft side").

### 2. Bloom / glow with light spill onto nearby surfaces
- **Industry method:** emission (Strength > 1) + compositor Glare, Fog
  Glow (Blender glow practice: Cycles has no native bloom, so Glare is
  the photoreal route; two stacked Glares — Streaks for star shape, Fog
  Glow for halo — is the standard candle/flame stack).
- **Node setup:** emissive object (Strength 8) + a real Point light at
  the same position (energy 800, same colour) so nearby surfaces actually
  brighten. Compositor: Glare Fog Glow, Threshold 0.8, Size 8,
  Strength 0.5, Mix ADD over original.
- **World effect:** the glow spills onto the ground and the character's
  near side; the spill colour follows the key hue family (rim rule).
- **Shot-spec fields:** glow_source, colour, strength, threshold, size,
  spill_radius, spill_targets (ground, character, wall).

### 3. Atmospheric scattering / haze / fog that shifts with the grade
- **Industry method:** World Volume (global haze) or a bounded
  Principled Volume cube (local mist); Noise Texture into Density for
  patchy fog; density 0.001–0.05 for god-ray work.
- **Node setup:** same volume cube as system 1, or a second low cube at
  ground level for ground mist. Grade shifts the fog colour: warm grade
  → fog colour warm; a JoJo shift recolours the fog with the shift, and
  the rim follows the SHIFTED key (per UNIVERSE-COLOR-LANGUAGE.md).
- **World effect:** distant silhouettes soften, depth reads, the whole
  shot's air takes the grade's colour.
- **Shot-spec fields:** fog_type (world/local/ground), density,
  colour, grade_link (lut name or shift name).

### 4. Particle systems: dust, sparks, embers, rain/snow with light interaction
- **Industry method:** Blender particle system, emit from volume,
  physics NO (for dust) or Newtonian + gravity (sparks/embers/rain),
  instance object = small emissive sphere; particles inside a volume
  catch the spot/point light.
- **Node setup:** emitter cube, 200 particles, lifetime 250, instance =
  icosphere radius 0.02, material = Emission (1.0, 0.8, 0.5), Strength 2.
  Rain/snow variant: same system, stretched instance, gravity on,
  ground collision off for a proof frame.
- **World effect:** the air gains texture; particles inside a shaft
  sparkle; embers rise and light the ground beneath them as they pass.
- **Shot-spec fields:** particle_type, count, size, colour, light_source,
  motion (drift/fall/rise), duration_frames.

### 5. Impact shockwave + ground dust + light flash that lights the scene for 2–3 frames
- **Industry method:** expanding ring (scaled torus/plane with a radial
  gradient, fading over 2–3 frames) + a dust burst (system 4, short
  lifetime, radial velocity) + a Point light flash keyed to frames 0–2
  at full energy, then 0.
- **Node setup:** flash light energy animated 1500 → 0 over 3 frames;
  dust burst count 120, lifetime 12; ring scale animated 0.2 → 3.0,
  opacity 1.0 → 0.
- **World effect:** for 2–3 frames the whole scene brightens and shadows
  pop, then settle; the ground shows a dust ring that lingers one beat.
- **Shot-spec fields:** impact_frame, flash_energy, flash_frames (2–3),
  ring_scale_start/end, dust_count, ground_mark (yes/no).

### 6. Fire / energy aura with flickering light cast on character and ground
- **Industry method:** emissive aura geometry (spheres at the fists in
  the proof) + a flickering Point light (energy driven by a noise
  curve, ±25% per frame) + Glare Fog Glow.
- **Node setup:** aura spheres, Emission (1.0, 0.70, 0.30), Strength 8;
  Point light, same colour, energy 800 with a noise driver; Glare Fog
  Glow Threshold 0.8.
- **World effect:** the character's near side and the ground pool pulse
  with the aura; the flicker reads as living energy, not a static halo.
- **Shot-spec fields:** aura_location (fists/whole body), colour,
  base_energy, flicker_range, flicker_rate_frames.

### 7. Water / reflection / wet-surface sheen
- **Industry method:** ground plane with low roughness + a reflection
  (planar reflection in Eevee, or a mirrored copy of the subject at low
  opacity for a 2D-proof frame); wet sheen = roughness map driven by a
  noise texture, lower roughness in puddle patches.
- **Node setup:** ground Principled, Roughness 0.15 in puddle mask,
  1.0 elsewhere; a flipped, darkened, blurred copy of the subject below
  the ground line at 0.35 opacity for the proof frame.
- **World effect:** the scene doubles downward; lights stretch into
  streaks on the wet ground; the atmosphere feels damp and reflective.
- **Shot-spec fields:** wet_area, roughness_puddle, reflection_opacity,
  reflection_blur, light_streak (yes/no).

### 8. Smoke / steam with shadow and rim interaction
- **Industry method:** smoke as a second volume (higher density,
  greyer colour, slower noise) that both blocks light (casts a soft
  shadow volume) and catches rim light on its lit edge.
- **Node setup:** smoke cube, Volume Principled, Density 0.05,
  Anisotropy 0.3, Colour (0.6, 0.6, 0.65); rim Spot from behind the
  smoke so its edge glows in the key hue family.
- **World effect:** the air thickens locally; the smoke's shadow side
  darkens the ground behind it; its lit edge glows.
- **Shot-spec fields:** smoke_source, density, colour, rim_source,
  drift_direction, duration_frames.

### 9. Motion blur + speed lines that follow the action arc
- **Industry method:** vector blur in the compositor (Vector Blur node,
  driven by the object's motion vectors) + speed lines drawn ALONG the
  limb's arc (sampled from the pose's joint path), never random.
- **Node setup:** Vector Blur, samples 32, speed factor 1.0, on the
  moving limb's layer; speed-line layer = arcs through the elbow/wrist
  key positions of the punch or swing, fading along the arc.
- **World effect:** the action reads fast without the character going
  soft; the lines tell the eye where the limb travelled.
- **Shot-spec fields:** moving_part, arc_key_positions, blur_samples,
  line_count, line_fade (head→tail).

### 10. Depth of field + lens effects (bokeh, anamorphic flare) tied to the shot's light source
- **Industry method:** camera Depth of Field (focus object = subject,
  F-stop 2.8 for a soft background) + Bokeh Blur / Glare Streaks for
  highlights, with the flare's streak axis aligned to the light source.
- **Node setup:** camera DOF focus = character plane, aperture f/2.8;
  compositor Defocus on the background layer; Glare Streaks, angle =
  angle from subject to light source.
- **World effect:** the subject separates from the background; bright
  background points bloom into bokeh; the flare points at the light.
- **Shot-spec fields:** focus_target, f_stop, bokeh_shape,
  flare_source, flare_angle.

### 11. Electricity / lightning with scene-wide flash + shadow pop
- **Industry method:** lightning bolt (jagged polyline, emissive,
  branched) + a scene-wide Point/Spot flash on the bolt's peak frame
  + a thunder-frame shadow pop (shadows harden for 1 frame as the flash
  peaks).
- **Node setup:** bolt Emission Strength 20, Glare Streaks; flash light
  energy animated 0 → 4000 (peak frame) → 0 over 4 frames; shadow
  soft size animated 0.8 → 0.1 → 0.8 with the flash.
- **World effect:** the whole scene strobes; every shadow sharpens for
  one frame; the air after the flash feels charged.
- **Shot-spec fields:** bolt_path, peak_frame, flash_energy,
  flash_frames, shadow_pop (yes/no).

### 12. Shadow casting from effects
- **Industry method:** every effect light casts shadows (Spot/Point
  use_shadow on, soft size set); every effect volume is in the shadow
  path, so an aura, a smoke puff, or a shockwave ring darkens what is
  behind it.
- **Node setup:** all effect lights: use_shadow True; shadow soft size
  0.5 (spot) / 0.8 (point); Eevee volumetric shadows on; ground plane
  receives shadows.
- **World effect:** effects stop floating on top of the scene — they
  sit IN it, because they darken and lighten real surfaces.
- **Shot-spec fields:** effect_name, casts_shadow (must be yes for a
  production effect), shadow_soft_size, shadow_target.

## Shot-spec template (new fields, added to color-shot-spec-template.json)

```json
{
  "effect_systems": ["volumetric_god_rays", "bloom_spill", "dust_particles"],
  "light_source": {"name": "warm gold key", "colour": [255, 180, 80], "position": "upper right behind"},
  "effect_colour": [255, 180, 80],
  "effect_intensity": 1.0,
  "effect_duration_frames": 24,
  "world_effect": "shaft pool on ground + dust sparkle inside shaft",
  "atmosphere_effect": "warm haze, distant silhouettes soften",
  "casts_shadow": true,
  "rim_follows": "key"
}
```

A spec that names an effect but names no light source, no world effect,
and no atmosphere effect is incomplete and must not render as final —
same gate as the colour spec.

## Proof frame (Blender 5.2.3, Eevee)

- **File:** `showcase/effects-v2-proof-20261031/effects-v2-proof-blender-20261031.png`
- **Script:** `showcase/effects-v2-proof-20261031/blender_effects_v2_proof.py`
- **Pose:** arms-up reference pose (FlexOut lowers, upper −70/70, lower
  150/−150), clean, labels=False, base art untouched — used as an
  emissive billboard card so the cutout reads exactly as drawn; all
  effects are separate scene layers (lights, volume, particles).
- **Systems in the frame:** (1) volumetric god rays — Spot + Principled
  Volume cube + Glare Sun Beams; (2) bloom/glow with spill — emissive
  aura spheres at the raised fists + Point light + Glare Fog Glow;
  (3) dust particles — 80 emissive instances inside the volume;
  (4) ground light pool + cast shadow — ground plane receiving the spot
  shadow and the aura pool. Warm grade via Bright/Contrast.
- **Status: VIEWED, PRODUCTION PIPELINE, PROOF-GRADE (not a final shot).**
  Rendered in Blender 5.2.3, Cycles CPU, 640×480, 32 samples, compositor
  CPU (Glare Fog Glow + Glare Sun Beams, Mix ADD). Viewed twice by the
  builder. V1 defects found in viewing and fixed for V2: (a) a newly
  created Material Output node is INACTIVE in Blender 5.2 — only the
  tree's original Output node is used, so every material that created
  a new Output rendered black (this was the black-frame bug, not the
  scene); (b) the billboard's grey-128 background showed as a card
  rectangle until texture Alpha was mixed through a Transparent BSDF;
  (c) aura orbs were oversized (radius 0.35) and have been shrunk to
  0.22 and moved onto the measured fist positions (±0.9, 1.3).
  Remaining proof defects, named not hidden: aura orbs still sit
  slightly high/wide of the fists (snap owed); visible Cycles noise at
  32 samples (denoise / higher samples owed for a final); the volume
  haze is uniform rather than shaft-shaped (shaft masking owed).
  The frame proves the systems work in the real pipeline; it is not
  claimed as a finished shot.

## Builds on (not a replacement)

- `INDUSTRY-VFX-PIPELINE.md` — internal line lighting as separate
  Screen/Add (light), edge-band bleed, and Multiply shadow layers over
  untouched base art. V2's effects sit in the same layer logic: effect
  layers on top, base art recoverable by turning them off.
- `COLOR-KEY-VFX-STACK-10.md` — the 10-piece stack order (colour key →
  character → hard shadow → rim → energy → glow → volumetric → fog →
  foreground → LUT → delivery). V2's 12 systems slot into that order;
  V2 does not reorder it.

## Still owed

- Per-shot effect specs: 0/30 (template above is done, filled specs are not).
- Effect systems with a viewed production frame: 4/12 in the V2 proof
  (god rays, bloom/spill, dust particles, ground pool + shadow); the
  other 8 (haze grade-link, impact flash, fire aura flicker, water,
  smoke, motion blur/speed lines, DOF/flare, lightning, effect shadows
  as a named pass) have node setups in this doc but no viewed frame yet.
- Aura orb-to-fist snap: orbs still slightly high/wide of the fists.
- Denoise / higher samples for a final-quality frame: 0/1.
- Shaft masking so the volume reads as shafts, not uniform haze: 0/1.
- Full-shot effect passes (impact flash 2–3 frames, lightning strobe,
  smoke, water, DOF/flare) as animated sequences: 0/5 sequences.
- GPU run (Kaggle/Colab free) for the volumetric sequence render: 0/1.
