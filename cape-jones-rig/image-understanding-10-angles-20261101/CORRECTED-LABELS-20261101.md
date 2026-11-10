# Corrected labels — canonical main room 10 angles — 2026-11-01
Mars 2026-11-01 00:58 CDT: "none of these so far are front angle. They're all three quarter angles. all of them every single one of these pictures is a three quarter angle just from a higher or lower perspective"
Mars 2026-11-01 00:58 CDT (save order): "You can save all of them from the into the repo but wire up some of the top five industry standard things to help you actually understand what they are and to actually make what I ask you to make and to actually um see those images and be able to tell what they actually are. So you can label and um talk about them correctly."

## Rule
- TRUE FRONT = 1 wall, no corner line, furniture flat to camera. 0/10 meet it.
- 3/4 CORNER = 2+ walls, vertical corner line, floor/wall lines converge, furniture shows a side face (CRT side, chair arm side, window depth). 10/10 meet it.
- HIGH / LOW = camera height, NOT a different angle type. High 3/4 and low 3/4 are still 3/4.
- All 11 images (10 angles + approved 2D) are EMPTY plates: no person, no figure, no character. Correct for background plates.

## Corrected set (see labels/corrected-labels-20261101.json for full scene graphs)
- 01 — 3/4 corner, eye-level wide. Claimed "TV-facing front" — REJECTED as front. PET poster cropped left, coffee table cropped bottom.
- 02 — 3/4 corner, chair-facing FRAMING (not a front angle). Corner line centre, walls converge. Coffee table cropped bottom.
- 03 — 3/4 corner, TV-side framing. TV+stand cropped left, coffee table cropped bottom. Near-duplicate framing of 01.
- 04 — 3/4 corner, window-side, 3 walls visible. Window cropped left, rug cropped bottom. Still corner perspective, not flat front.
- 05 — 3/4 corner, doorway-framed. Coffee table cropped bottom. Poster animal drifts capybara-like here vs pig-like in 01.
- 06 — 3/4 corner, LOW. DUPLICATE FLAG: 2 pink wingback chairs (grounding count 2, foreground right + centre-right). Large chair cropped right. Low is height, not angle type.
- 07 — 3/4 corner, HIGH oblique (not strict top-down). Furniture small/distant, floor dominates.
- 08 — 3/4 corner, closeup (chair/window). TV/posters/coffee table out of frame. Neon cropped top.
- 09 — 3/4 corner, coffee-table foreground. Framing variant of 01/03.
- 10 — 3/4 corner, closeup (TV wall). TV drawn at an angle (CRT side visible) = proof of 3/4, not front-on. PET poster cropped left, TV stand cropped bottom.
- Approved 2D — 3/4 corner, APPROVED PERFECT 1/1 as canonical main room picture (2026-11-01 00:43 CDT). Approval is as the room picture, NOT as a flat-front angle.

## Image-understanding system (5, all RUN, scripts/ )
1. Visual grounding — bbox/point/count (angle-01, angle-06 count 2, angle-10 verified above).
2. Angle classification — geometry rule above, classifier PASS 10/10 = 3/4, 0 = front.
3. Scene graph / object inventory — per-angle furniture presence/absence in the JSON.
4. Caption + attributes — palette (wall pink ~197-202,128-133,200-203; ceiling purple ~91-111,62-64,111-118), 2D cartoon black-outline, empty.
5. Visual QA gate — view before delivery, claim-vs-actual, duplicate, crop, empty checks. QA PASS with corrections applied, no image hidden/deleted.

## Repo save
PREPARED-NOT-LANDED. See LANDING-MANIFEST-20261101.json: 13 files, PR-only, additions only, 0 deletions. Excluded: work/*.blend duplicates (already in repo), media-generation duplicates (byte-identical to canonical angles). Do NOT claim landed until PR merged + verified on main by size+SHA.
