# Cape Jones 2D Animation Post-Production Pipeline (2026)

Owner order 2026-10-19: pull the free 2D stack in, wire it up, prove it on Cape
Jones, then use it for the other shows. This doc is the map. Prove each stage on
a Cape Jones episode before calling it pipeline.

## Stage map

```
DRAW            RIG/TWEEN              INTERPOLATE (post)      COMPOSITE
Tahoma2D   →    Synfig            →    RIFE (Kaggle GPU)   →   OpenToonz
(hand-drawn     (vector keys +          (AI inbetweening          (node schematic:
 keys,           auto-tween,             of rendered               glows, multiplane,
 timeline,       bone rigs)              footage)                  particles)
 Xsheet)
   │                │                        │                        │
   └───────────────┤─────────────────────────┤───────────────────────┘
                                    │
                              FINISH (existing)
                    FLIPACLIP-POST-PIPELINE.md
        (grades → bloom → watermark removal → audio master → cards)
                                    │
                              Blender 5.2.3 LTS VSE / ffmpeg
                              (final assembly → MP4)
```

## Stage 1 — Draw: Tahoma2D (pinned 1.6)

Primary 2D workhorse. Hand-drawn frame-by-frame keys and breakdowns, Xsheet
timeline with implicit holds. Raster, smart-raster, or vector levels.
Doc: `production/tools/tahomad2d/README.md`

Output: PNG image sequences, or `.tnz` scenes (shared engine with OpenToonz).

## Stage 2 — Rig & Tween: Synfig Studio (pinned 1.5.5, stable fallback 1.4.5)

Vector keyframes + automatic tweening + bone/skeleton rigs. This is interpolation
**at the authoring level** — the tweener generates in-betweens from posed keys,
resolution-independent. Use for new animated shots built from our drawings.
Doc: `production/tools/synfig/README.md`

Output: PNG sequences → OpenToonz (compositing) or straight to Finish.

**Eval gate:** prove on one Cape Jones shot (rig → 3 keys → tween → render) and
document the result in `production/tools/synfig/README.md` before production use.

## Stage 3 — Interpolate (post): RIFE on Kaggle T4 (replaces ffmpeg minterpolate)

AI frame interpolation of **rendered footage**: Viggle AI clips, expression
montages, any choppy section. 12fps → 24fps on GPU in minutes (vs CPU hours).
Notebook: `production/kaggle/cape_jones_rife_kaggle.ipynb`
Docs + known-bug workaround: `production/kaggle/rife/README.md`

**Known bug (do not re-learn):** `kaggle kernels push` does NOT propagate
`dataset_sources` — attach datasets via the browser Input tab and verify before
running. Save & Run All (never Quick Save).

**Rule: episode interpolation goes through RIFE. `ffmpeg minterpolate` is fallback
only** (weakest quality on fast motion, CPU-only).

## Stage 4 — Composite: OpenToonz (pinned 1.8.0)

Node-based compositing schematic: levels → effects → composite → camera.
Glows, blurs, color, multiplane moves, particles. Closest free equivalent to
Toon Boom Harmony's compositor. Shares the Toonz engine with Tahoma2D (`.tnz`).
Doc: `production/tools/opentoonz/README.md`

Linux install: Flatpak `io.github.OpenToonz` (1.8.0). Upstream ships no Linux
binary.

## Stage 5 — Finish (existing, unchanged)

`production/pipeline/FLIPACLIP-POST-PIPELINE.md` — the proven chain:
grades (LED sequences, canon palette) → bloom → **watermark removal**
(`tools/watermark-removal/`: template-match + OpenCV Telea inpainting —
the Kiko-video method; black-box/blur cover-ups are banned) → audio master
(loudnorm + compressor + limiter) → bump cards → final MP4.

## Stage 6 — Final assembly: Blender 5.2.3 LTS VSE / ffmpeg

**Blender 5.2.3 LTS** (wired 2026-10-31 — see `production/tools/BLENDER-5X-UPGRADE.md`)
for 2D/3D hybrid shots (Grease Pencil), node-compositor bloom passes, and VSE
final assembly. ffmpeg for transcoding and delivery encodes.

## Handoff contracts (file formats between stages)

| From → To | Format |
|---|---|
| Tahoma2D → OpenToonz | `.tnz` scene, or PNG sequence |
| Tahoma2D → RIFE | MP4 or PNG sequence (via Kaggle dataset) |
| Synfig → OpenToonz | PNG sequence |
| RIFE → Finish | Interpolated MP4 / PNG sequence |
| OpenToonz → Finish | Composited PNG sequence / video |
| Finish → Delivery | Final MP4 (H.264 + AAC, +faststart) |

## What is NOT in this pipeline (and why)

- **Toon Boom Harmony** — industry standard, but closed-source, subscription-only,
  Windows/macOS only. Cannot run on our Linux stack, cannot be repo-integrated.
  Use the 14-day trial to *study* pro compositing/rigging technique, then replicate
  in the open tools above. No cracked copies — the free stack covers every stage.
- **Adobe Animate / Moho** — paid, no Linux. Nothing to pull.
- **ffmpeg minterpolate** — kept as fallback only; RIFE outclasses it.

## Already in the repo (don't duplicate)

- Krita — card art, cleanup/paint, textured backgrounds.
- `production/tools/pencil2d/` — lightweight 2D (PR #118).
- `production/tools/rhubarb-lip-sync/` — audio → mouth-shape timelines.
- `tools/watermark-removal/` — the correct AI pipeline (template-match + Telea).
- RIFE notebook + model (`production/kaggle/`).
- Blender 5.2.3 LTS (production default).

## Proving order (owner's order)

1. RIFE interpolation on a real Cape Jones choppy section — prove the GPU path.
2. Synfig eval lane — one rigged/tweened shot, documented.
3. OpenToonz composite of a finished shot — node schematic proven.
4. Full episode through all six stages — pipeline proven, then roll to other shows.
