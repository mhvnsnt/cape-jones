# CAPE-JONES-WIRING.md — BlenderTools (Send to Unreal + UE to Rigify)

Upstream: `EpicGames/BlenderTools` (mirrored identically at `EpicGamesExt/BlenderTools` — same HEAD `04cae45d`), depth-1 pull 2026-10-23, send2ue v2.4.3.
License: **MIT ✅ own-eyes verified on `LICENSE.md` in this tree** (Copyright (c) 2020–2024 Epic Games, Inc. — standard MIT grant: use, copy, modify, merge, publish, distribute, sublicense, sell). Free + commercial OK. Trimmed at pull: upstream `.github/` CI, `tests/test_files/` (23MB .blend/.fbx/.uproject fixtures, re-downloadable), doc GIFs (35MB) — code-only 6.9MB. One upstream-only `SyntaxWarning` in `send2ue/dependencies/rpc/factory.py:116` (invalid escape sequence) — warning only, untouched.

## What it is
The official Epic pipeline pair between Blender and Unreal Engine:
1. **Send to Unreal** (`send2ue/`) — one-click export of rigged, textured, animated meshes from Blender into UE via FBX + an RPC link (the addon talks to a "Send to Unreal" Unreal plugin / remote execution). Handles export presets, collision, sockets, LODs, groom, morph targets, animation sequences, extensions (combine assets, instance assets, collections-as-folders).
2. **UE to Rigify** (`ue2rigify/`) — node-based retargeting system for Blender's built-in Rigify addon: converts UE marketplace skeletons (Manny/Quinn mannequins etc.) into Rigify rigs so new animation can be authored in Blender and sent back.

This is the natural complement to the UE4SS + UAssetAPI + FModel trio (cape-jones PR #210): UE4SS/FModel/UAssetAPI tear Unreal games apart and read assets; BlenderTools moves assets back and forth between Blender and Unreal.

## Slot in the show/game pipeline
- Western Heart character work → export rigged fighters from Blender to UE5 for the interactive game runtime (replaces ad-hoc FBX settings; presets are shareable `.py` export pipelines in `send2ue/core/`).
- Rigify retarget: take a UE skeleton (or our chimera-built UE-compatible rig), convert to Rigify, animate in Blender with our existing rig tooling, re-export.
- Headless batch: the `core/export.py` + RPC path can be driven from Blender background scripts for farm export of animation banks.

## Install
- Blender: Edit → Preferences → Add-ons → Install from Disk → zip the `send2ue/` folder (same for `ue2rigify/`). Requires Blender ≥ the version in `bl_info` (send2ue 2.4.3). Rigify ships with Blender — enable it for UE to Rigify.
- Unreal side: install the matching "Send to Unreal" plugin in UE4/UE5 (marketplace / upstream releases page) so the RPC link has something to talk to; enable remote execution.
- Headless use: `scripts/` has dev helpers (`dev_helpers.py`, `addon_watcher.py`); `send2ue/core/export.py` is the programmatic export path.

## Show-pipeline uses
- Cape Jones / Western Heart fighters: Blender-authored attires + anims → UE5 runtime with one click, consistent scale/axis presets instead of per-artist FBX roulette.
- Animation reuse: import a UE mannequin anim set via UE to Rigify → retarget to our Rigify rigs → bake → ship as animation-bank rows.
- Rapid iteration: change pose in Blender, hit Send, test in-engine — the tight loop the Unreal lanes need.

## Caveats (documented, not invented)
- Community reports (BlenderArtists 2020, Unreal forums) note it wraps Blender's FBX exporter — scale/axis discipline matters (Blender 0.01 unit scale for UE). Use the addon's project settings, don't fight them by hand.
- Export paths with Physics/Skeletal asset file paths had known issues in 2.2.1/2.3.0 (upstream issue #564, workaround in repo issues) — pin versions per project.
- No test fixtures in this tree (`tests/test_files/` trimmed) — pull upstream depth-1 again if you need the `.blend`/`.fbx` fixtures.

## Verify
`python3 -m py_compile` clean over `send2ue/ ue2rigify/ scripts/` (upstream-only SyntaxWarning noted above). No binaries >50MB, no weights, no `.env`.
