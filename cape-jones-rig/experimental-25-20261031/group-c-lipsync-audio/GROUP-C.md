# Group C — Lip-sync / Audio (experimental-25, 2026-10-31)

**Scope:** Cape Jones, 2D cutout show, v7c rig, visemes v2 exist.
**Honest headline: 0/5 models were run. 5/5 are METHOD-WIRED.**
No model weights were downloaded, no paid service was used, no GPU
was available on this VM (`nvidia-smi` not found), and no output below
is a photoreal talking-head video. Every proof is a deterministic
timeline built from the project's published method, applied to a
synthetic, word-free amplitude envelope (6 bursts, 24 fps, 58 frames,
2.4 s nominal). No show character appears, no dialogue was copied,
no file Mars has seen was overwritten. Nothing was pushed to any repo.
**Mars approval: 0/1 — do NOT claim approved.**

## Why reference/timing only, for all five

Cape uses **viseme swap drawings** (Pack 4 spec, 14 slots: rest, EE,
EH, AH, OH, OO, MBP [M/B/P closed], FV [F/V], L, SZ [S/Z], TH, R, W,
GK [G/K]), not a photoreal head that a generator can redraw frame by
frame. All five tools below output photoreal / rendered portrait
video. Their pixels cannot be pasted into a cutout rig without breaking
the style, the v7c joint lock, and the checkpoint rule. What transfers
honestly is **timing**: when a mouth changes, how long it holds, and
how the head moves with the voice. That is what the method-wired
proofs deliver — a frame-by-frame exposure sheet, not a Cape render.

## Table

| # | Project | Method (published) | Exact Cape problem it helps | Free / paid | Wired status | Proof file (viewed) |
|---|---|---|---|---|---|---|
| 1 | Wav2Lip | Mel-spectrogram audio + masked face frames -> generator redraws mouth; a pre-trained SyncNet lip-sync expert discriminator scores audio/video sync | Lip-sync to dialogue: per-frame viseme timing, incl. dialogue shots (CJ-26 etc. per task brief); onset-aligned mouth changes | Free, open source (original code); commercial successor Sync (sync.so) is paid — not used | METHOD-WIRED — model NOT run: envelope onset -> Cape viseme per frame + SyncNet-style confidence | `proofs/01-wav2lip-viseme-timeline.png` + `.csv` (58 rows) |
| 2 | SadTalker | Audio -> 3DMM coefficients via ExpNet (expression) + PoseVAE (head pose), then 3D-aware face rendering; adds blinks | Audio-driven head motion + expression for dialogue shots; mouth itself stays a Cape swap viseme, head curve is borrowed | Free, open source, Apache 2.0 per sources | METHOD-WIRED — model NOT run: audio envelope -> yaw/pitch + expression + blink timeline | `proofs/02-sadtalker-head-motion.png` + `.csv` (58 rows) |
| 3 | LivePortrait | Implicit-keypoint portrait animation: a DRIVING VIDEO's expression/head motion is retargeted onto a still portrait, with stitching/retargeting control — NOT audio-driven | Head-motion / expression reference ONLY, and only if an acted driving video exists first; does NOT solve lip-sync from audio alone | Free, open source (KwaiVGI code); hosted wrappers sell credit packs — not used | METHOD-WIRED, PROXY ONLY — model NOT run: envelope labelled PROXY-DRIVING-SIGNAL, not a real driving video | `proofs/03-liveportrait-retarget.png` + `.csv` (58 rows) |
| 4 | EMO (Emote Portrait Alive) | Direct audio-to-video diffusion (Stable Diffusion backbone + temporal modules): ReferenceNet holds identity, audio encoder drives expression/head pose; speed + face-region controllers stabilise it; no 3D model or landmarks | Expressive dialogue/singing timing: smooth head + expression curve, 2-frame viseme holds (Cape-friendly smoothing) | Research paper/project page free; NO hosted free generation interface confirmed — not a deployable free tool as-is | METHOD-WIRED — model NOT run: audio energy + speed controller -> smooth pose + 2-frame-held visemes | `proofs/04-emo-expression-timeline.png` + `.csv` (58 rows) |
| 5 | Hallo | Hierarchical audio-driven diffusion synthesis: audio features aligned at multiple levels (coarse motion + fine lip detail) via UNet denoiser + ReferenceNet, with temporal alignment | Dialogue shots end-to-end timing: coarse syllable-level head motion + fine frame-level viseme in one exposure sheet | Free, open source, MIT (code) per sources; needs CUDA GPU + large weights to run for real | METHOD-WIRED — model NOT run: coarse syllable head motion + fine per-frame viseme, temporally aligned | `proofs/05-hallo-hierarchical-timeline.png` + `.csv` (58 rows) |

**Counts:** 5/5 projects researched, 5/5 method-wired, 0/5 models run,
0/5 direct Cape outputs, 5/5 reference/timing only, 0 paid installs,
6 proof images viewed (5 timelines + 1 viseme schematic), 5 CSVs
(58 data rows each, 290 total), 1 script, 0 repo pushes.

## Per-project notes

