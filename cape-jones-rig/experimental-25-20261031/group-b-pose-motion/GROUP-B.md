# GROUP B — Pose & Motion (Cape Jones, v7c rig) — 2026-10-31

**Scope:** 5 project slots. Slot 5 counts once but documents both Plask (primary) and MoveAI (compared), per brief.
**Mars approval: 0/1 — NOT approved. Nothing here is claimed approved.**
**No repo push made. No original file Mars has seen was overwritten. No base art was recoloured.**
Every overlay below is drawn on a NEW copy; the source in `pose-dialects-20261031/` was opened read-only.
No show character is shipped by this work; Cape poses used are the project's own v7c test art.

## Result table

| # | Project | Who made it | Method (experimental) | Exact Cape problem it helps | Free / paid | Wired status | Proof file |
|---|---------|-------------|------------------------|------------------------------|-------------|--------------|------------|
| 1 | MediaPipe Pose (BlazePose) | Google | Single-person pose estimation from RGB video/image; BlazePose infers 33 3D landmarks (shoulders, elbows, wrists, hips, knees, ankles, face, feet) + segmentation mask; CPU-friendly | Pose reference + joint-angle readout for any Cape pose: elbow/knee/shoulder/hip angles, knee-feet alignment, foot turnout — the numbers the v7c rig's knee-feet and arm rules need checked against | Free, open source (Apache-2.0) | **method-wired** — real install attempted, see §1 | `proofs/proof-01-mediapipe-jojo01-overlay-20261031.png` |
| 2 | OpenPose | CMU Perceptual Computing Lab (Cao, Hidalgo, Simon, Wei, Raaj, Joo, Sheikh) | Bottom-up multi-person 2D pose via Part Affinity Fields; BODY_25 = 25 body/foot points, up to 135 with face+hands; runtime ~invariant to person count for body | Multi-figure Cape shots (mirrored pair, towering-behind stands): both figures' skeletons in one frame; foot keypoints (toe/heel) for knee-feet checks | Free for non-commercial use; commercial use needs a paid CMU licence — NOT free for a commercial show | **method-wired** — cannot run honestly here, see §2 | `proofs/proof-02-openpose-ginyu02-squat-overlay-20261031.png` |
| 3 | DWPose | IDEA Research (Yang et al., ICCV 2023 workshop) — distilled RTMPose | Two-stage distillation of a whole-body estimator; 133 points (17 body + 6 foot + 68 face + 21/hand); t/s/m/l sizes, 256×192 or 384×288; drop-in ControlNet preprocessor replacing OpenPose | Whole-body reference where hands + face matter (JoJo twist/point, menacing lean): finger/hand pose and head angle that BlazePose-33 and BODY_25 approximate only coarsely | Free, open source (code + checkpoints public) | **method-wired** — cannot run honestly here, see §3 | `proofs/proof-03-dwpose-jojo02-twist-overlay-20261031.png` |
| 4 | Cascadeur | Nekki (Limassol, Cyprus; Shadow Fight studio) | AI-assisted keyframe animation: AutoPosing (neural pose fill from few controls), AutoPhysics (centre-of-mass / balance / weight correction shown on a green preview twin), inbetweening, Animation Unbaking for mocap cleanup, Video Mocap | Jump / punch / dance inbetweens that obey weight and balance instead of floaty hand-keyed arcs; flagging physically impossible Cape poses before render; cleaning any mocap before retarget | Free tier (non-commercial only, export to .casc only, 300 frames / 120 joints cap reported); paid Indie/Pro needed for FBX/DAE/USD export + commercial use — **no paid plan installed or bought** | **method-wired** — cannot run honestly here, see §4 | `proofs/proof-04-cascadeur-method-ginyu02-balance-20261031.png` |
| 5 | Plask — PRIMARY (MoveAI compared) | Plask (plask.ai) / Move.ai | Markerless motion capture from ordinary video: upload or phone-record, AI extracts full-body (+hand) motion, export FBX/GLB/BVH to Blender/Maya/Unity/Unreal; no suit, no markers | Dance / motion capture for Cape: record a real shimmy, jump or fight move, retarget its joint angles onto the 2D cutout rig instead of hand-posing every frame | Plask: free tier (15 s/day, 1 GB reported) then ~$18/mo Standard / ~$50/mo Pro (annual billing). MoveAI: free tier (30 credits, Move One, 1 person) then from ~$18/mo. **No account created, no paid plan used** | **method-wired** — cannot run honestly here, see §5 | `proofs/proof-05-plask-moveai-ginyu03-dance-retarget-20261031.png` |

