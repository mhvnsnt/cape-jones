# PROJECT BIBLE — Cape Jones

> The world the `cape-jones-scene-builder` skill directs inside. Canon sources of truth: `docs/SHOW-BIBLE.md`, `docs/SHOW-BIBLE-SEED.md`, `docs/CANON-MASTER-SHOW.md`, `characters/cape-jones.md`, and `docs/story/EP01-IMMORTAL-QOMBAT-SHOOTING-SCRIPT.md` in the `mhvnsnt/cape-jones` repo. If anything here conflicts with those docs, the docs win — flag the mismatch, never propagate it. Anything not in the repo docs is marked TBD — never invented.

## SERIES

- **Logline:** A washed-up cosmic cape-hero keeps "saving" a town that never asked him to, and fails upward every time because he cannot stop performing the hero part.
- **Title:** EP1 (3D show) — "IMMORTAL QOMBAT." The 2D show's episode is the CJ-01..CJ-30 storyboard cut with real in-betweens filled in.
- **Visual style:** Adult Swim limited animation in the Space Ghost Coast to Coast + Home Movies model. Hanna-Barbera humanoid construction, clean medium-weight outlines, smooth confident arcs, flat limited palette, silhouette-first. Gumball-style mixed media (2D characters over photographic/3D environments) for hero shots and establishing shots where it pays off. Signature visual device: DYNAMIC COLORED LIGHTING — the blast's light becomes the scene lighting while it fires.
- **Tone (owner, in his own words, 2026-10-29):** Comedic, deadpan, accidentally funny. Wild card and unpredictable, mixed with the mundane and the deadpan. The setting does the work. The comedy lives in the actions, and just as much in the lack of action. The dialogue is straightforward and lands plain. It lives in the show's writing, gags and canon, and across the whole network umbrella of the owner's shows, all of it in Space Ghost tone and language.
- **Format:** 11-minute episodes (from the Gumball bible: "THE 36X11 MINUTES SERIES"), animated sitcom following misadventures. 2D-first production with Gumball-style mixed media where it pays off. The 3D show's EP1 is the TV-portal origin (see Episode Notes).
- **Comedic engine:** the protagonist's flaw generates every episode. Cape Jones's flaw: he needs an audience more than he needs a rescue. Every episode = Jones wants glory → attempts a heroic feat → succeeds at the wrong thing (or fails at the right thing) → gets the credit anyway → tag undercuts him.
- **Aspect ratio:** 16:9 (episode material: 1920×1080, 24 fps; animatic 1920×1440, 24 fps). Social exports: TikTok 9:16, IG 1:1, IG 4:5.
- **Default scene length:** one scene, 15 seconds when no cut spec exists. Format: 24fps; animate on twos (12 drawings per second) for drama and dialogue, on ones (24 drawings per second) for impacts and fast action; every cut over 1 second needs an exposure note. Adult Swim snap-hold timing: short snap, then a hold WITH LIFE — never a 3-second freeze.
- **Master-show canon (owner 2026-11-05, binding):** Cape Jones is the master show and the TEST GROUND for every pipeline (2D, 3D, game, software, animation, show). Get ONE production pipeline perfected and hardened here first — that pipeline is the template for every other project. Everything else converges into Cape Jones as parody / in-universe versions inside the Cape Jones multiverse. Other games and shows appear in Cape Jones show style.

## CHARACTERS

