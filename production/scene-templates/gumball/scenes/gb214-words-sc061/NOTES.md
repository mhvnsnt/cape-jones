# The Words — Sc061: Darwin peeks and points around the layout-video giant (100 frames)

GB214 "The Words" (season 2) · slug `gb214-words-sc061` · SWF `GB214WORDS_Sc061_V012_Clean_MB.swf` · 100 frames @ 25fps

## Story / beat
As rendered, a giant classmate fills the frame — horned, long-haired, clawed, eyes hidden under her fringe, deadpan. Darwin plays around her: only his fin shows at first (f1), then he pops out from behind the right side of her head grinning (f13), gapes (f26), laughs (f38), switches to her left side still grinning and chin-resting (f51–63), and finally steps out in front of her at the end (f75–100), finger up, then pointing straight at her with shocked, arguing faces. She never reacts. The size difference is the joke: he is performing *at* someone ten times his size who doesn't care.

**Critical honesty note:** the giant is not a Flash puppet in this file (see Construction). She is the embedded layout/reference video. Darwin is the only animated puppet the FLA contains.

## Cast
- **Darwin** — the only puppet: `GB200_DRW_ORIGINAL_PUPPET_v001` on the `dwn` layer (279 kf; face comps 2,415 kf). All peek/point performance is his.
- **The giant classmate (unnamed in the file)** — present only as a `DOMVideoInstance` on the `layout mov` layer: a separately produced 3D-style character (horned, long-haired, clawed — consistent with a dinosaur classmate) embedded as reference for the composite. The FLA names her nowhere, so this library does not name her either.

## Construction
- Layer stack: audio / framecounter / fieldguide / `dwn` (Darwin) / white (a DOMShape) / background / `layout mov` (DOMVideoInstance). One keyframe per character layer — Darwin's animation is inside his puppet, the giant's motion is inside the video.
- The reference video is not a thumbnail guide: it renders at full frame, full opacity in places, and its content changes state mid-shot (flat white/unlit-looking in the early samples, textured grey-and-tan later) — consistent with a layout pass of the external character that the Flash side was timed against.
- **Field-guide leak:** in this file the `fieldguide` layer is a *regular* layer (3 keyframes), not a guide layer as in the other batch scenes — so the red production safe-area marks ("14:9 safe", "16:9 safe") render visibly into the exported frames and the staged video. The framecounter numbers render too.
- Background: `GB214_WORDS_SC057_LO_BG_crop.jpg` again, almost fully occluded by the reference character.

## Techniques (tags + evidence)
- `layout-mov-reference` (auto) — the scene carries a `layout mov` layer; its element is a `DOMVideoInstance`, and the reference character dominates the rendered frames.
- `face-comp-driven` (auto) — face comps hold 2,415 kf vs body puppets 279 kf.
- No manual tags claimed: the background plate is too occluded in the render to judge `photo-plate` honestly, and the two-character staging is a puppet-plus-reference composite rather than a library puppet technique.

## What Cape Jones steals from this scene
- **Composite against the real reference, in-file.** When one character comes from another pipeline (3D, paper, another animator), embed their actual render in the scene file and puppeteer against its exact positions — Darwin's peeks land on her head edges because the animator could see her head. Guessing at composite time is how eyelines and overlaps break.
- **One unresponsive giant + one hyperactive small character = a complete two-hander.** Darwin does 100% of the acting; the comedy is his energy against her stillness. Cape Jones can pair a held (or separately produced) character with a face-comp-driven reactor and get a full scene for the price of one puppet.
- **Keep guides on guide layers.** This file is the cautionary example: a fieldguide left as a regular layer ships in the render. Cape Jones scene templates should lock production overlays to guide/output-off layers before export.

## Media status
- Contact sheet: done (100/100 frames rendered). Video: done, with production audio muxed from the SWF sound asset — note the video inherits the visible field-guide overlay described above, because that is what the SWF renders. See `media_status.json`.

## Gaps / honesty
- The giant classmate's identity is not stated anywhere in the FLA; she is described, not named. Her finished, fully composited appearance cannot be verified from this file — the embedded video is a layout/reference pass, not final footage.
- Whether the final broadcast shot replaced the reference with a finished external render is outside this file's evidence; what the file proves is the *method* (puppet timed against embedded reference video).
