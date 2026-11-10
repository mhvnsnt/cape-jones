# Show-Repo Animation + Rig Audit — 100%
Date: 2026-10-31. Task: Mars, 2026-10-31 17:34 CDT.
Question: do the show repos hold rigs and SAVED animations, or only
model sheets / pose libraries / drag-built timelines with no saved file?
Scope (Mars standing): barred ONLY — exact likeness shipped as-is,
using a character literally, character name, dialogue literally from
a script, brand image/logo. Everything else pullable; character
material here is TRANSFORM-ONLY / placeholder reference, never shipped
as-is. No character art, names beyond file identifiers, dialogue, or
logos are reproduced in this file. Systems and counts only.

## Headline answer (read this first)

- **Teen Titans: NO rig, NO saved animation, in all three archives.**
  All three releases list out to model packs only (see table). There
  is no Teen Titans rig to get moving, because the show was made as
  traditional hand-drawn animation, not a Flash puppet show: the saved
  material is model sheets + expression sheets + colour callouts, not
  timelines. What moves in Teen Titans was drawn frame by frame; the
  repo holds the poses it was drawn FROM, not the animation itself.
- **"Drag-built vs saved" is a false split for Flash shows.** In
  Flash/Animate, dragging symbols onto a timeline and keying them IS
  how animation is built — and the .fla file SAVES that timeline.
  So Gumball, Foster's web reels, Smiling Friends, Randy Cunningham
  and the Cartoon Vault unsorted FLAs are BOTH drag-built AND saved:
  the FLA is the saved animation file. The real split is:
  (a) FLA timeline saved (Flash puppet shows) vs
  (b) NO timeline saved at all (hand-drawn shows: model sheets only,
  movement lives in finished video/animatics, if anywhere).
- **Saved-animation repos, verified by file evidence this task:**
  Gumball (62 + 71 FLAs, 53 + 54 SWFs), Foster's web reels (7 FLAs,
  15 SWFs, frame counts + 24 fps parsed from SWF headers this task),
  Randy Cunningham (6 FLAs, 4 SWFs, 1 After Effects project for a
  full scene), Smiling Friends (2 rig FLAs, scene timelines EMPTY —
  rigs only), Cartoon Vault unsorted (ch_max/ch_ruby = pose-library /
  build files, NOT performed scenes), Nick single-show archive
  (Maya .ma rigs + .abc baked caches = animation saved as cache,
  not as timeline), Disney FLA rar (1 FLA by filename only, content
  unknown), Rick & Morty Toon Boom files (present, cannot open here).
- **Everything else audited is model sheets / art / video / docs
  only — 0 .fla, 0 .swf, 0 rig files** (counts below, all from
  central-directory listings done this task by range reads, NOT
  guesses, NOT full downloads).
- **Motion proof delivered:** NO Teen Titans rig exists to move, so
  the moving proof is a retarget, labelled as such: Cape Jones pieces
  moving on a 24 fps timeline whose rate comes from the parsed
  Foster's SWF headers (24 fps, reels 1,618–2,190 frames). No donor
  art is in the proof. Files in this folder.

## Method (this task)
- GitHub API helper `~/workspace/cape-jones-rig-repo-batch/gh_api.py`
  (`req()`, no token printed/stored). Release-asset range reads
  (Accept: application/octet-stream + Range header) through the
  same credential — this is how split-ZIP central directories were
  listed WITHOUT downloading multi-GB archives in full.
- ZIP central-directory parse: EOCD (PK\x05\x06) → entry count,
  CD size/offset → per-entry name + sizes. ZIP64 EOCD used for MGM.
  Split-ZIP parts concatenated in name order; stray-part traps
  documented (Regular Show part-066, OKKO ab).
- SWF header parse: CWS (zlib) → RECT → frame rate (8.8 fixed) →
  frame count (UI16). Verified on all 15 Foster's SWFs.
- One Foster's FLA range-fetched and decompressed (Berry_v20.fla,
  6,981,106 compressed → 19,509,760 bytes, OLE binary FLA, NOT XFL)
  — confirms the reels' FLAs are binary-era files, not XFL.
- Prior verified work reused, not re-proven: deep audit (41 rows),
  wired pulls (ch_max/ch_ruby XFL parse, pds3hx binary parse, Nick
  ZIP 1,610-entry listing, Disney RAR 12-entry listing, Gumball
  Darwin dance JSON 198f Sc057 + 32-keyframe twist, Gumball RAR5
  2,259-file walk).

