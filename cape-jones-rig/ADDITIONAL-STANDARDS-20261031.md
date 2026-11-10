# Additional industry standards — wired into Cape Jones (2026-10-31)

Workstream H, Mars 2026-10-31: find ANYTHING ELSE industry-standard beyond the
6 groups already pulled, and wire it up 100% too.

Already pulled (do NOT duplicate — see INDUSTRY-STANDARDS-PULL-20261031.md):
1) 12 Principles of Animation, 2) studio pipeline 10 stages, 3) colour management
(LUTs 70/70, Rec.709 gamma 2.4 L5), 4) rigging standards (v7c bone rig, node view,
drawing substitution, xsheet/Darwin beat ~14f @ 25fps on twos), 5) audio standards
(cue sheet v2, −14 LUFS), 6) free stack (OpenToonz/Tahoma2D, Synfig, Blender
Grease Pencil, Krita, FFmpeg, Brinimate).

Standing rules for this file: new dated file only — nothing Mars has seen was
overwritten. Labels are DEBUG ONLY, never in a final shot. Base art is never
recoloured; light/shadow/colour go on as separate layers. Barred ONLY, per
SHOW-BUILDING-METHOD.md: exact character likeness shipped as-is, character
literally, name, script dialogue, logo. No show character art, names, dialogue,
or logos are copied here — only tools, systems, and methods. Character images
are transform-only. Reference + transformation, not stealing content/characters
(Robot Chicken / South Park / Family Guy / Simpsons style of working, as framed
in SHOW-BUILDING-METHOD.md).

## What "wired" means here — and what it does not

"Wired" in this file means BOTH of these, per the task rule — a standard that is
only listed is NOT counted:
(a) it is cited in a Cape Jones doc (this doc, which is a Cape Jones doc), AND
(b) it is given a concrete Cape Jones application: a named artifact, template,
field, or check it now governs.

"Wired" as a template/spec does NOT mean executed per shot. Every section below
therefore carries a "Still owed" line with honest counts. Template-level wiring
for all 7 groups is the claim of this file; per-shot execution is a separate
pass and is NOT claimed.

## Score

| # | Standard group | Wired (template/spec level) | Per-shot execution still owed |
|---|---|---|---|
| 1 | Storyboard + animatic | YES — template + panel fields + animatic spec below | Boards drawn 0/30 shots; animatics built 0/30 |
| 2 | Camera language | YES — shot-size/angle/180°/staging/depth tables + layout-pass fields | Layout passes applying them 0/30 (room 2.5x lock already exists, see §2) |
| 3 | Editing | YES — cut rules + hold-length table mapped to punch + dance | Edited sequences cut to these rules 0/30 |
| 4 | Sound design (foley/ambience/whoosh/impact) | YES — layer stack mapped to the 5 cue-sheet cues | Recorded final audio 0% (demo tones only, DEMO ONLY) |
| 5 | Lip-sync (phoneme timing, viseme holds, mouth charts) | YES — timing rules + phoneme→viseme map for Pack 4 | Dialogue shot built 0/1; Mars approval of Pack 4 0/5 sets |
| 6 | Background painting | YES — perspective/light-key/atmosphere/layer rules mapped to the 4 new backgrounds | Final painted backgrounds approved 0/4 (new painted files exist, approval owed) |
| 7 | Title/credits + delivery | YES — companion sections extending delivery-spec.md (not replacing it) | Delivery frame size + safe-area drawing + archive still open (see §7) |

**Standards wired (template/spec level): 7/7 = 100%.**
**Standards executed per shot: 0/30 — not claimed.**

---

## 1. Storyboard + animatic standards

### Public source (named)
- Standard studio storyboard practice: one panel per shot (or per camera setup),
  with panel number, shot description/action, camera instruction, and dialogue /
  sound-effect columns — the field set used in studio board templates including
  Toon Boom Storyboard Pro's default panel fields.
- Animatic practice: timed board panels cut to scratch/temp audio at the delivery
  frame rate, with frame-accurate timing on an exposure sheet — the method already
  wired in PIPELINE-TEMPLATE-20261031.md stage 3 via
  `production/pipeline/animatic_builder.py` (storyboard images + timing + temp
  audio → timed animatic, cape-jones repo, verified 2026-10-31).
- Timing discipline: Richard Williams, *The Animator's Survival Kit* — timing
  written in frames before drawing; holds and moves decided on the board, not
  discovered in clean-up.

