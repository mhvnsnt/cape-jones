# SCENE-FULLSTACK — Living Room Full-Stack Research + Pull-ins

**Lane:** `scene/fullstack-research-20261017` | **Date:** 2026-10-17
**Owner directive:** "As good as possible, pulling in as much as possible, wiring up as much as possible — full stack, industry standard, production grade, fully wired, all agents using them."
**Blender pin:** 4.5.x LTS (verified on 4.5.3 LTS, real headless runs).

Everything below was checked against primary sources on 2026-10-17, not guessed
from training data. Confidence tags: `verified` (checked myself, 2+ sources),
`single-source` (one real run), `inferred` (reasoning, marked as such).

---

## 1. What was already in the repo (do NOT duplicate — point lanes at these)

| Tool | Path | What it covers | Verdict |
|---|---|---|---|
| Light It Up (free ed., GPL-3.0-or-later) | `tools/lighting/` | 17 studio lighting presets; rigs are native lights in `LIU_*` collections, render on Colab with no add-on | Use for look-dev moods |
| procedural-pbr (MIT) | `tools/textures-proc/` | Seamless PBR sets via numpy/PIL, zero GPU | Rug/fabric tiling variants if needed |
| Material Maker (MIT) | `tools/textures-proc/` (documented) | Free Substance Designer; exports PBR PNG sets | The texture-authoring path |
| Poly Haven + ambientCG (CC0) | `tools/hdri-textures/` | HDRIs, PBR textures, license-verified 2026-10-17 | The HDRI source (fetch script upgraded this lane) |
| GScatter (free, GPL) | `tools/scatter/` | Geometry-nodes scattering (rug fibers, shelf clutter) | Natural detail, no hand-placing |
| fSpy + importer (GPL) | `tools/camera-match/` | Solve the canon camera from the owner's 2D drawing | The camera-match path |
| layout-rules (in-house) | `tools/layout-rules/` | `living_room_layout.json` contract + validator | The ONLY thing a human edits for placement |
| OIDN / OptiX denoise (built-in) | `tools/upscale-denoise/` | GPU OIDN on 4.5 LTS | The denoise path for all scene renders |
| cycles_speed_config.py (in-house) | `production/pipeline/` | 16spp/adaptive-0.05/GPU-OIDN presets (measured 2-3x) | The base — extended, not duplicated |
| blender-mcp (MIT) | `tools/blender-mcp/` | Agent eyes+hands: scene info, screenshots, bpy exec | The agent iteration loop |
| LED 2D pipeline (in-house) | `production/pipeline/led_controller.py` | ffmpeg color grading for 2D LED gag scenes | 2D only — the 3D half is new this lane |

---

## 2. Evaluated — won and pulled (licenses verified from the source)

### 2a. Light Editor v2.4.6 — Robert Rioux (riouxr/Light-Editor) — GPL-3.0 — PULLED
Spreadsheet UI for every light in the scene: toggle/isolate/filter by name and
type, group lights, manage light linking. Rioux was CG Supervisor at VFX studio
Real by Fake — this is the studio tool.
**Why it won:** the room's light count is growing (RoomLight, Sun, HallLight,
LED strips, lamp lights, TV glow, shaft spots). Auditioning lights one panel at
a time doesn't scale.
**Verified:** cloned @ `a4a08e9`, installed headless via
`bpy.ops.extensions.package_install_files` on Blender 4.5.3 LTS,
`LightEditor.register()` clean, operators `toggle_group`/`toggle_collection`/
`toggle_kind`/`isolate_group_emissive` live.
**Landed:** `tools/pulled/Light-Editor/` + `tools/light-editor/` (README +
`install_light_editor.py`).

