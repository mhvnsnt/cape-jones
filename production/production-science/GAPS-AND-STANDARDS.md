# Gaps and Standards — what else a production like this runs on

*Production science, study C of 3. The visual study covered layers and cast;
`AUDIO-MAP.md` covered sound; `MOVEMENT-MATH.md` covered timing. This
document covers the remaining industry-standard machinery of a production
like Gumball's — for each aspect: what it is, the evidence for or against it
in these two files (Sc057/Sc059, "The Words," GB214), and the verdict for
Cape Jones production. Evidence first; where the files are silent, it says
so plainly.*

## Verdict table

| # | Aspect | In these files? | Cape Jones verdict |
|---|---|---|---|
| 1 | Exposure / dope sheets | Present in digital form — a `chart` layer inside every puppet | **Adopt** (chart layer + exported timing CSV per scene) |
| 2 | Bar sheets (music timing sheets) | Present as `beat`/`BEAT` layers inside puppets | **Adopt, corrected** — generate beat layers from the *measured* audio grid |
| 3 | Layout stage with approval gate | Present and formal — approved layout movies embedded in the FLA | **Adopt** — no animation before an approved layout exists |
| 4 | Model sheets / puppet library system | Present — the GB200 library, versioned part comps | **Adopt** — already the CJ plan; version every part comp |
| 5 | Color styling / color pass as a separate stage | Present as pipeline state — line-art characters in a late file version | **Adopt the discipline** — file names carry stage + version + initials |
| 6 | Compositing as its own stage | The FLA is *not* the composite — mixed media is assembled later | **Adopt** — never ship a raw scene-file render as final |
| 7 | Retakes / QC loop | Present — version counts, `clean` stages, frame counters burned into working renders | **Adopt** — frame-accurate notes, framecounter on every review render |
| 8 | Broadcast delivery specs | Deliberately *not* met by these files — they are pre-mix working documents | **Adopt at the right stage** — master at delivery, with DX/MX/FX stems |
| 9 | Field / format guides | Present — a Fieldguide symbol embedded in every scene | **Adopt** — a CJ field guide symbol in every scene file |
| 10 | Sound breakdown discipline | Present — per-shot mono AIFFs from a numbered department folder | **Adopt** — a breakdown track per shot, before animation |

## The aspects, one by one

