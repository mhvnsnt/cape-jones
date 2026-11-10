#!/usr/bin/env python3
"""Proxy cloth bake setup: decimated cape (~6.5k verts) BEFORE cloth.
Full-res (82k) cloth OOM-kills this VM at solver init; the mini test proved
a ~5k proxy bakes fine (10f in 72s). The full cape will follow the baked
proxy via Surface Deform for proof renders (standard proxy workflow).
"""
import bpy

SRC = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_slim.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_proxy.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
cape = bpy.data.objects["CapeJones_Cape"]
for m in list(cape.modifiers):
    if m.type == "CLOTH":
        cape.modifiers.remove(m)
dec = cape.modifiers.new("Decimate", "DECIMATE")
# 0.05 (~4.1k sim verts), quality 5: the 0.08/q8 bake died at frame 50
# (system-wide memory pressure, silent SIGKILL). Lighter = finishes.
dec.ratio = 0.05
print(f"proxy base verts={len(cape.data.vertices)} (decimate 0.05 -> ~4.1k sim verts)", flush=True)
cloth = cape.modifiers.new("Cloth", "CLOTH")
cs = cloth.settings
cs.quality = 5
cs.mass = 0.35
cs.tension_stiffness = 15.0
cs.compression_stiffness = 15.0
cs.shear_stiffness = 8.0
cs.bending_stiffness = 0.8
cs.tension_damping = 5.0
cs.compression_damping = 5.0
cs.shear_damping = 5.0
cs.bending_damping = 0.5
cs.air_damping = 1.0
cs.vertex_group_mass = "cape_pin"
try:
    cs.pin_stiffness = 1.0
except Exception:
    pass
col = cloth.collision_settings
col.use_collision = True
col.collision_quality = 3
col.distance_min = 0.010
col.use_self_collision = True
col.self_distance_min = 0.006
pc = cloth.point_cache
pc.frame_start, pc.frame_end = 0, 96
pc.use_disk_cache = True
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 0, 96
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED PROXY", OUT, flush=True)
