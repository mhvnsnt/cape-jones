# King Voice Acquisition for Pantera — Status & Pull Request (2026-10-24)

**Status: NO CLIPS DELIVERED — by design, not by omission.**
No verifiable King voice clip exists on this VM from any owned Tekken
game today. Nothing below is presented as King's voice. Nothing is
sound-locked. This doc records the exact blocker per source and the
precise pull that unblocks it, so the next lane (Grok's Steam-logged-in
box) can execute without re-doing this survey.

**Show context:** Pantera's greeting + fight vocalizations for Cape
Jones Episode 1, "Immortal Qombat." King does not speak words — the
need is growls, roars, grunts from a CHARACTER voice bank.
Tekken names appear here because this is a technical/production doc
only; they never appear in in-universe show writing.

## 1. Owner authorization (broadened 2026-10-24, supersedes "T6-only")

> "We need to get those voice files either from Tekken 7 or Tekken 6
> or whatever has King's voice in any of them anyway possible... I only
> [have] Tekken 7 [that's] on Steam... you have access to it and you
> know I own the other games but they're not on Steam but whatever
> games you can get the goddamn voice files from however even if you
> need to decrypt them or whatever."

Rules that did NOT change: character voice bank ONLY; NEVER stage
sounds; NEVER an unattributed carved clip presented as King; label
the TRUE source game per clip; nothing sound-locks until the owner
ear-checks. NEVER Tekken 8 — the user does not own it, so no T8 pull,
period.

## 2. Per-source verdicts (all checked 2026-10-24 from this VM)

### Tekken 7 (Steam, app 389730, depot 389731) — PREFERRED, BLOCKED ON AUTH HERE

- Pipeline is WIRED (tools vendored: repak, CUE4Parse, umodel,
  TKMovesets; runbooks `T7-STEAM-EXTRACTION.md`,
  `T7-EXTRACTION-PIPELINE-2026-10-23.md`). T7 paks are NOT
  AES-encrypted, so unpacking is straightforward once the paks land.
- Audio lives at `TekkenGame/Content/Paks/` → unpacked
  `Game/Content/WwiseAudio/Windows/` (Wwise `.bnk`/`.wem` → decode
  with wwiseutil/vgmstream → WAV/MP3).
- **Blocker, proven:** anonymous DepotDownloader on this VM reaches
  Steam and reads AppInfo, then reports: "App 389730 (TEKKEN 7) is
  not available from this account." No saved Steam login exists on
  this VM (no DepotDownloader account config, no Steam client
  state). This VM cannot authenticate to the paid depot, and
  credentials must never be solicited or handled by agents.
- **Disk note:** 27 GB free on this VM — the full 47 GB depot does
  NOT fit, but a SELECTIVE audio pull (manifest → paks containing
  WwiseAudio → one pak at a time, extract → delete) does fit.
- **Unblock path:** §3, Grok's Steam-logged-in box (saved login,
  one pak at a time). This is the fastest real path to clips.

### Tekken 6 PSP — BLOCKED (no attribution)

- Bulk pack IS decrypted (`DATA401.BIN`, 2,169 entries, 384 MB) but
  `DATA401.IDX` is encrypted with no working keyset, so bulk files
  have no filenames, no bank boundaries, no character mapping.
