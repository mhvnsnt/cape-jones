# Eyes + Mouths — TV PRODUCTION READINESS, Workstream A sweep 2026-10-31

Focus per Mars 2026-10-31 20:53 CDT: what blocks episodes/segments vs what is
additive/extra. Shading library is saved; NO new shading presets were made in
this sweep. No repo push, no deletions, no force-push, no existing file
overwritten — this folder only. NOTHING here is claimed approved or landed;
landing is separate.

## What was built in THIS sweep (new folder only)

Builder: `build_production.py`. All pulled, nothing vector-drawn, nothing
invented. Run vs mapping labelled below.

### 1. Clean continuous front MBP — RESOLVED as a re-cut, approval 0/1
Old pahgo MBP-front-09 read as two segments because its patch included a
jaw-diagonal fragment at the right edge. Re-measured in box
(180,680,321,711) of `09_RBN01_CAMS_DCTTAS.png`: 3 dark components —
jaw-L 122px (touches edge), jaw-R 109px (touches edge), MOUTH 71px,
x213–246, y690–694, touches NO edge, 1 component = continuous.
New patch `mbp-clean-front-09_patch.png` is that mouth component alone,
verbatim pixels (34×5px), jaw fragments EXCLUDED and documented, not redrawn.
Fitted at the pahgo placement (target 231.5,504.5, alpha-bbox centre anchor,
alpha width normalised to 178px): scale 5.2353x, resized 178×26, alpha 3,301px.
Viewed: `mbp-old-vs-new-contact-20261031.png` — old = line + slanted second
segment; new = one continuous line at head scale.
Defect/caveat, NOT hidden: 5.24x upscale of a 34px source, so at 3x zoom the
line reads soft/stepped. It is a simple black stroke, so it reads clean at
head scale, but it is NOT crisp vector. Clean-continuity 1/1; resolution
is the remaining limit, not continuity.
Checked-and-NOT-used alternatives, so they are not re-proposed later:
- `00_Robin_1.png` mouth: single continuous line, but near-front (eyes
  asymmetric) and only ~25px wide — worse angle and worse resolution than 09.
- `15_RBN01_CAMSb_DCTTAS.png` (B&W front): SAME art as 09, identical dark
  count (109px) in the MBP box — not a separate cleaner source.

### 2. Longer test phrase — BUILT, fixed timing only, approval 0/1
`phrase-pah-go-see-pah-20261031.gif`: "PAH GO, SEE PAH", 48 frames @24fps
= 2.0s, 6 frames per viseme slot. Slots: MBP(new), AH(03), GK(05),
OH(GAP), SZ(GAP), EE(04), MBP(new), AH(03) = 6/8 pulled = 75%, 2/8 gap = 25%.
Viewed: `phrase-contact-20261031.png` (full heads, no mouth jump — single
target for every viseme) and `phrase-mouthzone-contact-20261031.png`
(gaps read as blank heads, slots 3 and 4).
Carried defects, NOT hidden: AH patch keeps a small jaw sliver at its right
edge; GK keeps small right-edge fragments; EE (04) keeps its small upper
mark from the source. All are pulled-source fragments, not new art.
Timing is FIXED 6f/viseme. It is NOT audio-driven (see blocker 1).

### 3. Robin-eyes gate re-run in this sweep
`robin-eyes-limits-broken-20261031/check_limits.py`: GATE PASS 9/9
(expression 10/10 sides, profile 1,760/1,760px, night gradient preserved).
No eye files were changed in this sweep; the gate result is a re-verification.

### 4. Archive re-count in this sweep (970 entries, tt-entries.json)
robin by name 61 + 2 RBNEXPRES files without "robin" in the name = 63 Robin
files (matches prior report); batman 0, superman 0, cyborg 65, starfire 61,
raven 63, beast 65, slade 16, justice 0, flash 0. Local disk: Robin raw 63
files; other-Titans source files 0 on local disk. All 40 local Robin renders
were checked in this sweep (contact sheet + head crops) for a front
MBP / front AH shout / front OH-OO — none found beyond the MBP re-cut above.

## PRODUCTION BLOCKERS — episodes/segments cannot ship dialogue without these

Primary blockers: 4 items; resolved pending approval 1/4 = 25%;
still blocking 3/4 = 75%.

1. Audio-driven lip-sync timing — 0/1, BLOCKING every dialogue segment.
   Current timing is fixed 6f/viseme. No Rhubarb binary on this VM
   (`which rhubarb` = none), no dialogue audio track: the only WAVs found
   are a 5.96s wired-audio mix and sound-demo mixes, not a dialogue phrase
   track. A dialogue recording + a timing run (Rhubarb or equivalent) is
   still owed before any segment can claim audio-synced lips.
2. OH/OO round front mouths — 0/2 shapes, BLOCKING any "oh/oo" word.
   0 in the 40 Robin renders checked. In the phrase proof the OH slot is a
   blank head. EH (03) was NOT duplicated to paper over OH.
3. Front AH shout WITH teeth — 0/1, BLOCKING loud/shout dialogue.
   The only shout with teeth (01, 51_RBEXPRES01) is 3/4, not front.
   Front AH (03) is an open smile: tongue, no upper teeth, softer read.
   Trading angle for intensity is a real cost, stated plainly.
