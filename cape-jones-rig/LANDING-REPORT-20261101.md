# Cape Jones — Clean Landing ALL — Final Report — 2026-11-01

Repo: `mhvnsnt/cape-jones`. All merges PR-only, additions only, 0 deletions,
no force-push. Every merge was made only when `mergeable_state` was `clean`
(GREEN); `unstable` while Cast CI ran was treated as transient, never merged
on. Every batch below was verified on main by git blob SHA (a blob SHA match
implies a size match, since blob SHA = sha1("blob <len>\0" + bytes)).

## Original scope: 10,595 / 10,597 verified = 99.98%

Local uploadable snapshot was 15,377 files; 4,785 were already landed by prior
work (A–F, G1, UI v2, clean-100); the landing scope was 10,592 new paths +
5 updated root docs = 10,597 files, split into 20 batches.

| Batch | PR | Merge SHA | Verified |
|---|---|---|---|
| B0-second-pass-large | #299 | fed409f083aff9ab8707d39f91a593f316716374 | 32/34 |
| H-3 | #300 | 62efe4c3c2d7efb526ba3d09c78ed68bd7b4bf50 | 28/28 |
| H-6 | #301 | a330d83d11bf942f5e886f61305997f697e11d0b | 295/295 |
| B1-new-folders-roots | #302 | 078b2f18145b5d94d3dfbecfce4ce924919bf8a5 | 592/592 |
| H-1 | #303 | fdba7c6560ba14df9aa02f4ad07d81b604a53339 | 672/672 |
| H-4 | #304 | 462f8039f6993998ab1727ac7a9bee20dff9b6b1 | 316/316 |
| G2-2 | #305 | 3785518952e1ea38d50ee0db61db30a87affa0f1 | 527/527 |
| G2-6 | #306 | be00843220cd885b5150f54609bc1a513bd948d6 | 32/32 |
| H-2 | #307 | 8c6bb965b42a855ad2d52505815dd3ceecfb8f07 | 750/750 |
| G2-4 | #308 | 0156a2d5001f9937a44e416763c9e0709a637bd9 | 559/559 |
| H-5 | #309 | c17c4dbd750d5d98b543b3201ad599b68efaa5b2 | 750/750 |
| G2-3 | #310 | 9ecf66882f899aceff2e5ab2baac3bb2787e233c | 582/582 |
| G2-1 | #311 | 82797df46ceb8411f901ac767839dafc54970b3f | 710/710 |
| H-7 | #312 | af634d748d2ee0c19c2583d2e862cf52dc4cd34d | 748/748 |
| G2-7 | #313 | 00ae77a5a348af30cfe6b84a986b12915dd0a482 | 750/750 |
| G2-5 | #314 | d871f5ef4b7de83462e9cf85e728d0242c6f8285 | 735/735 |
| G2-8 | #315 | ade18df7a3c30758cfc5bcf302b37a4b6db513df | 750/750 |
| G2-11 | #316 | 92d3999559d00664df12bf0cabd90101c0e3305c | 273/273 |
| G2-9 | #317 | a20e69685494ee417155c0a7766e7b348267315d | 750/750 |
| G2-10 | #319 | 1178c53302c59aa3b560635fc3251afe5dbc10cf | 744/744 |

Total verified from the original scope: 10,595 / 10,597 = 99.98%.
Still owed from the original scope: 2 files = 0.02% (see "Still owed" below).

## NEW sweep (files created after the original snapshot): 780 / 782 new files

| Batch | PR | Merge SHA | Verified |
|---|---|---|---|
| NEW-1 (new 20261101 folders, rig-34, pipeline, locked-default) | #321 | 55ea6d2b9a821fd6bcc923574fcc5bc221b1886d | 748/750 |
| NEW-2 (sitting-rig-34, threequarter-sitting-sheet) | #320 | cb04aff261236ecee44c67b82ce74bb7245a24b1 | 32/32 |

NEW-1's 2 unverified files are NOT missing content: both are byte-identical
duplicates of the repo's own `3d-assets/living_room.blend` already on main
(same blob SHA `c537475db64c33c5c36fa308ba16adb921e7df16`, 92,300,171 bytes),
so all NEW content is present in the repo: 782/782 = 100% by content.

## Final micro-batch FIN-1 (post-snapshot stragglers): 16 / 17 verified

