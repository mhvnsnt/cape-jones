# UE4SS — Cape Jones Wiring

**Upstream:** https://github.com/UE4SS-RE/RE-UE4SS (branch `main` @ 2026-10-23 pull)
**What:** Injectable Lua/C++ scripting system, SDK generator, live property editor, and
dumping utilities for Unreal Engine 4/5 games (shipped games, no source access needed).
**License:** MIT (own-eyes on `LICENSE` in this tree: "MIT License, Copyright (c) 2022 Narknon").
Free + commercial use OK.
**Pull:** code-only, 27MB, ~1018 files, 0 binaries >50MB. Upstream `.github/` stripped per
repo convention (CI only). PR: unreal tooling lane, overnight pipeline 2026-10-23.

## Why it's here (show-pipeline slot)

This repo tears down games. UE4SS is the standard open tool for introspecting Unreal Engine
titles at runtime: dump object graphs, generate SDK headers, hook UFunctions, drive live
property edits, and prototype gameplay logic in Lua without rebuilding the game. For the
operation it fills the **Unreal-game teardown/modding slot** alongside:

- `production/tools/uassetapi/` — offline read/write of UE `.uasset`/`.pak` assets (MIT)
- `production/tools/fmodel/` — browse/export UE archives, find the asset before you touch the game (GPL-3.0)
- UnrealEngine repo + M-Engine `tools/unreal-worker/` — engine-side automation

## Build notes (honest)

This tree is a `--depth 1` snapshot WITHOUT submodules. To build from source, clone fresh
from upstream with submodules:

```bash
git clone --recursive https://github.com/UE4SS-RE/RE-UE4SS.git
cd RE-UE4SS
git submodule update --init --recursive
```

- `deps/first/Unreal` and `deps/first/patternsleuth` are EMPTY here (submodule dirs not
  fetched). `deps/first/Unreal` needs an Epic Games account linked to GitHub + accepted
  @EpicGames org invite for Unreal source access (upstream README requirement).
- Build systems: CMake (`CMakeLists.txt`) and xmake (`xmake.lua`). Windows MSVC is the
  primary target; Linux builds are community-supported — check upstream docs first.
- For USE (not build): grab the prebuilt release ZIP from upstream Releases and drop the
  `UE4SS/` folder next to the game's executable. Nothing in this tree needs to be on disk
  for that path.

## Quick map of this tree

- `UE4SS/` — core: injection, Lua scripting runtime, SDK generator, live property editor
- `cppmods/` — C++ mod examples/templates
- `UVTD/` — Unreal virtual table dumper utilities
- `tools/` — helper tools
- `docs/` — upstream docs (full manual at https://docs.ue4ss.com)
- `assets/` — branding assets

## Show-pipeline uses

1. **UE teardown recon:** inject into a shipped UE title, dump the object/UFunction list,
   generate the SDK — the fastest way to learn a game's internals before writing an
   extractor.
2. **Live staging:** live property editor to pose/tweak actors in a running game for
   reference captures (staging, lighting, camera) without a rebuild loop.
3. **Mod prototyping:** Lua mods to test gameplay/character behavior ideas before
   committing to engine-side work.
4. **Companion to FModel/UAssetAPI:** FModel finds the asset in the pak, UAssetAPI
   reads/writes it offline, UE4SS observes and drives it live. The three cover the full
   loop.

## License record

- Upstream `LICENSE`: MIT License, Copyright (c) 2022 Narknon — verified in-tree 2026-10-23.
- No copyleft obligations on our side; attribution preserved in this tree.
