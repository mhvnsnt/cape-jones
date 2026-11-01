# GROUP D — Effects / Depth / Style (experimental, 2026-10-31)

**Scope:** 5/5 projects researched, 5/5 with a viewed proof. **0/5 real models run.**
All proofs are METHOD-WIRED in PIL/numpy/scipy on this VM (no GPU, torch not
installed, no Natron binary installed). Nothing below claims a real model ran.
**Mars approval: 0/1 — do NOT claim approved. No repo push made.**
**Base art:** source pose never overwritten (md5 unchanged, see below); all
effects/flats are separate proof files, labelled REFERENCE / PROXY only.
No show character is shipped by this folder.

**Source frame (all proofs):**
`~/workspace/cape-jones-rig/pose-dialects-20261031/jojo-01-contrapposto-s-curve-20261031.png`
(1100×1500 RGBA, 370,701 opaque px; md5 `1c3a089232abceb9fb45ec08e302d1a4` before and after — unchanged)
**Builder:** `build_group_d.py` in this folder. Proofs in `proofs/`.

## Table

| # | Project | What it is / who made it | Experimental method | Exact Cape problem it helps | Free / paid | Wired status | Proof file (viewed) |
|---|---|---|---|---|---|---|---|
| 1 | ControlNet (depth / lineart conditioning) | Neural structure adding extra conditions to a frozen diffusion model; Lvmin Zhang, Anyi Rao, Maneesh Agrawala, Stanford, 2023, arXiv:2302.05543; checkpoints `control_v11f1p_sd15_depth` / `control_v11p_sd15_lineart` | Conditioning method, NOT a character generator: feed a depth map or lineart + text, model keeps structure, prompt decides style | Re-render / re-light a locked pose without redrawing it: depth keeps 3D arrangement + silhouette, lineart keeps outlines, while L0–L5 lighting / Sunbeam / afterglow change | Free / open (code + checkpoints, Apache-2.0 family; needs GPU + Stable Diffusion weights) | METHOD-WIRED — conditioning pack built, model NOT run | `proofs/01-controlnet-conditioning-pack-20261031.png` + `01-controlnet-conditioning-spec-20261031.json` |
| 2 | Style2Paints | AI lineart colourisation by Lvmin Zhang (lllyasviel); V4 is the first system to colourise in a real human workflow with LAYERED (PSD) output: flat colour, then shading/highlight, not a single flat JPG | Lineart + sparse colour hints / reference → flat fill → shading, layer by layer | Colourisation REFERENCE for a new flat pass: test a palette on a lineart before any hand repaint; never recolours base art in place | Free / open code (Apache-2.0 per project page); V4.5 Windows build free, needs Nvidia GPU; V5 preview unreleased at last check | METHOD-WIRED — hint workflow demo, model NOT run | `proofs/02-style2paints-method-reference-20261031.png` + spec JSON |
| 3 | Anime2Sketch / line extraction | Sketch extractor for anime/illustration/manga by Xiaoyu Xiang et al. (2021), from "Adversarial Open Domain Adaptation for Sketch-to-Photo Synthesis"; MIT licence; PyTorch + pretrained weights | Learned GAN extraction: colour art → clean binary lineart, removing colour/shading/texture, better than plain Canny/XDoG on anime line quality | Recover clean lineart from a coloured Cape frame so it can be re-flatted, re-lit, or fed to ControlNet-lineart / Style2Paints without redrawing | Free / open (MIT) | METHOD-WIRED — edge + XDoG-style proxy, model NOT run | `proofs/03-anime2sketch-line-extraction-proxy-20261031.png` + spec JSON |
| 4 | Natron | Free open-source node-based compositor (GPL-2.0), started by Alexandre Gauthier (2012), Nuke-style node graph, OpenFX 1.4 plugins; upstream community-maintained, Qt5-era | Node graph: Read → Grade → Rim/Glow → Merge → Write, each pass a separate node/layer, non-destructive | Free compositor for rim/wrap/glow passes (L2 warm grade + amber rim 255,180,80) as an alternative to the Blender compositor, with a readable node graph Mars can audit | Free / open (GPL-2.0) | METHOD-WIRED — node graph + composite built in PIL, Natron binary NOT run | `proofs/04-natron-node-graph-20261031.png`, `proofs/04-natron-composite-proof-20261031.png` + spec JSON |
| 5 | MiDaS / Depth Anything (monocular depth) | Single-image depth: MiDaS (Ranftl et al., 2020, robust mixed-dataset training, relative depth); Depth Anything (Lihe Yang et al., HKU/TikTok, 2024, ~62M unlabeled images, Apache-2.0) — the current stronger successor, sharper on unseen images | One 2D frame → per-pixel relative depth map (near/bright, far/dark); relative, NOT metres, unless calibrated | Depth maps for 2.5D parallax, layer ordering, and rim/wrap falloff: which limb is in front, how far a glow wraps, without building a 3D model | Free / open (MiDaS + Depth Anything code Apache-2.0; weights free for research use — check weight licence before shipping) | METHOD-WIRED — silhouette-distance pseudo-depth, models NOT run | `proofs/05-midas-depthanything-pseudo-depth-20261031.png` + spec JSON |

