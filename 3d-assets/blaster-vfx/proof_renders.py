"""Render the proof set from the built blaster_fx.blend (no rebuild).

Usage: blender -b blaster_fx.blend --python proof_renders.py
Renders into 3d-assets/blaster-vfx/proof/:
  - blaster_charge_proof.png (charge=1, fire=0, energy_beam)
  - blaster_fire_proof.png   (charge=1, fire=1, energy_beam)
  - blaster_bolt_proof.png   (fx_type=1 gauntlet_bolt)
  - blaster_pulse_proof.png  (fx_type=2 wave_pulse)
  - blaster_arc_proof.png    (fx_type=3 arc_chain)
  - blaster_scene_tint_proof.png (per-scene tint: cyan blast, core stays white)
"""
import bpy
import os

proof_dir = os.path.join(os.path.dirname(bpy.data.filepath), "proof")
drv = bpy.data.objects["CJ_BlasterDriver"]
sc = bpy.context.scene

AMBER = (1.0, 0.70196, 0.0)

proofs = [
    ("blaster_charge_proof.png", 1.0, 0.0, 0, AMBER),
    ("blaster_fire_proof.png", 1.0, 1.0, 0, AMBER),
    ("blaster_bolt_proof.png", 1.0, 1.0, 1, AMBER),
    ("blaster_pulse_proof.png", 0.6, 1.0, 2, AMBER),
    ("blaster_arc_proof.png", 1.0, 0.6, 3, AMBER),
    # canon check: per-scene tint recolors glow + blast lighting, core stays white
    ("blaster_scene_tint_proof.png", 1.0, 1.0, 0, (0.2, 0.9, 1.0)),
]

for name, charge, fire, fx, tint in proofs:
    drv["charge"] = charge
    drv["fire"] = fire
    if "fx_type" in drv:
        drv["fx_type"] = fx
        drv["tint_r"], drv["tint_g"], drv["tint_b"] = tint
    bpy.context.view_layer.update()
    sc.render.filepath = os.path.join(proof_dir, name)
    bpy.ops.render.render(write_still=True)
    print("PROOF-RENDERED:", sc.render.filepath)
