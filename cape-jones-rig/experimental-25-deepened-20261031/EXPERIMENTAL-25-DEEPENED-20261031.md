# EXPERIMENTAL 25 — DEEPENED, TV-PRODUCTION-TRIAGED — Mars 100% sweep, 2026-10-31

**Status, plainly. No claim of approval, landing, or vendor success.**
- Researched: 25/25 = 100%
- Vendor tool actually ran on this VM: 0/25 = 0%
- Method-wired with a labelled proxy proof: 25/25 = 100%
- Deepened in this task (what it helps / run vs mapping / honest proxy limit / next gate): 25/25 = 100%
- Next-gate GPU/paid runs done in this task: 0/25 = 0% — every next gate below needs a specific Mars approval first. No Kaggle/Colab run was made, no paid tier bought, no account created for a paid tool. The only account named in the parent task (FMMG, fmmg.mars@gmail.com) was NOT used, because no GPU run was approved or attempted.
- No repo push in this task. No file Mars saw was overwritten. All outputs are new dated files in this folder and in `limits-broken-push2-20261031/`.
- Source index carried forward: `experimental-25-20261031/EXPERIMENTAL-25-INDEX-20261031.md` (25/25 researched, 0/25 vendor-run, 25/25 proxy-wired). This document deepens that index; it does not replace its honesty labels, and no proxy is re-labelled here as a vendor result.

## 1. TV PRODUCTION READINESS TRIAGE — focus change 2026-10-31 20:53 CDT

Work that does not block an episode/segment is **ADDITIVE/EXTRA, not a production blocker** — even if it is technically interesting. Priority is: anything that actually unblocks a shot, a storyboard/animatic, or an audio step, first.

| Tier | Count | Share | Meaning |
|---|---|---|---|
| PRODUCTION-UNBLOCKING — shot | 6/25 | 24% | Removes a bottleneck for a named shot step |
| PRODUCTION-UNBLOCKING — storyboard/animatic | 2/25 | 8% | Gives a timing/motion reference before hand-keyframing |
| PRODUCTION-UNBLOCKING — audio/dialogue | 3/25 | 12% |
| **PRODUCTION-UNBLOCKING total** | **11/25** | **44%** | **Do these first if Mars approves a next gate** |
| ADDITIVE/EXTRA | 14/25 | 56% | Alternative, measurement, polish, or pipeline alternative; the step already works without it (hand-keyframe, Blender, ffmpeg, 14-viseme swap) |

**Production-unblocking 11:** A2 FILM, B1 MediaPipe Pose, D1 ControlNet, D5 Depth Anything/MiDaS, E1 SAM 2, E2 Grounding DINO, E3 MotionDiffuse, E4 Animate Anyone, C1 Wav2Lip, C2 SadTalker, C5 Hallo.

**Additive/extra 14:** A1 RIFE, A3 ToonCrafter, A4 EbSynth, A5 RAFT, B2 OpenPose, B3 DWPose, B4 Cascadeur, B5 Plask/MoveAI, C3 LivePortrait, C4 EMO, D2 Style2Paints, D3 Anime2Sketch, D4 Natron, E5 Olive.

**Why the split is drawn this way (auditable, not taste):**
- A duplicate method is additive even if it is good: RIFE duplicates FILM, OpenPose/DWPose duplicate MediaPipe's pose job, Plask/MoveAI duplicate a performer-clip pose route, EMO duplicates Hallo/Wav2Lip timing, Natron duplicates a Blender compositor that already renders, Olive duplicates an ffmpeg edit that already exists.
- A measurement or reference-only method is additive unless it is the *only* route to a required artefact: RAFT measures motion but does not make a frame; Style2Paints/Anime2Sketch give a reference, not a locked shot.
- A method is unblocking only if it supplies a shot artefact, a storyboard/animatic timing, or an audio-step artefact (exposure sheet, dialogue timing, head-motion curve) that the current pipeline cannot already supply by hand at the same step.

