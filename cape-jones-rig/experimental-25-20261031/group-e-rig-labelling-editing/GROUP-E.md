# Group E — Rig, Labelling & Editing — 25 Experimental Projects (Cape Jones)

**Folder:** `~/workspace/cape-jones-rig/experimental-25-20261031/group-e-rig-labelling-editing/`
**Date:** 2026-10-31 · **Pushed to any repo: NO** (per task) · **Mars approval: 0/1 — NOT approved, do not claim approved**
**No show character shipped.** All proofs use one synthetic flat-colour cutout figure
(head / torso / arms / hands / legs / feet, 10 parts), drawn for this task only.
It is NOT Cape Jones art and NOT a likeness of any show character.

## Count — stated plainly

**Exactly 5 counted projects:** 1 SAM 2, 2 Grounding DINO, 3 MotionDiffuse,
4 Animate Anyone, 5 Olive.
**Compared-only, NOT counted:** MagicAnimate (compared under #4).
**Pipeline note, NOT an extra count:** SAM 2 + Grounding DINO are documented as a
detection → segmentation pair (Grounding DINO finds the box from words, SAM 2
cuts the mask from that box), but each is counted once above. Counting the pair
itself as a sixth slot would make 6 — that is NOT what this table does.
Total counted = 5/5, not 6.

## Honest wiring status — read this first

**No original model weights ran in this group.** Reason, verified on this VM:
no GPU (`nvidia-smi` not found), no `torch`, no `cv2` (pip blocked by PEP 668
system-package protection; not overridden), headless VM. SAM 2, Grounding DINO,
MotionDiffuse and Animate Anyone checkpoints are large GPU models; running them
honestly here was not possible, and no paid run / paid install was made.
Olive's GUI also did not run here (headless VM; Olive 0.2 is an alpha rewrite).

So every row below is **(b) method-wired, free**: a PIL / NumPy / FFmpeg
implementation of that project's *interface* (prompt → mask, words → boxes,
text → pose angles, pose sequence → frames, EDL → edited clip) on the synthetic
figure. **Never claim a tool ran if only its method was implemented — none of
these proofs claim the original tool ran.** Every proof image is labelled
PROXY on the image itself, and no fake model scores are shown.
Builder: `build_proofs.py` in this folder. Manifest: `proofs/proof-manifest-20261031.json`.

## Table

