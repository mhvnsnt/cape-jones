# Universe Color Language — Cape Jones / Space Jones canon
Written 2026-10-31. Approved base: Level 2 v2 warm-rim, Mars 2026-10-31 15:11 CDT ("perfect exactly").

## The idea, in Mars's words, made into a system
Colour is the universe language here. It has two dialects, and they are
NOT the same thing. Confusing them is how a shot goes wrong.

DIALECT 1 — LIGHTING-MOTIVATED COLOUR (LUT / grade / rim).
  The colour comes from a light source in the scene. LUTs, grades,
  key/fill/rim, bleed, shadow. Rule: rim follows the key colour
  (RIM-COLOR-RULE.md). When the light changes, the rim changes with it.
  Default for every shot, unless Dialect 2 or a power override is
  explicitly recorded.

DIALECT 2 — JOJO NON-CANON COLOUR (palette shift, NOT from lighting).
  The colour changes even though no light in the scene changed, to
  create a scenario, vibe, atmosphere, or feeling. This is the JoJo
  dialect, and it can run alone OR combined with Dialect 1 (a shift
  on top of a grade, recorded as both).

## What JoJo actually does (public research, pulled 2026-10-31)
- Hirohiko Araki: "None of my characters have a canon color palette."
  Colours change by scene for action, suspense, drama, or excitement.
  In Part 4, Morioh has a deep yellow sky instead of blue, with
  vibrant, drastically different coloured houses.
- Araki, 2017: he changes palettes to "put more emphasis on giving
  readers different feelings and impressions through different color
  combinations." The manga was mostly black-and-white, so readers
  imagined hues freely; the anime honours that with shifts.
- David Production (anime): shifts use a set of APPROVED palettes,
  not random per-frame colours. Shifts are associated with moments
  where characters are unsure of themselves, hero or villain, and
  the colour change instantly conveys that uncertainty.
- Uses, documented: heightened tension / drama, Stand / power
  activation, time stops / deep thought / power-ups (inverted
  schemes, ominous red tints), complementary opposition in a
  confrontation (Josuke's black hair turns red against Kira's
  green — opposition on the colour wheel), and whole-environment
  shifts (yellow sky, purple hills, pink grass).
- Roots Araki cites: Gauguin — disregard reality for colours that
  look good together and evoke emotion (soft pink grass against
  dark horses); Fauvism — intense, non-naturalistic colour to
  express emotion rather than depict reality accurately.
- IMPORTANT for our canon: Araki has no fixed canon palette. WE DO.
  Our base palette IS canon. A JoJo shift is a named, temporary
  variant on top of canon, and it returns to base when the beat ends.
  A shift that is not named, triggered, and returned is a mistake,
  not a style.

## How Dialect 2 works in Space Jones canon
1. TRIGGER FIRST. Every shift is tied to a story beat, recorded in
   the shot spec before it is used: beat name, feeling/vibe, palette
   name, scope (character only / environment only / both),
   duration (frames or seconds), and return (back to base, or to
   another shift). No trigger = no shift.
2. APPROVED PALETTES ONLY. Like David Production's approved sets,
   a shift palette is approved by Mars once, then reused by name.
   Demo palettes in this doc (approved as a DEMO, not as final
   canon palettes — Mars approves each for canon use separately):
   - JOJO-TENSION: purple/pink family, for uncertainty and rising
     tension. Character gain (1.20, 0.70, 1.30), rim follows the
     shifted key (magenta-rose family).
   - JOJO-POWER: red family, for power activation / climax.
     Character gain (1.30, 0.60, 0.60), rim in the red family.
   - JOJO-UNCERTAINTY: near black-and-white, high contrast, for
     a character unsure of themselves (the David Production
     uncertainty use, e.g. Kakyoin's black-and-white victory beat).
   - JOJO-ATMOSPHERE: environment-only shift, e.g. yellow sky /
     purple hills, while the character stays in base palette.
     Character gain (1.0, 1.0, 1.0), background gain recorded
     separately. This is the Morioh use.
3. RIM UNDER A SHIFT. The rim rule still applies, to the SHIFTED
   key, not the base key. A tension shift gets a magenta-rose rim,
   a power shift gets a red rim, never the default warm amber and
   never cyan. The rim is recorded in the same shot spec as the
   shift name, so a later shot cannot silently reuse it.
4. COMBINED WITH LIGHTING. A shift may sit on top of a grade:
   record BOTH — LUT/grade name + shift name + rim under shift.
   Example: golden-hour grade + JOJO-TENSION shift = warm grade
   first, then tension palette, rim in tension family. Never
   record only one of the two.
5. POWER OVERRIDE, RESTATED. A specific power that calls for a
   specific rim is its own override, recorded by power name.
   A JoJo shift is NOT a power override unless the shift IS the
   power's colour — if it is, record it as both (shift name +
   power name) so the reason is never lost.
6. OPPOSITION. In a confrontation, protagonist and antagonist may
   be put in complementary hues (red vs green, etc.), recorded as
   a pair in the shot spec, not as two independent shifts.

## What was searched in Mars's repos (honest note)
Searched 2026-10-31: memory (JoJo / colour), GitHub code search
across mhvnsnt repos for JoJo / Araki / non-canon, and local
cape-jones docs. Found: NO JoJo non-canon colour research doc in
those places. The only JoJo mentions in cape-jones docs are pose
filenames (dance = jojo packs) and one placeholder line in
INDUSTRY-VFX-PIPELINE.md saying findings "wire in when they land."
The research in this doc is therefore public JoJo / Araki /
David Production research (see above), applied to Space Jones
canon by the rules in this file. If the JoJo research Mars meant
lives in a specific repo under a different name (the message said
"emoji child repose" — no repo by that name exists in the 48
mhvnsnt repos listed 2026-10-31), name that repo and it will be
pulled in and this doc will be updated with it, not replaced.

## Tertiary level inside Dialect 1 (Mars, 2026-10-31 15:13 CDT)
Dialect 1 (lighting-motivated colour) has levels, not just one key:
- Primary: front key (warm gold here).
- Secondary: fill / bleed (warm orange bleed, cool shadow).
- Tertiary: back / contrast light — a second source from behind,
  here cyan, radiating as god rays. Its rim belongs to the back
  source, not to the front key, and it is recorded as a second
  source in the shot spec. This is how the original cyan rim
  "works and looks good": warm in front, cyan behind, two lights,
  not one light with a wrong rim.
God-ray setup: cyan rays from behind + warm gold rays from in front,
demo file showcase/dual-light-cyan-back-godrays-warm-front-v2-20261031.png
(PIL draft proof; production = Blender volumetric passes).