**Priority order if Mars gives specific approval for a next gate (in order, unblockers first):**
1. Audio: Hallo (C5) then Wav2Lip (C1) — real exposure sheet for one dialogue shot (e.g. CJ-26 class), checked against visemes v2. GPU output would be timing reference only, never pasted Cape output.
2. Shot labelling: SAM 2 + Grounding DINO (E1+E2, one workflow, two projects) — one free-GPU run on a real rig frame, mask vs hand-traced ground truth, before any batch labelling is trusted.
3. Shot pose: MediaPipe Pose (B1) — install libegl1, run Pose Landmarker on 4 pose frames + 1 real performer dance clip, report detector-vs-by-eye delta (±10–15° by-eye tolerance). If it fails on cutout art, run on performer and retarget, never on cartoon.
4. Shot inbetween: FILM (A2) — one free-tier run on ginyu-01→ginyu-03, A–B vs proxy, for large jumps / wide disocclusion only.
5. Shot depth: Depth Anything Small (D5) — one free-GPU run on JoJo-01, A–B vs pseudo-depth proxy; fallback if thin limbs fail = hand-assigned per-limb depth layers.
6. Additives only after 1–5, and only with their own licence/approval check (see per-project rows).

**What still blocks episodes/segments, regardless of the 25 (so the 25 are not oversold):**
From the limits audit, production-blocking limits are 7/20 = 35% (L01 masters, L11 per-shot finals frame size/safe areas, L12 final recorded audio, L13 Arm1, L14 torso-twist master, L15 device-grip prop, L16 129-sheet eye pass). The other 13/20 = 65% are additive/polish/validation or already broken (L02, L03, L04, L05, L06, L07, L08, L09, L10, L17, L18, L19, L20 — see limits-push report). No experimental project in the 25 removes L11, L12, or L16: those need a Mars decision, a recording session, and human viewing respectively. Saying otherwise would be false.

## 2. TOP 5, DEEPENED (ranked as in the source index)

### 1. A2 FILM (Google, Reda et al., ECCV 2022) — PRODUCTION-UNBLOCKING, shot
- **What it helps:** Large pose jumps and wide disocclusion inbetweening — exactly Cape's hardest inbetween cases. Scale-agnostic single network, Gram loss.
- **Run vs mapping:** MAPPING ONLY in this task and in the source index. No FILM inference ran. The source proof is a PIL proxy (film-proxy-ginyu01-to-ginyu03), not FILM output.
- **Honest proxy limit:** Pixel-flow warping ghosts/doubles on large Cape pose changes (white-on-white, rigid cutout parts). Proxy proves the *timing/onion-skin aid* idea for small motion, not a replacement for rig-part joint-angle inbetweening. Do not quote the proxy as a FILM frame.
- **Licence / cost:** Free/open, Apache 2.0. Paid wrappers not used, none bought.
- **Next gate (needs specific Mars approval, NOT run):** One free-tier FILM run on ginyu-01→ginyu-03, A–B vs proxy.

### 2. B1 MediaPipe Pose / BlazePose, 33 pts (Google) — PRODUCTION-UNBLOCKING, shot
- **What it helps:** Pose reference, elbow/knee/shoulder/hip angles, knee-feet, foot turnout. Schema maps 1:1 onto v7c joints; cheapest mocap on-ramp; if it works on a performer clip, paid Plask/MoveAI may be unnecessary.
- **Run vs mapping:** PARTIAL RUN, FAILED INFERENCE, honestly recorded. Version 1.2.0 was installed; inference failed (libEGL missing). The source proof is a labelled overlay proxy, not a detector output.
- **Honest proxy limit:** Detectors are unproven on cutout art (likely out-of-distribution). By-eye tolerance ±10–15° — good to flag a pose, not to lock a rig joint. Run on performer and retarget if cartoon art fails.
- **Licence / cost:** Free, Apache-2.0, commercial use allowed (unlike OpenPose).
- **Next gate (needs specific Mars approval for any GPU/hosted step; the local libEGL fix itself is free):** Install libegl1, run Pose Landmarker on 4 pose frames + 1 real performer dance clip, report detector-vs-by-eye delta.

