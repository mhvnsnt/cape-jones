# Universe Color Language V3 — TRUE palette replacement, not lighting overlay
Written 2026-10-31. NEW file. Does NOT overwrite UNIVERSE-COLOR-LANGUAGE.md (v1)
or UNIVERSE-COLOR-LANGUAGE-V2-20261031.md (v2). V1/V2 rules still stand unless
this file explicitly corrects them; where they disagree, the newest Mars
correction in this file wins.

## 0. Mars's correction (2026-10-31 16:14 CDT) — the whole point of v3
The JoJo dialect/language does NOT just alter the lighting. When a JoJo
color shift happens, it BREAKS the canon — it is NON-CANON — the world
colors change AND the character's colors change. He CANNOT look like he
stayed the base same color with just an overlay on top of him. His colors
have to ALSO alter, with the color theory of how JoJo does it.
Mars: the creators explain it better than he can — so v3 researches
that method and shows another application of it. V3 is NOT perfect.
It is another application, improved, still to be perfected by Mars's eye.
Do NOT quote v3 as approved canon. No palette in v3 is approved until
Mars approves it by name, per the show-first rule carried from v2.

## 1. Research — how Araki / David Production actually reassign palettes
Sources (public, method and palette theory only; no character art,
script dialogue, or logo copied; Cape Jones only in every sheet):

- Araki, creator of JoJo's Bizarre Adventure: "None of my characters
  have a canon color palette." Colours change by scene for action,
  suspense, drama, excitement. The manga was mostly black-and-white,
  so readers imagined hues freely; covers vary freely — one cover one
  scheme, the next another. Variability IS the method, not a mistake
  in it. Shueisha handles manga colouring and Araki has limited input
  there; David Production references the manga and chooses the
  palettes they believe will look best, with input from Araki.
  (CBR, "8 Misconceptions About JoJo's Bizarre Adventure, Debunked",
  misconception 5; MyAnimeList forum discussion of the same Araki
  statement.)
- David Production, anime studio (2012 adaptation onward): shifts use
  APPROVED palettes, not random per-frame colours. Shifts appear in
  opening songs and at dramatic moments; whole scenes bathed in pink
  or turquoise (Part 5, Golden Wind); a character's look in an opening
  may follow a volume-cover palette rather than the episode default.
  A victory beat may go chic black-and-white. The shift is a
  RE-PAINT of the frame: character flats, hair/costume colours, and
  environment colours are all chosen again, together, for that beat.
- Morioh, Part 4 (Diamond is Unbreakable), the environment case:
  yellow skies, purple hills, pink grass in a seemingly normal town.
  "Incorrect" colours creating unease — the world is re-coloured,
  not just lit differently. David Production leaned into this:
  when things get real, the sky turns purple and the grass turns
  pink/orange. The visual cue is that the RULES of reality have bent.
- Complementary opposition: in a climax, one side's hair turns red
  against the other's green — opposition ON the colour wheel, not
  two random colours. Red vs green is a pair, never two solo shifts.
- Inverted schemes: time stops, deep thought, power-ups get inverted
  schemes and ominous red tints — the whole value structure flips,
  not just a warm grade laid over it.
