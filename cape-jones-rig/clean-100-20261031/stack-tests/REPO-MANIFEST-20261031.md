# Repo verification (READ-ONLY) — mhvnsnt/cape-jones main, 2026-10-31

Method: `~/workspace/cape-jones-rig-repo-batch/gh_api.py` GET only (no token
printed, no push/commit/delete). Main head at check time:
**02694af9d149e57d619402c8ecf154ed2be87f13** — this is the PR #287 merge SHA
from push_v7c.log, so main has NOT advanced past #287 in this check. The
separate parent worker's post-#287 batch is therefore NOT yet on main.
Full tree dump: repo-main-tree.json (47,541 blobs returned; GitHub reported
`truncated: true`, so tree absence alone was NOT treated as proof — every
"missing" item below was re-checked individually via the contents API, 404).

Script: verify_repo_readonly.py. Machine log: repo-verification.json.

## Checklist result (valid items only)

One checklist path was INVALID and is excluded from the count, not counted as
missing: `clips-v7c-clean-20261031/flex/true-flex-double-bicep-v7c-clean.png`
does not exist locally (that folder's flex file is the fighting pose only).

- **Present on main, size-matched: 18/31**
- **Present on main, STALE (older version than local): 4/31**
- **Absent from main (contents API 404): 9/31**
- **Present in any version: 22/31; fully current: 18/31 = 58%**

### Size-matched (repo size = local size at check time)

| repo path (under cape-jones-rig/) | repo size |
|---|---:|
| joint_locked_rig_v7c.py | 5,676 |
| rig-apose-v7c-clean-transparent.png | 478,221 |
| cut-limbs-v7c-gauntlet-out-fixed/Arm_Front_Lower_OutFixed.png | 39,624 |
| cut-limbs-v7c-gauntlet-out-fixed/Arm_Back_Lower_OutFixed.png | 38,291 |
| cut-limbs-v7c-flex-out/Arm_Front_Lower_FlexOut.png | 40,437 |
| reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png | 399,260 |
| reposes-v7c-clean/true-flex-double-bicep-v7c-clean.png | 434,759 |
| reposes-v7c-clean/true-flex-double-bicep-gauntlet-out-fist-in-roll-v7c-clean.png | 446,174 |
| apply_lighting_level2_v2.py | 8,453 |
| showcase/lighting-level2-v2/level-2-v2-colored-warm-rim-20261031.png | 606,536 |
| showcase/luts-spectrum-v2/lut-33-blue-violet-normal.cube | 754,747 |
| showcase/luts-spectrum-v2/lut-33-magenta-rose-deep.cube | 754,747 |
| showcase/lut-neutral.cube | 688,234 |
| showcase/lut-warm.cube | 688,234 |
| LIGHTING-LEVELS-0-5.md | 4,656 |
| RIM-COLOR-RULE.md | 4,782 |
| GAUNTLET-FLIP-RULE.md | 7,376 |
| UNIVERSAL-PIPELINE.md | 5,110 |

SHA evidence (contents API, for the stale items where SHA was returned):
STATUS sha 65e9edea411eb99221d901c2a950a970743b47b8,
TRACKER sha 0179dcde3bfd2ad6a286aff768f70ad9ea4faea4,
FREE-FIRST-WIRING sha 049f4bf045259215900910feaec2f99ef0e7332a,
UNIVERSE-COLOR-LANGUAGE sha a5f2676039841a5e2598c0d5996b7fadf3f1d226.
(TREE SHAs are git tree SHAs, not blob SHAs, so they are not quoted as file SHAs.)

### Stale on main (present, but local is newer — needs the separate worker's push)

| file | repo size | local size at check |
|---|---:|---:|
| STATUS-20261031-1428.md | 24,733 | 37,488 at check, 44,578 later the same evening — local is a moving target, other lanes editing it live |
| TRACKER-20261031.md | 8,412 | 8,763 |
| FREE-FIRST-WIRING.md | 2,647 | 2,988 |
| UNIVERSE-COLOR-LANGUAGE.md | 6,834 | 7,233 |

### Absent from main (contents API 404; whole directories also 404)

- COMPARISON-TESTS.md (local 2,853 bytes) — this workstream's own doc is not on main yet
- 12-PRINCIPLES-CHECKLIST-20261031.md (local 4,229)
- pack4-20261031/ — whole directory 404: PACK4-REPORT-20261031.md,
  pack4-manifest-20261031.json, visemes/viseme-01-rest-20261031.png,
  eye-strips/eye-strip-01-determined-focused-20261031.png,
  cape-states/cape-billowing-20261031.png, head-34-front-derived-20261031.png.
  Local pack4 total: 36 files (14 visemes + 8 eye strips + 4 cape states +
  foreshortened + head-34 + proofs + report + manifest).
- clips-v7c-clean-20261031/ — whole directory 404 (local 17 files:
  dance 3, flex 1, flying 4, jump 4, punch 1, walk 4; walk-01 checked
  individually, 404).
- clean-100-20261031/ — directory 404 (this workstream's folder itself is not
  on main yet, as expected — it is this batch's output, for the worker to push).

## Prior lock, for context (not re-verified file-by-file here)

PRs #276–#285: 194/194 files verified on main (push_pr.log). PR #287: 292/294
OK on main in push_v7c.log, the 2 exceptions being the then-current STATUS /
TRACKER sizes — consistent with the stale STATUS/TRACKER finding above.

## Disney FLA / nick.7z — still unknown, NOT claimed absent

- GitHub code search (repo:mhvnsnt/cape-jones and user:mhvnsnt):
  `ww226_26s_016` → 0 hits; `ww226` → 0 hits; `nick.7z` → 0 hits.
- Tree listing: 0 `.fla` paths among the 47,541 returned blobs — but the tree
  was truncated, so this is NOT conclusive for the whole repo, and code search
  does not reliably index binary .fla / archive contents.
- Local filesystem search (workspace, maxdepth 4, names `*nick*.7z`, `*ww226*`,
  `*.fla`): 0 hits.
- 7z tooling: NO `7z` / `7za` / `p7zip` / `py7zr` binary on this VM, and no
  nick.7z file was located to list — so its contents are still unknown.
  Reason, plainly: no file found + no 7z tool + no download route in this
  subagent's scope (browser download is a parent task). Do NOT report nick.7z
  as checked, opened, or absent.
- No show content was downloaded in this batch (listing/search only, as tasked).
