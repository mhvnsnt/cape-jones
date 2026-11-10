# GB211 "The Treasure" — Sc122: heads on a string (23-frame bedroom insert)

**Cast (named, from the file):** Gumball (layer "GUMBALL", puppet `GB200_GUMBALL_PUPPET_001`), Darwin (layer "DARWIN", puppet `GB211_DARWIN_IN_BOWL_SHOT125_PUPPET_v001` — the fishbowl-shot variant), Anais (layer "ANAIS", puppet `GB200_ANAIS_ORIGINAL_PUPPET_V001`).
**Shape:** 23 frames @ 25 fps · source `GB211TREASURE_Sc122_V002_clean_MS.fla`
**Media:** contact sheet done + video done (production audio muxed from the SWF sound asset) — see media_status.json.

## Story / beat (from the contact sheet)
- All 23 frames are one held composition: the kids' bedroom, bunk beds centre, door right.
- At top-bunk height, frame-left, Gumball and Darwin hang from a thin yellow cord: only their heads (plus Gumball's one raised arm gripping the cord) are in play. Eyes closed, blissful; their mouths cycle open/closed as if singing or chanting; the pair sways gently, and by frame 20 Gumball tips toward Darwin.
- On the floor at frame-right, Anais stands looking up at them, smiling, holding her pose with minor stance shifts for the whole shot.

## Construction
- Three scene layers, one per character (DARWIN / ANAIS / GUMBALL), each a single keyframe placement — all performance lives inside the puppet/face-comp symbols, not in scene-level keys.
- Background: bitmap plate `GB211TREASURE_SC122_LO_AE.JPG` — in the render it is a genuine photographic bedroom (wood grain bunk frame, panelled door, carpet, skateboard props), flat vector puppets over it.
- Darwin's puppet is the in-bowl variant built for Sc125 (`GB211_DARWIN_IN_BOWL_SHOT125_PUPPET_v001`, with its own EYECOMP/HEADCOMP set); here no bowl layer is present, so he reads as a round floating head.
- A 'layout mov' guide layer (type: guide) ships in the file alongside the standard fieldguide/framecounter overlays.

## Techniques (tags + evidence)
- face-comp-driven (auto) — face comps 3,210 kf vs body puppets 1,180 kf.
- layout-mov-reference (auto) — guide-type 'layout mov' layer with a DOMVideoInstance.
- photo-plate (manual, render-verified) — photographic bedroom plate under vector puppets.
- multi-character-staging (manual) — three characters, one held composition, three separate layers.

## What Cape Jones steals from this scene
The 23-frame insert as a complete library unit: one weird staged image (heads dangling from a cord), one witness character planted on the floor to sell scale and reaction, mouths doing all the acting. Cape Jones scene-building should bank inserts like this — a held sub-second shot that only works because the staging is the gag.

## Gaps / honesty
- Why the boys are hanging from a cord is not explained inside these 23 frames — it belongs to the surrounding scenes (Sc117/Sc125 share the same in-bowl Darwin asset family); described here only as staged.
- The mouth cycles suggest singing/speaking, but no transcript was made from the production audio.