### 1. Wav2Lip — lip-sync from audio
- **What / who:** "Accurately Lip-syncing Videos In The Wild" (2020),
  from IIIT Hyderabad researchers; the team later founded Sync
  (sync.so). A generator modifies the mouth region to match input
  audio; a pre-trained SyncNet discriminator checks sync.
- **Experimental method:** feed audio + a face video, get a
  re-synced mouth. Zero-shot (no per-person training), any language.
- **Cape fit:** closest to the core need — pure lip-sync timing.
  Wav2Lip's own output is a redrawn photoreal mouth, so for Cape it
  is a timing reference: its onset/confidence curve tells the
  animator *when* to swap visemes, not *what* the Cape mouth looks like.
- **Blocker to a real run here:** CUDA GPU + `wav2lip.pth` /
  `wav2lip_gan.pth` weights + face-detection weights; also the
  original models were trained on LRS2, with sources noting research/
  personal use for the open model and commercial use via Sync.
- **Method wired as:** envelope onset -> viseme per frame, with a
  SyncNet-style confidence column (onset alignment, 0–1).
  Proof viewed: envelope peaks line up with viseme blocks; rest
  frames sit in the gaps.

### 2. SadTalker — audio-driven talking head
- **What / who:** CVPR 2023, Zhang et al., "Learning Realistic 3D
  Motion Coefficients for Stylized Audio-Driven Single Image Talking
  Face Animation". Single portrait + audio -> talking-head video
  with lip motion, blinks, expression, head movement.
- **Experimental method:** generate 3DMM motion coefficients
  (ExpNet for expression, PoseVAE for pose) separately, then render
  — motion is explicit and editable, unlike direct pixel warping.
- **Cape fit:** second-best. Its head-pose + blink + expression
  curves are directly reusable as v7c head-motion keys; its mouth
  rendering is NOT reusable (Cape mouth is a swap drawing).
- **Blocker to a real run here:** CUDA GPU + checkpoints + a
  portrait input; photoreal output would still need manual
  translation to viseme swaps.
- **Method wired as:** smoothed yaw/pitch (deg), expression
  (0–1), blink flag on pauses, plus a viseme column.
  Proof viewed: yaw curve swings with the envelope, blinks only
  in low-energy gaps.

### 3. LivePortrait — portrait animation
- **What / who:** Kuaishou Technology (KwaiVGI) with USTC and Fudan,
  2024, "Efficient Portrait Animation with Stitching and
  Retargeting Control". Implicit-keypoint framework, ~12.8 ms/frame
  on an RTX 4090 in the research implementation.
- **Experimental method:** source portrait + DRIVING VIDEO ->
  portrait mirrors the driving performance (expression, eyes, lips,
  head). Stitching handles multi-person / shoulder regions;
  retargeting scales motion to the source face.
- **Cape fit — weakest for lip-sync, honest warning:** it is NOT
  audio-driven. It cannot lip-sync dialogue from audio alone. It
  only helps if Mars (or an actor) first records a driving
  performance video; then its retargeted head/expression curve can
  be read as timing reference. Do not pitch it as a lip-sync tool.
- **Blocker to a real run here:** CUDA GPU + pretrained weights +
  a driving video (which does not exist for this test); the
  envelope proxy below is explicitly NOT a driving video.
- **Method wired as:** proxy lip aperture + head pose, with every
  CSV row labelled `PROXY-DRIVING-SIGNAL (envelope, NOT a real
  driving video)`. Proof viewed: smoothest curve of the five,
  because retargeting/stitching smoothing was applied — that
  smoothness is the method's signature, not a measured result.

### 4. EMO (Emote Portrait Alive, Alibaba) — audio-driven portrait video
- **What / who:** Alibaba Group Institute for Intelligent Computing,
  Tian, Wang, Zhang & Bo, February 2024 (arXiv 2402.17485).
  Single reference image + vocal audio -> expressive talking or
  singing video, any duration, in photographic, painted, or anime
  styles, without 3D models or facial landmarks.
- **Experimental method:** direct audio-to-video diffusion:
  ReferenceNet extracts identity, an audio encoder + attention
  modulates a Stable-Diffusion-based video backbone (temporal
  modules, 3D convolutions), with speed and face-region controllers
  for stability across long clips.
- **Cape fit:** good for expressive/singing dialogue timing — its
  speed-controller idea maps cleanly to Cape: hold visemes longer
  on slow/sung lines, change faster on patter. Its video pixels
  are NOT a Cape output.
- **Blocker to a real run here:** no hosted generation interface
  confirmed in sources; local use needs the research codebase,
  diffusion weights, and a strong GPU. Paper/project page are free
  to read, which is not the same as a free runnable tool.
- **Method wired as:** audio energy + speed controller -> smooth
  head pose, visemes held 2 frames (quantised) to mimic the
  stability controllers. Proof viewed: viseme blocks are visibly
  longer/steadier than Wav2Lip's per-frame changes.

