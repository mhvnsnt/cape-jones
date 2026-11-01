# Color key + lighting + VFX — 10 industry-standard pieces, wired together, 2026-10-31
Cape Jones color keys: 6 sheets, 30 panels total, all viewed 2026-10-31.
- Lighting conditions sheet: daylight, night city, warm interior, purple, blue spotlight (5)
- Sheet 1: Golden Hour, Rainy Night, Warm Lamp, Fluorescent, Spotlight (5)
- Sheet 2: sunset rooftop, neon alley pink/cyan, kitchen daylight, purple neon, blue warehouse (5)
- Sheet 3: overcast, fire, underwater, red alert, neutral (5)
- Sheet 4: Desert Sun, Foggy Morning, Candlelight, Green Night Vision, Warm Sunset (5)
- Sheet 5: City Noon, Stormy Night, Cozy Fire, Cyan Cyber Light, Natural Window Light (5)

## The 10, in compositing order — use them together, not alone
1. Color script / color keying (Pixar/Disney TVA standard) — pick the key per scene from the 30 above,
   before any shot is built. Why it goes hard: the whole episode reads as one colour story, not random shots.
2. Rim light + environment bleed (Cape Jones's own rule, 2-4px, Add) — cyan for void, pink for neon,
   red for fire/nebula, strictly on rim/glow, suit stays white.
3. Node compositing (Nuke standard, free: Natron; also Blender Compositor) — every effect below is a node,
   editable per shot, not baked paint.
4. Glow / bloom (After Effects Glow, Blender Glare fog-glow + streaks) — energy, neon, spotlight halos.
5. Color Dodge / Add energy (After Effects / Photoshop standard) — gauntlet core white Normal,
   outer glow #FFB300 Color Dodge/Add, sparks above line art.
6. LUT grading (ACES / DaVinci Resolve standard, .cube files) — neutral/warm/cool templates already built,
   plus per-key LUTs (golden hour warm, rainy night cyan/pink, etc.) — still to grade per key, not just per shot.
7. Volumetric light / god rays (spotlight, candlelight, desert sun keys) — light cone + fog, Add, low opacity.
8. Wet / reflective surfaces (rainy night, neon alley keys) — Screen/Add reflections on floor, neon bleed on wet ground.
9. Fog / atmosphere / depth haze (foggy morning, desert keys) — blurred grey layer, distance fades, character stays sharp.
10. Hard shadow + contact shadow (TV cutout standard) — hard shape, no soft multiply wash, per Cape Jones sheet rule.
    Bonus, already in VFX sheet: smear / speed lines, burst, impact, lightning arcs, energy beams.

## Order that makes them stack, not fight
Background -> color key tint -> character -> hard shadow -> rim (environment colour) -> energy (Add/Color Dodge)
-> glow/bloom -> volumetric cone -> fog -> foreground -> LUT -> delivery.
If rim and energy use different environment colours in one shot, rim wins for silhouette, energy wins for glow —
never tint the whole suit to the environment colour. That is the sheet rule, and it is what keeps the white suit readable
in every one of the 30 keys above.

## Built demo
showcase/color-key-vfx-stack-combined.jpg — night skyline + spotlight cone + fog + pink neon rim + gauntlet glow,
all 5 stack pieces in one frame, viewed 2026-10-31. Demo, not a final shot.
Still left: per-key LUTs for all 30 keys, per-shot compositing in Natron/Blender (not PIL),
wet reflection pass, and Mars's specific picks.
