# Mouth / jaw cleanup — 5 industry-standard methods — 2026-10-31

Status: DELIVERED, approval 0/1 for the cleaned PAH GO movement.
No repo push. No existing file overwritten. No original deleted.
Folder: mouth-jaw-cleanup-5-methods-20261031/

## What Mars ordered
2026-10-31 21:20 CDT, replying to pahgo-movement.gif: pull in and wire
100% five industry-standard things to help with the mouth stuff and
the jaw movement stuff, to make it cleaner and look better.

Known defects fixed here (Mars 21:18 CDT):
- f00 MBP and f29 REST: mouth line missing in the middle, part edited
  over, line fragmented/not continuous.
- f09 AH key: too much of Robin's features around the mouth, not
  mouth-only.
Mars's closer list is STILL OPEN — he said he will look closer and
list other messed-up frames. This does NOT claim all defects fixed,
only these known ones, measured below.

## The 5 methods — run vs mapping, labelled
1. **Toon Boom Harmony mouth-chart substitution — RUN.** Mouth on its
   own layer, swapped per frame over the masked clean head base
   (476x688, mouth zone already blanked), no old mouth bleeding
   through. This is the substitution system itself, in build script.
2. **Mouth-ROI + garbage matte (rotoscope matte) — RUN locally;
   MediaPipe Face Mesh model itself is MAPPING only.** MediaPipe lip
   contour (landmarks 61-68) was NOT run on this VM — no model run.
   Its ROI idea is implemented locally as: 2D connected components
   (scipy label, 8-connectivity) on the colour-filtered AH patch, keep
   ONLY the component containing the tongue/mouth body, drop every
   other component. That is the matte, not hand-erasing.
3. **Animation cleanup / line continuity — RUN.** MBP fragmented line
   bridged with a continuous stroke through measured endpoints (see
   below). Original fragments kept, bridge pixels only added.
4. **Colour decontamination (compositing spill suppression equivalent)
   — RUN.** Keep only mouth colours: dark outline/interior, orange
   tongue, white teeth (GK). Drop JPEG fringe colours (red/green/
   yellow edge spill) from the pulled patches.
5. **FACS jaw-hinge + Preston Blair slow-in/slow-out — RUN.**
   Jaw drops preserved exactly: MBP 0, AH 16, GK 8, GAP 10, REST 0.
   Smoothstep 3-frame inbetweens, upper lip fixed, lower lip follows
   jaw, mouth centre follows jaw by 1/4 of jaw drop, hinge-row fill
   masked to the head silhouette (no flat skin stripe, no full-width
   leak). FACS names (AU24 MBP, AU25+AU26 AH, AU12 GK) are mappings
   to FACS; no FACS coder ran.

NOT counted in the five, and not run: Rhubarb/audio-driven timing
(timing here is fixed 6f/viseme, recorded audio 0%), Harmony bone jaw
rig, Character Animator jaw behaviour, Blender shape-key jaw, ARKit
blendshapes (taxonomy only), true 3D mandible rotation/muscle
simulation (needs a true 3D head model — that is the separate 2D-3D
bridge work, not this cleanup).

## Measured fixes
### AH — mouth-only, Robin features removed
Source ah-front-03_tight_patch.png, 296x98, alpha 11,096 px.
After colour filter: 10,522 px (574 fringe px dropped).
Components (colour-filtered, 8-connectivity):
- Component 2 KEPT: 9,007 px, bbox x0-231 y17-97 — the mouth body
  (black interior + orange tongue + lips). This is the only kept piece.
- Component 1 DROPPED: 100 px, x11-55 y8-10 — the thin top dash
  above the mouth (visible in old f09 zoom, top-left).
- Component 3 DROPPED: 1,078 px, x152-270 y24-97 — the right-side
  jaw/chin outline + black triangle + vertical fringe line (visible
  in old f09 zoom, bottom-right of the mouth). This is the main
  "too much of Robin's features" piece.
- Component 4 DROPPED: 231 px, x0-63 y55-97 — left cheek/jaw
  fragment below the mouth.