## Per-repo table
Columns: Rigs (Y/N + count + format) | Saved animations (Y/N +
count + format) | Drag-built vs saved | Pull method into free
stack (Tahoma2D 1.6.3 / Blender 5.2.3 / PIL / FFmpeg).

| Show / repo | Rigs | Saved animations | Drag vs saved | Pull method |
|---|---|---|---|---|
| Teen Titans — complete-v1 (970 entries) | N (0) | N (0) | Neither: model sheets only, no timeline ever saved in this archive | Pose/expression reference only: EPS model sheets (615 EPS, 33 AI, 29 JPG, 24 PSD, 33 PDF, 36 TIF). Render EPS via a free vector renderer (Ghostscript/Inkscape — NOT on VM, next step, not claimed). Eye/cape pulls are the usable pieces (see eyes v4). |
| Teen Titans — cnleaks-v1 (970 entries) | N (0) | N (0) | Same as complete — identical type counts, a repack of the same content | Same as above. |
| Teen Titans — cowchicken-v1 (1,139 entries) | N (0) | N (0) | Same file types + 169 extra dir entries, still 0 .fla/.swf | Same as above. |
| Gumball — S2 Rigs zip (132 entries) | Y — 62 .fla puppets + scene files (ORIGINAL_PUPPET versions, Carrie Ghost, Ocho, Tobias, Penny) | Y — 62 .fla + 53 .swf: KeyAnim scenes (GB202REMOTE Sc144/Sc147, GB218Flakers Sc002/Sc117) + fight scenes (DARWIN_HURT_BACK_KICK Sc159, GUMBALL_HURT_FACEKICK Sc155, HURT_FLOOR Sc160, HURT_HIMSELF Sc158/161) | Drag-built AND saved: XFL/Flash timelines, keyframed on stage | XFL parse (proven) → Tahoma2D xsheet/level, Blender retarget. Fight-move timing + puppet slot structure are the pull; Darwin dance (prior JSON) is the only verified dance. |
| Gumball — CN-Leaks-001 zip (876 entries) | Y — 71 .fla (same rig set + more) | Y — 71 .fla + 54 .swf, KeyAnim scenes incl. GB219WATCH Sc077/078/111, GB222Bumpkin Sc035 | Drag-built AND saved | Same as above. |
| Gumball — full RAR5 leak (2,259 files, prior walk) | Y — puppets v001–008 + Hector (prior) | Y — 20 dance FLAs, 10 unique Darwin dance scenes (prior) | Drag-built AND saved | Same as above. |
| Foster's Home — flash zip (61 entries) | N as a rig file in this zip (the Frankie rig is separate, below) | Y — 7 .fla + 15 .swf CN dot-com reels: Berry 1,847f, Bloo 2,190f, Cheese 1,892f, Coco 1,808f, Ivan 1,618f, Uncle Pockets 2,031f, Wilt 1,892f — ALL 24 fps (SWF headers parsed this task) | Drag-built AND saved: binary-era FLA timelines + SWF exports | SWF header timing (proven here) → retarget timing to Cape Jones (see motion proof). Full FLA timeline render needs Animate or a SWF renderer (Ruffle is the free route to try, NOT installed/claimed). |
| Foster's Home — Frankie rig pds3hx.fla (single asset) | Y — 1 binary FLA, 430 part comps, 6 pages, turnaround views (3/4: 118, side: 82, 3/4-back: 30, front: 28, back: 16), chin+mouth expression pair | N — rig only, no performed scene in this file | Rig built, not a scene | OLE Contents-stream symbol index (prior) → turnaround-page structure for Cape Jones visemes/expressions. |
| Smiling Friends (Cartoon Vault tv-gigaleak-fla-v1) | Y — 2 XFL FLAs: Charlie (82,390 B), PimRigUpdate (296,483 B), Animate 22, 1920×1080, master-symbol stacks, 25-frame mouth library, 10-frame leg library | N — scene timelines EMPTY (prior dissection) | Rig only; animation would be drag-built in Animate, but no saved scene exists here | XFL parse (proven) → frame-addressed swap libraries for Cape Jones eyes/mouth/legs. |
| Cartoon Vault unsorted — ch_max.fla (57.4 MB) | Y — 677 symbols, 224 multi-keyframe / 453 single-frame | N — stage = 46-frame HOLD, pose-library sheet (guide layers), not a performance | Build/pose sheet, not a scene | XFL parse (prior) → multi-view part-swap puppet + pose-library sheet system. |
| Cartoon Vault unsorted — ch_ruby.fla (44.1 MB) | Y — 175 symbols, 134 multi-keyframe | N — build file, all frames single holds | Build file, not a scene | XFL parse (prior) → build-vs-reference layer separation + variant-as-layer-set. |
| Cartoon Vault unsorted — yyo_spl_act_flipflopfoo.fla | N — Flash 9.0 binary GAME file (localisation/UI), NOT a rig | N | N/A | None. Removed from rig candidates (prior correction). |
| Cartoon Vault unsorted — other 7 FLAs (alien/earth/BOSS/BG/poster) | Format-level only, content unexamined | UNKNOWN | Unknown | Parse one at a time by XFL method; do not assume show from filename. |
| Randy Cunningham zip (19 entries) | Y — 6 .fla (ejq323, mi2y6f, pux9h5 88.8 MB, sercad, 0xmvez, dulzh3; ejq323 = 0xmvez duplicate by size/CRC) | Y — 4 .swf Flash exports (RC118_SC001 L02/L03/L05/L06) + 1 After Effects project (RC118_SC001_T1.aep) + BG .ai + report txt = a SAVED SCENE, layered for compositing | Drag-built AND saved, plus AE composite | XFL/binary check per FLA (next pull) → scene layer structure (Flash exports + BG + AE comp) is the template for Cape Jones scene assembly in Blender compositor. |
| Nick 2024 zip (1,610 entries, single show, prior) | Y — 8 Maya .ma rigs (character v041, location v008, noodle-arm/hands/feet/noodle-wrap/catcher props) | Y — 4 Alembic .abc caches (frames 1–182, 183–244, 244–399, 400–586) = animation saved as BAKED CACHE, not timeline | Baked-cache pipeline (3D) | Blender imports .abc natively (free route); .ma needs Maya or conversion. Also listed: pose-sheet + storyboard PDFs, 1 dance video (timing only), 1,028 audio files. |
| nick.7z (7.21 GB) | UNKNOWN | UNKNOWN | Unknown | Needs a full 7z header parser + LZMA + full download; no 7z tool on VM. NOT claimed empty, NOT claimed to hold rigs. |
| Disney FLA RAR (12 entries, prior) | 1 .fla by filename only: ww226_26s_016_final.fla (39.9 MB unpacked) | UNKNOWN (content not downloaded) | Unknown | Fetch its data range + XFL/binary check (clear next pull if Mars wants it). Rest: 2 MP4s, 7 PDFs, 1 stored ZIP (unknown). |
| PPG_flas.rar | N — contains 1 ZIP (56.3 MB), 0 .fla | N | N/A | Name promise debunked (prior). The inner ZIP size-matches the 10th-anniversary ZIP (hint, not proof). |
| Powerpuff Girls original zip (9,105 entries) | N (0 .fla/.swf) | N — 16 .mov QTVR turnarounds (pose reference, baked video) | Model sheets + QTVR only | EPS 7,397 + QTVR frame extraction via FFmpeg for pose reference. |
| Rick & Morty Toon Boom files (17.7 MB zip) | Files present (.tpl/.tvg) | Present but UNOPENABLE here | Saved (Toon Boom), blocked on tool | Needs Toon Boom trial (blocked on Mars's secure entry) — no free opener on VM. |
| Disney TVA (bibles + pilot MP4s) | N | N — pilot MP4s are finished video, catalogued not pulled | Video only | Bible architecture + pilot timing study only. |
| Scooby-Doo Mystery Inc. complete (95 individual assets) | N (0 .fla per inventory) | N — ep. 607 act D song animatic .mov (baked video timing only) | Video only | Animatic frame-by-frame timing; PSD backgrounds, model packs as reference. |
| Adventure Time — loose release | N | N — AT003 animatic .mov/.mp4 + notes PDF | Video only | Animatic timing. |
| Adventure Time — cnzip (18 parts, 8.59 GB) | UNKNOWN — no EOCD in last 70 KB of nominal last part (part_aq) | UNKNOWN | Unknown | Archive as held does not terminate with a central directory; do not claim rigs or emptiness. |
| Regular Show (67 zip parts, 6.83 GB) | UNKNOWN — no EOCD in last 70 KB of part-065 or part-066; part-066 is a stray chunk (8.26 MB) after the EOCD-bearing part-065's false-positive PK signature | UNKNOWN | Unknown | Same as above. 1 production PDF verified. |
| Foster's complete (8 parts, 3.40 GB) | UNKNOWN — no EOCD in last 70 KB of part-ah | UNKNOWN | Unknown | Same as above. Use the flash zip + Frankie rig instead (verified). |
| OK K.O. complete (2 parts, 1.02 GB) | UNKNOWN — no EOCD in last 70 KB of part-ab; both parts exactly 500 MB suggests truncation | UNKNOWN | Unknown | OKKO extract (123 PSD/JPG assets) is art only — verified separately. |
| Cow & Chicken zip (1,317 entries) | N (0 .fla/.swf) | N | Model/style-guide only | EPS 1,164 + style-guide structure. |
| Dexter's Lab zip (2,579 entries) | N (0) | N | Model packs only | EPS 1,803 + model-pack structure. |
| Duck Dodgers zip (454 entries) | N (0) | N | Model/style only | EPS 187, AI 50, PSD 35. |
| Ed, Edd n Eddy complete (1,905 entries) | N (0 .fla/.swf) | N | Model/art only | EPS 825, PSD 549. (Other Ed releases not listed: cnleaks 9 parts, gap-fill 24 + 12 parts — same content family, unlisted.) |
| Grim Adventures complete (1,777 entries) | N (0) | N | Art/bible only | PSD 969, EPS 459. |
| Johnny Test cowchicken zip (884 entries) | N (0 .fla/.swf) | N | Art/scripts only | JPG 348, PDF 118, AI 69. Scripts NOT pulled as dialogue. |
| KND complete (3,099 entries) | N (0 .fla/.swf) | N — 10 .mov QTVR turnarounds | Model/style + QTVR only | EPS 1,762, PSD 704, QTVR via FFmpeg. |
| Looney Tunes splits + singles | N (0) | N | Art/stills only | New Looney: 100 JPG; Looney Cartoons: 6 JPG + 6 PSD; ltc/lts splits unlisted (same family). |
| MGM Shorts (739 entries, ZIP64) | N (0) | N | Scans only | TIF 635. |
| Animaniacs zip (183 entries) | N (0) | N | Stills only | JPG 168, TIF 8. |
| Pink Panther zip (83 entries) | N (0) | N | Art/palette only | EPS 75. |
| Robot Chicken zip (171 entries) | N (0 .fla — stop-motion show; a "rig" here would be puppets/sets) | N | Physical puppets, no digital timeline | Style-guide + prop organisation only. |
| Space Ghost C2C zip (530 entries) | N (0) | N | Style-guide only | EPS 233. (Cape Jones is already the successor line — do not re-pull its identity material.) |
| Johnny Bravo (zip + 9 EPS) | N (evidence) | N | Model sheets/bible only | EPS + model-sheet structure; zip not listed. |
| Camp Lazlo / Samurai Jack / Primal / public-domain | N | N (films = finished video reference) | Docs/films only | Bible + episode-structure method; PD films for timing principles. |
| Bakugan / I Am Weasel | N — empty/placeholder repos | N | N/A | Nothing held. |

## Counts (this task + prior verified)
- Archives newly listed this task by central directory: 22
  (TT ×3, Cow&Chicken, KND, Grim, Johnny Test, PPG original,
  Dexter, Duck Dodgers, Robot Chicken, Space Ghost, Pink Panther,
  New Looney, Looney Cartoons, Randy, Animaniacs, MGM, EdEddEddy,
  Gumball S2, Gumball CN-Leaks-001, Foster's flash, Foster's SWF
  headers).
- Archives newly proven to hold 0 animation files: 17/22 = 77%.
- Archives newly proven to hold saved animation: 4/22 = 18%
  (Gumball ×2, Foster's flash, Randy) — plus prior: Smiling
  Friends rigs, ch_max/ch_ruby builds, Nick Maya caches, Disney
  FLA (filename only).
- Archives still UNKNOWN after this task: 5 (Regular Show,
  Foster's complete, AT cnzip, OKKO complete, nick.7z) + 7
  unexamined Cartoon Vault FLAs + Disney FLA content + Ed
  gap-fill/cnleaks parts + Looney splits + My Gym Partner batches.
  UNKNOWN means "archive as held does not terminate with a
  readable central directory" or "not listed" — never "empty".
- Saved-animation totals (verified, all repos): FLAs 62 + 71 +
  7 + 6 + 2 + 2 (ch_max/ch_ruby) + 1 (Frankie, rig) = 151 FLA
  files, of which performed-scene FLAs ≈ 62 + 71 + 7 + 4 (Randy
  scene exports are SWF) — rig/build FLAs are the rest. SWFs:
  53 + 54 + 15 + 4 = 126. Maya caches: 4. Toon Boom: 1 zip,
  unopened. These counts mix rigs and scenes; the table above
  separates them per repo — do not quote "151 animations".

## How to get a rig MOVING in our free stack (per format)
1. **XFL FLA (Gumball, Smiling Friends, ch_max/ch_ruby):** unzip
   the .fla → DOMDocument.xml (stage timeline: layers, frames,
   keyframes) + LIBRARY/*.xml (symbols) → convert keyframe
   transforms (x/y/scale/rotation, symbol swaps per frame) to a
   Tahoma2D level + xsheet, or to Blender (Grease Pencil / image
   planes) keyframes, or to PIL frame renders (this proof's method).
   Proven on ch_max/ch_ruby; Gumball scene FLAs use the same XFL
   2.7 structure — next pull is one Gumball KeyAnim FLA parsed
   end-to-end, not just listed.
2. **Binary FLA (Foster's reels, Frankie, possibly Randy):** OLE
   Compound Document → Contents stream → symbol index + scene
   strings (proven for pds3hx; Berry_v20 confirmed OLE this task).
   Full timeline render needs Animate or a SWF renderer; the
   SWF export already gives fps + frame count (proven here), and
   pose retargeting (this proof) works without rendering donor art.
3. **SWF exports:** header parse gives fps + frames (proven).
   Frame-by-frame render: Ruffle (free, open-source Flash player)
   is the route to try — NOT installed, NOT claimed working here.
4. **Maya .ma / .abc:** Blender imports .abc natively; .ma needs
   Maya or a converter — cache-first (use the .abc frames).
5. **EPS/AI model sheets (Teen Titans and all CN style packs):**
   these are POSE libraries, not motion. Motion comes from
   re-timing them: pick poses → order them on a beat grid (Gumball
   14f @25fps, Foster's 24fps) → hold/swap per frame in Tahoma2D
   or Blender. A free EPS renderer (Ghostscript/Inkscape) is the
   missing step for direct use — install it, do not hand-trace.
6. **QTVR .mov / animatic .mov/.mp4:** FFmpeg frame extraction →
   timing/pose reference only. No rig comes out of baked video.
7. **Toon Boom .tpl/.tvg:** no free opener on this VM; trial route
   is blocked on Mars's secure entry (separate task).

## Motion proof (this task, in this folder)
- `rig-motion-proof-24fps-20261031.gif` — 48 frames @24 fps
  (42 ms/frame), Cape Jones clean poses cycling walk-contact →
  walk-passing → walk-contact → walk-passing → dance → punch
  impact, 8 frames per pose. VIEWED (contact sheet + GIF).
- `rig-motion-proof-contact-20261031.png` — the 6 poses, viewed.
- `rig-motion-xsheet-24fps-20261031.csv` — frame, time, pose,
  timing source per frame.
- HONEST LIMITS: this is a RETARGET timing test, not a donor rig
  moving and not Teen Titans moving — because no Teen Titans rig
  exists in any of the three archives. Timing rate (24 fps) is
  real (parsed Foster's SWF headers); the poses are Cape Jones's
  own clean clips; no donor art, no donor character, no
  hand-drawn substitute. A full Gumball KeyAnim FLA parse +
  retarget (with its own keyframe transforms, not 8-frame holds)
  is the next motion step, not claimed here.

## Still owed (not claimed done)
- Teen Titans rig/motion: 0/1 — DOES NOT EXIST in the archives;
  the honest deliverable is the model-sheet pose library, not a
  rig. Do not keep searching the same three archives for a rig
  that is not there.
- Gumball KeyAnim FLA end-to-end parse + retarget: 0/1.
- Randy scene FLA check (XFL vs binary) + AE project structure: 0/1.
- Disney FLA ww226_26s_016_final.fla content: 0/1 (filename only).
- Ruffle SWF render test: 0/1 (not installed).
- Free EPS renderer install + Teen Titans expression-sheet render: 0/1.
- Unknown archives (Regular Show, Foster's complete, AT cnzip,
  OKKO complete, nick.7z): 0/5 listed — need their true last
  part / a 7z tool / full download, in that order.
- No repo push made in this task. No character shipped, placeholders only.
