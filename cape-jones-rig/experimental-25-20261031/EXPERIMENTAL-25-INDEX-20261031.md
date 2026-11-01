# 25 EXPERIMENTAL PROJECTS — Index (Mars, 2026-10-31)
## Status plainly
- 25/25 researched with sources in group docs. 0/25 vendor tools actually ran on this VM (no GPU, no PyTorch, headless, missing libEGL, PEP 668 pip blocks — reasons per group). 25/25 method-wired with viewed proofs (PIL/OpenCV/FFmpeg proxies, labelled as proxies, never claimed as vendor output). 0/25 README-only. 0 repo pushes. Mars approval: 0/1 for the whole set.
- Scope: 2D Cape Jones first; 2.5D/3D effects only as perspective-bending flavour; 3D-side notes are separate. No show character shipped, no dialogue, no logo, base art never recoloured in place, no file Mars saw overwritten.
- Mainstream standards already wired (Harmony, Animate, Blender, OpenToonz/Tahoma2D, Godot, Spine, Ruffle, OpenCV, CLIP) do NOT count toward the 25, except where a group explicitly notes an experimental fork/branch — none is counted that way here.

## Counts
- Wired-and-proven (vendor tool ran): 0/25 = 0%
- Method-wired (method implemented free + viewed proof): 25/25 = 100%
- Cannot-run, no method wired: 0/25 = 0%
- Free/open: 25/25 researched as free/open code (paid tiers/wrappers noted, none bought, no accounts created for paid tools)
- Groups: A 5/5, B 5/5, C 5/5, D 5/5, E 5/5

## Group A — Interpolation (group-a-interpolation/GROUP-A.md)
| # | Project | Method | Cape problem | Free/paid | Status | Proof |
|---|---|---|---|---|---|---|
| A1 | RIFE (Huang et al., ECCV 2022) | Learned intermediate-flow interpolation | More fps / smoother key transitions | Free/open, paid wrappers not used | Method-wired | proofs/rife-proxy-jojo01-to-jojo02-20261031.png |
| A2 | FILM (Google, Reda et al., ECCV 2022) | Scale-agnostic single-network interpolation, Gram loss | Large pose jumps, wide disocclusion | Free/open Apache 2.0 | Method-wired | proofs/film-proxy-ginyu01-to-ginyu03-20261031.png |
| A3 | ToonCrafter (CUHK/CityU/Tencent, 2024) | Generative diffusion cartoon interpolation + sketch encoder | Exaggerated/non-linear cartoon inbetweens | Free research code; checkpoint CC BY-NC (commercial use to resolve) | Method-wired | proofs/tooncrafter-proxy-jojo02-to-jojo03-20261031.png |
| A4 | EbSynth (Jamriska & Sochorova) | Example-based patch synthesis, paint one keyframe, propagate | Style/look propagation across a shot, NOT frame-rate | Free beta/freemium; Pro/upload path not used, no art uploaded | Method-wired | proofs/ebsynth-proxy-dance01-to-dance13-20261031.png |
| A5 | RAFT (Teed & Deng, Princeton, ECCV 2020) | Recurrent all-pairs optical flow | Motion measurement under all interpolation; trust scoring | Free/open research code | Method-wired | proofs/raft-proxy-flow-ginyu01-to-ginyu02-20261031.png |
Key finding: pixel-flow warping ghosts/doubles on large Cape pose changes (white-on-white, rigid cutout parts). Pixel interpolation = timing/onion-skin aid for small motion, NOT a replacement for rig-part joint-angle inbetweening.

## Group B — Pose / Motion (group-b-pose-motion/GROUP-B.md)
| # | Project | Method | Cape problem | Free/paid | Status | Proof |
|---|---|---|---|---|---|---|
| B1 | MediaPipe Pose / BlazePose, 33 pts (Google) | Pose estimation | Pose reference, elbow/knee/shoulder/hip angles, knee-feet, foot turnout | Free Apache-2.0 | Method-wired (1.2.0 installed, inference failed: libEGL missing) | proofs/proof-01-mediapipe-jojo01-overlay-20261031.png |
| B2 | OpenPose BODY_25 (CMU) | Multi-person pose, up to 135 pts | Multi-figure shots, toe/heel for knee-feet | Free non-commercial only; commercial show needs paid CMU licence | Method-wired (C++/Caffe build, v1.7.0 2020, licence-gated) | proofs/proof-02-openpose-ginyu02-squat-overlay-20261031.png |
| B3 | DWPose, 133-pt whole-body (IDEA, ICCV 2023) | Whole-body pose incl. hands/face | Hand/face detail for twist/point/lean | Free/open | Method-wired (MMPose/ONNX checkpoints not downloaded, no inference claimed) | proofs/proof-03-dwpose-jojo02-twist-overlay-20261031.png |
| B4 | Cascadeur (Nekki) | AI-assisted keyframe animation, AutoPhysics/AutoPosing | Weight/balance inbetweens, jump/punch/dance, mocap cleanup | Free tier non-commercial only; FBX/commercial paid, none bought | Method-wired (desktop GUI, no headless run) | proofs/proof-04-cascadeur-method-ginyu02-balance-20261031.png |
| B5 | Plask (primary) / MoveAI (compared) | Markerless motion capture | Dance/motion capture retargeted to 2D cutout rig | Plask free 15s/day then ~$18/mo; MoveAI free 30 credits then ~$18/mo; no account, no payment | Method-wired (both need account + video upload) | proofs/proof-05-plask-moveai-ginyu03-dance-retarget-20261031.png |
By-eye tolerance stated everywhere: ±10–15°, good to flag a pose, not to lock a rig joint.

