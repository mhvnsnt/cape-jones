# BATCH E — UNKNOWN-ARCHIVE LISTING ONLY — 2026-11-01

Scope: listing only. No new archive was downloaded, no donor pixel was pulled,
no FLA binary was parsed in this batch (binary parses need separate parent approval).
No repo landing was done in this batch; this is a report only.

## Plain statement (required)

**Nothing from these archives is claimed as a dance, rig, or piece in this report.**
No archive below is on local disc as a donor archive. Every donor-archive count
below is carried forward from a prior audit's remote listing (central-directory /
range reads, not a full download), cited per table — it was NOT re-verified by
re-downloading in this batch, and it is NOT a claim that any donor file is in hand.

## How disc presence was checked (this batch)

1. `~/workspace/cape-jones-rig/` searched to depth 3 for
   `.zip` / `.7z` / `.rar` / `.fla` / `.swf` — only two Cape Jones's own zips found
   (see "Local archives found — NOT donor archives").
2. Full `~/workspace/` scan, `.git` directories and `__pycache__` pruned, for
   `.zip` / `.7z` / `.rar` / `.fla` / `.swf` / split-part extensions
   (`.z01` / `.r00` / `.001`). Result: **26 files total, 0 donor archives,
   0 `.fla` files, 0 `.swf` files, 0 `.7z` files, 0 `.rar` files.**
   Full scan output is saved alongside this report as `archive-scan-20261101.txt`.
3. `~/workspace/cape-jones-rig/donor-fla-rig-pull-20261101/INVENTORY-20261101.json`
   and the prior audits it rests on were read for remote-archive references.
   The inventory references **remote GitHub releases, not local folders** —
   there is no local archive folder named in it to open. The prior audits state
   explicitly that their listings were made by remote range reads, not local copies.
4. No archive was extracted. Nothing was written to disc except this report
   folder. Disc was not filled by this batch.

## Result in one line

| Check | Result |
|---|---|
| Donor archives found on local disc | **0 of 9 task items (0%)** |
| Donor archives NOT ON DISC (remote-only, per prior audits) | **9 of 9 task items** |
| `.fla` / `.swf` files found anywhere in `~/workspace/` (excluding `.git`) | **0** |
| `.7z` / `.rar` files found anywhere in `~/workspace/` (excluding `.git`) | **0** |
| Local archives found, all unrelated to the task list | 26 (see last section; largest is a Mochiichao cries zip, 12,022,665 bytes) |

---

