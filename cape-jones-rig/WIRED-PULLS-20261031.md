# Wired Pulls — top pulls from the deep audit, parsed 2026-10-31

Source audit: `SHOW-REPO-DEEP-AUDIT-20261031.md` (41 rows). This file is the
wiring step for its top 5 pulls. Nothing here claims a file was pulled if
it was not. Character art, character names (beyond the file identifiers
needed to cite a source), script dialogue, and logos are NOT reproduced
in this file. Systems only: poses, timing, layer structure, part
organisation, naming, pipeline method.

Scope (Mars, 2026-10-31): barred ONLY — (1) exact character likeness
image shipped as-is, (2) using a character literally, (3) character
name, (4) dialogue literally from a script, (5) brand image / logo.
Character images are transform-only production reference (parody or
wholly different character before release, never ship-as-is). Everything
else is pullable, including any type of move, not just dances.

## Count summary

- Pulls attempted: 5/5.
- Files fully parsed as XFL (DOMDocument + library XML): 2 (ch_max.fla,
  ch_ruby.fla).
- Files parsed at Contents-stream level (binary FLA, no XFL):
  2 (yyo_spl_act_flipflopfoo.fla, pds3hx.fla) — structure and part
  categories recovered, full timeline XML not available in this format.
- Archives fully listed by range reads / header walk, NOT downloaded
  in full: 3 (2024_Nick_Gigaleak.zip — 1,610 entries; Disney FLA RAR —
  12 entries; PPG_flas.rar — 1 entry).
- Archives NOT listed: 1 (nick.7z — see Pull 3, reason given).
- Wired systems with a concrete Cape Jones application: 6 (see below).
- Files claimed as rigs/dances that turned out NOT to be: 2 corrections
  (yyo is a game file, not a rig; PPG_flas.rar contains no .fla files).

## Pull 1 — Cartoon Vault unsorted .fla set

Source: `mhvnsnt/cn-gigaleak-cartoon-vault`, release `tv-gigaleak-fla-v1`.
Downloaded via GitHub release-asset API, sizes verified byte-exact
against the release listing. All three downloads verified.

### 1a. ch_max.fla — 57,402,049 bytes — PARSED (XFL)

- Format: ZIP-based XFL, Adobe Animate CC 15.1, XFL 2.7, stage
  1920×1080. Local-header walk: 671 library includes + DOMDocument.
- Stage timeline: `Scene 1`, 11 layers, single 46-frame hold (each
  layer 1 keyframe, duration 46). This is NOT a performed scene — it
  is a puppet build / pose-library sheet. Layers: one main comp layer,
  one folder layer, and 8 guide layers (pose-library placements, size
  refs, size lines, info/text slot, body reference). Guide layers hold
  dozens of pose-comp instances placed across the stage (crawl,
  tip-toe, sneak variants, rotation comp) — a model-sheet / pose
  library presented on stage, not a timeline performance.
- Library: 677 symbol XML files, 224 multi-keyframe (frame-addressed
  swap libraries) / 453 single-frame. Part folders, by part type only:
  arms, body, ears, eyes, feet, head, mouth, nose, shadow, tail,
  whiskers, plus props and expression folders and a rotation comp.
- View system: part variants for back view, front view, profile view,
  3/4-back, 3/4-front, plus side-left / side-right and close / far
  variants. Eye sample symbol: 8+ keyframes (frame-addressed
  expression/eye swap library).
- Show: NOT stated in any file parsed. The audit's instruction stands:
  do not guess a show from a filename prefix. No show is named here.
- What was NOT pulled: no character art, no pose images, no names
  from inside the symbols. The 46-frame stage hold contains no
  movement timing to pull — timing must come from the swap libraries,
  not this timeline.