### 2b. Render Manager v3.0.11 — Robert Rioux (riouxr/Render-Manager) — GPL-3.0 — PULLED
Render-layer + render-pass management the VFX-house way: create/reorder layers,
per-layer collection/pass control, copy/paste pass sets, export per-layer
16-bit color + 32-bit data passes (incl. Cryptomatte) + precomp, Z-up→Y-up.
**Why it won:** the room is heading for compositing (god-ray glare pass,
TV-screen pass, LED glow pass, Cryptomatte on the remote/buttons). Hand-rolled
File Output nodes are the amateur version of this.
**Verified:** cloned @ `e827295`, headless install + `render_manager.register()`
clean on Blender 4.5.3 LTS.
**Landed:** `tools/pulled/Render-Manager/` + `tools/render-manager/`.

### 2c. Extra Lights v1.3.0 — Jonathan Lampel / CG Cookie (jlampel/extra-lights) — GPL-3.0 — PULLED
21 photometric light presets in the Add menu (Natural/Incandescent/LED/
Fluorescent): lumens→watts conversion, Kelvin temperatures from real sources,
IES profiles (Cycles) for real bulb throw patterns, softbox modifiers.
**Why it won:** physical lighting without guessing. Lamps, hallway, LED
practicals should be lumens+Kelvin presets, not hand-tuned energies. Industry
rule: start from real-world values, break them intentionally.
**Verified:** cloned @ `bb75dac` (manifest `blender_version_min=4.2.0`),
headless install + register clean; functional —
`bpy.ops.light.add_1000a19()` built a POINT light, energy 1000.0; 21
`light.add_*` ops live.
**Landed:** `tools/pulled/extra-lights/` + `tools/extra-lights/`.

### 2d. fetch_polyhaven_hdri.py upgrade (in-house, CC0 pipeline) — WIRED
Now resolves the free Poly Haven API (`api.polyhaven.com/files/{slug}`, no key)
for the authoritative URL + published md5/size, asserts bytes, skips on md5
match. `--indoor` pulls the curated set: `studio_small_03`, `studio_small_09`,
`leburb`, `brown_photostudio_02` (window-daylight candidates).
**Verified:** `studio_small_03_1k.hdr` (1.7 MB), md5 matched the API record;
old positional CLI, `--indoor`, and md5-skip all exercised.

### 2e. godray_kit.py (in-house) — WIRED — `tools/volumetrics/`
Two-mode god-ray system: `build_fake_shaft()` (emission→Volume cone: fresnel
edge fade × length fade × frame-driven noise breakup + a real Spot light doing
the illumination, one `shaft_strength` master prop) and
`build_true_volume_box()` (Principled Volume, driver-driven `fog_density`).
Presets: `window_shafts()` tuned to the canon window (right wall x=3.5, opening
1.4×1.1 @ z=1.6), `lamp_haze()`.
**Verified:** fake + true builds asserted (drivers, Track To, no-shadow
flags), 32px Cycles render compiled both volume shaders, PNG written.
Quirk documented: after `nodes.clear()`, `Noise.inputs["W"]` name lookup can
KeyError — kit sets `noise_dimensions` explicitly + index fallback.

### 2f. crt_tv.py (in-house) — WIRED — `tools/crt-tv/`
Procedural CRT look stack as node group `CJ_CRT_Screen`: content (image/movie)
→ 240-line scanlines → aperture-grille RGB stripes → rolling refresh band →
flicker → vignette → Emission. Driver-ready inputs: `crt_power`,
`crt_brightness`, `crt_flicker`, `crt_refresh`, `scanline_count`.
**Verified:** group builds with all inputs + Shader output, assigns to a mesh,
32px Cycles render compiles.

### 2g. led3d.py (in-house) — WIRED — `tools/led-3d/`
The 3D half of the LED gag. Scene master props `LED_color` (`#731AE5` canon
default) + `LED_brightness`; `wire_strip_material("LEDStripMat")` /
`wire_light("RoomLight")` add drivers non-destructively; `apply_preset()` and
`gag_press_sequence()` keyframe the remote-gag animations.
**Verified:** drivers proved via depsgraph evaluation (color → (1,0,0),
energy → 150.0 at brightness 0.5); rainbow-cycle keyed 25 color keys.

