# CAPE JONES TV-SHOW PLAYBOOK

**Owner order:** 2026-11-22 — keep studying Metalocalypse, $UPEREGO, and Aqua Teen Hunger Force, keep building, put all the notes in the repo, so the work feels like an actual TV show, never a slideshow, and uses everything already built in the repo.
**Method doc:** `docs/TV-SHOW-METHOD-STUDY.md` — the three shows' real production methods, side by side, with sources.
**Three-target bar:** at least as good as Metalocalypse + $UPEREGO + Aqua Teen Hunger Force — "real puppets, real rigs on backgrounds and real scenery doing real shit."

**The method in one sentence:** draw once, rig like a puppet, pose the rig on twos, dialogue first, one sincere beat + one undercut, hard cut to black — with the lighting shift as the feeling.

---

## 1. THE PIPELINE — what we actually have, with real paths

Every tool below is real, with its real location. Status is as of 2026-11-22. Nothing here is claimed from a doc alone — each entry names where the proof lives. (Full verification: `~/workspace/_cape-jones-parking-lot-2d/HIGHEST-V-INVENTORY.md` — 24 VERIFIED EXISTS · 6 MISSING · 3 N/A — and the lane checkpoints named in §6.)

### 1a. The rig (the show lives here)

| Tool | What it does | Real path / proof | Status |
|---|---|---|---|
| **COA Tools 2 v2.3.0** (Aodaruma fork) | Cutout puppet rigger inside Blender: layered art → auto-mesh → bone rigs + IK + sprite swapping for mouth/eye libraries. The free Spine-equivalent. | Installed in Blender 5.2 extensions (`user_default/coa_tools2`). P9 PASS (real sprite import + automesh + bind + pose + render). Catalog: `~/workspace/_anime-rig-pullin-20261114/PULLIN-CATALOG.md` §1. **Rig-build lane running now:** `~/workspace/_cape-jones-parking-lot-2d/rig/` (`PROGRESS.md`, `slice_parts.py`, `probe_coa.py`). Bind pose = sheet-01 T-pose. Parts sliced from sheets 01/05/08 + poses. | **PRIMARY RIG BUILDER — IN USE** |
| **AnimLab v0.2.27** (KevesDev, $0 freeware, NOT open-source) | Vector drawing, pegs, rigging (Bone / Game Bone / Curve / Envelope deformers), node-graph compositing, multi-camera timeline, audio mixer, MP4 + PNG-sequence export. The Toon Boom Harmony equivalent. | `.deb` on Release `production-stack-free-20261120` (mhvnsnt/dream-girl), sha256 `46de41ac484a9dd8f19e7251bb453fb577ad07620bcf098440f8502c211ccfbf`. Wired into cape-jones in **PR #426** (merged 2026-11-22): `tools/animlab/README.md`, `tools/animlab/fetch-animlab.sh`, `tools/animlab/PIPELINE-STAGE.md`, `docs/ANIMLAB-PIPELINE.md`. Binary: `/usr/bin/animlab-desktop`. | **EXPERIMENT CANDIDATE — smoke test PENDING** (Kaggle kernel `marsfmmg/animlab-smoke-test`; local install blocked by a disk-write wall). AnimLab earns a bigger role only by proving itself on real shots through the same own-eyes gate as every other stage. It is NOT the core until then. |
| **Grease Pencil v3** (Blender, built-in) | Hand-drawn animation. **THE ANIMATION CORE** — per the stack rule, nothing replaces it unless verified better on our own shots. | Blender 5.2.4. Role in this pipeline: hand in-betweens **only where the rig cannot reach** — never the drawing engine for 240 frames. | **CORE — IN USE** |
| **Gumball S2 .fla puppet rigs** | Pose library / physical-comedy timing reference. Real Flash puppet rigs to study. | `workspace/toon-mash-studio/animation-study/gumball-s2-rigs/` (local) + `mhvnsnt/cn-gigaleak-gumball` (study only). | **REFERENCE — HAVE** |

### 1b. Secondary motion — the cape

