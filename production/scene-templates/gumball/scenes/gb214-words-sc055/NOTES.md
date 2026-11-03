# The Words — Sc055: Darwin's pleading close-up, nested in one master symbol (94 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc055` · SWF `GB214WORDS_Sc055_V012_Clean_MB.swf` · 94 frames @ 25fps

## Story / beat
Darwin alone in the school corridor, in close-up, delivering an emotional plea/song straight ahead. He opens serene with his eyes closed (f1), turns worried and open-mouthed (f13–24), squeezes his eyes shut with his fins clasped like a singer at the big note (f36–47), grimaces anxiously (f59), pleads sidelong and sad (f71) — then falls straight out of frame: frame 82 catches only his green-shoed legs kicking up, and frame 94 is the empty hallway. The collapse is the punctuation at the end of the plea.

## Cast
- **Darwin** — the only character. He is never placed as a bare puppet at scene level: the `dwn` layer holds one instance of the master symbol `DRW_marche + lente`, and Darwin's parts (`GB200_DRW_HEADCOMP`, legs) are nested inside it.

## Construction
- Layer stack: audio (guide) / framecounter / fieldguide (guide) / `dwn` (one master-symbol placement) / background / `layout mov`. Every scene layer holds exactly one keyframe — the scene timeline is a shell.
- The performance lives inside `DRW_marche + lente` (303 kf, internal end frame 103). Inside it, face comps dominate: `GB200_DRW_HEADCOMP` 658 kf, `GB200_DRW_Mouth` 304 kf, eyes/eyebrows as separate small comps.
- Background: one bitmap, `GB214_WORDS_SC055_LO_BG.jpg`, frames 0–94, no switches. A photographic classroom corridor (doors, alarm bell, tiled pillar).
- Name-vs-content warning: the master symbol's name promises a slow walk ("marche + lente"); the rendered shot is a stationary close-up performance ending in a fall. The name is a reused nest, not a description of this scene.

## Techniques (tags + evidence)
- `nested-master-symbol` (auto) — `DRW_marche + lente` nests 2 puppets (303 kf) and is the scene's only character placement.
- `layout-mov-reference` (auto) — the scene carries a `layout mov` reference-video layer.
- `face-comp-driven` (manual) — inside the nest, HEADCOMP 658 kf + Mouth 304 kf vs the master's own 303 kf of body placement; sheet frames 1–71 are large facial changes on a near-static body.
- `solo-close-up` (manual) — Darwin's head fills most of the frame in sheet frames 1–71; single character layer.
- `photo-plate` (manual) — sheet shows a photographic corridor (real doors, alarm bell, ceiling lights) under the vector puppet; judged from the render.

## What Cape Jones steals from this scene
- **Build the shot as one nest, drop it in once.** A 94-frame emotional close-up with zero scene-level keyframing: all acting is edited inside the master symbol, so the scene file stays trivially clean and the same nest can be re-placed at another scale for the wide version.
- **End a plea by leaving the frame, not by cutting.** The fall out of frame (legs-up frame, then empty plate) is a full stop the audience feels. Cape Jones can end any begging/singing beat the same way: character drops, hold the empty background a few frames, cut.
- **Clasped fins + squeezed eyes = the "big note" pose.** The f36–47 pose reads instantly as heartfelt singing with no props and no body animation — a face-comp and hand-placement change only.

## Media status
- Contact sheet: done (94/94 frames rendered). Video: done, with production audio muxed from the SWF sound asset. See `media_status.json`.

## Gaps / honesty
- Whether Darwin is singing a specific lyric or pleading in dialogue can't be settled from the sheet alone; the SWF's production audio is muxed into the staged video for the parent to check.
- The pre-fix builder mislabelled this scene's cast (it attributed Darwin's DRW symbols to Gumball); the fixed builder and the render agree: Darwin only.
