# The Words — Sc056: Darwin performs on a ladder, nose-to-nose with the T-Rex (178 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc056` · SWF `GB214WORDS_Sc056_V021_Clean_STN.swf` · 178 frames @ 25fps

## Story / beat
The widest, strangest shot in this batch. A school hallway rendered pale and washed: a photorealistic T-Rex stands at right, a blue ladder centre, and a crowd of classmates (banana, one-eyed robot, an orange dome, a winged eyeball overhead) watches from the foreground. Almost all of that is the embedded layout/reference video (see Construction) — the actual Flash performance is Darwin on top of the ladder, playing directly to the dinosaur's face: cross-legged and serene (f23), standing tall and smug (f45), balancing arms-out (f67), crouched and singing with his eyes shut (f89–112). In the final third the Flash classmates switch on at full opacity around him — Tobias huge and laughing in the foreground, Masami smiling lower-left, Carrie annoyed upper-right, Ocho descending on a thread — while Darwin keeps performing on the ladder behind them.

## Cast
- **Darwin** — the performer; two `dwn` layers, both placing the master symbol `DRW_marche + lente` (426 kf; his puppet 235 kf, head comps 734/360 kf).
- **Tobias** — own `tobias` layer; foreground reactor in the final third.
- **Masami** — own `masami` layer; lower-left reactor in the final third.
- **Carrie** — own `carrie` layer; upper-right, annoyed, in the final third.
- **Ocho** — own `ocho` layer (5 scene keyframes, the most of any reactor); drops in on a thread in the final third.
- **The T-Rex and the foreground crowd** — present only in the `layout mov` reference video (a `DOMVideoInstance`); unnamed in the FLA and not Flash puppets, so this library describes rather than names them.

## Construction
- Layer stack: audio / framecounter / fieldguide (guide) / `dwn` ×2 / `tobias` / `masami` / `carrie` / `ocho` / white (DOMShape) / background / `layout mov` (DOMVideoInstance).
- Background bitmap: `GB214_WORDS_SC056_LO_BG.jpg`, one placement, no switches — but in the render it is largely covered by the reference video's own washed hallway.
- Darwin's ladder act is the same master symbol used in Sc055 (`DRW_marche + lente`), here placed twice on two layers — the episode's performances are re-placements of one nest, re-timed per scene.
- The reactors' late arrival is choreographed inside their comps (one scene keyframe each, except Ocho's 5): the scene timeline does not bring them in; their own timelines do.

## Techniques (tags + evidence)
- `nested-master-symbol` (auto) — `DRW_marche + lente` nests 10 puppets (426 kf) and carries Darwin's whole act.
- `layout-mov-reference` (auto) — the `layout mov` layer's element is a `DOMVideoInstance`; the T-Rex, ladder, crowd and much of the hallway in the render come from it.
- `multi-character-staging` (manual) — sheet frames 134–178 stage six-plus characters in one wide shot, the five Flash characters each on a named layer.
- No `photo-plate` tag: the photographic content here is the reference *video*, not the background bitmap, and the bitmap itself is too covered to judge from the render.

## What Cape Jones steals from this scene
- **Perform at the giant's face, on a ladder.** The scale gag needs no camera trick: put the small character on a prop that lifts him to the giant's eyeline and play the whole act there. A ladder, a stack of books, a shoulder — one prop sells a 10:1 size difference.
- **Reactors on a delay.** Four classmates contribute nothing for 110 frames and everything in the last 60: their arrival re-frames the shot and tells the audience the act is landing. In Cape Jones, hold the crowd out of a performance scene and bring them in only for the verdict.
- **Don't redraw another pipeline's character.** The T-Rex is a finished external render carried as reference; the Flash file spends its budget on timing, eyelines and the five puppets it owns. Mixed-media scenes should be built exactly this way.

## Media status
- Contact sheet: done (178/178 frames rendered). Video: done, with production audio muxed from the SWF sound asset. The washed look of both is what the SWF itself renders (layout-stage composite), not an export defect. See `media_status.json`.

## Gaps / honesty
- This is a layout-stage file: the final broadcast composite (full-opacity crowd, finished T-Rex render, colour timing) is not in this SWF, and this entry does not pretend otherwise. What it documents is the staging and timing method.
- The foreground crowd in the reference video (banana, robot, winged eyeball, orange dome) is described from the render only; the FLA gives them no names or symbols.
- Whether the two `dwn` placements are two segments of one performance or a duplicate for safety can't be distinguished from the anatomy alone; both place the same 426-kf master symbol.
