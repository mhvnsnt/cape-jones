# The Words — Sc057: the hallway dance — whole class advances on camera (198 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc057` · SWF `GB214WORDS_Sc057_V036_clean_MUI.swf` · 198 frames @ 25fps

## Story / beat
The episode's dance number, staged as one long advancing wide shot. Frame 1 is an almost empty corridor — just a tiny angry Darwin visible far down at the right-hand lockers. The class dances toward camera for the full 198 frames: by f26 the group is a distant cluster, by f99 Darwin is mid-frame doing a big grin pose next to Tobias, by f124 he's leg-up mid-dance, and the last third (f149–198) is foreground-size — crouch-shout, wide surprised squat, and a backview bend to close. Nobody cuts away; the approach *is* the shot. (Darwin's choreography itself is already extracted in production/dance-choreo; this entry is the scene's library anatomy.)

## Cast
Finished Flash puppets, each on its own named scene layer:
- **Darwin** — front and centre throughout (on `Layer 2` as a Duplicate Items copy of `GB200_DRW_ORIGINAL_PUPPET_v001`, 459 kf; head comps 566 kf). The dance lead.
- **Tobias** — `tobias` layer; his comp is the file's biggest nest (805 kf, 7 puppets inside). Dances at Darwin's side, ends foreground right.
- **Carmen** — `carmen` layer (`GB200_CARMEN_34_COMP`, 458 kf); left flank, arms up.
- **Masami** — `masami` layer; small cloud, left of frame.
- **Ocho** — `ocho` layer; the 8-bit spider, rides the left locker wall.
- **Carrie** — `carrie` layer (10 scene keyframes, the most scene-level keyframing of any dancer); ghost, right side, expressions shifting from flat to alarmed.

Plus the **white reference classmates** (see Construction): a huge T-Rex holding a balloon, a winged eyeball, a small toast-shaped figure and others — present as unfinished white placeholders, unnamed as symbols (`c2`–`c10`), so this library describes rather than names them.

## Construction
- Layer stack (24 layers): audio / framecounter / fieldguide / mask / Darwin (`Layer 2`) / tobias / carmen / masami / ocho / carrie / white (DOMShape) / a second mask / a `3d character ref` folder containing 7 layers placing items `c9, c6, c5, c2, c3, c7, c10` (7 keyframes each) / background / `layout mov` (DOMVideoInstance).
- The c-items are this file's stand-ins for the mixed-media classmates: fully timed and scaled with the group (7 keyframes each, growing with the approach) but rendered flat white — other departments' finished versions are not in this file.
- Background: one bitmap, `GB214_WORDS_SC057_LO_BG.jpg` — the master hallway plate for this whole sequence (Sc058 crops it, Sc062 uses it whole), frames 0–198, no switches. The "camera move" is entirely the cast scaling/advancing against this fixed plate.
- Two scene-level mask layers (auto-tagged `per-character-mask`) handle occlusion as dancers pass the corridor pillars at different depths.
- Census: 7,811 total keyframes across symbols — the largest file in this batch by a wide margin.

## Techniques (tags + evidence)
- `per-character-mask` (auto) — 2 mask layers at scene level.
- `nested-master-symbol` (auto) — Tobias's comp nests 7 puppets (805 kf).
- `layout-mov-reference` (auto) — `layout mov` layer present (DOMVideoInstance).
- `multi-character-staging` (manual) — six named puppets plus seven reference characters dance simultaneously in one wide shot for 198 frames; sheet frames 99–198 show the full ensemble at once.
- `photo-plate` (manual) — the photographic corridor (real lockers, ceiling lights, floor reflections) is visible in full for the entire shot; judged from the render.

## What Cape Jones steals from this scene
- **Fake the tracking shot by advancing the cast.** A fixed plate + a group that scales and steps toward camera reads as a dolly-in and costs no camera work at all. Any Cape Jones musical or parade beat can use the same trick: lock the BG, grow the ensemble.
- **Choreograph the placeholders with the finished cast.** The white c-item classmates are keyframed (7 keys each) in the same file, on the same beats, as the finished puppets — so when another department's version drops in, the dance still locks. Never leave the unfinished characters out of the timing pass.
- **Masks are what let a crowd pass architecture.** Two mask layers are the unglamorous reason the advance reads as depth instead of a slide show. Budget mask layers for any group-crossing shot.

## Media status
- Contact sheet: done (198/198 frames rendered). Video: done, with production audio muxed from the SWF sound asset. See `media_status.json`. (The render chain was interrupted twice by VM restarts during this scene's processing; the final pass completed from cached frames and verified 198/198.)

## Gaps / honesty
- The white c-item characters are placeholders: their finished mixed-media versions (photo/3D) are not in this FLA, and the staged video therefore shows them white. Identity of each c-item is not stated in the file (the T-Rex-with-balloon and winged eyeball are described from the render only).
- The approach is described from 9 sheet samples plus the layer keyframe counts (7 kf per ref layer, 10 on Carrie's layer, the rest inside comps); the exact scale curve per character lives inside the comps and is not measured here.
- Darwin's dance steps are deliberately not re-documented — they live in production/dance-choreo per the parent brief.
