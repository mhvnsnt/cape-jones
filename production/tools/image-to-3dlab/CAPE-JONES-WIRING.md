# CAPE-JONES-WIRING — AssetFurnace (Bingeljell/image-to-3dlab)

**Upstream:** https://github.com/Bingeljell/image-to-3dlab @ (pulled 2026-10-20, `main`, pushed upstream same day)
**License:** Apache-2.0 — own-eyes verified in-tree (`LICENSE`, Apache License Version 2.0). Free AND commercial-safe.
**What:** AssetFurnace — open-source image-to-3D pipeline. Prompt or picture in →
textured, rigged, animated game character out. Local-first: Apple Silicon or NVIDIA.
**Pull:** 16MB code-only (`--depth 1`, `.github/` stripped, upstream `AGENTS.md`/`CLAUDE.md`
renamed to `ASSETFURNACE-UPSTREAM-*` so they never collide with repo law files,
`docs/images/` marketing media pruned per convention). 422/422 `.py` pass
`py_compile`; `install.sh` passes `bash -n`; no model weights (GPU-lane download);
no binaries >2MB.

## Backends (all local, model weights NOT in repo — download on the GPU machine)

| Backend | Role |
|---|---|
| Pixal3D | image-to-3D (front+back, Pixel Match keeps text/logos sharp at ~5k faces) |
| TRELLIS.2 | image-to-3D alternative |
| Hunyuan3D | image-to-3D alternative (incl. `hunyuan_mlx/` for Apple Silicon) |
| SkinTokens | auto-rig (skeleton + skin weights, pure PyTorch — runs AMD/ROCm too) |

## Pipeline stages

`image_to_3dlab/` → Create (image/prompt → 3D) → Finish (decimate to ~5k faces,
compress, Pixel Match re-projects source pixels) → Rig (SkinTokens) → Animate
(21 move presets: walk/run/jump/dance/kicks, fitted so feet stay on the floor) → GLB.

CLI: `pipeline.py` / `lab` entrypoints. Studio: `viewer/` (Library + 3D viewer + Steps panel).
MCP: agent-driven asset generation (Claude Code / Codex MCP clients) — see
`ASSETFURNACE-UPSTREAM-AGENTS.md`.

## Cape Jones uses (GPU lane: Kaggle T4 / Colab)

1. **Character concept → 3D base:** reference art or Tripo GLB screenshot → textured
   game-ready humanoid → feed into our rig pipeline (Skintokens rig here vs
   `../skintokens-autorig/` standalone — same model family, compare bakeoff).
2. **Prop sheets:** one picture → separate props with LODs (living-room set dressing,
   Tekken-style stage props). Game-size compressed output.
3. **Animation presets:** 21 fitted moves as placeholder motion before custom mocap lands.
4. **License provenance:** every output carries a record of the licenses behind it —
   matches the owner's steal-like-an-artist documentation requirement.

## Synergy with existing tools in this repo

- `../skintokens-autorig/` — same SkinTokens family; cross-check rig quality.
- `../tripo-pull/` — Tripo models can be the "bring your own model" input.
- `../mpfb2/` — MPFB2 morphs apply to AssetFurnace humanoid bases.
- `../toon-shader/` / `../three-anime-style/` — cel-shade the finished GLB.
- `../natron/` — composite the GLB renders into show footage.

## Gotchas

- Weights are fetched at runtime (requirements + HF/cache) — never commit them.
- `install.sh` / `install.ps1` install system deps — run on the GPU machine, not the VM.
- README is marked "DRAFT for 0.4.0" upstream — treat docs as living.