### 3. E1 SAM 2 + E2 Grounding DINO (Meta; IDEA/Tsinghua/Microsoft) — PRODUCTION-UNBLOCKING, shot — counted as two projects, one workflow
- **What it helps:** The FLA piece segmentation/labelling bottleneck. Grounding DINO: words → boxes (hand/piece detection, no retraining). SAM 2: click/box/mask → mask. Together they slot into the existing pipeline without shipping generated footage.
- **Run vs mapping:** MAPPING + SYNTHETIC PROXY ONLY. E1 proxy: point → head mask 9,009 px on a synthetic figure, NOT Cape art. E2 proxy: 4 boxes, no weights/scores faked. No vendor weights ran.
- **Honest proxy limit:** Synthetic-figure masks do not prove Cape-piece masks. Batch labelling must not be trusted until a real-rig-frame mask is measured against hand-traced ground truth.
- **Licence / cost:** Both free/open (SAM 2 Apache 2.0; Grounding DINO free/open).
- **Next gate (needs specific Mars approval, NOT run):** One free-GPU run on a real rig frame, mask vs hand-traced ground truth.

### 4. D5 Depth Anything / MiDaS (Yang 2024; Ranftl 2020) — PRODUCTION-UNBLOCKING, shot
- **What it helps:** Per-limb relative depth from one frame, for 2.5D parallax, layer ordering, and depth-graded rim/wrap falloff. ControlNet depth conditioning also needs this map.
- **Run vs mapping:** MAPPING + WEAKEST PROXY. Source proxy is silhouette-distance pseudo-depth, not a model depth map.
- **Honest proxy limit:** The proxy is inverted for thin limbs (torso bright, thin limbs dark — opposite of true body-part depth) and shows a parallax seam. It is plumbing only, not depth. Do not use it as a depth map for a shot.
- **Licence / cost:** Free/open, Apache-2.0.
- **Next gate (needs specific Mars approval, NOT run):** One real Depth Anything Small run on free GPU on JoJo-01, A–B vs proxy; fallback = hand-assigned per-limb depth layers.

### 5. C5 Hallo (hierarchical audio-driven diffusion) — PRODUCTION-UNBLOCKING, audio
- **What it helps:** Dialogue timing end-to-end in a form that ports to a Cape exposure sheet with least translation loss: syllable head motion + frame viseme = exposure-sheet rows.
- **Run vs mapping:** MAPPING ONLY. No Hallo inference ran; needs CUDA + large weights. Source proof is a hierarchical timeline proxy, not Hallo video.
- **Honest proxy limit:** Hallo outputs photoreal video that cannot be pasted into the v7c rig. It is timing/reference only, like every Group C tool: Cape output stays the 14-viseme swap drawings. A GPU run would be timing reference only, never a Cape output.
- **Licence / cost:** Free MIT code; compute/weights are the gate, not a purchase made here.
- **Next gate (needs specific Mars approval, NOT run):** First, a no-GPU method script against a real Cape dialogue audio file to produce a real exposure sheet for one dialogue shot, checked vs visemes v2 — before any GPU run. Runner-ups for pure sync: Wav2Lip (C1); for head-motion curves: SadTalker (C2).

## 3. ALL 25, DEEPENED — one row each: what it helps | run vs mapping | honest proxy limit | next gate (all gates need specific Mars approval; none run here)

### Group A — Interpolation
| # | Project | Tier | What it helps | Run vs mapping | Honest proxy limit | Next gate |
|---|---|---|---|---|---|---|
| A1 | RIFE | Additive | More fps / smoother key transitions (learned intermediate flow) | Proxy only | Same pixel-ghosting as FILM on large cutout jumps; duplicates FILM's job | Free-tier A–B vs FILM proxy, only if FILM gate fails |
| A2 | FILM | **Shot** | Large jumps, wide disocclusion | Proxy only | See §2.1 | Free-tier ginyu-01→ginyu-03 |
| A3 | ToonCrafter | Additive | Exaggerated/non-linear cartoon inbetweens (diffusion + sketch encoder) | Proxy only | Generative cartoon output is not a rig inbetween; checkpoint CC BY-NC — commercial show use must be resolved before any real use | Licence resolution first, then free-tier sketch→inbetween test |
| A4 | EbSynth | Additive | Style/look propagation across a shot (paint one keyframe, propagate) | Proxy only | NOT frame-rate interpolation; Pro/upload path not used, no art uploaded | Paint-one-keyframe propagation test on a locked shot, no upload |
| A5 | RAFT | Additive | Motion measurement under all interpolation; trust scoring (recurrent all-pairs flow) | Proxy only | Measures motion, makes no frame; flow on white-on-white cutouts is unreliable | Flow-vs-joint-angle trust-score comparison on a locked shot |