17 files created after the NEW snapshot: `canonical-room-3d-2d-20261101` (5:
report, blender render/log files, render_room.py),
`rig-34-locked-default-sitting-neck-v2-20261101` (9: neck-v2 manifest,
landing list, lean/idle animations, chat-playable versions, neck zoom
contact), `shots-final-painted-bg-20261101` (3: report, painted-bg contact,
gates).

| Batch | PR | Merge SHA | Verified |
|---|---|---|---|
| FIN-1 | #322 | 54be513b44daf73e1c2bcfeb91de4e3ef80ec1ab | 16/17 |

FIN-1's 1 unverified file is the 51 MB neck-v2 lean MP4 (see "Still owed"
item 3). This report file itself landed separately as FIN-2; its PR, merge
SHA, and verify count are in the landing delivery that accompanied it.

## Still owed (3 files) — GitHub API route failed

Items 1–2 are from the original scope (2/10,597 = 0.02%); item 3 is from the
FIN-1 straggler scope (1/17). All three are under GitHub's 100 MB per-file
limit, but the API route rejects them from this environment.

Both are under GitHub's 100 MB per-file limit, but the API route rejects them
from this environment. Direct git push is unavailable (no git credential for
this repo on the VM; the local room-clone was deleted by another agent).
No token was requested or injected. Kept local, NOT deleted.

1. `duplicates-organize-20261031/features.json` — 60,245,091 bytes,
   local blob SHA `d9a2bc79c8faee8e437e0fab2bf261eff24a1ecc`.
   Contents API PUT: 422. Two direct probes: 401 `{"message": "Bad
   credentials"}` (small PUTs on the same branch succeed, so auth works;
   large payloads fail). Git Data API `POST /git/blobs`: 422
   `{"message": "Sorry, your input was too large to process. Consider creating
   the blob in a local clone of the repository and then pushing it to
   GitHub."}`
2. `mixed-media-2d-3d-bridge-actual-model-20261031/model/cape_jones_rigged.blend`
   — 95,744,707 bytes. Contents API PUT: 422 (same pattern).
3. `rig-34-locked-default-sitting-neck-v2-20261101/animation-lean/sit-lean-neck-v2-20261101.mp4`
   — 51,363,811 bytes, local blob SHA `cd7fbf9bd69bd3bf7cee74ddde16b85813ad015b`.
   Contents API PUT: first attempt 422 with fallback GET 404 (file
   not on branch — the 422 was a payload rejection, not a conflict); retry:
   401 `{"message": "Bad credentials"}`. Same large-payload failure mode.
   Practical Contents API ceiling from this environment sits between 36 MB
   (worked) and 51 MB (failed). A 21 MB GIF version of the same animation
   and 700w chat-playable versions ARE on main via FIN-1.

TerraBox is BACKUP ONLY. The GitHub-route failure condition for TerraBox is
met for these 3 files, but this landing ran as a subagent with no browser
login, so TerraBox upload must be delegated as a browser task with Mars's own
sign-in. No TerraBox credentials were invented.

## Excluded, kept local, NOT deleted

- `__pycache__/`, `venv/`, `gsroot/` rebuildables; any `.git/` tree;
  `*.blend1` backups; `media-generation` JSON scratch (image deliverables
  were included).
- `canonical-room-3d-2d-20261101/work/room-clone/` — a clone of repo content
  itself; re-uploading it under `cape-jones-rig/` would duplicate repo
  content. `.git` objects there are rebuildables, not work.
- NEW-1's 2 `living_room.blend` copies (see above) — proven duplicates of
  `3d-assets/living_room.blend` already on main; landing them again would be
  a second 92 MB copy of the same blob. The 409 "Repository rule violations /
  Timed out validating the rule" on the first copy is consistent with the
  repo ruleset timing out on a 92 MB duplicate.

## Notes

- Duplicate PR #318 exists for the G2-9 branch (created by a concurrent
  finish process); PR #317 for the same branch already merged. #318 was left
  open, not merged — merging it is unnecessary since its branch is in main.
- Probe branch `feature/cape-jones-probe-large-20261101` remains, no PR,
  containing only `cape-jones-rig/probe-small-20261101.txt` (created to prove
  small PUTs work while large payloads fail). Harmless; not deleted.
- G2-9's upload run recorded 117 transient 409 conflicts; all 750 files were
  nevertheless verified on main after merge — the conflicts were on files
  already correct on the branch.
- Older unrelated open PRs #270–#274 were left alone.
- Pipeline: `~/workspace/cape-jones-rig-repo-batch/landing_all_20261101/landing_all.py`
  (per-batch state files in the same directory).