WIRED SYSTEM 1 — Multi-view part-swap puppet + pose-library sheet.
Cape Jones application: (a) organise Cape Jones parts by view
(back/front/profile/3-4 + close/far) instead of a single view set;
(b) build a pose-library guide sheet (one stage, many pose comps
placed across it, guide layers only) for flex / fight / dance /
walk poses, so poses are picked from a sheet instead of rebuilt;
(c) convert Cape Jones eyes/mouth from separate files into
frame-addressed swap libraries inside one symbol each (the 8-frame
eye pattern is the template). Status: system wired as a design spec
in this file; Cape Jones parts themselves are unchanged (no files
rewritten in this task).

### 1b. ch_ruby.fla — 44,128,963 bytes — PARSED (XFL)

- Format: ZIP-based XFL, Adobe Animate CC 15.1, XFL 2.7, stage
  1920×1080. 175 library includes + DOMDocument.
- Stage timeline: `Scene 1`, 7 layers: Build (2 comp instances at
  scale 1.89999), Folder, a second puppet's reference layer, Ruby
  size-ref layer, Text, design, colour-card layer. All frames are
  single holds (no duration = hold). This is a puppet BUILD file, not
  a scene — the build layer holds the puppet, the other layers are
  reference only.
- Library: 175 symbol XML files, 134 multi-keyframe / 41 single-frame.
  Part folders, by part type only: arm (close/far), body, dots, ear
  (close/far), eye, eyewhite, foot (close/far), head, head comp,
  mouth, nose, pupil, skirt, tail, whisker (close/far), dress back,
  foot overlay, hand overlay, shadow, plus a full reference-template
  set for a second puppet (ears, whiskers, eyes, head, mouth, nose,
  tail, templates).
- Variant system: a night variant of the puppet (separate folder set)
  plus a reference-template set kept on its own layers — variant and
  reference are layered, not baked into the build.
- Show: NOT stated in any file parsed. No show is named here.
- What was NOT pulled: no character art, no reference-template images,
  no names from inside the symbols.

WIRED SYSTEM 2 — Build layer separated from reference layers +
variant-as-layer-set.
Cape Jones application: (a) keep Cape Jones build layers strictly
separate from reference layers (size refs, colour card, design,
text) — this matches and hardens the existing grey-128 control rule:
reference layers are never graded, rim-lit, or composited into a
final shot; (b) a night/dark variant of Cape Jones is a layer/palette
variant (LUT + rim family), NOT a second puppet — same build, variant
layers only. Status: design spec in this file; no Cape Jones files
rewritten in this task.

### 1c. yyo_spl_act_flipflopfoo.fla — 14,114,304 bytes — DOWNLOADED, FORMAT CORRECTED, NOT A RIG

- Format: NOT XFL. OLE Compound Document, Adobe Flash Windows 9.0
  build 494 (2008-era binary FLA). 772 directory entries, 771
  streams, Contents stream 396,570 bytes. The audit's XFL assumption
  does not apply to this file.
- Contents-stream strings show: `Scene 1`, `Page 1`, a game
  localisation class path, and game UI text-field identifiers. This
  is a FLASH GAME file (localisation / UI text system), not a
  character rig, not a scene, not a dance. Its filename segment
  suggesting a split/action does NOT prove animation content.
- What was NOT pulled: no game text, no UI strings, no dialogue,
  no art. No movement system exists in this file for Cape Jones.
- Correction to the audit: yyo is removed from the rig candidate
  list. It is a game-localisation file, not movement material.

WIRED SYSTEM: none from this file (0 systems). Recorded so it is not
re-pulled as a rig candidate.

## Pull 2 — Foster's Frankie rig (pds3hx.fla)

Source: `mhvnsnt/cn-gigaleak-fosters-home`, release
`frankie-rig-fla-v1`, asset `pds3hx.fla`, 18,385,408 bytes, downloaded
via GitHub release-asset API, size verified byte-exact.

- Format CORRECTION: NOT XFL, despite the audit's "XFL parseable"
  note. OLE Compound Document (binary FLA, pre-CS5 style), 608
  directory entries, 607 streams, Contents stream 284,161 bytes,
  Page 1 stream 7,701 bytes. No DOMDocument XML exists in this file,
  so the Charlie/Pim XFL layer-stack parse does not apply directly.
  What WAS recovered is the Contents-stream symbol index (2,294
  UTF-16 strings), which gives page structure, part categories, and
  view distribution — the same level of system information, by a
  different route.
