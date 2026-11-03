# Gumball scene templates — the complete-scene library

Owner's program (2026-11-02): every complete animated scene in the Gumball production holdings, logged into this repo fully deconstructed — every FLA piece, background, animation, rig, seam and technique labeled — as reusable template work for Cape Jones production. Built with the wired stack: JPEXS FFDec (renders/video), XFL structure parsing (the FLA is a zip of XML), and the dance-choreo neutral JSON format.

**The library: 31 complete animated scenes** (the wave-1 survey of all 71 FLAs in `CN-Leaks-001-gumball.zip` found 31 complete / 11 partial / 28 static / 1 unverified — the survey table is preserved at the bottom of this file). Deconstructed: **31/31** · contact sheets: **31** · videos: **31**.

## How to recall a scene

`CATALOG.json` is the machine-readable index — one record per scene with cast, backgrounds, rigs, animation counts, seams, technique tags and media status. It answers questions like:

- *every scene with a per-character mask* → filter `tags` for `per-character-mask`
- *every scene Tina appears in* → filter `cast` for `Tina` (Tina appears in none of the 31 — she is not in this archive's complete scenes; the Wattersons plus Penny/Carrie-class puppets live in the static rig files)
- *every scene reusing the school hallway plate* → `shared_backgrounds` in CATALOG.json

Each scene folder holds `scene-anatomy.json` (library standard v2: layer stack with per-layer contents, named cast with the puppet/rig identity for each character, backgrounds census, animations census, seams, evidence-tagged techniques), `NOTES.md` (what the scene teaches, in plain words), `contact-sheet.png` and `video.mp4` (native fps/resolution, production audio kept where the SWF exports a sound asset).

## The 31 scenes, by episode

### GB202 "The Remote"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc094](scenes/gb202-remote-sc094/) | 56 | Nicole | nested-master-symbol, layout-mov-reference, photo-plate | done | done |
| [Sc103](scenes/gb202-remote-sc103/) | 141 | Darwin, Gumball, Richard | run-cycle-library, layout-mov-reference, face-comp-driven, multi-character-staging | done | done |
| [Sc108](gb202-remote-sc108/) | 40 | Darwin, Gumball | run-cycle-library, layout-mov-reference, face-comp-driven, forced-perspective, speed-smear, cycle-multi-scale | done | done |
| [Sc144](gb202-remote-sc144/) | 262 | Darwin, Gumball, Nicole, Richard | nested-master-symbol, run-cycle-library, layout-mov-reference, multi-character-staging | done | done |
| [Sc147](scenes/gb202-remote-sc147/) | 147 | Darwin, Gumball, Nicole, Richard | layout-mov-reference, face-comp-driven, photo-plate, multi-character-staging | done | done |
| [Sc160](scenes/gb202-remote-sc160/) | 31 | Darwin, Gumball, Nicole, Richard | layout-mov-reference, face-comp-driven, multi-character-staging | done | done |

### GB204 "The Phone"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc154](scenes/gb204-phone-sc154/) | 184 | Darwin, Gumball | rough-layer-shipped, layout-mov-reference, face-comp-driven, photo-plate, dialogue-two-shot | done | done |

### GB206 "The Job"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc019](gb206-job-sc019/) | 56 | Darwin, Gumball | layout-mov-reference, photo-plate, dialogue-two-shot | done | done |
| [Sc119](gb206-job-sc119/) | 57 | Nicole | head-comp-swap, layout-mov-reference, face-comp-driven, punch-zoom, solo-close-up | done | done |

### GB211 "The Treasure"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc105](gb211-treasure-sc105/) | 123 | Gumball, Nicole, Richard | per-character-mask, rough-layer-shipped, overlay-hands, costume-variant-puppet, layout-mov-reference, face-comp-driven | done | done |
| [Sc117](scenes/gb211-treasure-sc117/) | 136 | Anais, Darwin, Gumball | layout-mov-reference, face-comp-driven, photo-plate, multi-character-staging | done | done |
| [Sc122](scenes/gb211-treasure-sc122/) | 23 | Anais, Darwin, Gumball | layout-mov-reference, face-comp-driven, photo-plate, multi-character-staging | done | done |

### GB214 "The Words"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc054](scenes/gb214-words-sc054/) | 229 | Darwin | mask-layer, nested-master-symbol, layout-mov-reference, photo-plate, solo-close-up | done | done |
| [Sc055](scenes/gb214-words-sc055/) | 94 | Darwin | nested-master-symbol, layout-mov-reference, face-comp-driven, solo-close-up, photo-plate | done | done |
| [Sc056](scenes/gb214-words-sc056/) | 178 | Carrie, Darwin, Masami, Ocho, Tobias | nested-master-symbol, layout-mov-reference, multi-character-staging | done | done |
| [Sc057](scenes/gb214-words-sc057/) | 198 | Carmen, Carrie, Darwin, Masami, Ocho, Tobias | per-character-mask, nested-master-symbol, layout-mov-reference, multi-character-staging, photo-plate | done | done |
| [Sc058](scenes/gb214-words-sc058/) | 17 | Darwin | face-comp-driven, angle-variant-puppet, solo-close-up, photo-plate | done | done |
| [Sc059](scenes/gb214-words-sc059/) | 105 | Darwin, Masami | layout-mov-reference, face-comp-driven, dialogue-two-shot, photo-plate | done | done |
| [Sc061](scenes/gb214-words-sc061/) | 100 | Darwin | layout-mov-reference, face-comp-driven | done | done |
| [Sc062](scenes/gb214-words-sc062/) | 59 | Carmen, Carrie, Darwin, Masami, Ocho, Tobias | nested-master-symbol, layout-mov-reference, multi-character-staging, photo-plate | done | done |
| [Sc063](scenes/gb214-words-sc063/) | 109 | Carrie, Darwin | layout-mov-reference, face-comp-driven, dialogue-two-shot, photo-plate | done | done |
| [Sc099](gb214-words-sc099/) | 284 | Darwin, Gumball | costume-variant-puppet, head-comp-swap, layout-mov-reference, face-comp-driven, dialogue-two-shot | done | done |

### GB218 "The Flakers"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc002](scenes/gb218-flakers-sc002/) | 42 | Darwin, Gumball | forced-perspective, run-cycle-library, layout-mov-reference, face-comp-driven, cycle-multi-scale, photo-plate | done | done |
| [Sc117](scenes/gb218-flakers-sc117/) | 312 | Anais, Darwin, Gumball | rough-layer-shipped, layout-mov-reference, face-comp-driven, multi-character-staging | done | done |

### GB219 "The Watch"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc075](scenes/gb219-watch-sc075/) | 78 | Darwin, Gumball, Richard | layout-mov-reference, face-comp-driven, multi-character-staging | done | done |
| [Sc076](scenes/gb219-watch-sc076/) | 209 | Darwin, Gumball | layout-mov-reference, face-comp-driven, dialogue-two-shot | done | done |
| [Sc111](scenes/gb219-watch-sc111/) | 68 | Darwin, Gumball | rough-layer-shipped, layout-mov-reference, face-comp-driven, costume-variant-puppet | done | done |

### GB2215 "The Apology"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc142](gb2215-apology-sc142/) | 75 | Gumball | rough-layer-shipped, layout-mov-reference, face-comp-driven, dissection-gag, transformation-gag | done | done |
| [Sc144](scenes/gb2215-apology-sc144/) | 51 | Gumball | layout-mov-reference, face-comp-driven, solo-close-up | done | done |
| [Sc146](scenes/gb2215-apology-sc146/) | 86 | Darwin, Gumball | layout-mov-reference, face-comp-driven, photo-plate, dialogue-two-shot | done | done |

### GB222 "The Bumpkin"

| Scene | Frames | Cast | Tags | Sheet | Video |
|---|---|---|---|---|---|
| [Sc089](scenes/gb222-bumpkin-sc089/) | 177 | Anais, Darwin, Nicole | layout-mov-reference, face-comp-driven, multi-character-staging | done | done |

## The 31 scenes, by technique

- **angle-variant-puppet** (1): GB214 Sc058
- **costume-variant-puppet** (3): GB211 Sc105, GB214 Sc099, GB219 Sc111
- **cycle-multi-scale** (2): GB202 Sc108, GB218 Sc002
- **dialogue-two-shot** (7): GB204 Sc154, GB206 Sc019, GB214 Sc059, GB214 Sc063, GB214 Sc099, GB219 Sc076, GB2215 Sc146
- **dissection-gag** (1): GB2215 Sc142
- **face-comp-driven** (24): GB202 Sc103, GB202 Sc108, GB202 Sc147, GB202 Sc160, GB204 Sc154, GB206 Sc119, GB211 Sc105, GB211 Sc117, GB211 Sc122, GB214 Sc055, GB214 Sc058, GB214 Sc059, GB214 Sc061, GB214 Sc063, GB214 Sc099, GB218 Sc002, GB218 Sc117, GB219 Sc075, GB219 Sc076, GB219 Sc111, GB2215 Sc142, GB2215 Sc144, GB2215 Sc146, GB222 Sc089
- **forced-perspective** (2): GB202 Sc108, GB218 Sc002
- **head-comp-swap** (2): GB206 Sc119, GB214 Sc099
- **layout-mov-reference** (30): GB202 Sc094, GB202 Sc103, GB202 Sc108, GB202 Sc144, GB202 Sc147, GB202 Sc160, GB204 Sc154, GB206 Sc019, GB206 Sc119, GB211 Sc105, GB211 Sc117, GB211 Sc122, GB214 Sc054, GB214 Sc055, GB214 Sc056, GB214 Sc057, GB214 Sc059, GB214 Sc061, GB214 Sc062, GB214 Sc063, GB214 Sc099, GB218 Sc002, GB218 Sc117, GB219 Sc075, GB219 Sc076, GB219 Sc111, GB2215 Sc142, GB2215 Sc144, GB2215 Sc146, GB222 Sc089
- **mask-layer** (1): GB214 Sc054
- **multi-character-staging** (12): GB202 Sc103, GB202 Sc144, GB202 Sc147, GB202 Sc160, GB211 Sc117, GB211 Sc122, GB214 Sc056, GB214 Sc057, GB214 Sc062, GB218 Sc117, GB219 Sc075, GB222 Sc089
- **nested-master-symbol** (7): GB202 Sc094, GB202 Sc144, GB214 Sc054, GB214 Sc055, GB214 Sc056, GB214 Sc057, GB214 Sc062
- **overlay-hands** (1): GB211 Sc105
- **per-character-mask** (2): GB211 Sc105, GB214 Sc057
- **photo-plate** (15): GB202 Sc094, GB202 Sc147, GB204 Sc154, GB206 Sc019, GB211 Sc117, GB211 Sc122, GB214 Sc054, GB214 Sc055, GB214 Sc057, GB214 Sc058, GB214 Sc059, GB214 Sc062, GB214 Sc063, GB218 Sc002, GB2215 Sc146
- **punch-zoom** (1): GB206 Sc119
- **rough-layer-shipped** (5): GB204 Sc154, GB211 Sc105, GB218 Sc117, GB219 Sc111, GB2215 Sc142
- **run-cycle-library** (4): GB202 Sc103, GB202 Sc108, GB202 Sc144, GB218 Sc002
- **solo-close-up** (5): GB206 Sc119, GB214 Sc054, GB214 Sc055, GB214 Sc058, GB2215 Sc144
- **speed-smear** (1): GB202 Sc108
- **transformation-gag** (1): GB2215 Sc142

## Scene details

### GB202 "The Remote" — Sc094
**The Remote — Sc094: Nicole dives over the car (photo-plate garage stunt)** · 56 frames @ 25 fps · cast: Nicole · folder: `production/scene-templates/gumball/scenes/gb202-remote-sc094/`

Stunt staging on a photographic plate with an unfinished prop: the shot opens on ~14 frames of empty parking-garage photo plate with only a blue layout-line car in it, then Nicole drops in from the TOP of the frame (not through any door), tumbles, stretches into a full horizontal dive over the car roof (~frame 35), lands past it (~frame 42) and holds an angry crouch (~frame 49) before vanishing, leaving the empty plate again. The entire performance lives inside one nested master symbol ('Mom angry run rough', 1752 kf) placed over a single 'bg' symbol; the comedy and the danger come from trajectory and timing against a static plate, not from camera moves or extra drawings -- the car itself is never even painted.

### GB202 "The Remote" — Sc103
**The Remote — Sc103: Richard hogs the remote (three run cycles, one garage)** · 141 frames @ 25 fps · cast: Darwin, Gumball, Richard · folder: `production/scene-templates/gumball/scenes/gb202-remote-sc103/`

Three run cycles, three jobs: Gumball and Darwin charge in from frame-left on their library run cycles, furious, while Richard -- also on a run cycle ('dad_run') -- runs nowhere: he sits cross-legged at centre frame clutching the remote, hovering in place, grinning. When the kids exit (~frame 71) the same static garage plate and the same seated pose carry a 70-frame solo rant, performed almost entirely by face comps (1720 kf of face work vs 294 kf of body), until a final-frame flip puts Richard upside down with his soles to camera. The lesson: a cycle is not locomotion until staging says so -- placed on a seated, centred character, a run cycle becomes pure manic energy.

### GB202 "The Remote" — Sc108
**The Remote — Sc108: forced-perspective run (giant Darwin FG, small Gumball BG)** · 40 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/gb202-remote-sc108/`

Locomotion + forced perspective: both characters run library cycles ('gb run cycle' 410 kf, 'dar run cycle' 223 kf), but the staging does the work — Darwin's cycle is placed HUGE in the foreground, cropped by the frame edge, one giant leg swinging across the shot, while Gumball runs the same kind of cycle small in the background clutching the remote. The background is reduced to a horizontal speed smear: no location detail at all. Travel, scale comedy and near-collision (Darwin's foot swings past Gumball ~frame 23) all come from placement scale, not new drawings.

### GB202 "The Remote" — Sc144
**The Remote — Sc144: kids burst in, Richard tackles them for the remote** · 262 frames @ 25 fps · cast: Darwin, Gumball, Nicole, Richard · folder: `production/scene-templates/gumball/gb202-remote-sc144/`

Multi-character staging in one master animation symbol: the whole family's performance is nested inside a single 'animation' symbol placed over white + background, instead of one scene layer per character. Entrances, a run cycle and a tackle are choreographed inside the nest where all the timing can be seen together.

### GB202 "The Remote" — Sc147
**The Remote — Sc147: family pile on the sidewalk, neighbour rants back (in-file cut)** · 147 frames @ 25 fps · cast: Darwin, Gumball, Nicole, Richard · folder: `production/scene-templates/gumball/scenes/gb202-remote-sc147/`

Two held tableaux joined by a cut INSIDE the scene file: the background layer swaps at frame 42. First, the Wattersons sit in a heap on a photographic suburban sidewalk -- Richard reclined on the ground, Nicole, Gumball and Darwin clustered over him -- and hold it for ~41 frames with only face-comp micro-variation (the whole group is one nested symbol, 'animation', on a single 'family' layer; there are zero scene-level body-puppet keyframes in the file). Then the file cuts to the neighbour (a stock CROWD_GUY build) alone in his driveway, arms up and mouth wide in a shout that he holds, with slow settling, for the remaining ~105 frames. The lesson is reaction-shot economy: when the joke is 'they stare / he yells', build one group nest and one solo hold, and let a background keyframe do the cutting.

### GB202 "The Remote" — Sc160
**The Remote — Sc160: Richard erupts at the family (31-frame punctuation shot)** · 31 frames @ 25 fps · cast: Darwin, Gumball, Nicole, Richard · folder: `production/scene-templates/gumball/scenes/gb202-remote-sc160/`

The punctuation shot: a complete story beat — entrance, scatter, eruption — in 31 frames on an empty stage. Richard storms in, the family hits the floor, and the scream is a single held pose with micro-variations. Nothing is wasted: one entrance vector, one group reaction, one held accent. Short shots in this production are built like jokes — setup inside 12 frames, payoff held.

### GB204 "The Phone" — Sc154
**The Phone — Sc154: tug-of-war over the phone (photo street, one held grapple)** · 184 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb204-phone-sc154/`

How to run a 184-frame scene on one held body pose: Gumball and Darwin sit tangled on a lawn in front of a photographic suburban fence, limbs bound up together with grey bands, both gripping the same green-cased phone, and for ~160 frames almost nothing moves except their faces -- rage, strain and shouted insults cycle through the face-comp system (2,683 face kf against 1,680 body kf) while the grapple itself is a single sustained strain. The payoff is saved for the last ~24 frames: Darwin's expression flips to delight, the tangle breaks, he exits frame-right with the prize and Gumball is left toppling backwards, dazed. A shouting match is a face scene; the bodies just have to hold the tension.

### GB206 "The Job" — Sc019
**The Job — Sc019: amazed two-shot on a photographic background plate** · 56 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/gb206-job-sc019/`

Two-character close interaction over a PHOTO plate: the background is a real photograph of a house and picket fence (Gumball's mixed-media signature), and both puppets play a 'squee' reaction — hands pressed to cheeks, star-pupil eyes — stacked as separate scene layers (DARWIN over the Gumball puppet layer). The comedy timing is offset: Darwin holds the delight for the whole 56 frames while Gumball's face falls to a worried blank stare around frame 35. Same frame, two reaction clocks.

### GB206 "The Job" — Sc119
**The Job — Sc119: Nicole close-up that punch-zooms into an extreme face shot** · 57 frames @ 25 fps · cast: Nicole · folder: `production/scene-templates/gumball/gb206-job-sc119/`

Emotion close-up with an in-scene camera punch: the shot opens as a medium close-up of Nicole against a blurred room background ('background 1st'), then smash-zooms around frame 15 into an extreme close-up where her eyes and mouth fill the entire 16:9 frame over flat blue ('background Last'). One character layer (MOM) the whole time — the 'cut' is a scale/background swap inside the scene, and the scream is carried entirely by the eye/mouth comp system plus a dedicated 'evil mum face' symbol.

### GB211 "The Treasure" — Sc105
**The Treasure — Sc105: the whole family in one bed, the duvet layer sandwich** · 123 frames @ 25 fps · cast: Gumball, Nicole, Richard · folder: `production/scene-templates/gumball/gb211-treasure-sc105/`

The layering masterclass of this wave: 18+ scene layers build one bed holding THREE characters — Nicole, Gumball (middle) and Richard — all tucked under a single dark duvet while a bedtime story is read. Each character gets duvet-side and duvet MASK layers so bodies sink under the blanket correctly, Gumball gets his own duvet piece, and 'DAD OVERLAY HANDS' rides on top so hands rest on the covers. The performances are tiny (mouths, eyelids, one eye popping open) — the construction is the show.

### GB211 "The Treasure" — Sc117
**The Treasure — Sc117: Anais makes her case (Darwin in the fishbowl)** · 136 frames @ 25 fps · cast: Anais, Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb211-treasure-sc117/`

Dialogue staging with an unequal movement budget: over 136 frames in the photographic bedroom, only Anais actually performs -- she starts centre-frame smiling, cracks up laughing (~frame 35), turns furious and stomps her way to frame-right (frames 52-69), softens into pleading (~frame 85) and ends smiling again. Her brothers are near-frozen gags: Gumball sits on the lower bunk wearing one worried look for the whole scene, and Darwin stands inside a fishbowl on the dresser -- body behind the BOWL_FRONT glass layer, head out of the top -- moving only his eyes until the last frame, when his mouth finally opens. The construction lesson is the sandwich: character layer(s) + a front-glass prop layer = a character credibly inside a transparent container, no special rig required.

### GB211 "The Treasure" — Sc122
**The Treasure — Sc122: heads on a string (23-frame bedroom insert)** · 23 frames @ 25 fps · cast: Anais, Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb211-treasure-sc122/`

The sub-second insert: 23 frames (under one second at 25 fps) that exist only to hold a reaction inside a bigger sequence. Gumball and Darwin hang from a yellow cord at top-bunk height, rendered as blissful floating heads -- eyes closed, mouths cycling through a sung/spoken line, swaying slightly -- while Anais stands on the floor below looking up at them, delighted. The stage is a photographic bedroom plate; the puppets are flat vector. Nothing is chased, built or transformed: the scene teaches how little motion a cut-in needs when the staging (two heads dangling at bunk height, one small witness on the floor) is already the joke.

### GB214 "The Words" — Sc054
**The Words — Sc054: Darwin's hallway solo (one symbol, borrowed photo plate)** · 229 frames @ 25 fps · cast: Darwin · folder: `production/scene-templates/gumball/scenes/gb214-words-sc054/`

A solo corridor scene with one actor, one plate and one master symbol: Darwin enters from behind a hallway pillar (clipped by a mask layer, not redrawn), then wanders the photographic corridor inside a single nested symbol -- 'DRW_marche + lente' ('walk + slow') -- cycling through an emotion tour: smug singing with clasped hands, an eyes-closed belted note, worry, pleading, annoyed explaining. Nobody else exists in the shot. The ending is a scale punch on the same plate: small distant figure (frame 172) to looming worried near-camera (frame 201) to a frame-filling bliss close-up (frame 229) -- a 'zoom' achieved purely by scaling the placement, no camera and no new background. Even the plate is borrowed: it is a crop of a GB110 'The Fight' background.

### GB214 "The Words" — Sc055
**The Words — Sc055: Darwin's pleading close-up, nested in one master symbol (94 frames)** · 94 frames @ 25 fps · cast: Darwin · folder: `production/scene-templates/gumball/scenes/gb214-words-sc055/`

The nested-master pattern at its purest: the scene timeline is almost empty (one keyframe on the character layer, one on the background) and the whole 94-frame performance - a pleading, singing close-up that ends with Darwin falling out of frame - lives inside a single master symbol, 'DRW_marche + lente' (303 kf). Inside the nest, the face system does the acting: GB200_DRW_HEADCOMP carries 658 kf and the mouth comp 304 kf while the body barely moves. It also teaches name-vs-content discipline: the symbol is named for a slow walk, but the placed performance is a stationary emotional close-up - always trust the render over the filename.

### GB214 "The Words" — Sc056
**The Words — Sc056: Darwin performs on a ladder, nose-to-nose with the T-Rex (178 frames)** · 178 frames @ 25 fps · cast: Carrie, Darwin, Masami, Ocho, Tobias · folder: `production/scene-templates/gumball/scenes/gb214-words-sc056/`

The scale-gag wide shot, built as a composite: a photorealistic T-Rex and the whole crowd exist only as the embedded layout/reference video, and the Flash production animates just five puppets against it. Darwin's entire ladder performance - meditating, preening, balancing, singing, all nose-to-nose with the dinosaur - is the reusable master symbol 'DRW_marche + lente' placed on two 'dwn' layers, while the four classmate reactors stay off or invisible for two-thirds of the shot and pop to full presence only for the final third, so the eye stays on the small fish performing at the giant's face. Lesson: when the environment and the giant are somebody else's render, your file's job is timing and eyelines, not redrawing their work.

### GB214 "The Words" — Sc057
**The Words — Sc057: the hallway dance — whole class advances on camera (198 frames)** · 198 frames @ 25 fps · cast: Carmen, Carrie, Darwin, Masami, Ocho, Tobias · folder: `production/scene-templates/gumball/scenes/gb214-words-sc057/`

How to shoot a group dance number as a single advancing wide shot. One photographic corridor plate never changes; the entire class is layered - six finished puppets on named layers (Tobias's comp alone is an 805-kf nest of 7 puppets; Darwin's head comps run 566 kf) and seven white placeholder characters on '3d character ref' layers for the classmates other departments finish - and the whole ensemble scales/moves toward camera for 198 frames so a static background feels like a tracking shot. Two per-character mask layers keep the advancing dancers correctly occluded by the corridor. The mixed cast is the point: finished Flash puppets and unfinished white references share one choreography, timed together in one file, because the dance only works if every department hits the same beats.

### GB214 "The Words" — Sc058
**The Words — Sc058: Darwin backview whip-turn close-up (17 frames)** · 17 frames @ 25 fps · cast: Darwin · folder: `production/scene-templates/gumball/scenes/gb214-words-sc058/`

How to stage a whip-turn reaction close-up with almost nothing: one backview puppet, one face-comp performance, one cropped background. The scene is 17 frames and a single scene-level placement - Darwin seen from behind for the first 5 frames (a dedicated GB200_DARWIN_PUPPET_BACKVIEW_v001), then turned to camera where the entire performance is face comps (1702 face kf vs 271 body kf in the census): closed-eye grin, open-mouth shock, blushing smile. The background is not repainted for the close-up - it is a crop (GB214_WORDS_SC057_LO_BG_crop.jpg) of the Sc057 wide hallway plate, so the close-up inherits the wide shot's photographic corridor for free.

### GB214 "The Words" — Sc059
**The Words — Sc059: Darwin's smug sway vs Masami's frozen smile (105 frames)** · 105 frames @ 25 fps · cast: Darwin, Masami · folder: `production/scene-templates/gumball/scenes/gb214-words-sc059/`

The held-reaction two-shot: stage one character as a frozen smile and let the other do all the work. Masami's puppet is placed once and her happy face does not change for 90+ frames while Darwin slides in and runs a smug finger-up sway routine in the lower frame; her reaction - a worried grimace - is saved for the single final frame, after he has already exited, which is what makes it land as the punchline. Structurally the scene is two layers and two placements; the entire budget went into Darwin's face comps (2,758 kf in the census) and one saved expression swap.

### GB214 "The Words" — Sc061
**The Words — Sc061: Darwin peeks and points around the layout-video giant (100 frames)** · 100 frames @ 25 fps · cast: Darwin · folder: `production/scene-templates/gumball/scenes/gb214-words-sc061/`

A Flash scene can be only half of the finished shot. Sc061's only puppet is Darwin (279 kf, with 2,415 kf of face comps), but the frame is dominated by a giant classmate who is not in the Flash file at all as artwork - she is a DOMVideoInstance on the 'layout mov' layer, a separately produced (3D-style) character embedded as reference so the Flash animator can puppeteer Darwin around her exact head positions: peeking right, peeking left, then stepping out front to point at her. The lesson for any mixed-pipeline production: animate the in-file character against the other pipeline's render, in the same file, frame-matched - never guess the composite positions later. The file also shows the failure mode to avoid: its fieldguide layer was left as a regular layer, so the safe-area guides render into the export.

### GB214 "The Words" — Sc062
**The Words — Sc062: Darwin's taunt-dance for a hallway audience (59 frames)** · 59 frames @ 25 fps · cast: Carmen, Carrie, Darwin, Masami, Ocho, Tobias · folder: `production/scene-templates/gumball/scenes/gb214-words-sc062/`

How to stage a one-kid performance with a built-in audience: the performer (Darwin) gets the only fully animated puppet (196 kf plus 644+360 kf of head comps), placed centre on his own layer, while four classmates are parked on named layers around him as near-static reactors - Tobias's pointing-laugh comp (350 kf master symbol) does most of the audience's acting, Carmen, Ocho and Carrie hold poses. The comedy is in the performer's escalation (smug -> furious grimace-stomp -> bow -> splits), not in moving the crowd. One background, no cuts, 59 frames.

### GB214 "The Words" — Sc063
**The Words — Sc063: Darwin leans on Carrie — her smile falls last (109 frames)** · 109 frames @ 25 fps · cast: Carrie, Darwin · folder: `production/scene-templates/gumball/scenes/gb214-words-sc063/`

A two-character scene built as a single nested placement: the scene timeline has one 'animation' layer with one puppet instance, and both performances - Darwin's (445 kf puppet, 1,226 kf in the largest head comp) and Carrie's ('car head' 189 kf plus her mouth/eye comps) - are choreographed inside it, including their position swap mid-shot. The scene also repeats the episode's signature reaction device: Carrie keeps her pleasant face for the entire exchange and drops it only in the last frame, after Darwin has exited - the audience gets her true reaction as a private final beat.

### GB214 "The Words" — Sc099
**The Words — Sc099: Darwin's about-to-explode rant (two-shot on white)** · 284 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/gb214-words-sc099/`

Dialogue two-shot construction: one scene layer per character (GUMBALL / DARWIN) over a WHITE layer and background, so each performance can be retimed independently. Uses an episode-specific costume head comp ('DRWAboutToExplode') swapped onto the standard Darwin puppet for one story beat.

### GB218 "The Flakers" — Sc002
**The Flakers — Sc002: panic run straight at the camera down the school hallway** · 42 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb218-flakers-sc002/`

Forced-perspective run straight at the camera: the camera never moves and the hallway background is a single locked plate for all 42 frames — the entire gag is placement scale. Darwin runs a library cycle ('Darwin Panic Run' / 'Panic Run Cycle', 318 kf) ramped from 0.33x at the far end of the hallway to 3.89x until his panicked face fills the frame and exits past camera; Gumball runs the same beat smaller and behind him. Because this is a KeyAnim (not clean) file, the production process is visible in the export: red timing charts are drawn over the middle frames and Darwin's legs are still red rough lines under his clean body.

### GB218 "The Flakers" — Sc117
**The Flakers — Sc117: the couch pile-on — phone, pile-on, face-off, laugh (312f, KeyAnim)** · 312 frames @ 25 fps · cast: Anais, Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb218-flakers-sc117/`

The longest scene in the archive is a single locked couch shot holding a full three-act mini-play for 312 frames: Anais alone, swooning and laughing over her phone (f1-40); Gumball and Darwin pile in on top of her in a three-head couch stack while she stays delighted underneath (f79-157); a standing confrontation (f195-234); then a shared laugh that settles into deadpan (f273-312). The stack is built for it: clean puppet layers (gb / dwn / anais) run parallel to DOMShape layers (GB / DRW / ANAIS / BRIEF) carrying the rough work, with a ROUGH layer, TEMP_PILLOWS and sofa-pillow props (GB218Flakers_Props_SophaPillows_v001.fxg) as separate items. In this KeyAnim export the heads are finished colour comps while every body is red rough lines.

### GB219 "The Watch" — Sc075
**The Watch — Sc075: giant smug Richard hogs the controller while Gumball melts down** · 78 frames @ 25 fps · cast: Darwin, Gumball, Richard · folder: `production/scene-templates/gumball/scenes/gb219-watch-sc075/`

Three-character staging on one locked living-room plate, with the acting deliberately unbalanced: Richard sits huge and motionless centre-left, smug and half-lidded, holding the game controller for the full 78 frames, while the performance is pushed onto the smallest figure — Gumball's face comps cycle worried, grimacing, screaming and finally tongue-out disgust, and Darwin holds one flat side-eye as the timing foil. Construction is one scene layer per character (DAD / GB / Darwin) over a single background, so each reaction clock can be retimed independently; the controller is a reused library prop, not a scene-specific drawing.

### GB219 "The Watch" — Sc076
**The Watch — Sc076: two-shot crying escalation — both boys end up bawling on the floor** · 209 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb219-watch-sc076/`

A dialogue two-shot built as an escalation machine: locked camera, one living-room background, and two stock puppets on separate scene layers trading grief beats for 209 frames. Gumball leads — teary and wobbling from f1, open-mouthed wail at f27, collapsed to his knees sobbing by f131 — and Darwin answers each beat late (flat until f53, tear streaks at f79, his own floor collapse at f183) until both end bawling on the floor at f209. The face system does nearly all of it: GB_HEADCOMP alone holds 1,190 keyframes, the largest symbol in the file, and face comps total 4,699 kf against 1,505 body-puppet kf.

### GB219 "The Watch" — Sc111
**The Watch — Sc111: faces mashed flat against the glass pane (KeyAnim line art)** · 68 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb219-watch-sc111/`

The faces-on-glass gag is a layer trick: a translucent glass-pane prop (GB219Watch_Props_GlassPane_v001.fxg) sits on its own foreground 'glass' layer over the whole shot, and the characters — riding episode-specific mobility-scooter pose puppets — come up behind it and squash. For the first ~30 frames Gumball (top) and Darwin (below) are upright and worried with their palms on the glass; then the face comps flatten, cheeks balloon and features smear across the pane until both are pressed blobs (f43-68). This file is the KeyAnim export, so the render is pale line art with only accent colours (Gumball's ear, Darwin's legs) — the construction, not the finish, is what it teaches.

### GB2215 "The Apology" — Sc142
**The Apology — Sc142: Gumball falls apart and reassembles (body-part gag)** · 75 frames @ 25 fps · cast: Gumball · folder: `production/scene-templates/gumball/gb2215-apology-sc142/`

Transformation by puppet dissection: the joke is staged by breaking the puppet into separately-placed pieces. The scene opens on Gumball's legs walking in ALONE; head, torso and limbs are then placed as independent scene elements on the GB layer, splayed in impossible positions (multiple legs, head too big for the body, parts trailing behind), and the pieces progressively recombine until a strained, teeth-gritted whole Gumball stands at frame 75. No morphing — just per-part placement, scale and timing on a locked hallway background.

### GB2215 "The Apology" — Sc144
**The Apology — Sc144: solo close-up — Gumball nurses a hurt arm, screams, drops out of frame** · 51 frames @ 25 fps · cast: Gumball · folder: `production/scene-templates/gumball/scenes/gb2215-apology-sc144/`

Solo close-up construction at its most economical: one puppet on one scene layer (GB) over a single locked background, and 51 frames carried almost entirely by the face-comp system. Gumball holds a gritted-teeth wince — eyes up, teeth clamped, rocking a hurt arm — for over 30 frames (head/mouth/eye comps: 1,112 kf vs the puppet's 655), and the release is punctuated in two steps: eyes slam shut at f39, a full open-mouth scream at f45, then he drops out of frame and the scene ends on the empty background. Pain, build and payoff are all face-comp poses; the body barely moves.

### GB2215 "The Apology" — Sc146
**The Apology — Sc146: Darwin bursts out of a locker — hop-in, face-off, make-up** · 86 frames @ 25 fps · cast: Darwin, Gumball · folder: `production/scene-templates/gumball/scenes/gb2215-apology-sc146/`

Entrance-and-confrontation staging on one locked photographic locker plate with no cuts and no background change: the scene opens on the empty lockers (f1), Gumball hops in from frame-right with his ankles strapped together (f12-22), a locker door pops open and Darwin emerges from inside the locker (f33), and the two play a complete arc — shock, a mutual shouting face-off (f43-65, both still hopping), then a calm make-up (f75-86). Separate GB and DWN scene layers carry the offset reactions, and the open locker door is the only piece of 'set' that ever moves.

### GB222 "The Bumpkin" — Sc089
**The Bumpkin — Sc089: top-shot tableau — Nicole, Anais and Darwin flat on the ground (KeyAnim)** · 177 frames @ 25 fps · cast: Anais, Darwin, Nicole · folder: `production/scene-templates/gumball/scenes/gb222-bumpkin-sc089/`

Top-shot staging in a KeyAnim file: the camera looks straight down at a grey ground plate (GB222_BUMPKIN_Sc089_LO_BG.jpg) and three characters lie flat in a diagonal row — Nicole centre, Anais lower-left, Darwin right — each on their own scene layer, for 177 frames. The export shows the production split honestly: the heads are finished colour face comps and carry a full dialogue scene (Anais talks through f23-89, Darwin answers f111-155, Nicole's shifting reactions carry f133-177) while every body below the neck is still red rough construction lines in every frame. Three head comps on a held overhead tableau are the whole scene.

## Also in the library (not counted in the 31)

- **GB209 "The Banana" crashed top shot** (`gb209-banana-crashed-topshot/`) — an approved pose sheet (2 root frames) kept as a template because its FLA holds the dedicated overhead-angle puppets. Classified partial in the survey.

- **GB214 Sc057 + Sc059** are in the 31 (folders under `scenes/`) and are ALSO the Darwin dance: their frame-by-frame choreography lives in `production/dance-choreo/`.

## Complete scenes that exist SWF-only (no FLA in this archive)

- **GB222 "The Bumpkin" Sc035** (411f) — SWF only in archive, no FLA — SWF-tag extraction is future work.
- **GB222 "The Bumpkin" Sc090** (444f) — SWF only in archive, no FLA — the kids-looking-up-at-the-giant shot.
- **GB219 "The Watch" Sc077** (109f) — SWF only in archive, no FLA.
- **GB219 "The Watch" Sc078** (181f) — SWF only in archive, no FLA.

These were not counted in the 31 (the survey counts FLA-backed scenes). Pulling them in needs the SWF-tag extraction route — future work, stated plainly.

---

## Wave-1 survey — all 71 FLAs in CN-Leaks-001 (preserved)

The owner asked what complete animated scenes actually exist in the holdings. Every `.fla` entry in the archive is classified below from file evidence: companion-SWF frame counts (measured), XFL symbol/layer scans, FLAs extracted and parsed in full (★ = deep-extracted as a wave-1 template above; ‡ = extracted by the dance-choreo lane, PR #275), and rendered sheets where noted. Classes: **Complete animated scene** · **Partial** (pose sheet, pass file, test or duplicate) · **Static — not a scene** (puppet library / model sheet / rig file) · **Unverified**.

Totals: **31 complete animated scenes · 11 partial · 28 static · 1 unverified.**

| File | Block / episode | Class | Evidence |
|------|------|-------|----------|
| GB202REMOTE_Sc094_Clean_V023_STN.fla | GB202 "The Remote" | Complete animated scene | SWF 56f @25 |
| GB202REMOTE_Sc103_V0024_cleanup_LW.fla | GB202 "The Remote" | Complete animated scene | SWF 141f @25 |
| GB202REMOTE_Sc108_Clean_V001_STN.fla | GB202 "The Remote" | Complete animated scene ★ | Extracted; SWF 40f |
| GB202REMOTE_Sc144_KeyAnim_V050_clean_MS.fla | GB202 "The Remote" | Complete animated scene ★ | Extracted; SWF 262f |
| GB202REMOTE_Sc147_KeyAnim_V012_clean_WL_RTK.fla | GB202 "The Remote" | Complete animated scene | SWF 147f @25 |
| GB202REMOTE_Sc160_CLean_V003_jf.fla | GB202 "The Remote" | Complete animated scene | SWF 31f @25 (short shot) |
| RECOVER_GB202REMOTE_Sc160_CLean_V003_jf.fla | GB202 "The Remote" | Partial | Recovery duplicate of Sc160 (same size/content class) |
| GB204PHONE_Sc154_Clean_V007_KR.fla | GB204 "The Phone" | Complete animated scene | SWF 184f @25 |
| GB206JOB_Sc019_V007_Clean_MB.fla | GB206 "The Job" | Complete animated scene ★ | Extracted; SWF 56f |
| GB206JOB_Sc119_V004_clean_AO.fla | GB206 "The Job" | Complete animated scene ★ | Extracted; SWF 57f |
| GB211TREASURE_Sc105_V013_clean_GD.fla | GB211 "The Treasure" | Complete animated scene ★ | Extracted; SWF 123f |
| GB211TREASURE_Sc117_V004_RTK_MO.fla | GB211 "The Treasure" | Complete animated scene | SWF 136f @25 |
| GB211TREASURE_Sc122_V002_clean_MS.fla | GB211 "The Treasure" | Complete animated scene | SWF 23f @25 (short shot) |
| GB214WORDS_Sc054_V011_Clean_STN.fla | GB214 "The Words" | Complete animated scene | SWF 229f @25 |
| GB214WORDS_Sc055_V012_Clean_MB.fla | GB214 "The Words" | Complete animated scene | SWF 94f @25 |
| GB214WORDS_Sc056_V021_Clean_STN.fla | GB214 "The Words" | Complete animated scene | SWF 178f @25 |
| GB214WORDS_Sc057_V036_clean_MUI.fla | GB214 "The Words" | Complete animated scene ‡ | The Darwin dance, wide shot; SWF 198f — extracted in production/dance-choreo |
| GB214WORDS_Sc058_V005_clean_ST.fla | GB214 "The Words" | Complete animated scene | SWF 17f @25 (very short shot) |
| GB214WORDS_Sc059_V001_clean_RR.fla | GB214 "The Words" | Complete animated scene ‡ | The Darwin twist close-up; SWF 105f — extracted in production/dance-choreo |
| GB214WORDS_Sc060_V003_SFX_AC.fla | GB214 "The Words" | Partial | SFX-pass file for the scene, not the full scene (SWF 56f of effects) |
| GB214WORDS_Sc061_V012_Clean_MB.fla | GB214 "The Words" | Complete animated scene | SWF 100f @25 |
| GB214WORDS_Sc062_V010_clean_LB.fla | GB214 "The Words" | Complete animated scene | SWF 59f @25 |
| GB214WORDS_Sc063_V016_Clean_MB.fla | GB214 "The Words" | Complete animated scene | SWF 109f @25 |
| GB214WORDS_Sc099_V006_CLEAN_HS_FR_157.fla | GB214 "The Words" | Complete animated scene ★ | Extracted; SWF 284f |
| GB218Flakers_Sc002_KeyAnim_V004.fla | GB218 "The Flakers" | Complete animated scene | SWF 42f @25 |
| GB218Flakers_Sc117_KeyAnim_V007.fla | GB218 "The Flakers" | Complete animated scene | SWF 312f @25 — longest scene in the archive |
| GB219WATCH_Sc075_V007_Clean_HS.fla | GB219 "The Watch" | Complete animated scene | SWF 78f @25 |
| GB219WATCH_Sc076_Clean_V012_KR.fla | GB219 "The Watch" | Complete animated scene | SWF 209f @25 |
| GB219WATCH_Sc111_KeyAnim_V002.fla | GB219 "The Watch" | Complete animated scene | SWF 68f @25 (faces-on-glass gag, rendered in dance-lane triage) |
| GB2215APOLOGY_Sc142_V005_Clean_JA.fla | GB2215 "The Apology" | Complete animated scene ★ | Extracted; SWF 75f |
| GB2215APOLOGY_Sc144_V002_CLEAN_MO.fla | GB2215 "The Apology" | Complete animated scene | SWF 51f @25 |
| GB2215APOLOGY_Sc146_V004_CLEAN_MO.fla | GB2215 "The Apology" | Complete animated scene | SWF 86f @25 |
| GB2215APOLOGY_TEST_EXPORT.fla | GB2215 "The Apology" | Partial | Test export (26 symbols; body comps only) |
| GB222Bumpkin_Sc089_KeyAnim_V008.fla | GB222 "The Bumpkin" | Complete animated scene | SWF 177f @25 (giant-scale sequence; 64 MB FLA — wave-2 pull) |
| GB200_GUMBALL_HURT_FACEKICK_SC155_FINAL.fla | GB209 "The Banana" (per its slate) | Partial | Approved gag pose sheet — rendered & verified (2 root frames) |
| GB200_GUMBALL_HURT_FLOOR_SC160_FINAL.fla | GB209 "The Banana" (per set) | Partial | Approved gag pose sheet (SWF 2f) |
| GB200_GUMBALL_HURT_HIMSELF_SC158_FINAL.fla | GB209 "The Banana" (per set) | Partial | Approved gag pose sheet (SWF 18f of poses) |
| GB200_DARWIN_HURT_BACK_KICK_SC159_FINAL.fla | GB209 "The Banana" (per set) | Partial | Approved gag pose sheet (SWF 2f) |
| GB200_DARWIN_HURT_HIMSELF_SC161_FINAL.fla | GB209 "The Banana" (per set) | Partial | Approved gag pose sheet (SWF 10f of poses) |
| GB209_BANANA_GB+D_BILBOQUET_SC162_FINAL.fla | GB209 "The Banana" | Partial | Approved pose sheet, 19 poses — rendered & verified |
| GB209_DESTROYED_FACE_GUMBALL_V002.fla | GB209 "The Banana" | Partial | Face-gag pose sheet (SWF 2f) |
| GB209_GB+DRW_CRASHED_TOP_SHOT_V002.fla | GB209 "The Banana" | Partial ★ | Approved pose sheet (SWF 2f) — deep-extracted for its angle puppets |
| GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla | GB200 puppet block | Static — not a scene | Pose library; SWF export is a 162f model-sheet presentation (dance-lane verified) |
| GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_006.fla | GB200 puppet block | Static — not a scene | Pose library (version duplicate), SWF 162f presentation |
| GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_004.fla | GB200 puppet block | Static — not a scene | Pose library (version duplicate), SWF 162f presentation |
| GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_001_CS3.fla | GB200 puppet block | Static — not a scene | Pose library (CS3-era version) |
| GB200_ORIGINAL_PUPPET_DARWIN_Version002.fla | GB200 puppet block | Static — not a scene | Pose library; SWF 150f presentation |
| GB200_ORIGINAL_PUPPET_DARWIN_Version002 (9).fla | GB200 puppet block | Static — not a scene | Pose library (duplicate copy) |
| GB200_ORIGINAL_PUPPET_DARWIN_Version002_CS5.fla | GB200 puppet block | Static — not a scene | Pose library (CS5 version), SWF 150f presentation |
| GB200_ORIGINAL_PUPPET_MOM_VERSION_002.fla | GB200 puppet block | Static — not a scene | Pose library (Nicole); SWF 155f presentation |
| GB200_ORIGINAL_PUPPET_MOM_VERSION_002 (10).fla | GB200 puppet block | Static — not a scene | Pose library (duplicate copy) |
| GB200_ORIGINAL_PUPPET_DAD_VERSION_004.fla | GB200 puppet block | Static — not a scene | Pose library (Richard) |
| GB200_ORIGINAL_PUPPET_DAD_VERSION_003.fla | GB200 puppet block | Static — not a scene | Pose library (version duplicate), SWF 145f presentation |
| GB200_ORIGINAL_PUPPET_ANAIS_VERSION_002.fla | GB200 puppet block | Static — not a scene | Pose library (Anais); SWF 98f presentation |
| GB200_ORIGINAL_PUPPET_ANAIS_VERSION_002 (8).fla | GB200 puppet block | Static — not a scene | Pose library (duplicate copy) |
| GB200_HECTOR_ORIGINAL_PUPPET_V001_CS3.fla | GB200 puppet block | Static — not a scene | Pose library (Hector, CS3-era) |
| Carrie_Ghost.fla | Gumball S2 rigs | Static — not a scene | Single-character rig (Carrie) |
| Ocho_Spider.fla | Gumball S2 rigs | Static — not a scene | Single-character rig (Ocho, spider form) |
| Penny_PeanutAntlers.fla | Gumball S2 rigs | Static — not a scene | Single-character rig (Penny) |
| Tobias_SportyPuff.fla | Gumball S2 rigs | Static — not a scene | Single-character rig (Tobias) |
| Madam_Foster_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Goo_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Goo_Hair.fla | Foster's model turns | Static — not a scene | Single-element sheet (hair) |
| Duchess_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Ed_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Cheese_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Frankie_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Terrence_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Coco_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Wilt_Turnaround.fla | Foster's model turns | Static — not a scene | Model-sheet turnaround |
| Gumball-em_V06.fla | Gumball S2 rigs | Unverified | No readable XFL symbols (0 in scan) and no companion SWF in the archive; name suggests an emoticon/element file — needs a binary-FLA look before anyone claims what it is |

**Not FLAs, but complete scenes that exist in the same archive as SWF only** (no FLA to dissect): GB222 "The Bumpkin" Sc035 (411f) and Sc090 (444f — the kids-looking-up-at-the-giant shot), GB219 "The Watch" Sc077 (109f) and Sc078 (181f). If the owner wants those as templates, the SWF-tag extraction route is the wave-2 job.


## Honest gaps

None for media: every scene has its sheet and video. (The sandbox write guard from wave 1 proved intermittent during this build — renders were verified frame-by-frame and retried through the bursts.)
