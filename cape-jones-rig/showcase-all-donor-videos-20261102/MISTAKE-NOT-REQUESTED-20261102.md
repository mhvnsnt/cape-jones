# MISTAKE — NOT WHAT WAS REQUESTED — 2026-11-02

## Plain statement

These 49 showcase videos are SCHEMATIC-SHOWCASE sheet pans, NOT requested
original video clips, and they were shown by mistake.

- They are NOT original show playback.
- They are NOT Animate renders, NOT Harmony renders, and NOT assembled
  character animation.
- What each video actually does is pan, bob and zoom over a still, a rig
  sheet, a schematic, or a structure title card. That is showcase movement
  only.
- No new slideshows were made for this correction. No video was deleted,
  renamed on disk, or overwritten. Original filenames are kept exactly.
- The SCHEMATIC-SHOWCASE label lives in the new index file
  (INDEX-SCHEMATIC-SHOWCASE-20261102.json), not in renamed files.
- NOTE ON LOCAL PLACEMENT: writing this file into
  ~/workspace/cape-jones-rig/showcase-all-donor-videos-20261102/ was
  blocked by "Disk quota exceeded" (os error 122) at landing time, so
  this copy is staged at /tmp/taskA-staging/ and landed in the repo PR
  at cape-jones-rig/showcase-all-donor-videos-20261102/ alongside the
  videos. Copy it into the local folder once the quota block is cleared;
  do NOT delete anything to make room for it.

## Status

- Approval: 0/1 for all. Local only until the PR below lands; nothing here
  is approved, reskinned, or shipped.
- Every video is burned with: ACTUAL DONOR CHARACTER PLACEHOLDER -
  DO NOT SHIP AS-IS - RESKIN PENDING.
- No donor audio and no donor dialogue are used.
- Mars said on 2026-11-02 that this set was NOT what he asked for. This
  file records that correction so the set is never again presented as
  original clips.

## What they actually are, per group

### 1. SpongeBob rig sheets (workspace, landed in this PR)
- 01-spongebob-main.mp4, 02-spongebob-spongebob3.mp4,
  03-spongebob-pineapple.mp4, 04-spongebob-noodle02.mp4,
  05-spongebob-noodle03.mp4 — SpongeBob Maya/Blender-import rig sheets.
  A Cycles probe render of the main rig shows the meshes SCATTERED, not
  assembled into a posed character. Skinning/assembly is owed; no
  turntable of an assembled SpongeBob is claimed.
- 06-spongebob-noodlewrap.mp4, 07-spongebob-handsfeet.mp4,
  08-spongebob-squidcatcher.mp4 — Blender-import prop sheet pans
  (noodle wrap prop, hands-and-feet prop with partial parenting,
  squid catcher prop). Static props, not character clips.

### 2. Foster's blocked sheets (part workspace, part still pending in /tmp)
- 09-foster-frankie.mp4 (workspace) — BLOCKED sheet pan. Frankie is
  binary OLE; only 182/599 symbols were decoded as SVG pieces. No full
  render was faked.
- 10-foster-berry.mp4 (workspace) — BLOCKED sheet pan, binary OLE.
- 11-foster-bloo.mp4, 12-foster-cheese.mp4, 13-foster-coco.mp4,
  14-foster-ivan.mp4, 15-foster-wilt.mp4, 16-foster-pockets.mp4
  (still pending in /tmp, see below) — BLOCKED sheet pans, binary OLE.
  Uncle Pockets additionally FAILED to parse (incomplete OLE sector).

### 3. Gumball schematic (part workspace scenes, part still pending in /tmp)
- 17-gumball.mp4, 18-darwin.mp4 — XFL SCHEMATIC STILLS, not Animate
  renders (still pending in /tmp).
- 19-anais.mp4 — PARTIAL XFL schematic: head and arms present, legs
  mostly missing at frame 0 (still pending in /tmp).
- 20-dad.mp4 — XFL schematic still (still pending in /tmp).
- 21-mom.mp4 — PARTIAL XFL schematic: torso mostly white at frame 0
  (still pending in /tmp).
- 22-hector.mp4, 23-carrie.mp4, 24-penny.mp4, 25-tobias.mp4,
  26-ocho.mp4 — BLOCKED sheet pans, binary OLE (still pending in /tmp).
