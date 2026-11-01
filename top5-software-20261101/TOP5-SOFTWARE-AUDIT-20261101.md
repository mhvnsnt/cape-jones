# TOP 5 INDUSTRY-STANDARD SOFTWARE / AI TOOLS — NOT RULES — 2026-11-01

Mars corrections, in order: (1) 09:45 CST — "I didn't ask you to wire in industry standard
systems… top five industry standard softwares / AI things, code or app or software, not just
rules, because you just hand tooled those rules." (2) 09:46 CST — "a lot of those things you
should already have wired up here in the repo 100% and you're just not using them. Get
everything you don't have and actually remember to start using all the things that we do have.
Get them 100% completed and wired up and fully in and landed."

## 1. ALREADY IN REPO, UNUSED — audit first (Mars 09:46, correct)
- Blender 4.5.3 LTS + 5.2.3 LTS, ~/workspace/tools-industry/blender-*/blender — WAS in repo
  tooling, NOT used on the side proof rig. Now USED: see side-rig-blender-20261101.blend.
- Blender Grease Pencil — in Blender, was NOT used on side proof. Now USED: FacingCheck_GP
  object in the .blend (bpy.ops.object.grease_pencil_add() in Blender 4.5).
- slice_clean.py, ~/workspace/cape-jones-rig/slice_clean.py — WAS used to cut side pack
  (17 pieces) and back pack (14 pieces). Reused, not re-invented.
- FK rig scripts joint_locked_rig_v7c.py etc. + large-temp 3x rotate method — WAS in repo,
  used by the parallel side-fix for idle arms-down rotation, NOT by the sloppy proof.
- Cape Jones Toon (cjtoon.py, toon-boom-own-version-20261101/) — 19 nodes, FK 6/6, runs
  exit 0 today. $0 production path while Harmony is blocked. NOT a Harmony replacement.
- Spine skeleton JSON cape-jones-rig-spine.json (Spine 3.8 skeleton, joint-locked v4 bones)
  — WAS in repo, UNUSED on side rig. Recorded here as already-wired, not re-bought.
- Tahoma2D 1.6.3 (OpenToonz fork) — in ~/workspace/tools-industry/tahoma2d-1.6.3/,
  AppImage + extracted squashfs-root. Binary runs: tahoma2d -version = Tahoma2D v1.6.3.
  AppImage mount FAILS headless (no FUSE / fusermount), extracted binary is the usable route.
- Toon Boom Harmony wiring (toon-boom-wire100-20261101/, 34/40 documented) — wiring only,
  NOT live software. See tool 1 below.

## 2. TOP 5 SOFTWARE, tested live here (not names only)
1. Toon Boom Harmony — INDUSTRY STANDARD, TV/film 2D rig. STATUS: BLOCKED, NOT RUNNING.
   - No live install: shop fmmg.mars@gmail.com = 0 subscriptions/orders/licenses (2026-11-01
     01:48 CST check). Windows .exe is on Mars's own browser Downloads, NOT on this VM.
   - Azure free trial route: PAUSED 2026-11-01 09:33 CST — Azure cannot accept prepaid
     cards, resume only on a non-prepaid card. No trial, no VM, no charge.
   - Do NOT claim Harmony works. Fallback in use: Cape Jones Toon.
2. Blender 4.5.3 LTS + Grease Pencil — FREE, runs HERE, USED FOR THIS FIX.
   - Version verified: Blender 4.5.3 LTS, 2025-09-09. 5.2.3 also present.
   - Side rig .blend: SideRigArmature, bones pelvis/chest/neck/head/upper_arm/forearm/
     thigh/shin. Forearm bone vector = +X (head.x 0.1 -> tail.x 0.9, delta +0.8): forward,
     flexion direction, toward chest facing. That is the flip fix, in bone data, not a rule.
   - Image planes parented to bones (BONE parent): side_torso_belt -> chest,
     side_head_profile -> head, with image textures + alpha.
   - Render blocker, then fix: headless render first failed "libEGL.so.1: cannot open" on
     both 4.5.3 and 5.2.3. Fix attempted in this task: apt install libegl1 + libgl1
     (running, see render note below). .blend saved BEFORE render so the rig survives a
     render failure: side-rig-blender-20261101.blend, 502 KB.
