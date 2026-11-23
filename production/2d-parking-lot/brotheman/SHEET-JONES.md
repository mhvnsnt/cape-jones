# BROTHERMAN — SHEET JONES (Model Sheets) — LOCKED LIKENESS v2

**Character:** BROTHERMAN — all caps, ALL ONE WORD. Not "Brother Man", not "Brother".
**Likeness lock:** owner, 2026-11-23 07:17 EST. Landed in repo main as PR #436,
merge commit `9d0c79f` (`docs/BROTHERMAN.md`, `HANDOFF.md`, `AGENTS.md`). The 5
reference webp images are NOT in the repo yet (binary upload needed via a
git-authenticated machine / browser UI to
`production/2d-parking-lot/brotherman/`) — do not claim they are landed.
Reference used here (read-only, NOT copied): the parallel `brotherman/` lane's
concept images, especially `v4-bald-top-long-hair`, `v3-pink-bandana`,
`v4-cape-correct`. All art in `brotheman/` is built fresh in this lane.
**Status:** Sheet Jones v2 (locked), 2026-11-23. Rig Jones 1 is built from these
sheets (see `BROTHERMAN-REPORT.md`). He appears in the SECOND full episode
only. Episode 1 (Cape goes into the game into Immortal Kombat, mix of 2D and
3D) does NOT have him.
**Do not land in the repo** — workdir only until the owner calls it.

## 1. Who he is

- He calls everyone "brother". Everyone calls him "brother".
- Larger than life, very big / bulky / muscular, warm, loud, confident — a
  big-brother energy, not a villain. He is Cape Jones's big brother figure.
- His line to Cape Jones (episode 2): *"You just gotta motherfucking keep up
  with the Joneses, brother."* Voice is owner-gated — no synthesized voice
  ever. The test video shows the line as an on-screen speech card, silent.
- First full episode: NOT in it. Second full episode: his debut.

## 2. Design — LOCKED likeness (use exactly this, do not change it)

- **Build:** big muscular wrestler, 7 heads tall, shoulders 3 heads wide, chest
  ~2 heads wide, hands 1 head long, arms ~3 heads, legs ~3 heads. Cape Jones
  reaches only to his chest (see scale figure on sheet 01).
- **Head:** bald on top, LONG BLOND hair at the sides and back as DEFAULT.
  Strong jaw. Thick BLOND horseshoe mustache. Tanned skin. White eyes with
  dark pupils, big grin.
- **Costume:** BLUE tank top with "BROTHERMAN" in PINK Hulkamania-style comic
  letters across the chest. White wristbands. Black belt with gold buckle.
  PINK + BLUE + PURPLE tie-dye LONG TIGHTS. BLUE boots with PINK laces.
- **Bandana (continuity rule):** PINK bandana on first appearance, BLUE bandana
  sometimes, NO bandana most of the time. A bandana change happens ONLY visibly
  (on-screen change) or as a noticed look-away joke — never random
  scene-to-scene. The rig carries bandana as a swap (pink / blue / none).
- **Full-hair version:** ONLY for old-him / flashback "this used to be me" gag.
  Not the default, not in the test video.
- **Hands:** very big. Fist, Open, Point are his three hand poses. Wrist-to-wrist
  rule (see §5): wrist at the top of the hand, fingers at the far end, fingers
  pointing DOWN at rest — never upside down, never floating.

## 3. Palette — locked

| Part | Color | Hex |
|---|---|---|
| Skin | Tanned skin | `#D89B62` |
| Hair / mustache | Blond | `#E8C25E` |
| Tank top | Blue | `#2B8FD4` |
| BROTHERMAN letters | Pink | `#EC4D8C` |
| Tie-dye | Pink / Blue / Purple swirls | `#EC4D8C` / `#2B8FD4` / `#7B4BD6` |
| Boots | Blue, pink laces | `#2B8FD4` / `#EC4D8C` |
| Wristbands | White | `#FFFFFF` |
| Belt | Black, gold buckle | `#000000` / `#E8B83A` |
| Bandana (first appearance) | Pink | `#EC4D8C` |
| Bandana (sometimes) | Blue | `#2B8FD4` |
| Eyes | White + dark pupil | `#FFFFFF` / `#1A1A1A` |

## 4. Cape Jones likeness rule (applies in ANY shot with him)

