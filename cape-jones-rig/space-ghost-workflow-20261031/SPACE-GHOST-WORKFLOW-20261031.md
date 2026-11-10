# SPACE GHOST WORKFLOW — Episode-First Pipeline for Cape Jones
## Workstream 9, TV Production Gap — 2026-10-31

**Order locked by Mars, 2026-10-31 22:01 CDT (standing):** build full episodes
FIRST — visuals / animation / shots end-to-end — and do NOT wait on dialogue,
song tempo choice, or dialogue QC. Mars fills dialogue where needed AFTER
episodes are done, THEN the audio pass, THEN QC on dialogue. This is the
Space Ghost Coast to Coast type workflow: picture first, dialogue after.

**Status: PIPELINE DOCUMENT ONLY. Approval 0/1 until Mars sees it.**
Nothing here is approved, landed, or pushed. No repo push was made by this
workstream. No dialogue, tempo, or QC ruling is decided here — those are
Mars's post-episode steps, and this document only reserves their slots.

**Scope:** Cape Jones 2D project, rig root `~/workspace/cape-jones-rig/`,
30 shots CJ-01..CJ-30 (specs: `clean-100-20261031/shots/shot-specs-30-20261031.md`).
This document does not overwrite any existing file and does not change any
standing rule (version-lock, image-cache, rim-color, dual-light, show-building
method). Where this document and a shot spec conflict, the shot spec's picture
values stand and the conflict goes to the post-episode QC gate — it does not
block the picture build.

---

## 1. What Space Ghost Coast to Coast actually did (public sources)

Space Ghost Coast to Coast (SGC2C, Cartoon Network, 1994–2004, plus later
revivals) was Cartoon Network's first original series and first animated
talk show, built by Mike Lazzo's Ghost Planet Industries (later Williams
Street Productions) on a low budget. Its production method, as documented in
public sources, was picture-first in the strongest sense:

1. **The picture already existed.** The show reused animation from the 1960s
   Hanna-Barbera *Space Ghost* series, which Cartoon Network already owned
   the rights to. The team re-edited that footage and traced over old frames
   rather than animating a new show from a script.
2. **The guest material was captured separately.** Celebrity guests were
   filmed separately, largely improvisationally, in front of a green screen
   (in New York / Los Angeles), talking to a producer or puppet — not in a
   scene with the animated characters.
3. **The edit created the meaning.** Back in Atlanta, editors chopped the
   guest footage up and re-cut the questions so answers landed out of their
   original context. The interview was assembled in the edit, not performed
   live in one take.
4. **New dialogue was laid over old mouths.** The reorganised footage was
   given crudely animated lips delivering the new dialogue. The mouth
   movement followed the new lines; the lines did not precede the animation.
   Continuity errors and sloppy, limited movement were part of the result
   and became the show's signature, not a defect to hide.
5. **Format, not story.** The show was a talk-show parody: host at a desk,
   bandleader (Zorak) and director (Moltar) as captive staff, guest appearing
   on a monitor screen beside the desk. Episodes ran roughly 12 minutes in
   the original run.

That is the exact inversion of the standard feature-animation method, in
which voices are recorded first and animation is timed to them (see §3,
method SG-12, marked INVERTED — documented so no workstream defaults to it).

Sources are listed with verbatim URLs in
`SOURCES-AND-METHODS-20261031.md`. No SGC2C character, name, script dialogue,
or logo is used in Cape Jones; only the production method is pulled, per the
standing show-building method (reference + transformation, barred list
unchanged).

## 2. The Cape Jones translation (one paragraph)

Cape Jones does not reuse Hanna-Barbera footage and has no live guest. What
transfers is the ORDER and the SEPARABILITY: (a) our own locked picture
library (v7c clean rig builds, walk / punch / flex / dance / flying clips)
plays the role SGC2C's existing footage played — picture that exists before
any new line is written; (b) Mars's dialogue plays the role of the separately
captured guest/host lines — recorded / written after picture lock, fitted to
slots the picture already defines; (c) the edit, not a re-shoot, is where a
line re-frames a shot; (d) the lip/viseme pass happens AFTER the line lands,
over the locked picture. If a line truly cannot fit a locked shot, the remedy
is the exception path in §6, not a silent rebuild of the episode.

