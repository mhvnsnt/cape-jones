# EFFECTS WIRING MAP — 12 Effects V2 systems → CJ shots (2026-10-31)

COORDINATION, not rebuild: the 12 V2 proofs in `showcase/effects-v2-proof-20261031/` are NOT rebuilt here. This map wires them to shots from `shot-specs-30-20261031.json` + `god-ray-placement-30-20261031.json`. Shot specs carry no `effect_systems` field, so anything only inferable is PROPOSED, not counted as wired. Nothing is hidden: unwired systems are listed as unwired.

Counts: 12 systems — WIRED 4 (systems 1, 2, 5, 6) · PROPOSED 5 (3, 4, 7, 9, 10) · UNWIRED 2 (8, 11) · GATE 1 (12, applies to all wired shots). Shots with ≥1 wired system: 10 (CJ-03 + the 9 god-ray shots). Shots with no wired system: 20.

| # | System | Status | Shots | Production method | Gate (spill / shadow / atmosphere) |
|---|---|---|---|---|---|
| 1 | Volumetric god rays | WIRED | CJ-11, CJ-12, CJ-13, CJ-14, CJ-19, CJ-22, CJ-28, CJ-29, CJ-30 | Blender Principled Volume cube + Spot; Glare Sun Beams added back | atmosphere + shadow |
| 2 | Bloom / glow + spill | WIRED | CJ-03 | Emissive + Point light; Glare Fog Glow, Mix ADD | spill |
| 3 | Haze / fog shifting with grade | PROPOSED | CJ-11..CJ-30 god-ray set (proposed) | World/bounded volume, Noise into Density | atmosphere |
| 4 | Particles (dust/sparks/embers/rain/snow) | PROPOSED | CJ-03 (via system 5 dust burst) | Blender particles, emissive instances | atmosphere + shadow |
| 5 | Impact shockwave + dust + flash | WIRED | CJ-03 | Ring 0.2→3.0 + flash 1500→0 over 3f + dust burst | shadow + atmosphere |
| 6 | Fire / energy aura, flickering | WIRED | CJ-03 | Emissive aura + flickering Point light + Fog Glow | spill + shadow |
| 7 | Water / reflection / wet sheen | PROPOSED | CJ-08, CJ-30 | Roughness 0.15 puddle mask; flipped copy 0.35 opacity | spill |
| 8 | Smoke / steam | UNWIRED | — (none) | Volume Density 0.05 + rim Spot | shadow + atmosphere |
| 9 | Motion blur + speed lines | PROPOSED | CJ-02, CJ-14 | Vector Blur samples 32 + lines along limb arc | atmosphere |
| 10 | DOF + lens (bokeh, flare) | PROPOSED | CJ-28, CJ-29 | Camera DOF f/2.8 + Defocus + Glare Streaks | spill |
| 11 | Electricity / lightning | UNWIRED | — (none) | Bolt + flash 0→4000→0 over 4f + shadow pop | shadow |
| 12 | Shadow casting from effects | GATE | All wired shots (CJ-03, CJ-11–14, CJ-19, CJ-22, CJ-28–30) | All effect lights use_shadow; ground receives | shadow |

Still owed: per-shot production VFX frames (the V2 proof frame is generic, not per-shot); `effect_systems` fields in shot specs for the 5 proposed systems before they count as wired; Mars approval of all wiring (0). JSON: `effects-wiring-map-20261031.json`.
