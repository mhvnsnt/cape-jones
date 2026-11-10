# extra-lights — Extra Lights (free, GPL), wired

**What:** Extra Lights v1.3.0 by Jonathan Lampel (CG Cookie) — 21+ photometric
light presets in the Add menu, all built from real-world fixture data:
- **21 `bpy.ops.light.add_*` presets** organized Natural / Incandescent / LED /
  Fluorescent (halogen under incandescent, metal-halide/HID under fluorescent).
- **Lumens-based strength**: converts lumens → radiant watts for you (Blender
  lights are calculated in emitted watts, not the bulb's electrical watts — the
  add-on does the spectral conversion so you don't have to).
- **Kelvin color temperatures** per real source (candle 1800K, incandescent
  ~2700K, fluorescent 3000–4000K, daylight ~5000–6500K).
- **IES profiles** for point/spot lights (real bulb throw patterns; Cycles only —
  Eevee doesn't support light nodes), plus softbox modifiers on area lights.

**Why for us:** physical lighting for the living room without guessing. The
lamps, hallway light, and LED strips should be Extra Lights presets (lumens +
Kelvin) instead of hand-tuned energies — that is the industry approach: start
from real-world values, break the rules intentionally. Blends with Light It Up
(the other lane's studio rigs): LIU for look-dev moods, Extra Lights for the
canon physical fixtures.

**Verified 2026-10-17 by this lane (real run, Blender 4.5.3 LTS):**
- Clone `jlampel/extra-lights` @ `bb75dac` (v1.3.0, `blender_version_min=4.2.0`),
  vendored to `tools/pulled/extra-lights/` (.git stripped, license kept).
- SPDX: GPL-3.0 (`license.txt`; IES profiles derived from leomoon's GPL IES
  Lights Pack, also GPL).
- Installed headless via `bpy.ops.extensions.package_install_files`
  (repo=`user_default`), registered by path — `extra_lights.register()` OK.
- Functional: `bpy.ops.light.add_1000a19()` created a POINT light, energy
  1000.0 — 21 `light.add_*` ops live.

**Install:**
```bash
# GUI: Blender 4.2+ -> Edit -> Preferences -> Add-ons -> Install from Disk ->
#        tools/pulled/extra-lights/ -> enable "Lighting: Extra Lights"
# Headless (agents):
BLENDER=<blender-4.5.x> xvfb-run -a env -u PYTHONPATH \
  $BLENDER -b --python tools/extra-lights/install_extra_lights.py
```

**Location in scene:** 3D Viewport > Add > Light > Natural / Incandescent /
LED / Fluorescent.
