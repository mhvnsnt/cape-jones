# Cape Jones Lighting-Gag Reel — Production Handoff

Status: coordination/specification only. No scene files were changed and no render is claimed by this document.

## Goal

Produce a short review reel using the existing Cape Jones living-room scene, character model, furniture, lighting grades, and LED presets. Preserve Muse's scene work and avoid duplicating or overwriting assets.

## Source-of-truth and integration rules

- Keep the existing Blender scene, model, furniture, materials, and lighting implementation as the source of truth.
- Do not rename, move, re-export over, or modify shared scene assets as part of the reel setup.
- Keep render outputs in a new, dedicated output directory (suggested: `renders/lighting-gag-reel/`) and keep temporary files outside tracked source directories.
- Do not hard-code local absolute paths, credentials, tokens, or machine-specific cache locations.
- Before rendering, confirm the actual preset names/order from the lighting implementation and the original production conversation. The counts reported by the owner (32 grades and 15 LED presets) are planning context, not independently verified here.
- If Muse has an active branch, coordinate through a separate branch/PR and rebase or update against the latest `main` before merging. Never force-push or merge over concurrent scene changes.

## Suggested reel structure

1. **Establishing shot** — Cape Jones in the existing living room under the baseline setup; hold long enough to read the composition.
2. **Lighting-grade pass** — cycle through the confirmed grade list while keeping camera, pose, exposure policy, and scene layout fixed.
3. **LED-presets pass** — show the confirmed LED presets in a consistent order, one at a time, with a brief transition or label between looks.
4. **Selected combinations** — show only combinations already approved in the development log; don't invent these combinations if the source notes aren't available.
5. **Final comparison** — baseline, strongest approved looks, and a clean end card.

## Consistency and render settings

- Use one locked camera and frame range for all lighting comparisons unless the approved gag explicitly calls for camera motion.
- Keep resolution, frame rate, color management, exposure, and output codec consistent across the comparison shots.
- Use short preview renders first; inspect flicker, clipping, shadow artifacts, missing textures, and scene-loading errors before full-quality output.
- If a lighting change is intended to be the gag, keep the change readable and avoid adding unrelated camera or geometry changes.
- Include a simple shot/preset label only if it matches the naming already used in the project.
- Export a review MP4 and retain the render settings/shot manifest beside it. Do not commit large generated videos or caches unless the repo's existing media policy calls for that.

## Merge-safety checklist

- This change is additive documentation only; no production assets or Muse-owned files are replaced.
- Confirm the target branch is current before merge.
- Review the PR diff for accidental binary files, generated outputs, secrets, and unrelated changes.
- Run any repository checks available for the changed paths. If no checks exist for documentation, report that explicitly rather than claiming tests passed.
- Verify the pull request's status checks and mergeability on GitHub; a successful document commit alone does not prove the video rendered or that the PR is green.
- Do not merge until the actual preset sequence and any conflicts with Muse's concurrent work are reviewed.

## Current blockers

The connected repository inspection did not surface the original lighting-gag conversation log or the actual living-room Blender scene/preset files. Those inputs must be identified in the existing production workspace before this document can be turned into a verified shot-by-shot render plan. No video has been rendered by this change.
