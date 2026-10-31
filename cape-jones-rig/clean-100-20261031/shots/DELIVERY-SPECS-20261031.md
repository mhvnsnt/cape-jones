# Delivery specs — formal doc, clean-100, 2026-10-31

Status: formal delivery spec for the 30-shot set in this folder
(`shot-specs-30-20261031.json/.md`, `god-ray-placement-30-20261031.json/.md`).
It formalises rules already locked on 2026-10-31; it does NOT claim Mars
approval of any of the 30 shots. Every shot remains PENDING Mars looking
at the frames himself.

Companion (template, superseded by this doc where they conflict):
`~/workspace/cape-jones-rig/delivery-spec.md` (template only — it left
delivery frame size, safe areas and format approval open; those stay
open below until Mars sets them, and are not silently filled in here).

## 1. What a shot delivery is

A delivered shot = clean character plate + background + the lighting
level recorded in its spec + effects passes (where the spec calls for
them) + audio cue, each as separate, re-tunable passes where the
pipeline supports it (shadow / rim / bleed / volume / emission are
separate passes, not baked into base art). A composite with a missing
colour source, an unnamed second rim colour, a labelled plate, or an
overwritten Mars-seen filename is NOT a delivery — it is a draft, and
must be labelled as such.

## 2. Formats

- Frames: PNG frames, one new dated/versioned file per version
  (see §6). No frame is delivered by overwriting a previous version.
- Finish: MP4 finish. Pattern from TRIPPEDD practice: `scene.mp4` +
  a 9:16 variant when applicable. The 9:16 variant is produced only
  when the shot's framing supports it; it is not cropped blindly.
- Frame rate: 24 fps (rig default). Normal action on 2s = 12
  drawings/sec; fast snaps on 1s = 24/sec; holds 6–24 frames
  (per-shot timing in the shot specs).
- Character canvas: 1100×1500 (rig default). This is the CHARACTER
  canvas, NOT a delivery frame size.
- Delivery frame size: STILL TO BE SET by Mars. Do not present
  1100×1500 as the delivery frame size, and do not ship a “final”
  master until Mars sets frame size + safe areas. Safe areas are to
  be marked on layout passes first, then carried into delivery.
- Backgrounds: stand-in backgrounds (flying / rooftop / alley / desk)
  are NOT final painted backgrounds. A shot on a stand-in background
  is delivered as “on stand-in background” until its final painted
  background is built; the final painted background is a separate
  owed item, not something a grade can fake.

## 3. Colour / LUT / `.cube` delivery

- Approved LUT set: 70/70 (base 30 + spectrum 24 + spectrum v2 16,
  all approved by Mars 2026-10-31, final batch 15:17 CDT). Only a LUT
  from that approved set may be named in a shot spec. A new LUT needs
  its own Mars approval before use.
- Delivery form: the actual `.cube` file (33³), named in the shot
  spec (`lut_file`), applied with FFmpeg `lut3d` (or Blender/OCIO
  equivalent). A PIL Level-1 grade is NOT a LUT grade and must not
  be presented as one.
- Per-shot colour record (required, from `color-shot-spec-template.json`):
  LUT/grade, key colour + direction, rim colour, bleed colour, shadow
  colour, plus shift name (or none, with return-to-base), power name
  (or null — currently null in all 30 shots; no power is named, so no
  power override is active), and dual-light sources (or null).
  A spec missing a rim or missing a named source for a second colour
  is incomplete and must not render as final.
- Rim rule: rim follows key/LUT hue ±20°. Rim is the lighter,
  brighter version of that family; bleed is the darker, more
  saturated version of the same family; shadow stays cool
  blue-violet (the contrast exception). Dual-light exception ONLY
  when BOTH sources are named and the spec states which rim belongs
  to which source (CJ-19, CJ-30 in this set).
- JoJo / Dialect 2: JOJO-ATMOSPHERE palette is approved (Mars
  2026-10-31 15:36, environment-only, character stays base).
  JOJO-TENSION, JOJO-POWER and JOJO-UNCERTAINTY are DEMO-ONLY in
  this set — NOT canon until Mars approves each palette for canon
  use separately. Every shift records trigger/beat, scope
  (character / environment / both), palette name, and return to base.
  A shift with no trigger, no scope, or no return is a mistake, not
  a style. Opposition pairs (protagonist vs antagonist in
  complementary hues) require an antagonist plate, which is owed and
  is not claimed here.
- LUT judgement rule: a LUT MULTIPLIES what is already there, it
  does not paint over it. To judge a LUT alone, use a grey-128
  control (character on grey); to judge a shot, use character on
  its background. Room colour always shifts the result — never
  mistake room colour for LUT colour.
- Never recolour base art. Light, shadow, bleed, rim and god rays
  are separate layers on top of clean art. Bleed is edge-band only,
  never whole-suit tint. Rim is outer-only, 2–4px, never a thick
  inner outline.
- Lighting levels (Mars wording + industry term): L0 plate/raw
  (no lighting); L1 LUT only; L2 shadows + rim + bleed + key bleed,
  NO god rays; L3 god rays + rim + full effects; L4 FX/emission
  passes; L5 finishing/master. Coloured and non-coloured sets run
  in parallel (non-coloured = neutral grade, white rim/bleed, white
  god rays at L3, no hue introduced at L5).
- Level 2 v2 warm-rim is the approved Level 2 coloured version
  (Mars 2026-10-31 15:11 CDT, “perfect exactly”):
  `showcase/lighting-level2-v2/level-2-v2-colored-warm-rim-20261031.png`
  (warm amber rim 255,180,80, bleed 255,120,0, gain 1.10, 0.95, 0.70).
  Earlier cyan-rim v2 files are superseded for single-light shots.

