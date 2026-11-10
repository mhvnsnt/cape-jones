# PUSH HANDOFF — for the landing agent (do NOT push from this package itself)

**Order from Mars (2026-10-31 ~18:37 + 18:40 + 18:42-18:43 CDT):**
get all this landed; anything undecided/held with no reason to hold
gets pushed; if Mars needs to see it, show it to him; make sure
everything lands; document all this in the repo.

**Landing rules (standing, do not shortcut):** PR-only, additions
only, 0 deletions (no deletion approved in this task), no
force-push, merge gate (mergeable clean; build/lint/validate where
applicable), verify on main by size + SHA AFTER merge — a PR number
alone is NOT confirmation. Nothing deleted locally. Landing is NOT
approval — label unapproved items as unapproved in PR bodies.
Re-verify repo head first (last known: cape-jones PR #289, merge
70acb397d52b6f3f8483bd35aaa08e08f606dedb).

## Push THIS package first (in this order)
1. `repo-knowledge-package-20261031/` — ALL files in this folder:
   README-INDEX, CONSOLIDATED-RULES, APPROVALS-LEDGER,
   METHODS-INDEX, GAPS-OWED, MEMORY-NOTE, WIRE100-SWEEP, ADR,
   PUSH-HANDOFF, check_package.py, check_package_proof.json,
   _proof.json. Run `python3 check_package.py` immediately before
   pushing and include its PASS output in the PR body; if it FAILS,
   stop and report the failure, do not push a broken package.

## Then, in order (only if not already verified on main)
2. Earlier staged batch 2 (348 files — re-verify the staged list on
   disk first; if a file changed, push the current version, never a
   stale copy): eyes v4 (16), godray-level3 (34), wrap v2 (11),
   wrap v3 (25), wrap v4 scratch (13), dance-kneefeet v1 (71),
   dance-kneefeet correction (73), JoJo variation (5), arm2-aligned
   (5), fist v5 (15), fist v5 correction (10), afterglow (4),
   godray-level4 (17), joint-cleanup (17), gap-close-color (26),
   hip-lower (6).
3. Post-staging builds: approval-pack-20261031, reshow-approval-
   pack-20261031, production-ready-20261031, pose-dialects-20261031
   (+ COLORED-SHADOW doc/JSON), pose-dialects-fix-face-cowl-
   20261031, pose-dialects-video-20261031, ginyu-force-poses-
   20261031, ginyu-force-limits-broken-20261031, afterglow-videos-
   20261031 (+ AFTERGLOW-SHOT-PRESETS), godray-level5-20261031,
   show-repo-animation-audit-20261031, dance-arm-snap-20261031,
   face-cowl-snap-wire100-20261031, inbetween-20261031,
   fight-and-sheets-20261031, fla-piece-labelling-top5-20261031,
   wired-100-20261031, unseen-unapproved-showpack-20261031
   (PARTIAL — label it partial in the PR body, do not claim it
   complete), plus updated rule docs: ARM-FRONT-SNAP-RULE.md,
   POSE-DIALECTS-20261031.md, GINYU-FORCE-POSE-STUDY-20261031.md.
4. Dated snapshots of STATUS-20261031-1428.md / TRACKER-20261031.md
   IF appending has stopped or as a timestamped snapshot — if they
   are still moving, push a dated snapshot copy, never the live file
   as a final.

## HOLD — with reasons (do not push as finals; list in PR/report)
- Robin eye library `raw/` — EMPTY, nothing to push.
- `*.blend1` backups, media-generation-*.json, repo-main-tree.json
  (8.7 MB audit dump) — internal scratch, not content.
- Parts-catalogue single 14 MB `index.html` — phone-unloadable;
  24 split chunks already landed in PR #288. Re-check against
  Mars's 18:40 CDT rule ("no reason to hold = push"): phone-
  unloadable is NOT a repo reason — if there is no other repo
  reason, push it and say so; if there is one, name it.
- Mars-undecided items AS FINALS: device v3 scale, delivery frame
  size + safe areas, parts exceptions 6, canonical room ID,
  dual-light pick, JoJo DREAM pick, soft-on-halo experimental.
  Docs noting them as PENDING do land.
- Workstreams still running at push time (2.5D depth, spec archive,
  any inbetween/fight/labelling work not yet completion-reported):
  push only completed subfolders, label the rest as running, never
  claim a running job landed.

## Report back (required)
Per-batch PR numbers, merge SHAs, main-tree verification (files
verified by size+SHA, counts + percentages), held list with reasons
+ unblockers, any merge-gate failure with the exact blocker, and
what is still on disk and why. No file is "landed" until verified
on main after merge.