- ~299 carved RIFF/WAVE clips exist but cannot be attributed to King
  (vs Kuma, Roger, stage SFX, etc.). Delivering one as King would be
  guessing — forbidden. Full survey: `docs/research/EP1-PANTERA-VOICE-TRACK-G-2026-10-24.md`
  (merged via PR #242).
- Unblock path (only one with true T6 provenance): PPSSPP live run
  dumping the decrypted IDX via the game's own `openPac` path
  (previously flagged blocked-headless).

### Tekken 6 PS3 — BLOCKED (encrypted as stored)

- Release `tekken6-ps3-full-v1` (`TEKKEN.psarc`, ~4.83 GB, 10 parts)
  is reachable only via the GitHub API asset endpoint. First 500 MB
  contains NO `PSAR`/`DSAR` header anywhere (entropy 7.997) — not a
  plain PSARC; PS3 disc-level decryption would come first. Partial
  parts kept at `~/workspace/t6work/ps3-dl/` for resume.

### Tekken Tag Tournament 2 — BLOCKED (undocumented archive format)

- Disc image mapped: XDVDFS volume (GoD title `4E4D0859`), 78 files;
  game data in `data000.bin` … `data053.bin` (numbering has gaps).
  Only small bins pulled locally (data000, data006, data019,
  data026, data034); the large bins are "(not yet pulled)".
- The bins are `0ff512ed` archives — proprietary Namco format,
  content compressed/encrypted (not zlib/lzma), NOT publicly
  documented, requires reverse-engineering. No internal file
  listing exists; character/voice attribution requires parsing that
  format first. Strings-level fragments (bnk/XMA shards) carry no
  filenames and prove nothing about King.
- Runbook expectation (unexecuted): per-character bundle includes
  "voice bank refs"; audio = XMA banks decoded to WAV/OGG. That
  lane has not run — Law/Lars carve and audio banks are unchecked.
- Unblock path: RE lane for the `0ff512ed` format, then stream-pull
  the large bins, then King-bank attribution, then XMA decode.
  Days of work, not a quick pull.

### Tekken 5 (PS2) — BLOCKED (no audio mapped)

- ISO acquired + surveyed (~15%): DW anim files located, but
  model/anim/moveset decode is missing (romD + TK5DATA0 formats →
  RE bench). No voice bank has been mapped or extracted. Same shape
  of lane as TTT2, earlier stage.

### Stage sounds (`F_KING`) — FORBIDDEN, not reused

- The 9 files in western-heart
  `teardown/eastern-mind/stage-1-plains-of-chi-u/sounds/F_KING/`
  were owner ear-checked 2026-10-24 as music/SFX, not dialogue.
  NOT reused, copied, or re-sent here. The script correction for
  this is PR #248 (cape-jones).

### Tekken 8 — FORBIDDEN, not attempted

- User does not own T8. No T8 source was touched.

## 3. Pull request for Grok's box (the unblock — execute in order)

On the Steam-logged-in machine (saved login, one pak at a time):

1. DepotDownloader manifest for app 389730 / depot 389731
   ("TEKKEN 7 Content"). List pak contents; identify which pak
   chunk(s) contain `TekkenGame/Content/Paks/` entries under
   `WwiseAudio/Windows/`.
2. Pull ONLY those paks, one at a time (disk rules: extract →
   convert → delete the pak before the next; never hold the full
   47 GB depot).
3. `repak unpack` (no AES key — T7 paks are unencrypted; Geese /
   Noctis per-file encryption is out of scope and not needed).
4. In `Game/Content/WwiseAudio/Windows/`, identify King's voice
   bank BY BANK NAME / METADATA at pull time. If no bank can be
   attributed to King from its name, path, or Wwise metadata, STOP
   and report that — do not guess, do not deliver a neighbouring
   bank as King.
5. Decode the bank (wwiseutil / vgmstream) to WAV, cut greeting +
   fight vocalizations (growls, roars, grunts — pick the clips
   that read as a greeting and as fight exertion; King has no
   spoken lines), convert to MP3.
6. Return: the MP3s + a manifest with EXACTLY these columns —
   source game (Tekken 7), source pak path, Wwise bank name,
   clip ID, duration, what it is (greeting / growl / roar /
   grunt), decode tool + version. No clip ships without its row.
7. Sound lock stays open: the owner ear-checks every clip before
   anything locks. Clips go to the owner as direct download links,
   never in-chat attachments.

## 4. What happens when clips land (manifest template)

| Clip ID | Source game | Source pak path | Wwise bank | Duration | Content | Status |
|---|---|---|---|---|---|---|
| (e.g. `t7-king-greet-01`) | Tekken 7 | (pak path) | (bank name) | (s) | greeting growl | awaiting owner ear-check |

Manifest file (when clips exist):
`docs/research/KING-VOICE-MANIFEST-2026-10-24.md` (new file; this
status doc stays as the audit trail).

## 5. What was NOT done here

- No Steam credentials solicited, handled, or copied. No T8 source
  touched. No stage sounds reused. No carved/unattributed clip
  delivered or relabelled. No game runtime code changed (show
  audio acquisition only).
- This doc is a status + pull request, not a clip delivery. The
  moment §3 returns clips, the manifest PR replaces this doc's
  "no clips" status — it does not silently edit it away.
