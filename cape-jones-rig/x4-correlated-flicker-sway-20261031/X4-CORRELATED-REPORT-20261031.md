# X4 Correlated Flicker-Sway — Report (2026-10-31)

## Mars's defect, confirmed, Mars is right
Old X4: ground shadow moves, character shadow does not. Verified in
`shadows-wire100-20261031/build_shadows.py`: the X4 loop recomputed
`ground_layers(..., light_dx+off)` per frame but reused the SAME
`cl["I4_form"]` built once. Ground moved, figure did not.

## Fix — one light parameter drives everything, per frame
`light_dx(frame) = 30 + off`. Same dx, same frame, same sign drives:
ground cast shear, form terminator, self-cast projection, lit-side rim.
AO is the one honest exception: AO is contact darkening, it does NOT
translate with the light; it only breathes slightly on the away side
(X-C2). That limit is stated, not hidden.

## Deliverables (new folder, approved X4 untouched, no repo push)
- [x4-CORRELATED-3f.gif](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/x4-CORRELATED-3f.gif) — 3 frames, offsets -6/0/+6, 400 ms
- [x4-CORRELATED-5f.gif](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/x4-CORRELATED-5f.gif) — 5 frames, offsets -8/-4/0/+4/+8, 300 ms
- [x4-OLD-defect-3f.gif](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/x4-OLD-defect-3f.gif) — defect reproduction, ground moves / figure fixed
- [old-vs-new contact](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/contacts/old-vs-new-contact-20261031.png)
- [diff contact, x4 amplified](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/contacts/diff-contact-20261031.png) — OLD panel black in the figure region; NEW panel shows the figure
- [Research](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/X4-CORRELATED-RESEARCH-20261031.md)
- [Builder](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/build_correlated_x4.py)
- [Measurements](sandbox://workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031/measurements-x4-correlated-20261031.json)

## Measurements — frame by frame (figure bbox 237,359,864,1400; centre 550; ground Gy 1400; rim 255,180,80; shadow tint 46,32,14)
3-frame NEW, ground centroid / terminator / self-cast / rim:
- off -6: ground 550.08, terminator 538, self-cast 47,797 px, rim 16,622 px
- off  0: ground 550.50, terminator 550, self-cast 45,360 px, rim 16,419 px
- off +6: ground 550.94, terminator 562, self-cast 41,693 px, rim 16,198 px
Gate NEW 3f: PASS — ground monotonic up, terminator monotonic up,
terminator delta +24 px (2 px per 1 px sway, as designed, expected
538/550/562 = measured 538/550/562 exactly).
Gate OLD 3f: FAIL — ground same 550.08/550.50/550.94, terminator
550/550/550, delta 0. That FAIL is the defect, measured, not eyeballed.
5-frame NEW: terminators 534/542/550/558/566, gate PASS, delta +32 px;
ground centroids 549.94/550.22/550.50/550.81/551.09, monotonic up.

Diff proof (f-6 vs f+6, x4 amplified, figure region x237-864 y359-1400):
- OLD: figure mean diff 0.0, 0 px >20 — the figure literally did not change.
- NEW: figure mean diff 3.27, 18,035 px >20 — the figure's shadow moved.
Ground diff is the same small blurred shift in both (mean 0.14), because
the static contact ellipse dominates the soft-shadow centroid; the
ground centroid move is therefore small (0.86 px over 3f) even though
the cast shear moves. Stated plainly: the headline movement in the NEW
version is the character terminator (+24 px), not a large ground
centroid jump. At thumbnail scale the form shift is subtle (smooth
0-0.28 gradient); the diff contact is where it reads clearly.

Gates: feet 1400 = Gy 1400 on every frame; figure inside 1100x1500;
figure alpha unchanged on every frame (character darkening applied to
a figure copy, alpha reset EXACTLY to the original, verified True);
ground layers behind the figure; character darkening inside figure only.

## Methods — industry 5 + experimental 5, all RUN
Industry: C1 single-key-light parameter; C2 form terminator tracking;
C3 self-cast projection; C4 lit-side rim tracking; C5 cast
length/direction coupling (shear = light_dx * (y-Gy)/120).
Experimental: X-C1 terminator-shifted cel gradient (2 px per 1 px sway);
X-C2 sway-phase AO breathing; X-C3 flicker-phase rim breathing;
X-C4 correlation gate (fails if ground and terminator do not move the
same sign — this gate would have caught old X4); X-C5 5-frame smooth
sway.
Mapping only, NOT claimed: Blender Cycles true 3D moving-light pass,
ray-traced shadow map, 3D-head Rembrandt triangle, mocap light rig.

## Bugs caught in-run, owned plainly
1. First build unpacked the canvas bbox as (x0,x1,y0,y1) instead of
   (x0,y0,x1,y1), giving centre 298 and width 122; terminator measured
   a constant 320 and the gate failed. Fixed; centre 550, width 627,
   terminator now matches expected exactly.
2. First self-cast used disjoint Y bands (caster y<659, receiver y>659),
   giving 0 px. Fixed with a downward projection (shift +40 y) onto the
   body; self-cast is now 41k-48k px and moves monotonically.

## Status
- Approved X4 (ground-only, 3-frame): APPROVED 1/1, untouched, still stands
  as the ground-only version.
- Correlated X4 pipeline (this folder): approval 0/1 separately.
- No repo push by this task.