- Page structure: 6 pages — turnaround, bodies, mouths, plus 3
  further pages (page names only, no content copied).
- Part symbols: 430 comp/part symbols. Part categories, by type only:
  head, hair / hair-back / fringe / spikes, eye, pupil, nose, mouth,
  chin, neck, body / torso / tummy, jacket / hood, skirt, shirt,
  arm left/right, upper/lower arm, forearm, hand, leg left/right,
  upper/lower leg, foot, shoe. 107 mouth-related strings.
- View distribution (from symbol-view tokens): 3/4 view 118, side
  view 82, 3/4-back view 30, front view 28, back view 16, plus
  jacket-specific views. This is a multi-view turnaround rig, not a
  single-view puppet.
- Expression system: chin comps and mouth comps in happy and sad
  variants, plus mouth-page organisation — an expression swap system
  built from chin + mouth comps together, not mouth alone.
- How it differs from the Charlie/Pim rigs (audit §28): Charlie/Pim
  are XFL master-symbol rigs with a single head comp, separate
  pupil/brow/lid symbols, and a 25-frame mouth library; this rig is
  a binary-FLA turnaround build with 6 pages, 430 part comps, and a
  chin + mouth expression pair. Same principle (part comps + swap
  libraries), different organisation (pages + turnaround views vs
  master symbol + head sub-symbols).
- What was NOT pulled: no part art, no turnaround images, no symbol
  names verbatim (part categories only), no dialogue, no logos.

WIRED SYSTEM 3 — Turnaround-page rig + chin + mouth expression pair.
Cape Jones application: (a) build Cape Jones turnaround as separate
pages (front / 3-4 / side / back / bodies / mouths) instead of one
flat sheet — this is the sheet structure for the owed viseme and
expression work; (b) expressions as chin + mouth comp pairs
(happy/sad as a starting pair), not mouth-only swaps; (c) the
viseme plan (0/14 owed) takes its page structure from this: one
mouths page, one comp per viseme, chin comp paired per expression.
Status: design spec in this file; no Cape Jones files rewritten in
this task.

## Pull 3 — Nick archives listing (range reads, NO full download)

### 3a. 2024_Nick_Gigaleak.zip — FULLY LISTED (central directory parsed)

Method: range-fetched the last 8,654,633 bytes of part-0041
(42 parts, 41 × 104,857,600 + 31,654,633), parsed the ZIP64 end
records, then parsed the full central directory in that tail:
1,610 entries, central directory 286,448 bytes. No other part was
downloaded.

- CORRECTION to the audit: this archive is NOT a multi-show Nick
  archive. All 1,610 entries sit under three top-level folders of a
  single show's material (counts: third folder 1,262, second 201,
  first 147). No other show appears in the listing.
- Rig files: 0 .fla, 0 .swf, 0 Toon Boom files. BUT a `RIGS/`
  directory exists with 12 rig entries: Maya `.ma` rigs (a character
  rig v041, a location rig v008, and prop rigs — noodle-arm, hands
  and feet, noodle-wrap (two versions), catcher prop) plus 4
  Alembic `.abc` caches covering frame ranges 1–182, 183–244,
  244–399, 400–586. These are 3D Maya rigs + baked caches, not 2D
  FLA rigs. They were listed only — no .ma or .abc file was
  downloaded or opened here.
- Movement-adjacent material listed (not pulled): pose-sheet PDFs
  (including season 1–2 pose sheets), storyboard PDFs, 17 PSD
  production-art files, 12 .mov / 19 .mp4 videos (including one
  dance video — video timing only, not a rig), 741 .wav + 287 .aif
  audio files, and script PDFs (scripts are NOT pullable as
  dialogue and were not opened).
- What was NOT pulled: no Maya files, no caches, no pose sheets, no
  videos, no audio, no scripts.

