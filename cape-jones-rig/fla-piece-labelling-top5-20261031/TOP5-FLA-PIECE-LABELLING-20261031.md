# Top-5 industry-standard FLA piece detection / labelling / understanding tools
## Wired 100% fully — 2026-10-31 (Mars order, ~18:39 CDT)

Folder: `fla-piece-labelling-top5-20261031/`. Python venv in `venv/` (OpenCV 5.0.0).
Ruffle 0.7.1 in `./ruffle`. No repo push made in this task.
Mars approval of this system: 0/1 — do NOT claim approved.

## Why the ranking is honest, not a brochure list
The ranking was tested on OUR pieces, not on a generic benchmark:
- Our pieces on disk are PNG slices (2,854 in sliced-clean-20261031, named
  Row1_1 etc. — no part name in the filename), plus 31 already-labelled
  templates in sliced/. There is NO real .fla/.xfl/.swf for Cape Jones on
  disk, and Adobe Animate is not installed (trial blocked on Mars's secure
  entry). Any tool that needs a real FLA or Animate therefore cannot be
  #1 here, however good it is in general — and this doc says so.
- The batch test (below) proved the hard limit: most unlabelled pieces are
  FRAGMENTS (a foot, a lower leg, a torso section, a joint ball), not whole
  templates. Whole-template matching therefore disagrees most of the time.
  That is a property of the pieces, not a bug in the ranking — and it is
  exactly why Mars's eye is the deciding vote.

## Ranked top 5

### #1 — OpenCV shape matching (contours + Hu moments + template matching)
Script: `tool1_opencv_match.py`. Command: `venv/bin/python tool1_opencv_match.py <piece.png>`
Source: OpenCV (free, open source) — cv2.matchShapes, CONTOURS_MATCH_I1,
Hu-moment distance, lower = more similar; tested in both orientations
because a mirrored limb is a real mislabel risk.
Why #1: the only tool that runs today, with no download, no Animate, and
an exact proof — a known template matched against itself scores distance
0.0 (Hand_3_Open -> Hand_3_Open, 0.0). It also exposes its own weakness
honestly: hand sub-types sit at distance 0.025 from each other, so a
silhouette alone cannot tell Hand_2 from Hand_3 — Mars's eye must.
Output per piece: best template, mirrored Y/N, distance, confidence,
second-best template, reason.

### #2 — Naming + metadata schema (Harmony / Animate convention)
Script: `tool3_naming_schema.py`. Command: `venv/bin/python tool3_naming_schema.py <raw_name> [source_folder]`
Source: Toon Boom Harmony / Adobe Animate naming practice —
character_part_view_angle_variant, e.g. capejones_arm1_upper_lower_front,
capejones_hand_open_front; peg/hierarchy naming for limbs.
Why #2: it detects nothing, and that is the point — without a schema,
every other tool's output is noise Mars cannot correct consistently. It
turns a raw proposal into a canonical name and flags the traps this rig
already proved: Front/Back = WHICH LIMB (Arm_Front = ARM1, our left),
not body-facing; CLEAN variants = provenance unverified, not canonical;
GRAFTED = reject; Eye_White_R shadow-vs-reject and Face_Angry
combined-vs-split are Mars-pending exceptions, flagged, never decided
by the tool. Folder-mismatch warnings (e.g. a "front" proposal from a
fla-back folder) force an eye-check.

### #3 — Local colour + proportion nearest-neighbour classifier
Script: `tool2_embedding_knn.py`. Command: `venv/bin/python tool2_embedding_knn.py <piece.png>`
Source: the embedding/classifier idea (CLIP-style nearest-neighbour in a
feature space), implemented locally and auditably — NOT a downloaded
CLIP model. Feature vector = aspect ratio, fill ratio, centroid, and a
12-bin RGB histogram, matched against the 31 labelled templates.
Why #3: complementary to #1 (colour/proportion, not shape), runs today
with no model download, and its distance is interpretable. Self-match
proof: Hand_3_Open -> Hand_3_Open, distance 0.0. Why it is not a real
CLIP run: a downloaded CLIP model's generic vocabulary has no entry for
"capejones_arm1_lower", and its cartoon-fragment labels would need the
same Mars correction pass anyway — the local kNN is the version that
actually ran on our templates.

