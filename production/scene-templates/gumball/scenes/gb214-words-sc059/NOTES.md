# The Words — Sc059: Darwin's smug sway vs Masami's frozen smile (105 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc059` · SWF `GB214WORDS_Sc059_V001_clean_RR.swf` · 105 frames @ 25fps

## Story / beat
A locker-wall two-shot. Masami the cloud floats at upper left wearing one big frozen happy smile. Darwin slides in from the right edge (a sliver at f14–27), rises into frame looking anxious (f40), then performs a smug little routine in front of her — eyes-closed finger-up (f53), then a side-eyed sway with one finger raised and the other fin at his mouth (f66–92). Then he drops out of frame, and only in the final frame (105), alone in the shot, does Masami's smile finally collapse into a worried grimace. Her delayed reaction is the punchline.

## Cast
- **Darwin** — on the `dwn` layer (`GB200_DRW_ORIGINAL_PUPPET_v001`, 313 kf; face comps total 2,758 kf in the census). Entrance, grimace, smug sway, exit: all his.
- **Masami** — on the `masami` layer (`GB200_MASAMI_PUPPET_V002` family). Placed once, held in a single happy expression for ~90 frames, one expression change at the very end.

## Construction
- Layer stack: audio / framecounter / fieldguide / `masami` / `dwn` / white / background / `layout mov`. One keyframe per character layer at scene level — this is a two-placement scene.
- Background: one bitmap, `GB214_WORDS_SC059_LO_BG.jpg` — a tight locker-wall view (not the corridor wide), frames 0–105, no switches.
- The animation budget is entirely one-sided: Darwin's head comps (764 kf in the largest HEADCOMP instance) carry the shot; Masami's puppet has 118 kf available in the library but the shot uses essentially one held pose plus a final face swap.

## Techniques (tags + evidence)
- `face-comp-driven` (auto) — face comps hold 2,758 kf vs body puppets 502 kf.
- `layout-mov-reference` (auto) — scene carries a `layout mov` reference-video layer.
- `dialogue-two-shot` (manual) — exactly two character layers (`masami`, `dwn`), one puppet each, over the shared locker background; sheet frames 40–92 hold the two-character framing throughout.
- `photo-plate` (manual) — sheet shows a photographic locker wall (real doors, stickers, vents, scuffs) behind the vector puppets; judged from the render.

## What Cape Jones steals from this scene
- **Save the reaction for after the exit.** Masami's grimace means ten times more at frame 105, alone, than it would mid-routine. When a Cape Jones character delivers a devastating line/dance, hold the listener's face frozen and pay the reaction off in a one-frame-held final beat.
- **A held puppet is a legitimate scene partner.** One placement, one expression, zero scene-level keys — the cloud still reads as a character the whole shot because Darwin plays to her. Budget follows the performer.
- **Enter from the frame edge in slices.** Darwin's entrance is staged as sliver → rise → full pose across ~25 frames instead of a walk cycle: cheap, and it keeps the two-shot framing intact.

## Media status
- Contact sheet: done (105/105 frames rendered). Video: done, with production audio muxed from the SWF sound asset. See `media_status.json`.

## Gaps / honesty
- The contact sheet samples every ~13 frames; Darwin's sway between samples (the "twist" in the episode's dance) is inferred from the pose progression, not measured frame-by-frame. The choreography itself is documented in production/dance-choreo per the episode's dance extraction; this entry covers the scene's library anatomy.
- Masami's single-expression hold is verified at sample density — a brief intermediate face between samples can't be excluded, though her layer holds one placement and the samples are uniform.
