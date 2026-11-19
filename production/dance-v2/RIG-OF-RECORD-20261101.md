# 2D RIG OF RECORD — Nov 1, 2026 (owner order 2026-11-17)

The ball-jointed 2D Cape Jones rig built/landed **2026-11-01** is the 2D rig
of record. ALL future 2D dance/rig work uses THIS stuff. No regressions:
use it as-is unless the owner says otherwise, or unless we upgrade it —
and an upgrade never goes back to anything older.

## THE RULE (owner 2026-11-17)
- Use the Nov 1 rig files below for all 2D rig/dance work.
- The Oct 29 cutout build (`_cj-dance-v2/build/parts/`, `parts2/`,
  `fallback_sheet_backup_20261029.png`, `vace_in/` driving videos, the
  fallback video) is SUPERSEDED. It is not the rig. Never use it as the
  rig again. Never feed it to VACE again (VACE work is paused anyway).
- The VACE source pieces (square-cropped posed pieces) are BANNED — never
  use them to make a rig.
- Upgrades only with the owner's say-so. No silent swaps, no going back.

## WHERE IT LIVES (repo: mhvnsnt/cape-jones, branch main)
Full file list (3,399 blobs, 19 dirs): `nov1_rig_inventory.txt` (same folder).

### The pieces (the rig itself)
- `cape-jones-rig/sliced-clean-20261031/D-xray-angle-ref/fla-front/Row1_*.png`
  — 88 pieces + `MANIFEST.json` (grey bg 153,153,153). Head = Row1_21,
  leg with knee ball = Row1_18. Verified by own eyes to match the
  owner's videos exactly.

### The proof videos (owner's clips = these files)
- Kick: `batch-a-head-turn-forward-kick-20261101/forward-kick-true-20261101.mp4`
  (1100x750, 2.291667s) + head-turn, xsheets, build script, report.
- Sit idle: `rig-34-locked-neck-v4-cape-fix-20261101/chat-playable/sit-idle-neck-v4-cape-fix-20261101-chat-700w.mp4`
  (700x800) + `animation-idle/` full version + build script + manifest.
- Side FK chain: `batch-b-side-rig-next-20261101/side-fk-chain-20261101.mp4`
- Dance test: `dance-test-20261101/` (EN/JP excerpts + silent, 1920x1080)
- Dance scene: `dance-scene-2videos-20261101/` (V1 EN + V2 JP FINAL)
- Dance flash fix: `dance-flash-fix-20261101/` (FIXED v2 EN/JP full + one-loop)

### Assembly / build
- `cape-jones-rig/build-fla-timeline.jsfl` — Flash timeline builder
- `cape-jones-rig/build-still-20261101/fla-corrections/build_native_sheets.py`
- `rig-34-locked-neck-v4-cape-fix-20261101/build_cape_fix_v4.py`
- `batch-a-head-turn-forward-kick-20261101/build_batch_a.py`
- `movement-library-clips-20261101/build_clips.py`

### Supporting sets (all Nov 1)
- `arm-front-snap-auto-20261101/` (37) — arm-snap-fixed clips incl. dance-test excerpts
- `batch-c-gif-principles-beatsync-20261101/` (17) — beatsync samples, GIFs
- `donor-fla-rig-pull-20261101/` (6), `fla-choose-side-back-20261101/` (13)
- `learning-remembering-gate-20261101/` (29), `movement-dance-presets-20261101/` (16)
- `movement-library-clips-20261101/` (31) — 8 movement clips (gumball, kick, etc.)
- `nosferatu-video5-20261101/` (7), `top5-software-20261101/` (5, side-rig .blend)
- `cape-jones-rig/fla-piece-labelling-top5-20261031/` (30)
- `cape-jones-rig/fla-compare-flex-inspect-20261101/` (19)
- `cape-jones-rig/sliced-clean-20261031/` (2,994 — all sliced sheets/xray refs)

## VERIFICATION (2026-11-16/17)
- Pieces + kick + sit videos verified by own eyes against the owner's clips.
- Only deletion under `cape-jones-rig/` in all history: commit 9ae4369fa
  (2026-11-09) deleting .md docs only. The rig was never clobbered.
- The Nov 1 clone in /tmp was lost on VM restart; inventory was rebuilt
  from the GitHub API (per-directory trees, all complete).

## STILL UNMATCHED (owner's clips, 2026-11-16)
- Stage dance, 480x270, 5.27s, with audio — NOT dance-test-EN-excerpt
  (that one is 1920x1080, 4.52s). Possibly a phone-downscaled export.
- Crossed-arms standing, 700x950, 2s — no repo match found by name.
