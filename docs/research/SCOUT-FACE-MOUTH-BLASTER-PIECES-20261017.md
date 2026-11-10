# Scout Research — Face/Mouth Rig, Blaster VFX Extensions, Attire-2 Pieces

Lane 4 (restart x2), 2026-10-17. Owner unblocked ~14:45 CDT ("disc situation is settled", "get those scouted and get it going").
Spec sheets: `characters/sheets/06` (viseme/phoneme mouth matrix), `05` (expression + eye-dart matrix),
`03` (gauntlet energy rules: core #FFFFFF Normal, glow #FFB300 Color Dodge/Add, energy overlaps black line art),
`04` (charge rings, lightning arcs, zigzag beam tip, burst, impact).

## 1. FACE/MOUTH RIG SYSTEMS — winner: Telltale-style swap-set + Rhubarb automation

### What "Telltale-style interchangeable mouths" means (technique, studied not copied)
The classic cartoon swap method: the mouth is a **container holding one mesh per viseme**; exactly one
child is visible at a time, the rest hidden, swapped on phoneme boundaries. (Documented across Flash/Toon Boom
mouth-chart workflows and Adobe's mouth-swap-set behavior: "The mouth is like a swap set. One of the children
is displayed (Triggered). The others are hidden.") Telltale's 3D games used the same principle with
phoneme-driven mouth geometry inserts rather than blendshape interpolation — ideal for our hard-vector,
no-gradient toon look (sheet 03: "HARD VECTOR SHAPE / NO MULTIPLY"), where smooth morphing would fight the style.

### Why not blendshapes / bone-driven lips
Cape Jones's mouths are drawn shapes (sheet 06: "cheek and mouth lines only") — discrete graphic symbols,
not deforming flesh. A swap-set keeps every viseme pixel-true to the sheet. It also makes Rhubarb/Papagayo
output trivially consumable (phoneme → mouth index, no curve fitting).

### Winner wired in: `3d-assets/face-rig/`
- `build_mouthkit.py` — procedural builder (Blender 4.0.2 headless, xvfb-run). Builds 16 mouth meshes
  matched to sheet 06 (resting, A/AH, E/I, O/OO, U, M/B/P, F, C/D/G/K/N/R/S/T/Y, L/Th, W/Q, Sh/Ch,
  intense/clenched, gasp/surprise) + teeth/tongue parts + white-eye cards with 3 pupil variants per sheet 05
  (pupils sometimes-only for emphasis; white default). All mouths are OUR geometry, drawn from OUR sheet —
  nothing redistributed from any third party.
- `cj_mouth_kit.blend` — the built kit: `CJ_MouthDriver` empty with int property `mouth_index`;
  visibility drivers show exactly one mouth (Telltale swap-set). Eye-dart cards included.
- `rhubarb_map.json` — Rhubarb's A–H+X mouth shapes → our mouth indices (incl. G/H/X optional handling).
- `rhubarb_to_blender.py` — consumes Rhubarb TSV/JSON (or Papagayo .dat) and keyframes `mouth_index`
  on the driver at 24fps. Comedy timing note: holds beats, doesn't interpolate — swaps are hard cuts.
- `tools/rhubarb/` — Rhubarb Lip Sync **1.14.0** Linux binary vendored (MIT — see LICENSE-Rhubarb.md,
  SHA256 in SHA256.txt). Auto-generates phoneme timings from dialogue WAVs; optional transcript boosts accuracy.
- Manual refinement tool: **Papagayo-NG** (steveway/papagayo-ng) — NOT vendored: repo carries **no license
  file**; its readme references `gpl.txt` → treat as **GPL**. Use as an external app only; never link its code
  into our pipeline. Its `phonemes/*.json` sets are a useful reference for phoneme-set design (study, don't copy).

### Licenses (honest log)
| Item | License | Status |
|---|---|---|
| Rhubarb Lip Sync 1.14.0 (Daniel S. Wolf) | **MIT** (verbatim from its LICENSE.md, verified 2026-10-17 via GitHub API) | Vendored binary + license text |
| Papagayo-NG | **GPL** (gpl.txt in repo; no LICENSE file) | External tool only, not vendored |
| Mouth meshes / eye cards | Ours (built from our sheet 06/05) | No third-party art |
| Swap-set technique | Industry method (Flash/Toon Boom/Adobe docs) | Studied, not copied |

### What the face lane does next (not this lane)
Parent `CJ_MouthDriver` to the head bone in the rig file (rig lane owns the rig — we don't touch it),
key `mouth_index` per shot via `rhubarb_to_blender.py`. Eye darts keyed as separate cards.

## 2. BLASTER VFX — built ON `3d-assets/blaster-vfx/blaster_fx.blend`, not duplicated

Existing system (PR #102): `CJ_BlasterFX` geo-nodes group (charge rings, white-core/amber-shell beam,
zigzag tip, burst flash, sparks) driven by `charge`/`fire`/`recoil` on `CJ_BlasterDriver`; palette locked
in `blaster_palette.json`; proof renders in `proof/`. Verified present before touching: 445-line
`build_blasterfx.py`, blend 769KB, two proof PNGs.

### Gap analysis (what the palette promises but the build lacks)
`blaster_palette.json` declares `type_personalities` (arc_chain, energy_beam, gauntlet_bolt, wave_pulse)
and the task canon says: **blaster colors are per-scene**, and **while firing, the blast light BECOMES the
scene lighting** (rim + spill + grade). The build had none of: per-scene color override, an appendable
blast-light rig, the three extra FX types, or an impact flash (sheet 04, bottom right).

### Extensions added (additive edits to `build_blasterfx.py` — existing look untouched)
1. **`scene_grade` input** — tints the outer glow per scene (wardrobe recolor system); core stays #FFFFFF
   Normal per canon. Driven from a new `CJ_BlasterDriver.scene_tint` custom prop (RGB).
2. **`CJ_BlastLightRig`** — appendable light rig: blast point light (amber, driven by `fire`) + two rim
   lights whose color crossfades cyan→blast color on `fire` (the "blast light becomes scene lighting"
   canon, §blaster-lighting 2026-10-17). Shot files link this rig; the rig file itself is never edited.
3. **FX type variants** — `fx_type` enum on the group implementing the palette's `type_personalities`:
   `energy_beam` (default, existing), `gauntlet_bolt` (short jagged bolt, no sustained beam),
   `wave_pulse` (expanding torus pulse), `arc_chain` (cyan lightning arcs only, sheet 04).
4. **Impact flash** — starburst flash + ground ring at beam terminus (sheet 04 "Impact"), driven by `fire`.
5. Rebuilt `blaster_fx.blend` + new proof renders (charge / fire / impact), all in `proof/`.

### Open-source technique studied (not copied)
- `laishi/GeometryNodesByTutorials` Chapter 31 lightning-ray build (**MIT**, verified via GitHub API):
  resample-curve → per-point random offset → curve-to-mesh lightning technique. Our arcs use the same
  *principle* (per-vertex Random Value jitter — required anyway since Blender 4.0.2 has no GN texture nodes)
  rebuilt from scratch in our script; nothing copied from the tutorial files.
- Blender Studio open movies (CC-BY) were reviewed for beam-compositing reference (glare + color-dodge
  stacking); our compositor guidance in the spec already matches.

### Licenses
| Item | License | Status |
|---|---|---|
| GeometryNodesByTutorials (technique reference) | MIT | Studied only, nothing vendored |
| All blaster geometry/materials/drivers | Ours (procedural) | — |

## 3. SUPERHERO PIECES FOR ATTIRE 2 — staged, NOT built

Canon (owner 2026-10-17 ~14:47 CDT): Cyborg X = Cape Jones, same person. Future Attire 2 = female-universe
reskin of Cyborg X (Alisa's Tekken model): **Space Ghost style WITHOUT head ears, WHITE eyes,
Batgirl-style pieces — from OUR pulled pieces, NOT any actual 3D Cape Ghost model.** Attire 2 itself is
NOT built in this lane — pieces are staged only.

### Honest sourcing report
There is **no central CC0 "superhero costume parts" library** on Kenney / KayKit / Quaternius (verified by
pulling their catalogs 2026-10-08..17 — see `~/workspace/customization-pulls/MANIFEST.md`: character kits,
hair, no masks/cowls/capes). poly.pizza's API requires a key (dead end without signup). Sketchfab downloads
require OAuth. thingiverse is mostly CC-BY-NC (excluded for a commercial show). OpenGameArt has scattered
CC0 pieces but no coherent set. **No Batgirl/Spider-Girl pieces were pulled by this lane** — that pull-in
was dispatched as a separate lane ~15:00 CDT (eyes + mask/cowl pieces); not duplicated here.

### What this lane staged (`3d-assets/attire2-pieces/`)
Because no open superhero-parts pack exists, the toon-specific hero pieces are **built procedurally as OUR
geometry** (clean hard-vector style matching sheet 03), staged as separate appendable objects:
- `cj_attire2_pieces.blend` (built by `build_attire2_pieces.py`): domino eye mask (Batgirl-style, no cowl
  ears — canon: Space Ghost WITHOUT head ears), plain cowl shell (earless), shoulder-hung cape panel
  (matches cape lane's single-sheet spec, unposed), gauntlet gloves, boots, utility belt, chest emblem blank.
- `PULL-LOG.md` — every source checked, what was taken vs excluded and why (license honesty).
- `~/workspace/customization-pulls/` selects (Kenney/KayKit/Quaternius, CC0) remain the generic-parts
  reference; nothing superhero-specific was found there — logged, not fudged.

### Excluded with reasons (license honesty)
- Mixamo costume pieces — Adobe license, no redistribution → reference only, never committed.
- thingiverse "batman cowl" STLs — CC-BY-NC / unclear → excluded (commercial show).
- Any "3D Cape Ghost" model — explicitly forbidden by owner canon.
- Papagayo-NG code — GPL → external tool only.

## Verification
- Mouth kit: proof grid render of all 16 mouths + eye cards, viewed with own eyes (`face-rig/proof/`).
- Blaster: rebuilt blend + charge/fire/impact proof PNGs viewed (`blaster-vfx/proof/`).
- Pieces: piece turnaround render viewed (`attire2-pieces/proof/`).
- Claim tags per repo AGENTS.md: every "done" below is `verified` (file + hash checked) or marked otherwise.

## Branch / PR
Branch `lane/scout-resume-20261017`, pushed at creation and after every turn. PR → merge per repo law.