WIRED SYSTEM 4 — Prop-rig separation + noodle deformer + baked-cache
pipeline (Maya system, translated to Cape Jones 2D terms).
Cape Jones application: (a) rig props separately from the character
(cape as its own prop rig, not baked into the body rig); (b) a
noodle-arm / noodle-wrap deformer concept for squash-and-stretch
limbs and cape — a limb that bends along a curve rather than at a
single joint, which is the 2D equivalent of the listed prop rigs;
(c) a baked-cache step: once a clip is approved, bake it to a
cache (the clean clip re-render pipeline, 0/17 owed) instead of
re-posing every frame — the Alembic frame-range caches are the
template (cache per frame range, not per whole show). Status:
design spec in this file; no Maya file was opened, so no Maya
values are claimed.

### 3b. nick.7z — NOT LISTED (reason documented, not skipped silently)

Method attempted: range-fetched the first 1,048,576 bytes of
part-0000 and the final 40 bytes of part-0068 (69 parts total,
7,209,034,412 bytes concatenated).
- Signature valid (`7z` magic). Start header: next-header offset
  7,209,034,340, next-header size 40 bytes, located at the very end
  of part-0068.
- Those 40 bytes are a kEncodedHeader (0x17): the real file list is
  inside an LZMA-compressed packed header stream elsewhere in the
  archive. Listing it therefore requires a full 7z header parser
  (pack-stream location + LZMA decompression + header parse), not a
  simple range read — and no 7z tool is installed on this VM
  (`7z`/`7za`/`unar` all absent; Python `olefile`/`rarfile` do not
  cover 7z). A full download + 7z tool is the honest route; it was
  NOT done here, per the task's no-full-download rule for this pull.
- Contents: UNKNOWN. Do not claim any show, rig, or dance from
  nick.7z. It is the largest remaining unknown from the audit
  (7.21 GB).

WIRED SYSTEM: none from this file (0 systems). The Nick ZIP in 3a
is the Nick material actually listed; nick.7z remains unknown.

## Pull 4 — Disney .fla RAR listing (range reads + sparse header walk, NO full download)

Source: `mhvnsnt/cn-gigaleak-bonus-non-cn`, release `bonus-non-cn-v1`,
`DISNEY.LEAKS.and.wow.wubbsy.fla.rar` parts 0000–0007 (756,705,253
bytes concatenated).
Method: range-fetched 4,194,304 bytes of part-0000, then walked RAR5
headers by building a sparse file (real header bytes + zero holes
for file data) and fetching only 100–200 KB chunks at each next
header offset. Total data actually fetched: a few MB, not 757 MB.
Listing is COMPLETE: 11 files + 1 directory entry, ending at the
archive end block (offset 756,704,115 of 756,705,253).

Contents (folder prefix omitted; 12 entries total = 11 files +
1 directory entry):
- 2 video files (.mp4): 452,937,758 and 97,061,766 bytes unpacked.
- 7 PDF files: 22,988,330 / 154,490 / 278,715 / 187,058 / 274,161 /
  7,018,461 / 83,822,266 bytes unpacked.
- 1 ZIP file: 92,956,574 bytes, stored (not compressed) — contents
  unknown, not opened.
- 1 FLA file: `ww226_26s_016_final.fla`, 39,875,072 bytes unpacked,
  31,556,127 bytes compressed — the ONLY Disney-side rig/scene
  lead in the audit, confirmed by filename only. Its data was NOT
  downloaded and its content (scene vs rig vs background) is NOT
  known. Do not claim a dance, rig, or show from this name.
- The FLA and the ZIP are the only entries that could contain rig
  material; everything else is video or PDF reference.

WIRED SYSTEM 5 — Shot-code filename pattern (inferred from filename
pattern only, NOT from file content).
Cape Jones application: name Cape Jones shot files as
`show_scene_shot_final` (the listed FLA's pattern is
two-letter code + number + duration-ish code + shot number +
`_final`) so a shot's identity is in its filename and a `_final`
file is never overwritten — this matches the existing checkpoint /
version-lock rule (dated, versioned filenames, never overwrite a
version shown to Mars). Status: naming convention only; the FLA
itself is NOT wired, NOT parsed, NOT downloaded.

