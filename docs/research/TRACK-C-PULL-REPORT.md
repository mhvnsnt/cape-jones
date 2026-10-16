# TRACK C PULL REPORT — 3D Assets + Game Dev Overlap + Comic/Manga
**Date:** 2026-10-16 | **Track:** C (MEGA PULL) | **Agent:** subagent session 775d0083

**Disk:** 81% (79G/100G) before → 81% (79G/100G) after. ~112MB added (small packs only, per constraint).
**Already-have check:** did NOT re-pull Quaternius interior/furniture, Kenney furniture/suburban/roads kits, living_room.blend, tripo-pull.py, Godot 4.7.2, Tiled, Blender 4.0.2 + GP addons, Cascadeur.

---

## 1. 3D ASSETS — PULLED (local)

| Pack | Source URL | License | Contents | Size | Local path |
|------|-----------|---------|----------|------|------------|
| Kenney Nature Kit | https://kenney.nl/assets/nature-kit | **CC0 1.0** | 329 GLB models (+FBX/OBJ): trees, rocks, plants, bushes, bridges (stone/wood), flowers — ATHF-style outdoor dressing | 10.5MB zip, ~50MB extracted | `~/workspace/cape-jones-build/3d-assets/kenney-extra/nature-kit/` |
| Kenney Car Kit | https://kenney.nl/assets/car-kit | **CC0 1.0** | 50 GLB models: cars, ambulance, vans, traffic cones, crash-debris parts (doors, bumpers, bolts) — good for cartoon crash gags | 4.8MB zip, ~15MB extracted | `~/workspace/cape-jones-build/3d-assets/kenney-extra/car-kit/` |
| KayKit Halloween Bits 1.0 | https://github.com/KayKit-Game-Assets (user acct, not org) / https://kaykit.co | **CC0 1.0** | 63 models (glTF + OBJ + MTL): pumpkins, jack-o'-lanterns, ghosts, witches, candy, spooky props — ghost-cave / gag dressing | 1.15MB zip, ~4.9MB extracted | `~/workspace/cape-jones-build/3d-assets/kaykit/` |
| ambientCG additions | https://ambientcg.com (get?file=ID_1K-JPG.zip) | **CC0 1.0** | 2 PBR texture sets @1K JPG: **Grass004** (lawn/ground), **Wood062** (floor/planks). 7 maps each (albedo, normal, roughness, AO…) | 21MB zips | `~/workspace/cape-jones-build/3d-assets/ambientcg-additions/` |

**Note:** 4 other ambientCG texture IDs tried (Plaster001C, Tile057A, Asphalt039C, Roofing047C) returned error pages — IDs don't exist on current site. Valid IDs verified with `unzip -t`. Wall/interior plaster + asphalt still gaps.

## 1b. 3D ASSETS — DOCUMENTED ONLY (not pulled, with reason)

| Source | URL | License | What's there | Why documented-only |
|--------|-----|---------|--------------|---------------------|
| OpenGameArt CC0 picks | https://opengameart.org/content/low-poly-rpg-level-models etc. | CC0 | "LowPoly House Interior Pack" (quaternius, 120+ models, 12.8MB, FBX/OBJ/Blend — interior doors/kitchen/bath); "Low Poly RPG Pack" (100+ props/weapons, 44.6MB); "LOW POLY 3D MODEL PACKS" (byzmod3d chars); "Fox Trees Pack" (9 trees); "LowPoly Glasses Pack" (29 props); "3D Low-Poly RPG Level Models" (village structures) | Downloads require free OGA login — needs live browser session |
| itch.io CC0 picks | https://lightning-poly.itch.io/low-poly-battle-pack (CC0 vehicles/weapons/env); https://plewr.itch.io/mauser-c96-low-poly (CC0 .blend+.glb, 1.7MB); tag pages https://itch.io/game-assets/tag-low-poly/tag-rigged ("8 free CC0 rigged+animated characters GLB", "10 free CC0 rigged+animated animals GLB", "11 PSX-style rigged characters"); "Models for the living room" (~10 living-room models) | CC0 | Battle pack, weapons, living-room models, rigged+animated characters/animals | Per-file downloads need browser session; rigged characters especially worth a browser pull later |
| Poly Haven | https://polyhaven.org | **CC0** | HDRIs, PBR textures, models — direct download, no account | Overlaps ambientCG (already have 8 sets); flagged for next pull if interior-wall textures needed |
| BlendSwap | https://blendswap.com | CC0/CC-BY (per model) | Large .blend model library | Needs free signup — browser task later |
| Sketchfab | https://sketchfab.com (CC0 filter) | CC0 (filterable) | Downloadable models incl. CC0 | Needs free signup — browser task later |
| Free3D | https://free3d.com | Mixed/"personal use" on many | Free 3D models | **SKIPPED — license murky** (many models personal-use only, not redistribution-safe) |
| Quaternius remaining packs | https://quaternius.com/packs.html | **QAL v1.0 (NOT CC0 anymore)** | Dozens of themed packs (characters, animations, environments) | **FLAGGED:** license changed from CC0 → QAL v1.0: commercial *games* OK, but **no standalone asset redistribution**. A cartoon show uses renders (end-product), likely fine, but needs owner call before shipping any Quaternius-derived content |
| Kenney character-kit | https://kenney.nl/assets/character-kit | CC0 (if exists) | Modular low-poly characters (NPCs) | **Slug 404s as of 2026-10-16** — pack renamed or removed from kenney.nl; flagged for re-check |