## Group C — Lip-sync / Audio (group-c-lipsync-audio/GROUP-C.md)
| # | Project | Method | Cape problem | Free/paid | Status | Proof |
|---|---|---|---|---|---|---|
| C1 | Wav2Lip | Mel-spectrogram + masked face generator, SyncNet discriminator | Lip-sync timing, dialogue shots incl. CJ-26 | Free/open (commercial Sync successor paid, not used) | Method-wired | proofs/01-wav2lip-viseme-timeline.png |
| C2 | SadTalker | Audio → 3DMM coefficients (ExpNet + PoseVAE) → render + blinks | Audio-driven head motion + expression; mouth stays Cape viseme swap | Free Apache 2.0 | Method-wired | proofs/02-sadtalker-head-motion.png |
| C3 | LivePortrait (KwaiVGI) | Implicit-keypoint retargeting from a DRIVING VIDEO | Head/expression reference ONLY if acted driving video exists; NOT audio lip-sync | Free/open; hosted wrappers sell credits, not used | Method-wired, proxy only | proofs/03-liveportrait-retarget.png |
| C4 | EMO, Alibaba | Direct audio-to-video diffusion, ReferenceNet + audio encoder | Expressive dialogue/singing timing, 2-frame viseme holds | Research paper free; no hosted free generation interface confirmed | Method-wired | proofs/04-emo-expression-timeline.png |
| C5 | Hallo | Hierarchical audio-driven diffusion, coarse motion + fine lip detail | Dialogue timing end-to-end: syllable head motion + frame viseme = exposure sheet rows | Free MIT code; needs CUDA + large weights to run | Method-wired | proofs/05-hallo-hierarchical-timeline.png |
Verdict: all 5 are reference/timing ONLY, never a direct Cape output (Cape = 14 viseme swap drawings; these output photoreal video that cannot be pasted into v7c rig).

## Group D — Effects / Depth / Style (group-d-effects-depth-style/GROUP-D.md)
| # | Project | Method | Cape problem | Free/paid | Status | Proof |
|---|---|---|---|---|---|---|
| D1 | ControlNet, depth/lineart (Zhang et al., Stanford 2023) | Conditioning, not a character generator | Re-render/re-light a locked pose for L0–L5/Sunbeam/afterglow without redrawing | Free/open | Method-wired, model NOT run | proofs/01-controlnet-conditioning-pack-20261031.png |
| D2 | Style2Paints V4 (Zhang) | Lineart + colour hints → flat fill → shading | Colourisation reference for a new flat pass; hand repaint only | Free/open code, GPU build free | Method-wired, workflow-demo only | proofs/02-style2paints-method-reference-20261031.png |
| D3 | Anime2Sketch (Xiang et al. 2021, MIT) | Learned GAN colour→lineart extraction | Recover clean lineart from coloured frame for re-flatting / ControlNet-lineart | Free MIT | Method-wired (edge + XDoG proxy) | proofs/03-anime2sketch-line-extraction-proxy-20261031.png |
| D4 | Natron (Gauthier 2012, GPL-2.0) | Node compositor: Read → Grade → Rim → Merge → Write | Free compositor for rim/wrap/glow, auditable graph | Free/open | Method-wired in PIL, binary NOT run | proofs/04-natron-node-graph-20261031.png, proofs/04-natron-composite-proof-20261031.png |
| D5 | MiDaS / Depth Anything (Ranftl 2020; Yang 2024, Apache-2.0) | Single frame → relative depth map | Depth for 2.5D parallax, layer ordering, rim/wrap falloff | Free/open | Method-wired (silhouette-distance pseudo-depth) | proofs/05-midas-depthanything-pseudo-depth-20261031.png |
Caveats: Natron upstream is community/Qt5-era (FreeBSD port expired 2026-09-30); Qt6/Cycles fork is Windows-only and self-described vibe-coded — do not adopt sight-unseen; Natron-vs-Blender A–B still owed. Depth proxy is weakest (torso bright, thin limbs dark — opposite of true body-part depth; parallax seam visible) — plumbing only, not depth.

