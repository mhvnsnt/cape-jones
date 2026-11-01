# MOCHIICHAO INTO CAPE JONES / SPACE JONES — Combine Spec + Design
Date: 2026-10-31. Mars, 2026-10-31 15:36 CDT (atmosphere approval message).
Status: SPEC + DESIGN ONLY. Nothing here is wired into a final shot yet.
Do not claim otherwise.

## 0. CANON RULE FIRST (non-negotiable, Mars's own framing)
- Cape Jones / Space Jones has a DIFFERENT canon and a DIFFERENT show
  language than Mochiichao. Do NOT merge the canons.
- Bring only a little Mochiichao aspect / soul into Cape Jones, the same
  way a little Western Heart aspect was brought into its soul.
- Mochiichao stays its own thing. Cape Jones borrows vibe, systems, and
  ONE device (Section 3). It does not borrow Mochiichao's roster, world,
  story, or canon.
- Third-party show material in this doc is systems/methods only, under
  the standing barred list: exact likeness shipped as-is, character
  literally, name, script dialogue, logo. Mochiichao material is Mars's
  own internal IP, so it is not third-party material — but its species
  still stay out of Cape Jones except on the device screen (Section 3).

## 1. BACKGROUND LIFE — systems pulled from Mochiichao, mapped to Cape Jones
Sources (all read 2026-10-31, local work clone
~/workspace/mochiichao-work/fresh-start, main branch, read-only, no push
from that clone):
- src/world/WorldRenderer.tsx (verified code)
- src/lib/garden-data.ts (verified code)
- src/lib/mochiichao-systems.ts (verified code, Garden Stats / alignment /
  colorway functions)
- src/lib/stacks.ts — boids-stack, status SPEC (not code)
- goals/mochiichao-fresh-start-repo/files/chao-garden-conversion.md
- goals/mochiichao-fresh-start-repo/files/garden-mode-spec.md
- goals/mochiichao-fresh-start-repo/files/creature-mode-spec.md

Systems inventoried: 10. Pulled for Cape Jones mapping: 10/10 = 100% as
spec mappings (code/spec status per row — a mapping is not a wired shot).