## 1. Nick 2024 zip — NOT ON DISC

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | Release `bonus-non-cn-v1` in `mhvnsnt/cn-gigaleak-bonus-non-cn`, asset `2024_Nick_Gigaleak.zip`, split parts 0000–0041 |
| Size | 4.33 GB (remote, per prior deep audit; combined with nick.7z = 11.54 GB ≈ the ~11.5 GB in the task) |
| Entry count | 1,610 entries (remote central-directory listing, prior audit) |
| `.fla` / `.swf` counts | 0 / 0 — this archive's animation is NOT Flash; see below |
| Rig / dance-relevant entries (remote listing only) | 8 Maya `.ma` rigs (character v041, location v008, noodle-arm / hands / feet / noodle-wrap / catcher props); 4 Alembic `.abc` baked caches, frames 1–182, 183–244, 244–399, 400–586; 1 dance video (timing only, show unidentified — do NOT label it as a named show's dance); pose-sheet + storyboard PDFs |
| Other listed contents | 1,028 audio files listed remotely — content unknown, NOT downloaded, NOT used |
| Top-level listing | Cannot be produced from disc — no local copy. The 1,610-entry remote listing is held only as a prior-audit summary, not as a local file list. |
| Could not be listed locally because | No local copy exists; listing it would require a remote range read / download, which this batch does not do. |

## 2. nick.7z — NOT ON DISC

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | Release `bonus-non-cn-v1` in `mhvnsnt/cn-gigaleak-bonus-non-cn`, asset `nick.7z`, split parts 0000–0068 |
| Size | 7.21 GB (remote, per prior audit) |
| Entry count | UNKNOWN — never listed, even remotely, in any prior audit checked |
| `.fla` / `.swf` / `.xfl` counts | UNKNOWN |
| Rig / dance-relevant entries | UNKNOWN — do not claim it holds rigs, and do not claim it is empty |
| Top-level listing | None available. Prior audit (2026-10-31) states it "needs a full 7z header parser + LZMA + full download; no 7z tool on VM" at that time. |
| Could not be listed locally because | No local copy exists, and its remote header has never been walked in the audits checked. This is the largest single unknown in the set. |

## 3. Disney FLA rar — NOT ON DISC

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | Release `bonus-non-cn-v1` in `mhvnsnt/cn-gigaleak-bonus-non-cn`, asset `DISNEY.LEAKS.and.wow.wow.wubbsy.fla.rar`, split parts 0000–0007 |
| Size | 757 MB (remote, per prior audit) |
| Entry count | 12 entries (remote listing, prior audit) |
| `.fla` / `.swf` counts | 1 `.fla` BY FILENAME ONLY / 0 `.swf` |
| Rig / dance-relevant entries (filename only) | `ww226_26s_016_final.fla` — 39.9 MB unpacked. Content NOT downloaded, format (XFL vs binary) NOT checked, so no rig, scene, or dance is claimed from it. |
| Other listed contents | 2 MP4s, 7 PDFs, 1 stored ZIP (contents unknown) |
| Top-level listing | The 12-entry summary above is all the prior audit records; the individual filenames beyond the one `.fla` are not reproduced in the audits checked, so they are not invented here. |
| Could not be listed locally because | No local copy exists. A content check needs a parent-approved single-asset range fetch, which is outside this batch. |

Note: the separate Disney pitch-bibles rar (`A.TON.OF.DISNEY.PITCH.BIBLES.AND.CLUB.PENGUIN.PDFS.rar`,
2.48 GB, parts 0000–0023) is a different archive — bibles/PDFs, not a FLA archive — and is
also NOT ON DISC. It is noted here only to prevent confusing the two Disney rars.

## 4. PPG rar (Powerpuff Girls, `PPG_flas.rar`) — NOT ON DISC

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | Backup release in `mhvnsnt/cn-gigaleak-powerpuff-girls` (and `-special`), asset `PPG_flas.rar` |
| Size | RAR total not stated in the audits checked; the single inner ZIP is 56.3 MB |
| Entry count | 1 inner ZIP; 0 `.fla` |
| `.fla` / `.swf` counts | **0 / 0** — the name promise is debunked by the prior audit |
| Rig / dance-relevant entries | NONE. The rar contains 1 ZIP (56.3 MB) and nothing else by the prior listing. |
| Other listed contents | The inner ZIP size-matches the 10th-anniversary ZIP — recorded in the prior audit as a hint, not proof, and not verified here. |
| Top-level listing | `PPG_flas.rar` → 1 ZIP (56.3 MB), 0 `.fla`. That is the complete listing as recorded. |
| Could not be listed locally because | No local copy exists; the remote listing above is the prior audit's result. |

### 4a. Powerpuff Girls original zip (context for the PPG rar) — NOT ON DISC

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | Release `ppg-original-cowchicken-v1`, 3 parts |
| Entry count | 9,105 entries |
| `.fla` / `.swf` counts | 0 / 0 |
| Rig / dance-relevant entries | NONE — 16 `.mov` QTVR turnarounds (pose reference, baked video), 7,397 EPS model sheets |
| Could not be listed locally because | No local copy exists. |

## 5. Johnny Bravo zip — NOT ON DISC (and its own zip was never listed)

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | Release `johnny-bravo-cowchicken-v1` in `mhvnsnt/cn-gigaleak-johnny-bravo` (10 assets including `johnny-bravo.zip` + EPS files); in-repo dirs: `model-sheets`, `show-bible` |
| Size | Not stated in the audits checked |
| Entry count | UNKNOWN — the zip itself was never listed in the audits checked |
| `.fla` / `.swf` counts | 0 verified; the prior animation audit records "N (evidence)" for a rig and notes "zip not listed" — so 0 is the evidence from the model-sheet/bible material, NOT a proven count inside the unlisted zip |
| Rig / dance-relevant entries | NONE verified. Model sheets / show bible only. |
| Top-level listing | Cannot be produced: the zip was never listed, locally or remotely, in the audits checked. |
| Could not be listed locally because | No local copy exists, and no remote listing of this zip exists in the audits checked. Do not claim a rig count for it either way. |

## 6. Regular Show material — NOT ON DISC, and still UNKNOWN (not "empty")

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | Release `regular-show-cnleaks-v1` in `mhvnsnt/cn-gigaleak-regular-show`; in-repo dir `production-docs` (1 PDF seen: `RS_SIZE4C01_CASC_CAP.pdf`) |
| Size | CONFLICTING prior notes, not resolved in this batch: animation audit says 67 zip parts, 6.83 GB; deep audit says 71 assets and "~180 × 100 MB parts, 18.9 GB". Neither figure is re-verified here. |
| Entry count | UNKNOWN |
| `.fla` / `.swf` counts | UNKNOWN |
| Rig / dance-relevant entries | UNKNOWN — no rig, scene, or dance is claimed |
| Top-level listing | Cannot be produced. Prior animation audit: "no EOCD in last 70 KB of part-065 or part-066; part-066 is a stray chunk (8.26 MB) after the EOCD-bearing part-065's false-positive PK signature." In plain terms: the split archive as held does not terminate with a readable central directory, so a trustworthy entry list cannot be built from it without its true last part. |
| Verified separately | 1 production PDF only (`RS_SIZE4C01_CASC_CAP.pdf`, production-doc format). |
| Could not be listed locally because | No local copy exists, and the remote split archive itself lacks a readable central directory in the audits checked. |

## 7. Teen Titans (3 archives) — NOT ON DISC, 0 `.fla` / 0 `.swf` in all three (remote listings)

| Archive (remote release) | Entries | `.fla` | `.swf` | Contents per prior listing |
|---|---|---|---|---|
| `teen-titans-complete-v1` (2 parts) | 970 | 0 | 0 | Model sheets only: 615 EPS, 33 AI, 29 JPG, 24 PSD, 33 PDF, 36 TIF |
| `teen-titans-cnleaks-v1` (10 parts) | 970 | 0 | 0 | Same type counts — a repack of the same content |
| `teen-titans-cowchicken-v1` (8 parts) | 1,139 | 0 | 0 | Same file types + 169 extra directory entries, still 0 `.fla`/`.swf` |
| **Total** | **3,079** | **0** | **0** | Model + expression sheets + colour callouts only; no timeline ever saved in these archives |

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Rig / dance-relevant entries | NONE. The show was traditional hand-drawn animation; the saved material is the poses it was drawn FROM (model/expression sheets), not a rig or timeline. No Teen Titans rig, scene, or dance is claimed. |
| Could not be listed locally because | No local copy exists; counts above are the prior remote listings. |

## 8. KND — Codename: Kids Next Door — NOT ON DISC, 0 `.fla` / 0 `.swf` (complete archive)

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | `mhvnsnt/cn-gigaleak-kids-next-door`; releases `knd-complete-v1` (5 parts, listed) and `knd-cnleaks-v1` (6 parts, NOT listed) |
| Entry count | 3,099 entries (`knd-complete-v1`) |
| `.fla` / `.swf` counts | 0 / 0 (`knd-complete-v1`) |
| Rig / dance-relevant entries | NONE — 10 `.mov` QTVR turnarounds (pose reference, baked video); 1,762 EPS, 704 PSD model/style material |
| Top-level listing | Counts by type above; a full filename list is not held locally and was not reproduced in the audits checked. |
| Could not be listed locally because | No local copy exists; the `knd-cnleaks-v1` parts additionally have no remote listing in the audits checked, so nothing is claimed about them. |

## 9. Johnny Test — NOT ON DISC, 0 `.fla` / 0 `.swf` (cowchicken archive)

| Field | Value |
|---|---|
| Exact local path | — none. NOT ON DISC. |
| Remote location (prior audit) | `mhvnsnt/cn-gigaleak-johnny-test`; releases `johnny-test-cowchicken-v1` (14 parts, listed) and `johnny-test-extracted-v1` (0 assets, empty) |
| Entry count | 884 entries (`johnny-test-cowchicken-v1`) |
| `.fla` / `.swf` counts | 0 / 0 |
| Rig / dance-relevant entries | NONE — art / scripts only: 348 JPG, 118 PDF, 69 AI. Scripts were NOT pulled as dialogue. |
| Could not be listed locally because | No local copy exists. |

---

## Totals

### Task items: disc presence

| Item | On disc? | Entries (remote listing) | `.fla` | `.swf` |
|---|---|---|---|---|
| Nick 2024 zip | NO | 1,610 | 0 | 0 |
| nick.7z | NO | UNKNOWN | UNKNOWN | UNKNOWN |
| Disney FLA rar | NO | 12 | 1 (filename only) | 0 |
| PPG rar (`PPG_flas.rar`) | NO | 1 inner ZIP | 0 | 0 |
| Johnny Bravo zip | NO | UNKNOWN (never listed) | 0 verified | 0 verified |
| Regular Show material | NO | UNKNOWN (no readable central directory) | UNKNOWN | UNKNOWN |
| Teen Titans ×3 | NO | 3,079 | 0 | 0 |
| KND complete | NO | 3,099 | 0 | 0 |
| Johnny Test cowchicken | NO | 884 | 0 | 0 |
| **Total, task items** | **0 / 9 on disc** | **8,685 known + 3 unknown** | **1 (filename only)** | **0** |

Known-entry total: 1,610 + 12 + 3,079 + 3,099 + 884 = 8,684, plus the PPG rar's 1 inner ZIP = **8,685**.
Unknown: nick.7z, Johnny Bravo zip, Regular Show parts — no entry count is claimed for any of them.

### Context (not task items, for disambiguation)

| Item | On disc? | Note |
|---|---|---|
| Gumball full-leak RAR5 (86 parts, 43,516,516,745 bytes remote) | NO — listing file only | Local listing file `~/workspace/cape-jones-rig/gumball-full-leak-file-list-20261031.json` (2,259 entries: 138 `.fla`, 109 `.swf`, 20 dance `.fla` = 10 unique Darwin dance scenes duplicated across two trees). This is a JSON listing, NOT the archive. No Gumball binary is on disc. |
| Disney pitch-bibles rar (2.48 GB) | NO | Different archive from the Disney FLA rar; bibles/PDFs only. |
| PPG original zip | NO | 9,105 entries, 0 `.fla`/`.swf` (see §4a). |

### Local archives actually found on disc (NOT donor archives — do not confuse with the task list)

The workspace-wide scan found 26 archive files. None is a donor/show archive.
The two in `cape-jones-rig/` are Cape Jones's own work; the rest are fonts, sound
packs, game-dev assets, and Python package test zips. Full list: `archive-scan-20261101.txt`.

| Local archive | Size (bytes) | Entries | Contents (central-directory listing, this batch) |
|---|---|---|---|
| `~/workspace/cape-jones-rig/cape-jones-pack1-clean.zip` | 1,316,446 | 34 | Cape Jones pack1-clean PNG pieces (gauntlets, hands, upper arms, cut limbs) + MANIFEST.json. 0 `.fla`, 0 `.swf`. |
| `~/workspace/cape-jones-rig/cape-jones-sliced.zip` | 854,783 | 29 | Cape Jones sliced PNG pieces (arms, legs, torso, head, cape, 5 mouth pieces) + MANIFEST.json. 0 `.fla`, 0 `.swf`. |
| `~/workspace/mochiichao-work/title-creatures-9/work/cries/all-47-cries-20261026.zip` | 12,022,665 | not listed (out of scope; Mochiichao work, not a show archive) | Mochiichao creature cries. Not opened for this batch. |
| Other 23 scan hits | ≤ 834,536 each | — | Kenney sound/font packs, browser-download font zips, Python venv test-data zips. None show-related. See `archive-scan-20261101.txt`. |

## Archives that could not be listed, and why

| Archive | Why it could not be listed in this batch |
|---|---|
| nick.7z | NOT ON DISC, and never remotely listed in any audit checked. Needs a 7z header walk / download — outside this batch. |
| Johnny Bravo zip | NOT ON DISC, and never listed (locally or remotely) in any audit checked. |
| Regular Show parts | NOT ON DISC, and the remote split archive has no readable central directory (no EOCD in the last 70 KB of part-065/066; part-066 is a stray 8.26 MB chunk). Needs its true last part. |
| KND `knd-cnleaks-v1` parts | NOT ON DISC, and unlisted in the audits checked (only `knd-complete-v1` was listed). |
| All other task archives | NOT ON DISC; their tables above reproduce prior remote listings only and were not re-listed here. |

## Sources used (all local, all listing-level)

- `~/workspace/cape-jones-rig/donor-fla-rig-pull-20261101/INVENTORY-20261101.json` (2026-11-01)
- `~/workspace/cape-jones-rig/donor-fla-rig-pull-20261101/DONOR-FLA-RIG-PULL-REPORT-20261101.md` (2026-11-01)
- `~/workspace/cape-jones-rig/show-repo-animation-audit-20261031/SHOW-REPO-ANIMATION-RIG-AUDIT-20261031.md` (2026-10-31)
- `~/workspace/cape-jones-rig/SHOW-REPO-DEEP-AUDIT-20261031.md` (2026-10-31)
- `~/workspace/cape-jones-rig/gumball-full-leak-file-list-20261031.json` + `gumball-full-leak-rar5-summary-20261031.md` (2026-10-31)
- Workspace-wide archive scan, this batch: `archive-scan-20261101.txt` (26 files)

## What is still owed (not claimed, not done here)

- A remote listing of nick.7z, the Johnny Bravo zip, the Regular Show true last part,
  and the KND cnleaks parts — each needs a parent-approved remote range-read / download step.
- A content check (XFL vs binary) of the Disney FLA `ww226_26s_016_final.fla` — filename only so far.
- No approval is claimed (0/1). No repo landing was done in this batch.

## Plain statement, repeated at the end

**Nothing from these archives is claimed as a dance, rig, or piece in this report.**