Never draw Cape Jones away from his likeness: purple cowl, white eyes, tan
lower face, white skin-tight suit with purple V, white belt, long black cape,
white gloves, white boots. NO jacket, NO lapels, NO black gloves. (The
`v4-bald-top-long-hair` reference gets Cape wrong — jacket + lapels + black
gloves. The `v4-cape-correct` reference and the V2 plate
`v2/check-f0001.png` get him right.) Sheet 01's scale figure uses the
correct Cape.

## 5. Rig rules (carried into Rig Jones 1)

- Wrist-to-wrist hand attachment: arm wrist meets hand wrist, same direction,
  fingers at the far end of the hand. Hands are never upside down, never
  floating, never detached from the forearm. Owner hand log 2026-11-23 07:06:
  CORRECT = wrist-to-wrist, same direction, fingers at far end, remote in
  fingers pointing DOWN, hands attached to forearm cuff, thumbs medial,
  clean-cropped transparent alpha, no white box. INCORRECT (never again) =
  top-layer hands fingers-up, wrist at bottom, floating beside thighs,
  detached; remote upside down, remote pointing UP, arm-wrist and hand-wrist
  opposite; white background box not cropped. Hands are SWAP planes with
  correct orientation — never layered on with wrong orientation.
- No white-background boxes on any part or prop — every part is
  transparent-alpha PNG, cropped to the art.
- Gumball rig method (see `BROTHERMAN-REPORT.md` §Gumball): layered puppet
  with a fixed z-stack, swappable part libraries (hands / mouths / eyes /
  bandana), real elbow + knee joints with overlap caps, articulating fingers
  + thumbs, squash & stretch, and secondary-motion follow-through on the
  long hair and bandana tails. The rig is cleaned up from the start so it
  already reads at Draw Jones / Video Jones level — a live Video Jones of
  BROTHERMAN, not a puppet substitute. This rig is the EXAMPLE for the Cape
  Jones Clean-Up Jones plan (see report).
- Eyes are swap planes (Open / Happy / Wink) with scale-Y blink; mouths are
  swap planes (Closed / Smile / Grin / Open / Shout / Frown); fingers +
  thumbs articulate on the Open hand.
- Same base pipeline as the Cape Jones V2 rig (native Blender armature +
  emission image planes, transparent film, ortho camera) — see
  `rig/build_rig.py` in the workdir root for the reference pipeline. BROTHERMAN's
  rig is a NEW file, `brotheman/brotheman-rig.blend`; no Cape rig file was
  edited. The bar is to BEAT V2, not match it (owner, 2026-11-23 07:19 EST).

## 6. Sheets (files)

| File | What it is |
|---|---|
| `sheets/01-turnaround.png` (+ `.webp`) | Front / Side / Back turnaround (pink bandana front) + scale figure vs correct Cape Jones |
| `sheets/02-construction.png` (+ `.webp`) | Construction (T-pose, red construction lines) + proportions, 7 heads tall, design-notes box |
| `sheets/03-expressions-hands-colors.png` (+ `.webp`) | Expressions (Neutral / Grin / Shout / Wink), hand studies (Fist / Open / Point), locked palette |

Known sheet artifacts (generator, not canon — do not copy into the rig):
- Sheet 03 labels two different grins both "GRIN" (2nd and 3rd heads). They are
  two grin variants (closed grin / toothy grin); the label duplication is a
  generator artifact, not two different expressions.
- Sheet 03's blond swatch reads `#E8C256`; the lock is `#E8C25E`. Same color,
  one digit of generator drift — the lock value rules.

## 7. History — superseded v1 (do NOT deliver as final)

- Sheet Jones v1 / Rig Jones v1 (teal bandana, dark handlebar mustache, white
  tank, black trunks, teal wristbands) was built 2026-11-23 from the first
  brief and SUPERSEDED the same day by the owner likeness lock (07:17 EST).
  Its sheets, parts, and renders were replaced in place by the locked v2
  files in this folder. Nothing teal ships.

## 8. What is NOT done yet

- 3/4 head angle, up/down angles — Front + Profile only so far (same gap as
  Cape Jones Sheet Jones).
- Full-hair flashback head variant (gag only) — not built; Rig Jones 1 uses
  the default bald-top / long-back-hair head.
- No episode-2 boards, no Action Jones (animatic), no voice (owner-gated).
- Rig Jones 1 is the first rig; Clean-Up Jones (Rig Jones 2) is a later pass.
  The Cape Jones Clean-Up plan that this rig demonstrates is in
  `BROTHERMAN-REPORT.md`.