| # | Mochiichao system (source) | What it is | Cape Jones mapping (room / street / forest atmosphere) | Canon-safe? |
|---|---|---|---|---|
| 1 | Fake-perspective scaling, WorldRenderer.tsx | perspScale = 0.88 + (vy/viewH)*0.12; tile height and sprite scale grow toward the bottom of frame | Room (locked 2.5x scale): foreground floor/rug larger, background window smaller — same depth trick, painted background, not a tile grid | Yes — method only |
| 2 | Waterflow animation, WorldRenderer.tsx | WATER tile: repeating-linear-gradient + "waterflow 2.5s linear infinite" | Street/forest: rain, window light, curtain sway, tree shimmer — one slow looping gradient/pattern drift per background, never a character | Yes — method only |
| 3 | NPC shadow + bounce, WorldRenderer.tsx | Ellipse shadow under NPC, walkbob 0.5s ease-in-out on alternate walk frames, "!" bounce for battle NPCs | Room/street: background figures get a soft ellipse shadow + a 0.5s bob on walk cycles; a small "!"-style pop (shape only, no text bubble from another show) marks a background beat | Yes — method only |
| 4 | Tall-grass / path pattern, WorldRenderer.tsx | Repeating-linear-gradient stripes for grass/path/ledge, building gradient + top highlight | Forest atmosphere (the approved yellow-sky forest): grass stripes sway by offsetting the gradient phase; path stones keep a fixed pattern so the eye reads depth | Yes — method only |
| 5 | Door glow, WorldRenderer.tsx | DOOR tile: radial gradient ellipse at 50%/80%, warm (255,200,100) at 0.4 alpha, fading to transparent at 70% | Room: TV glow, lamp glow, hallway-door glow — same radial warm ellipse, tied to Cape Jones lighting levels (Level 2 bleed, Level 3 god rays), not a Mochiichao door | Yes — method only |
| 6 | Garden Critter behaviours, garden-data.ts (21 types, verified list) | Backstroke, flutter, hop, chest-pound, steady-walk, dive-loop, drift, dash, dig-pound, root-stand, float, soar, spark-hop, charge, graze, sidestep, cloud-drift, bolt-run, roll-pound, ember-walk, glow-drift | Background life vocabulary: abstract background figures (Cape Jones universe shapes, NOT Mochiichao critters) hop / flutter / drift / graze on a loop in the forest and street backgrounds. The BEHAVIOUR words carry over; the critter species do not | Yes — behaviour only, species kept out |
| 7 | Boids flocking, garden-mode-spec.md §3 + stacks.ts (SPEC only, not code) | Separation / alignment / cohesion for critter flocks and Creature Mode packs | Forest/street: background groups move as a flock (separation + alignment + cohesion) instead of each figure moving alone — this is what makes a background feel alive rather than tiled | Yes — algorithm only, MIT-source method, no copied code |
| 8 | Need icons, chao-garden-conversion.md (minute-to-minute) + garden-data.ts OTHER_GAMES_RULES (Tamagotchi rule mapping) | ! hungry, Z sleepy, flower ring = Bonding Season — visible state, never hidden | Room: Space Jones's own state icons as a gag/system — TV on/off, light switch, device beep — visible, readable, never hidden behind a menu. This is the Tamagotchi-care readability idea, applied to a human character's house, not to a Mochiichao creature | Yes — readability method only |
| 9 | Data Lessons: Dance, Song, Sketch, Rhythm, chao-garden-conversion.md (Academy) | Lessons unlock Garden idle animations + Bond, NOT battle power | Room/street: idle-animation library for Cape Jones — a small set of idle loops (tapping foot, humming, sketching, swaying) that play when he is NOT the focus, so backgrounds breathe even in a held shot | Yes — idle-loop method only |
| 10 | Data-Fruit farm cycle, chao-garden-conversion.md + garden-data.ts FRUIT_MAP | 3 trees per garden; shake → harvest → feed; regrow 1 in-game day / ~7 min active time; fruit→stat map (Aqua→Dive, Aero→Glide, Swift→Sprint, Chrome→Might, Earth→Endurance) | Street/forest: a repeating background cycle (tree shake → leaves fall → regrow) on a slow timer, plus a market-stall / kitchen cycle in the room — a loop the audience can learn, not a one-off effect | Yes — cycle structure only, fruit names kept out |

What is NOT pulled: Mochiichao species/roster (47), Mochiichao world
maps (Sector 0 / Binary Woods / Neon City), Mochiichao story, Mochiichao
battle numbers, and any Mochiichao creature appearing in a Cape Jones
background as itself. Those stay in Mochiichao.

## 2. DANCE COMBINE — ONE dance-scene spec (spec first, no final clip yet)
Dance spec done: YES (this section). Final dance clip built: NO — 0/1,
owed after the spec is approved.

### Sources combined (by name)
(a) Mochiichao dance / Creature Mode movement, already built as spec:
- chao-garden-conversion.md: Academy Data Lessons — Dance, Song,
  Sketch, Rhythm — unlock idle animations + Bond, not battle power.
- creature-mode-spec.md: temperament matrix — solitary / pack /
  skittish / territorial — as movement data; pack creatures move as a
  flock (Boids); skittish flees if approached too fast; territorial
  engages on sight; curious approaches and watches. Sprint drains
  stamina, dodge ~0.25s i-frames, perfect dodge refunds cooldown.
- garden-mode-spec.md: races use Sprint + Glide for speed, Endurance
  for late-race fade — a stamina curve, not a flat speed.
(b) Cape Jones Darwin dance (the ONLY verified dance in the show audit):
- Source: cape-jones/production/dance-choreo/ (README, INVENTORY,
  dance-gumball-darwin-words-sc057-sc059.json); audit row 11,
  SHOW-REPO-DEEP-AUDIT-20261031.md.
- Sc057 wide hallway strut, 198 frames; Sc059 close-up twist.
- Beat grid ~14 frames at 25 fps (~107 BPM); keyframing ON TWOS;
  twist layer 32 keyframes, frames 43–97; beat layers in onlooker
  puppets; progression stride → groove → kick → split stance → twist.
