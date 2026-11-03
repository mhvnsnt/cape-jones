# The Words — Sc063: Darwin leans on Carrie — her smile falls last (109 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc063` · SWF `GB214WORDS_Sc063_V016_Clean_MB.swf` · 109 frames @ 25fps

## Story / beat
A locker-wall two-shot in close-up. Carrie the ghost opens alone, calm and pleasant (f1). Darwin pops in from the left and leans his whole body against her, grinning (f15), performs at her — big singing mouth (f28), a startled O-face (f41) — and they trade laughs as they swap sides of the frame (f55–69). He grins his way out to the left in slices (f82–95). Alone again in the final frame (109), Carrie finally drops the pleasant face: mouth open, worried, little arms raised. Whatever he said has just landed.

## Cast
- **Darwin** — `GB200_DRW_ORIGINAL_PUPPET_v001` (445 kf; largest head comp 1,226 kf). The performer: lean, grin, song, startle, laughs, exit.
- **Carrie** — no scene layer of her own: her performance (`car head` 189 kf, `GB200_CARRIE_MOUTHCOMP_V002` 43 kf, Carrie eye comps) is nested inside the same placed puppet timeline as Darwin's. The listener whose final-frame reaction closes the scene.

## Construction
- Layer stack: audio / framecounter / fieldguide / `animation` (the single placement) / white / background / `layout mov`. One character layer total for a two-character scene.
- The placed puppet's internal timeline runs to frame 170 while the scene is 109 frames — the scene plays a segment of a longer nested performance, inside which both characters are choreographed, including their mid-shot position swap.
- Background: one bitmap, `GB214_WORDS_SC063_LO_BG.jpg` (pink locker wall), frames 0–109, no switches.
- Face census: 2,820 face-comp kf vs 445 body-puppet kf — the exchange is acted almost entirely with faces, fitting a shot where both characters are cropped at the shoulders.

## Techniques (tags + evidence)
- `face-comp-driven` (auto) — face comps 2,820 kf vs body puppets 445 kf.
- `layout-mov-reference` (auto) — scene carries a `layout mov` reference-video layer.
- `dialogue-two-shot` (manual) — sheet frames 15–95 hold both characters in one two-character framing, trading expressions; both performances nested in the single `animation`-layer placement.
- `photo-plate` (manual) — sheet shows a photographic locker wall (real doors, stickers, graffiti, vents) behind the vector puppets; judged from the render.

## What Cape Jones steals from this scene
- **Nest the pair, not the scene.** Two characters who touch, lean and swap places are easier to choreograph inside one symbol than across two scene layers — their contact points can never drift. Cape Jones two-handers with physical contact should be built as one nest placed once.
- **The private reaction as final frame.** Carrie's worried face exists for exactly the frames after Darwin leaves. Holding the listener's true reaction until they're alone turns a throwaway exchange into a story beat — and it costs one face swap.
- **Shoulders-up cropping makes face comps do everything.** With both characters cropped, the production spends nothing on bodies: 2,820 kf of faces against one puppet. Close two-shots are the cheapest scenes in the episode and among the most expressive.

## Media status
- Contact sheet: done (109/109 frames rendered). Video: done, with production audio muxed from the SWF sound asset. See `media_status.json`.

## Gaps / honesty
- The pre-fix builder labelled this scene's cast as Gumball alone; the fixed builder (Carrie + Darwin) matches the render exactly. Carrie's presence rests on her named comps inside the nest plus the sheet — she has no scene-level placement, which is itself the construction lesson.
- What Darwin says/sings to Carrie can't be settled from the sheet; production audio is muxed into the staged video.
