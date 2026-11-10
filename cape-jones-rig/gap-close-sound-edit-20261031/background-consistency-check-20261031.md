# BACKGROUND CONSISTENCY CHECK — 2026-10-31

Scope: 4 painted backgrounds + 4 new layout passes (`clean-100-20261031/layouts/`) + the locked room layout pass (5th).
`showcase/backgrounds-new-20261031/` flat vector files are EXCLUDED — per the layouts README they were NOT used and are NOT counted as final painted backgrounds.

Rule checked: room-only 2.5x scale applies to the room ONLY, never elsewhere. Feet on the ground plane, or a stated exception (airborne flying, seated desk). Horizon and light direction named per background.

| Background | Painted size | Layout pass | Scale / feet | Horizon | Light direction | Verdict |
|---|---|---|---|---|---|---|
| flying | 1168x784 | layout-pass-flying-painted-20261031.jpg (1168x784) | PASS (exception): airborne, plate 520px, feet y=550 over open sky, city far below | Low: skyline at bottom edge, open sky centre, large low moon | Dusk purple/gold sky; moon/sky glow above | PASS |
| rooftop | 1168x784 | layout-pass-rooftop-painted-20261031.jpg (1168x784) | PASS: plate 560px, feet y=750 on roof floor (corrected from y=690 inside parapet band) | Night skyline mid-frame, full moon above, roof slab + parapet below | Moonlight + lit windows, gold edge light | PASS |
| alley | 1168x784 | layout-pass-alley-painted-20261031.jpg (1168x784) | PASS: plate 560px, feet y=650 on cobbles, puddles foreground | Vanishing point: lit tower at alley end, walls both sides | Warm windows + tower light at end; puddle reflections | PASS |
| desk | 1168x784 | layout-pass-desk-painted-20261031.jpg (1168x784) | PASS (seated exception): seated plate 480px, pose bottom y=685 on rug in front of desk | Interior; window right with hills beyond (exterior horizon through window) | Warm lamp + window daylight right | PASS |
| room | (locked prior batch room) | layout-pass-room-scaled-25x-20261031.jpg (1168x1060) | PASS: ROOM-ONLY 2.5x correctly applied HERE ONLY — rig 950px, feet on floor/rug, chair back at waist | Interior floor plane under feet | Warm interior/lamp key | PASS |

Counts: checked 5, pass 5, fail 0, layout passes found 5/5. The 2.5x rule was NOT applied to flying, rooftop, alley, or desk (their plate heights are 480–560px, not the room's 950px scale).
Mars approval: 0 — all pending Mars's look. JSON: `background-consistency-check-20261031.json`.
