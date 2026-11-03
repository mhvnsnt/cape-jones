# The Words — Sc058: Darwin backview whip-turn close-up (17 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc058` · SWF `GB214WORDS_Sc058_V005_clean_ST.swf` · 17 frames @ 25fps

## Story / beat
A 17-frame punctuation shot. Darwin stands in the school hallway with his back to camera for the first ~5 frames — just the big orange back of his head filling the shot. He whips around grinning with his eyes shut (f7), throws an open-mouth reaction (f9–11), and settles into a pleased, blushing little smile with his fins spread (f13–17). No dialogue partner, no camera move: one turn, three facial beats.

## Cast
- **Darwin** — the only character, placed once at scene level on the `dwn` layer as `GB200_DRW_ORIGINAL_PUPPET_v001/GB200_DRW_PUPPET_BACKVIEW_v001/GB200_DARWIN_PUPPET_BACKVIEW_v001`. The whole performance is his: backview hold, turn, grin, reaction, smile.

## Construction
- Layer stack (top→bottom): audio / framecounter / fieldguide (guide) / `dwn` (the single puppet placement) / background. That is the entire scene — one character layer, one background layer.
- Background: a single bitmap, `GB214_WORDS_SC057_LO_BG_crop.jpg`, present frames 0–17 with no switches. It is a **crop of the Sc057 wide hallway plate** — the close-up reuses the wide shot's background instead of commissioning a new one.
- Face-comp use: the performance is carried by Darwin's head/face comps (`GB200_DRW_HEADCOMP`, `GB200_DRW_Mouth`, `GB200_DRW_EYECOMP`, plus `GB200_DRW_BACKVIEW_HEAD` for the opening). Census: 1,702 face-comp keyframes vs 271 body-puppet keyframes in the file's symbol library.
- No layout-mov layer in this file (unusual for this episode batch) — seams report `has_layout_mov_reference: false`; framecounter and fieldguide overlays are still present.

## Techniques (tags + evidence)
- `face-comp-driven` (auto) — face comps hold 1,702 kf vs body puppets 271 kf.
- `angle-variant-puppet` (manual) — the scene placement is a dedicated backview puppet, `GB200_DARWIN_PUPPET_BACKVIEW_v001` (36 kf), built for this exact camera angle; contact sheet frames 1–5 show only the back of his head.
- `solo-close-up` (manual) — Darwin's head fills most of the frame in all 9 sampled sheet frames; one scene layer, performance carried by face comps.
- `photo-plate` (manual) — the contact sheet shows a photographic school corridor (real red lockers, tiled floor with reflections, wall alarm) under the vector puppet; judged from the render, per the library rule for .jpg plates.

## What Cape Jones steals from this scene
- **The backview hold as a free anticipation beat.** Five frames of the back of a head costs one static angle-variant puppet and makes the turn land like a joke/reveal. Any Cape Jones reaction shot can open on a backview puppet instead of animating a turn.
- **Crop the wide plate for the close-up.** Sc058's background is literally Sc057's BG with `_crop` in the name. When a Cape Jones scene cuts from wide to close-up in the same location, crop the existing plate — same light, same perspective, zero new painting.
- **Three faces = a complete beat.** Grin → shock → blush-smile, all from the stock head-comp library. A 17-frame interstitial needs no new drawings if the face comps are deep enough.

## Media status
- Contact sheet: done (17/17 frames rendered). Video: done, with production audio muxed from the SWF sound asset. See `media_status.json`.

## Gaps / honesty
- The SWF's audio asset was exported and muxed, but the sheet alone can't say whether Darwin has a line, a gasp, or a musical sting in these 17 frames.
- Cast is Darwin only by both placement and the fixed builder; the library also carries the full-size `GB200_DRW_ORIGINAL_PUPPET_v001` (235 kf) as the parent of the backview nest — it is not separately placed at scene level.