### Group B — Pose / Motion
| # | Project | Tier | What it helps | Run vs mapping | Honest proxy limit | Next gate |
|---|---|---|---|---|---|---|
| B1 | MediaPipe Pose | **Shot** | Pose reference, joint angles, knee-feet | Installed 1.2.0, inference failed (libEGL) | See §2.2 | libegl1 + 4 frames + 1 performer clip |
| B2 | OpenPose BODY_25 | Additive | Multi-person pose, toe/heel for knee-feet | Proxy only; C++/Caffe build, v1.7.0 (2020) | Licence-gated: free non-commercial only; commercial show needs paid CMU licence — Mars decision before real use; duplicates MediaPipe | Licence decision first, then build/run test |
| B3 | DWPose 133-pt | Additive | Whole-body incl. hands/face for twist/point/lean | Proxy only; MMPose/ONNX checkpoints not downloaded | No inference claimed; duplicates MediaPipe + hand/face detail is already hand-keyframed | Checkpoint + real-frame test, only if MediaPipe hand detail proves insufficient |
| B4 | Cascadeur | Additive | AI-assisted keyframe, AutoPhysics/AutoPosing, weight/balance, mocap cleanup | Proxy only; desktop GUI, no headless run | Free tier non-commercial only; FBX/commercial paid, none bought | Desktop trial decision, then jump/punch balance test |
| B5 | Plask / MoveAI | Additive | Markerless mocap retargeted to 2D cutout rig | Proxy only; both need account + video upload | Plask free 15s/day then ~$18/mo; MoveAI free 30 credits then ~$18/mo; no account, no payment; performer-clip MediaPipe may make both unnecessary | Performer-clip test first; account/payment decision only if that fails |

### Group C — Lip-sync / Audio
| # | Project | Tier | What it helps | Run vs mapping | Honest proxy limit | Next gate |
|---|---|---|---|---|---|---|
| C1 | Wav2Lip | **Audio** | Lip-sync timing, dialogue shots incl. CJ-26 (mel + masked face + SyncNet) | Proxy only (viseme timeline) | Timing only; photoreal output cannot be pasted into rig; commercial Sync successor paid, not used | Audio→viseme timeline for one dialogue shot, checked vs visemes v2 |
| C2 | SadTalker | **Audio** | Audio-driven head motion + expression; mouth stays Cape viseme swap | Proxy only (head-motion) | Head-motion curves only; mouth is not SadTalker output | Head-motion curve for one dialogue shot, viseme mouth overlaid by hand |
| C3 | LivePortrait | Additive | Head/expression reference from a DRIVING VIDEO | Proxy only | NOT audio lip-sync; needs an acted driving video that does not yet exist | Only if a driving video is acted/recorded first |
| C4 | EMO (Alibaba) | Additive | Expressive dialogue/singing timing, 2-frame viseme holds (audio→video diffusion) | Proxy only | Research paper free; no hosted free generation interface confirmed; duplicates Hallo/Wav2Lip timing | Confirm a free interface, or drop in favour of Hallo/Wav2Lip |
| C5 | Hallo | **Audio** | Dialogue timing end-to-end, syllable head + frame viseme | Proxy only | See §2.5 | Exposure-sheet script first, then GPU timing reference only |

### Group D — Effects / Depth / Style
| # | Project | Tier | What it helps | Run vs mapping | Honest proxy limit | Next gate |
|---|---|---|---|---|---|---|
| D1 | ControlNet depth/lineart | **Shot** | Re-render/re-light a locked pose for L0–L5 / Sunbeam / afterglow without redrawing | Proxy only; model NOT run | Conditioning, not a character generator; needs a good depth map (D5) to work well; output is not a locked rig frame | Depth-map (D5) first, then locked-pose relight test |
| D2 | Style2Paints V4 | Additive | Colourisation reference for a new flat pass; hand repaint only | Workflow-demo only | Reference only; flat pass is still hand-painted | Colour-reference test on one new flat pass |
| D3 | Anime2Sketch | Additive | Recover clean lineart from a coloured frame for re-flatting / ControlNet-lineart | Proxy only (edge + XDoG) | Learned GAN not run; edge proxy is not learned lineart | Real-model lineart test on one coloured frame, A–B vs XDoG proxy |
| D4 | Natron | Additive | Free node compositor (Read→Grade→Rim→Merge→Write), auditable graph | Proxy only in PIL; binary NOT run | Upstream community/Qt5-era (FreeBSD port expired 2026-09-30); Qt6/Cycles fork is Windows-only and self-described vibe-coded — do not adopt sight-unseen; Blender compositor already renders, so Natron is an alternative, not a blocker | Natron-vs-Blender A–B still owed; fork review before any adoption |
| D5 | Depth Anything / MiDaS | **Shot** | Per-limb relative depth for parallax, ordering, rim/wrap falloff | Pseudo-depth proxy only | See §2.4 — weakest proxy in the set | Depth Anything Small on JoJo-01 |

