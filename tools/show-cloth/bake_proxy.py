#!/usr/bin/env python3
"""Bake the proxy cape (frames 0-96). Slim scene, no body mesh."""
import bpy, time

SRC = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_proxy.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_proxy_baked.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
cape = bpy.data.objects["CapeJones_Cape"]
cloth = next(m for m in cape.modifiers if m.type == "CLOTH")
pc = cloth.point_cache
print(f"proxy bake: base verts={len(cape.data.vertices)} frames 0-96", flush=True)
sc = bpy.context.scene
bpy.ops.ptcache.free_bake_all()
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
print(f"proxy bake took {time.time() - t0:.1f}s; is_baked={pc.is_baked}", flush=True)
assert pc.is_baked, "bake did not complete"
sc.frame_set(48)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
print("PROXY BAKE DONE", flush=True)