## 3. Methods pulled — RUN vs MAPPING, each labelled

12 methods total: 8 RUN (8/12 = 67%), 3 MAPPING (3/12 = 25%),
1 INVERTED / NOT USED (1/12 = 8%). "RUN" means the industry method is used
as-is in this pipeline, with only Cape Jones names substituted.
"MAPPING" means the logic transfers but the source material differs, and the
exact reason is stated. Nothing below is a Mars decision.

| # | Method | RUN / MAPPING | Exact reason for the label |
|---|---|---|---|
| SG-01 | Picture lock before dialogue record (standard post-production: lock the edit, then record to it) | RUN | The step is identical: freeze shot order, holds, and durations, then fit dialogue to them. Only the project name changes. |
| SG-02 | ADR / post-sync / looping (actor re-records while watching locked picture; 3-beep / streamer cueing; multiple takes; best take selected) | RUN | Standard ADR definition and session shape apply unchanged to Mars's dialogue-fill session, watching CJ picture. |
| SG-03 | Spotting + cue sheet (dialogue editor marks every line: shot, timecode in/out, character, intent, breaths/lip beats) | RUN | The dialogue-fill template in this folder IS a cue sheet; fields are the industry fields, relabelled per shot (CJ-xx). |
| SG-04 | Scratch / temp / guide dialogue during edit (placeholder lines for timing only, replaced before delivery, never shipped as final) | RUN | Any placeholder line used while an episode is being cut is labelled SCRATCH in the template and must be replaced at Phase 4. Scratch is not Mars dialogue. |
| SG-05 | Lip / viseme pass AFTER dialogue (mouth shapes timed to the recorded line, last animation step) | RUN | Cape Jones already has a viseme plan (`MODEL-SHEET-VISEME-PLAN.md`); this method only fixes WHEN it runs — after the line, never before. |
| SG-06 | Stems + final mix after dialogue (dialogue stem, music stem, SFX stem; delivery −14 LUFS per standing delivery spec) | RUN | Stem structure and the −14 LUFS delivery target are already standing Cape Jones specs; this workflow only orders them after dialogue. |
| SG-07 | Dialogue QC after mix (sync check, intelligibility, lip-sync drift, continuity, alternate-take fallback kept) | RUN | Standard post-sync QC checklist, applied as a post-episode gate (see `POST-EPISODE-AUDIO-QC-20261031.md`). |
| SG-08 | Conform / re-conform as an exception (if a line forces a picture change, re-lock picture and re-QC everything downstream) | RUN | Standard conform discipline: a post-lock picture change is a named exception with a re-lock, never a quiet edit. |
| SG-09 | Repurposed-animation reuse (SGC2C: re-edit + trace 1960s footage) | MAPPING | Same picture-first logic, different library: Cape Jones reuses ONLY its own locked v7c builds and clips, never third-party footage — required by the show-building barred list (no shipped likeness / literal character). |
| SG-10 | Separately captured interview, re-cut in edit (SGC2C: guests filmed apart, questions re-cut so answers read differently) | MAPPING | Same separability logic, different separable element: there is no live guest in Cape Jones, so the separable element is Mars's line itself, which can re-frame a locked shot via line + cut order without re-shooting picture. |
| SG-11 | Talk-show desk format (host at desk, staff beside him, guest on a monitor) | MAPPING | Format borrowed as slot structure only, not as show identity: the Cape Jones room/desk block (CJ-23/24/25/26/27) provides host/desk beats and dialogue slots. Cape Jones is not claimed to BE a talk show. |
| SG-12 | Pre-lay dialogue-first animation (standard feature animation: record voices first, animate to them) | INVERTED — NOT USED | Documented explicitly so no workstream defaults to it. It is the normal animation order and it is the opposite of the order Mars locked for this workflow. If a future episode ever needs pre-lay, that needs a separate Mars order. |

## 4. Episode-first build order (the pipeline)

