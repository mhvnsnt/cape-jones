# Crystal Cape Jones V2 — Transformation #4, chest-emblem origin
2026-10-31. Approval 0/1 for Transformation #4. No repo push. No existing file overwritten.
Transformation #3 is SAVED as Transformation Three (Mars, 2026-10-31 20:54 CDT:
"awesome, cool") — NOT overwritten, NOT reworked into #4.

## What Mars ordered
Instead of starting from the bottom of his cape, start from the centre of his
chest, around his emblem — the symbol on his chest. Save #3 as Transformation
Three, and make a Transformation Four that starts from his chest emblem.

## Emblem origin — VERIFIED from the plate, not guessed
Base plate: `rig-apose-v7c-clean-transparent.png` (1100x1500, mask 373,846 px).
Purple connected-component analysis of the chest found one small purple piece:
- bbox x539–562, y475–510, 474 px, centroid (550.8, 491.1)
- Origin used: **(551, 491)**
- Correction, stated plainly: the earlier future-symbiote diamond used centre
  (557, 502) / zone x540–575 y460–545. That was approximate and is ~6 px right
  / ~11 px low versus the measured purple emblem piece. #4 uses the measured
  piece. The old symbiote files are untouched. If Mars's symbol is a different
  chest shape, that zone still needs his correction — the measured purple
  piece is the best plate evidence available.

## Method
Same Preset 8 facet system as #2/#3: Voronoi, spacing 48, seed 7, 308 seed-grid
facets, **208 occupied facets** with actual pixels. Facets revealed by
Euclidean distance from the emblem centre + jitter (0–45 px, so the front is
organic, not perfect rings). Frontier = last 20 revealed facets, 60% crystal +
40% base + 25 brighten, plus a cyan (0,200,255) edge on the frontier boundary.
No spikes, no dust in #4 — those belong to #3; #4's read is the radial emblem
burst. Palette: cyan (42,126,207) / pink (213,123,206) / centre (128,136,219);
the vivid boost (0,200,255)/(255,110,210)/(140,120,255) was NOT used in the #4
frames (P8-06 file as-is). Base art never recoloured; grey in GIF/contact is
display-only; frames in `frames_t4/` are transparent RGBA.

## Measurements (20 frames @160 ms, 3.2 s loop)
- Frame 0: 10/208 facets = 4.8%, 21,714 px = 5.8%, revealed max distance 88.5 px
  (the emblem facets themselves).
- Frame 9 (50%): 104/208 facets = 50.0%, 199,786 px = 53.4%, revealed max
  distance 367.7 px — a radial disc around the chest: chest, shoulders and
  head are crystallised while legs/feet are still base. Head crystallises
  earlier than in #3 because it is nearer the chest than the feet are; that
  is correct radial behaviour, not a bug.
- Frame 19 (100%): 208/208 facets = 100.0%, 373,846 px = 100.0%, revealed max
  distance 815.5 px (farthest facet centroid, a foot/cape tip).
- End state: 100% P8-06 glint, V2 default power-on, same as #2/#3.

## Honest start-frame note (not hidden)
The GIF's first frame shows 4.8% revealed (10 emblem facets), following the
#2/#3 convention where frame k reveals (k+1)/20 of the order. True 0% is the
unmodified base plate itself, not a GIF frame. If Mars wants a 0% hold frame
at the head of the GIF, that is a trivial addition — it was not added here
so #4 stays directly comparable to #3 (20 frames @160 ms).

## Files (all new, in this folder)
- [transformation-4-chest-emblem-20261031.gif](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-4-chest-emblem-20261031/transformation-4-chest-emblem-20261031.gif)
- [transformation-4-chest-emblem-20261031.mp4](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-4-chest-emblem-20261031/transformation-4-chest-emblem-20261031.mp4)
- [transformation-4-contact-20261031.png](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-4-chest-emblem-20261031/transformation-4-contact-20261031.png) (frames 0, 4, 9, 14, 19 + DIAGRAM ONLY origin/rings tile)
- [build_transformation4.py](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-4-chest-emblem-20261031/build_transformation4.py)
- [measurements-20261031.json](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-4-chest-emblem-20261031/measurements-20261031.json) (all 20 frames)
- `frames_t4/` (20 transparent PNGs)

## Still owed
- Transformation #4 approval: 0/1 (Mars to save/log/approve; #3 approval stands
  separately and is NOT re-asked).
- Per-shot transformation application: 0/30. Animated glint sparkle in settled
  V2: 0/1. No repo push (landing is a separate step).
- This is a Crystal Form V2 transformation, NOT V1, NOT canon story effects.
