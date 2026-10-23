# light-editor — Light Editor (free, GPL), wired

**What:** Light Editor v2.4.6 by Robert Rioux ("Blender Bob", ex-CG-Supervisor at
Real by Fake VFX studio) — a spreadsheet-style panel for managing every light in
a scene: toggle on/off, isolate, filter by name/type, group lights, manage light
linking collections. The living room is accumulating lights (RoomLight, Sun,
HallLight, LED strips, lamp lights, TV glow) — this is how you keep them sane.

**Why for us:** the studio tool for light management, GPL free. The lighting
lane (`scene/lighting-volumetrics-20261017`) should use this to audition the
canon lights, isolate the LED rig from the sun fill, and toggle groups while
blocking out the scene.

**Verified 2026-10-17 by this lane (real run, Blender 4.5.3 LTS):**
- Clone `riouxr/Light-Editor` @ `a4a08e9` (v2.4.6), vendored to
  `tools/pulled/Light-Editor/` (.git stripped, license kept).
- SPDX: GPL-3.0 (`LICENSE`).
- Installed headless via `bpy.ops.extensions.package_install_files`
  (repo=`user_default`), registered by path — `LightEditor.register()` OK.
- Operators live: `light_editor.toggle_group`, `toggle_collection`,
  `isolate_group_emissive`, `toggle_kind`, `toggle_group_exclusive`.

**Install:**
```bash
# GUI: Blender 4.2+ -> Edit -> Preferences -> Add-ons -> Install from Disk ->
#        tools/pulled/Light-Editor/ -> enable "Object: Light Editor"
# Headless (agents):
BLENDER=<blender-4.5.x> xvfb-run -a env -u PYTHONPATH \
  $BLENDER -b --python tools/light-editor/install_light_editor.py
```

**Location in scene:** 3D Viewport > N-panel > Light Editor.
