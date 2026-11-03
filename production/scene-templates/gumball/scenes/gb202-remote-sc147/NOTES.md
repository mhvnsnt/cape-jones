# GB202 "The Remote" — Sc147: family pile on the sidewalk, neighbour rants back (in-file cut)

**Cast (named, from the file):** the Watterson family as a group — Nicole, Gumball, Darwin and Richard are all evidenced by their face comps (GB200_GB_*, GB200_DRW_*, GB200_MOM_*, GB200_RICHARD_* head/mouth/eye/brow sets) nested inside the master symbol `animation` on the "family" layer — plus the neighbour, `CROWD_GUY_01_FV_COMP`, on the "neighbour" layer. (The builder emits a single grouped cast entry for the family nest; no scene-level puppets exist.)
**Shape:** 147 frames @ 25 fps · source `GB202REMOTE_Sc147_KeyAnim_V012_clean_WL_RTK.fla`
**Media:** contact sheet done + video done (production audio muxed from the SWF sound asset) — see media_status.json. Frames rendered from the video-stripped copy (see Gaps).

## Story / beat (from the contact sheet)
- Setup A (frames 1–~41): a washed photographic suburban street. Centre frame, small in shot: Richard lies reclined on the sidewalk while Nicole (tall, frame-left of the pile), Gumball (centre) and Darwin (right) cluster standing over him. The group barely moves — a held tableau with face-level micro-variation.
- The cut (~frame 42, background layer keyframe): a different photographic house front — white house, garage, black car in the drive.
- Setup B (frames ~42–147): the neighbour, a small round purple fellow with thin legs and yellow hands, stands alone mid-driveway, arms raised, mouth wide open in a sustained shout. He holds it for ~90 frames; by frames 129–147 the arms drop a little and the mouth closes down — the rant runs out of steam.

## Construction
- Scene layers are minimal: 'family' (holds `animation`, 2 kf), 'neighbour' (holds CROWD_GUY_01_FV_COMP, 2 kf), 'white' (a DOMShape layer), 'background' (LO bitmap, keyframed 0 and 42), plus framecounter/fieldguide/audio and the 'layout mov' video layer.
- Face-comp census: 929 face kf vs 0 body-puppet kf — the most extreme face-driven ratio in this batch, because every body is inside a nest.
- Both backgrounds render as photographic plates (pale/washed), the same Elmore suburb look as Sc154's street plate.
- The neighbour's comps (CROWD_GUY_01_FV_HEADCOMP 86 kf, MOUTHCOMP) give a stock crowd character a full solo performance.

## Techniques (tags + evidence)
- face-comp-driven (auto) — 929 face kf vs 0 body kf.
- layout-mov-reference (auto) — 'layout mov' video layer in file.
- photo-plate (manual, render-verified) — two photographic suburb plates.
- multi-character-staging (manual) — four-character family pile in setup A.

## What Cape Jones steals from this scene
Cut inside the file, not between files: one scene unit can carry a group tableau AND its reaction shot if the background layer takes the cut. And a stock crowd character, given a 100-frame hold and a mouth comp, can carry a whole second setup — Cape Jones's hallway neighbours never need bespoke rigs for a shouting cameo.

## Gaps / honesty
- Render path (the hard one of this batch): the original SWF (10.9 MB, embedded layout video = 148 video tags) rendered at ~1.5–2 frames/min under machine contention and the render script's 25-minute attempt cap could not reach 147 frames (attempt 1: 33 frames). Following the pipeline's wave-1 precedent, the video was stripped with tools/swf_strip_video.py (novid copy, 9.1 MB) and the frames were completed with two ranged FFDec exports using its -select option (frames 1–14 and 15–147, the second taking 31:44 alone, ~25 s/frame intrinsic to this heavy nested symbol). All 147 frames verified present, numbered 1–147, no gaps; sheet and video were then built by the standard render_scene.sh, with production audio exported from the original SWF. The original SWF is untouched in swfs/.
- The family members are identified from face-comp evidence and the render; Anais is NOT evidenced in the comps list and does not appear to be in the pile — she is not claimed.
- What either side is shouting about is not recoverable from the sheets; no transcript was made.
