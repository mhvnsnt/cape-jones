# FModel — Cape Jones Wiring

**Upstream:** https://github.com/4sval/FModel (branch `dev` @ 2026-10-23 pull, 3280★, active)
**What:** Unreal Engine archives explorer — browse `.pak`/`.utoc`/`.ucas` archives, preview
assets, and export them (models, textures, audio, animations) from shipped UE games.
**License:** GNU GPL-3.0 (own-eyes on `LICENSE` in this tree). Free + commercial use OK as a
tool; copyleft applies only if we modified and distributed FModel itself — we run it, we
don't embed it.
**Pull:** code-only, 5.6MB, 411 files, 0 binaries >50MB. Upstream `.github/` stripped per
repo convention (CI only). PR: unreal tooling lane, overnight pipeline 2026-10-23.

## Why it's here (show-pipeline slot)

Fills the **find-and-export slot** in the Unreal teardown trio:

- `production/tools/fmodel/` — THIS: browse the pak, FIND the asset, export it (GPL-3.0)
- `production/tools/uassetapi/` — parse/rewrite the exported asset offline (MIT)
- `production/tools/ue4ss/` — inject into the running game, observe/drive assets live (MIT)

Before this pull, a lane facing a UE game's pak had no in-repo tooling; now the full
find → parse → drive loop is covered.

## Quick map of this tree

- `FModel/` — the WPF application (Windows-first; needs .NET to build)
- `CUE4Parse/` — vendored UE parsing library (pak/utoc/ucas, asset serialization, AES);
  this is the reusable core — usable as a library independent of the GUI
- `NOTICE`, `README.md` — upstream notes

## Build / use

Requires the .NET SDK (check `FModel/FModel.csproj` for the target framework):

```bash
cd production/tools/fmodel
dotnet build FModel/FModel.csproj
```

Runtime use: point FModel at a game's pak directory (+ AES key when the game encrypts its
paks — keys come from the game's own research/teardown lanes, never committed), browse the
asset tree, export skeletal meshes/textures/animations for the chimera pipeline. CUE4Parse
can also be referenced as a library from our own C# tooling.

Note: FModel is Windows/WPF-first. On this Linux VM the GUI won't run; the value here is
the source (CUE4Parse especially) plus documented Windows-side use for lanes with Windows
access. No prebuilt binaries are committed — build from this source.

## Show-pipeline uses

1. **UE teardown recon:** enumerate a shipped UE title's full asset manifest before writing
   a single extractor — know what characters, stages, and animations exist.
2. **Asset export:** pull skeletal meshes + textures for chimera reskin lanes
   (Bannon/Western Heart character work).
3. **AES-key workflow:** with a game's pak key (from teardown research), unlock the full
   archive for browsing — the standard first step of any UE teardown.

## License record

- Upstream `LICENSE`: GNU General Public License v3 — verified in-tree 2026-10-23.
- Same pattern as the repo's other GPL-3.0 tools (Glaxnimate, Flowblade): tool-use is fine;
  only modified redistribution would trigger copyleft, which we don't do.
