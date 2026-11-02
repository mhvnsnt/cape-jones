# STUDY — the hallway scene, dissected (GB214 "The Words", Sc057 + Sc059)

Owner's order (2026-11-02): study this scene completely — every character named,
every layer accounted for — so Cape Jones can be brought to this level, then put
him in it. This is that study. Everything below is measured from the production
files (`GB214WORDS_Sc057_V036_clean_MUI.fla`, `GB214WORDS_Sc059_V001_clean_RR.fla`
and their SWFs); the numbers live in `hallway-study-data.json` next to this doc.
Where the file does not name something, this doc says so instead of guessing.

Stage: 1920×1080, 25 fps. Sc057 = 198 frames (7.9 s). Sc059 = 105 frames (4.2 s).
Both scenes are built the same way: a handful of puppet comps placed **once** on
the scene timeline, and all the performance living *inside* the puppets.

---

## 1. The cast — every character in the scene, named

### Sc057 (the wide shot)

| Who | Scene layer | Puppet (library item) | Placement | Role |
|---|---|---|---|---|
| **Darwin Watterson** | `Layer 2` | `GB200_DRW_ORIGINAL_PUPPET_v001` | a=−0.366 (flipped), tx 1089.4, ty 544.6, **one keyframe, never moves at scene level** | The dancer. His puppet's internal timeline is 277 frames; the scene plays the first 198. |
| **Tobias Wilson** | `tobias` | `GB200_TOBIAS_ORIGINAL_P_COMP_V002` | 0.344 @ (1258, 584) | Groover, right side. The most animated onlooker: 18-layer comp, 215 internal frames — arms 58/52 keyframes, legs 56/74, head 75, headband 75, hairs 78, all on twos from frame 11. Full-body bounce. |
| **Carmen** (the cactus) | `carmen` | `GB200_CARMEN_34_COMP` | 0.352 @ (1421, 570) | Sway, far right. Face/arms/body keyed on twos ×80 from frame 5 — but her legs and right arm have **4 keyframes with a 147-frame hold**: a potted cactus dances top-half only, legs planted. |
| **Masami Yoshida** (the cloud) | `masami` | `GB200_MASAMI_PUPPET_V002` | 0.352 @ (1245, 383) | Floater, upper right. 6 layers; face + body 61 keyframes on twos from frame 9. In this V036 export she renders as line art — her colour pass is not in the file (production state, not a style choice). |
| **Ocho** (the 8-bit spider) | `ocho` | `GB200_OCHO_ORIGINAL_PUPPET_V001` | 0.350 @ (918, 360) | Scuttler, left side. 3 layers: body comp 49 keyframes, legs swapping between the symbols literally named `ocho legs walk cycle` and `ocho legs rest` (46 keyframes from frame 7). No BEAT layer — the leg cycle *is* his beat. |
| **Carrie Krueger** (the ghost) | `carrie` | `GB200_CARRIE_COMP_V002` | 0.262 @ (1233, 355) | Late joiner, furthest back (smallest scale of the named cast). The **only** cast member re-keyed at scene level: 10 keyframes — her comp's `firstFrame` is re-synced at f22/26/35/49/77/100/129/149/164 while ty drifts 355 → 337 → 343 (a float bob). Inside her comp, head + body key on twos ×65 **starting at frame 22** — she starts dancing 22 frames in, and the scene layer keeps re-syncing her to the performance. |
| **The background crowd — 7 figures** | `3d character ref` (c9), `Layer 13` (c6), `Layer 12` (c5), `Layer 11` (c2), `Layer 8` (c3), `Layer 7` (c7), `Layer 6` (c10) | symbols `c2, c3, c5, c6, c7, c9, c10` | shared track, see §3 | Seven **single hand-drawn shapes**, one per symbol, sitting in a folder the file itself names `3d character ref`. Five more sit unused in the library (c1, c4, c8, c11, c12). |

**Honest limit on the crowd's names:** the FLA never names these seven. They are
identified in the data file by symbol, size and position (c7 is the big one,
320×421 px — the slot the finished episode fills with Tina Rex; c10 is the tall
thin one, 90×221 px; c5/c6 are small, ~60–70 px). In this file they render as the
white/uncoloured students. Anyone who tells you their names from *this* file is
guessing; what the file proves is seven drawn stand-ins for the show's
mixed-media background students, animated as one block (§3).

Also in the file, not characters: `framecounter` (the burned-in blue counter —
it is in the clean video because it is in the production file), `fieldguide`
(guide layer), the scene's own audio (`GB214_WORDS_057.aiff`), and under
everything a `layout mov` layer holding the layout video
`GB214_WORDS_SC057_LO_QT.flv` — the animatic the scene was built on top of.

### Sc059 (the twist close-up)

Two characters only:

| Who | Scene layer | Placement | Role |
|---|---|---|---|
| **Darwin Watterson** | `dwn` | a=−2.841 (flipped), tx 1764.3, ty 485.3, one keyframe | The twist, waist-up and huge. This scene carries its own copy of his puppet with a 113-frame internal timeline (§4). |
| **Masami Yoshida** | `masami` | a=−2.895 (flipped), tx 1112.4, ty 43.3 | Big at the frame edge — and she is not just watching: her puppet copy here has its own `beat` layer (9 keyframes) and face/body keyed on twos ×54. She dances along inside the close-up. |

Background: `GB214_WORDS_SC059_LO_BG.jpg`. Audio: `GB214_WORDS_059.aif`.

---

## 2. Layer stack and staging

Sc057, top to bottom (23 scene layers):

```
audio · framecounter · fieldguide (guide)
mask ──────────────── masks the layer below
Darwin (Layer 2)
tobias · carmen · masami · ocho · carrie      ← named cast band
white                                          ← full-frame white card
[folder "3d character ref": mask + crowd ×7]   ← background crowd block
background (GB214_WORDS_SC057_LO_BG.jpg, photographic, static, scale 3.0)
layout mov (the animatic, static)
```

How eight-plus characters share one hallway without clutter:

- **The named cast lives in one tight scale band** — 0.262 to 0.352 — placed
  once and never re-keyed at scene level (Carrie excepted). Nobody competes
  with the dancer for size or movement; all their motion is internal.
- **The `white` layer is the depth trick.** A full-frame white shape sitting
  *exactly* at the split between the named cast and everything behind them.
  It washes the photographic background and the crowd flat and pale, so the
  saturated cast pops in front of it. Depth here is not drawn — it's a
  sandwich: photo → crowd → white wash → cast.
- **The crowd is white on purpose.** Seven flat uncoloured shapes behind the
  wash read as "students further down the hall" without a single detail
  competing with the cast. In this export Masami/Tina-slot/Carrie also render
  uncoloured, which is the file's unfinished colour pass — but the crowd's
  whiteness is structural: they are single shapes with no colour layers at all.
- **Two masks do the cropping.** One mask (extent ≈1822×992, re-keyed at f58
  and f87) sits over Darwin; one sits over the crowd folder. The crowd is only
  ever visible through its mask window — that's how flat shapes at the wrong
  scale never break the hallway's perspective.
- **The camera never moves.** The background is one static photograph at one
  static scale for all 198 frames. The sense of travelling down the hallway is
  manufactured inside the characters (§3). Sc059 is the same recipe at
  close-up scale: 9 layers, two puppets, one photo.

Sc059 stack: `audio · framecounter · fieldguide · masami · dwn (Darwin) ·
white · background · layout mov` — same sandwich, tighter cast.

---

## 3. The fake dolly — how Darwin walks *toward* a camera that never moves

Darwin's scene placement is a single static keyframe. His growth is keyed
**inside his puppet**, on the head comp, on twos (full track in the data file):