### 2h. scene_cycles_config.py (in-house) — WIRED — `tools/scene-render/`
Interior presets extending `cycles_speed_config.py` (not duplicating):
`living_room` (diffuse 4 / volume 2 / step_rate 2.0 / max_steps 256 / volume
guiding on; inherits 16spp + adaptive 0.05 + GPU OIDN), `living_room_preview`
(~4x faster), `living_room_hero` (close-ups).
**Verified:** all three presets apply cleanly on Blender 4.5.3 LTS.
**Bug note for the pipeline lane:** the base script sets
`c.scrambling_distance = 'AUTOMATIC'`, but on 4.5.3 LTS that property is a
**float** → TypeError. This preset catches it and sets 1.0. Base file left
untouched (pipeline lane owns it).

---

## 3. Industry-standard approaches (steal-like-an-artist: study, write our own)

### Volumetric lighting / god rays
- **Film/VFX (the standard):** hero "god rays" are almost always fake —
  geometry cones/planes with fresnel-faded emission, paired with a real light
  doing the illumination. True volumes only where fog must catch shadows.
  (This is the Light Volume vs Real Fog split the $19 Volume Forge add-on
  productized — reimplemented here as our own code.)
- **Games (UE5):** global height fog + local light-shaft cards; cinematics
  still composite 2D shaft cards for control.
- **Our adaptation:** `tools/volumetrics/godray_kit.py` — fake shafts default,
  one true-volume box max per room.

### Interactive TV screens
- **Film/VFX:** on-set screens are emission planes fed by video playback; the
  "CRT" is a look stack (scanlines, phosphor mask, refresh band, flicker) —
  never a simulation. Playback = image sequence / movie texture.
- **Real-time/VP (Unreal LED walls):** emissive screen + media texture;
  interactivity = material parameters driven by logic.
- **Our adaptation:** `tools/crt-tv/crt_tv.py` — content socket + five
  driver-ready inputs the gag lane keyframes. Renders identically everywhere.

### Animated furniture (recliner mechanism)
- **Studios (Pixar/Blender Studio method):** prop mechanisms are armature +
  drivers + custom properties — one `recline` property drives footrest,
  backrest, cushion squash via drivers; never keyframed per-part. No add-on
  exists because it's 20 lines of rigging.
- **Our adaptation:** documented for the `scene/recliner-mechanism-20261017`
  lane (their branch, their build).

### Physical + studio lighting
- **Studios:** start physical (lumens/Kelvin/IES), art-direct from there;
  manage via spreadsheet/isolate tools; look-dev with preset rigs, bake the
  winner into native lights.
- **Our adaptation:** Extra Lights (physical fixtures) + Light It Up
  (look-dev moods, already in repo) + Light Editor (manage/isolate).

### Render optimization for Colab/Kaggle T4
- Repo findings stand: 16spp + adaptive 0.05 + GPU OIDN (2-3x, temporally
  stable vs OptiX). Interiors add: diffuse 4 (bounced LED wash), volume
  bounces 2, step_rate 2.0, volume guiding on. Compositor Sun Beams node is
  the cheap 2D god-ray fallback if volumetrics ever blow the budget.

---

## 4. Evaluated — documented, NOT pulled (and why)

| Candidate | License / Cost | Verdict |
|---|---|---|
| Physical Starlight and Atmosphere (Upitis) | $70 paid, GPL | Not pulled — no spending. Free substitute: built-in Sky Texture (Nishita) for the exterior |
| Volume Forge (Depth Optica) | $19 paid, GPL | Not pulled — no spending. Technique reimplemented as `godray_kit.py` |
| CRT Monitor Generator / Phosphor (Superhive) | paid | Not pulled. Look stack reimplemented as `crt_tv.py` |
| Light It Up Pro ($49) volumetrics | paid | Not pulled. Free ed. already wired; volumetrics via `godray_kit.py` |
| Gaffer (Blender light manager) | paid (trial w/ watermark) | Not pulled — Rioux Light Editor covers it, free |
| Turbo Tools / Render+ | paid | Not pulled — measured presets + `scene_cycles_config.py` cover it |
| Extra Lights paid preset pack | paid | Not pulled — free GitHub 21 presets suffice |

