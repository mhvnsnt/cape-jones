# Movement Math — Gumball "The Words" (GB214), Sc057 + Sc059

*Production science, study B of 3. Measured 2026-11-02 from the production
FLA files and the choreography extraction. Data: `data/movement-per-character.csv`,
`data/movement-math.json`, `chart-movement.svg`.*

## The units, once

- **fps: 25.** Both scenes, the layout movies, and the puppets all run at
  25 fps (the European broadcast standard this production works in).
- **Stage: 1920×1080 authoring pixels.** Speeds are given in those pixels
  unless marked "puppet units" (a puppet's own internal coordinate space —
  puppets are placed in the scene at a scale, so puppet units are bigger
  than screen pixels for the onlookers).
- **A "drawing" in a puppet system** is an *authored pose*: a keyframe where
  the animator set a part's placement, swapped its drawing, or changed its
  transform. The headline rate — **authored pose changes per second** —
  counts the frames where at least one part of the character gets a new
  authored pose. It is the honest equivalent of "drawings per second" for
  cut-out/puppet production: nobody redraws the whole character per frame;
  the character you see is a composite of parts, each on its own clock.

## Headline table — every character, measured

| Character | Scene | Pose changes | **Poses / sec** | Unique poses | Keyframes (all parts) | Spacing: 1f / 2f / 3f / 4f+ |
|---|---|---|---|---|---|---|
| **Darwin** | Sc059 | 52 in 105 f | **12.4** | 53 | 170 | 1.8% / **91.8%** / 0.6% / 5.9% |
| **Darwin** | Sc057 | 90 in 198 f | **11.4** | 86 | 439 | 2.1% / **86.3%** / 0% / 11.6% |
| Tobias | Sc057 | 87 | **11.0** | 83 | **716** | 0.3% / 83.4% / 2.4% / 14.0% |
| Carrie | Sc057 | 79 | **10.0** | 77 | 324 | 0% / 85.2% / 1.2% / 13.6% |
| Carmen | Sc057 | 78 | **9.9** | 79 | 342 | 1.2% / 86.3% / 2.6% / 9.9% |
| Masami | Sc057 | 60 | **7.6** | 61 | 122 | 1.6% / 73.8% / 4.9% / 19.7% |
| Ocho | Sc057 | 48 | **6.1** | 48 | 95 | 0% / 88.4% / 0% / 11.6% |

Background extras (the drawn critters on the `3d character ref` / Layer 6–13
scene layers, symbols c1–c10): **7 keyframes each across 198 frames** — a new
pose about every 28 frames, ~0.9/s. They are scenery that breathes.

## The twos engine — how the rate is actually built

**Every character in both scenes is keyed on twos.** Between 83% and 92% of
all authored keyframes, for every character, are 2-frame holds. Ones are
rare (0–2%) and reserved for accent hits and exits. So why doesn't the
composite rate cap at 12.5 poses/sec (25 fps ÷ 2)?

- **Per part**, the busiest layers run at 6–12 keyframes/sec — twos with
  rests. Darwin's head comp in Sc059: 50 keyframes in 105 frames =
  **11.9/sec**, nearly unbroken twos. His busiest Sc057 part layer: 88
  keyframes = 11.1/sec.
- **The composite** (any part changing) reaches 11–12.4/sec for the lead
  because 10+ part layers are keyed on twos but **staggered** — when the
  legs rest on a hold, the head or an arm fires. Darwin's per-second rate in
  Sc057 barely moves: 7, 12, 12, 13, 12, 11, 11. He never stops.
- **Threes barely exist** (0–5%). The spacing vocabulary of this production
  is: *twos as the default, ones for hits, holds for rests* — no economy
  threes. If a part isn't moving on twos, it's usually *held*, not slowed.

## Per-character movement personalities

**Darwin (the lead).** Sustained 11.4–12.4 poses/sec, no rest longer than a
17-frame hold anywhere in Sc057. 439 authored keyframes in the wide shot
alone. This is the most expensive performance in the scene and it's spent on
the character the camera is watching.

**The twist, by numbers (Sc059).** The `twist` layer is held for the first
43 frames — the move doesn't exist. Then **27 keyframes on strict twos,
frames 43–97** (12.5 poses/sec on that layer, no exceptions), an exit of
1f/3f/1f, and an 11-frame hold-out. The signature move is the most
disciplined piece of timing in either file: pure twos, fired exactly on the
audio accent at frame 43 (see `AUDIO-MAP.md` §3), over a bed that pulls back
under it.