3. Tahoma2D 1.6.3 (OpenToonz fork, Studio Ghibli lineage) — FREE, runs HERE (extracted
   binary), bone / cut-out rig + frame-by-frame. NOT yet used to pose this side rig —
   recorded as available next rig tool, not claimed as used. AppImage route fails headless
   (FUSE), extracted squashfs-root/usr/bin/tahoma2d is the route.
4. Adobe Animate — INDUSTRY STANDARD, now in maintenance mode (Sep 2024, no major new
   features, per 2026 comparisons). STATUS: NOT INSTALLED, NOT AVAILABLE HERE — no binary
   on VM, paid Creative Cloud, no licence in repo. Not faked, not installed on guess.
5. Spine (Esoteric) / DragonBones — 2D skeletal rig for games. STATUS: Spine RUNTIME
   FORMAT present (cape-jones-rig-spine.json, Spine 3.8, joint-locked v4 bones), Spine
   EDITOR itself NOT installed here (no binary, $69 one-time, trial not started, no purchase
   without Mars approval). DragonBones: not installed. AI pose check (MediaPipe/OpenPose):
   NOT RUN — mediapipe install failed: system pip blocked (PEP 668), venv install failed
   "No space left on device" on /tmp tmpfs (512 MB, 240 MB used at check; home disk itself
   56 GB free, /tmp is the limit). That is a real blocker, stated plainly, not a fake
   pose-detection result. A pose check was therefore done in bone data (forearm +X) and in
   the parallel fixed rig's anatomy/flip checks, not by MediaPipe.

## 3. THE FLIP FIX, in software terms (not a rule)
- Native side pack faces RIGHT (+X): head face, torso chest emblem, belt buckle, boot toes
  all +X. The sloppy proof flipped bent/forearm/fist to -X (hand behind back = extension).
- Correct: NO horizontal flips on arm pieces in this pack. Upper-arm bicep stays on +X
  (front) side. Forearm bone +X = flexion, toward chest facing.
- Finished poses from the parallel anatomy fix (already on disc, side-rig-fixed-20261101/):
  side-idle-arms-down-fixed-20261101.png (1400x1600, bbox 410,120-893,1450, ground 1450)
  and side-bent-correct-20261101.png (1400x1600, bbox 410,120-1151,1450, ground 1450),
  with before-after-flip-20261101.png. Those are the finished rig images for Mars approval;
  the Blender .blend in this folder is the software rig that encodes the same +X forearm.
- Honest limits (from that fix, not hidden): idle forearm gauntlet rotated from horizontal
  reads cup-like; leg joint balls remain visible; FK pivots recorded in manifests; full FK
  animation chain (walk etc.) NOT built — two finished poses, idle + bent, ready for approval.

## 4. WHAT WAS NEW vs ALREADY-WIRED
- NEW in this task: Blender side-rig .blend + Grease Pencil object + bone-parented image
  planes, libEGL install attempt, this audit file. No new paid software bought.
- ALREADY-WIRED, NOW ACTUALLY USED: Blender, Grease Pencil, slice_clean, FK scripts,
  Cape Jones Toon, Spine JSON (recorded), Tahoma2D binary (verified, not yet posed).
- STILL BLOCKED (parent/root browser task, not this subagent): Harmony live install,
  Azure trial (prepaid card), Adobe Animate licence, Spine editor purchase/trial,
  MediaPipe on /tmp (needs a venv on home disk, not /tmp, or disk cleanup).

## 5. LANDING — owed, not claimed here
- This folder (top5-software-20261101/) + side-rig-fixed-20261101/ need a PR-only landing
  batch: branch -> PR -> merge only on clean/GREEN -> verify size+SHA on main.
  No PR number is claimed in this file until that run returns one.

## 6. RENDER CORRECTION (checked, not faked)
- Blender render blender-side-rig-render-20261101.png, 1400x1600, is BLANK GREY.
  Reason not yet isolated: bone-parented planes likely offset out of camera frustum, or
  EEVEE alpha/hash material did not show. Do NOT present that render as a finished rig.
- What IS verified in Blender: .blend opens, SideRigArmature exists, forearm bone
  delta +0.8 in +X, Grease Pencil object exists, torso/head planes are bone-parented.
- Finished rig IMAGES for Mars approval remain the parallel anatomy fix:
  side-rig-fixed-20261101/side-idle-arms-down-fixed-20261101.png and
  side-rig-fixed-20261101/side-bent-correct-20261101.png, both 1400x1600, ground 1450.
  Blender render fix (camera aim / plane placement / unparented plane test) is still owed
  before Blender is claimed as the rendering tool for this rig.