```
Phase 0  SHOT LIST + PICTURE SPEC   (already exists: 30 shot specs)
   ↓
Phase 1  PICTURE BUILD              (rig → pose → background → L2/L3 light
                                      → composite; clean builds, labels off)
   ↓
Phase 2  PICTURE EDIT / ASSEMBLY    (shot order, holds, loops; silent or
                                      scratch-guide cut only)
   ↓
Phase 3  ★ PICTURE LOCK ★           (gate: picture frozen; see §5)
   ↓
Phase 4  DIALOGUE-FILL (Mars)       (spotting → Mars lines → record →
                                      viseme/lip pass over locked picture)
   ↓
Phase 5  AUDIO PASS                 (stems, music lay-in incl. tempo
                                      decision, SFX, −14 LUFS mix)
   ↓
Phase 6  POST-EPISODE QC            (dialogue QC + picture QC incl.
                                      CJ-05/06/26 rim rulings + final mix QC)
   ↓
Phase 7  DELIVERY                   (version-locked filenames; audio as
                                      LINK, never in chat)
```

Phases 1–3 proceed with NO dialogue, NO tempo decision, and NO dialogue QC.
A workstream that stops Phase 1–3 to ask for a line, a tempo, or a QC ruling
is working against this locked order — record the item in its slot and keep
building picture.

## 5. Picture lock gate (Phase 3) — what "locked" means

Picture is locked for an episode when ALL of these are true (checklist in
`EPISODE-FIRST-CHECKLIST-20261031.md`):

1. Every shot in the episode has a clean build (labels off, 0 red label
   pixels per standing spec) under a new version-locked filename.
2. Shot order, per-shot hold/loop durations, and total runtime are written
   down in the episode cut sheet.
3. Backgrounds are named per shot; stand-ins are labelled STAND-IN, not
   presented as final painted backgrounds.
4. Lighting level (L2/L3), LUT, rim, and bleed are named per shot from the
   shot spec. A shot whose rim value is under a QC question (CJ-05, CJ-06,
   CJ-26 — see §7) still locks with its CURRENT rim value recorded; the
   question travels with the shot to Phase 6. It does not hold the lock.
5. No dialogue text is required for the lock. Dialogue slots exist as
   EMPTY, timed slots (shot + in/out timecode + speaker), not as lines.
6. The lock is dated and named (e.g. `EP01-picture-lock-20261031`). After
   the lock, any picture change uses the §6 exception path.

## 6. Exception path (the only way picture changes after lock)

1. Mars's line (Phase 4) or a QC finding (Phase 6) requires a picture
   change → file it as a PICTURE-CHANGE NOTE naming shot, frames, reason.
2. Change is made as a NEW version-locked file; the locked version is never
   overwritten.
3. Picture is RE-LOCKED under a new dated lock name; viseme, stems, and QC
   downstream of that shot are re-run.
4. If the change is only a grade/rim value (e.g. a CJ-05/06/26 ruling), it is
   a re-grade pass on the same geometry, not a re-animation.

## 7. How the three known open items slot in (NOT episode blockers)

These are the items Mars's 22:01 CDT order explicitly unblocked. Each rides
its post-episode slot; none holds Phases 1–3.

### 7a. Dialogue QC items CJ-05, CJ-06, CJ-26 — read carefully

These three QC flags are NOT dialogue items. They are rim-rule QC flags
from `gap-close-tv-20261031/qc-cj01-cj30-20261031.md`: CJ-05 and CJ-06
record a "neutral exception: neutral key, white rim" that is NOT the
dual-light exception and needs a ruling; CJ-26 records a near-black-and-white
uncertainty shift with a neutral grey rim (240,240,240), hue N/A by design,
also not the dual-light exception, also needing a ruling. The QC sheet
counts all three as FAIL until ruled.

In this workflow they slot as **post-episode PICTURE QC rulings by Mars**
(Phase 6, queue B — see the QC doc), travelling with their shots through
Phases 1–3 with current values intact:

- CJ-05 (punch across-down placement, daylight, white rim/bleed): builds and
  locks as specced. Ruling owed: is neutral-key/white-rim accepted here, or
  re-graded?
- CJ-06 (walk street contact, daylight, white rim/bleed): same — builds and
  locks as specced, ruling owed at Phase 6.
- CJ-26 (dialogue neutral/unsure, natural window light, white rim/bleed,
  JOJO-UNCERTAINTY demo-only shift): builds and locks as specced. Note CJ-26
  is ALSO a dialogue shot, so it carries two Phase 6 queues: its rim ruling
  (queue B) and its dialogue QC (queue A) once Mars's line lands. The two
  queues are separate and neither blocks the other.

