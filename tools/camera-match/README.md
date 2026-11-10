# camera-match — fSpy camera matching, wired

**What:** fSpy (open source, GPL) — still-image camera matching. You mark
vanishing-point lines on a photo/drawing; it solves the camera (position,
rotation, focal length, principal point). The **fSpy-Blender importer** add-on
creates a Blender camera with the solved parameters + the image as background.

**Why for us:** the owner's 2D living-room reference drawing
(`~/workspace/user/files/1000174416_0_yip0.png`) is the layout ground truth.
fSpy lets us solve a Blender camera that matches the drawing's perspective —
then we can overlay our 3D room on his drawing and check alignment by eye,
instead of eyeballing camera angles.

**Verified 2026-10-17 by this lane (real run, Blender 4.0.2):**
- Importer: community fork `jmossymoss/fspy-blender-4.5` (tracks the official
  `stuffmatic/fSpy-Blender` 1.0.3). **License: GPL-3.0.**
- Installed headless from zip: `ADDON STATE: True`, `import_scene.fspy` op registered.
- Imported a synthetic `.fspy` project (magic `2037412710`, v1): created camera
  `fspy_test.fspy` with **lens_unit=FOV, angle exactly 1.2 rad** (as authored),
  **location exactly (0, 0, 2.5)** (from the transform matrix), render resolution
  set to the project image dims, background image attached.

## Workflow

1. Open the reference drawing in fSpy (desktop app, fspy.io — or the maintained
   fork `EnneiteG/fSpy-Reframe`, which adds a Blender XYZ-Euler preset).
2. Set the two vanishing points + horizon, set the reference distance / origin.
3. Save the `.fspy` project.
4. In Blender: File → Import → fSpy (or headless):
   ```python
   bpy.ops.preferences.addon_install(filepath='/path/to/fspy_blender.zip')
   bpy.ops.preferences.addon_enable(module='fspy_blender')
   bpy.ops.fspy_blender.import_project(filepath='/path/to/ref.fspy')
   ```
5. Point the solved camera at the scene, render, overlay on the drawing —
   alignment errors become visible immediately.

## Notes

- fSpy solves from **vanishing points**, so it works on drawings/paintings, not
  just photos — perfect for his hand-drawn reference.
- The importer's `set_up_3d_area` touches the 3D view; headless it only needs the
  camera + background image, which work fine under `-b`.
- Principal point in the project file is in **pixels**, not normalized — the
  importer divides by image dims itself.
