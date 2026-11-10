# 3/4 SITTING SHEET — EXHAUSTIVE SEARCH REPORT 20261101

Owned error, plainly: the previous sitting-rig job searched only
sliced-68 / transparent-plates / sliced / fla-packs locally and claimed
no sheet literally named that. That was an incomplete search, NOT proof
it does not exist in the repo. Mars was right to call that lazy.
This job searched the full repo tree. It does NOT claim absence.

## PRIMARY SOURCE — Mars's upload, 2026-11-01 00:54 CDT

- File: `workspace/user/files/1000179383_25_yh27.jpg`
- Size: 1200x1648, RGB, 90 KB, md5 4dc11a3dc88b9bd0cba55bc156971ecb
- What it is, viewed with own eyes: exploded rig sheet on grey
  background, sitting configuration. Head (purple cowl), torso with
  purple emblem, belt + pelvis piece, upper arms (2, with joint balls),
  forearms + hands (2), spare hands (3), thighs (2, angled diagonally
  = sitting thighs), shins + feet (3 full, 1 shin-only + 1 spare knee
  ball), cape (black, full back piece, right side).
- This is the 3/4 sitting sheet Mars meant. A separate build job is
  cutting it and piecing it into the 3/4 sitting rig. This search
  report does NOT block that build, and does NOT claim that build
  is done here.
- This upload is NOT byte-identical to any of the 11 repo
  lounge-3quarter sheets below (different md5, different piece
  layout: thighs and shins are SEPARATE pieces here).

## EXHAUSTIVE SEARCH — what was searched

- Repo: mhvnsnt/cape-jones, main tree via local study clone
  `~/workspace/cape-jones-flying/` (sparse checkout, characters/sheets
  only on disk; tree listing is full, NOT sparse-limited):
  `git ls-tree -r --name-only HEAD` = 63,033 files.
- Search terms over the full tree: sit, sitting, seated, lounge,
  chair, 3quarter, three, quarter, angle, pose, sheet.
  "sit" alone matches 1,649 tree paths (mostly 3D/scripts/tools).
- Sheet-only scope: `characters/sheets/` = 251 files.
  Sheet matches for sit/lounge/3quarter = 30 paths (see below).
- Local rig folders searched: `~/workspace/cape-jones-rig/` for
  sit/lounge/3quarter (excluding venv), plus sliced-68 manifests,
  transparent-plates-grok-full-sweep plates, sliced-clean-20261031.
- No commit or push was made from the sparse clone, per the
  repo AGENTS.md no-sparse-commit law. This job: no push at all.

## CANDIDATES FOUND IN THE REPO (exact paths)

Folder literally named for this job — this is what the first job
should have found and named:

`characters/sheets/fla-packs/lounge-3quarter-packs/` — 11 sheets,
each md5-identical to the same-named file in
`characters/sheets/fla-packs/lounge-packs/` (duplicate folder,
same content under two names):

- clean-DGb2j.jpg — md5 32e1f4702c10754f8953b41e54996166,
  1792x1008. Kit: head, torso, arms, legs, cape. NOT sitting-only.
- clean-F72A5.jpg — md5 66430136dcfdc7832cf741484dfca269,
  1200x1648. BEST REPO MATCH. Kit: head Row1_1, torso Row2_3,
  arms Row2_1/2/4/5, legs Row3_1/2/3 straight + Row3_4/Row3_5
  PRE-BENT sitting legs (thigh angled, shin vertical, foot
  forward). Already sliced in
  sliced-68-unsliced-20261031/sheets/fla-packs/clean-F72A5/
  (11 pieces, manifest verified).
- clean-IUUgX.jpg — 61fc87d2afe3563d41454eeb1a38e7f8, kit.
- clean-IowZk.jpg — 4147d5c5240740a49d6f28ffbda91aa2, kit.
- clean-N3ies.jpg — c90d25b07041355b58de6b172e81cd00, kit,
  many hands, straight legs, cape.
- clean-OAFac.jpg — c7132156bed427e5d223883019d2ab65, kit.
- clean-U8YqN.jpg — 3fa30be349da109b9486ff7cb0731772, kit +
  one assembled 3/4 figure on the left of the sheet.
- clean-ZdzDG.jpg — c6ce04c65101e93610e2a599ca9b5b5c, kit.
- clean-jvqhV.jpg — 2a0b03c42fab9c7a0cfa077c40375c64, kit.
- clean-wDheK.jpg — afd775a8c395416366572a9dcbf59bed, kit.
- clean-zxxqO.jpg — 48d9f7ff18568baf5fbb54340bd0394c, kit.

Other sheet matches, NOT the sitting sheet:
- characters/sheets/exposure-sheets/exposure-sheet-6-sit.jpg
  — sitting exposure strip sheet, not a rig kit.
- characters/sheets/fla-packs/angle-sheets/fla-3quarter-front.jpg
  and fla-3quarter-back.jpg — 3/4 kits, STANDING, not sitting.
- characters/sheets/fla-packs/xray-vision/xray-fla-3quarter-*.jpg
  — 3/4 x-ray reference, standing.
- characters/sheets/model-sheets/model-sheet-3quarter-*-set*.jpg
  — 3/4 model sheets, standing.

3D sitting three-quarter renders (NOT FLA sheets, listed so they
are not mistaken for the sheet): 3d-assets/cape-jones-rig/
sitting-canon/final_threeq.png, sitting-redo/pose_sit_*_threeq.png
(lean_forward, leg_folded, normal, recline, shrug),
sitting-take3/*_threeq.png (incl. lounge_threeq.png),
living-room/sit-targets/renders/sit_pose_sit_normal_threeq.png,
proof/mocap-sit/sit_threequarter.png.

Honest limit: no single ASSEMBLED sitting figure sheet was found
in the 2D sheets. The repo sitting material is kits (above) plus
3D renders. Mars's upload fills that gap exactly: it IS an
exploded sitting rig sheet.

## SECONDARY RIG BUILT FROM THE REPO SHEET (not the Mars build)

Builder: build_34_rig.py in this folder.
Pieces: clean-F72A5 head/torso/arms/bent legs + cape from
clean-DGb2j Row2_6 (F72A5 has no cape piece — stated, not hidden).
Output: threequarter-sitting-rig-20261101.png, 1100x1500
transparent, bbox 258,150-843,1349, alpha 453,531px.
Viewed: knees up, shins down, feet planted forward, hands at
knees — reads as seated. Thighs are the angled part of Row3_4/5,
mostly occluded by torso/hands in this assembly.
This is a SECONDARY fallback rig only. The Mars-upload build is
primary and is NOT duplicated here.

## RIG RECORD

- ORIGINAL RIG = front-facing rig, RIG-00 v7c apose, used for
  front facing.
- NEW RIG = 3/4 angle rig, built from the 3/4 sitting sheet,
  for the 3/4 angle room. This room, as currently drawn, is a
  3/4 angle room, so the 3/4 rig is needed NOW for this room.
- Room angles context, plainly: the 10-angle job is RUNNING
  separately (front-facing level to TV + facing-chair angles are
  IN that job, not yet delivered). Do NOT claim they are done here.

## APPROVALS

- Found sheet (repo side): 0/1.
- New 3/4 rig (repo-side secondary rig): 0/1.
- Mars-upload sheet + its separate build: approval belongs to
  that build job, NOT claimed here.
- No repo push by this job.