## Group E — Rig / Labelling / Editing (group-e-rig-labelling-editing/GROUP-E.md)
| # | Project | Method | Cape problem | Free/paid | Status | Proof |
|---|---|---|---|---|---|---|
| E1 | SAM 2 (Meta) | Promptable segmentation, image+video, click/box/mask → mask | Piece segmentation/labelling for FLA top-5 + hand library | Free Apache 2.0 | Method-wired proxy (point → head mask 9,009 px, synthetic figure, NOT Cape art) | proofs/01-sam2-proxy_synthetic-cutout-20261031.png |
| E2 | Grounding DINO (IDEA/Tsinghua/Microsoft) | Open-vocabulary detection: words → boxes | Hand/piece detection by words, no retraining; boxes feed SAM 2 | Free/open | Method-wired proxy (4 boxes, no weights/scores faked) | proofs/02-grounding-dino-proxy_boxes-20261031.png |
| E3 | MotionDiffuse (Zhang et al., NTU) | Text-to-motion diffusion, DDPM + cross-modality transformer | Motion REFERENCE for dance/fight, never shipped footage | Free research code | Method-wired proxy (6 prompts → 6 parametric poses + CSV) | proofs/03-motiondiffuse-proxy_keyframes-v2-20261031.png |
| E4 | Animate Anyone (Alibaba, primary); MagicAnimate compared-only | Reference image + pose sequence → video, ReferenceNet | Pose-driven timing preview, then hand-keyframe the real rig | Free research code (needs SD weights + CUDA in practice) | Method-wired proxy (12 frames → real MP4, ffmpeg-verified) | proofs/04-animate-anyone-proxy_pose-driven-20261031.mp4 |
| E5 | Olive (olive-editor) | Open-source NLE, C++/Qt, FFmpeg, node compositing | Editing pipeline for dance/fight sequences | Free GPL v3.0 | Method-wired proxy (real ffmpeg edit, NOT Olive GUI — headless, 0.2 alpha) | proofs/05-olive-proxy_edited-dance-fight-20261031.mp4 |

## Top 5 overall (ranked)
1. **FILM (A2)** — Cape's hardest inbetweening cases are exactly its named problem (large jumps, wide disocclusion), free Apache 2.0, single network, no style/character change. Next gate: one real FILM run on Kaggle/Colab free tier on ginyu-01→ginyu-03, A–B vs proxy.
2. **MediaPipe Pose (B1)** — free commercial use (unlike OpenPose), CPU-runnable, one-pip install, 33-pt schema maps 1:1 onto v7c joints; cheapest on-ramp to mocap (if it works on a phone dance clip, paid Plask/MoveAI may be unnecessary). Next gate: install libegl1, run Pose Landmarker on 4 pose frames + 1 real phone dance clip, report detector-vs-by-eye delta; if it fails on cutout art, run on performer and retarget, never on cartoon.
3. **SAM 2 + Grounding DINO pair (E1+E2, counted as two projects, one workflow)** — only workflow that directly removes the FLA piece segmentation/labelling bottleneck, free, slots into existing pipeline without shipping generated footage. Next gate: one free-GPU run on a real rig frame, mask vs hand-traced ground truth, before batch labelling is trusted.
4. **Depth Anything / MiDaS (D5)** — only route to per-limb relative depth from one frame for 2.5D parallax, ordering, depth-graded rim/wrap; ControlNet needs that depth map to work well. Next gate: one real Depth Anything Small run on free GPU on JoJo-01, A–B vs proxy; fallback if thin limbs fail = hand-assigned per-limb depth layers.
5. **Hallo (C5)** — hierarchical coarse+fine structure ports to a Cape exposure sheet with least translation loss (syllable head motion + frame viseme). Runner-ups: Wav2Lip for pure sync timing, SadTalker for head-motion curves. Next gate: run method script against a real Cape dialogue audio file to produce a real exposure sheet for one dialogue shot, checked vs visemes v2, before any GPU run — GPU run would be timing reference only, never a Cape output.

## Honest limits (whole set)
- 0/25 vendor tools ran: no GPU, no PyTorch, headless VM, libEGL missing, PEP 668 pip blocks, desktop-GUI tools with no headless run, paid/account-gated tools not bought/created. Every proof is therefore a method proxy, labelled as such in group docs — do NOT quote any proxy as a vendor result.
- Pixel interpolation ghosts on large cutout jumps; pose detectors are unproven on cutout art (likely out-of-distribution — run on performer, retarget); lip-sync tools are timing-only; depth proxy inverts thin-limb depth; Natron fork and ToonCrafter licence need resolution before adoption; OpenPose commercial licence, Cascadeur/Plask/MoveAI paid tiers, EbSynth upload/Pro path all need Mars decisions before any real use.
- No repo push in this task. Mars approval of the experimental set: 0/1.
