# JONES VERSIONS — Draw Jones, Video Jones, Rig Jones, and the Other Joneses

**Owner direction: 2026-11-23 06:48 + 06:49 + 06:54 + 06:55 EST. Consolidated 2026-11-23 and landed in `mhvnsnt/cape-jones` main.**

**This whole way of categorizing and organizing production / director / animation / development talk is THE JONES MODEL, for short THE CAPE JONES MODEL.** It is UNIVERSAL across all the owner's projects — if he says any of these terms while working on Dream Girl, Bannon, the Bastard, God Molecule, or Western Heart, it means the same thing as in Cape Jones. See §8 for the per-project meaning.

**"Clean Up Jones this shit"** = take the current official rig / build / character as it is (Rig Jones 1), clean it up to the next level (Rig Jones 2 / Clean-Up Jones 1) — fix the amateur stuff, make it industry-standard, no regressions, prove it with a short test before a full render/cut.

## NAMES THAT CHANGED — read this first (owner rename, 2026-11-23 06:57 EST)

- **SHEET JONES (S-H-E-E-T)** = model sheets. Turnaround front/side/back, construction, proportions, expressions, hands, colors — on paper. This is what "Model Jones this nigga" meant on 2026-11-23 06:56 EST: making his sheets on paper. **Sheet Jones is the foundation: without a good Sheet Jones, Draw Jones and Rig Jones end up different and fucked up — and Model/3D Jones and Rig Jones too. Everything gets fucked up if Sheet Jones ain't good.** (owner, 2026-11-23 06:58 EST) **Nuance (owner, 2026-11-23 06:59 EST): they are the same guy right now, just a little different physiques (slim puppet vs bulky drawn) — animation flair, human imperfection. Alignment converges version by version; by V10 all Joneses are the same guy. Sheet Jones drives that convergence — do not over-correct the flair away.**
- **MODEL JONES = 3D JONES. 3D JONES = MODEL JONES. Same thing, interchangeable.** "Model" = the 3D model in Blender and all that. If the owner says Model Jones, that means 3D Jones. If he says 3D Jones, that means Model Jones.
- **"Model Jones" NEVER means sheets anymore.** Any old text that used "Model Jones" to mean sheets now says **Sheet Jones**. Any old text that meant the 3D model now says **Model Jones / 3D Jones**.

**"Sheet Jones this nigga"** = make his model sheets / turnaround / construction on paper. **"Model Jones this nigga" / "Rig Jones this nigga, he ain't got no Rig Jones"** (owner, 2026-11-23 06:56 EST, Dream Girl example — owner confirmed "That's damn right. You got it."): **Model Jones** = build his 3D model / first official rig (Rig Jones 1) because he has none yet — bones, moving hands/fingers, mouth, blink, proved with a movement test — then **Clean-Up Jones** to level it up.

**Repo:** `mhvnsnt/cape-jones`. **Workdir:** `~/workspace/_cape-jones-parking-lot-2d/`.
**Rule for this whole doc:** the names below are the owner's terms, used exactly as he said them. A version is only "done" when a whole video proves it — never frames alone, never a claim without a file.

---

## 0. The three Joneses, in one paragraph

- **Draw Jones** = the hand-drawn Jones. The drawings themselves. Already really good — owner said so.
- **Video Jones** = Draw Jones brought to life as video. The drawn Jones moving in the actual video — not a slideshow, not a puppet substitute.
- **Rig Jones** = the Blender cutout-puppet Jones. Currently only V2. Must be perfected and upgraded all the way to V6, to the rig quality of Adventure Time / Regular Show / Amazing World of Gumball / Metalocalypse — so that when we use Rig Jones, it looks like Video Jones. Rig Jones has to get up to Draw Jones and Video Jones levels.

The test for all three is the same: **does it look like the drawn Jones moving, on TV, at 24fps?** If Rig Jones looks like a puppet and Video Jones looks like a slideshow, neither is done.

## 0a. THE JONES MODEL / THE CAPE JONES MODEL — universal

This whole way of categorizing and organizing production / director / animation / development talk is **THE JONES MODEL**, for short **THE CAPE JONES MODEL**. It is **universal across all the owner's projects**: if he says any of these terms while working on Dream Girl, Bannon, the Bastard, God Molecule, or Western Heart, it means the same thing as in Cape Jones.