**Counts:** 5/5 projects researched and documented; 0/5 proven by running the vendor tool itself; 5/5 method-wired with a viewed overlay + angle readout; 0/5 paid installs.
**Contact sheet (all 5 proofs at a glance):** `proofs/proofs-contact-20261031.png`
**Shared tool:** `pose_angle_tool.py` — angle maths + overlay renderer, detector-agnostic (see its header for the honesty label).
**Raw numbers:** `pose-angles-20261031.json` (regenerated with the proofs).

## What "method-wired" means here, exactly

A detector was NOT run to place the dots. The dots were placed by eye from the viewed Cape frame
(the v7c art's own joint circles mark shoulder/elbow/wrist/hip/knee/ankle, which is why this is
feasible at all). What WAS run, for real, on real Cape frames:

1. `pose_angle_tool.py` computed every angle below from those keypoints (vector maths, no guessing).
2. It ran the knee-feet check (knee x vs ankle x) and the Cascadeur-method balance proxy
   (hip-midpoint COM vs ankle support span) for every pose.
3. It rendered each skeleton on a new copy only.

By-eye tolerance: treat every angle as **±10–15°**. That is good enough to flag a pose
("knee is bent ~85°, not ~125°") and NOT good enough to lock a rig joint. A real detector run
replaces the keypoint JSON and the same script re-runs unchanged — that is the upgrade path,
and it is the only honest next step for any of these five.

## Measured angles (method-wired; L/R = image-left / image-right)

| Pose (source) | Elbow L / R | Knee L / R | Shoulder L / R | Hip L / R | Foot turnout L / R | Knee–ankle offset L / R | COM inside support? |
|---|---|---|---|---|---|---|---|
| jojo-01 contrapposto (MediaPipe proof) | 44.5° / 95.3° | 117.2° / 118.6° | 89.7° / 55.2° | 114.3° / 110.6° | 45.0° / 35.5° | 0.045 / 0.040 | yes, margin 0.167 |
| ginyu-02 squat (OpenPose + Cascadeur proofs) | 62.4° / 62.4° | 84.3° / 84.3° | 93.6° / 93.6° | 101.9° / 101.9° | 26.6° / 26.6° | 0.120 / 0.120 | yes, margin 0.140 |
| jojo-02 twist (DWPose proof) | 164.6° / 13.7° | 146.0° / 125.3° | 127.4° / 85.5° | 128.7° / 120.3° | 40.6° / 40.6° | 0.005 / 0.035 | yes, margin 0.148 |
| ginyu-03 dance shimmy (Plask/MoveAI proof) | 118.3° / 118.3° | 117.9° / 114.5° | 135.4° / 134.2° | 119.1° / 116.5° | 15.9° / 29.7° | 0.060 / 0.060 | yes, margin 0.143 |

Reading notes (honest, not smoothed over):
- **jojo-02 elbow_R 13.7°** is not a bug in the maths: the image-right forearm is folded
  hard back across the chest, so shoulder→elbow→wrist really does close to ~14°. A detector
  would be expected to report a similarly small angle there; a rigger should check that limb
  against the gauntlet-flip rule before trusting it.
- **ginyu-02 knee–ankle offset 0.120** is the largest in the set: knees sit well outboard of
  the ankles in the wide squat. That is the pose's intent (elbows-out goofy squat), but it is
  exactly the knee-feet flag this tool exists to surface — wide squat, check the feet.
- **jojo-01** numbers are in `pose-angles-20261031.json` and on its proof strip (re-measured
  after the knee/ankle keypoints were corrected — see run log below).
- All four single-figure poses pass the 2D balance proxy (COM inside the ankle span). That
  proxy ignores depth, cape weight and motion, so it is a screen, not a physics verdict.

## Per-project detail

### 1. MediaPipe Pose (Google) — method-wired

- **What it is:** Google's open-source, cross-platform ML framework; Pose Landmarker runs
  BlazePose, which infers 33 3D landmarks from a single RGB frame, plus a segmentation mask.
  Runs on CPU; no GPU required; used in fitness apps and webcam mocap pipelines (e.g. FreeMoCap).