| Tool | What it does | Real path / proof | Status |
|---|---|---|---|
| **Wiggle 2 RTX Edition 2.4.0** | Real-time spring physics on pose bones — lag, overshoot, settle on the cape. | Proof: `~/workspace/_cape-jones-parking-lot-2d/wiggle-cape-proof/` (`PROOF-REPORT.md`, `wiggle-cape-proof.blend`, 48f @ 24fps). Measured: lag f06 (shoulder 19.8° vs tip −13.8°), overshoot tip −46.6° at f15, settle residual 1.8° at f48. **LANE RULE: render the live sim per-frame; do NOT rely on the bake** (bake captures head/tail bones only). Recipe: enable as `bl_ext.user_default.wiggle_2`; `scene.wiggle_enable = True` is CRITICAL (defaults False); Cape1 `use_connect=False`. | **PROVEN (live sim) / PARTIAL (bake) — IN USE** |
| Honest limit | Bend concentrates in the cape's bottom quarter; a full-length distributed curve is NOT proven. Proof is a flat-color panel, not the drawn CJ cape — the animation lane still wires it onto the real COA/Grease Pencil cape. | — | **OPEN** |

### 1c. Drawing, compositing, rendering

| Tool | What it does | Real path / proof | Status |
|---|---|---|---|
| **Tahoma2D 1.6.3** | Draw + composite + headless render host (`tcomposer`). | `~/workspace/tools/tahoma2d/`. **PROVEN end-to-end twice** (Nov 12 + Nov 22 re-pull: Ozzie 12-drawing re-render, 1.39s, own-eyes PASS; PURPLE LOT V1 480/480 frames rendered in 240.32s). **RULE: ALWAYS pass ABSOLUTE paths to tcomposer** — relative paths hang forever. Setup fixes (libOpenGL syslibs, xvfb-run required, SystemVar.ini TAHOMA2DROOT, project files from source): `docs/2D-PARKING-LOT-PRODUCTION.md` §3. Bundled Rhubarb 1.13.0 verified working. | **PROVEN RENDERER/COMPOSITOR — IN USE** |
| **ffmpeg 8.1.2** | The engine under every grade, preset, and encode. | `/usr/bin/ffmpeg` on disk. All grade chains and the LED controller run against it with zero errors. | **LIVE — IN USE** |
| **Synfig Studio 1.5.5** | Bone-rigged cut-out + auto vector tweening, actively maintained, GPL. | Release `harmony-equivalents-20261120` (mhvnsnt/dream-girl), AppImage 115,539,968 B, sha256 matches upstream exactly. Companion-fetch agent running (Kaggle). | **PULLED — AWAITING WIRE-UP** |
| **Glaxnimate 0.6.0** | Motion graphics / Lottie / SVG animation. | Same release as Synfig. Companion-fetch agent running. | **PULLED — AWAITING WIRE-UP** |
| **Storyboarder 3.0.0** | Storyboarding (Wonder Unit, free OSS). | Direct GitHub URL verified in search. Companion-fetch agent running. | **RESEARCHED — PULL PENDING** |
| **Wick Editor** | Browser + Flathub vector animation (GPL-3.0; original team discontinued, community fork Candlestick). | Browser + Flathub. | **RESEARCHED — NOT PULLED** |
| **Pencil2D 0.7.2 / Rigby2D 0.5.1 / AniCraft 0.2.1** | Traditional 2D (Pencil2D), skeletal/mesh/IK editor (Rigby2D), clean-room Adobe Animate reimplementation (AniCraft). | Release `production-stack-free-20261120` (mhvnsnt/dream-girl). Pencil2D + AniCraft CLI proven (smoke lane 2026-11-20); Rigby2D needs libEGL this box lacks. | **ON RELEASE — USABLE** |
| **Kdenlive 26.08.3 / Olive 0.2.0-nightly** | Edit + assembly. | Same dream-girl release (AppImages, download on demand). Kdenlive proven with host shims (libOpenGL symlink + vendored libEGL); Olive `--help`/`--version` exit 0 headless. | **ON RELEASE — USABLE** |
| **Natron 2.5.0** | Node compositing. | Nowhere: NOT on disk, NOT in the tools-archive manifest, NOT on the release. | **MISSING — not needed for PURPLE LOT** (Tahoma2D + comp_glow + ffmpeg cover it). If a future short needs it: fresh download from natron.fr, verify binary, record version. Do not claim it until pulled. |
| **Krita 6.0.4** | Draw / paint / cleanup. | Nowhere on disk; NOT in the tools-archive manifest. | **MISSING — not needed for PURPLE LOT.** Fresh download from krita.org if a lane needs it. |

