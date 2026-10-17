"""Render the proof set from the built blaster_fx.blend (no rebuild).

Usage: blender -b blaster_fx.blend --python proof_renders.py
Renders into 3d-assets/blaster-vfx/proof/:
  - blaster_charge_proof.png (charge=1, fire=0)
  - blaster_fire_proof.png  (charge=1, fire=1)  [already rendered by build script]
"""
import bpy
import os

proof_dir = os.path.join(os.path.dirname(bpy.data.filepath), "proof")
drv = bpy.data.objects["CJ_BlasterDriver"]
sc = bpy.context.scene

for name, charge, fire in (("blaster_charge_proof.png", 1.0, 0.0),
                           ("blaster_fire_proof.png", 1.0, 1.0)):
    drv["charge"] = charge
    drv["fire"] = fire
    bpy.context.view_layer.update()
    sc.render.filepath = os.path.join(proof_dir, name)
    bpy.ops.render.render(write_still=True)
    print("PROOF-RENDERED:", sc.render.filepath)