- **Cape problem:** the everyday one — "what are this pose's joint angles, and are the knees
  over the feet?" BlazePose's 33 points cover exactly the v7c joints (shoulder/elbow/wrist,
  hip/knee/ankle) with foot points (heel/toe) included.
- **Attempt log (honest, full — this is the closest any project got to a real run):**
  system `pip install mediapipe` failed (PEP 668 externally-managed environment); a `/tmp`
  venv failed with "No space left on device" (`/tmp` is a 512 MB tmpfs); a home-disk venv
  install **did succeed: mediapipe 1.2.0** (`mediapipe OK 1.2.0`). The legacy
  `mp.solutions.pose` API is gone in 1.2.0 (`module 'mediapipe' has no attribute 'solutions'`,
  deprecated Mar 2023), so the run was rewritten for the Tasks API
  (`mp.tasks.vision.PoseLandmarker`, IMAGE mode, num_poses=1) and the official heavy model
  bundle was downloaded (30,664,242 bytes, `pose_landmarker_heavy.task`).
  **Inference then failed before any frame was processed:**
  `OSError: libEGL.so.1: cannot open shared object file` — this VM has `libGL.so.1` but no
  `libEGL.so.1`, and there is no sudo/apt route available to this subagent to install it.
  **So: MediaPipe is installed and model-ready, but no MediaPipe detection ran and no
  MediaPipe output is claimed.** Next run (on a machine with libegl1, or after that package
  is installed): Tasks-API PoseLandmarker, IMAGE mode, num_poses=1, heavy model bundle,
  on the four pose-dialects frames, comparing detector landmarks with the by-eye set
  (the scratch script was deleted with `.work/`; the API call shape is in the attempt log). Cutout-on-black
  art is out-of-distribution for a model trained on photos, so a low-confidence /
  no-detection result would itself be a finding, not a failure to hide. Full log:
  `mediapipe-attempt-log-20261031.txt`.
- **Why it still leads (see verdict):** free, CPU, simplest install of the three estimators,
  and its output schema maps 1:1 onto the Cape rig joints.

### 2. OpenPose (CMU) — method-wired, cannot run here

- **What it is:** the first real-time multi-person system to jointly detect body, hand, face
  and foot keypoints (135 total) on a single image, via Part Affinity Fields (Cao et al.,
  CVPR 2017 / TPAMI 2019). BODY_25 gives 25 body/foot points including 6 foot points.
- **Cape problem:** the only estimator here built for multi-person frames — the mirrored-pair
  and towering-behind stand poses, where two figures overlap. Its foot points are also the
  most direct knee-feet input of the older systems.
- **Cannot-run reason (plain):** C++/Caffe build, CUDA/OpenCL-oriented, last tagged release
  v1.7.0 (Nov 2020), no maintained pip install; building it on this CPU-only VM was not
  attempted as a credible same-task run, and its licence is **non-commercial only** — a
  commercial Cape show would need a paid CMU licence. Method-wired instead: BODY_25-style
  body+foot subset on the squat, where foot placement matters most.
- **Cape note:** for a 2D cutout show, OpenPose's multi-person edge is real but its licence
  and stalled maintenance make it a reference vocabulary, not the tool to build on.

### 3. DWPose (IDEA Research) — method-wired, cannot run here

- **What it is:** "Effective Whole-body Pose Estimation with Two-stage Distillation"
  (Yang et al., ICCV 2023 CV4Metaverse workshop). Distils strong whole-body teachers into
  efficient students (t/s/m/l); 133 points; reported COCO-WholeBody AP 66.5% (DWPose-l),
  above its RTMPose-l baseline (64.8%) and RTMPose-x teacher (65.3%). Ships as the
  `dw_openpose_full` preprocessor in ControlNet, replacing OpenPose.
- **Cape problem:** hands + face. JoJo twist/point and menacing-lean poses live or die on
  finger/hand placement and head angle; BlazePose-33 gives a wrist, DWPose gives a hand.
  For the 2D rig that maps to gauntlet/fist orientation and cowl/head angle checks.