### 1d. Lip sync + dialogue

| Tool | What it does | Real path / proof | Status |
|---|---|---|---|
| **Rhubarb Lip Sync 1.14.0** (CLI) | Phoneme timing from recorded dialogue. | Bundled with Tahoma2D (1.13.0 verified working); standalone 1.14.0 PASS on real dialogue. | **PROVEN — runs on the owner's recorded voice only** |
| **Rhubarb Lipsync NG 1.8.2** | Top-pick lip-sync add-on (same add-on sold $12 on Superhive — the GitHub release is the same add-on free, do not buy). | P10 PASS. | **PROVEN — same voice rule** |
| **Dialogue pipeline** | `production/pipeline/dialogue_pipeline.py`, `lipsync_align.py` — dialogue → timing → mouth shapes. | Repo `production/pipeline/`. | **IN REPO — wire on first voiced short** |
| **NO synthesized voice, ever** | Cape's dialogue is the owner's recorded voice only. No temp voice, no TTS stand-in, in any tool, on any lane. | Standing owner law. | **BINDING** |

### 1e. Lighting, grades, finish — `production/pipeline/` (the real home)

The docs' old `tools/post-pipeline/` path is **STALE** — the tools live at `production/pipeline/` in mhvnsnt/cape-jones (main). Verified live 2026-11-22 (HIGHEST-V-INVENTORY, 24 verified).

| Tool | What it does | Status |
|---|---|---|
| `led_controller.py` (13,650 B) | 15 LED presets incl. `streetlight-hum` (purple-streetlight + 0.004 hum, 30s) and `purple-pulse`. `--list` run live. | **VERIFIED — IN USE** |
| `grades.py` (16,910 B) | 36 grades incl. `purple-streetlight` (colorchannelmixer rr 0.70 / bb 1.35 + sat 1.30 / contrast 1.18 + red/yellow-crushing curves) and `bulb-orange` (dim sodium-orange start, + brightness −0.08). `--list-grades` run live. | **VERIFIED — IN USE** |
| `finish.py` (5,585 B) | QC (ffprobe) → grade → audio mix → libx264 CRF 18 encode. Ran live end-to-end, PASS. | **VERIFIED — IN USE** |
| `comp_glow.py` (5,146 B) | ffmpeg bloom (`--glow`, `--light-wrap`, `--atmosphere`, `--vignette`); presets energy-blast / neon-sign / dream / night-exterior / subtle. **Use `night-exterior` or `subtle` as the starting point — `energy-blast` is too aggressive** (turned a whole test frame magenta/pink). | **VERIFIED — IN USE** |
| `pupil_gag.py` (4,747 B) | Inserts pupil-reaction frames into a face sequence (`--shock-at`, `--look left/right`, `--hold`, clip mode). The exact tool for the fourth-wall button beat. | **VERIFIED — IN USE** |
| `palette-enforce.py` (4,356 B) | k-means palette extract from key art; `enforce` quantizes frames to the palette. Run `extract` on sheet 03 + `enforce` on final frames as a palette QC pass before merge. | **VERIFIED (header) — functional run owed** |
| `led_scene_assembler.py` (13,873 B) | 3 drawings → LED scene (sit/press/release → preset sequence). NOT the PURPLE LOT assembler (that short is a 480f drawn animation) — reference / alt route for the press beat only. | **VERIFIED — REFERENCE** |
| `energy_blast.py` (10,251 B) | Beam / rings / freeze / burst, white core + yellow/cyan corona. | **VERIFIED — N/A for PURPLE LOT (no blaster fires). Ready for shorts that do.** |
| `render_looks.py` + OCIO config | Blender view transforms (Pale Wash / Deep Saturation). **3D-only** — Tahoma2D/Grease Pencil don't use them. 2D equivalents: `cj-day` / `cj-night` / `cj-royal` grades. | **VERIFIED (3D) — do not list as a 2D deliverable** |
| `led_controller` caveats | `streetlight-hum` is sub-visible on a 2s test (byte-identical to the static grade, per its own 0.004/30s spec) — its value is the held constant purple over 20s. The sodium chain reads yellow-bright on white-void poses — judge the start look on boards only. | **RECORDED** |

