# CAPE JONES — Blaster VFX Spec (canon-locked)

**Owner lock basis (verbatim sources):**
- PALETTE LOCKED (2026-10-17 ~10:24 CDT): current canon = the 10 uploaded model sheets; old repo sheet/bible colors are ALTERNATE colorways (logged, never used until he says so).
- Locked values: suit **#FFFFFF** (blown out, no gradients), cowl deep violet **#3E1473**, skin **#E5B28C**, cape absolute black **#000000**, cyan 2–4px rim light, **blaster core white #FFFFFF + outer glow #FFB300**.
- 2D-TO-3D TRANSLATION (2026-10-17 ~10:27 CDT): blaster = white core #FFFFFF + #FFB300 outer glow on additive; environment color ONLY on rim/glow, **never tint the white suit**; toon/cel shader (hard shadows, no gradients, suit blown out); cape = separate mesh + cloth sim; every key pose reads by silhouette alone; cyan rim light separates black cape from dark bg.
- Sheets: `characters/sheets/03-color-lighting-vfx-key.jpg` (gauntlet energy rules) + `04-action-flight-vfx-reference.jpg` (charge/blast/beam/burst/impact vocabulary). The owner is showing these sheets to the team for confirmation — this spec is built off them.

**Style filter (owner verbatim):** "We're a bit more comedic than Batman — we're a little bit more Space Ghost, Aqua Teen Hunger Force style." Every FX decision is comedy-first: exaggerated charge-up, hold the pose a beat too long, BANG, springy recoil. If it reads grim, it's wrong.

## 1. The sheet's blaster vocabulary (read straight off sheets 03 + 04)

| FX | What the sheet shows | Where it fires from |
|---|---|---|
| **GAUNTLET BLAST CHARGE** | Concentric energy rings around the forearm cuff, cyan/amber lightning arcs, fist cocked back, cuff glowing | Forearm gauntlet cuff |
| **IN FORCE / firing state** | Cuff ringed with glowing torus bands, spark arcs crawling | Forearm cuff |
| **ENERGY BEAM** | White-hot core, amber edge, **zigzag waveform leading edge**, straight beam body | Fist |
| **BURST** | Jagged starburst erupting from the fist | Fist |
| **IMPACT** | Radial starburst (yellow/white spikes) | Target / ground |
| **LIGHTNING ARCS** | Thin cyan arcs, jagged, between charge rings | Around gauntlet |

**Sheet rules (§3 of sheet 03, verbatim logic):**
- CORE BLAST: pure white #FFFFFF, Normal blend.
- OUTER GLOW: #FFB300, Color Dodge / Add.
- ENERGY & SPARKS **OVERLAP BLACK LINE ART** — the FX sits on top of the outlines, never under them.
- ENVIRONMENT COLOR BLEED: environment color goes strictly on the outer rim and energy glow — suit stays blown-out white.

## 2. Blaster types × colors (canon)

