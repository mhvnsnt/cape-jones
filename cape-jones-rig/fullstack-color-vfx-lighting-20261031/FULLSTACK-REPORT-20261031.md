# Full-Stack Color / VFX / Lighting / Shadow / Keying — 20261031

Mars ordered 2026-10-31 23:42 CDT, replying to the preset index.
Mars's words (paraphrased in the task): cel shadow was really cool, all presets are really nice, exactly what he has been trying to go for, build more in those lighting/shadow directions, a mix of color, and 5 industry + 5 experimental full-stack projects wired 100% to work with VFX, lighting effects, color keying, shadows, lighting — all together.

Recorded: cel shadow (I4 form-shadow, cel gradient — Mars said "sail shadow", read as cel shadow) APPROVED 1/1, really nice. All presets are really nice, good, exactly what he has been trying to go for. Approved presets untouched here.

## Method — one pipeline, all five layers, every project
Order, every project: (1) COLOR — LUT/grade gains on a labelled test room; (2) VFX — shafts / glow / glints behind and around the figure; (3) LIGHTING — key rim colour, cel form gradient (I4), wrap 0.3, AO interior band <12px darkened 25%; (4) SHADOW — contact ellipse + cast (figure alpha squashed 28%, sheared by light dx) + cel form + AO; (5) COLOR KEYING — hue-keyed glow applied ONLY to pixels matching a hue class (purple / cyan / white / gold / face), blurred 10px.
Base art never recoloured in place: every step is a separate layer masked to plate alpha.
Base: rig-apose-v7c-clean-transparent.png, shifted +106 so feet = 1400, bbox (248,359,875,1400), figure alpha 373,846px. Ground line Gy = 1400.

## Industry 5 — all RUN
- F-I1 Golden Hour Hero — color warm grade (1.15,1.0,0.85); VFX god-ray shafts + warm glow; lighting rim (255,180,80), form x→0.78; shadow dx +30; keying purple glow (255,180,80) x0.4, key mask 9,731px.
- F-I2 Night City Neon — color night grade (0.85,0.95,1.2); VFX cyan neon rim glow + city shafts; lighting rim (0,200,255), form -x→0.72; shadow dx -120; keying cyan glow (0,220,255) x0.5.
- F-I3 Comic Dramatic Uplight — color comic grade (1.1,1.05,1.05); VFX underlight spot + AO drama; lighting rim (255,220,150), form -y→0.70 (uplight); shadow dx +60; keying face glow (255,200,120) x0.5, key mask 3,226px.
- F-I4 Desert Day Dappled — color day grade (1.1,1.05,0.9); VFX dappled shaft stripes on figure (x1.08 inside columns / x0.92 between) + ground; lighting rim (255,200,120), form y→0.78; shadow dx +30; keying gold glow (255,210,100) x0.4.
- F-I5 Dual-Light Split — color dual grade (1.05,0.95,1.05); VFX dual god rays warm front + cyan back, double shadow; lighting rim (255,180,80), form x→0.72; shadow dx +60 plus second cast -60; keying purple glow with cyan (0,200,255) x0.4.

## Experimental 5 — all RUN
- F-X1 Chroma Prism — color prism grade (1.1,0.95,1.15); VFX prismatic RGB edge shift (R -3px, B +3px inside figure) + light leak; lighting rim (255,120,220), form x→0.72; shadow dx +90; keying purple glow (255,100,220) x0.6.
- F-X2 Crystal Power — color crystal grade (0.9,1.1,1.2); VFX crystal cyan/pink glints + facet tint (x-split); lighting rim (42,126,207), form y→0.75; shadow dx +30; keying white-suit glow (42,200,255) x0.5, key mask 161,595px.
- F-X3 Ghost Outline — color ghost grade (0.85,0.9,0.95); VFX invisible outline + halo, desaturated ghost; lighting rim (0,200,255), form -x→0.72; shadow dx -60; keying cyan glow (180,245,255) x0.6.
- F-X4 Storm Flicker — color storm grade (0.9,0.95,1.15); VFX lightning flash + flicker sway shadow; lighting rim (160,200,255), form x→0.70; shadow dx +120; keying white glow (200,220,255) x0.5.
- F-X5 Ground Pool Dance — color pools grade (1.15,1.0,0.85); VFX floor pool glow + ground bounce, depth-gradient shadow; lighting rim (255,180,80), form y→0.78; shadow dx +30; keying gold glow (255,180,80) x0.5.

## Gates — all 10 PASS
Feet 1400 = Gy 1400, diff 0, all 10. Figure inside canvas 1100x1500, all 10. Figure alpha 373,846px unchanged by construction (ground behind figure, character layers masked to plate alpha; finals are RGB composites, alpha claim is by construction, not a byte-identical opaque test — that test does not apply once character shadows darken the figure). Rim 34,840px each (dilate 6 minus figure). Ground shadow px: I1 100,897; I2 100,958; I3 100,875; I4 100,897; I5 107,157 (dual); X1 100,893; X2 100,897; X3 100,934; X4 100,868; X5 99,497.

## Honest limits
- Rooms are labelled TEST gradient rooms, not prior renders, so the 10 are comparable. Shaft columns are the v4 columns [58,212],[267,418],[474,622],[679,832],[887,1041] applied as a VFX layer, not 10 separate Blender renders.
- Hue-key masks vary honestly with the figure's actual colours: cyan key = only 60px (this plate has almost no cyan), gold key = 284px, face key = 3,226px, purple key = 9,731px, white key = 161,595px. The keying step RAN on every project; on cyan/gold projects its visible effect is small because the key colour barely exists in the plate — that is a plate fact, not a hidden skip. A wider key (e.g. rim-colour key) would read larger.
- All 10 are 2D-plate composites (PIL/numpy), not Blender Cycles renders — no true 3D shadow pass claimed here.

## Status
Approval 0/1 for the industry 5 + 0/1 for the experimental 5 separately. Approved presets untouched. No repo push.