### 1. Exposure sheets (dope sheets / X-sheets)
The classic frame-by-frame plan of a scene: one row per frame, one column
per layer, dialogue and camera notes down the side. In a digital puppet
pipeline the paper sheet is gone, but its function survives **inside the
file**: every puppet in both scenes carries a layer literally named
**`chart`** (Darwin: 15 keyframes in each scene's puppet; Masami: 22) — the
timing chart the animator worked from, kept in the timeline next to the
animation it describes.
**CJ verdict — adopt twice over:** keep a `chart` layer in every Cape Jones
scene file, *and* export the per-scene timing data as CSV (this study's
`data/` folder is the template) so a scene can be re-timed, audited, or
handed to another tool without opening the FLA.

### 2. Bar sheets
For music-driven scenes, the traditional companion to the dope sheet is the
**bar sheet**, mapping musical bars/beats to frame numbers. Here that job is
done by the `beat` (Sc059) and `BEAT` (Masami, Sc057) layers. The catch,
measured in `AUDIO-MAP.md` §2: the Sc059 beat layer is drawn at a rounded
14-frame period against a true 13.4-frame beat, sits ~half a beat off the
final track's grid, and Masami's library `BEAT` layer matches no grid in
this scene at all.
**CJ verdict — adopt, corrected:** beat layers are the right tool, but ours
get generated from the *measured* grid of the finished track (tempo, phase,
phrase accents — the `AUDIO-MAP.md` method), never drawn by ear or inherited
from a library puppet.

### 3. Layout, with an approval gate
Both FLAs embed the scene's **approved layout movie** on a layer named
`layout mov`: `GB214_WORDS_SC057_LO_QT.flv`, sourced from
`N:/08_ANIMATION/05_LAYOUT/02_APPROVED/Sc057/` — a department path with an
*approval* folder in it. The layout is 1280×720 while the finished scene is
1920×1080: layout works at ⅔ resolution, is approved, and only then does
full animation begin, with the layout movie sitting inside the FLA as the
animator's reference for staging and timing.
**CJ verdict — adopt as a hard gate:** no scene gets animated before a
layout pass exists and is approved; the layout lives inside the scene file
while animating.

### 4. Model sheets and the puppet library
The characters are not drawn per episode. They are **library puppets** from
a shared GB200 series library — part-level components (`GB200_TB_ARM_L`,
`GB200_CARRIE_MOUTHCOMP_V002`, `…EYESCOMP…`), each versioned (V001/V002),
reused across episodes and scenes, with per-episode variants when a shot
needs one (Carmen's `34` comp). The hallway study documents the full cast
assembly. This is the model-sheet system's digital form: the "sheet" is a
buildable, versioned puppet.
**CJ verdict — adopt (already the plan):** Cape Jones gets one FLA library
of versioned part comps — the thing the dance-choreography swap is waiting
on — and every part comp carries a version, never an overwrite.

### 5. Color as a stage, and honest file states
Sc057's file is version **V036** — and in it, Tina, Carrie, and Masami still
render as **line art**: their color pass is not in this version of the file
(Darwin, Carmen, Tobias are fully colored). File names across the holdings
carry the same honesty: `_clean`, `KeyAnim`, animator initials (`_MUI`,
`_RR`, `_STN`). The production never pretends a file is further along than
it is; the name *is* the status.
**CJ verdict — adopt the naming discipline:** scene files carry
stage + version + author (`_keyanim`, `_clean`, `_comp`…), and a scene is
called done only at its final stage. (This matches the standing rule that a
fighter/scene is never presented as proof before its pipeline is finished.)

### 6. Compositing
The FLA is not the finished picture. The hallway "background" in the file is
a flat **layout** plate (`GB214_WORDS_SC057_LO_BG.jpg` — LO = layout), the
3D characters arrive via `3d character ref` elements, and the series is
famous for mixing 2D puppets with photographic backgrounds and CGI — work
assembled at a compositing stage (for the series: 2D in Flash with After
Effects compositing; Studio SOI built backgrounds and 3D characters;
backgrounds are photographed plates treated in Photoshop so the perspective
tricks the eye correctly — art director Antoine Perez's published account).
The FLA is one ingredient — the character performance — not the composite.
**CJ verdict — adopt:** Cape Jones scenes get a real comp step (graded
plates, LED/lighting treatment, the LOOK 1 / LOOK 2 system). A raw
scene-file render is a *review* artifact, never the delivery.

### 7. Retakes and QC
Thirty-six versions of Sc057's file exist by the time of the one we hold.
Every working render carries a **frame counter and field guide burned into
the frame** (the `Field&Framecounter` library device, top-right of every
frame of the clean video) — so any note, from anyone, can name the exact
frame it is about.
**CJ verdict — adopt:** framecounter + field guide burned into every review
render (the device already exists in our pipeline vocabulary), retake notes
by frame number only, versions never overwritten.

### 8. Broadcast delivery
These files would fail broadcast QC on audio — integrated loudness
−16.6/−15.1 LUFS against a **−24 LKFS (ATSC A/85, US) / −23 LUFS (EBU R128,
EU)** target, true peak +2.11 dBTP against a **−2/−1 dBTP** ceiling — and
they are *supposed* to: delivery masters are built in post-production from
dialogue/music/effects **stems**, at the end of the chain, not in the
animator's file. There are no stems anywhere in the animation files because
stems are not an animation-stage artifact.
**CJ verdict — adopt at the right stage:** animation-stage audio stays a
mono breakdown (Study A). When Cape Jones episodes ship, the final mix is
built with DX/MX/FX stems and mastered to the destination's spec
(−24 LKFS / −2 dBTP for US broadcast-style delivery; −14 LUFS / −1 dBTP is
the common streaming normalization target).

### 9. Field guides
Every scene file embeds the show's **Fieldguide** symbol (safe areas /
framing reference) on a guide layer, next to the frame counter. One
canonical framing reference, present in the file, not in someone's memory.
**CJ verdict — adopt:** one CJ field guide symbol, embedded in every scene
file from the template.

### 10. The sound department's shape
The audio's paper trail (Study A §1, §5) shows a numbered department tree —
`08_ANIMATION/03_SHOT BREAKDOWNS/MONO AIFFS` on a shared production drive,
`05_LAYOUT/02_APPROVED` for layouts — with voices recorded first and the
editor (Richard Overall, for this series) cutting breakdown tracks per shot
before animation. Sound is not "added later"; it is *broken down* early and
*finished* late.
**CJ verdict — adopt, with the owner's one deliberate deviation:** for music
and dance, audio is finished first and animation keys to it (already true —
the EN/JP mixes are final). For dialogue, the owner runs the opposite order
by design: he records lines after animation and lip-syncs in post
(MouthSwap). That deviation is a choice, made knowingly — this study's job
is to record that the industry default is dialogue-first, and that our
music pipeline follows the standard exactly.

## What was looked for and NOT found (honest absences)

- **Paper-style dope sheets / bar sheets as documents** — none in the
  holdings; their functions live in-file (`chart` / `beat` layers).
- **Color scripts** (the per-episode color-design document used on many
  productions) — no evidence in these two files; the color stage shows up
  only as file *state* (§5). Marked absent, not assumed.
- **Separate SFX/Foley/dialogue recordings** — none; one flattened mix per
  shot (Study A §1).
- **Camera-work paperwork** — the camera is locked in both scenes (the
  approach is faked inside the puppet, `MOVEMENT-MATH.md`); nothing to
  learn about camera moves from these two shots. Other scenes in the
  harvest (e.g. the Sc119 punch-zoom) are where that evidence lives.

## Sources

File evidence: `GB214WORDS_Sc057_V036_clean_MUI.fla/.swf`,
`GB214WORDS_Sc059_V001_clean_RR.fla/.swf`, their XFL documents (library
paths, media items, publish settings) and internal media stores.
Published accounts (cited in `AUDIO-MAP.md` / research notes): Ben
Bocquelet interview (Anime Superhero forum archive) on pipeline, editor and
composer roles, and post at Fitzrovia; Animation Magazine, "Colorful
Gumball Premieres on CN Tonight" (2011) — Flash + After Effects for 2D,
Maya for CG, Photoshop backgrounds; Kidscreen animation services issue
(2012) — Antoine Perez on background-plate perspective treatment.
Standards: ATSC A/85 (−24 LKFS, −2 dBTP); EBU R128 (−23 LUFS, −1 dBTP);
ITU-R BS.1770 (the measurement both use).