**Tobias (the surprise).** 716 keyframes — **the most of any character,
including Darwin.** Hair, headband, eyes, mouth, arms, legs: every part of a
background onlooker is re-keyed on twos for the full shot, at 11.0 composite
poses/sec. The lesson cuts against the usual assumption: in this scene the
featured onlookers are animated at near-lead density, because they share the
frame with the lead for 8 seconds and the camera would catch them freezing.

**Carrie.** Joins late — 2 pose changes in her first second, then a steady
~11/sec. Plus a second, slower performance at **scene level**: her whole
puppet is placed on a layer with 10 keyframes and drifts **up 17.4 px across
the shot** (~2.2 px/sec) on long motion tweens with 22–34-frame holds. A
ghost hover: the float is in the placement, the life is in the puppet.

**Carmen.** 9.9/sec, and a production secret in plain sight: her arms' final
animation lives on a layer literally named **`rough arms`** (95 keyframes,
12.0/sec — her busiest layer). The rough pass was good enough to ship as
final. Three of her parts hold for 147 frames and one part never moves at
all (a 225-frame hold — longer than the shot; it's a static element inside a
living puppet).

**Masami.** The bursty one: 7.6/sec average, but her per-second rate swings
8, 8, 12, **3**, 11, 6, 6 — she performs in gusts and rests between them.
Face and body comps are keyed in lockstep (exactly 61 keyframes each — they
were keyed together, as one instrument). Her cloud body doesn't need the
lead's density; the gusts land on the phrase figures.

**Ocho.** The economy model: 6.1/sec, built from bursts of twos separated by
**dead holds — the longest is 69 frames (2.76 seconds)** of a frozen cactus.
48 unique poses for a 198-frame shot. He reads as alive because his bursts
are timed (his per-second counts spike to 12 in seconds 3 and 5), not
because he's dense.

**The c1–c10 critters.** 7 poses per shot each. At ~0.9 changes/sec they're
below the threshold of "character" and function as animated texture — cheap
because they're tiny, distant, and numerous.

## The approach shot — Darwin walks at the camera without moving

Measured from the render: Darwin's screen footprint grows from **4,533 to
46,548 pixels of orange (×10.3)** across Sc057; his height grows 95 → 257 px
(×2.7). Measured from the file: **his scene placement never changes** — one
keyframe, 198 frames, scale −0.366 (the negative is a horizontal flip),
locked position. The approach is manufactured *inside the puppet*: his head
comp scales **1.00 → 1.18 (f50) → 1.79 (f100) → 2.32 (f150) → 2.32 (f196)**
while the limbs keep dancing around it. The camera never dollies, the symbol
never translates — the character inflates in place, and because the hallway
background is a locked plate, the eye reads pure approach. Part-anchor
speeds confirm the violence under the smoothness: Darwin's head-comp anchor
moves at up to ~4,091 puppet px/sec at swaps (≈1,500 screen px/sec at his
placement scale) — the head *snaps* between drawn angles while the scale
curve does the traveling.

## Holds and the beat

Long holds cluster at about a beat (≈14 frames) or multiples of it:
Darwin's longest Sc057 hold is 17 frames; Masami's 19; Tobias's 20;
Carrie's 27 (≈2 beats); Ocho's 69 (≈5 beats). Rests are timed in beats,
not in arbitrary frames — even the stillness is on the grid (audio grid:
13.4 frames/beat, `AUDIO-MAP.md` §2).

## Match THESE numbers (the Cape Jones target card)

- **25 fps.** Everything — scenes, puppets, layout movies.
- **Key on twos by default:** 83–92% of keyframes are 2-frame holds. Ones
  (~2%) are for accent hits and exits only. Almost no threes — rest with
  *holds*, not slower spacing.
- **Lead character: 11–12.5 authored pose changes/sec, sustained**, built
  from staggered part layers each running 6–12 keyframes/sec.
- **Featured onlookers: 10–11/sec** (near-lead density when they share a
  long take). **Background cast: 6–8/sec**, bursty, with dead holds up to
  ~2.8 s. **Extras/scenery: ~1 change/sec.**
- **Signature moves:** strict twos for the move's full run; start the move
  **on an audio accent** (the twist lands within half a frame); exit on a
  short hold.
- **Music math:** ~112 BPM = a beat every 13.4 frames; phrase figure every
  4 beats (~54 frames); time holds in beats.
- **Approach shots:** lock the placement; scale the parts inside the
  puppet (head ×2.3 over ~6 seconds) for a ×10 screen-area growth.
