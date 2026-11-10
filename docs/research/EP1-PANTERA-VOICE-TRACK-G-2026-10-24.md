# TRACK G — Pantera real voice clips (Tekken 6 character voice bank) — BLOCKED, no clips delivered

**Date:** 2026-10-24 · **Worker:** TRACK G · **Episode:** 1, "Immortal Qombat"
**Status: BLOCKED — no clips are delivered with this report, by design.**
Nothing here is sound-locked. Nothing below is presented as King's voice.

## 1. What was asked

Pull King's REAL voice clips from the Tekken 6 character voice bank (not
Tekken 3, not stage sounds) for Pantera's greeting + fight vocals, with a
per-clip manifest (source path + clip ID), verified as coming from a
CHARACTER voice bank, for the owner's ear-check. The owner is the final
verification; nothing locks before his ear-check.

## 2. What was NOT reused (owner correction honoured)

The 9 old files from
`western-heart: teardown/eastern-mind/stage-1-plains-of-chi-u/sounds/F_KING/F_KING_s000–s008.wav`
were NOT reused, NOT copied, NOT re-sent, and the old folder was NOT
modified. The owner ear-checked them on 2026-10-24 as music/SFX, not
dialogue. They came from a STAGE sounds folder, not a character voice
bank. Their measured properties (for the record only): mono, 22,254 Hz,
2.40–7.99 s each (s008 is 0.10 s). They stay separate from this track:
the old local copies remain in `~/workspace/pantera-clips/`; this track's
work lives in `~/workspace/pantera-clips-t6/` (currently: this report +
`verify_clips.py` only — no audio).

## 3. Survey — what T6 voice/teardown data already exists (checked first)

- **western-heart repo, `teardown/tekken6/`:** docs, tools and models
  only (TEARDOWN.md, MOTION-UNBLOCK-2026-10-23.md, DINF-400-DECRYPTED.md,
  sector-cipher / keyhunt docs, EBOOT). **No audio, no voice bank, no
  character sound files.** GitHub code search for T6 voice / DATA401 /
  tekken6 in western-heart returned 0 hits.
- **No T6 character voice bank exists anywhere in either repo**
  (western-heart or cape-jones) that this worker could reach.
- **No substitution was made.** No T3 clips, no stage sounds, no T5 /
  T7 / TTT2 clips were delivered or relabelled as T6 voice. T7 and T5
  are different games' banks and would not satisfy the owner's
  "Tekken 6 character voice bank" instruction.

## 4. Tekken 6 PSP — bulk data IS decrypted, but the file map is not

This is the closest existing T6 source, and it still does not yield a
verifiable King voice bank:

- Source on this VM: `~/workspace/t6work/tekken6-psp.iso` (ISO filesystem
  lists only movies, EBOOT, `DATA401.IDX` (26,028 bytes) and
  `DINF_400.BIN` (120 bytes); the 384 MB game-data region lives in raw
  disc sectors, not as a file).
- `DINF_400.BIN` decrypts (verified by the 2026-10-23 lane): pack
  `DATA401.BIN`, **2,169 entries, 384,051,200 bytes**, build 2009-11-09.
  The manifest carries **no filenames and no keys**.
- The Oct 16 recon backup (`western-heart` release
  `tekken6-recon-20261016`, re-downloaded and verified complete this
  run: 524,288,000 + 524,288,000 + 82,708,480 bytes) DOES contain
  `tekken6/work/decrypt3/bulk_decrypted.bin` (384,073,728 bytes) — the
  decrypted bulk pack, extracted this run to
  `~/workspace/t6work/recon-x/tekken6/work/decrypt3/bulk_decrypted.bin`.
- **The blocker is `DATA401.IDX`:** it is encrypted and does not
  decrypt with any known keyset (2026-10-23 lane tested keyset A,
  keyset B, sector keys, tweak brute force — all chance level). This
  worker re-checked the raw IDX: 2,169 × 12-byte entries, random-looking
  in both byte orders, no monotonic offsets, no plausible sizes. The
  decrypt path goes through imported `openPac`, which is not on the
  disc — i.e. it needs a live PPSSPP run, not a static pull.
- Carving the decrypted bulk finds **~299 RIFF/WAVE files**
  (RIFF-wrapped ATRAC3plus, 44.1 kHz stereo; spot-checked: one 2.63 s
  clip, one 104.56 s clip that is plainly a music-length file). Carved
  clips have **no filenames, no character mapping, and no bank
  boundary** — the bulk is a flat concatenation of 2,169 files in an
  unknown (IDX) order. Attributing any carved growl to King (vs Kuma,
  Roger, or any other growling fighter, or a stage SFX file) would be
  guessing — the exact failure the owner's 2026-10-24 correction
  punished. **So no carved clips are delivered as King's voice.**
  The carve inventory is research for the next lane, not sound-lock
  material.