- Gauguin / Synthetism / Cloisonnism (Araki's cited root): colour
  liberated from its descriptive role — large flat areas of intense,
  non-naturalistic hue, separated by strong outlines, chosen because
  they look good together and evoke emotion. The black outline STAYS
  in v3 for exactly this reason: the line is the drawing, the flat
  inside it is the palette, and the palette is free to change.
- Fauvism (Matisse, Derain, Vlaminck): colour as pure expression,
  intense juxtapositions placed side by side so the eye vibrates.
  A 5% nudge is not a JoJo shift; a named palette jump is.
- Colour theory used for every reassignment in section 3:
  complementary (opposites on the wheel), split-complementary
  (a colour + the two beside its opposite), triadic (three evenly
  spaced hues), analogous (neighbours on the wheel), monochromatic
  (one hue, value steps only — UNCERTAINTY), and value-first
  (DREAD is darker overall, not just redder).

## 2. Why a LUT gain is WRONG for Dialect 2 — v2 vs v3, stated plainly
- V2 method: PIL gain (R,G,B) multiplied over the clean A-pose.
  Example TENSION (1.20,0.70,1.30). A gain PRESERVES base hues:
  purple cowl stays purple, only pinker; white suit stays white,
  only pinker; black cape stays black. That is grading. Grading is
  Dialect 1 (lighting-motivated). It is the right tool for a LUT,
  a rim, a grade — and the WRONG tool for a JoJo shift.
- V3 method: palette replacement. Each part gets a NEW flat colour,
  chosen by colour theory, and the old shading steps are carried
  across as deltas from the new base (new = shifted + (pixel − base),
  clamped). Shading and form survive; hue does NOT survive — that
  is the point. Purple cowl BECOMES hot pink (TENSION), scarlet
  (POWER), turquoise (DREAM), grey (UNCERTAINTY). White suit BECOMES
  rose, red-orange, pale cyan, grey. Black cape BECOMES plum-black,
  red-black, teal-black — dark, but tinted to the palette, not
  untouched black. The world is reassigned in parallel: sky, hills,
  ground each get a new flat colour from the same palette family.
- The test that separates them: cover the world panel and look only
  at the character. Under v2, you can still read the base palette
  underneath the grade. Under v3, you cannot — the character IS a
  different palette. If you can still read base purple/white/black
  unchanged, it is not a v3 shift, it is a v2 grade wearing a v3 name.
- ATMOSPHERE is the one exception, and it proves the rule: it is
  environment-only by definition (approved 15:36 CDT as a world
  shift). In v3 its character panel is IDENTICAL to base, on
  purpose, while its world is yellow sky / purple hills / pink
  ground. Every other v3 palette changes the character.
- CAPE UNDER A SHIFT — v3's answer, pending Mars's confirmation:
  Mars's earlier pending question was whether the cape stays black
  under a shift. V3 does NOT leave it untouched black and does NOT
  turn it bright: it reassigns it to a DARK TINT of the palette
  (plum-black, red-black, teal-black, navy-black). Silhouette and
  weight survive; the cape reads as part of the new palette, not as
  a base-colour leftover. If Mars says "cape stays pure black",
  that is a one-line change to the cape row — the rest of v3 stands.
- Per-palette .cube LUTs are Dialect 1 tools, NOT Dialect 2 tools.
  A .cube grades light; it cannot reassign a cowl from purple to
  scarlet while reassigning a suit from white to red-orange and a
  sky from blue to red-orange at the same time, independently.
  Do not confuse "we have a .cube for TENSION" with "we have a
  Dialect 2 TENSION palette". V3 tables below are the Dialect 2
  artefact; .cubes remain the Dialect 1 artefact.

## 3. TRUE palette tables — base -> shifted, per part and per world element
Base palette, measured from the rig (not guessed):
- Cowl purple (90,39,114) — from sliced/Head_Front.png, Neck.png
- Skin (239,175,131) — from sliced/Head_Front.png
- Suit white (255,255,255) — from sliced/Torso_Chest.png
- Suit shadow grey-blue (178,186,199) — from sliced/Leg_Front.png
- Cape near-black (23,21,26) — from sliced/Cape_Back_Main.png
- Eye white (255,255,255) — normal superhero eyes are white/angular;
  eye row follows the suit at near-full brightness, except where noted
- Black outline (0,0,0) — NEVER reassigned. The line stays black in
  every palette (Cloisonnism: strong outline, free flat colour).
- Base world (canon world, for the left panel of every sheet):
  sky (150,180,210), hills (90,140,90), ground (120,90,60)

### TENSION — magenta-rose, split-complementary off violet
Trigger: rising tension, a threat lands, the beat tightens.
Theory: base violet pushed to its hot neighbour (magenta-rose) and
the world split around it — pink sky, violet hills, plum ground.
| Part | Base | Shifted | Reason |
| Cowl | (90,39,114) | (255,40,140) | Violet -> hot magenta: same family, turned up to felt, not graded |
| Skin | (239,175,131) | (250,170,150) | Warm skin, pink-tinted: stays readable as skin, joins the palette |
| Suit | (255,255,255) | (255,110,180) | White -> rose: the suit IS the tension colour now, not lit pink |
| Suit shadow | (178,186,199) | (200,90,150) | Shadow deepens into rose, not grey |
| Cape | (23,21,26) | (45,10,35) | Plum-black: dark tint, silhouette held |
| Eye | (255,255,255) | (255,220,235) | Near-white rose tint |
| World sky/hills/ground | (150,180,210)/(90,140,90)/(120,90,60) | (255,110,180)/(130,40,170)/(90,20,60) | Whole scene in the palette |

### POWER — scarlet / red-orange, complementary heat
Trigger: power lands, explosive beat, climax energy.
Theory: warm triad — scarlet cowl, red-orange suit, red-orange sky.
Bright/explosive, the opposite pole of DREAD (dark/held).
| Part | Base | Shifted |
| Cowl | (90,39,114) | (200,20,40) |
| Skin | (239,175,131) | (245,180,140) |
| Suit | (255,255,255) | (255,80,50) |
| Suit shadow | (178,186,199) | (190,60,50) |
| Cape | (23,21,26) | (40,10,10) |
| Eye | (255,255,255) | (255,230,200) |
| World sky/hills/ground | as base | (255,90,40)/(140,30,30)/(70,15,15) |

### UNCERTAINTY — near black-and-white, monochromatic
Trigger: doubt, a beat where nothing is certain, Kakyoin-style
black-and-white victory/uncertainty beat.
Theory: monochromatic — hue removed, value structure kept. This is
the ONLY palette where "no new hue" is correct, because the hue
removal IS the shift.
| Part | Base | Shifted |
| Cowl | (90,39,114) | (110,110,110) |
| Skin | (239,175,131) | (190,190,190) |
| Suit | (255,255,255) | (230,230,230) |
| Suit shadow | (178,186,199) | (150,150,150) |
| Cape | (23,21,26) | (30,30,30) |
| Eye | (255,255,255) | (240,240,240) |
| World sky/hills/ground | as base | (170,170,170)/(110,110,110)/(60,60,60) |

### DREAM — pink/turquoise whole-scene bath, split-complementary
Trigger: dream, memory, a scene that is not quite real.
Theory: Part 5 whole-scene bath — turquoise character against a
pink hills band. Turquoise and pink are not neighbours; their clash
is what makes the scene feel unreal.
| Part | Base | Shifted |
| Cowl | (90,39,114) | (40,200,210) |
| Skin | (239,175,131) | (255,200,180) |
| Suit | (255,255,255) | (170,240,250) |
| Suit shadow | (178,186,199) | (120,190,210) |
| Cape | (23,21,26) | (10,35,45) |
| Eye | (255,255,255) | (220,250,255) |
| World sky/hills/ground | as base | (80,220,230)/(255,140,200)/(30,90,110) |

### DREAD — ominous desaturated red, dark/held (NOT Power)
Trigger: dread, a held threat, time-stop/deep-thought weight.
Theory: inverted/darkened scheme — same red family as POWER, but
value pulled DOWN (0.85 and darker flats). POWER is bright and
explosive; DREAD is dark and held. If DREAD reads as POWER, it failed.
| Part | Base | Shifted |
| Cowl | (90,39,114) | (110,20,30) |
| Skin | (239,175,131) | (210,170,160) |
| Suit | (255,255,255) | (170,60,60) |
| Suit shadow | (178,186,199) | (120,40,45) |
| Cape | (23,21,26) | (15,8,10) |
| Eye | (255,255,255) | (230,200,200) |
| World sky/hills/ground | as base | (140,50,50)/(80,25,30)/(35,10,12) |

### RESOLVE — cool teal, the return path out of UNCERTAINTY
Trigger: resolve, clarity after doubt, the beat where he decides.
Theory: cool analogous family — teal cowl, ice-blue suit, teal sky.
The opposite temperature to POWER/DREAD, and the way back from
the grey of UNCERTAINTY is through colour, not through more grey.
| Part | Base | Shifted |
| Cowl | (90,39,114) | (30,140,160) |
| Skin | (239,175,131) | (240,185,150) |
| Suit | (255,255,255) | (210,235,250) |
| Suit shadow | (178,186,199) | (140,180,205) |
| Cape | (23,21,26) | (15,25,40) |
| Eye | (255,255,255) | (230,245,255) |
| World sky/hills/ground | as base | (70,180,200)/(50,110,120)/(25,60,70) |

### ATMOSPHERE — environment-only (the exception, approved 15:36 CDT)
Trigger: a place feels wrong/strange while he himself is unchanged.
Theory: Morioh — the world is "incorrect", the character is not.
Character rows are BASE, unchanged, on purpose.
| Part | Base | Shifted |
| Cowl / Skin / Suit / Shadow / Cape / Eye | as base | UNCHANGED |
| World sky/hills/ground | as base | (230,200,60)/(130,70,170)/(200,90,150) |

### OPPOSITION — red vs green, a PAIR, never two solo shifts
Trigger: climax, two sides opposed.
Theory: complementary opposition ON the wheel. Left = POWER red
(above); right = green reassignment below. Shown as a pair, and
both return to base after.
| Part (green side) | Base | Shifted |
| Cowl | (90,39,114) | (30,180,80) |
| Skin | (239,175,131) | (220,200,170) |
| Suit | (255,255,255) | (90,220,130) |
| Suit shadow | (178,186,199) | (70,170,100) |
| Cape | (23,21,26) | (10,35,20) |
| Eye | (255,255,255) | (220,255,230) |
| World sky/hills/ground | as base | (90,200,120)/(40,120,60)/(20,60,30) |

### BRIGHT PINK JOJO TENSION / PINK HOUR JOJO TENSION — carried, renamed
Approved as an image + name 15:49-15:50 CDT, never "golden hour"
for that image. In v3 terms it is a TENSION-family palette with a
pink-hour world: cowl (255,40,140)-family, suit rose, sky pink.
Its full table is the TENSION table above with the world sky held
at pink-hour pink; it is not a ninth separate theory, it is the
named TENSION image Mars already approved.

## 4. Shot-spec fields for Dialect 2 (v3, replaces the v2 gain fields)
shift_name, trigger_beat, scope (character / world / both — ATMOSPHERE
is world-only, all others are both), duration_frames, return_to
(always BASE unless Mars names otherwise), palette_table (section 3
row, by name), cape_rule (dark-tint, pending Mars's stay-black call),
opposition_pair (for OPPOSITION only), approved (name + date, blank
until Mars approves), dialect1_combined (LUT/rim/grade applied BEFORE
or AFTER the palette swap — record it; a Dialect 1 grade on top of a
Dialect 2 swap is allowed only if the swap is still readable as a
new palette, not as base-under-grade).

## 5. How the sheets were built (honest method, not a claim of production)
- Source: reposes-v7c-clean/joint-apose-v7c-clean.png (A-pose).
  Grey background (128,128,128) flood-filled out from the borders;
  character pixels classified by part (cowl purple family, skin
  family, white suit, grey-blue shadow, dark cape, black outline kept
  black), then delta-remapped to each palette table above.
- World panels are FLAT bands (sky / hills / ground) in the palette's
  world colours — a palette proof, NOT a painted background. A painted
  background recoloured by these tables is still owed (see section 6).
- Defects found in viewing and fixed: v1 titles truncated at the
  right edge and bottom captions clipped — titles shortened, sheet
  height raised to 880, captions moved to y=840, re-viewed clean.
- Minor artifact, NOT hidden: in TENSION (and faintly elsewhere) a
  few pink/red speckles sit on the cape edge where the classifier
  caught fringe pixels. They are on the cape fringe, not on the face
  or suit, and do not change the palette read — but they are there,
  and a production pass must clean the cape fringe mask.
- No show character art, name as a character, script dialogue, or
  logo appears in this doc or any sheet. Cape Jones only.

## 6. What v3 still does NOT prove — what is still owed to perfection
- Mars's per-palette canon approval: 0/8 v3 palettes approved
  (ATMOSPHERE's world and the BRIGHT PINK image/name were approved
  in v2 terms; their v3 tables are still unapproved until Mars says
  the v3 versions by name).
- Cape stay-black call: pending (section 2, dark-tint answer is v3's
  proposal, not Mars's decision).
- Production (Blender) renders of any shift: 0/8. These sheets are
  PIL palette proofs on an A-pose, not production renders.
- Painted-background versions: 0/8 — flat world bands only.
- Per-palette .cube LUTs: 0/8, and deliberately NOT the deliverable
  for Dialect 2 (see section 2). If a .cube is built for a palette,
  it is a Dialect 1 companion, labelled as such, never the shift itself.
- A colour script for an actual Cape Jones sequence: 0/1 (the v2
  trigger table is a template, not a sequence script).
- Poses beyond A-pose: 0/8 palettes shown on a flex, punch, dance,
  or seated pose. A-pose proves the palette; a pose proves it survives
  movement.
- V3 is an application so far, improved over v2, NOT perfected.
  Mars's eye is the perfection step, and it has not happened yet.
