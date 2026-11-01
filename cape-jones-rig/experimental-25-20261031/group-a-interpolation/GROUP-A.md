# GROUP A — Interpolation (Cape Jones v7c rig) — 2026-10-31

**Scope:** 5 projects. **No repo push made.** No file Mars has seen was overwritten — all outputs are new
dated 20261031 files in this folder. No base art was recoloured in place: the EbSynth proof's painted
stroke lives on a separate layer (saved alone as `ebsynth-proxy-painted-stroke-layer-only-20261031.png`)
and is only composited over the warped base. No show character is shipped, no dialogue, no logo.
**Mars approval: 0/1 — nothing here is claimed approved.**

## Honest headline (read this first)

**0 of 5 original tools ran on this VM, 5 of 5 methods are method-wired and viewed.**
Reason, same for the four neural tools: this VM has **no GPU** (`nvidia-smi` not found), **no PyTorch**,
and 7.7 GB RAM. RIFE / FILM / RAFT need PyTorch + pretrained weights (+ CUDA for practical use);
ToonCrafter needs ~16–26 GB VRAM and a ~5 GB diffusion checkpoint. EbSynth is different: it has no
Linux CLI — it is a Windows/macOS desktop tool, now also a browser v2 that uploads video/keyframes to
its servers (Pro needed for PNG-sequence / high-res output) — so it was not run and no Cape art was
uploaded to a third party. **Nothing below is labelled as the tool itself running.** Every proof is
labelled `-proxy` in its filename and panel text.

The method proxy that *did* run for real, on real Cape frames, is **OpenCV Farnebäck dense optical
flow + bidirectional warp + blend** (free, `opencv-python-headless`, installed in a throwaway venv
that has since been deleted as regenerable; reinstall: `python3 -m venv venv && venv/bin/pip install
opencv-python-headless numpy pillow`, then run `interpolate_methods.py`). Inputs were downscaled 2×
(1100×1500 → 550×750) for CPU speed.

**Key finding from viewing the proofs:** pixel-flow warping ghosts/doubles on large Cape pose
changes (see RIFE/FILM/ToonCrafter mids — limbs double because white limbs on a white background
carry almost no texture, and cutout parts move rigidly, not as a pixel warp). Pixel interpolation is
therefore a *smoothing* aid for small inter-key motion, not a replacement for rig-part inbetweening
(joint-angle interpolation between pose keys) on this 2D cutout rig. That is a method result, not a
failure to hide: the ghosting is visible in the proofs.

## Table