## 5. Tekken 6 PS3 — archive as stored is not a plain PSARC

- `western-heart` release `tekken6-ps3-full-v1` holds
  `TEKKEN.psarc` split into 10 parts (~4.83 GB total; manifest sha256
  `c98fb02602d58564ef4e80d386310cb3c48634566990a5050ef20ef2a4afd340`).
- Public download URLs for this untagged release 404; the parts are
  reachable only through the GitHub API asset endpoint (signed
  redirect). Asset IDs are saved in `~/workspace/t6work/ps3-assets.txt`
  for a future resume.
- Parts aa–ab fully downloaded this run, ac partial (~217 MB), then the
  download was stopped: the first 500 MB contains **no `PSAR`/`DSAR`
  header anywhere, entropy 7.997 throughout** — the stored file is NOT
  a plain PSARC extractable with PSARC tools. It behaves like
  encrypted/compressed-as-a-whole data (PS3 disc-level protection is
  the likely explanation, unproven). Completing the 4.83 GB download
  would still leave a decryption project, not a voice bank. The
  partial parts are kept at `~/workspace/t6work/ps3-dl/` for resume;
  the joined-file sha256 was NOT verified (download incomplete).

## 6. Exact blocker (for the coordinator / owner decision)

To deliver verifiable T6 King voice clips, one of these must happen
(first is the only one that yields T6 character-bank provenance):

1. **PPSSPP live run lane:** run the T6 PSP ISO under PPSSPP with the
   game's own `openPac` path executing, dump the decrypted IDX (and/or
   the per-character sound files as the game opens them). This is a
   reverse-engineering lane, not a file pull; it was already flagged
   blocked-headless by earlier lanes. Until the IDX is decrypted, no
   bulk file can be attributed to any character.
2. **Owner decision (explicit, separate from T6):** approve a different
   game's King bank (e.g. T7, where King voice banks are a known,
   documented format) as a *replacement source, labelled as such* —
   NOT as "T6 voice". This worker did not do that unilaterally, per
   the task's no-substitution rule.
3. **Owner-supplied T6 console files:** if the owner holds T6 on a
   platform whose voice bank is already extracted (or can be), that
   file set, with its character paths, would unblock this track
   directly.

## 7. Verification status (honest)

| Check | Result |
|---|---|
| Old F_KING stage sounds reused? | No — excluded, folder untouched |
| T3 / other-game clips substituted as T6? | No |
| T6 voice bank found in either repo? | No (surveyed, 0 hits) |
| PSP bulk decrypted? | Yes (pre-existing recon backup, re-verified complete) |
| PSP IDX decrypted / files attributable to King? | **No — this is the blocker** |
| PS3 psarc extractable? | No — no PSAR header in first 500 MB, entropy 7.997 |
| Clips delivered for ear-check? | **None — correctly, since none are verifiable** |
| Sound lock? | **PENDING — blocked on acquisition, then on owner's ear-check** |

## 8. Local work products (this run, no audio delivered)

- `~/workspace/pantera-clips-t6/TRACK-G-REPORT.md` (this file)
- `~/workspace/pantera-clips-t6/verify_clips.py` (ffprobe
  format/duration checker for future delivered clips)
- `~/workspace/t6work/recon.tar` (joined Oct 16 recon backup, verified sizes)
- `~/workspace/t6work/recon-x/tekken6/work/decrypt3/bulk_decrypted.bin`
  (decrypted PSP bulk pack, 384,073,728 bytes)
- `~/workspace/t6work/psarc_list.py` (PSARC lister/extractor, written
  for the PS3 route; untested against a real PSARC since none was found)
- `~/workspace/t6work/gh_asset_dl.py` (API asset downloader, resumable)
- `~/workspace/t6work/ps3-assets.txt` (PS3 part asset IDs for resume)
- `~/workspace/t6work/ps3-dl/` (partial PS3 parts aa, ab, ac-partial)

## 9. OWNER-NEEDED

- **Decision on §6:** authorise the PPSSPP live-run / IDX-decrypt lane,
  or explicitly approve a labelled non-T6 replacement source, or
  supply T6 voice-bank files with character paths.
- **After acquisition (not now):** ear-check of the real clips before
  anything is locked. No ear-check is requested for any clip in this
  report because no clips are attached to it.
