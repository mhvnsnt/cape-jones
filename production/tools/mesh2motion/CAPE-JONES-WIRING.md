# Mesh2Motion — Cape Jones Wiring (CC0 animation library)

**What:** Mesh2Motion is the open-source Mixamo alternative: browser-based
auto-rig + a library of **170+ animations, all CC0** (public domain —
personal AND commercial use, no attribution, remix freely). Every animation
ships with its **Blender source .blend** (rig + action), so the library is
editable, extendable, and retargetable inside our pipeline.

**Source:** https://github.com/Mesh2Motion/mesh2motion-app (app, MIT) ·
https://github.com/Mesh2Motion/mesh2motion-assets (assets, CC0) ·
https://mesh2motion.org
**License:** Code MIT; **all art assets (models, rigs, animations) CC0** —
verified from the repo's Licenses section: "Free for personal or commercial
use. Licensed under CC0."
**Vendored:** `glb/` — the COMPLETE human animation library as import-ready
GLB (see below), pulled 2026-10-18 from `Mesh2Motion/mesh2motion-app` main.
Full 170+ library (all rigs) stays upstream; the download recipe below fetches
any of it.

## Why GLB, not the .blend sources

The `mesh2motion-assets` repo ships each animation as a Blender `.blend`
— but those are saved in a **newer .blend format our Blender 4.0.2 cannot
read** (verified: `Failed to read blend file, not a blend file`). The
`mesh2motion-app` repo ships the same library as **GLB**, which imports
natively into Blender 4.0.2. GLB is the correct vendored format for this
pipeline.

## Smoke test (own eyes, headless Blender 4.0.2, 2026-10-18)

`human-base-animations.glb` → `bpy.ops.import_scene.gltf()`:
- **87 animation actions** imported (`Chest_Open`, `Dance_Simple`,
  `Crouch_Idle`, …) on a **66-bone** armature. Import completes in ~15 s.
- Known quirk: the glTF importer logs `F-Curve ... already exists` warnings
  for a few actions (duplicate channels in the source file) — it continues
  and finishes; the actions are usable.

## Why this fills the gap

Our animation sourcing is currently afk-rig's 240 CC0 clips + Mixamo (Adobe ID,
browser, commercial-terms check). Mesh2Motion adds a **second fully-open,
no-account, CC0 library** whose killer feature for us is the **Blender source
files**: each animation is a .blend containing the rig and the action, so we
can open it, study it, fix it, and retarget it — no black-box FBX.

## The curated set (why these 20)

Picked for a comedic superhero (Cape Jones) — locomotion, acting, and
superhero-specific moves:

| File | Use |
|---|---|
| `glb/human-base-animations.glb` (5.6 MB, **87 actions**) | core set: locomotion, acting, comedy, dances |
| `glb/human-addon-animations.glb` (5.3 MB) | addon set: more attacks, gestures, emotes |
| `glb/human-mocap-animations.glb` (2.0 MB) | mocap set |
| `glb/rig-human.glb` (21 KB) | the authoring rig (retarget SOURCE) |

## Retargeting onto the Cape Jones rig

Each .blend contains the Mesh2Motion human rig with the action on it.
Retarget path (no new tools needed):

1. Open the animation .blend, note the source rig's bone names.
2. In the Cape Jones scene: import the source rig + action, build a bone map
   (source → CapeJones_Rig), then bake the action onto our rig with
   `bpy.ops.nla.bake()` (visual keying, only the mapped bones).
3. Our retargeting stack (Rokoko plugin / Blender 5 slotted actions when we
   upgrade) applies the same map; the bone-map JSON should be saved per
   animation so the set stays re-usable.

The Mesh2Motion app itself (https://mesh2motion.org) can also auto-fit its
skeleton to an uploaded model in the browser — useful for quick previews
before committing to a retarget.

## Fetching more from the upstream library

```bash
# any animation from the 170+ set:
curl -sL -o animation-human-<name>.blend \
  "https://raw.githubusercontent.com/Mesh2Motion/mesh2motion-assets/main/rigs/human/animation-human-<name>.blend"
# other rigs: rigs/{bird,dragon,fox,horse,kaiju,shark,snake}/  +  rig-<x>.blend
# CC0 character packs: CC0-packs/{Kaykit,Quaternius,psx-lowpoly}/
```

Full animation list: `https://github.com/Mesh2Motion/mesh2motion-assets/tree/main/rigs/human`
(80 human animations at last count; 170+ across all rigs).

## License & provenance

- Assets: CC0 1.0 Universal — public domain. No attribution required.
  Commercial use explicitly allowed ("Free for personal or commercial use").
- Upstream: https://github.com/Mesh2Motion/mesh2motion-assets · Scott Petrovic.
- Note: some human animations derive from Quaternius (also CC0) — same terms.
