# fSpy-Blender — still-image camera matching into Blender (wiring doc)

**Upstream:** https://github.com/stuffmatic/fSpy-Blender (v1.0.3, GPL-3.0)
**Companion app:** https://github.com/stuffmatic/fSpy (fspy.io) — the camera-matching
app itself (TypeScript/Electron, GPL-3.0). NOT vendored here: it needs
node_modules to build; fetch from fspy.io or build from source when needed.
Only the Blender importer add-on is vendored (pure Python, zero deps).
**License:** GPL-3.0 — free, commercial use allowed (copyleft on derivative
distribution of the add-on itself).
**Why:** matchmove for the show — take a still photo (a room, a street, a set
reference), solve the real camera's focal length/position/orientation from
vanishing points in fSpy, import the solved camera into Blender, and build/set
dress directly against the photo. This is how environments get built to match
real plates without eyeballing perspective.

## Install

```bash
python3 production/tools/fspy-blender/install_fspy_blender.py --help
python3 production/tools/fspy-blender/install_fspy_blender.py \
    --blender ~/workspace/tools/blender/blender-4.0.2-linux-x64
```

The installer zips `fspy_blender/` and drops it into the Blender addons dir,
then prints the enable step. Or manually: Blender → Edit → Preferences →
Add-ons → Install from file → select the built zip → enable "Import-Export:
fSpy importer".

## Use

1. In fSpy (the app): open a photo, set 2 vanishing-point axes from parallel
   lines in the image, fSpy solves the camera.
2. Save the `.fspy` project.
3. In Blender: File → Import → fSpy (.fspy). The add-on creates a camera with
   the solved focal length, sensor fit, and transform, and loads the photo as
   the camera background image.
4. Model the set/environment aligned to the background plate.

The parser (`fspy_blender/fspy.py`) is also importable standalone — the test
suite (`test/test.py`, `run_tests.sh`) validates `.fspy` project loading
without Blender.

## Verified (2026-10-19)

- `python3 -m py_compile` clean on all addon modules.
- Test suite present upstream; parser-only path has no Blender dependency.

## Cape Jones uses

- **Set building:** photograph the living-room reference, solve the camera,
  model the TV/shelf/chair layout to match — no more eyeballed perspective.
- **Set extension:** extend photographed locations with 3D geometry that
  perspective-matches the plate.
- **Previz:** quick camera solves from location photos before full scene builds.

## Limits

- Still images only — no video tracking (that's a different tool class).
- Works on perspective photos from near-distortion-free lenses; fisheye,
  panoramas, and perspective-corrected images will not solve well.
- The fSpy app itself is Electron — runs on a desktop, not headless. Solve on
  a machine with a display, import the `.fspy` anywhere.