- f8–f23: scale **0.998** (flat — he's at the far end of the hall)
- f25 → f127: a steady climb — 1.10, 1.15, 1.18, 1.23, 1.27, 1.40, 1.44, 1.59,
  1.63, 1.79, 1.83, 1.94, 2.06, 2.13, 2.20, 2.27 — landing on **2.319 at f127**
- f127–f197: locked at 2.319. The last 70 frames are pure dance at full size.

Measured on the render (Darwin-orange pixels, frames057_hd): his on-screen
height goes 93 px → 243 px across the shot, ≈2.6×. The puppet even carries a
guide layer named `perspective` holding the perspective drawing he grows along,
and his head-comp tx walks +578 → −371 → +550 → −8 while it grows: he weaves
side to side down the hall as he comes at you.

The crowd gets the same treatment at scene level: all seven figures share
**one** perspective track — keyframes at f5/36/47/85/114/138, scale stepping
0.773 → 0.787 → 1.221 → 1.612 for every figure simultaneously (some mirrored,
a flips negative). One track, seven puppets: the whole crowd block slides and
grows as a single perspective unit while Darwin passes it. Nobody keyed seven
characters — they keyed one crowd.

And a truth about the wide shot's craft: Darwin's Sc057 body is substantially
**hand-drawn**. His puppet's `rough arms` (94 keyframes) and `rough legs`
(81 keyframes) are drawn shape passes; the clean leg symbols underneath carry
only 7 keyframes. The symbol-driven part is the head comp (80 keyframes,
pose-scrubbed: its `firstFrame` always equals the frame number) plus the drawn
body. The strut reads as fluid because a human drew it, on twos, over a
timing chart.

---

## 4. The timing system — beat, twos, and the twist

**The beat is a layer.** Sc059's Darwin puppet opens with a layer literally
named `beat`: 9 keyframes with spans (0,9), then 14 frames ×6, then (93,10),
(103,10). Fourteen frames at 25 fps = 0.56 s = **≈107 BPM**. Masami's Sc059
puppet carries the same `beat` layer. In Sc057, every onlooker comp (Tobias,
Carmen, Carrie, Masami) carries a shared `BEAT` track instead: 21 keyframes,
alternating 11/10-frame spans — boundaries at 0, 11, 21, 32, 42, 53, 63, 74,
84, 95, 105… — one track, copied into every comp, so the whole crowd breathes
on the same grid without anyone animating them together.

**Everything is on twos.** Part layers are keyframed every 2 frames with
pose-to-pose holds (keyMode 9728 — the pose *is* the frame; there is no
in-betweening to hide behind). The animators' `chart` guide layers and the
rough guides share a signature rhythm — holds of 1, 6, 2, 2, 2, 2, 6 frames —
long anticipation holds, then quick twos through the move.

**Staggered joins.** Nobody starts together: Carmen's parts start at f5,
Ocho's legs at f7, Masami at f9, Tobias at f11, Carrie's head/body at f22.
The scene *fills up* over its first second.

**The twist (Sc059), built in four moves:**

1. **Frames 0–42 — the wind-up.** The `twist`, leg and body layers hold a
   single pose for 43 frames while the head comp (50 keyframes, twos
   throughout) and the rough arm guides keep grooving. The body is cocked;
   only the head is dancing.
2. **Frame 43 — launch, on the chart, not on a beat boundary.** The chart
   layer's 50-frame hold also ends at 43. From here the `twist` layer's
   32 keyframes fire every 2 frames.
3. **Frames 43–97 — the twist itself.** 27 poses on twos (54 frames ≈ 3.9
   beats), legs and body layers keyed in lockstep (29 keyframes each, same
   spans). Inside the puppet sits the move's seed: a library symbol named
   `darwin twist` — a 4-frame rough fragment whose head layer swaps in
   `GB200_DRW_BACKVIEW_HEAD` mid-move. The twist is the one place the puppet
   turns him all the way around, and they drew a special fragment for it
   instead of trusting the standard parts.
4. **Frames 97–113 — the settle.** Spans widen (1, 3, 1, 11): a couple of
   single-frame accents, then an 11-frame hold. The move lands and breathes.

**Part libraries are pose libraries.** Darwin's fin (arm) symbol is a
124-frame strip of single-frame poses with a LABELS layer (segments at
0/24/115); each leg symbol is an 18-pose strip (labels at 0/115). The
performance is pose-swap + transform on twos — the library is the vocabulary,
the puppet timeline is the sentence.

---

## 5. What "that level" is made of — the recipe

1. Pose libraries with labelled sections, deep enough that a whole dance is
   pose-swap + transform (fins: 24 poses; legs: 18 poses; head comp: a
   scrubbed expression/pose strip).
2. A hand-drawn rough pass wherever symbols can't carry the motion — in the
   wide shot, the star's body is drawn, not assembled.
3. Beat and chart as literal layers in every file, before any part moves.
4. Twos discipline: poses held, accents on single frames only at hits.
5. Staging by sandwich: photo plate → crowd block on one shared perspective
   track → white wash card → named cast in one scale band → masked dancer.
6. Growth/travel faked inside the puppet (head-comp ramp + perspective
   guide), never by moving the scene camera.
7. One special fragment (`darwin twist`, back-view head) drawn for the one
   move the standard parts can't do.

---

## 6. The gap list — what Cape Jones needs to hit this level

Concrete, in build order:

1. **A CJ puppet with the same slot anatomy** as `GB200_DRW_ORIGINAL_PUPPET`:
   head comp (scrubbed pose/expression strip, 50+ keys worth), L/R arm pose
   libraries (~24 labelled poses each), L/R leg pose libraries (~18 each),
   torso, and — the slot Darwin fills with `dar tail` — **the cape as its own
   keyed layer**. Plus a **back-view head** (the twist swaps one in; without
   it CJ can't turn around).
2. **Drawn rough-pass material for CJ's arms/legs** in the wide shot, or a
   pose library dense enough to stand in for it. Sc057's strut is drawn;
   a pose-swap-only CJ will read stiffer than Darwin in the same slot. This
   is the single biggest quality gap.
3. **His own hallway cast**: five onlooker slots with distinct dance logics
   (full-body groover / top-half sway / floater / leg-cycle scuttler /
   late-join floater) and a 7-figure white crowd block. CJ's world has to
   supply those drawings; the Gumball figures stay Gumball's.
4. **Beat/chart layers as a production habit**: 14-frame beat grid (107 BPM
   for this song) in the dancer's file; the shared ~10.5-frame BEAT track in
   every onlooker comp.
5. **A hallway plate + layout pass**: one static background plate, a layout
   movie under the scene while building, masks over dancer and crowd, and a
   white wash card at the cast/background split.
6. **The internal growth ramp**: CJ's approach keyed inside his puppet on
   the head comp (Darwin's exact track is in the data file), with a
   perspective guide drawing.
7. **Choreography data**: CJ's parts get keyed from
   `dance-gumball-darwin-words-sc057-sc059.json` — Darwin's per-part
   transforms are the performance; CJ's poses map onto them slot by slot.
8. **No framecounter in CJ finals.** It's a production artifact that ships
   in these files (and therefore in the pulled clean video); his show
   shouldn't carry one.

Phase 2 (the parody scene) is built against this list; whatever it can't
honestly satisfy gets named there, not papered over.