## 4. Audio delivery — LINKS, never in chat

- Target: −14 LUFS for audio on the finished shot.
- Audio is delivered as a LINK, never as audio in chat. A cue ID
  in a shot spec (CJ-A01…CJ-A30) is a cue-sheet reference, not a
  claim that recorded audio exists.
- Link handling: every audio link is a new dated delivery; an
  expired link is re-issued as a new link, never re-presented as
  live. Demo/synthesised audio is labelled DEMO (synthesised tones,
  no recorded audio claimed) until real audio replaces it.
- Cue-sheet fields per shot: cue_id, shot_id, timecode, music, SFX,
  dialogue, viseme clip (where dialogue exists), loudness (−14 LUFS).
  Dialogue shots CJ-26/CJ-27 are spec-only until visemes (0/14
  sliced) + eye strips (0/8) exist — no dialogue audio is claimed
  for them here.

## 5. Labels — debug only

- Red numbered circles (ARM 1, ARM 2, LEG 1, LEG 2) are DEBUG TOOL
  pieces. They are NOT scene, NOT character, and are NEVER rim-lit,
  graded, composited, or given effects.
- Final shots, lighting passes, LUT grades, effects and composites
  use CLEAN builds only (`joint_locked_rig_v7c.py` with
  `labels=False`). Any plate with >100 pure-red label pixels is
  refused by the lighting script.
- White elbow/knee joint balls stay: they are character joints
  (circle-masked caps), not debug labels. Rim follows the character
  silhouette including those joints; it does not circle or highlight
  any red numbered label.
- Older labelled images are DEBUG ONLY, not final shots, and must
  not be used as shot plates.

## 6. Image cache / version-lock rules

- Every changed image gets a NEW dated/versioned filename. Never
  overwrite a file Mars has already seen — a rebuild shown under
  the same filename will display the cached old version (this
  happened with the warm-rim v2 rebuild on 2026-10-31 and is why
  this rule exists).
- Filename pattern for this set: `CJ-XX-<slug>-20261031-v1.png`
  (v2, v3… for later versions, each a new file). The version-locked
  filename is recorded in each shot's gate checklist.
- Superseded files are kept as checkpoints, not deleted (e.g. v1
  floating gauntlet version, labelled plates) — but a superseded
  file must never be selected for a final shot. “Kept” ≠ “usable”.
- No push, no delete, and no file move is authorised by this doc
  alone; moves/deletes need their own explicit instruction.

## 7. PR / merge verification — remote size + SHA, or it is NOT confirmed

- A local commit, a push receipt, or a PR number alone is NOT
  confirmation that work landed.
- Confirmation requires, AFTER merge: fetch the file from the
  remote (main branch, not the PR branch), and verify BOTH its size
  in bytes AND its SHA-256 against the local delivered file.
  Only a remote size + SHA match counts as “merged and verified”.
- If the remote file is missing, smaller/different-sized, or its
  SHA differs, the delivery is UNVERIFIED — report it as such,
  with the expected vs actual size/SHA, and do not claim the merge.
- Verification is recorded per file (filename, remote size, SHA-256,
  verification date/time), not as a blanket “PR merged” statement.

## 8. Approval gates (all must pass before a shot is called done)

1. Gate checklist in the shot spec: labels 0, base art untouched,
   version-locked filename, every colour source named, rim rule
   checked (hue ±20° or named dual-light exception).
2. Level gate: god rays only at Level 3 with a named source and
   rim ownership; Level 2 shots contain no god-ray layer.
3. Spec-only gates: CJ-15 (foreshortened forearm piece), CJ-18
   (true-flex wrist-seam fix), CJ-26/CJ-27 (visemes + eye strips),
   CJ-24/CJ-28/CJ-29/CJ-30 and flying shots (final painted
   backgrounds) must clear their owed item before the shot can
   leave “spec only” — the spec existing does not clear the gate.
4. JoJo gate: tension/power/uncertainty shots stay demo-only
   until Mars approves each palette for canon use; atmosphere
   shots use the approved palette but the shot itself still needs
   Mars's look.
5. Mars look gate: NO shot in this set is called done, approved,
   or final until Mars looks at its frames himself. QC status for
   all 30 shots in this delivery is PENDING.
6. Delivery gate: frame size + safe areas set by Mars (§2),
   LUT `.cube` delivered (§3), audio delivered as a link at
   −14 LUFS (§4), and PR verification by remote size + SHA (§7)
   where the delivery goes through a repo.

## 9. Still owed (not hidden by this doc)

- Mars look / approval on all 30 shots (0/30 claimed).
- Delivery frame size + safe areas (to be set by Mars).
- Final painted backgrounds: flying, rooftop, alley, desk.
- Foreshortened forward-flight forearm piece (CJ-15).
- True-flex wrist-seam fix (CJ-18).
- Visemes 0/14 + eye strips 0/8 (CJ-26, CJ-27).
- Blender volumetric god-ray production passes (PIL wedge
  numbers in the god-ray file are draft preview only).
- Canon approval of JOJO-TENSION, JOJO-POWER, JOJO-UNCERTAINTY
  (demo-only until approved each).
- Antagonist plate for any opposition pair (none claimed).
- Remote size + SHA verification for any repo delivery of
  this set (not yet performed — no push is made by this workstream).

## 10. Files in this delivery

- `shot-specs-30-20261031.json` + `shot-specs-30-20261031.md` — 30/30
- `god-ray-placement-30-20261031.json` + `god-ray-placement-30-20261031.md` — 30/30 decisions (9 god-ray, 21 Level-2 none)
- `DELIVERY-SPECS-20261031.md` — this file, 1/1
