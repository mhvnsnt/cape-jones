# GB214 "The Words" — Sc054: Darwin's hallway solo (one symbol, borrowed photo plate)

**Cast (named, from the file):** Darwin only — master symbol `DRW_marche + lente` on layer "dwn"; face comps `GB200_DRW_HEADCOMP` (1,083 kf), `GB200_DRW_Mouth`, head/eye/brow comp set. No other character appears in symbol, layer or comp evidence.
**Shape:** 229 frames @ 25 fps · source `GB214WORDS_Sc054_V011_Clean_STN.fla`
**Media:** contact sheet done + video done (production audio muxed from the SWF sound asset) — see media_status.json. Rendered from the video-stripped copy `GB214WORDS_Sc054_novid.swf` (see Gaps).

## Story / beat (from the contact sheet)
- Frame 1: empty photographic school hallway, long perspective, washed pale.
- ~Frame 29: Darwin peeks from behind a pillar at frame-right, gritted and annoyed — clipped by the pillar.
- Frame 58: out in the corridor, eyes closed, hands clasped, smug — mid-song sway.
- Frame 87: crossed to centre-left, eyes shut, mouth wide — belting it out.
- Frames 115–172: the tour turns — a wide-legged worried stance (115), pleading look upward at frame-right (143), annoyed explaining with a pointing fin at frame-left (172).
- Frame 201: he steps toward camera — suddenly large, worried, fins raised.
- Frame 229: frame-filling close-up, eyes closed, blissful, hands clasped at his chest. Hold on that.

## Construction
- One character layer ("dwn", 21 keyframes) holding one master symbol, `DRW_marche + lente` (775 kf; French production naming: marche = walk, lente = slow). Everything else is overlays: 'perspective' guide, framecounter, fieldguide, a 'white' shape layer, the background, and the 'layout mov' video layer.
- Occlusion: a mask layer ('Layer 5', DOMShape) — Darwin's pillar peek is a mask solve.
- Background: bitmap `GB110FIGHT_SC143_crop.jpg` — a cropped background from GB110 "The Fight" (season 1) doing duty as this scene's hallway; in the render it is a genuine photographic corridor, pale-washed.
- The face system dwarfs everything: DRW_HEADCOMP alone holds 1,083 of the scene's 2,547 total keyframes.

## Techniques (tags + evidence)
- mask-layer (auto) — mask layer 'Layer 5'.
- nested-master-symbol (auto) — 'DRW_marche + lente' nests 4 puppets' worth of Darwin parts (775 kf).
- layout-mov-reference (auto) — 'layout mov' video layer ships in the file.
- photo-plate (manual, render-verified) — photographic hallway plate.
- solo-close-up (manual) — sole character; closing scale-up to a frame-filling close-up on the same plate.

## What Cape Jones steals from this scene
The one-symbol solo: bank a "walk + emote" master symbol per character and a whole corridor scene becomes 21 placement keyframes. Occlusion by mask instead of redraw, a borrowed plate cropped from an earlier production, and a closing scale-punch instead of a camera move — three separate economies in one 229-frame shot.

## Gaps / honesty
- Render path: the original SWF rendered at ~2 frames/min under machine contention (its 5.3 MB is almost entirely the embedded layout video — 230 video tags). Following the pipeline's own wave-1 precedent, the video stream was stripped with tools/swf_strip_video.py (283 KB result) and the scene rendered from the novid copy; the stripped element is the guide/reference video only, and the SWF's sound asset survived (production audio is muxed into the video). The original SWF remains untouched in swfs/.
- What Darwin is singing/saying cannot be recovered from the sheet; no transcript was made.