### Group E — Rig / Labelling / Editing
| # | Project | Tier | What it helps | Run vs mapping | Honest proxy limit | Next gate |
|---|---|---|---|---|---|---|
| E1 | SAM 2 | **Shot** | Piece segmentation/labelling for FLA top-5 + hand library | Synthetic proxy only | See §2.3 | Real rig frame, mask vs hand-traced truth |
| E2 | Grounding DINO | **Shot** | Hand/piece detection by words, no retraining; boxes feed SAM 2 | Proxy only (4 boxes, no scores faked) | See §2.3 | Real rig frame, boxes vs hand-labelled boxes |
| E3 | MotionDiffuse | **Storyboard** | Motion REFERENCE for dance/fight, never shipped footage (text→motion diffusion) | Proxy only (6 prompts → 6 parametric poses + CSV) | Reference poses, not shipped footage; text prompts do not encode Cape joint limits | Prompt→pose reference sheet for one dance/fight beat, hand-keyframed after |
| E4 | Animate Anyone | **Storyboard** | Pose-driven timing preview, then hand-keyframe the real rig (ReferenceNet) | Proxy only (12 frames → real MP4 via ffmpeg, not the model) | Preview only; needs SD weights + CUDA in practice; output is not a rig shot | Pose-sequence timing preview for one shot, then hand-keyframe |
| E5 | Olive | Additive | Open-source NLE for dance/fight sequences | Proxy only (real ffmpeg edit, NOT Olive GUI — headless, 0.2 alpha) | Editor alternative, not a blocker: ffmpeg editing already exists in this pipeline | GUI edit test only if a GUI NLE is ordered |

## 4. COUNTS — RECONCILED, NO DOUBLE-COUNTING

| Measure | Count | % |
|---|---|---|
| Researched | 25/25 | 100% |
| Vendor-proven (tool ran) | 0/25 | 0% |
| Method-wired, labelled proxy | 25/25 | 100% |
| README-only, no method wired | 0/25 | 0% |
| Deepened in this task | 25/25 | 100% |
| Production-unblocking | 11/25 | 44% |
| Additive/extra | 14/25 | 56% |
| Next gates run in this task (GPU/paid) | 0/25 | 0% |
| Next gates awaiting specific Mars approval | 25/25 | 100% |
| Groups fully deepened | 5/5 (A, B, C, D, E) | 100% |
| Mars approval of this set | 0/1 | 0% — NOT claimed approved |

**Top-5 proof for this task:** the deepened contact sheet in this folder is a labelled diagram of the five unblocking methods and their proxy limits — it is NOT a vendor output, and it does not upgrade any project's status from proxy to proven. The status change this task actually makes is triage + depth, not vendor proof.

## 5. STILL OWED / BLOCKED — EXPERIMENTAL

- Vendor runs: 25/25 still owed, all gated on specific Mars approval (GPU/paid/hosted). No run is smuggled in as a proxy.
- Licence decisions before real use: OpenPose commercial licence, ToonCrafter CC BY-NC commercial use, Cascadeur/Plask/MoveAI paid tiers, EbSynth Pro/upload path, Natron fork review. Count: 5 licence/decision items across the 25 (OpenPose, ToonCrafter, Cascadeur, Plask/MoveAI counted as one mocap decision, EbSynth) + 1 fork review (Natron) = 6 decisions owed.
- LibEGL fix for MediaPipe: free local fix, still owed (not attempted as an install in this task to keep the task free/local-only and to avoid claiming a fix that was not verified).
- No Kaggle run, no Colab run, no paid run, no other-account use. FMMG account not used and not needed for this deliverable.
