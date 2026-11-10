# lighting — Light It Up (free edition), wired

**What:** *Light It Up* 4.0.0 — free, open-source (GPL-3.0-or-later) studio
lighting presets for Blender. 17 presets (Portrait/Cinematic/Environment/Product:
Rembrandt, Loop, Split, Butterfly, Short, Broad…), each builds an editable rig of
ordinary Blender lights parented to an empty — nothing baked, nothing hidden.
Four live master controls: intensity, colour temperature (6500 K neutral),
key/fill ratio, orbit. `Fit To Subject` rescales a rig to the selected object.

**Why for us:** look-dev for the living room — try lighting moods in one click,
then bake the winner into the scene. Rigs are native Blender data, so a `.blend`
lit with this renders on the Kaggle/Colab lanes with no add-on installed.

**Verified 2026-10-17 by this lane (real run):**
- Extension id `light_it_up` v4.0.0 on extensions.blender.org; archive
  `add-on-light-it-up-v4.0.0.zip` (128,122 bytes) — **sha256 matches the
  platform's published hash** `773e46ef…9900f9`.
- Installed headless on **Blender 4.5.12 LTS** via `bpy.ops.extensions.package_install_files`
  (repo=`user_default`).
- Applied the **Butterfly** preset headless: 1 default point light + rig of
  2 AREA lights (key 370.4, fill 246.9) inside collection `LIU_Butterfly`.
- License: SPDX `GPL-3.0-or-later` (from the platform metadata).

**Don't confuse with:** *Light It Up Pro* ($49, 37–39 presets) — we use the FREE
edition only. Owner law: no spending.

## Install

GUI (recommended): Blender 4.2+ → Edit → Preferences → Get Extensions →
search "Light It Up" → Install. Tested by the author on 4.2 LTS / 4.5 LTS / 5.1 / 5.2.

Headless (agents) — see `install_light_it_up.py`:
```bash
xvfb-run -a <blender-4.5.12> -b --python tools/lighting/install_light_it_up.py
```
Quirk found: under `-b` the extension doesn't auto-enable; the script registers
it by path (`sys.path` + `register()`), which works.

## Use (headless example)

```python
import sys; sys.path.insert(0, LIU_EXT_DIR)   # .../extensions/user_default
import light_it_up; light_it_up.register()
bpy.ops.light_it_up.butterfly()   # or .rembrandt, .loop, .split, .clamshell, ...
```

Rigs layer into their own collections (`LIU_<Preset>`); delete the collection to
remove a rig without touching scene lights. Save your own presets from scene
lights — they persist outside the add-on folder across updates.