| # | Project | What it is / who made it | Experimental method | Exact Cape problem it helps | Free / paid | Wired status | Proof file (in `proofs/`) |
|---|---|---|---|---|---|---|---|
| 1 | RIFE — Real-Time Intermediate Flow Estimation | Neural frame interpolation; Huang, Zhang, Heng, Shi & Zhou, ECCV 2022, arXiv:2011.06294; repo hzwer/Arxiv2020-RIFE / Practical-RIFE, MIT | Learned intermediate-flow estimation: estimate bidirectional flow between two frames, warp both to t, blend; arbitrary-timestep, 2×/4×/8× frame-rate multiplication | **More frames per second / smoother transitions between pose keys** — turn a 4-frame dance/punch clip into 8–16 frames without hand-drawing inbetweens | Free / open (MIT); paid wrappers exist (RIFE-App) — none used, none bought | **Method-wired, NOT proven as RIFE** — Farnebäck flow warp, jojo-01→jojo-02, t=0.5 + 5-frame GIF | `rife-proxy-jojo01-to-jojo02-20261031.png`, `rife-proxy-jojo01-to-jojo02-20261031.gif` (5 frames, 550×750) |
| 2 | FILM — Frame Interpolation for Large Motion | Google Research (+ Univ. of Washington), Reda, Kontkanen, Tabellion, Sun, Pantofaru & Curless, ECCV 2022, arXiv:2202.04901; repo google-research/frame-interpolation, Apache 2.0 | Unified single network, shared-weight multi-scale feature pyramid + scale-agnostic bidirectional motion estimator, Gram-matrix loss to inpaint wide disocclusions; trainable from frame triplets alone, no separate flow/depth net | **Smoother transitions on LARGE pose jumps** — e.g. rollcall→dance-shimmy, jump/flying extremes where limbs travel far between keys and disocclusion is wide | Free / open (Apache 2.0); hosted runs cost (e.g. ~$0.28/run on Replicate) — none used | **Method-wired, NOT proven as FILM** — large-window/5-level Farnebäck warp, ginyu-01→ginyu-03, t=0.5 + 5-frame GIF | `film-proxy-ginyu01-to-ginyu03-20261031.png`, `film-proxy-ginyu01-to-ginyu03-20261031.gif` (5 frames, 550×750) |
| 3 | ToonCrafter — Generative Cartoon Interpolation | Xing, Liu, Xia, Zhang, Wang, Shan & Wong (CUHK, CityU, Tencent AI Lab), arXiv:2405.17933; repo ToonCrafter/ToonCrafter, Apache 2.0 code | Generative (diffusion) interpolation, not correspondence/warping: toon-rectification learning adapts live-action video priors to cartoons, dual-reference 3D decoder restores detail, flexible sketch encoder gives user control over the motion; up to 16 frames at 512×320 in the open build | **Inbetweening exaggerated, non-linear cartoon motion** — the case flow-warping handles worst: squash, anticipation, poses where a limb appears/disappears or occludes, plus sketch-guided control of an inbetween | Free / open research code (Apache 2.0); checkpoint licence reported as CC BY-NC for the public checkpoint, so commercial use of the raw model is restricted — flag for Mars before any show use | **Method-wired, NOT proven as ToonCrafter** — flow warp on cartoon pair jojo-02→jojo-03 + flow-guide arrow panel (guide *concept* only; no diffusion, no invented content) + 5-frame GIF | `tooncrafter-proxy-jojo02-to-jojo03-20261031.png`, `tooncrafter-proxy-guide-20261031.png`, `tooncrafter-proxy-jojo02-to-jojo03-20261031.gif` |
| 4 | EbSynth — style transfer / video stylization from keyframes | Ondřej Jamriška & Šárka Sochorová, Secret Weapons / Czech Technical University + Adobe Research lineage; paper "Stylizing Video by Example"; ebsynth.com | Example-based (patch/texture) synthesis, NOT a neural net: paint/edit one keyframe, EbSynth propagates that painted appearance across the whole sequence by patch matching against the source frames | **Style/look propagation across a shot, not frame-rate** — paint one pose key (e.g. a rim/glow/painted finish) and carry it through every inbetween instead of repainting each frame; also rotoscope/retouch propagation | **Free beta / freemium** — free download for Windows/macOS, free for commercial use in beta per contemporary reports; current v2 is browser-based with a Free plan and a Pro plan for high-res/PNG-sequence/priority; final professional version was flagged as paid — **no purchase made, no account created** | **Method-wired, NOT proven as EbSynth** — amber painted stroke on a *separate* layer, warped by the same flow field and composited over the flow-warped dance mid; layer also saved alone | `ebsynth-proxy-dance01-to-dance13-20261031.png`, `ebsynth-proxy-painted-stroke-layer-only-20261031.png` |
| 5 | RAFT — Recurrent All-Pairs Field Transforms for Optical Flow | Zachary Teed & Jia Deng, Princeton, ECCV 2020 (Best Paper), arXiv:2003.12039; repo princeton-vl/RAFT | Deep optical flow: per-pixel features, multi-scale 4D correlation volumes for all pixel pairs, recurrent unit iteratively refining the flow field by correlation lookup; state-of-the-art on KITTI/Sintel at publication | **The measurement underneath all the others** — accurate per-pixel motion between pose keys: drives warp quality, detects large/disoccluded regions, and can score whether an inbetween is trustworthy (flow magnitude / consistency) | Free / open research code | **Method-wired, NOT proven as RAFT** — Farnebäck flow for ginyu-01→ginyu-02, shown as an HSV flow map (hue = direction, brightness = magnitude) + warped mid | `raft-proxy-flow-ginyu01-to-ginyu02-20261031.png`, `raft-proxy-warped-mid-20261031.png` |