---

## 5. Lane guide — what each scene lane should use

**`scene/lighting-volumetrics-20261017` (lighting + god rays):**
1. Look-dev moods with Light It Up (`tools/lighting/`) — bake the winner into
   native lights (rigs live in `LIU_*` collections, canon-safe).
2. Replace hand-tuned lamp/hallway lights with Extra Lights presets
   (`tools/extra-lights/`) — lumens + Kelvin (e.g. 2700K incandescent for the
   table lamp). Wire LED strips via `tools/led-3d/led3d.py`
   (`wire_strip_material("LEDStripMat")`, `wire_light("RoomLight")`).
3. God rays: `tools/volumetrics/godray_kit.py` — `window_shafts()` for window
   beams (fake = fast), `lamp_haze()` for floor-lamp glow. Manage the light
   list with Light Editor (`tools/light-editor/`).
4. False Color view transform (built into Blender) for exposure checks.

**`scene/tv-functional-20261017` (TV screen):**
1. `tools/crt-tv/crt_tv.py` — `apply_to_screen("crt_screen")` on the canon
   blend, `set_content()` with the static/episode clip. Keyframe
   `crt_flicker`/`crt_power` on the group node for the gag.
2. Export the screen as its own render layer with Render Manager
   (`tools/render-manager/`) for independent bloom in comp.

**`scene/recliner-mechanism-20261017` (recliner):**
- Armature + drivers + one `recline` custom prop (§3). No add-on needed. Parent
  the sit-target empties to the seat bone once built.

**`scene/sit-targets-20261017` (sitting):**
- Nothing new to pull; keep the measured layout contract
  (`tools/layout-rules/`). Parent sit targets to the recliner rig when it lands.

**Render lane (Colab/Kaggle):**
- `tools/scene-render/scene_cycles_config.py` — `living_room` preset via
  `--python ... -- living_room` before rendering. Headless install scripts in
  each `tools/<tool>/install_*.py` put the add-ons on render boxes sans GUI.

**All lanes:** `tools/blender-mcp/` for the screenshot→tweak loop;
`tools/pulled/README.md` for the vendored-source catalog.

---

## 6. Pull log (RESEARCH-TO-REPO LAW)

| # | What | Where from | License | Where it landed |
|---|---|---|---|---|
| 1 | Light Editor v2.4.6 | `github.com/riouxr/Light-Editor` @ `a4a08e9` | GPL-3.0 | `tools/pulled/Light-Editor/` + `tools/light-editor/` |
| 2 | Render Manager v3.0.11 | `github.com/riouxr/Render-Manager` @ `e827295` | GPL-3.0 | `tools/pulled/Render-Manager/` + `tools/render-manager/` |
| 3 | Extra Lights v1.3.0 | `github.com/jlampel/extra-lights` @ `bb75dac` | GPL-3.0 | `tools/pulled/extra-lights/` + `tools/extra-lights/` |
| 4 | godray_kit.py | in-house (technique studied from Volume Forge / film practice) | in-house | `tools/volumetrics/` |
| 5 | crt_tv.py | in-house (technique studied from CRT add-ons / film practice) | in-house | `tools/crt-tv/` |
| 6 | led3d.py | in-house (studio master-control pattern) | in-house | `tools/led-3d/` |
| 7 | scene_cycles_config.py | in-house (extends `production/pipeline/cycles_speed_config.py`) | in-house | `tools/scene-render/` |
| 8 | fetch_polyhaven_hdri.py upgrade | in-house (Poly Haven free API; assets CC0) | CC0 assets | `tools/hdri-textures/` |

All licenses commercial-use OK. Code only — no weights/models. Nothing paid was
pulled (owner law: no spending).
