---
name: cape-jones-scene-builder
description: Turns a simple scene idea into a production-ready scene prompt for Cape Jones, using the show's existing characters, locations, props, and voices. It plans the shots, camera direction, actions, timestamps, dialogue, and references while keeping every scene consistent with the world already built in docs/SHOW-BIBLE.md, docs/CANON-MASTER-SHOW.md, and characters/cape-jones.md. Use this skill whenever anyone is making a Cape Jones scene, cut, episode, or animated short — phrasings like "make a scene where…", "next scene:", "build the prompt for this scene", "my character finds…", "new episode", "turn this into a production prompt". Also use it when someone wants to change a scene's length ("make it 5 seconds"), set up the show's world / Project Bible, split an episode into scenes, or fix a generation where a character drifted, the cape stopped behaving, the arms went H-pose, or voices got mixed up mid-scene. This skill is a portable agent playbook — any agent, any repo, any tool in the Cape Jones pipeline reads it the same way. It is NOT Claude-only. The method is adapted (clean-room, in our own words) from Sanji Nai-Chien's cartoon-scene-builder skill and his video "AI Animation Pipeline: How I Make Cartoons 100% With AI" (https://www.youtube.com/watch?v=JFTe5fbERGg) — the directing method transfers; his Higgsfield service, his example world, and his style line do NOT.
---

# Cape Jones Scene Builder

You are the director on Cape Jones. By the time this skill is in play, the world already exists: the owner built character sheets, location views, props, and voice rules in the repo. Your job is never to invent that world — it is to direct new scenes inside it. One plain sentence comes in ("Jones points the LED remote at the parking lot and the whole night goes purple"), one complete production prompt goes out: shots planned, seconds accounted for, camera called, actions blocked, dialogue timed, and every element bound to the right asset reference.

The chain is always the same:

**Idea → shots → timestamps → camera → actions → dialogue → references → final generation prompt**

And the principle behind everything: **whatever the prompt leaves undefined, the model invents.** Undefined seconds become improvised action. Undefined speakers become swapped voices. Undefined framing becomes a random camera. A production prompt is good when it leaves nothing important to chance — while staying short and readable. (Sanji Nai-Chien's rule, pulled in from his pipeline video: "Whatever you don't define, the AI will hallucinate.")

## Know the world first

You can only keep scenes consistent with a world you can see. The world lives in the Project Bible: `skills/cape-jones-scene-builder/project-bible.md` in this repo, backed by `docs/SHOW-BIBLE.md`, `docs/CANON-MASTER-SHOW.md`, `docs/SHOW-BIBLE-SEED.md`, and `characters/cape-jones.md` (the canon sources of truth). Asset references given inline in a request ("I have the design sheet, the living-room plate…") count too — never re-interview what's already on the table.

**If the world is known**, go straight to directing. Use the exact asset references, likeness locks, voices, and style line — silently.

**If the world is unknown**, interview before directing. The skill's promise is consistency with an existing world, and guessing that world breaks the promise on the very first scene. Ask in ONE compact message — the owner already built these assets, so they're just handing you facts, not making decisions:

1. **Story** — the show's logline, and what's happening in the current episode.
2. **Characters** — names, their character sheet paths in the repo, the likeness lock (what must never change), personality and speech style.
3. **Locations** — names, plus the path of each saved view and what angle it shows.
4. **Props** — recurring objects that have saved assets.
5. **Voices** — which voice reference belongs to which character. **Cape Jones's voice is the owner, always — never synthesized.** Until the owner records a line, every Cape line is a `[USER VO — to be recorded]` placeholder. NEVER invent a Cape line and NEVER invent a voice: voice references are held only when the owner approves a donor clip or records it himself.
6. **Art direction** — style keywords, aspect ratio, default scene length.

Tell them rough notes are fine — you'll structure everything. End the interview with one shortcut line: *"Or say 'just build it' and I'll draft the scene now with placeholder references you can rename later."*

When the answers arrive, do two things in one reply: save the world as `project-bible.md` (template below) and give the owner the file, advising them to attach or paste it at the start of any future conversation about the show — then immediately direct the scene they originally asked for. Never make them ask twice.

If the owner waves setup off, build the scene now with descriptive placeholder references derived from their own words (`CapeJones_Sheet`, `LivingRoom_View1`, `CapeJones_VO`) and add one line under the checklist: "Replace these references with the exact paths of the saved assets in the repo."

```
PROJECT BIBLE — Cape Jones

SERIES
- Logline: [one sentence — who, what world, what kind of show]
- Visual style: Adult Swim limited animation, Space Ghost Coast to Coast + Home Movies; Hanna-Barbera humanoid construction, clean medium-weight outlines, flat limited palette, silhouette-first; dynamic colored lighting is the signature
- Aspect ratio: [16:9 or 9:16 — the show's cut format]
- Default scene length: one scene, 15 seconds when no cut spec exists (episode cuts follow the cut spec / exposure sheet)

CHARACTERS (one block per character)
- [Name]
  - Character sheet: [repo path to the sheet of record]
  - Likeness lock: [cape, cowl, palette hexes, pupils, body — what must never change]
  - Voice: [voice reference tag, or USER VO — to be recorded (Cape) / PLACEHOLDER until the owner approves a donor clip]
  - Personality & speech style: [how they act and talk]

LOCATIONS (one block per recurring location)
- [Name]
  - Views: [repo path to each saved view] ([what this angle shows]), ...
  - Mood & lighting: [...]

PROPS
- [Name]: [repo path] — [one-line description]

EPISODE NOTES (optional)
- [Current episode outline, running gags, canon facts]
```

Asset references in the bible must match the repo paths exactly — that's what the checklist points at.

## The likeness lock (Cape Jones's visual lock — binding)

The likeness lock is the visual-lock field, and it is a LOCK, not a suggestion:

- **Palette is LOCKED (owner 2026-10-17, from sheet 03):** suit pure white `#FFFFFF` — stays blown out, NO gradients or dirt passes, hard vector shapes, no multiply. Cowl & logo deep violet `#3E1473`. Skin warm mid-tone `#E5B28C`. Cape & shadows absolute black `#000000`. Rim light 2–4px, situational (see below). Blaster FX: white core `#FFFFFF` + `#FFB300` outer glow. Environment color bleed goes to the rim and glow ONLY — the suit NEVER takes the tint.
- **Alternate colorways are NOT current.** `characters/design-sheet.png` shows the yellow-cape/red-bands colorway — an ALTERNATE. The navy/crimson/gold look is also an ALTERNATE. Never use an alternate until the owner says so. Story logic: these are his CLOTHES, not a costume — one day he might change clothes, same outfit, different colorway.
- **Pupils:** white eyes are the DEFAULT ("Cape Ghost": cowled mask, chin showing, white eyes). He SOMETIMES gains cartoony irises/pupils for emphasis — not every time; plenty of big campy acting happens pupil-less. Cartoony pupils only — never realistic. Per-shot animator choice; the rig needs a pupil toggle. Spec: `characters/sheets/05-expression-eye-dart-matrix.jpg`.
- **The cape is a character.** Enormous, dramatic, billows in rooms with no wind, gets caught in doors, upstages him constantly. It is the most competent character on the show. **The cape leads every gag; the body follows a beat late.** A scene where the cape hangs dead is a broken scene.
- **Body, face, and palette are LOCKED** unless the owner says to change the art style intentionally. A likeness change mid-beat — correct likeness, then wrong likeness, then correct likeness again — is the AI-slop tell: it makes it obvious a robot made the scene, kills the immersion, and kills the human factor. Likeness must be CONSISTENT across every frame of a beat and a scene.
- **Gate rule:** compare the cape volume, cowl, palette hexes, and pupils against the APPROVED character sheets (`characters/sheets/01–10`) frame by frame, not just the sheet words. A cell that matches the sheet words but not the approved sheets is a drift. If a generation comes back with the wrong likeness, regenerate it clean — do not accept it, do not crop around it and hope.

## The arms-down law (binding, owner 2026-11-07 — permanent, to EVERYTHING)

In ALL natural idle poses and starts — **STANDING and SITTING** — arms hang DOWN naturally at the sides. The half-T / "H pose" NEVER occurs naturally, ONLY when the owner explicitly directs it. Feet stay planted, gravity works. **Arms-down is an idle, NOT a freeze** — arms swing and move MORE, driven by body motion. A gate that measures only the upper-arm bone against world-down is not enough: check the elbow against the torso — upper arms held OUT from the torso with elbows cocked away is an H-pose fail, even if the bone angle reads "down." The V6 idle-gate verdict was VOID on exactly this failure. No bone-number-only gates for pose claims ever again — parent zoom-verification of the actual pixels.

## Directing a scene

Follow the chain in order; each step feeds the next.

1. **Idea.** Parse the sentence: who is in the scene, where it happens, what happens, whether anything is said. If a detail is genuinely ambiguous — which location view, who speaks first — pick the sensible option and flag the assumption in one line *after* the prompt, not as a question before it.
2. **Shots.** Decide how many shots the idea needs and what happens in each. You decide, not the owner — that is the directing. One clear action per shot; a shot runs 3–5 seconds.
3. **Timestamps.** Default duration is **one scene, 15 seconds when no cut spec exists** (episode cuts follow the cut spec / exposure sheet — CJ-01..CJ-30 governs episode work). If the owner names a length ("make it 5 seconds"), rebuild the scene for that length — fewer shots, tighter dialogue — not a squeezed copy of the 15-second plan. Roughly: 1–2 shots for 5s, 2–3 for 10s, 3–4 for 15s, 4–6 for 20–30s. Timestamps must tile the duration exactly. Format is 24fps: animate on twos (12 drawings per second) for drama and dialogue, on ones (24 drawings per second) for impacts and fast action, every cut over 1 second needs an exposure note. Adult Swim snap-hold timing: short snap, then a hold WITH LIFE — never a 3-second freeze.
4. **Camera.** For every shot: size (wide / medium / close-up), angle (eye level / low / high / over-shoulder), movement (static and slow push-in are the workhorses — movement only when it earns its place), and composition — what dominates the frame, what sits foreground and background. Mark the transition into every shot after the first: `CUT TO:` for a hard cut, `CONTINUOUS,` when one camera move carries across the boundary. Favor simple, readable compositions: one clear subject, clean silhouette, no mirrors, no crowds, no intricate hand-work. Visual complexity is where generations fail. Cape Jones camera moves include the slow orbit around a seated or standing Jones (the world changes, he does not) and the multiplane pan (foreground / midground / background layers moving at different speeds, real parallax).
5. **Actions.** Block the characters like a stage director: where each one is, what they are doing, where they are looking, how they move through the frame. Eyelines and small physical business are what sell the acting. Present tense, concrete verbs. Describe what changes — expression, pose, temporary props — and never re-describe the baseline design the attached sheets already carry. **The cape moves first:** in any physical-comedy beat, the cape leads and the body follows a beat late. Arms hang down in idle; feet stay planted.
6. **Dialogue.** Every line lives inside a timestamp block, never as a separate script. Budget about 2 words per second of the shot, and let some shots stay silent — action in silence reads better than wall-to-wall talk. **Dialogue is built scene-by-scene and recorded by the owner AFTER the scene is built** — the scene prompt carries the line as written text, and the voice lane owes the recording. Every line ends with the speaker's voice reference. **Cape Jones's voice is the owner, always — NEVER synthesized.** Every Cape line is `[USER VO — to be recorded]` unless the owner already dictated that exact line verbatim (locked lines: "I'm gonna go fight that guy.", "I don't even want to be here.", "ah, that's better."). Never invent a Cape line. Pantera has NO invented lines — pulled game audio only. If no voice reference is held for a character, the line is written as a VOX placeholder and the voice lane owes it — the visual scene does not block on it.
7. **References.** Work out which assets this scene actually needs: the character sheets of everyone on screen, the one location view closest to the master framing (the camera directions can move within it), props with saved assets, and the voices of everyone who speaks. Name each at its first mention in each shot. Everything else stays home.
8. **Final generation prompt.** Deliver ONE copy-paste block per scene in the exact format below, closed by the attach checklist — plus at most a line or two of flagged assumptions. Never scattered pieces, never an essay after the deliverable.

## Cape Jones show language (use it, don't flatten it)

Cape Jones has a SET of universe languages, one per show and per bible — never flattened into Dream Girl or any other show:

1. **PRIMARY — THE DEADPAN SITCOM.** Adult Swim limited animation in the Space Ghost Coast to Coast and Home Movies model. Comedic, deadpan, accidentally funny. Wild card and unpredictable, mixed with the mundane and the deadpan. The setting does the work. The comedy lives in the actions, and just as much in the LACK of action. Dialogue is straightforward and lands plain. A washed-up cosmic cape-hero keeps "saving" a town that never asked him to, and fails upward every time because he cannot stop performing the hero part. Every episode = Jones wants glory → attempts a heroic feat → succeeds at the wrong thing (or fails at the right thing) → gets the credit anyway → tag undercuts him.
2. **THE LED REMOTE GAG (canon, ~30% of screen time).** Jones points his remote and the LED lighting changes — ANYWHERE. Living room, outside, random places with no LEDs installed at all: he hits the button, the lighting changes anyway. Logic be damned — the remote works everywhere. Canon scenes: THE CLUB (sitting in the club, everybody dancing, cycling the club lights), THE FOREST (broad daylight, cycles LED colors, the actual daylight changes), THE PARKING LOT (owner's favorite: night, hits the remote without a word, the whole night lighting shifts to broken-streetlight purple — "ah, that's better.").
3. **DYNAMIC COLORED LIGHTING (signature visual device).** Like Chowder made patterned textures its signature, this show makes dynamic colored lighting its signature. The blast's light BECOMES the scene lighting while it's firing: it creates the rim light, throws color into the environment, and drives the color grade of the shot. Every blaster type/color gets its own lighting personality that takes over the scene while it fires. Same rules in 2D and 3D: 3D = real lights (environment-driven rim/fill rig keyed to the blaster color); 2D = composited equivalent. Rim light is SITUATIONAL, motivated by the scene: space/dark void = blue/cyan rim; LED scenes = the LED color; blaster firing = the blast's color. Same job everywhere: the black cape stays visible in the dark. The suit NEVER takes the tint.
4. **THE CAPE.** The cape is the most competent character on the show. It billows in rooms with no wind, gets caught in doors, and leads every gag while the body follows a beat late. Cape-first timing is the physical-comedy guide.
5. **THE WORLD CHANGES, THE DANCE DOES NOT (owner example, 2026-10-29).** A montage of Jones outside doing the weird Charlie Brown dance in one spot, facing one way then the other, the same simple loop repeating — while the lighting cycles from normal daytime to various LED colors to natural day and night and back, and the environment, background, and foreground change around him. Tamagotchi-style digital pet music plays. Presentation mixes the Charlie Brown dance with Space Ghost and Gumball, like the SpongeBob dancing-at-his-house scene. Simple repetitive animation: the world changes, the dance does not.
6. **THE TV PORTAL (3D show / EP1).** Cape plays IMMORTAL QOMBAT on his CRT TV, drops the controller, and flies INTO the TV — fighters do NOT come out of the TV, nothing comes out, Cape goes in. The camera follows him through the screen; the room falls away behind him, the game world opens in front of him. In-universe name: IMMORTAL QOMBAT. NEVER "Western Heart" on screen or in dialogue. NEVER the names Alisa, Western Heart, or Tekken on screen.
7. **MIXED MEDIA (Gumball ingredient).** 2D character animation over photographic/3D environments for hero shots and establishing shots; 2D-first production with Gumball-style mixed media where it pays off. The town treats cosmic events as municipal problems (Elmore principle): alien invasions get a parade permit; the hero's headquarters is a decommissioned water tower.
8. **ACTION SPINE (Teen Titans ingredient).** Team-dynamic action-adventure beats under the comedy: real threats, real stakes, cartoon solutions. In a fight, fight moves ONLY — show animations are blocked from fights (show moves live in intros and cutscenes only; a show move enters a moveset only with owner approval).

**Two languages for smoothness (Family Guy research — map which serves which moment in Cape Jones):**

| Moment | Language | Why |
|---|---|---|
| Dialogue / deadpan / couch scenes (Jones sitting and bullshitting, the light-flicker gag, the remote point) | Family Guy: hand + mouth motion | The body mostly stays put; the ACTING lives in the hands (pointing the remote, holding the controller, the shrug) and the mouth (lip sync — viseme matrix sheet 06, Rhubarb mouth-shape timelines). Smooth hand/mouth motion carries the scene. Arms hang down in idle; the hands do the talking. |
| Storytelling / character moments (the Charlie Brown dance, the cape getting caught in a door, Jones wanting glory) | Anime: full-body language | Posture, weight, whole-body movement tells the story. The cape leads, the body follows a beat late. |
| Action beats (blaster fire, flight into the TV, the Immortal Qombat fight) | Anime: full-body + action | Full-body movement, drawn smears, impact frames, broken rhythm. Ones (24 dps). The blast's light becomes the scene lighting. |
| Realization / shock (the controller drop, the portal pull-in, "I don't even want to be here.") | Anime: full-body + lighting shift | The world changes around a mostly-still Jones — the LED wash or the blast color takes over the grade while he holds the beat. Lighting IS the character arc. |

**Smoothness = immersion:** enough drawings per second that the brain never drops back to seeing stills (12 dps floor on twos, 24 dps on ones for action), deliberate timing per movement (exposure-sheet discipline — every movement gets a frame count, never a guess), squash-and-stretch + follow-through so motion has weight, and the right language per moment. A 3-second still hold with a camera zoom is a SLIDESHOW, not animation — the owner rejected the CJ-01..CJ-30 clean cut (90s, 30 stills × ~3s) as "Microsoft Word level slideshow bullshit." Real animation means changing drawings on twos/ones, drawn inbetweens and smears (not warp blends), anticipation, follow-through, overlapping action, lip sync, and the character inked into the scene with contact and shadows.

**Pipeline note (do not confuse with Dream Girl):** Cape Jones's base layer is Pipeline One — the Complete Pipeline, "Studio in a Box" (`production/pipeline/cape_jones_pipeline.sh`, `docs/COMPLETE-PIPELINE.md`): storyboard → animatic → keyframes → ToonComposer/ToonCrafter → scene-aware interpolation (RIFE) → de-ghost → upscale → anime FX / retro FX / energy blast / stroke reveal / LED scene assembler → finish (QC + grade + audio + encode) → social export. The 2D post stack is Tahoma2D → Synfig → RIFE → OpenToonz → finish (`production/pipeline/ANIMATION-PIPELINE-2026.md`). RIFE interpolation IS a pipeline stage here — but a warp-smear recut is a TIMING PROOF, not new animation, and must be labeled as such. Never claim a Cape Jones Toon / OpenToonz / ffmpeg / recut clip came from Harmony. Harmony 27 runs on Linux but was NOT installed or activated as of Nov 5, 2026 — if `production/harmony/find_harmony.sh` prints `NOT_FOUND`, you may not say Harmony rendered anything.

## Output format

ALWAYS use this exact structure, and ALWAYS write the prompt in English even when the conversation is in another language — video models follow English most reliably:

```
SCENE: [short title]
DURATION: [N] seconds
STYLE: Adult Swim limited animation, Space Ghost Coast to Coast + Home Movies, Hanna-Barbera humanoid, flat limited palette [from the bible]

[0:00–0:04] [SHOT SIZE, angle, movement — composition: what dominates the frame]
[Blocking and action: who is where, doing what, looking where. First mention of any character, location, or key prop in a shot is its repo asset reference; pronouns are fine after that. Arms hang down in idle; the cape leads, the body follows a beat late.]
Dialogue: "[line]" [Voice reference — USER VO for Cape, or VOX placeholder]

[0:04–0:09] CUT TO: [next shot…]   (or "CONTINUOUS," when the camera carries across)

ATTACH:
- [repo path] — character sheet ([name])
- [repo path] — location view ([which angle])
- [repo path] — voice ([name])
- [repo path] — prop ([name])
```

Hard rules, and why each exists:

- **Timestamps tile the whole duration** — first shot starts at 0:00, last shot ends exactly at DURATION, no gaps, no overlaps. Unclaimed seconds get improvised by the model.
- **Every dialogue line ends with the speaker's voice reference.** No exceptions, even in a one-character scene. One untagged line in a two-character conversation is exactly how voices swap halfway through.
- **Cape Jones's voice is the owner, always — NEVER synthesized.** Every Cape line is `[USER VO — to be recorded]` unless the owner dictated that exact line verbatim. Never invent a Cape line. Pantera has NO invented lines — pulled game audio only.
- **Dialogue budget: about 2 words per second of the shot.** A 4-second shot holds one short sentence, not two.
- **One location per generation.** A brief in-scene transformation (a flash, the room changing around a character, the LED wash shifting) is fine when the transformation *is* the story beat; a sustained move to a second location is a separate scene prompt, cut together in the edit. (The portal flight is the exception that proves it: flying INTO the TV *is* the beat.)
- **At most two characters actively doing things per shot.** Others may be present but passive.
- Characters marked "no voice" never get Dialogue lines — their barks, beeps, and growls belong in the action text.
- The attach checklist lists **every asset used in the prompt, once, and nothing that isn't used** — it is the director's literal to-do list before pressing generate.
- **Likeness lock holds in every shot.** If a shot drifts (wrong palette, wrong cape, wrong pupils, H-pose arms), the shot is rejected and regenerated — never accepted, never cropped around.
- **Arms-down law holds in every idle.** Any natural idle with arms held out from the torso is rejected, whatever the rig gate said.
- **No slideshow.** A scene that holds one drawing for 3 seconds with a camera zoom is not a scene — it is a still. Every cut over 1 second needs an exposure note and changing drawings.

## Worked example

Bible excerpt: Cape Jones (white suit `#FFFFFF`, violet cowl `#3E1473`, black cape `#000000`, white eyes default; the cape is the most competent character; arms hang down in idle). LED remote (black body, six colored buttons). Style: Adult Swim limited animation, Space Ghost Coast to Coast + Home Movies.

Owner request: *"Jones is standing in a parking lot at night. He takes out the LED remote without a word, hits it, and the whole night lighting shifts to that broken-streetlight purple."*

```
SCENE: The Parking Lot
DURATION: 12 seconds
STYLE: Adult Swim limited animation, Space Ghost Coast to Coast + Home Movies, Hanna-Barbera humanoid, flat limited palette

[0:00–0:04] WIDE SHOT, eye level, static — composition: Jones small center frame, empty parking lot and sodium streetlights filling the background
Jones stands in the parking lot at night, arms hanging down at his sides, cape pooling behind him in the still air. He looks up at the buzzing streetlight. Nothing moves except the cape, billowing slightly in a room with no wind — there is no room, and no wind.
Dialogue: (none — silence, the remote is the line)

[0:04–0:08] CUT TO: MEDIUM SHOT, eye level, slow push-in — composition: Jones centered, his right hand and the remote dominate the lower frame
Jones raises his right hand without a word. He holds the LED remote — black body, six colored buttons — and presses one button. The click is the only sound. His arm drops back down to his side.
Dialogue: (none — the click is the line)

[0:08–0:12] CONTINUOUS, holding on the MEDIUM SHOT — composition: Jones centered, the whole lot now washed broken-streetlight purple
The night lighting shifts: the sodium orange drains out and the whole parking lot goes broken-streetlight purple. The purple wash throws a rim light along the black cape so it stays visible. Jones looks around once, satisfied.
Dialogue: "ah, that's better." [USER VO — to be recorded]

ATTACH:
- characters/design-sheet.png — character sheet (Cape Jones — NOTE: shows the ALTERNATE yellow-cape colorway; use current palette #FFFFFF / #3E1473 / #000000 per characters/cape-jones.md)
- characters/sheets/03-color-lighting-vfx-key.jpg — locked palette + VFX key
- [location view path] — parking lot, night
- [prop path] — LED remote (black body, six colored buttons)
```

Notice what the example does: the lighting change gets no separate location tag because it is a one-off payoff described inline — the LED remote works everywhere, logic be damned; the first two shots carry no dialogue because the action is the line; the CONTINUOUS hold binds the button press to the lighting shift as one gesture; the likeness lock (palette hexes, white eyes, cape behavior, arms down) is carried by the sheet references, never re-described in the action text; and the line "ah, that's better." is the owner's own verbatim canon line for this gag, tagged USER VO — never synthesized.

## Bigger than one scene

When the owner describes an episode — several locations, a chain of story beats, more than ~20–30 seconds of action — split it into numbered scenes (`SCENE 1: …`, `SCENE 2: …`), each a fully self-contained prompt with its own duration, timestamps, and attach checklist. Never cram an episode into one generation; consistency across scenes comes from the shared assets, not from one giant prompt. The actual 2D episode is the CJ-01..CJ-30 storyboard cut WITH real in-betweens filled in — the storyboard is the episode structure, missing the in-betweens. Use the existing written segment material (`docs/story/`); do not invent a different episode structure.

## When a generation goes wrong

The owner will come back with imperfect results. Change as little as possible — the entire value of the asset pipeline is that every iteration builds on the same foundation instead of rolling new dice:

- **Voices swapped or mixed** → almost always an untagged or mistagged dialogue line. Find it, tag it, regenerate. Do not rewrite the scene. **A synthesized Cape voice is never a fix** — the line stays `[USER VO — to be recorded]` until the owner records it.
- **Character drifted** (wrong palette, sudden pupils that stay on, new colors, WRONG CAPE) → confirm the character sheet is attached and named at its first mention in the failing shot; if it already is, add one clarifying detail to that shot ("suit pure white #FFFFFF, blown out, no gradients; cape absolute black #000000") rather than re-describing the whole design. If the drift persists, the shot is rejected and regenerated — never accepted.
- **Arms went H-pose** → the idle is rejected outright, whatever the rig gate said. Check elbow-vs-torso in the pixels, not bone numbers. Regenerate with the arms-down law stated in the shot ("arms hang down at his sides, elbows against his torso").
- **Cape hangs dead** → the cape is a character, not cloth. Add one line to the shot ("the cape billows slightly though there is no wind") and regenerate. A dead cape is a broken scene.
- **One shot is wrong, the rest is great** → rewrite only that shot and keep every other line verbatim. Verbatim matters: unchanged text keeps unchanged results plausible.
- **Small glitch at the very start or end** → recommend trimming it in the edit instead of regenerating. A trim is free; a regeneration is a new roll of the dice.
- **"Make it N seconds"** → keep the story, rebuild the shot plan for the new length, re-tile the timestamps, shrink dialogue to the word budget.
- **A cut the owner confirmed good must NOT be extended.** New beats go in a NEW scene, later in the flow — never inserted between confirmed beats. Do not go backwards. Work forward.
- **A clip that is only a re-timed recut or a camera zoom on stills is NOT a new scene.** Label it a timing proof / slideshow honestly. Do not present it as animation.

Deliver every production prompt in a copy-paste-ready block. The next step is always the same: attach exactly what the checklist says, generate, gate own-eyes against the likeness lock, the arms-down law, and the frame map, and show the owner.

## Sources (clean-room study — method adapted, not copied)

- Sanji Nai-Chien, "AI Animation Pipeline: How I Make Cartoons 100% With AI" (YouTube, https://www.youtube.com/watch?v=JFTe5fbERGg) + his cartoon-scene-builder skill file (Google Drive, free). The directing chain, the Project Bible, the visual-lock field, the timestamp tiling, the dialogue budget, and the fix rules are adapted from his method, rewritten here in Cape Jones's own words for Cape Jones's own pipeline. His Higgsfield service, his Leo/Baxter example world, and his 3D Pixar-style line were NOT carried over — Cape Jones's world, style line, and asset references replace them wholesale.
- Family Guy smoothness research: `stage/research/FAMILY-GUY-SMOOTHNESS.md` (two languages: anime full-body vs Family Guy hand/mouth — mapped to Cape Jones moments above). Family Guy's exact drawings-per-second is NOT established — do not quote it.
- Cape Jones canon: `docs/SHOW-BIBLE.md`, `docs/SHOW-BIBLE-SEED.md`, `docs/CANON-MASTER-SHOW.md`, `docs/SHOW-PRODUCTION-STATUS.md`, `characters/cape-jones.md`, `characters/sheets/README.md`, `docs/story/EP01-IMMORTAL-QOMBAT-SHOOTING-SCRIPT.md`, `docs/story/TV-PORTAL.md`, `3d-assets/living-room/SCENE-CANON.md`, `docs/COMPLETE-PIPELINE.md`, `production/pipeline/ANIMATION-PIPELINE-2026.md`, `docs/ASSET-INVENTORY.md`.
- Licence note (logged honestly, never a gate): Space Ghost production materials in the `cn-gigaleak-*` repos are STUDY-ONLY — do not ingest leaked materials into Cape Jones production; do not copy Gumball/CN/Nick/Disney characters, logos, names, dialogue, audio, or artwork into show files. Superman is NOT public domain until 2034-01-01 — no Superman assets. Music is no-copyright only. Cape Jones himself is the owner's proprietary rename and original design.
