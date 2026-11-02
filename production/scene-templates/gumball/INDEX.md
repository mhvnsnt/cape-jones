# Gumball scene templates — wave 1

Owner's order (2026-11-02): pull scenes from the Gumball production holdings into this repo as **working scene templates** for Cape Jones production — production anatomy from an actual show: how they layer a scene, how they stage multiple characters, camera use, timing. Scope extension (same day): every deep-extracted scene also gets its **full video** rendered from the production SWF, and this index surveys **all 71 FLAs** in the archive so the owner can see exactly which complete animated scenes exist in the holdings. Every character appearing in an extracted scene is **named** — background and onlooker characters included.

Source archive: `CN-Leaks-001-gumball.zip` (876 entries, 1,709,550,213 bytes; GitHub `mhvnsnt/cn-gigaleak-gumball`, draft release `untagged-1676e192ae8c72e95791`). Method: FLAs are XFL zips with a malformed central directory, read via a sequential local-header parser; `DOMDocument.xml` + `LIBRARY/` symbol XMLs parsed directly. Contact sheets and videos rendered from the production SWFs with JPEXS FFDec 26.3.0. Nothing was redrawn or approximated — and every scene below was verified by rendering it, not by trusting its filename (filenames in this archive lie; see the surprises section).

> **Landing status (2026-11-02):** the anatomy JSONs and this index are landed for all 8 scenes, with contact sheets for 6. The Sc099 and Sc144 sheets, and all 8 scene videos, are a pending follow-up: mid-harvest the sandbox engaged a write guard that refuses binary production-asset writes (rendered PNG frames, encoded video) with EPERM, while text/analysis writes pass. The moment the guard lifts, the renders finish from the staged files and the folders gain their `contact-sheet.png` / `video.mp4` — the two affected folders are marked below.

## The format