### Cape Jones application (concrete — not a list)
- This section is the storyboard/animatic template for the 30-shot list. It does
  NOT duplicate Workstream D's shot specs: D owns per-shot camera/background/LUT/
  effects/audio/QC values; this section owns the board panel format and the
  animatic assembly rule that every shot's spec must pass through.
- Board source frames: v7c poses rendered with labels=False clean mode
  (`reposes-v7c-clean/*.png`), same rule as PIPELINE-TEMPLATE stage 2. A board
  panel that shows a red debug label fails the gate — labels are DEBUG ONLY.
- Frame-rate rule: Cape Jones boards are timed at 24 fps (rig default). Darwin
  dance source material is 25 fps and must be converted, never mixed into a
  24 fps animatic timeline (same rule as PIPELINE-TEMPLATE stage 10).
- Scratch audio rule: animatic audio is temp/scratch only, labelled DEMO ONLY
  until recorded — same status as the 5 demo cues in §4. A scratch track never
  ships as final audio.

### Storyboard panel template (required fields per panel)
| Field | What goes in it | Cape Jones rule |
|---|---|---|
| Panel / shot no. | `S01` … `S30`, panel `P01` … within the shot | Matches the 30-shot list numbering; one shot = one row in the tracker |
| Board image | Clean v7c pose frame (labels off) | Silhouette must read at thumbnail size (12 Principles #3, staging) |
| Action | What the character does, in one line | Must name the key pose (apose / punch / flex / dance / jump / seated) |
| Camera | Size + angle + move (terms from §2) | Must use a §2 shot size and angle name, not free text ("close" is not a size) |
| Timing | Frames + hold, on the exposure sheet | Normal on 2s, snaps on 1s, holds 6/12/24 (see §3); timing written before in-betweens |
| Dialogue / SFX | Line cue or SFX cue id | Dialogue maps to §5 visemes; SFX maps to a §4 cue id — no orphan cues |
| Transition | Cut / fade / dissolve / hold | Default is a cut (§3); anything else must be named and justified |

### Animatic assembly spec
1. Panels in shot order, each held for its exposure-sheet frame count.
2. Scratch audio laid under at the cue-sheet timecodes (cue sheet v2).
3. Export at 24 fps; check: panel count = shot count, total frames = sum of
   exposure-sheet holds, no panel held 0 frames, no audio cue without a panel.
4. Animatic is a timing approval artifact: Mars approves timing from the
   animatic, not from finished clean-up.

### Gate — do not pass without it
- [ ] Every panel has all 7 fields above; a panel missing camera or timing fails.
- [ ] Board reads in silhouette at thumbnail size; debug labels absent.
- [ ] Animatic total frames reconcile with the exposure sheets; frame rate is
  24 fps throughout (25 fps Darwin material converted).

### Still owed
- Boards drawn: 0/30 shots. Animatics built: 0/30. Per-shot 12-principles checks:
  0/30 (see INDUSTRY-STANDARDS-PULL-20261031.md). Scratch audio is demo tones
  only; recorded audio 0%.

---

## 2. Camera language

### Public source (named)
- Shot sizes and angles: standard film grammar as codified in Nicholas Proferes,
  *Film Directing Fundamentals* and in standard cinematography teaching (Blain
  Brown, *Cinematography: Theory and Practice*): extreme wide / wide / full /
  medium / medium close-up / close-up / extreme close-up; eye-level / low /
  high / bird's-eye / worm's-eye; over-the-shoulder and point-of-view setups.
- 180-degree rule and screen direction: the axis-of-action rule from classical
  continuity editing (Proferes; Walter Murch, *In the Blink of an Eye*): once a
  camera side of the axis is established, the camera stays on that side unless
  a neutral or establishing shot resets it, or screen direction flips
  deliberately and is flagged.
- Staging and depth: Frank Thomas & Ollie Johnston, *The Illusion of Life*
  (staging principle) + standard layout practice: foreground / midground /
  background layers, leading room, headroom, and floor contact as depth cues.

### Cape Jones application (concrete)
- This section governs the layout passes, and it extends — does not replace —
  `layout-passes-templates.json` (room / flying / rooftop / alley / desk) and
  PIPELINE-TEMPLATE stage 4. New required layout fields (add to that template
  on its next dated revision; this doc is the authority until then):
  `shot_size`, `camera_angle`, `axis_side` (L/R of the action axis),
  `foreground_layer`, `midground_layer`, `background_layer`,
  `floor_contact` (feet-on-floor Y, or "n/a — flying").
- Room 2.5x lock (existing, PIPELINE-TEMPLATE stage 4): room only, character
  full body in frame, chair back at waist at 2.5x; seated = standing − 0.2
  (2.5x → 2.3x, approximate, verify visually). Under this section the room lock
  is now ALSO a camera spec: room default = full shot, eye-level, static,
  axis side recorded on the first room pass and held for every later room shot
  unless a neutral reset shot is boarded.
- Punch framing: punch impact locked −110 across-up (see §3) is a medium /
  medium-close framing decision, not just a pose: the punching arm must read
  against background, not against the torso, at the chosen size. If it does
  not read, change the size or the staging — do not add effects to rescue it
  (12 Principles #3).

### Shot-size table (use these names, exactly)
| Size | Frames | Cape Jones use |
|---|---|---|
| Extreme wide (EWS) | Character small in environment | Flying / skyline establishing |
| Wide (WS) | Full environment + character | Rooftop, alley establishing |
| Full shot (FS) | Head to feet, full body | Room default (2.5x lock); dance full-body |
| Medium full / cowboy | Head to knees | Flex / power pose alternative |
| Medium shot (MS) | Head to waist | Dialogue default (with §5 visemes) |
| Medium close-up (MCU) | Head to chest | Punch −110 impact framing |
| Close-up (CU) | Head / face only | Reaction, viseme read, eye-strip read |
| Extreme close-up (ECU) | Eye / fist / gauntlet detail | Impact detail insert only — never as the only punch frame |

### Angle + 180° + staging + depth rules
- Angles: eye-level is the default; low angle = power (flex, punch impact);
  high angle = vulnerability or scale (alley, rooftop edge). A low/high choice
  must be recorded in the shot spec with its story reason.
- 180° rule: record `axis_side` on the first shot of every scene. Every later
  shot in that scene keeps the same side unless the board includes a neutral
  shot (character moving straight toward/away from camera) or an establishing
  reset — either must be named in the board's Transition field (§1).
- Staging: one idea per shot; action reads in silhouette at thumbnail size.
  Character centre is the layout default; off-centre staging needs a reason
  (leading room for a punch travel direction, or a foreground prop).
- Depth: every layout pass names all three layers — foreground (dressing /
  prop, may be out of focus in compositing), midground (character + floor
  contact), background (painted background, §6). A pass with an empty
  foreground layer must say "none — intentional" rather than leaving it blank.
- Floor contact: feet on the floor line in every grounded shot; a floating
  character fails the layout gate. Flying shots record "n/a — flying" plus the
  cape state (draped / lying-flat / swinging / billowing, Pack 4).

### Gate — do not pass without it
- [ ] Layout pass names shot size + angle + axis_side + all three depth layers
  + floor contact (or flying exception).
- [ ] Room passes honour the 2.5x lock (chair back at waist; seated 2.3x approx).
- [ ] No axis cross without a boarded neutral/reset shot; no floating feet in
  grounded shots.

### Still owed
- Layout passes revised to the new fields: 0/5 scenes (templates exist, passes
  applying this section do not yet). Per-shot camera specs for the 30-shot list
  are Workstream D's, not duplicated here.

---

## 3. Editing standards

### Public source (named)
- Cutting on action: classical continuity practice (Murch, *In the Blink of an
  Eye*; Karel Reisz & Gavin Millar, *The Technique of Film Editing*): cut
  mid-movement, not at the end of a movement, so the viewer's eye follows the
  action across the cut.
- L/J cuts: standard sound-editing terms — an L-cut carries the outgoing
  shot's audio under the incoming picture; a J-cut brings the incoming shot's
  audio in before its picture. Both are named in the edit decision list, never
  improvised in the mix.
- Hold lengths and rhythm: animation timing practice (Williams, *The
  Animator's Survival Kit*; Thomas & Johnston) — holds let a pose register;
  cutting rhythm follows the action beat, not a fixed shot length.

### Cape Jones application (concrete)
- This section governs the cut from shot to shot across the 30-shot list and
  two named sequences: the punch sequence and the dance beat grid. It does not
  re-specify per-shot content (Workstream D owns that); it owns the edit rules
  between shots and within sequences.
- Punch sequence edit (existing locked frames, now under edit rules):
  - Punch impact locked −110 across-up = the impact frame (the cut-ON-action
    target: cut into the punch mid-swing, land on −110, do not cut to a static
    pre-punch pose and then start the swing).
  - Punch sequence frame −70 across-down = the before/during/after frame for
    the sequence (approved for before/during/after punch) — it is the
    anticipation/continuation frame the cut crosses, not a second impact.
  - Edit order for the punch beat: anticipation (windup, hold 6) → snap
    (extend, hold 2, on 1s) → impact −110 (hold 12) → recover (hold 6). Those
    holds are the existing SHOT-SPECS-V6-20261031.md punch spec, now also the
    edit's hold-length authority for this beat.
- Dance beat grid edit: Darwin beat ~14f @ 25fps on twos (~107 BPM), converted
  to 24 fps for Cape Jones timelines (do not mix rates). Cuts in a dance
  sequence land ON the beat grid, not between beats; a cut that lands off-grid
  must be re-timed to the nearest beat or justified as a deliberate off-beat
  accent in the edit list.
- Hold-length table (Cape Jones values, from SHOT-SPECS-V6 + clip specs):
| Hold | Frames @24fps | Use |
|---|---|---|
| Snap | 2 | Extend-snap (punch F7), takeoff (jump F7) — fast moves, on 1s |
| Short hold | 6 | Windup, recover, crouch, land, apose bookends |
| Standard hold | 12 | Impact-hold (punch F9), contacts/passing (walk), dance beats, tuck, hovering |
| Long hold | 24 | Flex-hold (flex F7) — power-pose register; use sparingly, never as a default |
- Rule: no hold shorter than 2 frames (unreadable) and no default hold longer
  than 24 frames without a story reason recorded in the shot spec. A 24-frame
  hold that is just "waiting for the next shot" is an edit failure, not a pose.
- L/J cut application: dialogue scenes (when built, §5) use a J-cut to bring the
  next speaker's voice in before the picture cut, and an L-cut to let a line's
  tail play over the reaction shot. Punch/dance sequences default to straight
  cuts on action; an L/J cut there must be named in the edit list.

### Gate — do not pass without it
- [ ] Edit decision list exists: every cut named (straight cut on action /
  L-cut / J-cut / fade / dissolve), with the frame it lands on.
- [ ] Punch beat holds match windup 6 / snap 2 / impact 12 / recover 6; impact
  frame is −110, sequence frame is −70 — the two are not swapped.
- [ ] Dance cuts land on the converted 24 fps beat grid (25 fps source
  converted, never mixed).
- [ ] No hold < 2f or unexplained hold > 24f.

### Still owed
- Edit decision list built: 0/30 shots. Edited punch sequence cut to these
  rules: 0/1. Edited dance sequence cut to the beat grid: 0/1. Dialogue
  L/J-cut application: 0/1 (no dialogue shot exists yet).

---

## 4. Sound design (distinct from music)

### Public source (named)
- Foley: Vanessa Theme Ament, *The Foley Grail* — footsteps, cloth, props and
  body sounds performed to picture, in sync, as a separate layer from music
  and dialogue.
- Sound design layers: David Sonnenschein, *Sound Design: The Expressive Power
  of Music, Voice and Sound Effects in Cinema* — ambience beds, spot effects,
  and designed impacts/whooshes as distinct layers with distinct jobs; and
  standard film-sound practice (Walter Murch's "sound montage" layering) —
  no single sound carries a moment alone.
- Delivery: −14 LUFS target and FFmpeg LUFS check (already wired, cue sheet v2
  + PIPELINE-TEMPLATE stage 10). Sound design layers are mixed to that target;
  loudness is checked with FFmpeg, not by ear alone.

### Cape Jones application (concrete — VFX-adjacent audio design, not music)
- This section is the sound-DESIGN layer stack for the existing 5 cue-sheet
  cues (`showcase/audio/audio-cue-sheet-v2.json`, all DEMO ONLY). It does not
  replace the cue sheet and does not add music cues: music (if any) is a
  separate layer with its own cue ids. Every cue below gets its design layers
  recorded against its existing cue id — no new cue is invented here.
- Layer stack (every designed moment uses as many of these as it needs, and
  records which ones it used):
| Layer | Job | Cape Jones rule |
|---|---|---|
| Ambience bed | Continuous room/street/rooftop/alley tone under the scene | One bed per scene, not per shot; bed level stays below dialogue/SFX; a scene change = a bed change, crossfaded, never hard-cut |
| Foley — footsteps | Foot contacts in sync with the walk cycle | Walk cue: steps land on contact frames (walk contacts F1/F25 pattern), not on a free rhythm |
| Foley — cloth/body | Cape movement, body shifts, gauntlet handling | Cape states (swinging/billowing) get a cloth layer whose intensity follows the cape state, not a generic rustle |
| Whoosh | Fast movement through air (punch swing, jump rise, fighting-stance move) | Whoosh leads the impact by 2–4 frames and ends AT the impact frame — a whoosh that continues past impact fails sync |
| Impact | The hit itself: punch impact, landing | Impact = layered hit (low thump + crack/noise transient + tail), not a single tone; impact frame = −110 punch frame / landing frame, frame-accurate |
| Tail / ring-out | Decay after an impact or power moment | 4-frame fade precedent from cue sheet v2 (impact "out 4f"); tails are part of the cue, not trailing noise |
- Mapping to the 5 existing cues (cue id → design layers):
| Cue (existing, DEMO ONLY) | Design layers to record at build |
|---|---|
| Punch impact | Whoosh (leads, ends at −110) + impact (thump + transient) + tail (out 4f) |
| Fighting stance whoosh | Whoosh only + cloth (gauntlet/cape shift); NO impact layer — a stance move is not a hit |
| Walk steps x2 | Foley footsteps (2 contacts, on contact frames) + ambience bed (street/town) underneath |
| Jump rise | Whoosh (rise) + cloth (cape billowing) + landing impact is a SEPARATE cue when the landing shot is built — do not fold it into the rise |
| Dance beat x4 | Beat accents (4, on the converted 24 fps grid) + foley steps on the beat; dance music, if added, is a separate music layer, not the beat accents |
- Demo-tone status (honest): all 5 cues are currently synthesized demo tones /
  noise, labelled DEMO ONLY. The design layers above are the spec the recorded
  replacements must satisfy — they are not a claim that recorded layers exist.

### Gate — do not pass without it
- [ ] Every cue records which design layers it uses (from the stack above);
  a cue with no layer list fails.
- [ ] Whoosh ends at the impact frame; footsteps land on contact frames;
  ambience bed is per-scene, not per-shot.
- [ ] Mix checks at −14 LUFS via FFmpeg; demo tones stay labelled DEMO ONLY
  until replaced by recorded audio.

### Still owed
- Recorded final audio: 0% (demo tones only, recorded 0%). Foley sessions,
  ambience recordings, and designed whoosh/impact recordings: 0/5 cues
  recorded. Music layer (if Mars wants one): not specced here — separate decision.

---

## 5. Lip-sync standards

### Public source (named)
- Mouth chart / phoneme shapes: Preston Blair, *Cartoon Animation* — the
  standard mouth-shape chart (rest, wide, open, closed, etc.) that studio
  lip-sync charts descend from; and the standard viseme-set practice used in
  studio dialogue animation (a small closed set of mouth shapes standing in
  for the full phoneme inventory, timed on the exposure sheet).
- Timing: Williams, *The Animator's Survival Kit* — dialogue on 2s normally,
  on 1s for fast snaps; mouth shapes held 2–4 frames for readability, never
  changed every frame; anticipation of a mouth shape by 1 frame on hard
  consonants (M/B/P closure lands ON the consonant frame, not after it).

### Cape Jones application (concrete — prep, NOT approval)
- Applies to Pack 4 visemes 14/14 (`pack4-20261031/visemes/`,
  PACK4-REPORT-20261031.md): rest, EE, EH, AH, OH, OO, M/B/P, F/V, L, S/Z, TH,
  R, W, G/K. Pack 4 status is PREP ONLY: pieces exist, Mars approval is still
  owed for all 5 Pack 4 sets (visemes, eye strips, cape states, foreshortened
  forearm, 3/4 head). Nothing in this section claims approval.
- Phoneme → viseme map (the chart every dialogue shot must use; one viseme
  per phoneme group, no invented shapes):
| Viseme (Pack 4) | Phonemes it covers | Hold rule |
|---|---|---|
| rest | Silence, pauses, neutral | Default between lines; hold, do not cycle |
| EE | EE, I (as in "see") | Narrow wide shape; 2–3f |
| EH | EH, E (as in "bed") | Mid-open; 2–3f |
| AH | AH, A (as in "father") | Open; 2–4f, longest vowel hold |
| OH | OH, O (as in "go") | Rounded mid; 2–3f |
| OO | OO, U (as in "boot") | Small round; 2–3f |
| M/B/P | M, B, P (closed) | Full closure, lands ON the consonant frame; 1–2f, never skipped |
| F/V | F, V | Lower lip to upper teeth; 2f |
| L | L | Tongue-tip shape; 2f |
| S/Z | S, Z | Near-closed with teeth; 2f |
| TH | TH | Tongue between teeth; 2f |
| R | R | Slight pucker; 2f |
| W | W, Q | Tight round, leads into the following vowel by 1f |
| G/K | G, K (throat) | Brief open/neutral — do not over-articulate; 1–2f |
- Exposure-sheet fields for dialogue (add to the shot spec on its next dated
  revision): `phoneme_track` (phoneme per frame or per 2-frame pair),
  `viseme_clip` (already a field in `audio-cue-template.json`), `eye_strip`
  (one of Pack 4's 8 expression strips, so the eyes match the line's feeling —
  a neutral eye strip under an angry line fails the gate).
- Timing rules: dialogue on 2s normally, on 1s for fast snaps (same as clips);
  viseme holds 2–4 frames (M/B/P and G/K excepted at 1–2f); no viseme change
  every single frame; consonant closures (M/B/P) are never dropped for speed —
  if a line is too fast to show a closure, the line is re-timed, not the mouth
  faked.
- Dialogue shot status: NO dialogue shot exists yet (SHOT-SPECS-V6-20261031.md:
  "NO shot yet — needs viseme pieces"). This section is the prep chart for
  that shot, not the shot itself.

### Gate — do not pass without it
- [ ] Dialogue exposure sheet has a phoneme track + viseme per phoneme group
  from the map above + a matching eye strip.
- [ ] M/B/P closures present and on the consonant frame; no 1-frame viseme
  churn; holds within 2–4f (1–2f for M/B/P, G/K).
- [ ] Pack 4 approval recorded by Mars before any dialogue shot ships — prep
  pieces alone do not pass this gate.

### Still owed
- Mars approval of Pack 4: 0/5 sets (visemes 14/14 are prep, not approved).
- Dialogue shot: 0/1. Hand-drawn lip-sync set (if Mars wants one beyond the
  Pack 4 first-pass clean ovals/teeth/tongue style): 0/1, separate step.

---

## 6. Background painting standards

### Public source (named)
- Perspective: standard linear-perspective practice (1/2/3-point perspective,
  horizon line + vanishing points) as taught in studio layout/background
  training and codified in Disney layout practice (see e.g. *Layout and
  Background* materials from the Disney studio tradition; and John K. Wright /
  standard perspective teaching: horizon at the character's eye level for an
  eye-level shot, vanishing points placed before painting, never guessed after).
- Light key: the background-painting light-key system — one key light per
  scene, recorded as a colour/temperature + direction, with shadow side and
  lit side consistent across every object in the painting (the same discipline
  as UNIVERSE-COLOR-LANGUAGE.md Dialect 1, applied to the background plate).
- Atmospheric perspective: standard painting practice (Leonardo's aerial
  perspective, as used in studio background painting): distant planes lose
  contrast and shift toward the sky colour; near planes keep full contrast and
  saturation. Distance is painted, not just scaled.
- Paint layers: standard background layer order — sky / far plane / mid plane /
  near plane / foreground dressing, painted as separable layers so a colour
  shift or grade can target one plane without repainting the whole background.

### Cape Jones application (concrete)
- Applies to the 4 new painted backgrounds in
  `showcase/backgrounds-new-20261031/`: `bg-alley-new-20261031.jpg`,
  `bg-desk-new-20261031.jpg`, `bg-flying-new-20261031.jpg`,
  `bg-rooftop-new-20261031.jpg`. These files exist as new painted backgrounds;
  final-painted-background approval is still owed (TRACKER-20261031.md listed
  final painted backgrounds 0/4 for flying/rooftop/alley/desk — that count is
  the approval count, and this section does not change it).
- Per-background rules (record in the shot spec for every shot that uses one):
| Background | Perspective | Light key (must match the shot's LUT/key) | Atmospheric treatment |
|---|---|---|---|
| Alley | 1-point (or 2-point if the camera angle says so, §2); vanishing point on the horizon at eye level | Scene key; shadow side consistent down the alley walls | Far end of the alley: lower contrast, shifted toward sky/key colour |
| Desk (room) | Room interior perspective matching the 2.5x room lock (§2) | Warm interior key (matches L2 v2 warm-rim approval); desk props lit from the same side as the character | N/A indoors — depth by overlap + scale, not aerial shift; foreground desk edge = near plane |
| Flying (sky) | Horizon + sky planes; no ground vanishing point unless a ground plane is in frame | Sky key per scene (daylight / golden-hour / night-city LUT family) | Distant skyline/planes: strong aerial shift; near clouds: full contrast |
| Rooftop | 2-point for the roof edge + skyline; horizon at eye level | Scene key; roof plane lit side matches character lit side | Skyline planes: stepped aerial shift per distance band |
- Paint-layer order (required for every one of the 4, so grades/shifts can
  target planes): sky → far plane → mid plane → near plane → foreground
  dressing. A background delivered as a single flattened layer fails the gate
  for any shot that needs a plane-targeted grade or shift.
- Atmosphere shift (JoJo Dialect 2, UNIVERSE-COLOR-LANGUAGE.md): an
  environment-only shift (e.g. yellow sky / purple hills, Morioh use) is
  applied to the BACKGROUND planes only, character stays in base palette, and
  is recorded as shift name + scope (environment only) + return to base in
  the shot spec. A shift applied to the background without a recorded trigger
  + return is a mistake, not a style — same rule as Dialect 2. A shift is
  never painted permanently into the only copy of a background: the base
  background file is kept, the shift is a layer/grade on top (base art is
  never recoloured — same rule as the character).

### Gate — do not pass without it
- [ ] Vanishing point(s) + horizon recorded before painting; horizon matches
  the §2 camera angle (eye-level default).
- [ ] Light key recorded and consistent: background lit side = character lit
  side for the same shot; rim follows the (possibly shifted) key.
- [ ] Distant planes show atmospheric shift (lower contrast, toward sky
  colour); paint layers separable in sky → far → mid → near → foreground order.
- [ ] Any atmosphere shift has trigger + scope + return recorded; base
  background file preserved unshifted.

### Still owed
- Final painted background approval: 0/4 (files exist, approval owed).
- Background layout line-art versions: not yet built (MODEL-SHEET-VISEME-PLAN.md
  §3). Per-shot background placement: 0/30.

---

## 7. Title/credits + delivery standards (companion to delivery-spec.md)

### Public source (named)
- Safe areas: SMPTE / EBU safe-area practice — action-safe 90% (action must
  stay inside 90% of frame width/height) and title-safe 80% (titles/credits
  text must stay inside 80%), centred; the standard broadcast safe-area
  convention used in delivery specs (SMPTE RP 218 / EBU R95 lineage).
- Title cards and credits order: standard film/TV credit-block order
  (production → direction → animation → design → sound → music → special
  thanks, with the show title card first and end credits in that department
  order) as used in broadcast delivery specs; title-card typography stays
  inside title-safe and is held long enough to read (minimum 2 seconds for a
  main title card, 1 second per credit line as a floor, not a target).
- File naming and archive: standard post-production naming + archival practice
  (SMPTE / studio delivery conventions): human-readable, sortable, versioned
  names (`show_episode_scene_shot_version.ext`), a delivery manifest with
  SHA-256 per file, and a preservation copy kept separately from the working
  copy — the same manifest discipline already used in Cape Jones
  (`frame-proof-manifest.json`, clip manifests).

### Cape Jones application (concrete — companion, NOT a replacement)
- This section EXTENDS `delivery-spec.md` (template only: 24 fps, 1100x1500
  rig canvas explicitly NOT a delivery frame size, PNG frames + MP4 finish,
  −14 LUFS). It does not duplicate or overwrite that doc, and it does not set
  the delivery frame size — that decision is still open (see Still owed).
  Workstream D owns the delivery spec doc; this section owns only the
  title/credits + archive additions that D's doc does not contain.
- Title/credits additions:
  - Title card: show title inside title-safe 80%, held ≥ 2 seconds, on a
    clean background or a held establishing frame — never over a fast-moving
    action frame. Title-card art uses the approved base palette; a JoJo shift
    on a title card must be named like any other shift.
  - Credits order (Cape Jones): show title → created/directed → animation
    (rig, keys, clean-up) → backgrounds/layout → colour/compositing → sound
    design → music (if any) → special thanks. Every credit line inside
    title-safe 80%; end-credit roll speed set so each line is readable
    (≥ 1 second per line on screen as a floor).
  - Safe-area drawing (new work this section creates): safe-area guides
    (action-safe 90% + title-safe 80%) to be drawn on layout passes as a
    DEBUG-ONLY overlay — same rule as labels: the guides are for checking,
    never burned into a final shot. `delivery-spec.md` already said "safe
    areas: to be marked on layout passes (not yet drawn)" — this section
    defines what those marks are (90%/80% rectangles, centred).
- File-naming addition (applies to every delivery file from now on):
  `cape-jones_<episode>_<scene>_<shot>_v<nn>.<ext>` — e.g. a punch-shot
  delivery frame set is named by scene + shot + version, never by a bare
  date or a tool default. Version increments on every re-delivery; a
  re-delivery never overwrites a delivered version (new dated/versioned file
  only — same standing rule as the rig docs).
- Archive addition (applies to every delivery):
  - Delivery manifest per delivery: file list + SHA-256 per file + frame
    count + frame rate + LUT/grade name + loudness (−14 LUFS check result) +
    title/credits version. Same manifest discipline as
    `frame-proof-manifest.json`, extended to the finished delivery.
  - Preservation copy: one copy of the delivered manifest + final frames /
    MP4 + cue sheet + shot specs kept as the archive set, separate from the
    working rig folder; the archive set is read-only after delivery (no
    in-place edits — a correction is a new version).
  - Final-output check (existing rule, restated here so the archive inherits
    it): final output is checked by remote API size + SHA after repo merge,
    never by local commit alone (PIPELINE-TEMPLATE stage 10).

### Gate — do not pass without it
- [ ] Title card inside title-safe 80%, held ≥ 2s; credits in the order above,
  all inside title-safe, each line readable ≥ 1s.
- [ ] Safe-area guides (90% action / 80% title) drawn as DEBUG-ONLY overlays on
  layout passes; no guide burned into a final shot.
- [ ] Delivery files follow `cape-jones_<episode>_<scene>_<shot>_v<nn>.<ext>`;
  delivery manifest (files + SHA-256 + frames + fps + LUT + LUFS + title/
  credits version) exists; archive set stored read-only, separate from working files.

### Still owed
- Delivery frame size: still to set (`delivery-spec.md` — the 1100x1500 rig
  canvas is NOT a delivery frame size). Safe-area guides drawn on layout
  passes: 0/5 scenes. Title card designed: 0/1. Credits list compiled: 0/1
  (names/roles to be confirmed by Mars — no names are invented here).
  Archive set created: 0/1 (no delivery has been made yet).

---

## Cross-links (so this file is wiring, not a standalone list)

| This section | Already-wired doc it extends | What it adds that the other doc lacks |
|---|---|---|
| §1 Storyboard/animatic | PIPELINE-TEMPLATE stages 2–3 | Panel field template + animatic assembly spec + silhouette/timing gates |
| §2 Camera | PIPELINE-TEMPLATE stage 4; layout-passes-templates.json | Shot-size/angle names, 180° rule, depth-layer + floor-contact fields, room 2.5x as a camera spec |
| §3 Editing | SHOT-SPECS-V6-20261031.md (holds); PIPELINE-TEMPLATE stage 6 | Cut rules (on action, L/J), hold-length table, punch −110/−70 + dance-grid edit rules |
| §4 Sound design | showcase/audio/audio-cue-sheet-v2.json; PIPELINE-TEMPLATE stage 10 | Design layer stack + per-cue layer mapping (foley/ambience/whoosh/impact/tail) |
| §5 Lip-sync | pack4-20261031/PACK4-REPORT-20261031.md; audio-cue-template.json | Phoneme→viseme map + hold rules + dialogue exposure-sheet fields |
| §6 Backgrounds | showcase/backgrounds-new-20261031/; UNIVERSE-COLOR-LANGUAGE.md | Perspective/light-key/atmosphere/layer rules per background + shift-on-background rule |
| §7 Title/credits/delivery | delivery-spec.md (template only) | Title-safe/action-safe definitions, title/credits order, file naming, archive manifest |

## Overall still owed (honest counts, not claims)
- Boards drawn 0/30; animatics built 0/30; shots run end-to-end 0/30.
- Layout passes to the new §2 fields 0/5 scenes; safe-area guides drawn 0/5.
- Edit decision list 0/30; punch sequence edited 0/1; dance sequence edited 0/1.
- Recorded final audio 0% (demo tones only, DEMO ONLY); foley/ambience/whoosh/
  impact recordings 0/5 cues.
- Pack 4 Mars approval 0/5 sets; dialogue shot 0/1; hand-drawn lip-sync set 0/1.
- Final painted background approval 0/4; background line-art versions not built.
- Delivery frame size unset; title card 0/1; credits compiled 0/1; archive set 0/1.
- Carried from the 6-group pull: per-shot 12-principles checks 0/30; ACES in a
  colour-managed tool 0/1; viewed Blender render 0/1; per-shot god-ray placement
  0/30; Harmony trial install + method study report pending (separate lane).
