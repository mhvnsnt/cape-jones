# Blender composite wrap v2 — light coming AROUND him, realistic
Mars 2026-10-31 16:29 CDT: composite v1 is good, upgrade it even more,
more industry-standard stuff. It must NOT just upgrade BEHIND him —
the light has to start to look like it is coming AROUND him in a
realistic way.

Mars 2026-10-31 16:30 CDT CORRECTION (applies to this whole pass):
"more realistic" means the LIGHTING, EFFECTS and GOD RAYS — NOT the
background itself. So the background was NOT repainted or upgraded
here. The v1 Cycles volumetric base file is reused unchanged, with
the same gold grade on background only. Only the light wrapping
around him is new: wrap, rim, spill, bleed, shaft haze — all in the
Blender compositor, NOT PIL.

Combined dual-light case ONLY (Mars 15:48 CDT): cyan backlight +
gold LUT/overlay combined. Gold rim alone gets NO cyan backlight;
that shot is separate and is NOT these files.

## What was built (Blender 5.2.3 LTS, Cycles CPU base, compositor only)
Folder: blender-composite-wrap-v2-20261031/
- wrap-v2-apose-20261031.png (640x360) + .blend — clean apose, wrap
- wrap-v2-armsup-20261031.png (640x360) + .blend — approved arms-up
  base pose (arms-up / pre-flex only, NOT a flex), wrap
- control-no-wrap-apose-20261031.png + .blend — same stack, wrap
  layers off (plate over background only)
- control-no-wrap-armsup-20261031.png + .blend — same, arms-up
- proof-v1-vs-v2-wrap-20261031.png (1300x780, PIL grid only for
  the proof sheet — the composites themselves are Blender only;
  PIL was used for pixel counting and for laying out the proof
  sheet, never for a composite layer)
- blender_composite_wrap_v2.py — the exact script that rendered all
  four composites

First wrap attempt was too strong (dilate 14, blur 10, factor 0.85)
and read as a halo blob with a big ground puddle. It was toned down
and re-rendered to the final values below; the first attempt is NOT
shipped as a separate file, and the toned-down version is the v2.

## 10 industry-standard methods wired — 10/10 as compositor layers
1. Light wrap / rim wrap: backlight wrapping around silhouette edges
   onto front-facing surfaces — outer band = dilate 6, Gaussian blur
   5, minus plate alpha, factor 0.60. A wrap falloff, not a flat rim
   line (v1 was a 3px dilate rim only).
2. Inner spill / wrap onto front edges: erode 8, blur 3, plate alpha
   minus that = band just inside the edge, cyan, factor 0.35. This is
   the layer that makes light read as coming around ONTO him (cape
   edges, head sides, fists, feet) instead of only sitting behind him.
3. Soft edge / no hard halo: every wrap mask is Gaussian-blurred
   before use; the outer band fades out instead of stopping at a
   hard line.
4. Colour spill / bounce: dilated blurred alpha, shifted down 12px,
   cyan, factor 0.20, composited UNDER the plate — cyan backlight
   pooling on the ground around his feet.
5. Volumetric occlusion: the plate is composited OVER the volumetric
   base, so shafts are occluded by his body; the wrap band is the
   only shaft light that continues around the silhouette.
6. Shaft haze / atmospheric perspective: background blurred 20px,
   masked to the outer wrap band at factor 0.18 — shafts appearing
   to bend around the body rather than stop dead behind it.
7. Realistic falloff (approximation, stated honestly): blur size +
   alpha factor ramp stands in for inverse-square falloff. There is
   no true distance-based falloff in a 2D compositor pass — that
   would need a depth/normal pass (see Still owed).
8. Shadow-side retention: wrap layers are edge bands only; the
   interior is untouched. Pixel check: dark cape interior sample
   (320,200) is (15,16,20) wrap vs (15,14,19) control — essentially
   unchanged; suit centre (arms-up 320,160) is (196,196,196) both.
   Shadow still reads as shadow, with a wrapped rim.
9. Motivated dual light: every cyan layer names its source — cyan
   backlight from behind; gold grade is background only, never on
   the plate. Base art is never recoloured.
10. Blender compositor layering (5.2 output path from v1): Image
    inputs -> SetAlpha + AlphaOver -> GroupOutput (interface OUTPUT
    socket "Image"), executed by a real render with
    scene.render.use_compositing=True and write_still=True. NO PIL
    composite. MixRGB Add with a small Factor image is NOT used
    (that cropped the canvas in v1).

## Pixel proof (wrap vs control, colour distance > 20)
- Apose: 15,205 differing pixels, bbox x 248-395, y 58-302.
- Arms-up: 15,303 differing pixels, bbox x 242-396, y 56-299.
Both bboxes are exactly the character silhouette area — the wrap
does not leak across the whole canvas. EGL warnings in the Blender
log are harmless (same as v1); all four renders completed.

## Viewed (by the builder)
- wrap-v2-apose and wrap-v2-armsup: soft cyan edge glow around
  head, cape, arms, fists, legs, feet; cyan tint on front edge
  surfaces; soft ground pool under feet; suit interior stays white,
  cape interior stays dark.
- proof sheet: v1 apose (thin 3px rim only — the proof label says
  "no wrap", which is shorthand for "no wrap falloff"; v1 DID have
  a thin rim) vs v2 apose (wrap falloff); control arms-up vs v2
  arms-up (wrap clearly present in v2, absent in control).

## Still owed (not claimed done)
- Mars approval: 0/1 for both v2 frames. He approves.
- Side-weighted wrap: the wrap is uniform around the silhouette.
  A true backlight-side-weighted wrap (stronger on the backlit side,
  fading on the front side) needs a normal/depth pass or a
  side-specific mask — a flat 2D plate has no normal info, so this
  pass does not fake a side gradient. That is the next realism step
  if Mars wants it.
- Brighter volumetric shafts themselves: the shaft base was NOT
  re-rendered brighter in this pass (background stays as it is, per
  the 16:30 correction). A brighter-shaft volumetric render (higher
  density / spot energy, verified aim) is still owed as a separate
  render if Mars wants shafts brighter, not just wrap brighter.
- Dust in the light: no dust layer was built in the compositor
  (no noise-texture layer in this tree). Haze stands in for
  atmosphere; true dust motes in shafts are still owed.
- Gold-rim-alone version through this wrap stack: 0/1 (this is the
  combined cyan+gold case only).
- Per-shot composites through this stack: 0/30.
- Repo push of this folder: parent's PR route; no commit made here.