| # | Project | Method (what it really does) | Exact Cape problem it helps | Free / paid | Wired status | Proof file (viewed) |
|---|---|---|---|---|---|---|
| 1 | SAM 2 — Segment Anything Model 2, Meta (Meta AI / FAIR) | Promptable segmentation, unified for images + video: a click, box or mask prompt returns a mask, tracked across video frames via a streaming memory module; Hiera backbone. Released 2024-07-29. | Piece segmentation / labelling: click a hand, arm or head in a rig frame and get a clean piece mask for the FLA top-5 labelling pass and the hand library, instead of hand-tracing every piece. | FREE — open source, Apache 2.0; no paid tier from Meta for the model itself, only your own compute | METHOD-WIRED (proxy): prompt point (450,120) in head → exact-colour mask, 9,009 px. On flat synthetic colour this equals the connected component; on real textured art the real SAM 2 would be required. SAM 2 weights did NOT run. | `proofs/01-sam2-proxy_synthetic-cutout-20261031.png` — left: synthetic figure, right: head masked magenta, prompt dot marked. Viewed. |
| 2 | Grounding DINO — IDEA Research / Tsinghua / Microsoft Research (Liu et al., arXiv:2303.05499, 2023) | Open-vocabulary / open-set detection: text (category names or referring expressions) → bounding boxes, by marrying Transformer detector DINO with grounded pre-training. 52.5 AP zero-shot on COCO (paper). | Hand + piece detection by words: prompt "hand", "head", "torso" over rig frames to auto-box pieces for labelling, without retraining a detector per new piece name. Pairs with #1: boxes feed SAM 2 as box prompts. | FREE — open-source code/checkpoints (IDEA-Research/GroundingDINO); compute only | METHOD-WIRED (proxy): 4 text-prompt boxes (head, hand ×2, torso) from labelled synthetic geometry. NO Grounding DINO weights, NO confidence scores invented. | `proofs/02-grounding-dino-proxy_boxes-20261031.png` — boxes + prompt labels over the figure. Viewed. |
| 3 | MotionDiffuse — Zhang et al., S-Lab NTU Singapore (arXiv:2208.15001, 2022; IEEE TPAMI 2024) | Text-to-motion diffusion: DDPM + cross-modality linear transformer; probabilistic (not deterministic) text→motion mapping, body-part-independent control via noise interpolation, arbitrary-length synthesis from time-varied prompts. | Motion REFERENCE for dance / fight: turn a sentence ("raises left arm", "dances, both arms up") into a pose sequence to keyframe against — reference only, never a shipped performance. | FREE — open research code/paper; compute only | METHOD-WIRED (proxy): 6 text prompts → 6 parametric poses (arm angles in CSV). This is a hand-written text→angle table, NOT diffusion sampling; MotionDiffuse weights did NOT run. | `proofs/03-motiondiffuse-proxy_keyframes-v2-20261031.png` (v2: wrapped labels, viewed) + `proofs/03-motiondiffuse-proxy_poses-20261031.csv`. Original v1 had overlapping labels and is superseded by v2. |
| 4 | Animate Anyone — PRIMARY. Hu et al., Alibaba Institute for Intelligent Computing (arXiv:2311.17117, 2023) | Reference image + pose sequence → video via diffusion: ReferenceNet preserves reference appearance via spatial attention, a pose guider drives movement, temporal modelling keeps frames smooth. Built on Stable Diffusion. | Character animation reference: drive a still pose sheet with a dance/fight pose sequence to preview timing before hand-keyframing the cutout rig. Reference only; the diffusion output must NOT replace the rig or ship as show footage. | FREE — open research code; needs SD weights + CUDA GPU in practice (not available here) | METHOD-WIRED (proxy): same reference figure re-posed by arm angles over 12 frames → real MP4 (900×600, 12 frames, 2.0 s, ffmpeg). NOT a diffusion output; Animate Anyone weights did NOT run. | `proofs/04-animate-anyone-proxy_pose-driven-20261031.mp4` + `proofs/04-animate-anyone-proxy_contact-sheet-20261031.png` (12 frames, viewed) + `proofs/frames-animate-anyone-proxy-20261031/`. |
| 4c | MagicAnimate — COMPARED ONLY, not counted | Diffusion human-image animation from one reference image + motion video (DensePose/OpenPose driven), Stable Diffusion v1.5 based, temporally consistent; Show Lab, National University of Singapore + ByteDance (CVPR 2024). | Same job as #4, alternative implementation. | FREE — open source; CUDA + SD 1.5 / VAE weights in practice | NOT wired separately; compared on method only. Known limits reported for it: hand/face distortion, body-proportion shift on stylised characters — both are live risks for a cutout rig, which is why Animate Anyone is the primary and neither is recommended to ship output. | No separate proof; covered by #4's pose-driven proof + this comparison note. |
| 5 | Olive — olive-editor/olive (open-source NLE) | Free open-source non-linear video editor, C++ / Qt, FFmpeg-based, node-based compositing, hardware-accelerated rendering; GPL v3.0. 0.1 alpha was the stable line; 0.2 is a major rewrite (alpha, features being re-implemented — treat as unstable). | Editing pipeline for dance / fight sequences: assemble dance + fight clips on a timeline, cut / crossfade, then export — the step after rig animation, before delivery. | FREE — open source, GPL v3.0; no subscription | METHOD-WIRED (proxy): a real ffmpeg edit, NOT the Olive GUI. Dance clip (12 frames, 2.0 s) + fight clip (6 frames, 1.0 s) → xfade 0.5 s at 1.5 s → 15 frames, 2.5 s. Olive GUI did NOT run (headless VM, alpha). The EDL is written in Olive-timeline form so it can be rebuilt in Olive later. | `proofs/05-olive-proxy_edited-dance-fight-20261031.mp4` (ffprobe-verified: 900×600, 15 frames, 2.5 s) + `proofs/05-olive-proxy_edl-20261031.txt` + `proofs/05-olive-proxy_fight-clip-20261031.mp4`. MP4 frames verified by ffprobe; the contact-sheet method for #4 is the viewed visual check for the same figure. |

## Per-project detail

### 1. SAM 2
- **Who:** Meta AI / FAIR. **What:** first unified image+video promptable
  segmentation model; click/box/mask → mask, propagated through video with
  streaming memory, even through temporary disappearance.
- **Cape use, concrete:** FLA labelling top-5 — click each piece once, take the
  mask, export the piece + label. Hand library — same click per hand pose.
  Next step if Mars approves: run real SAM 2 (tiny checkpoint) on a Kaggle/Colab
  GPU against one real rig frame and compare its mask to this proxy's 9,009 px
  head mask; do not trust the proxy on textured art.
- **Limit:** needs GPU for real-time video; mask quality on cutout edges /
  overlapping pieces is unproven until that GPU run.

### 2. Grounding DINO
- **Who:** Shilong Liu et al., IDEA Research, Tsinghua, HKUST, CUHK Shenzhen,
  Microsoft Research. **What:** open-set detector — language is the class list.
- **Cape use, concrete:** the labelling front-end for #1. Prompt vocabulary
  lives in a text file (head, hand, torso, arm, leg, foot, gauntlet …), not in
  retraining. Its boxes become SAM 2 box prompts — this is the published
  Grounded-Segment-Anything pattern (detection → SAM), which is why the two
  are paired in this group without double-counting.
- **Limit:** boxes only — no mask, no depth, no pose. Prompt/threshold
  sensitivity is the known failure mode; "hand" vs "gauntlet" vs "fist" prompts
  need a tested vocabulary list before any batch labelling.