### #4 — FLA/XFL parsing + JSFL library reading
Script: `tool4_xfl_jsfl.py`.
Commands: `venv/bin/python tool4_xfl_jsfl.py xfl <file.xfl>`,
`... jsfl <file.jsfl>`, `... make-test-xfl <out.xfl>`
Source: Adobe Animate XFL format (an XFL file is a ZIP; DOMDocument.xml
holds the timeline, LIBRARY holds symbols) and the JSFL API
(fl.getDocumentDOM, timeline layers, convertToSymbol) for reading a
library — the native metadata route for FLA pieces.
Why #4, not #1: it is the CORRECT native route, but there is no real
Cape .fla/.xfl on disk and Animate is not installed, so it could only
be proven on (a) a synthetic XFL built from the 31 sliced/ names
(31 symbols parsed back correctly) and (b) our real .jsfl rig builders
(build-cape-jones-rig-v7.jsfl: STACK of 12 layers parsed, pivots found).
The moment a real XFL lands, this tool reads its symbol names straight
into Tool #3's schema — that wiring is already in place.

### #5 — SWF inspection + Ruffle rendering
Script: `tool5_swf_ruffle.py`. Ruffle binary: `./ruffle` (0.7.1-stable,
89a7049965f3090e706265670df309a5128233ac, 2026-10-07).
Commands: `... header <file.swf>`, `... make-test-swf <out.swf>`,
`... ruffle-version`; eye-check a real SWF with `./ruffle <file.swf>`.
Source: Ruffle (free, open source Flash player) + the SWF header format
(FWS/CWS/ZWS, RECT bit-packing, frame rate, frame count).
Why #5: header parsing is proven — it is the same read the show-repo
audit used to get Foster's reel fps + frame counts (all 24 fps), and it
was re-proven here on a synthetic SWF (FWS v10, 1100x1500, 24.0 fps,
1 frame, parsed back exactly). Honest limit, stated in the script:
Ruffle desktop is a PLAYER, not a headless batch renderer — there is
no screenshot mode in the stable CLI, so this tool does NOT claim batch
SWF rendering. It eye-checks a real SWF and parses any SWF header.

## NOT picked — one line each
- OCR for sheet text: the sheets carry no text labels, so OCR would find nothing to read.
- Pose estimation (e.g. MediaPipe): needs a full body in frame; it fails on isolated fragments like a foot or a joint ball.
- DAM / asset-management tagging alone: tagging organises labels, it does not propose them — no detection power.
- Downloaded CLIP out of the box: vocabulary mismatch for our part names, plus a model download, for no proven gain over the local kNN that actually ran.

## Batch run — 60 pieces, honestly counted
Batch: sliced-clean-20261031/D-xray-angle-ref/fla-front (33 pieces, all)
+ fla-back (first 27, sorted) = 60 pieces, all previously unlabelled
(Row1_x names only, no part name in the filename).
Command: `venv/bin/python label_pieces.py <60 piece paths> --out batch-60-20261031`
Outputs: `batch-60-20261031/proposals.json`, 8 contact sheets,
`mars_corrections.txt` (the blank correction form for Mars).

Results, after the banding honesty fix (see below):
- Total: 60/60 = 100% processed
- HIGH confidence (both tools agree, conf >= 0.8): 2/60 = 3.3%
  (fla-front/Row1_20.png -> belt, fla-back/Row1_16.png -> torso chest)
- MEDIUM (tools agree, lower conf): 0/60 = 0%
- NEEDS-MARS-EYE (tools disagree): 58/60 = 96.7%
- REJECT (no opaque pixels / GRAFTED winner): 0/60 = 0%
- Tool agreement: 2/60 = 3.3% — this is the headline, not a footnote.
- Folder-mismatch warnings: 3 (fla-back pieces proposed as "front" — eye-check required)
- Mislabel caught by eye-checking sheets 1-2 (agent's eye, NOT Mars's):
  foot -> cape_collar, pelvis/briefs -> torso, leg -> belt, torso chest ->
  hand_fist, head -> pelvis. These are exactly the fragment-matching
  failures the NEEDS-MARS-EYE band exists for.

BANDING FIX (important, not hidden): the first run scored disagreeing
pairs as MEDIUM (51/60 MEDIUM). Eye-checking sheets 1-2 showed most of
those MEDIUM proposals were wrong. The rule was fixed in label_pieces.py
and the sheets regenerated: disagree = NEEDS-MARS-EYE, full stop.
Future runs use the fixed rule. The old MEDIUM count must never be quoted.

## Honest limits — where Mars's eye is the deciding vote
- Fragment matching: whole-template shape/colour matching cannot reliably
  name a fragment (a foot is not a whole leg). Next step, not claimed
  here: sub-template matching against cropped template regions (e.g.
  lower-leg and foot regions of Leg_Front/Leg_Back).
- Hand sub-types: silhouettes at distance ~0.025 apart — the tool cannot
  separate them; Mars's eye can.
- No real FLA/SWF: Tools #4 and #5 are proven on synthetic files + real
  JSFL, not on a real Cape FLA/SWF, because none exists on disk.
- Auto accuracy is NOT claimed: with 2/60 agreement, any "auto accuracy"
  percentage would be a lie. The system's value is the contact sheet +
  correction workflow, which makes Mars's eye pass fast and auditable.