- **Dream Girl** = clean up its character rigs / drawings using the Cape Jones pipeline it inherits (Cape Jones is Dream Girl's test ground).
- **Bannon** = clean up the universal 2K26 rig / models / animations.
- **Western Heart** = clean up fighter rigs / moveset data.
- **The Bastard and God Molecule** = same rule applied to their official rigs. Their specific Rig Jones 1 has **not** been given by the owner yet — recorded as pending his confirmation, do **not** invent their rigs.

**"Clean Up Jones this shit"** = take the current official rig / build / character as it is (Rig Jones 1), clean it up to the next level (Rig Jones 2 / Clean-Up Jones 1) — fix the amateur stuff, make it industry-standard, no regressions, prove it with a short test before a full render/cut.

**"Sheet Jones this nigga"** = make his model sheets / turnaround / construction on paper. **"Model Jones this nigga" / "Rig Jones this nigga, he ain't got no Rig Jones"** (owner, 2026-11-23 06:56 EST, Dream Girl example — owner confirmed "That's damn right. You got it."): **Model Jones** = build his 3D model / first official rig (Rig Jones 1) because he has none yet — bones, moving hands/fingers, mouth, blink, proved with a movement test — then **Clean-Up Jones** to level it up.

---

## 1. Draw Jones — the hand-drawn Jones

### Definition
Draw Jones is Jones as drawn by hand — every line, proportion, expression, and pose as it exists on paper / in the drawing files. He is the source of truth. Everything else (rig, video) is judged against him: if it does not look like Draw Jones, it is wrong, no matter how smooth the motion is.

### What Draw Jones actually is today (verified in the repo)
- **7 boards** — `production/2d-parking-lot/boards/cj-pl-01.png` … `cj-pl-07.png` + `BOARD-LIST.md`. The PURPLE LOT storyboard, Jones + Cape alone, no Fan.
- **8 poses** — `production/2d-parking-lot/poses/` + `POSE-LIST.md`: `pose-01-idle`, `pose-02-raise`, `pose-03-press`, `pose-04-shift`, `pose-05-lower`, `pose-06-nod`, plus `cape-01-billow` / `cape-02-settle` cape studies.
- **10 in-betweens** — `production/2d-parking-lot/inbetweens/` + `INBETWEEN-LIST.md`: `ib-01a-breath-in`, `ib-01b-breath-out`, `ib-02a-hand-drift`, `ib-03a-raise-mid`, `ib-03b-raise-high`, `ib-04b-click`, `ib-06a-lower-mid`, `ib-06b-arm-down-turn`, `ib-07a-nod-mid`, `ib-07b-pupil-half`.
- **Model sheets** — the design source of truth per the Playbook (`docs/CAPE-JONES-TV-SHOW-PLAYBOOK.md` §1, "Design once"): `characters/sheets/01-tpose-turnaround.jpg` (bind pose), `02-model-sheet-orthographic-turnaround.jpg`, `03-color-lighting-vfx-key.jpg` (palette + rim spec), `05-expression-eye-dart-matrix.jpg` (eye/pupil spec), `08-body-parts-limbs-capes.jpg` (parts). Locked palette: suit #FFFFFF, cowl #3E1473, skin #E5B28C, cape #000000.
- **Canon locks** (HANDOFF): white eyes default (pupils only for a specific beat), glove gag at PL-04, ending pupil rolls to audience with head NOT turning then hard cut to black, lighting shift sodium orange → broken-streetlight purple.

### What makes Draw Jones good (owner: "you did it really good")
- On-model proportions and construction — the T-pose / turnaround is locked (v8, 2026-10-31) and the boards hold it.
- Acting is in the drawing — the raise, the click gag, the nod, the pupil button are all *drawn* performances, not poses the computer invented.
- The line, the colour, the cape shape are the show's look. The production grade (sodium → purple) is applied to the drawing, not instead of it.

### What Draw Jones still needs
- More drawings, not more holding. V1 had 17 drawings across 480 frames — that is why it read as a slideshow. Draw Jones becomes Video Jones only when there are enough drawings (or rig keys driven by drawings) that the motion never stops.
- No new angles invented yet: heads are Front + Profile only (2/5 angles). A drawn Jones that can only face two ways cannot carry a 30-episode show.

### Done looks like
Draw Jones is done for a shot when the keys + in-betweens for that shot exist as drawings, on twos, with no beat held longer than the story needs — and a viewer can point at any frame and say "that is Jones."

---

## 2. Video Jones — Draw Jones brought to life as video

### Definition
Video Jones is Draw Jones *moving in the actual video*. Same drawings, same proportions, same acting — but alive: breathing, drifting, raising, clicking, nodding, with the light shifting under him. He is not a slideshow (drawings held still) and he is not a puppet substitute (the rig Jones doing the moving while the drawn Jones flashes in and out). He is the drawn Jones, in motion, frame after frame.

### How Draw Jones becomes Video Jones
1. **Keys are drawings.** The 7 boards + 8 poses are the extremes — the poses the story needs.
2. **In-betweens are drawings.** The 10 in-betweens are the motion between the keys — breath in/out, raise-mid, raise-high, lower-mid, nod-mid, pupil-half. Where a rig cannot reach a pose, a Grease Pencil / hand in-between fills it — that is the Playbook's rule, not a fallback to be ashamed of.
3. **On twos, at 24fps.** A new drawn change every 2 frames (12 drawings/sec); on ones only for impacts. This is the Grok-Animation-Project timing standard the repo already cites (`SHOW-PRODUCTION-STATUS.md` §4 / line 77: 24fps, twos, ones for impacts, every cut >1s needs an exposure note).
4. **Hard cuts between beats, no dissolves between two Joneses.** This is the lesson of the rejected mixed cut (see §4): fading a drawn Jones in over a rig Jones shifts between the bulkier drawn physique and the slimmer puppet physique for ~6 frames per anchor — same guy, a little different physiques, but the dissolve makes the shift read as phasing, not animation. Video Jones changes pose by *drawing the next pose*, or by cutting to it — never by dissolving one Jones into another.
5. **Something is always moving on purpose.** The TV-SHOW-METHOD-STUDY's shared truth across Metalocalypse / ATHF / $UPEREGO: "the drawing count is never the aliveness… something is always moving on purpose — a rig posing, a puppet's arm chopped into a new timing, a mouth flapping on dense dialogue, a light changing colour — and the edit never lets a dead frame sit."

### What Video Jones currently is (honest)
- **V1 — slideshow, REJECTED.** `production/2d-parking-lot/video/purple-lot-v1.mp4`, 480f/20s, 17 drawings across 480 frames. Owner: "Microsoft Word slideshow," "not a real cartoon." Stays on main as superseded. Do NOT delete, do NOT present as the standard.
- **V2 — puppet cut, arm correct, hands wrong.** `~/workspace/_cape-jones-parking-lot-2d/v2/purple-lot-v2.mp4`, 480f/20s, 240 pose keys on twos, sha256 `e18a78b7…8483f`. The *arm* in V2 works perfectly (owner, 2026-11-23). The top-layer hands are upside down (see §4) and the remote has a white background box. V2 moves — it is not a slideshow — but it is Rig Jones doing the moving, and the drawn Jones only appears in the gag plates (f169–205).
- **Mixed cut — REJECTED for animation/editing, production amazing.** `v2/purple-lot-v2-mixed.mp4`, 480f/20s, sha256 `604e4903…7777`. Production level is the standard to keep on everything. Animation/editing is rejected: the arm detaches in the mixed cut (it did not in V2), the V1-anchor dissolves phase between drawn Jones and rig Jones, editing is amateur. Do NOT land it.
- **So: Video Jones does not exist yet as a finished thing.** V1 is Draw Jones held still. V2 / mixed are Rig Jones moving. Video Jones is the thing still to build: Draw Jones, moving, for the whole 20 seconds.

### Done looks like
A whole 480f / 20s video, 1280×720, 24fps, where every frame is recognisably Draw Jones, motion never stops, no dissolve-phasing, no floating hands, no white-box props — and the owner watches the *whole video* (not frames) and says it moves like the drawing does.

---

## 3. Rig Jones — the Blender cutout-puppet Jones

### Definition
Rig Jones is Jones as a cutout puppet in Blender: sliced part art, bound to bones, posed and tweened by the computer. He exists so the show can move fast — 240 keys on twos without redrawing every frame — but he only counts if he *looks like* Draw Jones / Video Jones when he moves. A rig that moves well but looks wrong is a puppet, not Jones.

### Current state: Rig Jones V2 (verified, honest)
- **Build:** native Blender 5.0.1 cutout puppet — NOT COA Tools 2 (no COA install on that VM). 12 bones (pelvis, torso, neck, head, arm R/L, hand R/L, leg R/L, capeTop, capeTip), 28 sliced parts from `cape-jones-rig/cape-jones-sliced.zip` (locked T-pose v8), 12 part planes + 14 hand planes + remote prop + drawn pupil overlays + ground shadow. Cycles CPU render.
- **Proof:** dance test 96f/4s (`dance/dance-test.mp4`) — full-body articulation, cape lag/overshoot/settle — and the V2 cut 480f/20s, 240 pose keys on twos. Own-eyes verified 2026-11-22.
- **Cape:** 2-bone spring chain (top/tip, split at 55%), damped-spring follow-through — not Wiggle 2, not cloth.
- **Plates:** clean plates rebuilt from board 01 by inpainting Jones out (HANDOFF's claim of 4/4 plates in `v2/backgrounds/` was false — that directory never existed before this lane).
- **Collision on main:** PR #430 landed a *different* V2 cut on main (`production/2d-parking-lot/video/purple-lot-v2.mp4`, Blender 5.2.4 + COA Tools 2 + Wiggle 2, 44 re-sliced parts with elbow/knee cuts, 11 eye swaps, 6 cape variants) — but its delivered video is visibly broken at 3/3 beats checked own-eyes: forearms + hands do not render, head oversized, cape a flat black slab. Stronger rig on paper, broken video on screen. Landing is held for the owner's call.

### Honest gaps in Rig Jones V2 (what keeps him at V2, not V6)
1. **No elbow/knee cuts.** Arms and legs are one piece each — whole-limb rotation at shoulder/hip only. No mid-limb bend.
2. **Hands are the known bug — and the only thing the owner asked to fix.** The top-layer / swap-hand overlay planes are upside down: fingers up, wrist down, floating beside the thighs, detached from the forearms — in every beat of the owner's 7 screenshots (close-up sodium, wide, raise, purple close-up). The rig's own fists are correct. The remote hand is upside down too: remote pointing up, fingers to wrist, arm-wrist and hand-wrist pointing opposite ways. Correct is **wrist-to-wrist** — arm wrist meets hand wrist, same direction, fingers at the far end of the hand, remote pointing **down** in the fingers. The remote also carries a pale white rectangular background box — never cropped to transparent alpha. A hand/remote fix lane is running separately (agent b2a75c71) — do not touch its files.

### Hand regression log (owner, 2026-11-23 07:06 EST) — log BOTH ways, labeled, so we never regress
- **V2 camera cuts are the standard to keep** — V2 had BETTER camera cuts than the phasing mixed cut. The phasing cut had to show more clips, understood, but make it all work better: Draw Jones clips must move like Video Jones; cuts must use Rig Jones cleaned up with Clean-Up Jones so he looks clean. Use this Rig Jones for now — just do NOT flip his hands wrong.
- **Hand attachment rule:** if you attach hands over the hands, EITHER swap the hands instead of doing the layers AND swap them with the correct orientation, OR lay them on top with the correct orientation — NEVER put them on with the wrong orientation, ever.
- **INCORRECT (never again):** top-layer hands fingers-up, wrist at bottom, floating beside thighs, detached; remote hand upside down, remote pointing UP, fingers toward wrist, arm-wrist and hand-wrist opposite; remote white background box not cropped.
- **CORRECT (always):** wrist-to-wrist, same direction; fingers at far end; remote in fingers pointing DOWN; hands attached to forearm cuff, thumbs medial; remote clean-cropped transparent alpha, no white box.
- **Process:** if the owner says "you did it the incorrect way", answer "this was the incorrect way, don't do it this way" and log it as incorrect. If he says "that's good" / does not say it was incorrect, that was the RIGHT way — record it as the way to keep doing it.
- **Pre-delivery check, every hand at every beat, logged before any cut is delivered:** wrist-to-wrist? fingers down / at far end? remote pointing down? hands attached to forearm cuff? thumbs medial? no white box on the remote? A cut with any "no" does not ship.
3. **No COA Tools 2 build, no deformer/peg.** AnimLab peg/deformer is step 2 of the work order — PR #429: placement + export proven, peg partial (no peg node/pivot seen on canvas). Grease Pencil stays the animation core until rig/deformer is fully proven.
4. **Cape is a spring, not a sim.** 2-bone chain, no Wiggle 2, no cloth collision.
5. **No eye/mouth libraries in the V2 rig.** Pupils are drawn overlays; no eye swaps, no mouth shapes, no lip sync (voice is owner-gated anyway).
6. **Cycles CPU only, no EEVEE.** Renders are slow (~5.5s/frame at 32 samples; the mixed-cut Cycles render died twice on this VM and the frames had to be produced via the PIL path from Blender's own transforms — honest, documented in MIXED-REPORT.md §3).
7. **Heads: Front + Profile only.** No invented angles, no 3/4 turn.
8. **Same guy, a little different physiques — animation flair, not a fatal flaw (owner nuance, 2026-11-23 06:59 EST).** The slim puppet Jones vs the bulky drawn Jones is a little bit of animation flair — just him and Muse each getting it a little wrong, that is what makes it human. They DO look like the same guy right now, just a little different physiques, which the owner understands. Do NOT over-correct the flair away. The goal is more accurate / more aligned versions as the Vs grow — by V10 of all those Joneses they will all be the same guy. Sheet Jones is the foundation that drives that convergence, version by version.

---

## 4. The V3 → V6 ladder for Rig Jones

**Clean-Up mapping (owner, 2026-11-23 06:54 EST): Rig Jones 1 = current official V2 rig. Rig Jones 2 = Clean-Up Jones 1. Rig Jones 3 = Clean-Up Jones 2, and so on — each clean-up level is the next Rig Jones version.**

**Rule for every version: prove it with a short whole video first, then the full cut. No version moves on until its proof video passes own-eyes. No dissolves between Draw Jones and Rig Jones at any version — hard cuts only. The V2 arm is the baseline that must not regress: it worked perfectly, and no version is allowed to break it.**

**Target quality, named by the owner:** Adventure Time / Regular Show / Amazing World of Gumball / Metalocalypse rigs. What those rigs do that Rig Jones V2 does not (from the repo's own studies — `docs/TV-SHOW-METHOD-STUDY.md`, `docs/CAPE-JONES-TV-SHOW-PLAYBOOK.md`):
- **Metalocalypse (Titmouse, 24fps broadcast):** few physical drawings, but the rig moves every frame and the animation is synced to the music — the puppet serves the music, guitar fingering shown in detail. *Rig Jones lacks:* music-synced motion, and a rig that can actually "play" a prop correctly (cf. the remote — a Metalocalypse rig would hold the instrument right).
- **Regular Show / Adventure Time (CN, Flash/Toon Boom puppet + drawn):** squash & stretch, exaggerated follow-through, expressive eye/mouth libraries, clean line boil control, characters that deform without breaking construction. *Rig Jones lacks:* squash & stretch, deformers, eye/mouth libraries, line-boil control.
- **Amazing World of Gumball (CN, mixed media puppet):** layered rigs, 9 `.fla` rig files found in the owner's study material (`~/workspace/agent-ops/fla-puppets-program-2026-10-30/gumball/`), characters built from swappable parts with real secondary motion. *Rig Jones lacks:* swappable part libraries at Gumball depth, secondary motion beyond a 2-bone cape spring.
- **ATHF (Photoshop + After Effects puppet):** radio play first, animatic as loose blueprint, "popsicle stick" cheats that read as style, arms chopped up in comp to make a tween that does not exist. *Rig Jones lacks:* the edit-first discipline and the comp-level arm fixes — the mixed cut tried comp fixes (dissolves) and chose the wrong one.

### V3 — Fix the hands, fix the remote, keep the arm (IN PROGRESS — separate lane)
*This is the hand/remote fix already running (agent b2a75c71). V3 is that fix, nothing more, nothing less.*
- [ ] Top-layer hands: fingers down, wrist-to-wrist, thumbs medial, attached to the forearm cuff — both sides, every beat. No floating upside-down hands in any frame.
- [ ] Remote hand: wrist-to-wrist, fingers at the far end, remote pointing DOWN in the fingers.
- [ ] Remote prop: clean re-crop, transparent alpha, no white/pale background box at any zoom.
- [ ] No dissolves. V1 drawings are reference for rig poses only, hard cuts.
- [ ] **Arm untouched.** V2 arm — bones, parenting, pivots, keys — identical to `rig/purple-lot-v2-rig.blend` / `v2/purple-lot-v2.mp4`. Any arm change is a regression: stop and revert.
- [ ] **Proof test:** short arm-raise test video (raise f121–168 range + close-up + wide) checked own-eyes against the owner's 7 screenshots — hands attached, remote down, no white box — *before* any full 480f render.
- [ ] Deliverable: new mixed cut, whole video, 480f/20s, distinct name in `v2/`. Not landed without owner approval.

### V4 — Real joints + deformers (Rig Jones becomes a real puppet)
- [ ] **Elbow/knee cuts.** Re-slice arms and legs into upper/lower segments. Source: PR #430's 44 re-sliced parts (they *have* elbow/knee cuts) merged onto the verified V2 pipeline — take their *parts*, not their broken cut. Verify the forearm + hand render at every beat (their cut's failure was forearms+hands not rendering — that must never recur).
- [ ] **COA Tools 2 build.** Blender 5.2 + COA Tools 2 (Aodaruma fork) as in the Playbook: layered art → auto-mesh → bone rigs + IK + sprite swapping. The native-Blender V2 rig is the reference; COA replaces the renderer, not the part set or the pivots.
- [ ] **Peg / deformer proven.** AnimLab peg/deformer (work order step 2, PR #429): a peg node/pivot actually visible and working on canvas, deformer bending a limb without breaking the line. Grease Pencil stays animation core until this is fully proven — do not claim it before then.
- [ ] **Proof test:** short video — arm bend at the elbow through the raise, leg bend at the knee, deformer bend holding the line — own-eyes, whole video.

### V5 — Acting, cape, and look (Rig Jones gets more aligned with Draw Jones — convergence, not a fix for a different guy)
- [ ] **Wiggle 2 cape** (live sim, per Playbook §1b) replacing the 2-bone spring — cape with real follow-through, overlap, and settle, that keeps its shape and does not go flat black slab.
- [ ] **Eye swaps + mouth library.** 11 eye swaps from sheet 05 (PR #430's set, verified against the sheet), pupil overlays replaced by real swaps; neutral + half-smile mouths from the Playbook's sprite library — so the face can act without a redraw.
- [ ] **EEVEE rendering.** libEGL resolved, EEVEE proven on the same frames as Cycles — faster renders, no more PIL-path workaround, same grade.
- [ ] **Proportions / line more aligned with Draw Jones.** Rig Jones re-proportioned and re-weighted so a side-by-side of rig frame vs drawn board reads as the *same* guy, more closely aligned — convergence toward V10, where all Joneses are the same guy. Do not over-correct the flair away; align gradually, version by version.
- [ ] **Proof test:** short video — hero beat f206–312 with cape sim, eye swap, and nod — own-eyes, whole video, side-by-side against board 05.

### V6 — Adventure Time / Regular Show / Gumball / Metalocalypse level (Rig Jones = Video Jones)
*V6 is not a feature list — it is the bar. Rig Jones is V6 when a viewer cannot tell whether a shot was drawn or rigged.*
- [ ] **Squash & stretch.** The rig deforms on impacts and settles (breath, landing, click) without breaking construction — the Adventure Time / Regular Show principle. Deformers, not just rotation.
- [ ] **Secondary motion everywhere.** Cape, head, hands, and torso all carry follow-through and overlap — the Gumball layered-rig standard. Nothing stops dead when the main motion stops.
- [ ] **Line boil control.** The line has life but does not jitter amateurishly — clean line, controlled boil, on purpose.
- [ ] **Eye / mouth acting.** Full eye-dart matrix (sheet 05) and mouth shapes driven by performance — the fourth-wall pupil button lands because the eyes can act, not because an overlay was pasted on.
- [ ] **Music-synced motion (Metalocalypse rule).** When a track plays, the rig moves *to* it — prop handling, timing, and accents synced, not just moving while music happens. (Track itself is owner-gated; the rig must be ready for it.)
- [ ] **Edit-first discipline (ATHF rule).** Radio play / animatic blocked in edit before posing; no comp trick (dissolve, smear, warp) sold as animation.
- [ ] **Proof test:** a full 480f/20s PURPLE LOT cut, whole video, own-eyes at every beat — and the owner cannot pick which shots were drawn and which were rigged. That is the V6 test. If he can, it is not V6.
- [ ] **Deliverable:** V6 rig + V6 cut, landed in the repo by the owner's call only (branch → PR → merge, never direct to main).

---

## 5. OTHER JONESES NEEDED — to the highest industry-standard professional level, $UPEREGO level

**Owner question, 2026-11-23 06:49 EST:** "Save all of that, and so we have Draw Jones, Video Jones and Rig Jones on the highest industry standard professional level — looking at all the Cartoon Network files we have, their official files — what other types of Joneses do we need to get to the highest levels of cartoon to get to Super Ego levels?"

**Grounding (read for this section, not guessed):**
- CN gigaleak Space Ghost production files — README.md line 6: "Source materials: Cartoon Network gigaleak Space Ghost production files (study/production use)." `animation-study/` — model sheets, rigs, style analysis for the Cape Jones look.
- `docs/TV-SHOW-METHOD-STUDY.md` — Metalocalypse / ATHF methods, the shared truth ("something is always moving on purpose"), the comparison table.
- `docs/CAPE-JONES-TV-SHOW-PLAYBOOK.md` — the pipeline mapped to those methods: design once (model sheets), COA rig, Wiggle 2 cape, Tahoma2D composite, Rhubarb lip sync, `finish.py` QC → grade → audio mix → encode, "feels like TV" checklist.
- `docs/SUPERIOR-TURBINATE-STUDY.md` / `SUPERIOR-TURBINATE-DEEP-STUDY.md` / `SUPERIOR-TURBINATE-FEELING-STUDY.md` (PRs #416–418) — the $UPEREGO formula, packaging, and feeling.
- `docs/SHOW-PRODUCTION-STATUS.md` §6 + line 77 — owner has CN / Gumball, Nickelodeon, Disney and related study repos (`mhvnsnt/cn-gigaleak-gumball` and other `cn-gigaleak-*`, `mhvnsnt/cn-gigaleak-bonus-non-cn`, `mhvnsnt/disney-tva-bbb-pulls`, `mhvnsnt/animation-research-library`), plus `mhvnsnt/Grok-Animation-Project` (timing/cuts/DPS rules). **Hard rule from that file: do NOT ingest leaked/gigaleak materials into Cape Jones production. Study timing, exposure, cutting, layer structure; apply them to original Cape Jones art. Do not copy CN/Gumball/Nick/Disney characters, logos, names, dialogue, audio, or artwork into show files.**
- Gumball S2 `.fla` rigs found on disk: 9 files, `~/workspace/agent-ops/fla-puppets-program-2026-10-30/gumball/`.

**$UPEREGO note, from the owner and the studies:** take $UPEREGO's **formula, packaging, and feeling** — not their long holds. Their holds run 10–30 seconds (ep6: 25–30s, ep7: 10–25s, per the TV-SHOW-METHOD-STUDY). The owner **rejected** long holds — that is what V1 was rejected for. A $UPEREGO-level Jones keeps the sincere monologue, the feeling of being understood, the dialogue density, and the single-as-a-song — and keeps Jones moving.

Each Jones below is a named stage a professional CN / $UPEREGO-level pipeline needs. For each: what it is, where it lives in the repo / CN files, what Draw / Video / Rig Jones already cover, what is still missing, and what "done" looks like.

### 5.1 Sheet Jones — the design bible (WE HAVE IT, as pieces of sheets) [RENAMED 2026-11-23: was 'Model Jones', now Sheet Jones]
- **Definition:** Jones on the model sheet — turnarounds, construction, proportions, expressions — the single source of truth every other Jones is checked against.
- **In the repo / CN files:** Playbook "Design once": sheets 01 (T-pose turnaround, bind pose), 02 (orthographic turnaround), 03 (colour/lighting/VFX key), 05 (expression/eye-dart matrix), 08 (body parts/limbs/capes). Locked palette suit #FFFFFF / cowl #3E1473 / skin #E5B28C / cape #000000. CN Space Ghost production files are the reference for how a professional model sheet is built — study the *structure* (turnaround, construction lines, expression matrix), not the art.
- **Covered already:** WE HAVE Sheet Jones, as pieces of sheets — sheets 01 (T-pose turnaround, bind pose), 02 (orthographic turnaround), 03 (colour/lighting/VFX key), 05 (expression/eye-dart matrix), 08 (body parts/limbs/capes). The T-pose is locked at v8. What exists is real, it is just pieces, not yet one complete bible.
- **Missing:** heads Front + Profile only (2/5 angles) — no 3/4, no back, no up/down; no expression matrix drawn for Jones beyond sheet 05's spec; no construction guide a new artist could draw from.
- **Done looks like:** a complete model sheet set — turnaround (front/side/back/3/4), construction, expression matrix, colour key — that a stranger could use to draw Jones on-model. Proof: the sheets, read own-eyes.

### 5.2 Board Jones / Storyboard Jones — the story as a sequence
- **Definition:** Jones in the boards as a *sequence* — Draw Jones as boards, not 7 single drawings, but the story told shot by shot, with staging, camera, and cutting. **That is the slideshow thing from earlier**: boards held still and claimed as a scene — the owner rejected it: "this isn't moving, this isn't acceptable." Board Jones is boards. Boards are not the scene. Boards become a scene only when they move (see Action Jones / Keyframe Jones).
- **In the repo / CN files:** 7 boards `cj-pl-01`…`07` + BOARD-LIST.md. Playbook: "Block the episode in edit first… For PURPLE LOT the 7 boards are the blueprint." ATHF rule in the method study: episodes are blocked out in edit; the animatic is a loose blueprint.
- **Covered already:** the 7 boards exist and carry the beat structure V1/V2/mixed all reused.
- **Missing:** boards as a timed sequence (see 5.3); boards for CJ-01…CJ-30 (the episode goal in HANDOFF) do not exist yet — only the PURPLE LOT short is boarded.
- **Done looks like:** a boarded sequence where the story reads without any animation — staging, camera, and cuts decided before a single pose is rigged.

### 5.3 Action Jones — boards timed to sound (Animatic / Timing Jones FOLDED IN — no longer standalone)
- **Definition:** Jones in ACTION — boards cut to time, with dialogue / sound / music timing, exposure sheets, twos/ones marked. The edit before the animation. Animatic Jones / Timing Jones was too specific / a little extra as its own Jones, so the owner folded it into Action Jones (2026-11-23 06:54 EST). Do not keep Animatic as a standalone Jones.
- **In the repo / CN files:** Grok-Animation-Project timing standard (cited in SHOW-PRODUCTION-STATUS.md line 77): 24fps, twos, ones for impacts, every cut >1s needs an exposure note. Playbook: "radio play / voice line cut first, then a bare-bones animatic that implies the action." ATHF: radio play cut before any animation; dialogue leads.
- **Covered already:** the timing standard is *written down*; the V2 cut's beat map (f1–72, 73–120, 121–168, 169–205, 206–312, 313–379, 380–480) is a timing structure.
- **Missing:** no Action Jones exists yet — no boards timed to a soundtrack, no exposure sheets, no radio play (voice is owner-gated, 0/30 lines recorded for CJ-01…30 per SHOW-PRODUCTION-STATUS.md §8). The V2/mixed beat map was built from the boards, not from a timed animatic. Honest progress: 0%.
- **Done looks like:** a timed action video (boards + timing + temp silence where voice will go) approved by the owner *before* posing starts. Proof: the action file + its timing sheet.

### 5.4 Keyframe Jones — keys + in-betweens, one cleaner Jones (Key Jones + In-Between Jones FOLDED IN)
- **Definition:** Jones at the keys AND the in-betweens — the extremes (key poses) and the motion between them (in-between frames), as one stage. Key Jones and In-Between Jones were folded together into this one cleaner Jones (owner, 2026-11-23 06:54 EST). It is about colour keys / key frames and in-betweening frames — the strongest pose for each beat, and the drawn/rigged motion that gets between them, on twos, with real arcs, timing, and follow-through.
- **In the repo / CN files:** the 8 poses (`pose-01-idle` … `pose-06-nod` + cape studies) are Key Jones's raw material. The Playbook's rig proof is "9 rig poses rendered (transparent) + composited over board backdrops, own-eyes verified."
- **Covered already:** 8 poses exist; V2's 240 keys are computer tweens *between* poses.
- **Missing:** keys are not yet all *drawn* extremes — V2's keys are rig poses, and the rig's poses are only as strong as the puppet allows (no elbow bend, no squash). In-betweens as a *stage* are also missing: 10 in-betweens exist as drawings, but not drawn in-betweens for the full 20s with arcs and timing charts. The mixed cut's anchor fades were a shortcut around this stage, and the owner rejected the shortcut. Work order step 3 (boards and in-betweens) is not started as a standalone step.
- **Done looks like:** every beat has a named key that reads on its own as a drawing, and the motion between every pair of keys is drawn or rigged with intent — no beat is a hold, no beat is a dissolve, and the keys and in-betweens are listed and checked like each other.
- **Done looks like:** every beat has a named key that reads on its own as a drawing — idle, raise, click, hero, lower, nod — and the in-betweens exist to get between them, not to invent them.

### 5.5 Clean-Up Jones — FOLDED INTO Rig Jones (not standalone)
- **Definition:** Clean-Up Jones IS the cleaner Rig Jones. It is not a standalone Jones — the owner said it is wild / he does not get it as its own thing, so it folds into Rig Jones (2026-11-23 06:54 EST). Every time we upgrade the rig, that is a Clean-Up Jones level. **Mapping: Rig Jones 1 = the current official rig we are using right now (the V2 cut rig). Cleaning up that official rig makes Rig Jones 2, which is Clean-Up Jones 1.** Then Rig Jones 3 = Clean-Up Jones 2, and so on — each clean-up is the next Rig Jones version. Clean-Up Jones = fix the amateur stuff, make it industry-standard, no regressions, prove with a short test first. That is also what "Clean Up Jones this shit" means (see §0a).
- **In the repo / CN files:** the sliced parts in `cape-jones-sliced.zip` are cleaned-up line art (that is why the rig can use them). The Playbook's palette QC (`palette-enforce.py`) and the "feels like TV" checklist cover line/colour QC at finish. No clean-up stage document exists in the repo — this Jones is *implied* by the parts, not named as a stage.
- **Covered already:** the parts are clean enough to rig; the line reads on screen.
- **Missing:** no line-boil control (V6 item), no clean-up pass defined for new drawings — a new in-between drawn rough has no named step that turns it into final line.
- **Done looks like:** every drawing that reaches the video has been through a clean-up pass with a defined line weight and boil rule — and the rig's parts match that line, so drawn and rigged frames sit in the same shot without a visible line change.

### 5.5 Color Jones / Paint Jones — colour, light, and the sodium → purple shift
- **Definition:** Jones in colour — the colour model, the palette enforced on every frame, and the lighting shift (sodium orange → broken-streetlight purple) as a *designed* change, not a filter slapped on at the end. Color Jones is a cross-Jones layer: it is pretty much Rig Jones in different colors, but it also translates to Video Jones and Draw Jones — same Jones, same palette, different colors per Jones / per beat.
- **In the repo / CN files:** locked palette (suit #FFFFFF, cowl #3E1473, skin #E5B28C, cape #000000); sheet 03 colour/lighting/VFX key; `production/pipeline/grades.py` (BULB_ORANGE brightness −0.08 for sodium, PURPLE_STREETLIGHT for purple) applied verbatim in ffmpeg; `palette-enforce.py` (extract on sheet 03 + enforce on final frames — functional run owed, per Playbook).
- **Covered already:** the grades are verbatim and verified; the light shift is the short's central visual idea and it works — production is the part the owner called amazing.
- **Missing:** palette-enforce has never had a functional run on final frames; the purple plate is the sodium plate re-graded (the Playbook's rule — "the light moves in post, the drawing stays clean" — is followed, but it is not yet a *designed* colour script for the whole short).
- **Done looks like:** a colour script for the short (sodium → purple, frame by frame, with the shift timed to the story) + a palette-enforce QC pass on the final video that passes.

### 5.5 Layout Jones / Background Jones — Jones in real scenery
- **Definition:** Jones placed in the parking lot — layout, perspective, scale, and the clean plates he stands on, so he belongs in the space instead of floating over it. Background Jones, Scenery Jones, and Setting Jones are all Layout Jones — him in the background, backgrounds and settings, scenery and setting, all one Jones (owner, 2026-11-23 06:54 EST). We already have good backgrounds and settings for Layout Jones.
- **In the repo / CN files:** 4/4 clean lot plates were *claimed* in HANDOFF — that claim was false (the directory never existed); the V2 lane rebuilt plates from board 01 by inpainting Jones out, with known limits (faint inpaint seams, half-clipped blue car at the patch edge). The 3D track has a proven lot scene (`parking_lot_test.blend`, 480f, CPU proof frames f1 + f230 PASS).
- **Covered already:** plates exist and work in the V2 cut; the lot is a real place with a stop sign, buildings, and a car.
- **Missing:** clean plates as a repo asset (they live only in the workdir, not landed); no layout stage that places Jones at the right scale/perspective per shot — the V2 camera is ortho (wide 71 / medium 34 / medium-close 26), which is a staging choice, not a layout.
- **Done looks like:** landed clean plates in the repo with a MANIFEST, Jones placed at verified scale in each shot, and no inpaint seam visible on screen.

### 5.5 Voice Jones — the owner's voice only
- **Definition:** Jones with a voice — the owner's recorded performance, mouth flaps timed to it, and the line landing because the performance lands.
- **In the repo / CN files:** HANDOFF Blocked: voice + original track are owner-gated. Cape's line "ah, that's better" is a GAP for the owner's recording. **No synthesized voice ever for Cape** (his recorded voice only). Playbook: Rhubarb Lip Sync 1.14.0 (PROVEN — runs on the owner's recorded voice only), Rhubarb Lipsync NG 1.8.2, `production/pipeline/dialogue_pipeline.py` + `lipsync_align.py` — dialogue → timing → mouth shapes, in repo, to be wired on the first voiced short. SHOW-PRODUCTION-STATUS.md §8: Rhubarb 1.14.0 is installed on the Producerbot box but there is no recorded dialogue to sync; 0/30 lines recorded for CJ-01…30.
- **Covered already:** the lip-sync tooling is proven and waiting; the mouth-flap rule is written (mouth moves when he talks; $UPEREGO's lip sync is approximate and it works).
- **Missing:** the recording itself — the owner will record his voice and get it to us; Voice Jones IS him. Owner-gated, do not chase it, do not synthesise it. **No synthesized voice ever.** No mouth library in the rig yet (V5 item).
- **Done looks like:** the owner's recording, Rhubarb timing, mouth shapes moving on the dialogue, and the punchline rule held: line + beat of silence + drawn held reaction, no sting, no music bed under the dialogue, then hard cut.

### 5.5 Music Jones / Sound Jones — the track and the sound design
- **Definition:** Jones with sound — one original track per short, sound design, and the edit paced by sound, not just by pictures.
- **In the repo / CN files:** TV-SHOW-METHOD-STUDY: Metalocalypse — story first, music second, music must stand alone (the Dethalbum rule); animation synced to the music, guitar fingering shown in detail. ATHF — sound is part of the animation (sound design + editor pacing + composite). $UPEREGO — one original song per episode opens it; songs exist as TikTok sounds + Patreon OST posts. Playbook: "Music is a single, not a bed. One original per short, opens the short, drops as a single the same day. Real is the Carmen slot. No music bed under the line, no temp track." Owner is the Carmen slot.
- **Covered already:** the rule is written and the bar is named.
- **Missing:** no original track exists yet for PURPLE LOT — owner-gated, like the voice. The V2/mixed cuts are silent by necessity, not by choice.
- **Done looks like:** one original track, opening the short, standing alone as a single — and the rig moving *to* it (V6 music-sync item), not just moving while it plays.

### 5.5 FX Jones — cape, remote glow, lighting effects
- **Definition:** Jones with effects — FX Jones and Effects Jones are the same thing, one Jones. The cape's motion, the remote's glow, the lighting shift, and any energy/blast work, composited so they read as part of the scene. We have good effects for FX Jones, good lighting and keys too.
- **In the repo / CN files:** `production/pipeline/` scripts: `comp_glow.py`, `energy_blast.py`, `led_controller.py`, `led_scene_assembler.py`, `grades.py`, `pupil_gag.py` (inserts pupil-reaction frames — the exact tool for the fourth-wall button beat). Sheet 03 is the colour/lighting/VFX key. The cape is the show's most competent character (HANDOFF) — its motion *is* an effect.
- **Covered already:** the glow/grade tooling exists in the repo; the sodium → purple shift is an FX beat and it works.
- **Missing:** FX as a *stage* — no FX pass is scheduled or checked per shot; the cape's motion is still a 2-bone spring (V5 Wiggle 2 item), and the remote glow is a prop, not a composited effect.
- **Done looks like:** an FX pass per shot — cape, glow, light shift, pupils — checked own-eyes, with the effects reading as light in the scene, not as a filter.

### 5.5 Final Jones / Master Jones / Broadcast Jones — the finished video as delivered
- **Definition:** Jones finished — **Final Jones is the perfect cell of Cape Jones, the aim.** The graded, composited, encoded, QC'd video as the audience sees it. The "feels like TV" checklist, passed.
- **In the repo / CN files:** Playbook §11 "Finish": `finish.py` — QC → grade → audio mix (owner's voice/track only, when they exist) → encode; palette QC; proof is ffprobe (480f, 20.000s, 1280×720, 24fps) + hash + size. SHOW-PRODUCTION-STATUS.md §7: before claiming progress, name the exact media file (path, resolution, fps, duration, sha256, what it is), look at the pixels (OWN-EYES law), show the owner the video/shots. TV-SHOW-METHOD-STUDY: 24fps broadcast standard; Metalocalypse budget $109,099/ep is the *scale* reference, not a target.
- **Covered already:** the finish pipeline and the QC rules exist; V2 and the mixed cut both passed ffprobe + own-eyes checks as *files*.
- **Missing:** no cut has passed the *whole* finish checklist and been landed — V1 is superseded, V2 is unlanded, the mixed cut is rejected, main's PR #430 cut is broken. Final Jones does not exist yet for PURPLE LOT.
- **Done looks like:** a landed cut on main, 480f/20s/1280×720/24fps, ffprobe + sha256 recorded, palette QC passed, own-eyes at every beat, and the owner watches the whole video and calls it TV.

### 5.5 3D Jones — the rigged-model Jones (separate track)
- **Definition:** Jones as a 3D rigged model in the same parking-lot scene — the 3D test shorts track, built on the Western Heart pipeline. **Model Jones = 3D Jones, 3D Jones = Model Jones.** "Model" = the 3D model in Blender and all that (rename, owner 2026-11-23 06:57 EST).
- **In the repo / CN files:** `parking_lot_test.blend`, 480f @24fps, 1280×720, EEVEE→Cycles; CPU proof frames f1 + f230 own-eyes PASS; staged on Release `cj-parking-lot-proof-20261122`. JANCTION preview proved the scene (frames 1 + 230 free, 7.9 GPU-s, 0 JPY); owner approved the preview as good for the 3D, dark night look kept as-is, do not brighten. Full 480f final estimate 293 JPY, balance 0 JPY — **PAUSED, owner must say go + fund it** (save a card for +400 JPY bonus, no charge, or top up ~300 JPY). Colab sign-in as marquiswhitacre is refused (no Tap Yes, passkey fails in the cloud browser) — do not retry a password.
- **Covered already:** scene proven, preview approved.
- **Missing:** the full 480f 3D render — paused, not a quality gap, a funding/permission gap. AND the 3D rig itself: 3D Jones needs fingers and hands that move and are rigged, plus mouth, blinking, talking, and moving better. He gets upgraded from ALL our teardowns / decrypted / extracted game files — animations from all the games. 3D Jones can do every animation.
- **Done looks like:** the full 3D video rendered, own-eyes verified, landed — on the owner's "go" only. 3D Jones is a *separate* Jones from Rig Jones (2D puppet); do not confuse them in the repo.

### 5.14 What is NOT a Jones (checked against the files — do not invent these)
- **No "AI Jones" / generated Jones.** The repo's pipeline is drawn + rigged, not generated. Wan 2.1 I2V (ComfyUI) is listed in the Playbook as "only where the owner directs. No GPU run of the workflow yet." Do not add a generated-Jones stage unless the owner directs it.
- **No "Harmony Jones" yet.** Harmony 27 Premium runs on Linux (owner correction, SHOW-PRODUCTION-STATUS.md §5) but the Linux package is not on the box, not installed, not activated. `harmony_stage.py` falls back to Cape Jones Toon and MUST label that output "NOT Harmony." Do not claim a Harmony Jones exists until Harmony has actually rendered a shot.
- **No "Gumball Jones" / "CN Jones" as a character.** The CN / Gumball / Nick / Disney files are *study* material for craft (timing, exposure, cutting, layer structure). The hard rule is: do not ingest them into production, do not copy their characters, logos, names, dialogue, audio, or artwork into show files. What we take from them is method, not material.

---

## 6. The ladder, in order — what to do next

1. **V3 (now, separate lane):** hands + remote, arm untouched, no dissolves. Proof: short arm-raise test video.
2. **Video Jones, first pass:** Draw Jones moving for the whole 20s — keys + in-betweens on twos, hard cuts, no dissolve-phasing. This is the mixed cut done *right*, on the V3 rig.
3. **V4:** elbow/knee + COA + peg/deformer proven.
4. **V5:** Wiggle 2 cape + eye/mouth libraries + EEVEE + proportions matched to Draw Jones.
5. **V6:** squash & stretch, secondary motion, line-boil control, eye/mouth acting, music-sync, edit-first — Rig Jones indistinguishable from Video Jones.
6. **Beyond V6, to V10:** alignment keeps converging version by version — by V10 of all those Joneses they will all be the same guy. Do not over-correct the flair away; converge gradually.
6. **The Other Joneses, in pipeline order (consolidated 2026-11-23):** Model → Board → Action (Animatic/Timing folded in) → Keyframe (Key + In-Between folded in) → Colour → Layout → FX → Voice → Music → Final/Broadcast. Clean-Up is not a separate step — it is the Rig Jones upgrade ladder (Rig Jones 2 = Clean-Up Jones 1, etc.). Model Jones / 3D Jones runs on its own track, on the owner's "go."
7. **Landing:** every version lands by the owner's call only — branch → PR → merge, never direct to main. This doc is a draft until he approves it for the repo.

---

## 7. HOW FAR TO FINAL JONES — honest % (owner, 2026-11-23 06:54 EST)

The owner guessed **50–60–75% to Final Jones** based on how it looks. **The honest figure is ~30–35% to 100% Final Jones.** The eye overestimates it because the production look is high — the grade, the plates, the lighting shift all look TV-level in a still. What the still does not show is everything that is still 0%: no voice, no music, no action/animatic, no finished cut. A still can look 75% done while the video is 30% done, because a video has to *move, talk, and finish*.

| Jones | % to 100% | Why |
|---|---|---|
| Draw Jones | ~70% | Drawings are really good, 7 boards / 8 poses / 10 in-betweens / sheets 01/02/03/05/08 exist. Missing: more drawings, 3/4 + back + up/down heads, expression matrix, CJ-01…30 boards. |
| Video Jones | ~25% | V1 rejected slideshow, V2 is Rig Jones moving, mixed cut rejected. No finished Video Jones exists yet. |
| Rig Jones | ~30–40% | V2 proven, arm correct, dance + cut work. Hands upside down, remote white box, no elbow/knee cuts, no COA, no deformer, cape is a spring, no eye/mouth libraries, no EEVEE. |
| Sheet Jones | ~60% | We HAVE it as pieces of sheets (01/02/03/05/08). Missing: complete bible, 3/4 + back heads, expression matrix. Sheet Jones is the foundation — without a good Sheet Jones, Draw/Rig/Model Jones all end up different and fucked up. |
| Board Jones | ~50% | 7 boards for PURPLE LOT exist. Missing: CJ-01…30 boards, boards as a timed sequence. |
| Action Jones | 0% | No animatic / timed boards / exposure sheets / radio play. Voice 0/30 lines. |
| Keyframe Jones | ~30% | 8 poses + 10 in-betweens exist. Missing: drawn extremes for every beat, drawn in-betweens for the full 20s. |
| Clean-Up Jones | ~30% | Rig Jones 1 (V2) exists; Clean-Up Jones 1 = Rig Jones 2 has not started. |
| Color Jones | ~60% | Palette locked, grades verbatim, light shift works. Missing: palette-enforce functional run, colour script for the whole short. |
| Layout Jones | ~60% | Good backgrounds/settings/plates exist in the workdir. Missing: plates landed in the repo, layout stage per shot. |
| Voice Jones | 0% | No recording yet — owner will record it. No synthesized voice ever. Rhubarb tooling proven and waiting. |
| Music Jones | 0% | No original track yet — owner-gated. |
| FX Jones | ~50% | Good effects, glow/grade tooling, lighting shift works. Missing: FX pass per shot, Wiggle 2 cape, remote glow as a composited effect. |
| Model Jones / 3D Jones | ~35% | Scene proven, JANCTION preview approved. Full 480f render paused (293 JPY, 0 balance, owner must say go). No finger/hand/mouth/blink/talk rig yet. |
| Final Jones | 0% | No cut has passed the full finish checklist and been landed. V1 superseded, V2 unlanded, mixed cut rejected, main's PR #430 cut broken. |
| **Overall to Final Jones** | **~30–35%** | Production look is high; voice, music, action, and finish are 0%; rig/video/3D are roughly a third done; clean-up / V4–V6 not started. |

## 8. Sources (so anyone can check this doc)

- Workdir: `~/workspace/_cape-jones-parking-lot-2d/CHECKPOINT.md`, `RIG-REPORT.md`, `MIXED-REPORT.md` (2026-11-22).
- Repo (read-only, `mhvnsnt/cape-jones`, main): `HANDOFF.md`; `README.md` (line 6: CN gigaleak Space Ghost production files, study/production use); `production/2d-parking-lot/boards/` (7), `poses/` (8), `inbetweens/` (10); `production/2d-parking-lot/v2/` (PR #430 rig report, 44 parts); `cape-jones-rig/` (sliced parts, T-pose v8, 12-principles checklist).
- `docs/TV-SHOW-METHOD-STUDY.md`, `docs/CAPE-JONES-TV-SHOW-PLAYBOOK.md`, `docs/SHOW-PRODUCTION-STATUS.md` (§4 timing, §5 Harmony, §6 study repos + hard rule, §7 claim rules, §8 open items, §10 method change), `docs/SUPERIOR-TURBINATE-STUDY.md`, `docs/SUPERIOR-TURBINATE-DEEP-STUDY.md`, `docs/SUPERIOR-TURBINATE-FEELING-STUDY.md`.
- Owner directions: 2026-11-22 (V1 rejected; V2 arm correct; mixed cut rejected for animation/editing, production amazing; hands top-layer only; remote white background; wrist-to-wrist, remote down), 2026-11-23 06:43–06:49 EST (Jones versions terminology; Other Joneses question).
- Study repos named in SHOW-PRODUCTION-STATUS.md §6 (not read in full for this doc — their *rules* are cited, not their binaries): `mhvnsnt/Grok-Animation-Project`, `mhvnsnt/animation-research-library`, `mhvnsnt/disney-tva-bbb-pulls`, `mhvnsnt/cn-gigaleak-gumball` and other `cn-gigaleak-*`, `mhvnsnt/cn-gigaleak-bonus-non-cn`.