### 5. Hallo — audio-driven portrait animation
- **What / who:** Fudan Generative Vision team (Xu et al., 2024),
  "Hierarchical Audio-Driven Visual Synthesis for Portrait Image
  Animation"; Hallo2 (Fudan + Baidu) extends it to 4K and hour-long
  clips with text-prompt expression control; Hallo3 adds
  cross-attention audio conditioning. This task's item is Hallo
  (v1); v2/v3 are noted only to avoid version confusion.
- **Experimental method:** hierarchical diffusion: audio is aligned
  to visuals at coarse and fine levels, with a UNet denoiser,
  ReferenceNet for identity, and temporal alignment for
  consistency across frames.
- **Cape fit:** most promising for Cape's actual workflow (see
  below). A two-level timeline — syllable-level head motion +
  frame-level viseme — is exactly how a cutout exposure sheet is
  laid out (pose/hold row + mouth row). Hallo's hierarchy is the
  only one of the five whose structure matches the animator's
  sheet, rather than just its timing.
- **Blocker to a real run here:** CUDA GPU (sources note 12 GB+
  VRAM for web UIs), pretrained weights from Hugging Face, and
  photoreal output that still needs manual viseme translation.
- **Method wired as:** coarse column (nod / tilt-L / tilt-R /
  settle per syllable burst) + fine viseme column per frame.
  Proof viewed: coarse blocks change only at burst boundaries
  while fine visemes change per frame — the two-level split is
  visible in the CSV and in the strip.

## Most promising project — and why

**Hallo (v1 method), for Cape specifically.** Not because it is the
most photoreal — EMO arguably is — but because its hierarchical
structure ports to a cutout show with the least translation loss:
coarse head motion per syllable + fine viseme per frame = the two
rows of a Cape exposure sheet. Wav2Lip is the runner-up for pure
lip-sync timing (its SyncNet confidence is the most defensible
onset check), and SadTalker is the runner-up for head motion
(explicit 3DMM curves). LivePortrait ranks last for this task
because it needs a driving video; EMO ranks below Hallo because
its diffusion smoothness, while expressive, hides the discrete
viseme decisions a swap-drawing show needs to see.

**Recommended next step (needs Mars's call, not built here):**
run the Hallo method-wired script against a REAL Cape dialogue
audio file (not the synthetic envelope) to produce a real
exposure sheet for one dialogue shot, then have an animator check
it against visemes v2 before any GPU run is attempted. A GPU run
(Kaggle/Colab free tier, per the free-first rule) should only be
attempted for timing reference, never as a Cape output, and only
after Mars approves that specific run.

## Files in this folder

- `GROUP-C.md` — this table and notes.
- `method_wired.py` — the single script that generated all proofs.
  Re-run: `python3 method_wired.py` (needs numpy, matplotlib, PIL;
  no GPU, no downloads, no paid calls).
- `proofs/00-cape-viseme-schematic.png` — generic abstract mouth
  shapes for the 14 Pack-4 viseme slots. NOT show character art,
  NOT a head drawing; a schematic only.
- `proofs/01-wav2lip-viseme-timeline.png/.csv`
- `proofs/02-sadtalker-head-motion.png/.csv`
- `proofs/03-liveportrait-retarget.png/.csv`
- `proofs/04-emo-expression-timeline.png/.csv`
- `proofs/05-hallo-hierarchical-timeline.png/.csv`
- All 6 proof images were opened and viewed in this session;
  charts are legible, viseme labels are readable (every 2nd frame
  labelled on the strip; the CSV carries every frame).

## Sources (public web, searched 2026-10-31)

- Wav2Lip — open-source overview, SyncNet discriminator, IIIT
  Hyderabad origin, Sync commercial successor:
  https://lipsync.com/blog/open-source-lip-sync
  https://trtc.io/blog/details/ai-lip-sync-tools-video-translation
- SadTalker — CVPR 2023, 3DMM coefficients, Apache 2.0:
  https://sync.so/blog/what-is-sadtalker
  https://sadtalker.ai/
- LivePortrait — KwaiVGI, driving-video retargeting, 12.8 ms/frame
  on RTX 4090, open code vs paid hosted wrappers:
  https://www.visionstory.ai/open-source/liveportrait
  https://aitools.fyi/live-portraits
- EMO — Alibaba Institute for Intelligent Computing, arXiv
  2402.17485, direct audio-to-video diffusion, no 3D/landmarks,
  no hosted interface:
  https://arxiv.org/html/2402.17485v3
  https://thetoolsverse.com/tools/emote-portrait-alive-emo
- Hallo — Fudan Generative Vision, hierarchical diffusion, MIT,
  Hallo2 4K/long-duration context:
  https://ai-search.io/tool/liveportrait
  https://huggingface.co/fudan-generative-ai/hallo2/raw/main/README.md
  https://aisharenet.com/en/hallo2/

## What was NOT done (honest gaps)

- No model was installed, built, or run (no GPU, weights untested
  here). Any future claim of a "run" needs a GPU session log and
  frames in hand, not a script receipt.
- No real Cape dialogue audio was used (synthetic envelope only),
  so no timeline here matches a real line or a real CJ shot yet.
- No real Cape head/viseme frame was fed to any tool — the
  schematic is abstract, and the timelines are method translations,
  not renders of the v7c rig.
- No paid service, API key, or account was created.
