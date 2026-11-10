# Landing Report — batch G1 and beyond (2026-10-31)

Repo landing is NOT content approval. Mars approves content; this report only
proves files are in the repo.

## Verified on main before batch G

- Main at batch G start: 90f0a926b353117e970f2d08b405c64320aa0447
- PRs #290, #291, #292, #293, #294, #295 — all closed/merged (landing
  batches 3A-3F). PR #289 was the previous verified main before those.
- Main tree sample (API, truncated at 52,999 entries): 4,213 files under
  cape-jones-rig/.

## Diff at batch G snapshot

- Local non-junk files in cape-jones-rig/: 13,088
- New, not in main sample: 9,214 files, 2,107.2 MB
- Junk excluded, plainly, kept local, NOT deleted: venv/ tool installs,
  gsroot/, __pycache__/, *.blend1 backups, media-generation-* metadata.
- Held over 50 MB (Contents-API limit, needs git LFS / direct git push):
  mixed-media-2d-3d-bridge-actual-model-20261031/model/cape_jones_rigged.blend
  (95,744,707 bytes).

## Batch G1 (in progress at report time)

- Branch: feature/cape-jones-landingG1-20261031
- Files in batch: 1,236, 518.6 MB (see push_landingG.py in
  cape-jones-rig-repo-batch/ — that folder itself is NOT in the rig push,
  it is the landing tooling kept in the workspace).
- Folders: serve moves (up, up-left, up20/right5, right5, right5-nocrop-fix,
  up2), hand flips, Ghoul handswap/V2/V3, dance inbetween + lastframe fix,
  mouth-jaw cleanup 5-methods, PAH GO v2, AH/SMILE34 clean, mouth packs
  clean pipeline, figure-matched room lighting, shafts fix-100, walk
  layer fix + elbow fix, mixed-media bridge + actual-model (minus 95 MB
  .blend), Cape Consumed bare/upper + feet-uncropped, future symbiote
  capeless, transparent plates sweep, ground gate complete, Space Ghost
  workflow, crystal transformation-4, invisible power v1 no-crop fix,
  ground-feet placement wire100, plus root docs PROGRESS-STATUS,
  DELIVERY-PROTOCOL, README-EXTERNAL-AI, FOLDER-INDEX.
- PR number, merge SHA, and size+SHA verification on main: APPENDED HERE
  ONLY when the PR merges and verification passes. Until then, batch G1
  is NOT landed, it is only uploaded to a branch.
- Root docs edited after the G1 snapshot (23:01/23:02 log entries) are
  re-uploaded in a second pass before the PR is created, so the branch
  version matches the local version at PR time.

## Batch G2 (still not landed — bulk legacy, counted)

- Remaining new files after G1: ~7,978 files, ~1,589 MB, dominated by:
  sliced-clean-20261031 (2,994 files), dance-recreation-20261031 (443),
  poses-as-movements-20261031 (492), lipsync-production-20261031 (250),
  workstream-b-sweep-20261031 (209), showcase (205), storyboards-animatic
  (413, from production coordinator, may still be changing), rig-chains
  (778), robin-eyes-100 (291), inbetween (313), fight-and-sheets (353),
  mochiichao-combine-build (117), and other folders in FOLDER-INDEX.
- G2 must be split into further PR batches (G2a, G2b, ...) at ~500-700
  files each, PR-only, same gate, verified on main per batch. Do NOT claim
  G2 landed until each sub-batch's PR + merge SHA + verification are here.
- Files added by running agents AFTER the G1 snapshot (figure-matched
  vertical/horizontal, Grok full transparent sweep, etc.) go in G2, not G1,
  unless a second pass picks them up before the G1 PR merges.

## How to verify any file (external AI or Mars)

1. Open the file on main at github.com/mhvnsnt/cape-jones, path
   cape-jones-rig/<folder>/<file>.
2. Compare size + git blob SHA (sha1 of "blob <len>\0" + file bytes) to
   the local file. A PR number alone is NOT verification. A branch upload
   alone is NOT verification. Only main + size + SHA after merge counts.
