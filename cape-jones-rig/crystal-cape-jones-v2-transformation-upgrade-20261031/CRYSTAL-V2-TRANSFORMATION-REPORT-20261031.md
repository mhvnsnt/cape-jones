# Crystal Cape Jones V2 — Transformation #2 and #3, plus future all-black variant
2026-10-31. Approval 0/1 for all new work. No repo push. No existing file overwritten. Base art never recoloured.

## Naming, logged plainly (Mars, 2026-10-31 20:30 CDT, final naming supersedes his earlier uncertainty)
- Crystal Cape Jones **V1** = the earlier Crystal Cape Jones, already made before this pack.
- Crystal Cape Jones **V2** = this Preset 8 set (`crystallization-preset8-power-20261031/`), P8-06 facet-glint = default power-on look.
- **Transformation #1** = the existing transition GIF in that folder: feet-up sweep, 6 frames, 0% → 100%, a horizontal band by y-threshold. That is why it reads like an edit / crop edit.
- **Transformation #2 and #3** = the new animations in this folder, of transforming INTO V2. They are not new character forms.
- Do NOT confuse the two numbering systems: V2 is the form, #1/#2/#3 are transformation animations.

## What was built, all viewed by me before reporting
### Transformation #2 — facet creep from the feet
- [transformation-2-creep-20261031.gif](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/transformation-2-creep-20261031.gif)
- [transformation-2-contact-20261031.png](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/transformation-2-contact-20261031.png) (frames 0, 3, 7, 11, 15)
- 16 frames, 200 ms each, 3.2 s loop. Seed: 15 feet facets (centroid y ≥ 1180 or ymax ≥ 1250).
- Growth: BFS over facet adjacency, shuffled within each BFS layer, so the front is jagged and branching, not a straight horizontal line. Frontier = last 15 revealed facets, rendered 50% base + 50% crystal + 30 brighten, with a cyan (0,200,255) edge around the frontier.
- At 50% (frame 8): 104/208 facets, 184,848 px = 49.4% of mask, revealed facet centroids y 774.1–1268.8. Honest note: #2 still progresses bottom-up overall (it creeps UP him, by design), but its front is facet-irregular with branches into cape/legs, unlike #1's clean y-cut. If Mars wants a front that is even less bottom-up, #3 is the vein version.

### Transformation #3 — vein-first, shard spikes, Gaussian-dot dust
- [transformation-3-vein-shard-20261031.gif](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/transformation-3-vein-shard-20261031.gif)
- [transformation-3-contact-20261031.png](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/transformation-3-contact-20261031.png) (frames 0, 4, 9, 14, 19)
- 20 frames, 160 ms each, 3.2 s loop. Vein skeleton: centre feet→legs→torso→head, plus branches to both arms and both legs (polylines in `build_transformations.py`).
- Growth: facets sorted by distance to the vein skeleton, plus a small height term, plus jitter, so vein facets crystallise first and the crystal then fills outward — a branching, symbiote-vein read. Frontier = last 20 facets, 60% crystal + 40% base + 25 brighten.
- Shard spikes: on intermediate frames only, silhouette-edge frontier facets get an outward triangle 10–14 px, cyan (0,200,255). Spikes fade to 0 at the final frame, so the settled V2 is clean P8-06.
- Gaussian-dot dust: on intermediate frames only, 60 soft Gaussian-blurred dots per frame (cyan (0,200,255) / pink (255,110,210), radius 2.5–5.5 px) in not-yet-revealed facets just ahead of the front. This is a PIL proxy of the Gaussian Splatting point-field look, NOT a true splat render (see Gaussian section below). Dust fades to 0 at the final frame.
- At 50% (frame 10): 104/208 facets, 208,894 px = 55.9% of mask. Vein facets up the centre and arms are crystallised while large off-vein areas are still base — the opposite of #1's horizontal band.
- Both #2 and #3 end at 100% P8-06 glint, exactly the V2 power-on look, and start at 0% base plate. Neither is shot timing; they are transformation proofs.

### Facet-count correction, not hidden
The original Preset 8 report said "308 facets". That was the Voronoi seed-grid count (spacing 48 over the bbox). Occupied facets with actual pixels are **208**. All percentages in this folder use 208 occupied facets. The seed grid is still 308, spacing 48, seed 7, same as Preset 8.