- **Cannot-run reason (plain):** needs the MMPose stack or the ONNX detector+pose pair
  (YOLOX detector + RTMPose-based pose checkpoint, ~250 MB class) plus a person detector
  that assumes photographic input. Not installed in this task: the existing rig venv has
  `onnxruntime` 1.31.1, so an ONNX DWPose run is the most credible next attempt, but no
  checkpoint was downloaded and no DWPose inference ran here — nothing is claimed.
  Method-wired instead: whole-body schema on the twist pose, body subset drawn (face/hand
  points are the documented gap, not drawn as if detected).

### 4. Cascadeur (Nekki) — method-wired, cannot run here

- **What it is:** standalone AI-assisted 3D keyframe animation software. AutoPhysics adjusts
  keyframed motion to plausible centre-of-mass/balance/weight (shown on a green preview twin);
  AutoPosing fills limbs from a few controls via neural posing; inbetweening, Animation
  Unbaking (dense mocap → editable keys), Video Mocap, and FBX/DAE/USD export on paid plans.
- **Cape problem:** inbetweens and balance. Cape's jump/punch/dance clips are hand-keyed;
  Cascadeur's method is the check "does this landing carry weight, is the COM over the
  support, does the arc float?" — plus mocap cleanup before any retarget.
- **Cannot-run reason (plain):** desktop GUI application, no headless/CLI run on this Linux
  VM; free tier is non-commercial-only and exports only to proprietary `.casc`, so even a
  successful free run could not feed the Cape pipeline without a paid Indie/Pro plan, which
  was **not bought and must not be bought without Mars's approval**. Method-wired instead:
  the COM-vs-support proxy + knee angles on the squat (the pose where balance matters most).
  The proxy is labelled a proxy on the proof itself — it is not AutoPhysics.
- **Cape caveat:** Cascadeur is 3D-first. Its value to a 2D cutout show is as a
  reference/cleanup stage (pose + timing + balance), not as a renderer; retargeting its 3D
  output onto 2D cutout pieces needs the mapping in §5.

### 5. Plask (primary) / MoveAI (compared) — method-wired, cannot run here

- **What it is:** markerless motion capture from ordinary video. Plask (browser): upload a
  clip, get a rigged character + FBX/GLB/BVH export, foot locking and smoothing included.
  MoveAI (Move One / Pro / Live / API): phone/iPhone-based capture, patented AI/CV, also
  markerless, multi-person and large-volume on higher tiers.
- **Cape problem:** dance/motion capture. The ginyu-03 shimmy, jump and fight moves are
  currently hand-posed; a 15-second phone clip of the same move, retargeted, gives real
  timing and weight for free — if the retarget map is right.
- **Retarget map used for the proof (video-mocap joint → Cape v7c piece):**

  | Mocap joint | Cape rig piece |
  |---|---|
  | wrist / hand | fist / gauntlet (`Arm_Front/Back_Lower` + cap) |
  | elbow | arm joint circle (`Arm_Front/Back_Upper` ↔ Lower) |
  | shoulder | torso shoulder (`Arm_*_Upper` root) |
  | hip / pelvis | pelvis / belt |
  | knee | leg joint circle (`Leg_Front/Back_Upper` ↔ Lower) |
  | ankle / toe | boot / foot (`Leg_*_Lower` + foot) |
  | head / nose | cowl / head (angle only — Cape head is a fixed cowl piece, not a mocap head) |

  Cape-specific limits the map must respect: 2D cutout has no depth axis (mocap Z becomes
  scale/foreshortening, never a new limb angle); the gauntlet-flip rule (panels outward when
  arms are up in front) overrides any mocap wrist roll; feet are boots, so toe splay from
  mocap is dropped and only ankle angle + foot turnout survive.
- **Cannot-run reason (plain):** both are account-based web/phone services; running one
  needs creating an account and uploading video, which was not done in this task (and no
  browser task is available to this subagent). No Plask or MoveAI capture is claimed.
  Free tiers exist (Plask 15 s/day; MoveAI 30 credits) so a real test costs $0, but it needs
  Mars's go-ahead on the account + a real dance/fight clip to capture.
- **Plask vs MoveAI, briefly:** Plask wins for this show on friction — browser, no phone
  rig, fastest single-person test, FBX/GLB/BVH out. MoveAI wins on capture quality/volume
  (multi-camera, multi-person, AAA-grade claims) at the cost of phone setup and higher paid
  tiers. For Cape's first mocap test, Plask is the free-first pick; MoveAI is the upgrade
  if Plask's single-view quality shows foot-slide or hand noise.

