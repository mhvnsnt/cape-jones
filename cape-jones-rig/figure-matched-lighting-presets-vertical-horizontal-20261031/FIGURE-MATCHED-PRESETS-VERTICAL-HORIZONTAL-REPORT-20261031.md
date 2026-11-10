# Figure-matched lighting — presets + vertical / horizontal, 2026-10-31

Mars, 2026-10-31 23:00 CDT, replying to the figure-matched lighting per-room contact:
"Yo, these are all good, save those as all presets for their things that they're in
and then we'll continue to build on those in vertical and horizontal ways"

Status: original figure-matched set SAVED AS GOOD by Mars (saved-good, NOT upgraded
to full 1/1 approval silently). This folder: approval 0/1 preset set, 0/1 vertical set,
0/1 horizontal set separately. No repo push. No existing file overwritten.

## Presets, 8/8, each its own folder + spec + files

| Preset | Room / thing | Rim RGB | Lit mean RGB (source) | Direction | Gain |
|---|---|---|---|---|---|
| S1 | V2 warm overhead | 255,180,80 | 161.3,132.7,94.5 | overhead | 1.10,0.95,0.70 |
| S2 | V3 warm overhead strong | 255,190,90 | 169.8,140.0,99.9 | overhead_centre | 1.15,0.98,0.72 |
| S3 | V3+pools warm ground bounce | 255,185,85 | 171.7,140.1,98.2 | overhead_centre | 1.12,0.96,0.71 |
| S4 | Glare warm overhead glow | 255,180,80 | 156.9,128.8,91.4 | overhead | 1.10,0.95,0.70 |
| S5 | Colour magenta-rose | 255,178,229 | 214.6,127.1,166.6 | front | 1.25,0.70,0.90 |
| S6 | Colour cyan dual backlight | 0,200,255 | 94.9,149.5,175.5 | back | 0.90,1.05,1.15 |
| S7 | Colour golden-hour front | 255,180,80 | 195.5,159.2,109.1 | front | 1.10,0.95,0.70 |
| S8 | Colour cool-blue night | 160,200,255 | 143.1,163.2,210.7 | cool_front | 0.85,0.95,1.20 |

Shared method (from source report, not re-invented): cel bands 1.12/0.92/0.72 by
light direction; rim = dilate(figure,6) − figure; interior ink band = dark pixels
within 3 px of non-dark, recoloured 80% toward rim on the light side and toward
shadow on the away side, so pec/rib/ab/belt/gauntlet/cape-fold/cowl lines carry
light; interior sheen ≤14 px inside-edge band, up to 38% rim; S3 ground bounce
45% in the bottom 28% of the figure; ground bounce for other scenarios was not
specified in the source report and is recorded as not specified, not invented.
Base art never recoloured; lighting is on separate layers over a copy of the
clean plate.

Alpha discrepancy, recorded not hidden: source JSON figure_alpha_px = 374,127,
measured lit-transparent alpha = 408,573 (S4: 423,488). Source value preserved
verbatim in each preset JSON; measured value also recorded. Rim expansion in
the lit file is the likely cause.

## Vertical and horizontal, 8/8 each

- Source canvas: 1260×1660 (per scenario, on-room composite).
- Vertical (portrait): 1080×1920. Full source fitted to 1080×1423, scale 0.8571,
  paste (0,248). Backdrop behind it is a blurred cover of the same room only.
  Figure margins (S1–S3, S5–S8): left 253, right 252, top 517, bottom 499.
  S4: left 249, right 248, top 513, bottom 499. All margins > 0, no edge touch.
- Horizontal (landscape): 1920×1080. Full source fitted to 820×1080, scale
  0.6506, paste (550,0). Backdrop behind it is a blurred cover of the same room
  only. Figure margins (S1–S3, S5–S8): left 742, right 742, top 204, bottom 189.
  S4: left 739, right 738, top 201, bottom 189. All margins > 0, no edge touch.
- No-crop rule applied as: figure fully inside canvas, source fitted not cropped.
  The backdrop blur is room only; the figure layer itself is never cropped.
  This is NOT the 1920×1920 master / central 1080×1080 protected-square crop
  from dual-orientation-20261031 (that system crops a square master); here the
  whole 1260×1660 composite is preserved in both orientations, which is the
  correct no-crop choice for a room composite that is not a square master.
- Feet/ground: this is an arms-up plate, not a grounded standing shot, so no
  ground-line claim is made for these versions. Per-shot ground application
  remains 0/30 elsewhere.

## Files

- presets/<scenario>/PRESET-<scenario>-20261031.json (own spec per preset)
- presets/<scenario>/<scenario>-lit-transparent-20261031.png (copied, not recoloured)
- presets/<scenario>/<scenario>-on-room-20261031.png (copied source composite)
- presets/<scenario>/<scenario>-on-grey-20261031.png (copied)
- presets/<scenario>/<scenario>-vertical-1080x1920-20261031.png
- presets/<scenario>/<scenario>-horizontal-1920x1080-20261031.png
- preset-index-contact-20261031.png, vertical-contact-20261031.png,
  horizontal-contact-20261031.png (contact sheets only; labels on contacts are
  proof labels, not on the delivered preset files; vertical-contact label row
  is cramped/overlapping in the contact sheet itself, delivered files are clean)
- build_presets.py, PRESET-INDEX-20261031.json

Counts: presets 8/8 = 100%, vertical 8/8 = 100%, horizontal 8/8 = 100%.