The brief (owner 2026-10-17 ~10:11): Mega Man-style charge/fire/recoil; multiple types + colors; blasters = lighting (the shot's color casts into the scene: rims/grade).

| Type | Canon color | Source | Cast-light color |
|---|---|---|---|
| **1. GAUNTLET BOLT** (default) | white core #FFFFFF / #FFB300 glow | sheet 03 §3 | #FFB300 amber |
| **2. ENERGY BEAM** (sustained) | white core / #FFB300 edge, zigzag lead | sheet 04 "ENERGY BEAM/BEAMS" | #FFB300 amber |
| **3. ARC CHAIN** (chain lightning) | cyan arcs (rim-light cyan family) | sheet 04 "lightning arcs" | cyan #22D3EE |
| **4. WAVE / PULSE** (radial shockwave) | white core / #FFB300 expanding ring | brief ("waves") | #FFB300 amber |

Colorway alternates (the alternate outfit colorways): when the wardrobe recolor system swaps the outfit, blaster colors stay sheet-canon UNLESS the owner asks — the FX is not part of the outfit. **Never invent new blaster colors** until he says so.

**Build as recolorable system** (WARDROBE CANON 10:27): blaster colors live in ONE place — the `CJ_BlasterPalette` node group / `blaster_palette.json` — so a colorway swap is a single edit, not a hunt.

## 3. Charge / fire / recoil state machine

Comedy timing is the whole gag. The charge builds until it's ridiculous, he keeps talking through it, then the BANG.

| State | Duration (24fps) | What happens | Comedy beat |
|---|---|---|---|
| **IDLE** | — | No FX. Cuff is just a cuff. | — |
| **CHARGE** | 24–36f | Rings spin up around cuff, arcs crawl, cuff glow ramps, point light ramps #FFB300, faint fist shake (last 8f) | Builds past the point it should. He keeps bullshitting. |
| **HOLD** | 12f | Full charge held, rings at max, arcs crackling | The beat where nothing happens. (The cape reacts a beat late — body-gag rule.) |
| **FIRE** | 3f snap | Burst starburst or beam snaps on; light flashes to full | BANG. No wind-up past the hold. |
| **RECOIL** | 12f | Fist kicks back with springy overshoot, glow decays, light falls off | Exaggerated, springy — cartoon recoil, not military. |
| **SETTLE** | 12f | Rings fade, arcs die, cuff back to white | Back to bullshitting. |

**Driver interface (3D):** a `CJ_BlasterDriver` empty in the shot file, custom props:
- `charge` 0.0–1.0 → drives ring visibility/scale, arc density, cuff-glow strength, charge light energy
- `fire` 0.0–1.0 → drives beam length / burst flash scale, fire light energy, rim takeover, grade shift
- `recoil` 0.0–1.0 → drives fist-bone kickback (animation lane), camera micro-shake

Animators keyframe these three props; everything else is driven. No hand-tweaking per shot.

## 4. Geometry-nodes build (`CJ_BlasterFX`)

Reference implementation: `3d-assets/blaster-vfx/build_blasterfx.py` (headless-buildable, tested). All procedural — no textures, no external assets.

**Group inputs:** `Charge`, `Fire`, `Seed`, `BeamLength`, `BlasterColor` (#FFB300), `ArcColor` (cyan), `CoreColor` (#FFFFFF).

**Charge rings:** 3 torus instances around the gauntlet axis; scale = `Charge × (1 + 0.15 × pulse(t))`; rotation driven by Scene Time — rings tighten as charge rises. Material: `CJ_FX_Glow`.

**Beam:** two coaxial cylinders along fist-forward (+Y of the blaster bone): white inner core (radius × 0.6, `CJ_FX_Core`) + amber outer shell (radius × 1.0, `CJ_FX_Glow`, slightly transparent); length = `Fire × BeamLength`; leading edge: displaced end ring (zigzag via noise on the end cap ring vertices).

**Burst flash:** icosphere with vertex-noise displacement, flat-ish scale along axis; scale = Fire envelope × seed-varied; white core material; sits OVER the fist geometry.

**Sparks:** points scattered in a sphere at the muzzle, instance small icosahedrons (`CJ_FX_Glow`); per-point random offset from Seed; visible ∝ Fire.

**Lightning arcs:** jagged poly-lines (resampled curve + noise offset) between the cuff rings, cyan emission, count ∝ Charge.

**Materials:**
- `CJ_FX_Core` — Emission #FFFFFF, strength 20 (Normal).
- `CJ_FX_Glow` — Emission #FFB300, strength 12 (drives compositor bloom → reads as Color Dodge/Add).
- `CJ_FX_Arc` — Emission cyan, strength 10.

**Compositing:** FX render layer gets Glare (Fog Glow) in the compositor — that's the additive #FFB300 bloom. Core stays white-hot. **White suit never graded** — color goes on rim/glow only.

**Attachment:** `blaster_*` bones on the rig (parented to `hand_*`, per RIG-DOCS.md). The FX object parents to the blaster bone (Bone parent or Child Of). **The rig .blend itself is NOT edited by this lane** — this is a separate `3d-assets/blaster-vfx/blaster_fx.blend` that animators link in. (Rig lane owns the rig file; anti-clobber law.)

**Cast light:** Point light parented to the blaster bone, color = BlasterColor, energy driven by `charge`/`fire` props (charge ramp → fire flash → decay). In the living-room scene this is the mechanism behind "red blaster throws red light" — the light's color is the blaster's color.

**BLASTER LIGHTING CONCEPT (owner 2026-10-17 ~10:36 CDT) — the show's signature visual device:**
The blast's light BECOMES the scene lighting while firing — it creates the rim light on him, throws color into the environment, and drives the shot's color grade. Reference: how Chowder made patterned textures its signature — this show makes dynamic colored lighting its signature. (Docs lane is logging this in the lighting docs + show bible — this spec applies it, doesn't duplicate.)

Concretely, per firing shot (3D — real lights; 2D — composited the same way):
1. **FIRE flash:** blaster light energy spikes (charge×200 + fire×1500 in the proof rig); it becomes the dominant scene light.
2. **Rim takeover:** the rim rig switches to the blaster's color during fire — rim light color/energy driven by the `fire` prop (environment rim dims to a floor value, blast-color rim ramps up). Consistent with the 10:35 rim refinement: the blaster is the environment's dominant light source during the shot, so the motivated rim IS the blaster color.
3. **Spill:** a spill light (or the blaster light's radius) throws the blaster color onto nearby set/characters.
4. **Grade shift:** compositor/grade nudges toward the blaster color for the fire frames (2D: LED-controller-style grade preset per blaster color).
5. **Lighting personality per type:** GAUNTLET BOLT / ENERGY BEAM / WAVE = amber personality (warm, aggressive bloom); ARC CHAIN = cyan personality (cold, electric). When the type changes, the whole scene's color personality changes with it.

Outside firing (charge/idle), the rim returns to the environment-motivated state (space cyan, LED color, etc.). The `fire` prop is the crossfade control — animators key it, the rig does the rest.

**RIM LIGHT REFINEMENT (owner 2026-10-17 ~10:35 CDT) — situational, motivated, real lights in 3D:**
- The rim is NEVER a generic always-cyan overlay in 3D. It is a real light rig, keyed to the environment's actual light sources.
- Space / dark void → cyan-blue rim (matches sheet 03's 2–4px cyan rim on dark bg).
- LED scenes (living room, the Club) → rim takes the **LED strip color** (driven by the same LED-controller state as the scene).
- Any other environment → rim is keyed to that scene's real key/fill sources.
- The black cape #000000 must stay readable in dark settings through this motivated rim — never blown out, never unmotivated. The 2D compositor reference (cyan 2–4px rim) is the 2D translation; in 3D the light rig does the work.
- The blaster's cast light is SEPARATE from the rim rig — two different systems, never one generic "glow light".

**2D→3D rules applied to this FX (docs lane owns the full translation doc — this spec applies them, doesn't duplicate):**
- Toon/cel shading, hard vector shadows, no gradients / no soft AO on the character — the FX is emission, not shaded geometry.
- Blaster glow renders ADDITIVE (compositor Glare on the FX layer), **overlapping the black line art** per sheet 03.
- Environment tint NEVER touches the white suit — color lives on rim + FX glow only.
- POSING RULE: charge/fire/recoil silhouettes must read instantly — rings and beam form clean outer shapes, no fiddly internal detail.

**Detachable fist (rig-owned, FX notes here):** when the fist detaches (Android 16 canon), the socket shows a white-hot ring (`CJ_FX_Core` material on the socket mesh) and the detached fist trails a short beam + arcs. Rig lane implements the mechanism; this spec defines the look.

## 5. 2D pipeline counterpart

Same visual language for the 2D/FlipaClip post pipeline: export white-core/#FFB300-glow PNG sprites (transparent, additive) from `blaster_fx.blend` orthographic renders; composite with Screen/Add over the 2D frames. Energy overlaps line art. The 2D sheet is the authority on the shapes — match them, don't reimagine them.

## 6. Scout pull-ins (open-source beams / geo-nodes setups / free VFX packs)

As of this write, **no scout blaster pull-ins have landed in the repo** (checked `docs/`, `production/`, `tools/` — nothing VFX landed yet). When they land, this lane will:
1. Research each pull-in's actual interface (check-research-wire-do).
2. Wire the compatible pieces into `blaster_fx.blend` (e.g. a better zigzag-displacement technique, a spark system) WITHOUT changing the sheet-canon look.
3. Never duplicate the scout's pulls — if they've landed a beam system, I use theirs; I don't rebuild it.

The current build is native/procedural precisely so it doesn't collide with incoming scout systems.

## 7. License / steal-like-an-artist

This spec and the GN build are original/procedural — no third-party assets. The technique lineage (Mega Man charge timing, Android 16 detachable fist, Space Ghost energy-bolt look) is study reference only; the character, FX language, and implementation are original to this show. Any scout-pulled systems get their licenses logged honestly in the spec when they land.

## 8. Visual proof

`3d-assets/blaster-vfx/proof/` — test renders of the FX on a dummy fist against a dark background: charge state, fire state, beam. The owner signs off with his own eyes.