No ruling is made here. A ruling that changes a rim is a re-grade pass
(§6 step 4), not an episode rebuild.

### 7b. Song tempo: 152 BPM vs ~107 BPM

Facts on disk (from `mars-sweep-G-20261031/REPORT-20261031.md` and
`dance-improved-20261031/BEAT-SHEET.md`; not re-decided here):

- Song spec as supplied: C major, 152 BPM, 48 bars, 75.8 s
  (48 × 4 = 192 beats; 192 / 152 × 60 = 75.79 s, 4/4 assumed).
- Visual dance grid on disk: ~107 BPM at 24 fps (beat ≈ 13–14 frames).
- Mismatch: 152 / 107 ≈ 1.42×. The same 192 beats at 107 BPM would take
  ~107.7 s, ~31.9 s longer than the song. Playing the 152 BPM song over
  ~107 BPM visuals drifts ~42%.
- The visual phrase on disk is only ~4.5 s, so this is a tempo-grid
  mismatch to resolve before a full song video is cut, not a claim that a
  4.5 s clip is 75.8 s long.

Post-episode slot (Phase 5, music lay-in): Mars chooses ONE of the three
options prepared in the sweep-G report — (a) re-time the AUDIO to ~107 BPM,
(b) re-time the VISUALS to 152 BPM, or (c) accept drift as the intended
feel. Until Mars chooses:

- Dance episodes build on the visual grid (~107 BPM) as picture.
- The song is NOT laid in as final; cuts are silent or scratch-guide only.
- Neither side is silently stretched, sped up, or pitch-shifted to fake a
  match. A silent stretch of either side to force sync is banned by this
  pipeline until Mars picks an option, because it would decide the tempo
  question by stealth.
- If option (b) is later chosen, the approved knee-feet correction and
  arm-snap work must be re-checked at the new speed (noted in sweep-G);
  that re-check is a Phase 5/6 task, not a reason to stop Phase 1–3 now.

### 7c. Dialogue itself, and dialogue QC generally

- Dialogue shots in the 30: CJ-26 (dialogue, neutral/unsure) and CJ-27
  (dialogue, shout/angry) are the dialogue-primary shots. All other shots
  carry optional, silent-OK dialogue slots — a shot without a line is a
  finished silent/visual beat, not an incomplete shot.
- Mars fills lines at Phase 4, after picture lock, watching locked picture
  (ADR method SG-02). Lines are recorded in the dialogue-fill template;
  the viseme pass follows the recording (SG-05).
- Dialogue QC (sync, intelligibility, lip drift, continuity) runs at
  Phase 6, after the audio pass — never as a precondition for building
  picture.

## 8. What other workstreams must do (handoff)

1. Build picture to the Phase 3 lock. Do not wait for lines, tempo, or
   rulings.
2. When a shot is picture-locked, open its row in
   `DIALOGUE-FILL-TEMPLATE-20261031.csv` (slot exists, line blank) and
   leave it blank for Mars — do not invent a line to "complete" the row.
3. Carry every open item (rim ruling, tempo option, unfilled slot) forward
   by shot ID into Phase 6. An item not carried forward is an item lost.
4. Use new dated filenames for every new version (version-lock +
   image-cache rules). Never overwrite a Mars-seen file.

## 9. What this workstream did NOT do

- Did not write, choose, or approve any dialogue line.
- Did not choose 152 BPM, ~107 BPM, or drift.
- Did not rule on CJ-05, CJ-06, or CJ-26 rim values.
- Did not push to any repo, change any account, or spend anything.
- Did not overwrite any existing file. All outputs are new files in
  `space-ghost-workflow-20261031/`.

## 10. Counts (percentage rule)

- Methods documented: 12/12 = 100% (8 RUN, 3 MAPPING, 1 INVERTED).
- Pipeline phases defined: 8/8 = 100% (Phases 0–7).
- Dialogue-fill slots templated: 30/30 shots = 100% (2 dialogue-primary,
  28 silent-OK optional slots).
- Mars decisions made here: 0/3 = 0% — dialogue, tempo, and QC rulings are
  all still owed to Mars, by design.
- Approval: 0/1. This pipeline is a proposal until Mars sees it.
