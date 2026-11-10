# AUDIO PASS SPEC + DIALOGUE QC CHECKLIST — EMPTY, NOT FILLED — 2026-11-01

Space Ghost workflow order: picture FIRST (Phases 1–3), Mars dialogue-fill (Phase 4),
audio pass (Phase 5), post-episode QC (Phase 6), delivery (Phase 7). This spec runs
ONLY after Mars fills dialogue. Nothing here is mixed, recorded, or approved.
Source spec carried forward (not overwritten):
cape-jones-rig/space-ghost-workflow-20261031/POST-EPISODE-AUDIO-QC-20261031.md
and cape-jones-rig/audio-cue-template.json (template only, no per-shot cue sheets built).

## 1. Delivery target — fixed

- Final mix loudness: **−14 LUFS** (standing delivery spec).
- Audio is delivered as a LINK, never in chat.
- A cue ID alone claims no recorded audio (standing shot-spec rule). Cue IDs
  CJ-A01 to CJ-A30 exist as IDs only; no recorded dialogue, music, or SFX is
  claimed by this batch.
- Final mix filename must be new and version-locked; never overwrite a
  Mars-heard version.

## 2. Audio pass (Phase 5) — steps, in order, all unstarted

1. Spotting review: re-read the cue sheet against locked picture. Every line
   needs shot + timecode in/out + speaker + intent. A line without a timecode
   is not ready to mix. Status: NOT STARTED.
2. Take selection: best take per line; alternates + guide/scratch kept as
   fallback, never deleted. Status: NOT STARTED.
3. Sync edit: selected takes on a dedicated dialogue track, slip-edited to
   lip beats, handles kept. Mic perspective / room tone matched to the shot's
   setting (room shots CJ-23 to CJ-27 vs street / alley / rooftop) — studio-clean
   dialogue over a street shot without ambience matching reads as dubbed.
   Status: NOT STARTED.
4. Viseme / lip conform: viseme pass must match the SELECTED take, not the
   scratch. If the take changed after the viseme pass, re-run the viseme pass
   for that shot only. Status: NOT STARTED.
5. Music lay-in + tempo decision: apply Mars's tempo choice ONLY if one has
   been made. Until then music stays scratch/silent and the mix is labelled
   TEMP-MIX, never final. Tempo options (post-episode, not a shot blocker):
   (a) re-time audio to ~107 BPM, (b) re-time visuals to 152 BPM, (c) accept
   drift as the intended feel. Chosen option: __________ (blank).
   Banned until chosen: silently stretching either side, pitch-shifting the
   song to fake a match, or claiming a temp mix is a final song mix.
   Song spec as supplied: C major, 152 BPM, 48 bars, 75.8 s. Visual dance grid:
   ~107 BPM at 24 fps (beat ≈ 13–14 frames). Ratio ≈ 1.42x.
   Status: NOT STARTED, option blank.
6. SFX + stems: dialogue / music / SFX stems built separately, conformed to
   final picture timecode (every stem clip carries shot + frame, so a
   re-conform can be checked). Status: NOT STARTED.
7. Mix: balance stems, verify −14 LUFS. Status: NOT STARTED.

## 3. Dialogue QC checklist (Phase 6, queue A) — EMPTY

Check every filled line; check silent-OK shots only for accidental scratch
audio left in. Result per line: PASS / FIX (re-record or re-slip, then re-QC
that line) / PICTURE-CHANGE NOTE (line cannot fit its locked slot — exception
path, never a silent re-cut of picture).

- [ ] Sync: line starts/ends inside its slot timecode; no line drifts into
      the next shot's slot.
- [ ] Lip sync: visemes match the selected take's phonemes, not the scratch;
      drift over a line is visible on the mouth, not just audible.
- [ ] Intelligibility: every word audible at mix level; no line buried under
      music/SFX (dialogue stem is the top priority in the mix hierarchy).
- [ ] Continuity: same speaker sounds like the same speaker across CJ-26
      and CJ-27; room tone is continuous across a cut, not jumping.
- [ ] No scratch shipped: search the timeline for SCRATCH-labelled clips;
      count must be 0 in a final mix (a temp mix may carry scratch, labelled).
- [ ] Fallback kept: alternates + guide retained with the episode, not deleted.
- [ ] Dialogue-primary shots checked first: CJ-26 (neutral/unsure) [ ],
      CJ-27 (shout/angry) [ ] — anger is viseme/pose, not a colour shift
      (per shot spec); the shout QC is on the line + viseme, not on the LUT.

Per-line QC results: NONE — 0/30 lines filled, so 0/30 lines QC'd, by design.

## 4. Picture QC queue (Phase 6, queue B) — separate from dialogue QC

- CJ-05, CJ-06, CJ-26 rim rulings: R1 APPROVED 1/1 (achromatic clause),
  QC 30/30 PASS. See open-picks-20261101.md for the one remaining CJ-26
  item: the rim NUMBER correction (255,255,255 vs 240,240,240), which is a
  paperwork correction under any ruling, not a new QC fail.
- A ruling that changes a rim = a re-grade pass on the same geometry,
  followed by a re-run of queue B for that shot only. Not a re-animation,
  not a reason to re-open Phases 1–3 for other shots.

## 5. Final mix QC (Phase 6, queue C) — EMPTY

- [ ] Stems balance: dialogue intelligible over music/SFX at −14 LUFS.
- [ ] No scratch audio in final mix (count 0, see §3).
- [ ] No silent-stretch artefacts (if tempo option (a) or (b) was applied,
      artefacts checked at the new speed, not assumed clean).
- [ ] Audio delivered as LINK; version-locked filename; approval 0/1 until
      Mars hears/sees the episode.

## 6. Counts

- Audio pass steps started: 0/7 = 0%.
- Dialogue QC lines checked: 0/30 = 0% (0/30 lines exist to check, by design).
- Final mix QC items checked: 0/4 = 0%.
- Mix loudness verified: NO — no mix exists yet to verify against −14 LUFS.
- Audio approval: 0/1.
