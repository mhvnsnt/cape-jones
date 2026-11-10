# BlenRig 6 — Cape Jones wiring

**What:** BlenRig 6 v4.0.1 (Blender 4.x branch), free + open source (GPL-3.0, commercial use allowed).
Film-quality auto-rigging + skinning system for bipeds: guided rig creation, mesh-deform
muscle system, weight-painting guides, and a full facial rig. Used on Blender open movies
and studio shorts. Upstream: https://github.com/jpbouza/BlenRig (`master_blender4` branch).

**Why here:** the REV3 big task is "rig + animate the Cape Jones model full-stack"
(skinning/meshing, correct stretch/no-stretch weight zones). BlenRig 6 is the strongest
FREE option in the Oct-2026 rigging roundups — full body AND face rig at zero cost,
with deformation quality a step above default Rigify. Additive tooling: it does not
replace the live rig lane's work, it gives that lane a production-grade rigging system.

**Verified this lane (2026-10-16, own-eyes):**
- 99/99 `.py` files pass `python3 -m py_compile`.
- Headless install+enable on local Blender 4.0.2 (`xvfb-run`): `ADDON_ENABLE_OK`, `ENABLED: (True, True)`.

## Install (Blender 4.x, headless or GUI)

Headless (Kaggle/Colab/VM):
```bash
cd <repo>/production/tools
zip -qr /tmp/blenrig6.zip blenrig6
blender -b --python-expr "
import bpy
bpy.ops.preferences.addon_install(filepath='/tmp/blenrig6.zip')
bpy.ops.preferences.addon_enable(module='blenrig6')
"
```

GUI: Edit > Preferences > Add-ons > Install from Disk > pick the zip > enable "BlenRig 6".

## Rigging workflow (Cape Jones model)

1. Import the Cape Jones GLB (`3d-assets/cape-jones/cape-jones-3d.glb`, native 0.925 m — DO NOT rescale).
2. Add > Armature > BlenRig 6 biped guide; fit the guide bones to the mesh
   (Reproportion guide). Keep proportions at native scale.
3. Generate the rig; run the Binding/Skinning guides (mesh-deform cage + lattices
   give the muscle-like deformation; the guides walk through weight cleanup —
   the exact "correct stretch/no-stretch weight zones" work REV3 needs).
4. Face: BlenRig ships a full facial rig — use it for the dialogue/expression work
   instead of hand-building face bones.
5. Bake to DEF bones for export (see `blenderartists` thread notes in the research doc).

## Lane runbook

- BlenRig rigs are complex control rigs, not game skeletons: for any engine export,
  duplicate the DEF bones, add Copy Transforms constraints, bake visual transforms,
  export the baked armature + mesh.
- Blender 3.x is NOT supported by this branch — use Blender 4.0+.
- Docs live in-repo (`readme.rst`, `guides/`); upstream wiki:
  https://cloud.blender.org/p/blenrig/56966411c379cf44546120e8
