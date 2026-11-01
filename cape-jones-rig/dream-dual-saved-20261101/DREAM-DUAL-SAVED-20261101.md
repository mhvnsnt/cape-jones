# DREAM + Dual-Light — Saved, Full Size, Dream 1–10

Mars, 2026-11-01 00:03 CDT, replying to DREAM + dual-light contact: "All are awesome save all and show me the dream ones full size and save dream 1 and 2 as presets and we make 8 more"
Clarification, 00:03 CDT: bottom 2 = dual-light V3 and V4, save BOTH as preset OPTIONS, named, not defaults, no pick between V3/V4.

Recorded: DREAM A, DREAM B, dual-light V3, dual-light V4 — ALL AWESOME, SAVE ALL. No pick between A/B or V3/V4 is made here.

## 1. Saved all
- Dream 1 = DREAM A: cape FULL magenta-pink (255,60,180), helm/cowl turquoise (40,200,210), suit WHITE (255,255,255), skin pink-tinted (255,200,180), eye ice (220,250,255). Source: jojo-shift-variation-20261031/jojo-dream-dream-a-cape-full-suit-white-20261031.png, 1100x1500.
- Dream 2 = DREAM B: same cape/helm, suit GOLD (255,205,90), suit_shadow (200,150,70). Source: jojo-dream-dream-b-cape-full-suit-gold-20261031.png, 1100x1500.
- Dual-Light V3 preset OPTION, named: gold-inner / cyan-outer. Source: dual-light-variants-20261031/v3-gold-inner-cyan-outer-20261031.jpg. OPTION, NOT a default.
- Dual-Light V4 preset OPTION, named: cyan-inner / gold-outer. Source: dual-light-variants-20261031/v4-cyan-inner-gold-outer-20261031.jpg. OPTION, NOT a default.

## 2. Full size DREAM
- Dream 1 full size: dream-1-fullsize-20261101.png, 1100x1500, original file copied, untouched.
- Dream 2 full size: dream-2-fullsize-20261101.png, 1100x1500, original file copied, untouched.
- Preset folders: presets/dream-1/PRESET.json + dream-1-20261101.png; presets/dream-2/PRESET.json + dream-2-20261101.png.
- Dual preset folders: presets/dual-light-v3/PRESET.json + dual-light-v3-20261101.jpg; presets/dual-light-v4/PRESET.json + dual-light-v4-20261101.jpg.

## 3. Dream 3–10 (new, 8 more)
Method: same nearest-base-colour recolour as jojo-shift-variation build_variation.py, base rig-apose-v7c-clean-transparent.png, dist>110 untouched, black outline never reassigned. Rim: thin 6px, dilate(alpha,6)-alpha, in the preset's cape colour, plate pasted AFTER rim, interior preserved 100%.
Bug caught and fixed in-run, owned plainly: first numpy build used int16 for colour distances, which overflowed on large colour differences (e.g. white vs black) and left capes black / mis-mapped. Rebuilt with int32 distances; cape pixels verified (Dream 3 cape centre (0,199,254), Dream 7 cape centre (253,254,254)). First broken contact was NOT delivered.
- Dream 3 — Cyan Cape: cowl (255,60,180), suit white, cape (0,200,255), rim (0,200,255)
- Dream 4 — Red Cape, Violet Helm: cowl (140,80,220), suit (200,210,220), cape (255,60,60), rim (255,60,60)
- Dream 5 — Green Cape, Orange Helm: cowl (255,140,40), suit white, cape (60,220,120), rim (60,220,120)
- Dream 6 — Purple Cape, Gold Suit: cowl (40,200,210), suit (255,205,90), cape (140,60,255), rim (140,60,255)
- Dream 7 — White Cape, Black Suit: cowl (255,60,180), suit (20,20,30), cape (255,255,255), rim (255,255,255)
- Dream 8 — Teal Cape, Lavender Suit: cowl (255,205,90), suit (200,180,255), cape (0,180,180), rim (0,180,180)
- Dream 9 — Orange Cape, Blue Helm: cowl (40,100,255), suit white, cape (255,120,40), rim (255,120,40)
- Dream 10 — Light Pink Cape, Cyan Suit: cowl (60,220,120), suit (180,240,255), cape (255,120,220), rim (255,120,220)
All 8: 1100x1500, alpha>0 416,053px (figure + 6px rim), inside canvas, no-crop PASS. Each in presets/dream-N/ with PRESET.json + dream-N-20261101.png. Builder: build_dream_3_10.py. Measurements: dream-3-10-measurements.json.

## Approvals
- Dream 1 preset: approval 0/1 separately.
- Dream 2 preset: approval 0/1 separately.
- Dual-Light V3 option: approval 0/1 separately (as an option, not a default).
- Dual-Light V4 option: approval 0/1 separately (as an option, not a default).
- Dream 3–10: approval 0/1 for the 8 new ones separately.
- "All are awesome, save all" from Mars is the save order, not a preset approval vote for Dream 3–10 — those are new and unapproved.
- No repo push by this job. No original touched.
