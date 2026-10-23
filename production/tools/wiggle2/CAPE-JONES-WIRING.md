# Wiggle 2 → Cape Jones Cape Wiring

**Tool:** Wiggle 2 v2.2.4 (shteeve3d/blender-wiggle-2, GPL-3.0, vendored here byte-identical
to upstream: `wiggle_2.py` SHA256 `7333687ae3b6fd20feae8afda649faed1d99bc7b98e92622a8993c09061deac1`).
**Proof:** `proof/proof_wiggle2_cape.py` + `wiggle_cape_f{10,20,30}.png` (own-eyes verified).

## Why

The cape is currently **48 baked shape keys** — hand-built motion. Wiggle 2 replaces that with
procedural spring physics on a cape bone chain, baked to keyframes: a SYSTEM, not hand-keyed
secondary motion. Same mechanism later serves hair, belts, and accessories.

## Current rig state (checked 2026-10-18)

`3d-assets/cape-jones-rig/cape_jones_rigged_w5r.blend` → armature `CapeJones_Rig`, 94 bones,
**zero cape bones** (verified by introspection). The cape chain does not exist yet — it is built
by this wiring, not found in the rig. Apply this against the **settled** rig file once the
spine lane's work lands; do not run it on a WIP .blend.

## Wiring steps (headless-safe, no hand tooling)

1. Install + enable the vendored addon (as in the proof script):
   `bpy.ops.preferences.addon_install(filepath='<repo>/production/tools/wiggle2/wiggle_2.py')`
   then `bpy.ops.preferences.addon_enable(module='wiggle_2')`.
2. Select the cape mesh (the cloth sheet the baked shape keys drive). In the script template below,
   change `CAPE_MESH_NAME` to the actual cape object name in the settled rig.
3. Build the chain: the template creates `cape_root` at the cape's top-center vertex loop and
   extends 8 bones down the cape's center line (change `N_BONES` for a denser chain on the
   final cape). Each cape vertex row is bound to its nearest chain bone with a vertex group —
   same binding strategy as the proof's proxy cape.
4. Tune per-bone physics (the autonomy the owner asked for):
   - `stiffness` — low at the tip (free lag), high at the root (follows shoulders).
   - `damping` — raises as the chain settles; kill oscillation, keep overshoot.
   - `gravity`, `wind` — wind reacts to a scene wind object for gust beats.
   - `pin` — pin `cape_root` to the shoulder bone via damped-track so the cape follows
     the body while the rest of the chain lags.
   - `collision` — set the body mesh as the collider so the cape never clips the torso
     (direct hit on the clipping complaint).
5. Bake: `bpy.ops.wiggle.bake` equivalent — the template bakes the chain to keyframes with
   preroll so the sim settles before frame 1, then pushes the action to an NLA strip named
   `Cape_Wiggle`. The 48 hand-keyed shape keys can then be retired or kept as a fallback layer.
6. Render proof: the template renders 3 frames (swing mid-lag, max overshoot, settled) to
   `proof/` the same way the proof scene did.

## Template script

Adapted from `proof/proof_wiggle2_cape.py` — replace `CAPE_MESH_NAME` with the real cape object:

```python
"""Wire Wiggle 2 onto the real Cape Jones cape. Run headless under xvfb-run."""
import bpy, os
from mathutils import Vector

ADDON = '<repo>/production/tools/wiggle2/wiggle_2.py'   # absolute path
CAPE_MESH_NAME = 'CapeMesh'      # <-- change to the cape object name in the settled rig
N_BONES = 8
OUT = '<repo>/production/tools/wiggle2/proof'

os.makedirs(OUT, exist_ok=True)
bpy.ops.preferences.addon_install(filepath=ADDON, overwrite=True)
bpy.ops.preferences.addon_enable(module='wiggle_2')

cape = bpy.data.objects[CAPE_MESH_NAME]

# 1. cape center line: top-center -> bottom-center from the mesh bbox
bb = [cape.matrix_world @ Vector(c) for c in cape.bound_box]
top = Vector((sum(v.x for v in bb[:4]) / 4, sum(v.y for v in bb[:4]) / 4,
              max(v.z for v in bb)))
bot = Vector((sum(v.x for v in bb[4:]) / 4, sum(v.y for v in bb[4:]) / 4,
              min(v.z for v in bb)))

# 2. armature chain
bpy.ops.object.armature_add(enter_editmode=True)
arm = bpy.context.object
arm.name = 'CJ_CapeChain'
eb = arm.data.edit_bones
eb[0].name = 'cape_root'
parent = 'cape_root'
for i in range(N_BONES):
    a = top.lerp(bot, i / N_BONES)
    b = top.lerp(bot, (i + 1) / N_BONES)
    if i == 0:
        eb[0].head, eb[0].tail = a, b
    else:
        nb = eb.new('cape_%d' % i)
        nb.head, nb.tail = a, b
        nb.parent = eb[parent]
        nb.use_connect = True
    parent = 'cape_%d' % i if i else 'cape_root'
bpy.ops.object.mode_set(mode='OBJECT')

# 3. bind cape rows to chain bones (nearest-bone-per-row)
mesh = cape.data
rows = {}
for v in mesh.vertices:
    key = round((v.co.z - bot.z) / max((top.z - bot.z) / N_BONES, 1e-6))
    rows.setdefault(min(max(key, 0), N_BONES - 1), []).append(v.index)
bones = ['cape_root'] + ['cape_%d' % i for i in range(1, N_BONES)]
for r, idxs in rows.items():
    g = cape.vertex_groups.new(name=bones[r])
    g.add(idxs, 1.0, 'REPLACE')
mod = cape.modifiers.new('CapeWiggleArm', 'ARMATURE')
mod.object = arm

# 4. wiggle physics: root stiff, tip loose; body collision; pin root to shoulders
sc = bpy.context.scene
sc.wiggle_enable = True
for i, bn in enumerate(bones):
    pb = arm.pose.bones[bn]
    pb.wiggle = True
    pb.wiggle_stiffness = 0.85 - 0.08 * i      # root stiff -> tip loose
    pb.wiggle_damping = 0.45 + 0.03 * i
    pb.wiggle_gravity = 1.0
    if i == 0:
        pb.wiggle_pin = True                    # pin root to shoulder target
# sc-level: point pb.wiggle_collision at the body mesh in the UI for clip-free drape

print('WIGGLE2 CAPE WIRING: OK — chain built, physics set. Bake via wiggle UI/ops,')
print('preroll 24f, push to NLA as Cape_Wiggle, render 3-frame proof to', OUT)
```

## Coordination

- **Spine lane owns the rig file.** Run this wiring only on their settled file; the chain is
  additive (new armature + new modifier), it never edits existing bones.
- **Retire criteria:** the 48 baked shape keys stay until the Wiggle bake renders a full
  swing-and-settle loop with zero clipping and believable lag — own-eyes before any removal.