**Counts:** 5/5 researched with sources · 0/5 original tools run (hardware/OS reasons above, stated
plainly, not hidden) · 5/5 method-wired with a viewed proof · 0/5 claimed as the tool itself ·
0 paid installs/purchases · 0 repo pushes · Mars approval 0/1.

## What was actually run, and what each proof shows (viewed 2026-10-31)

All proofs were opened and viewed in this session. Inputs are real Cape v7c frames:
`pose-dialects-20261031/` (jojo/ginyu poses) and `clips-v7c/dance/` (dance-01-a, dance-13-b).
Flow statistics (550×750, Farnebäck proxy — *proxy* numbers, not RAFT/RIFE benchmarks) are in
`method-proxy-stats-20261031.json`:

| Proxy pair | Mean flow | p90 flow | Max flow | % pixels >20 px |
|---|---|---|---|---|
| RIFE proxy jojo-01→jojo-02 | 2.18 px | 6.86 px | 69.49 px | 3.2% |
| FILM proxy ginyu-01→ginyu-03 | 2.90 px | 11.61 px | 143.57 px | 3.9% |
| RAFT proxy ginyu-01→ginyu-02 | 2.09 px | 7.48 px | 43.70 px | 3.1% |
| ToonCrafter proxy jojo-02→jojo-03 | 2.32 px | 6.77 px | 61.25 px | 4.6% |
| EbSynth proxy dance-01-a→dance-13-b | 2.35 px | 9.69 px | 55.23 px | 2.1% |

- **RIFE proxy:** mid frame is recognisably between the two JoJo poses (torso/cape land mid-way),
  but arms/legs ghost — two faint limb positions instead of one clean limb. Usable as an onion-skin /
  timing guide, not as a shippable inbetween at this pair distance.
- **FILM proxy:** largest motion of the group (max 143.57 px, p90 11.61 px) and the worst ghosting —
  exactly the large-motion/disocclusion problem FILM's Gram loss is designed for, and exactly what a
  classical warp cannot invent. This proof *demonstrates the gap* FILM/ToonCrafter would need to close.
- **RAFT proxy:** the HSV flow map is sparse and edge-only: white limbs on white background give the
  flow estimator almost no texture to track, so most of the body is black (no flow) and only outlines/
  high-contrast regions colour up. Lesson: for Cape, flow should be computed on rig/part masks or
  edge maps, not raw RGB, or it will under-measure body motion.
- **ToonCrafter proxy:** same ghosting as RIFE, plus the guide panel shows flow arrows only where
  motion is strong — a sketch/guide layer can steer *where* motion goes, but a warp cannot invent a
  limb that is occluded in one key and visible in the other. That invented-content case is
  ToonCrafter's claimed advantage and remains unproven here (needs GPU diffusion).
- **EbSynth proxy:** the amber sash stroke survives onto the mid frame and follows the warped body
  (stroke layer composited, base untouched — layer file proves separation). The red dots visible in
  the dance frames are in the source dance frames themselves, not added by this task. Propagation
  works as a *mechanism*; EbSynth's patch-matching quality on painted texture is not proven by a
  flat-colour stroke and should not be claimed.

## Most promising project in this group

**FILM — with ToonCrafter a close second, for different jobs.**

- **Why FILM first:** Cape's hardest interpolation cases are *large* pose jumps (fight/flying/dance
  extremes), which is FILM's named problem, and it is free/open (Apache 2.0), single-network, and
  needs no separate flow/depth model — the simplest of the neural tools to wire when a GPU lane
  (Kaggle/Colab, per the free-way-around rule) is available. It directly targets "more frames per
  second + smoother transitions" for the existing rig, without changing the character or style.
- **Why ToonCrafter second:** it is the only one in the group built for *cartoon* motion specifically
  (exaggerated, non-linear, disoccluding) and the only one offering sketch control of an inbetween —
  both are Cape-native needs. It ranks second only because it is the heaviest (diffusion, 16–26 GB
  VRAM, ~5 GB checkpoint, non-commercial checkpoint licence to resolve) and therefore the furthest
  from a same-day GPU-free run.
- **Why not RIFE first:** excellent and lightest/fastest for small motion, but Cape's value is in
  the large jumps where RIFE's flow-warp approach ghosts the same way the proxy does.
