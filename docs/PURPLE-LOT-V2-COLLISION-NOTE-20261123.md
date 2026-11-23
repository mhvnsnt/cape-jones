# PURPLE LOT V2 — Cut Collision Note (2026-11-23)

**Repo:** `mhvnsnt/cape-jones`. **Status: UNRESOLVED — owner call still open. Nothing on this page overwrites any cut.**

## The collision

Two different V2 cuts exist for the same repo path
`production/2d-parking-lot/video/purple-lot-v2.mp4`:

| Cut | Size | sha256 | Where it is |
|---|---|---|---|
| PR #430 cut (on main NOW) | 1,998,110 B | blob SHA `d2dcbd2d2286d9481d4e22d12b07b2a5f1f9b939` (GitHub blob) | main, `production/2d-parking-lot/video/purple-lot-v2.mp4` |
| Verified lane cut (NOT landed) | 2,644,070 B | `e18a78b760d966389634e88f6bf9e39fa18ecbf712643b482d644214c2c8483f` | workspace only: `~/workspace/_cape-jones-parking-lot-2d/v2/purple-lot-v2.mp4` |

## What is wrong with the cut on main

Checked own-eyes at f1 / f313 / f441 (2026-11-22): forearms + hands do
not render, head oversized, cape a flat black slab. Built with COA Tools 2
+ Wiggle 2, 44 parts. Its own-eyes pass was never done.

## What is right with the lane cut

Native Blender cutout puppet (12 bones, 28 sliced parts, T-pose v8),
dance test 96f/4s, V2 cut 480f / 20s / 1280x720 / 24fps, silent,
240 pose keys on twos. Verified own-eyes 2026-11-22. See
`docs/RIG-REPORT.md` in this PR.

## Later cuts in the workspace (also NOT landed, also binaries)

| File (workspace `_cape-jones-parking-lot-2d/v2/`) | Size | sha256 | Note |
|---|---|---|---|
| `purple-lot-v2-mixed.mp4` | 6,822,132 B | `604e49030bd316e55b18953022cd11ec57cb37094e91c544b0d90183ee297777` | V1+V2 mixed cut, 480f/20s, hand-fix verified own-eyes; see `docs/MIXED-REPORT.md` |
| `purple-lot-v2-fixed.mp4` | 2,801,354 B | `60a1311dd950da6b3a7344923c940f110189180a24bd4a36ec5323738079a39b` | Hand-fix iteration |
| `purple-lot-v2-fixed2.mp4` | 2,756,091 B | `0d50fcd6b679edc49ba9e8ad7b9bebe502783a8838e87edafe304f79f41ba222` | Hand-fix iteration 2 |
| `purple-lot-v2-handswap.mp4` | 2,684,976 B | `0a2533ab0d50720a5673455a549ebd3309d5da87c802243991fae9415e334d60` | Hand-swap iteration |
| `purple-lot-v3.mp4` | 2,690,677 B | `a9dd6b6f9202594d5666641a82a8a7c9a22506c2994f43f42003b158ae192f26` | V3 cut, re-rendered 2026-11-23 15:42 (V3 lane still running at push time; its own `pr-stage/` exists in its workdir — do not touch, that lane lands it) |

No MP4 above is in this PR: the GitHub connector carries text only
(max 16 MiB UTF-8 per snapshot, no binaries). Video landing needs a
git-authenticated route (VM git push, or browser upload) — see the
manifest in `HANDOFF-PUSH-EVERYTHING-CAPE-JONES-20261123.md` in this PR
and `~/workspace/push-everything-2026-11-23/cape-jones/VIDEO-MANIFEST.md`.

## Owner options (pick one — this PR does NOT pick)

1. **Replace** main's cut with the verified lane cut
   (`v2/purple-lot-v2.mp4`, sha256 `e18a78b7…`).
2. **Fix the parallel lane's cut** (COA Tools 2 + Wiggle 2, 44 parts) until
   it passes own-eyes at f1/f313/f441, then keep it.
3. **Merge rigs** — verified lane rig + parallel lane's 44 re-sliced parts
   (which have the elbow/knee cuts the lane rig lacks).

Until the owner picks, main keeps the PR #430 cut and this PR lands
reports only. Do NOT overwrite `production/2d-parking-lot/video/purple-lot-v2.mp4`
blindly.
