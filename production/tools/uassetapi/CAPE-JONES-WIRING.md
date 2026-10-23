# UAssetAPI — Cape Jones Wiring

**Upstream:** https://github.com/atenfyr/UAssetAPI (branch `master` @ 2026-10-23 pull, 512★, active)
**What:** Low-level .NET library for reading and writing Unreal Engine game assets
(`.uasset`/`.uexp`/`.umap`, versioned UE4/UE5 serialization).
**License:** MIT (own-eyes on `LICENSE` in this tree: "MIT License, Copyright (c) 2020 - 2026 atenfyr").
Free + commercial use OK.
**Pull:** code-only, 11MB, 1261 files, 0 binaries >50MB. Upstream `.github/` stripped per
repo convention (CI only). Test/benchmark fixture bulk trimmed: `UAssetAPI.Tests/TestAssets`
(181MB) and `UAssetAPI.Benchmark/TestAssets` (30MB) removed — fixture data, not code;
test and benchmark CODE kept, fixtures re-downloadable from upstream if needed. PR: unreal
tooling lane, overnight pipeline 2026-10-23.

## Why it's here (show-pipeline slot)

Fills the **offline UE asset read/write slot** in the Unreal teardown trio:

- `production/tools/fmodel/` — browse/export UE archives, FIND the asset (GPL-3.0)
- `production/tools/uassetapi/` — THIS: parse, inspect, and rewrite the asset offline (MIT)
- `production/tools/ue4ss/` — inject into the running game, observe/drive assets live (MIT)

## Quick map of this tree

- `UAssetAPI/` — the library (5.6MB): asset classes, serialization, Unreal version handling
- `UAssetAPI.Tests/` — test suite code (fixtures trimmed, see above)
- `UAssetAPI.Benchmark/` — benchmark harness code (fixtures trimmed)
- `UAssetAPI.sln` — solution file; `docs/` — upstream docs
- `NOTICE.md`, `README.md` — upstream notes

## Build / use

Requires the .NET SDK (upstream targets modern .NET; check `UAssetAPI/UAssetAPI.csproj` for
the exact TFM):

```bash
cd production/tools/uassetapi
dotnet build UAssetAPI.sln
dotnet test UAssetAPI.sln   # needs TestAssets/ re-fetched from upstream for full pass
```

Typical pipeline use: load a `.uasset` extracted from a pak (via FModel), walk its exports,
patch properties (materials, morph targets, skeleton references), write it back — all
without the engine. Pair with the repo's existing teardown extractors for UE-sourced
characters bound for Western Heart / Bannon chimera work.

## Show-pipeline uses

1. **UE character extraction:** read skeletal meshes, skeletons, and animation sequences
   out of shipped UE titles into our DCC tools (Blender) for chimera reskin work.
2. **Asset patching:** rewrite asset properties offline (e.g. retarget material slots,
   fix up import tables) before re-injection.
3. **Format research:** the versioned serialization code is the reference implementation
   for any lane writing its own UE asset reader.

## License record

- Upstream `LICENSE`: MIT License, Copyright (c) 2020 - 2026 atenfyr — verified in-tree 2026-10-23.
- No copyleft obligations; attribution preserved in this tree.