- 27-scene-darwin-dance.mp4, 28-scene-darwin-twist.mp4,
  29-scene-darwin-hurt.mp4, 30-scene-gumball-hurt.mp4 (workspace) —
  XFL SCENE schematic showcases, NOT original playback. Audio references
  are listed only, NOT used.

### 4. Rick / Morty structure title cards (workspace, landed in this PR)
- 45-rick.mp4, 46-morty.mp4, 47-beth.mp4, 48-jerry.mp4, 49-summer.mp4 —
  TOON BOOM STRUCTURE ONLY. Each video is a title/structure card built
  from template element, drawing-name and PEG counts (e.g. Rick: 66
  elements, 1,083 drawing names, 120 PEGs). NO Harmony render exists for
  any of them. These are the clearest example of the mistake: a structure
  card is not a clip.

### 5. Other groups in the same set (same mistake, same label)
- 31-scene-bossybear-021.mp4, 32-scene-bossybear-065.mp4,
  33-scene-bossybear-bg079.mp4, 34-scene-bossybear-bg001.mp4
  (workspace) — BossyBear XFL scene/BG schematic showcases.
- 35-scene-disney.mp4 (still pending in /tmp) — BLOCKED sheet pan,
  binary OLE. Character/show NOT identified; no name is claimed.
- 36-charlie.mp4 (workspace, current) — Smiling Friends Charlie XFL
  v3 still showcase. 36-charlie-OLD-v3.mp4 (workspace) is the previous
  v3 still showcase file, kept untouched.
- 37-pim.mp4 (still pending in /tmp) — Smiling Friends Pim XFL still
  showcase.
- 38-max.mp4 (still pending in /tmp) — Max & Ruby Max XFL rig showcase.
- 39-ruby.mp4 (still pending in /tmp) — Max & Ruby Ruby BUILD FILE
  ONLY. Ruby appears only as a size reference; this is NOT a standalone
  rig, and the video is not a Ruby clip.
- 40-ab112-alien.mp4, 41-ab112-earth.mp4 (still pending in /tmp) —
  AB112 lineup BLOCKED sheet pans, binary OLE, unidentified.
- 42-yyo.mp4 (still pending in /tmp) — BLOCKED sheet pan, binary OLE,
  unidentified.
- 43-dime.mp4 (still pending in /tmp) — DIME POSTER, not a rig.
- 44-randy.mp4 (still pending in /tmp) — Randy Cunningham SCENES ONLY.
  Characters exist as symbols inside scenes, not as standalone rigs.
- master-showcase-20261102.mp4 (still pending in /tmp) — a compilation
  reel of these same schematic showcases. It is likewise NOT original
  clips.

## Count, reconciled (so the "49" is not a mystery)

- Numbered slots 01–49 = 49 slots. Every slot is accounted for:
  24 slots sit in this workspace folder, 25 slots sit only in /tmp.
- This workspace folder actually holds 25 video files, not 24, because
  slot 36 appears twice: 36-charlie.mp4 (current, 125,220 bytes) and
  36-charlie-OLD-v3.mp4 (previous, 102,608 bytes). Both are kept.
- /tmp holds 26 video files, but /tmp/showcase_mp4s/36-charlie.mp4 is
  byte-identical to workspace 36-charlie-OLD-v3.mp4 (same SHA-256 and
  same git blob SHA), so it is a duplicate copy, not a 26th pending
  video. It was left intact in /tmp and was NOT copied over anything.
- Total distinct numbered showcase contents: 49. Total video files
  across both locations: 51 (25 workspace + 26 /tmp), of which one
  /tmp file duplicates a workspace file.
- The master reel is extra, on top of the 49: 1 file, 4,852,152 bytes.

## What was landed, and what is still pending

