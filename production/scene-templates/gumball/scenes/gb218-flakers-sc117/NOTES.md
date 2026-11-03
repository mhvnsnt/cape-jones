# The Flakers — Sc117: the couch pile-on — phone, pile-on, face-off, laugh (312f, KeyAnim)

**Episode:** GB218 "The Flakers" (Season 2) · **Scene:** Sc117 · **Frames:** 312 @ 25fps (the longest scene in the archive) · **Source:** GB218Flakers_Sc117_KeyAnim_V007.fla (51,767,121 bytes)

## Story / beat
One locked couch shot, a full mini-play in four movements. (1) f1–40: Anais alone on the plaid couch with her phone — red-lensed swoon at f1, delighted laughing by f40. (2) f79–157: Gumball and Darwin pile in on top of her — a three-head couch stack, Gumball shouting angrily from the top, Darwin gritting at the side, Anais squished underneath, still thrilled, phone in hand. (3) f195–234: up off the couch — Gumball mid-argument, Darwin smug, the phone dropped. (4) f273–312: all three crack up laughing together, then settle deadpan; the phone ends on the floor and Darwin ends flatly unimpressed.

## Cast
- **Anais** — GB200_ANAIS_ORIGINAL_PUPPET_V001 (911 kf) on the 'anais' layer. The scene's anchor; her head comp (787 kf) is the second-largest symbol in the file.
- **Gumball** — GB200_GUMBALL_PUPPET_001 (1,024 kf) on the 'gb' layer. The largest puppet track in the file.
- **Darwin** — GB200_DRW_ORIGINAL_PUPPET_v001 (752 kf) on the 'dwn' layer.

## Construction
- One locked background: GB218_Flakers_Sc117_LO_BG.jpg (bitmap plate, frames 0–312), rendering washed-out and pale in this KeyAnim export.
- A doubled stack: clean puppet layers (gb / dwn / anais) run parallel to DOMShape layers (GB / DRW / ANAIS / BRIEF) that carry the rough work, plus a ROUGH layer (0 kf of shapes held as a layer), a PHONE layer near the top, TEMP_PILLOWS and a pillows layer holding pillow2 / pillow3 / GB218Flakers_Props_SophaPillows_v001.fxg.
- Opens and closes on all three puppets plus the pillows (seams: opens_with and closes_with both list all three puppets and the background).

## Techniques (tags + evidence)
- **multi-character-staging** — three characters choreographed in one locked shot for 312 frames on separate puppet layers plus parallel shape layers (manual, layers + sheet).
- **rough-layer-shipped** — a layer named 'ROUGH' ships inside the KeyAnim file (auto); the export shows red rough bodies throughout and a second BLUE rough pass on Darwin's arms from ~f234.
- **face-comp-driven** — face comps 4,208 kf vs body puppets 2,687 kf (auto).
- **layout-mov-reference** — scene carries a 'layout mov' reference-video layer (auto).

## What Cape Jones steals from this scene
- The pile-on stack: three heads in one couch frame, each on its own layer, is a complete staging pattern for 'everyone wants the same seat/object' scenes — squash is vertical placement, not new drawings.
- Parallel rough layers: keeping GB/DRW/ANAIS shape layers beside the clean puppet layers lets the rough pass and the clean pass coexist in one file — steal the doubled stack for Cape Jones KeyAnim templates.
- The two-colour rough tell: a second pass in blue over red rough (Darwin's arms, final third) marks corrections without erasing the first pass — a cheap, honest revision convention.
- One phone prop motivates 312 frames: give the pile-on a single contested object and the long scene structures itself.

## Media status
- Contact sheet: done (312 frames). Video: done, production audio muxed from the SWF sound asset. Frames rendered: 312/312 — completed on the first FFDec attempt, unusually for this batch.

## Gaps / honesty
- KeyAnim state throughout: heads are finished colour comps, bodies are red (later also blue) rough lines, the couch plate renders pale and the right-hand cushions start as plain TEMP shapes. All documented as-is from the sheet.
- The draft anatomy build (pre-fix builder) grouped all three puppets under Gumball in the cast list; the finalize build with the fixed builder splits Anais / Darwin / Gumball correctly, as recorded above.