## What was actually viewed (honest QC)

- **01 ControlNet pack — GOOD.** Original / depth / lineart read clearly side by side.
  Lineart is clean and pose-faithful. Depth panel is the weak one (see #5).
- **02 Style2Paints — WORKFLOW DEMO ONLY, not a true colourisation.** Lineart panel
  is good; hint dots are blindly sampled (two land on cape/black, one below the
  feet) and the "flat" panel is a quantized copy of the original, NOT a
  hint-driven fill. Useful only to show the hint → flat workflow shape. A real
  Style2Paints run (or hand flat) is still needed before any palette decision.
- **03 Anime2Sketch proxy — GOOD for a proxy.** Edge lineart is clean and complete;
  XDoG-style panel is fainter but still readable. Real Anime2Sketch should beat
  this on thin interior lines and line breaks — this proxy over-keeps texture edges.
- **04 Natron — NODE GRAPH GOOD, rim SUBTLE.** Graph reads clearly
  (Read → Grade → Rim → Merge → Write). Composite's background + grade change is
  visible; the amber edge rim is barely visible at sheet scale and needs a
  zoomed rim-only check before it is trusted for L2 rim proof.
- **05 MiDaS/Depth Anything proxy — WEAKEST, labelled as such.** Silhouette-distance
  depth makes the torso bright and thin limbs (arms/legs/cape edges) dark, which
  is the OPPOSITE of true body-part depth (a forward fist should be near, not dark).
  The parallax demo therefore shows a visible split seam down the torso.
  Conclusion: silhouette distance is NOT a substitute for a learned depth model;
  it only proves the parallax plumbing (near/far split + shift + merge).

## Most promising project — and why

**MiDaS / Depth Anything (project 5), despite having the weakest proxy.**
Reason: it is the only project in this group that unlocks something Cape does
not already have another way to do. Lineart extraction (#3) and colourisation
reference (#2) are useful but replaceable by hand; ControlNet conditioning (#1)
is powerful but needs #5's depth map to work well for 2.5D; Natron (#4) duplicates
the Blender compositor already in use. A real Depth Anything Small run on a free
GPU (Kaggle/Colab, per the free-way-around rule) gives per-limb relative depth
from a single frame — the missing input for 2.5D parallax, front/back layer
ordering, and depth-graded rim/wrap. Next step is exactly that one run, then an
A–B: real depth vs this proxy on the same pose. If the real depth also fails on
thin limbs, the fallback is hand-assigned per-limb depth layers, not more proxy.

## Next steps (in order, none done yet)

1. Depth Anything V2/V3-Small on Kaggle/Colab free GPU on this same pose;
   compare to `05-…-pseudo-depth` and record which limbs it gets right/wrong.
2. Real Anime2Sketch run (PyTorch + weights) on a coloured frame; compare line
   breaks against the proxy in `03-…`.
3. Real Natron install + the same Read→Grade→Rim→Merge graph, OR a documented
   decision to stay on the Blender compositor — do not adopt the 2026 Windows-only
   community Natron fork (self-described vibe-coded) sight-unseen.
4. ControlNet depth+lineart conditioning test only AFTER step 1 gives a real depth
   map; conditioning is not a character generator and must not be used to invent
   a new character.

## Sources (web search, 2026-10-31)

- ControlNet: Zhang, Rao & Agrawala, "Adding Conditional Control to Text-to-Image
  Diffusion Models", arXiv:2302.05543 — https://www.ultralytics.com/glossary/controlnet
- Style2Paints: V4 layered human-workflow colourisation, Apache-2.0 code —
  https://githubhelp.com/lllyasviel/style2paints
- Anime2Sketch: Xiang et al. 2021, MIT, PyTorch + weights —
  http://gitmemories.com/Mukosame/Anime2Sketch
- Natron: GPL-2.0 node compositor; community fork status (Qt6/Cycles, Windows-only,
  2026-09-15) — https://discuss.pixls.us/t/natron-fork-3d-system-cycles-renderer-deep-particles-and-more-windows-build/60644 ;
  FreeBSD port expired 2026-09-30 (Qt5 WebEngine) — https://www.freshports.org/graphics/natron/
- Depth Anything: Yang et al. 2024, ~62M unlabeled, Apache-2.0 —
  http://arxiv.org/html/2401.10891v2/ ; MiDaS lineage via the same paper's comparison
  to MiDaS v3.1.

## Counts

- Projects: 5/5 researched, 5/5 with viewed proof, 0/5 real models run, 0/5 paid installs.
- Proof files: 6 PNGs + 5 JSON specs = 11 files in `proofs/`, plus `build_group_d.py`.
- Repo pushes: 0 (per task). Mars approval: 0/1.