- Component 5 DROPPED: 96 px, x0-11 y66-97 — left sliver.
- Component 6 DROPPED: 10 px, x221-229 y96-97 — tiny fragment.
Total dropped from the colour-filtered patch: 1,515 px.
Kept mouth body was cropped to its own bbox (232x81) and resized to
the original placed size 196x67 at the same single target centre
(231.5, 504.5), so placement does not jump and mouth size does not
shrink. The mouth now ends at its true right corner (source x231),
not at the jaw line (source x270).

### MBP — continuous line, gap bridged
Source mbp-front-09_tight_patch.png, 86x10, alpha 93 px, 0 fringe px.
At placed size 178x23, dark columns were x16-87 (left fragment) and
x138-157 (right diagonal fragment), with a GAP of 50 columns,
x88-137, with no dark pixels at all — that is the missing middle
Mars saw.
Bridge: straight stroke, width 6 px (median fragment thickness),
from left end (x87, median y13.5) to right start (x138, median
y14.5), 258 bridge pixels added, original fragments untouched.
After repair: dark columns x16-157, missing columns inside: NONE.
f00 and f29 now show one continuous line. Honest note: at 3x zoom
the bridge is a straight segment and the left fragment is wavy, so
there is a small step at the join — visible only at 3x zoom, not at
normal size, and the line is continuous, not broken. This is a
REPAIR, labelled as such: a clean, continuous, front, closed Robin
line at usable resolution does NOT exist in this set, so this bridge
is the cleanup, not a pulled clean line, and not a newly invented
mouth shape (endpoints, width, and fragments are all original).

### GK — decontaminated only
Source gk-front-05_tight_patch.png, 531x81, alpha 15,716 px.
After colour filter: 15,393 px, 323 fringe px removed. It was already
a single connected component (15,393 px, x64-530 y0-68), so no
component was dropped — GK had no surrounding-feature defect, only
fringe. Placed size unchanged: 188x30.

## What was rebuilt
PAH GO movement only (phrase not rebuilt here): keys
MBP -> AH -> GK -> GAP -> REST, 30 frames @24fps, 1.25s, keys every
6 frames, 3-frame smoothstep inbetweens — same timeline, same
placement, same jaw drops as the original movement, only the patches
are cleaned.
Key frames measured: f3 MBP 178x23 jaw 0; f9 AH 196x67 jaw 16;
f15 GK 188x30 jaw 8; f21 GAP 0x0 jaw 10; f27 REST 178x23 jaw 0.
Jaw range 0-16 px, unchanged.

## Per-frame defect check (viewed)
- f00 MBP: PASS — continuous line, no gap, no edited-over break.
- f09 AH: PASS — mouth-only, black interior + orange tongue, no top
  dash, no right chin triangle, no left slivers, no coloured fringe.
- f29 REST: PASS — same continuous MBP line as f00 (REST = MBP).
- f15 GK: PASS — clean teeth, no surrounding features.
- f21 GAP: PASS — no mouth patch, jaw still drops 10 px.
Full contact (key frames) and defect-check sheet (f00/f09/f29 full +
mouth zooms) were viewed before reporting.

## Files
- build_clean_movement.py (builder: 5 methods, measurements)
- pahgo-movement-clean-20261031.gif (30f @24fps)
- pahgo-movement-clean-contact-20261031.png (f3, f9, f15, f21, f27)
- pahgo-defect-check-20261031.png (f00, f09, f29 + mouth zooms)
- pahgo-movement-clean-measurements-20261031.json (per-frame + clean stats)
- frames_clean/ (30 PNGs)
- clean-mbp-patch.png, clean-ah-patch.png, clean-gk-patch.png
- CLEANUP-5-METHODS-REPORT-20261031.md (this file)

## Still owed
- Cleaned movement approval: 0/1.
- Mars's closer list of other messed-up frames: OPEN — when it arrives,
  fix those in the same pass style, do not claim this pass covered them.
- AH is still an open smile, not a shout (front AH shout with teeth
  does not exist in this front Robin set) — shape cost carried over,
  unchanged by this cleanup.
- Audio-driven timing, true 3D jaw, full-body talking, per-shot
  lip-sync: unchanged, still owed elsewhere.
- No repo push; landing is a separate step.
