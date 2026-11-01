# Compositing, lighting, color keying — wired spec, 2026-10-31
Source of truth for Cape Jones's own rules: characters/sheets/03-color-lighting-vfx-key.jpg
and characters/sheets/color-keys/color-key-lighting-conditions.jpg, viewed 2026-10-31.
No other show's characters, names, logos, or dialogue are in this spec — only systems.

## Cape Jones's own rules (from his sheets, verbatim numbers)
- Base palette: Suit #FFFFFF, Cowl #3E1473, Skin #E5B28C, Cape #000000
- No gradients, no dirt passes, stay blown out, hard vector shape, no multiply (for the character shape)
- Rim light: 2-4px, Cyan / Environment Light, use rim to separate silhouette from void,
  environment bleed on rim ONLY
- Gauntlet energy: Core blast Pure White #FFFFFF (Normal blend),
  Outer glow #FFB300 (Color Dodge / Add blend),
  Energy & sparks OVERLAP black line art (i.e. energy is above line art, not under it)
- Environment color bleed: Suit base stays White. Apply environment tint strictly to outer rim and energy glow.
  Example on sheet: red nebula -> red tint on rim/glow only, suit stays white.
- Lighting conditions (color-key sheet, 5 panels): daylight, night city, warm interior, purple, blue spotlight.
  Suit tint changes per condition, cape stays black.

## Highest industry standard stack wired for this (free first, then paid standard)
Layer order, bottom to top:
1. Background (painted)
2. Character (hard vector, no multiply)
3. Shadow / contact (hard shape, not a soft multiply wash — per sheet rule)
4. Rim light (Add, 2-4px, cyan or environment colour, dilated silhouette mask — built in showcase/compositing-rim-light-cyan.jpg)
5. Energy core (Normal, white) + outer glow (Color Dodge/Add, #FFB300) + sparks (above line art)
6. Foreground
7. Grade LUT (.cube, neutral/warm/cool templates already built)
8. Delivery (FFmpeg, -14 LUFS)
Tools, free: Natron (node compositing, Nuke-like, free — the high-level node stack for this),
Blender Compositor + Glare node (fog glow, streaks), OpenToonz, Krita.
Tools, paid standard (for reference, not required): After Effects (Glow, Add, Screen, Color Dodge),
DaVinci Resolve Fusion (node compositing), Toon Boom Harmony (node compositing).
Why Natron/Blender are above layer tools for this: rim, glow, and bleed are node operations
(mask -> dilate -> colour -> Add) that stay editable per shot, not baked paint.

## What is built, what is still template
Built and viewed: rim light composite (cyan, night skyline), gauntlet energy rings (white core, #FFB300, cyan ring, sparks),
color-key strip (5 conditions, tint multipliers).
Still left: per-shot compositing (each shot gets its own rim colour from its background),
energy beam / lightning arcs as separate FX pieces, bloom/glare pass in Blender/Natron (not just PIL),
and Mars's specific picks from these sheets — which is the next step, per his message.
