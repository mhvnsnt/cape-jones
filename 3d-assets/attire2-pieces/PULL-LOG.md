# Attire-2 Pieces — PULL LOG (license honesty)

Lane 4 scout, 2026-10-17. Canon: future Attire 2 = female-universe reskin of Cyborg X
(Alisa's Tekken model): Space Ghost style WITHOUT head ears, WHITE eyes, Batgirl-style
pieces — from OUR pulled pieces, NOT any actual 3D Cape Ghost model. Pieces STAGED only;
Attire 2 itself is NOT built here.

## Sources checked

| Source | What was sought | Result |
|---|---|---|
| Kenney.nl (CC0) — character-kit, animated-characters, blocky/mini packs | mask / cowl / cape / gloves / boots | **Nothing superhero-specific.** Character kits are plain low-poly people. Already staged generics in `~/workspace/customization-pulls/kenney/`. |
| KayKit (CC0) — Character-Pack-Adventures | hood / cape / costume bits | Rogue_Hooded has a hood (fantasy, not superhero). No masks/cowls/capes. Staged generics in `~/workspace/customization-pulls/kaykit/`. |
| Quaternius (QAL v1.0, owner-approved) | costume attachments | Hair/eyebrows only relevant pieces; no superhero parts. In `~/workspace/customization-pulls/quaternius/`. |
| poly.pizza API | "cowl", "cape" (CC0 GLTF) | **Dead end:** API requires a key (`{"error":"You need an API key..."}`). No signup performed; logged. |
| Sketchfab | CC0 mask/cowl/cape | Downloads require OAuth login. Not pulled. |
| thingiverse ("batman cowl" etc.) | cowl STLs | Mostly **CC-BY-NC** or unclear licenses → **EXCLUDED** (commercial show). |
| OpenGameArt | CC0 cape/mask 3D | Scattered single pieces, no coherent set; nothing pulled (no matching hero set found). |
| Mixamo | costume pieces | Adobe license — **no redistribution** → reference only, never committed. |
| "3D Cape Ghost" models | — | **Explicitly forbidden by owner canon.** Never searched for, never pulled. |
| Batgirl / Spider-Girl eye + mask/cowl pieces | — | **Separate lane** (dispatched ~15:00 CDT). NOT duplicated here. |

## What was staged instead

No open superhero-parts pack exists, so the toon-specific hero pieces were **built
procedurally as OUR geometry** (clean hard-vector style, sheet-03 compliant):
`cj_attire2_pieces.blend` via `build_attire2_pieces.py`. 15 objects:

- `CJ_A2_DominoMask` — Batgirl-style eye band (front arc, earless) + 2 gold eye rims
- `CJ_A2_Cowl` — earless cowl shell, open face (canon: NO head ears)
- `CJ_A2_Cape` — single-sheet shoulder-hung panel, unposed
- `CJ_A2_Gauntlet_L/R` — flared forearm gauntlets
- `CJ_A2_Boot_L/R` — shin + foot
- `CJ_A2_Belt` + 4 `CJ_A2_Pouch_*` — utility belt
- `CJ_A2_Emblem` — blank diamond shield (unpainted)

Materials are neutral placeholders (dark/gray/gold) — colors UNSET, the attire lane
paints per the future Attire-2 sheet. White eyes come from the face-rig eye cards
(`3d-assets/face-rig/`), which sit behind the domino mask's eye slots.

## For the attire lane

- Fit/scale/paint onto Alisa's model. Nothing here is fitted.
- The cowl has no solidify thickness (staging) — add before cloth sim if needed.
- Do NOT source from Mixamo/thingiverse/any "Cape Ghost" model (see exclusions above).