- Puppet slots: head comp, L/R fin (arm), L/R leg, body.
(c) Other show pulls (audit, systems only):
- Smiling Friends gait/pose swaps (audit row: Charlie/Pim rigs):
  legs 10 pose frames, arms 2–3, brows/lids 3 each, mouth 25-frame
  swap library — a pose-swap library, not a dance.
- Foster's Home character reels + Frankie rig (audit row 9):
  long character reels at 24 fps, master-symbol layer stack.
- Scooby-Doo! Mystery Inc. ep. 607 song animatic (audit video
  reference): timing reference only, baked video, not a rig.
- Chowder kit (audit row 4, already extracted): static pattern-fill,
  district colour families, shop-window foreground framing.

### The combined spec — "Space Jones dance scene"
- Tempo / beat grid: master tempo ~107 BPM. At Cape Jones's 24 fps
  clip standard (ANIMATION-SYSTEM.md: 24 fps, on 2s normal, on 1s for
  snaps, holds 6–24 frames), one beat = 13–14 frames (0.54–0.58 s).
  Beat grid is marked on the timeline every 13–14 frames; onlooker /
  background figures get their own beat layer, same grid.
- Keyframing: ON TWOS for the body (12 drawings/sec), ON ONES for
  snaps (kick, twist snap, head turn). Holds: 6 frames (short accent),
  12 frames (beat hold), 24 frames (pose hold, the "flex hold" length
  from the old flex clip).
- Progression (one 8-beat phrase, ~108 frames at 24 fps):
  1. Stride in (2 beats, wide, toward camera, fake-perspective scale
     growing) → 2. Groove (2 beats, hips + shoulders, on twos) →
  3. Kick (1 beat, snap on ones) → 4. Split stance (1 beat, hold 6) →
  5. Twist (2 beats, twist layer, 32-keyframe shape compressed to the
     24 fps grid, torso twist + head counter-turn) → hold 12, return.
- Temperament layer (Mochiichao, as movement data): background figures
  are assigned one temperament each — pack (flock together, Boids),
  skittish (back off on the kick beat), curious (lean in on the twist),
  territorial (hold ground, arms crossed on holds). This is what makes
  the crowd read as alive, not as clones.
- Stamina curve (Mochiichao races): energy starts high, fades in the
  last beat (Endurance fade) — the twist is big, the return is smaller,
  then a breath hold. No flat-energy dancing.
- Kawaii Tamagotchi vibe / Digicore energy (Mars's words for the
  dance-scene source): small, bright, readable, bouncy. In concrete
  terms: (i) bounce on every beat (walkbob-style 0.5s ease, scaled to
  the beat), (ii) sparkle / need-icon-style pops on accent beats
  (shape pops, not text), (iii) colour shifts from the Universe Color
  Language — JoJo tension/power shifts on the twist beat, returning to
  base on the hold, (iv) device beep on the beat (Section 3) as the
  scene's metronome gag. "Kawaii" here means small + bright + bouncy,
  not a Mochiichao creature on screen.
- What the dance is NOT: it is not a copy of Darwin's dance (different
  character, different rig, different slots), it is not a Mochiichao
  creature dance (no Mochiichao species), and it is not a final clip
  yet — this spec must be approved before a clip is built.

## 3. HANDHELD GAG DEVICE — "Mochiichao in his universe" (design only)
Device design done: YES (this section). Device drawing / prop sheet
built: NO — 0/1, owed. Device in a final shot: NO — 0/1, owed.

### The idea, in Mars's words (logged exactly)
Mochiichao is one of Space Jones's things, other than just chilling
in his house, flipping the lights, watching TV, bullshitting, and
playing video games. Mochiichao goes into this universe as a little
handheld pocket video game — like a Game Boy Advance, mixed with a
Tamagotchi. It is "Mochiichao in his universe."