LANDED in this PR (25 workspace files, original filenames kept):
01-spongebob-main.mp4, 02-spongebob-spongebob3.mp4,
03-spongebob-pineapple.mp4, 04-spongebob-noodle02.mp4,
05-spongebob-noodle03.mp4, 06-spongebob-noodlewrap.mp4,
07-spongebob-handsfeet.mp4, 08-spongebob-squidcatcher.mp4,
09-foster-frankie.mp4, 10-foster-berry.mp4,
27-scene-darwin-dance.mp4, 28-scene-darwin-twist.mp4,
29-scene-darwin-hurt.mp4, 30-scene-gumball-hurt.mp4,
31-scene-bossybear-021.mp4, 32-scene-bossybear-065.mp4,
33-scene-bossybear-bg079.mp4, 34-scene-bossybear-bg001.mp4,
36-charlie-OLD-v3.mp4, 36-charlie.mp4,
45-rick.mp4, 46-morty.mp4, 47-beth.mp4, 48-jerry.mp4, 49-summer.mp4.

STILL PENDING — NOT copied, NOT deleted, /tmp copies left intact
(the workspace copy was blocked by "Disk quota exceeded" on every file,
including a 59,638-byte test file, even though `df` shows free space;
this is a quota block, not a free-space block):
- /tmp/showcase_mp4s/11-foster-bloo.mp4
- /tmp/showcase_mp4s/12-foster-cheese.mp4
- /tmp/showcase_mp4s/13-foster-coco.mp4
- /tmp/showcase_mp4s/14-foster-ivan.mp4
- /tmp/showcase_mp4s/15-foster-wilt.mp4
- /tmp/showcase_mp4s/16-foster-pockets.mp4
- /tmp/showcase_mp4s/17-gumball.mp4
- /tmp/showcase_mp4s/18-darwin.mp4
- /tmp/showcase_mp4s/19-anais.mp4
- /tmp/showcase_mp4s/20-dad.mp4
- /tmp/showcase_mp4s/21-mom.mp4
- /tmp/showcase_mp4s/22-hector.mp4
- /tmp/showcase_mp4s/23-carrie.mp4
- /tmp/showcase_mp4s/24-penny.mp4
- /tmp/showcase_mp4s/25-tobias.mp4
- /tmp/showcase_mp4s/26-ocho.mp4
- /tmp/showcase_mp4s/35-scene-disney.mp4
- /tmp/showcase_mp4s/37-pim.mp4
- /tmp/showcase_mp4s/38-max.mp4
- /tmp/showcase_mp4s/39-ruby.mp4
- /tmp/showcase_mp4s/40-ab112-alien.mp4
- /tmp/showcase_mp4s/41-ab112-earth.mp4
- /tmp/showcase_mp4s/42-yyo.mp4
- /tmp/showcase_mp4s/43-dime.mp4
- /tmp/showcase_mp4s/44-randy.mp4
- /tmp/master-showcase-20261102.mp4 (master reel)
- /tmp/showcase_mp4s/36-charlie.mp4 (duplicate of workspace
  36-charlie-OLD-v3.mp4; left intact, not counted as pending-new)

Pending count: 25 videos + 1 master reel = 26 files still only in /tmp
(plus the 1 duplicate /tmp charlie copy, also left intact).

## Sources for the descriptions above

- REPORT-20261102.md and INDEX-20261102.json in this folder (kept
  untouched; this file does NOT overwrite them).
- work/INDEX-chunkA.json, work/INDEX-chunkB.json,
  work/INDEX-chunkC.json (kept untouched).
- File sizes, SHA-256 and git blob SHAs in
  INDEX-SCHEMATIC-SHOWCASE-20261102.json were computed from the actual
  bytes on disk at landing time. One mid-task change was observed and
  is recorded honestly: workspace 36-charlie.mp4 was replaced during
  this task (previous bytes matched 36-charlie-OLD-v3.mp4; current
  bytes are 125,220 bytes, SHA-256
  98a5537a6326a520287d18bb2fefe17719ec055d6b0b1c7481f8329885ea28a2).
  The PR verifies against the bytes actually uploaded, not against
  any earlier listing.

## What must happen next

1. Do NOT present any file in this set as an original video clip.
2. Land the 25 pending /tmp videos + master reel only after the quota
   block is cleared, under the same SCHEMATIC-SHOWCASE label, via a
   separate PR-only landing with the same size+SHA verification.
3. The actually-requested original video clips, if they exist anywhere,
   are a separate job. Nothing in this folder substitutes for them.