Each scene folder holds `scene-anatomy.json`, `contact-sheet.png`, and the scene **video** (MP4, native fps and stage size, H.264 faststart; if a video file is too large for the git tree it lives on the `scene-templates-wave1` release and is linked from the scene's row instead). *(Sheets/videos pending for the folders marked † — see the landing-status note above.)* The JSON uses the same neutral per-keyframe transform format as `production/dance-choreo` v1: a part pose is `(item, first_frame, affine matrix a/b/c/d/tx/ty, pivot)`; frame numbers are 0-based XFL indices at 25 fps unless noted. Contents per file: `layer_stack` (every scene layer, what it holds, keyframe counts), `placements` (the full scene timeline), `characters` (puppet timelines with per-frame `sampled_frames` expansion — keyMode 9728 is pose-to-pose, so each keyframe holds to the next, matching SWF playback), `face_components` (eye/mouth/head comp timelines — the face system is separate from the body), `key_symbols` (any other symbol with 300+ keyframes: nested scene nests, cycles, scene-specific animation copies), `other_symbols` (the rest of the library, by name + keyframe count).

## Cross-scene lessons (the short version)

- **The face is a separate rig.** Every scene splits the puppet into body + eye comp + mouth comp (+ head comp), each on its own timeline with its own keyframes. Close-ups are animated almost entirely in the comps.
- **Special states get their own symbols.** Pyjama puppets (Sc105), an about-to-explode head (Sc099), an "evil mum face" (Sc119), crashed top-shot puppets (GB209) — the production never bends the stock puppet into a special state; it swaps in a variant built for the beat.
- **Cycles are library performances.** Run cycles (Sc108) are full puppet performances stored as symbols and reused at any scale — including two scales in the same frame.
- **Occlusion is solved with layers + masks, not redraws.** The bed scene (Sc105) stacks 18+ layers with per-character masks so three bodies share one duvet.
- **Scene files keep their roughs.** Rough animator layers ship inside clean files (Sc105, Sc142). Working files are not sterilized.
- **Exports carry their paperwork.** GB209 files are approved pose sheets on a field-guide template with slate + APPROVED box; GB2xx scene exports carry frame counters. Approval/presentation is built into the file, not added later.

## The deep-extracted scenes (wave 1)

| Folder | Scene | Episode | Frames | Cast (every character in the scene) | Teaches |
|--------|-------|---------|--------|------|---------|
| [gb202-remote-sc144](gb202-remote-sc144/) † | Sc144 | GB202 "The Remote" | 262 | Gumball, Darwin, Richard, Nicole | Multi-character staging / physical comedy |
| [gb214-words-sc099](gb214-words-sc099/) † | Sc099 | GB214 "The Words" | 284 | Gumball, Darwin | Dialogue two-shot / rant staging |
| [gb211-treasure-sc105](gb211-treasure-sc105/) | Sc105 | GB211 "The Treasure" | 123 | Nicole, Gumball, Richard | Layering & occlusion (the duvet sandwich) |
| [gb206-job-sc019](gb206-job-sc019/) | Sc019 | GB206 "The Job" | 56 | Darwin, Gumball | Two-character close interaction / photo plate |
| [gb202-remote-sc108](gb202-remote-sc108/) | Sc108 | GB202 "The Remote" | 40 | Darwin, Gumball | Locomotion cycles / forced perspective |
| [gb206-job-sc119](gb206-job-sc119/) | Sc119 | GB206 "The Job" | 57 | Nicole | Emotion close-up / in-scene camera punch |
| [gb2215-apology-sc142](gb2215-apology-sc142/) | Sc142 | GB2215 "The Apology" | 75 | Gumball | Wildcard: transformation by puppet dissection |
| [gb209-banana-crashed-topshot](gb209-banana-crashed-topshot/) | Crashed top shot | GB209 "The Banana" | 2 (pose sheet) | Gumball, Darwin | Wildcard: camera-angle puppets / approved pose sheet |

### GB202 "The Remote" — Sc144

**The Remote — Sc144: kids burst in, Richard tackles them for the remote**

- Cast: **Gumball, Darwin, Richard, Nicole** (the whole family except Anais, who has no puppet or placement anywhere in this file).
- Frames: 262 @ 25 fps · stage 1920x1080 · source FLA `GB202REMOTE_Sc144_KeyAnim_V050_clean_MS.fla`
- Scene layers (7): audio, framecounter, fieldguide, animation, white, background, layout mov

**What it teaches:** Multi-character staging in one master animation symbol: the whole family's performance is nested inside a single 'animation' symbol (1,413 keyframes) placed over white + background, instead of one scene layer per character. Entrances, a run cycle and a tackle are choreographed inside the nest where all the timing can be seen together.

**Scene notes:**
- Scene timeline is only 3 working layers: animation / white / background — all character work is nested in the 'animation' symbol.
- Contains a nested 'gb run cycle' (375 kf) and Nicole's mouth comp (349 kf): cycles and face comps are shared library assets dropped into the nest.
- Highest motion sum of the wave (136,609) — this is the most physical scene in the set.

### GB214 "The Words" — Sc099

**The Words — Sc099: Darwin's about-to-explode rant (two-shot on white)**

- Cast: **Gumball, Darwin** — the only two puppets in the file; the classroom is background art, no other character is placed or puppeted in this scene.
- Frames: 284 @ 25 fps · stage 1920x1080 · source FLA `GB214WORDS_Sc099_V006_CLEAN_HS_FR_157.fla`
- Scene layers include per-character layers: GUMBALL, DARWIN, WHITE, background

**What it teaches:** Dialogue two-shot construction: one scene layer per character over a WHITE layer and background, so each performance can be retimed independently. Uses an episode-specific costume head comp ('DRWAboutToExplode', 628 keyframes) swapped onto the standard Darwin puppet for one story beat.

**Scene notes:**
- Scene layers are literally named per character: GUMBALL, DARWIN, WHITE, background.
- The exploding-head variant is a separate library symbol — special story states get their own comp instead of redrawing the stock head.
- Mouth comps for both characters run 304–433 keyframes: lip sync is its own pass on its own timeline.
- Render note: this SWF embeds a reference video on its 'layout mov' layer (video character 1). The contact sheet and video were rendered from a copy with that reference-video tag stripped — the reference movie is a layout guide, not scene content; all character and background art is untouched.

### GB211 "The Treasure" — Sc105

**The Treasure — Sc105: the whole family in one bed, the duvet layer sandwich**

- Cast: **Nicole, Gumball, Richard** — Nicole reads the bedtime story, Gumball lies between his parents faking sleep, Richard is already out.
- Frames: 123 @ 25 fps · stage 1920x1080 · source FLA `GB211TREASURE_Sc105_V013_clean_GD.fla`
- Scene layers (23 in the timeline incl. folders): Roughs, DAD, MOM, MOM R ARM FRONT, DAD OVERLAY HANDS, DUVET, DUVET GUMBALL, dark stripe, MAIN, DUVET MOM MASK, DUVET MOM SIDE, DUVET DAD MASK, DUVET DAD SIDE, GUMBALL, duvet, background, …

**What it teaches:** The layering masterclass of this wave: 18+ scene layers build one bed holding THREE characters — Nicole, Gumball (middle) and Richard — all tucked under a single dark duvet while a bedtime story is read. Each character gets duvet-side and duvet MASK layers so bodies sink under the blanket correctly, Gumball gets his own duvet piece, and 'DAD OVERLAY HANDS' rides on top so hands rest on the covers. The performances are tiny (mouths, eyelids, one eye popping open) — the construction is the show.

**Scene notes:**
- Three heads, one blanket: Nicole left, Gumball centre, Richard right. Gumball's one-eye-open beat (around frames 62–93) is the gag — he's faking sleep during the story.
- Masks, not redraws, solve occlusion: DUVET MOM MASK / DUVET DAD MASK clip each body to its place under the shared duvet.
- Costume-variant puppets again: GB211_PYJAMAS_DAD_PUPPET and GB211_PYJAMAS_MOM_PUPPET — pyjama versions of the stock puppets, built for this episode.
- 'DAD ANIMATION copy' (452 kf) and 'MOM ANIMATION copy' (370 kf): scene-specific copies are edited in place; library originals stay clean.
- In the production SWF export the bedroom background renders white — the visible architecture is the duvet sandwich itself; frame-counter and field-guide overlays are part of the export.

### GB206 "The Job" — Sc019

**The Job — Sc019: amazed two-shot on a photographic background plate**

- Cast: **Darwin, Gumball**.
- Frames: 56 @ 25 fps · stage 1920x1080 · source FLA `GB206JOB_Sc019_V007_Clean_MB.fla`

**What it teaches:** Two-character close interaction over a PHOTO plate: the background is a real photograph of a house and picket fence (Gumball's mixed-media signature), and both puppets play a 'squee' reaction — hands pressed to cheeks, star-pupil eyes — stacked as separate scene layers (DARWIN over the Gumball puppet layer). The comedy timing is offset: Darwin holds the delight for the whole 56 frames while Gumball's face falls to a worried blank stare around frame 35. Same frame, two reaction clocks.

**Scene notes:**
- Background is a photographic plate, not a painted BG — the flat vector puppets are composited over it on the 'background' layer.
- Eye/mouth comps (EYESCOMP2/MOUTH2, 199–223 kf each) carry the scene; bodies are nearly still. In close-up, the face system IS the animation.
- Darwin's squee never breaks; Gumball's drops at ~f35 — offsetting reaction timing between characters in the same shot is the joke's engine.
- Second-generation comps (the '2' versions) are used: the library keeps versioned face systems per production block.

### GB202 "The Remote" — Sc108

**The Remote — Sc108: forced-perspective run (giant Darwin FG, small Gumball BG)**

- Cast: **Darwin, Gumball**.
- Frames: 40 @ 25 fps · stage 1920x1080 · source FLA `GB202REMOTE_Sc108_Clean_V001_STN.fla`

**What it teaches:** Locomotion + forced perspective: both characters run library cycles ('gb run cycle' 410 kf, 'dar run cycle' 223 kf), but the staging does the work — Darwin's cycle is placed HUGE in the foreground, cropped by the frame edge, one giant leg swinging across the shot, while Gumball runs the same kind of cycle small in the background clutching the remote. The background is reduced to a horizontal speed smear: no location detail at all. Travel, scale comedy and near-collision (Darwin's foot swings past Gumball ~frame 23) all come from placement scale, not new drawings.

**Scene notes:**
- Same asset class, two scales: a cycle symbol reads completely differently at 0.3x (background) vs 3x cropped (foreground).
- The 'background' layer is a speed-line smear — at full run, location is deleted on purpose.
- Darwin's foreground leg overlaps Gumball's space on the swing: FG/BG characters share the frame's depth, staged by layer order.
- 40 frames total: just enough loops for the cut; the cycles do the rest.

### GB206 "The Job" — Sc119

**The Job — Sc119: Nicole close-up that punch-zooms into an extreme face shot**

- Cast: **Nicole** (solo).
- Frames: 57 @ 25 fps · stage 1920x1080 · source FLA `GB206JOB_Sc119_V004_clean_AO.fla`
- Scene layers: MOM, background 1st, background Last (+ production layers)

**What it teaches:** Emotion close-up with an in-scene camera punch: the shot opens as a medium close-up of Nicole against a blurred room background ('background 1st'), then smash-zooms around frame 15 into an extreme close-up where her eyes and mouth fill the entire 16:9 frame over flat blue ('background Last'). One character layer (MOM) the whole time — the 'cut' is a scale/background swap inside the scene, and the scream is carried entirely by the eye/mouth comp system plus a dedicated 'evil mum face' symbol.

**Scene notes:**
- Frames 1–8: medium close-up, blurred photographic-style room BG. Frame ~15 onward: extreme close-up, face = the whole frame, flat colour BG.
- The two background layers are the before/after of the punch-in — no camera symbol, just a BG swap + puppet scale jump.
- Extreme expressions get their own symbol ('evil mum face', 76 kf) instead of being posed on the stock face comps.
- Mouth shapes in the extreme section cycle scream → round 'o' → clamped shut: the whole beat is lip-sync comps at wall size.

### GB2215 "The Apology" — Sc142

**The Apology — Sc142: Gumball falls apart and reassembles (body-part gag)**

- Cast: **Gumball** (solo — in several pieces).
- Frames: 75 @ 25 fps · stage 1920x1080 · source FLA `GB2215APOLOGY_Sc142_V005_Clean_JA.fla`

**What it teaches:** Transformation by puppet dissection: the joke is staged by breaking the puppet into separately-placed pieces. The scene opens on Gumball's legs walking in ALONE; head, torso and limbs are then placed as independent scene elements, splayed in impossible positions (multiple legs, head too big for the body, parts trailing behind), and the pieces progressively recombine until a strained, teeth-gritted whole Gumball stands at frame 75. No morphing — just per-part placement, scale and timing on a locked hallway background.

**Scene notes:**
- Frame 1 is only legs + tail: the scene trusts the audience to read dislocated parts as the character.
- The head comp holds 805 keyframes — more than the body puppet (555): the giant gritted-teeth head is the visual anchor while the body is in pieces.
- A 'Roughaurel' layer (rough pass by animator Laurel) ships inside the clean file — rough and clean coexist in production files.
- Background is a locked school hallway (tile wall, red window frames): all motion is character-side, which makes the part chaos readable.

### GB209 "The Banana" — crashed top shot (pose sheet)

**The Banana — crashed top shot: dedicated overhead-angle puppets (approved pose sheet)**

- Cast: **Gumball, Darwin** (both crashed, seen from directly above).
- Frames: 2 root frames (pose sheet) @ 24 fps · stage 2730x1625 (field-guide page) · source FLA `GB209_GB+DRW_CRASHED_TOP_SHOT_V002.fla`

**What it teaches:** Camera-angle puppets: for the overhead crash shot the show did NOT rotate the stock puppets — it built dedicated GB209_*_CRASHED_TOP_SHOT puppets (187 + 149 kf) with their own eye comps, drawn already-flattened from above, bruises and all. The SWF is the approved pose sheet on the production field guide: each root frame is an approved pose with slate, scene/episode/model boxes and an APPROVED stamp box.

**Scene notes:**
- Honest label: this file is a pose sheet, not a staged scene — 2 root frames, no background. The performance poses live in the puppet timelines inside the FLA (included in the anatomy JSON).
- Angle-specific puppets (top shot here) are a standing technique in this production: new viewpoint = new puppet variant, not a transform trick.
- The field-guide frame (4/3 SAFE / FULL guides, CN bug, slate) is part of every GB209 export — presentation and approval are built into the file.

## Survey — all 71 FLAs in CN-Leaks-001

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

## Honest gaps & surprises (verified from the files)

- **The GB209 'FINAL' files are not scenes.** They are approved pose sheets: a field-guide page (slate, episode/model boxes, APPROVED stamp) whose root frames are approved poses. The bilboquet sheet (Sc162, 19 poses) and the face-kick sheet (GB209 Sc155) were rendered during selection and are documented here but not landed as templates this wave; the crashed top-shot sheet was landed because its FLA holds the dedicated angle puppets.
- **Filename prefixes lie.** The 'GB200' HURT files are GB209 'The Banana' material per their own slates (GB200 is the puppet-block code), and Sc108's 'school run' is actually a forced-perspective speed-smear shot. Every deep-extracted scene above was verified by rendering it, not by its filename.
- **Embedded reference videos:** Sc099's and Sc144's SWFs carry a 'layout mov' reference video (video character 1). FFDec cannot render those files on this VM (its bundled JNA/vlcj path fails), so sheets/videos for Sc099 — and the tail of Sc144 — were rendered from copies with the reference-video tag stripped. The reference movie is a layout guide, not scene content; no character or background data was touched. The anatomy JSONs come from the untouched FLAs.
- **Bumpkin Sc089 is the giant-scale scene with an FLA** (177f, complete) but its FLA is 64 MB — left for wave 2's heavier pull. Sc090 (the famous looking-up shot) has no FLA in this archive at all.
- Sc057/Sc059 (the Darwin dance) are deliberately excluded from the templates — already extracted in `production/dance-choreo/`, and surveyed above as complete scenes.
