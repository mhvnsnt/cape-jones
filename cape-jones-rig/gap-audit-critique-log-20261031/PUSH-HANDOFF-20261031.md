# Push Handoff — Gap Closure (for the separate repo-push workstream)
## Land PR-only, gate-checked, additions only, 0 deletions, no force-push.
## Verify on main by size + SHA AFTER merge before calling anything landed.
## Routing: original Cape Jones work only -> mhvnsnt/cape-jones.
## No show character art/name/dialogue/logo in any of these folders.
## No file in these folders was pushed by the gap-audit work itself.

Folders to land, in order:
1. gap-audit-critique-log-20261031/ — CRITIQUE-LEARNING-LOG, GAP-AUDIT,
   PIPELINE-WIRING, this handoff, 5 viewed sheets, ACES plate renders
   (preliminary; colour chunk's fighting-pose ACES comparison supersedes
   them as the comparison of record — land both, note the supersession).
2. gap-close-rig-20261031/ — missing pieces pack, fist v4b + punch v4c,
   true-final-flex v2, 3/4 kitbash + side/back stand-ins (labelled),
   cape bone-chain + composite, foreshortened forearms, QC scripts +
   results, folder report. (Pre-existing forearm-fist-v4-20261031/ is a
   separate parallel folder — do NOT merge or overwrite it; land it
   only if the push workstream already owns it.)
3. gap-close-tv-20261031/ — storyboards (6-panel + 30-panel index),
   animatic MP4 + contact + frames, EDL JSON+CSV, QC JSON+MD,
   principles matrix JSON+sheet, title card, credits template,
   dialogue shot CJ-26, archive manifest (68 files), build script.
4. gap-close-color-20261031/ — ACES 1.3 comparison (renders + .blend +
   sheet), room-2.5x Blender proof (+ .blend, with its desk-substitute
   caveat in the report), JoJo pose shifts, JoJo sequence colour script,
   Level-3 PIL composites + sheet (labelled PIL), painted-bg shifts,
   background colour scripts, folder report, build scripts.
5. gap-close-sound-edit-20261031/ — sound layer stack + demo WAV
   (measured -16.27 LUFS, NOT -14) + intermediates, lip-sync strip +
   timeline JSON, camera-move sheet, edited punch + dance MP4s +
   contact sheets + edit JSON, background consistency check, safe-area
   overlay, effects wiring map, build script, frame intermediates.

Known caveats to carry into PR bodies (do not silently fix):
- QC 27/30 PASS, 3 FAIL (CJ-05/06/26, rim hues unstated).
- 9 storyboard thumbnails are POSE PENDING; 17 EDL holds are ASSUMED 12f.
- True hand-drawn 3/4/side/back masters are NOT in these folders (stand-ins only).
- Recorded audio is 0%; demo audio is synthesized, measured -16.27 LUFS.
- Delivery frame size is NOT set anywhere in these folders.
- Room-2.5x proof uses a desk-painting substitute (true KKGuh not found on disk);
  chair-back-at-waist is not claimed against it.
- Level-3 composites in the colour chunk are PIL, not Blender production renders.