## Future all-black symbiote variant — FUTURE ONLY, NOT V2, NOT canon
- [future-symbiote-contact-20261031.png](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/future-symbiote-contact-20261031.png)
- Left: [future-symbiote-black-white-symbol-WITH-cape-20261031.png](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/future-symbiote-black-white-symbol-WITH-cape-20261031.png)
- Right: [future-symbiote-black-white-symbol-NO-cape-20261031.png](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/future-symbiote-black-white-symbol-NO-cape-20261031.png)
- Body: all figure pixels (18,18,22), alpha verbatim from the base plate (373,846 px).
- Symbol: WHITE (255,255,255) only, centre chest diamond, zone x540–575, y460–545, diamond |x−557|/18 + |y−502|/42 ≤ 1. This is an approximate chest emblem identification — the head cowl purple was deliberately NOT recoloured white, because that would be a white cowl, not the symbol. If Mars's symbol is a different chest shape, that zone needs his correction.
- Cape consumed / loses cape: for y ≥ 600, alpha erased outside x380–720 (cape side flaps), legs kept. Alpha removed: 85,752 px (373,846 → 288,094). Limitation, stated plainly: above y600 the cape sits behind the shoulders and is black-on-black, so no difference is claimed there. True cape-piece separation would need the sliced cape pieces, not a zone erase. This variant is therefore a proof of the all-black + white-symbol + no-lower-cape read, not a finished cape-consumption animation. A cape-consumption animation (cape visibly being eaten / shrinking) was NOT built — that is still owed if Mars wants it animated.
- Mars said "maybe later" for this variant, so it stays FUTURE, approval 0/1, and V2 is unchanged by it.

## Methods — run vs mapping, labelled
### Industry-standard / creeping-growth methods, RUN as PIL/numpy/scipy CPU proxies
1. Facet-adjacency BFS propagation (cellular / diffusion growth) — RUN, #2.
2. Voronoi facet reveal (same facet field as Preset 8) — RUN, #2 and #3.
3. Growth-front glow (frontier mix + cyan edge, symbiote tendril edge read) — RUN, #2 and #3.
4. Vein / vascular branching growth (symbiote veins, crystal dendrites) — RUN, #3 skeleton.
5. Crystal nucleation / shard sprout spikes on the silhouette edge — RUN, #3, 10–14 px.
6. Gaussian-dot particle dust ahead of the front (Gaussian Splatting point-field idea) — RUN as PIL dots, NOT a true splat render.
7. Facet-by-facet dissolve reveal (VFX dissolve / pixel-dissolve transformation) — RUN, both.
8. Compositor overlay layering (base never recoloured, power as a layer) — RUN, inherited from Preset 8.
### Mappings only — NOT runs, with exact reason
9. Houdini / Blender Geometry Nodes true crystal-growth simulation — MAPPING, no simulation run on this VM, PIL facet proxy instead.
10. After Effects growth / shatter plug-ins — MAPPING, no After Effects licence on this VM.
11. Unreal Niagara / Substance symbiote tendril systems — MAPPING, no engine run, vein skeleton is a PIL proxy.
12. True 3D crystal growth (Blender Cycles glass, growing mesh) — MAPPING, only the earlier gem material reference exists, not a Cape growth render.
13. AI / ML video morph transformation — MAPPING, no model run, no morph claimed.
14. Vendor Gaussian Splatting CUDA training (gsplat / splatfacto) — MAPPING, no torch, no GPU, no paid run.

## Gaussian Splatting — pulled where it helps, name kept
Mars's speech "Gajin stuff / Gassian stuff" = **Gaussian Splatting**. Tool name stays Gaussian Splatting, not renamed.
Pulled: existing `gaussian-splatting-20261031/splat-front-20261031.png` (5,846 Gaussians, stride 8, sigma 3.2, IoU 0.6472, synthetic bulge depth) as the point-field reference for #3's dust colours and soft-dot look.
NOT claimed: no new gsplat/splatfacto run, no CUDA run, no true splat render of the crystal transformation. The dust in #3 is a PIL proxy, labelled as such in every file name and in this report.

## Honest limits / still owed
- #2's front is jagged but still bottom-up; #3 is the more branching, less sweep-like version. Neither is a true 3D growing crystal, neither is a vendor simulation.
- Face / eyes / muscle detail inside full crystal facets is still lost, as in Preset 8 — P8-07 mix-base remains the detail-preserving variant, not used as the transformation end state here (end state is P8-06, per V2 default).
- Cape-consumption animation: 0/1 (still proof only, see future variant limitation).
- Per-shot transformation application: 0/30. Animated glint sparkle in the settled V2: 0/1 (static glints only).
- All new work approval: 0/1. No repo push.

## Files
- Builder: [build_transformations.py](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/build_transformations.py)
- Measurements: [measurements-20261031.json](sandbox://workspace/cape-jones-rig/crystal-cape-jones-v2-transformation-upgrade-20261031/measurements-20261031.json)
- Frames: `frames_t2/` (16 PNGs), `frames_t3/` (20 PNGs), transparent, base alpha verbatim except crystal overlay.