4. Clean front MBP — RESOLVED in this sweep as a re-cut (above), approval
   0/1. Was fragmented; now 1 component, fitted and viewed. Remaining limit
   is the 5.24x upscale softness, not continuity.

Lip-sync chart, 14 visemes (visemes-v2 set: rest, EE, EH, AH, OH, OO, MBP,
FV, L, SZ, TH, R, W, GK):
- Clean front pulled: 5/14 = 36% (MBP-new, EE-04, EH-03, GK-05, rest via MBP)
- Partial front pulled: 1/14 = 7% (AH via 03 smile, wrong intensity/no teeth)
- Gap, no true front shape: 8/14 = 57% (OH, OO, FV, L, SZ, TH, R, W)
- Distinct pulled front mouth shapes behind those slots: 4 (MBP-new, 03, 04, 05)

## EYES — production position
- Front neutral refit: APPROVED PERFECT 1/1 (Mars, prior — not a new claim).
- Limits-broken: 2/3 fully broken = 67% (L1 expression masks, L2 profile);
  1/3 partially broken = 33% (L3 detail — night gradient preserved, pupil
  impossible from this library, NOT claimed broken).
- Expression eyes: masks differ from neutral 10/10 sides = 100%, BUT redrawn
  black outlines around the new masks are 0/1. BLOCKER only if an episode
  needs expression eyes as finals; neutral-only episodes are NOT blocked.
- Profile: near eye filled 1/1 = 100%, ready for profile shots. Far-eye
  fragment (41px) left as original art — additive, not a blocker (a profile
  shot needs the near eye).
- Detail/pupil: pupil-bearing pulled source 0/1, but NOT a blocker for
  Robin mask eyes — the source eyes contain no pupil by design (dark
  interior px = 0 in 23/25 library entries). It is an additive for
  pupil-bearing characters, not a Robin-episode blocker.
- 3/4 depth proxy: near eye 108/108px, far eye depth-shrunk 0.85 to
  78/105px = 74% — ready as a labelled proxy, not a true profile.

## ADDITIVES / EXTRAS — do NOT block Cape Jones episodes
- Other-Titans mouths: extracted 0/5 characters = 0% (Cyborg 65, Starfire 61,
  Raven 63, Beast Boy 65, Slade 16 are ARCHIVE COUNTS, not extractions).
  Extracting them is a new pull from repo mhvnsnt/cn-gigaleak-teen-titans
  (release teen-titans-complete-v1, verified by name count in this sweep);
  no other-Titans file exists on local disk. Additive — different characters.
- Batman mouth: 0 in the 970-entry set. Superman mouth: 0 in the set.
  Together 0/2 characters = 0%. Web search 2026-10-31 found NO verified
  downloadable Batman/Superman mouth file in hand (generic lip-sync
  articles, a Batman art book PDF, a model-sheet gallery page — none
  verified as a mouth-chart file). NOTHING was pulled from an auction
  listing, nothing invented, nothing vector-claimed as pulled. Additive /
  separate-character gap, not a Cape episode blocker.
- Shading presets: 0 new in this sweep, by the focus instruction (library
  already saved).
- Longer phrase GIF: a test/additive (above), not production audio.

## Still owed (every unfinished list, with percentages)
- New MBP-clean approval: 0/1. Phrase-proof approval: 0/1.
  Limits-broken new-work approval: 0/1 (refit itself is already approved).
- Audio-driven timing: 0/1. Front AH shout with teeth: 0/1.
  OH/OO round front: 0/2 shapes = 0%.
- Full lip-sync gaps: 8/14 visemes = 57% (OH, OO, FV, L, SZ, TH, R, W).
- Expression-eye black-outline redraw: 0/1 (only if expression finals wanted).
- Pupil-bearing source: 0/1 (additive, not a Robin blocker).
- Other-Titans extractions: 0/5 = 0%. Batman/Superman mouths: 0/2 = 0%.
- Wiring pulled mouths into the main lip-sync builder as the default chart:
  0/1 — the phrase here is a standalone proof using the pahgo placement
  method, not yet the builder default.
- No repo push made; landing is a separate step, not claimed.

## Methods: run vs mapping (honest labels)
RUN in this sweep: connected-component mouth isolation (09 mouth component);
alpha-bbox centre-anchor placement; head-width proportional scale;
gate re-run (9/9); archive name-count audit; contact-sheet render audit
(40/40 renders); fixed-timing phrase assembly.
MAPPING (not run, no model/binary on this VM): Rhubarb Lip Sync
audio-driven timing; MediaPipe Face Mesh mouth ROI (tight cut is its manual
equivalent); SAM-style segmentation (threshold+components is the manual
equivalent used here). No vendor software run is claimed.

## Files in eyes-mouths-production-20261031/
- build_production.py, measurements-20261031.json
- mbp-clean-front-09_patch.png (34x5, 71px, 1 component)
- fitted/ — MBP-new, MBP-OLD-fragmented, AH, GK, EE on Cape head
- phrase-pah-go-see-pah-20261031.gif (48f @24fps, 2.0s), frames/ (48 PNGs)
- mbp-old-vs-new-contact-20261031.png, phrase-contact-20261031.png,
  phrase-mouthzone-contact-20261031.png (all viewed in this sweep)
- PRODUCTION-READINESS-20261031.md (this file)