### 3. MotionDiffuse
- **Who:** Mingyuan Zhang, Zhongang Cai et al., S-Lab, NTU Singapore.
- **Cape use, concrete:** dance/fight REFERENCE. A choreographer writes
  sentences; the model returns joint motion; the animator keys the cutout rig
  to match the timing, keeping the rig's own shapes. The proxy's lesson is
  already visible: a naive text→angle table gives stiff, sometimes wrong
  poses (e.g. "arms up" at −120° reads as crossed) — real diffusion output
  still needs animator cleanup, and is never shipped as-is.
- **Limit:** outputs 3D human joint motion, not 2D cutout pieces; retargeting
  human joints onto a cutout rig is its own step, and hand detail is weak in
  this whole model family.

### 4. Animate Anyone (primary) vs MagicAnimate (compared)
- **Animate Anyone, who:** Li Hu, Xin Gao, Peng Zhang, Ke Sun, Bang Zhang,
  Liefeng Bo, Alibaba Institute for Intelligent Computing.
- **Why primary over MagicAnimate:** ReferenceNet is explicitly designed to
  hold reference appearance detail across frames, which is the exact failure
  (identity/style drift) that matters for a character sheet; MagicAnimate's
  reported hand/face distortion and anime→realism style shift are worse risks
  for a cutout character. Both need a CUDA GPU + SD weights, both are
  reference-only for Cape, neither output ships.
- **Cape use, concrete:** pose-sheet → timing preview for a dance or fight
  beat, then hand-keyframe the real rig to that timing.

### 5. Olive
- **Who:** olive-editor/olive community project. **What:** open NLE aiming at
  a Premiere-class free editor, node compositing, OpenColorIO colour.
- **Cape use, concrete:** the only counted project in this group that produced
  a genuinely edited (cut + crossfaded) sequence file by a real encoder, even
  though via ffmpeg rather than the Olive GUI. EDL in
  `proofs/05-olive-proxy_edl-20261031.txt` is the rebuildable timeline.
- **Limit:** alpha / rewrite instability is the headline risk — do not put a
  deadline edit solely in Olive 0.2 until a full export is proven on a real
  sequence; keep the ffmpeg EDL as the fallback.

## Most promising project — and why

**The SAM 2 + Grounding DINO pair (counted as #1 + #2, not as a sixth slot).**
Why, in one line: it is the only pair that directly removes the group's named
bottleneck — piece segmentation and labelling for the FLA top-5 and the hand
library — with free, permissively licensed, already-published code, and with a
workflow (words → boxes → masks) that slots into the existing rig pipeline
without asking Mars to ship any generated footage or change the character.
MotionDiffuse and Animate Anyone only produce reference that still needs
animator cleanup, and both carry hand/style-drift risk; Olive only edits
footage that does not yet exist at scale. The pair's next step is also the
cheapest to prove: one GPU run on one real rig frame, mask vs hand-traced
ground truth, before any batch labelling is trusted.

## What was NOT done / needs Mars (not decided here)

- No repo push (per task). No paid install, no paid run.
- No real SAM 2 / Grounding DINO / MotionDiffuse / Animate Anyone inference
  (needs a GPU run — Kaggle/Colab free GPU is the standing free-first route;
  needs Mars's go-ahead for that specific run, per the GPU-first rule).
- No Olive GUI run (needs a GUI machine, not this headless VM).
- No approval claimed: **Mars approval 0/1.**
- No file Mars has seen was overwritten: the v2 MotionDiffuse strip is a new
  file; v1 remains in the folder, superseded.

## Sources (public, web search 2026-10-31)

- SAM 2, Meta: https://ai.meta.com/research/sam2/
- SAM 2 paper/project: https://artinte.github.io/deep-learning/segment_anything.html
- Segment Anything overview: https://en.wikipedia.org/wiki/Segment_Anything
- Grounding DINO paper: https://arxiv.org/html/2303.05499v5
- Grounding DINO, grounded-segmentation pipeline (detection → SAM):
  https://deepwiki.com/heshuting555/ReferSplat/3.2-groundingdino-detection-component
- Grounding DINO, NVIDIA TAO overview: https://docs.nvidia.com/tao/tao-toolkit/6.25.11/text/cv_finetuning/pytorch/object_detection/grounding_dino.html
- MotionDiffuse paper: https://ar5iv.labs.arxiv.org/html/2208.15001
- MotionDiffuse record: https://pubmed.ncbi.nlm.nih.gov/38285589/
- Animate Anyone paper: https://arxiv.org/html/2311.17117v2
- MagicAnimate overview: https://www.aitechsuite.com/tools/18057
- MagicAnimate / Animate Anyone star comparison: https://github.locker/topics/video-generation
- Olive overview: https://www.blog.brightcoding.dev/2026/07/19/olive-editorolive-open-source-node-based-video-editor-for-developers
- Olive features / 0.2 rewrite note: https://filmora.wondershare.com/answers/main-features-of-olive-video-editor.html