---

## 2. GAME DEV OVERLAP — TOOLS

| Tool | URL | Local path / status | What / why | License |
|------|-----|---------------------|------------|---------|
| **TIC-80 v1.3.1** | https://github.com/nesbox/TIC-80/releases/tag/v1.3.1 | **PULLED + VERIFIED** → `~/workspace/tools/game-dev-overlap/tic80/tic80` (`--version` → `1.3.1 (62c24e5)`), 5.9MB zip / 15MB binary | Free fantasy console for retro 2D effects: 240×136, 16 colors, built-in sprite/map/sfx/music editors. PICO-8 alternative | MIT |
| LibreSprite | https://libresprite.github.io / https://github.com/LibreSprite/LibreSprite | Documented only (source build too heavy for VM; on Flathub + distro repos) | Free Aseprite fork (last GPLv2 codebase) — pixel art + animation | GPL-2.0 |
| Pixelorama | https://orama-interactive.itch.io/pixelorama / https://github.com/Orama-Interactive/Pixelorama | Documented only (AppImage on GitHub releases) | Godot-based pixel-art/animation editor, most actively developed free option | MIT |
| Piskel | https://www.piskelapp.com | Documented only (web app) | Simple web pixel-art + sprite animation, no install | Open source |
| PixiEditor | https://pixieditor.net | Documented only | Layer-based pixel-art editor | GPL |
| free-tex-packer | https://github.com/odrick/free-tex-packer / web app https://free-tex-packer.com/app | Documented only | Sprite-sheet packer: rotation/trimming/multipack, exports json/xml/css/pixi.js/**godot**/phaser/cocos2d, built-in **split-sheet tool**. CLI: free-tex-packer-cli | Open source (maintainer: critical-bug-fixes only) |
| open-texture-packer | https://github.com/webcyou-org/open-texture-packer | Documented only (`cargo install open_texture_packer`) | Rust texture packer, shelf/next-fit/etc algorithms, CSS+JSON+PNG output | Open source |
| Alferd Spritesheet Unpacker | https://github.com/ForkandBeard/Alferd-Spritesheet-Unpacker/releases | Documented only (Windows .NET, v19) | Grid/multi-select sprite-sheet splitter, transparency handling | Open source |
| TextureUnpacker (Node) | https://github.com/topics/texture-packer | Documented only | Unpacks TexturePacker-packed sheets to sprites (updated 2026-03) | Open source |
| Effekseer | https://effekseer.github.io/en/ / https://github.com/effekseer/Effekseer | Documented only | 2D/3D particle effect editor + runtimes (Godot/Unity/Unreal/Cocos). Standard free particle tool | Open source |
| DragonBones | https://github.com/DragonBones/ | Documented only (editor free, runtimes on GitHub) | 2D skeletal animation (Spine alternative). Editor free-but-closed; **runtimes open source** | Open source runtimes |
| Spine runtimes | https://esotericsoftware.com | **FLAGGED** | Runtimes are open source BUT EULA requires a Spine license ($69–299) to legally use them to render/distribute | Paid — do NOT use without license |
| Spriter / SCML | https://brashmonkey.com | Documented only | 2D skeletal animation, free version + $60 Pro, open SCML runtimes | Free/paid |
| Tiled (status check) | https://thorbjorn.itch.io/tiled/devlog | Have it already — **latest is 1.12.2 (May 2026)**; 1.12 adds rewritten Properties view, list-valued custom properties, oblique map orientation, layer blending modes, capsule objects; 1.11.1 added Aseprite image loading | Worth upgrading installed copy | BSD-2 |
| LIKO-12 | https://github.com/LIKO-12/LIKO-12 | Documented only | Open-source fantasy console (LÖVE2D/Lua), code/sprite/map editors | Open source |
| Pixel Vision 8 | (itch.io / GitHub) | Documented only | Open-source fantasy console, C#/Lua | Open source |
| WASM-4 | https://wasm4.org | Documented only | Open-source fantasy console, WebAssembly carts | Open source |
| LowRes NX | (GitHub, RetroArch core) | Documented only | Open-source BASIC fantasy console, authentic retro effects | Open source |
| Pyxel | https://github.com/kitao/pyxel (`pip install pyxel`) | Documented only | Python retro game engine, MIT — good for quick retro effect prototyping | MIT |