- **Why not RAFT/EbSynth first:** RAFT is infrastructure (it *measures* motion; it does not itself
  make a frame), and EbSynth solves look-propagation, not frame-rate — both are supporting tools,
  and EbSynth's current browser/upload + Pro-gated PNG path needs a Mars decision before any real
  Cape art goes near it.

**Recommended next step (needs Mars / parent decision, not done here):** run the real FILM model
once on a GPU lane (Kaggle/Colab free tier) on the same ginyu-01→ginyu-03 pair, and compare its mid
frame side-by-side against `film-proxy-ginyu01-to-ginyu03-20261031.png`. That single A/B is the
honest gate for adopting any neural interpolator on this rig. Until then, use the proxy only as a
timing/onion-skin guide, and keep rig-part (joint-angle) inbetweening as the primary method.

## Files in this folder

- `GROUP-A.md` (this file)
- `interpolate_methods.py` — the proxy that actually ran (OpenCV Farnebäck + warp + blend + EbSynth
  separate-layer propagation); rerun after reinstalling opencv/numpy/pillow in a venv
- `method-proxy-stats-20261031.json` — flow statistics for the five proxy pairs
- `proofs/` — 11 files: 5 main contact PNGs + 2 extra panels (RAFT warped mid, ToonCrafter guide) +
  1 EbSynth layer-only PNG + 3 five-frame GIFs (RIFE, FILM, ToonCrafter), all 550×750, all viewed

## Sources

- RIFE: Huang et al., "Real-Time Intermediate Flow Estimation for Video Frame Interpolation",
  ECCV 2022, arXiv:2011.06294; open-source repo hzwer/Arxiv2020-RIFE (MIT); overview at
  https://llmbook.icsgen-ai.org/part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html
  and https://raw.githubusercontent.com/lj1995-computer-vision/arXiv2020-RIFE/main/README.md
- FILM: Reda et al., "FILM: Frame Interpolation for Large Motion", ECCV 2022, arXiv:2202.04901;
  Google Research page https://research.google/pubs/film-frame-interpolation-for-large-motion/ ;
  paper text at https://ar5iv.labs.arxiv.org/html/2202.04901 ; repo google-research/frame-interpolation
  (Apache 2.0); hosted-run pricing note from https://replicate.com/zsxkib/film-frame-interpolation-for-large-motion
- ToonCrafter: Xing et al., "ToonCrafter: Generative Cartoon Interpolation", arXiv:2405.17933,
  https://arxiv.org/html/2405.17933v1 ; project page doubiiu.github.io/projects/ToonCrafter;
  repo ToonCrafter/ToonCrafter (Apache 2.0 code); GPU/VRAM and 512×320/16-frame figures from
  https://www.blog.brightcoding.dev/2025/09/14/from-still-to-story-how-tooncrafter-uses-ai-to-turn-cartoons-into-living-animation
  and https://aipure.ai/products/tooncrafter-ai
- EbSynth: Jamriška & Sochorová, "Stylizing Video by Example" lineage, Secret Weapons;
  https://ebsynth.com/?ref=futureen (free plan, Pro for high-res/PNG output, browser v2 uploads);
  beta/free-commercial-use history at
  https://www.cgchannel.com/2020/08/free-tool-ebsynth-turns-video-into-hand-painted-animation/?fbclid=IwAR0K0kWcJhfnwBx-8Dt9TC5NnJCQdG39gzWZRGAPrh412GCDc06rw5-pm2g
  and https://github.com/jamriska/ebsynth (Windows binary, example-based synthesis, no neural net)
- RAFT: Teed & Deng, "RAFT: Recurrent All-Pairs Field Transforms for Optical Flow", ECCV 2020,
  arXiv:2003.12039, https://arxiv.org/abs/2003.12039v2 and
  https://link.springer.com/chapter/10.1007/978-3-030-58536-5_24 ; repo princeton-vl/RAFT

## Guardrails honoured

- No repo push. No paid install/purchase/account. No upload of Cape art to any third-party service.
- No recolouring of base art in place; EbSynth effect is a separate layer, saved alone.
- No overwrite of any file Mars has seen; every output is a new 20261031-dated file.
- No tool is claimed to have run when only its method was implemented; every proof filename and
  panel says `-proxy` / `NOT <Tool>`.