### 1f. Gated / do-not-use-until-judged

| Tool | Rule |
|---|---|
| **GP Tween 2.4.0** | OWNER-GATED. Interpolates vector strokes between keys. The owner's standing rule (2026-11-11) bans ghostly AI frame interpolation and orders clean solid tween drawings instead. Its output is NEVER shipped as finished in-betweens until the owner eye-judges a real test frame by frame. |
| **Harmony 27 Premium** | Owned, runs on Linux, NOT installed. Unblocker in `docs/SHOW-PRODUCTION-STATUS.md` §5. Account **fmmg.mars@gmail.com ONLY** — never marquiswhitacre@gmail.com. No pirated copies, no licence bypass. |
| **Wan 2.1 I2V (ComfyUI)** | Only where the owner directs. No GPU run of the workflow yet; no end-to-end generated clip yet. |
| **RIFE / interpolation** | Owner law = tweening, NOT ghostly AI interpolation. Use only where directed. |

---

## 2. THE RIG-FIRST WORKFLOW — step by step

This is the Metalocalypse method, built in our stack. Each step names the tool, the input, and the proof that it happened.

1. **Design once.** Model sheets are the source of truth: `characters/sheets/01-tpose-turnaround.jpg` (bind pose), `02-model-sheet-orthographic-turnaround.jpg`, `03-color-lighting-vfx-key.jpg` (palette + rim spec), `05-expression-eye-dart-matrix.jpg` (eye/pupil spec), `08-body-parts-limbs-capes.jpg` (parts). Locked palette: suit #FFFFFF, cowl #3E1473, skin #E5B28C, cape #000000. **Proof:** the sheets, read own-eyes.
2. **Slice the parts.** Cut the T-pose figure (sheet 01) into parts — head, torso, pelvis, upper/forearms, open hands, thighs, shins+feet; cape shapes + hands + belt from sheet 08; 9 eye-pair sprites from sheet 05; remote + gag hand from poses 02/03. Slice from real source art first; Gemini (custom.gemini, Key 3, LIVE) only for what is missing. **Proof:** `rig/parts/*.png` + manifest + contact sheet, own-eyes checked. (Rig lane running: `~/workspace/_cape-jones-parking-lot-2d/rig/`.)
3. **Build the rig.** COA Tools 2: sprite object → import parts → automesh → bones → IK → bind. Mouth/eye sprite libraries for swapping (9 eye pairs from sheet 05; neutral + half-smile mouths). Wiggle 2 RTX on the cape bones (live sim, per §1b). **Proof:** `RIG-REPORT.md` + 9 rig poses rendered (transparent) + composited over board backdrops, own-eyes verified.
4. **Paint the backgrounds.** Real painted lot plates, sodium + purple versions, Jones removed. Backgrounds are the real lot from the boards (`production/2d-parking-lot/boards/`), never void-white. **Proof:** clean plates, both lighting states, own-eyes verified. (Backgrounds lane running: `~/workspace/_cape-jones-parking-lot-2d/v2/backgrounds/`.)
5. **Block the episode in edit first.** ATHF rule: radio play / voice line cut first, then a bare-bones animatic that implies the action — the short is blocked out in edit before any posing starts. For PURPLE LOT the 7 boards (CJ-PL-01..07) are the blueprint. **Proof:** the edit (boards + timing) approved before posing.
6. **Pose the rig on twos.** A new rig pose every 2 frames at 24fps (12 poses/sec). The computer tweens between poses. The cape leads every gag; the body follows a beat late. Arms down, feet planted on idles. **Proof:** the pose list with exact frame numbers; no two consecutive twos share a pose unless the beat is a deliberate drawn hold (see §3).
7. **Hand in-betweens only where the rig cannot reach.** Grease Pencil, drawn, for the beats the rig genuinely cannot do (the glove-gag slow hand-lift, the pupil roll, the cape billow past the sim's range). Never as the drawing engine for the whole cut. **Proof:** each hand in-between own-eyes verified against its adjacent rig poses.
8. **Face and pupil beats.** Eye sprites swap per the pupil canon (white eyes default; pupils only for a specific sensation the beat requires). The fourth-wall button: pupil appears + rolls to the audience, head unmoved, via `pupil_gag.py` + eye sprites. Face bar on every key: defined brow, nose bridge, jaw line, cheek plane — never flat/cartoony. **Proof:** the face frames, own-eyes verified.
9. **The lighting shift happens in post.** "Animated lights animate the GRADE, not the drawing. The drawing stays clean; the light moves in post." (REAL-LIGHTING-RESEARCH §6.) Sodium start = `bulb-orange` + brightness −0.08; end = `purple-streetlight` grade / `streetlight-hum` preset; shift over the beat's frames. **Proof:** graded board pairs (sodium-dim + purple-streetlight on CJ-PL-02), own-eyes PASS.
10. **Composite.** Tahoma2D (`tcomposer`, absolute paths) — rig renders + backgrounds + glow + rim. AnimLab node graph when its smoke test proves it. **Proof:** the composited frames, own-eyes verified.
11. **Finish.** `finish.py`: QC → grade → audio mix (owner's voice/track only, when they exist) → encode. Palette QC: `palette-enforce.py` extract on sheet 03 + enforce on final frames. **Proof:** ffprobe (480f, 20.000s, 1280×720, 24fps) + hash + size.
12. **Own-eyes gate.** The lane lead reads the cut frame by frame against the checklist in §5. Nothing reaches the owner unviewed. **Proof:** the frame-range verification log in the lane checkpoint.
13. **Stage it.** Branch → PR → merge, add-only, zero-conflict, post-merge readback of every file (blob sha + size). The repo is the save — work lands in the repo the second it exists, never in /tmp, never only on local disk.

---

## 3. TIMING RULES — the numbers that make it TV

| Rule | Value | Source |
|---|---|---|
| Frame rate | **24fps**, always. Not 48. | Metalocalypse broadcast standard; SHOW-PRODUCTION-STATUS §4; V2 bar correction 2026-11-22. |
| Drawing/pose density | **On twos as the floor** — a new rig pose every 2 frames (12 poses/sec). On ones (24/sec) for fast action, impacts, the pupil roll. | Hand-drawn TV standard; SHOW-PRODUCTION-STATUS §4. |
| Holds | **Only with micro-motion.** A hold is a short snap, then a hold WITH LIFE — pose change, arms down, cape settling, light shifting. Never a 3-second freeze, never 15–30 second static holds ($UPEREGO's holds are what the owner rejected). | SHOW-PRODUCTION-STATUS §4; owner rejections (90s slideshow, V1). |
| Mouth flaps | On the dialogue, from Rhubarb timing on the owner's recorded voice. Approximate is fine — $UPEREGO's lip sync is approximate and it works — but the mouth must move when he talks. | $UPEREGO Part 1; Rhubarb P10 PASS. |
| Punchline | **Line + beat of silence + drawn held reaction, no sting, no music bed under the dialogue.** Then hard cut. | $UPEREGO Parts 1–2; SHOW-PRODUCTION-STATUS §4. |
| Episode format | **11 minutes** for episodes. Cut hard in the edit — hours of material down to 11. (Metalocalypse tried 22 in S3, went back to 11 in S4.) | Metalocalypse (MediaMikes); SHOW-BIBLE §1 (36×11-min Gumball unit). |
| Short format | **1–2.5 minutes**, cold open, one location, hard-cut ending, title phrase or button line last. | $UPEREGO Parts 1–2 (episodes 1:06–2:28). |
| Cadence | **Biweekly Fridays.** Same handle everywhere. Patreon a week early. TikTok discovery, YouTube binge home. | $UPEREGO Parts 1–2. |
| Setups per short | **4–6 setups in ~2 minutes** (ep8: 5/129s; ep9: 4/131s; ep10: 5–6/147s; ep7: 7–9/147s). | $UPEREGO Part 4 beat maps (this study). |
| Sincere beat | **One per short**, 20–45 seconds, never announced, never apologised for. In Cape Jones it lands through a pose change + a lighting shift, not a lecture freeze. | $UPEREGO Parts 2–3 (ep9's 43s monologue is the longest single beat). |
| Titles | **Meme-bait, two words, carries the premise** (PURPLE LOT, W33D RABIES, SLIME BABY). | $UPEREGO Part 1. |

---

## 4. CANON CHECKLIST — every cut, every time

From `docs/SHOW-BIBLE.md` + owner corrections 2026-11-22 (all in MEMORY.md). A cut that fails any line does not ship.

- [ ] Locked palette: suit #FFFFFF (stays blown out, tint on rim/glow only), cowl & logo #3E1473, skin #E5B28C, cape & shadows #000000. 2–4px rim light, environment-coloured. No gradients.
- [ ] White eyes default. Pupils ONLY for a specific sensation the beat requires — never decoration. (CJ-PL-06: no-pupil smug side-eye + half-smile. Ending button: pupil appears + rolls to the audience, head unmoved.)
- [ ] Comic-book face bar: defined brow, nose bridge, jaw line, cheek plane. Never flat/cartoony.
- [ ] All-white gloves in every normal/wide shot. Bare hand ONLY inside the glove-gag beat: hand lifts slowly, Jones out of focus behind, thumb clicks, cut to wide and the gloves are back on with no explanation.
- [ ] Arms down at sides, feet planted, for every natural idle. The cape leads every gag; the body follows a beat late. The Cape is the most competent character.
- [ ] Lighting shift big and visible: dim sodium orange → broken-streetlight purple (`streetlight-hum` → `purple-streetlight`). The light IS the sincere beat.
- [ ] Real painted backgrounds, never void-white. The lot, the water tower, the couch — real places.
- [ ] Jones + Cape alone in PURPLE LOT (the Fan does not appear). The Fan never mocks Jones.
- [ ] Hard cut to black at the end. No fade, no sting. (V1 lesson: never use empty cells for black — use an explicit black level frame.)
- [ ] Silent until the owner records. Voice "ah, that's better" is his recording only. One original track per short is his call (he is the Carmen slot). No temp music, no synthesized voice, no music bed under the line.
- [ ] 480 frames, 20.000s, 1280×720, 24fps for PURPLE LOT. Hash + size recorded. Post-merge readback from main.

---

## 5. PRE-DELIVERY CHECKLIST — the "feels like TV" gate

**No cut passes this gate without every box checked.** The lane lead checks them with their own eyes, on the actual frames, and logs the result in the lane checkpoint. If a box cannot be checked, the cut does not ship — the gap is logged and worked, never hidden (NO-GAPS law).

**Motion**
- [ ] The rig moves every 2 frames — no two consecutive twos share a pose without a deliberate, logged reason.
- [ ] No static hold longer than the beat requires, and every hold has visible micro-motion (cape settling, breathing, light shifting).
- [ ] The hero hold from V1 (59 static frames on one drawing) does not recur — the cape-settle beat covers it.
- [ ] Walk-ins / moves are posed, not slid. Cheats (popsicle-stick in, cutaway + cut back) are logged as cheats, never presented as full animation.

**Look**
- [ ] Every frame on palette (palette-enforce pass run, or the reason it wasn't is logged).
- [ ] Real painted background in every shot. No void-white frames except the deliberate black tail.
- [ ] Lighting shift visible on the actual frames (sodium → purple), not just in the grade chain.
- [ ] Rim light present and environment-coloured; the suit stays blown out except the grade's designed tint.

**Performance**
- [ ] Mouth moves when he talks (Rhubarb timing on the recorded voice, when voice exists).
- [ ] Pupil beats exactly as canon: no-pupil smug at 06, pupil appears + rolls at the button, head unmoved.
- [ ] Glove gag staged exactly: bare hand ONLY in the gag beat, gloves back on in the next wide with no explanation.
- [ ] Face bar holds on every key (brow, nose bridge, jaw, cheek plane).

**Edit + sound**
- [ ] Cold open, no title card. One location. Hard cut to black, no fade, no sting.
- [ ] Punchline = line + beat of silence + drawn held reaction.
- [ ] Silent unless the owner's voice/track landed. No temp audio anywhere.
- [ ] ffprobe: 480 frames, 20.000s, 1280×720, 24fps, h264. Hash + size recorded.

**Honesty**
- [ ] The delivery states the TRUE drawing/pose count and the TRUE method (rig poses vs hand drawings). Never "240 drawings" unless 240 drawings exist.
- [ ] Every gap is named in the report (voice, track, AnimLab status, open in-betweens). No gap is reported as done.
- [ ] Post-merge readback: every payload file read back from main (blob sha + size) before the cut is called done.

---

## 6. WHERE THINGS LIVE — index

- **Method study:** `docs/TV-SHOW-METHOD-STUDY.md` (this playbook's companion — the three shows, side by side, with sources).
- **Show bible:** `docs/SHOW-BIBLE.md` (logline, flaw engine, palette, pupil canon, cast slots, canon gags, THE PARKING LOT).
- **Production status (source of truth):** `docs/SHOW-PRODUCTION-STATUS.md` (§4 the "real cartoon" list; §5 Harmony; §9–10 the test-short order + the rig-first method change).
- **Asset inventory:** `docs/ASSET-INVENTORY.md` (Gumball bible + S2 .fla rigs HAVE; Space Ghost sheets HAVE; Teen Titans GAP).
- **$UPEREGO studies:** `docs/SUPERIOR-TURBINATE-STUDY.md`, `docs/SUPERIOR-TURBINATE-DEEP-STUDY.md`, `docs/SUPERIOR-TURBINATE-FEELING-STUDY.md`.
- **2D production doc:** `docs/2D-PARKING-LOT-PRODUCTION.md` (Tahoma2D setup fixes §3; V1 status §5).
- **AnimLab runbook:** `docs/ANIMLAB-PIPELINE.md` (PR #426).
- **Boards + poses:** `production/2d-parking-lot/boards/` (CJ-PL-01..07, BOARD-LIST.md) + `production/2d-parking-lot/poses/` (8 poses + cape study, POSE-LIST.md).
- **Video:** `production/2d-parking-lot/video/purple-lot-v1.mp4` (SUPERSEDED cut — do not delete, do not present as the standard). V2 lands here when the rig-first build finishes.
- **Pipeline scripts:** `production/pipeline/` (led_controller.py, grades.py, finish.py, comp_glow.py, pupil_gag.py, palette-enforce.py, led_scene_assembler.py, energy_blast.py, lipsync_align.py, dialogue_pipeline.py, + more).
- **Highest-V inventory:** `~/workspace/_cape-jones-parking-lot-2d/HIGHEST-V-INVENTORY.md` (24 verified / 6 missing / 3 N/A — the proof log for §1).
- **Rig lane:** `~/workspace/_cape-jones-parking-lot-2d/rig/` (PROGRESS.md, slice_parts.py, probe_coa.py).
- **Backgrounds lane:** `~/workspace/_cape-jones-parking-lot-2d/v2/backgrounds/`.
- **Wiggle cape proof:** `~/workspace/_cape-jones-parking-lot-2d/wiggle-cape-proof/PROOF-REPORT.md`.
- **AnimLab lane:** `~/workspace/_animlab-wireup-20261120/CHECKPOINT.md`.
- **This lane:** `~/workspace/_cape-jones-tv-show-method/CHECKPOINT.md`.

## GAPS — stated plainly

- **Voice** "ah, that's better" — owner-only, his recording. **Original track** for PURPLE LOT — owner-gated, Real is the Carmen slot. Both stay open until he lands them; the cut ships silent until then.
- **AnimLab smoke test** — pending (Kaggle `marsfmmg/animlab-smoke-test`). AnimLab stays an experiment candidate until it proves on a real shot.
- **COA rig proof renders** — the rig lane is building now; no rig poses have been rendered and verified yet.
- **Background plates** — the backgrounds lane is cleaning the lot plates now; no sodium + purple plate pair is staged yet.
- **ib-04a slow hand-lift** — the media tool declined it (integrity check), not retried; the gag stages via board 04 → ib-04b click. A hand-drawn lift is still owed to the rig/Grease Pencil lane.
- **Natron / Krita** — missing, not needed for PURPLE LOT.
- **GP Tween** — owner-gated, never ship until he eye-judges a test.

---

*Playbook v1 — 2026-11-22. When a lane proves a new piece of the pipeline on a real shot, the finding lands here (and the method study, if it changes what we copy). The playbook is the working doc; the method study is the evidence behind it.*
