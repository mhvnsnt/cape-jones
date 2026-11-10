# The Words — Sc062: Darwin's taunt-dance for a hallway audience (59 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc062` · SWF `GB214WORDS_Sc062_V010_clean_LB.swf` · 59 frames @ 25fps

## Story / beat
A wide hallway shot. Darwin performs in the middle of the corridor for four classmates who ring the frame and mostly just watch. Tobias (right) points and laughs the whole time. Darwin escalates: mock-horror pointing (f1), a smug lean (f8), a finger-up lecture pose (f15), a furious grimace-stomp (f23–30), a deep bow that shows the back of his head (f37), a delighted hop (f45) — and finishes in a full splits with a shocked face (f52–59), still holding it at the cut.

## Cast
- **Darwin** — the performer, centre, on the `dwn` layer (`GB200_DRW_ORIGINAL_PUPPET_v001`, 196 kf, plus head comps of 644/360 kf).
- **Tobias** — right, on his own `tobias` layer; his comp (`GB200_TOBIAS_ORIGINAL_P_COMP_V002`, 350 kf) nests 3 puppets and does the pointing/laughing.
- **Carmen** — the cactus, left, on the `carmen` layer; near-static witness.
- **Ocho** — the 8-bit spider, upper left by the lockers, on the `ocho` layer; near-static.
- **Carrie** — the ghost, floating upper right, on the `carrie` layer; near-static, facial reactions only.
- **Masami** — counted in the builder's cast from her puppet symbols in the file, but she never appears in the sampled frames (see Gaps).

## Construction
- One named scene layer per character (`dwn`, `carrie`, `tobias`, `carmen`, `ocho`) over a single background, plus audio / framecounter / fieldguide / white / `layout mov`. Nobody shares a layer; the staging is a diagram of the shot.
- Background: one bitmap, `GB214_WORDS_SC057_LO_BG.jpg` (the full Sc057 hallway plate — the same plate Sc058 crops for its close-up), frames 0–59, no switches. In the render it reads as a pale, washed photographic corridor.
- Animation budget is deliberately lopsided: Darwin's puppet + head comps carry the scene; the audience comps are small, and Carmen/Ocho/Carrie are effectively held poses with face changes.

## Techniques (tags + evidence)
- `nested-master-symbol` (auto) — Tobias's comp nests 3 puppets (350 kf); Darwin's performance is likewise comp-driven.
- `layout-mov-reference` (auto) — scene carries a `layout mov` reference-video layer.
- `multi-character-staging` (manual) — five characters visible simultaneously in every sheet frame, each on its own named scene layer over one shared background.
- `photo-plate` (manual) — sheet shows a photographic corridor (real lockers, ceiling-light perspective, floor reflections) under the vector puppets; judged from the render.

## What Cape Jones steals from this scene
- **Park the audience, animate the act.** Four reactors on four named layers, three of them near-static, still read as a crowd because one of them (Tobias) has a strong looping reaction. Cape Jones group scenes can afford one animated reactor per group, not five animated characters.
- **Escalation ladder inside one shot.** Smug → lecture → rage-stomp → bow → splits: five poses of rising absurdity with no cut and no camera move. A taunt or brag beat in Cape Jones can climb the same ladder by pose swaps alone.
- **The splits as a held final frame.** The last pose is the most extreme and it's simply held to the cut (f52–59) — let the audience sit in the gag instead of animating an exit.

## Media status
- Contact sheet: done (59/59 frames rendered). Video: done, with production audio muxed from the SWF sound asset. See `media_status.json`.

## Gaps / honesty
- **Masami discrepancy:** the builder counts Masami from puppet symbols present in the FLA (`GB200_MASAMI_PUPPET_V002` family), but she is not visible in any of the 9 contact-sheet samples and has no scene layer (unlike the other five, who each have a named layer). Her parts may be nested inside Tobias's comp as shared cloud-body pieces, or she may appear only between sampled frames. Reported as file-evidence only, not as a visible performer.
- The sheet can't tell whether Tobias's laughter is on the audio track as dialogue/SFX; the production audio is muxed into the staged video.
