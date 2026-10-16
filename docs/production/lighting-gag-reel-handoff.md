# Cape Jones Lighting-Gag Reel — Production Handoff

Status: implementation review in progress. The scene and first-pass Colab notebook are now present on `main`; this handoff does not claim a successful render.

## Verified project inputs

- Scene: `3d-assets/living_room.blend` (added by PR #23).
- Colab notebook: `production/colab/cape_jones_lighting_reel_colab.ipynb` (added by PR #23).
- Canonical LED preset implementation: `production/pipeline/led_controller.py` (15 named presets).
- Canonical color-grade library: `production/pipeline/grades.py` (32 grades; intended for the video pipeline).
- Pipeline overview: `docs/COMPLETE-PIPELINE.md`.

The blend file itself has not been opened or rendered in this environment, so the scene's node names, camera, light names, visual quality, and GPU render result remain unverified.

## Current notebook review

The existing notebook defines eight RGB looks for a 24-second reel (8 × 72 frames at 24 fps). They are a subset of the canonical LED controller's 15 presets. The notebook does not yet run the 32-grade pass, so it is a LED-lighting preview rather than full coverage of the planned lighting/grade library.

The current inline render script has several reliability risks to resolve before calling it production-ready:

- It assumes the scene contains a material named `LEDStripMat`, a Principled BSDF node, an `Emission Color` input, and an object named `RoomLight`; missing items cause a hard failure without a useful diagnostic.
- The last keyframe of each 72-frame segment is placed at `base + 72`, which is also the next segment's first frame. Keep keyframes inside their own segment (for example, use `SEG - 1` for the last offset) to avoid boundary collisions.
- It clears animation data on the emission input's owning node tree, which can remove unrelated animation on that material. Prefer to clear only the animation/action created for this render, or work on a temporary copy.
- The notebook's 8-item hard-coded list can drift from the canonical 15-preset names in `led_controller.py`. Treat that file as the source of truth and record any deliberately omitted presets.
- The render command pipes Blender output through `tail`; without `set -o pipefail`, the shell may report success even if Blender fails. Capture and check Blender's exit code before attempting to inspect/download the MP4.
- Confirm the actual scene loads in the selected Blender version and that the requested denoiser/device are available in the chosen Colab runtime.

These are static-review findings only; none has been confirmed by executing Blender against the scene. A separate proposed fix in PR #26 adds setup guards, isolated render datablocks, non-overlapping keyframes, reliable process status handling, and fail-fast output verification; it still needs a real Colab run.

## Source-of-truth and integration rules

- Keep the existing Blender scene, model, furniture, materials, and lighting implementation as the source of truth.
- Do not rename, move, re-export over, or modify shared scene assets as part of the reel setup.
- Keep outputs in a dedicated folder such as `renders/lighting-gag-reel/`; keep temporary files outside tracked source directories.
- Do not hard-code credentials, account details, local absolute paths, or machine-specific cache locations in reusable scripts.
- Keep the lighting comparisons on a locked camera and consistent resolution, frame rate, color management, and exposure unless a shot intentionally calls for a change.
- If Muse has an active branch, coordinate through a separate branch/PR and integrate against the latest `main`. Never force-push or overwrite concurrent scene work.

## Suggested reel structure

1. **Establishing shot** — baseline living-room scene.
2. **LED preset pass** — run the canonical 15 presets in a documented order, or clearly label the initial eight-look preview as a subset.
3. **Grade pass** — apply the 32 grades only through the intended grade pipeline, with a consistent source clip and documented grade names.
4. **Approved combinations** — include only combinations already approved in the production notes.
5. **Final comparison** — baseline, strongest approved looks, and a clean end card.

## Validation and merge checklist

- Run a small preview before full-quality rendering.
- Check for missing materials/nodes, incorrect light behavior, clipping, flicker, boundary pops, and missing textures.
- Verify output file existence, non-zero size, duration, frame rate, and that the render process actually exited successfully.
- Preserve a shot/preset manifest and render settings beside the review MP4.
- Do not commit large generated videos or caches unless the repository's media policy calls for it.
- Review the PR diff for binary outputs, secrets, and unrelated changes; check required GitHub status checks and mergeability before merging.
- A mergeable documentation PR does not prove the scene rendered or that the final video is complete.

## Remaining blockers

The real Blender render has not been executed or inspected here, and the original shot-by-shot gag notes have not been located. Next concrete step is to run the proposed notebook hardening from PR #26 on Colab, inspect a short preview against the checked-in scene, and verify the MP4 metadata before declaring the reel ready.