### Cape Jones — LEAD
- **Character sheet:** `characters/design-sheet.png` (full-body, white void, full arm reach with margin — own-eyes verified). **WARNING: the design sheet shows the ALTERNATE yellow-cape/red-bands colorway, NOT the current palette.** The 10 locked build-spec sheets are `characters/sheets/01-tpose-turnaround.jpg` through `10-hero-in-space.jpg` (see below).
- **Likeness lock:** Washed-up cosmic cape-hero, still performing like it's his premiere. **Body gag (one exaggeration, committed fully): THE CAPE** — enormous, dramatic, billows in rooms with no wind, gets caught in doors, upstages him constantly. The most competent character on the show. **Want:** to be watched being heroic. **Flaw:** performs heroism instead of doing it. **Powers:** flight, power-band blasts (wrist bands), cosmic durability — all real, all deployed at the wrong moment for the wrong reason. Hand cannons like Mega Man / Android 16 (3D model canon). **Pupils:** white eyes are the DEFAULT ("Cape Ghost": cowled mask, chin showing, white eyes). He SOMETIMES gains cartoony irises/pupils for emphasis — not every time; plenty of big campy acting happens pupil-less. Cartoony pupils only — never realistic. Rig needs a pupil toggle; per-shot animator choice. Spec: `characters/sheets/05-expression-eye-dart-matrix.jpg`.
- **Locked palette — CURRENT (owner 2026-10-17, from sheet 03 `characters/sheets/03-color-lighting-vfx-key.jpg`):** suit pure white `#FFFFFF` (stays blown out, NO gradients or dirt passes, hard vector shapes, no multiply); cowl & logo deep violet `#3E1473`; skin warm mid-tone `#E5B28C`; cape & shadows absolute black `#000000`; rim light 2–4px, situational (space/dark void = blue/cyan; LED scenes = the LED color; blaster firing = the blast's color); blaster FX white core `#FFFFFF` + `#FFB300` outer glow (color dodge/add). Environment color bleed goes to rim + energy glow ONLY — the suit NEVER takes the tint.
- **Alternate colorways (design history — NOT current, never use until the owner says so):** yellow-cape / red-bands (`characters/design-sheet.png`); navy cape + crimson lining + gold power bands + black domino mask with glowing yellow eyes (the v1 likeness anchors were written against this colorway — kept for design history). Story logic: people think his look is a superhero costume, but these are just his CLOTHES — one day he might change clothes (same outfit, different colorway). The 3D outfit is built as a recolorable system (material slots per colorway).
- **Locked sheets (`characters/sheets/`, owner 2026-10-17):** 01 T-pose turnaround (construction baseline); 02 orthographic model-sheet turnaround; 03 color/lighting/VFX key (LOCKED PALETTE); 04 action/flight/VFX reference; 05 expression + eye-dart matrix (pupil canon); 06 viseme/phoneme mouth matrix (dialogue rig spec); 07 character parts + expression variants; 08 body parts, limbs, cape variants (hands = priority zone); 09 hero shot on black (rim-light read test); 10 hero in space (situational rim-light reference).
- **Voice:** THE OWNER, ALWAYS. `[USER VO — to be recorded]` on every line. NEVER synthesized. Big, theatrical, mid-century hero-announcer cadence — undercut constantly by the cape and the sidekick. Voice casting is the owner's call. Locked verbatim lines (owner-dictated): "I'm gonna go fight that guy." / "I don't even want to be here." / "ah, that's better."
- **Catchphrase:** TBD by owner. (Bible premise #6 is the in-show origin of it.)
- **Personality & speech style:** Deadpan, straightforward, lands plain. A Space Ghost / Batman-type who does NOT want to fight or be a hero — he only fights because everyone thinks he looks like a superhero. "I don't even want to be here." is his whole character in one sentence.
- **Arms-down law (owner 2026-11-07, permanent, to EVERYTHING):** in ALL natural idle poses/starts — STANDING and SITTING — arms hang DOWN naturally; half-T / H pose NEVER occurs naturally, ONLY when the owner explicitly directs it. Feet stay planted, gravity works. Arms-down is idle, NOT freeze — arms swing/move MORE, driven by body motion. Gate on elbow-vs-torso in the pixels, never bone numbers alone (V6 idle-gate verdict VOID on this failure).

### Pantera — EP1 fighter (Immortal Qombat)
- **Character sheet:** TBD — best rig on the roster (owner-confirmed 2026-10-23); rig-quality order casts him first. No sheet path is locked in the repo docs as of Nov 2026 — confirm the current rig file before directing a Pantera scene.
- **Likeness lock:** Black panther, yellow eyes, black tail, purple tights, red PANTERA metal lettering, thigh tattoo-panther. Fights because fighting is what he is; predatory patience. "The mat is here. I am here." In the fight he uses a chain grapple (King-style chain-throw sequence in technical notes — in-universe it is simply Pantera's chain grapple, never named after another game's fighter).
- **Voice:** PULLED GAME AUDIO ONLY — Tekken 6 character voice bank (pending; acquisition BLOCKED as of 2026-10-24 — see `docs/research/EP1-PANTERA-VOICE-TRACK-G-2026-10-24.md`). NO invented lines. His "lines" are growls, roars, and grunts from the character voice bank, not spoken words. CORRECTION: the `F_KING` stage voices are stage sounds/music/SFX, NOT King dialogue — do NOT use as dialogue.
- **Personality & speech style:** Patient, unbothered predator. Waits the way a predator waits. EP1 outcome (owner-decided 2026-10-24): PANTERA WINS — one-hit-left comeback, chain grapple finishes Cape.
- **Fight rule:** In a fight, fight moves ONLY. Cape fights with his hand cannons and reluctant-hero physicality. Never put the names Alisa, Western Heart, or Tekken on screen.

### Supporting cast (2D sitcom) — SLOTS ARE PLACEHOLDERS, NOT CANON
Cast is locked by the owner only. The six slots below are production placeholders from the Johnny Bravo template — do NOT treat any of them as a named canon character:
- **1. The Straight-Man Sidekick** — sees every failure clearly; never believed.
- **2. The Rival Hero** — actually competent; gets no credit.
- **3. The Fan** — a kid who thinks Jones hung the moon; the show's heart.
- **4. The Nemesis** — petty, small-time; Jones inflates him into an arch-villain.
- **5. The Cape** — not a joke slot; the cape gets physical-comedy sequences.
- **6. The Authority** — mayor/chief who keeps hiring Jones because the paperwork is easier.
- **Voice casting for all six:** TBD — owner's call. No voice references held.

## LOCATIONS

### Cape's living room — the 3D show anchor (SCENE CANON, owner-approved 2026-10-16)
- **Views:** `3d-assets/living-room/` — `colorway-reference.png` (owner-approved front view), `scene-overview.png` (3/4 view from the open front side), `scene-rev2-capejones-front.png`, `scene-rev2-window-wall.png`, `scene-rev3-window-wall.png`, `scene-rev3-lamp-closeup.png`, `scene-rev2-mug-closeup.png`. Build: `3d-assets/living_room.blend`.
- **Mood & lighting:** Coral-pink furniture + warm oak wood on a dark floor, all soaked in violet LED glow (`#731AE5`). Coral-pink recliner `#F15E57`, blue sofa `#5B84DD`, warm bone walls `#D1C7B8`, dark warm-brown floor `#735238`, oak `#E59964`, cool silver metal `#BDD2D6`, lamp amber `#FFE996`. LED strips emission `#731AE5` strength 4.0; `RoomLight` POINT energy 300 color `#731AE5` (dominant light); `Sun` fill 1.5 white. World background near-black `#0D0D0D`. Room shell 7.0 × 6.0 m, walls 3.0 m high.
- **Canon furniture:** coral-pink recliner by the window wall (round rug under it), blue sofa, coffee table, CRT TV + rabbit ears on oak console (`crt_tv` + `crt_screen` + antennae; screen emission `#731AE5`), VCR/DVD player, monster toy (canon-blue, bottom shelf), side table with the WORLD'S OKAYEST HERO mug, bookcase, floor + table lamps, LED remote on the coffee table, FRY EM UP poster, squid wall hanging, framed ghost picture, doorway + hallway stub, window with exterior diorama.
- **Canon note:** the recliner stays EMPTY until the light-flicker gag rig lands (owner 2026-10-16). Do NOT place the character in the room yet in canon builds — scenes that seat him must note the gag rig as the dependency.

### The town (2D sitcom world)
- **Views:** TBD — no saved town views are locked in the repo docs as of Nov 2026.
- **Mood & lighting:** A mid-size town that treats cosmic events as municipal problems (Gumball's Elmore principle). Alien invasions get a parade permit. The hero's headquarters is a decommissioned water tower.
- **Canon:** universe-ending threats, handled like a parking dispute.

### The club / the forest / the parking lot (LED remote gag canon scenes)
- **Views:** TBD — no saved views locked in the repo docs as of Nov 2026.
- **Mood & lighting:** THE CLUB: everybody dancing, Jones cycling the club lights with the remote. THE FOREST: broad daylight, LED colors cycling, the actual daylight changes. THE PARKING LOT (owner's favorite): night, one remote click, the whole night lighting shifts to broken-streetlight purple.

### Jungle Outpost — the Immortal Qombat arena (EP1)
- **Views:** TBD — T7 extraction arena (NOT a Tekken 3 arena; owner-picked 2026-10-24 — T3 arenas are "scrambled").
- **Mood & lighting:** Dense green jungle outpost, temple/outpost structures, wide and readable. No crowd characters; the arena's own dressing carries the space. Fitting for Pantera: a panther in his jungle.

### Space / dark void
- **Views:** `characters/sheets/10-hero-in-space.jpg` (rim-light reference), `09-hero-shot-black.png` (rim-light read test).
- **Mood & lighting:** Blue/cyan rim flying around the black cape so it stays visible in the dark.

## PROPS

- **LED remote:** black body `#0D0D0D`, six colored buttons (red `#FF0000`, green `#00FF00`, blue `#0000FF`, yellow `#FFFF00`, magenta `#FF00FF`, cyan `#00FFFF`, emission 1.5 each). Canon gag: it works EVERYWHERE, logic be damned (~30% of screen time). Lives on the coffee table (`3d-assets/living-room/`).
- **Power-band blasters / hand cannons:** gold wrist bands (alternate-colorway anchor; current-palette band color follows sheet 03). Blaster FX: white core `#FFFFFF` + `#FFB300` outer glow. Every blaster type/color gets its own lighting personality that takes over the scene while it fires.
- **Controller:** the game controller Cape drops in EP1 Scene 4 — the episode's turn ("I'm gonna go fight that guy.").
- **CRT TV + rabbit ears:** violet screen glow (`tvScreenMat` emission `#731AE5` strength 1.5). The portal: Cape flies INTO it, never the reverse.
- **WORLD'S OKAYEST HERO mug:** on the side table by the recliner (close-up verified).
- **The cape:** not a prop — a character. Billows with no wind, gets caught in doors, leads every gag.
- **Immortal Qombat title card:** "IMMORTAL QOMBAT" + kanji 不死 (*fushi* — "immortality; eternal life"; owner to confirm the "undeath" shade is acceptable). The stylized Q opens into the word "Qombat." NEVER "Western Heart" on screen.

## UNIVERSE LANGUAGES (one set, never flattened)

1. **PRIMARY — THE DEADPAN SITCOM.** Adult Swim limited animation, Space Ghost Coast to Coast + Home Movies. The setting does the work; the comedy lives in the actions and the lack of action.
2. **THE LED REMOTE GAG.** The remote changes the world's lighting anywhere, logic be damned. ~30% of screen time.
3. **DYNAMIC COLORED LIGHTING.** The signature: blast light becomes scene lighting; rim light is situational and motivated. The suit never takes the tint.
4. **THE CAPE.** The most competent character; cape-first physical comedy — the cape leads, the body follows a beat late.
5. **THE WORLD CHANGES, THE DANCE DOES NOT.** The Charlie Brown dance montage: one simple loop repeating in one spot while lighting, environment, background, and foreground change around him. Tamagotchi-style digital pet music.
6. **THE TV PORTAL.** Cape flies INTO the TV; fighters never come out. In-universe name IMMORTAL QOMBAT only.
7. **MIXED MEDIA.** 2D characters over photographic/3D environments for hero and establishing shots (Gumball ingredient).
8. **ACTION SPINE.** Real threats, real stakes, cartoon solutions (Teen Titans ingredient). Fight moves only in fights.

## EPISODE NOTES

- **EP1 "IMMORTAL QOMBAT" (3D show) — OWNER-APPROVED 2026-10-24 (PR #234, merged as 688bcacc).** Shooting script: `docs/story/EP01-IMMORTAL-QOMBAT-SHOOTING-SCRIPT.md`. 6 scenes + tag: (1) living room, sitting in the recliner, LED flicker gag, no dialogue; (2) LED remote, CRT wakes, channel-flips through the owner's own shows (TRIPPEDD, wizard gang, bumps/cards/commercials; most recent El Toro De Oro + Stick Up entrance kits); (3) title card IMMORTAL QOMBAT + 不死, the Q opens; (4) plays, drops the controller — "I'm gonna go fight that guy."; (5) stands, CRT flicker, flies INTO the TV (`portal_02_pull_in`); (6) Jungle Outpost arena, Pantera waiting — "I don't even want to be here." — fight, PANTERA WINS (one-hit-left comeback, chain grapple). Tag TBD. Cast: Cape + Pantera only. No crowd, no narrator. Music: no-copyright only (Loyalty Freak Music, CC0 1.0 — attribute, do NOT activate Content ID, do NOT distribute to streaming).
- **2D episode = CJ-01..CJ-30 storyboard + real in-betweens (binding, owner 2026-11-05).** The 90s clean cut (`episode-cj01-cj30-clean-20261101.mp4`, PR #354) is a SLIDESHOW — 30 stills × ~3s camera zooms, 0/30 dialogue — owner-rejected as "Microsoft Word level slideshow bullshit." Do NOT call it an episode. The animatic (`cape-jones-animatic-CJ01-CJ30-20261031.mp4`, 1920×1440, 24fps, 13.833s) is the storyboard. The job is filling in the in-betweens from the existing written segment material (`docs/story/`), not inventing a different episode structure.
- **Premises (first 8, from `docs/SHOW-BIBLE.md` §6 — formula: [Jones wants X] + [attempts Y] + [fails due to own flaw] + [tag]):** (1) wants a parade → "stops" a meteor (already burning up) → town parades the meteor → tag: the cape gets the key to the city. (2) wants a nemesis → inflates a parking-ticket villain → villain leans in → tag: they do a podcast together. (3) wants a sidekick → auditions → picks the only applicant who boos him → tag: the kid is right about everything. (4) wants merch → cape gets its own action figure → Jones's figure is the accessory → tag: cape outsells him 40:1. (5) wants a day off → real threat shows up → town handles it without him → tag: he takes credit in the group photo. (6) wants a catchphrase → every attempt is taken → settles on one in another language he can't pronounce → tag: it means "plumber." (7) wants the rival's respect → hero-duel → loses theatrically → tag: the crowd loved the theater. (8) wants to retire → nobody notices for a week → tag: the cape kept working. Pilot pick is the owner's call.
- **Canon gags (owner-logged):** LED remote gag (canon 2026-10-17, ~30% of screen time); light-flicker couch gag (living-room couch, lighting flickers/misfires around him while he sits and bullshits); cape-got-there-first.
- **In-universe mappings (owner 2026-11-05 — ONLY these two):** Immortal Qombat = Western Heart; Mochiichao handheld game + Mochiichao-related segments in Cape Jones show style. No other mappings are canon. Do not create them without an owner decision.
- **Immortal Qombat fight casting/motion law (owner 2026-11-05):** Pantera must be the most updated, most corrected version with the most moves and latest animations. Cape Jones must use his most updated 3D show rig that can pose and fight, with Alisa's full moveset/animations/fight data attached to him in the cape-jones repo (linked on the Western Heart side) — in the fight he uses Alisa's moves. NEVER put the names Alisa, Western Heart, or Tekken on screen. Do not use an old Cape mesh or a clay/Blender chain proof as the fight (`ep1_chain_170_195.mp4` is bare clay junk, NOT valid fight footage).
- **Honest status (snapshot Nov 5, 2026, `docs/SHOW-PRODUCTION-STATUS.md`):** there is real 2D material in the repo; there is NOT a finished voiced, fully animated episode. 0/30 lines recorded for the CJ-01..CJ-30 clean cut. In-betweens for CJ-01..CJ-30 not drawn. Immortal Qombat fight not yet pulled from Western Heart. Harmony 27 runs on Linux but is NOT installed/activated (`production/harmony/find_harmony.sh` → `NOT_FOUND`); do not claim Harmony rendered anything. Rhubarb 1.14.0 installed but no recorded dialogue to sync. Dance V1 (`dance-scene-V1-EN-FINAL-20261101.mp4`) is a SEGMENT only, not the episode. Hallway parody (`cape-jones-hallway-parody-20261102.mp4`, PR #372): owner verdict 2026-11-09 — Cape Jones is NOT THE RIGHT SIZE in it; STOP ORDER — it stays as-is, banked in `production/dance-choreo/parody/`. 2D dance decision (owner 2026-11-09): RETRY THE 2D VACE PASS WITH TWEAKED/DIFFERENT SETTINGS.
- **Pipeline One (base layer, `docs/COMPLETE-PIPELINE.md` + `production/pipeline/ANIMATION-PIPELINE-2026.md`):** "Studio in a Box" — `production/pipeline/cape_jones_pipeline.sh`: storyboard → animatic → keyframes → ToonComposer/ToonCrafter → scene-aware RIFE interpolation → de-ghost → upscale → anime FX / retro FX / energy blast / stroke reveal / LED scene assembler → finish (QC + grade + audio + encode) → social export. 2D post stack: Tahoma2D → Synfig → RIFE → OpenToonz → finish. A warp-smear recut is a TIMING PROOF, not new animation — label it honestly.
- **Voice refs held:** Cape = owner records (0/30 EP1 lines recorded as of Nov 5). Pantera = pulled audio only, acquisition BLOCKED. All other voices: TBD, owner's call. Voice tags in any scene prompt are PLACEHOLDERS until the owner records or approves a donor clip. Never invent a voice, never synthesize Cape's.
- **Skin-tone / body fidelity:** hold the locked palette and the real build; never recolor the suit, never tint it with the environment, never slim or reshape the character.
- **A cut the owner confirmed good must NOT be extended.** New beats go in a NEW scene, later in the flow — never inserted between confirmed beats. Work forward.
- **Licence note (logged honestly, never a gate):** Space Ghost production materials in the `cn-gigaleak-*` repos are STUDY-ONLY — do not ingest leaked materials into production; do not copy Gumball/CN/Nick/Disney characters, logos, names, dialogue, audio, or artwork into show files. Superman is NOT public domain until 2034-01-01. Teen Titans repo is README-only as of 2026-10-15 (action-tone notes pending). Music is no-copyright only. Cape Jones himself is the owner's proprietary rename and original design.

## TBD (open owner decisions — do NOT fill in silently)

- Supporting-cast names and designs (slots 1–6 are placeholders; cast locked by owner only).
- Pilot premise pick (8 premises locked; owner picks or orders a new one).
- Cape Jones catchphrase (premise #6 is its in-show origin).
- Town / water-tower HQ / club / forest / parking-lot / Jungle Outpost saved location views.
- Pantera's current rig file path for scene work.
- Pantera voice-bank acquisition (BLOCKED — owner decision: PPSSPP lane, labelled non-T6 replacement, or owner-supplied files).
- EP1 runtime, tag, and exact channel-flip clip picks (production lock).
- Teen Titans action-tone pass (repo README-only as of 2026-10-15).
- Harmony Linux install + activation (owner's Toon Boom account; unblocker in `docs/SHOW-PRODUCTION-STATUS.md` §5).