## Pull 5 — PPG_flas.rar listing (fully listed, name promise debunked)

Source: `mhvnsnt/cn-gigaleak-powerpuff-girls`, release
`home-hatch-backup-2026-10-14`, asset `PPG_flas.rar`, 38,268,928
bytes, downloaded via GitHub release-asset API (the public
browser-download URL returned 404; the API asset endpoint returned
the full 38,268,928 bytes, size verified).
Method: RAR5 header parse with the `rarfile` module (header-only,
no extraction — no unrar binary is installed).

- Contents: EXACTLY 1 entry — a ZIP file, 56,327,384 bytes
  unpacked, inside a folder whose name matches the archive's
  subject. No .fla file exists in this RAR.
- The contained ZIP's unpacked size (56,327,384 bytes) is identical
  to the size of the separately listed 10th-anniversary ZIP in the
  same repo. That is consistent with the RAR being a re-wrap of
  that ZIP, but it is NOT proven (the ZIP was not extracted and its
  central directory was not read). Treat it as a size-match hint,
  not a verified identity.
- Correction to the audit: the audit's "only PPG asset whose name
  promises rig files" does not deliver rig files. The promise was
  in the outer RAR's filename only; the contents are a ZIP whose
  name promises anniversary material, not FLAs.

WIRED SYSTEM: none from this file (0 systems). Recorded so it is not
re-pulled as a rig candidate.

## Wired systems — consolidated, with Cape Jones application

1. Multi-view part-swap puppet + pose-library sheet (ch_max).
   Application: Cape Jones parts by view + a guide-layer pose sheet.
2. Build layer separated from reference layers + variant-as-layer-set
   (ch_ruby). Application: build vs reference separation; night
   variant as LUT/rim variant, not a second puppet.
3. Turnaround-page rig + chin + mouth expression pair (pds3hx).
   Application: turnaround pages for visemes/expressions; chin +
   mouth comp pairs.
4. Prop-rig separation + noodle deformer + baked-cache pipeline
   (Nick ZIP RIGS/ listing). Application: cape as separate prop rig;
   noodle-bend limbs/cape; bake approved clips to caches.
5. Shot-code filename pattern (Disney RAR FLA filename pattern only).
   Application: `show_scene_shot_final` naming, never overwrite a
   shown version.
6. Pose-swap frame libraries as a general principle (ch_max eyes
   8+ frames; ch_ruby 134 multi-keyframe symbols; pds3hx mouth/chin
   comps). Application: Cape Jones eyes/mouth/expressions become
   frame-addressed libraries inside single symbols, replacing
   one-file-per-expression. (Counted as a cross-cutting system; the
   per-file systems above are 1–5.)

## What was NOT pulled, and why

- No character art, likeness, name (beyond file identifiers), script
  dialogue, or logo from any file — barred by scope.
- No .ma / .abc Maya files (Nick ZIP) — listed only, not downloaded.
- No Disney FLA data (`ww226_26s_016_final.fla`) — listed only; its
  31,556,127 compressed bytes were not fetched. Parsing it is the
  next pull if Mars wants it (fetch its data range + XFL/binary
  check, same method as Pull 1).
- No ZIP contents (Disney RAR's 92,956,574-byte ZIP; PPG RAR's
  56,327,384-byte ZIP) — listed only, not extracted.
- No nick.7z contents — compressed encoded header, needs a full 7z
  parser/tool + full download.
- No yyo game text or UI strings — game file, not movement material.
- No Cape Jones rig files were rewritten in this task. All six
  wired systems above are design specs recorded here, to be applied
  to Cape Jones parts/poses in the next build step. Claiming them
  as already built into the rig would be false.
- Source downloads used for parsing (4 .fla files, 134,030,724
  bytes total: 57,402,049 + 44,128,963 + 14,114,304 + 18,385,408)
  were worked on in `/tmp/wired-pulls/` and are not part of this
  deliverable; the parsed outputs are the counts and systems
  recorded above.