---

## 3. COMIC / MANGA

### 3a. Pulled — open-license comic lettering fonts (OFL, commercial-safe)
Path: `~/workspace/tools/comic-manga/fonts/` (~6MB total, all verified TrueType via `file`)

| Font | Role |
|------|------|
| Bangers-Regular.ttf (93KB) | Titles, hero names, SFX — classic comic display |
| ComicNeue-Regular.ttf (57KB) | Dialogue body text (clean, no Comic Sans amateur vibe) |
| LuckiestGuy-Regular.ttf (58KB) | Retro 1950s covers, bold titles |
| PermanentMarker-Regular.ttf (73KB) | Zine/gritty indie style |
| ZenMaruGothic-Regular.ttf (3.8MB) | Manga-flavored Japanese-capable rounded gothic |
| DotGothic16-Regular.ttf (2MB) | Pixel/dot-matrix manga SFX flavor |

### 3b. Documented only
| Tool | URL | What / why | License |
|------|-----|------------|---------|
| Storyboarder (Wonder Unit) | https://wonderunit.com/storyboarder/ | Open-source storyboard/panel-layout tool — board episodes, export panels | Open source |
| Krita 5.3+ comic tools | https://krita.org | **Built-in comic panel tool + speech-bubble/text tools** (David Revoy's "Comic strip from A to Z with Krita" tutorial) — panel layout + lettering in one free app | GPL |
| Kumiko panel extractor | https://github.com/avan06/KumikoMangaPanelExtractor (kumikolib by njean42) | Auto-detect + crop comic panels from pages — useful to slice reference/webtoon pages | Open source |
| Screentone / halftone | Krita: built-in halftone filter; GIMP: Newsprint plugin; David Revoy Krita brush packs (pepper&carrot) | Manga screentone + effect brushes | CC-BY (Revoy brushes) |
| Blambot free fonts (Anime Ace, BadaBoom BB) | https://blambot.com | Industry-standard comic fonts | **SKIPPED — freeware for non-commercial/indie ONLY** (per track rules: NC = skip) |
| Webtoon vertical-scroll | Webtoon Canvas platform; Krita vertical-scroll page templates | Vertical-scroll comic formatting | Documented only |

---

## Open items / follow-ups for parent
1. **Browser pulls needed:** OpenGameArt CC0 interior pack (quaternius 120+ models, needs free login), itch.io CC0 rigged+animated characters/animals GLBs, BlendSwap/Sketchfab CC0 (signups).
2. **License flag:** Quaternius is QAL v1.0 now, not CC0 — needs owner's call before any Quaternius content ships in the show.
3. **Spine runtimes:** open source but require paid Spine license — excluded; DragonBones/Spriter are the free skeletal-animation path.
4. **Kenney character-kit:** 404 on kenney.nl as of today — re-check slug later.
5. **ambientCG gaps:** wall plaster + asphalt/road texture IDs need re-discovery on the current site.