### The gag, logged exactly
It is ALWAYS in his pocket even though he has NO visible pockets.
- Never show a pocket opening, a pocket bulge, or a pocket flap.
- The gag beat is: hand goes to hip / cape fold → device is in hand;
  hand goes back → device is gone. No explanation, no visible pocket.
- A small screen glow from the cape fold, or a beep, can announce the
  device before it appears — the glow/beep is the joke, not a pocket.

### Device design (original prop, Mars's IP on screen, Cape Jones prop)
- Shape: horizontal handheld, Game Boy Advance family — wider than
  tall, rounded corners, screen centred at the top, controls below.
  Tamagotchi mix: a small egg/pet window in the screen corner, plus a
  Tamagotchi-style care row (hunger / happiness / sleep icons, the
  readable-need-icon method from Section 1, row 8).
- Screen: shows the Mochiichao game itself — garden / dance mini-game
  on a tiny screen. This is a game-within-the-show: Mochiichao on the
  screen is fine (Mars's own game); Mochiichao creatures walking around
  Cape Jones's world are not (canon rule, Section 0).
- Controls: D-pad left, A/B buttons right, Start/Select centre, one
  speaker grille, one cartridge slot on the back (never seen in normal
  shots). Buttons are plain shapes, no third-party logo, no
  third-party brand image.
- Colour: Cape Jones universe palette for the shell (white / black /
  purple family, matching his suit + cape), screen in Mochiichao garden
  colours (bright / gold for Bright, black / purple for Umbral — the
  alignment palette method from mochiichao-systems.ts, applied to a
  screen, not to a character).
- How it is drawn in a scene:
  (a) IN HAND, playing: device held in both hands, screen toward
      camera, thumbs on buttons, head tilted down — the "playing video
      games" activity, same as his other house activities.
  (b) POCKET GAG, not playing: hand to hip/cape fold, device appears
      or vanishes off-screen, no pocket drawn.
  (c) DANCE CONNECTION: the device is the scene's metronome — it beeps
      on the beat, its screen flashes on accent beats, and the dance
      mini-game on screen mirrors the big dance (same beat grid,
      Section 2, at tiny scale). That is how the kawaii Tamagotchi vibe
      gets into the dance scene without a Mochiichao creature on stage.
- Space Jones's activity list (context, Mars's words, unchanged):
  chilling in his house, flipping the lights, watching TV,
  bullshitting, playing video games — plus Mochiichao-the-device as
  one more of those things, not a replacement for any of them.

## 4. COUNTS + SOURCES + STILL OWED
- Background-life systems mapped: 10/10 = 100% (spec mappings; code
  status per row in Section 1 — WorldRenderer + garden-data verified
  code, Boids SPEC only, Creature Mode spec only).
- Dance spec: done 1/1 = 100% (Section 2). Dance clip: 0/1.
- Device design: done 1/1 = 100% (Section 3). Device prop sheet: 0/1.
  Device in a final shot: 0/1.
- Sources by name: fresh-start src/world/WorldRenderer.tsx,
  src/lib/garden-data.ts, src/lib/mochiichao-systems.ts,
  src/lib/stacks.ts (boids-stack, SPEC),
  goals/mochiichao-fresh-start-repo/files/chao-garden-conversion.md,
  garden-mode-spec.md, creature-mode-spec.md,
  cape-jones/ANIMATION-SYSTEM.md,
  cape-jones/production/dance-choreo/ (Darwin GB214),
  cape-jones/SHOW-REPO-DEEP-AUDIT-20261031.md (rows 9, 11, Smiling
  Friends, Foster's, Scooby animatic, Chowder kit),
  cape-jones/UNIVERSE-COLOR-LANGUAGE.md (JoJo shifts),
  cape-jones/SHOW-BUILDING-METHOD.md (placeholder → kitbash →
  redesign, transform-only reference).
- Still owed, in order: (1) approve this spec, (2) device prop sheet
  drawing, (3) background-life animation pass for room/street/forest
  using Section 1, (4) dance clip from Section 2, (5) a shot that uses
  the device gag (hand to hip/cape fold, no pocket drawn).
- Nothing in this doc is a final shot, a final clip, or a shipped
  character. Spec + design only, as tasked.
