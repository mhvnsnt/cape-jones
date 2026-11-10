# Toon / Cel Shader — Cape Jones Wiring

**What:** the hard-shadow, no-gradient cartoon look for the Cape Jones
pipeline, as a **reusable system** (node-group spec + one-click apply script),
not per-material hand-wiring.

**Status: RECIPE, not a vendored add-on.** Researched 2026-10-18: there is no
dominant open-source Blender toon-shader with a clean commercial-safe license
to vendor. The landscape (StraySpark 2026 roundup,
https://www.strayspark.studio/blog/best-blender-toon-shader-addons-2026):

| Option | License | Verdict |
|---|---|---|
| Hand-built Shader-to-RGB node groups | free (your own nodes) | ✅ **this doc — the pull** |
| Free community node groups (itch.io etc.) | unclear / per-author | documented only — licenses not verifiable |
| Style Engine (StraySpark) | GPL-3.0, **$24.99** | paid — documented only |
| Pencil+ 4 Material | commercial | paid — documented only |
| ParaNormal Toon Shader | commercial | paid — documented only |
| Goo Engine (Blender NPR fork) | GPL (Blender fork) | open, but a full Blender fork — pipeline decision, not a pull |

## The system: CJ_Toon node group (spec)

Build **once** as a reusable node group, apply to every material. Works in
Eevee (Shader to RGB is Eevee-only; Cycles fallback uses Toon BSDF — see below).

**CJ_Toon (Eevee) — inputs:** `Base Color` (color), `Shadow Color` (color),
`Shadow Threshold` (float 0–1, default 0.5), `Rim Color` (color),
`Rim Strength` (float, default 0.0).

Node chain (all standard Blender nodes, no add-ons):

1. `Diffuse BSDF` ← Base Color → `Shader to RGB`
2. `Shader to RGB` → `ColorRamp` set to **Constant** interpolation, two stops:
   stop 0 = Shadow Color, stop 1 = Base Color, split at Shadow Threshold.
   **Constant interpolation = hard shadow edge, no gradient** (the look).
3. Rim (optional): `Fresnel` → `ColorRamp` (Constant) → `Mix` with Rim Color
   at Rim Strength → add over the cel result.
4. → `Material Output`.

**Outlines (required — flat shading without line work doesn't read as toon):**
`Solidify` modifier, flipped normals, material offset to a black
`CJ_Outline` material, thickness ≈ 0.002–0.005 at our 0.925 m scale. This is
the standard inverted-hull method; bake-safe and deforms with the rig.

**Cycles fallback:** replace steps 1–2 with a `Toon BSDF` (Diffuse, Size ≈
0.5, Smooth = 0.0 for the hard edge) → same Shadow Color ramp. Shader to RGB
does not exist in Cycles.

## One-click apply (script contract)

`tools/shading/apply_cj_toon.py` (to be written by the shading lane):
for each selected mesh — create/assign `CJ_Toon` material from the spec above
(building the node group if missing), set Shadow Color from the character
colorway (`#731AE5` family → shadow = base × 0.55), add the Solidify outline
modifier. Idempotent: re-running updates instead of duplicating.

## Lighting rules for the look

- One strong key (sun/area) for a single clean shadow terminator.
- Keep fill lights weak — competing lights create double shadow bands that
  break the cel read.
- World: flat mid-gray; no HDRI gradients fighting the bands.

## What was NOT pulled (honest)

- **Style Engine** ($24.99, GPL-3.0, Blender 4.2+): the best-priced dedicated
  option; revisit if budget allows — 7 styles, one-click, node groups stay
  editable. https://www.strayspark.studio
- **Goo Engine**: open Blender fork with renderer-level NPR features. Real
  commitment (version lag, add-on compat on us). Revisit as a pipeline
  decision, not a casual pull.
- Community itch.io node groups: quality varies, licenses unverifiable —
  never vendor what you can't license-check.

## Sources

- https://www.strayspark.studio/blog/best-blender-toon-shader-addons-2026
- Blender Manual: Shader to RGB (Eevee), Toon BSDF, ColorRamp interpolation.
