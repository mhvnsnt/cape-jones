# HANDOFF — Cape Jones push-everything (2026-11-23)

**Lane:** push-everything coordinator, cape-jones. **Repo:** `mhvnsnt/cape-jones`.
**Workdir:** `~/workspace/push-everything-2026-11-23/cape-jones/`
(full inventory: `INVENTORY.md`; video manifest: `VIDEO-MANIFEST.md`).

## What this PR landed (docs only — no video, no rig, no cut touched)

- `docs/RIG-REPORT.md` — PURPLE LOT V2 rig report (native Blender cutout
  puppet, 12 bones / 28 parts, dance-test proven, V2 cut verified
  own-eyes 2026-11-22). Was NOT on main (verified absent before push).
- `docs/MIXED-REPORT.md` — V2-mixed cut report (V1+V2, hand-fix cause +
  fix, verified own-eyes). Was NOT on main (verified absent before push).
- `docs/PURPLE-LOT-V2-COLLISION-NOTE-20261123.md` — the V2 cut collision:
  main's PR #430 cut is visibly broken at f1/f313/f441; the verified lane
  cut was never landed; owner options (replace / fix parallel lane /
  merge rigs) with exact sizes + sha256 for every candidate cut.
- This file.

## What did NOT land, and why

- **All MP4s.** The GitHub connector carries text only (16 MiB UTF-8
  snapshot limit, no binaries). Every V2/V3 cut is a binary over that
  route. Exact file / size / sha256 / target path / route needed is in
  `VIDEO-MANIFEST.md` in the workdir — a git-authenticated machine (the
  VM, or browser upload) must land them. Main's
  `production/2d-parking-lot/video/purple-lot-v2.mp4` is still the broken
  PR #430 cut (1,998,110 B) until the owner picks an option in the
  collision note.
- **V3 lane files** (`v3-swap-system/`, incl. its `pr-stage/`). That lane
  was STILL RUNNING at push time; its files were read-only to this lane.
  It lands its own PR.
- **Backgrounds lane files** (`torbox-pulls/`, layered rebuild). Lane
  still running at push time; read-only to this lane.
- **Other unpushed text** (not verified against main this round because
  GitHub's git-tree API returned 500s during the checks — see INVENTORY):
  `HAND-ATTACHMENT-LOG.md`, `LEAP-PLAN.md`,
  `v3-swap-system/GUMBALL-FIRSTHAND.md`,
  `v3-swap-system/CN-IN-OUR-LANGUAGE.md`,
  `torbox-pulls/TORBOX-PULLS.md`, `HANDOFF-LAYERED-BACKGROUNDS.md`,
  `HANDOFF-V3-CLEANUP-JONES-1.md`, `CHECKPOINT.md` updates. A follow-up
  lane should verify each against main (get_file_contents) and push the
  ones still absent — do NOT assume they are absent without checking.

## Already on main — NOT duplicated by this lane (checked first)

- Only open PR before this one: #429 (AnimLab smoke verdict) — untouched.
- PR #430's cut is on main (the broken one — see collision note).
- Merged 2026-11-23: #433 Jones Model, #434 pinnacle/REUSE-FIRST,
  #435 hand regression log, #436 BROTHERMAN likeness, #437 BROTHERMAN
  reference images, #438 lessons, #439 tooling audit, #440 CN inventory
  (`docs/CN-INVENTORY.md`), #441 documents catalogue, #442 Gumball
  backgrounds, #443 Gumball backgrounds use. Main head at branch time:
  see PR body.

## Exact next step

1. Owner picks collision option 1 / 2 / 3 (collision note).
2. A git-authenticated route lands the chosen MP4 to
   `production/2d-parking-lot/video/purple-lot-v2.mp4` (manifest in
   workdir `VIDEO-MANIFEST.md`; verify sha256 after upload).
3. Follow-up lane verifies + pushes the unpushed text listed above.