## Most promising: MediaPipe Pose

**Pick: MediaPipe Pose (Google), free/open, for the next real run.**

Why, in order: (1) it is the only estimator here that is free for commercial use, CPU-runnable,
and installable with one pip command — the other two estimators are either licence-gated
(OpenPose, non-commercial) or stack-heavy (DWPose, MMPose/ONNX + detector); (2) its 33-point
schema already covers every joint the v7c rig checks (shoulder/elbow/wrist, hip/knee/ankle,
heel/toe), so its output drops straight into `pose_angle_tool.py` with no schema translation;
(3) it is the engine inside free mocap pipelines (FreeMoCap), so it doubles as the cheap
on-ramp to the Plask/MoveAI question — if MediaPipe on a phone clip gives clean dance angles,
paid mocap may not be needed at all. DWPose is the runner-up for hand/face detail, and Plask
is the runner-up for full motion (not single poses). Cascadeur stays a reference method until
a paid plan is approved, because its free export cannot feed the pipeline.

**Next honest step (needs Mars's word only for accounts/payment, not for this):**
run MediaPipe Pose Landmarker on the four pose-dialects frames + one real phone dance clip,
compare detector angles with the by-eye table above, and report the delta. If MediaPipe
fails on cutout art (likely, out-of-distribution), the fallback is already built: run it on
the *performer* (photo/video), never on the cartoon, and retarget via the §5 map.

## Run log

- 2026-10-31: viewed `jojo-01`, `jojo-02`, `ginyu-02`, `ginyu-03` (1100×1500) in full before
  placing keypoints. Originals untouched (read-only open).
- 2026-10-31: `pip install mediapipe` (system) → PEP 668 refusal; `/tmp` venv → "No space
  left on device" (512 MB tmpfs); home-disk venv install started, still running at first
  proof generation — no vendor run claimed from it.
- 2026-10-31: `pose_angle_tool.py` run 1 → 5 overlays + contact sheet + JSON. Correction:
  jojo-01 knee/ankle/toe keypoints moved up (knee 0.675→0.645, ankle 0.87→0.84, toe
  0.905→0.875) after the first overlay showed the toe dots colliding with the footer;
  readout moved to an added strip below the art so no readout ever covers the feet.
  Re-run numbers are the ones in `pose-angles-20261031.json`.
- 2026-10-31: work venv removed from the deliverable folder after the task (`.work/` scratch
  deleted) so the folder contains only the report, tool, JSON and proofs. No repo push.

## Sources (web search, 2026-10-31)

- MediaPipe / BlazePose 33 landmarks, CPU, open source:
  <https://menonlab-blog-production.up.railway.app/blog/freemocap-open-source-motion-capture> ;
  <https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2025.1649330/full>
- OpenPose, CMU, Part Affinity Fields, 135 keypoints, non-commercial licence, v1.7.0 (2020):
  <https://deepwiki.com/cbsudux/awesome-human-pose-estimation/4.3-other-implementations> ;
  <https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/openpose-mediapipe-rtmpose-pose-tracking> ;
  <https://viso.ai/deep-learning/openpose/>
- DWPose, two-stage distillation, 133 whole-body points, ControlNet preprocessor:
  <https://instavar.com/pdf/DWPose_Effective_Whole_Body_Pose_Estimation_Two_Stage_Distillation.pdf> ;
  <https://deepwiki.com/Tencent-Hunyuan/HunyuanDiT/6.3-dwpose-integration>
- Cascadeur, Nekki, AutoPhysics/AutoPosing, free non-commercial / .casc-only export:
  <https://toolradar.com/guides/best-free-animation-software> ;
  <https://aitools.fyi/cascadeur> ; <https://creati.ai/ai-tools/cascadeur/>
- Plask vs MoveAI, markerless mocap, free tiers and paid prices:
  <https://2aqnwhtbqr.us-east-1.awsapprunner.com/compare/move-ai-vs-plask> ;
  <https://rankite.com/blog/best-motion-capture-software> ;
  <https://creati.ai/ai-tools/move-ai/>
- Prices are vendor/secondary-page reports as of the search date and must be re-checked on
  the vendor's own pricing page before any purchase; no purchase was made.
