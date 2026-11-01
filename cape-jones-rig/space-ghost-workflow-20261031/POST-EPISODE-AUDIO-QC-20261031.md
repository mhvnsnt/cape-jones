# POST-EPISODE AUDIO PASS + DIALOGUE QC — Space Ghost Workflow, 2026-10-31

Order reminder: this whole document runs AFTER picture lock (Phase 3) and
AFTER Mars's dialogue-fill (Phase 4). Nothing here blocks Phases 1–3.
Approval 0/1 until Mars sees it. No ruling in this document is made — every
ruling slot is blank for Mars.

## A. Post-episode audio pass (Phase 5), step by step

Adapted from standard ADR/post-sync practice (SG-02, SG-03, SG-06):

1. **Spotting review.** Re-read the cue sheet against locked picture. Confirm
   every line has shot + timecode in/out + speaker + intent. A line without a
   timecode is not ready to mix.
2. **Take selection.** Per line, select the best take; keep alternates and the
   original guide/scratch (labelled SCRATCH) as fallback. Do not delete
   alternates — a rejected take is the fallback if the selected take fails QC.
3. **Sync edit.** Lay selected takes on a dedicated dialogue track. Slip-edit
   to lip beats; keep handles on each clip so a re-cut does not destroy the
   line. Match mic perspective / room tone to the shot's setting (room shots
   CJ-23..27 vs street/alley/rooftop) — studio-clean dialogue over a street
   shot without ambience matching will read as dubbed.
4. **Viseme/lip conform.** Confirm the viseme pass (SG-05) matches the
   SELECTED take, not the scratch. If the take changed after the viseme pass,
   re-run the viseme pass for that shot only.
5. **Music lay-in + tempo decision.** Apply Mars's tempo choice ONLY if one
   has been made (see §C). Until then, music stays scratch/silent and the
   mix is labelled TEMP-MIX, never final.
6. **SFX + stems.** Build dialogue / music / SFX stems separately. Keep the
   stems conformed to final picture timecode (SMPTE-style frame addressing:
   every stem clip carries shot + frame, so a re-conform can be checked).
7. **Mix.** Balance stems, verify −14 LUFS (standing delivery spec), deliver
   audio as a LINK, never in chat. No recorded audio is claimed by a cue ID
   alone (standing shot-spec rule).

## B. Post-episode dialogue QC (Phase 6, queue A)

Check every filled line; check silent-OK shots only for accidental scratch
audio left in (a scratch line shipped as final is a FAIL):

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
- [ ] Dialogue-primary shots checked first: CJ-26 (neutral/unsure) ☐,
      CJ-27 (shout/angry) ☐ — anger is viseme/pose, not a colour shift
      (per shot spec); the shout QC is on the line + viseme, not on the LUT.

Result per line: PASS / FIX (re-record or re-slip, then re-QC that line) /
PICTURE-CHANGE NOTE (line cannot fit locked slot → §6 exception path in the
main workflow doc). A FIX never silently re-cuts picture.

## C. Song tempo slot (Phase 5, music lay-in — Mars's choice, not made here)

- Song spec as supplied: C major, 152 BPM, 48 bars, 75.8 s.
- Visual dance grid on disk: ~107 BPM at 24 fps (beat ≈ 13–14 frames).
- Ratio ≈ 1.42×; full-song drift ≈ 31.9 s if played together unadjusted.
- Mars's options (from `mars-sweep-G-20261031/REPORT-20261031.md`):
  (a) Re-time AUDIO to ~107 BPM — song gets ~31.9 s longer; pitch/time
      artefacts and lyric timing are Mars's call.
  (b) Re-time VISUALS to 152 BPM — dance re-cut/re-posed faster; approved
      knee-feet correction + arm-snap work re-checked at the new speed.
  (c) Accept drift — song and visuals run at different tempos; beats fall
      out of sync over the song; acceptable ONLY if Mars says the drift is
      the intended feel, not a mistake.
- Chosen option (blank until Mars chooses): __________
- Banned until chosen: silently stretching either side, pitch-shifting the
  song to fake a match, or claiming a temp mix is a final song mix.
- Note: the visual phrase on disk is ~4.5 s, not the full 75.8 s song — the
  tempo decision matters when a full song video is cut, and the full-song
  cut is a Phase 5 task, not a Phase 1–3 blocker.

## D. Picture QC queue (Phase 6, queue B) — the CJ-05/06/26 rim rulings

Separate from dialogue QC. These travel with their shots from Phase 1 and are
ruled here, by Mars:

| Shot | Current spec value | Ruling owed | Mars ruling (blank) |
|---|---|---|---|
| CJ-05 punch across-down | Daylight, white rim [255,255,255], white bleed; "neutral exception: neutral key, white rim" — NOT the dual-light exception | Accept neutral/white here, or re-grade? | __________ |
| CJ-06 walk street contact | Daylight, white rim [255,255,255], white bleed; same neutral exception, NOT dual-light | Accept neutral/white here, or re-grade? | __________ |
| CJ-26 dialogue neutral/unsure | Natural window light, white rim [255,255,255], white bleed; near-B&W uncertainty shift, grey rim 240,240,240, hue N/A by design; NOT dual-light; JOJO-UNCERTAINTY demo-only | Accept grey/white here, or re-grade? (Plus queue A dialogue QC for its line, separately) | __________ |

A ruling that changes a rim = a re-grade pass on the same geometry (§6 step 4
of the main doc), followed by a re-run of queue B for that shot only. It is
not a re-animation and not a reason to re-open Phases 1–3 for other shots.

## E. Final mix QC (Phase 6, queue C)

- [ ] Stems balance: dialogue intelligible over music/SFX at −14 LUFS.
- [ ] No scratch audio in final mix (count 0, see §B).
- [ ] No silent-stretch artefacts (if tempo option (a) or (b) was applied,
      artefacts checked at the new speed, not assumed clean).
- [ ] Audio delivered as LINK; version-locked filename; approval 0/1 until
      Mars hears/sees the episode.
