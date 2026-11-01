# ROOM-SCALE RULE — standing, 2026-10-31

Mars, 2026-10-31 19:42 CDT, replying to the dual-orientation delivery:
he was shown in the room floating in the middle, way too small.
**Do not show him in that room at that scale again.**

## 1. The lock (Mars, 2026-10-31 15:34 CDT, room ONLY)
- 2.5x standing, rig 950px tall, feet ON THE FLOOR, chair back at his waist.
- Seated = standing minus 0.2, i.e. 2.3x, approximate, verify visually.
- Room ONLY. Other backgrounds are NOT changed by this rule.
- Room background in all proofs here is the STAND-IN batch-KKGuh.
  It is NOT the canonical room. Canonical room pictures are still
  pending from Mars. Do not call this background canonical, and do
  not recolour it toward a guessed canonical.

## 2. Measured translation — no guessing
Locked preview: `showcase/layout-pass-room-scaled-25x-20261031.jpg`,
1168x1060. Measured in that file:
- Head (purple cowl) top y = 268
- Feet (white) bottom y = 911
- Figure alpha height = 643 preview px
- 643 / 950 = 0.677 preview scale (the preview is downscaled)
- Figure height / frame height = 643 / 1060 = 60.7%

Translation to a 1920-tall master at the same relative scale:
- Figure alpha height = 0.607 x 1920 = 1165px
- Original rig in that system was ~380px tall; 2.5x = 950px rig height.
  "950px" is a rig-coordinate height, not a pixel count to copy
  blindly into a differently-sized frame. The invariant is the
  60.7% frame proportion and feet-on-floor, verified in each frame.

Old dual-orientation proof (the violation):
- Figure alpha height 709 in a 1920 master = 36.9% of master
- Head master 613, feet master 1322, centred in the protected square
- Rug top in master ~1371, chair feet ~1518
- Old feet were 49px ABOVE the rug top and 196px above chair feet:
  floating in the middle of the room, too small. That is exactly
  what Mars called out.

New room-scale master (this folder):
- Figure alpha height 1165 (64% taller than old 709)
- Head 385, feet 1550, waist (belt, 0.53 down the figure) ~1003
- Feet 179px BELOW rug top, 32px below chair feet: on the rug,
  slightly closer to camera than the chair, which is correct
  perspective for a figure standing in front of the chair's plane.

## 3. What fits, what does not — plain numbers
Protected square = central 1080x1080 (master 420-1500 both axes).
Room-scale figure height 1165 > 1080 by 85px.
- Centre-crop landscape (master y420-1500): cuts head 35px
  (420-385) AND feet 50px (1550-1500). NOT a whole-figure export.
- Centre-crop portrait (master x420-1500, full height): whole.
  Figure x 593-1327 sits inside 420-1500, head 385, feet 1550
  inside 0-1920. Whole.
- Centre-crop square (420-1500 both): cuts head and feet, same
  as landscape. NOT a whole-figure export at room scale.

**Rule: never silently shrink him back to 709 to make the centre
crop fit.** A figure-only shrink is the old violation in reverse.
The whole scene must be re-framed together (section 4).

## 4. Recommended method — pull-back / two-framing (RUN, proven here)
- Portrait: centre crop from the room-scale master. Whole, no resize.
- Landscape: a DEDICATED 1920x1080 framing of the same room at the
  same relative scale. Figure 655px in a 1080 frame = 60.7% of frame
  height, feet 924 on the floor in that framing, head 269, whole.
  Figure and room are scaled together; his size RELATIVE to the
  room furniture is unchanged. This is not a figure-only shrink.
- Square: a pull-back resize of the 1165x1165 master window
  (378,385)-(1543,1550) to 1080x1080, labelled pull-back, never
  presented as a centre crop.

Alternative that also keeps him whole: blurred pillarbox from the
new landscape (portrait-blurfill-room-scale file). It is weaker
for portrait-first viewing because the subject is smaller in the
pillarbox (608px tall in a 1920 portrait), so it is the backup,
not the recommendation.

## 5. Chair-back-at-waist — CONTRADICTION, reported not faked
Chair-back top in the KKGuh master is ~700 (visual estimate,
background y~286 x cover scale 2.449). Waist in the new master
is ~1003. Difference = 303px.
Forcing waist = chair-back with feet on the floor (1550) would
need figure height = (1550-700) / 0.47 = 1809px, head at -161,
i.e. head off-frame. At NO feet-on-floor scale in this KKGuh
arms-up crop does chair-back top equal waist.
Possible explanations, none assumed: the phrase may refer to
the apose layout-pass composition (different figure position),
to the chair armrest rather than the back top, or to a seated
pose. **Mars clarification is owed for this crop.**
The gate in this folder therefore hard-fails on scale ratio
and feet-on-floor, and reports chair-back as a WARNING with
numbers, never as a faked PASS. A builder that reports
chair-back PASS in this crop has not measured it.

## 6. Gate — mandatory, every time, every orientation
`check_room_scale.py <alpha_height> <feet_y> <master_height> [seated]`
- Standing: ratio 0.607 +/- 0.03, feet 1371..1700 in a 1920 master
  (scale proportionally for other master heights: feet must be
  on the rug plane, not above it, not below the frame).
- Seated: ratio 0.558 +/- 0.03 (0.607 x 2.3/2.5).
- If the gate fails, the builder exits 2 and produces NO delivery.
- This applies EVERY time he is shown in that room, at any scale,
  in any orientation, in any builder, including dual-orientation
  crops, contacts, and diagrams. A diagram that shows the old
  floating scale is a violation, even if it is "only a diagram".

## 7. Still owed
- Mars clarification: chair-back-at-waist in the KKGuh crop (see s5).
- Canonical room pictures from Mars; when they arrive, re-measure
  floor, chair, and scale in THAT room and re-issue this rule for it.
- Per-shot room-scale application beyond this arms-up proof (0/30).
- Approval of this fix: 0/1.
