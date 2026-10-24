#!/usr/bin/env python3
"""Bake the v3 idle cape (bone-parented pins, frames 0-96)."""
import bpy, time

SRC = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_v3.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_v3_baked.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
cape = bpy.data.objects["CapeJones_Cape"]
cloth = next(m for m in cape.modifiers if m.type == "CLOTH")
pc = cloth.point_cache
print(f"v3 bake: cape parent={cape.parent.name if cape.parent else None} bone={cape.parent_bone}", flush=True)
sc = bpy.context.scene
bpy.ops.ptcache.free_bake_all()
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
print(f"v3 bake took {time.time() - t0:.1f}s; is_baked={pc.is_baked}", flush=True)
assert pc.is_baked, "bake did not complete"
sc.frame_set(48)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
print("V3 BAKE DONE", flush=True)
